from warnings import warn

from .types import SetsType
from .utils import reduc
from .utils import sequence_to_set
from .utils import uniq


def validate_euler_generator_input(
    sets_: SetsType
):
    """This function validates the input for euler_generator.
    
    Now works with SetLike protocol objects and built-in types.

    :param dict sets_: dictionary with sets
    :returns: validated sets
    :rtype: dict
    """

    # There are no sets
    if not isinstance(sets_, (list, dict)):
        msg_1 = 'Ill-conditioned input.'
        msg_2 = 'It must be either a dict or array of arrays object!'
        raise TypeError(msg_1 + msg_2)

    # Check for duplicates (skip for SetLike objects that handle this internally)
    is_unique_set_arr = []
    for values in sets_.values():
        # Skip validation for SetLike objects - they handle their own invariants
        if hasattr(values, 'union') and hasattr(values, 'intersection'):
            is_unique_set_arr.append(True)
        else:
            # Traditional validation for built-in types
            try:
                is_unique_set_arr.append(len(sequence_to_set(values)) == len(values))
            except (TypeError, AttributeError):
                # If we can't validate, assume it's okay (custom type)
                is_unique_set_arr.append(True)

    def and_map(a, b):
        return (a and b)

    if not reduc(and_map, is_unique_set_arr, True):
        warn('Each array MUST NOT have duplicates')
        # Only deduplicate built-in types
        validated_sets = {}
        for key, values in sets_.items():
            if hasattr(values, 'union') and hasattr(values, 'intersection'):
                # SetLike object - keep as is
                validated_sets[key] = values
            else:
                # Built-in type - deduplicate
                validated_sets[key] = uniq(values)
        return validated_sets

    return sets_
