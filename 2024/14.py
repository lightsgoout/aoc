import functools
import operator
from collections import defaultdict
from pprint import pprint

import aoc


def silver(lines):
    width = 101
    height = 103
    if len(lines) == 12:
        width = 11
        height = 7

    lines2 = []
    for y in range(height):
        lines2.append("".join("." for _ in range(width)))

    g = aoc.grid(lines2)

    robots = []
    velocities = []
    for line in lines:
        left, right = line.split()
        x, y = left.split("=")[-1].split(",")
        robots.append(aoc.point(y=int(y), x=int(x)))
        x, y = right.split("=")[-1].split(",")
        velocities.append(aoc.point(y=int(y), x=int(x)))

    for _ in range(100):
        robots2 = []
        for r, v in zip(robots, velocities):
            y = r.y + v.y
            x = r.x + v.x
            if y > g.max_y:
                y = y - g.max_y - 1
            elif y < 0:
                y = g.max_y + y + 1
            if x > g.max_x:
                x = x - g.max_x - 1
            elif x < 0:
                x = g.max_x + x + 1
            robots2.append(aoc.point(y=y, x=x))
        robots = robots2

    quads = defaultdict(int)
    for r in robots:
        if r.y < height // 2 and r.x < width // 2:
            quads[0] += 1
        elif r.y < height // 2 and r.x > width // 2:
            quads[1] += 1
        elif r.y > height // 2 and r.x < width // 2:
            quads[2] += 1
        elif r.y > height // 2 and r.x > width // 2:
            quads[3] += 1

    pprint(quads)

    return functools.reduce(operator.mul, quads.values())


def gold(lines):
    width = 101
    height = 103
    if len(lines) == 12:
        width = 11
        height = 7

    lines2 = []
    for y in range(height):
        lines2.append("".join("." for _ in range(width)))

    g = aoc.grid(lines2)

    robots = []
    velocities = []
    for line in lines:
        left, right = line.split()
        x, y = left.split("=")[-1].split(",")
        robots.append(aoc.point(y=int(y), x=int(x)))
        x, y = right.split("=")[-1].split(",")
        velocities.append(aoc.point(y=int(y), x=int(x)))

    for i in range(50000):
        for j, (r, v) in enumerate(zip(robots, velocities)):
            y = r.y + v.y
            x = r.x + v.x
            if y > g.max_y:
                y = y - g.max_y - 1
            elif y < 0:
                y = g.max_y + y + 1
            if x > g.max_x:
                x = x - g.max_x - 1
            elif x < 0:
                x = g.max_x + x + 1

            robots[j] = aoc.point(y=y, x=x)

        if connected_count(robots) > len(robots) * 0.50:
            print(f"===== {i=} =====")
            g.dump(special=[(set(robots), "#")], clear_non_special=True)
            return i + 1


def connected_count(robots):
    r = 0
    s = set(robots)
    for p in s:
        exists = False
        for d in aoc.directions4():
            if p + d in s:
                exists = True
                break
        if exists:
            r += 1
    return r


def connected(robots):
    s = set(robots)
    for p in s:
        exists = False
        for d in aoc.directions4():
            if p + d in s:
                exists = True
                break
        if not exists:
            return False
    return True


def main():
    print("silver:", silver(aoc.stdin()))
    print("gold:", gold(aoc.stdin()))


if __name__ == "__main__":
    main()
