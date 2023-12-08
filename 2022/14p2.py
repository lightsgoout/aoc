import enum
import sys
from collections import namedtuple
from functools import reduce

point = namedtuple("point", "x y")


class PointState(enum.Enum):
    AIR = "."
    ROCK = "#"
    SAND_SRC = "+"
    SAND = "o"


class FlowResult(enum.Enum):
    OK = enum.auto()
    REST = enum.auto()
    ABYSS_REACHED = enum.auto()


flow_blockers = {PointState.ROCK, PointState.SAND}


class Grid:
    def __init__(self, line_groups: list[list[point]], sand_src: list[point]):
        g = []
        rocks: set[point] = set()
        for line_group in line_groups:
            for start, end in zip(line_group, line_group[1:]):
                if start.x == end.x:
                    # vertical
                    for y in range(min(start.y, end.y), max(start.y, end.y) + 1):
                        rocks.add(point(x=start.x, y=y))
                elif start.y == end.y:
                    # horizontal
                    for x in range(min(start.x, end.x), max(start.x, end.x) + 1):
                        rocks.add(point(x=x, y=start.y))
                else:
                    raise AssertionError("invalid line")

        # noinspection PyTypeChecker
        self.floor = reduce(max, [r.y for r in rocks]) + 2
        # noinspection PyTypeChecker
        self.max_x = reduce(max, [r.x for r in rocks]) + 1

        for y in range(self.floor + 1):
            row = []
            for x in range(self.max_x * 2):
                state = PointState.AIR
                if (x, y) in sand_src:
                    state = PointState.SAND_SRC
                elif (x, y) in rocks:
                    state = PointState.ROCK
                elif y == self.floor:
                    state = PointState.ROCK
                row.append(state)

            g.append(row)

        self.grid = g
        self.sand_src = sand_src

    def dump(self):
        min_x = +sys.maxsize
        max_x = -sys.maxsize
        min_y = +sys.maxsize
        max_y = -sys.maxsize
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if self.grid[y][x] != PointState.AIR:
                    if y != self.floor:
                        min_x = min(min_x, x)
                        max_x = max(max_x, x)
                    min_y = min(min_y, y)
                    max_y = max(max_y, y)

        for y in range(min_y, max_y + 1):
            row = []
            for x in range(min_x, max_x + 1):
                row.append(self.grid[y][x].value)
            print("".join(row))
        print("")

    def flow_grain(self, grain: point) -> tuple[point, FlowResult]:
        positions_to_consider = [
            point(y=grain.y + 1, x=grain.x),  # straight down
            point(y=grain.y + 1, x=grain.x - 1),  # left down
            point(y=grain.y + 1, x=grain.x + 1),  # right down
        ]
        for position in positions_to_consider:
            if not self.is_blocked(position):
                if self.grid[grain.y][grain.x] != PointState.SAND_SRC:
                    self.grid[grain.y][grain.x] = PointState.AIR
                self.grid[position.y][position.x] = PointState.SAND
                return position, FlowResult.OK

        return grain, FlowResult.REST

    def is_blocked(self, p: point):
        return self.grid[p.y][p.x] in flow_blockers or p.y == self.floor

    def simulate_sand(self) -> int:
        total_grains = 0
        for src in self.sand_src:
            total_grains += self.simulate_sand_from(src)
        return total_grains

    def simulate_sand_from(self, src: point):
        total_grains = 0
        while True:
            # spawn a new grain
            grain = src
            grain_moves = 0
            while True:
                grain, result = self.flow_grain(grain)
                if result == FlowResult.OK:
                    grain_moves += 1
                elif result == FlowResult.REST:
                    if grain_moves == 0:
                        # overflow
                        total_grains += 1
                        return total_grains
                    # spawn next grain
                    total_grains += 1
                    break
                elif result == FlowResult.ABYSS_REACHED:
                    return total_grains

            # print(f"{total_grains=}")
            # self.dump()


def main():
    line_groups = []
    for s in sys.stdin.readlines():
        s = s.strip()
        line = []
        for p in s.split("->"):
            p = p.strip()
            x, y = p.split(",")
            line.append(point(x=int(x), y=int(y)))
        line_groups.append(line)

    grid = Grid(line_groups, [point(500, 0)])
    # grid.dump()

    total_grains = grid.simulate_sand()
    print(f"total_grains = {total_grains}")


if __name__ == "__main__":
    main()
