from __future__ import annotations

import eule.utils as utils


def test_one_set_euler():
    """
    tests the reduce function
    """

    def reduce_func(a, b):
        return a + b

    input_ = [1, 2]
    result = utils.reduc(reduce_func, input_, 0)
    expected_output = 3

    assert result == expected_output


def test_unique_elems():
    """
    tests the reduce function
    """
    input_ = [1, 2, 3, 3]
    result = utils.uniq(input_)
    expected_output = [1, 2, 3]

    assert result == expected_output


def test_dsort():
    """
    tests sorting delimited by token
    """
    input_ = '4,1,2,3'
    config = ','
    result = utils.dsort(input_, config)
    expected_output = '1,2,3,4'

    assert result == expected_output


def test_clear_sets():
    """
    tests dict clean with empty values
    """
    input_ = {'a': [1, 2, 3], 'b': []}
    result = utils.clear(input_)
    expected_output = ['a']

    assert result == expected_output
