import sys
from functools import reduce

grid = []
for line in sys.stdin.readlines():
    line = line.strip()
    grid.append([*map(int, line)])

grid_rotated = [list(l) for l in zip(*grid)]


def iter_x():
    return range(len(grid[0]))


def iter_y():
    return range(len(grid))


MAX_Y = len(grid) - 1
MAX_X = len(grid[0]) - 1


visible = 0
for x in iter_x():
    for y in iter_y():
        tree = grid[y][x]
        if y == 0 or y == MAX_Y:
            visible += 1
        elif x == 0 or x == MAX_X:
            visible += 1
        else:
            rows = [
                # west
                grid[y][:x],
                # east
                grid[y][x + 1 :],
                # north
                grid_rotated[x][:y],
                # south
                grid_rotated[x][y + 1 :],
            ]
            if tree > reduce(min, map(max, rows)):
                visible += 1

print(visible)
# print(f'{edge=}')
# print(horizontal_max)
# print(vertical_max)
# print(grid)
