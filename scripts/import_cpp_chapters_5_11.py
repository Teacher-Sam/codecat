#!/usr/bin/env python3
"""Import and adapt Snakify lessons 5-11 as self-contained C++ exercises."""

from __future__ import annotations

import html
import json
import re
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "cpp" / "data"
RAW = "https://raw.githubusercontent.com/vpavlenko/content/master/problems"

CHAPTERS = {
    "5": ("字串", "Strings", "使用 std::string 處理索引、子字串、搜尋與替換。", "String indexing, substrings, search, and replacement with std::string.", "str", [
        "slices", "num_words", "two_halves", "swap_two_words", "first_and_last_occurences", "second_occurence",
        "delete_chunk", "reverse_chunk", "replace_substring", "delete_char", "replace_in_chunk", "delete_every_third_char",
    ]),
    "6": ("while 迴圈", "While loop", "使用 while 迴圈處理未知次數的重複、數列與費氏數列。", "Unknown-length repetition, sequences, and Fibonacci numbers with while loops.", "while", [
        "list_of_squares", "minimal_divisor", "powers_of_two", "running", "seq_len", "seq_sum", "seq_avg", "seq_max",
        "seq_index_of_max", "seq_num_even", "seq_num_maximal", "seq_second_max", "seq_increasing_neighbours",
        "seq_max_chunk_of_repetitions", "std_dev", "bank_percents", "kth_fibonacci", "is_fibonacci",
    ]),
    "7": ("陣列（vector）", "Lists (arrays)", "以 std::vector 儲存、走訪及修改一維資料。", "Store, traverse, and modify one-dimensional data with std::vector.", "lists", [
        "even_indices", "even_elements", "more_than_neighbours", "increasing_neighbours", "same_sign_neighbours", "maximal_element",
        "swap_neighbours", "swap_min_and_max", "unique_elements", "num_distinct", "num_equal_pairs", "queens", "sherenga",
        "kegelbahn", "remove_element", "insert_element",
    ]),
    "8": ("函式與遞迴", "Functions and recursion", "撰寫 C++ 函式，並用遞迴分解問題。", "Write C++ functions and decompose problems recursively.", "functions", [
        "length_of_segment", "negative_power", "capitalize", "power_rec", "fibonacci_rec", "reverse_rec",
    ]),
    "9": ("二維陣列", "Two-dimensional arrays", "使用 vector<vector<T>> 建立、走訪及轉換矩陣。", "Create, traverse, and transform matrices with vector<vector<T>>.", "2d_arrays", [
        "2d_max", "snowflake", "chessboard", "diagonals", "secondary_diagonal", "swap_columns", "scale_matrix", "matrix_multiply",
    ]),
    "10": ("集合", "Sets", "使用 std::set 處理唯一值、交集及集合運算。", "Unique values, intersections, and set operations with std::set.", "sets", [
        "number_of_unique", "sets_intersection", "number_of_coincidental", "occurs_before", "cubes", "number_of_words",
        "guess_number", "guess_number_2", "polyglotes", "strikes",
    ]),
    "11": ("字典（map）", "Dictionaries (maps)", "使用 std::map 或 std::unordered_map 儲存鍵值對與統計資料。", "Key-value storage and frequency counting with std::map or std::unordered_map.", "dicts", [
        "occurency_index", "synonym_dictionary", "usa_elections", "most_frequent_word", "permissions", "countries_and_cities",
        "frequency_analysis", "english_latin_dict", "sales", "bank_accounts", "usa_elections_2", "accent_test",
        "genealogy_descendants_count", "genealogy_ancestors_and_descendants", "genealogy_level_count", "genealogy_lca",
    ]),
}

ZH_TITLES = {
    "slices":"字串切片", "num_words":"單字數量", "two_halves":"交換前後兩半", "swap_two_words":"交換兩個單字",
    "first_and_last_occurences":"第一次與最後一次出現", "second_occurence":"第二次出現", "delete_chunk":"移除片段",
    "reverse_chunk":"反轉片段", "replace_substring":"替換子字串", "delete_char":"刪除字元", "replace_in_chunk":"片段內替換",
    "delete_every_third_char":"刪除每第三個字元", "list_of_squares":"平方數列表", "minimal_divisor":"最小因數",
    "powers_of_two":"2 的冪", "running":"晨跑計畫", "seq_len":"數列長度", "seq_sum":"數列總和", "seq_avg":"數列平均",
    "seq_max":"數列最大值", "seq_index_of_max":"最大值索引", "seq_num_even":"偶數個數", "seq_num_maximal":"最大值個數",
    "seq_second_max":"第二大值", "seq_increasing_neighbours":"相鄰遞增對", "seq_max_chunk_of_repetitions":"最長連續相同片段",
    "std_dev":"標準差", "bank_percents":"銀行利息", "kth_fibonacci":"第 K 個費氏數", "is_fibonacci":"判斷費氏數",
    "even_indices":"偶數索引元素", "even_elements":"偶數元素", "more_than_neighbours":"大於相鄰元素",
    "increasing_neighbours":"相鄰遞增元素", "same_sign_neighbours":"同號相鄰元素", "maximal_element":"最大元素與索引",
    "swap_neighbours":"交換相鄰元素", "swap_min_and_max":"交換最大與最小值", "unique_elements":"只出現一次的元素",
    "num_distinct":"不同元素數量", "num_equal_pairs":"相等配對數", "queens":"八皇后攻擊判斷", "sherenga":"隊伍排序",
    "kegelbahn":"保齡球瓶", "remove_element":"移除元素", "insert_element":"插入元素", "length_of_segment":"線段長度",
    "negative_power":"負次方", "capitalize":"首字母大寫", "power_rec":"遞迴次方", "fibonacci_rec":"遞迴費氏數",
    "reverse_rec":"遞迴反向輸出", "2d_max":"二維陣列最大值", "snowflake":"雪花", "chessboard":"棋盤",
    "diagonals":"主對角線距離", "secondary_diagonal":"副對角線", "swap_columns":"交換欄", "scale_matrix":"矩陣縮放",
    "matrix_multiply":"矩陣乘法", "number_of_unique":"唯一數量", "sets_intersection":"集合交集",
    "number_of_coincidental":"共同出現數量", "occurs_before":"先前是否出現", "cubes":"立方表示", "number_of_words":"不同單字數",
    "guess_number":"猜數字", "guess_number_2":"猜數字（二）", "polyglotes":"多語者", "strikes":"罷工日",
    "occurency_index":"出現次序", "synonym_dictionary":"同義詞字典", "usa_elections":"美國大選",
    "most_frequent_word":"最高頻單字", "permissions":"存取權限", "countries_and_cities":"國家與城市",
    "frequency_analysis":"頻率分析", "english_latin_dict":"英語－拉丁語字典", "sales":"銷售統計", "bank_accounts":"銀行帳戶",
    "usa_elections_2":"美國大選（二）", "accent_test":"重音檢查", "genealogy_descendants_count":"家譜後代數",
    "genealogy_ancestors_and_descendants":"祖先與後代", "genealogy_level_count":"家譜層級", "genealogy_lca":"最近共同祖先",
}

CPP_NOTES = {
    "5": "C++ 沒有 Python 切片語法；請使用索引、迴圈、substr()、find()、rfind()、erase() 或 replace()。",
    "6": "輸入以 0 結束的題目不要把結尾的 0 納入統計；需要小數結果時使用 double。",
    "7": "Python list 在此章對應 C++ 的 vector；先讀取數量或整行資料，再用索引走訪。",
    "8": "請實作題目指定的函式並由 main 讀取輸入、呼叫函式及輸出結果；遞迴題不得使用迴圈取代。",
    "9": "Python 二維 list 在此章對應 vector<vector<int>>；第一個索引是列，第二個索引是欄。",
    "10": "使用 set 的 insert、count、find、set_intersection 等操作；輸出集合時依題意保持排序。",
    "11": "Python dictionary 在此章對應 map 或 unordered_map；需要字典序輸出時應選用 map 或另外排序鍵。",
}

CPP_NOTES_EN = {
    "5": "C++ has no Python slice syntax. Use indexes, loops, substr(), find(), rfind(), erase(), or replace().",
    "6": "For zero-terminated input, do not include the terminating zero. Use double when the result may be fractional.",
    "7": "Python lists correspond to std::vector in C++. Read the size or the complete line, then traverse by index.",
    "8": "Implement the requested function and call it from main. In recursion exercises, do not replace recursion with a loop.",
    "9": "Use vector<vector<int>> for a two-dimensional array. The first index is the row and the second is the column.",
    "10": "Use std::set operations such as insert, count, find, and set_intersection. Preserve the requested output order.",
    "11": "Use std::map or std::unordered_map. Choose map, or sort the keys separately, when lexicographic output is required.",
}

# Some bonus files in the upstream repository are Russian-only. These summaries
# keep those exercises usable in the English/C++ adaptation.
EN_OVERRIDES = {
    "std_dev": ("Standard deviation", "Read a sequence of real numbers terminated by 0 and print its sample standard deviation."),
    "bank_percents": ("Bank interest", "An initial integer deposit grows by P percent each year, discarding fractional cents. Print the number of years needed to reach at least Y."),
    "sherenga": ("The lineup", "A non-increasing sequence contains students' heights. Given a new student's height, print the 1-based position after which the student should be inserted."),
    "remove_element": ("Remove an element", "Given an array and an index, remove the element at that zero-based index and print the remaining elements."),
    "insert_element": ("Insert an element", "Given an array, an index, and a value, insert the value at that zero-based index and print the resulting array."),
    "guess_number_2": ("Guess the number II", "Maintain the possible numbers from 1 to N. For each guess set and YES/NO answer, intersect or subtract that set. On HELP, print all remaining possibilities."),
    "strikes": ("Strikes", "Given a calendar and several strike schedules, count working weekdays lost to strikes; Saturdays and Sundays are not working days."),
    "sales": ("Sales", "Aggregate product quantities for every customer, then print customers and their products in lexicographic order."),
    "bank_accounts": ("Bank accounts", "Process DEPOSIT, WITHDRAW, BALANCE, TRANSFER, and INCOME operations. Create accounts when required and print ERROR for a BALANCE query on an unknown account."),
    "usa_elections_2": ("Elections in the USA II", "Allocate each state's electoral votes to the candidate with the most votes in that state, then print every candidate's total in lexicographic order."),
    "accent_test": ("Stress test", "Check a pupil's text against a dictionary of correctly stressed words. Count words with an unknown or incorrectly placed uppercase stress mark."),
    "genealogy_descendants_count": ("Genealogy: descendant counts", "Given parent-child relationships forming a family tree, print the number of descendants of every person in lexicographic order."),
    "genealogy_ancestors_and_descendants": ("Genealogy: ancestors and descendants", "For each pair of people, print whether the first is an ancestor of the second, the second is an ancestor of the first, or neither."),
    "genealogy_level_count": ("Genealogy: generation levels", "Determine every person's generation level from the root of the family tree and print names in lexicographic order."),
    "genealogy_lca": ("Genealogy: lowest common ancestor", "For each query pair, find and print their lowest common ancestor in the given family tree."),
}

STARTERS = {
    "5": "#include <iostream>\n#include <string>\n#include <algorithm>\nusing namespace std;\n\nint main() {\n    string s;\n    getline(cin, s);\n    \n    return 0;\n}\n",
    "6": "#include <iostream>\n#include <cmath>\n#include <iomanip>\nusing namespace std;\n\nint main() {\n    \n    return 0;\n}\n",
    "7": "#include <iostream>\n#include <vector>\n#include <algorithm>\nusing namespace std;\n\nint main() {\n    \n    return 0;\n}\n",
    "8": "#include <iostream>\n#include <string>\n#include <cmath>\nusing namespace std;\n\n// 在這裡撰寫題目指定的函式\n\nint main() {\n    \n    return 0;\n}\n",
    "9": "#include <iostream>\n#include <vector>\n#include <algorithm>\nusing namespace std;\n\nint main() {\n    \n    return 0;\n}\n",
    "10": "#include <iostream>\n#include <set>\n#include <string>\n#include <sstream>\n#include <algorithm>\nusing namespace std;\n\nint main() {\n    \n    return 0;\n}\n",
    "11": "#include <iostream>\n#include <map>\n#include <unordered_map>\n#include <vector>\n#include <string>\n#include <sstream>\n#include <algorithm>\nusing namespace std;\n\nint main() {\n    \n    return 0;\n}\n",
}


def fetch(path: str) -> str:
    req = urllib.request.Request(f"{RAW}/{path}", headers={"User-Agent": "snakify-practice-importer"})
    with urllib.request.urlopen(req, timeout=30) as response:
        return response.read().decode("utf-8")


def parse(text: str) -> tuple[str, str, list[dict[str, str]]]:
    name = re.search(r"Name:\s*\n(.+?)\n\nStatement:", text, re.S)
    statement = re.search(r"Statement:\s*\n(.+?)(?=\n\nTest:|\Z)", text, re.S)
    if not name or not statement:
        raise ValueError("Unsupported Snakify problem format")
    tests = [
        {"input": a.rstrip("\n"), "output": b.rstrip("\n")}
        for a, b in re.findall(r"Test:\s*\n(.*?)\n\nAnswer:\s*\n(.*?)(?=\n\nTest:|\Z)", text, re.S)
    ]
    return name.group(1).strip(), statement.group(1).strip(), tests


def clean_statement(statement: str, chapter: str) -> str:
    # Preserve upstream markup but make the most misleading Python-only wording C++ neutral.
    statement = statement.replace("<code>**</code> operator or the built in function <code>math.pow()</code>", "<code>pow()</code>")
    statement = statement.replace("Python list", "array").replace("Python lists", "arrays")
    statement = re.sub(r"\btuple\b", "pair", statement, flags=re.I)
    note = html.escape(CPP_NOTES_EN[chapter])
    return f"{statement}<p><strong>C++ note:</strong> {note}</p>"


def intro(chapter: str, zh_title: str, en_title: str, zh_desc: str, en_desc: str) -> dict:
    return {
        "id": f"cpp-{chapter}-0", "type": "intro", "title": {"zh": f"{zh_title}導讀", "en": f"{en_title} overview"},
        "description": {"zh": f"<p>{zh_desc}</p><p>{CPP_NOTES[chapter]}</p>", "en": f"<p>{en_desc}</p><p>{CPP_NOTES_EN[chapter]}</p>"},
        "hint": {"zh": "", "en": ""}, "starterCode": "", "tests": [], "source": "https://snakify.org/en/",
    }


def main() -> None:
    index = json.loads((DATA / "index.json").read_text(encoding="utf-8"))
    index["chapters"] = [c for c in index["chapters"] if int(c["id"]) < 5]
    total = 0
    for chapter, (zh_title, en_title, zh_desc, en_desc, folder, slugs) in CHAPTERS.items():
        out = DATA / f"chapter-{chapter}"
        out.mkdir(parents=True, exist_ok=True)
        problems = [intro(chapter, zh_title, en_title, zh_desc, en_desc)]
        for number, slug in enumerate(slugs, 1):
            source_path = f"{folder}/{slug}.txt"
            source_title, statement, tests = parse(fetch(source_path))
            if slug in EN_OVERRIDES:
                source_title, english_summary = EN_OVERRIDES[slug]
                statement = f"<p>{english_summary}</p>"
            pid = f"cpp-{chapter}-{number}"
            existing_path = out / f"{pid}.json"
            existing_zh = ""
            if existing_path.exists():
                existing = json.loads(existing_path.read_text(encoding="utf-8"))
                candidate = existing.get("description", {}).get("zh", "")
                if candidate and "請依照下方英文原題" not in candidate:
                    existing_zh = candidate
            problem = {
                "id": pid,
                "title": {"zh": ZH_TITLES[slug], "en": source_title},
                "description": {
                    "zh": existing_zh or f"<p><strong>{ZH_TITLES[slug]}</strong>：請依照下方英文原題的輸入、輸出規格完成程式。</p><p>{CPP_NOTES[chapter]}</p>",
                    "en": clean_statement(statement, chapter),
                },
                "hint": {"zh": CPP_NOTES[chapter], "en": CPP_NOTES_EN[chapter]},
                "starterCode": STARTERS[chapter], "tests": tests,
                "source": f"vpavlenko/content/problems/{source_path}",
            }
            problems.append(problem)
        for old in out.glob("cpp-*.json"):
            old.unlink()
        for problem in problems:
            (out / f"{problem['id']}.json").write_text(json.dumps(problem, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        meta = {
            "id": chapter, "title": {"zh": zh_title, "en": en_title},
            "description": {"zh": zh_desc, "en": en_desc},
            "problemIds": [p["id"] for p in problems], "source": "https://snakify.org/en/",
        }
        (out / "chapter.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        index["chapters"].append({"id": chapter, "dir": f"chapter-{chapter}"})
        total += len(problems) - 1
        print(f"Chapter {chapter}: {len(problems) - 1} exercises")
    (DATA / "index.json").write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Imported {total} C++ exercises")


if __name__ == "__main__":
    main()
