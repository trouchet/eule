from warnings import warn

from .types import SetsType
from .utils import reduc
from .utils import sequence_to_set
from .utils import uniq


def validate_euler_generator_input(
    sets_: SetsType
):
    """This function validates the input for euler_generator

    :param dict sets_: dictionary with sets
    :returns: validated sets
    :rtype: dict
    """

    # There are no sets
    if not isinstance(sets_, (list, dict)):
        msg_1 = 'Ill-conditioned input.'
        msg_2 = 'It must be either a dict or array of arrays object!'
        raise TypeError(msg_1 + msg_2)

    is_unique_set_arr = [
        len(sequence_to_set(values)) == len(values)
        for values in sets_.values()
    ]

    def and_map(a, b):
        return (a and b)

    if not reduc(and_map, is_unique_set_arr, True):
        warn('Each array MUST NOT have duplicates')
        sets_ = {
            key: uniq(values)
            for key, values in sets_.items()
        }

    return sets_
