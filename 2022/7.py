import sys
from collections import defaultdict

pwd = []


def _tree():
    return defaultdict(_tree)


tree = _tree()
for line in sys.stdin.readlines():
    line = line.strip()
    if line.startswith("$"):
        _, cmd, *args = line.split()
        if cmd == "cd":
            assert len(args) == 1
            cd = args[0]
            if cd == "..":
                pwd.pop()
            elif cd == "/":
                pwd = ["/"]
            else:
                pwd.append(cd)
        elif cmd == "ls":
            pass
    else:
        node = tree
        for path in pwd:
            node = node[path]
        size, name = line.split()
        if size != "dir":
            node[name]["_size"] = int(size)

du = {}


def walk_tree(n: dict, p: str) -> int:
    if "_size" in n.keys():
        # leaf node
        return n["_size"]

    total = 0
    for k in n.keys():
        total += walk_tree(n[k], p=p + "/" + k)
    du[p] = total
    return total


walk_tree(tree, p="/")

print(sum((v for v in du.values() if v <= 100000)))
