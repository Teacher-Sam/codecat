#!/usr/bin/env python3
"""Import Snakify Chapter 1 from vpavlenko/content (official test cases)."""

from __future__ import annotations

import json
import re
import urllib.request
from pathlib import Path

BASE_URL = "https://raw.githubusercontent.com/vpavlenko/content/master/problems"
DATA = Path(__file__).resolve().parent.parent / "java" / "data"
ID_PREFIX = "java-"
CHAPTER_ID = "1"
CHAPTER_DIR = DATA / f"chapter-{CHAPTER_ID}"


def fetch_txt(filename: str) -> str:
    url = f"{BASE_URL}/{filename}"
    with urllib.request.urlopen(url, timeout=30) as resp:
        return resp.read().decode("utf-8")


def parse_official_txt(text: str) -> dict:
    name_match = re.search(r"Name:\s*\n(.+?)\n\nStatement:", text, re.S)
    statement_match = re.search(r"Statement:\s*\n(.+?)(?=\n\nTest:|\Z)", text, re.S)
    if not name_match or not statement_match:
        raise ValueError("Invalid problem file format")

    name = name_match.group(1).strip()
    statement = statement_match.group(1).strip()

    tests = []
    for block in re.findall(r"Test:\s*\n(.*?)\n\nAnswer:\s*\n(.*?)(?=\n\nTest:|\Z)", text, re.S):
        tests.append({"input": block[0].rstrip("\n"), "output": block[1].rstrip("\n")})

    return {"name": name, "statement": statement, "tests": tests}


def stmt_html_en(text: str) -> str:
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    parts = []
    for p in paragraphs:
        p = re.sub(r"`([^`]+)`", r"<code>\1</code>", p)
        p = p.replace("\n", " ")
        parts.append(f"<p>{p}</p>")
    return "".join(parts)


META = {
    "aplusbplusc.txt": {
        "id": "1-1",
        "title": {"zh": "三數相加", "en": "Sum of three numbers"},
        "zh": "寫一個程式，讀入三個整數（各佔一行），輸出它們的和。",
        "hint": {
            "zh": "使用 <code>Scanner.nextInt()</code> 讀取三個整數，再相加輸出。",
            "en": "Read three integers with <code>Scanner.nextInt()</code> and print their sum.",
        },
        "starter": (
            "import java.util.Scanner;\n\n"
            "public class Main {\n"
            "    public static void main(String[] args) {\n"
            "        Scanner scanner = new Scanner(System.in);\n"
            "        \n"
            "    }\n"
            "}"
        ),
    },
    "area_of_right_triangle.txt": {
        "id": "1-4",
        "title": {"zh": "直角三角形面積", "en": "Area of right-angled triangle"},
        "zh": "讀入直角三角形的底邊長與高（各佔一行），輸出面積。",
        "hint": {
            "zh": "面積 = 底 × 高 ÷ 2。請用 <code>double</code> 或除以 <code>2.0</code>，讓小數輸出正確。",
            "en": "Area = base × height ÷ 2. Use <code>double</code> or divide by <code>2.0</code> for correct decimal output.",
        },
        "starter": (
            "import java.util.Scanner;\n\n"
            "public class Main {\n"
            "    public static void main(String[] args) {\n"
            "        Scanner scanner = new Scanner(System.in);\n"
            "        \n"
            "    }\n"
            "}"
        ),
    },
    "hello_harry.txt": {
        "id": "1-5",
        "title": {"zh": "Hello, Harry!", "en": "Hello, Harry!"},
        "zh": (
            "讀入一個名字，輸出問候語：先印 <code>Hello, </code>，接著名字，最後印 <code>!</code>。"
            "名字與驚嘆號之間<strong>不能</strong>有空格。輸出必須與範例完全一致。"
        ),
        "hint": {
            "zh": "可用字串連接：<code>\"Hello, \" + name + \"!\"</code>",
            "en": "Concatenate strings: <code>\"Hello, \" + name + \"!\"</code>",
        },
        "starter": (
            "import java.util.Scanner;\n\n"
            "public class Main {\n"
            "    public static void main(String[] args) {\n"
            "        Scanner scanner = new Scanner(System.in);\n"
            "        \n"
            "    }\n"
            "}"
        ),
    },
    "apples.txt": {
        "id": "1-6",
        "title": {"zh": "分蘋果", "en": "Apple sharing"},
        "zh": (
            "<code>N</code> 位學生分 <code>K</code> 顆蘋果，盡量平均分給每位學生，"
            "無法整除的剩餘蘋果留在籃子裡。讀入 <code>N</code> 和 <code>K</code>，"
            "輸出兩行：每位學生拿到幾顆、籃子裡剩幾顆。"
        ),
        "hint": {
            "zh": "整除用 <code>/</code>，餘數用 <code>%</code>。",
            "en": "Use <code>/</code> for integer division and <code>%</code> for remainder.",
        },
        "starter": (
            "import java.util.Scanner;\n\n"
            "public class Main {\n"
            "    public static void main(String[] args) {\n"
            "        Scanner scanner = new Scanner(System.in);\n"
            "        \n"
            "    }\n"
            "}"
        ),
    },
    "next_and_previous.txt": {
        "id": "1-7",
        "title": {"zh": "前一個與下一個", "en": "Previous and next"},
        "zh": "讀入一個整數，依照範例格式輸出它的下一個數與上一個數。句號前不要多餘空格。",
        "hint": {
            "zh": "格式：<code>The next number for the number X is Y.</code>（上一行同理）",
            "en": "Format: <code>The next number for the number X is Y.</code> (same pattern for previous).",
        },
        "starter": (
            "import java.util.Scanner;\n\n"
            "public class Main {\n"
            "    public static void main(String[] args) {\n"
            "        Scanner scanner = new Scanner(System.in);\n"
            "        \n"
            "    }\n"
            "}"
        ),
    },
    "desks.txt": {
        "id": "1-9",
        "title": {"zh": "學校課桌", "en": "School desks"},
        "zh": (
            "三個班級各有 <code>a</code>、<code>b</code>、<code>c</code> 位學生，"
            "每張課桌坐 2 人。讀入三個整數，輸出至少要買幾張課桌。"
        ),
        "hint": {
            "zh": "每班所需課桌 = <code>(人數 + 1) / 2</code>（整數運算），再把三班相加。",
            "en": "Desks per class = <code>(students + 1) / 2</code> (integer math), then sum all three.",
        },
        "starter": (
            "import java.util.Scanner;\n\n"
            "public class Main {\n"
            "    public static void main(String[] args) {\n"
            "        Scanner scanner = new Scanner(System.in);\n"
            "        \n"
            "    }\n"
            "}"
        ),
    },
}

MANUAL = [
    {
        "id": "1-2",
        "title": {"zh": "Hi John", "en": "Hi John"},
        "description": {
            "zh": "<p>讀入一個名字，輸出 <code>Hi</code> 與名字，中間以一個空格分隔。請參考範例。</p>",
            "en": "<p>Read a name and print the word <code>Hi</code> followed by the name, separated by a single space.</p>",
        },
        "hint": {
            "zh": "使用 <code>System.out.println(\"Hi \" + name);</code> 或 <code>System.out.println(\"Hi \" + scanner.nextLine());</code>",
            "en": "Use <code>System.out.println(\"Hi \" + name);</code> or similar string concatenation.",
        },
        "starterCode": (
            "import java.util.Scanner;\n\n"
            "public class Main {\n"
            "    public static void main(String[] args) {\n"
            "        Scanner scanner = new Scanner(System.in);\n"
            "        \n"
            "    }\n"
            "}"
        ),
        "tests": [
            {"input": "John", "output": "Hi John"},
            {"input": "Jack", "output": "Hi Jack"},
            {"input": "Santa Claus", "output": "Hi Santa Claus"},
        ],
        "note": "官方 repo 無獨立測資檔，測試依題意推導",
    },
    {
        "id": "1-3",
        "title": {"zh": "平方", "en": "Square"},
        "description": {
            "zh": "<p>讀入一個整數，輸出它的平方。</p>",
            "en": "<p>Read an integer and print its square.</p>",
        },
        "hint": {
            "zh": "輸出 <code>n * n</code> 即可。",
            "en": "Print <code>n * n</code>.",
        },
        "starterCode": (
            "import java.util.Scanner;\n\n"
            "public class Main {\n"
            "    public static void main(String[] args) {\n"
            "        Scanner scanner = new Scanner(System.in);\n"
            "        \n"
            "    }\n"
            "}"
        ),
        "tests": [
            {"input": "5", "output": "25"},
            {"input": "12", "output": "144"},
            {"input": "0", "output": "0"},
        ],
        "note": "官方 repo 無獨立測資檔，測試依題意推導",
    },
    {
        "id": "1-8",
        "title": {"zh": "兩個時間戳", "en": "Two timestamps"},
        "description": {
            "zh": (
                "<p>時間戳由三個數字組成：時、分、秒。給定兩個時間戳（各三行），"
                "計算兩者相差多少秒。第一個時間一定早於第二個。</p>"
            ),
            "en": (
                "<p>A timestamp has three numbers: hours, minutes and seconds. "
                "Given two timestamps (three lines each), calculate how many seconds are between them. "
                "The first moment occurs before the second.</p>"
            ),
        },
        "hint": {
            "zh": "先把每個時間戳換算成秒，再相減：<code>h×3600 + m×60 + s</code>",
            "en": "Convert each timestamp to seconds, then subtract: <code>h×3600 + m×60 + s</code>",
        },
        "starterCode": (
            "import java.util.Scanner;\n\n"
            "public class Main {\n"
            "    public static void main(String[] args) {\n"
            "        Scanner scanner = new Scanner(System.in);\n"
            "        \n"
            "    }\n"
            "}"
        ),
        "tests": [
            {"input": "1\n1\n1\n2\n2\n2", "output": "3661"},
            {"input": "0\n0\n0\n0\n1\n0", "output": "60"},
            {"input": "0\n0\n0\n1\n0\n0", "output": "3600"},
        ],
        "note": "第一組測資來自社群驗證，其餘依題意推導",
    },
]

ORDER = [
    "aplusbplusc.txt",
    "manual:1-2",
    "manual:1-3",
    "area_of_right_triangle.txt",
    "hello_harry.txt",
    "apples.txt",
    "next_and_previous.txt",
    "manual:1-8",
    "desks.txt",
]


def build_from_official(filename: str) -> dict:
    meta = META[filename]
    official = parse_official_txt(fetch_txt(filename))
    return {
        "id": meta["id"],
        "title": meta["title"],
        "description": {
            "zh": f"<p>{meta['zh']}</p>",
            "en": stmt_html_en(official["statement"]),
        },
        "hint": meta["hint"],
        "starterCode": meta["starter"],
        "tests": official["tests"],
        "source": f"vpavlenko/content/{filename}",
    }


def write_chapter(problems: list[dict]) -> None:
    CHAPTER_DIR.mkdir(parents=True, exist_ok=True)
    problem_ids = []

    for problem in problems:
        pid = problem["id"]
        if not pid.startswith(ID_PREFIX):
            pid = f"{ID_PREFIX}{pid}"
            problem = {**problem, "id": pid}
        problem_ids.append(pid)
        (CHAPTER_DIR / f"{pid}.json").write_text(
            json.dumps(problem, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    intro_id = f"{ID_PREFIX}{CHAPTER_ID}-0"
    if (CHAPTER_DIR / f"{intro_id}.json").exists():
        problem_ids.insert(0, intro_id)

    chapter_meta = {
        "id": CHAPTER_ID,
        "title": {
            "zh": "輸入、輸出與數字",
            "en": "Input, print and numbers",
        },
        "description": {
            "zh": "學習 Java 的基本輸出、變數與 Scanner 讀取輸入。",
            "en": "Learn basic output, variables, and reading input with Scanner in Java.",
        },
        "problemIds": problem_ids,
        "source": "https://github.com/vpavlenko/content",
    }
    (CHAPTER_DIR / "chapter.json").write_text(
        json.dumps(chapter_meta, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    index_path = DATA / "index.json"
    index = {"chapters": []}
    if index_path.exists():
        index = json.loads(index_path.read_text(encoding="utf-8"))

    dir_name = f"chapter-{CHAPTER_ID}"
    if not any(ch.get("id") == CHAPTER_ID for ch in index["chapters"]):
        index["chapters"].append({"id": CHAPTER_ID, "dir": dir_name})
    else:
        index["chapters"] = [
            {"id": CHAPTER_ID, "dir": dir_name} if ch.get("id") == CHAPTER_ID else ch
            for ch in index["chapters"]
        ]

    index_path.write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(problems)} problems to {CHAPTER_DIR}")


def main() -> None:
    manual_by_id = {p["id"]: p for p in MANUAL}
    problems = []

    for item in ORDER:
        if item.startswith("manual:"):
            pid = item.split(":", 1)[1]
            prob = manual_by_id[pid].copy()
            prob.pop("note", None)
            problems.append(prob)
        else:
            problems.append(build_from_official(item))

    write_chapter(problems)


if __name__ == "__main__":
    main()
