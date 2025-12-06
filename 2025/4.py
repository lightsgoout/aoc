import itertools
import sys

import aoc


def silver(lines):
    res = 0
    g = aoc.grid(lines)
    for p in g:
        if g[p] == "@" and reachable(g, p):
            res += 1
    return res


def gold(lines):
    g = aoc.grid(lines)

    res = 0
    while True:
        diff = clear_pass(g)
        res += diff
        if diff == 0:
            break

    return res


def reachable(g, p) -> bool:
    count = 0
    for diff in itertools.chain(aoc.directions4(), aoc.diagonals4()):
        p2 = p + diff
        if g.inside(p2) and g[p2] == "@":
            count += 1
    return count < 4


def clear_pass(g):
    count = 0
    for p in g:
        if g[p] == "@" and reachable(g, p):
            g[p] = "."
            count += 1

    return count


def main():
    lines = []
    for line in sys.stdin.readlines():
        line = line.strip()
        if not line:
            continue
        lines.append(line)

    print("silver:", silver(lines))
    print("gold:", gold(lines))


if __name__ == "__main__":
    main()
