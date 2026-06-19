#!/usr/bin/env python3
"""Snakify 題目匯入共用工具。"""

from __future__ import annotations

import json
import re
import urllib.request
from pathlib import Path

BASE_URL = "https://raw.githubusercontent.com/vpavlenko/content/master/problems"
SNAKIFY_IMAGE_URL = "https://snakify.org/static/images/problems"
DATA = Path(__file__).resolve().parent.parent / "java" / "data"
JAVA_ROOT = DATA.parent
IMAGE_DIR = JAVA_ROOT / "images" / "problems"
IMAGE_WEB_PREFIX = "images/problems"
ID_PREFIX = "java-"

# Snakify chess-diagram assets (vpavlenko txt has no images; snakify.org serves PNGs).
PROBLEM_IMAGE_FILES = frozenset(
    {
        "rook_move.png",
        "chess_board.png",
        "king_move.png",
        "bishop_move.png",
        "queen_move.png",
        "knight_move.png",
    }
)

STARTER_INT = (
    "import java.util.Scanner;\n\n"
    "public class Main {\n"
    "    public static void main(String[] args) {\n"
    "        Scanner scanner = new Scanner(System.in);\n"
    "        \n"
    "    }\n"
    "}"
)

STARTER_DOUBLE = (
    "import java.util.Scanner;\n\n"
    "public class Main {\n"
    "    public static void main(String[] args) {\n"
    "        Scanner scanner = new Scanner(System.in);\n"
    "        \n"
    "    }\n"
    "}"
)


def fetch_txt(relpath: str) -> str:
    url = f"{BASE_URL}/{relpath}"
    with urllib.request.urlopen(url, timeout=30) as resp:
        return resp.read().decode("utf-8")


def parse_official_txt(text: str) -> dict:
    name_match = re.search(r"Name:\s*\n(.+?)\n\nStatement:", text, re.S)
    statement_match = re.search(r"Statement:\s*\n(.+?)(?=\n\nTest:|\Z)", text, re.S)
    if not name_match or not statement_match:
        raise ValueError("Invalid problem file format")

    tests = []
    for block in re.findall(r"Test:\s*\n(.*?)\n\nAnswer:\s*\n(.*?)(?=\n\nTest:|\Z)", text, re.S):
        tests.append({"input": block[0].rstrip("\n"), "output": block[1].rstrip("\n")})

    return {
        "name": name_match.group(1).strip(),
        "statement": statement_match.group(1).strip(),
        "tests": tests,
    }


def stmt_html_en(text: str) -> str:
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    parts = []
    for p in paragraphs:
        p = re.sub(r"`([^`]+)`", r"<code>\1</code>", p)
        p = p.replace("\n", " ")
        parts.append(f"<p>{p}</p>")
    return "".join(parts)


def download_problem_images() -> None:
    """Cache Snakify problem diagram PNGs under java/images/problems/."""
    IMAGE_DIR.mkdir(parents=True, exist_ok=True)
    headers = {"User-Agent": "Mozilla/5.0"}
    for filename in sorted(PROBLEM_IMAGE_FILES):
        dest = IMAGE_DIR / filename
        if dest.exists() and dest.stat().st_size > 0:
            continue
        url = f"{SNAKIFY_IMAGE_URL}/{filename}"
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=30) as resp:
            dest.write_bytes(resp.read())
        print(f"Downloaded {dest.relative_to(JAVA_ROOT.parent)}")


def image_file_for_slug(slug: str | None, relpath: str | None = None) -> str | None:
    if slug:
        candidate = f"{slug}.png"
        if candidate in PROBLEM_IMAGE_FILES:
            return candidate
    if relpath:
        candidate = f"{Path(relpath).stem}.png"
        if candidate in PROBLEM_IMAGE_FILES:
            return candidate
    return None


def problem_image_html(filename: str) -> str:
    return f'<p><img src="{IMAGE_WEB_PREFIX}/{filename}" alt="" width="500"></p>'


def rewrite_snakify_html(html: str) -> str:
    html = re.sub(
        r'src="/static/images/problems/([^"]+)"',
        rf'src="{IMAGE_WEB_PREFIX}/\1"',
        html,
    )
    html = re.sub(
        r"src='https://snakify\.org/static/images/problems/([^']+)'",
        rf'src="{IMAGE_WEB_PREFIX}/\1"',
        html,
    )
    return html


def enrich_description_html(html: str, image_file: str | None) -> str:
    html = rewrite_snakify_html(html)
    if image_file and f"{IMAGE_WEB_PREFIX}/{image_file}" not in html:
        html += problem_image_html(image_file)
    return html


def build_from_official(
    relpath: str,
    pid: str,
    title: dict,
    zh: str,
    hint: dict,
    starter: str = STARTER_INT,
) -> dict:
    official = parse_official_txt(fetch_txt(relpath))
    image_file = image_file_for_slug(None, relpath)
    zh_html = enrich_description_html(f"<p>{zh}</p>", image_file)
    en_html = enrich_description_html(stmt_html_en(official["statement"]), image_file)
    return {
        "id": pid,
        "title": title,
        "description": {"zh": zh_html, "en": en_html},
        "hint": hint,
        "starterCode": starter,
        "tests": official["tests"],
        "source": f"vpavlenko/content/{relpath}",
    }


def build_manual(problem: dict) -> dict:
    item = problem.copy()
    item.pop("note", None)
    return item


def write_chapter(chapter_id: str, chapter_meta: dict, problems: list[dict]) -> None:
    chapter_dir = DATA / f"chapter-{chapter_id}"
    chapter_dir.mkdir(parents=True, exist_ok=True)
    problem_ids = []

    for problem in problems:
        pid = problem["id"]
        if not pid.startswith(ID_PREFIX):
            pid = f"{ID_PREFIX}{pid}"
            problem = {**problem, "id": pid}
        problem_ids.append(pid)
        (chapter_dir / f"{pid}.json").write_text(
            json.dumps(problem, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    intro_id = f"{ID_PREFIX}{chapter_id}-0"
    if (chapter_dir / f"{intro_id}.json").exists():
        problem_ids.insert(0, intro_id)

    meta = {**chapter_meta, "id": chapter_id, "problemIds": problem_ids}
    (chapter_dir / "chapter.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    index_path = DATA / "index.json"
    index = {"chapters": []}
    if index_path.exists():
        index = json.loads(index_path.read_text(encoding="utf-8"))

    dir_name = f"chapter-{chapter_id}"
    chapters = [ch for ch in index["chapters"] if ch.get("id") != chapter_id]
    chapters.append({"id": chapter_id, "dir": dir_name})
    chapters.sort(key=lambda ch: int(ch["id"]))
    index["chapters"] = chapters
    index_path.write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote chapter {chapter_id}: {len(problems)} problems -> {chapter_dir}")
