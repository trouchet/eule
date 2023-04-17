from __future__ import annotations

import eule.utils as utils
from .fixtures import arrA, arrB, setA, tupleA, arrApB, arrAmB, arrAiB, \
    arr_with_repetition_uniq, arr_with_repetition, \
    unsorted_delimited_string, sorted_delimited_string, \
    delimiter, dict_keys_with_non_empty_elements, \
    uncleared_dict, tuple_, value, updated_tuple

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

def test_list_to_set():
    """
    tests list to set converter
    """
    assert utils.list_to_set(arrA) == setA

def test_union():
    """
    tests unite two list with non-repeated elements
    """
    assert utils.union(arrA, arrB) == arrApB

def test_difference():
    """
    tests subtract elements of a list from the other
    """
    assert utils.difference(arrA, arrB) == arrAmB

def test_intersection():
    """
    tests intersection elements of a list from the other
    """
    assert utils.intersection(arrA, arrB) == arrAiB

def test_update_tuple():
    assert utils.update_tuple(tuple_, value) == updated_tuple

def test_tuplify():
    """
    tests 
    """
    assert utils.tuplify(tupleA) == tupleA
    assert utils.tuplify(arrA) == tupleA
    assert utils.tuplify(42) == (42)
