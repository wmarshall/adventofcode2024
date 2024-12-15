import collections
import operator
import typing
from functools import reduce

import util

type tup2 = tuple[int, int]


class Robot(typing.NamedTuple):
    p: tup2
    v: tup2


def parse_robots(lines: list[str]) -> typing.Iterable[Robot]:
    for line in lines:
        p_section, v_section = line.split()
        p_section = p_section[len("p=") :]
        v_section = v_section[len("v=") :]
        px, py = p_section.split(",")
        vx, vy = v_section.split(",")
        yield Robot((int(px), int(py)), (int(vx), int(vy)))


def simulate(robot: Robot, steps: int, bounds: tup2) -> tup2:
    final_pos = (
        robot.p[0] + steps * robot.v[0],
        robot.p[1] + steps * robot.v[1],
    )
    final_pos_wrapped = (
        final_pos[0] % bounds[0],
        final_pos[1] % bounds[1],
    )
    return final_pos_wrapped


def visualize(positions: collections.Counter[tup2], bounds: tup2):
    center = (bounds[0] // 2, bounds[1] // 2)
    for y in range(bounds[1]):
        for x in range(bounds[0]):
            count = positions[(x, y)]
            if count > 9:
                raise Exception("can't visualize")
            if count == 0:
                count = "."
                if x == center[0] or y == center[1]:
                    count = "x"
            print(count, end="")
        print()


def safety_factor(positions: collections.Counter[tup2], bounds: tup2) -> int:
    center = (bounds[0] // 2, bounds[1] // 2)
    quad_counts = [0, 0, 0, 0]
    for pos, count in positions.items():
        if pos[0] < center[0] and pos[1] < center[1]:
            quad_counts[0] += count
        elif pos[0] < center[0] and pos[1] > center[1]:
            quad_counts[1] += count
        elif pos[0] > center[0] and pos[1] < center[1]:
            quad_counts[2] += count
        elif pos[0] > center[0] and pos[1] > center[1]:
            quad_counts[3] += count

    return reduce(operator.mul, quad_counts)


def main():
    input_path = util.REAL
    bounds = (11, 7)
    if input_path == util.REAL:
        bounds = (101, 103)

    robots = parse_robots(util.load_input(input_path, 14).splitlines())
    final_positions = collections.Counter(simulate(r, 100, bounds) for r in robots)
    visualize(final_positions, bounds)
    print(safety_factor(final_positions, bounds))


if __name__ == "__main__":
    main()
