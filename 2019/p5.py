# https://adventofcode.com/2019/day/5


opcode_func = dict()
def assign_opcode(opcode):
    def wrapper(f):
        opcode_func[opcode] = f
        return f
    return wrapper


@assign_opcode(1)
def add(l, idx, modes):
    operand1 = get_operand(l, l[idx + 1], modes[0])
    operand2 = get_operand(l, l[idx + 2], modes[1])
    l[l[idx + 3]] = operand1 + operand2
    return idx + 4


@assign_opcode(2)
def multiply(l, idx, modes):
    operand1 = get_operand(l, l[idx + 1], modes[0])
    operand2 = get_operand(l, l[idx + 2], modes[1])
    l[l[idx + 3]] = operand1 * operand2
    return idx + 4


@assign_opcode(3)
def input(l, idx, modes):
    INPUT = 5
    l[l[idx + 1]] = INPUT
    return idx + 2


OUTPUTS = []
@assign_opcode(4)
def output(l, idx, modes):
    operand1 = get_operand(l, l[idx + 1], modes[0])
    OUTPUTS.append(operand1)
    return idx + 2


@assign_opcode(5)
def jump_if_true(l, idx, modes):
    operand1 = get_operand(l, l[idx + 1], modes[0])
    operand2 = get_operand(l, l[idx + 2], modes[1])
    if operand1 != 0:
        return operand2
    return idx + 3


@assign_opcode(6)
def jump_if_false(l, idx, modes):
    operand1 = get_operand(l, l[idx + 1], modes[0])
    operand2 = get_operand(l, l[idx + 2], modes[1])
    if operand1 == 0:
        return operand2
    return idx + 3


@assign_opcode(7)
def less_than(l, idx, modes):
    operand1 = get_operand(l, l[idx + 1], modes[0])
    operand2 = get_operand(l, l[idx + 2], modes[1])
    l[l[idx + 3]] = int(operand1 < operand2)
    return idx + 4


@assign_opcode(8)
def equals(l, idx, modes):
    operand1 = get_operand(l, l[idx + 1], modes[0])
    operand2 = get_operand(l, l[idx + 2], modes[1])
    l[l[idx + 3]] = int(operand1 == operand2)
    return idx + 4


opcodes = set(opcode_func) | set([99])
def get_opcode_and_modes(inst):
    opcode = inst % 100
    assert opcode in opcodes, opcode
    inst //= 100
    modes = []
    for _ in range(3):
        assert inst % 10 in (0, 1), inst % 10
        modes.append(inst % 10)
        inst //= 10
    return opcode, modes


def get_operand(l, param, mode):
    if mode == 0:
        # position
        return l[param]
    elif mode == 1:
        # immediate
        return param
    else:
        assert False, mode

def run_program(l):
    idx = 0
    while True:
        opcode, modes = get_opcode_and_modes(l[idx])
        f = opcode_func.get(opcode, None)
        if f is None:
            assert opcode == 99, l[idx]
            assert all(output == 0 for output in OUTPUTS[:-1]), OUTPUTS
            return OUTPUTS[-1]
        idx = f(l, idx, modes)


with open("5.txt", "r") as f:
    l = list(map(int, f.readline().split(",")))

print("Answer:", run_program(l))
