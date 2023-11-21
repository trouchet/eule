from .utils import uniq, reduc
from warnings import warn

def validate_euler_generator_input(sets_):
    # There are no sets
    if not isinstance(sets_, (list, dict)):
        msg_1 = 'Ill-conditioned input.'
        msg_2 = 'It must be either a dict or array of arrays object!'
        raise TypeError(msg_1 + msg_2)

    is_unique_set_arr = [
        len(uniq(values)) == len(values) for values in sets_.values()
    ]

    def and_map(a, b):
        return (a and b)

    if not reduc(and_map, is_unique_set_arr, True):
        warn('Each array MUST NOT have duplicates')
        sets_ = {key: uniq(values) for key, values in sets_.items()}

    return sets_
