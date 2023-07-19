![a night owl](https://github.com/trouchet/eule/blob/main/images/eule_small.png?raw=true)

[![Version](https://img.shields.io/pypi/v/eule.svg)](https://pypi.python.org/pypi/eule)
[![python](https://img.shields.io/pypi/pyversions/eule.svg)](https://pypi.org/project/eule/)
[![downloads](https://img.shields.io/pypi/dm/eule)](https://pypi.org/project/eule/)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/trouchet/eule/HEAD)

[![codecov](https://codecov.io/gh/trouchet/eule/branch/main/graph/badge.svg?token=PJMBaLIqar)](https://codecov.io/gh/trouchet/eule)
[![Documentation Status](https://readthedocs.org/projects/eule/badge/?version=latest)](https://eule.readthedocs.io/en/latest/?version=latest)
[![Lint workflow](https://github.com/trouchet/eule/actions/workflows/check-lint.yaml/badge.svg)](https://github.com/trouchet/eule/actions/workflows/check-lint.yaml)

Euler\'s diagrams are non-empty Venn\'s diagrams. For further information about:

1. the library: on URL <https://eule.readthedocs.io>;
2. Euler diagrams: on wikipedia article <https://en.wikipedia.org/wiki/Euler_diagram>

Motivation
================

<img src="https://github.com/trouchet/eule/blob/main/images/euler_venn.png?raw=true" width="400" height="364"/>

How to install
================

We run the command on desired installation environment:

``` {.bash}
pip install eule
```

Minimal example
================

We run command `python example.py` on the folder with file `example.py` and following content:

``` {.python}
#!/usr/bin/env python
from eule import euler, euler_keys, euler_boundaries

sets = {
    'a': [1, 2, 3],
    'b': [2, 3, 4],
    'c': [3, 4, 5],
    'd': [3, 5, 6]
}

euler_diagram = euler(sets)
euler_keys_ = euler_keys(sets)
euler_boundaries_ = euler_boundaries(sets)

# Euler dictionary: 
# {
#     ('b', 'c'): [4],
#     ('c', 'd'): [5],
#     ('a', 'b', 'c', 'd'): [3],
#     ('d',): [6],
#     ('a', 'b'): [2],
#     ('a',): [1]
# }
print(euler_diagram)

# Euler keys list:
# [('b', 'c'), ('c', 'd'), ('a', 'b', 'c', 'd'), ('d',), ('a', 'b'), ('a',)]
print(euler_keys_)

# Euler boundaries dictionary: 
# {
#     'a': ['b', 'c', 'd'],
#     'b': ['a', 'c', 'd'],
#     'c': ['a', 'b', 'd'],
#     'd': ['a', 'b', 'c']
# }
print(euler_boundaries_)
```
