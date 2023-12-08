import functools
import itertools
import operator
import sys
from typing import Iterator

monkeys = []

magic = 0
primes = [7, 13, 2, 5, 17, 11, 3, 19]
for i in range(1, 100000000):
    if all((i % p == 0 for p in primes)):
        magic = i
        break

print(f"{magic=}")


class Monkey:
    def __init__(self):
        self.items = []
        self.operation = None
        self.test = None
        self.inspected = 0

    def run(self, monkey_idx):
        for idx, item in enumerate(self.items):
            worry_lvl = self.operation(item) % magic
            divisible_op = self.test["test"]
            test_result = worry_lvl % divisible_op == 0
            self.test["on"][test_result](item_idx=idx, worry_lvl=worry_lvl)
            self.inspected += 1
        self.items = [item for item in self.items if item is not None]


def parse_op(line: str):
    args = line.split()
    op, arg = args[-2], args[-1]
    return {
        "+": lambda a: a + (int(arg) if arg != "old" else a),
        "*": lambda a: a * (int(arg) if arg != "old" else a),
    }[op]


def parse_test(src_monkey: Monkey, gen: Iterator[str]):
    test, _, arg = next(gen).split()[-3:]
    on = {}

    while True:
        try:
            line = next(gen).strip()
        except StopIteration:
            break
        if not line:
            break

        if line.startswith("If "):
            cond, action = line.split(":")
            cond = cond.split()[-1]
            cond = {"true": True, "false": False}[cond]
            action = action.strip()
            if action.startswith("throw to monkey"):
                dst_monkey = int(action.split()[-1])
                action = functools.partial(throw_to_monkey, src=src_monkey, dst=dst_monkey)
            else:
                raise AssertionError("unknown action")
            on[cond] = action

    return {
        "test": {"divisible": int(arg)}[test],
        "on": on,
    }


def parse_items(line: str):
    return list(map(int, line.split(":")[-1].split(",")))


def throw_to_monkey(item_idx, src: Monkey, dst: int, worry_lvl: int):
    monkeys[dst].items.append(worry_lvl)
    src.items[item_idx] = None


def main():
    _input = iter(sys.stdin.readlines())
    while True:
        try:
            line = next(_input).strip()
        except StopIteration:
            break
        if not line:
            break

        if line.startswith("Monkey "):
            monkey = Monkey()
            monkey.items = parse_items(next(_input))
            monkey.operation = parse_op(next(_input))
            monkey.test = parse_test(monkey, _input)
            monkeys.append(monkey)

    for _ in range(10000):
        for i, m in enumerate(monkeys):
            m.run(i)


if __name__ == "__main__":
    main()
    print(functools.reduce(operator.mul, list(sorted([m.inspected for m in monkeys], reverse=True))[:2]))

    for i, m in enumerate(monkeys):
        print(f"monkey {i} {m.inspected=}")
