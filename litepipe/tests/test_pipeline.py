import unittest

from litepipe.pipeline import Pipeline
from litepipe.transform import Transform


def add_two(x):
    return x + 2


class PipelineTest(unittest.TestCase):
    def setUp(self):
        self.add_transform = Transform(add_two)
        self.mock_side_effect = Transform(lambda x: x)

    def test_empty_pipeline__raises_value_error(self):
        with self.assertRaisesRegex(AssertionError, '"transforms" is not type litepipe.Transform'):
            Pipeline(None)

    def test_valid_pipeline_with_no_input__raises_value_error(self):
        pipeline = Pipeline(self.add_transform)

        with self.assertRaisesRegex(AssertionError, 'input must not be None'):
            pipeline.run(None)

    def test_valid_pipeline_with_valid_input__returns_expected_value(self):
        pipeline = Pipeline(self.add_transform)

        result = pipeline.run(2)

        self.assertEqual(result, 4)
