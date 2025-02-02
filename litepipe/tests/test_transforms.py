import unittest

from litepipe.transform import Transform, GroupBy, Create
from litepipe.pipeline import Pipeline
from litepipe.examples.transforms import NoChange, Double, YieldMultipleOutputs, GroupCount, Filter


class TransformTestCase(unittest.TestCase):
    def test_single_transform(self):
        p = Pipeline()
        p | Create([1]) | Double()

        results = p.run()

        self.assertEqual([2], results)

    def test_transform_custom_init(self):
        class CustomInit(Transform):
            def __init__(self):
                super().__init__()
                self.multiplier = 2

            def expand(self, input):
                yield input * self.multiplier

        p = Pipeline()
        p | Create([1]) | CustomInit()

        results = p.run()

        self.assertEqual([2], results)


    def test_filter(self):
        p = Pipeline()
        p | Create([1, 2, 3, 6, 9, 15, 24]) | Filter()

        results = p.run()

        self.assertEqual([15, 24], results)

    def test_multiple_branches(self):
        p = Pipeline()
        filtered_items = p | Create([1, 2, 3, 6, 9, 15, 24]) | Filter()

        filtered_items | YieldMultipleOutputs()
        filtered_items | Double()

        results = p.run()

        self.assertEqual([15, 15, 24, 24, 30, 48], results)

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
         | Double()
         | Double()
         )

        results = p.run()

        self.assertEqual([4], results)

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
         | NoChange() >> 'DoNothing'
         | GroupBy() >> 'GroupBy')

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

    def test_pipeline_graph(self):
        p = Pipeline()
        (p
         | Create(["strawberry", "banana", "blueberry"])
         | NoChange() >> 'DoNothing'
         | GroupBy() >> 'GroupBy')

        self.assertEqual('Create -> (DoNothing -> (GroupBy -> ()))', p.graph)


if __name__ == '__main__':
    unittest.main()