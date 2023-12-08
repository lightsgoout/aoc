import sys

_result = []
for group in sys.stdin.read().split("\n\n"):
    _sum = sum(int(x.strip()) for x in group.split("\n") if x.strip())
    _result.append(_sum)

# print(max(_result))
print(sum(list(sorted(_result, reverse=True))[:3]))
