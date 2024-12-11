import util


def blink(stones: list[int]) -> list[int]:
    out_stones: list[int] = []

    for stone in stones:
        if stone == 0:
            out_stones.append(1)
        elif len(strd := str(stone)) % 2 == 0:
            prefix = strd[: len(strd) // 2]
            suffix = strd[len(strd) // 2 :]
            out_stones.append(int(prefix, base=10))
            out_stones.append(int(suffix, base=10))
        else:
            out_stones.append(stone * 2024)
    return out_stones


def main():
    stones = [int(i) for i in util.load_input(util.REAL, 11).split()]
    for _ in range(25):
        stones = blink(stones)
    print(len(stones))


if __name__ == "__main__":
    main()
