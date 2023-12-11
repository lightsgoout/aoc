import itertools
import sys
from copy import deepcopy


def parse():
    g = []
    for y, line in enumerate(sys.stdin.readlines()):
        line = line.strip()
        if not line:
            continue
        row = []
        for x, c in enumerate(line):
            row.append(c)
        g.append(row)
    return g


def dump_grid(g):
    for y in range(len(g)):
        row = ''
        for x in range(len(g[0])):
            c = g[y][x]
            row += c
        print(row)


def rotated(g):
    return [list(l) for l in zip(*g)]


def manhattan(y1, x1, y2, x2):
    return abs(y1 - y2) + abs(x1 - x2)


def solve(g, factor):
    rows = set()
    for y, row in enumerate(g):
        if all([c == '.' for c in row]):
            rows.add(y)

    columns = set()
    for x, row in enumerate(rotated(g)):
        if all([c == '.' for c in row]):
            columns.add(x)

    points = []
    for y in range(len(g)):
        for x in range(len(g[0])):
            if g[y][x] == '#':
                points.append((y, x))

    expanded_points = []
    for y, x in points:
        y2 = y
        for i in rows:
            if i < y:
                y2 += max(factor - 1, 1)

        x2 = x
        for i in columns:
            if i < x:
                x2 += max(factor - 1, 1)

        expanded_points.append((y2, x2))

    r = 0
    for (p1, p2) in itertools.combinations(expanded_points, 2):
        if p1 == p2:
            continue
        r += manhattan(*p1, *p2)
    return r


def main():
    g = parse()
    print('silver: ', solve(g, factor=1))
    print('gold: ', solve(g, factor=1000000))


if __name__ == '__main__':
    main()
