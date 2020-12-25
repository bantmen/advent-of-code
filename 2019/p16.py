# https://adventofcode.com/2019/day/16


with open("16.txt", "r") as f:
    x = f.read()
l = list(map(int, x))


def pattern(i):
    base = [0, 1, 0, -1]
    idx = 0
    while True:
        for _ in range(i):
            yield base[idx]
        idx = (idx + 1) % len(base)


for phase in range(1, 101):
    l2 = []
    for i in range(1, len(l) + 1):
        ps = pattern(i)
        # Skip the first pattern value
        next(ps)
        acc = 0
        for x, p in zip(l, ps):
            acc += x * p
        l2.append(abs(acc) % 10)
    l = l2


def list_to_int(l):
    return int("".join(map(str, l)))


print("1) Answer", list_to_int(l[:8])) # 96136976
