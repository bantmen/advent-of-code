s = """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45"""

s = open("day9.txt").read()

def create_seq(nums):
    new_seq = []
    is_all_zero = True
    for i in range(1, len(nums)):
        new = nums[i] - nums[i - 1]
        is_all_zero &= new == 0
        new_seq.append(new)
    return new_seq, is_all_zero

def create_all_seqs(nums):
    ret = [nums]
    all_zero = False
    while not all_zero:
        nums, all_zero = create_seq(nums)
        ret.append(nums)
    prev_nums = None
    for nums in reversed(ret):
        if prev_nums is None:
            nums.append(0) # Part 1
            nums.insert(0, 0) # Part 2
        else:
            nums.append(nums[-1] + prev_nums[-1]) # Part 1
            nums.insert(0, nums[0] - prev_nums[0]) # Part 2
        prev_nums = nums
    return ret

ans = 0
ans2 = 0

for line in s.split("\n"):
    all_seqs = create_all_seqs([int(x) for x in line.split(" ")])
    ans += all_seqs[0][-1]
    ans2 += all_seqs[0][0]

print("Part 1)", ans)
print("Part 2)", ans2)
