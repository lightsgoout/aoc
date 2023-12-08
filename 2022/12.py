import sys

import astar


def build_grid():
    grid = []
    start = None
    end = None
    y = 0
    for line in sys.stdin.readlines():
        line = line.strip()
        row = []
        for x, c in enumerate(line):
            if c == "S":
                start = (x, y)
                c = "a"
            if c == "E":
                end = (x, y)
                c = "z"
            row.append(c)
        grid.append(row)
        y += 1
    return grid, start, end


class GridSolver(astar.AStar):
    def __init__(self, grid):
        self.grid = grid
        self.width = len(self.grid[0])
        self.height = len(self.grid)

    def heuristic_cost_estimate(self, n1, n2):
        """computes the 'direct' distance between two (x,y) tuples"""
        return 1

    def distance_between(self, n1, n2):
        """this method always returns 1, as two 'neighbors' are always adajcent"""
        return 1

    def neighbors(self, node):
        """for a given coordinate in the maze, returns up to 4 adjacent(north,east,south,west)
        nodes that can be reached (=any adjacent coordinate that is not a wall)
        """
        x, y = node
        around = [
            (nx, ny)
            for nx, ny in [
                (x, y - 1),
                (x, y + 1),
                (x - 1, y),
                (x + 1, y),
            ]
        ]
        result = []
        for nx, ny in around:
            if nx < 0 or nx > self.width - 1:
                continue
            if ny < 0 or ny > self.height - 1:
                continue

            a = self.grid[y][x]
            b = self.grid[ny][nx]
            if ord(b) - ord(a) <= 1:
                result.append((nx, ny))
        return result


def main():
    grid, start, end = build_grid()
    print(f"{start=}")
    print(f"{end=}")
    print(f"{grid=}")

    path = list(GridSolver(grid).astar(start, end))
    print(f"{path=}")

    print(drawgrid(grid, list(path), start=start, end=end))
    # print(f'{path=}')
    print(len(path) - 1)


def drawgrid(grid, set1=[], set2=[], c="#", c2="*", start=(0, 0), end=(0, 0)):
    """returns an ascii maze, drawing eventually one (or 2) sets of positions.
    useful to draw the solution found by the astar algorithm
    """
    set1 = list(set1)
    set2 = list(set2)
    width = len(grid[0])
    height = len(grid)
    result = ""
    for j in range(height):
        for i in range(width):
            if (i, j) in set1:
                c = grid[j][i]
                if (i, j) == start:
                    c = 'S'
                if (i, j) == end:
                    c = 'E'
                result = result + "\033[32m" + c + "\033[0m"
            elif (i, j) in set2:
                result = result + c2
            else:
                c = grid[j][i]
                if (i, j) == start:
                    c = 'S'
                if (i, j) == end:
                    c = 'E'
                result = result + c
        result = result + "\n"
    return result


if __name__ == "__main__":
    main()
