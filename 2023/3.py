import sys
from pprint import pprint
from typing import Tuple


def around(g, y, x):
    # X..
    # ...
    # ...
    if y > 0 and x > 0:
        yield y - 1, x - 1

    # ...
    # X..
    # ...
    if x > 0:
        yield y, x - 1

    # ...
    # ...
    # X..
    if y < len(g) - 1 and x > 0:
        yield y + 1, x - 1

    # .X.
    # ...
    # ...
    if y > 0:
        yield y - 1, x

    # ...
    # ...
    # .X.
    if y < len(g) - 1:
        yield y + 1, x

    # ..X
    # ...
    # ...
    if x < len(g[0]) - 1 and y > 0:
        yield y - 1, x + 1

    # ...
    # ..X
    # ...
    if x < len(g[0]) - 1:
        yield y, x + 1

    # ...
    # ...
    # ..X
    if x < len(g[0]) - 1 and y < len(g) - 1:
        yield y + 1, x + 1


def silver(g, numbers) -> int:
    dump_grid(g)
    r = 0
    visited = set()
    visited_numbers = set()
    for y in range(len(g)):
        for x in range(len(g[y])):
            v = g[y][x]
            if v != '.' and not v.isdigit():
                for py, px in around(g, y, x):
                    if number := numbers.get((py, px)):
                        if number['id'] not in visited_numbers:
                            r += number['value']
                            visited_numbers.add(number['id'])
            visited.add((y, x))

    return r


def gold(g, numbers) -> int:
    dump_grid(g)
    r = 0
    for y in range(len(g)):
        for x in range(len(g[y])):
            v = g[y][x]
            if v == '*':
                gear_numbers = []
                gear_set = set()
                for py, px in around(g, y, x):
                    if number := numbers.get((py, px)):
                        if number['id'] not in gear_set:
                            gear_numbers.append(number)
                            gear_set.add(number['id'])

                if len(gear_numbers) == 2:
                    r += gear_numbers[0]['value'] * gear_numbers[1]['value']

    return r


def build_grid() -> Tuple[list[list], dict]:
    grid = []
    number_map = {}
    number_id = 0
    for y, line in enumerate(sys.stdin.readlines()):
        line = line.strip()
        row = []
        number = []
        number_coords = []
        for x, c in enumerate(line):
            row.append(c)
            if c.isdigit():
                number_coords.append((y, x))
                number.append(c)
            else:
                if number_coords:
                    for p in number_coords:
                        number_map[p] = {
                            'id': number_id,
                            'value': int(''.join(number)),
                        }
                    number = []
                    number_coords = []
                    number_id += 1
        if number_coords:
            for p in number_coords:
                number_map[p] = {
                    'id': number_id,
                    'value': int(''.join(number)),
                }
            number_id += 1
        grid.append(row)
    return grid, number_map


def dump_grid(g):
    min_x = +sys.maxsize
    max_x = -sys.maxsize
    min_y = +sys.maxsize
    max_y = -sys.maxsize
    for y in range(len(g)):
        for x in range(len(g[y])):
            min_x = min(min_x, x)
            max_x = max(max_x, x)
            min_y = min(min_y, y)
            max_y = max(max_y, y)

    for y in range(min_y, max_y + 1):
        row = []
        for x in range(min_x, max_x + 1):
            row.append(g[y][x])
        print("".join(row))
    print("")


def main():
    grid, numbers = build_grid()

    print('silver:', silver(grid, numbers))
    print('gold:', gold(grid, numbers))


if __name__ == '__main__':
    main()
