from __future__ import annotations

import pytest

from eule.eule import euler_generator, euler, \
    euler_keys, euler_boundaries, Euler

from .fixtures import sets, setsBoundaries, \
    verbose_key_sets, verbose_key_sets_euler, \
    sets_to_euler_tuples

def test_verbose_keys_euler():
    """
    Generates a tuple with key-value
    """
    
    assert euler(verbose_key_sets) == verbose_key_sets_euler

def test_euler_iter_1_input():
    """
    Generates a tuple with key-value
    """
    input_ = {'a': [1, 2]}
    euler_gen = euler_generator(input_)
    expected_output = (('a'), [1, 2])

    assert next(euler_gen) == expected_output


def test_euler_iter_2_input():
    """
    Generates all tuples with key-value
    """
    input_ = {'a': [1, 2], 'b': [2, 3]}
    euler_gen = euler_generator(input_)

    assert next(euler_gen) == (('b',), [3])
    assert next(euler_gen) == (('a','b',), [2])
    assert next(euler_gen) == (('a',), [1])


def test_euler_iter_warning_1item():
    """
    Raises a warning for duplicated dict values
    """
    input_ = {'a': [42, 42]}
    euler_gen = euler_generator(input_)

    with pytest.warns(UserWarning):
        next(euler_gen)


def test_euler_iter_warning_2items():
    """
    Raises a warning for duplicated dict values
    """
    input_ = {'a': [42, 42], 'b': [42, 42]}
    eule_gen = euler_generator(input_)

    with pytest.warns(UserWarning):
        next(eule_gen)


def test_spread_euler_ill_input_str():
    """
    Raises an Exception for ill-conditioned input as string
    """
    with pytest.raises(TypeError, match='Ill-conditioned input.'):
        euler('')


def test_spread_euler_ill_input_num():
    """
    Raises an Exception for ill-conditioned input as number
    """
    with pytest.raises(TypeError, match='Ill-conditioned input.'):
        euler(1)


def test_spread_euler_1_set():
    """
    Returns an euler dictionary for 1 valid set
    """
    input_ = {'a': [1, 2, 3]}
    result = euler(input_)
    expected_output = {('a'): [1, 2, 3]}

    assert result == expected_output


def test_spread_euler_2_sets_with_non_exclusivity():
    """
    Returns an euler dictionary for 2 valid sets
    """
    input_ = {'a': [1], 'b': [1, 2]}
    result = euler(input_)
    expected_output = {('b', ): [2], ('a','b'): [1]}

    assert result == expected_output


def test_spread_euler_2_sets():
    """
    Returns an euler dictionary for 2 valid sets
    """
    input_ = {'a': [1, 2, 3], 'b': [2, 3, 4]}
    result = euler(input_)
    expected_output = {
        ('b', ): [4],
        ('a','b'): [2, 3],
        ('a', ): [1],
    }

    assert result == expected_output


def test_spread_euler_3_sets():
    """
    Returns an euler dictionary for 3 valid sets
    """

    input_ = {'a': [1, 2, 3], 'b': [2, 3, 4], 'c': [3, 4, 5]}
    result = euler(input_)
    expected_output = {
        ('a','b'): [2],
        ('b','c'): [4],
        ('a','b','c'): [3],
        ('c', ): [5],
        ('a', ): [1],
    }

    assert result == expected_output


def test_spread_euler_4_sets():
    """
    Returns an euler dictionary for 4 valid sets
    """
    input_ = {'a': [1, 2, 3], 'b': [2, 3, 4], 'c': [3, 4, 5], 'd': [3, 5, 6]}

    result = euler(input_)
    expected_output = {
        ('a','b'): [2],
        ('b','c'): [4],
        ('a','b','c','d'): [3],
        ('c','d'): [5],
        ('d', ): [6],
        ('a', ): [1],
    }

    assert result == expected_output

def test_euler_keys():
    """
    Returns an euler keys for 4 valid sets
    """
    input_ = {'a': [1, 2, 3], 'b': [2, 3, 4], 'c': [3, 4, 5], 'd': [3, 5, 6]}

    result = euler_keys(input_)
    expected_output = [
        ('a','b'), ('b','c'), ('a','b','c','d'), ('c','d'), ('d', ), ('a', )
    ]

    def intersection(a, b): return list(set(a) & set(b))

    assert len(intersection(result, expected_output)) == len(expected_output)

def test_boundaries():
    assert euler_boundaries(sets) == setsBoundaries

@pytest.mark.parametrize(\
        sets_to_euler_tuples["labels"], sets_to_euler_tuples["test_cases"]\
)
def test_euler_class(test_sets, euler_sets):
    assert euler(test_sets) == euler_sets 