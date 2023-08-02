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

def dsort(str_, delimiter):
    """This map returns a sorted string delimited by token

    :param str str_:  string with delimiter between elements 
    :returns: string with sorted elements delimited by given delimiter 
    :rtype: str
    """
    return delimiter.join(sorted(str_.split(delimiter)))

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

def union(listA:list, listB:list):
    """This map returns the union of two lists without repetition

    :param listA:
    :param listB:
    :returns: list with non-repeated elements
    :rtype: list
    """

    return list(list_to_set(listA).union(list_to_set(listB)))

def difference(listA:list, listB:list):
    """This map returns the difference of a list respective to other, without repetition

    :param listA:
    :param listB:
    :returns: difference list with non-repeated elements
    :rtype: list
    """
    
    return list(list_to_set(listA)-(list_to_set(listB)))

def intersection(listA:list, listB:list):
    """This map returns the intersection of a list respective to other, without repetition

    :param listA:
    :param listB:
    :returns: intersection list with non-repeated elements
    :rtype: list
    """
    
    return list(list_to_set(listA).intersection(list_to_set(listB)))

