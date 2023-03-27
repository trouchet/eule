"""utils module."""
from functools import reduce 
from numpy import unique

def reduc(func, elems, elem0):
    """This function returns a reduce handler

    :param function func: Reduce callback
    :param dict elems: list of elements
    :param dict elem0: first elements 
    """
    return reduce(func, elems + [elem0])


def uniq(lst):
    """This map returns list with unique elements

    :param list lst: array of elements entries 
    :returns: list with unique elements 
    :rtype: list
    """
    return list(unique(lst))


def dsort(str_, delimiter):
    """This map returns a sorted string delimited by token

    :param str str_:  string with delimiter between elements 
    :returns: string with sorted elements delimited by given delimiter 
    :rtype: str
    """
    return delimiter.join(sorted(str_.split(delimiter)))


def clear(sets):
    """This map returns a set with non-empty values

    :param dict set:  
    :returns: a set universe with  
    :rtype: dict
    """
    return list(
        filter(
            lambda key: len(sets[key]) != 0,
            sets.keys(),
        ),
    )

def areSpiderKeys(arr):
    """This map returns a boolean variable that type check a list of arrays

    :param dict set:  
    :returns: a set universe with  
    :rtype: boolean
    """

    def isString(el): return isinstance(el, str)
    def and_(a, b): return a and b

    return reduce(and_, map(isString, arr)) if isinstance(arr, list) else False