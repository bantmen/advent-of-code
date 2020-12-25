s = """Player 1:
9
2
6
3
1

Player 2:
5
8
4
7
10"""

s = open("day22.txt").read()

p1, p2 = s.split("\n\n")
p1, p2 = [int(x) for x in p1.split("\n")[1:]], [int(x) for x in p2.split("\n")[1:]]

# returns winner and score
def play(p1, p2):
    while p1 and p2:
        if p1[0] > p2[0]:
            p1.extend([p1.pop(0), p2.pop(0)])
        else:
            p2.extend([p2.pop(0), p1.pop(0)])
        winner = p1 if p1 else p2
        winner_str = "p1" if p1 else "p2"
    return winner_str, sum((i + 1) * v for i, v in enumerate(reversed(winner)))


# 32413
print("Ans 1)", play(list(p1), list(p2))[1])

# returns winner, winner_deck
def rec(p1, p2, seen):
    while p1 and p2:
        game = (tuple(p1), tuple(p2))
        if game in seen:
            return "p1", p1
        seen.add(game)
        x1, x2 = p1.pop(0), p2.pop(0)
        if len(p1) >= x1 and len(p2) >= x2:
            winner_str, _ = rec(p1[:x1], p2[:x2], set())
        else:
            winner_str = "p1" if x1 > x2 else "p2"
        if winner_str == "p1":
            p1.extend([x1, x2])
        else:
            p2.extend([x2, x1])
    return "p1" if p1 else "p2", p1 if p1 else p2


winner_str, deck = rec(p1, p2, set())

# 31596
print("Ans 2)", sum((i + 1) * v for i, v in enumerate(reversed(deck))))
