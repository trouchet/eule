"""Main module."""
from __future__ import unicode_literals, absolute_import

from warnings import warn

from .utils import reduce_, unique, delimited_sort, non_empty_sets_keys


def euler(sets):
    '''
        @abstract returns each tuple [key, elems] of the Euler diagram
        systematic in a generator-wise fashion
        Rationale:
           1. Begin with the available sets and their exclusive elements;
           2. Compute complementary elements to current key-set;
           3. In case complementary set-keys AND current set content are not empty, continue;
           Otherwise, go to next key-set;
           4. Find the euler diagram on complementary sets;
           5. Compute exclusive combination elements;
           6. In case there are exclusive elements to combination:
           6.a Yield exclusive combination elements;
           6.b Remove exclusive combination elements from current key-set;

        @param {Array} sets
        @return {Array} keys_elems
    '''
    # There are no sets
    if not isinstance(sets, (list, dict)):
        raise TypeError("Ill-conditioned input.")

    is_unique_set_arr = [len(unique(values)) == len(values) for values in sets.values()]
    if not reduce_(lambda a, b: a and b, is_unique_set_arr, True):
        warn("Each array MUST NOT have duplicates")
        sets = {key: unique(values) for key, values in sets.items()}

    # Only a set
    if len(sets.values()) == 1:
        key = list(sets.keys())[0]
        value = list(sets.values())[0]
        yield (key, value)

    else:
        # Remove empty sets

        # Keys complementary to current available key-set
        compl_sets_keys = []

        # Sets with non-empty elements
        set_keys = non_empty_sets_keys(sets)

        # Traverse the combination lattice
        for set_key in set_keys:
            compl_sets_keys = list(set(set_keys) - set([set_key]))

            # There are still sets to analyze
            # Morgan Rule: ¬(A & B) = ¬A | ¬B
            if (len(compl_sets_keys) != 0 and len(sets[set_key]) != 0):
                csets = {cset_key: sets[cset_key] for cset_key in compl_sets_keys}

                for comb_str, celements in euler(csets):
                    # Exclusive combination elements
                    comb_excl = list(set(celements)-set(sets[set_key]))

                    # Non-empty combination exclusivity case
                    if len(comb_excl) != 0:
                        # 1. Exclusive group elements except current analysis set
                        yield (delimited_sort(comb_str, ','), comb_excl)

                        for ckey in comb_str.split(','):
                            sets[ckey] = list(set(sets[ckey])-set(comb_excl))

                    comb_intersec = list(set(celements).intersection(set(sets[set_key])))
                    sets[set_key] = list(set(sets[set_key]) - set(comb_intersec))

                    if len(comb_intersec) != 0:
                        # 2. Intersection of analysis element and exclusive group
                        comb_intersec_key = set_key+','+comb_str
                        yield (delimited_sort(comb_intersec_key, ','), comb_intersec)

                        # Remove intersection elements from current key-set and complementary sets
                        for ckey in comb_str.split(','):
                            sets[ckey] = list(set(sets[ckey])-set(comb_intersec))

                        sets[set_key] = list(set(sets[set_key])-set(comb_intersec))

                set_keys = non_empty_sets_keys(sets)

                # 3. Set-key exclusive elements
                if len(sets[set_key]) != 0:
                    yield (str(set_key), sets[set_key])


def spread_euler(sets):
    '''
        @abstract returns Euler diagram dictionary of set-dictionary of non-repetitive elements

        @param {Array} sets
        @return {dict} euler_diagram
    '''
    return dict(euler(sets))
