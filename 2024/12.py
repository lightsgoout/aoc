import dataclasses
import itertools
import typing
from collections import defaultdict
from pprint import pprint

import shapely

import aoc


def silver(lines):
    g = aoc.grid(lines)
    regions = []

    for p in g:
        sym = g[p]
        search_region(p, sym, regions)

    regions = merge_regions(regions)

    r = 0
    for reg in regions:
        r += reg.area() * reg.perimeter(g)
        # print(
        #     f"region {reg.sym} with price {reg.area()} * {reg.perimeter(g)} = {reg.price(g)}"
        # )

    return r


def search_region(p, sym, regions):
    for region in regions:
        if region.sym == sym:
            if try_grow_region(p, region):
                return

    regions.append(Region(sym=sym, points={p}))


def try_grow_region(p, region):
    for p2 in region.points:
        if aoc.is_adjacent(p, p2):
            region.points.add(p)
            return True
    return False


def merge_regions(regions):
    group = defaultdict(list)
    for r in regions:
        group[r.sym].append(r)

    while True:
        merged = 0
        for sym, regs in group.items():
            if len(regs) > 1:
                for r1, r2 in itertools.combinations(regs, 2):
                    if regions_touch(r1, r2):
                        r1.points = r1.points.union(r2.points)
                        r2.points = set()
                        merged += 1

        if merged == 0:
            break

    res = []
    for sym, regs in group.items():
        for reg in regs:
            if reg.points:
                res.append(reg)

    return res


def regions_touch(r1, r2):
    for p1 in r1.points:
        for p2 in r2.points:
            if aoc.is_adjacent(p1, p2):
                return True
    return False


@dataclasses.dataclass
class Region:
    sym: str
    points: set[aoc.point]

    def area(self):
        return len(self.points)

    def perimeter(self, g: aoc.grid):
        r = 0
        for p in self.points:
            for d in aoc.directions4():
                adj = p + d
                if not g.inside(adj):
                    r += 1
                    continue
                if g[adj] != self.sym:
                    r += 1
        return r

    def sides(self, g):
        pts = set()
        for p in self.points:
            for d in aoc.directions4():
                adj = p + d
                if not g.inside(adj):
                    pts.add(adj)
                    continue
                if g[adj] != self.sym:
                    pts.add(adj)

        crns = 0
        for a, b in itertools.combinations(list(pts), 2):
            if abs(a.x - b.x) == 1 and abs(a.y - b.y) == 1:
                for corner in corners(a, b):
                    if corner in self.points:
                        print(f"{self.sym=} found internal corner in {corner}")
                        crns += 1

        for a, b in itertools.combinations(self.points, 2):
            if abs(a.x - b.x) == 1 and abs(a.y - b.y) == 1:
                for corner in corners(a, b):
                    if corner not in self.points:
                        if opposite_corner(corner, a, b) in self.points:
                            print(
                                f"{self.sym=} found external corner in {corner} {a=} {b=}"
                            )
                            crns += 1

        return crns


def corners(a: aoc.point, b: aoc.point) -> typing.Iterable[aoc.point]:
    for candidate in [
        aoc.point(y=min(a.y, b.y), x=min(a.x, b.x)),
        aoc.point(y=max(a.y, b.y), x=max(a.x, b.x)),
        aoc.point(y=max(a.y, b.y), x=min(a.x, b.x)),
        aoc.point(y=min(a.y, b.y), x=max(a.x, b.x)),
    ]:
        if candidate != a and candidate != b:
            yield candidate


def opposite_corner(c: aoc.point, a: aoc.point, b: aoc.point) -> aoc.point:
    min_x = min(a.x, b.x, c.x)
    max_x = max(a.x, b.x, c.x)
    min_y = min(a.y, b.y, c.y)
    max_y = max(a.y, b.y, c.y)
    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            d = aoc.point(y, x)
            if d not in (a, b, c):
                return d


def gold(lines):
    g = aoc.grid(lines)
    regions = []

    for p in g:
        sym = g[p]
        search_region(p, sym, regions)

    regions = merge_regions(regions)

    r = 0
    for reg in regions:
        area = reg.area()
        sides = reg.sides(g)
        price = area * sides
        r += price
        print(f"region {reg.sym} with price {area} * {sides} = {price}")

    return r


def main():
    print("silver:", silver(aoc.stdin()))
    print("gold:", gold(aoc.stdin()))


if __name__ == "__main__":
    main()
