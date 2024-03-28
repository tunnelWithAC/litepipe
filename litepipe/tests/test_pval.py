import unittest

from litepipe.pipeline import Pipeline
from litepipe.pval import Pval
from litepipe.transform import Transform, t


@t
def double(x):
    return x * 2


class PvalTest(unittest.TestCase):

    def test_right_shift_appends_single_transform_to_result(self):
        add_transform = Transform(lambda x: x + 2)
        result = Pipeline(add_transform).run(2)

        pval = Pval(result=result) >> double

        self.assertEqual(8, pval)

    def test_right_shift_appends_multiple_transforms_to_result(self):
        result = Pipeline(double).run(2)

        pval = result >> double >> double

        self.assertEqual(16, pval.result)
