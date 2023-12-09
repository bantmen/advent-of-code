s = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"""

s = open("day4.txt").read()

def get_nums(s):
    l = []
    acc = ""
    for c in s:
        if c == " " and acc != "":
            # flush
            l.append(acc)
            acc = ""
        if c != " ":
            acc += c
    if acc != "":
        # flush
        l.append(acc)
    return l

ans = 0

# car num -> [ card nums ]
score_cards = {}

for i, line in enumerate(s.split("\n")):
    winning_nums, nums = line.split(": ")[1].split(" | ")
    s1 = set(get_nums(winning_nums))
    s2 = set(get_nums(nums))
    overlap = len(s1.intersection(s2))
    if overlap > 0:
        ans += 2 ** (overlap - 1)
        score_cards[i + 1] = list(range(i + 2, i + 2 + overlap))
    else:
        score_cards[i + 1] = []

print("Part 1)", ans)

# Store the number of expansions for each card number
d = {}
for card_num in range(i + 1, 0, -1):
    cur = 0
    for card_num2 in score_cards[card_num]:
        cur += 1 + d[card_num2]
    d[card_num] = cur

# Don't forget the count the original scratchcards
print("Part 2)", sum(d.values()) + i + 1)
