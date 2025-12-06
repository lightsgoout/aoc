import sys


def silver(lines):
    r = 0
    for line in lines:
        ranges = line.split(",")
        for rng in ranges:
            a, b = map(int, rng.split("-"))
            for v in range(a, b + 1):
                s = str(v)
                if len(s) % 2 != 0:
                    continue
                left, right = s[: len(s) // 2], s[len(s) // 2 :]
                if left == right:
                    r += v

    return r


def gold(lines):
    r = 0
    for line in lines:
        ranges = line.split(",")
        for rng in ranges:
            a, b = map(int, rng.split("-"))
            for v in range(a, b + 1):
                if repeating(str(v)):
                    r += int(v)

    return r


def repeating(s: str) -> bool:
    n = len(s) - 1
    while True:
        if n <= 0:
            break

        parts = chunks(s, n)
        if len(set(parts)) == 1:
            return True

        n -= 1
    return False


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


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
