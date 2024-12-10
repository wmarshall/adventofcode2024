import typing

import util


class Point2(typing.NamedTuple):
    row: int
    col: int


DIRECTIONS = (
    (0, 1),
    (-1, 0),
    (0, -1),
    (1, 0),
)


def trailheads(topo_map: list[list[int]]) -> typing.Iterable[Point2]:
    for i, row in enumerate(topo_map):
        for j, col_val in enumerate(row):
            if col_val == 0:
                yield Point2(i, j)


def reachable(
    start: Point2, topo_map: list[list[int]], rows: int, cols: int
) -> typing.Iterable[Point2]:
    next_val = topo_map[start.row][start.col] + 1
    if next_val > 9:
        return
    for d_row, d_col in DIRECTIONS:
        next_point = Point2(start.row + d_row, start.col + d_col)
        if not (0 <= next_point.row < rows and 0 <= next_point.col < cols):
            # OOB
            continue
        if topo_map[next_point.row][next_point.col] != next_val:
            # not ascending by 1
            continue
        yield next_point
        yield from reachable(next_point, topo_map, rows, cols)


def main():
    topo_map = [
        [int(v) for v in line] for line in util.load_input(util.REAL, 10).splitlines()
    ]
    rows = len(topo_map)
    cols = len(topo_map[0])
    s = 0
    for trailhead in trailheads(topo_map):
        peaks: set[Point2] = set()
        for point in reachable(trailhead, topo_map, rows, cols):
            if topo_map[point.row][point.col] == 9:
                peaks.add(point)
        s += len(peaks)
    print(s)


if __name__ == "__main__":
    main()
