import itertools
import operator

import aoc


def silver(lines):
    r = 0
    for line in lines:
        total, args = line.split(":")
        total = int(total)
        args = list(map(int, args.split()))
        if valid(total, args):
            r += total

    return r


# def concat(a, b):
#     return int(str(a) + str(b))


def valid(total, args):
    for variant in itertools.product(["+", "*"], repeat=len(args) - 1):
        stack = []
        opstack = list(variant)
        for a in args:
            stack.append(a)

        stack = list(reversed(stack))
        opstack = list(reversed(opstack))

        while len(stack) >= 2:
            a = stack.pop()
            b = stack.pop()

            op = opstack.pop()

            _res = ops[op](a, b)
            stack.append(_res)

        assert len(stack) == 1
        res = stack[0]

        assert len(opstack) == 0

        if res == total:
            return True

    return False


ops = {
    "+": operator.add,
    "*": operator.mul,
    "|": lambda a, b: int(str(a) + str(b)),
}


def valid2(total, args):
    for variant in itertools.product(["+", "*", "|"], repeat=len(args) - 1):
        stack = []
        opstack = list(variant)
        for a in args:
            stack.append(a)

        stack = list(reversed(stack))
        opstack = list(reversed(opstack))

        while len(stack) >= 2:
            a = stack.pop()
            b = stack.pop()
            op = opstack.pop()
            _res = ops[op](a, b)
            stack.append(_res)

        assert len(stack) == 1
        res = stack[0]

        assert len(opstack) == 0
        if res == total:
            return True

    return False


def gold(lines):
    r = 0
    for i, line in enumerate(lines):
        print(f"{i}/{len(lines)}")
        total, args = line.split(":")
        total = int(total)
        args = list(map(int, args.split()))
        if valid2(total, args):
            r += total

    return r


def main():
    print("silver:", silver(aoc.stdin()))
    print("gold:", gold(aoc.stdin()))


if __name__ == "__main__":
    main()
