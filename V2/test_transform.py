import unittest

from transform import Transform, GroupBy, Create
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


class GroupCount(Transform):
    def expand(self, input):
        values = input["values"]
        key = input["key"]
        yield {"key": key, "length": len(values), "values": values}


class TransformTestCase(unittest.TestCase):
    def test_single_transform(self):
        p = Pipeline()
        p | Create([1]) | Double()

        results = p.run()

        self.assertEqual([2], results)

    def test_yield_multiple_transform(self):
        p = Pipeline()
        p | Create([1]) | YieldMultipleOutputs()

        results = p.run()

        self.assertEqual([1, 1], results)

    def test_yield_multiple_dict_transform(self):
        p = Pipeline()
        p | Create([{"name": "test"}]) | YieldMultipleOutputs()

        results = p.run()

        self.assertEqual([{"name": "test"}, {"name": "test"}], results)
    def test_chain_transform(self):
        p = Pipeline()
        p | Create([1]) | YieldMultipleOutputs() | Double()

        results = p.run()

        self.assertEqual([2, 2], results)

    def test_multiple_children_transform(self):
        p = Pipeline()
        y = YieldMultipleOutputs()
        y | Double()
        y | Double()
        p | Create([1]) | y

        results = p.run()

        self.assertEqual([2, 2, 2, 2], results)

    def test_multiple_steps_transform(self):
        p = Pipeline()

        (p
         | Create([1])
         | YieldMultipleOutputs()
         | Double()
         | Double()
         )

        results = p.run()

        self.assertEqual([4, 4], results)

    def test_groupby(self):
        p = Pipeline()
        p | Create(["strawberry", "banana", "blueberry"]) | GroupBy()

        results = p.run()

        expected = [[{'key': 's', 'values': ['strawberry']}],
                    [{'key': 'b', 'values': ['banana', 'blueberry']}]]
        self.assertEqual(expected, results)

    def test_groupby_following_transform(self):
        p = Pipeline()
        (p
         | Create(["strawberry", "banana", "blueberry"])
         | NoChange()
         | GroupBy())

        results = p.run()

        expected = [[{'key': 's', 'values': ['strawberry']}],
                    [{'key': 'b', 'values': ['banana', 'blueberry']}]]
        self.assertEqual(expected, results)

    def test_group_by_into_transform(self):
        p = Pipeline()
        p | Create(["strawberry", "banana", "blueberry"]) | GroupBy() | GroupCount()

        results = p.run()

        expected = [{'key': 's', 'values': ['strawberry'], 'length': 1},
                    {'key': 'b', 'values': ['banana', 'blueberry'], 'length': 2}]

        self.assertEqual(expected, results)


if __name__ == '__main__':
    unittest.main()
