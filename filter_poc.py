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
            self.steps = []
        self.fn = fn

    @property
    def len_steps(self):
        return len(self.steps)

    def __rshift__(self, transform):
        self.steps.append(transform)
        return self

    # def run(self, input):
    #     transform_output = self.fn(input)
    #     for step in self.steps:
    #         current_step_val = self.fn(input)
    #         step(current_step_val)
    #         # transform_output = step(transform_output)
    def __call__(self, input):
        transform_output = self.fn(input)
        # steps = [self.fn] +
        for index, step in enumerate(self.steps):
            transform_output = step.fn(transform_output)
            step(transform_output)            # transform_output = step(transform_output)
            print(index, transform_output)

    def run(self, input):
        input = self.fn(input)
        for step in self.steps:
            yield step(input)


class Filter:
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
            self.steps = []
        self.fn = fn

    def __rshift__(self, transform):
        self.steps.append(transform)
        return self

    def __call__(self, input):
        is_true = self.fn(input)
        if is_true:
            for step in self.steps:
                step(input)

    def run(self, input):
        if self.fn(input):
            return input
        # return

def t(x) -> Transform:
    return Transform(x)


def add_transform(x):
    print("add_transform")
    return x + 2


t_add_transform = t(add_transform)


def add_transform_two_fn(x):
    print("add_transform_two_fn")
    return x + 2


add_transform_two = Transform(add_transform_two_fn)


def print_fn(x):
    print(x)


lambda_print = Transform(print_fn)


greater_than = Filter(lambda x: x > 2)

t_add_transform >> add_transform_two >> greater_than >> lambda_print

# for x in add_transform.run(2):
#     print(x)

# res = t_add_transform.fn(2)
# 2 + 2 + 2
# t_add_transform(2)

