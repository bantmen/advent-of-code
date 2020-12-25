# https://adventofcode.com/2020/day/2

from collections import Counter


s = open("day2.txt").read()

l = s.split("\n")

num_valid = 0
num_valid_part_2 = 0

for line in l:
    count, char, s = line.split(" ")
    low, high = count.split("-")
    low, high = int(low), int(high)
    char = char[0]
    s = s.rstrip()
    char_count = Counter(s)[char]
    num_valid += int(low <= char_count <= high)
    num_valid_part_2 += int((s[low - 1] == char) ^ (s[high - 1] == char))

print(num_valid)
print(num_valid_part_2)
