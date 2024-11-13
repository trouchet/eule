from typing import Set

from .types import SequenceType
from .utils import setify_sequences


def union(
    sequence_A: SequenceType,
    sequence_B: SequenceType
):
    """This map returns the union of two lists without repetition

    :param listA:
    :param listB:
    :returns: list with non-repeated elements
    :rtype: list
    """
    sequences = [sequence_A, sequence_B]
    set_A, set_B = setify_sequences(sequences)
    union_set = set_A.union(set_B)
    type_A = type(sequence_A)

    return type_A(union_set)

def difference(
    sequence_A: SequenceType,
    sequence_B: SequenceType
):
    """This map returns the difference of a list respective to other, without repetition

    :param listA:
    :param listB:
    :returns: difference list with non-repeated elements
    :rtype: list
    """
    sequences = [sequence_A, sequence_B]
    set_A, set_B = setify_sequences(sequences)

    diff_set = set_A-set_B
    type_A = type(sequence_A)

    return type_A(diff_set)

def intersection(
    sequence_A: SequenceType,
    sequence_B: SequenceType
):
    """This map returns the intersection of a list respective to other, without repetition

    :param listA:
    :param listB:
    :returns: intersection list with non-repeated elements
    :rtype: list
    """
    sequences = [sequence_A, sequence_B]
    set_A, set_B = setify_sequences(sequences)

    intersec_set =  set_A.intersection(set_B)
    type_A = type(sequence_A)

    return type_A(intersec_set)
