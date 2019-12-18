# https://adventofcode.com/2019/day/9

from intcode import Intcode, read_program

intcode = Intcode(read_program("9.txt"), [1])
out = intcode.program_output()
assert len(out) == 1, out
print("1) Answer:", out[0])

intcode = Intcode(read_program("9.txt"), [2])
out = intcode.program_output()
assert len(out) == 1, out
print("2) Answer:", out[0])
