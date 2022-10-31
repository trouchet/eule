.. image:: /images/eule_small.png
   :alt: a night owl
   :class: with-shadow
   :height: 10ex

.. image:: https://img.shields.io/pypi/v/eule.svg
        :target: https://pypi.python.org/pypi/eule

.. image:: https://codecov.io/gh/quivero/eule/branch/main/graph/badge.svg?token=PJMBaLIqar
        :target: https://codecov.io/gh/quivero/eule

.. image:: https://readthedocs.org/projects/eule/badge/?version=latest
        :target: https://eule.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status


.. image:: https://pyup.io/repos/github/brunolnetto/eule/shield.svg
     :target: https://pyup.io/repos/github/brunolnetto/eule/
     :alt: Updates



Euler's diagrams are non-empty Venn's diagrams


* Free software: MIT license
* Documentation: https://eule.readthedocs.io.


How to install
--------

.. code-block:: bash

    pip install eule

Features
--------

We run a `*.py` file with following content.

.. code-block:: python
    
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


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
