import logging
import time


class Transform:
    def __init__(self):
        # self.expand = expand
        self.children = []

    def __rshift__(self, other):
        self.children.append(other)
        # potential recursion issue
        return other

    def __call__(self, input):
        for _inp in input:
            transform_output = self.expand(_inp)
            if self.is_iterator(transform_output):
                for output_item in transform_output:
                    yield from self.__iterate_children(output_item, self.children)
            else:
                yield from self.__iterate_children(transform_output, self.children)

    @staticmethod
    def is_iterator(obj):
        try:
            iter(obj)
            return True
        except TypeError:
            return False

    def __iterate_children(self, transform_output, children):
        if len(children) > 0:
            for child in children:
                yield from child(iter((transform_output,)))
        else:
            yield transform_output

      # def expand(self, input_or_inputs: InputT) -> OutputT:
      #   raise NotImplementedError

    def expand(self, input_or_inputs):
        raise NotImplementedError


class Pipeline:
    def __init__(self, steps):
        self.steps = steps

    # def iterate(self, input):
    #     for element in self.steps(input):
    #         logging.info(f'Processing element: {element}')

    def run(self, input):
        """
        potential future improvement: batch using itertools and add to asyncio loop
        """
        for element in self.steps(input):
            print(f'Processing element: {element}')



def create_file(n, step='output'):
    from datetime import datetime
    now = datetime.now().timestamp()
    print(f'{step}{n}_{int(now)}.txt')


class Double(Transform):
    # def __init__(self):
    #     super.__init__(self.expand)
    # @property
    def expand(self, n):
        return n * n * n


def second_transform(n):
    yield n * n * n

# sec = Transform(second_transform)


class Cube(Transform):
    def expand(self, n):
        yield n * n * n


# def double(n):
#     create_file(n, 'double')
#     yield n * 2 * 2
#     yield n

# d = Transform(double)

class Double(Transform):
    def expand(self, n):
        create_file(n, 'double')
        yield n * 2 * 2
        yield n

def write_to_file(n):
    create_file(n)
    yield n


# c = Transform(write_to_file)

class WriteToFile(Transform):
    def expand(self, input_or_inputs):
        create_file(input_or_inputs)
        yield input_or_inputs

c = Cube()
c >> Double() >> WriteToFile()

pipe = Pipeline(c)

pipe.run([1,2])
"""
expected
double1_1718138638.txt
output4_1718138638.txt
Processing element: 4
output1_1718138638.txt
Processing element: 1
double8_1718138638.txt
output32_1718138638.txt
Processing element: 32
output8_1718138638.txt
Processing element: 8
"""

"""
actual
double1_1718138930.txt
output4_1718138930.txt
Processing element: 4
output1_1718138930.txt
Processing element: 1
double8_1718138930.txt
output32_1718138930.txt
Processing element: 32
output8_1718138930.txt
Processing element: 8
"""