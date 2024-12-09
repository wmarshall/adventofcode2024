import typing
from collections import deque

import util


def parse_disk_map(encoded_map: str) -> typing.Iterable[typing.Optional[int]]:
    is_file = True
    file_id = 0
    for block_len in encoded_map:
        for _ in range(int(block_len)):
            if is_file:
                yield file_id
            else:
                yield None
        if not is_file:
            file_id += 1
        is_file = not is_file


def compact(disk_map: deque[typing.Optional[int]]) -> typing.Iterable[int]:
    from_left = True
    while len(disk_map) > 0:
        if from_left:
            val = disk_map.popleft()
            if val is None:
                from_left = False
                continue
            yield val
        else:
            val = disk_map.pop()
            if val is not None:
                yield val
                from_left = True


def main():
    disk_map = deque(parse_disk_map(util.load_input(util.REAL, 9).strip()))
    compacted = compact(disk_map)
    print(sum(i * file_id for i, file_id in enumerate(compacted)))


if __name__ == "__main__":
    main()
