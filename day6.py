import typing

import util

OBSTACLE = "#"
GUARD = "^"


class Coord(typing.NamedTuple):
    row: int
    col: int


class Direction(typing.NamedTuple):
    name: str
    delta_row: int
    delta_col: int


DIRECTIONS = (
    Direction("UP", -1, 0),
    Direction("RIGHT", 0, 1),
    Direction("DOWN", 1, 0),
    Direction("LEFT", 0, -1),
)


def find_coords(c: str, lab_map: list[str]) -> typing.Iterable[Coord]:
    for i, row in enumerate(lab_map):
        for j, col in enumerate(row):
            if col == c:
                yield Coord(i, j)


def guard_path(
    rows: int, cols: int, obstacles: set[Coord], guard: Coord
) -> typing.Iterable[Coord]:
    direction = DIRECTIONS[0]
    while True:
        yield guard
        next_space = Coord(
            guard.row + direction.delta_row, guard.col + direction.delta_col
        )
        print(next_space)
        if not (0 <= next_space.row < rows and 0 <= next_space.col < cols):
            break
        if next_space in obstacles:
            direction = DIRECTIONS[(DIRECTIONS.index(direction) + 1) % len(DIRECTIONS)]
            continue
        guard = next_space


def main():
    lab_map = util.load_input(util.REAL, 6).splitlines()
    rows = len(lab_map)
    cols = len(lab_map[0])
    obstacles = set(find_coords(OBSTACLE, lab_map))
    guard = list(find_coords(GUARD, lab_map))[0]
    print(len(set(guard_path(rows, cols, obstacles, guard))))


if __name__ == "__main__":
    main()
