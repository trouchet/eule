# Fixture for functionalities

# tuplify
tuple_=(1,3,2,4)
value=5
updated_tuple=(1,3,2,4,5)

# "uniq"
arr_with_repetition=[1, 2, 3, 3]
arr_with_repetition_uniq=[1, 2, 3]

# "dsort"
unsorted_delimited_string='4,1,2,3'
delimiter=','
sorted_delimited_string='1,2,3,4'

# "clear"
uncleared_dict={'a': [1, 2, 3], 'b': []}
dict_keys_with_non_empty_elements=['a']

# "listToSet", "unite", "difference"
sets = {
    'a': [1, 2, 3],
    'b': [2, 3, 4],
    'c': [3, 4, 5],
    'd': [3, 5, 6]
}

setsBoundaries={
    'a': ['b', 'c', 'd'], 
    'b': ['a', 'c', 'd'], 
    'c': ['a', 'b', 'd'], 
    'd': ['a', 'b', 'c']
}

arrA=[1,2,3]
setA={1,2,3}
tupleA=(1,2,3)

arrB=[3,4,5]

arrApB=[1,2,3,4,5]
arrAmB=[1,2]
arrAiB=[3]

verbose_key_sets={
    "set A": [1,2,3,4],
    "set B": [2,3,4,5],
    "set C": [3,4,5,6],
    "set D": [4,5,6,7],
}

verbose_key_sets_euler={
    ("set A",): [1],
    ("set A","set B",):[2],
    ("set A","set B","set C",):[3],
    ("set A","set B","set C","set D",):[4],
    ("set B","set C","set D",):[5],
    ("set C","set D",):[6],
    ("set D",): [7],
}
