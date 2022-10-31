![a night owl](/images/eule_small.png){.with-shadow .with-shadow}

[![image](https://img.shields.io/pypi/v/eule.svg)](https://pypi.python.org/pypi/eule)
[![image](https://codecov.io/gh/quivero/eule/branch/main/graph/badge.svg?token=PJMBaLIqar)](https://codecov.io/gh/quivero/eule)
[![Documentation Status](https://readthedocs.org/projects/eule/badge/?version=latest)](https://eule.readthedocs.io/en/latest/?version=latest)
[![Updates](https://pyup.io/repos/github/brunolnetto/eule/shield.svg)](https://pyup.io/repos/github/brunolnetto/eule/)

Euler\'s diagrams are non-empty Venn\'s diagrams


How to install
========

``` {.bash}
pip install eule
```

Features
========

We run a file with extension `*.py` with following content.

``` {.python}
#!/usr/bin/env python
from eule import spread_euler

diagram = spread_euler(
    {
        'a': [1, 2, 3],
        'b': [2, 3, 4],
        'c': [3, 4, 5],
        'd': [3, 5, 6]
    })

# Euler dictionary: {'a,b': [2], 'b,c': [4], 'a,b,c,d': [3], 'c,d': [5], 'd': [6], 'a': [1]}
print(diagram)
```

License
=======

-   Free software: MIT license
-   Documentation: <https://eule.readthedocs.io>.


Credits
=======

This package was created with
[Cookiecutter](https://github.com/audreyr/cookiecutter) and the
[audreyr/cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage)
project template.