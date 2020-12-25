from copy import deepcopy
import itertools


s = """L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL"""

s = open("day11.txt").read()

EMPTY, TAKEN, FLOOR = "L", "#", "."

orig_grid = [list(line) for line in s.split("\n")]


def adj(grid, i, j):
    for di, dj in itertools.product(range(-1, 2), repeat=2):
        if di == dj == 0:
            continue
        i2, j2 = i + di, j + dj
        if 0 <= i2 < len(grid) and 0 <= j2 < len(grid[0]):
            yield grid[i2][j2]


def adj2(grid, i, j):
    for di, dj in itertools.product(range(-1, 2), repeat=2):
        if di == dj == 0:
            continue
        i2, j2 = i + di, j + dj
        while 0 <= i2 < len(grid) and 0 <= j2 < len(grid[0]) and grid[i2][j2] == FLOOR:
            i2 += di
            j2 += dj
        if 0 <= i2 < len(grid) and 0 <= j2 < len(grid[0]):
            yield grid[i2][j2]


def transform(grid, old_rules=True):
    adj_func = adj if old_rules else adj2
    taken_threshold = 4 if old_rules else 5

    grid2 = deepcopy(grid)
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            adjacent = list(adj_func(grid, i, j))
            num_adj_taken = adjacent.count(TAKEN)
            if grid[i][j] == EMPTY and num_adj_taken == 0:
                grid2[i][j] = TAKEN
            if grid[i][j] == TAKEN and num_adj_taken >= taken_threshold:
                grid2[i][j] = EMPTY
    return grid2, grid == grid2


grid = deepcopy(orig_grid)
while True:
    grid, no_change = transform(grid)
    if no_change:
        print("Ans 1)", sum(row.count(TAKEN) for row in grid))
        break

grid = deepcopy(orig_grid)
while True:
    grid, no_change = transform(grid, old_rules=False)
    if no_change:
        print("Ans 2)", sum(row.count(TAKEN) for row in grid))
        break
