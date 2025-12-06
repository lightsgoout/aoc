import dataclasses
import math

import aoc


import heapq


def solve(lines):
    g = aoc.grid(lines)
    start = None
    end = None
    for p in g:
        if g[p] == "S":
            start = p
        if g[p] == "E":
            end = p

    optimize_grid(g)

    best = 9999999999999
    sols = []
    for sol in search(g, start, end):
        new_best = min(best, sol.cost)
        if new_best < best:
            best = new_best
            sols = [sol]
        elif new_best == best:
            sols.append(sol)
            # g.dump(special=[(sol.path, "\033[32m" + "o" + "\033[0m")])
            # print(f"best path so far: {best=}")

    points = set()
    for s in sols:
        points |= s.s
    return best, len(points)


def optimize_grid(g: aoc.grid):
    walls_added = 0
    while True:
        changes = 0
        for p in g:
            walls_around = 0
            if g[p] == ".":
                for d in aoc.directions4():
                    p2 = p + d
                    if g[p2] == "#":
                        walls_around += 1
            if walls_around == 3:
                g[p] = "#"
                changes += 1
                walls_added += 1
        if changes == 0:
            break
    return walls_added


def get_crossroads(g: aoc.grid):
    crossroads = set()
    for p in g:
        if g[p] == ".":
            opts = 0
            for d in aoc.directions4():
                p2 = p + d
                if g.inside(p2) and g[p2] == ".":
                    opts += 1
            if opts > 2:
                crossroads.add(p)
    return crossroads


@dataclasses.dataclass
class Solution:
    path: list[aoc.point]
    s: set[aoc.point]
    cost: int
    end: aoc.point

    def __lt__(self, other: "Solution") -> bool:
        head1 = self.path[-1]
        head2 = other.path[-1]
        dist1 = dist(head1, self.end)
        dist2 = dist(head2, self.end)
        return dist1 < dist2


def search(g: aoc.grid, start, end):
    heap = []
    sol0 = Solution(path=[start], s={start}, cost=0, end=end)
    heapq.heappush(heap, (0, sol0))
    best_cost = 9999999999

    cross = get_crossroads(g)

    heads = {}
    for p in g:
        if g[p] in (".", "S", "E"):
            if p in cross:
                for d in ["N", "S", "W", "E"]:
                    heads[(p, d)] = 9999999999
            else:
                heads[p] = 9999999999

    while heap:
        _, sol = heapq.heappop(heap)
        if sol.cost > best_cost:
            continue

        head = sol.path[-1]
        if len(sol.path) > 1:
            if head in cross:
                dhead = direction(sol.path[-2], head)
                if sol.cost <= heads[(head, dhead)]:
                    heads[(head, dhead)] = sol.cost
                else:
                    # better path to this head exists
                    continue
            else:
                if sol.cost <= heads[head]:
                    heads[head] = sol.cost
                else:
                    # better path to this head exists
                    continue

        for move in aoc.directions4():
            candidate = head + move

            if not g.inside(candidate):
                continue

            if g[candidate] == "#":
                continue

            # disallow going back
            if candidate in sol.s:
                continue

            path = sol.path.copy()
            path.append(candidate)

            c = cost(path)
            if c > best_cost:
                continue

            s = sol.s.copy()
            s.add(candidate)

            sol2 = Solution(
                path=path,
                s=s,
                cost=c,
                end=end,
            )
            if candidate == end:
                if c <= best_cost:
                    best_cost = c
                yield sol2
            else:
                pri = dist(candidate, end)
                heapq.heappush(heap, (pri, sol2))


def dist(a, b):
    dy = a.y - b.y
    dx = a.x - b.x
    return math.sqrt(dy * dy + dx * dx)


def cost(path):
    r = 0
    d = "E"
    rotates90 = 0
    for a, b in zip(path, path[1:]):
        r += 1
        if d in ("E", "W"):
            if b == a.up():
                d = "N"
                rotates90 += 1
            elif b == a.down():
                d = "S"
                rotates90 += 1
        if d in ("S", "N"):
            if b == a.left():
                d = "W"
                rotates90 += 1
            elif b == a.right():
                d = "E"
                rotates90 += 1

    return rotates90 * 1000 + len(path) - 1


def direction(a, b):
    if b == a.left():
        return "W"
    elif b == a.right():
        return "E"
    elif b == a.down():
        return "S"
    else:
        return "N"


def main():
    silver, gold = solve(aoc.stdin())
    print("silver:", silver)
    print("gold:", gold)


if __name__ == "__main__":
    main()
