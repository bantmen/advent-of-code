s = """..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#"""

s = open("day3.txt").read()

l = s.split("\n")

max_x = len(l[0])
max_y = len(l)

x, y = 0, 0

num_trees = 0

while y + 1 < max_y:
    x = (x + 3) % max_x
    y += 1
    num_trees += int(l[y][x] == "#")

print(num_trees)

###

ans = 1

for dx, dy in [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]:
    num_trees = 0
    x, y = 0, 0
    while y + dy < max_y:
        x = (x + dx) % max_x
        y += dy
        num_trees += int(l[y][x] == "#")
    ans *= num_trees

print(ans)
