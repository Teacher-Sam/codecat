#!/usr/bin/env python3
"""將 data/chapters.json 拆成章節目錄 + 各題 JSON 檔。"""

import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "data"
LEGACY = ROOT / "chapters.json"


def chapter_dir(chapter_id: str) -> str:
    return f"chapter-{chapter_id}"


def split() -> None:
    if not LEGACY.exists():
        raise SystemExit(f"找不到 {LEGACY}")

    payload = json.loads(LEGACY.read_text(encoding="utf-8"))
    index = {"chapters": []}

    for chapter in payload["chapters"]:
        cid = chapter["id"]
        dir_name = chapter_dir(cid)
        chapter_path = ROOT / dir_name
        chapter_path.mkdir(parents=True, exist_ok=True)

        problem_ids = []
        for problem in chapter["problems"]:
            pid = problem["id"]
            problem_ids.append(pid)
            (chapter_path / f"{pid}.json").write_text(
                json.dumps(problem, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )

        meta = {
            "id": cid,
            "title": chapter["title"],
            "description": chapter["description"],
            "problemIds": problem_ids,
        }
        if chapter.get("source"):
            meta["source"] = chapter["source"]

        (chapter_path / "chapter.json").write_text(
            json.dumps(meta, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

        index["chapters"].append({"id": cid, "dir": dir_name})

    (ROOT / "index.json").write_text(
        json.dumps(index, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    backup = ROOT / "chapters.json.bak"
    if backup.exists():
        backup.unlink()
    shutil.move(str(LEGACY), str(backup))
    print(f"已建立 {len(index['chapters'])} 個章節目錄，舊檔備份為 chapters.json.bak")


if __name__ == "__main__":
    split()
