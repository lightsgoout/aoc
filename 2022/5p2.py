import sys

text = sys.stdin.read()
load, instructions = text.split("\n\n")
load = iter(reversed(load.split("\n")))
n_stacks = int(next(load).strip()[-1])
cargo = [[] for _ in range(n_stacks)]
step = 0
load = list(load)
for line in load:
    line = line.strip()
    step = max(step, len(line) // n_stacks + 1)

for line in load:
    for stack, slot in enumerate([line[i : i + step] for i in range(0, len(line), step)]):
        crate = slot.strip().strip("[").strip("]")
        if crate:
            cargo[stack].append(crate)

for line in instructions.split("\n"):
    line = line.strip()
    if not line:
        continue

    n, src, dst = map(int, [s for s in line.split() if s.isdigit()])
    crates = []
    for _ in range(n):
        crates.append(cargo[src - 1].pop())
    cargo[dst - 1].extend(reversed(crates))

print("".join(stack.pop() for stack in cargo))
