import itertools
from collections import defaultdict
from pprint import pprint

import aoc


def silver(lines):
    g = aoc.grid(lines)
    ants = defaultdict(set)

    for p in g:
        if g[p] not in ("#", "."):
            ants[g[p]].add(p)

    for ant, points in ants.items():
        for a, b in itertools.combinations(points, 2):
            y_diff = abs(a.y - b.y)
            x_diff = abs(a.x - b.x)

            if a.y <= b.y and a.x <= b.x:
                c = aoc.point(a.y - y_diff, a.x - x_diff)
                d = aoc.point(b.y + y_diff, b.x + x_diff)
            elif a.y <= b.y and a.x > b.x:
                c = aoc.point(a.y - y_diff, a.x + x_diff)
                d = aoc.point(b.y + y_diff, b.x - x_diff)
            elif a.y >= b.y and a.x > b.x:
                c = aoc.point(a.y + y_diff, a.x + x_diff)
                d = aoc.point(b.y - y_diff, b.x - x_diff)
            else:
                c = aoc.point(a.y + y_diff, a.x - x_diff)
                d = aoc.point(b.y - y_diff, b.x + x_diff)

            if g.inside(c):
                g[c] = "#"
            if g.inside(d):
                g[d] = "#"

    r = 0
    for p in g:
        if g[p] == "#":
            r += 1

    # g.dump()
    return r


def gold(lines):
    g = aoc.grid(lines)
    ants = defaultdict(set)

    for p in g:
        if g[p] not in ("#", "."):
            ants[g[p]].add(p)

    for ant, points in ants.items():
        for a, b in itertools.combinations(points, 2):
            g[a] = "#"
            g[b] = "#"
            add_antinode(g, a, b, set())

    r = 0
    for p in g:
        if g[p] == "#":
            r += 1

    return r


def add_antinode(g, a, b, v):
    y_diff = abs(a.y - b.y)
    x_diff = abs(a.x - b.x)
    v.add((a, b))

    if a.y <= b.y and a.x <= b.x:
        c = aoc.point(a.y - y_diff, a.x - x_diff)
        d = aoc.point(b.y + y_diff, b.x + x_diff)
    elif a.y <= b.y and a.x > b.x:
        c = aoc.point(a.y - y_diff, a.x + x_diff)
        d = aoc.point(b.y + y_diff, b.x - x_diff)
    elif a.y >= b.y and a.x > b.x:
        c = aoc.point(a.y + y_diff, a.x + x_diff)
        d = aoc.point(b.y - y_diff, b.x - x_diff)
    else:
        c = aoc.point(a.y + y_diff, a.x - x_diff)
        d = aoc.point(b.y - y_diff, b.x + x_diff)
    if g.inside(c):
        g[c] = "#"
        if (a, c) not in v:
            add_antinode(g, a, c, v)
    if g.inside(d):
        g[d] = "#"
        if (b, d) not in v:
            add_antinode(g, b, d, v)


def main():
    print("silver:", silver(aoc.stdin()))
    print("gold:", gold(aoc.stdin()))


if __name__ == "__main__":
    main()
