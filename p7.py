# https://adventofcode.com/2019/day/7

from intcode import read_program, Intcode
from itertools import permutations


def max_signal(l):
    num_amplifiers = 5
    max_out = float("-inf")
    for phase_setting in permutations(range(num_amplifiers)):
        out = 0
        for phase in phase_setting:
            out = list(Intcode(l, [phase, out]).run_program())[0]
        max_out = max(max_out, out)
    return max_out


def max_signal2(l):
    max_out = float("-inf")
    for phase_setting in permutations(range(5, 10)):
        amplifiers = [Intcode(l, [phase_setting[i]]) for i in range(5)]
        out = 0
        i = 0
        while True:
            idx = i % len(amplifiers)
            amplifier = amplifiers[idx]
            amplifier.inputs.append(out)
            try:
                out = next(iter(amplifier))
            except StopIteration:
                break
            i += 1
        max_out = max(max_out, out)
    return max_out


l = read_program("7.txt")

print(max_signal(l))
print(max_signal2(l))
