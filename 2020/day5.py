s = """FBFBBFFRLR"""

s = open("day5.txt").read()

l = s.split("\n")


def seat_id(row, col):
    return 8 * row + col


seats = []
ma, mi = float("-inf"), float("inf")

for x in l:
    x1 = x[:7].replace("F", "0").replace("B", "1")
    row = int(x1, 2)
    x2 = x[7:].replace("L", "0").replace("R", "1")
    col = int(x2, 2)
    sid = seat_id(row, col)
    seats.append(sid)
    ma, mi = max(ma, sid), min(mi, sid)

print("Ans 1", ma)
print("Ans 2", set(seats).symmetric_difference(range(mi, ma + 1)))
