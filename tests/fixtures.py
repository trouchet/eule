# Fixture for functionalities

def parametrize_cases(labels, test_cases):
    return {
        'labels': labels,
        'cases': test_cases
    }

keys_to_sets_tuples=parametrize_cases(\
    'key,set_elements', \
    [
        (('a',), [1, 2, 3]),
        (('a',), [1, 2, 3]),
        (('a', 'b'), [1, 2, 3, 4]),
        (('a', 'b', 'c'), [1, 2, 3, 4, 5]),
        (('a', 'b', 'c', 'd'), [1, 2, 3, 4, 5, 6])
    ]
)

match_items_tuple=parametrize_cases(\
    'elements,expected_matched_sets', \
    [
        ({1, 2, 3}, {'a'}),
        ({1, 2, 3, 4}, {'a', 'b'}),
        ({1, 2, 3, 4, 5}, {'a', 'b', 'c'}),
        ({2, 3, 4, 5}, {'b', 'c'}),
        ({2, 3, 4, 5, 6}, {'b', 'c', 'd'})
    ]
)

sets_to_euler_tuples=parametrize_cases(\
    'test_sets,euler_sets', \
    [
        (
            {'a': [1, 2, 3]},
            {('a', ): [1, 2, 3]}
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
            { 
                'a': [1, 2, 3],
                'b': [2, 3, 4],
                'c': [3, 4, 5],
                'd': [3, 5, 6]
            },
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
