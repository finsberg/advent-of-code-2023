"""Solutions to day 1"""

from textwrap import dedent
from typing import Sequence
import argparse
from pathlib import Path

here = Path(__file__).absolute().parent


def calibration_value_from_line(line: str) -> int:
    line = line.strip()

    try:
        first = next(s for s in line if s.isdigit())
        last = next(s for s in reversed(line) if s.isdigit())
    except StopIteration:
        return 0

    return int(first + last)


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

    def test_main():
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
    def test_calibration_value_from_line(line, expected_value):
        assert calibration_value_from_line(line) == expected_value
