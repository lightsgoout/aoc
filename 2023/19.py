import dataclasses
import itertools
import math
import operator
import sys
import typing
from pprint import pprint

import networkx as nx


def solve(lines):
    parts, accepted, rejected, rules = parse(lines)
    silver, gold = 0, 0
    for p in accepted:
        silver += p.total()

    return silver, solve_gold(rules)


def solve_gold(rules) -> int:
    pprint(rules)
    # t = {"in": tree(rules, rules["in"].rules)}
    # pprint(t)
    g = nx.Graph()

    for name, _rules in rules.items():
        for _rule in _rules.rules:
            if _rule.goto:
                if _rule.goto != "R":
                    g.add_edge(name, _rule.goto)

    r = 0

    # muls = []

    for path in nx.all_simple_paths(g, "in", "A"):
        cs = path_constraints(rules, path)
        print(cs)
        x, m, a, s = cs["x"], cs["m"], cs["a"], cs["s"]

        r += math.prod([size(x), size(m), size(a), size(s)])

        # if not muls:
        #     muls.append([to_set(x), to_set(m), to_set(a), to_set(s)])
        #     continue

        # sx, sm, sa, ss = to_set(x), to_set(m), to_set(a), to_set(s)

        # if not seen:
        #     seen.append([x, m, a, s])
        #     r += size(x) * size(m) * size(a) * size(s)
        # continue

        # this = 0
        # if len(merged["x"]):
        #     for i, prev in enumerate(merged["x"]):
        #         if overlap := intersects(prev, x):
        #             print(f"{prev=} {overlap=} {x=}")
        #             this = size(overlap) - size(x)
        #             merged["x"][i] = overlap
        #         else:
        #             this = size(x)
        #             merged["x"].append(x)
        # else:
        #     merged["x"].append(x)

        # for i, prev in enumerate(merged["m"]):
        #     if overlap := intersects(prev, m):
        #         this *= size(overlap) - size(m)
        #         merged["m"][i] = overlap
        #     else:
        #         this *= size(m)
        #         merged["m"] = m

        # r += this

    # pprint(merged)
    return r


# def unique()


# def intersects(a, b):
#     _as, _ae = a
#     _bs, _be = b
#     return _bs > _ae or _as > _be


def size(a):
    return a[1] - a[0] + 1


def to_set(a):
    return set(range(a[0], a[1] + 1))


def path_constraints(rules, path):
    constraint = [1, 4000]
    constraints = {}
    for attr in ["x", "m", "a", "s"]:
        constraints[attr] = constraint.copy()

    print(f"{path=}")
    for a, b in zip(path, path[1:]):
        for rule in rules[a].rules:
            if rule.goto != b:
                continue

            if rule.op == operator.gt:
                current = constraints[rule.attr][0]
                constraints[rule.attr][0] = max(current, rule.arg + 1)
            elif rule.op == operator.lt:
                current = constraints[rule.attr][1]
                constraints[rule.attr][1] = min(current, rule.arg - 1)

    return constraints


def tree(global_rules, rules):
    res = {}
    for _rule in rules:
        if _rule.goto is None:
            return res

        res[_rule.goto] = tree(global_rules, global_rules[_rule.goto].rules)
    return res


def parse(lines):
    parts = []
    accepted = []
    rejected = []
    rules = {
        "A": Rules(
            rules=[
                Rule(
                    op=operator.gt,
                    attr="x",
                    arg=-10000000,
                    on_cond=lambda p: accepted.append(p),
                    goto=None,
                ),
            ]
        ),
        "R": Rules(
            rules=[
                Rule(
                    op=operator.gt,
                    attr="x",
                    arg=-10000000,
                    on_cond=lambda p: rejected.append(p),
                    goto=None,
                ),
            ]
        ),
    }
    for line in lines:
        if "=" in line:
            attrs = {}
            for raw_part in line.replace("{", "").replace("}", "").split(","):
                attr, value = raw_part.split("=")
                attrs[attr] = int(value)
            parts.append(Part(**attrs))
        else:
            name, alg = line.split("{")
            alg = alg.replace("}", "")

            _rules = []
            for raw_rule in alg.split(","):
                if ":" not in raw_rule:
                    _rules.append(
                        Rule(
                            op=operator.gt,
                            attr="x",
                            arg=-10000000,
                            on_cond=None,
                            goto=raw_rule,
                        )
                    )
                    continue

                attr = raw_rule[0]
                op = raw_rule[1]
                if op == ">":
                    op = operator.gt
                elif op == "<":
                    op = operator.lt
                else:
                    raise AssertionError("unknown op: " + op)

                arg, goto = raw_rule[2:].split(":")
                arg = int(arg)

                rule = Rule(
                    attr=attr,
                    op=op,
                    arg=arg,
                    on_cond=None,
                    goto=goto,
                )
                _rules.append(rule)

            rules[name] = Rules(rules=_rules)

    while parts:
        p = parts.pop()
        _next = rules["in"](p)
        while _next:
            _next = rules[_next](p)

    return parts, accepted, rejected, rules


@dataclasses.dataclass
class Part:
    x: int
    m: int
    a: int
    s: int

    def total(self):
        return self.x + self.m + self.a + self.s


@dataclasses.dataclass
class Rule:
    attr: str
    op: callable
    arg: int
    on_cond: typing.Optional[callable]
    goto: typing.Optional[str]

    def __call__(self, p: Part) -> typing.Optional[str]:
        if self.op(getattr(p, self.attr), self.arg):
            if self.on_cond is not None:
                self.on_cond(p)
            return self.goto

    def __hash__(self):
        return hash((self.attr, self.op, self.arg, self.goto))

    @property
    def is_magic(self):
        return self.op == operator.gt and self.arg == -10000000


@dataclasses.dataclass
class Rules:
    rules: list[Rule]

    def __call__(self, p: Part) -> typing.Optional[str]:
        for rule in self.rules:
            if _next := rule(p):
                return _next


def main():
    lines = []
    for line in sys.stdin.readlines():
        line = line.strip()
        if not line:
            continue
        lines.append(line)

    silver, gold = solve(lines)
    print("silver: ", silver)
    print("gold: ", gold)


if __name__ == "__main__":
    main()
