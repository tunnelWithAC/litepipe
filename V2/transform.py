from itertools import groupby


class Transform:
    def __init__(self):
        self.children = []

    def __rshift__(self, other):
        self.children.append(other)
        return other

    def __call__(self, input):
        groupbys = []
        transforms = []
        # inputs are processed differently based on regular transform (per input) vs groupby
        for child in self.children:
            if isinstance(child, GroupBy):
                groupbys.append(child)
            else:
                transforms.append(child)

        transform_outputs = map(self.expand, input)

        if len(groupbys) > 0:
            collected = []
            for output in transform_outputs:
                # use try/except as quick hack for checking if output is iterable
                try:
                    collected.append(next(output))
                except:
                    collected.append(output)
            for g in groupbys:
                yield from g(collected)

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
