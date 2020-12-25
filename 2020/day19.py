import re

s = open("day19.txt").read()

rules, messages = s.split("\n\n")

d = {}

for line in rules.split("\n"):
    lhs, rhs = line.split(": ")
    d[lhs] = rhs


def get_pattern(rule_num):
    seq = d[rule_num].split(" ")
    if len(seq) == 1 and not seq[0].isdigit():
        return seq[0].replace('"', "")
    if "|" not in seq:
        return "".join(map(get_pattern, seq))
    else:
        sep_idx = seq.index("|")
        lhs = "(" + "".join(map(get_pattern, seq[:sep_idx])) + ")"
        rhs = "(" + "".join(map(get_pattern, seq[sep_idx + 1 :])) + ")"
        return "(" + lhs + "|" + rhs + ")"


pattern = "^" + get_pattern("0") + "$"
pattern = re.compile(pattern)

ans = 0

for line in messages.split("\n"):
    ans += int(pattern.match(line) is not None)

# 171
print("Ans 1)", ans)


def get_pattern2(rule_num):
    if rule_num == "8":
        # 42 | 42 8
        return "({})+".format(get_pattern2("42"))
    elif rule_num == "11":
        # 42 31 | 42 11 31
        # return get_pattern("11")
        lhs = "(" + get_pattern2("42") + ")"
        rhs = "(" + get_pattern2("31") + ")"
        return lhs + "{n}" + rhs + "{n}"
    seq = d[rule_num].split(" ")
    if len(seq) == 1 and not seq[0].isdigit():
        # assert not seq[0].isdigit(), seq
        return seq[0].replace('"', "")
    if "|" not in seq:
        return "".join(map(get_pattern2, seq))
    else:
        sep_idx = seq.index("|")
        lhs = "(" + "".join(map(get_pattern2, seq[:sep_idx])) + ")"
        rhs = "(" + "".join(map(get_pattern2, seq[sep_idx + 1 :])) + ")"
        return "(" + lhs + "|" + rhs + ")"


ans = 0

raw_pattern = "^" + get_pattern2("0") + "$"

patterns = [re.compile(raw_pattern.replace("{n}", "{%s}" % i)) for i in range(1, 5)]

for line in messages.split("\n"):
    ans += int(any(pattern.match(line) is not None for pattern in patterns))

# 369
print("Ans 2)", ans)
