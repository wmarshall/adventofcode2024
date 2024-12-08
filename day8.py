import itertools
import typing

import util

"""
.....
.A...
..A..
.....

A_0 = (1,1)
A_1 = (2,2)
antinodes = (0,0), (3,3)
(0, 0) = (1 + (1-2), ...) = (A_0 + (A_0-A_1))
(3, 3) = (2 + (2-1), ...) = (A_1+ (A_1-A_0))
"""


class Point2(typing.NamedTuple):
    row: int
    col: int


class Antenna(typing.NamedTuple):
    kind: str
    pos: Point2


def find_antennae(in_map: list[str]) -> typing.Iterable[Antenna]:
    for i, row in enumerate(in_map):
        for j, col_val in enumerate(row):
            if col_val != ".":
                yield Antenna(col_val, Point2(i, j))


def antinodes(ants: typing.Iterable[Antenna]) -> typing.Iterable[Point2]:
    for a, b in itertools.combinations(ants, 2):
        yield Point2(
            row=(a.pos.row + (a.pos.row - b.pos.row)),
            col=(a.pos.col + (a.pos.col - b.pos.col)),
        )
        yield Point2(
            row=(b.pos.row + (b.pos.row - a.pos.row)),
            col=(b.pos.col + (b.pos.col - a.pos.col)),
        )


def main():
    in_map = util.load_input(util.REAL, 8).splitlines()
    rows = len(in_map)
    cols = len(in_map[0])
    ants = find_antennae(in_map)
    grouped_ants: dict[str, set[Antenna]] = {}
    for ant in ants:
        grouped_ants.setdefault(ant.kind, set()).add(ant)
    unique_antinodes: set[Point2] = set()
    for kind, ants_of_kind in grouped_ants.items():
        for anode in antinodes(ants_of_kind):
            if 0 <= anode.row < rows and 0 <= anode.col < cols:
                unique_antinodes.add(anode)
    print(len(unique_antinodes))


if __name__ == "__main__":
    main()
