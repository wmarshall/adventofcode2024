import itertools
from typing import Iterable, NamedTuple, Sequence

import util

XMAS = "XMAS"

DIRECTIONS = [
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
    row: int
    col: int


class Match(NamedTuple):
    start: Coordinate
    end: Coordinate


def find_xmas(word_search: Sequence[Sequence[str]]) -> Iterable[Match]:
    for i, row in enumerate(word_search):
        for j, col in enumerate(row):
            if col == XMAS[0]:
                start = Coordinate(i, j)
                for dir_row, dir_col in DIRECTIONS:
                    end = Coordinate(
                        start.row + len(XMAS[1:]) * dir_row,
                        start.col + len(XMAS[1:]) * dir_col,
                    )
                    if 0 <= end.row < len(word_search) and 0 <= end.col < len(row):
                        for k, c in enumerate(XMAS[1:], 1):
                            if (
                                word_search[start.row + dir_row * k][
                                    start.col + dir_col * k
                                ]
                                != c
                            ):
                                break
                        else:
                            match = Match(start, end)
                            yield match


def find_x_mas(word_search: Sequence[Sequence[str]]) -> Iterable[tuple[Match, Match]]:
    for i, row in enumerate(word_search):
        for j, col in enumerate(row):
            if col == "A":
                # Find 2 diagonal matches
                matches = []
                for dir_row, dir_col in ((-1, -1), (-1, 1)):
                    start = Coordinate(i - dir_row, j - dir_col)
                    if not (0 <= start.row < len(word_search) and 0 <= start.col < len(row)):
                        break
                    start_val = word_search[start.row][start.col]
                    if start_val not in ("M", "S"):
                        break
                    expected_end_val = "S" if start_val == "M" else "M"
                    end = Coordinate(i + dir_row, j + dir_col)
                    if not (0 <= end.row < len(word_search) and 0 <= end.col < len(row)):
                        break
                    if word_search[end.row][end.col] != expected_end_val:
                        break
                    match start_val:
                        case "M":
                            matches.append(Match(start, end))
                        case "S":
                            matches.append(Match(end, start))
                if len(matches) == 2:
                    yield matches[0], matches[1]

def main():
    word_search = util.load_input(util.REAL, 4).splitlines()
    # print(sum(1 for _ in find_xmas(word_search)))
    print(sum(1 for _ in find_x_mas(word_search)))


if __name__ == "__main__":
    main()
