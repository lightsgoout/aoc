import sys

MARKER_SIZE = 14


def get_marker(line):
    r = 0
    for i, c in enumerate(line):
        if len(set(line[i : i + MARKER_SIZE])) == MARKER_SIZE:
            r = i + MARKER_SIZE
            break
    return r


assert get_marker("mjqjpqmgbljsphdztnvjfqwrcgsmlb") == 19
assert get_marker("bvwbjplbgvbhsrlpgdmjqwftvncz") == 23
assert get_marker("nppdvjthqldpwncqszvftbrmjlhg") == 23
assert get_marker("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg") == 29
assert get_marker("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw") == 26

result = get_marker(sys.stdin.read().strip())
print(result)
