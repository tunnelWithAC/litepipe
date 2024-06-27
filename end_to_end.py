class Transform:
    def __init__(self):
        self.children = []

    def __rshift__(self, other):
        self.children.append(other)
        return other

    def __call__(self, input):
        # this may need to be revised in order to use groupby
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

    def expand(self, input_or_inputs):
        raise NotImplementedError

    # def __iterate_children(self, transform_output, children):
    #     pass


class GroupBy(Transform):
    # def __init__(self, get_key_fn):
    #     self.get_key_fn = get_key_fn
    def __init__(self):
        # super.__init__()
        super().__init__()

    def __iterate_children(self):
        parent = super()
        return parent.__iterate_children()

    def __call__(self, input):
        """
        input: (x, 4), (y, 14), (z, 3), (x, 4),
        expected output: (x, 7), (y, 14), (z, 3)
        function: sum_iterables
        """
        from itertools import groupby

        groups = {}
        for key, group in groupby(input, self.get_key()):
            if key not in groups.keys():
                groups[key] = []
            for g in group:
                groups[key].append(g)

        for ele in groups.items():
            yield from self.__iterate_children()
            # pa  = super

    def get_key(self):
        # if self.get_key_fn is not None:
        #     return self.get_key_fn
        return lambda x: x[0]


class Temp(Transform):
    def __init__(self):
        s = super()
        super().__init__()


t = Temp()
class Pipeline:
    def __init__(self, steps):
        self.steps = steps

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


class Cube(Transform):
    def expand(self, n):
        yield n * n * n


class Double(Transform):
    def expand(self, n):
        yield n * 2 * 2
        # yield ('1', n)
        yield n

# https://realpython.com/python-filter-function/
class Filter(Transform):
    def expand(self, n):
        if n > 10:
            yield n


class WriteToFile(Transform):
    def expand(self, input_or_inputs):
        # create_file(input_or_inputs)
        yield input_or_inputs


c = Cube()
g = GroupBy()
c >> Double() >> Filter() >> WriteToFile()

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


class T:
    def print(self):
        print("T")

class G(T):
    def print(self):
        super().print()

_g  = G()
_g.print()