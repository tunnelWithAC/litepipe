from typing import Any

from litepipe.runner import Runner


class Pval:
    def __init__(self, result: Any):
        """
        :param result: The result of a pipeline execution. Instances of this class should primarily be created
        by running the Pipeline classes run method or as the result of chaining a transform to an existing Pval object.
        """
        self.result = result
        self.exception = None
        self.step = 0

    @property
    def has_error(self):
        return self.exception is not None

    def __rshift__(self, transform):
        pval = type(self)(self.result)
        return Runner.run(pval, [transform.fn])
