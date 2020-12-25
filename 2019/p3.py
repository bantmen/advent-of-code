# https://adventofcode.com/2019/day/3

def dir_to_delta(direction):
    # Returns delta x, delta y
    num = int(direction[1:])
    if direction[0] == "U":
        return 0, num 
    if direction[0] == "D":
        return 0, -num
    if direction[0] == "R":
        return num, 0
    if direction[0] == "L":
        return -num, 0

def range_until(x):
    if x > 0:
        return range(1, x + 1, 1)
    return range(-1, x - 1, -1)

def get_wire_coords(directions):
    coords = set()
    x, y = 0, 0
    for direction in directions:
        dx, dy = dir_to_delta(direction)
        if dx != 0:
            for i in range_until(dx):
                coords.add((x + i, y))
        elif dy != 0:
            for i in range_until(dy):
                coords.add((x, y + i))
        else:
            assert False
        x, y = x + dx, y + dy
    return coords 

def get_wire_coords2(directions):
    coords = dict()
    x, y = 0, 0
    total_steps = 0
    for direction in directions:
        dx, dy = dir_to_delta(direction)
        if dx != 0:
            for i in range_until(dx):
                total_steps += 1
                coords.setdefault((x + i, y), total_steps) 
        elif dy != 0:
            for i in range_until(dy):
                total_steps += 1
                coords.setdefault((x, y + i), total_steps)
        else:
            assert False
        x, y = x + dx, y + dy
    return coords

# dirs1 = ["R75","D30","R83","U83","L12","D49","R71","U7","L72"]
# dirs2 = ["U62","R66","U55","R34","D71","R55","D58","R83"]

# dirs1 = ["R8","U5","L5","D3"]
# dirs2 = ["U7","R6","D4","L4"]

with open('3.txt', 'r') as f:
    dirs1 = f.readline().split(',')
    dirs2 = f.readline().split(',')

coords1 = get_wire_coords2(dirs1)
coords2 = get_wire_coords2(dirs2)

def manhattan_distance(x_y):
    x, y = x_y
    return abs(x) + abs(y)

def solve(coords1, coords2):
    return manhattan_distance(
        min(coords1.intersection(coords2), key=manhattan_distance))

def solve2(coords1, coords2):
    min_dist = float('inf')
    for c1 in coords1:
        if c1 in coords2:
            min_dist = min(min_dist, coords1[c1] + coords2[c1])
    return min_dist

# print("Answer:", solve(coords1, coords2))
print("Answer:", solve2(coords1, coords2))

