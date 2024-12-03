import re

import util


def find_valid_muls(mem: str) -> list[tuple[int, int]]:
    return [(int(a), int(b)) for a, b in re.findall(r"mul\((\d{1,3}),(\d{1,3})\)", mem)]


def main():
    corrupted_memory = util.load_input(util.REAL, 3)
    print(sum((a * b) for a, b in find_valid_muls(corrupted_memory)))


if __name__ == "__main__":
    main()
