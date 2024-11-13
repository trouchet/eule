import pytest


# tuplify
@pytest.fixture()
def tuple_():
    return (1,3,2,4)

@pytest.fixture()
def value():
    return 5

@pytest.fixture()
def updated_tuple():
    return (1,3,2,4,5)

@pytest.fixture()
def ordenated_tuple():
    return (1,2,3,4)

# "uniq"
@pytest.fixture()
def arr_with_repetition():
    return [1, 2, 3, 3]

@pytest.fixture()
def arr_with_repetition_uniq():
    return [1, 2, 3]

# "clear_sets"
@pytest.fixture()
def uncleared_dict():
    return {'a': [1, 2, 3], 'b': []}

@pytest.fixture()
def cleared_dict():
    return {'a': [1, 2, 3]}

@pytest.fixture()
def uncleared_list():
    return [[1, 2, 3], [], [4, 5]]

@pytest.fixture()
def cleared_list():
    return [[1, 2, 3], [4, 5]]

# Sets to Euler sets

# "listToSet", "unite", "difference"
@pytest.fixture()
def sets():
    return {
        'a': [1, 2, 3],
        'b': [2, 3, 4],
        'c': [3, 4, 5],
        'd': [3, 5, 6]
    }

@pytest.fixture()
def euler_sets_keys():
    return [
        ('a','b'),
        ('b','c'),
        ('a','b','c','d'),
        ('c','d'),
        ('d', ),
        ('a', )
    ]

@pytest.fixture()
def sets_boundaries():
    return {
        'a': ['b', 'c', 'd'],
        'b': ['a', 'c', 'd'],
        'c': ['a', 'b', 'd'],
        'd': ['a', 'b', 'c']
    }

@pytest.fixture()
def arrA():
    return [1,2,3]

@pytest.fixture()
def setA():
    return {1,2,3}

@pytest.fixture()
def tupleA():
    return (1,2,3)

@pytest.fixture()
def arrB():
    return [3,4,5]

@pytest.fixture()
def arrApB():
    return [1,2,3,4,5]

@pytest.fixture()
def arrAmB():
    return [1,2]

@pytest.fixture()
def arrAiB():
    return [3]

@pytest.fixture()
def verbose_key_sets():
    return {
        'set A': [1,2,3,4],
        'set B': [2,3,4,5],
        'set C': [3,4,5,6],
        'set D': [4,5,6,7],
    }

@pytest.fixture()
def verbose_key_sets_euler():
    return {
        ('set A',): [1],
        ('set A','set B',):[2],
        ('set A','set B','set C',):[3],
        ('set A','set B','set C','set D',):[4],
        ('set B','set C','set D',):[5],
        ('set C','set D',):[6],
        ('set D',): [7],
    }
