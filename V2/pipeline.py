class Pipeline:
    def __init__(self, steps):
        self.steps = steps

    def run(self, input):
        """
        potential future improvement: batch using itertools and add to asyncio loop
        """
        results = []
        for element in self.steps(input):
            print(f'Processing element: {element}')
            results.append(element)
        return results
