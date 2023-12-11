import sys
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


def get_direction(p1, p2):
    py, px = p1
    y, x = p2
    dm = {
        y < py and x < px: 'NW',
        y == py and x < px: 'W',
        y > py and x < px: 'SW',
        y < py and x == px: 'N',
        y == py and x == px: 'impossible',
        y > py and x == px: 'S',
        y < py and x > px: 'NE',
        y == py and x > px: 'E',
        y > py and x > px: 'SE',
    }
    return dm[True]


def get_start(g):
    for y in range(len(g)):
        for x in range(len(g[y])):
            v = g[y][x]
            if v == 'S':
                start = y, x
                connections = []
                for dy in [-1, 0, 1]:
                    for dx in [-1, 0, 1]:
                        if (dy, dx) == (0, 0):
                            continue

                        p2 = (y + dy, x + dx)
                        y2, x2 = p2
                        direction = get_direction((y, x), p2)
                        if direction == 'N' and g[y2][x2] in ('7', 'F', '|'):
                            connections.append((direction, g[y2][x2]))
                        if direction == 'S' and g[y2][x2] in ('J', 'L', '|'):
                            connections.append((direction, g[y2][x2]))
                        if direction == 'E' and g[y2][x2] in ('-', 'J', '7'):
                            connections.append((direction, g[y2][x2]))
                        if direction == 'W' and g[y2][x2] in ('-', 'L', 'F'):
                            connections.append((direction, g[y2][x2]))

                assert len(connections) == 2
                shape = {
                    'NE': '7',
                    'NW': 'F',
                    'ES': 'F',
                    'SW': 'L',
                }[''.join([d for d, _ in connections])]

                return start, shape, connections


valid_segments = {
    '|': {
        'N': {'|', '7', 'F'},
        'S': {'|', 'J', 'L'},
    },
    '-': {
        'W': {'-', 'F', 'L'},
        'E': {'-', 'J', '7'},
    },
    'L': {
        'E': {'-', 'J', '7'},
        'N': {'|', '7', 'F'},
    },
    'J': {
        'N': {'|', '7', 'F'},
        'W': {'-', 'L', 'F'},
    },
    '7': {
        'S': {'|', 'J', 'L'},
        'W': {'-', 'L', 'F'},
    },
    'F': {
        'S': {'|', 'J', 'L'},
        'E': {'-', 'J', '7'},
    },
    'S': {},
    'G': {
        'E': {'G'},
        'S': {'G'},
        'N': {'G'},
        'W': {'G'},
    },
}


def opposite(d):
    return {
        'S': 'N',
        'E': 'W',
        'N': 'S',
        'W': 'E',
    }[d]


def next_pipe(g, p, visited):
    py, px = p
    prev = g[py][px]
    for dy in [-1, 0, 1]:
        for dx in [-1, 0, 1]:
            if (dy, dx) == (0, 0):
                continue

            y = py + dy
            x = px + dx

            if y < 0 or x > len(g[0]) - 1 or y > len(g) - 1 or x < 0:
                continue

            n = g[y][x]

            dm = {
                y < py and x < px: 'NW',
                y == py and x < px: 'W',
                y > py and x < px: 'SW',
                y < py and x == px: 'N',
                y == py and x == px: 'impossible',
                y > py and x == px: 'S',
                y < py and x > px: 'NE',
                y == py and x > px: 'E',
                y > py and x > px: 'SE',
            }
            d = dm[True]
            if n in (valid_segments[prev].get(d) or set()) and ((y, x) not in visited):
                return y, x


import subprocess


def polygon_check(p, pipe):
    solution = (
        "select st_contains(st_makepolygon(st_geomfromtext('LINESTRING({points})')), st_geomfromtext('point({point})'));"
    ).format(
        points=','.join([f'{y} {x}' for (y, x) in [*pipe, pipe[0]]]),
        point='{} {}'.format(p[0], p[1]),
    )
    output = subprocess.check_output(f"psql -c \"{solution}\"", shell=True)
    return b'\n f\n' in output


def solve(g):
    start, shape, connections = get_start(g)
    print(f'{start=} {shape=} {connections=}')
    for direction, symbol in connections:
        valid_segments['S'][direction] = symbol
        valid_segments[symbol][opposite(direction)].add('S')

    pipe = [start]
    while True:
        visited = set(pipe)
        n = next_pipe(g, pipe[-1], visited)
        if n is None:
            break
        pipe.append(n)

    print('silver: ', int(len(pipe) / 2))
    sy, sx = start
    g[sy][sx] = shape

    pipe_set = set(pipe)

    for y in range(len(g)):
        for x in range(len(g[0])):
            if (y, x) in pipe_set:
                continue
            g[y][x] = 'G'

    escapes = set()
    for y in range(len(g)):
        for x in range(len(g[0])):
            if (y, x) in pipe:
                continue

            if polygon_check((y, x), pipe):
                escapes.add((y, x))

    enclosed = 0
    for y in range(len(g)):
        for x in range(len(g[0])):
            if (y, x) in escapes:
                g[y][x] = 'O'
            elif (y, x) not in pipe:
                g[y][x] = 'I'
                enclosed += 1

    # dump_grid(g, pipe, True)
    # print()
    # dump_grid(g, pipe, False)

    print('gold:', enclosed)


def dump_grid(g, pipe, as_pipe=False):
    for y in range(len(g)):
        row = ''
        for x in range(len(g[0])):
            c = g[y][x]
            if as_pipe and (y, x) in pipe:
                c = 'P'
            row += c
        print(row)


def main():
    g = parse()
    solve(g)


if __name__ == '__main__':
    main()
