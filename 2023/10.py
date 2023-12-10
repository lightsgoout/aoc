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


def get_start(g):
    for y in range(len(g)):
        for x in range(len(g[y])):
            v = g[y][x]
            if v == 'S':
                return y, x


valid_segments = {
    '|': {
        'N': {'|', '7', 'F', 'S'},
        'S': {'|', 'J', 'L', 'S'},
    },
    '-': {
        'W': {'-', 'F', 'L', 'S'},
        'E': {'-', 'J', '7', 'S'},
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
    'S': {
        'E': {'-'},
        'S': {'|'},
    },
    'G': {
        'E': {'G'},
        'S': {'G'},
        'N': {'G'},
        'W': {'G'},
    },
}


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

            try:
                n = g[y][x]
            except IndexError:
                print(f'index error: {y=} {x=}')
                raise

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
    start = get_start(g)
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

    while validate:
        p = sorted(list(validate), reverse=True)[0]
        validate.remove(p)
        y, x = p
        seen = {p}
        res = escape(g, p, seen)
        print(f'validating {p} escapes={res}')
        if res:
            print(f'{p=} escapes')
            g[y][x] = 'O'

    for y in range(len(g)):
        row = ''
        for x in range(len(g[0])):
            row += g[y][x]
        print(row)

    enclosed = 0
    for y in range(len(g)):
        for x in range(len(g[0])):
            if g[y][x] == 'I':
                enclosed += 1
    print('gold: ', enclosed)


def escape(g, p, seen):
    py, px = p
    for dy in [-1, 0, 1]:
        for dx in [-1, 0, 1]:
            if (dy, dx) == (0, 0):
                continue

            y = py + dy
            x = px + dx

            if (y, x) in seen:
                continue

            if y < 0 or x > len(g[0]) - 1 or y > len(g) - 1 or x < 0:
                continue

            if g[y][x] == 'O':
                return True

            seen.add((y, x))

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

            print(direction)

            if direction == 'N':
                left, middle, right = (py - 1, px - 1), (py - 1, px), (py - 1, px + 1)
                for l, r in [(left, middle), (middle, right)]:
                    ly, lx = l
                    ry, rx = r
                    if (g[ly][lx], g[ry][rx]) in [
                        ('|', '|'),
                        ('J', 'L'),
                        ('|', 'L'),
                        ('J', '|'),
                        ('|', 'F'),
                        ('7', '|'),
                        ('7', 'F'),
                    ]:
                        return escape(g, l, seen) or escape(g, r, seen)

            elif direction == 'S':
                left, middle, right = (py + 1, px - 1), (py + 1, px), (py + 1, px + 1)
                for l, r in [(left, middle), (middle, right)]:
                    ly, lx = l
                    ry, rx = r
                    if (g[ly][lx], g[ry][rx]) in [
                        ('|', '|'),
                        ('J', 'L'),
                        ('|', 'L'),
                        ('J', '|'),
                        ('|', 'F'),
                        ('7', '|'),
                        ('7', 'F'),
                    ]:
                        return escape(g, l, seen) or escape(g, r, seen)

            elif direction == 'E':
                left, middle, right = (py - 1, px + 1), (py, px + 1), (py + 1, px + 1)
                for l, r in [(left, middle), (middle, right)]:
                    ly, lx = l
                    ry, rx = r
                    if (g[ly][lx], g[ry][rx]) in [
                        ('L', '-'),
                        ('-', '-'),
                        ('J', 'F'),
                        ('J', '-'),
                        ('-', '7'),
                        ('-', 'F'),
                        ('L', 'F'),
                    ]:
                        return escape(g, l, seen) or escape(g, r, seen)

            elif direction == 'W':
                left, middle, right = (py - 1, px - 1), (py, px - 1), (py + 1, px - 1)
                for l, r in [(left, middle), (middle, right)]:
                    ly, lx = l
                    ry, rx = r
                    if (g[ly][lx], g[ry][rx]) in [
                        ('L', '-'),
                        ('-', '-'),
                        ('J', 'F'),
                        ('J', '-'),
                        ('-', '7'),
                        ('-', 'F'),
                        ('L', 'F'),
                    ]:
                        return escape(g, l, seen) or escape(g, r, seen)

    return False


def main():
    sys.setrecursionlimit(10000)
    g = parse()
    solve(g)


if __name__ == '__main__':
    main()
