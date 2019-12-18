# https://adventofcode.com/2019/day/4

low = 248345
high = 746315

# def is_valid(num):
    # num = str(num)
    # has_adj = False
    # for i in range(1, len(num) - 1):
        # if num[i - 1] > num[i]:
            # return False
        # if num[i - 1] == num[i] and num[i] != num[i + 1]:
            # has_adj = i - 2 < 0 or num[i - 2] != num[i]
    # return num[-1] >= num[-2] and has_adj

def never_decrease(num):
    for i in range(1, len(num)):
        if num[i - 1] > num[i]:
            return False
    return True

def is_valid2(num):
    num = str(num)
    i = 0
    has_adj = False
    while i < len(num):
        n = num[i]
        num_adj = 1
        while i + 1 < len(num) and n == num[i + 1]:
            i += 1
            num_adj += 1
        if num_adj == 2:
            has_adj = True
        i += 1
    return has_adj and never_decrease(num)

ans = 0
for num in range(low, high + 1):
    ans += int(is_valid2(num))

print("Answer:", ans)

