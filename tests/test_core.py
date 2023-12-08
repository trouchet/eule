from __future__ import annotations

import pytest
from copy import deepcopy
from reprlib import repr

from eule.operations import intersection

from eule.core import euler_generator, euler, \
    euler_keys, euler_boundaries, Euler

from .fixtures import sets, setsBoundaries, \
    verbose_key_sets, verbose_key_sets_euler, \
    sets_to_euler_tuples, keys_to_sets_tuples, \
    match_items_tuple, eulerSetsKeys, euler_sets_keys

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
    expected_output = (('a', ), [1, 2])

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

@pytest.mark.parametrize(\
        sets_to_euler_tuples['labels'], sets_to_euler_tuples['test_cases']\
)
def test_euler(test_sets, euler_sets):
    assert euler(test_sets) == euler_sets

def test_euler_keys():
    """
    Returns an euler keys for 4 valid sets
    """
    input_ = {'a': [1, 2, 3], 'b': [2, 3, 4], 'c': [3, 4, 5], 'd': [3, 5, 6]}

    result = euler_keys(input_)
    intersec_sets=intersection(result, euler_sets_keys)

    assert len(intersec_sets) == len(euler_sets_keys)

def test_boundaries():
    assert euler_boundaries(sets) == setsBoundaries

@pytest.mark.parametrize(\
        sets_to_euler_tuples['labels'], sets_to_euler_tuples['test_cases']\
)
def test_euler_class_properties(test_sets, euler_sets):
    euler_instance=Euler(test_sets)

    assert euler_instance.sets == test_sets
    assert euler_instance.esets == euler_sets
    assert euler_instance.as_dict() == euler_sets

    esets_repr=repr(euler_instance.esets)
    expected_repr = f'Euler({esets_repr})'

    assert euler_instance.__repr__() == expected_repr

@pytest.mark.parametrize(\
        keys_to_sets_tuples['labels'], keys_to_sets_tuples['test_cases']\
)
def test_euler_class_getitem(key, set_elements):
    euler_instance=Euler(sets)

    assert euler_instance[key] == set_elements

def test_euler_class_getitem_error():
    """
    Raises an Exception for ill-conditioned input as string
    """
    euler_instance=Euler(sets)
    wrong_key='A'

    with pytest.raises(KeyError, match=wrong_key):
        euler_instance[wrong_key]

    with pytest.raises(KeyError, match='The keys must be among keys'):
        euler_instance[(wrong_key, )]

def test_euler_class_remove_key():
    """
    Raises an Exception for ill-conditioned input as string
    """
    euler_instance=Euler(deepcopy(sets))
    removing_key='a'
    remaining_sets={
        key: value
        for key, value in sets.items()
        if key is not removing_key
    }

    euler_instance.remove_key(removing_key)

    assert euler_instance.sets == remaining_sets
    assert euler_instance.esets == euler(remaining_sets)

def test_euler_class_warning_1item():
    """
    Raises a warning for duplicated dict values
    """
    euler_instance=Euler(deepcopy(sets))
    wrong_key='A'

    with pytest.warns(Warning):
        euler_instance.remove_key(wrong_key)

@pytest.mark.parametrize(\
        match_items_tuple['labels'], \
        match_items_tuple['test_cases']
)
def test_euler_class_match(elements,expected_matched_sets):
    """
    Raises an Exception for ill-conditioned input as string
    """
    euler_instance=Euler(deepcopy(sets))
    matched_sets=euler_instance.match(elements)

    assert matched_sets == expected_matched_sets

def test_euler_class_match_error():
    """
    Raises an Exception for ill-conditioned input as string
    """
    euler_instance=Euler(deepcopy(sets))
    matched_elems=['42', 'Ford Prefect']

    with pytest.raises(TypeError, match="Items must be of type 'set'"):
        euler_instance.match(matched_elems)

def test_euler_class_keys():
    """
    Returns an euler keys for 4 valid sets
    """
    euler_instance=Euler(deepcopy(sets))

    result = euler_instance.euler_keys()
    expected_output = eulerSetsKeys

    intersec_set=intersection(result, expected_output)

    assert len(intersec_set) == len(expected_output)

def test_euler_class_boundaries():
    euler_instance=Euler(deepcopy(sets))

    result = euler_instance.euler_boundaries()
    expected_output = setsBoundaries

    assert result == expected_output
