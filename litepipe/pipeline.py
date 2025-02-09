from litepipe import Transform


class Pipeline:
    def __init__(self):
        self.start = None

    def __or__(self, start: Transform):
        self.start = start
        return start

    def run(self):
        results = []
        for element in self.start():
            results.append(element)
        return results

    def stream(self):
        if self.start.streaming_enabled is not True:
            raise ValueError(f"stream() is not supported by {str(self.start)}")
        # In streaming mode the first Transform in the pipeline is responsible for
        # keeping the main thread active
        self.start()

    @property
    def graph(self):
        return str(self.start)