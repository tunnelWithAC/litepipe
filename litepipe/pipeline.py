import asyncio
# from typing import Callable, List
import types
import logging
from litepipe.pval import Pval
from litepipe.transform import Transform
# from litepipe.runner import Runner


class Pipeline:
    def __init__(self, start: Transform):
        """
        Executable collection of Transform objects

        :param transforms (Transform): a Transform object that 'steps' property contains one or more function that
        will be executed when the 'run' method of this class is called.
        """
        assert isinstance(start, Transform), '"transforms" is not type litepipe.Transform'
        self.start = start
        # self.result = None
        # self.steps: List[Callable] = transforms.steps

    def run(self, pipeline_input, collect=False):
        assert pipeline_input is not None, 'input must not be None'
        if collect is True:
            outputs = []
            pipe_output = self._previsitor(self.start, pipeline_input)
            for g in pipe_output:
                outputs.append(Pval(g))
            return outputs
        # elif collect is False:
            # yield self._previsitor(self.start, pipeline_input)
        # result = self.result or pipeline_input
        # pval = Pval(result)
        # return Runner.run(pval, self.steps)

    def collect(self, pipeline_output):
        outputs = []

        for g in pipeline_output:
            outputs.append(g)
        return outputs

    def _previsitor(self, tree, val):
        """Traverse tree in preorder applying a function to every node.

        Parameters
        ----------
        tree: TreeNode
            The tree to be visited.
        """
        fn_out = tree.fn(val)
        if isinstance(fn_out, types.GeneratorType):
            try:
                for fn_output in fn_out:
                    for child in tree.steps:
                        self._previsitor(child, fn_output)
            except Exception as e:
                logging.error("Exception occurred")
                # pval = Pval(fn_out)
                # pval.exception = str(e)
                # yield pval
        yield fn_out
    # async def iterate(self, elements):
    #     tasks = []
    #
    #     async with asyncio.TaskGroup() as tg:
    #         for element in elements:
    #             t = tg.create_task(self.run(element))
    #             tasks.append(t)
    #
    #     results = [t.result() for t in tasks]
    #     return results
