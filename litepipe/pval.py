class Pval:
    def __init__(self, result):
        self.result = result
        self.steps = []

    def __rshift__(self, transform):
        self.steps.append(transform.fn)
        result = self.run()
        return Pval(result=result)

    def run(self):
        _input = self.result

        for step in self.steps:
            _input = step(_input)
        return _input
