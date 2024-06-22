from itertools import groupby


class Transform:
    def __init__(self):
        self.children = []

    def __rshift__(self, other):
        self.children.append(other)
        return other

    def __or__(self, other):
        self.children.append(other)
        return other

    def __call__(self, input):
        groupbys = []
        transforms = []
        # inputs are processed differently based on regular transform (per input) vs groupby
        for child in self.children:
            if isinstance(child, GroupBy) or issubclass(type(child), GroupBy):
                groupbys.append(child)
            else:
                transforms.append(child)

        transform_outputs = map(self.expand, input)

        if len(groupbys) > 0:
            collected_values = []
            for output in transform_outputs:
                # use try/except as quick hack for checking if output is iterable
                try:
                    collected_values.append(next(output))
                except:
                    collected_values.append(output)
            for child in groupbys:
                yield from child(collected_values)

        for transform_output in transform_outputs:
            if self.is_iterator(transform_output):
                for output_item in transform_output:
                    yield from self.iterate_children(output_item, transforms)
            else:
                yield from self.iterate_children(transform_output, transforms)

    def iterate_children(self, transform_output, children):
        if len(children) > 0:
            for child in children:
                yield from child(iter((transform_output,)))
        else:
            yield transform_output
    @staticmethod
    def is_iterator(obj):
        try:
            iter(obj)
            return True
        except TypeError:
            return False

    def expand(self, input_or_inputs):
        raise NotImplementedError

class Create(Transform):
    def __init__(self, input_or_inputs):
        super().__init__()
        self.input_or_inputs = input_or_inputs

    def expand(self, input_or_inputs):
        yield input_or_inputs

    def __call__(self, _):
        yield from super().__call__(self.input_or_inputs)


class GroupBy(Transform):
    def __init__(self):
        super().__init__()

    def iterate_children(self, transform_output, children):
        parent = super()
        return parent.iterate_children(transform_output, children)

    def __call__(self, input):
        groups = {}
        for key, group in groupby(input, self.get_key()):
            if key not in groups.keys():
                groups[key] = []
            for g in group:
                groups[key].append(g)

        yield from self.iterate_children(groups, self.children)

    @staticmethod
    def get_key():
        return lambda x: x[0]


class NamedTransform(Transform):
    def __init__(self):
        super().__init__()
        self.label = "Unknown"
    def __rshift__(self, label):
        self.label = label
