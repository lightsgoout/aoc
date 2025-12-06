import sys
from collections import defaultdict


def silver(lines):
    res = 0
    for line in lines:
        numbers = [int(x) for x in line.split()]
        if valid_line(numbers):
            res += 1
    return res


def gold(lines):
    res = 0
    for line in lines:
        numbers = [int(x) for x in line.split()]
        valid = valid_line(numbers)
        if valid:
            res += 1
        else:
            for i in range(len(numbers)):
                var = numbers.copy()
                var.pop(i)
                if valid_line(var):
                    res += 1
                    break

    return res


def valid_line(numbers):
    asc = 0
    desc = 0
    valid = True
    for a, b in zip(numbers, numbers[1:]):
        if b < a:
            desc += 1
        else:
            asc += 1
        if not 1 <= abs(b - a) <= 3:
            valid = False
            break
    return (asc == 0 or desc == 0) and valid


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
