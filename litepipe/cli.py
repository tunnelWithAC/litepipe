"""

class CliHandler(ABC):

    def deploy(self):
        pass


create implementations for different cloud providers
deploy as cloud function
when pipeline is deployed - create a pub/sub topic and pass it as env param to function
"""
from typing import List

from abc import ABC


class AbstractStep(ABC):
    def run(self):
        pass


class Step(AbstractStep):
    def __init__(self, steps: List[AbstractStep]):
        self.steps = steps

    def run(self):
        for step in self.steps:
            print("Hello")