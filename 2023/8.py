import math
import sys
from collections import defaultdict
from itertools import cycle


def parse():
    lines = iter(sys.stdin.readlines())
    instr = next(lines).strip()
    next(lines)
    nodes = {}
    for line in lines:
        line = line.strip()
        src, dst = line.split(' = ')
        left, right = dst.replace('(', '').replace(')', '').split(', ')
        nodes[src] = {'L': left, 'R': right}
    return instr, nodes


def silver(instr, nodes):
    start = 'AAA'
    end = 'ZZZ'
    r = 0
    instr = iter(cycle(instr))
    current = start
    while True:
        i = next(instr)
        current = nodes[current][i]
        # print(f'{current=}')
        r += 1
        if current == end:
            break

    return r


def gold(instr, nodes):
    r = 0
    instr = iter(cycle(instr))
    current = [k for k in nodes.keys() if k.endswith('A')]
    steps_to_z = defaultdict(list)
    print(current)
    total = len(current)
    while True:
        r += 1
        i = next(instr)
        z = 0
        for j, c in enumerate(current):
            n = nodes[c][i]
            current[j] = n
            if n.endswith('Z'):
                z += 1
                try:
                    prev = steps_to_z[j][-1]
                except IndexError:
                    prev = 0
                steps_to_z[j].append(r - prev)
        if z == total:
            break

        if len(steps_to_z) == len(current):
            numbers = [v[0] for v in steps_to_z.values()]
            print(steps_to_z)
            r = math.lcm(*numbers)
            break

    return r


def main():
    instr, nodes = parse()

    print('silver:', silver(instr, nodes))
    print('gold:', gold(instr, nodes))


if __name__ == '__main__':
    main()
