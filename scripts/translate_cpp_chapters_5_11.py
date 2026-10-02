#!/usr/bin/env python3
"""Translate the complete English statements in C++ chapters 5-11 to Traditional Chinese."""

from __future__ import annotations

import json
import re
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "cpp" / "data"
TRANSLATE_URL = "https://translate.googleapis.com/translate_a/single"
PLACEHOLDER = "請依照下方英文原題"

TERMINOLOGY = {
    "字符串": "字串",
    "字符": "字元",
    "循環": "迴圈",
    "遞歸": "遞迴",
    "函數": "函式",
    "程序": "程式",
    "打印": "輸出",
    "返回": "回傳",
    "列表": "串列",
    "詞典": "字典",
    "創建": "建立",
    "實現": "實作",
    "選擇映射": "選擇 map",
}


def normalize_terminology(text: str) -> str:
    for source, target in TERMINOLOGY.items():
        text = text.replace(source, target)
    return text


def chunks(text: str, limit: int = 3500) -> list[str]:
    """Split on paragraph boundaries so requests remain comfortably below API limits."""
    blocks = re.split(r"(\n\s*\n)", text)
    result: list[str] = []
    current = ""
    for block in blocks:
        if current and len(current) + len(block) > limit:
            result.append(current)
            current = ""
        if len(block) <= limit:
            current += block
            continue
        if current:
            result.append(current)
            current = ""
        result.extend(block[i : i + limit] for i in range(0, len(block), limit))
    if current:
        result.append(current)
    return result


def translate_chunk(text: str) -> str:
    payload = urllib.parse.urlencode(
        {"client": "gtx", "sl": "en", "tl": "zh-TW", "dt": "t", "q": text}
    ).encode()
    request = urllib.request.Request(
        TRANSLATE_URL,
        data=payload,
        headers={"User-Agent": "snakify-practice-translator/1.0"},
    )
    with urllib.request.urlopen(request, timeout=45) as response:
        body = json.loads(response.read().decode("utf-8"))
    return "".join(part[0] for part in body[0] if part and part[0])


def translate(text: str) -> str:
    translated: list[str] = []
    for index, part in enumerate(chunks(text)):
        for attempt in range(4):
            try:
                translated.append(translate_chunk(part))
                break
            except Exception:
                if attempt == 3:
                    raise
                time.sleep(2 ** attempt)
        if index:
            time.sleep(0.15)
    return "".join(translated)


def main() -> None:
    updated = 0
    for chapter in range(5, 12):
        chapter_dir = DATA / f"chapter-{chapter}"
        for path in sorted(chapter_dir.glob("cpp-*.json")):
            problem = json.loads(path.read_text(encoding="utf-8"))
            if problem.get("type") == "intro":
                continue
            current = problem["description"].get("zh", "")
            if current and PLACEHOLDER not in current:
                translated = normalize_terminology(current)
                if translated == current:
                    continue
            else:
                translated = normalize_terminology(translate(problem["description"]["en"]))
            problem["description"]["zh"] = translated
            path.write_text(
                json.dumps(problem, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            updated += 1
            print(f"Translated {problem['id']}")
    print(f"Updated {updated} problem descriptions")


if __name__ == "__main__":
    main()
