import sys

count = 0
for line in sys.stdin.readlines():
    a, b = line.strip().split(",")
    a1, a2 = map(int, a.split("-"))
    b1, b2 = map(int, b.split("-"))

    s1 = set(range(a1, a2 + 1))
    s2 = set(range(b1, b2 + 1))
    if s1.intersection(s2):
        count += 1
print(f"{count=}")
