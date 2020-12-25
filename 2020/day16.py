s = open("day16.txt").read()

l = s.split("\n\n")

rules = []
for line in l[0].split("\n"):
    first, second = line.split(": ")[1].split(" or ")
    first, second = first.split("-"), second.split("-")
    rules.append([(int(first[0]), int(first[1])), (int(second[0]), int(second[1]))])

your_ticket = list(map(int, l[1].split("\n")[1].split(",")))

nearby_tickets = []
for line in l[2].split("\n")[1:]:
    nearby_tickets.append(list(map(int, line.split(","))))


def is_match(x, rule):
    return any(lower <= x <= upper for lower, upper in rule)


ans = 0

valid_tickets = []

for ticket in nearby_tickets:
    if ticket[0] == 18:
        # import pdb; pdb.set_trace()
        pass
    is_valid = True
    for x in ticket:
        if not any(is_match(x, rule) for rule in rules):
            ans += x
            is_valid = False
    if is_valid:
        valid_tickets.append(ticket)

print("Ans 1)", ans)

# all values for each field to be sorted later
l = [list() for _ in range(len(your_ticket))]

for ticket in valid_tickets:
    for i, x in enumerate(ticket):
        l[i].append(x)

# field idx -> [rule idx]
possible = [list() for _ in range(len(your_ticket))]

for i in range(len(your_ticket)):
    for j, rule in enumerate(rules):
        if all(is_match(x, rule) for x in l[i]):
            possible[i].append(j)

# heuristic to speed up the search
idx_order = [t[0] for t in sorted(enumerate(map(len, possible)), key=lambda t: t[1])]


def resolve(idx=0, soln={}):
    if idx == len(possible):
        return len(your_ticket) == len(set(soln.values())), soln
    else:
        for x in possible[idx_order[idx]]:
            if x not in soln.values():
                soln[idx_order[idx]] = x
                found, ret = resolve(idx + 1, soln)
                if found:
                    return True, ret
                del soln[idx_order[idx]]
        return False, []


# print(possible)

# soln maps field idx to rule idx
_, soln = resolve()

# verify the soln
for i in range(len(your_ticket)):
    for x in l[i]:
        assert is_match(x, rules[soln[i]]), (x, i, soln[i])

# print(soln)

ans = 1

# departures
for i in range(6):
    for field_idx, rule_idx in soln.items():
        if i == rule_idx:
            ans *= your_ticket[field_idx]
            break

# 366871907221
print("Ans 2)", ans)
