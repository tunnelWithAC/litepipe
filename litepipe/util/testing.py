from typing import List


def assert_equal(actual, expected):
    if isinstance(actual, List) and isinstance(expected, List):
        sorted_expected = sorted(expected)
        sorted_actual = sorted(actual)
        if sorted_expected == sorted_actual:
            return True
        if len(sorted_actual) != len(sorted_expected):
            return False
        for act, exp in zip(actual, expected):
            if act.result != exp.result or act.exception != exp.exception:
                return False
    else:
        raise AssertionError("Expected actual and expected inputs to both have type List")
