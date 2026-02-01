from typing import Set

from .types import SequenceType
from .utils import setify_sequences


def union(
    sequence_A: SequenceType,
    sequence_B: SequenceType
):
    """This map returns the union of two sequences without repetition.
    
    Automatically uses protocol methods if available, otherwise falls back
    to set conversion for backward compatibility.

    :param sequence_A: First sequence
    :param sequence_B: Second sequence
    :returns: union of sequences with non-repeated elements
    :rtype: same type as sequence_A
    """
    # Try protocol method first (for SetLike objects)
    if hasattr(sequence_A, 'union') and callable(sequence_A.union):
        return sequence_A.union(sequence_B)
    
    # Fallback to original implementation for backward compatibility
    sequences = [sequence_A, sequence_B]
    set_A, set_B = setify_sequences(sequences)
    union_set = set_A.union(set_B)
    type_A = type(sequence_A)

    return type_A(union_set)


def difference(
    sequence_A: SequenceType,
    sequence_B: SequenceType
):
    """This map returns the difference of a sequence respective to other, without repetition.
    
    Automatically uses protocol methods if available, otherwise falls back
    to set conversion for backward compatibility.

    :param sequence_A: First sequence
    :param sequence_B: Second sequence
    :returns: difference with non-repeated elements
    :rtype: same type as sequence_A
    """
    # Try protocol method first (for SetLike objects)
    if hasattr(sequence_A, 'difference') and callable(sequence_A.difference):
        return sequence_A.difference(sequence_B)
    
    # Fallback to original implementation for backward compatibility
    sequences = [sequence_A, sequence_B]
    set_A, set_B = setify_sequences(sequences)

    diff_set = set_A - set_B
    type_A = type(sequence_A)

    return type_A(diff_set)


def intersection(
    sequence_A: SequenceType,
    sequence_B: SequenceType
):
    """This map returns the intersection of a sequence respective to other, without repetition.
    
    Automatically uses protocol methods if available, otherwise falls back
    to set conversion for backward compatibility.

    :param sequence_A: First sequence
    :param sequence_B: Second sequence
    :returns: intersection with non-repeated elements
    :rtype: same type as sequence_A
    """
    # Try protocol method first (for SetLike objects)
    if hasattr(sequence_A, 'intersection') and callable(sequence_A.intersection):
        return sequence_A.intersection(sequence_B)
    
    # Fallback to original implementation for backward compatibility
    sequences = [sequence_A, sequence_B]
    set_A, set_B = setify_sequences(sequences)

    intersec_set = set_A.intersection(set_B)
    type_A = type(sequence_A)

    return type_A(intersec_set)
