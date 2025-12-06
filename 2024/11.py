from collections import defaultdict

import aoc


def silver(lines):
    stones = list(map(int, lines[0].split()))
    return blink(stones, 25)


def gold(lines):
    stones = list(map(int, lines[0].split()))
    return blink(stones, 75)


def blink(stones, n):
    res = defaultdict(int)
    for s in stones:
        res[s] += 1

    for _ in range(n):
        for s, count in list(res.items()):
            res[s] -= count
            if s == 0:
                res[1] += count
                continue

            if len(str(s)) % 2 == 0:
                ss = str(s)
                left = int(ss[: len(ss) // 2])
                right = int(ss[len(ss) // 2 :])
                res[left] += count
                res[right] += count
                continue

            res[s * 2024] += count
    return sum(res.values())


def main():
    print("silver:", silver(aoc.stdin()))
    print("gold:", gold(aoc.stdin()))


if __name__ == "__main__":
    main()
