# https://adventofcode.com/2019/day/12

import re
import numpy as np


s = """<x=-10, y=-13, z=7>
<x=1, y=2, z=1>
<x=-15, y=-3, z=13>
<x=3, y=7, z=-4>"""


def read_planets(s):
    pattern = r"<x=(-?\d+), y=(-?\d+), z=(-?\d+)>"
    planet_tuples = re.findall(pattern, s)
    return list(map(int, sum(planet_tuples, ())))


def update_gravity(pos, gravity):
    for i in range(pos.shape[1]):
        for j in range(pos.shape[0]):
            gravity_ji = 0
            for j2 in range(pos.shape[0]):
                if pos[j2, i] > pos[j, i]:
                    gravity_ji += 1
                if pos[j2, i] < pos[j, i]:
                    gravity_ji -= 1
            gravity[j, i] = gravity_ji
    return gravity


def total_energy(pos, vel):
    return (np.abs(pos).sum(axis=1) * np.abs(vel).sum(axis=1)).sum()


planets = read_planets(s)
shape = (len(planets) // 3, 3)
pos = np.array(planets).reshape(shape)
vel = np.zeros(shape, dtype=pos.dtype)


def solve_1(pos, vel):
    gravity = np.empty(pos.shape, dtype=pos.dtype)
    for i in range(1000):
        update_gravity(pos, gravity)
        vel += gravity
        pos += vel
    print("1) Answer:", total_energy(pos, vel))


def find_repeat(pos, vel):
    initial_pos, initial_vel = pos.copy(), vel.copy()
    gravity = np.empty(pos.shape, dtype=pos.dtype)
    i = 0
    while True:
        i += 1
        update_gravity(pos, gravity)
        vel += gravity
        pos += vel
        # Minor optimization: Check the "hash" first before incurring the
        # overhead - ~3s speed up.
        if (
            pos[0, 0] == initial_pos[0, 0]
            # and vel[0, 0] == initial_vel[0, 0]
            and np.array_equal(pos, initial_pos)
            and np.array_equal(vel, initial_vel)
        ):
            return i


def solve_2(pos, vel):
    i0 = find_repeat(pos[:, 0][None].T, vel[:, 0][None].T)
    i1 = find_repeat(pos[:, 1][None].T, vel[:, 1][None].T)
    i2 = find_repeat(pos[:, 2][None].T, vel[:, 2][None].T)
    print("2) Answer:", np.lcm.reduce([i0, i1, i2]))


solve_1(pos.copy(), vel.copy())  # 8454
solve_2(pos.copy(), vel.copy())  # 362336016722948
