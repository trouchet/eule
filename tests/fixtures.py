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

worker_args_tuples=parametrize_cases("args, expected", [
    (
        # Test case 1: Simple input sets
        ({'A': {1, 2}, 'B': {2, 3}}, ['A', 'B'], 'A'),
        [(('B',), {3}), (('A', 'B',), {2}), (('A',), {1})]
    ),
    (
        # Test case 2: Empty input set for a key
        ({'A': set(), 'B': {3, 4}}, ['A', 'B'], 'A'),
        []
    ),
    (
        # Test case 3: All sets have elements, but some are disjoint
        ({'A': {1, 2, 3}, 'B': {4, 5, 6}}, ['A', 'B'], 'A'),
        [(('B',), {4, 5, 6}), (('A',), {1, 2, 3}), ]
    ),
    (
        # Test case 4: Complete subset - one set is a subset of another
        ({'A': {1, 2}, 'B': {1, 2, 3}}, ['A', 'B'], 'A'),
        [(('B',), {3}), (('A', 'B'), {1, 2})]
    ),
    (
        # Test case 5: Multiple overlapping elements across sets
        ({'A': {1, 2, 3}, 'B': {2, 3, 4}, 'C': {3, 4, 5}}, ['A', 'B', 'C'], 'A'),
        [
            (('C',), {5}),
            (('B', 'C'), {4}),
            (('A', 'B', 'C'), {3}),
            (('A', 'B'), {2}),
            (('A',), {1})
        ]
    ),
    (
        # Test case 6: Single-element sets with partial overlaps
        ({'A': {1}, 'B': {1, 2}, 'C': {2}}, ['A', 'B', 'C'], 'A'),
        [
            (('B', 'C',), {2}),
            (('A', 'B'), {1})
        ]
    ),
    (
        # Test case 7: No other keys to compare (only one set)
        ({'A': {1, 2}}, ['A'], 'A'),
        [(('A',), {1, 2})]
    ),
    (
        # Test case 8: Complex overlapping and disjoint elements
        ({'A': {1, 2, 3, 6}, 'B': {3, 4, 5}, 'C': {2, 5, 7}}, ['A', 'B', 'C'], 'A'),
        [
            (('C', ), {7}),
            (('A', 'C'), {2}),
            (('B', 'C'), {5}),
            (('B',), {4}),
            (('A', 'B'), {3}),
            (('A',), {1, 6})
        ]
    ),
    (
        # Test case 9: All sets empty
        ({'A': set(), 'B': set(), 'C': set()}, ['A', 'B', 'C'], 'A'),
        []
    ),
    (
        # Test case 10: `set_key` is non-empty, all other sets are empty
        ({'A': {1, 2, 3}, 'B': set(), 'C': set()}, ['A', 'B', 'C'], 'A'),
        [(('A',), {1, 2, 3})]
    )
])