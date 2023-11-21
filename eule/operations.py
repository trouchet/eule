from .utils import list_to_set

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
