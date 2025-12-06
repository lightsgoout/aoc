import functools
import operator
import sys
from collections import defaultdict


def silver(raw):
    lines = []
    for line in raw:
        if line := line.strip():
            lines.append(line)

    cols = []
    for line in lines:
        cols.append(line.split())
    cols = list(zip(*cols))

    r = 0
    for col in cols:
        col = list(reversed(col))
        sign = col[0]
        col = col[1:]
        col = list(map(int, col))

        ops = {
            "+": operator.add,
            "*": operator.mul,
        }

        r += functools.reduce(ops[sign], col)

    return r


def gold(raw):
    cols = defaultdict(list)

    d = "".join(raw)
    j = 0
    for c in d:
        if c == "\n":
            j = 0
            continue
        cols[j].append(c)
        j += 1

    n_cols = max(cols.keys())

    buffer = []
    res = 0
    for i in range(n_cols + 1):
        col = cols[i]

        if not any([c.strip() for c in col]):
            res += run_buffer(buffer)
            buffer = []

        buffer.append(col)

    if buffer:
        res += run_buffer(buffer)

    return res


def run_buffer(buffer):
    sign = None
    digits = []
    for segment in buffer:
        digit = ""
        for char in segment:
            if char.isdigit():
                digit += char
                continue
            if char in ("+", "*"):
                sign = char
        if digit:
            digits.append(digit)

    ops = {
        "+": operator.add,
        "*": operator.mul,
    }

    return functools.reduce(ops[sign], map(int, digits))


def main():
    raw = list(sys.stdin.readlines())
    print("silver:", silver(raw))
    print("gold:", gold(raw))


if __name__ == "__main__":
    main()
