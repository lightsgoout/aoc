import dataclasses
import sys
from collections import defaultdict
from pprint import pprint
from typing import Tuple


@dataclasses.dataclass
class Config:
    seeds: list[int]
    gates: dict[int, list[Tuple[int, int, int]]]


def calc(seed: int, cfg: Config) -> int:
    for level in range(1, 8):
        gates = cfg.gates[level]
        for dst, src, rng in gates:
            if src <= seed <= src + rng:
                diff = seed - src
                seed = dst + diff
                break

    return seed


def silver(cfg: Config) -> int:
    r = sys.maxsize
    for seed in cfg.seeds:
        sv = calc(seed, cfg)
        r = min(sv, r)
    return r


def gold(cfg: Config) -> int:
    r = sys.maxsize
    for pair_idx, (seed_start, seed_rng) in enumerate(zip(cfg.seeds[::2], cfg.seeds[1::2])):
        print('calculating pair ', pair_idx)
        for seed in range(seed_start, seed_start + seed_rng):
            sv = calc(seed, cfg)
            r = min(sv, r)
    return r


# def gate(cfg: Config, level: int, lo: int, hi: int) -> int:
#     r = sys.maxsize
#     for dst, src, rng in cfg.gates[level]:
#         if (src <= lo <= src + rng) or (src <= hi <= src + rng):
#             gate_lo = max(lo, src)
#             gate_hi = min(hi, src+rng)
#             if level < 7:
#                 r = min(r, gate(cfg, level+1, gate_lo, gate_hi))


def build_hops(cfg: Config, level: int):
    hops = {}
    i = 0
    for dst, src, rng in cfg.gates[level]:
        next_hops = None
        if level < 7:
            next_hops = build_hops(cfg, level + 1)
        hops[(src, src + rng)] = {
            'dst': dst,
            'rng': rng,
            'gates': next_hops,
        }
        i += 1
    hops[(0, sys.maxsize, i + 1)] = {
        'gates': next_hops,
    }
    return hops


def iterate_range(hops: dict, lo: int, hi: int, level: int = 1) -> int:
    r = sys.maxsize
    for (src_lo, src_hi), next_hops in hops.items():
        # print(next_hops)
        if (src_lo <= lo < src_hi) or (src_lo <= hi < src_hi):
            print(f'matched {src_lo=} {src_hi=} {level=}')
            gate_lo = max(lo, src_lo)
            gate_hi = min(hi, src_hi)
            # assert gate_lo <= src_lo
            # assert gate_hi >= src_hi
            diff = lo - gate_lo
            gate_lo -= diff
            gate_hi -= diff

            ranges = []
            if lo < gate_lo:
                ranges.append((lo, gate_lo - 1))
            if hi > gate_hi:
                ranges.append((gate_hi + 1, hi))
            ranges.append((gate_lo, gate_hi))

            print(f'{len(ranges)=}')
            print(ranges)

            for next_lo, next_hi in ranges:
                if next_hops['gates'] is not None:
                    print(f'going to next with {next_lo=} {next_hi=}')
                    print(next_hops['gates'].keys())
                    r = min(r, iterate_range(next_hops['gates'], next_lo, next_hi, level + 1))
                else:
                    print('here')
                    r = min(next_lo, r)
            break

    return r


def gold2(cfg: Config) -> int:
    hops = build_hops(cfg, 1)
    r = sys.maxsize
    for pair_idx, (seed_start, seed_rng) in enumerate(zip(cfg.seeds[::2], cfg.seeds[1::2])):
        print(f'calculating pair: {pair_idx} ({seed_start}, {seed_start+seed_rng})')
        r = min(r, iterate_range(hops, seed_start, seed_start + seed_rng))
    return r


def prepare_ranges(lo: int, hi: int, cfg: Config) -> list:
    ranges = []
    for level in range(1, 8):
        gates = cfg.gates[level]
        for dst, src, rng in gates:
            gate_lo = src
            gate_hi = src + rng - 1
            if lo < gate_lo:
                ranges.append((level, lo, gate_lo - 1))
            if hi > gate_hi:
                ranges.append((level, gate_hi + 1, hi))
            ranges.append((level, gate_lo, gate_hi))
    return ranges


# def exec_range(level: int, lo: int, hi: int, cfg: Config) -> int:
#     for dst, src, rng in cfg.gates[level]:
#         if src <=
#
#     pass


def calc2(lo: int, hi: int, cfg: Config) -> int:
    seed = lo
    incr = 1
    while seed < hi:
        for level in range(1, 8):
            gates = cfg.gates[level]
            for dst, src, rng in gates:
                if src <= seed <= src + rng:
                    diff = seed - src
                    seed = dst + diff
                    break
        seed += incr

    return seed


def gold4(cfg: Config) -> int:
    r = sys.maxsize
    for pair_idx, (seed_start, seed_rng) in enumerate(zip(cfg.seeds[::2], cfg.seeds[1::2])):
        print('calculating pair ', pair_idx)
        seed = seed_start
        incr = 14
        hi = seed_start + seed_rng - 1
        while True:
            sv = calc(seed, cfg)
            r = min(sv, r)
            seed += incr
            if hi - seed == 50:
                incr = 1
            seed = min(hi, seed)
            if seed >= hi:
                sv = calc(seed, cfg)
                r = min(sv, r)
                break
    return r


# def calc(seed: int, cfg: Config) -> int:
#     for level in range(1, 8):
#         gates = cfg.gates[level]
#         for dst, src, rng in gates:
#             if src <= seed <= src + rng:
#                 diff = seed - src
#                 seed = dst + diff
#                 break
#
#     return seed


def gold3(cfg: Config) -> int:
    r = sys.maxsize
    for range_idx, (seed_start, seed_rng) in enumerate(zip(cfg.seeds[::2], cfg.seeds[1::2])):
        print(f'calculating range: {range_idx} ({seed_start}, {seed_start+seed_rng})')
        ranges = prepare_ranges(seed_start, seed_start + seed_rng - 1, cfg)
        # sv = calc_range(seed_start, seed_start + seed_rng - 1, cfg)
        pprint(ranges)
        # r = min(sv, r)

    return r


# def gold2(cfg: Config) -> int:
#     hops = {}
#     for dst, src, rng in cfg.gates[1]:
#         hops[(src, src+rng)] = {
#             'dst': dst,
#             'rng': rng,
#             'gates': {},
#         }
#
#
#
#
#
#
#
#
#     # r = sys.maxsize
#     for pair_idx, (seed_start, seed_rng) in enumerate(zip(cfg.seeds[::2], cfg.seeds[1::2])):
#         print('calculating pair ', pair_idx)
#         pair_min = sys.maxsize
#         for level in range(1, 8):
#             for dst, src, rng in cfg.gates[level]:
#
#
#
#
#
#
#
#
#         for seed in range(seed_start, seed_start + seed_rng):
#             sv = calc(seed, cfg)
#             r = min(sv, r)
#     return r


def main():
    cfg = parse()
    print('silver:', silver(cfg))
    print('gold:', gold4(cfg))


def parse() -> Config:
    seeds = []
    gate = 0
    gates = defaultdict(list)
    for line in sys.stdin.readlines():
        line = line.strip()
        if not line:
            continue

        if line.startswith('seeds:'):
            seeds = [int(x.strip()) for x in line.split(':')[1].split(' ') if x.strip() != '']
            continue

        if '-to-' in line:
            gate += 1
            continue

        dst, src, rng = [int(x.strip()) for x in line.split(' ') if x.strip() != '']
        gates[gate].append((dst, src, rng))

    return Config(seeds=seeds, gates=gates)


if __name__ == '__main__':
    main()
