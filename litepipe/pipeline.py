from typing import Callable, List

from litepipe.pval import Pval
from litepipe.transform import Transform


class Pipeline:
    def __init__(self, transforms: Transform):
        """
        Executable collection of Transform objects

        :param transforms (Transform): a Transform object that 'steps' property contains one or more function that
        will be executed when the 'run' method of this class is called.
        """
        assert type(transforms) == Transform, '"transforms" is not type litepipe.Transform'

        self.result = None
        self.steps: List[Callable] = transforms.steps

    def run(self, input, return_pval=True):
        assert input is not None, 'input must not be None'

        result = self.result or input
        for step in self.steps:
            result = step(result)

        if return_pval:
            return Pval(result=result)
        return result
