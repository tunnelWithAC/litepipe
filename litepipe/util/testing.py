from typing import List

"""

def equal_to(expected):

  def _equal(actual):
    expected_list = list(expected)

    # Try to compare actual and expected by sorting. This fails with a
    # TypeError in Python 3 if different types are present in the same
    # collection. It can also raise false negatives for types that don't have
    # a deterministic sort order, like pyarrow Tables as of 0.14.1
    try:
      sorted_expected = sorted(expected)
      sorted_actual = sorted(actual)
      if sorted_expected != sorted_actual:
        raise BeamAssertException(
            'Failed assert: %r == %r' % (sorted_expected, sorted_actual))
    # Slower method, used in two cases:
    # 1) If sorted expected != actual, use this method to verify the inequality.
    #    This ensures we don't raise any false negatives for types that don't
    #    have a deterministic sort order.
    # 2) As a fallback if we encounter a TypeError in python 3. this method
    #    works on collections that have different types.
    except (BeamAssertException, TypeError):
      unexpected = []
      for element in actual:
        try:
          expected_list.remove(element)
        except ValueError:
          unexpected.append(element)
      if unexpected or expected_list:
        msg = 'Failed assert: %r == %r' % (expected, actual)
        if unexpected:
          msg = msg + ', unexpected elements %r' % unexpected
        if expected_list:
          msg = msg + ', missing elements %r' % expected_list
        raise BeamAssertException(msg)

  return _equal

"""


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

# def return_pipeline_result():