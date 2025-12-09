import itertools
import sys
import time

from PIL import Image
import aoc
import psycopg2
import pygame

SCALE = 200


def main():
    t0 = time.time()
    lines = aoc.stdin()

    points = []
    for line in lines:
        p = tuple(map(int, line.split(",")))
        points.append(p)

    fw = max([p[0] for p in points]) // SCALE + 10
    fh = max([p[1] for p in points]) // SCALE + 10
    pygame.init()
    screen = pygame.display.set_mode((fw, fh))

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

    pixels = set()
    best_quad = None
    candidate_quad = None
    border = []

    time.sleep(2)
    for p1, p2 in itertools.pairwise(points + [points[0]]):
        border.append(scale(p1))
        render_frame(screen, fw, fh, border, best_quad, candidate_quad)

        if p1[0] == p2[0]:
            if p2[1] > p1[1]:
                rng = range(p1[1], p2[1] + 1)
            else:
                rng = range(p2[1], p1[1] + 1)

            for y in rng:
                p = scale((p1[0], y))
                if p not in pixels:
                    pixels.add(p)
                    border.append(p)
                    render_frame(screen, fw, fh, border, best_quad, candidate_quad)
        else:
            if p2[0] > p1[0]:
                rng = range(p1[0], p2[0] + 1)
            else:
                rng = range(p2[0], p1[0] + 1)

            for x in rng:
                p = scale((x, p1[1]))
                if p not in pixels:
                    pixels.add(p)
                    border.append(p)
                    render_frame(screen, fw, fh, border, best_quad, candidate_quad)

        border.append(scale(p2))
        render_frame(screen, fw, fh, border, best_quad, candidate_quad)

    conn = psycopg2.connect("")
    cur = conn.cursor()

    best = 0
    i = 0
    throttle = 100
    for a, b, _ in sorted(flat, key=lambda k: k[2], reverse=True):
        i += 1

        h = abs(a[0] - b[0]) + 1
        w = abs(a[1] - b[1]) + 1
        if h * w > best:
            c = (a[0], b[1])
            d = (b[0], a[1])
            quad = [a, c, b, d]

            if i % throttle == 0:
                candidate_quad = quad

            render_frame(screen, fw, fh, border, best_quad, candidate_quad)
            if not within(cur, quad, points):
                continue

            candidate_quad = quad
            render_frame(screen, fw, fh, border, best_quad, candidate_quad)

            best = h * w
            best_quad = quad

    candidate_quad = None
    print("finished in ", time.time() - t0)
    while True:
        render_frame(screen, fw, fh, border, best_quad, candidate_quad)
        time.sleep(1)


frame_cache = None


def render_frame(screen, w, h, border, best_quad, candidate_quad):
    cache = (*(border or []), *(best_quad or []), *(candidate_quad or []))

    global frame_cache
    if frame_cache == cache:
        return

    frame_cache = cache

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)

    img = Image.new("RGB", (w, h))

    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    YELLOW = (255, 255, 0)

    for x, y in border:
        img.putpixel((x, y), RED)

    if best_quad is not None:
        a, b, c, d = best_quad
        x0 = min(a[0], b[0], c[0], d[0]) // SCALE
        x1 = max(a[0], b[0], c[0], d[0]) // SCALE
        y0 = min(a[1], b[1], c[1], d[1]) // SCALE
        y1 = max(a[1], b[1], c[1], d[1]) // SCALE

        for x in range(x0, x1 + 1):
            for y in range(y0, y1 + 1):
                img.putpixel((x, y), GREEN)

    if candidate_quad is not None:
        a, b, c, d = candidate_quad
        x0 = min(a[0], b[0], c[0], d[0]) // SCALE
        x1 = max(a[0], b[0], c[0], d[0]) // SCALE
        y0 = min(a[1], b[1], c[1], d[1]) // SCALE
        y1 = max(a[1], b[1], c[1], d[1]) // SCALE

        for x in range(x0, x1 + 1):
            img.putpixel((x, y0), YELLOW)
            img.putpixel((x, y1), YELLOW)

        for y in range(y0, y1 + 1):
            img.putpixel((x0, y), YELLOW)
            img.putpixel((x1, y), YELLOW)

    screen.fill("black")
    screen.blit(pygame.image.fromstring(img.tobytes(), img.size, img.mode), (0, 0))
    pygame.display.flip()


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


def pair_key(p1, p2):
    return min(p1, p2), max(p1, p2)


def distance(a, b):
    da = a[0] - b[0]
    db = a[1] - b[1]
    return da * da + db * db


def scale(p):
    return (p[0] // SCALE, p[1] // SCALE)


if __name__ == "__main__":
    main()
