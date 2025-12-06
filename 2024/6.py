import aoc


def silver(lines):
    g = aoc.grid(lines)
    # g.dump()

    pos = None
    d = "^"

    for p in g:
        if g[p] == "^":
            pos = p
            d = "^"
            break

    while True:
        # print(f"{pos=} {d=}")
        # g.dump()
        g[pos] = "X"

        p2 = None
        if d == "^":
            p2 = pos.up()
        elif d == "v":
            p2 = pos.down()
        elif d == ">":
            p2 = pos.right()
        elif d == "<":
            p2 = pos.left()
        else:
            raise AssertionError("unknown")

        if not g.inside(p2):
            break

        if g[p2] in (".", "X"):
            pos = p2

        elif g[p2] == "#":
            d = next_d(d)

    g.dump()

    r = 0
    for p in g:
        if g[p] == "X":
            r += 1

    return r


def next_d(d):
    if d == "^":
        return ">"
    if d == ">":
        return "v"
    if d == "v":
        return "<"
    if d == "<":
        return "^"


def gold(lines):
    g = aoc.grid(lines)
    r = 0
    total = len(list(g))
    for i, p in enumerate(g):
        print(f"{i}/{total}")
        if g[p] == ".":
            g2 = g.copy()
            g2[p] = "#"
            if is_loop(g2):
                r += 1
    return r


def is_loop(g):
    pos = None
    d = "^"

    for p in g:
        if g[p] == "^":
            pos = p
            d = "^"
            break

    visited = set()
    while True:
        g[pos] = "X"
        if (pos, d) in visited:
            return True
        visited.add((pos, d))

        p2 = None
        if d == "^":
            p2 = pos.up()
        elif d == "v":
            p2 = pos.down()
        elif d == ">":
            p2 = pos.right()
        elif d == "<":
            p2 = pos.left()
        else:
            raise AssertionError("unknown")

        if not g.inside(p2):
            break

        if g[p2] in (".", "X"):
            pos = p2

        elif g[p2] == "#":
            d = next_d(d)

    return False


def main():
    print("silver:", silver(aoc.stdin()))
    print("gold:", gold(aoc.stdin()))


if __name__ == "__main__":
    main()
