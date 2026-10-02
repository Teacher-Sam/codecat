#!/usr/bin/env python3
"""Convert the reviewed C++ Snakify chapters 5-11 into Java exercises."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CPP = ROOT / "cpp" / "data"
JAVA = ROOT / "java" / "data"

NOTES = {
    "5": {
        "zh": "Java 字串不可直接修改；請使用 charAt()、substring()、indexOf()、lastIndexOf()，需要大量修改時使用 StringBuilder。",
        "en": "Java strings are immutable. Use charAt(), substring(), indexOf(), lastIndexOf(), and StringBuilder for repeated modifications.",
    },
    "6": {
        "zh": "輸入以 0 結束時不要把結尾的 0 納入統計；可能出現小數結果時使用 double。",
        "en": "Do not include a terminating zero in the sequence. Use double when the result may be fractional.",
    },
    "7": {
        "zh": "本章以陣列或 ArrayList 儲存資料；大小固定時優先使用陣列，需要插入或刪除時使用 ArrayList。",
        "en": "Use arrays for fixed-size data and ArrayList when insertion or removal is required.",
    },
    "8": {
        "zh": "請在 Main 類別中撰寫 static 方法，由 main 讀取輸入、呼叫方法並輸出結果；遞迴題不得以迴圈取代。",
        "en": "Write a static method in Main and call it from main. Do not replace recursion with a loop in recursion exercises.",
    },
    "9": {
        "zh": "Java 二維陣列使用 int[][]；第一個索引是列，第二個索引是欄。",
        "en": "Use int[][] for a Java matrix. The first index is the row and the second is the column.",
    },
    "10": {
        "zh": "使用 HashSet 處理唯一值；需要自然排序輸出時使用 TreeSet。",
        "en": "Use HashSet for unique values and TreeSet when naturally sorted output is required.",
    },
    "11": {
        "zh": "使用 HashMap 儲存鍵值對；需要依鍵排序輸出時使用 TreeMap。",
        "en": "Use HashMap for key-value data and TreeMap when output must be sorted by key.",
    },
}

STARTERS = {
    "5": """import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        String s = scanner.nextLine();

    }
}
""",
    "6": """import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

    }
}
""",
    "7": """import java.util.*;

public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

    }
}
""",
    "8": """import java.util.Scanner;

public class Main {
    // 在這裡撰寫題目指定的 static 方法

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

    }
}
""",
    "9": """import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

    }
}
""",
    "10": """import java.util.*;

public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

    }
}
""",
    "11": """import java.util.*;

public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

    }
}
""",
}

CHAPTER_DESCRIPTIONS = {
    "5": {"zh": "使用 Java String 處理索引、子字串、搜尋與替換。", "en": "String indexing, substrings, search, and replacement with Java String."},
    "6": {"zh": "使用 while 迴圈處理未知次數的重複、數列與費氏數列。", "en": "Unknown-length repetition, sequences, and Fibonacci numbers with while loops."},
    "7": {"zh": "以陣列與 ArrayList 儲存、走訪及修改一維資料。", "en": "Store, traverse, and modify one-dimensional data with arrays and ArrayList."},
    "8": {"zh": "撰寫 Java static 方法，並用遞迴分解問題。", "en": "Write Java static methods and decompose problems recursively."},
    "9": {"zh": "使用 Java 二維陣列建立、走訪及轉換矩陣。", "en": "Create, traverse, and transform matrices with Java two-dimensional arrays."},
    "10": {"zh": "使用 HashSet 與 TreeSet 處理唯一值和集合運算。", "en": "Unique values and set operations with HashSet and TreeSet."},
    "11": {"zh": "使用 HashMap 與 TreeMap 儲存鍵值對和統計資料。", "en": "Key-value storage and frequency counting with HashMap and TreeMap."},
}


def strip_cpp_note(text: str) -> str:
    return re.sub(r"<p><strong>C\+\+[^<]*</strong>.*?</p>\s*$", "", text, flags=re.S).rstrip()


def add_java_note(text: str, note: str, label: str) -> str:
    return f'{strip_cpp_note(text)}<p><strong>{label}</strong> {note}</p>'


def convert_problem(problem: dict, chapter: str) -> dict:
    converted = json.loads(json.dumps(problem, ensure_ascii=False))
    converted["id"] = converted["id"].replace("cpp-", "java-", 1)
    if converted.get("type") == "intro":
        converted["title"]["zh"] = converted["title"]["zh"].replace("C++", "Java")
        converted["title"]["en"] = converted["title"]["en"].replace("C++", "Java")
        return converted
    converted["description"]["zh"] = add_java_note(
        converted["description"]["zh"], NOTES[chapter]["zh"], "Java 注意："
    )
    converted["description"]["en"] = add_java_note(
        converted["description"]["en"], NOTES[chapter]["en"], "Java note:"
    )
    converted["hint"] = NOTES[chapter]
    converted["starterCode"] = STARTERS[chapter]
    return converted


def main() -> None:
    index = json.loads((JAVA / "index.json").read_text(encoding="utf-8"))
    index["chapters"] = [entry for entry in index["chapters"] if int(entry["id"]) < 5]
    for chapter in map(str, range(5, 12)):
        source_dir = CPP / f"chapter-{chapter}"
        target_dir = JAVA / f"chapter-{chapter}"
        target_dir.mkdir(parents=True, exist_ok=True)
        source_meta = json.loads((source_dir / "chapter.json").read_text(encoding="utf-8"))
        problem_ids: list[str] = []
        for cpp_id in source_meta["problemIds"]:
            problem = json.loads((source_dir / f"{cpp_id}.json").read_text(encoding="utf-8"))
            converted = convert_problem(problem, chapter)
            java_id = converted["id"]
            problem_ids.append(java_id)
            (target_dir / f"{java_id}.json").write_text(
                json.dumps(converted, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
            )
        meta = {**source_meta, "description": CHAPTER_DESCRIPTIONS[chapter], "problemIds": problem_ids}
        (target_dir / "chapter.json").write_text(
            json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        index["chapters"].append({"id": chapter, "dir": f"chapter-{chapter}"})
        print(f"Converted Java chapter {chapter}: {len(problem_ids) - 1} exercises")
    (JAVA / "index.json").write_text(
        json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
