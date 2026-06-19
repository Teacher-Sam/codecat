#!/usr/bin/env python3
"""Import Snakify Chapter 3 (Conditions: if, then, else)."""

from snakify_import import STARTER_INT, build_from_official, write_chapter

CHAPTER_META = {
    "title": {
        "zh": "條件敘述",
        "en": "Conditions: if, then, else",
    },
    "description": {
        "zh": "if / else、比較運算、邏輯運算，以及西洋棋與閏年等題型。",
        "en": "if/else, comparisons, logical operators, chess moves, and leap year.",
    },
    "source": "https://github.com/vpavlenko/content",
}

OFFICIAL = [
    (
        "ifelse/minimum.txt",
        "3-1",
        {"zh": "兩數取小", "en": "Minimum of two numbers"},
        "讀入兩個整數，輸出較小的那一個。",
        {"zh": "若 <code>a &lt; b</code> 輸出 a，否則輸出 b。", "en": "Compare with <code>&lt;</code> or use <code>Math.min</code>."},
    ),
    (
        "ifelse/signum.txt",
        "3-2",
        {"zh": "符號函數", "en": "Sign function"},
        "讀入整數 x，輸出 1（正）、0（零）或 -1（負）。",
        {"zh": "依 x 的正負零分三支 <code>if</code>。", "en": "Three branches for positive, zero, negative."},
    ),
    (
        "ifelse/minimum3.txt",
        "3-3",
        {"zh": "三數取小", "en": "Minimum of three numbers"},
        "讀入三個整數，輸出最小值。",
        {"zh": "可先比較兩個，再與第三個比。", "en": "Compare pairs, or use nested <code>if</code>."},
    ),
    (
        "ifelse/num_equal.txt",
        "3-4",
        {"zh": "相等個數", "en": "Equal numbers"},
        "讀入三個整數，輸出有幾對數字相等（0、1 或 3）。",
        {"zh": "檢查 <code>a==b</code>、<code>a==c</code>、<code>b==c</code>。", "en": "Count how many pairs are equal."},
    ),
    (
        "ifelse/rook_move.txt",
        "3-5",
        {"zh": "車的走法", "en": "Rook move"},
        "棋盤上兩格 (x1,y1)、(x2,y2)，判斷車能否一步走到（同一行或同一列），輸出 YES/NO。",
        {"zh": "同一行：<code>x1==x2</code>；同一列：<code>y1==y2</code>。", "en": "Same row or same column."},
    ),
    (
        "ifelse/chess_board.txt",
        "3-6",
        {"zh": "棋盤同色", "en": "Chess board - same color"},
        "讀入兩格座標，判斷是否同色，輸出 YES/NO。",
        {"zh": "同色 ⟺ 兩格 (x+y) 的奇偶性相同。", "en": "Same color iff <code>(x1+y1)%2 == (x2+y2)%2</code>."},
    ),
    (
        "ifelse/king_move.txt",
        "3-7",
        {"zh": "王的走法", "en": "King move"},
        "判斷王能否從 (x1,y1) 一步走到 (x2,y2)，輸出 YES/NO。",
        {"zh": "兩座標差均 ≤ 1 且不全相同。", "en": "Chebyshev distance 1 (not same cell)."},
    ),
    (
        "ifelse/bishop_move.txt",
        "3-8",
        {"zh": "象的走法", "en": "Bishop move"},
        "判斷象能否一步斜走至 (x2,y2)，輸出 YES/NO。",
        {"zh": "斜線：<code>|x1-x2| == |y1-y2|</code> 且不同格。", "en": "Same diagonal, different cells."},
    ),
    (
        "ifelse/queen_move.txt",
        "3-9",
        {"zh": "后的走法", "en": "Queen move"},
        "判斷后能否一步走到 (x2,y2)，輸出 YES/NO。",
        {"zh": "同行、同列或同對角線。", "en": "Rook move or bishop move."},
    ),
    (
        "ifelse/knight_move.txt",
        "3-10",
        {"zh": "馬的走法", "en": "Knight move"},
        "判斷馬能否一步 L 形走到 (x2,y2)，輸出 YES/NO。",
        {"zh": "一軸差 2、另一軸差 1。", "en": "One axis diff 2, other diff 1."},
    ),
    (
        "ifelse/chocolate.txt",
        "3-11",
        {"zh": "巧克力", "en": "Chocolate bar"},
        "矩形巧克力 N×M 格，一次只能沿格線直向或橫向掰開，問至少掰幾次能分成 1×1。",
        {"zh": "每次掰開只增加一塊，答案為 <code>N*M - 1</code>。", "en": "Each break adds one piece: <code>N*M - 1</code>."},
    ),
    (
        "ifelse/leap_year.txt",
        "3-12",
        {"zh": "閏年", "en": "Leap year"},
        "讀入年份，依格里曆規則輸出 LEAP 或 COMMON（全大寫）。",
        {
            "zh": "能被 400 整除 → LEAP；能被 100 整除 → COMMON；能被 4 整除 → LEAP。",
            "en": "Divisible by 400 → LEAP; by 100 → COMMON; by 4 → LEAP.",
        },
    ),
]

ORDER = [("official", item[0]) for item in OFFICIAL]
OFFICIAL_MAP = {item[0]: item for item in OFFICIAL}


def main() -> None:
    problems = []
    for kind, key in ORDER:
        entry = OFFICIAL_MAP[key]
        relpath, pid, title, zh, hint = entry[:5]
        starter = entry[5] if len(entry) > 5 else STARTER_INT
        problems.append(build_from_official(relpath, pid, title, zh, hint, starter))

    write_chapter("3", CHAPTER_META, problems)


if __name__ == "__main__":
    main()
