"""Solutions to day 1"""

from textwrap import dedent
from typing import Sequence
import argparse
from pathlib import Path

here = Path(__file__).absolute().parent

numbers = dict(
    zip(
        [
            "one",
            "two",
            "three",
            "four",
            "five",
            "six",
            "seven",
            "eight",
            "nine",
        ],
        map(str, range(1, 10)),
    )
)
numbers.update(dict(zip(map(str, range(1, 10)), map(str, range(1, 10)))))


def digitlist2number(digits: list[str]) -> int:
    try:
        return int(digits[0] + digits[-1])
    except IndexError:
        return 0


def line2digits(line):
    for i in range(len(line)):
        for word, digit in numbers.items():
            if line.startswith(word, i):
                yield digit


def calibration_value_from_line(line):
    return digitlist2number(list(line2digits(line)))


def run(text: str) -> int:
    return sum(map(calibration_value_from_line, text.split("\n")))


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
    if not fname.is_file():
        raise FileNotFoundError(f"File {fname} not found")
    value = run(fname.read_text())
    print(f"Solution is {value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

else:
    import pytest

    def test_run_part1():
        test_input = dedent(
            """
        1abc2
        pqr3stu8vwx
        a1b2c3d4e5f
        treb7uchet
        """
        )
        value = run(test_input)
        assert value == 142

    @pytest.mark.parametrize(
        "line, expected_value",
        (
            ("1abc2", 12),
            ("pqr3stu8vwx", 38),
            ("a1b2c3d4e5f", 15),
            ("treb7uchet", 77),
        ),
    )
    def test_calibration_value_from_line_part1(line, expected_value):
        assert calibration_value_from_line(line) == expected_value

    def test_run_part2():
        test_input = dedent(
            """
        two1nine
        eightwothree
        abcone2threexyz
        xtwone3four
        4nineeightseven2
        zoneight234
        7pqrstsixteen
        """
        )
        value = run(test_input)
        assert value == 281

    @pytest.mark.parametrize(
        "line, expected_value",
        (
            ("two1nine", 29),
            ("eightwothree", 83),
            ("abcone2threexyz", 13),
            ("xtwone3four", 24),
            ("4nineeightseven2", 42),
            ("zoneight234", 14),
            ("7pqrstsixteen", 76),
            ("eightwo", 82),
            ("eighttwo", 82),
        ),
    )
    def test_calibration_value_from_line_part2(line, expected_value):
        assert calibration_value_from_line(line) == expected_value
