s = open("day1.txt").read()

sum = 0

for line in s.split("\n"):
    fst, lst = None, None
    for c in line:
        if c.isdigit():
            if fst is None:
                fst = c
            else:
                lst = c
    if lst is None:
        lst = fst
    sum += int(fst + lst)

print("Answer 1", sum)

sub_strs = ["1", "2", "3", "4", "5", "6", "7", "8", "9", 
            "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]

def find_first(line):
    ret, idx = None, float("inf")
    for i, sub_str in enumerate(sub_strs):
        cur_idx = line.find(sub_str)
        if cur_idx != -1 and cur_idx < idx:
            ret = i % 9 + 1
            idx = cur_idx
    return ret

def find_last(line):
    ret, idx = None, float("-inf")
    for i, sub_str in enumerate(sub_strs):
        cur_idx = line.rfind(sub_str)
        if cur_idx != -1 and cur_idx > idx:
            ret = i % 9 + 1
            idx = cur_idx
    return ret

sum = 0

for line in s.split("\n"):
    sum += int(10 * find_first(line) + find_last(line))

print("Answer 2", sum)
