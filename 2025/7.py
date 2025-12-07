from collections import defaultdict

import aoc


def silver(lines):
    g = aoc.grid(lines)
    paths = set()
    for p in g:
        if g[p] == "S":
            paths.add(p)
            break

    splits = 0

    while paths:
        tmp = set()
        for p in paths:
            p2 = p.down()
            if not g.inside(p2):
                continue

            if g[p2] == "^":
                splits += 1
                l, r = p2.left(), p2.right()
                if g.inside(l):
                    tmp.add(l)
                if g.inside(r):
                    tmp.add(r)
                continue

            tmp.add(p2)

        paths = tmp

    return splits


def gold(lines):
    g = aoc.grid(lines)

    rays = defaultdict(int)
    for p in g:
        if g[p] == "S":
            rays[p.x] += 1
            break

    for y in range(1, g.max_y + 1):
        new_rays = defaultdict(int)
        for x in range(g.max_x + 1):
            p = aoc.point(y=y, x=x)
            if g[p] == "^":
                count = rays[x]
                if count == 0:
                    continue

                l, r = p.left(), p.right()
                if g.inside(l):
                    new_rays[l.x] += count
                if g.inside(r):
                    new_rays[r.x] += count
            else:
                new_rays[x] += rays[x]

        rays = new_rays

    return sum(rays.values())


def main():
    print("silver:", silver(aoc.stdin()))
    print("gold:", gold(aoc.stdin()))


if __name__ == "__main__":
    main()
