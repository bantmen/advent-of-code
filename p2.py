# https://adventofcode.com/2019/day/2

def run_program(noun, verb, l):
    l[1] = noun
    l[2] = verb
    idx = 0
    while l[idx] != 99:
        if l[idx] == 1:
            l[l[idx + 3]] = l[l[idx + 1]] + l[l[idx + 2]]
            idx += 4
        elif l[idx] == 2:
            l[l[idx + 3]] = l[l[idx + 1]] * l[l[idx + 2]]
            idx += 4
        else:
            assert l[idx] == 99
    return l[0]

def solve(l):
    for noun in range(100):
        for verb in range(100):
            if run_program(noun, verb, l.copy()) == 19690720:
                return noun, verb
    assert False 

with open('2.txt', 'r') as f:
    l = list(map(int, f.readline().split(',')))

noun, verb = solve(l)

ans = 100 * noun + verb

print("Answer:", ans)

