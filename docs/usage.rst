=====
Usage
=====

To use eule in a project::

    import eule

Minimal example
-----------------------------

We run a file with extension `*.py` with following content:

..  code-block:: python
    :caption: Minimal example

    from eule import euler, euler_keys, euler_boundaries, Euler

    sets = {
        'a': [1, 2, 3],
        'b': [2, 3, 4],
        'c': [3, 4, 5],
        'd': [3, 5, 6]
    }

    euler_diagram = euler(sets)
    euler_keys = euler_keys(sets)
    euler_boundaries = euler_boundaries(sets)
    euler_instance=Euler(sets)

    # Euler dictionary:
    # {'a,b': [2], 'b,c': [4], 'a,b,c,d': [3], 'c,d': [5], 'd': [6], 'a': [1]}
    print(euler_diagram)
    print(euler_instance.as_dict())

    print('\n')

    # Euler keys list:
    # ['a,b', 'b,c', 'a,b,c,d', 'c,d', 'd', 'a']
    print(euler_keys)
    print(euler_instance.euler_keys())

    print('\n')

    # Euler boundaries dictionary:
    # {
    #   'a': ['b', 'c', 'd'],
    #   'b': ['a', 'c', 'd'],
    #   'c': ['a', 'b', 'd'],
    #   'd': ['a', 'b', 'c']
    # }
    print(euler_boundaries)
    print(euler_instance.euler_boundaries())

    print('\n')

    # Euler instance match:
    # {'a'}
    # {'a', 'b'}
    # {'c', 'a', 'b'}

    print(euler_instance.match({1,2,3}))
    print(euler_instance.match({1,2,3,4}))
    print(euler_instance.match({1,2,3,4,5}))

    print('\n')

    # Euler instance getitem dunder:
    # [1, 2, 3]
    # [1, 2, 3]
    # [1, 2, 3, 4]
    # [1, 2, 3, 4, 5]
    print(euler_instance['a'])
    print(euler_instance[('a', )])
    print(euler_instance[('a', 'b', )])
    print(euler_instance[('a', 'b', 'c',)])

    print('\n')

    # Euler instance remove_key:
    euler_instance.remove_key('a')
    print(euler_instance.as_dict())
