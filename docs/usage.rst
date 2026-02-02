=====
Usage
=====

Eule is a universal logic engine that can generate Euler diagrams for any type of data that supports set operations (union, intersection, difference).

It supports:

* **Discrete Sets** (standard Python sets, lists)
* **Continuous Intervals** (via ``interval-sets``)
* **Geometric Shapes** (via ``shapely``)

Discrete Sets (Standard)
------------------------

The most common usage is with standard Python sets or lists of hashable items.

.. code-block:: python

    from eule import euler

    sets = {
        'A': {1, 2, 3},
        'B': {2, 3, 4},
        'C': {3, 4, 5}
    }

    # Compute disjoint regions
    diagram = euler(sets)
    
    # Result:
    # {
    #   ('A',): {1}, 
    #   ('A', 'B'): {2},
    #   ('A', 'B', 'C'): {3},
    #   ('B', 'C'): {4},
    #   ('C',): {5}
    # }

Continuous Intervals
--------------------

Eule can analyze continuous ranges such as time intervals or numerical ranges using the ``interval-sets`` library.
This is useful for scheduling, resource allocation, and timeline analysis.

**Installation**: ``pip install "eule[interval]"``

.. code-block:: python

    from interval_sets import IntervalSet, Interval
    from eule import euler

    # Define schedules
    # Alice is busy 9-12 and 13-17
    # Bob is busy 11-14
    schedules = {
        'Alice': IntervalSet([Interval(9, 12), Interval(13, 17)]),
        'Bob':   IntervalSet([Interval(11, 14)])
    }

    # Compute overlap
    diagram = euler(schedules)

    # Result keys will show:
    # ('Alice', 'Bob') -> Interval [11, 12] and [13, 14]
    # ('Alice',)       -> Interval [9, 11] and [14, 17]
    # ('Bob',)         -> empty (Bob is fully covered by Alice during his busy time except... wait)
    # Actually Bob is busy 11-14. 
    # Alice 9-12 covers 11-12. 
    # Alice 13-17 covers 13-14.
    # So Bob is exclusive during [12, 13].

Geometric Shapes (2D/3D)
------------------------

Eule can compute the exact intersection and difference regions of 2D/3D shapes using ``shapely``.
This is useful for GIS, CAD, and spatial analysis.

**Installation**: ``pip install "eule[geometry]"``

.. code-block:: python

    from shapely.geometry import Polygon
    from eule import euler

    territories = {
        'Wolves': Polygon([(0,0), (0,10), (10,10), (10,0)]), # 10x10 square at 0,0
        'Bears':  Polygon([(5,5), (5,15), (15,15), (15,5)])  # 10x10 square at 5,5
    }

    diagram = euler(territories)

    # Access the geometry of the intersection
    intersection_region = diagram[('Wolves', 'Bears')]
    print(intersection_region.area) 
    # 25.0 (Overlap is 5x5 square)

Advanced: Custom Types
----------------------

You can use eule with any custom class that implements the **SetLike Protocol**.

Your class must implement:

* ``union(self, other)``
* ``intersection(self, other)``
* ``difference(self, other)``
* ``__iter__(self)``
* ``__bool__(self)`` (to check for emptiness)

See the `Protocol Specification <https://github.com/trouchet/eule/blob/main/docs/design/PROTOCOL_SPECIFICATION.md>`_ for details.
