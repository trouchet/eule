from __future__ import annotations

import pytest
from eule.utils import clear_sets
from eule.utils import ordenate_tuple
from eule.utils import reduc
from eule.utils import sequence_to_set
from eule.utils import tuplify
from eule.utils import uniq
from eule.utils import update_tuple


def test_one_set_euler():
    """
    Tests the reduce function
    """

    def reduce_func(a, b):
        return a + b

    input_ = [1, 2]
    result = reduc(reduce_func, input_, 0)
    expected_output = 3

    assert result == expected_output


def test_unique_elems(
    arr_with_repetition_uniq,
    arr_with_repetition
):
    """
    tests the reduce function
    """
    input_ = arr_with_repetition
    result = uniq(input_)
    expected_output = arr_with_repetition_uniq

    assert result == expected_output


def test_clear_sets(
    uncleared_dict,
    cleared_dict
):
    """
    tests dict clean with empty values
    """
    input_ = uncleared_dict
    expected_output = cleared_dict

    assert clear_sets(input_) == expected_output

def test_clear_sets_with_list(
    uncleared_list,
    cleared_list
):
    input_list = uncleared_list
    expected_output = cleared_list
    assert clear_sets(input_list) == expected_output

def test_clear_sets_with_invalid_input():
    with pytest.raises(TypeError):
        clear_sets("invalid input")

def test_list_to_set(arrA, setA):
    """
    tests list to set converter
    """
    assert sequence_to_set(arrA) == setA

def test_ordenate_tuple(ordenated_tuple, tuple_):
    assert ordenate_tuple(tuple_) == ordenated_tuple

def test_update_tuple(tuple_, value, updated_tuple):
    assert update_tuple(tuple_, value) == updated_tuple

def test_tuplify(arrA, tupleA):
    """
    tests
    """
    assert tuplify(tupleA) == tupleA
    assert tuplify(arrA) == tupleA
    assert tuplify(42) == (42, )
