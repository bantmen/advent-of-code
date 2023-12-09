from collections import defaultdict


s = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598.."""

s = open("day3.txt").read()

l = s.split("\n")

rows = len(l)
cols = len(l[0])

# gear coord to list of touched nums
gear_touched = defaultdict(list)

def near_symbol(row_idx, i, j, x):
    found = False
    for row in range(row_idx - 1, row_idx + 2):
        for col in range(i - 1, j + 2):
            # out of bounds
            if row < 0 or row >= rows or col < 0 or col >= cols:
                continue
            # don't check itself
            if row == row_idx and i <= col <= j:
                continue
            if l[row][col] != ".":
                found = True
            if l[row][col] == "*":
                gear_touched[(row, col)].append(x)
    return found

ans = 0

for row_idx, line in enumerate(l):
    i = None
    x = ""
    for col_idx, c in enumerate(line):
        if c.isdigit() and i is None:
            i = col_idx
            x += c
        elif c.isdigit():
            x += c
        elif x != "":
            # flush
            if near_symbol(row_idx, i, col_idx - 1, int(x)):
                ans += int(x)
            x = ""
            i = None
    if x != "":
        # flush
        if near_symbol(row_idx, i, col_idx, int(x)):
            ans += int(x)
        x = ""
        i = None

print("Part 1)", ans)

ans = 0

for coord in gear_touched:
    if len(gear_touched[coord]) == 2:
        ans += gear_touched[coord][0] * gear_touched[coord][1]

print("Part 2)", ans)
