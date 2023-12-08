import sys


def priority(c):
    if c.isupper():
        return ord(c) - 38
    return ord(c) - 96


assert priority("a") == 1
assert priority("z") == 26
assert priority("A") == 27
assert priority("Z") == 52

_sum = 0
for line in sys.stdin.readlines():
    line = line.strip()
    a, b = line[: int(len(line) / 2)], line[int(len(line) / 2) :]
    assert len(a) == len(b)

    common = list(set(a).intersection(set(b)))[0]
    _sum += priority(common)

    # print(f'{line}')
    # print(f'{a=} {b=}')
    # print(f'{common=} {priority(common)=}')

print(_sum)
