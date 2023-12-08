import sys
from collections import defaultdict


def _tree():
    return defaultdict(_tree)


tree = _tree()

pwd = []
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
        return n["_size"]
    total = 0
    for k in n.keys():
        total += walk_tree(n[k], p=p + "/" + k)
    du[p] = total
    return total


walk_tree(tree, p="")
_max = max(du.values())
disk_space = 70000000
disk_used = disk_space - _max
required = 30000000
to_free = required - disk_used
_min = sys.maxsize
for k, v in du.items():
    if v > to_free:
        _min = min(_min, v)
print(_min)
