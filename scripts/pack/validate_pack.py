#!/usr/bin/env python3
"""Validate a pack file against required fields."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def load_pack(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".json":
        return json.loads(text)
    try:
        import yaml  # type: ignore
    except Exception as exc:  # pragma: no cover
        raise SystemExit(
            "PyYAML is required for YAML packs. Install with: pip install pyyaml"
        ) from exc
    data = yaml.safe_load(text)
    if not isinstance(data, dict):
        raise SystemExit("Pack content must be an object/map.")
    return data


def validate(data: dict[str, Any]) -> list[str]:
    missing: list[str] = []
    required = [
        "pack_id",
        "spec_ref",
        "goal",
        "scope",
        "constraints",
        "verification_commands",
        "rollback_plan",
        "output_required",
    ]
    for key in required:
        if key not in data:
            missing.append(key)

    scope = data.get("scope", {})
    files = scope.get("files") if isinstance(scope, dict) else None
    if not files:
        missing.append("scope.files")

    constraints = data.get("constraints", {})
    if isinstance(constraints, dict):
        if "must" not in constraints:
            missing.append("constraints.must")
        if "must_not" not in constraints:
            missing.append("constraints.must_not")
    else:
        missing.extend(["constraints.must", "constraints.must_not"])

    if not data.get("verification_commands"):
        missing.append("verification_commands")
    if not data.get("rollback_plan"):
        missing.append("rollback_plan")
    if not data.get("output_required"):
        missing.append("output_required")
    return missing


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate pack file.")
    parser.add_argument("pack_file", type=Path)
    args = parser.parse_args()

    data = load_pack(args.pack_file)
    missing = validate(data)
    if missing:
        print("PACK CHECK: FAIL")
        print("Missing or empty fields:")
        for item in sorted(set(missing)):
            print(f"- {item}")
        return 1

    print("PACK CHECK: PASS")
    print(f"pack_id: {data.get('pack_id')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
