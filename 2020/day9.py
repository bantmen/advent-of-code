from queue import Queue
from collections import defaultdict
import numpy as np

s = open("day9.txt").read()

l = [int(x) for x in s.split("\n")]

preamble_length = 25  # 5

q = Queue()

x_counts = defaultdict(int)

target = None

for i, x in enumerate(l):
    if i < preamble_length:
        x_counts[x] += 1
        q.put_nowait(x)
        continue
    found = False
    for x2 in q.queue:
        # Handle the case where the x complement is equal to x2
        if x_counts[x - x2] > 0 and (x2 != x - x2 or x_counts[x - x2] > 1):
            found = True
            break
    if not found:
        target = x
        break
    # Update
    x_counts[x] += 1
    q.put_nowait(x)
    x_counts[q.get_nowait()] -= 1

print("Ans 1)", target)

l_cumsum = np.cumsum(l)
d = {}
start = end = None
for i, x in enumerate(l_cumsum):
    if x - target in d:
        start = d[x - target]
        end = i
        break
    d[x] = i

print("Ans 2)", min(l[start + 1 : end + 1]) + max(l[start + 1 : end + 1]))
