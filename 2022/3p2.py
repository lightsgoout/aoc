import sys
from functools import reduce


def priority(c):
    if c.isupper():
        return ord(c) - 38
    return ord(c) - 96


assert priority("a") == 1
assert priority("z") == 26
assert priority("A") == 27
assert priority("Z") == 52

_sum = 0
for group in zip(*(iter(sys.stdin.readlines()),) * 3):
    sets = []
    for line in group:
        line = line.strip()
        sets.append(set(line))

    unique = reduce(lambda a, b: a.intersection(b), sets)
    assert len(unique) == 1
    _sum += priority(list(unique)[0])

print(_sum)
