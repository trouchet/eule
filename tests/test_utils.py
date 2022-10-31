#!/usr/bin/env python

"""Tests for `eule` package."""

from eule.utils import keyfy, reduce_, unique, delimited_sort, non_empty_sets_keys


# define the tests
def test_keyfy():
    assert keyfy([1, 2, 3]) == '1,2,3'


def test_one_set_euler():
    assert reduce_(lambda a, b: a+b, [1, 2], 0) == 3


def test_unique_elems():
    assert unique([1, 2, 3]) == [1, 2, 3]


def test_delimited_sort():
    assert delimited_sort('4,1,2,3', ',') == '1,2,3,4'


def test_non_empty_sets_keys():
    assert non_empty_sets_keys({
        'a': [1, 2, 3],
        'b': []
        }) == ['a']
