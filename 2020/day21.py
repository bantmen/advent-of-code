from collections import defaultdict
from constraint import Problem, AllDifferentConstraint


s = """mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)"""

s = open("day21.txt").read()

i = []

i_to_a = defaultdict(set)
a_to_i = defaultdict(set)

for line in s.split("\n"):
    lhs, rhs = line.split(" (contains ")
    ingredients, allergens = lhs.split(" "), rhs.split(", ")
    allergens[-1] = allergens[-1][:-1]
    for ing in ingredients:
        i_to_a[ing] |= set(allergens)
    for al in allergens:
        if not a_to_i[al]:
            a_to_i[al] = set(ingredients)
        else:
            a_to_i[al] &= set(ingredients)
    i.append(ingredients)

p = Problem()

p.addConstraint(AllDifferentConstraint())

for al, ingredients in a_to_i.items():
    p.addVariable(al, list(ingredients))

not_seen = set(i_to_a.keys())
for soln in p.getSolutions():
    for ing in soln.values():
        if ing in not_seen:
            not_seen.remove(ing)

count = 0
for ingredients in i:
    for ing in ingredients:
        if ing in not_seen:
            count += 1
# 1679
print("Ans 1)", count)

allergens = [t[1] for t in sorted(p.getSolutions()[0].items(), key=lambda t: t[0])]

# lmxt,rggkbpj,mxf,gpxmf,nmtzlj,dlkxsxg,fvqg,dxzq
print("Ans 2)", ",".join(allergens))
