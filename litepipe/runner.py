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
        """
        Notes from me to me
        - See if I can create an abstract for transform where __call__ must be implemented
        - Calling this function for transform will return a value / exception
        - Calling it for a filter will return 
         
        """
        for index, step in enumerate(steps):
            if pval.result is not None:
                try:
                    new_pval.result = step(pval.result)
                except Exception as e:
                    new_pval.exception = str(e)
                    new_pval.step = index
        return new_pval
