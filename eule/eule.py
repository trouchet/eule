"""Main module."""

from copy import deepcopy
from warnings import warn

from .utils import delimited_sort, non_empty_sets_keys, reduce_, unique

delimiter = ','


def euler(sets):
    """
    @abstract returns each tuple [key, elems] of the Euler diagram
    systematic in a generator-wise fashion
    Rationale:
    1. Begin with the available sets and their exclusive elements;
    2. Compute complementary elements to current key-set;
    3. In case complementary set-keys AND current set content
    are not empty, continue. Otherwise, go to next key-set;
    4. Find the euler diagram on complementary sets;
    5. Compute exclusive combination elements;
    6. In case there are exclusive elements to combination:
    6.a Yield exclusive combination elements;
    6.b Remove exclusive combination elements from current key-set;

    @param {Array} sets
    @return {Array} euler_diagrams
    """
    sets_ = deepcopy(sets)

    # There are no sets
    if not isinstance(sets_, (list, dict)):
        msg_1 = 'Ill-conditioned input.'
        msg_2 = 'It must be either a json-like or array of arrays object!'
        raise TypeError(msg_1 + msg_2)

    is_unique_set_arr = [
        len(unique(values)) == len(values) for values in sets_.values()
    ]
    if not reduce_(lambda a, b: a and b, is_unique_set_arr, True):
        warn('Each array MUST NOT have duplicates')
        sets = {key: unique(values) for key, values in sets.items()}

    # Only a set
    if len(sets_.values()) == 1:
        comb_key = list(sets_.keys())[0]
        comb_elements = list(sets_.values())[0]
        yield (comb_key, comb_elements)

    else:
        # Sets with non-empty elements
        set_keys = non_empty_sets_keys(sets_)

        # Traverse the combination lattice
        for set_key in set_keys:
            compl_sets_keys = list(set(set_keys) - {set_key})

            # There are still sets to analyze
            if len(compl_sets_keys) != 0 and len(sets[set_key]) != 0:
                # Complementary sets
                csets = {cset_key: sets_[cset_key] for cset_key in compl_sets_keys}

                # Instrospective recursion: Exclusive combination elements
                for comb_str, celements in euler(csets):

                    # Remove current set_key elements
                    comb_elems = list(set(celements) - set(sets_[set_key]))

                    # Non-empty combination exclusivity case
                    if len(comb_elems) != 0:
                        # Sort keys to assure deterministic behavior
                        sorted_comb_key = delimited_sort(comb_str, delimiter)

                        # 1. Exclusive group elements except current analysis set
                        yield (sorted_comb_key, comb_elems)

                        # Remove comb_elems elements from its original sets
                        for ckey in comb_str.split(delimiter):
                            sets_[ckey] = list(set(sets_[ckey]) - set(comb_elems))

                    # Retrieve intersection elements
                    comb_elems = list(
                        set(celements).intersection(set(sets[set_key])),
                    )

                    # Non-empty intersection set
                    if len(comb_elems) != 0:
                        # 2. Intersection of analysis element and exclusive group:
                        # Sort keys to assure deterministic behavior
                        comb_key = delimited_sort(
                            set_key + delimiter + comb_str, delimiter
                        )

                        yield (comb_key, comb_elems)

                        # Remove intersection elements from current key-set and complementary sets
                        for ckey in comb_str.split(delimiter):
                            sets_[ckey] = list(set(sets_[ckey]) - set(comb_elems))

                        sets_[set_key] = list(set(sets_[set_key]) - set(comb_elems))

                    set_keys = non_empty_sets_keys(sets_)

                # 3. Remaining exclusive elements
                if len(sets_[set_key]) != 0:
                    # Load combination key
                    comb_key = str(set_key)
                    comb_elems = sets_[set_key]

                    # Yield tuple
                    yield (comb_key, comb_elems)

                    # Remove remaining set elements
                    sets_[set_key] = []

                set_keys = non_empty_sets_keys(sets_)


def spread_euler(sets):
    """
    @abstract returns Euler diagram dictionary of set-dictionary of
    non-repetitive elements

    @param {Array} sets
    @return {dict} euler_diagram
    """
    return dict(euler(sets))
