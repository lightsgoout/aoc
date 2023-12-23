import sys
from copy import deepcopy


def parse():
    data = []
    g = []
    for y, line in enumerate(sys.stdin.readlines()):
        line = line.strip()
        if not line:
            if g:
                data.append(g)
                g = []
            continue
        row = []
        for x, c in enumerate(line):
            row.append(c)
        g.append(row)

    if g:
        data.append(g)

    return data


def rotated(g):
    return list(zip(*g))


def reflection(g):
    for x in range(len(g[0])):
        valid = True
        for y, row in enumerate(g):
            left, right = row[:x], row[x:]
            m = min(len(left), len(right))
            if m == 0:
                valid = False
                break

            left = list(reversed(list(reversed(left))[:m]))
            right = right[:m]

            if left != list(reversed(right)):
                valid = False
                break

        if valid:
            return x

    return 0


def multi_reflection(g):
    result = []
    for x in range(len(g[0])):
        valid = True
        for y, row in enumerate(g):
            left, right = row[:x], row[x:]
            m = min(len(left), len(right))
            if m == 0:
                valid = False
                break

            left = list(reversed(list(reversed(left))[:m]))
            right = right[:m]

            if left != list(reversed(right)):
                valid = False
                break

        if valid:
            result.append(x)

    return result


def silver(data):
    vert = 0
    horiz = 0
    for i, g in enumerate(data):
        vert += reflection(g)
        horiz += reflection(rotated(g))

    return vert + 100 * horiz


def alternate(g):
    v, h = reflection(g), reflection(rotated(g))
    for y, row in enumerate(g):
        for x, c in enumerate(row):
            ag = deepcopy(g)
            ag[y][x] = '.' if c == '#' else '#'

            for alt_v in multi_reflection(ag):
                if alt_v != 0 and alt_v != v:
                    return alt_v, 0

            for alt_h in multi_reflection(rotated(ag)):
                if alt_h != 0 and alt_h != h:
                    return 0, alt_h

    print('falling back')
    return v, h


def gold(data):
    vert = 0
    horiz = 0
    for i, g in enumerate(data):
        print('pattern ', i)
        dump_grid(g)
        v, h = alternate(g)
        vert += v
        horiz += h

    return vert + 100 * horiz


def dump_grid(g):
    for y in range(len(g)):
        row = ''
        for x in range(len(g[0])):
            c = g[y][x]
            row += c
        print(row)


def main():
    data = parse()
    # for i, pattern in enumerate(data):
    #     print('pattern ', i)
    #     dump_grid(pattern)

    # pprint(data)
    print('silver: ', silver(data))
    print('gold: ', gold(data))


if __name__ == '__main__':
    main()
