import time
from contextlib import ContextDecorator


class Timer(ContextDecorator):
    def __init__(self, name=""):
        self.name = name

    def __enter__(self):
        self.start = time.time()

    def __exit__(self, *_):
        print(self.name, "took:", round((time.time() - self.start) * 1000, 3), "ms")
