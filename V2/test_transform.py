import unittest

from transform import Transform, GroupBy
from pipeline import Pipeline


class NoChange(Transform):
    def expand(self, input):
        return input


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


    def test_group_by_0(self):
        start = NoChange()
        start >> GroupBy()
        pipe = Pipeline(start)

        results = pipe.run(["strawberry", "banana", "blueberry"])

        expected = [{'s': ['strawberry'], 'b': ['banana', 'blueberry']}]

        self.assertEqual(results, expected)


    def test_group_by_1(self):
        pipe = Pipeline(GroupBy())

        results = pipe.run(["strawberry", "banana", "blueberry"])

        expected = [{'s': ['strawberry'], 'b': ['banana', 'blueberry']}]

        self.assertEqual(results, expected)

    def test_group_by_into_transform(self):
        start = NoChange()
        start >> GroupBy()
        pipe = Pipeline(start)

        results = pipe.run(["strawberry", "banana", "blueberry"])

        expected = [{'s': ['strawberry'], 'b': ['banana', 'blueberry']}]

        self.assertEqual(results, expected)


if __name__ == '__main__':
    unittest.main()
