"""Main module."""

from copy import deepcopy
from warnings import warn

from .utils import update_tuple, clear, reduc, uniq, union, difference, intersection, tuplify

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


def euler_generator(sets):
    """This generator function returns each tuple (key, elems) of the Euler diagram in a generator-wise fashion systematic:
    
    1. Begin with the available `sets` and their exclusive elements;
    2. Compute complementary elements to current key-set;
    3. In case complementary set-keys AND current set content are not empty, continue; Otherwise, go to next key-set;
    4. Find the euler diagram on complementary sets;
    5. Compute exclusive combination elements;
    6. In case there are exclusive elements to combination: yield exclusive combination elements; Remove exclusive combination elements from current key-set. 

    :param dict sets: array/dict of arrays
    :returns: (key, euler_set) tuple of given sets
    :rtype: tuple
    """
    sets_ = deepcopy(sets)
    sets_ = validate_euler_generator_input(sets_)

    # Only a set
    if len(sets_.keys()) == 1:
        comb_key = list(sets_.keys())[0]
        comb_elements = list(sets_.values())[0]
        yield ((comb_key), comb_elements)

    else:
        # Sets with non-empty elements
        set_keys = clear(sets_)

        # Traverse the combination lattice
        for set_key in set_keys:
            compl_sets_keys = difference(set_keys, [set_key])
            
            # There are still sets to analyze
            if len(compl_sets_keys) != 0 and len(sets[set_key]) != 0:
                # Complementary sets
                csets = {cset_key: sets_[cset_key] for cset_key in compl_sets_keys}

                # Instrospective recursion: Exclusive combination elements
                for euler_tuple, celements in euler_generator(csets):

                    # Remove current set_key elements
                    comb_elems = difference(celements, sets_[set_key])
                    
                    # Non-empty combination exclusivity case
                    if len(comb_elems) != 0:
                        # Sort keys to assure deterministic behavior
                        sorted_comb_key = tuplify(sorted(tuplify(euler_tuple)))
                        
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
                        comb_key = tuplify(sorted(update_tuple(euler_tuple, set_key)))
                        
                        # 2. Intersection of analysis element and exclusive group:
                        yield (comb_key, comb_elems)

                        # Remove intersection elements from current key-set and complementary sets
                        for euler_set_key in comb_key:
                            sets_[euler_set_key] = difference(sets_[euler_set_key], comb_elems)

                        sets_[set_key] = difference(sets_[set_key], comb_elems)

                    else:
                        pass

                    set_keys = clear(sets_)

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

                set_keys = clear(sets_)


def euler(sets):
    """Euler diagram dictionary of set-dictionary of non-repetitive elements
    
    :param dict sets: array/dict of arrays
    :returns: euler sets
    :rtype: dict
    """
    return dict(euler_generator(sets))

def euler_keys(sets):
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
                boundaries[setKey] = union(boundaries[setKey], difference(eulerSetKeys, [setKey]))
                
    return {setKey: sorted(neighborsKeys) for setKey, neighborsKeys in boundaries.items()}

class Euler(object):
    def __init__(self, sets):
        self.sets=deepcopy(sets)
        self.esets=euler(sets)

    def __getitem__(self, keys):
        if not isinstance(keys, tuple):
            try:
                return self.sets[keys]

            except:
                raise KeyError(keys)
        
        else:
            elements=[]
            try:
                for key in keys:
                    elements=union(self.sets[key], elements)

                return elements
            except:
                keys=str(keys)
                header=f"The keys must be among keys: ({keys})."
                
                msg=f"{header}"

                raise TypeError(msg)
    
    def __repr__(self):
        return str(self.as_dict())

    def euler_keys(self):
        return euler_keys(self.sets)

    def euler_boundaries(self):
        return euler_boundaries(self.sets)

    def as_dict(self):
        return self.esets
    
    def match(self, items: set):
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
        if(key in list(self.sets.keys())):
            self.sets = {
                key_: value \
                for key_, value in self.sets.items() \
                if key_ is not key 
            }

            self.esets=euler(self.sets)
        
        else:
            keys=list(self.sets.keys())

            msg1=f"Key {key} is not available on current set."
            msg2=f"Available keys are: {keys}"
            
            warn(msg1+" "+msg2)

    
    