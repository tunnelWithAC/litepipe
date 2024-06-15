import unittest

from litepipe import Pipeline, Transform, t, Pval
from litepipe.util.testing import assert_equal


def add_two(x):
    new_result = x + 2
    return new_result


class PipelineTest(unittest.TestCase):
    def setUp(self):
        self.add_transform = Transform(add_two)
        self.mock_side_effect = Transform(lambda x: x)

    def test_empty_pipeline__raises_value_error(self):
        with self.assertRaisesRegex(AssertionError, '"transforms" is not type litepipe.Transform'):
            Pipeline(None)

    def test_valid_pipeline_with_no_input__raises_value_error(self):

        with self.assertRaisesRegex(AssertionError, 'input must not be None'):
            pipeline = Pipeline(self.add_transform)

            pipeline.run(None)

    def test_valid_pipeline_with_valid_input__returns_expected_value(self):
        pipeline = Pipeline(self.add_transform)

        pvals = pipeline.run(2, collect=True)

        # self.assertEqual(pval.result, 4)
        assert_equal(pvals, [Pval(4)])

    def test_pipeline_with_error_steps__returns_pval_with_error_details(self):
        @t
        def err_transform(_):
            raise ValueError("this isn't valid")

        pvals = Pipeline(self.add_transform >> err_transform).run(0, collect=True)

        expected_pval = Pval(None)
        expected_pval.exception = "this isn't valid"
        # self.assertEqual(pval.exception, "this isn't valid")
        # self.assertEqual(pvals, [expected_pval])
        assert_equal(pvals, [expected_pval])
