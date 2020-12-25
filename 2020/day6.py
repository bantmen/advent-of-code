from collections import Counter


s = open("day6.txt").read()


def get_groups(it, sep):
    l = []
    for x in it:
        if x == sep:
            yield l
            l = []
        else:
            l.append(x)
    yield l


counts = 0
all_yes_counts = 0
for group in get_groups(s.split("\n"), ""):
    c = Counter()
    for person in group:
        c += Counter(person)
    counts += len(c)
    for v in c.values():
        if v == len(group):
            all_yes_counts += 1

print(counts)
print(all_yes_counts)
