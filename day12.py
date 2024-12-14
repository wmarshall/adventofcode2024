import functools
import typing

import util


class Point2(typing.NamedTuple):
    row: int
    col: int


class Region(typing.NamedTuple):
    kind: str
    plots: set[Point2]

    def area(self):
        return len(self.plots)

    def perimeter(self):
        s = 0
        for plot in self.plots:
            neighboring_points = {
                Point2(plot.row + d_row, plot.col + d_col)
                for d_row, d_col in DIRECTIONS
            }
            s += len(neighboring_points - self.plots)
        return s

    def sides(self):
        edges: dict[tuple[int, int], set[Point2]] = {d: set() for d in DIRECTIONS}
        for plot in self.plots:
            for d_row, d_col in DIRECTIONS:
                neighboring_point = Point2(plot.row + d_row, plot.col + d_col)
                if neighboring_point not in self.plots:
                    edges[(d_row, d_col)].add(neighboring_point)

        side_count = 0
        for direction, edge_set in edges.items():
            for outside_point in edge_set:
                perpendicular = (direction[1], direction[0])
                preceding = Point2(
                        outside_point.row - perpendicular[0],
                        outside_point.col - perpendicular[1],
                    )
                side_count += preceding not in edge_set
        return side_count


DIRECTIONS = (
    (0, 1),
    (-1, 0),
    (0, -1),
    (1, 0),
)


def find_contiguous(
    garden: list[str], start: Point2, rows: int, cols: int
) -> typing.Iterable[Point2]:
    kind = garden[start.row][start.col]
    seen: set[Point2] = set()
    q: set[Point2] = {start}
    while len(q) > 0:
        test_point = q.pop()
        seen.add(test_point)
        if garden[test_point.row][test_point.col] != kind:
            # dead_end
            continue
        yield test_point
        for d_row, d_col in DIRECTIONS:
            next_point = Point2(test_point.row + d_row, test_point.col + d_col)
            if not (0 <= next_point.row < rows and 0 <= next_point.col < cols):
                continue
            if next_point in seen:
                continue
            q.add(next_point)


def find_regions(garden: list[str]) -> typing.Iterable[Region]:
    rows = len(garden)
    cols = len(garden[0])
    seen: set[Point2] = set()
    for i, row in enumerate(garden):
        for j, kind in enumerate(row):
            if Point2(i, j) in seen:
                continue
            region = Region(
                kind, set(find_contiguous(garden, Point2(i, j), rows, cols))
            )
            seen |= region.plots
            yield region


def main():
    garden = util.load_input(util.REAL, 12).splitlines()
    price = 0
    for region in find_regions(garden):
        area, sides = region.area(), region.sides()
        print(f"{region.kind}{area, sides}")
        price += area * sides
    print(price)


if __name__ == "__main__":
    main()
