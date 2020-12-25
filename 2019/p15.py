# https://adventofcode.com/2019/day/15

from intcode import Intcode, read_program
from collections import defaultdict
from math import isinf


N, S, W, E = range(1, 5)

WALL_STATUS, SUCCESS_STATUS, OXYGEN_STATUS = range(3)

START_COORD = (0, 0)

VISUALIZE = False


def apply_delta(coord, delta):
    return coord[0] + delta[0], coord[1] + delta[1]


def opposite_delta(delta):
    return -delta[0], -delta[1]


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


def render_sparse_grid(grid, coord):
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
    for row in l:
        print(" ".join(c for c in row))


class FoundOxygenException(Exception):
    pass


class Traversal:
    def __init__(self, intcode):
        self.intcode = intcode
        self.it = intcode.run_program()
        self.coord = START_COORD

        self.delta_to_dir = {(0, 1): N, (0, -1): S, (1, 0): W, (-1, 0): E}

    def explore(self, stop_at_oxygen=False):
        self.grid = {self.coord: SUCCESS_STATUS}
        self.remaining_deltas = defaultdict(lambda: list(self.delta_to_dir.keys()).copy())
        self.min_steps = defaultdict(lambda: float("inf"))

        try:
            self.travel(self.coord, stop_at_oxygen)
        except FoundOxygenException:
            pass

    def travel(self, coord, stop_at_oxygen, steps=0):
        self.coord = coord

        m = min(self.min_steps[coord], steps)
        for delta in self.delta_to_dir:
            m = min(m, self.min_steps[apply_delta(coord, delta)] + 1)
        self.min_steps[coord] = m

        deltas = self.remaining_deltas[coord]
        while len(deltas) > 0:
            delta = deltas.pop()
            new_coord = apply_delta(coord, delta)
            self.intcode.inputs.append(self.delta_to_dir[delta])
            status = next(self.it)

            if status == OXYGEN_STATUS and stop_at_oxygen:
                # Easy way to escape recursion
                raise FoundOxygenException()

            self.grid[new_coord] = status
            if status != WALL_STATUS:
                self.travel(new_coord, steps=steps + 1, stop_at_oxygen=stop_at_oxygen)
                # Since this path is traversed, go back and keep exploring
                self.intcode.inputs.append(self.delta_to_dir[opposite_delta(delta)])
                # Can't be a wall because we just came from here and the grid is not changing
                assert next(self.it) != WALL_STATUS


traversal = Traversal(Intcode(read_program("15.txt")))

traversal.explore()

if VISUALIZE:
    render_sparse_grid(traversal.grid, START_COORD)

oxygen_coord = None
for k, v in traversal.grid.items():
    if v == OXYGEN_STATUS:
        oxygen_coord = k
        break

print("1) Answer", traversal.min_steps[oxygen_coord])  # 280

# Reposition at the oxygen
traversal.explore(stop_at_oxygen=True)
# Explore starting from the oxygen
traversal.explore()

# Unreachable positions get +inf, filter those out to find the true max
print("2) Answer", max(filter(lambda x: not isinf(x), traversal.min_steps.values())))  # 400
