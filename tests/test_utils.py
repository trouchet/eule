from __future__ import annotations

import src.utils as utils


# define the tests
def test_keyfy():
    """
    tests the key string generation
    """
    assert utils.keyfy([1, 2, 3]) == "1,2,3"


def test_one_set_euler():
    """
    tests the reduce function
    """
    assert utils.reduce_(lambda a, b: a + b, [1, 2], 0) == 3


def test_unique_elems():
    """
    tests the reduce function
    """
    assert utils.unique([1, 2, 3, 3]) == [1, 2, 3]


def test_delimited_sort():
    """
    tests sorting delimited by token
    """
    assert utils.delimited_sort("4,1,2,3", ",") == "1,2,3,4"


def test_non_empty_sets_keys():
    """
    tests dict clean with empty values
    """
    assert utils.non_empty_sets_keys({"a": [1, 2, 3], "b": []}) == ["a"]
