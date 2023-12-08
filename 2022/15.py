import sys
from collections import namedtuple, defaultdict

point = namedtuple('point', 'x y')


def manhattan_distance(a, b):
    return abs(a.x - b.x) + abs(a.y - b.y)


def around(p: point, d: int, target_y: int):
    if not (p.y - d <= target_y <= p.y + d + 1):
        return

    for x in range(p.x - d, p.x + d + 1):
        p2 = point(x, target_y)
        if manhattan_distance(p, p2) <= d:
            yield point(x=x, y=target_y)


def solve_silver(pairs, beacons, sensors):
    # target_y = 10
    target_y = 2000000
    coverage = set()
    for s, b in pairs:
        distance = manhattan_distance(s, b)
        print(f'processing pair sensor={s} beacon={b} {distance=}')
        for p in around(s, distance, target_y=target_y):
            if p not in beacons and p not in sensors:
                coverage.add(p)

    silver = set()
    for p in coverage:
        if p.y == target_y:
            silver.add(p)
    print('silver:', len(silver))


def solve_gold(pairs):
    min_x, min_y = 0, 0
    max_x, max_y = 4000000, 4000000
    # max_x, max_y = 20, 20

    ranges_to_skip = defaultdict(list)  # inclusive ranges
    intermediate_count = 0
    for s, b in pairs:
        d = manhattan_distance(s, b)

        # top side including the wide lane
        """
         d = 2
            #  
           ### 
          #####
           ###
            #  
        """
        print(f'{s=} {d=}')
        step = 0
        for y in reversed(range(s.y - d, s.y + 1)):
            if not min_y <= y <= max_y:
                continue

            lx = s.x - d + 1 * step
            rx = s.x + d - 1 * step

            ranges_to_skip[y].append([max(lx, min_x), min(rx, max_x)])  # inclusive
            step += 1
            intermediate_count += 1

        # down side excluding wide lane
        """
         d = 2
           ###
            #
        """
        step = 1
        for i, y in enumerate(range(s.y + 1, s.y + d + 1), start=0):
            if not min_y <= y <= max_y:
                continue

            lx = s.x - d + 1 * step
            rx = s.x + d - 1 * step

            ranges_to_skip[y].append([max(lx, min_x), min(rx, max_x)])  # inclusive
            step += 1
            intermediate_count += 1

    print("merging ranges...")
    final_ranges = dict()
    final_count = 0
    for y, ranges in ranges_to_skip.items():
        ranges = list(sorted(ranges, key=lambda r: r[0]))
        i = 0
        while True:
            if i == len(ranges) - 1:
                break
            r1 = ranges[i]
            r2 = ranges[i + 1]
            if r2[0] <= r1[1] or r2[0] - r1[1] == 1:
                r1[1] = max(r2[1], r1[1])
                del ranges[i + 1]
                continue
            i += 1

        final_ranges[y] = ranges
        final_count += len(final_ranges[y])

    for y, ranges in final_ranges.items():
        if len(ranges) != 1:
            print(f'{y=} {ranges=}')
            assert len(ranges) == 2
            result_x = ranges[0][1] + 1
            freq = result_x * 4000000 + y
            print(f'gold = {freq}')


def main():
    beacons = set()
    sensors = set()
    pairs = []
    for line in sys.stdin.readlines():
        sensor, beacon = line.split(':')
        sensor_x = int(sensor.split(',')[0].split('=')[-1])
        sensor_y = int(sensor.split(',')[1].split('=')[-1])
        beacon_x = int(beacon.split(',')[0].split('=')[-1])
        beacon_y = int(beacon.split(',')[1].split('=')[-1])
        beacon = point(beacon_x, beacon_y)
        sensor = point(sensor_x, sensor_y)
        pairs.append((sensor, beacon))
        beacons.add(beacon)
        sensors.add(sensor)

    solve_silver(pairs, beacons, sensors)
    solve_gold(pairs)


if __name__ == '__main__':
    main()
