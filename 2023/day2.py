s = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""

s = open("day2.txt").read()

num_blue = 14
num_red = 12
num_green = 13

ret = 0
ret2 = 0

for i, line in enumerate(s.split("\n")):
    _, lst = line.split(": ")
    max_blue = max_red = max_green = float("-inf")
    for subset in lst.split("; "):
        blue = red = green = 0
        for pick in subset.split(", "):
            x, _ = pick.split(" ")
            x = int(x)
            if "blue" in pick:
                blue = x
            elif "red" in pick:
                red = x
            else:
                green = x
        max_blue = max(max_blue, blue)
        max_red = max(max_red, red)
        max_green = max(max_green, green)
    if num_blue >= max_blue and num_red >= max_red and num_green >= max_green:
        ret += i + 1
    ret2 += max_blue * max_red * max_green

print("Part 1)", ret)
print("Part 2)", ret2)
