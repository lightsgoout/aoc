import sys
from pprint import pprint


def extrapolate(numbers):
    pyramid = [numbers]
    while True:
        latest = pyramid[-1]
        new = []
        for a, b in zip(latest, latest[1:]):
            new.append(b - a)
        pyramid.append(new)
        if all([x == 0 for x in new]):
            break

    r = 0
    for row in pyramid:
        r += row[-1]
    return r


def extrapolate_backwards(numbers):
    pyramid = [numbers]
    while True:
        latest = pyramid[-1]
        new = []
        for a, b in zip(latest, latest[1:]):
            new.append(b - a)
        pyramid.append(new)
        if all([x == 0 for x in new]):
            break

    rev = list(reversed(pyramid))

    r = 0
    for i, row in enumerate(rev):
        if i == 0:
            row.insert(0, row[0])
        else:
            row.insert(0, row[0] - rev[i - 1][0])
            if i == len(rev) - 1:
                r += row[0]

    # for i, row in enumerate(reversed(rev)):
    #     print('  ' * i + '  '.join(map(str, row)))

    return r


def silver(data):
    r = 0
    for row in data:
        r += extrapolate(row)

    return r


def gold(data):
    r = 0
    for row in data:
        r += extrapolate_backwards(row)

    return r


def parse():
    result = []
    for line in sys.stdin.readlines():
        line = line.strip()
        if not line:
            continue
        result.append([int(x.strip()) for x in line.split() if x.strip() != ''])
    return result


def main():
    data = parse()

    print('silver:', silver(data))
    print('gold:', gold(data))


if __name__ == '__main__':
    main()
