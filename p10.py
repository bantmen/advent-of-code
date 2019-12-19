# https://adventofcode.com/2019/day/10

from math import atan2, hypot, pi, degrees, sin, cos
from collections import defaultdict
import numpy as np


with open("10.txt", "r") as f:
    s = f.read()


def asteroid_coords(s):
    l = []
    y = 0
    for line in s.split("\n"):
        x = 0
        for char in line:
            if char == "#":
                l.append((x, y))
            x += 1
        y += 1
    return l


def rotate(x, y, radians):
    x2 = x * cos(radians) + y * sin(radians)
    y2 = -x * sin(radians) + y * cos(radians)
    return x2, y2


def clockwise_angle(c1, c2):
    x, y = c2[0] - c1[0], c2[1] - c1[1]
    # After the rotation, atan2 turn angles become clockwise
    # i.e. they go from 0 to 360 in a clockwise manner.
    x, y = rotate(x, y, -pi / 2)
    a = degrees(atan2(y, x)) % 360
    if np.isclose(a, 360):
        return 0
    return a


# Check the axis around (1, 1) to confirm the clockwise degrees.
assert np.isclose(clockwise_angle((1, 1), (1, 1)), 0)
assert np.isclose(clockwise_angle((1, 1), (1, 0)), 0)
assert np.isclose(clockwise_angle((1, 1), (2, 1)), 90)
assert np.isclose(clockwise_angle((1, 1), (1, 2)), 180)
assert np.isclose(clockwise_angle((1, 1), (0, 1)), 270)


def distance_sort(c1, coords):
    return sorted(coords, key=lambda c2: hypot(c2[0] - c1[0], c2[1] - c1[1]))


coords = asteroid_coords(s)
ans = float("-inf")
coord = None
for c1 in coords:
    d = {}
    for c2 in coords:
        if c1 != c2:
            d[clockwise_angle(c1, c2)] = 1
    if len(d) > ans:
        ans = len(d)
        coord = c1
print("1) Answer:", ans)

c1 = coord
d = defaultdict(lambda: list())
for c2 in coords:
    if c1 != c2:
        d[clockwise_angle(c1, c2)].append(c2)
for a in d:
    # To hit the closer asteroids first
    d[a] = distance_sort(c1, d[a])
hit_count = 0
wanted_count = 200
ans_coord = None
# Traverse clockwise
angles = sorted(d)
while hit_count != wanted_count:
    for a in angles:
        if len(d[a]) == 0:
            continue
        hit_count += 1
        hit = d[a].pop(0)
        if hit_count == wanted_count:
            ans_coord = hit
            break
print("2) Answer:", 100 * ans_coord[0] + ans_coord[1])
