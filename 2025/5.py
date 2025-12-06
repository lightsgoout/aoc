import sys


def silver(lines):
    ranges = []

    fresh = 0
    for line in lines:
        if "-" in line:
            start, end = map(int, line.split("-"))
            ranges.append((start, end))
        else:
            ingr = int(line)
            for start, end in ranges:
                if start <= ingr <= end:
                    fresh += 1
                    break

    return fresh


def gold(lines):
    ranges = []

    for line in lines:
        if "-" in line:
            start, end = map(int, line.split("-"))
            ranges.append([start, end])

    intervals = merge_intervals(ranges)

    fresh = 0
    for start, end in intervals:
        fresh += end - start + 1

    return fresh


def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    if len(intervals) < 2:
        return intervals

    while True:
        before = len(intervals)
        intervals = merge_pass(intervals.copy())
        after = len(intervals)
        if before == after:
            return intervals


def merge_pass(intervals: list[list[int]]) -> list[list[int]]:
    res = []
    while intervals:
        ival1 = intervals.pop()
        if len(res) == 0:
            res.append(ival1)
            continue

        found = False
        for i, ival2 in enumerate(res):
            if mergeable(ival1, ival2):
                res[i] = merge(ival1, ival2)
                found = True
                break

        if not found:
            res.append(ival1)

    return res


def mergeable(a, b):
    if b[0] <= a[0]:
        a, b = b, a

    lo1, hi1 = a[0], a[1]
    lo2, hi2 = b[0], b[1]
    return (lo1 <= hi2 <= hi1) or (lo1 <= lo2 <= hi1)


def merge(a, b):
    return [
        min(a[0], b[0]),
        max(a[1], b[1]),
    ]


def main():
    lines = []
    for line in sys.stdin.readlines():
        line = line.strip()
        if not line:
            continue
        lines.append(line)

    print("silver:", silver(lines))
    print("gold:", gold(lines))


if __name__ == "__main__":
    main()
