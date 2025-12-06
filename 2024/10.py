from collections import defaultdict

import aoc


def silver(lines):
    g = aoc.grid(lines)

    starts = []
    ends = []
    for p in g:
        if g[p] == "0":
            starts.append(p)
        elif g[p] == "9":
            ends.append(p)

    res = defaultdict(int)
    for start in starts:
        for end in ends:
            if len(paths(g, start, end)) > 0:
                res[start] += 1

    return sum(res.values())


def gold(lines):
    g = aoc.grid(lines)

    starts = []
    ends = []
    for p in g:
        if g[p] == "0":
            starts.append(p)
        elif g[p] == "9":
            ends.append(p)

    res = defaultdict(int)
    for start in starts:
        for end in ends:
            res[start] += len(paths(g, start, end))

    return sum(res.values())


def paths(g, start, end):
    res = []
    stack = [[start]]
    while len(stack) > 0:
        path = stack.pop()
        head = path[-1]
        for move in aoc.directions4():
            _next = head + move
            if not g.inside(_next):
                continue
            if ord(g[_next]) - ord(g[head]) == 1:
                path2 = path.copy()
                path2.append(_next)
                if _next == end:
                    res.append(path2)
                else:
                    stack.append(path2)
    return res


def main():
    print("silver:", silver(aoc.stdin()))
    print("gold:", gold(aoc.stdin()))


if __name__ == "__main__":
    main()
