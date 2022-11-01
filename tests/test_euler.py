#!/usr/bin/env python
"""Tests for `eule` package."""

import pytest

from eule import euler, spread_euler


def test_euler_iter_1_input():
    '''
    Generates a tuple with key-value
    '''
    assert next(euler({'a': [1, 2]})) == ('a', [1, 2])


def test_euler_iter_2_input():
    '''
    Generates all tuples with key-value
    '''
    eu_fun = euler({'a': [1, 2], 'b': [2, 3]})

    assert next(eu_fun) == ('b', [3])
    assert next(eu_fun) == ('a,b', [2])
    assert next(eu_fun) == ('a', [1])


def test_euler_iter_warning_1item():
    '''
    Raises a warning for duplicated dict values
    '''
    with pytest.warns(UserWarning):
        next(euler({'a': [42, 42]}))


def test_euler_iter_warning_2items():
    '''
    Raises a warning for duplicated dict values
    '''
    with pytest.warns(UserWarning):
        next(euler({'a': [42, 42], 'b': [42, 42]}))


def test_spread_euler_ill_input_str():
    '''
    Raises an Exception for ill-conditioned input as string
    '''
    with pytest.raises(TypeError, match='Ill-conditioned input.'):
        spread_euler('')


def test_spread_euler_ill_input_num():
    '''
    Raises an Exception for ill-conditioned input as number
    '''
    with pytest.raises(TypeError, match='Ill-conditioned input.'):
        spread_euler(1)


def test_spread_euler_1_set():
    '''
    Returns an euler dictionary for 1 valid set
    '''
    assert spread_euler(
        {
            'a': [1, 2, 3]
        }
    ) == {'a': [1, 2, 3]}


def test_spread_euler_2_sets_with_non_exclusivity():
    '''
    Returns an euler dictionary for 2 valid sets
    '''

    assert spread_euler(
        {
            'a': [1],
            'b': [1, 2]
        }
    ) == {'b': [2], 'a,b': [1]}


def test_spread_euler_2_sets():
    '''
    Returns an euler dictionary for 2 valid sets
    '''
    assert spread_euler(
        {
            'a': [1, 2, 3],
            'b': [2, 3, 4]
        }
    ) == {'b': [4], 'a,b': [2, 3], 'a': [1]}


def test_spread_euler_3_sets():
    '''
    Returns an euler dictionary for 3 valid sets
    '''
    assert spread_euler(
        {
            'a': [1, 2, 3],
            'b': [2, 3, 4],
            'c': [3, 4, 5]
        }) == {'a,b': [2], 'b,c': [4], 'a,b,c': [3], 'c': [5], 'a': [1]}


def test_spread_euler_4_sets():
    '''
    Returns an euler dictionary for 4 valid sets
    '''
    assert spread_euler(
        {
            'a': [1, 2, 3],
            'b': [2, 3, 4],
            'c': [3, 4, 5],
            'd': [3, 5, 6]
        }) == {'a,b': [2], 'b,c': [4], 'a,b,c,d': [3], 'c,d': [5], 'd': [6], 'a': [1]}
