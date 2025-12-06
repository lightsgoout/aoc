import sys


def solve(lines, n):
    r = 0
    for line in lines:
        r += solve_line(line, n)
    return r


def solve_line(line, n):
    result = ""
    start = 0
    remaining = n
    while remaining > 0:
        m = 0
        pos = 999999
        for i, c in enumerate(line[start : len(line) - remaining + 1]):
            if int(c) > m:
                m = int(c)
                pos = i + start
        start = pos + 1
        result += str(m)
        remaining -= 1
    return int(result)


def silver(lines):
    return solve(lines, 2)


def gold(lines):
    return solve(lines, 12)


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
