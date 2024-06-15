import unittest

from transform import Transform, GroupBy
from pipeline import Pipeline


class NoChange(Transform):
    def expand(self, input):
        yield input


class Double(Transform):
    def expand(self, input):
        yield input * 2


class YieldMultipleOutputs(Transform):
    def expand(self, input):
        yield input
        yield input


class MyTestCase(unittest.TestCase):
    def test_single_transform(self):
        pipe = Pipeline(NoChange())

        results = pipe.run([1])

        self.assertEqual([1], results)

    def test_yield_multiple_transform(self):
        pipe = Pipeline(YieldMultipleOutputs())

        results = pipe.run([1])

        self.assertEqual([1, 1], results)


    def test_chain_transform(self):
        y = YieldMultipleOutputs()
        y >> Double()
        pipe = Pipeline(y)

        results = pipe.run([1])

        self.assertEqual([2, 2], results)

    def test_multiple_children_transform(self):
        y = YieldMultipleOutputs()
        y >> Double()
        y >> Double()
        pipe = Pipeline(y)

        results = pipe.run([1])

        self.assertEqual([2, 2, 2, 2], results)

    def test_multiple_steps_transform(self):
        y = YieldMultipleOutputs()
        y >> Double() >> Double()
        pipe = Pipeline(y)

        results = pipe.run([1])

        self.assertEqual([4, 4], results)


    def test_group_by(self):
        start = NoChange()
        start >> GroupBy()
        pipe = Pipeline(start)

        results = pipe.run(["strawberry", "banana", "blueberry"])

        expected = [{'s': ['strawberry'], 'b': ['banana', 'blueberry']}]

        self.assertEqual(results, expected)
    # def test_multiple_children_on_separate_branches(self):
    #     root  = NoChange()
    #     steps = YieldMultipleOutputs() >> Double()
    #     pipe = Pipeline(steps)
    #
    #     results = pipe.run([1])
    #
    #     self.assertEqual([2], results)


if __name__ == '__main__':
    unittest.main()
