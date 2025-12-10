import functools
import itertools
import operator

import aoc

from collections import defaultdict

import z3


def silver(lines):
    res = 0
    for line in lines:
        res += solve_silver(line)
    return res


def solve_silver(line):
    target, buttons, _, _, _ = parse_line(line)

    i = 1
    while True:
        for comb in itertools.combinations(buttons, i):
            v = 0
            for b in comb:
                v ^= b
            if v == target:
                return i

        i += 1


def parse_line(line):
    raw_lights, raw_buttons, joltage = "", [], None
    for part in line.split():
        t = part[0]
        if t == "[":
            raw_lights = part.replace("[", "").replace("]", "")
        elif t == "(":
            raw_buttons.append(
                tuple(map(int, part.replace("(", "").replace(")", "").split(",")))
            )
        elif t == "{":
            joltage = tuple(map(int, part.replace("{", "").replace("}", "").split(",")))

    lights = int("".join(reversed(raw_lights.replace(".", "0").replace("#", "1"))), 2)

    buttons = []
    for button in raw_buttons:
        v = 0
        for pos in button:
            v |= 1 << pos
        buttons.append(v)

    for i in range(len(raw_buttons)):
        raw_buttons[i] = tuple([v for v in raw_buttons[i]])

    return lights, buttons, joltage, raw_buttons, raw_lights


def gold(lines):
    res = 0
    for line in lines:
        this = solve_gold(line)
        res += this
    return res


def solve_gold(line):
    target, buttons, joltage, raw_buttons, raw_lights = parse_line(line)

    """
    [.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}

    B4 + B5 = 3
    B1 + B5 = 5
    B2 + B3 + B4 = 4
    B0 + B1 + B3 = 7
    """
    slv = z3.Optimize()

    button_vars = []
    for i, b in enumerate(buttons):
        button_vars.append(z3.Int("B" + str(i)))

    slv.minimize(functools.reduce(operator.add, button_vars))

    # which joltage position (key) affected by which button positions (list value)
    conns = defaultdict(list)

    for button_pos, button in enumerate(raw_buttons):
        for joltage_pos in button:
            conns[joltage_pos].append(button_pos)

    for v in button_vars:
        slv.add(v >= 0)

    for pos, button_positions in conns.items():
        agg = []
        for button_pos in button_positions:
            agg.append(button_vars[button_pos])

        target_jolt = joltage[pos]
        summ = functools.reduce(operator.add, agg)
        slv.add(summ == target_jolt)

    slv.check()
    m = slv.model()

    res = 0
    for v in button_vars:
        res += m[v].as_long()

    return res


def main():
    print("silver:", silver(aoc.stdin()))
    print("gold:", gold(aoc.stdin()))


if __name__ == "__main__":
    main()
