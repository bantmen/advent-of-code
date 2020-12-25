import copy
from collections import defaultdict


s = open("day24.txt").read()

dirs = {
    "ne": (0.5, 1),
    "e": (1, 0),
    "se": (0.5, -1),
    "sw": (-0.5, -1),
    "w": (-1, 0),
    "nw": (-0.5, 1),
}

WHITE, BLACK = False, True
# Optimization: Only store BLACK
grid = defaultdict(lambda: WHITE)


def to_coord(d):
    x, y, = (
        0,
        0,
    )
    for direction, count in d.items():
        dx, dy = dirs[direction]
        x, y = x + count * dx, y + count * dy
    return x, y


for line in s.split("\n"):
    i = 0
    x, y = 0, 0
    while i < len(line):
        if line[i] in dirs:
            dx, dy = dirs[line[i]]
            i += 1
        else:
            dx, dy = dirs[line[i : i + 2]]
            i += 2
        x, y = x + dx, y + dy
    grid[(x, y)] = not grid[(x, y)]

# 424
print("Ans 1)", sum(map(int, grid.values())))


def neighbors(coord):
    for dx, dy in dirs.values():
        yield coord[0] + dx, coord[1] + dy


def change_color(coord, color, grid):
    num_black = 0
    for coord2 in neighbors(coord):
        if coord2 in grid and grid[coord2] == BLACK:
            num_black += 1
    if color == BLACK and (num_black == 0 or num_black > 2):
        return WHITE
    elif color == WHITE and num_black == 2:
        return BLACK
    return None


def transform(grid):
    new_grid = copy.deepcopy(grid)
    seen = set()
    for coord, color in grid.items():
        new_color = change_color(coord, color, grid)
        if new_color is not None:
            new_grid[coord] = new_color
        for coord2 in neighbors(coord):
            if coord2 in seen:
                continue
            seen.add(coord2)
            color2 = grid[coord2] if coord2 in grid else WHITE
            new_color = change_color(coord2, color2, grid)
            if new_color is not None:
                new_grid[coord2] = new_color
    return new_grid


for _ in range(100):
    grid = transform(grid)

# 3737
print("Ans 2)", sum(map(int, grid.values())))
