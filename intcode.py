from itertools import cycle


opcode_func = dict()


def assign_opcode(opcode):
    def wrapper(f):
        opcode_func[opcode] = f
        return f

    return wrapper


def get_operand(l, param, mode):
    if mode == 0:
        # position
        return l[param]
    elif mode == 1:
        # immediate
        return param
    else:
        assert False, mode


class Intcode:
    def __init__(self, program, inputs):
        self.l = program
        self.idx = 0
        self.inputs = inputs
        self.outputs = []

        self.new_output = False
        self.halted = False

        self.it = None

    @assign_opcode(1)
    def add(self, l, idx, modes):
        operand1 = get_operand(l, l[idx + 1], modes[0])
        operand2 = get_operand(l, l[idx + 2], modes[1])
        l[l[idx + 3]] = operand1 + operand2
        return idx + 4

    @assign_opcode(2)
    def multiply(self, l, idx, modes):
        operand1 = get_operand(l, l[idx + 1], modes[0])
        operand2 = get_operand(l, l[idx + 2], modes[1])
        l[l[idx + 3]] = operand1 * operand2
        return idx + 4

    @assign_opcode(3)
    def input(self, l, idx, modes):
        l[l[idx + 1]] = self.inputs[0]
        self.inputs = self.inputs[1:]
        return idx + 2

    @assign_opcode(4)
    def output(self, l, idx, modes):
        operand1 = get_operand(l, l[idx + 1], modes[0])
        self.outputs.append(operand1)
        self.new_output = True
        return idx + 2

    @assign_opcode(5)
    def jump_if_true(self, l, idx, modes):
        operand1 = get_operand(l, l[idx + 1], modes[0])
        operand2 = get_operand(l, l[idx + 2], modes[1])
        if operand1 != 0:
            return operand2
        return idx + 3

    @assign_opcode(6)
    def jump_if_false(self, l, idx, modes):
        operand1 = get_operand(l, l[idx + 1], modes[0])
        operand2 = get_operand(l, l[idx + 2], modes[1])
        if operand1 == 0:
            return operand2
        return idx + 3

    @assign_opcode(7)
    def less_than(self, l, idx, modes):
        operand1 = get_operand(l, l[idx + 1], modes[0])
        operand2 = get_operand(l, l[idx + 2], modes[1])
        l[l[idx + 3]] = int(operand1 < operand2)
        return idx + 4

    @assign_opcode(8)
    def equals(self, l, idx, modes):
        operand1 = get_operand(l, l[idx + 1], modes[0])
        operand2 = get_operand(l, l[idx + 2], modes[1])
        l[l[idx + 3]] = int(operand1 == operand2)
        return idx + 4

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
            assert inst % 10 in (0, 1), inst % 10
            modes.append(inst % 10)
            inst //= 10
        return opcode, modes

    def __iter__(self):
        if self.it == None:
            self.it = self.run_program()
        return self.it

    def run_program(self):
        while True:
            opcode, modes = self.get_opcode_and_modes(self.l[self.idx])
            self.idx = opcode_func[opcode](self, self.l, self.idx, modes)
            if self.new_output:
                yield self.outputs[-1]
                self.new_output = False
            if self.halted:
                self.it = None
                return


def read_program(fname):
    with open(fname, "r") as f:
        return list(map(int, f.readline().split(",")))


if __name__ == "__main__":
    l = read_program("7.txt")
    intcode = Intcode(l.copy(), [9, 0])
    it = iter(intcode)
    while True:
        try:
            print("inputs before:", intcode.inputs)
            out = next(it)
            print("out:", out)
            intcode.inputs.append(out)
        except StopIteration:
            break
