"""
The Runner class is an abstraction of the logic called when a pipeline is run.
This class is used by the Pipeline and Pval class via Dependency Injection and called in their run method.
"""


class Runner:
    @staticmethod
    def run(pval):
        result = pval.result

        for index, step in enumerate(pval.steps):
            try:
                result = step(result)
            except Exception as e:
                pval.exception = str(e)
                pval.step = index

        pval.result = result
        return pval
