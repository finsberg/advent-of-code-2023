"""Solutions to day 3"""

from textwrap import dedent
from typing import NamedTuple, Sequence
import string
import argparse
from functools import reduce
from pathlib import Path
import re

here = Path(__file__).absolute().parent
symbols = set(string.punctuation).difference({".", " "})


def check_part_number(n, start, mid, upper, lower) -> tuple[int, bool]:
    for i in range(start, len(mid)):
        if mid.startswith(n, i):
            s = max(i - 1, 0)
            e = min(len(mid), i + len(n) + 1)

            if (
                set(lower[s:e]).intersection(symbols)  # Symbol below
                or set(upper[s:e]).intersection(symbols)  # Symbol above
                or set(mid[s:i]).intersection(symbols)  # Symbol to the left
                or set(mid[i + len(n) : e]).intersection(symbols)  # Symbol to the right
            ):
                return e, True
            else:
                return e, False

    else:
        raise RuntimeError(f"Invalid number {n} for line {mid}")


def part_numbers(upper: str, mid: str, lower: str) -> list[int]:
    # Find all numbers
    numbers = []
    potential_numbers = [
        el
        for el in re.split("|".join(map(re.escape, list(string.punctuation))), mid)
        if el != ""
    ]

    start = 0
    for n in potential_numbers:
        start, is_part = check_part_number(n, start, mid, upper, lower)
        if is_part:
            numbers.append(int(n))

    return numbers


class Symbol(NamedTuple):
    start: int
    end: int
    value: str

    def find_adjacent(self, text) -> list[int]:
        numbers = []
        for letter in re.finditer(r"\d+", text):
            if letter.end() < self.start or letter.start() > self.end:
                continue

            numbers.append(letter.group())
        return numbers


def part2(upper: str, mid: str, lower: str) -> list[int]:
    numbers = []
    for letter in re.finditer(r"[\*]", mid):
        adj = []
        x = Symbol(
            letter.start(),
            letter.end(),
            letter.group(),
        )

        adj.extend(x.find_adjacent(upper))
        adj.extend(x.find_adjacent(mid))
        adj.extend(x.find_adjacent(lower))

        if len(adj) == 2:
            value = reduce(lambda x, y: x * y, map(int, adj))
            numbers.append(value)

    return numbers


def run(text: str, part: int) -> int:
    lines = text.strip().split("\n")
    padding = "." * len(lines[0])

    if part == 1:
        return sum(
            sum(part_numbers(*args))
            for args in zip([padding] + lines[:-1], lines, lines[1:] + [padding])
        )
    elif part == 2:
        return sum(
            sum(part2(*args))
            for args in zip([padding] + lines[:-1], lines, lines[1:] + [padding])
        )
    else:
        raise ValueError(f"Invalid part {part}")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "-i",
        "--input",
        type=Path,
        default=here / ".." / "input.txt",
        help="Path to input file. In not exist it will be downloaded",
    )

    parser.add_argument("part", type=int)
    args = vars(parser.parse_args(argv))
    fname: Path = args["input"]
    if not fname.is_file():
        raise FileNotFoundError(f"File {fname} not found")
    if args["part"] == 1:
        value = run(fname.read_text(), 1)
    elif args["part"] == 2:
        value = run(fname.read_text(), 2)
    else:
        raise ValueError("Invalid part {part}, expected 1 or 2")
    print(f"Solution is {value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

else:
    import pytest

    def test_run_part1():
        test_input = dedent(
            """
        467..114..
        ...*......
        ..35..633.
        ......#...
        617*......
        .....+.58.
        ..592.....
        ......755.
        ...$.*....
        .664.598..
        """
        )
        assert run(test_input, 1) == 4361

    def test_run_part2():
        test_input = dedent(
            """
        467..114..
        ...*......
        ..35..633.
        ......#...
        617*......
        .....+.58.
        ..592.....
        ......755.
        ...$.*....
        .664.598..
        """
        )
        assert run(test_input, 2) == 467835
