import itertools
import re
import typing

import numpy as np

import util

type tup2 = tuple[int, int]


class Machine(typing.NamedTuple):
    a: tup2
    b: tup2
    prize: tup2


def parse_machines(
    lines: list[str], prize_offset=10000000000000
) -> typing.Iterable[Machine]:
    for a, b, prize, *_ in itertools.batched(lines, 4):
        ax, ay = re.findall(r"\d+", a)
        bx, by = re.findall(r"\d+", b)
        px, py = re.findall(r"\d+", prize)
        yield Machine(
            (int(ax), int(ay)),
            (int(bx), int(by)),
            (int(px) + prize_offset, int(py) + prize_offset),
        )


# cribbed from https://stackoverflow.com/a/42727584
def get_intersect(
    a1: tup2, a2: tup2, b1: tup2, b2: tup2
) -> typing.Optional[tuple[float, float]]:
    """
    Returns the point of intersection of the lines passing through a2,a1 and b2,b1.
    a1: [x, y] a point on the first line
    a2: [x, y] another point on the first line
    b1: [x, y] a point on the second line
    b2: [x, y] another point on the second line
    """
    s = np.vstack([a1, a2, b1, b2])  # s for stacked
    h = np.hstack((s, np.ones((4, 1))))  # h for homogeneous
    l1 = np.cross(h[0], h[1])  # get first line
    l2 = np.cross(h[2], h[3])  # get second line
    x, y, z = np.cross(l1, l2)  # point of intersection
    if z == 0:  # lines are parallel
        return None
    return (x / z, y / z)


def soln(machine: Machine) -> typing.Optional[tup2]:

    # prize[0] = A*a[0] + B*b[0]
    # 0 <=A <= prize[0]/a[0]
    # 0 <=B <= prize[0]/b[0]
    # same for [1]
    # prefer more B, less A
    # Draw two vectors,
    #   one from (0,0) to max_b*b
    #   one from prize to prize - max_a*a
    # The intercept is the cheapest solution - if it's not a whole number the puzzle is impossible

    max_b = min(machine.prize[0] // machine.b[0], machine.prize[1] // machine.b[1])
    max_a = min(machine.prize[0] // machine.a[0], machine.prize[1] // machine.a[1])
    b_start = (0, 0)
    b_end = (max_b * machine.b[0], max_b * machine.b[1])
    a_start = machine.prize
    a_end = (a_start[0] - max_a * machine.a[0], a_start[1] - max_a * machine.a[1])

    intercept = get_intersect(b_start, b_end, a_start, a_end)
    if intercept is None:
        print("No intercept")
        return
    print(intercept)
    # hackity hack - I tried to make the code use int64, but that exploded things
    int_intercept = (round(intercept[0]), round(intercept[1]))
    print(int_intercept)
    # if intercept is valid, how many presses?
    b_pressed = int_intercept[0] // machine.b[0]
    a_pressed = (machine.prize[0] - int_intercept[0]) // machine.a[0]
    computed_soln = (
        machine.b[0] * b_pressed + machine.a[0] * a_pressed,
        machine.b[1] * b_pressed + machine.a[1] * a_pressed,
    )
    if computed_soln != machine.prize:
        print("intercept doesn't work")
        return
    return a_pressed, b_pressed


def main():
    machines = parse_machines(util.load_input(util.REAL, 13).splitlines())
    s = 0
    for machine in machines:
        print(machine)
        if sol := soln(machine):
            print(sol)
            tokens = 3 * sol[0] + 1 * sol[1]
            print(tokens)
            s += tokens
    print(s)


if __name__ == "__main__":
    main()
