import sys
from functools import reduce


def dist(gas, time):
    s = gas
    d = (time - gas) * s
    return d


def silver(pairs):
    wins = []
    for time, distance in pairs:
        w = 0
        for gas in range(0, time):
            d = dist(gas, time)
            if d > distance:
                w += 1
        wins.append(w)
    return reduce(lambda a, b: a * b, wins)


def gold(pairs):
    pair = [0, 0]
    pair[0] = int(''.join(str(x) for x, y in pairs))
    pair[1] = int(''.join(str(y) for x, y in pairs))
    return silver([pair])


def main():
    times, distances = [], []
    for line in sys.stdin.readlines():
        line = line.strip()
        if not line:
            continue

        if 'Time' in line:
            times = [int(x.strip()) for x in line.split(':')[1].split() if x.strip() != '']
        if 'Distance' in line:
            distances = [int(x.strip()) for x in line.split(':')[1].split() if x.strip() != '']

    pairs = list(zip(times, distances))

    print('silver:', silver(pairs))
    print('gold:', gold(pairs))


if __name__ == '__main__':
    main()
