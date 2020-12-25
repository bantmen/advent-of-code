subject = 7

card = 1526110
door = 20175123

card_loop_size = 0
val = 1
while val != card:
    val *= subject
    val %= 20201227
    card_loop_size += 1
print(card_loop_size)

val = 1
for _ in range(card_loop_size):
    val *= door
    val %= 20201227
print("Ans 1)", val)
