from itertools import cycle
from collections import defaultdict


MODES = range(3)
POSITION_MODE, IMMEDIATE_MODE, RELATIVE_MODE = MODES

opcode_func = dict()


def assign_opcode(opcode):
    def wrapper(f):
        opcode_func[opcode] = f
        return f

    return wrapper


class Intcode:
    def __init__(self, l, inputs=[]):
        self.l = Program(l.copy())
        self.idx = 0
        self.inputs = inputs
        self.outputs = []
        self.relative_base = 0

        self.new_output = False
        self.halted = False

        self.it = None

    def write(self, val, address, mode):
        assert mode in (POSITION_MODE, RELATIVE_MODE), mode
        offset = self.relative_base if mode == RELATIVE_MODE else 0
        self.l[address + offset] = val

    @assign_opcode(1)
    def add(self, l, idx, modes):
        operand1 = self.get_operand(l, l[idx + 1], modes[0])
        operand2 = self.get_operand(l, l[idx + 2], modes[1])
        self.write(operand1 + operand2, l[idx + 3], modes[2])
        return idx + 4

    @assign_opcode(2)
    def multiply(self, l, idx, modes):
        operand1 = self.get_operand(l, l[idx + 1], modes[0])
        operand2 = self.get_operand(l, l[idx + 2], modes[1])
        self.write(operand1 * operand2, l[idx + 3], modes[2])
        return idx + 4

    @assign_opcode(3)
    def input(self, l, idx, modes):
        self.write(self.inputs[0], l[idx + 1], modes[0])
        self.inputs = self.inputs[1:]
        return idx + 2

    @assign_opcode(4)
    def output(self, l, idx, modes):
        operand1 = self.get_operand(l, l[idx + 1], modes[0])
        self.outputs.append(operand1)
        self.new_output = True
        return idx + 2

    @assign_opcode(5)
    def jump_if_true(self, l, idx, modes):
        operand1 = self.get_operand(l, l[idx + 1], modes[0])
        operand2 = self.get_operand(l, l[idx + 2], modes[1])
        if operand1 != 0:
            return operand2
        return idx + 3

    @assign_opcode(6)
    def jump_if_false(self, l, idx, modes):
        operand1 = self.get_operand(l, l[idx + 1], modes[0])
        operand2 = self.get_operand(l, l[idx + 2], modes[1])
        if operand1 == 0:
            return operand2
        return idx + 3

    @assign_opcode(7)
    def less_than(self, l, idx, modes):
        operand1 = self.get_operand(l, l[idx + 1], modes[0])
        operand2 = self.get_operand(l, l[idx + 2], modes[1])
        self.write(int(operand1 < operand2), l[idx + 3], modes[2])
        return idx + 4

    @assign_opcode(8)
    def equals(self, l, idx, modes):
        operand1 = self.get_operand(l, l[idx + 1], modes[0])
        operand2 = self.get_operand(l, l[idx + 2], modes[1])
        self.write(int(operand1 == operand2), l[idx + 3], modes[2])
        return idx + 4

    @assign_opcode(9)
    def adjust_relative(self, l, idx, modes):
        operand1 = self.get_operand(l, l[idx + 1], modes[0])
        self.relative_base += operand1
        return idx + 2

    @assign_opcode(99)
    def halt(self, *_):
        self.halted = True

    opcodes = set(opcode_func)

    def get_opcode_and_modes(self, inst):
        opcode = inst % 100
        assert opcode in self.opcodes, opcode
        inst //= 100
        modes = []
        for _ in range(3):
            assert inst % 10 in MODES, f"Unknown mode: {inst % 10}"
            modes.append(inst % 10)
            inst //= 10
        return opcode, modes

    def get_operand(self, l, param, mode):
        if mode == POSITION_MODE:
            return l[param]
        elif mode == IMMEDIATE_MODE:
            return param
        elif mode == RELATIVE_MODE:
            return l[self.relative_base + param]
        else:
            assert False, mode

    def __iter__(self):
        if self.it == None:
            self.it = self.run_program()
        return self.it

    def run_program(self):
        while True:
            opcode, modes = self.get_opcode_and_modes(self.l[self.idx])
            # print('op', opcode, modes[0])
            self.idx = opcode_func[opcode](self, self.l, self.idx, modes)
            if self.new_output:
                yield self.outputs[-1]
                self.new_output = False
            if self.halted:
                self.it = None
                return

    def program_output(self):
        return list(self.run_program())


class Program:
    def __init__(self, l):
        self.l = l
        self.d = defaultdict(lambda: 0)

    def __getitem__(self, idx):
        assert idx >= 0, idx
        if len(self.l) > idx:
            return self.l[idx]
        return self.d[idx]

    def __setitem__(self, idx, val):
        assert idx >= 0, idx
        if len(self.l) > idx:
            self.l[idx] = val
        else:
            self.d[idx] = val


def read_program(fname):
    with open(fname, "r") as f:
        return list(map(int, f.readline().split(",")))


if __name__ == "__main__":
    l = read_program("7.txt")
    intcode = Intcode(l, [9, 0])
    it = iter(intcode)
    while True:
        try:
            print("inputs before:", intcode.inputs)
            out = next(it)
            print("out:", out)
            intcode.inputs.append(out)
        except StopIteration:
            break
    # 9
    l = [109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99]
    intcode = Intcode(l)
    out = intcode.program_output()
    assert l == out, ou

    intcode = Intcode([1102, 34915192, 34915192, 7, 4, 7, 99, 0])
    assert [1219070632396864] == intcode.program_output()

    intcode = Intcode([104, 1125899906842624, 99])
    assert [1125899906842624] == intcode.program_output()
