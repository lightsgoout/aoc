import sys
import typing
from collections import namedtuple
from copy import deepcopy
from functools import lru_cache

_point = namedtuple("point", ["y", "x"])


class point(_point):
    def down(self, c: int = 1) -> "point":
        return point(self.y + c, self.x)

    def up(self, c: int = 1) -> "point":
        return point(self.y - c, self.x)

    def left(self, c: int = 1) -> "point":
        return point(self.y, self.x - c)

    def right(self, c: int = 1) -> "point":
        return point(self.y, self.x + c)

    def __add__(self, other: "point") -> "point":
        return point(self.y + other.y, self.x + other.x)

    def __sub__(self, other: "point") -> "point":
        return point(self.y - other.y, self.x - other.x)


class grid:
    def __init__(self, lines):
        g = []
        for line in lines:
            row = []
            for c in line:
                row.append(c)
            g.append(row)

        self.g = g
        self.max_y = len(g) - 1
        self.max_x = len(g[0]) - 1
        self.width = len(g[0])
        self.height = len(g)

    def __iter__(self) -> typing.Iterator[point]:
        for y in range(self.max_y + 1):
            for x in range(self.max_x + 1):
                yield point(y, x)

    def __getitem__(self, p: point):
        return self.g[p.y][p.x]

    def __setitem__(self, p: point, value):
        self.g[p.y][p.x] = value

    def __hash__(self):
        return hash(tuple([self[p] for p in self]))

    def inside(self, p: point):
        return not (p.y < 0 or p.y > self.max_y or p.x < 0 or p.x > self.max_x)

    def try_point(self, p: point, on_outside):
        if not self.inside(p):
            return on_outside
        return self[p]

    def dump(self, special=None, clear_non_special=False, limit_to_special=False):
        max_y = self.max_y + 1
        max_x = self.max_x + 1
        if limit_to_special:
            max_y = 0
            max_x = 0
            for points, _ in special:
                for p in points:
                    max_y = max(max_y, p.y)
                    max_x = max(max_x, p.x)
            max_y += 1
            max_x += 1

        for y in range(max_y):
            row = ""
            for x in range(max_x):
                c = self.g[y][x]
                sp = False
                for points, char in special or []:
                    if point(y, x) in points:
                        c = char
                        sp = True
                        break
                if clear_non_special and not sp:
                    c = " "
                row += c
            print(row)

    def copy(self):
        return deepcopy(self)


def directions() -> typing.Iterator["point"]:
    for dy in [-1, 0, 1]:
        for dx in [-1, 0, 1]:
            if (dy, dx) == (0, 0):
                continue
            yield point(dy, dx)


def is_adjacent(p1: point, p2: point) -> bool:
    for d in directions4():
        if p1 + d == p2:
            return True
    return False


def directions4() -> typing.Iterator["point"]:
    yield point(-1, 0)
    yield point(1, 0)
    yield point(0, 1)
    yield point(0, -1)


def diagonals4() -> typing.Iterator["point"]:
    yield point(-1, -1)
    yield point(1, 1)
    yield point(-1, 1)
    yield point(1, -1)


@lru_cache
def stdin():
    lines = []
    for line in sys.stdin.readlines():
        if line := line.strip():
            lines.append(line)
    return lines
