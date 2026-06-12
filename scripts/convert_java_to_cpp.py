#!/usr/bin/env python3
"""Convert Java chapter JSON to proper C++ problems (descriptions, hints, starter code)."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
JAVA_DIR = ROOT / "java" / "data"
CPP_DIR = ROOT / "cpp" / "data"
PREFIX = "cpp-"

STARTER_INT = """#include <iostream>
using namespace std;

int main() {
    
    return 0;
}
"""

STARTER_STRING = """#include <iostream>
#include <string>
using namespace std;

int main() {
    
    return 0;
}
"""

STARTER_DOUBLE = """#include <iostream>
#include <iomanip>
using namespace std;

int main() {
    
    return 0;
}
"""

STARTER_INT3 = """#include <iostream>
using namespace std;

int main() {
    int a, b, c;
    cin >> a >> b >> c;
    
    return 0;
}
"""

STARTER_IOMANIP = """#include <iostream>
#include <iomanip>
using namespace std;

int main() {
    
    return 0;
}
"""

FLOAT_PROBLEMS = frozenset({"2-10", "2-11", "2-18", "2-19"})

# Per-problem C++ hints and optional description patches (bare id without prefix)
CPP_META: dict[str, dict] = {
    # --- Chapter 1 ---
    "1-1": {
        "starterCode": STARTER_INT3,
        "hint": {
            "zh": "使用 <code>cin >> a >> b >> c;</code> 讀取三個整數，相加後用 <code>cout</code> 輸出。",
            "en": "Read three integers with <code>cin >> a >> b >> c;</code>, add them, and print the sum with <code>cout</code>.",
        },
    },
    "1-2": {
        "starterCode": STARTER_STRING,
        "hint": {
            "zh": "整行讀名字：<code>getline(cin, name);</code>，輸出：<code>cout << \"Hi \" << name;</code>",
            "en": "Read the full line with <code>getline(cin, name);</code>, then <code>cout << \"Hi \" << name;</code>",
        },
    },
    "1-3": {
        "starterCode": STARTER_INT,
        "hint": {
            "zh": "讀入整數 <code>n</code>，輸出 <code>n * n</code>。",
            "en": "Read integer <code>n</code> and print <code>n * n</code>.",
        },
    },
    "1-4": {
        "starterCode": STARTER_DOUBLE,
        "hint": {
            "zh": "面積 = 底 × 高 ÷ 2。請用 <code>double</code> 或除以 <code>2.0</code>，讓小數輸出正確。",
            "en": "Area = base × height ÷ 2. Use <code>double</code> or divide by <code>2.0</code> for correct decimal output.",
        },
    },
    "1-5": {
        "starterCode": STARTER_STRING,
        "description": {
            "en": "<p>Write a program that greets the user by printing the word \"Hello\", a comma, the name of the user and an exclamation mark after it. See the examples below.</p><p><b>Warning.</b> Your program's output should strictly match the desired one, character by character. There shouldn't be any space between the name and the exclamation mark. In C++, chain output with <code>&lt;&lt;</code>, for example: <code>cout &lt;&lt; \"Hello, \" &lt;&lt; name &lt;&lt; \"!\";</code></p>",
        },
        "hint": {
            "zh": "使用輸出串接：<code>cout << \"Hello, \" << name << \"!\";</code>",
            "en": "Chain output: <code>cout << \"Hello, \" << name << \"!\";</code>",
        },
    },
    "1-6": {
        "starterCode": STARTER_INT,
        "hint": {
            "zh": "整除用 <code>/</code>，餘數用 <code>%</code>。分別輸出兩行。",
            "en": "Use <code>/</code> for integer division and <code>%</code> for remainder. Print two lines.",
        },
    },
    "1-7": {
        "starterCode": """#include <iostream>
using namespace std;

int main() {
    long long n;
    cin >> n;
    
    return 0;
}
""",
        "description": {
            "en": "<p>Write a program that reads an integer number and prints its previous and next numbers. See the examples below for the exact format your answers should take. There shouldn't be a space before the period.</p><p>Use <code>long long</code> if the input can be very large. Print with <code>cout</code> and <code>&lt;&lt;</code>.</p>",
        },
        "hint": {
            "zh": "格式：<code>The next number for the number X is Y.</code>（上一行同理）。大整數請用 <code>long long</code>。",
            "en": "Format: <code>The next number for the number X is Y.</code> Use <code>long long</code> for large inputs.",
        },
    },
    "1-8": {
        "starterCode": STARTER_INT,
        "hint": {
            "zh": "先把每個時間戳換算成秒，再相減：<code>h×3600 + m×60 + s</code>",
            "en": "Convert each timestamp to seconds, then subtract: <code>h×3600 + m×60 + s</code>",
        },
    },
    "1-9": {
        "starterCode": STARTER_INT,
        "hint": {
            "zh": "每班所需課桌 = <code>(人數 + 1) / 2</code>（整數運算），再把三班相加。",
            "en": "Desks per class = <code>(students + 1) / 2</code> (integer math), then sum all three.",
        },
    },
    # --- Chapter 2 ---
    "2-1": {
        "hint": {
            "zh": "使用 <code>n % 10</code>。",
            "en": "Use <code>n % 10</code>.",
        },
    },
    "2-2": {
        "hint": {
            "zh": "十位：<code>n / 10</code>，個位：<code>n % 10</code>。",
            "en": "Tens: <code>n / 10</code>, units: <code>n % 10</code>.",
        },
    },
    "2-3": {
        "hint": {
            "zh": "<code>units * 10 + tens</code>",
            "en": "<code>units * 10 + tens</code>",
        },
    },
    "2-4": {
        "hint": {
            "zh": "使用 <code>n % 100</code>。",
            "en": "Use <code>n % 100</code>.",
        },
    },
    "2-5": {
        "hint": {
            "zh": "<code>(n / 10) % 10</code>",
            "en": "<code>(n / 10) % 10</code>",
        },
    },
    "2-6": {
        "hint": {
            "zh": "分別取出百、十、個位再相加（整數除法與 <code>%</code>）。",
            "en": "Extract hundreds, tens, and units digits with <code>/</code> and <code>%</code>, then sum.",
        },
    },
    "2-7": {
        "starterCode": STARTER_IOMANIP,
        "hint": {
            "zh": "反轉各位數後，用 <code>cout << setfill('0') << setw(3) << ans;</code> 保留前導零。",
            "en": "Reverse the digits, then print with <code>setfill('0') << setw(3)</code> to keep leading zeros.",
        },
    },
    "2-8": {
        "hint": {
            "zh": "例如 12 與 34 → 輸出 <code>1324</code>（交替取十位、個位）。",
            "en": "Example: 12 and 34 → output <code>1324</code> (alternate tens and units).",
        },
    },
    "2-9": {
        "hint": {
            "zh": "<code>n % 100 * 100 + n / 100</code>（整數運算）",
            "en": "<code>n % 100 * 100 + n / 100</code> (integer arithmetic)",
        },
    },
    "2-10": {
        "starterCode": STARTER_DOUBLE,
        "hint": {
            "zh": "可用 <code>x - (long long)x</code>；注意浮點精度，必要時用字串處理或調整 <code>setprecision</code>。",
            "en": "Use <code>x - (long long)x</code>; watch floating-point precision — string parsing or <code>setprecision</code> may help.",
        },
    },
    "2-11": {
        "starterCode": STARTER_STRING,
        "hint": {
            "zh": "讀成字串，找 <code>'.'</code> 後的第一個字元：<code>s[s.find('.') + 1]</code>",
            "en": "Read as string and take the character after <code>'.'</code>: <code>s[s.find('.') + 1]</code>",
        },
    },
    "2-12": {
        "hint": {
            "zh": "無條件進位：<code>(M + N - 1) / N</code>。",
            "en": "Ceiling division: <code>(M + N - 1) / N</code>.",
        },
    },
    "2-13": {
        "hint": {
            "zh": "<code>(k + 3) % 7</code>",
            "en": "<code>(k + 3) % 7</code>",
        },
    },
    "2-14": {
        "hint": {
            "zh": "<code>hours = N / 60</code>，<code>minutes = N % 60</code>。",
            "en": "<code>hours = N / 60</code>, <code>minutes = N % 60</code>.",
        },
    },
    "2-15": {
        "starterCode": """#include <iostream>
using namespace std;

int main() {
    long long a, b, n;
    cin >> a >> b >> n;
    
    return 0;
}
""",
        "hint": {
            "zh": "總分 = <code>n * (100*a + b)</code>（用 <code>long long</code>），元 = 總分/100，分 = 總分%100。",
            "en": "Total cents = <code>n * (100*a + b)</code> using <code>long long</code>; dollars = total/100, cents = total%100.",
        },
    },
    "2-16": {
        "hint": {
            "zh": "<code>(year - 1) / 100 + 1</code>",
            "en": "<code>(year - 1) / 100 + 1</code>",
        },
    },
    "2-17": {
        "hint": {
            "zh": "第一天結束已在 <code>a</code> 公尺；之後每天淨增 <code>a - b</code>。",
            "en": "After day 1 the snail is at <code>a</code>; each later day net gain is <code>a - b</code>.",
        },
    },
    "2-18": {
        "starterCode": STARTER_DOUBLE,
        "hint": {
            "zh": "<code>30*h + 30.0*m/60 + 30.0*s/3600</code>，輸出用 <code>cout << fixed << setprecision(...)</code> 對齊測資。",
            "en": "<code>30*h + 30.0*m/60 + 30.0*s/3600</code>; use <code>fixed << setprecision(...)</code> to match expected output.",
        },
    },
    "2-19": {
        "starterCode": STARTER_DOUBLE,
        "hint": {
            "zh": "分針角度：<code>fmod(alpha, 30.0) * 12</code>（或等價寫法），注意小數輸出格式。",
            "en": "Minute hand angle: <code>fmod(alpha, 30.0) * 12</code> (or equivalent); match decimal output format.",
        },
    },
}


def default_starter(bare_id: str) -> str:
    if bare_id in FLOAT_PROBLEMS:
        return STARTER_DOUBLE
    return STARTER_INT


def convert_problem(java_problem: dict, bare_id: str) -> dict:
    meta = CPP_META.get(bare_id, {})
    cpp_id = f"{PREFIX}{bare_id}"

    description = dict(java_problem.get("description", {}))
    if "description" in meta:
        description.update(meta["description"])

    hint = meta.get("hint", java_problem.get("hint"))
    starter = meta.get("starterCode", default_starter(bare_id))

    return {
        "id": cpp_id,
        "title": java_problem.get("title"),
        "description": description,
        "hint": hint,
        "starterCode": starter,
        "tests": java_problem.get("tests", []),
        "source": java_problem.get("source"),
    }


def convert_chapter(chapter_num: str) -> None:
    java_ch_dir = JAVA_DIR / f"chapter-{chapter_num}"
    cpp_ch_dir = CPP_DIR / f"chapter-{chapter_num}"
    cpp_ch_dir.mkdir(parents=True, exist_ok=True)

    java_chapter = json.loads((java_ch_dir / "chapter.json").read_text(encoding="utf-8"))
    cpp_ids = []

    for java_id in java_chapter["problemIds"]:
        bare = java_id.removeprefix("java-")
        cpp_id = f"{PREFIX}{bare}"
        cpp_ids.append(cpp_id)

        java_path = java_ch_dir / f"{java_id}.json"
        java_problem = json.loads(java_path.read_text(encoding="utf-8"))
        cpp_path = cpp_ch_dir / f"{cpp_id}.json"

        if java_problem.get("type") == "intro" and cpp_path.exists():
            continue

        cpp_problem = convert_problem(java_problem, bare)
        cpp_path.write_text(
            json.dumps(cpp_problem, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    desc = java_chapter.get("description", {})
    cpp_chapter = {
        "id": java_chapter["id"],
        "title": java_chapter.get("title"),
        "description": desc,
        "problemIds": cpp_ids,
        "source": java_chapter.get("source"),
    }
    (cpp_ch_dir / "chapter.json").write_text(
        json.dumps(cpp_chapter, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Converted chapter {chapter_num}: {len(cpp_ids)} problems")


def write_index() -> None:
    chapters = []
    for ch_dir in sorted(CPP_DIR.glob("chapter-*"), key=lambda p: int(p.name.split("-")[1])):
        chapter = json.loads((ch_dir / "chapter.json").read_text(encoding="utf-8"))
        chapters.append({"id": chapter["id"], "dir": ch_dir.name})
    (CPP_DIR / "index.json").write_text(
        json.dumps({"chapters": chapters}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Index: {len(chapters)} chapter(s)")


def main() -> None:
    CPP_DIR.mkdir(parents=True, exist_ok=True)
    for chapter_num in ("1", "2"):
        convert_chapter(chapter_num)
    write_index()
    print("C++ chapters regenerated.")


if __name__ == "__main__":
    main()
