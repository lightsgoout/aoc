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


def _tilt(g, dy, dx):
    moves = 0
    for y, row in enumerate(g):
        for x, c in enumerate(row):
            if c == 'O':
                ny, nx = y + dy, x + dx
                if 0 <= ny <= len(g) - 1 and 0 <= nx <= len(row) - 1:
                    if g[ny][nx] == '.':
                        g[ny][nx] = 'O'
                        g[y][x] = '.'
                        moves += 1

    return moves


def tilt(g, dy, dx):
    while True:
        moves = _tilt(g, dy, dx)
        if moves == 0:
            break


def weight(g):
    r = 0
    for y, row in enumerate(g):
        for x, c in enumerate(row):
            if c == 'O':
                w = len(g) - y
                r += w
    return r


def silver(g):
    tilt(g, dy=-1, dx=0)
    return weight(g)


def find_pattern(seq):
    max_len = len(seq) // 2
    for x in range(2, max_len):
        if seq[:x] == seq[x : 2 * x]:
            return seq[:x]

    return []


def gold(g):
    cycle = []
    n = 1000
    for i in range(n):
        tilt(g, dy=-1, dx=0)
        tilt(g, dy=0, dx=-1)
        tilt(g, dy=1, dx=0)
        tilt(g, dy=0, dx=1)
        cycle.append(weight(g))

    patterns = []
    for i in range(n):
        pat = find_pattern(cycle[i:])
        if pat:
            patterns.append(pat)
    pattern = list(sorted(patterns, key=lambda x: len(x)))[0]
    print('pattern: ', pattern)

    start = -1
    for i in range(n):
        if cycle[i : i + len(pattern)] == pattern:
            start = i
            break

    assert start >= 0
    print('start: ', start)

    loop = itertools.cycle(pattern)
    v = start
    for _ in range(1000000000 - start):
        v = next(loop)

    return v


def dump_grid(g):
    for y in range(len(g)):
        row = ''
        for x in range(len(g[0])):
            c = g[y][x]
            row += c
        print(row)


def main():
    g = parse()
    print('silver: ', silver(deepcopy(g)))
    print('gold: ', gold(deepcopy(g)))


if __name__ == '__main__':
    main()
