from itertools import product


s = """.#.
..#
###"""

s = open("day17.txt").read()

l = s.split("\n")

ACTIVE, INACTIVE = "#", "."


def neighbors(xyz):
    x, y, z, w = xyz
    for dx, dy, dz in product(range(-1, 2), repeat=3):
        if dx == dy == dz == 0:
            continue
        yield x + dx, y + dy, z + dz, w


def neighbors2(xyz):
    x, y, z, w = xyz
    for dx, dy, dz, dw in product(range(-1, 2), repeat=4):
        if dx == dy == dz == dw == 0:
            continue
        yield x + dx, y + dy, z + dz, w + dw


input_actives = set()

z = w = 0
for y, row in enumerate(l):
    for x, state in enumerate(row):
        if state == ACTIVE:
            input_actives.add((x, y, z, w))


def transform(actives, neighbors):
    actives2 = set(actives)
    seen = set()
    for xyz in actives:
        active_count = 0
        for xyz2 in neighbors(xyz):
            # Rule 1
            if xyz2 in actives:
                active_count += 1
            # Rule 2
            elif xyz2 not in seen:
                active_count2 = 0
                for xyz3 in neighbors(xyz2):
                    if xyz3 in actives:
                        active_count2 += 1
                if active_count2 == 3:
                    actives2.add(xyz2)
                seen.add(xyz2)
        if active_count not in (2, 3):
            actives2.remove(xyz)
    return actives2


actives = set(input_actives)
for _ in range(6):
    actives = transform(actives, neighbors)

print("Ans 1)", len(actives))

actives = set(input_actives)
for _ in range(6):
    actives = transform(actives, neighbors2)

print("Ans 2)", len(actives))
