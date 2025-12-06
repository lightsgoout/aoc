import sys
from collections import defaultdict


def silver(lines):
    left = []
    right = []
    for line in lines:
        a, b = line.split()
        a = int(a)
        b = int(b)
        left.append(a)
        right.append(b)

    res = 0
    left = sorted(left)
    right = sorted(right)
    for a, b in zip(left, right):
        res += abs(b-a)

    return res


def gold(lines):
    left = []
    right = defaultdict(int)
    for line in lines:
        a, b = line.split()
        a = int(a)
        b = int(b)
        left.append(a)
        right[b] += 1


    res = 0
    for a in left:
        res += a * right.get(a, 0)

    return res


def main():
    lines = []
    for line in sys.stdin.readlines():
        line = line.strip()
        if not line:
            continue
        lines.append(line)

    print('silver:', silver(lines))
    print('gold:', gold(lines))


if __name__ == '__main__':
    main()
