s = """nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6"""

s = open("day8.txt").read()

l = s.split("\n")

# Returns (is_infinite, acc)
def interpreter(l):
    seen_idx = set()
    idx = 0
    acc = 0
    while idx < len(l):
        if idx in seen_idx:
            return True, acc
        seen_idx.add(idx)

        inst, val = l[idx].split(" ")
        val = int(val)
        if inst == "nop":
            idx += 1
        elif inst == "acc":
            acc += val
            idx += 1
        elif inst == "jmp":
            idx += val
        else:
            assert False
    return False, acc


is_infinite, acc = interpreter(l)
assert is_infinite
print("Ans 1)", acc)

idx = 0
while idx < len(l):
    inst, val = l[idx].split(" ")
    if inst == "nop":
        l[idx] = " ".join(["jmp", val])
    elif inst == "jmp":
        l[idx] = " ".join(["nop", val])
    is_infinite, acc = interpreter(l)
    if not is_infinite:
        print("Ans 2)", acc)
        break
    l[idx] = " ".join([inst, val])  # undo the instruction change
    idx += 1
