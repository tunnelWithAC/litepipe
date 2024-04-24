class Pval:
    def __init__(self, result):
        self.result = result
        self.steps = []
        self.exception = None
        self.step = 0

    @property
    def has_error(self):
        return self.exception is not None


    def __rshift__(self, transform):
        self.steps.append(transform.fn)
        result = self.run()
        return Pval(result=result)

    def run(self):
        _input = self.result

        for step in self.steps:
            _input = step(_input)
        return _input
