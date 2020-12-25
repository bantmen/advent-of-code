s = "219748365"

l = list(map(int, s))
l.extend(range(10, 1000001))
ma = max(l)

num_moves = 10000000

d = [None] * (len(l) + 1)


class Node:
    def __init__(self, val, nxt=None):
        self.val = val
        self.next = nxt
        # assert val not in d
        d[val] = self

    def print(self):
        l = [self.val]
        cur = self.next
        while cur is not None and cur.val not in l:
            l.append(cur.val)
            cur = cur.next
        l.append(None if cur is None else cur.val)
        print(" -> ".join(str(x) for x in l))

    # Only works when non-circular
    def values(self):
        l = []
        cur = self
        while cur is not None:
            l.append(cur.val)
            cur = cur.next
        return l


nodes = [Node(x) for x in l]
for i in range(len(nodes) - 1):
    nodes[i].next = nodes[i + 1]
# Circular
nodes[len(nodes) - 1].next = nodes[0]

# Returns the head and tail of the removed segment.
def remove(node, n_after):
    head = node.next
    cur = node
    for _ in range(n_after):
        cur = cur.next
    node.next = cur.next
    cur.next = None
    return head, cur


def insert(node, head, tail):
    temp = node.next
    node.next = head
    tail.next = temp


def grab(node, n):
    l = []
    cur = node
    for _ in range(n):
        l.append(cur.val)
        cur = cur.next
    return l


cur = nodes[0]

for _ in range(num_moves):
    pick, pick_tail = remove(cur, 3)

    dest = cur.val - 1
    if dest == 0:
        dest = ma
    while dest in (pick.val, pick.next.val, pick_tail.val):
        dest -= 1
        if dest == 0:
            dest = ma
    dest_node = d[dest]

    insert(dest_node, pick, pick_tail)

    cur = cur.next

# 35827964
# print("Ans 1)", "".join([str(v) for v in grab(d[1].next, 8)]) )

fst, snd = grab(d[1].next, 2)
# 5403610688
print("Ans 2)", fst * snd)
