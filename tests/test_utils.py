#!/usr/bin/env python

"""Tests for `eule` package."""

import pytest
from eule.utils import keyfy, reduce_, unique, delimited_sort

# define the tests
def test_keyfy():
    assert keyfy([1, 2, 3]) == '1,2,3'

def test_one_set_euler():
    assert reduce_(lambda a, b: a+b, [1, 2], 0) == 3

def test_unique_elems():
    assert unique([1, 2, 3]) == [1, 2, 3]

def test_unique_elems():
    assert delimited_sort('4,1,2,3', ',') == '1,2,3,4'
