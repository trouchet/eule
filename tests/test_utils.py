#!/usr/bin/env python

"""Tests for `eule` package."""

import pytest
from eule.utils import keyfy, reduce_, unique

# define the tests
def test_keyfy():
    assert keyfy([1, 2, 3]) == '1,2,3'

def test_one_set_euler():
    assert reduce(lambda a, b: a+b, [1, 2], 0) == 3

def test_unique_elems():
    assert unique([1, 2, 3]) == [1,2,3]
