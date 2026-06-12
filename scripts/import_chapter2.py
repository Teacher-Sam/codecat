#!/usr/bin/env python3
"""Import Snakify Chapter 2 (Integer and float numbers)."""

from snakify_import import (
    STARTER_DOUBLE,
    STARTER_INT,
    build_from_official,
    build_manual,
    write_chapter,
)

CHAPTER_META = {
    "title": {
        "zh": "整數與浮點數",
        "en": "Integer and float numbers",
    },
    "description": {
        "zh": "位數處理、小數運算、時間與時鐘角度等題型。",
        "en": "Digit manipulation, decimals, time, and clock angle problems.",
    },
    "source": "https://github.com/vpavlenko/content",
}

MANUAL = [
    {
        "id": "2-2",
        "title": {"zh": "兩個位數", "en": "Two digits"},
        "description": {
            "zh": "<p>讀入一個整數（至少兩位），輸出十位數與個位數，中間以空格分隔。</p>",
            "en": "<p>Read an integer and print its tens and units digits separated by a space.</p>",
        },
        "hint": {
            "zh": "十位：<code>n / 10</code>，個位：<code>n % 10</code>。",
            "en": "Tens: <code>n / 10</code>, units: <code>n % 10</code>.",
        },
        "starterCode": STARTER_INT,
        "tests": [
            {"input": "179", "output": "17 9"},
            {"input": "40", "output": "4 0"},
            {"input": "5", "output": "0 5"},
        ],
    },
    {
        "id": "2-3",
        "title": {"zh": "交換位數", "en": "Swap digits"},
        "description": {
            "zh": "<p>讀入一個兩位整數，輸出十位與個位交換後的數字。</p>",
            "en": "<p>Read a two-digit integer and print the number with its digits swapped.</p>",
        },
        "hint": {
            "zh": "<code>units * 10 + tens</code>",
            "en": "<code>units * 10 + tens</code>",
        },
        "starterCode": STARTER_INT,
        "tests": [
            {"input": "63", "output": "36"},
            {"input": "10", "output": "1"},
            {"input": "55", "output": "55"},
        ],
    },
    {
        "id": "2-4",
        "title": {"zh": "最後兩位數", "en": "Last two digits"},
        "description": {
            "zh": "<p>讀入一個整數，輸出它的最後兩位數（對 100 取餘）。</p>",
            "en": "<p>Read an integer and print its last two digits.</p>",
        },
        "hint": {"zh": "使用 <code>n % 100</code>。", "en": "Use <code>n % 100</code>."},
        "starterCode": STARTER_INT,
        "tests": [
            {"input": "179", "output": "79"},
            {"input": "100", "output": "0"},
            {"input": "1234", "output": "34"},
        ],
    },
    {
        "id": "2-7",
        "title": {"zh": "反轉三位數", "en": "Reverse three digits"},
        "description": {
            "zh": "<p>讀入一個三位整數，輸出數字順序反轉後的結果（保留前導零）。</p>",
            "en": "<p>Read a three-digit integer and print its digits in reverse order.</p>",
        },
        "hint": {
            "zh": "可將數字轉成字串後反轉，或逐位取出再組合。",
            "en": "Convert to string and reverse, or extract digits mathematically.",
        },
        "starterCode": STARTER_INT,
        "tests": [
            {"input": "179", "output": "971"},
            {"input": "100", "output": "001"},
            {"input": "530", "output": "035"},
        ],
    },
    {
        "id": "2-8",
        "title": {"zh": "合併兩數", "en": "Merge two numbers"},
        "description": {
            "zh": "<p>讀入兩個兩位整數，依序交替取出它們的十位、個位並串接輸出（共四位字元）。</p>",
            "en": "<p>Read two two-digit integers and merge their digits alternately.</p>",
        },
        "hint": {
            "zh": "例如 12 與 34 → <code>1324</code>。",
            "en": "Example: 12 and 34 → <code>1324</code>.",
        },
        "starterCode": STARTER_INT,
        "tests": [
            {"input": "12\n34", "output": "1324"},
            {"input": "56\n78", "output": "5768"},
            {"input": "90\n12", "output": "9102"},
        ],
    },
    {
        "id": "2-9",
        "title": {"zh": "循環移位", "en": "Cyclic rotation"},
        "description": {
            "zh": "<p>讀入一個四位整數，將最後兩位移到最前面，輸出新的四位數。</p>",
            "en": "<p>Read a four-digit integer and cyclically shift its last two digits to the front.</p>",
        },
        "hint": {
            "zh": "<code>n % 100 * 100 + n / 100</code>（整數運算）",
            "en": "<code>n % 100 * 100 + n / 100</code> (integer arithmetic)",
        },
        "starterCode": STARTER_INT,
        "tests": [
            {"input": "1234", "output": "3412"},
            {"input": "1790", "output": "9017"},
            {"input": "1200", "output": "12"},
        ],
    },
    {
        "id": "2-13",
        "title": {"zh": "星期幾", "en": "Day of the week"},
        "description": {
            "zh": "<p>已知第 1 天是星期一，讀入 <code>k</code>（第 k 天），輸出該天是星期幾（0=週一 … 6=週日）。</p>",
            "en": "<p>Day 1 is Monday. Given <code>k</code>, print the weekday index (0=Mon … 6=Sun).</p>",
        },
        "hint": {"zh": "<code>(k + 3) % 7</code>", "en": "<code>(k + 3) % 7</code>"},
        "starterCode": STARTER_INT,
        "tests": [
            {"input": "1", "output": "4"},
            {"input": "2", "output": "5"},
            {"input": "7", "output": "3"},
        ],
    },
    {
        "id": "2-16",
        "title": {"zh": "世紀", "en": "Century"},
        "description": {
            "zh": "<p>讀入年份，輸出該年屬於第幾世紀。</p>",
            "en": "<p>Read a year and print its century number.</p>",
        },
        "hint": {
            "zh": "<code>(year - 1) / 100 + 1</code>",
            "en": "<code>(year - 1) / 100 + 1</code>",
        },
        "starterCode": STARTER_INT,
        "tests": [
            {"input": "2017", "output": "21"},
            {"input": "1900", "output": "20"},
            {"input": "2000", "output": "20"},
        ],
    },
    {
        "id": "2-17",
        "title": {"zh": "蝸牛", "en": "Snail"},
        "description": {
            "zh": (
                "<p>蝸牛白天向上爬 <code>a</code> 公尺、晚上下滑 <code>b</code> 公尺（<code>a &gt; b</code>）。"
                "井深 <code>h</code> 公尺，問幾天能爬出井口？</p>"
            ),
            "en": (
                "<p>A snail climbs <code>a</code> meters by day and slips <code>b</code> meters by night "
                "(<code>a &gt; b</code>). Given well depth <code>h</code>, find days to escape.</p>"
            ),
        },
        "hint": {
            "zh": "第一天結束已在 <code>a</code> 公尺；之後每天淨增 <code>a - b</code>。",
            "en": "After day 1 the snail is at <code>a</code>; each later day net gain is <code>a - b</code>.",
        },
        "starterCode": STARTER_INT,
        "tests": [
            {"input": "10\n2\n1", "output": "9"},
            {"input": "20\n3\n2", "output": "18"},
            {"input": "100\n5\n4", "output": "96"},
        ],
    },
]

OFFICIAL = [
    (
        "int_and_float/last_digit.txt",
        "2-1",
        {"zh": "整數的最後一位", "en": "Last digit of integer"},
        "讀入一個整數，輸出它的個位數字。",
        {"zh": "使用 <code>n % 10</code>。", "en": "Use <code>n % 10</code>."},
    ),
    (
        "int_and_float/tens_digit.txt",
        "2-5",
        {"zh": "十位數字", "en": "Tens digit"},
        "讀入一個整數，輸出它的十位數字。",
        {"zh": "<code>(n / 10) % 10</code>", "en": "<code>(n / 10) % 10</code>"},
    ),
    (
        "int_and_float/sum_of_digits.txt",
        "2-6",
        {"zh": "各位數之和", "en": "Sum of digits"},
        "讀入一個三位整數，輸出各位數字之和。",
        {
            "zh": "分別取出百、十、個位再相加。",
            "en": "Extract hundreds, tens, and units digits, then sum.",
        },
    ),
    (
        "int_and_float/fractional_part.txt",
        "2-10",
        {"zh": "小數部分", "en": "Fractional part"},
        "讀入一個正實數，輸出它的小數部分。",
        {
            "zh": "可用 <code>x - (int)x</code>；注意浮點精度，必要時用字串處理。",
            "en": "Use <code>x - (int)x</code>; watch floating-point precision.",
        },
        STARTER_DOUBLE,
    ),
    (
        "int_and_float/digit_after_separator.txt",
        "2-11",
        {"zh": "小數點後第一位", "en": "First digit after decimal point"},
        "讀入一個正實數，輸出小數點右側第一位數字。",
        {
            "zh": "可用字串找 <code>.</code> 後的字元，或數學運算。",
            "en": "Parse as string after <code>.</code>, or use math.",
        },
        STARTER_DOUBLE,
    ),
    (
        "int_and_float/motor_rally.txt",
        "2-12",
        {"zh": "開車路程", "en": "Car route"},
        "汽車每天可開 N 公里，路程長 M 公里，問至少要幾天？（無法整除要加一天）",
        {
            "zh": "使用無條件進位：<code>(M + N - 1) / N</code>。",
            "en": "Ceiling division: <code>(M + N - 1) / N</code>.",
        },
    ),
    (
        "electronic_watch.txt",
        "2-14",
        {"zh": "數位時鐘", "en": "Digital clock"},
        "午夜過後經過 N 分鐘，輸出 24 小時制的小時與分鐘（兩個整數，空格分隔）。",
        {
            "zh": "<code>hours = N / 60</code>，<code>minutes = N % 60</code>。",
            "en": "<code>hours = N / 60</code>, <code>minutes = N % 60</code>.",
        },
    ),
    (
        "int_and_float/purchase_price.txt",
        "2-15",
        {"zh": "總價", "en": "Total cost"},
        "杯子蛋糕單價 A 元 B 分，買 N 個，輸出總價的元與分（兩個整數）。",
        {
            "zh": "先換算成總分：<code>N * (100*A + B)</code>，再除以 100 與取餘。",
            "en": "Total cents = <code>N * (100*A + B)</code>, then split dollars and cents.",
        },
    ),
    (
        "int_and_float/watch_1.txt",
        "2-18",
        {"zh": "時鐘角度 - 1", "en": "Clock face - 1"},
        "讀入時、分、秒（12 小時制），輸出時針角度（度，可為小數）。",
        {
            "zh": "<code>30*h + 30*m/60 + 30*s/3600</code>",
            "en": "<code>30*h + 30*m/60 + 30*s/3600</code>",
        },
        STARTER_DOUBLE,
    ),
    (
        "int_and_float/watch_2.txt",
        "2-19",
        {"zh": "時鐘角度 - 2", "en": "Clock face - 2"},
        "時針已轉過 α 度，求分針在當前這一小時內轉過的角度。",
        {
            "zh": "分針角度對 30 度取餘後再換算：<code>(alpha % 30) * 12</code>",
            "en": "<code>(alpha % 30) * 12</code>",
        },
        STARTER_DOUBLE,
    ),
]

ORDER = [
    ("official", "int_and_float/last_digit.txt"),
    ("manual", "2-2"),
    ("manual", "2-3"),
    ("manual", "2-4"),
    ("official", "int_and_float/tens_digit.txt"),
    ("official", "int_and_float/sum_of_digits.txt"),
    ("manual", "2-7"),
    ("manual", "2-8"),
    ("manual", "2-9"),
    ("official", "int_and_float/fractional_part.txt"),
    ("official", "int_and_float/digit_after_separator.txt"),
    ("official", "int_and_float/motor_rally.txt"),
    ("manual", "2-13"),
    ("official", "electronic_watch.txt"),
    ("official", "int_and_float/purchase_price.txt"),
    ("manual", "2-16"),
    ("manual", "2-17"),
    ("official", "int_and_float/watch_1.txt"),
    ("official", "int_and_float/watch_2.txt"),
]

OFFICIAL_MAP = {item[0]: item for item in OFFICIAL}
MANUAL_MAP = {p["id"]: p for p in MANUAL}


def main() -> None:
    problems = []
    for kind, key in ORDER:
        if kind == "manual":
            problems.append(build_manual(MANUAL_MAP[key]))
        else:
            entry = OFFICIAL_MAP[key]
            relpath, pid, title, zh, hint = entry[:5]
            starter = entry[5] if len(entry) > 5 else STARTER_INT
            problems.append(build_from_official(relpath, pid, title, zh, hint, starter))

    write_chapter("2", CHAPTER_META, problems)


if __name__ == "__main__":
    main()
