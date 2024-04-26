class Runner:
    def run(self, pval):
        result = pval.result

        for index, step in enumerate(pval.steps):
            try:
                result = step(result)
            except Exception as e:
                pval.exception = str(e)
                pval.step = index

        pval.result = result
        pval.steps = []
        return pval
