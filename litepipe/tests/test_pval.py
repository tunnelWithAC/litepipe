import unittest

from litepipe import Pipeline, Pval, Transform, t


@t
def double(x):
    return x * 2


class PvalTest(unittest.TestCase):

    def test_right_shift_appends_single_transform_to_result(self):
        add_transform = Transform(lambda x: x + 2)
        result = Pipeline(add_transform).run(2)

        pval: Pval = result >> double

        self.assertEqual(8, pval.result)

    def test_right_shift_appends_multiple_transforms_to_result(self):
        result = Pipeline(double).run(2)

        pval: Pval = result >> double >> double

        self.assertEqual(16, pval.result)

    def test_chain_multiple_transforms__run_independently(self):
        result = Pipeline(double).run(2)
        result >> double

        pval: Pval = result >> double >> double

        self.assertEqual(16, pval.result)
