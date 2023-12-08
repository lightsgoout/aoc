import sys
from typing import Tuple


def parse_line(line: str) -> Tuple[int, list[dict]]:
    left, right = line.split(':')
    game_id = int(left.split(' ')[-1])
    reveals = []
    for raw in right.split(';'):
        reveal = {}
        for part in raw.split(','):
            part = part.strip()
            count, color = part.split(' ')
            count = int(count)
            reveal[color] = count
        reveals.append(reveal)

    return game_id, reveals


def silver(lines) -> int:
    r = 0
    for line in lines:
        game_id, reveals = parse_line(line)
        red, green, blue = 0, 0, 0
        for rev in reveals:
            red = max(rev.get('red', 0), red)
            green = max(rev.get('green', 0), green)
            blue = max(rev.get('blue', 0), blue)
        if red <= 12 and green <= 13 and blue <= 14:
            r += game_id
    return r


def gold(lines) -> int:
    r = 0
    for line in lines:
        game_id, reveals = parse_line(line)
        red, green, blue = 0, 0, 0
        for rev in reveals:
            red = max(rev.get('red', 0), red)
            green = max(rev.get('green', 0), green)
            blue = max(rev.get('blue', 0), blue)
        r += red * green * blue
    return r


def main():
    lines = []
    for line in sys.stdin.readlines():
        line = line.strip()
        if not line:
            continue
        lines.append(line)

    print('silver:', silver(lines))
    print('gold:', gold(lines))


if __name__ == '__main__':
    main()
