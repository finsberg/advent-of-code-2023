"""Solutions to day 4"""

from textwrap import dedent
from typing import Sequence
import argparse
from collections import defaultdict

from pathlib import Path


here = Path(__file__).absolute().parent


def game_points(game: str) -> int:
    game_no, game_ = game.strip().split(":")

    winning_str, your_str = game_.split("|")
    your = set(your_str.split())
    winning = set(winning_str.strip().split())

    num_winning_numbers = len(your & winning)
    if num_winning_numbers == 0:
        return 0, 0
    else:
        return pow(2, num_winning_numbers - 1), num_winning_numbers


def run(text: str, part: int) -> int:
    if part == 1:
        return sum(game_points(line)[0] for line in text.strip().split("\n"))
    elif part == 2:
        values = [game_points(line) for line in text.strip().split("\n")]
        instances = defaultdict(lambda: 0)
        for i, v in enumerate(values):
            instances[i] += 1
            for j in range(1, v[1] + 1):
                instances[i + j] += instances[i]
        return sum(instances.values())


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
            Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
            Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
            Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
            Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
            Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
            Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
            """
        )
        assert run(test_input, 1) == 13

    @pytest.mark.parametrize(
        "game, expected_points",
        (
            ("Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53", 8),
            ("Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19", 2),
            ("Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1", 2),
            ("Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83", 1),
            ("Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36", 0),
            ("Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11", 0),
        ),
    )
    def test_game_points(game, expected_points):
        assert game_points(game)[0] == expected_points

    def test_run_part2():
        test_input = dedent(
            """
            Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
            Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
            Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
            Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
            Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
            Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
            """
        )
        assert run(test_input, 2) == 30
