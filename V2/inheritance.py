class Transform:
    def __init__(self):
        print("init")
    #     self.children = []

    def __rshift__(self, other):
        raise NotImplementedError
    def __call__(self, input):
        raise NotImplementedError
    @staticmethod
    def is_iterator(obj):
        raise NotImplementedError

    def iterate_children(self, transform_output, children):
        raise NotImplementedError

    def expand(self, input_or_inputs):
        # raise NotImplementedError
        print("Parent")


class GroupBy(Transform):
    # def __init__(self, get_key_fn):
    #     self.get_key_fn = get_key_fn
    def __init__(self):
        # super.__init__()
        x = super()
        super().__init__()

    def expand(self, _input):
        super().expand([])
        super().iterate_children([],[])


g = GroupBy()
g.expand("saa")

class T:
    def print(self):
        print("T")

class G(T):
    def print(self):
        x = super()
        super().print()
#
# _g  = G()
# _g.print()