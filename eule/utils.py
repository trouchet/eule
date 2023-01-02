"""utils module."""
import functools

import numpy as np


def keyfy(lst):
    """
    @abstract returns array entries in string fashion delimited by commas

    @param {Array} arr
    @return {string} str
    """
    return str(lst).strip('[]').replace(' ', '')


def reduce_(func, elems, elem0):
    """
    @abstract returns reduce function handler

    @param {function} func
    @param {object} elems
    @param {object} elem0
    @return {string} str
    """
    return functools.reduce(func, elems + [elem0])


def unique(lst):
    """
    @abstract returns list with unique elements

    @param {array} arr
    @return {array} sorted_arr
    """
    return list(np.unique(lst))


def delimited_sort(str_, delimiter):
    """
    @abstract returns a sorted string delimited by token

    @param {array} arr
    @return {array} sorted_arr
    """
    return delimiter.join(sorted(str_.split(delimiter)))


def non_empty_sets_keys(sets):
    """
    @abstract returns a set with non-empty values

    @param {dict} set
    @return {dict} cleaned_set
    """

    return list(
        filter(
            lambda key: len(sets[key]) != 0,
            sets.keys(),
        ),
    )
