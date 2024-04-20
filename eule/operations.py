from typing import Union, List, Set

from .utils import setify_sequences

SetType = Union[List, Set]

def union(
    set_A: SetType, 
    set_B: SetType
):
    """This map returns the union of two lists without repetition

    :param listA:
    :param listB:
    :returns: list with non-repeated elements
    :rtype: list
    """
    set_A, set_B = setify_sequences([set_A, set_B])
    
    return list(set_A.union(set_B))

def difference(
    set_A: SetType, 
    set_B: SetType
):
    """This map returns the difference of a list respective to other, without repetition

    :param listA:
    :param listB:
    :returns: difference list with non-repeated elements
    :rtype: list
    """
    set_A, set_B = setify_sequences([set_A, set_B])

    return list(set_A-set_B)

def intersection(
    set_A: SetType, 
    set_B: SetType
):
    """This map returns the intersection of a list respective to other, without repetition

    :param listA:
    :param listB:
    :returns: intersection list with non-repeated elements
    :rtype: list
    """
    set_A, set_B = setify_sequences([set_A, set_B])
    
    return list(set_A.intersection(set_B))
