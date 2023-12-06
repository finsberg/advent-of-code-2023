"""Solutions to day 5"""

from textwrap import dedent
from typing import Sequence
import argparse
from collections import defaultdict

from pathlib import Path


here = Path(__file__).absolute().parent


def run(text: str, part: int) -> int:
    groups = text.strip().split("\n\n")
    seeds = map(int, groups[0].strip().lstrip("seeds: ").split(" "))

    data = {}
    loc = {}
    for seed in seeds:
        src_value = seed
        for group in groups[1:]:
            name, numbers = group.split(" map:")
            src_name, dst_name = name.split("-to-")
            data[src_name] = {dst_name: {}}

            dst_value = None
            for dst_start, src_start, step in map(
                lambda x: map(int, x.split(" ")), numbers.strip().split("\n")
            ):
                if src_start <= src_value <= src_start + step:
                    dst_value = dst_start + (src_value - src_start)
            if dst_value is None:
                dst_value = src_value

            src_value = dst_value
        loc[seed] = src_value

    return min(loc.values())


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
            seeds: 79 14 55 13

            seed-to-soil map:
            50 98 2
            52 50 48

            soil-to-fertilizer map:
            0 15 37
            37 52 2
            39 0 15

            fertilizer-to-water map:
            49 53 8
            0 11 42
            42 0 7
            57 7 4

            water-to-light map:
            88 18 7
            18 25 70

            light-to-temperature map:
            45 77 23
            81 45 19
            68 64 13

            temperature-to-humidity map:
            0 69 1
            1 0 69

            humidity-to-location map:
            60 56 37
            56 93 4
            """
        )
        assert run(test_input, 1) == 35
