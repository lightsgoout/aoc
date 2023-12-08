import operator
import sys
from functools import reduce


def compare_pair(left, right, indent=0):
    tab = " " * indent
    print(f"{tab} - Compare {left} vs {right}")

    if isinstance(left, int) and isinstance(right, int):
        if left == right:
            return None
        if left < right:
            print(f"{tab} - Left side is smaller, so inputs are in the right order")
            return True
        else:
            print(f"{tab} - Right side is smaller, so inputs are not in the right order")
            return False

    if isinstance(left, int) and not isinstance(right, int):
        left = [left]
        print(f"{tab} - Mixed types; convert left to {left} and retry comparison")
        return compare_pair(left, right, indent + 2)
    elif isinstance(right, int) and not isinstance(left, int):
        right = [right]
        print(f"{tab} - Mixed types; convert right to {right} and retry comparison")
        return compare_pair(left, right, indent + 2)

    assert isinstance(left, list)
    assert isinstance(right, list)

    result = None
    for i, l in enumerate(left):
        try:
            r = right[i]
        except IndexError:
            print(f"{tab} - Right side ran out of items, so inputs are not in the right order")
            return False

        result = compare_pair(l, r, indent + 2)
        if result is None:
            continue

        return result

    if len(left) < len(right):
        print(f"{tab} - Left side ran out of items, so inputs are in the right order ({left=} {right=})")
        return True

    return result


assert compare_pair([1, 1, 3, 1, 1], [1, 1, 5, 1, 1]) == True
assert compare_pair([[1], [2, 3, 4]], [[1], 4]) == True
assert compare_pair([9], [[8, 7, 6]]) == False
assert compare_pair([[4, 4], 4, 4], [[4, 4], 4, 4, 4]) == True
assert compare_pair([7, 7, 7, 7], [7, 7, 7]) == False
assert compare_pair([], [3]) == True
assert compare_pair([[[]]], [[]]) == False
assert compare_pair([1, [2, [3, [4, [5, 6, 7]]]], 8, 9], [1, [2, [3, [4, [5, 6, 0]]]], 8, 9]) == False


def bubble_sort(arr):
    n = len(arr)
    swapped = False
    for i in range(n - 1):
        for j in range(0, n - i - 1):
            comp = compare_pair(arr[j + 1], arr[j])
            assert isinstance(comp, bool)
            if comp:
                swapped = True
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
        if not swapped:
            return


def main():
    decoder_packets = [
        [[2]],
        [[6]],
    ]

    lines = list(sys.stdin.read().split("\n\n"))
    pairs = []
    for l in lines:
        p = l.split("\n")
        pairs.append(eval(p[0]))
        pairs.append(eval(p[1]))

    for dec in decoder_packets:
        pairs.append(dec)

    bubble_sort(pairs)

    result = []
    for idx, p in enumerate(pairs, start=1):
        if p in decoder_packets:
            result.append(idx)

    print(reduce(operator.mul, result))


if __name__ == "__main__":
    main()
