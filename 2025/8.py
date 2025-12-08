import functools
import math
import operator

import aoc


def silver(lines):
    connections = 10 if len(lines) < 30 else 1000

    points = []
    for line in lines:
        p = tuple(map(int, line.split(",")))
        points.append(p)

    flat = []
    pairs = set()

    for p1 in points:
        for p2 in points:
            if p1 == p2:
                continue

            if pair_key(p1, p2) in pairs:
                continue

            flat.append((p1, p2, distance(p1, p2)))
            pairs.add(pair_key(p1, p2))

    belong = {p: {p} for p in points}

    top = iter(sorted(flat, key=lambda k: k[2]))
    i = 0
    while True:
        p1, p2, _ = next(top)
        cc1 = belong[p1]
        cc2 = belong[p2]
        cc1 |= cc2

        belong[p2] = cc1
        for p in cc2:
            belong[p] = cc1

        i += 1
        if i >= connections:
            break

    islands = set()
    for cc in belong.values():
        islands.add(frozenset(cc))

    largest = list(sorted(islands, key=lambda x: len(x), reverse=True))
    res = []
    for i, cc in enumerate(largest[:3]):
        res.append(len(cc))

    return functools.reduce(operator.mul, res)


def pair_key(p1, p2):
    return min(p1, p2), max(p1, p2)


def gold(lines):
    points = []
    for line in lines:
        p = tuple(map(int, line.split(",")))
        points.append(p)

    flat = []
    pairs = set()

    for p1 in points:
        for p2 in points:
            if p1 == p2:
                continue

            if pair_key(p1, p2) in pairs:
                continue

            flat.append((p1, p2, distance(p1, p2)))
            pairs.add(pair_key(p1, p2))

    belong = {p: {p} for p in points}

    top = iter(sorted(flat, key=lambda k: k[2]))
    while True:
        p1, p2, _ = next(top)
        cc1 = belong[p1]
        cc2 = belong[p2]
        cc1 |= cc2

        belong[p2] = cc1
        for p in cc2:
            belong[p] = cc1

        islands = set()
        for cc in belong.values():
            islands.add(frozenset(cc))

        if len(islands) == 1:
            return p1[0] * p2[0]


def distance(a, b):
    return math.sqrt(
        (a[0] - b[0]) * (a[0] - b[0])
        + (a[1] - b[1]) * (a[1] - b[1])
        + (a[2] - b[2]) * (a[2] - b[2])
    )


def main():
    print("silver:", silver(aoc.stdin()))
    print("gold:", gold(aoc.stdin()))


if __name__ == "__main__":
    main()
