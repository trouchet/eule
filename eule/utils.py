"""utils module."""
from functools import reduce
from typing import Any
from typing import Callable
from typing import Iterable
from typing import List
from typing import Set
from typing import Tuple

from numpy import unique

from .types import PseudoSequenceType
from .types import SequenceType
from .types import SetsType


def reduc(
    func: Callable[[Any, Any], Any],
    elems: Iterable[Any],
    elem0: Any
) -> Any:
    """This function returns a reduce handler

    :param function func: Reduce callback
    :param dict elems: list of elements
    :param dict elem0: first elements
    """
    return reduce(func, elems + [elem0])

def uniq(lst: List) -> List[Any]:
    """This map returns list with unique elements

    :param list lst: array of elements entries
    :returns: list with unique elements
    :rtype: list
    """
    return list(unique(lst))

def tuplify(
    candidate: PseudoSequenceType
) -> Tuple:
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

def sequence_to_set(sequence: SequenceType) -> Set:
    """This map converts a list or a tuple into a set

    :param list or tuple of elements:
    :returns: a set-converted sequence
    :rtype: set
    """
    return {s for s in sequence}

def setify_sequences(
    sequence_list: List[SequenceType]
) -> Tuple[Set]:
    """ This map returns a set of sets

    :param list of sets:
    :returns: set of sets
    :rtype: tuple
    """

    return (
        sequence_to_set(sequence)
        if isinstance(sequence, (list, tuple))
        else sequence
        for sequence in sequence_list
    )

def clear_sets(sets: SetsType):
    """This map returns a set with non-empty values

    :param dict set:
    :returns: a set universe with
    :rtype: dict
    """
    if isinstance(sets, dict):
        return {k: v for k, v in sets.items() if v}
    elif isinstance(sets, list):
        return [elem for elem in sets if elem]
    else:
        raise TypeError("Input must be a list or dictionary")

def cleared_set_keys(
    candidate: SetsType
) -> List[Any]:
    """This map returns a set with non-empty values

    :param dict set:
    :returns: a set universe with
    :rtype: dict
    """
    return list(clear_sets(candidate).keys())

def ordenate_tuple(
    tuple_: Tuple
) -> Tuple[Any]:
    """This map returns a sorted tuple element on given candidate

    :param input_tuple: The original tuple to be updated.
    :type input_tuple: tuple
    :param value: The element to be added to the tuple.
    :type value: Any
    :return: An ordered and updated tuple.
    :rtype: tuple
    """

    return tuplify(sorted(tuple_))

def update_tuple(
    tuple_: Tuple,
    value: Any
) -> Tuple[Any]:
    """This map updates and sorts a tuple with a value

    :param tuple of elements:
    :param value: element to update
    :returns: an ordered and updated tuple
    :rtype: tuple
    """

    tuple_lst = list(tuplify(tuple_))
    tuple_lst.append(value)

    return tuple(tuple_lst)

def ordered_tuplify(
    candidate: str | List | Tuple
) -> Tuple[Any]:
    """This map returns a sorted tuple element on given candidate

    :param candidate: tuplification candidate
    :returns: tuple with sorted elements
    :rtype: tuple
    """
    return ordenate_tuple(tuplify(candidate))

def update_ordered_tuple(
    candidate: Tuple,
    value: Any,
) -> Tuple[Any]:
    """This map returns a sorted tuple element on given candidate

    :param candidate: tuplification candidate
    :returns: tuple with sorted elements
    :rtype: tuple
    """
    return ordenate_tuple(
        update_tuple(tuplify(candidate), value)
    )
