# Fixture for functionalities

def parametrize_test_cases(labels, test_cases):
    return {
        "labels": labels,
        "test_cases": test_cases
    }

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

# Sets to Euler sets



# "listToSet", "unite", "difference"
sets = {
    'a': [1, 2, 3],
    'b': [2, 3, 4],
    'c': [3, 4, 5],
    'd': [3, 5, 6]
}

keys_to_sets_tuples=parametrize_test_cases(\
    "key,set_elements", \
    [
        ('a', [1, 2, 3]),
        (('a',), [1, 2, 3]),
        (('a', 'b'), [1, 2, 3, 4]),
        (('a', 'b', 'c'), [1, 2, 3, 4, 5]),
        (('a', 'b', 'c', 'd'), [1, 2, 3, 4, 5, 6])
    ]
)

match_items_tuple=parametrize_test_cases(\
    "elements,expected_matched_sets", \
    [
        ({1, 2, 3}, {'a'}),
        ({1, 2, 3, 4}, {'a', 'b'}),
        ({1, 2, 3, 4, 5}, {'a', 'b', 'c'}),
        ({2, 3, 4, 5}, {'b', 'c'}),
        ({2, 3, 4, 5, 6}, {'b', 'c', 'd'})
    ]
)

sets_to_euler_tuples=parametrize_test_cases(\
    "test_sets,euler_sets", \
    [
        (
            {'a': [1, 2, 3]}, 
            {('a'): [1, 2, 3]}
        ),
        (
            {'a': [1], 'b': [1, 2]}, 
            {('b', ): [2], ('a','b'): [1]}
        ),
        (
            {'a': [1, 2, 3], 'b': [2, 3, 4]}, 
            {
                ('b', ): [4],
                ('a','b'): [2, 3],
                ('a', ): [1],
            }
        ),
        (
            {'a': [1, 2, 3], 'b': [2, 3, 4], 'c': [3, 4, 5]}, 
            {
                ('a','b'): [2],
                ('b','c'): [4],
                ('a','b','c'): [3],
                ('c', ): [5],
                ('a', ): [1],
            } 
        ),
        (
            sets,
            {
                ('a','b'): [2],
                ('b','c'): [4],
                ('a','b','c','d'): [3],
                ('c','d'): [5],
                ('d', ): [6],
                ('a', ): [1],
            }
        )
    ]
)

eulerSetsKeys=[
    ('a','b'), ('b','c'), ('a','b','c','d'), ('c','d'), ('d', ), ('a', )
]

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
