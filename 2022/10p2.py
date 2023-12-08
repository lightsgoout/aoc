import sys

cycles = {
    "noop": 1,
    "addx": 2,
}

registers = {
    "x": 1,
}


def _draw():
    for y in range(6):
        for x in range(40):
            if x in [registers["x"] - 1, registers["x"], registers["x"] + 1]:
                sys.stdout.write("#")
            else:
                sys.stdout.write(".")
            yield
        sys.stdout.write("\n")
    sys.stdout.write("\n")


crt = _draw()
for line in sys.stdin.readlines():
    args = line.strip().split()
    cmd, arg = None, None
    if len(args) == 1:
        cmd = args[0]
    else:
        cmd, arg = args
        arg = int(arg)

    for c in range(cycles[cmd]):
        next(crt)

    if cmd == "addx":
        registers["x"] += arg
