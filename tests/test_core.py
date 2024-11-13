from __future__ import annotations

from reprlib import repr

import pytest
from eule.core import Euler
from eule.core import euler
from eule.core import euler_boundaries
from eule.core import euler_generator
from eule.core import euler_keys
from eule.core import euler_parallel
from eule.core import euler_generator_worker 
from eule.operations import intersection
from eule.utils import sequence_to_set

from .fixtures import keys_to_sets_tuples
from .fixtures import match_items_tuple
from .fixtures import sets_to_euler_tuples
from .fixtures import worker_args_tuples

# Define test cases
@pytest.mark.parametrize(\
    worker_args_tuples['labels'], \
    worker_args_tuples['cases']
)
def test_euler_generator_worker(args, expected):
    print(args)
    result = euler_generator_worker(args)
    print(result)
    assert result == expected

# Edge cases
def test_empty_all_sets():
    args = ({'A': set(), 'B': set()}, ['A', 'B'], 'A')
    expected = []  # Since all sets are empty
    result = euler_generator_worker(args)
    assert result == expected

def test_verbose_keys_euler(
    verbose_key_sets,
    verbose_key_sets_euler
):
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
        sets_to_euler_tuples['labels'], \
        sets_to_euler_tuples['cases']\
)
def test_euler(test_sets, euler_sets):
    """
    Returns an euler set for 4 valid sets
    """
    assert euler(test_sets) == euler_sets

    setified_test_sets = {
        key: sequence_to_set(sequence)
        for key, sequence in test_sets.items()
    }
    setified_euler_sets = {
        key: sequence_to_set(sequence)
        for key, sequence in euler_sets.items()
    }

    assert euler(setified_test_sets) == setified_euler_sets
    assert euler_parallel(setified_test_sets) == setified_euler_sets


def test_euler_keys(sets, euler_sets_keys):
    """
    Returns an euler keys for 4 valid sets
    """
    result = euler_keys(sets)
    intersec_sets = intersection(result, euler_sets_keys)

    assert len(intersec_sets) == len(euler_sets_keys)

def test_boundaries(sets, sets_boundaries):
    assert euler_boundaries(sets) == sets_boundaries

@pytest.mark.parametrize(\
        sets_to_euler_tuples['labels'], \
        sets_to_euler_tuples['cases'] \
)
def test_euler_class_properties(test_sets, euler_sets):
    """
    Raises an Exception for ill-conditioned input as string
    """
    euler_instance=Euler(test_sets)

    assert euler_instance.sets == test_sets
    assert euler_instance.esets == euler_sets
    assert euler_instance.as_dict() == euler_sets

    esets_repr=repr(euler_instance.esets)
    expected_repr = f'Euler({esets_repr})'

    assert euler_instance.__repr__() == expected_repr

@pytest.mark.parametrize(\
        keys_to_sets_tuples['labels'], \
        keys_to_sets_tuples['cases']\
)
def test_euler_class_getitem(key, set_elements, sets):
    """
    Raises an Exception for ill-conditioned input as string
    """
    euler_instance=Euler(sets)

    assert euler_instance[key] == set_elements

def test_euler_class_getitem_error(sets):
    """
    Raises an Exception for ill-conditioned input as string
    """
    euler_instance=Euler(sets)
    wrong_key='A'

    with pytest.raises(KeyError, match=wrong_key):
        euler_instance[wrong_key]

    with pytest.raises(KeyError, match='The keys must be among keys'):
        euler_instance[(wrong_key, )]

def test_euler_class_remove_key(sets):
    """
    Raises an Exception for ill-conditioned input as string
    """
    euler_instance=Euler(sets)
    removing_key='a'
    remaining_sets={
        key: value
        for key, value in sets.items()
        if key is not removing_key
    }

    euler_instance.remove_key(removing_key)

    assert euler_instance.sets == remaining_sets
    assert euler_instance.esets == euler(remaining_sets)

def test_euler_class_warning_1item(sets):
    """
    Raises a warning for duplicated dict values
    """
    euler_instance=Euler(sets)
    wrong_key='A'

    with pytest.warns(Warning):
        euler_instance.remove_key(wrong_key)

@pytest.mark.parametrize(\
        match_items_tuple['labels'], \
        match_items_tuple['cases']
)
def test_euler_class_match(elements,expected_matched_sets, sets):
    """
    Raises an Exception for ill-conditioned input as string
    """
    euler_instance=Euler(sets)
    matched_sets=euler_instance.match(elements)

    assert matched_sets == expected_matched_sets

def test_euler_class_match_error(sets):
    """
    Raises an Exception for ill-conditioned input as string
    """
    euler_instance=Euler(sets)
    matched_elems=['42', 'Ford Prefect']

    with pytest.raises(TypeError, match="Items must be of type 'set'"):
        euler_instance.match(matched_elems)

def test_euler_class_keys(sets, euler_sets_keys):
    """
    Returns an euler keys for 4 valid sets
    """
    euler_instance=Euler(sets)

    result = euler_instance.euler_keys()
    expected_output = euler_sets_keys

    intersec_set=intersection(result, expected_output)

    assert len(intersec_set) == len(expected_output)

def test_euler_class_boundaries(sets, sets_boundaries):
    euler_instance=Euler(sets)

    result = euler_instance.euler_boundaries()
    expected_output = sets_boundaries

    assert result == expected_output
