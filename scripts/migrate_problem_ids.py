#!/usr/bin/env python3
"""Add language prefix to problem IDs and rename JSON files (e.g. 1-1 -> java-1-1)."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def migrate(data_dir: Path, prefix: str) -> None:
    if not prefix.endswith("-"):
        prefix = f"{prefix}-"

    for chapter_dir in sorted(data_dir.glob("chapter-*")):
        chapter_file = chapter_dir / "chapter.json"
        if not chapter_file.exists():
            continue

        chapter = json.loads(chapter_file.read_text(encoding="utf-8"))
        new_ids: list[str] = []

        for old_id in chapter.get("problemIds", []):
            bare = old_id.removeprefix(prefix) if old_id.startswith(prefix) else old_id
            new_id = f"{prefix}{bare}" if not old_id.startswith(prefix) else old_id
            new_ids.append(new_id)

            old_path = chapter_dir / f"{old_id}.json"
            bare_path = chapter_dir / f"{bare}.json"
            new_path = chapter_dir / f"{new_id}.json"

            source = old_path if old_path.exists() else bare_path
            if not source.exists():
                print(f"  skip missing: {source}")
                continue

            problem = json.loads(source.read_text(encoding="utf-8"))
            problem["id"] = new_id
            new_path.write_text(json.dumps(problem, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

            if source != new_path and source.exists():
                source.unlink()

        chapter["problemIds"] = new_ids
        chapter_file.write_text(json.dumps(chapter, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"Updated {chapter_dir.name}: {len(new_ids)} problems")


def main() -> None:
    if len(sys.argv) != 3:
        print("Usage: migrate_problem_ids.py <java|cpp> <prefix>")
        sys.exit(1)

    lang = sys.argv[1]
    prefix = sys.argv[2]
    data_dir = ROOT / lang / "data"
    if not data_dir.is_dir():
        print(f"Missing {data_dir}")
        sys.exit(1)

    migrate(data_dir, prefix)
    print("Done.")


if __name__ == "__main__":
    main()
