from transform import Transform, GroupBy, Temp


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

class CreateGroups(Transform):
    def expand(self, n):
        # yield n * 2 * 2
        yield ('1', n)
        # yield n


# https://realpython.com/python-filter-function/
class Filter(Transform):
    def expand(self, n):
        if n > 10:
            yield n


class WriteToFile(Transform):
    def expand(self, input_or_inputs):
        # create_file(input_or_inputs)
        yield input_or_inputs

class T:
    def print(self):
        print("T")

class G(T):
    def print(self):
        super().print()

