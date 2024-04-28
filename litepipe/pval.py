from typing import Any, List

from litepipe.runner import Runner
from litepipe.transform import Transform


class Pval:
    def __init__(self, runner: Runner, result: Any, steps=None):
        """

        :param runner:
        :param result:
        :param steps:
        """
        self.runner = runner
        self.result = result
        if steps is None:
            self.steps: List[Transform] = []
        else:
            self.steps = steps
        self.exception = None
        self.step = 0

    @property
    def has_error(self):
        return self.exception is not None

    def __rshift__(self, transform):
        pval = type(self)(self.runner, self.result, [transform.fn])
        return self.runner.run(pval)
