import math


time = [7, 15, 30]
distance = [9, 40, 200]

time = [38, 94, 79, 70]
distance = [241, 1549, 1074, 1091]

# quadratic solution for
# -x^2 + time*x - distance > 0

def solve(t, d):
    a, b, c = -1, t, -d
    fst = -b / (2*a)
    snd = (b**2 - 4*a*c)**0.5 / (2*a)
    # there has to be a more elegant way to do this
    lower, upper = math.ceil(fst + snd), math.floor(fst - snd)
    lower = lower if lower > fst + snd else lower + 1
    upper = upper if upper < fst - snd else upper - 1
    return lower, upper

ans = 1

for (t, d) in zip(time, distance):
    x, y = solve(t, d)
    print(x, y)
    ans *= (y - x + 1)

print("Part 1)", ans)

x, y = solve(38947970, 241154910741091)
print("Part 2)", (y - x + 1))
