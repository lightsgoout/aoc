import dataclasses
import math
from pprint import pprint

import aoc


def silver(lines):
    arcades = parse(lines, add=0)
    res = 0
    for arc in arcades:
        a, b = solve2(arc)
        res += int(a) * 3 + int(b)
    return res


def gold(lines):
    arcades = parse(lines, add=10000000000000)
    res = 0
    for arc in arcades:
        a, b = solve2(arc)
        res += int(a) * 3 + int(b)

        # 153289529809382 too high
        # 77878889923885 too high
        # 77407675412647

    return res


@dataclasses.dataclass
class Arcade:
    a: aoc.point
    b: aoc.point
    p: aoc.point


def solve_retarded(arc: Arcade):
    max_a = 0
    current = aoc.point(0, 0)
    for i in range(102):
        max_a += 1
        current += arc.a
        if current.x > arc.p.x or current.y > arc.p.y:
            break

    max_b = 0
    current = aoc.point(0, 0)
    for i in range(102):
        max_b += 1
        current += arc.b
        if current.x > arc.p.x or current.y > arc.p.y:
            break

    wins = []
    for a in reversed(list(range(max_a + 1))):
        for b in reversed(list(range(max_b + 1))):
            y, x = 0, 0
            y += arc.a.y * a
            x += arc.a.x * a

            y += arc.b.y * b
            x += arc.b.x * b

            if (y, x) == arc.p:
                wins.append((a, b))

    if not wins:
        return 0

    best = 9999999999
    for a, b in wins:
        best = min(best, a * 3 + b)
    return best


def solve2(arc: Arcade):
    import numpy as np

    """
Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400    
    """

    """
    94X = 8400
    22X = 8400
    34Y = 5400
    67Y = 5400
    """
    A = np.array([[arc.a.x, arc.b.x], [arc.a.y, arc.b.y]])
    B = np.array([arc.p.x, arc.p.y])

    a, b = np.linalg.solve(A, B)

    if a <= 0 or b <= 0:
        return 0, 0

    a, b = int(round(a, 1)), int(round(b, 1))

    # validate
    y, x = 0, 0
    y += arc.a.y * a
    y += arc.b.y * b
    x += arc.a.x * a
    x += arc.b.x * b
    if aoc.point(y, x) != arc.p:
        return 0, 0

    print(a, b)

    return int(a), int(b)


def parse(lines, add=0) -> list[Arcade]:
    res = []
    ax, ay, bx, by, px, py = 0, 0, 0, 0, 0, 0
    for line in lines:
        left, right = line.split(":")
        if left.startswith("Button A"):
            dx, dy = right.split(",")
            ax = int(dx.split("+")[-1])
            ay = int(dy.split("+")[-1])
        elif left.startswith("Button B"):
            dx, dy = right.split(",")
            bx = int(dx.split("+")[-1])
            by = int(dy.split("+")[-1])
        elif left.startswith("Prize"):
            dx, dy = right.split(",")
            px = int(dx.split("=")[-1]) + add
            py = int(dy.split("=")[-1]) + add
            res.append(
                Arcade(
                    aoc.point(ay, ax),
                    aoc.point(by, bx),
                    aoc.point(py, px),
                )
            )

    return res


def main():
    print("silver:", silver(aoc.stdin()))
    print("gold:", gold(aoc.stdin()))


if __name__ == "__main__":
    main()
