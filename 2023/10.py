import sys


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
                return start, connections


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


def solve(g):
    start, connections = get_start(g)
    # print(f'{start=} {connections=}')
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

    pipe = set(pipe)

    for y in range(len(g)):
        for x in range(len(g[0])):
            if (y, x) in pipe:
                continue
            g[y][x] = 'G'

    enclosed = set()
    for y in range(len(g)):
        for x in range(len(g[0])):
            if g[y][x] == 'G':
                garbage = [(y, x)]
                visited = set(garbage)
                while True:
                    n = next_pipe(g, garbage[-1], visited)
                    if n is None:
                        break
                    garbage.append(n)
                    visited.add(n)

                if any([y == 0 or y == len(g) - 1 or x == 0 or x == len(g[0]) - 1 for y, x in garbage]):
                    # escaped
                    pass
                else:
                    enclosed = enclosed.union(visited)

    validate = set()
    for y in range(len(g)):
        for x in range(len(g[0])):
            p = (y, x)
            if p in pipe:
                c = g[y][x]
            elif p in enclosed:
                c = 'I'
                validate.add(p)
            else:
                c = 'O'
            g[y][x] = c

    # merge
    removes = set()
    while True:
        changes = 0
        validate = validate.difference(removes)
        for p in validate:
            y, x = p
            for dy in [-1, 0, 1]:
                for dx in [-1, 0, 1]:
                    if (dy, dx) == (0, 0):
                        continue

                    yy = y + dy
                    xx = x + dx
                    if yy < 0 or xx > len(g[0]) - 1 or yy > len(g) - 1 or xx < 0:
                        continue

                    if g[yy][xx] == 'O':
                        g[y][x] = 'O'
                        changes += 1
                        removes.add(p)

        if not changes:
            break

    for y in range(len(g)):
        row = ''
        for x in range(len(g[0])):
            row += g[y][x]
        print(row)

    validate = set()
    for y in range(len(g)):
        for x in range(len(g[0])):
            if g[y][x] == 'I':
                validate.add((y, x))

    # validate = {(6, 6)}
    escaped = set()
    while validate:
        # p = sorted(list(validate), key=lambda pp: (pp[1], pp[0]))[0]
        # validate.remove(p)
        p = validate.pop()
        y, x = p
        seen = {(*p, '')}
        print(f'validating {p} remain={len(validate)}')
        res = escape(g, p, seen)
        # print(f'{p} escapes={res}')
        if res:
            # print(f'{p=} escapes')
            # g[y][x] = 'O'
            escaped.add(p)

    for y in range(len(g)):
        row = ''
        for x in range(len(g[0])):
            if (y, x) in escaped:
                g[y][x] = 'O'
            row += g[y][x]
        print(row)

    enclosed = 0
    for y in range(len(g)):
        for x in range(len(g[0])):
            if g[y][x] == 'I':
                enclosed += 1
    print('gold: ', enclosed)
    # dump_grid(g)


def dump_grid(g):
    for y in range(len(g)):
        row = ''
        for x in range(len(g[0])):
            c = g[y][x]
            if c not in ('I', 'O'):
                c = 'P'
            row += c
        print(row)


def escape(g, p, seen):
    py, px = p
    for dy in [-1, 0, 1]:
        for dx in [-1, 0, 1]:
            if (dy, dx) == (0, 0):
                continue

            y = py + dy
            x = px + dx
            if y < 0 or x > len(g[0]) - 1 or y > len(g) - 1 or x < 0:
                continue

            # print(f'im in {y=} {x=}')

            dm = {
                'W': y == py and x < px,
                'N': y < py and x == px,
                'S': y > py and x == px,
                'E': y == py and x > px,
            }
            direction = None
            for d, v in dm.items():
                if v:
                    direction = d
                    break
            if not direction:
                continue

            if (y, x, direction) in seen:
                continue

            seen.add((y, x, direction))
            if g[y][x] == 'I' and g[py][px] == 'I':
                # print(f'passing to {y},{x}')
                # return escape(g, (y, x), seen)
                if escape(g, (y, x), seen):
                    print(f'{py},{px} escapes through I at {y},{x}')
                    return True

            # print(f'checking {y},{x}={g[y][x]} {direction=}')

            prev = g[py][px]
            v = g[y][x]
            if v == 'O':
                if direction == 'N' and prev not in ['-']:
                    print(f'N escaped: {y}, {x} {v=}')
                    return True
                if direction == 'S' and prev not in ['-']:
                    print(f'S escaped: {y}, {x} {v=}')
                    return True
                if direction == 'E' and prev not in ['|']:
                    print(f'E escaped: {y}, {x} {v=}')
                    return True
                if direction == 'W' and prev not in ['|']:
                    print(f'W escaped: {y}, {x} {v=}')
                    return True

            escapes = {}
            through = None
            if direction in ('N', 'S'):
                if v in ('F', 'L', '|') and x > 0 and g[y][x - 1] in ('|', 'J', '7'):
                    through = (y, x - 1)
                    assert direction not in escapes
                    escapes[direction] = escape(g, (y, x - 1), seen)
                if v in ('|', 'J', '7') and x < len(g[0]) - 1 and g[y][x + 1] in ('|', 'F', 'L'):
                    through = (y, x + 1)
                    assert direction not in escapes
                    escapes[direction] = escape(g, (y, x + 1), seen)
            elif direction in ('E', 'W'):
                if v in ('J', 'L', '-') and y < len(g) - 1 and g[y + 1][x] in ('-', '7', 'F'):
                    through = (y + 1, x)
                    assert direction not in escapes
                    escapes[direction] = escape(g, (y + 1, x), seen)
                if v in ('F', '7', '-') and y > 0 and g[y - 1][x] in ('-', 'J', 'L'):
                    through = (y - 1, x)
                    assert direction not in escapes
                    escapes[direction] = escape(g, (y - 1, x), seen)

            if any(escapes.values()):
                ty, tx = through
                assert len(escapes.values()) == 1
                print(
                    f'{py},{px}({g[py][px]}) escapes through {y},{x}({g[y][x]}) through {through}({g[ty][tx]}) {direction=}:'
                )
                # print(f'{y},{x} = {v}: {escapes=} {through=} {direction=} {prev=} ({py},{px})')
                return True

    return False


def main():
    sys.setrecursionlimit(100000)
    g = parse()
    solve(g)


if __name__ == '__main__':
    main()
