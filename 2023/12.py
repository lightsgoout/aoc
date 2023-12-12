import itertools
import sys
from pprint import pprint


def parse():
    data = []
    for y, line in enumerate(sys.stdin.readlines()):
        line = line.strip()
        if not line:
            continue

        springs, groups = line.split()
        groups = list(map(int, groups.split(',')))
        data.append((springs, groups))
    return data


def bits(n, s=96):
    return format(n, 'b').zfill(s).replace('1', "\033[32m" + '1' + "\033[0m")


def test(n, conf):
    bit = 1
    ones = 0
    g = 0
    x = 0
    while x < n:
        x = 1 << (bit - 1)
        if n & x:
            ones += 1
        else:
            if ones > 0:
                if g >= len(conf):
                    return False
                # print(f'testing {ones=} against {conf[g]=}')
                if ones != conf[g]:
                    return False
                g += 1
                ones = 0
        bit += 1

    if g != len(conf):
        return False
    # print(f'iteration: {bits(n)} matches {conf}')
    return True


def bitsolve(s, conf):
    # print(s)
    # print(conf)
    broken = 0
    operational = 0
    unknown = 0

    for i, c in enumerate(s):
        if c == '#':
            broken |= 1 << i
        elif c == '.':
            operational |= 1 << i
        else:
            unknown |= 1 << i

    # print(f'B:{bits(broken)}')
    # print(f'O:{bits(operational)}')
    # print(f'?:{bits(unknown)}')

    hi = (1 << unknown.bit_length()) - 1
    mask = hi ^ (hi & unknown)
    # print(f'M:{bits(mask)}')

    res = 0
    x = 0
    while True:
        if x > unknown:
            break
        # print(f'X:{bits(x)}')
        iteration = (unknown & x) | broken
        # print(f'iteration: {bits(iteration)}')
        if test(iteration, conf):
            res += 1

        x = (x | mask) + 1 & ~mask
        if x == 0:
            break

    return res


def silver(data):
    # data2 = []
    # for s, conf in data:
    #     s = '?'.join([s]*5)
    #     conf = list(itertools.chain.from_iterable([conf]*5))
    #     data2.append((s, conf))
    #

    r = 0
    for s, conf in data:
        res = bitsolve(s, conf)
        r += res
    return r


def gold(data):
    data2 = []
    for s, conf in data:
        s = '?'.join([s] * 5)
        conf = list(itertools.chain.from_iterable([conf] * 5))
        data2.append((s, conf))

    r = 0
    for s, conf in data2:
        print('solving ', s)
        res = bitsolve(s, conf)
        r += res
    return r


def main():
    data = parse()
    # pprint(data)
    # print('silver: ', silver(data))
    print('gold: ', gold(data))
    # print('gold: ', solve(g, factor=1000000))


if __name__ == '__main__':
    main()
