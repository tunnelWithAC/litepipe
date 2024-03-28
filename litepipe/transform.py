from typing import Callable, List


class Transform:
    def __init__(self, fn: Callable, steps: List[Callable] = None):
        if steps is not None:
            self.steps = steps
        else:
            self.steps = [fn]
        self.fn = fn

    def __rshift__(self, transform):
        self.steps.append(transform.fn)
        return type(self)(self.fn, self.steps)


def t(x) -> Transform:
    return Transform(x)
