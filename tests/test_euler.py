#!/usr/bin/env python

"""Tests for `eule` package."""
import pytest
import warnings

from eule.eule import euler, spread_euler

def test_euler_iter_1_input():
    assert next(euler({'a': [1,2]})) == ('a', [1,2])

def test_euler_iter_2_input():
    eu_fun = euler({'a': [1,2], 'b': [2,3]})
    
    assert next(eu_fun) == ('b', [3])
    assert next(eu_fun) == ('a,b', [2])
    assert next(eu_fun) == ('a', [1])
    
def test_euler_iter_error():
    with pytest.raises(Exception):
        next(euler(1))

def test_euler_iter_warning():
    with pytest.raises(Exception):
        next(euler(1))

def test_euler_iter_warning_1item():
    with pytest.warns(UserWarning):
        next(euler({'a': [42, 42]}))
        
def test_euler_iter_warning_2items():
    with pytest.warns(UserWarning):
        next(euler({'a': [42, 42], 'b': [42, 42]}))

def test_spread_euler_1_set():
    assert spread_euler(
        {
            'a': [1, 2, 3]
        }
    ) == {'a': [1, 2, 3]}
    
def test_spread_euler_2_sets():
    assert spread_euler(
        {
            'a': [1, 2, 3], 
            'b': [2, 3, 4]
        }
    ) == {'b': [4], 'a,b': [2, 3], 'a': [1]}

def test_spread_euler_3_sets():
    assert spread_euler(
        {
            'a': [1, 2, 3], 
            'b': [2, 3, 4], 
            'c': [3, 4, 5]
        }
    ) == {'a,b': [2], 'c,b': [4], 'a,c,b': [3], 'c': [5], 'a': [1]}

def test_spread_euler_4_sets():
    assert spread_euler(
        {
            'a': [1, 2, 3], 
            'b': [2, 3, 4], 
            'c': [3, 4, 5],
            'd': [3, 5, 6]
        }
    ) == {'a,b': [2], 'c,b': [4], 'a,d,c,b': [3], 'd,c': [5], 'd': [6], 'a': [1]}

    
