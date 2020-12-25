from collections import namedtuple
import re
from itertools import product
import numpy as np
from functools import reduce


# 144 tiles
s = open("day20.txt").read()

Tile = namedtuple("Tile", ["id", "up", "down", "left", "right", "raw"])

Tile.__eq__ = lambda tile1, tile2: tile1.id == tile2.id

Tile.__hash__ = lambda self: self.id

pattern = re.compile(r"Tile (\d+):")


def get_tile(tile_chunk):
    preamble, *tile = tile_chunk.split("\n")
    return Tile(
        id=int(pattern.match(preamble).group(1)),
        up=list(tile[0]),
        down=list(tile[-1]),
        left=[tile[i][0] for i in range(len(tile))],
        right=[tile[i][-1] for i in range(len(tile))],
        raw=tile,
    )


def rotate(tile):
    raw = list(
        map(
            lambda l: "".join(l),
            np.rot90(np.char.array([list(row) for row in tile.raw]), k=-1).tolist(),
        )
    )
    return Tile(
        id=tile.id,
        up=list(reversed(tile.left)),
        right=list((tile.up)),
        down=list(reversed(tile.right)),
        left=list((tile.down)),
        raw=raw,
    )


def flip(tile):
    raw = list(
        map(
            lambda l: "".join(l),
            np.fliplr(np.char.array([list(row) for row in tile.raw])).tolist(),
        )
    )
    return Tile(
        id=tile.id,
        up=list(reversed(tile.up)),
        down=list(reversed(tile.down)),
        left=list(tile.right),
        right=list(tile.left),
        raw=raw,
    )


def transforms(tile_in):
    for num_flip in range(2):  # none or once
        for num_rotate in range(4):  # none or up to 3 times
            tile = tile_in
            for _ in range(num_flip):
                tile = flip(tile)
            for _ in range(num_rotate):
                tile = rotate(tile)
            yield tile


class Board:
    def __init__(self, side_length):
        print("side_length", side_length)
        # Edges are (0, 0), (0, side_length-1), (side_length-1, 0), (side_length-1, side_length-1)
        self.grid = [[None for _ in range(side_length)] for _ in range(side_length)]
        self.empty_coords = set(product(range(side_length), repeat=2))

    # True if can add, False otherwise
    def add(self, row, col, tile):
        if self.grid[row][col] is not None:
            return False
        ###
        # Up
        row2, col2 = row - 1, col
        if self._tile_exists(row2, col2) and not self.grid[row2][col2].down == tile.up:
            return False
        # Right
        row2, col2 = row, col + 1
        if (
            self._tile_exists(row2, col2)
            and not self.grid[row2][col2].left == tile.right
        ):
            return False
        # Down
        row2, col2 = row + 1, col
        if self._tile_exists(row2, col2) and not self.grid[row2][col2].up == tile.down:
            return False
        # Left
        row2, col2 = row, col - 1
        if (
            self._tile_exists(row2, col2)
            and not self.grid[row2][col2].right == tile.left
        ):
            return False
        ###
        self.grid[row][col] = tile
        self.empty_coords.remove((row, col))
        return True

    def remove(self, row, col):
        assert self.grid[row][col] is not None
        self.grid[row][col] = None
        self.empty_coords.add((row, col))

    def _tile_exists(self, row, col):
        return (
            0 <= row < len(self.grid)
            and 0 <= col < len(self.grid[0])
            and self.grid[row][col] is not None
        )


tiles = []
for lines in s.split("\n\n"):
    tiles.append(get_tile(lines))


def unmatched_directions(t1):
    d = {"up": True, "right": True, "down": True, "left": True}
    for tile2 in tiles:
        if tile.id == tile2.id:
            continue
        for t2 in transforms(tile2):
            if t1.up == t2.down:
                d["up"] = False
            if t1.right == t2.left:
                d["right"] = False
            if t1.down == t2.up:
                d["down"] = False
            if t1.left == t2.right:
                d["left"] = False
    return d


side_length = int(len(tiles) ** 0.5)

b = Board(side_length)

tile_ids = {tile.id for tile in tiles}

top_left, top_right, bottom_left, bottom_right = [], [], [], []
tops, bottoms, lefts, rights = [], [], [], []
rest = []

for tile in tiles:
    for t in transforms(tile):
        directions = unmatched_directions(t)
        if directions["up"]:
            tops.append(t)
            if directions["left"]:
                top_left.append(t)
            if directions["right"]:
                top_right.append(t)
        if directions["down"]:
            bottoms.append(t)
            if directions["left"]:
                bottom_left.append(t)
            if directions["right"]:
                bottom_right.append(t)
        if directions["left"]:
            lefts.append(t)
        if directions["right"]:
            rights.append(t)
        if not any(directions.values()):
            rest.append(t)


def solve(tile_ids):
    if len(tile_ids) == 0:
        return True
    for row, col in product(range(side_length), repeat=2):
        candidates = rest
        if (row, col) == (0, 0):
            # top left
            candidates = top_left
        elif (row, col) == (0, side_length - 1):
            # top right
            candidates = top_right
        elif (row, col) == (side_length - 1, 0):
            # bottom left
            candidates = bottom_left
        elif (row, col) == (side_length - 1, side_length - 1):
            # bottom right
            candidates = bottom_right
        elif row == 0:
            # Edge up
            candidates = tops
        elif row == side_length - 1:
            # Edge down
            candidates = bottoms
        elif col == 0:
            # Edge left
            candidates = lefts
        elif col == side_length - 1:
            # Edge right
            candidates = rights
        for t in candidates:
            if t.id in tile_ids:
                tile_ids.remove(t.id)
                if b.add(row, col, t):
                    if solve(tile_ids):
                        return True
                    b.remove(row, col)
                tile_ids.add(t.id)
    return False


assert solve(tile_ids)
# 54755174472007
print(
    "Ans 1)",
    b.grid[0][0].id
    * b.grid[0][side_length - 1].id
    * b.grid[side_length - 1][0].id
    * b.grid[side_length - 1][side_length - 1].id,
)


def remove_borders(tile_raw):
    ret = []
    for i, row in enumerate(tile_raw):
        if i == 0 or i == len(tile_raw) - 1:
            # Top and bottom borders: skip first and last rows
            continue
        # Left and right borders: skip the first and last character of each row
        ret.append(row[1 : len(row) - 1])
    return ret


def stack_columns(tile_raws):
    return ["".join(l) for l in zip(*tile_raws)]


def stack_rows(tile_raws):
    return reduce(lambda a, b: a + b, tile_raws)


pic = stack_rows(
    [stack_columns(map(lambda tile: remove_borders(tile.raw), row)) for row in b.grid]
)

arr = np.char.array([list(row) for row in pic])


def transforms2(arr):
    arr_in = arr
    for num_flip in range(2):  # none or once
        for num_rotate in range(4):  # none or up to 3 times
            arr = arr_in
            for _ in range(num_flip):
                arr = np.fliplr(arr)
            for _ in range(num_rotate):
                arr = np.rot90(arr)
            yield arr


def num_patterns(arr):
    coords = [
        (0, 18),
        (1, 0),
        (1, 5),
        (1, 6),
        (1, 11),
        (1, 12),
        (1, 17),
        (1, 18),
        (1, 19),
        (2, 1),
        (2, 4),
        (2, 7),
        (2, 10),
        (2, 13),
        (2, 16),
    ]
    nr, nc = arr.shape
    count = 0
    for row, col in product(range(nr), range(nc)):
        if row + 3 < nr and col + 20 < nc:
            if all(arr[row + r][col + c] == "#" for r, c in coords):
                count += 1
    return count


ma = float("-inf")

for i, a in enumerate(transforms2(arr)):
    ma = max(ma, num_patterns(a))

# 1692
print("Ans 2)", (arr == "#").sum() - 15 * ma)
