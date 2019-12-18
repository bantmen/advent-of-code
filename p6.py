# https://adventofcode.com/2019/day/6

from collections import defaultdict

ROOT = "COM"
SRC = "YOU"
DEST = "SAN"


# str -> [str]
satellites = defaultdict(list)
# str -> str
orbits = dict()
with open("6.txt", "r") as f:
    for line in f.readlines():
        pl1, pl2 = line.rstrip().split(")")
        satellites[pl1].append(pl2)
        orbits[pl2] = pl1


def distance_from_planet(planet):
    num_visited = dict()
    def walk(pl, num_edge_visited):
        num_visited[pl] = num_edge_visited
        for s in satellites[pl]:
            walk(s, num_edge_visited + 1)
    walk(planet, 0)
    return num_visited


def count_orbits(planet):
    num_visited = distance_from_planet(ROOT)
    return sum(num_visited.values())


def lowest_common_ancestor(pl1, pl2):
    def get_path(src_pl):
        path = []
        cur_pl = src_pl
        while cur_pl != ROOT:
            path.append(cur_pl)
            cur_pl = orbits[cur_pl]
        return path
    pl1_path, pl2_path = get_path(pl1), get_path(pl2)
    common = set(pl1_path) & set(pl2_path)
    lowest_common = None
    for pl in pl1_path:
        if pl in common:
            lowest_common = pl
            break
    assert lowest_common is not None
    return lowest_common


def min_orbital_transfer(src_pl, dest_pl):
    num_visited = distance_from_planet(ROOT)
    # Our real pathing depends on parent vertices
    src_pl, dest_pl = orbits[src_pl], orbits[dest_pl]
    common_pl = lowest_common_ancestor(src_pl, dest_pl)
    # src_pl -> dest_pl = src_pl > common_ancestor + common_ancestor > dest_pl
    # src_pl > common_ancestor = COM > src_pl - COM > common_ancestor
    # common_ancestor > dest_pl = COM > dest_pl - COM > common_ancestor
    src_to_common = num_visited[src_pl] - num_visited[common_pl]
    common_to_dest = num_visited[dest_pl] - num_visited[common_pl]
    return src_to_common + common_to_dest


print("Answer 1:", count_orbits(ROOT))
print("Answer 2:", min_orbital_transfer(SRC, DEST))
