#!/usr/bin/env python3
"""Import Snakify Chapter 4 (For loop with range) — full 18 problems."""

from __future__ import annotations

import ast
import re
import urllib.request
from pathlib import Path

from snakify_import import (
    DATA,
    STARTER_INT,
    build_from_official,
    write_chapter,
)

LESSON = "for_loop_range"
HEADERS = {"User-Agent": "Mozilla/5.0"}

CHAPTER_META = {
    "title": {
        "zh": "for 迴圈",
        "en": "For loop with range",
    },
    "description": {
        "zh": "重複執行、累加、階乘、質數與數列輸出（共 18 題，含加碼題）。",
        "en": "Repetition, sums, factorials, primes, and sequences (18 problems, incl. bonus).",
    },
    "source": "https://github.com/vpavlenko/content",
}

# Snakify Lesson 4 curriculum order (matches snakify.org sidebar).
ORDER: list[tuple[str, str | None]] = [
    ("count_to_n", None),
    ("series_1", "for/series_1.txt"),
    ("first_n_odd_ascending", None),
    ("series_2", "for/series_2.txt"),
    ("first_n_even_descending", None),
    ("sum_of_ten_numbers", "for/sum_of_ten_numbers.txt"),
    ("sum_of_n_numbers", "for/sum_of_n_numbers.txt"),
    ("product_of_n_numbers", None),
    ("sum_of_cubes", "for/sum_of_cubes.txt"),
    ("factorial", "for/factorial.txt"),
    ("how_many_zeroes", "for/how_many_zeroes.txt"),
    ("sum_of_factorials", "for/sum_of_factorials.txt"),
    ("squares_in_range", None),
    ("ladder", "for/ladder.txt"),
    ("is_prime", None),
    ("print_primes_in_range", None),
    ("num_primes_in_range", None),
    ("lost_card", "for/lost_card.txt"),
]

# slug -> (title dict, zh description, hint dict)
META: dict[str, tuple[dict, str, dict]] = {
    "count_to_n": (
        {"zh": "數到 N", "en": "Count to N"},
        "讀入整數 n，依序輸出 1 到 n，每個數字一行。",
        {"zh": "<code>for (int i = 1; i &lt;= n; i++)</code>", "en": "Loop from 1 to n inclusive."},
    ),
    "series_1": (
        {"zh": "數列 - 1", "en": "Series - 1"},
        "讀入 A、B（A ≤ B），由小到大輸出 A 到 B 的所有整數，數字間以空格分隔（末尾保留一空格）。",
        {"zh": "<code>for (int i = A; i &lt;= B; i++)</code>", "en": "Print from A to B with spaces."},
    ),
    "first_n_odd_ascending": (
        {"zh": "前 N 個奇數（遞增）", "en": "First N odd, ascending"},
        "讀入 n，由小到大輸出前 n 個奇數，每個一行（1, 3, 5, …）。",
        {"zh": "步長 2：<code>for (int i = 1; i &lt;= 2*n - 1; i += 2)</code>", "en": "Step by 2 starting at 1."},
    ),
    "series_2": (
        {"zh": "數列 - 2", "en": "Series - 2"},
        "讀入 A、B：若 A &lt; B 由小到大；若 A ≥ B 由大到小。數字間以空格分隔（末尾保留一空格）。",
        {"zh": "依 A、B 大小選 <code>i++</code> 或 <code>i--</code>。", "en": "Ascending or descending loop."},
    ),
    "first_n_even_descending": (
        {"zh": "前 N 個偶數（遞減）", "en": "First N even, descending"},
        "讀入 n，由大到小輸出前 n 個偶數，每個一行（2n, 2n−2, …, 2）。",
        {"zh": "從 <code>2*n</code> 往下，步長 −2。", "en": "Start at 2n, step −2."},
    ),
    "sum_of_ten_numbers": (
        {"zh": "十個數之和", "en": "Sum of ten numbers"},
        "讀入 10 個整數並輸出總和。盡可能少用變數。",
        {"zh": "一個累加變數 + 10 次迴圈。", "en": "One accumulator, loop 10 times."},
    ),
    "sum_of_n_numbers": (
        {"zh": "N 個數之和", "en": "Sum of N numbers"},
        "第一行為 N，接著 N 行各一個整數。讀入並輸出總和。",
        {"zh": "先讀 N，再迴圈讀 N 次累加。", "en": "Read N, then sum N integers."},
    ),
    "product_of_n_numbers": (
        {"zh": "N 個數之積", "en": "Product of N numbers"},
        "第一行為 N，接著 N 個整數。輸出它們的乘積。",
        {"zh": "累乘初值設 1。", "en": "Multiply in a loop; start from 1."},
    ),
    "sum_of_cubes": (
        {"zh": "立方和", "en": "Sum of cubes"},
        "讀入 N，計算 1³ + 2³ + … + N³ 並輸出。",
        {"zh": "累加 <code>i * i * i</code>。", "en": "Accumulate <code>i * i * i</code>."},
    ),
    "factorial": (
        {"zh": "階乘", "en": "Factorial"},
        "讀入 n，計算 n! 並輸出。請勿使用 Math 函式庫捷徑。",
        {"zh": "用 <code>for</code> 累乘。", "en": "Multiply in a loop."},
    ),
    "how_many_zeroes": (
        {"zh": "零的個數", "en": "The number of zeros"},
        "第一行 N，接著 N 個整數。統計<strong>等於 0</strong> 的個數（不是零的位數）。",
        {"zh": "每讀一數，若為 0 則 +1。", "en": "Count values equal to zero."},
    ),
    "sum_of_factorials": (
        {"zh": "階乘和", "en": "Adding factorials"},
        "讀入 n，輸出 1! + 2! + … + n!。單一迴圈完成，勿用 math 函式庫。",
        {"zh": "維護「當前階乘」與累加和。", "en": "Running factorial and sum."},
    ),
    "squares_in_range": (
        {"zh": "範圍內平方", "en": "Squares in range"},
        "讀入 A、B，對每個 i（A ≤ i ≤ B）輸出一行 <code>i*i=結果</code>（格式如 <code>3*3=9</code>）。",
        {"zh": "外層 <code>for</code> 從 A 到 B，每行 <code>System.out.println(i + \"*\" + i + \"=\" + (i*i));</code>", "en": "Print i*i=… for each i in range."},
    ),
    "ladder": (
        {"zh": "階梯", "en": "Ladder"},
        "讀入 n（n ≤ 9），輸出 n 階階梯：第 k 階為 1～k 連續數字（無空格），每階一行。",
        {"zh": "雙層 <code>for</code>，內層用 <code>print</code>。", "en": "Nested loops with print."},
    ),
    "is_prime": (
        {"zh": "是否質數", "en": "Is prime"},
        "讀入整數 n（n ≥ 2），若為質數輸出 <code>PRIME</code>，否則 <code>COMPOSITE</code>（全大寫）。",
        {"zh": "用 <code>for</code> 從 2 試除到 √n 或 n−1。", "en": "Trial division from 2 upward."},
    ),
    "print_primes_in_range": (
        {"zh": "列印範圍內質數", "en": "Print primes in range"},
        "讀入 A、B，由小到大輸出 [A, B] 內所有質數，每個一行。",
        {"zh": "對每個 i 檢查是否質數。", "en": "Check primality for each i."},
    ),
    "num_primes_in_range": (
        {"zh": "範圍內質數個數", "en": "Number of primes in range"},
        "讀入 A、B，輸出 [A, B] 內質數的個數。",
        {"zh": "與上一題類似，符合質數則計數 +1。", "en": "Count primes in the interval."},
    ),
    "lost_card": (
        {"zh": "遺失的牌", "en": "Lost card"},
        "原有一副 1～N 的牌少一張。讀入 N 及剩餘 N−1 張號碼，輸出遺失的那張。",
        {"zh": "1～N 的和減去已給數字之和。", "en": "Sum 1..N minus given sum."},
    ),
}

# Snakify URL slug may differ from our logical slug.
SNAKIFY_SLUG: dict[str, str] = {
    "sum_of_n_numbers": "suf_of_n_numbers",
}


def fetch_snakify(slug: str) -> tuple[str, list[dict]]:
    url_slug = SNAKIFY_SLUG.get(slug, slug)
    url = f"https://snakify.org/en/lessons/{LESSON}/problems/{url_slug}/"
    html = urllib.request.urlopen(urllib.request.Request(url, headers=HEADERS), timeout=30).read().decode(
        "utf-8", "replace"
    )
    title_m = re.search(r'Solve problem "([^"]+)" online', html)
    en_title = title_m.group(1) if title_m else slug.replace("_", " ").title()
    tests_m = re.search(r"window\.tests\s*=\s*(\[.*?\]);", html, re.S)
    if not tests_m:
        raise ValueError(f"No window.tests for {slug} ({url})")
    raw = ast.literal_eval(tests_m.group(1))
    tests = [{"input": t.get("input", ""), "output": t["answer"]} for t in raw]
    return en_title, tests


def build_snakify(slug: str, pid: str) -> dict:
    title, hint = META[slug][0], META[slug][2]
    zh = META[slug][1]
    en_title, tests = fetch_snakify(slug)
    title = {**title, "en": en_title}
    url_slug = SNAKIFY_SLUG.get(slug, slug)
    return {
        "id": pid,
        "title": title,
        "description": {
            "zh": f"<p>{zh}</p>",
            "en": f"<p>{en_title}.</p>",
        },
        "hint": hint,
        "starterCode": STARTER_INT,
        "tests": tests,
        "source": f"snakify.org/en/lessons/{LESSON}/problems/{url_slug}/",
    }


def cleanup_orphans(chapter_dir: Path, keep_ids: set[str]) -> None:
    for path in chapter_dir.glob("java-4-*.json"):
        if path.stem not in keep_ids:
            path.unlink()
            print(f"Removed orphan {path.name}")


def main() -> None:
    problems = []
    keep_ids = {"java-4-0"}

    for index, (slug, source) in enumerate(ORDER, start=1):
        pid = f"4-{index}"
        keep_ids.add(f"java-{pid}")
        title, zh, hint = META[slug][0], META[slug][1], META[slug][2]

        if source:
            problems.append(build_from_official(source, pid, title, zh, hint, STARTER_INT))
        else:
            problems.append(build_snakify(slug, pid))

    chapter_dir = DATA / "chapter-4"
    cleanup_orphans(chapter_dir, keep_ids)
    write_chapter("4", CHAPTER_META, problems)


if __name__ == "__main__":
    main()
