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


def dump_visited(g, visited):
    for y in range(len(g)):
        row = ''
        for x in range(len(g[0])):
            c = g[y][x]
            if (y, x) in visited:
                c = '#'
            else:
                c = '.'
            row += c
        print(row)


right = (0, 1)
left = (0, -1)
down = (1, 0)
up = (-1, 0)

mirrors = {
    '/': {
        right: up,
        left: down,
        up: right,
        down: left,
    },
    '\\': {
        right: down,
        left: up,
        up: left,
        down: right,
    },
}

splitters = {
    '|': {
        up: [up],
        down: [down],
        right: [up, down],
        left: [up, down],
    },
    '-': {
        up: [right, left],
        down: [right, left],
        left: [left],
        right: [right],
    },
}


def traverse(g, at, impulse, visited):
    while True:
        dy, dx = impulse
        y, x = at
        y += dy
        x += dx
        at = (y, x)
        if y < 0 or y > len(g) - 1 or x < 0 or x > len(g[0]) - 1:
            return

        if (at, impulse) in visited:
            return

        visited.add((at, impulse))

        c = g[y][x]
        if c == '.':
            pass
        elif c in mirrors:
            impulse = mirrors[c][impulse]
        elif c in splitters:
            for new_impulse in splitters[c][impulse]:
                traverse(g, at, new_impulse, visited)
            return


def silver(g):
    visited = set()
    traverse(g, (0, -1), (0, 1), visited)
    dump_visited(g, set([a[0] for a in visited]))
    return len(set([a[0] for a in visited]))


def gold(g):
    best = 0
    for y in range(len(g)):
        for x in range(len(g[0])):
            if y == 0 or x == 0 or y == len(g) - 1 or x == len(g[0]) - 1:
                impulses = []
                if y == 0:
                    impulses.append(down)
                if x == 0:
                    impulses.append(right)
                if y == len(g) - 1:
                    impulses.append(up)
                if x == len(g[0]) - 1:
                    impulses.append(left)

                for impulse in impulses:
                    visited = set()
                    dy, dx = impulse
                    sy = y - dy
                    sx = x - dx
                    start = (sy, sx)
                    traverse(g, start, impulse, visited)
                    best = max(best, len(set([a[0] for a in visited])))

    return best


def main():
    # sys.setrecursionlimit(1000000)
    g = parse()
    print('silver: ', silver(deepcopy(g)))
    print('gold: ', gold(deepcopy(g)))


if __name__ == '__main__':
    main()
