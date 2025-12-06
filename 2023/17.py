import sys
from copy import deepcopy
from heapq import heapify, heappop
from pprint import pprint


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


def path_cost(g, p):
    r = 0
    for (y, x) in p:
        if (y, x) != (0, 0):
            r += int(g[y][x])
    return r


def same_direction(p):
    ys, xs = set(), set()
    for (y, x) in p:
        ys.add(y)
        xs.add(x)
    return len(ys) == 1 or len(xs) == 1


right = (0, 1)
left = (0, -1)
down = (1, 0)
up = (-1, 0)


def branches(g, p):
    tail = p[-1]
    paths = []
    for (dy, dx) in [right, left, down, up]:
        y, x = tail
        y += dy
        x += dx
        if y < 0 or y > len(g) - 1 or x < 0 or x > len(g[0]) - 1:
            continue

        if (y, x) in p:
            # no cycle allowed
            continue

        path = p + [(y, x)]

        # validate for max 3 same direction
        if len(path) > 3:
            if same_direction(path[-4:]):
                continue

        paths.append(path)

    return paths


def silver(g):
    start = (0, 0)
    finish = (len(g) - 1, len(g[0]) - 1)

    queue = [
        (0, [start]),
    ]
    heapify(queue)

    paths = [[start]]
    while queue:
        heat, path = heappop(queue)

        # pprint(len(paths))
        new_paths = []
        for p in paths:
            if p[-1] == finish:
                print('reached finish')
                continue

            print(f'cost = {path_cost(g, p)}')

            new_paths.extend(branches(g, p))
        if not new_paths:
            break

        paths = new_paths

    best = sys.maxsize
    for p in paths:
        best = min(best, path_cost(g, p))

    return best


def gold(g):
    return 0


def main():
    g = parse()
    print('silver: ', silver(deepcopy(g)))
    print('gold: ', gold(deepcopy(g)))


if __name__ == '__main__':
    main()
