import sys
from collections import namedtuple

from shapely.geometry.polygon import Polygon


def silver(lines):
    p = Polygon(dig(lines))
    return int(int(p.area) + int(p.length) / 2 + 1)


def gold(lines):
    p = Polygon(dig2(lines))
    return int(int(p.area) + int(p.length) / 2 + 1)


point = namedtuple("point", ["x", "y"])


def down(p: point, c: int = 1) -> point:
    return point(p.x, p.y + c)


def up(p: point, c: int = 1) -> point:
    return point(p.x, p.y - c)


def left(p: point, c: int = 1) -> point:
    return point(p.x - c, p.y)


def right(p: point, c: int = 1) -> point:
    return point(p.x + c, p.y)


def move(p: point, d: str, c: int) -> point:
    if d == "R":
        m = right
    elif d == "L":
        m = left
    elif d == "U":
        m = up
    elif d == "D":
        m = down
    else:
        raise AssertionError("unknown move")
    return m(p, c)


def dig(lines) -> list[point]:
    polygon = [point(0, 0)]
    ptr = point(0, 0)

    for line in lines:
        d, l, _ = line.split()
        l = int(l)
        ptr = move(ptr, d, l)
        polygon.append(ptr)

    return polygon


def dig2(lines) -> list[point]:
    polygon = [point(0, 0)]
    ptr = point(0, 0)

    for line in lines:
        _, _, color = line.split()
        color = color.replace(")", "").replace("(", "")
        l = int(color.replace("#", "")[:5], 16)
        last = color[-1]
        d = None
        if last == "0":
            d = "R"
        elif last == "1":
            d = "D"
        elif last == "2":
            d = "L"
        elif last == "3":
            d = "U"
        else:
            raise AssertionError("unknown")
        ptr = move(ptr, d, l)
        polygon.append(ptr)

    return polygon


def main():
    lines = []
    for line in sys.stdin.readlines():
        line = line.strip()
        if not line:
            continue
        lines.append(line)
    print("silver: ", silver(lines))
    print("gold: ", gold(lines))


if __name__ == "__main__":
    main()
