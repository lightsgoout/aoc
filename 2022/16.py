import functools
import itertools
import sys
from collections import defaultdict


def main():
    g = defaultdict(list)
    flow_rates = {}

    for line in sys.stdin.readlines():
        line = line.strip()
        src = line.split(';')[0].split()[1]
        rate = int(line.split(';')[0].split()[-1].split('=')[1])
        if ' valves ' in line:
            dst = [s.strip() for s in line.split(';')[1].split('valves')[1].split(',')]
        else:
            assert ' valve ' in line
            dst = [line.split(';')[1].split()[-1]]

        flow_rates[src] = rate
        g[src].extend(dst)

    # print('silver:', solve_silver(g, flow_rates, budget=30))
    print('gold:', solve_gold(g, flow_rates, budget=26))


def solve_silver(g, flow_rates, budget: int) -> int:
    valves = []
    for target, pressure in sorted(flow_rates.items(), key=lambda k: k[1], reverse=True):
        if pressure > 0:
            valves.append(target)

    valves = list(sorted(valves))

    costs = {}
    for a, b in itertools.combinations(['AA', *valves], 2):
        costs[frozenset([a, b])] = len(shortest_path(g, a, b))

    max_pressure = 0
    for path in permutations_pruned(set(valves), costs, budget):
        path_pressure = calc_path_pressure(g, path, flow_rates, budget)
        if path_pressure > max_pressure:
            max_pressure = path_pressure

    return max_pressure


def solve_gold(g, flow_rates, budget: int) -> int:
    valves = []
    for target, pressure in sorted(flow_rates.items(), key=lambda k: k[1], reverse=True):
        if pressure > 0:
            valves.append(target)

    valves = list(sorted(valves))

    costs = {}
    for a, b in itertools.combinations(['AA', *valves], 2):
        costs[frozenset([a, b])] = len(shortest_path(g, a, b))

    valves = set(valves)

    elephant_cache = dict()

    max_pressure = 0
    for path in permutations_pruned(valves, costs, budget):
        path_pressure = calc_path_pressure(g, path, flow_rates, budget)

        elephant_valves = frozenset(valves.difference(set(path).difference({'AA'})))
        elephant_pressure = elephant_cache.get(elephant_valves)
        print(f'my {path=} {path_pressure=} elephant_cache_hit={elephant_pressure is not None}')
        if elephant_pressure is None:
            max_elephant_pressure = 0
            for elephant_path in permutations_pruned(elephant_valves, costs, budget):
                elephant_path_pressure = calc_path_pressure(g, elephant_path, flow_rates, budget)
                max_elephant_pressure = max(max_elephant_pressure, elephant_path_pressure)
            elephant_cache[elephant_valves] = max_elephant_pressure
            elephant_pressure = max_elephant_pressure

        total_pressure = path_pressure + elephant_pressure
        if total_pressure > max_pressure:
            max_pressure = total_pressure

    return max_pressure


def calc_path_pressure(g, path, flow_rates, budget) -> int:
    path_pressure = 0
    per_tick = 0
    ticks = 0

    for src, dst in zip(path, path[1:]):
        path_len = len(shortest_path(g, src, dst))
        ticks += path_len
        path_pressure += per_tick * path_len

        # open valve
        ticks += 1
        path_pressure += per_tick
        per_tick += flow_rates[dst]

    assert ticks <= budget

    if budget > ticks:
        path_pressure += per_tick * (budget - ticks)

    return path_pressure


def shortest_path(graph, start, goal):
    explored = []

    # Queue for traversing the
    # graph in the BFS
    queue = [[start]]

    # Loop to traverse the graph
    # with the help of the queue
    while queue:
        path = queue.pop(0)
        node = path[-1]

        # Condition to check if the
        # current node is not visited
        if node not in explored:
            neighbours = graph[node]

            # Loop to iterate over the
            # neighbours of the node
            for neighbour in neighbours:
                new_path = list(path)
                new_path.append(neighbour)
                queue.append(new_path)

                # Condition to check if the
                # neighbour node is the goal
                if neighbour == goal:
                    return new_path[1:]
            explored.append(node)

    raise Exception('unreachable')


def permutations_pruned(valves, costs, budget):
    good = {('AA',)}
    for n in range(len(valves)):
        new_good = set()
        for base in good:
            for path in itertools.permutations(valves.difference(set(base)), 1):
                path = (*base, *path)
                cost = pcost(path, costs) + len(path) - 1
                if cost < budget:
                    yield path
                    new_good.add(path)
        good = new_good


def pcost(path, costs) -> int:
    cost = 0
    for a, b in zip(path, path[1:]):
        cost += costs[frozenset([a, b])]
    return cost


if __name__ == '__main__':
    main()
