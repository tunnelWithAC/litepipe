from typing import Callable, List


class Transform:
    def __init__(self, fn: Callable, steps: List[Callable] = None):
        """
        :param fn (Callable): A Python function that should be called when the transform is executed as part of a
            pipeline.
        :param steps (List[Callable]): A list of Python functions that are chained together whenever Transforms are
            chained using the rshift (>>) operator.
        """
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
