import math


s = """LR

AAA = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)"""

s = open("day8.txt").read()

fst, snd = s.split("\n\n")

d = {}
starting = []
for line in snd.split("\n"):
    src, dest = line.split(" = ")
    l, r = dest[1:-1].split(", ")
    d[src] = (l, r)
    if src.endswith("A"):
        starting.append(src)

def solve(start):
    i = 0
    cur = start
    while not cur.endswith("Z"):
        if fst[i % len(fst)] == "L":
            cur = d[cur][0]
        else: # "R"
            cur = d[cur][1]
        i += 1
    return i

print("Part 1)", solve("AAA"))

first_found = []
for start in starting:
    first_found.append(solve(start))

print("Part 2)", math.lcm(*first_found))
