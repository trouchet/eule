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

def uniq(lst:list):
    """This map returns list with unique elements

    :param list lst: array of elements entries
    :returns: list with unique elements
    :rtype: list
    """
    return list(unique(lst))

def tuplify(candidate):
    """This map returns a tuple element on given candidate

    :param candidate: tuplification candidate
    :returns: string with sorted elements delimited by given delimiter
    :rtype: str
    """
    return candidate if isinstance(candidate, tuple) \
        else ( \
            tuple(candidate) if isinstance(candidate, list) \
            else ( \
                (candidate,) if isinstance(candidate, str) \
                else (candidate,)
            )
        )

def clear(sets):
    """This map returns a set with non-empty values

    :param dict set:
    :returns: a set universe with
    :rtype: dict
    """
    def non_empty_mask(key):
        return (len(sets[key]) != 0)

    return list(filter(non_empty_mask, sets.keys(), ),)

def ordenate_tuple(tuple_:tuple):
    """
    Perform a custom operation on a tuple by updating it with a value and returning an ordered tuple.

    :param input_tuple: The original tuple to be updated.
    :type input_tuple: tuple
    :param value: The element to be added to the tuple.
    :type value: Any
    :return: An ordered and updated tuple.
    :rtype: tuple
    """

    return tuplify(sorted(tuple_))

def update_tuple(tuple_:tuple, value):
    """This map updates and sorts a tuple with a value

    :param tuple of elements:
    :param value: element to update
    :returns: an ordered and updated tuple
    :rtype: tuple
    """

    tuple_lst=list(tuplify(tuple_))
    tuple_lst.append(value)

    return tuple(tuple_lst)

def list_to_set(arr:list):
    """This map converts a list into a set

    :param list of elements:
    :returns: a set-converted list
    :rtype: set
    """
    return {s for s in arr}
