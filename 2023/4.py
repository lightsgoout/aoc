import collections
import sys
from pprint import pprint


def silver(cards) -> int:
    r = 0
    for idx, left, right in cards:
        left_set = set(left)
        right_set = set(right)
        win = left_set.intersection(right_set)
        card_score = 0
        if win:
            card_score = 1 << len(win) - 1

        r += card_score

    return r


def gold(cards) -> int:
    m = {}
    for idx, left, right in cards:
        m[idx] = (idx, left, right)

    pile = []
    queue = collections.deque()
    for c in cards:
        queue.append(c)

    while len(queue):
        idx, left, right = queue.popleft()
        left_set = set(left)
        right_set = set(right)
        win = left_set.intersection(right_set)
        if win:
            pile.append(idx)
            # print(f'card {idx} wins {len(win)}:')
            for i in range(len(win)):
                queue.append(m[idx + i + 1])
                # print(f'appending card {idx+i+1}')
        else:
            # print(f'card {idx} no win')
            pile.append(idx)

    return len(pile)


def parse() -> list:
    result = []
    for idx, line in enumerate(sys.stdin.readlines(), start=1):
        line = line.strip()
        if not line:
            continue

        _, data = line.split(':')
        left, right = data.split('|')

        left = [int(x.strip()) for x in left.split(' ') if x.strip() != '']
        right = [int(x.strip()) for x in right.split(' ') if x.strip() != '']

        result.append((idx, left, right))
    return result


def main():
    cards = parse()
    print('silver:', silver(cards))
    print('gold:', gold(cards))


if __name__ == '__main__':
    main()
