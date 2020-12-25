# https://adventofcode.com/2020/day/1

s = open("day1.txt").read()

l = [int(x) for x in s.split("\n")]

d = set(l)

for x in l:
    if 2020 - x in d:
        print(x * (2020 - x))

for i, x in enumerate(l):
    while i + 1 < len(l):
        y = l[i + 1]
        if 2020 - x - y in d:
            print(x * y * (2020 - x - y))
        i += 1
