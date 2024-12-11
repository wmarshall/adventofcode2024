import functools

import util


@functools.lru_cache(maxsize=None)
def blink_one_stone(stone: int, times: int) -> int:
    if times == 0:
        return 1
    if stone == 0:
        return blink_one_stone(1, times - 1)
    elif len(strd := str(stone)) % 2 == 0:
        prefix = strd[: len(strd) // 2]
        suffix = strd[len(strd) // 2 :]
        return blink_one_stone(int(prefix, base=10), times - 1) + blink_one_stone(
            int(suffix, base=10), times - 1
        )
    else:
        return blink_one_stone(stone * 2024, times - 1)


def main():
    stones = [int(i) for i in util.load_input(util.REAL, 11).split()]
    times = 75
    print(sum(blink_one_stone(s, times) for s in stones))


if __name__ == "__main__":
    main()
