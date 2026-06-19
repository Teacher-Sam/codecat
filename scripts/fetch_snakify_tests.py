#!/usr/bin/env python3
"""Fetch test cases from Snakify problem pages (window.tests in HTML).

Snakify embeds tests in public problem pages — no login required for inout problems.
Official .txt files in vpavify/content remain the source of truth when available.
"""

from __future__ import annotations

import ast
import json
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
JAVA_DATA = ROOT / "java" / "data"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ),
}

# Snakify lesson slug -> our chapter number
LESSONS = {
    "print_input_numbers": "1",
    "integer_float_numbers": "2",
    "if_then_else_conditions": "3",
}

# Snakify problem slug -> bare problem id (chapter-local, e.g. "1-2")
SNAKIFY_SLUG_TO_ID: dict[str, str] = {
    # Chapter 1
    "aplusbplusc": "1-1",
    "hi_john": "1-2",
    "square": "1-3",
    "area_of_right_triangle": "1-4",
    "hello_harry": "1-5",
    "apple_sharing": "1-6",
    "previous_and_next": "1-7",
    "two_timestamps": "1-8",
    "school_desks": "1-9",
    # Chapter 2 (official + manual on Snakify)
    "last_digit": "2-1",
    "two_digits": "2-2",
    "swap_digits": "2-3",
    "last_two_digits": "2-4",
    "tens_digit": "2-5",
    "sum_of_digits": "2-6",
    "reverse_three_digits": "2-7",
    "merge_two_numbers": "2-8",
    "cyclic_rotation": "2-9",
    "fractional_part": "2-10",
    "digit_after_decimal_point": "2-11",
    "car_route": "2-12",
    "day_of_week": "2-13",
    "digital_clock": "2-14",
    "total_cost": "2-15",
    "century": "2-16",
    "snail": "2-17",
    "clock_face_1": "2-18",
    "clock_face_2": "2-19",
    # Chapter 3
    "is_positive": "3-1",
    "is_odd": "3-2",
    "is_even": "3-3",
    "ends_on_seven": "3-4",
    "minimum": "3-5",
    "are_both_odd": "3-6",
    "at_least_one_odd": "3-7",
    "exactly_one_odd": "3-8",
    "signum": "3-9",
    "is_three_digit": "3-10",
    "minimum3": "3-11",
    "num_equal": "3-12",
    "rook_move": "3-13",
    "chess_board": "3-14",
    "king_move": "3-15",
    "bishop_move": "3-16",
    "queen_move": "3-17",
    "knight_move": "3-18",
    "chocolate": "3-19",
    "leap_year": "3-20",
    "sort_three_numbers": "3-21",
    "four_digit_palindrome": "3-22",
    "index_of_outlier": "3-23",
    "days_in_month": "3-24",
    "next_day": "3-25",
    "linear_equation": "3-26",
    "vertices_of_rectangle": "3-27",
    "numbers_in_ascending_order": "3-28",
    "chess_board_black": "3-29",
    "pawn_move": "3-30",
    "distance_to_closest_point": "3-31",
    "digits_in_ascending_order": "3-32",
}

# Problems we already import from vpavlenko/content .txt — skip unless --all
OFFICIAL_TXT_IDS = frozenset(
    {
        "1-1",
        "1-4",
        "1-5",
        "1-6",
        "1-7",
        "1-9",
        "2-1",
        "2-5",
        "2-6",
        "2-10",
        "2-11",
        "2-12",
        "2-14",
        "2-15",
        "2-18",
        "2-19",
        "3-5",
        "3-9",
        "3-11",
        "3-12",
        "3-13",
        "3-14",
        "3-15",
        "3-16",
        "3-17",
        "3-18",
        "3-19",
        "3-20",
    }
)

MANUAL_ONLY_IDS = frozenset(
    {
        "1-2",
        "1-3",
        "1-8",
        "2-2",
        "2-3",
        "2-4",
        "2-7",
        "2-8",
        "2-9",
        "2-13",
        "2-16",
        "2-17",
        "3-1",
        "3-2",
        "3-3",
        "3-4",
        "3-6",
        "3-7",
        "3-8",
        "3-10",
        "3-21",
        "3-22",
        "3-23",
        "3-24",
        "3-25",
        "3-26",
        "3-27",
        "3-28",
        "3-29",
        "3-31",
        "3-32",
        "3-30",
    }
)


def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8", "replace")


def parse_window_tests(html: str) -> list[dict] | None:
    match = re.search(r"window\.tests\s*=\s*(\[.*?\]);", html, re.S)
    if not match:
        return None
    raw = match.group(1)
    tests = ast.literal_eval(raw)
    return [{"input": t.get("input", ""), "output": t["answer"]} for t in tests]


def lesson_problem_urls(lesson_slug: str) -> list[str]:
    html = fetch(f"https://snakify.org/en/lessons/{lesson_slug}/")
    links = sorted(set(re.findall(r'href="(/en/lessons/[^"]+/problems/[^"]+/)"', html)))
    return [f"https://snakify.org{link}" for link in links]


def snakify_slug_from_url(url: str) -> str:
    return url.rstrip("/").split("/")[-1]


def update_problem_json(bare_id: str, tests: list[dict], dry_run: bool) -> None:
    chapter = bare_id.split("-")[0]
    pid = f"java-{bare_id}"
    path = JAVA_DATA / f"chapter-{chapter}" / f"{pid}.json"
    if not path.exists():
        print(f"  skip {pid}: file not found")
        return
    problem = json.loads(path.read_text(encoding="utf-8"))
    old_count = len(problem.get("tests", []))
    problem["tests"] = tests
    src = problem.get("source") or ""
    if "snakify.org" not in src:
        problem["source"] = (src + " + snakify.org tests").strip(" +")
    print(f"  {pid}: {old_count} -> {len(tests)} tests")
    if not dry_run:
        path.write_text(json.dumps(problem, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def snakify_problem_url(lesson_slug: str, problem_slug: str) -> str:
    return f"https://snakify.org/en/lessons/{lesson_slug}/problems/{problem_slug}/"


def urls_for_manual_problems() -> list[tuple[str, str, str]]:
    """Return (bare_id, lesson_slug, problem_slug) for manual-only problems."""
    lesson_by_chapter = {
        "1": "print_input_numbers",
        "2": "integer_float_numbers",
        "3": "if_then_else_conditions",
    }
    slug_by_id = {v: k for k, v in SNAKIFY_SLUG_TO_ID.items()}
    out = []
    for bare_id in sorted(MANUAL_ONLY_IDS, key=lambda x: (int(x.split("-")[0]), int(x.split("-")[1]))):
        ch = bare_id.split("-")[0]
        slug = slug_by_id.get(bare_id)
        if not slug:
            print(f"  ? no slug mapping for {bare_id}")
            continue
        out.append((bare_id, lesson_by_chapter[ch], slug))
    return out


def main() -> int:
    dry_run = "--dry-run" in sys.argv
    fetch_all = "--all" in sys.argv

    updated = 0

    if fetch_all:
        for lesson_slug in LESSONS:
            print(f"\nLesson: {lesson_slug}")
            for url in lesson_problem_urls(lesson_slug):
                slug = snakify_slug_from_url(url)
                bare_id = SNAKIFY_SLUG_TO_ID.get(slug)
                if not bare_id:
                    print(f"  ? unmapped slug: {slug}")
                    continue
                html = fetch(url)
                tests = parse_window_tests(html)
                if not tests:
                    print(f"  {bare_id} ({slug}): no window.tests")
                    continue
                update_problem_json(bare_id, tests, dry_run)
                updated += 1
    else:
        print("Fetching manual-only problems from snakify.org …")
        for bare_id, lesson_slug, slug in urls_for_manual_problems():
            url = snakify_problem_url(lesson_slug, slug)
            print(f"\n{bare_id} ({slug})")
            html = fetch(url)
            tests = parse_window_tests(html)
            if not tests:
                print("  no window.tests")
                continue
            update_problem_json(bare_id, tests, dry_run)
            updated += 1

    print(f"\n{'Would update' if dry_run else 'Updated'} {updated} problem(s).")
    if not dry_run and updated:
        print("Run: python scripts/convert_java_to_cpp.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
