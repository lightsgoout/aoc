import sys
from collections import namedtuple

point = namedtuple("point", ["x", "y"])


def down(p: point) -> point:
    return point(p.x, p.y + 1)


def up(p: point) -> point:
    return point(p.x, p.y - 1)


def left(p: point) -> point:
    return point(p.x - 1, p.y)


def right(p: point) -> point:
    return point(p.x + 1, p.y)


all_points = {point(0, 0)}
visited = {point(0, 0)}
H = point(0, 0)
T = point(0, 0)


def dump(instruction):
    if instruction:
        print("")
        print(instruction)
        print("====")
    min_x = min(p.x for p in all_points)
    max_x = max(p.x for p in all_points)
    min_y = min(p.y for p in all_points)
    max_y = max(p.y for p in all_points)

    for y in range(min_y, max_y + 1):
        row = []
        for x in range(min_x, max_x + 1):
            if (H.x, H.y) == (x, y):
                row.append("H")
            elif (T.x, T.y) == (x, y):
                row.append("T")
            else:
                row.append("*")
        print(" ".join(row))

    print("---")


for line in sys.stdin.readlines():
    direction, count = line.strip().split()
    count = int(count)
    # dump(line.strip())
    for _ in range(count):
        move = None
        if direction == "R":
            move = right
        elif direction == "L":
            move = left
        elif direction == "U":
            move = up
        elif direction == "D":
            move = down

        H = move(H)
        if H.y == T.y:
            if abs(H.x - T.x) > 1:
                T = move(T)
        elif H.x == T.x:
            if abs(H.y - T.y) > 1:
                T = move(T)
        else:
            # diagonal
            if (abs(H.x - T.x), abs(H.y - T.y)) == (1, 1):
                pass
            else:
                # чпоньк
                if direction == "U":
                    T = point(H.x, H.y + 1)
                elif direction == "D":
                    T = point(H.x, H.y - 1)
                elif direction == "R":
                    T = point(H.x - 1, H.y)
                elif direction == "L":
                    T = point(H.x + 1, H.y)

        visited.add(T)
        all_points.add(H)
        all_points.add(T)
        # dump(None)


print(len(visited))
