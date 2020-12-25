import re


s = """light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags."""

s = open("day7.txt").read()

pattern = re.compile("\sbags?,?\s?")

d = {}

for line in s.split("\n"):
    left, right = line.split(" bags contain ")
    right = pattern.split(right)
    d[left] = {}
    for r in right[:-1]:
        if r == "no other":
            break
        quantity, name = r.split(" ", maxsplit=1)
        d[left][name] = int(quantity)

# Missing: unknown. True/False: Leads / does not lead.
leads_to_target = {}

# Count number of nodes that lead to the target node
target = "shiny gold"


def visit(name):
    if name in leads_to_target:
        return leads_to_target[name]

    if name == target:
        return True

    found = False

    for child_name in d[name]:
        leads_to_target[child_name] = visit(child_name)
        found |= leads_to_target[child_name]

    leads_to_target[name] = found

    return found


for name in d:
    visit(name)

print("Ans 1)", sum(map(int, leads_to_target.values())) - 1)

num_bags = {}


def visit2(name):
    if name in num_bags:
        return num_bags[name]
    ans = 0
    for child_name, quantity in d[name].items():
        ans += quantity + quantity * visit2(child_name)
    num_bags[name] = ans
    return ans


visit2(target)

print("Ans 2)", num_bags[target])
