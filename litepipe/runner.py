class Runner:
    """
    The Runner class is an abstraction of the logic called when a pipeline is run.
    This class is used by the Pipeline and Pval class via Dependency Injection and called in their run method.
    """
    @staticmethod
    def run(pval, steps):
        # Import here to avoid circular imports
        from litepipe.pval import Pval

        assert isinstance(pval, Pval), '"pval" is not type litepipe.Pval'

        new_pval = Pval(pval.result)
        for index, step in enumerate(steps):
            try:
                new_pval.result = step(pval.result)
            except Exception as e:
                new_pval.exception = str(e)
                new_pval.step = index
        return new_pval
