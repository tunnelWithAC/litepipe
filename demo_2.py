
import logging
# import sys
# from statistics import median
#
#
# def stdin_source():
#     yield 1
#     # def try_to_int(val):
#     #     try:
#     #         return int(val)
#     #     except ValueError:
#     #         return None
#     #
#     # for input in sys.stdin:
#     #     if input.strip() == 'exit':
#     #         exit()
#     #
#     #     val = try_to_int(input)
#     #     if val is not None:
#     #         print('> %d' % val)
#     #         yield val
#
#
# def filter_numbers(numbers, predicate):
#     for val in numbers:
#         if predicate(val):
#             yield val
#
#
# def fixed_event_window(numbers, window_size):
#     arr = []
#     for val in numbers:
#         arr.append(val)
#
#         if len(arr) >= window_size:
#             res = arr.copy()
#             arr = []
#             yield res
#
#
# def fold_sum(arrs):
#     for arr in arrs:
#         yield sum(arr)
#
#
# def fold_median(arrs):
#     for arr in arrs:
#         yield median(arr)
#
#
# def stdout_sink(numbers):
#     for val in numbers:
#         print(val)
#         yield val
#
#
# numbers = stdin_source()
# filtered = filter_numbers(numbers, lambda x: x > 0)
# windowed_for_sum = fixed_event_window(filtered, 2)
# folded_sum = fold_sum(windowed_for_sum)
# windowed_for_median = fixed_event_window(folded_sum, 3)
# folded_median = fold_median(windowed_for_median)
# res = stdout_sink(folded_median)
#
# if __name__ == "__main__":
#     list(res)

#
# from itertools import chain
#
# def generator1():
#     for item in 'abcdef':
#         yield item
#
# def generator2():
#     for item in '123456':
#         yield item
#
# generator3 = chain(generator1(), generator2())
# for item in generator3:
#     print(item)


class T:
    def __init__(self, fn):
        self.fn = fn
        self.children = []

    def __rshift__(self, other):
        self.children.append(other)
        return other

    def __call__(self, input, *args, **kwargs):
        transform_output = self.fn(input)
        for child in self.children:
            yield from child(transform_output)

def add_one(inp):
    return inp + 1

def double(inp):
    return inp * 2


step_one = T(add_one)
step_two = T(double)

step_one >> step_two

step_one(2)


# def first_generator():
#     for i in range(5):
#         yield i
#
# def second_generator(numbers):
#     for n in numbers:
#         yield n * n
#
# def third_generator(numbers):
#     for n in numbers:
#         yield n * n * n
#
# def chain_generators():
#     numbers = first_generator()
#     yield from second_generator(numbers)
#     # yield from third_generator(numbers)
#
#
# for value in chain_generators():
#     print(value)
#
"""
input - yield
parent - yield from
child - yield
"""
def input():
    for i in range(5):
        yield i


class Tran:
    def __init__(self, fn):
        self.fn = fn
        self.children = []

    def __rshift__(self, other):
        self.children.append(other)
        # potential recursion issue
        return other

    def __call__(self, input, *args, **kwargs):
        for _inp in input:
            transform_output = self.fn(_inp)
            if len(self.children) > 0:
                for child in self.children:
                    yield from child(iter((transform_output,)))
            else:
                yield transform_output


def first_transform(numbers):
    # for n in numbers:
    #     # yield n * n
    #     yield second_transform(n)
    yield from sec(numbers)

def second_transform(n):
    # for n in numbers:
    # print(n*n*n)
    return n * n * n

def double(n):
    # for n in numbers:
    # print(n*n*n)
    return n * 2

def half(n):
    # for n in numbers:
    # print(n*n*n)
    with open(f'outout_{n}.txt', 'w') as f:
        # Write some text to the file
        f.write('Hello, world!')

    return n / 2

sec = Tran(second_transform)
b = Tran(double)
c = Tran(half)
d = Tran(half)
_print = Tran(print)

# sec >> b >> d

sec >> c >> d

def pipeline():
    numbers = input()
    yield from first_transform(numbers)
    # yield from third_generator(numbers)

#
# for value in pipeline():
#     print(value)


def is_iterator(obj):
    try:
        iter(obj)
        return True
    except TypeError:
        return False

class Pipeline:
    def __init__(self, steps):
        self.steps = steps

    def iterate(self, input):
        yield from self.steps(input)

    def run(self, input):
        for element in self.iterate(input):
            logging.info(f'Processing element: {element}')


numbers = input()
pipe = Pipeline(first_transform)
# for v in pipe.run(numbers):
#     print(v)

pipe.run(numbers)
# numbers = input()
# first_transform(numbers)