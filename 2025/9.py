import aoc

import psycopg2


def silver(lines):
    points = []
    for line in lines:
        p = tuple(map(int, line.split(",")))
        points.append(p)

    flat = []
    pairs = set()

    for p1 in points:
        for p2 in points:
            if p1 == p2:
                continue

            if pair_key(p1, p2) in pairs:
                continue

            flat.append((p1, p2, distance(p1, p2)))
            pairs.add(pair_key(p1, p2))

    best = 0
    for a, b, _ in sorted(flat, key=lambda k: k[2], reverse=True):
        h = abs(a[0] - b[0]) + 1
        w = abs(a[1] - b[1]) + 1
        best = max(best, h * w)

    return best


def pair_key(p1, p2):
    return min(p1, p2), max(p1, p2)


def distance(a, b):
    da = a[0] - b[0]
    db = a[1] - b[1]
    return da * da + db * db


def gold(lines):
    points = []
    for line in lines:
        p = tuple(map(int, line.split(",")))
        points.append(p)

    flat = []
    pairs = set()

    for p1 in points:
        for p2 in points:
            if p1 == p2:
                continue

            if pair_key(p1, p2) in pairs:
                continue

            flat.append((p1, p2, distance(p1, p2)))
            pairs.add(pair_key(p1, p2))

    conn = psycopg2.connect("")
    cur = conn.cursor()

    best = 0
    iters = 0
    for a, b, _ in sorted(flat, key=lambda k: k[2], reverse=True):
        iters += 1
        if iters % 1000 == 0:
            print(f"{iters=} {best=}")

        h = abs(a[0] - b[0]) + 1
        w = abs(a[1] - b[1]) + 1
        if h * w > best:
            c = (a[0], b[1])
            d = (b[0], a[1])
            quad = [a, c, b, d]
            if not within(cur, quad, points):
                continue

            best = h * w
            print(f"new {best=}")

    return best


def within(cur, quad, pipe):
    solution = (
        "select st_contains("
        "   st_makepolygon(st_geomfromtext('LINESTRING({points})')),"
        "   st_makepolygon(st_geomfromtext('LINESTRING({quad})')));"
    ).format(
        points=",".join([f"{x} {y}" for (x, y) in [*pipe, pipe[0]]]),
        quad=",".join([f"{x} {y}" for (x, y) in [*quad, quad[0]]]),
    )
    cur.execute(solution)
    return cur.fetchone()[0] is True


def main():
    print("silver:", silver(aoc.stdin()))
    print("gold:", gold(aoc.stdin()))


if __name__ == "__main__":
    main()
