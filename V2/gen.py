# def expand(i):
#     yield i
#
#
# # input = ["strawberry", "banana", "blueberry"]
# input = [[{'key': 's', 'values': ['strawberry']}], [{'key': 'b', 'values': ['banana', 'blueberry']}]]
#
# collected_values = []
# for output in map(expand, input):
#     # use try/except as quick hack for checking if output is iterable
#     try:
#         # do this for transforms
#         for o in output:
#             collected_values.append(o)
#     except:
#         collected_values.append(output)
#
# group_collected_values = []
# for output in map(expand, input):
#     # use try/except as quick hack for checking if output is iterable
#     try:
#         group_collected_values.append(next(output))
#     except:
#         group_collected_values.append(output)
#
#
# o = [x for x in map(expand, input)]
# print(collected_values)
# print(group_collected_values)


class Transform:
    def __init__(self):
        self.children = []
        self.label = 'Unknown'

    def __or__(self, child):
        self.children.append(child)
        return child

    def __rshift__(self, label):
        self.label = label
        return self

    def expand(self):
        raise NotImplementedError()

    def __call__(self, input):
        transform_output = self.expand(input)
        for child in self.children:
            transform_output = child(transform_output)
        return transform_output


class Double(Transform):
    def expand(self, input):
        print(self.label)
        return input * 2


class Square(Transform):
    def expand(self, input):
        print(self.label)
        return input * input


class Pipeline:

    def __init__(self, start):
        self.start = start

    def run(self, input):
        return self.start(input)

start = Double()
start >> 'Double'
start | Square()
pipeline = Pipeline(start)

print(pipeline.run(2))  # returns 16