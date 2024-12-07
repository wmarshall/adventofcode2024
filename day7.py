import operator
import typing

import util


def int_concat(a: int, b: int) -> int:
    return int(f"{a}{b}")


OPERATIONS = [operator.add, operator.mul, int_concat]


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
        # Bail early if we've overshot, since our operators can only increase
        if result > eq.lhs:
            continue
        if result == eq.lhs and len(eq.inputs) == 2:
            return [op]
        sub_solve = solve(Equation(eq.lhs, [result, *eq.inputs[2:]]))
        if sub_solve is None:
            continue
        return [op, *sub_solve]
    return None


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
            computed = eq.inputs[0]
            working_inputs = eq.inputs[1:]
            for op in soln:
                computed = op(computed, working_inputs[0])
                working_inputs = working_inputs[1:]
            if len(working_inputs) > 0 or computed != eq.lhs:
                breakpoint()
            s += eq.lhs
    print(s)


if __name__ == "__main__":
    main()
