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


def visualize(positions: collections.Counter[tup2], bounds: tup2) -> str:
    center = (bounds[0] // 2, bounds[1] // 2)
    s = ""
    for y in range(bounds[1]):
        for x in range(bounds[0]):
            count = positions[(x, y)]
            if count > 9:
                raise Exception("can't visualize")
            if count == 0:
                count = " "
                # if x == center[0] or y == center[1]:
                #     count = "x"
            s += str(count)
        s += "\n"
    return s


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


DIRECTIONS = (
    (0, 1),
    (-1, 0),
    (0, -1),
    (1, 0),
)

def largest_blob(positions: collections.Counter[tup2]) -> int:
    largest = 0
    seen: set[tup2] = set()
    for pos in positions:
        if pos in seen:
            continue
        blob_size = 0
        blob_q = {pos}
        while blob_q:
            blob_pos = blob_q.pop()
            seen.add(blob_pos)
            new_pos_count = positions[pos]
            if new_pos_count == 0:
                raise Exception("impossible")
            blob_size += new_pos_count
            for dx, dy in DIRECTIONS:
                neighbor = (blob_pos[0] + dx, blob_pos[1] + dy)
                if positions[neighbor] == 0:
                    continue
                if neighbor in seen:
                    continue
                blob_q.add(neighbor)
        if blob_size > largest:
            largest = blob_size

    return largest


def main():
    input_path = util.REAL
    bounds = (11, 7)
    if input_path == util.REAL:
        bounds = (101, 103)

    robots = list(parse_robots(util.load_input(input_path, 14).splitlines()))
    # Dude I don't know what a christmas tree looks like, let's just see what the cycle time is
    # cycle time for my real input was 10403, but that's not the answer!
    seen_final_positions:set[str] = set()
    for i in range(10404):
        print(f"{i=}")
        final_positions = collections.Counter(simulate(r, i, bounds) for r in robots)
        viz = visualize(final_positions, bounds)
        print(viz)
        largest = largest_blob(final_positions)
        print(largest)
        if largest >= 10:
            input("Enter to continue")
        if viz in seen_final_positions:
            break
        seen_final_positions.add(viz)


if __name__ == "__main__":
    main()
