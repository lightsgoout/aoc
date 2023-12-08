import contextlib
import sys
from collections import defaultdict


def silver(lines) -> int:
    r = 0
    for line in lines:
        digits = []
        for c in line:
            if c.isdigit():
                digits.append(c)
        r += int(digits[0] + digits[-1])
    return r


def gold(lines) -> int:
    r = 0

    tokens = {
        t: str(i)
        for i, t in enumerate(
            ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine'], start=1
        )
    }
    for i in range(1, 10):
        tokens[str(i)] = str(i)

    for line in lines:
        pos = defaultdict(set)
        for token in tokens.keys():
            with contextlib.suppress(ValueError):
                for i in range(len(line)):
                    pos[token].add(line.index(token, i))

        imin, imax = sys.maxsize, 0
        first, last = None, None
        for token, ii in pos.items():
            for i in ii:
                if i > imax:
                    imax = i
                    last = token
                if i < imin:
                    imin = i
                    first = token

        if last is None:
            last = first

        r += int(tokens[first] + tokens[last])

    return r


def main():
    lines = []
    for line in sys.stdin.readlines():
        line = line.strip()
        if not line:
            continue
        lines.append(line)

    # print('silver:', silver(lines))
    print('gold:', gold(lines))


if __name__ == '__main__':
    main()
