from collections import Counter
from functools import cmp_to_key


s = """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483"""

s = open("day7.txt").read()

d = {
    "A": 13,
    "K": 12,
    "Q": 11,
    "J": 10,
    "T": 9,
    "9": 8,
    "8": 7,
    "7": 6,
    "6": 5,
    "5": 4,
    "4": 3,
    "3": 2,
    "2": 1,
}

five_of_a_kind, four_of_a_kind, full_house, three_of_a_kind, two_pair, one_pair, high_card, none = range(8, 0, -1)

def identify_hand(hand, part2):
    c = Counter(hand)
    vals = sorted(c.values(), reverse=True)
    if "part 2" in d and "J" in c:
        if c["J"] == 1:
            if vals == [4, 1]:
                vals = [5]
            elif vals == [3, 1, 1]:
                vals = [4, 1]
            elif vals == [2, 1, 1, 1]:
                vals = [3, 1, 1]
            elif vals == [1, 1, 1, 1, 1]:
                vals = [2, 1, 1, 1]
            elif vals == [2, 2, 1]:
                vals = [3, 2]
            else:
                assert False, (c["J"], vals)
        elif c["J"] == 2:
            if vals == [3, 2]:
                vals = [5]
            elif vals == [2, 2, 1]:
                vals = [4, 1]
            elif vals == [2, 1, 1, 1]:
                vals = [3, 1, 1]
            else:
                assert False, (c["J"], vals)
        # 3 J
        elif c["J"] == 3:
            if vals == [3, 1, 1]:
                vals = [4, 1]
            elif vals == [3, 2]:
                vals = [5]
            else:
                assert False, (c["J"], vals)
        # 4 J
        if c["J"] == 4:
            if vals == [4, 1]:
                vals = [5]
            else:
                assert False, (c["J"], vals)

    assert sum(vals) == 5

    if vals == [5]:
        return five_of_a_kind
    elif vals == [4, 1]:
        return four_of_a_kind
    elif vals == [3, 2]:
        return full_house
    elif vals == [3, 1, 1]:
        return three_of_a_kind
    elif vals == [2, 2, 1]:
        return two_pair
    elif vals == [2, 1, 1, 1]:
        return one_pair
    elif vals == [1, 1, 1, 1, 1]:
        return high_card
    return none

def compare(hand1, hand2, part2=False):
    hand1, hand2 = hand1[0], hand2[0]
    hand1_type, hand2_type = identify_hand(hand1, part2=part2), identify_hand(hand2, part2=part2)
    if hand1_type == hand2_type:
        for x1, x2 in zip(hand1, hand2):
            if d[x1] > d[x2]:
                return 1
            elif d[x2] > d[x1]:
                return -1
        return 0
    elif hand1_type > hand2_type:
        return 1
    else: # hand2_type > hand1_type
        return -1

l = []

for line in s.split("\n"):
    hand, bid = line.split(" ")
    l.append((hand, int(bid)))

l.sort(key=cmp_to_key(compare))

ans = 0

for i, v in enumerate(l):
    ans += (i + 1) * v[1]

print("Part 1)", ans)

d = {
    "A": 13,
    "K": 12,
    "Q": 11,
    "T": 9,
    "9": 8,
    "8": 7,
    "7": 6,
    "6": 5,
    "5": 4,
    "4": 3,
    "3": 2,
    "2": 1,
    "J": 0,
    "part 2": True, # hacky but it's fine ;)
}

l.sort(key=cmp_to_key(compare))

ans = 0

for i, v in enumerate(l):
    ans += (i + 1) * v[1]

print("Part 2)", ans)

