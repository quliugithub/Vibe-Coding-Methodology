#!/usr/bin/env python3
"""Fail if changed files are outside pack scope."""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path
from typing import Any


def load_yaml(path: Path) -> dict[str, Any]:
    try:
        import yaml  # type: ignore
    except Exception as exc:  # pragma: no cover
        raise SystemExit(
            "PyYAML is required for YAML packs. Install with: pip install pyyaml"
        ) from exc
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise SystemExit("Pack content must be an object/map.")
    return data


def get_changed_files(repo: Path) -> list[str]:
    cmd = ["git", "-C", str(repo), "diff", "--name-only", "--"]
    proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if proc.returncode != 0:
        raise SystemExit(proc.stderr.strip() or "git diff failed")
    out = [line.strip().replace("\\", "/") for line in proc.stdout.splitlines()]
    return [x for x in out if x]


def main() -> int:
    parser = argparse.ArgumentParser(description="Enforce pack scope against git diff.")
    parser.add_argument("pack_file", type=Path)
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    args = parser.parse_args()

    pack = load_yaml(args.pack_file)
    scope = pack.get("scope", {})
    files = scope.get("files") if isinstance(scope, dict) else None
    if not isinstance(files, list) or not files:
        raise SystemExit("scope.files is missing or empty in pack.")

    allowed = {str(x).replace("\\", "/").strip() for x in files}
    changed = get_changed_files(args.repo)

    violations = [f for f in changed if f not in allowed]
    if violations:
        print("SCOPE CHECK: FAIL")
        print("Out-of-scope files:")
        for f in violations:
            print(f"- {f}")
        return 1

    print("SCOPE CHECK: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
