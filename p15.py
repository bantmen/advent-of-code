# https://adventofcode.com/2019/day/15

from intcode import Intcode, read_program
import curses
from collections import defaultdict


N, S, W, E = range(1, 5)
delta_dir = {(0, 1): N, (0, -1): S, (1, 0): W, (-1, 0): E}

WALL_STATUS, SUCCESS_STATUS, OXYGEN_STATUS = range(3)


def apply_delta(coord, delta):
    return coord[0] + delta[0], coord[1] + delta[1]


def opposite_delta(delta):
    return -delta[0], -delta[1]


coord = (0, 0)
grid = {coord: SUCCESS_STATUS}
dest_coords = []


def add_new_coords():
    for delta in delta_dir:
        c = apply_delta(coord, delta)
        if c not in grid:
            dest_coords.append(c)


add_new_coords()


def sign(x):
    if x > 0:
        return 1
    elif x < 0:
        return -1
    return 0


def get_deltas(from_c, to_c):
    diff_c = to_c[0] - from_c[0], to_c[1] - from_c[1]
    for _ in range(abs(diff_c[0])):
        yield sign(diff_c[0]), 0
    for _ in range(abs(diff_c[1])):
        yield 0, sign(diff_c[1])


# stdscr = curses.initscr()
# curses.noecho()
# curses.cbreak()


def render_sparse_grid(grid, coord, to_coord):
    min_x = min(t[0] for t in grid)
    max_x = max(t[0] for t in grid)
    min_y = min(t[1] for t in grid)
    max_y = max(t[1] for t in grid)

    num_cols = max_x - min_x + 1
    num_rows = max_y - min_y + 1

    l = [[" "] * num_cols for _ in range(num_rows)]
    for (x, y), v in grid.items():
        if (x, y) == coord:
            v = "D"
        elif v == WALL_STATUS:
            v = "#"
        elif v == SUCCESS_STATUS:
            v = "."
        elif v == OXYGEN_STATUS:
            v = "O"
        else:
            assert False
        x, y = x - min_x, y - min_y
        l[y][x] = v
    # s = f"Current coord: {coord}, To coord: {to_coord}, Remaining: {len(dest_coords)}\n\n"
    for row in l:
        print(" ".join(c for c in row))
        # s += " ".join(c for c in row) + "\n"
    # print(s)
    # stdscr.addstr(0, 0, s)
    # stdscr.refresh()


intcode = Intcode(read_program("15.txt"))
it = intcode.run_program()

remaining_deltas = defaultdict(lambda: list(delta_dir.keys()).copy())
min_steps = defaultdict(lambda: float("inf"))


def travel(coord, steps=0):
    deltas = remaining_deltas[coord]

    m = min(min_steps[coord], steps)
    for delta in delta_dir:
        m = min(m, min_steps[apply_delta(coord, delta)] + 1)
    min_steps[coord] = m

    while len(deltas) > 0:
        delta = deltas.pop()
        new_coord = apply_delta(coord, delta)
        intcode.inputs.append(delta_dir[delta])
        status = next(it)
        grid[new_coord] = status
        if status != WALL_STATUS:
            travel(new_coord, steps=steps + 1)
            intcode.inputs.append(delta_dir[opposite_delta(delta)])
            assert next(it) != WALL_STATUS


travel(coord)

render_sparse_grid(grid, coord, (-1, -1))

oxygen_coord = None
for k, v in grid.items():
    if v == OXYGEN_STATUS:
        oxygen_coord = k
        break

print(min_steps[oxygen_coord])
