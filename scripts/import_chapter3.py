#!/usr/bin/env python3
"""Import Snakify Chapter 3 (Conditions: if, then, else) — full 32 problems."""

from __future__ import annotations

import ast
import json
import re
import urllib.request
from pathlib import Path

from snakify_import import (
    DATA,
    STARTER_INT,
    build_from_official,
    build_manual,
    download_problem_images,
    enrich_description_html,
    image_file_for_slug,
    write_chapter,
)

LESSON = "if_then_else_conditions"
HEADERS = {"User-Agent": "Mozilla/5.0"}

CHAPTER_META = {
    "title": {
        "zh": "條件敘述",
        "en": "Conditions: if, then, else",
    },
    "description": {
        "zh": "if / else、比較與邏輯運算、西洋棋走法、閏年等（共 32 題）。",
        "en": "if/else, comparisons, logic, chess moves, leap year, and more (32 problems).",
    },
    "source": "https://github.com/vpavlenko/content",
}

# Snakify Lesson 3 order (bonus problems interleaved; matches snakify.org curriculum).
ORDER: list[tuple[str, str | None]] = [
    ("is_positive", None),
    ("is_odd", None),
    ("is_even", None),
    ("ends_on_seven", None),
    ("minimum", "ifelse/minimum.txt"),
    ("are_both_odd", None),
    ("at_least_one_odd", None),
    ("exactly_one_odd", None),
    ("signum", "ifelse/signum.txt"),
    ("numbers_in_ascending_order", "manual"),
    ("is_three_digit", None),
    ("minimum3", "ifelse/minimum3.txt"),
    ("num_equal", "ifelse/num_equal.txt"),
    ("rook_move", "ifelse/rook_move.txt"),
    ("chess_board_black", "manual"),
    ("chess_board", "ifelse/chess_board.txt"),
    ("king_move", "ifelse/king_move.txt"),
    ("bishop_move", "ifelse/bishop_move.txt"),
    ("queen_move", "ifelse/queen_move.txt"),
    ("knight_move", "ifelse/knight_move.txt"),
    ("pawn_move", None),
    ("distance_to_closest_point", "manual"),
    ("digits_in_ascending_order", "manual"),
    ("four_digit_palindrome", None),
    ("index_of_outlier", None),
    ("chocolate", "ifelse/chocolate.txt"),
    ("leap_year", "ifelse/leap_year.txt"),
    ("days_in_month", None),
    ("next_day", None),
    ("linear_equation", None),
    ("vertices_of_rectangle", None),
    ("sort_three_numbers", None),
]

MANUAL: dict[str, dict] = {
    "numbers_in_ascending_order": {
        "title": {"zh": "三數遞增", "en": "Numbers in ascending order"},
        "description": {
            "zh": "<p>讀入三個整數，若嚴格遞增（a &lt; b &lt; c）輸出 YES，否則 NO。</p>",
            "en": "<p>Given three integers, print <code>YES</code> if they are strictly in ascending order, otherwise <code>NO</code>.</p>",
        },
        "hint": {
            "zh": "<code>a &lt; b &amp;&amp; b &lt; c</code>",
            "en": "<code>a &lt; b and b &lt; c</code>",
        },
        "starterCode": STARTER_INT,
        "tests": [
            {"input": "1\n2\n3", "output": "YES"},
            {"input": "3\n2\n1", "output": "NO"},
            {"input": "1\n2\n2", "output": "NO"},
            {"input": "5\n6\n7", "output": "YES"},
            {"input": "-1\n0\n1", "output": "YES"},
            {"input": "10\n5\n20", "output": "NO"},
            {"input": "2\n2\n2", "output": "NO"},
            {"input": "100\n101\n102", "output": "YES"},
        ],
        "source": "snakify.org Lesson 3 bonus (iT 邦幫忙 Day7)",
    },
    "chess_board_black": {
        "title": {"zh": "棋格顏色", "en": "Chess board - black square"},
        "description": {
            "zh": "<p>讀入棋盤一格的欄、列座標（1～8），輸出該格顏色 <code>BLACK</code> 或 <code>WHITE</code>。</p>",
            "en": "<p>Given a chessboard cell column and row (1–8), print <code>BLACK</code> or <code>WHITE</code>.</p>",
        },
        "hint": {
            "zh": "同色 ⟺ <code>row % 2 == column % 2</code> → BLACK。",
            "en": "Same parity of row and column → <code>BLACK</code>.",
        },
        "starterCode": STARTER_INT,
        "tests": [
            {"input": "1\n1", "output": "BLACK"},
            {"input": "1\n2", "output": "WHITE"},
            {"input": "2\n1", "output": "WHITE"},
            {"input": "2\n2", "output": "BLACK"},
            {"input": "7\n8", "output": "WHITE"},
            {"input": "8\n8", "output": "BLACK"},
            {"input": "3\n5", "output": "BLACK"},
            {"input": "4\n7", "output": "WHITE"},
        ],
        "source": "snakify.org Lesson 3 bonus (iT 邦幫忙 Day8)",
    },
    "distance_to_closest_point": {
        "title": {"zh": "最近點距離", "en": "Distance to closest point"},
        "description": {
            "zh": "<p>讀入直線上三個整數座標 a、b、c，輸出 a 到 b、c 中較近者的距離。</p>",
            "en": "<p>Given three integers a, b, c on a line, print the distance from a to whichever of b or c is closer.</p>",
        },
        "hint": {
            "zh": "<code>min(|a-b|, |a-c|)</code>，相等時輸出 <code>|a-b|</code>。",
            "en": "<code>min(abs(a-b), abs(a-c))</code>; if equal, print <code>abs(a-b)</code>.",
        },
        "starterCode": STARTER_INT,
        "tests": [
            {"input": "1\n5\n3", "output": "2"},
            {"input": "0\n10\n0", "output": "0"},
            {"input": "5\n5\n9", "output": "0"},
            {"input": "-1\n3\n-5", "output": "4"},
            {"input": "10\n2\n15", "output": "5"},
            {"input": "7\n7\n7", "output": "0"},
            {"input": "3\n8\n1", "output": "2"},
            {"input": "-10\n-5\n-20", "output": "5"},
        ],
        "source": "snakify.org Lesson 3 bonus (iT 邦幫忙 Day9)",
    },
    "digits_in_ascending_order": {
        "title": {"zh": "數字遞增", "en": "Digits in ascending order"},
        "description": {
            "zh": "<p>讀入三位整數，若各位數字由左到右嚴格遞增輸出 YES，否則 NO。</p>",
            "en": "<p>Given a three-digit integer, print <code>YES</code> if its digits are strictly ascending left to right, otherwise <code>NO</code>.</p>",
        },
        "hint": {
            "zh": "百位 &lt; 十位 &lt; 個位。",
            "en": "Hundreds &lt; tens &lt; units digit.",
        },
        "starterCode": STARTER_INT,
        "tests": [
            {"input": "123", "output": "YES"},
            {"input": "321", "output": "NO"},
            {"input": "159", "output": "YES"},
            {"input": "135", "output": "YES"},
            {"input": "132", "output": "NO"},
            {"input": "111", "output": "NO"},
            {"input": "100", "output": "NO"},
            {"input": "579", "output": "YES"},
        ],
        "source": "snakify.org Lesson 3 bonus (iT 邦幫忙 Day9)",
    },
}

# zh title, zh description, hint zh, hint en
META: dict[str, tuple[dict, str, dict]] = {
    "is_positive": (
        {"zh": "是否為正數", "en": "Is positive"},
        "讀入整數，若為正數輸出 YES，否則輸出 NO。",
        {"zh": "使用 <code>if (a &gt; 0)</code>。", "en": "Use <code>if (a &gt; 0)</code>."},
    ),
    "is_odd": (
        {"zh": "是否為奇數", "en": "Is odd"},
        "讀入整數，若為奇數輸出 YES，否則輸出 NO。",
        {"zh": "奇數：<code>a % 2 != 0</code>。", "en": "Odd: <code>a % 2 != 0</code>."},
    ),
    "is_even": (
        {"zh": "是否為偶數", "en": "Is even"},
        "讀入整數，若為偶數輸出 YES，否則輸出 NO。",
        {"zh": "偶數：<code>a % 2 == 0</code>。", "en": "Even: <code>a % 2 == 0</code>."},
    ),
    "ends_on_seven": (
        {"zh": "個位是 7", "en": "Ends on seven"},
        "讀入整數，若個位數字是 7 輸出 YES，否則 NO。",
        {"zh": "<code>(a - 7) % 10 == 0</code> 或 <code>a % 10 == 7</code>。", "en": "Check the units digit."},
    ),
    "minimum": (
        {"zh": "兩數取小", "en": "Minimum of two numbers"},
        "讀入兩個整數，輸出較小的那一個。",
        {"zh": "若 <code>a &lt; b</code> 輸出 a，否則輸出 b。", "en": "Compare with <code>&lt;</code> or use <code>Math.min</code>."},
    ),
    "are_both_odd": (
        {"zh": "兩數皆奇", "en": "Are both odd"},
        "讀入兩個整數，若兩者都是奇數輸出 YES，否則 NO。",
        {"zh": "<code>a % 2 != 0 &amp;&amp; b % 2 != 0</code>", "en": "Both odd with <code>&amp;&amp;</code>."},
    ),
    "at_least_one_odd": (
        {"zh": "至少一奇", "en": "At least one odd"},
        "讀入兩個整數，若至少一個是奇數輸出 YES，否則 NO。",
        {"zh": "<code>a % 2 != 0 || b % 2 != 0</code>", "en": "Use logical OR."},
    ),
    "exactly_one_odd": (
        {"zh": "恰有一奇", "en": "Exactly one odd"},
        "讀入兩個整數，若恰有一個是奇數輸出 YES，否則 NO。",
        {"zh": "一奇一偶：<code>(a%2)!=(b%2)</code>。", "en": "XOR pattern on parity."},
    ),
    "signum": (
        {"zh": "符號函數", "en": "Sign function"},
        "讀入整數 x，輸出 1（正）、0（零）或 -1（負）。",
        {"zh": "依 x 的正負零分三支 <code>if</code>。", "en": "Three branches for positive, zero, negative."},
    ),
    "is_three_digit": (
        {"zh": "是否三位數", "en": "Is three digit"},
        "讀入整數，若為三位數（100～999）輸出 YES，否則 NO。",
        {"zh": "<code>100 &lt;= a &amp;&amp; a &lt;= 999</code>", "en": "Check the range 100–999."},
    ),
    "minimum3": (
        {"zh": "三數取小", "en": "Minimum of three numbers"},
        "讀入三個整數，輸出最小值。",
        {"zh": "可先比較兩個，再與第三個比。", "en": "Compare pairs, or use nested <code>if</code>."},
    ),
    "num_equal": (
        {"zh": "相等個數", "en": "Equal numbers"},
        "讀入三個整數，輸出有幾對數字相等（0、1 或 3）。",
        {"zh": "檢查 <code>a==b</code>、<code>a==c</code>、<code>b==c</code>。", "en": "Count how many pairs are equal."},
    ),
    "rook_move": (
        {"zh": "車的走法", "en": "Rook move"},
        "棋盤上兩格 (x1,y1)、(x2,y2)，判斷車能否一步走到（同一行或同一列），輸出 YES/NO。",
        {"zh": "同一行：<code>x1==x2</code>；同一列：<code>y1==y2</code>。", "en": "Same row or same column."},
    ),
    "chess_board": (
        {"zh": "棋盤同色", "en": "Chess board - same color"},
        "讀入兩格座標，判斷是否同色，輸出 YES/NO。",
        {"zh": "同色 ⟺ 兩格 (x+y) 的奇偶性相同。", "en": "Same color iff <code>(x1+y1)%2 == (x2+y2)%2</code>."},
    ),
    "king_move": (
        {"zh": "王的走法", "en": "King move"},
        "判斷王能否從 (x1,y1) 一步走到 (x2,y2)，輸出 YES/NO。",
        {"zh": "兩座標差均 ≤ 1 且不全相同。", "en": "Chebyshev distance 1 (not same cell)."},
    ),
    "bishop_move": (
        {"zh": "象的走法", "en": "Bishop move"},
        "判斷象能否一步斜走至 (x2,y2)，輸出 YES/NO。",
        {"zh": "斜線：<code>|x1-x2| == |y1-y2|</code> 且不同格。", "en": "Same diagonal, different cells."},
    ),
    "queen_move": (
        {"zh": "后的走法", "en": "Queen move"},
        "判斷后能否一步走到 (x2,y2)，輸出 YES/NO。",
        {"zh": "同行、同列或同對角線。", "en": "Rook move or bishop move."},
    ),
    "knight_move": (
        {"zh": "馬的走法", "en": "Knight move"},
        "判斷馬能否一步 L 形走到 (x2,y2)，輸出 YES/NO。",
        {"zh": "一軸差 2、另一軸差 1。", "en": "One axis diff 2, other diff 1."},
    ),
    "chocolate": (
        {"zh": "巧克力", "en": "Chocolate bar"},
        "矩形巧克力 N×M 格，一次只能沿格線直向或橫向掰開，問至少掰幾次能分成 1×1。",
        {"zh": "每次掰開只增加一塊，答案為 <code>N*M - 1</code>。", "en": "Each break adds one piece: <code>N*M - 1</code>."},
    ),
    "leap_year": (
        {"zh": "閏年", "en": "Leap year"},
        "讀入年份，依格里曆規則輸出 LEAP 或 COMMON（全大寫）。",
        {
            "zh": "能被 400 整除 → LEAP；能被 100 整除 → COMMON；能被 4 整除 → LEAP。",
            "en": "Divisible by 400 → LEAP; by 100 → COMMON; by 4 → LEAP.",
        },
    ),
    "sort_three_numbers": (
        {"zh": "三數排序", "en": "Sort three numbers"},
        "讀入三個整數，由小到大輸出（空格分隔）。",
        {"zh": "可用 <code>if</code> 比較後依序輸出。", "en": "Compare and print in ascending order."},
    ),
    "four_digit_palindrome": (
        {"zh": "四位回文數", "en": "Four-digit palindrome"},
        "讀入四位整數，判斷是否回文（正讀反讀相同），輸出 YES/NO。",
        {"zh": "比較千位與個位、百位與十位。", "en": "Compare first/last and middle digits."},
    ),
    "index_of_outlier": (
        {"zh": "離群值位置", "en": "Index of outlier"},
        "三個相異整數中恰有一個與另兩個不同，輸出它的位置（1、2 或 3）。",
        {"zh": "找出與另外兩個都不相等的數。", "en": "Find the value unlike the other two."},
    ),
    "days_in_month": (
        {"zh": "月份天數", "en": "Days in month"},
        "讀入月份（1～12），輸出該月天數（不考慮閏年 2 月）。",
        {"zh": "2 月 28 天；4、6、9、11 月 30 天；其餘 31 天。", "en": "Use <code>if</code> / <code>else if</code> by month."},
    ),
    "next_day": (
        {"zh": "隔日", "en": "Next day"},
        "讀入年、月、日，輸出下一天的 y m d（需處理月底與閏年）。",
        {"zh": "先處理日 +1，若超過當月天數則進位。", "en": "Increment day, roll month/year when needed."},
    ),
    "linear_equation": (
        {"zh": "一次方程", "en": "Linear equation"},
        "解 ax + b = 0，輸出 x（題目保證 a ≠ 0）。",
        {"zh": "<code>x = -b.0 / a</code>（注意整除與浮點）。", "en": "<code>x = -b.0 / a</code>."},
    ),
    "vertices_of_rectangle": (
        {"zh": "矩形第四頂點", "en": "Vertices of rectangle"},
        "給定矩形三個頂點座標 (x,y)，輸出第四個頂點。",
        {"zh": "矩形對邊平行；找出缺少的角點。", "en": "Use parallelogram / rectangle geometry."},
    ),
    "numbers_in_ascending_order": (
        {"zh": "三數遞增", "en": "Numbers in ascending order"},
        "讀入三個整數，若嚴格遞增輸出 YES，否則 NO。",
        {"zh": "<code>a &lt; b &amp;&amp; b &lt; c</code>", "en": "<code>a &lt; b and b &lt; c</code>"},
    ),
    "chess_board_black": (
        {"zh": "棋格顏色", "en": "Chess board - black square"},
        "讀入棋盤一格座標，輸出 BLACK 或 WHITE。",
        {"zh": "<code>row % 2 == column % 2</code> → BLACK。", "en": "Same row/column parity → BLACK."},
    ),
    "pawn_move": (
        {"zh": "白兵走法", "en": "White pawn move"},
        "判斷白兵能否從 (x1,y1) 一步走到 (x2,y2)，輸出 YES/NO。",
        {"zh": "直走一格、起點 y=2 可直走兩格、斜走吃子。", "en": "Forward 1, from row 2 forward 2, diagonal capture."},
    ),
    "distance_to_closest_point": (
        {"zh": "最近點距離", "en": "Distance to closest point"},
        "讀入直線上三點 a、b、c，輸出 a 到 b、c 中較近者的距離。",
        {"zh": "<code>min(|a-b|, |a-c|)</code>", "en": "<code>min(abs(a-b), abs(a-c))</code>"},
    ),
    "digits_in_ascending_order": (
        {"zh": "數字遞增", "en": "Digits in ascending order"},
        "讀入三位整數，若各位由左到右嚴格遞增輸出 YES，否則 NO。",
        {"zh": "百位 &lt; 十位 &lt; 個位。", "en": "Hundreds &lt; tens &lt; units."},
    ),
}


def fetch_snakify(slug: str) -> tuple[str, list[dict]]:
    url = f"https://snakify.org/en/lessons/{LESSON}/problems/{slug}/"
    html = urllib.request.urlopen(urllib.request.Request(url, headers=HEADERS), timeout=30).read().decode(
        "utf-8", "replace"
    )
    title_m = re.search(r'Solve problem "([^"]+)" online', html)
    en_title = title_m.group(1) if title_m else slug.replace("_", " ").title()
    tests_m = re.search(r"window\.tests\s*=\s*(\[.*?\]);", html, re.S)
    if not tests_m:
        raise ValueError(f"No window.tests for {slug}")
    raw = ast.literal_eval(tests_m.group(1))
    tests = [{"input": t.get("input", ""), "output": t["answer"]} for t in raw]
    return en_title, tests


def build_snakify(slug: str, pid: str) -> dict:
    title, hint = META[slug][0], META[slug][2]
    zh = META[slug][1]
    en_title, tests = fetch_snakify(slug)
    title = {**title, "en": en_title}
    image_file = image_file_for_slug(slug)
    return {
        "id": pid,
        "title": title,
        "description": {
            "zh": enrich_description_html(f"<p>{zh}</p>", image_file),
            "en": enrich_description_html(f"<p>{en_title}.</p>", image_file),
        },
        "hint": hint,
        "starterCode": STARTER_INT,
        "tests": tests,
        "source": f"snakify.org/en/lessons/{LESSON}/problems/{slug}/",
    }


def cleanup_orphans(chapter_dir: Path, keep_ids: set[str]) -> None:
    for path in chapter_dir.glob("java-3-*.json"):
        if path.stem not in keep_ids and path.stem != "java-3-0":
            path.unlink()
            print(f"Removed orphan {path.name}")


def main() -> None:
    download_problem_images()
    problems = []
    keep_ids = {"java-3-0"}

    for index, (slug, source) in enumerate(ORDER, start=1):
        pid = f"3-{index}"
        keep_ids.add(f"java-{pid}")
        title, zh, hint = META[slug][0], META[slug][1], META[slug][2]

        if source == "manual":
            item = {**MANUAL[slug], "id": pid}
            image_file = image_file_for_slug(slug)
            item["description"] = {
                "zh": enrich_description_html(item["description"]["zh"], image_file),
                "en": enrich_description_html(item["description"]["en"], image_file),
            }
            problems.append(build_manual(item))
        elif source:
            problems.append(build_from_official(source, pid, title, zh, hint, STARTER_INT))
        else:
            problems.append(build_snakify(slug, pid))

    chapter_dir = DATA / "chapter-3"
    cleanup_orphans(chapter_dir, keep_ids)
    write_chapter("3", CHAPTER_META, problems)


if __name__ == "__main__":
    main()
