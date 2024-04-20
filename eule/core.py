"""Main module."""
from typing import List, Dict, Union

from copy import deepcopy
from warnings import warn
from reprlib import repr

from .utils import \
    ordered_tuplify, \
    update_ordered_tuple, \
    cleared_set_keys
from .operations import \
    union, \
    difference, \
    intersection
from .validators import \
    validate_euler_generator_input
from .types import SetsType, KeyType

def euler_generator(
    sets: SetsType
):
    """This generator function returns each tuple (key, elems) of the
    Euler diagram in a generator-wise fashion systematic:

    1. Begin with the available `sets` and their exclusive elements;
    2. Compute complementary elements to the current key-set;
    3. In case complementary set-keys AND current set content are not empty, continue; 
    4. Otherwise, go to the next key-set;
    5. Find the euler diagram on complementary sets;
    6. Compute exclusive combination elements;
    7. In case there are exclusive elements to the combination: yield exclusive
       combination elements; Remove exclusive combination elements from the current key-set.

    :param dict sets: array/dict of arrays
    :returns: (key, euler_set) tuple of given sets
    :rtype: tuple
    """

    # Deep copy of sets and validates for List case
    sets_ = deepcopy(sets)
    sets_ = validate_euler_generator_input(sets_)
    
    # Only a set
    if len(sets_.keys()) == 1:
        comb_key = list(sets_.keys())[0]
        comb_elements = list(sets_.values())[0]
        yield ((comb_key, ), comb_elements)

    else:
        # Sets with non-empty elements
        set_keys = cleared_set_keys(sets_)

        # Traverse the combination lattice
        for set_key in set_keys:
            other_keys = difference(set_keys, [set_key])

            # There are still sets to analyze
            this_key_set = sets_[set_key]
            
            are_sets_still = len(other_keys) != 0 and \
                             len(this_key_set) != 0
            
            if are_sets_still:
                # Complementary sets
                csets = {
                    cset_key: sets_[cset_key] 
                    for cset_key in other_keys
                }

                # Instrospective recursion: Exclusive combination elements
                for euler_tuple, celements in euler_generator(csets):
                    
                    # Remove current set_key elements
                    this_key_set = sets_[set_key]
                    
                    comb_elems = difference(celements, this_key_set)

                    # Non-empty combination exclusivity case
                    if len(comb_elems) != 0:
                        # Sort keys to assure deterministic behavior
                        sorted_comb_key = ordered_tuplify(euler_tuple)

                        # 1. Exclusive elements respective complementary keys
                        yield (sorted_comb_key, comb_elems)

                        # Remove comb_elems elements from its original sets
                        for euler_set_key in sorted_comb_key:
                            sets_[euler_set_key] = difference(sets_[euler_set_key], comb_elems)
                    else:
                        pass

                    # Retrieve intersection elements
                    comb_elems = intersection(celements, sets[set_key])

                    # Non-empty intersection set
                    if len(comb_elems) != 0:
                        # Sort keys to assure deterministic behavior
                        comb_key = update_ordered_tuple(euler_tuple, set_key)

                        # 2. Intersection of analysis element and exclusive group:
                        yield (comb_key, comb_elems)

                        # Remove intersection elements from current key-set and complementary sets
                        for euler_set_key in comb_key:
                            sets_[euler_set_key] = difference(sets_[euler_set_key], comb_elems)

                        sets_[set_key] = difference(sets_[set_key], comb_elems)

                    else:
                        pass

                    set_keys = cleared_set_keys(sets_)

                if len(sets_[set_key]) != 0:
                    # Load combination key
                    comb_key = (set_key, )
                    comb_elems = sets_[set_key]

                    # 3. Remaining exclusive elements
                    yield (comb_key, comb_elems)

                    # Remove remaining set elements
                    sets_[set_key] = []

                else:
                    pass

                set_keys = cleared_set_keys(sets_)


def euler(
    sets: SetsType
):
    """Euler diagram dictionary of set-dictionary of non-repetitive elements

    :param dict sets: array/dict of arrays
    :returns: euler sets
    :rtype: dict
    """
    return dict(euler_generator(sets))

def euler_keys(
    sets: SetsType
):
    """Euler diagram keys

    :param dict sets: array/dict of arrays
    :returns: euler sets keys
    :rtype: list
    """
    return list(euler(sets).keys())

def euler_boundaries(sets):
    """Euler diagram set boundaries

    :param dict sets: array/dict of arrays
    :returns: euler boundary dict
    :rtype: list
    """

    setsKeys = list(sets.keys())
    eulerSetsKeys = euler_keys(sets)

    boundaries = dict(map(lambda key: (key, []), setsKeys))

    for setKey in setsKeys:
        for eulerSetKeys in eulerSetsKeys:
            if setKey in eulerSetKeys:
                this_boundaries = boundaries[setKey]
                ekeys_not_this = difference(eulerSetKeys, [setKey])
                boundaries[setKey] = union(this_boundaries, ekeys_not_this)

    return {\
        setKey: sorted(neighborsKeys) \
        for setKey, neighborsKeys in boundaries.items()\
    }

class Euler:
    def __init__(self, sets: Union[List, Dict]):
        """
        Initialize an Euler object.

        Parameters:
        sets (dict): A dictionary containing sets indexed by keys.

        This constructor makes a deep copy of the input sets and computes
        the Euler set representation.
        """
        self.sets=deepcopy(sets)
        self.esets=euler(sets)

    def __getitem__(self, keys: KeyType):
        """
        Get the elements from the sets associated with the specified keys.

        Parameters:
        keys (tuple or str): The key or keys for accessing the sets.

        Returns:
        list: The union of sets associated with the specified keys.

        If a single key is provided, it returns the elements of the set associated
        with that key. If a tuple of keys is provided, it returns the union of sets
        associated with those keys.
        """

        if not isinstance(keys, tuple):
            try:
                return self.sets[keys]

            except KeyError:
                raise KeyError(keys)

        else:
            elements=[]
            try:
                for key in keys:
                    elements=union(self.sets[key], elements)
                
                return elements
            except KeyError:
                keys=str(keys)
                header=f'The keys must be among keys: ({keys}).'

                msg=f'{header}'

                raise KeyError(msg)

    def euler_keys(self):
        """
        Get the keys associated with the Euler set representation.

        Returns:
        list: A list of keys corresponding to the Euler set representation.
        """

        return euler_keys(self.sets)

    def euler_boundaries(self):
        """
        Get the boundaries of the Euler set representation.

        Returns:
        tuple: A tuple containing the lower and upper boundaries of the Euler set representation.
        """
        return euler_boundaries(self.sets)

    def as_dict(self):
        """
        Get the Euler set representation as a dictionary.

        Returns:
        dict: The Euler set representation as a dictionary.
        """

        return self.esets

    def match(self, items: set):
        """
        Match a set of items to the sets in the Euler representation.

        Parameters:
        items (set): A set of items to match against the sets in the Euler representation.

        Returns:
        set: A set of keys corresponding to sets that are subsets of the provided items.

        It checks which sets in the Euler representation are subsets of the provided items
        and returns their keys.
        """

        if not isinstance(items, set):
            raise TypeError("Items must be of type 'set'")

        # Initial value: Empty set
        set_keys=set()

        # Loop along euler set key tuples
        for key, value in self.sets.items():
            intersection_elems=items.intersection(set(value))

            # Match operator produces the non-repeated union of euler keys which
            # has its value set as items subset.
            if(len(intersection_elems)==len(value)):
                set_keys.add(key)


        return set_keys

    def remove_key(self, key):
        """
        Remove a key from the sets in the Euler representation.

        Parameters:
        key: The key to be removed from the sets.

        If the key exists, it is removed from the sets, and the Euler representation is updated.
        If the key doesn't exist, a warning is issued.

        """

        if(key in list(self.sets.keys())):
            self.sets = {
                key_: value \
                for key_, value in self.sets.items() \
                if key_ is not key
            }

            self.esets=euler(self.sets)

        else:
            keys=list(self.sets.keys())

            msg1=f'Key {key} is not available on current set.'
            msg2=f'Available keys are: {keys}'

            warn(msg1+' '+msg2)

    def __repr__(self) -> str:
        """
        Get a string representation of the Euler object.

        Returns:
        str: A string representation of the Euler object in the
        format "Euler({Euler set representation})".
        """
        esets_repr=repr(self.esets)

        return f'Euler({esets_repr})'
