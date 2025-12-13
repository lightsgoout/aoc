import time

import aoc


class grid(aoc.grid):
    def __init__(self, lines):
        super().__init__(lines)
        self.max_dirty_point = aoc.point(-1, -1)

    def __setitem__(self, p: aoc.point, value):
        super().__setitem__(p, value)
        if p.y > self.max_dirty_point.y or (
            p.y == self.max_dirty_point.y and p.x > self.max_dirty_point.x
        ):
            self.max_dirty_point = p


def solve(lines):
    shapes = parse_shapes(lines)

    rotations = []

    for i, fig in enumerate(shapes):
        rotations.append(shape_variants(fig))

    piles = parse_piles(lines)
    res = 0
    for i, ((w, h), counts) in enumerate(piles, start=1):
        t0 = time.time()
        ans = solve_pile(w, h, counts, shapes, rotations)
        t1 = time.time() - t0
        res += ans
        print(f"[{i}/{len(piles)}] {w}x{h}: {counts} = {ans} | {round(t1, 2)} sec")
    return res


def parse_shapes(lines):
    shapes = []
    shape = []
    for line in lines:
        if "." in line or "#" in line:
            shape.append(line)
        else:
            if shape:
                shapes.append(shape.copy())
                shape = []

    return shapes


def solve_pile(w, h, counts, shapes, rotations) -> int:
    global cache

    cache = {}

    board = []
    for _ in range(h):
        row = ""
        for _ in range(w):
            row += "."
        board.append(row)
    board = grid(board)

    total_space = board.width * board.height
    required_space = 0

    figs = []
    for i, sh in enumerate(shapes):
        c = counts[i]
        if c == 0:
            continue

        for _ in range(c):
            figs.append(sh)
            g = grid(sh)

            for p in g:
                if g[p] == "#":
                    required_space += 1

    if total_space < required_space:
        print(f"{total_space=} < {required_space=}")
        return 0

    if total_space - required_space >= 50:
        return 1

    all_figs = []
    for i, fig in enumerate(shapes):
        for j in range(counts[i]):
            all_figs.append(rotations[i])

    return fit_shapes(board, tuple(all_figs), "A")


cache = {}


def fit_shapes(board, shapes, sym):
    if ord(sym) > ord("Z"):
        sym = "A"

    global cache

    key = hash((board, shapes))
    if key in cache:
        return cache[key]

    print(f"shapes remaining: {len(shapes)} {sym=} {hash(board)=}")
    board.dump()
    if not shapes:
        cache[key] = 1
        return 1

    # break if not fittable at all
    t0 = time.time()
    ok, _, start = fit_shape(board.copy(), shapes[0], sym, None)
    t1 = time.time() - t0
    # print("fitting took ", t1)

    if not ok:
        cache[key] = 0
        return 0

    bans = set([p for p in board if p < start])
    for p in board:
        if p < start:
            continue

        ok, board_var, best_point = fit_shape(board, shapes[0], sym, bans)
        if not ok:
            cache[key] = 0
            return 0

        bans |= set([p for p in board if p < best_point])

        if ok:
            if fit_shapes(board_var.copy(), tuple(shapes[1:]), chr(ord(sym) + 1)) == 1:
                cache[key] = 1
                return 1

        bans.add(p)

    cache[key] = 0
    return 0


def fit_shape(board, rots, sym, banned=None) -> tuple[bool, grid, aoc.point]:
    best_touches = -1
    best_rot = -1
    best_point = aoc.point(-1, -1)
    fit = False
    board2 = None

    for p in board:
        if banned and p in banned:
            continue

        if p > board.max_dirty_point and board.max_dirty_point != aoc.point(-1, -1):
            break

        for i, rot in enumerate(rots):
            fit_res, fit_touches = shape_fits(board, rot, p)
            if fit_res and fit_touches > best_touches:
                best_touches = fit_touches
                best_rot = i
                best_point = p
                fit = True

    if fit:
        # place it
        board2 = board.copy()
        place_shape(board2, rots[best_rot], best_point, sym)

    return fit, board2, best_point


def shape_fits(board, fig, at):
    touches = set()
    for p in fig:
        if fig[p] == ".":
            continue

        target = at + p
        if not board.inside(target):
            return False, 0

        if board[target] != ".":
            return False, 0

        for diff in list(aoc.directions4()):
            around = target + diff
            if board.inside(around) and board[around] != ".":
                touches.add(around)

    return True, len(touches)


def place_shape(board, fig, at, sym):
    for p in fig:
        if fig[p] == ".":
            continue

        target = at + p
        assert board.inside(target)
        assert board[target] == "."
        board[target] = sym

    return 0


def parse_piles(lines):
    result = []
    for line in lines:
        if not "x" in line:
            continue
        dims, counts = line.split(":")

        w, h = map(int, dims.split("x"))
        counts = list(map(int, counts.strip().split()))
        result.append(((w, h), counts))

    return result


def shape_variants(fig):
    fig = grid(fig)
    return (
        fig,
        rotate_fig(fig),
        rotate_fig(rotate_fig(fig)),
        rotate_fig(rotate_fig(rotate_fig(fig))),
    )


def reset_board(board: grid):
    for p in board:
        board[p] = "."
    board.max_dirty_point = aoc.point(-1, -1)


def rotate_fig(_fig):
    if not isinstance(_fig, grid):
        fig = grid(_fig)
    else:
        fig = _fig

    board = []
    for _ in range(fig.height * 4):
        row = ""
        for _ in range(fig.width * 4):
            row += "."
        board.append(row)
    fig2 = grid(board)

    start = aoc.point(fig2.height // 2, fig2.width // 2)

    for p in fig:
        if fig[p] == ".":
            continue
        p2 = start + aoc.point(-p.x, p.y)
        fig2[p2] = "#"

    # trim result
    min_x, min_y = 9999999, 9999999
    max_x, max_y = 0, 0
    for p in fig2:
        if fig2[p] == "#":
            min_x = min(min_x, p.x)
            max_x = max(max_x, p.x)
            min_y = min(min_y, p.y)
            max_y = max(max_y, p.y)

    res = []
    for y in range(fig2.max_y):
        row = []
        for x in range(fig2.max_x):
            if min_y <= y <= max_y and min_x <= x <= max_x:
                row.append(fig2[aoc.point(y, x)])
        if row:
            res.append(row)

    return grid(res)


def main():
    print(solve(aoc.stdin()))


if __name__ == "__main__":
    main()
