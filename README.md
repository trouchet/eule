![a night owl](https://raw.githubusercontent.com/quivero/eule/main/images/eule_small.png)

[![Version](https://img.shields.io/pypi/v/eule.svg)](https://pypi.python.org/pypi/eule)
[![python](https://img.shields.io/pypi/pyversions/eule.svg)](https://pypi.org/project/eule/)
[![Documentation Status](https://readthedocs.org/projects/eule/badge/?version=latest)](https://eule.readthedocs.io/en/latest/?version=latest)

[![codecov](https://codecov.io/gh/quivero/eule/branch/main/graph/badge.svg?token=PJMBaLIqar)](https://codecov.io/gh/quivero/eule)
[![Codecov workflow](https://github.com/quivero/eule/actions/workflows/test-coverage.yml/badge.svg)](https://github.com/quivero/eule/actions/workflows/test-coverage.yml)
[![Lint workflow](https://github.com/quivero/eule/actions/workflows/check-lint.yaml/badge.svg)](https://github.com/quivero/eule/actions/workflows/check-lint.yaml)
[![downloads](https://img.shields.io/pypi/dm/eule)](https://pypi.org/project/eule/)


Euler\'s diagrams are non-empty Venn\'s diagrams. For further information about:

1. the library: read the documentation on URL <https://eule.readthedocs.io>;
2. Euler diagrams: read the wikipedia article <https://en.wikipedia.org/wiki/Euler_diagram>

Motivation
================

<img src="https://github.com/quivero/eule/blob/main/images/euler_venn.png?raw=true" width="400" height="364"/>

How to install
================

We run the command on desired installation environment:

``` {.bash}
    pip install eule
```

Minimal example
================

We run a file with extension `*.py` with following content:

``` {.python}
#!/usr/bin/env python
from eule import spread_euler

set = {
    'a': [1, 2, 3],
    'b': [2, 3, 4],
    'c': [3, 4, 5],
    'd': [3, 5, 6]
}

diagram = spread_euler(set)

# Euler dictionary: {'a,b': [2], 'b,c': [4], 'a,b,c,d': [3], 'c,d': [5], 'd': [6], 'a': [1]}
print(diagram)
```

License
===============

-   Free software: MIT license


Credits
===============

This package was created with
[Cookiecutter](https://github.com/audreyr/cookiecutter) and the
[audreyr/cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage)
project template.
