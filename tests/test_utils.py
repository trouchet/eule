from __future__ import annotations

import eule.utils as utils
from .fixtures import arrA, arrB, setA, arrApB, arrAmB, \
    arr_with_repetition_uniq, arr_with_repetition, \
    unsorted_delimited_string, sorted_delimited_string, \
    delimiter, dict_keys_with_non_empty_elements, \
    uncleared_dict

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
    input_ = arr_with_repetition
    result = utils.uniq(input_)
    expected_output = arr_with_repetition_uniq

    assert result == expected_output


def test_dsort():
    """
    tests sorting delimited by token
    """
    input_ = unsorted_delimited_string
    config = delimiter
    result = utils.dsort(input_, config)
    expected_output = sorted_delimited_string

    assert result == expected_output


def test_clear_sets():
    """
    tests dict clean with empty values
    """
    input_ = uncleared_dict
    result = utils.clear(input_)
    expected_output = dict_keys_with_non_empty_elements

    assert result == expected_output

def test_listToSet():
    assert utils.listToSet(arrA) == setA

def test_unite():
    assert utils.unite(arrA, arrB) == arrApB

def test_difference():
    assert utils.difference(arrA, arrB) == arrAmB