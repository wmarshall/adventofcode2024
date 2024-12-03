import re

import util

MUL_RE = r"(?P<mul>mul)\((?P<a>\d{1,3}),(?P<b>\d{1,3})\)"
DO_RE = r"(?P<do>do)\(\)"
DONT_RE = r"(?P<dont>don't)\(\)"
COMBINED_RE = rf"(?:{MUL_RE})|(?:{DO_RE})|(?:{DONT_RE})"


def find_valid_muls(mem: str, conditional_parse=True) -> list[tuple[int, int]]:
    valid_muls = []
    parsing_enabled = True
    for instr in re.finditer(COMBINED_RE, mem):
        match instr.groupdict():
            case {"do": "do"} if conditional_parse:
                parsing_enabled = True
            case {"dont": "don't"} if conditional_parse:
                parsing_enabled = False
            case {"mul": "mul", "a": a, "b": b} if parsing_enabled:
                valid_muls.append((int(a), int(b)))
    return valid_muls


def main():
    corrupted_memory = util.load_input(util.REAL, 3)
    print(sum((a * b) for a, b in find_valid_muls(corrupted_memory)))


if __name__ == "__main__":
    main()
