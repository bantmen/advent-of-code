import re
from collections import defaultdict


# Part 1
s = """mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0"""

# Part 2
s = """mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1"""

s = open("day14.txt").read()

l = s.split("\n")


def left_pad(val, fill):
    return fill * (36 - len(val)) + val


def use_mask(val, mask):
    val = left_pad(val, "0")
    ret = []
    for c1, c2 in zip(val, mask):
        ret.append(c1 if c2 == "X" else c2)
    return "".join(ret)


d = defaultdict(lambda: "0")
mask = None
pattern = re.compile(r"mem\[(\d*)\]")

for line in l:
    lhs, rhs = line.split(" = ")
    if lhs == "mask":
        mask = rhs
    else:
        val = format(int(rhs), "b")
        idx = int(pattern.match(lhs).group(1))
        d[idx] = use_mask(val, mask)

print("Ans 1)", sum(int(x, 2) for x in d.values()))


def use_memory_mask(val, mask):
    val = left_pad(val, "0")
    new_val = []
    for c1, c2 in zip(val, mask):
        new_val.append(c1 if c2 == "0" else c2)
    ret = []

    def gen(val, idx=0):
        if idx == len(val):
            ret.append("".join(val))
        elif val[idx] == "X":
            val[idx] = "0"
            gen(val, idx + 1)
            val[idx] = "1"
            gen(val, idx + 1)
            val[idx] = "X"
        else:
            gen(val, idx + 1)

    gen(new_val)
    return ret


d = defaultdict(lambda: "0")

for line in l:
    lhs, rhs = line.split(" = ")
    if lhs == "mask":
        mask = rhs
    else:
        val = format(int(rhs), "b")
        mem_val = format(int(pattern.match(lhs).group(1)), "b")
        d.update({int(idx_val, 2): val for idx_val in use_memory_mask(mem_val, mask)})

print("Ans 2)", sum(int(x, 2) for x in d.values()))
