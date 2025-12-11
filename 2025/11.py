import functools

import aoc
import networkx as nx


def silver(lines):
    g = nx.DiGraph()
    for line in lines:
        src, dsts = line.split(":")
        for dst in dsts.split():
            dst = dst.strip()
            g.add_edge(src, dst)

    return len(list(nx.all_simple_paths(g, "you", "out")))


def gold(lines):
    g = nx.DiGraph()
    for line in lines:
        src, dsts = line.split(":")
        for dst in dsts.split():
            dst = dst.strip()
            g.add_edge(src, dst)

    return solve(g, "svr", "out")


@functools.cache
def solve(g, src, dst, has_dac=False, has_fft=False):
    res = 0
    for nb in g.successors(src):
        if nb == dst and has_dac and has_fft:
            res += 1
        else:
            res += solve(g, nb, dst, has_dac or nb == "dac", has_fft or nb == "fft")
    return res


def main():
    print("silver:", silver(aoc.stdin()))
    print("gold:", gold(aoc.stdin()))


if __name__ == "__main__":
    main()
