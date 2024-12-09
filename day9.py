import typing
from collections import deque

import util


class File(typing.NamedTuple):
    id: typing.Optional[int]
    length: int

    def __len__(self) -> int:
        return self.length


def parse_disk_map(encoded_map: str) -> typing.Iterable[File]:
    is_file = True
    file_id = 0
    for block_len in encoded_map:
        yield File(file_id if is_file else None, int(block_len))
        if not is_file:
            file_id += 1
        is_file = not is_file


# this won't work on the real thing because it doesn't file.id > 9
def visualize(disk_map: list[File]):
    parts = [
        str(file.id if file.id is not None else ".") * len(file) for file in disk_map
    ]
    print("".join(parts))


def compact(disk_map: list[File]) -> list[File]:
    # before head is dense, no compaction needed
    head_idx = 0
    tail_idx = len(disk_map)
    while head_idx < tail_idx:
        tail_idx -= 1
        tail = disk_map[tail_idx]
        if tail.id is None:
            continue
        maybe_dense = True
        for idx in range(head_idx, tail_idx):
            head = disk_map[idx]
            if head.id is not None:
                if maybe_dense:
                    head_idx = idx
                continue
            maybe_dense = False
            if len(head) >= len(tail):
                disk_map[idx] = tail
                remaining = len(head) - len(tail)
                if remaining > 0:
                    disk_map.insert(idx + 1, File(None, remaining))
                    tail_idx += 1
                disk_map[tail_idx] = File(None, len(tail))
                break

    return disk_map


def checksum(disk_map: list[File]) -> int:
    s = 0
    block = 0
    for f in disk_map:
        for i in range(len(f)):
            if f.id is not None:
                s += f.id * block
            block += 1
    return s


def main():
    disk_map = list(parse_disk_map(util.load_input(util.REAL, 9).strip()))
    compacted = compact(disk_map)
    print(checksum(compacted))


if __name__ == "__main__":
    main()
