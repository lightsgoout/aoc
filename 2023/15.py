import itertools
import sys
from copy import deepcopy
from pprint import pprint


def parse():
    steps = []
    for line in sys.stdin.readlines():
        line = line.strip()
        if not line:
            continue
        steps.extend(line.split(','))
    return steps


def hsh(s):
    r = 0
    for i, c in enumerate(s):
        r += ord(c)
        r *= 17
        r %= 256
    return r


def silver(steps):
    r = 0
    for s in steps:
        r += hsh(s)
    return r


class Box:
    def __init__(self):
        self.order = []
        self.focals = {}

    def rm(self, label):
        try:
            self.order.remove(label)
        except (IndexError, ValueError):
            pass

    def add(self, label, focal):
        try:
            self.order.index(label)
        except (IndexError, ValueError):
            self.order.append(label)
        self.focals[label] = focal


def gold(steps):
    boxes = [Box() for _ in range(256)]

    for s in steps:
        if '-' in s:
            label = s.replace('-', '')
            h = hsh(label)
            boxes[h].rm(label)
        elif '=' in s:
            label, focal = s.split('=')
            h = hsh(label)
            boxes[h].add(label, int(focal))

    r = 0
    for i, box in enumerate(boxes):
        for j, label in enumerate(box.order):
            lens_power = i + 1
            lens_power *= j + 1
            lens_power *= box.focals[label]
            r += lens_power
            # print(
            #     f'{label}: {i+1} (box {i}) * {j+1} (slot) * {box.focals[label]} (focal length) = {lens_power}'
            # )

    return r


def main():
    s = parse()
    print('silver: ', silver(s))
    print('gold: ', gold(s))


if __name__ == '__main__':
    main()
