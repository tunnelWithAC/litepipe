from litepipe import Pipeline, Transform, Create, GroupBy


class NoChange(Transform):
    def expand(self, input):
        yield input


class Double(Transform):
    def expand(self, input):
        yield input * 2


class YieldMultipleOutputs(Transform):
    def expand(self, input):
        yield input
        yield input


class GroupCount(Transform):
    def expand(self, input):
        values = input["values"]
        key = input["key"]
        yield {"key": key, "length": len(values), "values": values}


class Filter(Transform):
    def expand(self, input):
        if input > 10:
            yield input
