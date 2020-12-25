# https://adventofcode.com/2019/day/14

from collections import Counter
from math import ceil


with open("14.txt", "r") as f:
    s = f.read()


def symbol_quantity(s):
    q, sym = s.split(" ")
    return tuple([sym, int(q)])


def sym_q_count(sym_qs):
    return Counter({sym: q for (sym, q) in sym_qs})


# Map the produced chemical to the ingredients
d = {}
for line in s.split("\n"):
    left, right = line.split(" => ")
    sym, q = symbol_quantity(right)
    assert sym not in d, "Multiple production rules for the same chemical"
    d[sym] = Counter()
    # LHS is positive
    d[sym].update(sym_q_count(map(symbol_quantity, left.split(", "))))
    # RHS is negative
    d[sym].update(Counter({sym: -q}))


def only_ore(chemicals):
    num_pos = 0
    for sym, q in chemicals.items():
        num_pos += int(q > 0)
        if num_pos > 1:
            return False
    return chemicals.get("ORE", 0) > 0


def multiply_counter(counter, factor):
    for key in counter:
        counter[key] *= factor


def num_ores_for_fuel(fuel):
    chems = Counter({"FUEL": fuel})
    while not only_ore(chems):
        delta_chems = Counter()
        for sym, q in chems.items():
            if q > 0 and sym != "ORE":
                delta_chems = d[sym].copy()
                multiply_counter(delta_chems, int(ceil(q / abs(delta_chems[sym]))))
                break
        chems.update(delta_chems)
    return chems["ORE"]


ore_per_fuel = num_ores_for_fuel(1)
print("1) Answer", ore_per_fuel)


def largest_below_threshold(lower, upper, f, threshold):
    if lower > upper:
        return -1
    if f(lower) > threshold:
        return -1
    mid = (lower + upper) // 2
    score = f(mid)
    if score > threshold:
        return largest_below_threshold(lower, mid - 1, f, threshold)
    elif score < threshold:
        # Try going higher
        score_input = largest_below_threshold(mid + 1, upper, f, threshold)
        if score_input == -1:
            return mid
        return score_input
    else:
        return mid


max_ore = 1000000000000
ans = largest_below_threshold(lower=max_ore // ore_per_fuel, upper=max_ore, f=num_ores_for_fuel, threshold=max_ore)
print("2) Answer", ans)
