s = """1 + (2 * 3) + (4 * (5 + 6))
2 * 3 + (4 * 5)
((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2"""

s = open("day18.txt").read()


def backwards_index(l, c):
    for i in range(len(l) - 1, -1, -1):
        if l[i] == c:
            return i
    assert False


def eval_simple_expr(stack):
    stack.reverse()  # left-to-right
    while len(stack) > 1:
        x, op, x2 = stack.pop(), stack.pop(), stack.pop()
        if op == "+":
            stack.append(x + x2)
        else:  # op == "*"
            stack.append(x * x2)
    assert len(stack) == 1
    return stack[0]


def eval_simple_expr2(stack):
    stack2 = []
    for c in stack:
        if stack2 and stack2[-1] == "+":
            stack2.pop()
            stack2.append(stack2.pop() + c)
        else:
            stack2.append(c)
    while len(stack2) > 1:
        x, op, x2 = stack2.pop(), stack2.pop(), stack2.pop()
        assert op == "*", op
        stack2.append(x * x2)
    return stack2[-1]


ans = 0

for line in s.split("\n"):
    stack = []
    for c in "(" + line + ")":
        if c == " ":
            continue
        elif c in ("+", "*", "("):
            stack.append(c)
        elif c == ")":
            start_idx = backwards_index(stack, "(")
            stack[start_idx:] = [eval_simple_expr(stack[start_idx + 1 :])]
        else:
            stack.append(int(c))
    assert len(stack) == 1
    ans += stack[-1]

print("Ans 1)", ans)

ans = 0

for line in s.split("\n"):
    stack = []
    for c in "(" + line + ")":
        if c == " ":
            continue
        elif c in ("+", "*", "("):
            stack.append(c)
        elif c == ")":
            start_idx = backwards_index(stack, "(")
            stack[start_idx:] = [eval_simple_expr2(stack[start_idx + 1 :])]
        else:
            stack.append(int(c))
    assert len(stack) == 1
    ans += stack[-1]

print("Ans 2)", ans)
