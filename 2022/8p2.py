import operator
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


max_score = 0
for x in iter_x():
    for y in iter_y():
        tree = grid[y][x]
        rows = [
            # west
            list(reversed(grid[y][:x])),
            # east
            grid[y][x + 1 :],
            # north
            list(reversed(grid_rotated[x][:y])),
            # south
            grid_rotated[x][y + 1 :],
        ]
        visible_by_row = []
        for row in rows:
            visible = 0
            for t in row:
                visible += 1
                if t >= tree:
                    break
            visible_by_row.append(visible)
        max_score = max(max_score, reduce(operator.mul, visible_by_row))

print(max_score)
