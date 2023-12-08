import sys


class point:
    def __init__(self, x, y, idx=0):
        self.x = x
        self.y = y
        self.idx = idx

    def __hash__(self):
        return hash((self.x, self.y))

    def __repr__(self):
        return f"idx={self.idx} ({self.x}, {self.y})"


visited = {(0, 0)}
rope_size = 10
rope = [point(0, 0, i) for i in range(rope_size)]
dump_size = 20


def dump(instruction):
    if instruction:
        print(instruction)

    for y in range(-dump_size, +dump_size):
        row = []
        for x in range(-dump_size, +dump_size):
            sym = "."
            if (x, y) == (0, 0):
                sym = "s"

            if (rope[0].x, rope[0].y) == (x, y):
                sym = "H"
            else:
                for i, p in enumerate(rope):
                    if (p.x, p.y) == (x, y):
                        sym = str(i)
                        break

            row.append(sym)

        print("".join(row))
    print("")


def dump_visited():
    print("=== visited ===")
    for y in range(-dump_size, +dump_size):
        row = []
        for x in range(-dump_size, +dump_size):
            sym = "."
            if (x, y) in visited:
                sym = "#"
            row.append(sym)

        print("".join(row))
    print("")


def move(h: point, d: str):
    if d == "R":
        h.x += 1
    elif d == "L":
        h.x -= 1
    elif d == "U":
        h.y -= 1
    elif d == "D":
        h.y += 1


def reposition_t(h: point, t: point, debug: bool):
    # if debug:
    #     if h.idx == 4 and t.idx == 5:
    #         print((h, t))

    if h.y == t.y:
        if h.x - t.x > 1:
            t.x = h.x - 1
        elif h.x - t.x < -1:
            t.x = h.x + 1
    elif h.x == t.x:
        if h.y - t.y > 1:
            t.y = h.y - 1
        elif h.y - t.y < -1:
            t.y = h.y + 1
    else:
        # diagonal
        if (abs(h.x - t.x), abs(h.y - t.y)) == (1, 1):
            pass
        elif (abs(h.x - t.x), abs(h.y - t.y)) > (1, 1):
            if h.y < t.y:
                t.y = t.y - 1
            elif h.y > t.y:
                t.y = t.y + 1

            if h.x < t.x:
                t.x = t.x - 1
            elif h.x > t.x:
                t.x = t.x + 1

        else:
            if abs(h.y - t.y) > 1:
                if h.y < t.y:
                    t.y = h.y + 1
                    t.x = h.x
                else:
                    t.y = h.y - 1
                    t.x = h.x
            elif abs(h.x - t.x) > 1:
                if h.x < t.x:
                    t.x = h.x + 1
                    t.y = h.y
                else:
                    t.x = h.x - 1
                    t.y = h.y


dump("== Initial State ==")
for line in sys.stdin.readlines():
    direction, count = line.strip().split()
    count = int(count)
    print(f"\n== {line.strip()} ==")
    for i in range(count):
        move(rope[0], direction)
        for p, (h, t) in enumerate(zip(rope, rope[1:])):
            reposition_t(h, t, debug=False)
        # noinspection PyUnboundLocalVariable
        visited.add((t.x, t.y))
    dump(None)


dump_visited()
print(len(visited))
