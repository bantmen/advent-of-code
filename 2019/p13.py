# https://adventofcode.com/2019/day/13

from intcode import Intcode, read_program
import curses
import time


SLOW_PLAY = True

EMPTY, WALL, BLOCK, HORIZONTAL_PADDLE, BALL = range(5)
SCORE_XY = (-1, 0)
PADDLE_LEFT, PADDLE_NEUTRAL, PADDLE_RIGHT = -1, 0, 1


def batch(iterable, size):
    l = []
    for i in iterable:
        l.append(i)
        if len(l) == size:
            yield l
            l = []


def get_game(play_for_free=False):
    l = read_program("13.txt")
    # Memory address 0 represents the number of quarters that have been inserted;
    # set it to 2 to play for free.
    if play_for_free:
        l[0] = 2
    return Intcode(l)


num_block = 0
max_x, max_y = 0, 0
for out in batch(get_game().run_program(), size=3):
    x, y, tile = out
    num_block += int(tile == BLOCK)
    max_x, max_y = max(max_x, x), max(max_y, y)
print("1) Answer:", num_block)  # 329


class Grid:
    """Remember that, the coordinates are in x-y while
    grid indices are height, width i.e. (col, row).
    This means, (col, row) == (x, y).
    """

    def __init__(self, cols, rows):
        self.l = [["?"] * cols for _ in range(rows)]
        self.sym = {EMPTY: " ", WALL: "◾", BLOCK: "□", HORIZONTAL_PADDLE: "━", BALL: "◯"}
        self.ball_coord = None
        self.prev_ball_coord = None
        self.paddle_coord = None
        self.score = 0
        self.score_countdown = 3

    def __setitem__(self, key, val):
        col, row = key

        if (col, row) == SCORE_XY:
            self.score_countdown -= 1
            if self.score_countdown == 0:
                self.score = val
                self.score_countdown = 3
            return

        self.l[row][col] = self.sym[val]
        if val == BALL:
            self.ball_coord, self.prev_ball_coord = (col, row), self.ball_coord
        elif val == HORIZONTAL_PADDLE:
            self.paddle_coord = (col, row)

    def is_ready(self):
        return self.l[-1][-1] != "?" and self.prev_ball_coord

    def get_paddle_direction(self):
        if not self.is_ready():
            return PADDLE_NEUTRAL

        if self.ball_coord[0] < self.prev_ball_coord[0]:
            # Going left
            ball_dir = -1
        else:
            # Going right
            ball_dir = 1

        dist_down = self.paddle_coord[1] - self.ball_coord[1] - 1
        forecast_x = self.ball_coord[0] + ball_dir * dist_down
        if forecast_x > self.paddle_coord[0]:
            return PADDLE_RIGHT
        elif forecast_x < self.paddle_coord[0]:
            return PADDLE_LEFT
        return PADDLE_NEUTRAL

    def __str__(self):
        s = f"Score: {self.score}\n\n"
        for row in self.l:
            s += " ".join(c for c in row) + "\n"
        return s

    def __repr__(self):
        return str(self)


grid = Grid(cols=max_x + 1, rows=max_y + 1)

stdscr = curses.initscr()
curses.noecho()
curses.cbreak()

score_countdown = 3
intcode = get_game(play_for_free=True)
intcode.inputs = [0]
try:
    for out in batch(intcode.run_program(), size=3):
        x, y, tile = out
        grid[x, y] = tile
        intcode.inputs = [grid.get_paddle_direction()]

        if SLOW_PLAY:
            if grid.is_ready():
                time.sleep(0.01)
            else:
                time.sleep(0.001)

        stdscr.addstr(0, 0, str(grid))
        stdscr.refresh()
finally:
    curses.echo()
    curses.nocbreak()
    curses.endwin()

print("2) Answer:", grid.score)  # 15973
