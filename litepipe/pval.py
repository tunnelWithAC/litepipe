from typing import Any

from litepipe.runner import Runner

class Pval:
    def __init__(self, runner: Runner, result: Any, steps=[]):
        """

        :param runner:
        :param result:
        :param steps:
        """
        self.runner = runner
        self.result = result
        self.steps = steps
        self.exception = None
        self.step = 0

    @property
    def has_error(self):
        return self.exception is not None

    def __rshift__(self, transform):
        pval = type(self)(self.runner, self.result, [transform.fn])
        return self.runner.run(pval)
