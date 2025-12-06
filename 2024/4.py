import aoc


def silver(lines):
    g = aoc.grid(lines)
    r = 0
    for p in g:
        if g[p] == "X":
            for d in aoc.directions():
                r += xmas(g, p, d)
    return r


def xmas(g, p, d):
    want = "MAS"
    w = ""
    while len(w) < 3:
        p += d
        w += g.try_point(p, "Z")
    return 1 if w == want else 0


def gold(lines):
    g = aoc.grid(lines)
    r = 0
    want = {"M", "S"}
    for p in g:
        if g[p] == "A":
            diag1 = [
                g.try_point(aoc.point(p.y - 1, p.x - 1), "Z"),
                g.try_point(aoc.point(p.y + 1, p.x + 1), "Z"),
            ]
            diag2 = [
                g.try_point(aoc.point(p.y - 1, p.x + 1), "Z"),
                g.try_point(aoc.point(p.y + 1, p.x - 1), "Z"),
            ]
            if set(diag1) == want and set(diag2) == want:
                r += 1

    return r


def main():
    print("silver:", silver(aoc.stdin()))
    print("gold:", gold(aoc.stdin()))


if __name__ == "__main__":
    main()
