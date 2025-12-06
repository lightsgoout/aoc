import dataclasses
import itertools
from collections import defaultdict

import aoc


def silver(lines):
    parts = to_parts(lines[0])
    frag = defrag_parts(parts)
    return checksum(frag)


@dataclasses.dataclass
class Part:
    kind: str
    id: int


@dataclasses.dataclass
class File:
    id: int
    size: int
    start: int


def to_parts(s):
    seq = 0
    res = []
    for c, kind in zip(s, itertools.cycle(["file", "space"])):
        if kind == "file":
            res.extend([Part(kind=kind, id=seq) for _ in range(int(c))])
            seq += 1
        else:
            res.extend([Part(kind=kind, id=seq) for _ in range(int(c))])
    return res


def defrag_parts(parts):
    space = sum((1 for p in parts if p.kind == "space"))
    res = []
    tail = iter(reversed([p for p in parts if p.kind != "space"]))

    for p in parts:
        if p.kind == "space":
            res.append(next(tail))
        else:
            res.append(p)

    res = res[: len(parts) - space]
    return res


def parts_to_files(parts):
    agg = defaultdict(int)
    start = {}
    for i, p in enumerate(parts):
        if p.kind == "file":
            agg[p.id] += 1
            if p.id not in start:
                start[p.id] = i
    return [File(id=k, size=v, start=start[k]) for k, v in agg.items()]


def defrag_files(parts):
    files = parts_to_files(parts)
    files = sorted(files, key=lambda x: x.id, reverse=True)
    for file in files:
        res = move_file(parts, file)
        print(f"move {file}: {res}")


def move_file(parts, file):
    i = 0
    while i <= file.start - file.size:
        slot = parts[i : i + file.size]
        if all((p.kind == "space" for p in slot)):
            for p in parts:
                if p.kind == "file" and p.id == file.id:
                    p.kind = "space"
                    p.id = -1
            for p in parts[i : i + file.size]:
                p.kind = "file"
                p.id = file.id
            return True
        i += 1
    return False


def checksum(parts):
    r = 0
    for i, p in enumerate(parts):
        if p.kind == "file":
            r += i * p.id
    return r


def gold(lines):
    parts = to_parts(lines[0])
    s = ""
    for p in parts:
        if p.kind == "space":
            s += "."
        else:
            s += str(p.id)
    print(s)
    defrag_files(parts)
    s = ""
    for p in parts:
        if p.kind == "space":
            s += "."
        else:
            s += str(p.id)
    print(s)
    return checksum(parts)


def main():
    # print("silver:", silver(aoc.stdin()))
    print("gold:", gold(aoc.stdin()))


if __name__ == "__main__":
    main()
