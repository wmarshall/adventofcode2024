import itertools
import typing

import util

type tup2 = tuple[int, int]


class State(typing.NamedTuple):
    robot: tup2
    walls_left: set[tup2]
    walls_right: set[tup2]
    boxes_left: set[tup2]
    boxes_right: set[tup2]

    def checksum(self) -> int:
        return sum(x + 100 * y for x, y in self.boxes_left)

    def visualize(self) -> str:
        s = ""
        bounds = max(self.walls_right)
        for y in range(bounds[1] + 1):
            for x in range(bounds[0] + 1):
                pos = (x, y)
                if pos == self.robot:
                    s += "@"
                elif pos in self.boxes_left:
                    s += "["
                elif pos in self.boxes_right:
                    s += "]"
                elif pos in self.walls_left or pos in self.walls_right:
                    s += "#"
                else:
                    s += "."
            s += "\n"
        return s


def parse_state(warehouse: list[str]):
    s = State((0, 0), set(), set(), set(), set())
    for y, row in enumerate(warehouse):
        for x, val in enumerate(itertools.batched(row, 2)):
            x *= 2
            match val:
                case ["@", "."]:
                    s = s._replace(robot=(x, y))
                case ["[", "]"]:
                    s.boxes_left.add((x, y))
                    s.boxes_right.add((x + 1, y))
                case ["#", "#"]:
                    s.walls_left.add((x, y))
                    s.walls_right.add((x + 1, y))
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
    if next_robot in state.walls_left or next_robot in state.walls_right:
        print("Noop, wall bump")
        return state
    affected: list[tuple[tup2, tup2]] = []
    maybe_pushed_box_tile = next_robot
    match move:
        case "<":
            # Simple case - go straight left through the boxes
            while maybe_pushed_box_tile in state.boxes_right:
                print(f"moving box in {maybe_pushed_box_tile}")
                actual_pushed_box = (
                    (maybe_pushed_box_tile[0] - 1, maybe_pushed_box_tile[1]),
                    maybe_pushed_box_tile,
                )
                if actual_pushed_box[0] not in state.boxes_left:
                    raise Exception("mismatched box halves")
                affected.append(actual_pushed_box)
                maybe_pushed_box_tile = (
                    maybe_pushed_box_tile[0] - 2,
                    maybe_pushed_box_tile[1],
                )
                if maybe_pushed_box_tile in state.walls_right:
                    # Bail as soon as we'd push a box into a wall
                    print("Noop, box to wall bump")
                    return state
        case ">":
            # Simple case - go straight right through the boxes
            while maybe_pushed_box_tile in state.boxes_left:
                print(f"moving box in {maybe_pushed_box_tile}")
                actual_pushed_box = (
                    maybe_pushed_box_tile,
                    (maybe_pushed_box_tile[0] + 1, maybe_pushed_box_tile[1]),
                )
                if actual_pushed_box[1] not in state.boxes_right:
                    raise Exception("mismatched box halves")
                affected.append(actual_pushed_box)
                maybe_pushed_box_tile = (
                    maybe_pushed_box_tile[0] + 2,
                    maybe_pushed_box_tile[1],
                )
                if maybe_pushed_box_tile in state.walls_left:
                    # Bail as soon as we'd push a box into a wall
                    print("Noop, box to wall bump")
                    return state
        case "^":
            # complicated case, making a wave-front
            actual_pushed_box: typing.Optional[tuple[tup2, tup2]] = None
            if maybe_pushed_box_tile in state.boxes_left:
                actual_pushed_box = (
                    maybe_pushed_box_tile,
                    (maybe_pushed_box_tile[0] + 1, maybe_pushed_box_tile[1]),
                )
                if actual_pushed_box[1] not in state.boxes_right:
                    raise Exception("mismatched box halves")
            elif maybe_pushed_box_tile in state.boxes_right:
                actual_pushed_box = (
                    (maybe_pushed_box_tile[0] - 1, maybe_pushed_box_tile[1]),
                    maybe_pushed_box_tile,
                )
                if actual_pushed_box[0] not in state.boxes_left:
                    raise Exception("mismatched box halves")
            box_q: set[tuple[tup2, tup2]] = set()
            if actual_pushed_box is not None:
                box_q.add(actual_pushed_box)
            while box_q:
                pushed_box = box_q.pop()
                next_pushed_box = (
                    (pushed_box[0][0], pushed_box[0][1] - 1),
                    (pushed_box[1][0], pushed_box[1][1] - 1),
                )
                if (
                    next_pushed_box[0] in state.walls_left
                    or next_pushed_box[1] in state.walls_left
                    or next_pushed_box[0] in state.walls_right
                    or next_pushed_box[1] in state.walls_right
                ):
                    # Bail as soon as we'd push a box into a wall
                    print("Noop, box to wall bump")
                    return state
                affected.append(pushed_box)
                if (
                    next_pushed_box[0] in state.boxes_left
                    and next_pushed_box[1] in state.boxes_right
                ):
                    box_q.add(next_pushed_box)
                if next_pushed_box[1] in state.boxes_left:
                    box_q.add(
                        (
                            next_pushed_box[1],
                            (next_pushed_box[1][0] + 1, next_pushed_box[1][1]),
                        )
                    )
                if next_pushed_box[0] in state.boxes_right:
                    box_q.add(
                        (
                            (next_pushed_box[0][0] - 1, next_pushed_box[0][1]),
                            next_pushed_box[0],
                        )
                    )
        case "v":
            # complicated case, making a wave-front
            actual_pushed_box: typing.Optional[tuple[tup2, tup2]] = None
            if maybe_pushed_box_tile in state.boxes_left:
                actual_pushed_box = (
                    maybe_pushed_box_tile,
                    (maybe_pushed_box_tile[0] + 1, maybe_pushed_box_tile[1]),
                )
                if actual_pushed_box[1] not in state.boxes_right:
                    raise Exception("mismatched box halves")
            elif maybe_pushed_box_tile in state.boxes_right:
                actual_pushed_box = (
                    (maybe_pushed_box_tile[0] - 1, maybe_pushed_box_tile[1]),
                    maybe_pushed_box_tile,
                )
                if actual_pushed_box[0] not in state.boxes_left:
                    raise Exception("mismatched box halves")
            box_q: set[tuple[tup2, tup2]] = set()
            if actual_pushed_box is not None:
                box_q.add(actual_pushed_box)
            while box_q:
                pushed_box = box_q.pop()
                next_pushed_box = (
                    (pushed_box[0][0], pushed_box[0][1] + 1),
                    (pushed_box[1][0], pushed_box[1][1] + 1),
                )
                if (
                    next_pushed_box[0] in state.walls_left
                    or next_pushed_box[1] in state.walls_left
                    or next_pushed_box[0] in state.walls_right
                    or next_pushed_box[1] in state.walls_right
                ):
                    # Bail as soon as we'd push a box into a wall
                    print("Noop, box to wall bump")
                    return state
                affected.append(pushed_box)
                if (
                    next_pushed_box[0] in state.boxes_left
                    and next_pushed_box[1] in state.boxes_right
                ):
                    box_q.add(next_pushed_box)
                if next_pushed_box[1] in state.boxes_left:
                    box_q.add(
                        (
                            next_pushed_box[1],
                            (next_pushed_box[1][0] + 1, next_pushed_box[1][1]),
                        )
                    )
                if next_pushed_box[0] in state.boxes_right:
                    box_q.add(
                        (
                            (next_pushed_box[0][0] - 1, next_pushed_box[0][1]),
                            next_pushed_box[0],
                        )
                    )

    next_boxes_left = state.boxes_left
    next_boxes_right = state.boxes_right
    if affected:
        if move == "<" or move == ">":
            new_left_boxes = {box[1] for box in affected}
            new_right_boxes = {box[0] for box in affected}
            match move:
                case "<":
                    # remove rightmost left box, add leftmost left box
                    new_left_boxes.remove(affected[0][1])
                    new_left_boxes.add((affected[-1][0][0] - 1, affected[-1][0][1]))
                case ">":
                    # remove leftmost right box, add rightmost right box
                    new_right_boxes.remove(affected[0][0])
                    new_right_boxes.add((affected[-1][1][0] + 1, affected[-1][1][1]))
            next_boxes_left = (
                next_boxes_left - new_right_boxes - {affected[0][0]}
            ) | new_left_boxes
            next_boxes_right = (
                next_boxes_right - new_left_boxes - {affected[0][1]}
            ) | new_right_boxes
        elif move == "^" or move == "v":
            old_left_boxes = {box[0] for box in affected}
            old_right_boxes = {box[1] for box in affected}
            match move:
                case "^":
                    new_left_boxes = {(x, y - 1) for x, y in old_left_boxes}
                    new_right_boxes = {(x, y - 1) for x, y in old_right_boxes}
                case "v":
                    new_left_boxes = {(x, y + 1) for x, y in old_left_boxes}
                    new_right_boxes = {(x, y + 1) for x, y in old_right_boxes}
            next_boxes_left = (next_boxes_left - old_left_boxes) | new_left_boxes
            next_boxes_right = (next_boxes_right - old_right_boxes) | new_right_boxes
    return state._replace(
        robot=next_robot, boxes_left=next_boxes_left, boxes_right=next_boxes_right
    )


def widen_line(line: str) -> str:
    s = ""
    for c in line:
        match c:
            case "#":
                s += "##"
            case "O":
                s += "[]"
            case "@":
                s += "@."
            case ".":
                s += ".."
    return s


def main():
    input_path = util.REAL
    puzzle_input = util.load_input(input_path, 15).splitlines()
    warehouse_input = puzzle_input[: puzzle_input.index("")]
    if input_path == util.REAL:
        warehouse_input = [widen_line(line) for line in warehouse_input]
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
