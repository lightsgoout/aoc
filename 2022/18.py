import sys
from collections import namedtuple

point = namedtuple('point', 'x y z')


def solve_silver(cubes):
    index = {}
    for c in cubes:
        index[c] = c

    surface = 0
    for c in cubes:
        covered = 0
        if index.get(top(c)):
            covered += 1
        if index.get(bottom(c)):
            covered += 1
        if index.get(left(c)):
            covered += 1
        if index.get(right(c)):
            covered += 1
        if index.get(closer(c)):
            covered += 1
        if index.get(further(c)):
            covered += 1
        surface += 6 - covered
    return surface


def solve_gold(cubes):
    cubes = set(cubes)

    min_x = sys.maxsize
    min_y = sys.maxsize
    min_z = sys.maxsize
    max_x = -sys.maxsize
    max_y = -sys.maxsize
    max_z = -sys.maxsize
    for c in cubes:
        min_x = min(c.x - 1, min_x)
        min_y = min(c.y - 1, min_y)
        min_z = min(c.z - 1, min_z)
        max_x = max(c.x + 1, max_x)
        max_y = max(c.y + 1, max_y)
        max_z = max(c.z + 1, max_z)

    seen = set()
    candidates = [point(min_x, min_y, min_z)]
    result = 0
    while len(candidates) > 0:
        p = candidates.pop()
        if p in seen:
            continue
        seen.add(p)

        for p2 in adjacent(p):
            if p2 in cubes:
                result += 1
            else:
                if (
                        p2 not in candidates
                        and p2 not in seen
                        and p2.x >= min_x
                        and p2.y >= min_y
                        and p2.z >= min_z
                        and p2.x <= max_x
                        and p2.y <= max_y
                        and p2.z <= max_z
                ):
                    candidates.append(p2)
    return result


def adjacent(c: point) -> list[point]:
    return [
        point(c.x - 1, c.y, c.z),
        point(c.x + 1, c.y, c.z),
        point(c.x, c.y - 1, c.z),
        point(c.x, c.y + 1, c.z),
        point(c.x, c.y, c.z + 1),
        point(c.x, c.y, c.z - 1),
    ]


def top(c: point) -> point:
    return point(c.x, c.y + 1, c.z)


def bottom(c: point) -> point:
    return point(c.x, c.y - 1, c.z)


def left(c: point) -> point:
    return point(c.x - 1, c.y, c.z)


def right(c: point) -> point:
    return point(c.x + 1, c.y, c.z)


def closer(c: point) -> point:
    return point(c.x, c.y, c.z + 1)


def further(c: point) -> point:
    return point(c.x, c.y, c.z - 1)


def main():
    cubes = []
    for line in sys.stdin.readlines():
        cubes.append(point(*map(int, line.split(','))))

    print('silver:', solve_silver(cubes))
    print('gold:', solve_gold(cubes))


if __name__ == '__main__':
    main()
