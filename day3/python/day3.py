"""Solutions to day 2"""

from textwrap import dedent
from typing import Sequence
import string
import argparse
from pathlib import Path
import re

here = Path(__file__).absolute().parent
symbols = set(string.punctuation).difference({".", " "})


def check_number(n, start, mid, upper, lower) -> tuple[int, bool]:
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
        start, is_part = check_number(n, start, mid, upper, lower)
        if is_part:
            numbers.append(int(n))

    return numbers


def run(text: str) -> int:
    lines = text.strip().split("\n")
    padding = "." * len(lines[0])
    return sum(
        sum(part_numbers(*args))
        for args in zip([padding] + lines[:-1], lines, lines[1:] + [padding])
    )


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

    args = vars(parser.parse_args(argv))
    fname: Path = args["input"]

    value = run(fname.read_text())

    print(f"Solution is {value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

else:
    import pytest

    def test_run():
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
        ....*.....
        ..57.685..
        """
        )
        assert run(test_input) == 5103
