import sys

shapes = {
    "A": 1,
    "B": 2,
    "C": 3,
}


def stronger_than(throw):
    win = ord(throw) + 1
    if win > ord("C"):
        win = ord("A")
    return chr(win)


def weaker_than(throw):
    lose = ord(throw) - 1
    if lose < ord("A"):
        lose = ord("C")
    return chr(lose)


assert stronger_than("A") == "B"
assert stronger_than("B") == "C"
assert stronger_than("C") == "A"
assert weaker_than("A") == "C"
assert weaker_than("B") == "A"
assert weaker_than("C") == "B"

my_score = 0
for line in sys.stdin.readlines():
    opp, action = line.strip().split(" ")

    me = None
    if action == "X":
        # need to lose
        me = weaker_than(opp)
    elif action == "Y":
        # need to draw
        me = opp
    else:
        # need to win
        me = stronger_than(opp)

    my_score += shapes[me]

    if me == opp:
        my_score += 3
    elif stronger_than(opp) == me:
        my_score += 6

print(f"my score {my_score}")
