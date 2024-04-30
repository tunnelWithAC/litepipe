import asyncio
from typing import Callable, List

from litepipe.pval import Pval
from litepipe.transform import Transform
from litepipe.runner import Runner


class Pipeline:
    def __init__(self, transforms: Transform):
        """
        Executable collection of Transform objects

        :param transforms (Transform): a Transform object that 'steps' property contains one or more function that
        will be executed when the 'run' method of this class is called.
        """
        assert isinstance(transforms, Transform), '"transforms" is not type litepipe.Transform'

        self.result = None
        self.steps: List[Callable] = transforms.steps

    def run(self, pipeline_input) -> Pval:
        assert pipeline_input is not None, 'input must not be None'

        result = self.result or pipeline_input
        pval = Pval(result)
        return Runner.run(pval, self.steps)

    async def iterate(self, elements):
        tasks = []

        async with asyncio.TaskGroup() as tg:
            for element in elements:
                t = tg.create_task(self.run(element))
                tasks.append(t)

        results = [t.result() for t in tasks]
        return results
