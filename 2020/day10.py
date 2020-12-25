from collections import defaultdict
import functools

s = open("day10.txt").read()

l = list(map(int, s.split("\n")))
l.append(0)
l.append(max(l) + 3)
l.sort()

differences = defaultdict(int)

current = 0

for x in l:
    differences[x - current] += 1
    current = x

print("Ans 1)", differences[1] * differences[3])


@functools.lru_cache(maxsize=None)
def num_ways(idx):
    if idx == 0:
        return 1
    ret = 0
    for idx2 in range(max(idx - 3, 0), idx):
        if l[idx] - l[idx2] <= 3:
            ret += num_ways(idx2)
    return ret


print("Ans 2)", num_ways(len(l) - 1))
