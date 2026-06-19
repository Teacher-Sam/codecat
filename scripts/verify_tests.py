#!/usr/bin/env python3
"""Compare local problem tests with vpavlenko/content official files."""

from __future__ import annotations

import json
import re
import sys
import urllib.request
from pathlib import Path

BASE = "https://raw.githubusercontent.com/vpavlenko/content/master/problems"
ROOT = Path(__file__).resolve().parent.parent
JAVA = ROOT / "java" / "data"

OFFICIAL = {
    "java-1-1": "aplusbplusc.txt",
    "java-1-4": "area_of_right_triangle.txt",
    "java-1-5": "hello_harry.txt",
    "java-1-6": "apples.txt",
    "java-1-7": "next_and_previous.txt",
    "java-1-9": "desks.txt",
    "java-2-1": "int_and_float/last_digit.txt",
    "java-2-5": "int_and_float/tens_digit.txt",
    "java-2-6": "int_and_float/sum_of_digits.txt",
    "java-2-10": "int_and_float/fractional_part.txt",
    "java-2-11": "int_and_float/digit_after_separator.txt",
    "java-2-12": "int_and_float/motor_rally.txt",
    "java-2-14": "electronic_watch.txt",
    "java-2-15": "int_and_float/purchase_price.txt",
    "java-2-18": "int_and_float/watch_1.txt",
    "java-2-19": "int_and_float/watch_2.txt",
    "java-3-5": "ifelse/minimum.txt",
    "java-3-9": "ifelse/signum.txt",
    "java-3-12": "ifelse/minimum3.txt",
    "java-3-13": "ifelse/num_equal.txt",
    "java-3-14": "ifelse/rook_move.txt",
    "java-3-16": "ifelse/chess_board.txt",
    "java-3-17": "ifelse/king_move.txt",
    "java-3-18": "ifelse/bishop_move.txt",
    "java-3-19": "ifelse/queen_move.txt",
    "java-3-20": "ifelse/knight_move.txt",
    "java-3-26": "ifelse/chocolate.txt",
    "java-3-27": "ifelse/leap_year.txt",
}


def fetch(relpath: str) -> str:
    with urllib.request.urlopen(f"{BASE}/{relpath}", timeout=30) as resp:
        return resp.read().decode("utf-8")


def parse_tests(text: str) -> list[dict]:
    return [
        {"input": a.rstrip("\n"), "output": b.rstrip("\n")}
        for a, b in re.findall(
            r"Test:\s*\n(.*?)\n\nAnswer:\s*\n(.*?)(?=\n\nTest:|\Z)", text, re.S
        )
    ]


def main() -> int:
    issues: list[str] = []
    manual: list[str] = []

    for ch in ("1", "2", "3"):
        chdir = JAVA / f"chapter-{ch}"
        chapter = json.loads((chdir / "chapter.json").read_text(encoding="utf-8"))
        for pid in chapter["problemIds"]:
            if pid.endswith("-0"):
                continue
            problem = json.loads((chdir / f"{pid}.json").read_text(encoding="utf-8"))
            local = problem.get("tests", [])

            if pid in OFFICIAL:
                official = parse_tests(fetch(OFFICIAL[pid]))
                if local == official:
                    print(f"OK   {pid}: {len(local)} tests (official)")
                    continue
                issues.append(f"{pid}: count local={len(local)} official={len(official)}")
                for i, pair in enumerate(zip(local, official)):
                    l, o = pair
                    if l != o:
                        issues.append(
                            f"  {pid} test {i + 1}: output local={l['output']!r} official={o['output']!r}"
                        )
                if len(local) > len(official):
                    for extra in local[len(official) :]:
                        issues.append(
                            f"  {pid} extra local: in={extra['input']!r} out={extra['output']!r}"
                        )
                for miss in official[len(local) :]:
                    issues.append(
                        f"  {pid} missing: in={miss['input']!r} out={miss['output']!r}"
                    )
            else:
                manual.append(f"{pid}: {len(local)} tests (manual/derived)")

    print("\n--- Manual / derived (no official txt in repo) ---")
    for line in manual:
        print(line)

    print("\n--- Issues vs official Snakify ---")
    if not issues:
        print("None")
    else:
        for line in issues:
            print(line)

    return 1 if issues else 0


if __name__ == "__main__":
    sys.exit(main())
