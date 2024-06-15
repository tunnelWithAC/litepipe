import unittest

from litepipe import Transform, t


class TransformTest(unittest.TestCase):

    def test_right_shift_appends_function_without_errors(self):
        add_transform = Transform(lambda x: x + 2)
        mock_side_effect = Transform(lambda x: x)
        expected_step_count = 1

        add_transform >> mock_side_effect

        actual_step_count = len(add_transform.steps)
        self.assertEqual(actual_step_count, expected_step_count)

    def test_decorator_function_right_shift_appends_function_without_errors(self):
        @t
        def add_transform(x):
            return x + 2
        @t
        def subtract_transform(x):
            return x -2
        expected_step_count = 1

        add_transform >> subtract_transform

        actual_step_count = len(add_transform.steps)
        self.assertEqual(actual_step_count, expected_step_count)
