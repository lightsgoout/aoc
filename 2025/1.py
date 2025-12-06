import sys


class D:
    def __init__(self):
        self.value = 50
        self.max_value = 100

        self.silver = 0
        self.gold = 0

    def run(self, line: str):
        left = line.startswith("L")
        clicks = int(line[1:])

        full_rot = clicks // self.max_value
        self.gold += full_rot

        last_rot = clicks % self.max_value
        if last_rot > 0:
            if left and self.value - last_rot <= 0 and self.value != 0:
                self.gold += 1
            elif (
                not left
                and self.value + last_rot >= self.max_value
                and self.value != self.max_value
            ):
                self.gold += 1

        if left:
            self.value -= clicks
        else:
            self.value += clicks

        self.value = self.value % self.max_value
        if self.value == 0:
            self.silver += 1


test = D()
test.run("L1000")
assert test.gold == 10 and test.value == 50


test.run("R1000")
assert test.gold == 20 and test.value == 50


def main():
    d = D()
    for line in sys.stdin.readlines():
        line = line.strip()
        if not line:
            continue

        d.run(line)

    print("silver:", d.silver)
    print("gold:", d.gold)


if __name__ == "__main__":
    main()
