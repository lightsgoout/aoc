import re
import sys
from collections import namedtuple
from pprint import pprint

cost = namedtuple('cost', 'ore clay obsidian')


def main():
    bps = []
    for line in sys.stdin.readlines():
        bp = {}
        for cost_line in line.split('.'):
            cost_line = cost_line.strip()
            if not cost_line:
                continue
            robot_type = re.search(r"(ore|clay|obsidian|geode) robot", cost_line)
            robot_type = robot_type.group(1)
            resources = {}
            for resource in re.finditer(r"(\d+) (ore|clay|obsidian|geode)", cost_line):
                resources[resource.group(2)] = int(resource.group(1))
            bp[robot_type] = resources
        bps.append(bp)

    print('silver:', solve_silver(bps))


def solve_silver(bps):



if __name__ == '__main__':
    main()
