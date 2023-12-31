"""Solutions to day 2"""

from textwrap import dedent
from typing import Sequence, NamedTuple
import argparse
from functools import reduce
from pathlib import Path

here = Path(__file__).absolute().parent


class Set(NamedTuple):
    red: int
    blue: int
    green: int

    def power(self):
        return self.red * self.blue * self.green


def set2cubes(item: str) -> Set:
    items = [i.strip() for i in item.split(",")]
    values = {"blue": 0, "red": 0, "green": 0}

    for item in items:
        for color in values:
            if color in item:
                values[color] = int(item.strip(color).strip())
    return Set(**values)


def possible_set(s: Set) -> bool:
    return s.red <= 12 and s.green <= 13 and s.blue <= 14


def valid_game(text: str) -> tuple[bool, int]:
    game, sets = text.split(":")
    sets_list = sets.split(";")
    game_number = int(game.lstrip("Game").strip())
    return all(possible_set(set2cubes(item)) for item in sets_list), game_number


def run_part1(text: str) -> int:
    return sum(
        number
        for is_valid, number in map(valid_game, text.strip().split("\n"))
        if is_valid
    )


def min_power(text: str) -> int:
    game, sets = text.split(":")
    sets_list = sets.split(";")

    def func(xi: Set, x: Set) -> Set:
        return Set(
            red=max(x.red, xi.red),
            blue=max(x.blue, xi.blue),
            green=max(x.green, xi.green),
        )

    max_set = reduce(func, (set2cubes(item) for item in sets_list))
    return max_set.power()


def run_part2(text: str) -> int:
    return sum(number for number in map(min_power, text.strip().split("\n")))


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
        value = run_part1(fname.read_text())
    elif args["part"] == 2:
        value = run_part2(fname.read_text())
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
            Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
            Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
            Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
            Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
            Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
            """
        )
        assert run_part1(test_input) == 8

    @pytest.mark.parametrize(
        "input, expected_is_valid, expected_number",
        (
            ("Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green", True, 1),
            (
                "Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue",
                True,
                2,
            ),
            (
                "Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red",
                False,
                3,
            ),
            (
                "Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red",
                False,
                4,
            ),
            ("Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green", True, 5),
        ),
    )
    def test_valid_game(input, expected_is_valid, expected_number):
        is_valid, number = valid_game(input)
        assert number == expected_number
        assert is_valid == expected_is_valid

    def test_run_part2():
        test_input = dedent(
            """
            Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
            Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
            Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
            Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
            Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
            """
        )
        assert run_part2(test_input) == 2286

    @pytest.mark.parametrize(
        "input, expected_min_power",
        (
            ("Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green", 48),
            (
                "Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue",
                12,
            ),
            (
                "Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red",
                1560,
            ),
            (
                "Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red",
                630,
            ),
            ("Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green", 36),
        ),
    )
    def test_minimum_power(input, expected_min_power):
        power = min_power(input)
        assert expected_min_power == power
