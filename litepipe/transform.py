from typing import Callable


class Transform:
    def __init__(self, fn: Callable):
        """
        :param fn (Callable): A Python function that should be called when the transform is executed as part of a
            pipeline.
        :param steps (List[Callable]): A list of Python functions that are chained together whenever Transforms are
            chained using the rshift (>>) operator.
        """
        # if steps is not None:
        #     self.steps = steps
        # else:
        #     self.steps = [fn]
        self.steps = []
        self.fn = fn

    def __rshift__(self, transform):
        self.steps.append(transform.fn)
        # return type(self)(self.fn, self.steps)
        return transform

    def __call__(self, input):
        for _inp in input:
            transform_output = self.fn(_inp)
            if len(self.steps) > 0:
                for child in self.steps:
                    yield from child(iter((transform_output,)))
            else:
                yield transform_output

# class Filter:
#     def __init__(self, fn: Callable, steps: List[Callable] = None):
#         """
#         :param fn (Callable): A Python function that should be called when the transform is executed as part of a
#             pipeline.
#         :param steps (List[Callable]): A list of Python functions that are chained together whenever Transforms are
#             chained using the rshift (>>) operator.
#         """
#         if steps is not None:
#             self.steps = steps
#         else:
#             self.steps = [fn]
#         self.fn = fn
#
#     def __rshift__(self, transform):
#         # self.steps[:-1].steps.append(transform.fn)
#         self.steps.append(transform.fn)
#         # return type(self)(self.fn, self.steps)
#         return transform


def t(x) -> Transform:
    return Transform(x)
