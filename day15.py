import typing

import util

type tup2 = tuple[int, int]


class State(typing.NamedTuple):
    robot: tup2
    walls: set[tup2]
    boxes: set[tup2]

    def checksum(self) -> int:
        return sum(x + 100 * y for x, y in self.boxes)

    def visualize(self) -> str:
        s = ""
        bounds = max(self.walls)
        for y in range(bounds[1] + 1):
            for x in range(bounds[0] + 1):
                pos = (x, y)
                if pos == self.robot:
                    s += "@"
                elif pos in self.boxes:
                    s += "O"
                elif pos in self.walls:
                    s += "#"
                else:
                    s += "."
            s += "\n"
        return s


def parse_state(warehouse: list[str]):
    s = State((0, 0), set(), set())
    for y, row in enumerate(warehouse):
        for x, val in enumerate(row):
            match val:
                case "@":
                    s = s._replace(robot=(x, y))
                case "O":
                    s.boxes.add((x, y))
                case "#":
                    s.walls.add((x, y))
    return s


def simulate(state: State, move: str) -> State:
    next_robot = state.robot
    match move:
        case "<":
            next_robot = (state.robot[0] - 1, state.robot[1])
        case ">":
            next_robot = (state.robot[0] + 1, state.robot[1])
        case "v":
            next_robot = (state.robot[0], state.robot[1] + 1)
        case "^":
            next_robot = (state.robot[0], state.robot[1] - 1)
    # Bail early if we bump into a wall
    if next_robot in state.walls:
        print("Noop, wall bump")
        return state
    last_pushed_box: typing.Optional[tup2] = None
    maybe_pushed_box = next_robot
    while maybe_pushed_box in state.boxes:
        print(f"moving box {maybe_pushed_box}")
        last_pushed_box = maybe_pushed_box
        match move:
            case "<":
                maybe_pushed_box = (maybe_pushed_box[0] - 1, maybe_pushed_box[1])
            case ">":
                maybe_pushed_box = (maybe_pushed_box[0] + 1, maybe_pushed_box[1])
            case "v":
                maybe_pushed_box = (maybe_pushed_box[0], maybe_pushed_box[1] + 1)
            case "^":
                maybe_pushed_box = (maybe_pushed_box[0], maybe_pushed_box[1] - 1)
        if maybe_pushed_box in state.walls:
            # Bail as soon as we'd push a box into a wall
            print("Noop, box to wall bump")
            return state
    next_boxes = state.boxes
    if last_pushed_box:
        next_boxes = (state.boxes - {next_robot}) | {maybe_pushed_box}
    return state._replace(robot=next_robot, boxes=next_boxes)


def main():
    puzzle_input = util.load_input(util.REAL, 15).splitlines()
    warehouse_input = puzzle_input[: puzzle_input.index("")]
    program_input = "".join(puzzle_input[puzzle_input.index("") :])
    state = parse_state(warehouse_input)
    # print(state.visualize())
    for move in program_input:
        # print(f"{move=}")
        state = simulate(state, move)
        # print(state.visualize())

    print(state.checksum())


if __name__ == "__main__":
    main()
