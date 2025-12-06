import math
import sys
from collections import defaultdict


# 108756900251803 too high
# 107416870457097 too high


def silver(lines):
    reg, prog = parse(lines)
    return ",".join(map(str, eval_prog(reg, prog)))


def eval_prog(reg, prog):
    out = []
    ptr = 0
    while ptr < len(prog):
        inst = prog[ptr]
        literal = prog[ptr + 1]
        ptr += 2

        if inst == 0:
            reg["A"] //= 1 << combo(reg, literal)
        elif inst == 1:
            reg["B"] ^= literal
        elif inst == 2:
            reg["B"] = combo(reg, literal) % 8
        elif inst == 3:
            if reg["A"] == 0:
                continue
            ptr = literal
        elif inst == 4:
            reg["B"] ^= reg["C"]
        elif inst == 5:
            out.append(combo(reg, literal) % 8)
        elif inst == 6:
            reg["B"] = reg["A"] // (1 << combo(reg, literal))
        elif inst == 7:
            reg["C"] = reg["A"] // (1 << combo(reg, literal))

        print(f'A = {oct(reg["A"])}')

    return out


# def gold(lines):
#     _reg, _prog = parse(lines)
#
#     start = 0
#     while True:
#         start += 1
#         this = _reg.copy()
#         this["A"] = start
#
#         recheck = eval_prog(this, _prog)
#
#         best = common_start(_prog, recheck)
#         if best > 2 and len(recheck) == len(_prog):
#             print(f"{start=} {best=} {recheck=}")
#
#         if _prog == recheck:
#             return start


def gold(lines):
    _reg, _prog = parse(lines)

    start = 117440 - 1

    while True:
        start += 1
        this = _reg.copy()
        this["A"] = start

        recheck = eval_prog(this, _prog)

        if _prog == recheck:
            return start

        # best = common_start(_prog, recheck)
        # if best > 7:
        #     seeds.append(start)
        #     print(f"{best=} {start=}")
        #     bbest = max(bbest, best)
        # candidates.append(start)


#         """
# best=7 start=15206555
# best=7 start=15206810
# best=7 start=11643290
#         """
#
#         # print(f"{candidates=}")
#
#         # print("union: ", union(candidates))
#
#         # if start | ideal
#         # ideal &= start
#         # print(f"{start=} {ideal=}")
#         # if ideal > start:
#         #     start = ideal
#         #     print(f"switching to {start=}")
#
#         #
#         # if best > 2 and len(recheck) == len(_prog):
#         #     print(f"{start=} {best=} {recheck=}")
#
#         if i % 10000 == 0:
#             print(f"{start}/{m} {bbest=}")
#
#         if _prog == recheck:
#             return start


def find_seeds(_reg, _prog, n):
    i = 0
    m = (1 << 32) - 1
    bbest = 0
    start = 0

    seeds = []

    while True:
        i += 1
        start += 5
        this = _reg.copy()
        this["A"] = start

        recheck = eval_prog(this, _prog)
        best = common_start(_prog, recheck)
        if best >= (len(_prog) - 1) / 2:
            seeds.append(start)
            bbest = max(bbest, best)
            if len(seeds) >= n:
                return seeds


def union(candidates):
    a = candidates[0]
    for b in candidates[1:]:
        a &= b
    return a


def common_start(a, b):
    m = min(len(a), len(b))
    best = 0
    for i in range(1, m + 1):
        if a[:i] != b[:i]:
            return best
        best = i
    return best

    # try to decrement from each bit, starting with significant bits
    # for bit in reversed(range(bits_count(big))):
    #     tmp = big
    #     decr = 1 << bit
    #     print(f"trying {decr=}")
    #     tmp -= decr
    #     if count_correct(tmp, _prog) == 16 and tmp < big:
    #         big = tmp
    #         print(f"decr new {big=}")
    #
    # tmp = big
    # decr = 1
    # while True:
    #     tmp -= decr
    #     if tmp <= 0:
    #         tmp = big
    #         decr = decr << 1
    #         print("now decr=", decr)
    #         if decr >= big:
    #             break
    #
    #     # print(f"{tmp=} {decr=}")
    #
    #     correct = count_correct(tmp, _prog)
    #     if correct == 16 and tmp < big:
    #         big = tmp
    #         # print(f"new decr best: {big=}")
    #         print("new decr best:", big)
    #         # decr = decr >> 1
    #         # if decr == 0:
    #         #     break
    #
    # _reg["A"] = big
    # recheck = eval_prog(_reg, _prog)
    # assert ",".join(map(str, _prog)) == recheck
    # return big
    #


def count_correct(tmp, numbers):
    correct = 0
    for i, n in enumerate(numbers):
        if formula(tmp) == n:
            correct += 1
        else:
            break
        tmp = tmp // 8
    return correct


def bits_count(n):
    return n.bit_count()
    # return int((math.log(n) / math.log(2)) + 1)


def formula(a):
    return ((a & 7) ^ 3) ^ (a // (1 << ((a & 7) ^ 5))) & 7


# dat = [2, 4, 1, 5, 7, 5, 1, 6, 4, 2, 5, 5, 0, 3, 3, 0]
# dat = [0, 3, 5, 4, 3, 0]


def validate(a):
    div = 1
    for i in range(16):
        if formula(a // div) != dat[i]:
            return False, i

        div += 8

    return True, 16

    #
    # def validate2(a):
    #     valid = 0
    #     for i in range(16):
    #         if formula(a // (i + 1)) == dat[i]:
    #             valid += 1
    #
    #     return valid == 16, valid

    """
    таак падажжи ебана
    print 2
        B = A % 8
        B = B ^ 5
        C = A // (1 << B)
        B = B ^ 6
        B = B ^ C
        B % 8 = 2
        
        а потом такая хуйня
        A = A // 8
        повторяем
        
        =====
        
        т.е 
        А должно быть так чтобы 
        B = (A % 8) ^ 5
        B = (B ^ 6) ^ (A // (1 << B)) % 8 == 2
        
        еще проще
        (((A % 8) ^ 5) ^ 6) ^ (A // (1 << ((A % 8) ^ 5))) % 8 == 2        
        
        и после того как А поделится на 8 его должно хватить на 15 других цифр
        пизда
        
        
        -------
        B = A % 8
        B = (A % 8) ^ 5
        C = (A // (1 << ((A % 8) ^ 5))
        B = ((A % 8) ^ 5) ^ 6
        B = (((A % 8) ^ 5) ^ 6) ^ ((A // (1 << ((A % 8) ^ 5)))
        
        
        FINAL: 
        ((((a % 8) ^ 5) ^ 6) ^ ((a / (1 << ((a % 8) ^ 5)))) % 8 = 2
        (((((a/8) % 8) ^ 5) ^ 6) ^ (((a/8) / (1 << (((a/8) % 8) ^ 5)))) % 8 = 4
        
        WOLFRAM:
        BitXor[BitXor[BitXor[Mod[a,8],5],6],Mod[a/(2^BitXor[Mod[a,8],5]),8]] = 2
        BitXor[BitXor[BitXor[Mod[(a/8),8],5],6],Mod[(a/8)/(2^BitXor[Mod[(a/8),8],5]),8]] = 4
        
        
        
    print 4
        B % 8 = 4
    print 1
        B % 8 = 1
    print 7
        B % 8 = 7   
    print 5
        B % 8 = 5           
    """

    #
    # хотим 2
    #   для этого надо чтобы в B было X % 8 = 2
    # хотим 4
    #   для этог

    # i = 0
    # while True:
    #     for j in range(-512, 513):
    #         reg = _reg.copy()
    #         reg["A"] = i + j
    #
    #         if eval_prog_gold(reg, _prog):
    #             return i + j
    #
    #     # if i % 4100 == 0:
    #     #     i += 4000
    #
    #     i += 2048


def eval_prog_gold(reg, prog):
    val = reg.copy()

    seen = set()

    out = []
    expected = prog.copy()
    ptr = 0
    while ptr < len(prog):
        inst = prog[ptr]
        literal = prog[ptr + 1]
        ptr += 2

        if inst == 0:
            reg["A"] //= 1 << combo(reg, literal)
        elif inst == 1:
            reg["B"] ^= literal
        elif inst == 2:
            reg["B"] = combo(reg, literal) % 8
        elif inst == 3:
            if reg["A"] == 0:
                continue
            ptr = literal
        elif inst == 4:
            reg["B"] ^= reg["C"]
        elif inst == 5:
            out.append(combo(reg, literal) % 8)
        elif inst == 6:
            reg["B"] = reg["A"] // (1 << combo(reg, literal))
        elif inst == 7:
            reg["C"] = reg["A"] // (1 << combo(reg, literal))

        if out and not compare(out, expected):
            return False

        if len(out) > 2:
            if frozenset(val.values()) not in seen:
                seen.add(frozenset(val.values()))
                print(out)
                print(val)

    return out == expected


def compare(smaller, bigger):
    for a, b in zip(smaller, bigger):
        if a != b:
            return False
    return True


def combo(reg, op):
    if 0 <= op <= 3:
        return op
    elif op == 4:
        return reg["A"]
    elif op == 5:
        return reg["B"]
    elif op == 6:
        return reg["C"]


def parse(lines):
    reg = {
        "A": 0,
        "B": 0,
        "C": 0,
    }
    prog = []
    for line in lines:
        if line.startswith("Register "):
            line = line.replace("Register ", "")
            k, v = line.split(":")
            reg[k] = int(v.strip())
        if line.startswith("Program: "):
            line = line.replace("Program: ", "")
            prog = list(map(int, line.split(",")))
    return reg, prog


def main():
    s = stdin()
    print("silver:", silver(s))
    print("gold:", gold(s))


def stdin():
    lines = []
    for line in sys.stdin.readlines():
        if line.strip():
            lines.append(line.strip())
    return lines


if __name__ == "__main__":
    main()


def bla():
    a = 0
    return ((((a % 8) ^ 5) ^ 6) ^ ((a / (1 << ((a % 8) ^ 5))))) % 8 == 2
