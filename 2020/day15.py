from collections import defaultdict


s = "3,1,2"

# s = "0,5,4,1,10,14,7"

l = list(map(int, s.split(",")))

d = defaultdict(list)
d.update({v: [i + 1] for i, v in enumerate(l)})


def update(val, turn):
    if len(d[val]) == 0:
        d[val] = [turn]
    else:
        d[val] = [turn, d[val][0]]


last = l[-1]

target_turn = 2020
# target_turn = 30000000

i = len(l)
while i != target_turn:
    i += 1
    if len(d[last]) < 2:
        # That was the first time
        say = 0
    else:
        # Was spoken at least 2 times before
        say = d[last][0] - d[last][1]
    update(say, i)
    last = say

print(last)
