class Pipeline:
    def __init__(self):
        self.start = None
        self.pipeline_input = None

    def create(self, pipeline_input):
        self.pipeline_input = pipeline_input
        return self

    def __rshift__(self, start):
        self.start = start
        # return self
        return start

    def __or__(self, start):
        self.start = start
        # return self
        return start

    def run(self):
        """
        potential future improvement: batch using itertools and add to asyncio loop
        """
        results = []
        for element in self.start(self.pipeline_input):
            results.append(element)
        return results
