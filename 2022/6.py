import sys

MARKER_SIZE = 4


def get_marker(line):
    r = 0
    for i, c in enumerate(line):
        if len(set(line[i : i + MARKER_SIZE])) == MARKER_SIZE:
            r = i + MARKER_SIZE
            break
    return r


assert get_marker("bvwbjplbgvbhsrlpgdmjqwftvncz") == 5
assert get_marker("nppdvjthqldpwncqszvftbrmjlhg") == 6
assert get_marker("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg") == 10
assert get_marker("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw") == 11

result = get_marker(sys.stdin.read().strip())
print(result)
