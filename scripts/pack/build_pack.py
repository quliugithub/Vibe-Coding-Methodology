#!/usr/bin/env python3
"""Create a pack file from templates."""

from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path
import shutil


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a pack file.")
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--change", required=True, help="OpenSpec change name")
    parser.add_argument("--task-id", default="", help="Optional task id")
    parser.add_argument("--spec-ref", required=True, help="Spec path reference")
    parser.add_argument("--mode", choices=["lite", "full"], default="full")
    args = parser.parse_args()

    template = args.repo / ".pack" / "templates" / f"pack-{args.mode}.yaml"
    if not template.exists():
        raise SystemExit(f"Template not found: {template}")

    now = datetime.now()
    out_dir = args.repo / "docs" / "ai" / "packs" / now.strftime("%Y") / now.strftime("%m")
    out_dir.mkdir(parents=True, exist_ok=True)

    slug = f"{args.change}-{args.task_id}".strip("-")
    out_file = out_dir / f"{now.strftime('%Y-%m-%d')}_{slug}.pack.yaml"
    shutil.copyfile(template, out_file)

    text = out_file.read_text(encoding="utf-8")
    text = text.replace("CHG-001-task", slug or args.change)
    text = text.replace("openspec/changes/change-name", f"openspec/changes/{args.change}")
    text = text.replace("docs/specs/module/feature.spec.md", args.spec_ref)
    if args.task_id:
        text = text.replace("T012", args.task_id)
    out_file.write_text(text, encoding="utf-8")

    print(out_file)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
