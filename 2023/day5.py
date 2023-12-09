s = """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4"""

s = open("day5.txt").read()

def map(x, mapping):
    for (src_begin, src_end, offset) in mapping:
        if src_begin <= x <= src_end:
            return x + offset
    return x

l = s.split("\n\n")

# seeds = list(map(int, l[0].split("seeds: ")[1].split(" ")))
seeds = [int(x) for x in l[0].split("seeds: ")[1].split(" ")]

all_mapping = []

for mapping in l[1:]:
    mapping_l = []
    for line in mapping.split("\n")[1:]:
        dest, src, length = [int(x) for x in line.split(" ")]
        mapping_l.append((src, src + length - 1, dest - src))
        mapping_l.sort(key=lambda x: x[0])
    all_mapping.append(mapping_l)

ans = float("inf")

for x in seeds:
    for mapping in all_mapping:
        x = map(x, mapping)
    ans = min(ans, x)

print("Part 1)", ans)

intervals = []

for i in range(0, len(seeds) - 1, 2):
    intervals.append((seeds[i], seeds[i] + seeds[i + 1]))

def intersection(a1, a2, b1, b2):
    if a1 <= b1 <= a2:
        return (b1, min(a2, b2))
    if b1 <= a1 <= b2:
        return (a1, min(a2, b2))
    else:
        return None

def map2(intervals, mapping):
    intervals = intervals[:]
    out = []
    while len(intervals) > 0:
        begin, end = intervals[-1]
        intervals.pop()
        found = False
        for (src_begin, src_end, offset) in mapping:
            intersect = intersection(begin, end, src_begin, src_end)
            if intersect is not None:
                found = True
                if intersect == (begin, end):
                    # it all intersected
                    out.append((begin + offset, end + offset))
                else:
                    # some of it intersected

                    # left non-intersect
                    if (intersect[0] - 1 > begin):
                        intervals.append((begin, intersect[0] - 1))
                    
                    # intersection
                    out.append((intersect[0] + offset, intersect[1] + offset))
                    
                    # right non-intersect
                    if intersect[1] + 1 < end:
                        intervals.append((intersect[1] + 1, end))
                break
        if not found:
            # no change
            out.append((begin, end))
    return out

for mapping in all_mapping:
    intervals = map2(intervals, mapping)

print("Part 2)", min([x[0] for x in intervals]))
