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


class GuardState(typing.NamedTuple):
    pos: Coord
    direction: Direction


class LoopException(Exception):
    pass


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
    rows: int,
    cols: int,
    obstacles: set[Coord],
    guard_state: GuardState,
    seen_states: None | set[GuardState] = None,
) -> typing.Iterable[tuple[GuardState, Coord, set[GuardState]]]:
    if seen_states is None:
        seen_states = set()
    while True:
        # print(guard_state)
        if guard_state in seen_states:
            print("loop detected")
            raise LoopException()
        seen_states.add(guard_state)
        next_space = Coord(
            guard_state.pos.row + guard_state.direction.delta_row,
            guard_state.pos.col + guard_state.direction.delta_col,
        )
        yield guard_state, next_space, seen_states
        if not (0 <= next_space.row < rows and 0 <= next_space.col < cols):
            break
        if next_space in obstacles:
            guard_state = guard_state._replace(
                direction=DIRECTIONS[
                    (DIRECTIONS.index(guard_state.direction) + 1) % len(DIRECTIONS)
                ]
            )
            continue
        guard_state = guard_state._replace(pos=next_space)


def possible_obstructions(
    rows: int,
    cols: int,
    obstacles: set[Coord],
    guard_state: GuardState,
) -> typing.Iterable[Coord]:
    seen_positions = set()
    for state, next_space, seen_states in guard_path(
        rows, cols, obstacles, guard_state
    ):
        seen_positions.add(state.pos)
        if not (0 <= next_space.row < rows and 0 <= next_space.col < cols):
            continue
        if next_space in obstacles:
            continue
        # no need to check places we've already walked thhrough
        if next_space in seen_positions:
            continue
        next_state_if_obstructed = state._replace(
            direction=DIRECTIONS[
                (DIRECTIONS.index(state.direction) + 1) % len(DIRECTIONS)
            ]
        )
        try:
            print(f"trying {next_space}")
            for _ in guard_path(
                rows,
                cols,
                obstacles | {next_space},
                next_state_if_obstructed,
                seen_states.copy(),
            ):
                pass
        except LoopException:
            yield next_space


def main():
    lab_map = util.load_input(util.REAL, 6).splitlines()
    rows = len(lab_map)
    cols = len(lab_map[0])
    obstacles = set(find_coords(OBSTACLE, lab_map))
    guard = list(find_coords(GUARD, lab_map))[0]
    would_loop = list(possible_obstructions(
        rows, cols, obstacles, GuardState(guard, DIRECTIONS[0])
    ))
    seen = set()
    would_loop_uniq = []
    for o in would_loop:
        if o not in seen:
            would_loop_uniq.append(o)
            seen.add(o)

    for o in (would_loop_uniq):
        print(o)
    print(len(would_loop_uniq))


if __name__ == "__main__":
    main()
