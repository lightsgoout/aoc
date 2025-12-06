from ... import aoc

mmap = {
    "<": aoc.point.left,
    ">": aoc.point.right,
    "v": aoc.point.down,
    "^": aoc.point.up,
}


def silver(lines):
    grid_lines = [l for l in lines if "#" in l]
    g = aoc.grid(grid_lines)

    move_lines = [l for l in lines if "#" not in l]
    moves = "".join(move_lines)

    start = None
    for p in g:
        if g[p] == "@":
            g[p] = "."
            start = p
            break

    pos = start
    for move in moves:
        pos2 = mmap[move](pos)
        if g[pos2] == "#":
            # do nothing
            continue

        if g[pos2] == "O":
            # find empty pos3 to put the box in
            if move_boxes(g, pos2, move):
                pos = pos2

        if g[pos2] == ".":
            pos = pos2

    r = 0
    for p in g:
        if g[p] == "O":
            r += p.y * 100 + p.x

    return r


def move_boxes(g: aoc.grid, box_pos: aoc.point, move):
    # find empty pos3 to put the box in
    pos = box_pos
    while True:
        pos = mmap[move](pos)
        if g[pos] == "#":
            return False
        if g[pos] == ".":
            g[pos] = "O"
            g[box_pos] = "."
            return True


def gold(lines):
    grid_lines = [l for l in lines if "#" in l]
    double_lines = []
    for line in grid_lines:
        double_line = ""
        for c in line:
            if c == "#":
                double_line += "##"
            elif c == "O":
                double_line += "[]"
            elif c == ".":
                double_line += ".."
            elif c == "@":
                double_line += "@@"
        double_line = double_line.replace("@@", "@.")
        double_lines.append(double_line)

    g = aoc.grid(double_lines)
    g.dump()

    start = None
    for p in g:
        if g[p] == "@":
            g[p] = "."
            start = p
            break

    move_lines = [l for l in lines if "#" not in l]
    moves = "".join(move_lines)

    pos = start
    for move in moves:
        pos2 = mmap[move](pos)
        if g[pos2] == "#":
            # do nothing
            continue

        if g[pos2] == ".":
            pos = pos2
            continue

        if g[pos2] in ["[", "]"]:
            if push_box(g, pos2, move):
                pos = pos2

    r = 0
    for p in g:
        if g[p] == "[":
            r += p.y * 100 + p.x
    return r


def push_box(g: aoc.grid, orig: aoc.point, move) -> bool:
    if move in (">", "<"):
        return push_horizontally(g, orig, move)
    return push_vertically(g, orig, move, do_push=True)


def push_horizontally(g: aoc.grid, orig: aoc.point, move) -> bool:
    pos = orig
    vacancy = None
    while True:
        pos = mmap[move](pos)
        if g[pos] == "#":
            vacancy = None
            break
        if g[pos] == ".":
            vacancy = pos
            break
    if not vacancy:
        return False

    cur = vacancy
    while True:
        if move == ">":
            g[cur] = g[cur.left()]
            cur = cur.left()
        else:
            g[cur] = g[cur.right()]
            cur = cur.right()

        if cur == orig:
            g[cur] = "."
            break
    return True


def push_vertically(g: aoc.grid, pos: aoc.point, move, do_push=False) -> bool:
    boxes = [pos]
    if g[pos] == "[":
        boxes.append(pos.right())
    elif g[pos] == "]":
        boxes.append(pos.left())
    else:
        raise AssertionError("not a box")

    # each part of the box must be pushable
    parts = []
    for pos in boxes:
        pos2 = mmap[move](pos)
        if g[pos2] == "#":
            parts.append(False)
        elif g[pos2] == ".":
            parts.append(True)
        elif g[pos2] in ["[", "]"]:
            parts.append(push_vertically(g, pos2, move, do_push=False))

    if not all(parts):
        return False

    if do_push:
        readonly_g = g.copy()
        _push_boxes(g, readonly_g, pos, move)

    return True


def _push_boxes(
    g: aoc.grid, readonly_g: aoc.grid, pos: aoc.point, move, points=None, deep=False
):
    boxes = [pos]
    if points is None:
        points = []
    if readonly_g[pos] == "[":
        boxes.append(pos.right())
        points.append((pos, "["))
        points.append((pos.right(), "]"))

    elif readonly_g[pos] == "]":
        boxes.append(pos.left())
        points.append((pos, "]"))
        points.append((pos.left(), "["))

    for pos in boxes:
        pos2 = mmap[move](pos)
        if readonly_g[pos2] in ["[", "]"]:
            _push_boxes(g, readonly_g, pos2, move, points=points, deep=True)

    if not deep:
        moved_points = set([mmap[move](pos) for (pos, _) in points])
        old_points = set([pos for (pos, _) in points])

        for pos, sym in points:
            g[mmap[move](pos)] = sym

        for pos in old_points:
            if pos not in moved_points:
                g[pos] = "."


def main():
    print("silver:", silver(aoc.stdin()))
    print("gold:", gold(aoc.stdin()))


if __name__ == "__main__":
    main()
