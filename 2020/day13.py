import math


s = """939
1789,37,47,1889"""

s = open("day13.txt").read()

l = s.split("\n")

earliest = int(l[0])  # earliest you can depart
buses = [int(x) for x in l[1].split(",") if x != "x"]

mi = float("inf")  # earliest bus you can catch
bus_id = None
for x in buses:
    y = math.ceil(earliest / x) * x - earliest
    if mi > y:
        mi = y
        bus_id = x
print("Ans 1)", mi * bus_id)

buses_with_x = l[1].split(",")
y_offset_seq = []
offset = 0
for bus in buses_with_x:
    if bus != "x":
        y_offset_seq.append((int(bus), offset))
    offset += 1


def smallest(x, y, offset, delta):
    # Increase x until x + offset is a multiple of y
    while (x + offset) % y != 0:
        x += delta
    return x


combined = delta = y_offset_seq.pop(0)[0]
while len(y_offset_seq) > 0:
    combined = smallest(
        x=combined, y=y_offset_seq[0][0], offset=y_offset_seq[0][1], delta=delta
    )
    delta *= y_offset_seq.pop(0)[0]
# 404517869995362
print("Ans 2)", combined)
