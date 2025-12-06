import sys
import re


def silver(lines):
    r = 0
    pat = re.compile("mul\(\d+,\d+\)")
    for line in lines:
        for match in re.findall(pat, line):
            raw = match.replace("(", "").replace(")", "").replace("mul", "")
            a, b = raw.split(",")
            a, b = int(a), int(b)
            r += a * b
    return r


def gold(lines):
    r = 0
    mul = re.compile("mul\(\d+,\d+\)")
    dont = re.compile("don't\(\)")
    do = re.compile("do\(\)")
    enabled = True
    for line in lines:
        muls = list(re.finditer(mul, line))
        donts = list(re.finditer(dont, line))
        dos = list(re.finditer(do, line))
        merged = [*muls, *donts, *dos]
        merged = sorted(merged, key=lambda m: m.span())

        for m in merged:
            match = m.group()
            if match == "don't()":
                enabled = False
            elif match == "do()":
                enabled = True
            elif enabled:
                raw = match.replace("(", "").replace(")", "").replace("mul", "")
                a, b = raw.split(",")
                a, b = int(a), int(b)
                r += a * b

    return r


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
