import collections
import enum
import itertools
import sys
from functools import lru_cache


class HandType(enum.IntEnum):
    five = 500
    four = 400
    full_house = 399
    three = 300
    two_pair = 200
    one_pair = 100
    high_card = 1


class CardType(enum.IntEnum):
    A = 24
    K = 13
    Q = 12
    J = 11
    T = 10
    NINE = 9
    EIGHT = 8
    SEVEN = 7
    SIX = 6
    FIVE = 5
    FOUR = 4
    THREE = 3
    TWO = 2
    JOKER = 1


rules = [
    (HandType.five, lambda c: any(v == 5 for k, v in c.items())),
    (HandType.four, lambda c: any(v == 4 for k, v in c.items())),
    (HandType.full_house, lambda c: any(v == 3 for k, v in c.items()) and any(v == 2 for k, v in c.items())),
    (HandType.three, lambda c: any(v == 3 for k, v in c.items())),
    (HandType.two_pair, lambda c: sum([1 for k, v in c.items() if v == 2]) == 2),
    (HandType.one_pair, lambda c: sum([1 for k, v in c.items() if v == 2]) == 1),
    (HandType.high_card, lambda c: True),
]

strength = {
    '2': CardType.TWO,
    '3': CardType.THREE,
    '4': CardType.FOUR,
    '5': CardType.FIVE,
    '6': CardType.SIX,
    '7': CardType.SEVEN,
    '8': CardType.EIGHT,
    '9': CardType.NINE,
    'T': CardType.T,
    'J': CardType.J,
    'Q': CardType.Q,
    'K': CardType.K,
    'A': CardType.A,
    'j': CardType.JOKER,
}


def hand_type(card: str):
    cnt = collections.Counter(card)
    for t, rule in rules:
        if rule(cnt):
            return t


def jokerize(card: str):
    jpos = [i for i, c in enumerate(card) if c == 'j']
    if not jpos:
        return card

    if card == 'jjjjj':
        return 'AAAAA'

    combs = []
    for new in itertools.combinations_with_replacement([t for t in strength.keys() if t != 'j'], len(jpos)):
        if len(jpos) == 4:
            j1, j2, j3, j4 = jpos
            combs.append(
                card[:j1]
                + new[0]
                + card[j1 + 1 : j2]
                + new[1]
                + card[j2 + 1 : j3]
                + new[2]
                + card[j3 + 1 : j4]
                + new[3]
                + card[j4 + 1 :]
            )
        elif len(jpos) == 3:
            j1, j2, j3 = jpos
            combs.append(
                card[:j1] + new[0] + card[j1 + 1 : j2] + new[1] + card[j2 + 1 : j3] + new[2] + card[j3 + 1 :]
            )
        elif len(jpos) == 2:
            j1, j2 = jpos
            combs.append(card[:j1] + new[0] + card[j1 + 1 : j2] + new[1] + card[j2 + 1 :])
        elif len(jpos) == 1:
            j1 = jpos[0]
            combs.append(card[:j1] + new[0] + card[j1 + 1 :])
        else:
            raise AssertionError('unhandled: ' + card)

    best = list(sorted(combs, key=lambda cc: card_key(cc)))[-1]
    return best


@lru_cache(maxsize=None)
def card_key(card: str, joker=False):
    if joker:
        card = card.replace('J', 'j')
        original_card = card
        card = jokerize(card)
    else:
        original_card = card

    t = hand_type(card)
    return t, *[strength[c] for c in original_card]


def solve(pairs, joker=False):
    pairs = sorted([(c, bid) for c, bid in pairs], key=lambda c: card_key(c[0], joker=joker))
    r = 0
    for rank, (card, bid) in enumerate(pairs, start=1):
        print(
            f'{rank=} {card=} jokerized={jokerize(card.replace("J", "j"))} {bid=} key={card_key(card, joker=joker)}'
        )
        r += bid * rank

    return r


def main():
    pairs = []
    for line in sys.stdin.readlines():
        line = line.strip()
        if not line:
            continue

        card, bid = line.split()
        bid = int(bid)
        pairs.append((card, bid))

    print('silver:', solve(pairs, joker=False))
    print('gold:', solve(pairs, joker=True))


if __name__ == '__main__':
    main()
