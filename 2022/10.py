import sys

cycles = {
    "noop": 1,
    "addx": 2,
}

registers = {
    "x": 1,
}

_cc = 0

points_of_interest = [20, 60, 100, 140, 180, 220]
readings = []

for line in sys.stdin.readlines():
    args = line.strip().split()
    cmd, arg = None, None
    if len(args) == 1:
        cmd = args[0]
    else:
        cmd, arg = args
        arg = int(arg)

    for c in range(cycles[cmd]):
        _cc += 1
        if _cc in points_of_interest:
            readings.append(_cc * registers["x"])

    if cmd == "addx":
        registers["x"] += arg

print(sum(readings))
