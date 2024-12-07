import operator
import typing

import util

OPERATIONS = [operator.add, operator.mul]


class Equation(typing.NamedTuple):
    lhs: int
    inputs: typing.Sequence[int]


def parse_equation(raw: str) -> Equation:
    solution, *inputs = raw.split()
    return Equation(int(solution[:-1]), [int(i) for i in inputs])


def solve(eq: Equation) -> typing.Optional[typing.Iterable[typing.Callable]]:
    if len(eq.inputs) < 2:
        return None
    for op in OPERATIONS:
        a, b = eq.inputs[:2]
        result = op(a, b)
        if result == eq.lhs:
            return [op]
        # Bail early if we've overshot, since our operators can only increase
        if result > eq.lhs:
            continue
        sub_solve = solve(Equation(eq.lhs, [result, *eq.inputs[2:]]))
        if sub_solve is None:
            continue
        return [op, *sub_solve]


def main():
    equations = [
        parse_equation(line) for line in util.load_input(util.REAL, 7).splitlines()
    ]
    s = 0
    for eq in equations:
        print(eq)
        soln = solve(eq)
        print(soln)
        if soln is not None:
            s += eq.lhs
    print(s)


if __name__ == "__main__":
    main()
