from collections import defaultdict

import aoc


def silver(lines):
    r = 0
    before = defaultdict(set)
    for line in lines:
        if "|" in line:
            a, b = line.split("|")
            before[a].add(b)

        if "," in line:
            pages = line.split(",")
            visited = set()
            valid = True
            for p in pages:
                for v in visited:
                    if v in before.get(p, set()):
                        valid = False
                visited.add(p)

            if valid:
                middle = pages[len(pages) // 2]
                r += int(middle)

    return r


def gold(lines):
    r = 0
    before = defaultdict(set)
    for line in lines:
        if "|" in line:
            a, b = line.split("|")
            before[a].add(b)

        if "," in line:
            pages = line.split(",")
            visited = set()
            valid = True
            for p in pages:
                for v in visited:
                    if v in before.get(p, set()):
                        valid = False
                visited.add(p)

            if not valid:
                build = [pages[0]]
                for p in pages[1:]:
                    min_i = 999999999
                    for v in before.get(p, set()):
                        try:
                            lim = build.index(v)
                        except ValueError:
                            lim = -1

                        if lim != -1:
                            min_i = min(min_i, lim)

                    if min_i > len(build):
                        build.append(p)
                    else:
                        build.insert(min_i, p)

                middle = build[len(build) // 2]
                r += int(middle)
    return r


def main():
    print("silver:", silver(aoc.stdin()))
    print("gold:", gold(aoc.stdin()))


if __name__ == "__main__":
    main()
