from collections import Counter

import util


def parse(puzzle_input: str) -> tuple[list[int], list[int]]:
    puzzle_lists = ([], [])
    for line in puzzle_input.splitlines():
        split = line.split()
        if len(split) == 0:
            continue
        astr, bstr = split
        puzzle_lists[0].append(int(astr))
        puzzle_lists[1].append(int(bstr))
    return puzzle_lists


def list_distance(a: list[int], b: list[int]) -> int:
    return sum((abs(i - j) for i, j in zip(sorted(a), sorted(b))))


def similarity(a: list[int], b: list[int]) -> int:
    right_counts = Counter(b)
    return sum(aval * right_counts.get(aval, 0) for aval in a)


def main():
    puzzle_lists = parse(util.load_input(util.TEST, 1))
    print(list_dist(puzzle_lists[0], puzzle_lists[1]))
    print(similarity(puzzle_lists[0], puzzle_lists[1]))


if __name__ == "__main__":
    main()
