import itertools
from typing import Iterable, NamedTuple, Sequence

import util

target = "XMAS"

directions = [
    (-1, -1),
    (-1, 0),
    (-1, 1),
    (0, -1),
    (0, 1),
    (1, -1),
    (1, 0),
    (1, 1),
]


class Coordinate(NamedTuple):
    x: int
    y: int


class Match(NamedTuple):
    start: Coordinate
    end: Coordinate


def find_xmas(word_search: Sequence[Sequence[str]]) -> Iterable[Match]:
    for i, row in enumerate(word_search):
        for j, col in enumerate(row):
            if col == target[0]:
                start = Coordinate(i, j)
                for dir_x, dir_y in directions:
                    end = Coordinate(
                        start.x + len(target[1:]) * dir_x,
                        start.y + len(target[1:]) * dir_y,
                    )
                    if 0 <= end.x < len(word_search) and 0 <= end.y < len(row):
                        for k, c in enumerate(target[1:], 1):
                            if (
                                word_search[start.x + dir_x * k][start.y + dir_y * k]
                                != c
                            ):
                                break
                        else:
                            match = Match(start, end)
                            yield match


def main():
    word_search = util.load_input(util.REAL, 4).splitlines()
    print(sum(1 for _ in find_xmas(word_search)))


if __name__ == "__main__":
    main()
