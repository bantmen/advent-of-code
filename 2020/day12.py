from math import hypot, sin, cos, radians, atan2


s = """F10
N3
F7
R90
F11"""

s = open("day12.txt").read()

l = s.split("\n")

N, E, S, W = range(4)
delta = {N: (0, 1), E: (1, 0), S: (0, -1), W: (-1, 0)}

x, y = 0, 0
curr_dir = E

for line in l:
    cmd, val = line[0], line[1:]
    val = int(val)
    if cmd == "N":
        y += val
    elif cmd == "S":
        y -= val
    elif cmd == "E":
        x += val
    elif cmd == "W":
        x -= val
    elif cmd == "L":
        curr_dir = (curr_dir - val / 90) % 4
    elif cmd == "R":
        curr_dir = (curr_dir + val / 90) % 4
    elif cmd == "F":
        dx, dy = delta[curr_dir]
        x += val * dx
        y += val * dy
    else:
        assert False

print("Ans 1)", abs(x) + abs(y))

x, y = 0, 0
wp_x, wp_y = 10, 1
curr_dir = E


def rotate(x, y, deg):
    # Rotate point around a circle with origin at (0, 0)
    # Cartesian to Polar
    r, theta = hypot(x, y), atan2(y, x)
    # Rotate
    theta += radians(deg)
    # Polar to Cartesian
    return round(r * cos(theta)), round(r * sin(theta))


def rotate2(x, y, deg):
    rad = radians(deg)
    x2 = x * cos(rad) + y * sin(rad)
    y2 = -x * sin(rad) + y * cos(rad)
    return x2, y2


for line in l:
    cmd, val = line[0], line[1:]
    val = int(val)
    if cmd == "N":
        wp_y += val
    elif cmd == "S":
        wp_y -= val
    elif cmd == "E":
        wp_x += val
    elif cmd == "W":
        wp_x -= val
    elif cmd == "L":
        wp_x, wp_y = rotate(wp_x, wp_y, val)
    elif cmd == "R":
        wp_x, wp_y = rotate(wp_x, wp_y, -val)
    elif cmd == "F":
        x += wp_x * val
        y += wp_y * val
    else:
        assert False

print("Ans 2)", abs(x) + abs(y))
