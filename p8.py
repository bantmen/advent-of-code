# https://adventofcode.com/2019/day/8

from collections import Counter
import numpy as np
from matplotlib.pyplot import imshow, show


BLACK, WHITE, TRANSPARENT = range(3)


def batch(iterable, size):
    l = []
    for i in iterable:
        l.append(i)
        if len(l) == size:
            yield l
            l = []


def render_image(image, rows, cols):
    a = np.array(image).reshape((rows, cols))
    imshow(a, cmap="bone")
    show()


with open("8.txt", "r") as f:
    encoded = list(map(int, f.readline()))

rows, cols = 6, 25

min_num_0 = float("inf")
ans = None
for layer in batch(encoded, size=rows * cols):
    counter = Counter(layer)
    if counter[0] < min_num_0:
        min_num_0 = counter[0]
        ans = counter[1] * counter[2]
print("1) Answer:", ans)

image = [TRANSPARENT] * (rows * cols)
for layer in batch(encoded, size=rows * cols):
    for i, num in enumerate(layer):
        if image[i] == TRANSPARENT:
            image[i] = num
render_image(image, rows, cols)
