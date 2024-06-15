class Transform:
    def __init__(self):
        self.children = []

    def __rshift__(self, other):
        self.children.append(other)
        return other

    def __call__(self, input):
        # this may need to be revised in order to use groupby
        """
        currently we process per input

        for groups we want to process the iterator
        """
        groupbys = []
        transforms = []
        for c in self.children:
            if isinstance(c, GroupBy):
                groupbys.append(c)
            else:
                transforms.append(c)

        transform_outputs = map(self.expand, input)

        if len(groupbys) > 0:
            collected = [next(t) for t in transform_outputs]
            for g in groupbys:
                # t = list(transform_outputs)
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

    # def iterate_children(self, transform_output, children):
    #     pass


class GroupBy(Transform):
    # def __init__(self, get_key_fn):
    #     self.get_key_fn = get_key_fn
    def __init__(self):
        # super.__init__()
        super().__init__()

    def iterate_children(self, transform_output, children):
        parent = super()
        return parent.iterate_children(transform_output, children)

    def __call__(self, input):
        """
        input: (x, 4), (y, 14), (z, 3), (x, 4),
        expected output: (x, 7), (y, 14), (z, 3)
        function: sum_iterables
        """
        from itertools import groupby

        # if not isinstance(input, list):
        #     input = list(input)


        groups = {}
        for key, group in groupby(input, self.get_key()):
            if key not in groups.keys():
                groups[key] = []
            for g in group:
                groups[key].append(g)

        yield from self.iterate_children(groups, self.children)

    def get_key(self):

        return lambda x: x[0]

#
# class Temp(Transform):
#     def __init__(self):
#         s = super()
#         super().__init__()
