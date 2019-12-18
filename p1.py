# https://adventofcode.com/2019/day/1

def mass_to_fuel(mass):
    return max(mass // 3 - 2, 0)

def mass_to_fuel2(mass):
    ret = mass = mass_to_fuel(mass)
    while mass > 0:
        mass = mass_to_fuel(mass)
        ret += mass
    return ret 

ans1 = 0
ans2 = 0
with open('1.txt', 'r') as f:
    for line in f.readlines():
        mass = int(line.rstrip())
        ans1 += mass_to_fuel(mass)
        ans2 += mass_to_fuel2(mass)
print("1) Answer:", ans1)
print("2) Answer:", ans2)

