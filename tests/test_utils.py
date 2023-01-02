from __future__ import annotations

import eule.utils as utils


# define the tests
def test_keyfy():
    """
    tests the key string generation
    """
    input_ = [1, 2, 3]
    result = utils.keyfy(input_)
    expected_output = '1,2,3'

    assert result == expected_output


def test_one_set_euler():
    """
    tests the reduce function
    """

    def reduce_func(a, b):
        return a + b

    input_ = [1, 2]
    result = utils.reduce_(reduce_func, input_, 0)
    expected_output = 3

    assert result == expected_output


def test_unique_elems():
    """
    tests the reduce function
    """
    input_ = [1, 2, 3, 3]
    result = utils.unique(input_)
    expected_output = [1, 2, 3]

    assert result == expected_output


def test_delimited_sort():
    """
    tests sorting delimited by token
    """
    input_ = '4,1,2,3'
    config = ','
    result = utils.delimited_sort(input_, config)
    expected_output = '1,2,3,4'

    assert result == expected_output


def test_non_empty_sets_keys():
    """
    tests dict clean with empty values
    """
    input_ = {'a': [1, 2, 3], 'b': []}
    result = utils.non_empty_sets_keys(input_)
    expected_output = ['a']

    assert result == expected_output
