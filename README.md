![a night owl](https://github.com/trouchet/eule/blob/main/images/eule_small.png?raw=true)

[![Version](https://img.shields.io/pypi/v/eule.svg)](https://pypi.python.org/pypi/eule)
[![downloads](https://img.shields.io/pypi/dm/eule)](https://pypi.org/project/eule/)
[![codecov](https://codecov.io/gh/trouchet/eule/branch/main/graph/badge.svg?token=PJMBaLIqar)](https://codecov.io/gh/trouchet/eule)
[![Documentation Status](https://readthedocs.org/projects/eule/badge/?version=latest)](https://eule.readthedocs.io/en/latest/?version=latest)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/trouchet/eule/HEAD)

**Eule** is a universal logic engine for generating Euler diagrams and analyzing set relationships. 

It generates **non-empty Euler diagrams** (disjoint partitions) for **ANY** type of overlapping data:
- **Discrete Sets**: Strings, integers, custom objects.
- **Continuous Intervals**: Time ranges, numerical values (via `interval-sets`).
- **Geometric Shapes**: 2D Polygons, 3D Boxes (via `shapely` and `box-sets`).

Motivation
================

<img src="https://github.com/trouchet/eule/blob/main/images/euler_venn.png?raw=true" width="400" height="364"/>

Installation
================

```bash
# Standard install (Discrete sets)
pip install eule

# With Interval support
pip install "eule[interval]"

# With Geometry support
pip install "eule[geometry]"

# For all features
pip install "eule[interval,geometry]"
```

Universal Logic Engine 🚀
=========================

Eule is no longer just for Python sets. It now supports the **SetLike Protocol**, allowing it to compute disjoint regions for advanced mathematical objects.

### 1. Discrete Sets (Standard)
```python
from eule import euler

sets = {
    'A': {1, 2, 3},
    'B': {2, 3, 4},
    'C': {3, 4, 5}
}
diagram = euler(sets)
# Returns disjoint decomposition: 
# {'A': {1}, 'B': {5}, 'C': {6}, 'A,B': {2}, ...}
```

### 2. Continuous Intervals (Time/Numbers)
*Requires `interval-sets`*

```python
from interval_sets import IntervalSet, Interval
from eule import euler

schedules = {
    'Alice': IntervalSet([Interval(9, 12), Interval(13, 17)]),
    'Bob':   IntervalSet([Interval(11, 14)])
}

# Find exact overlap: 11:00-12:00 and 13:00-14:00
diagram = euler(schedules) 
```

### 3. Geometric Shapes (2D/3D)
*Requires `shapely`*

```python
from shapely.geometry import Polygon
from eule import euler

territories = {
    'Wolves': Polygon([(0,0), (0,10), (10,10), (10,0)]),
    'Bears':  Polygon([(5,5), (5,15), (15,15), (15,5)])
}

# Automatically computes the exact Intersection Polygon!
diagram = euler(territories)
```

Examples
========

Check the `examples/` directory for advanced real-world use cases:

- **[case_scatter_hulls.py](examples/case_scatter_hulls.py)**: 🐾 **Ecology / Spatial** - Convex Hull analysis of scatter points (e.g., animal territories).
- **[case_3d_clash_detection.py](examples/case_3d_clash_detection.py)**: 🏗️ **Engineering / BIM** - 3D Box collision detection (Beams vs HVAC).
- **[case_scheduling.py](examples/case_scheduling.py)**: 🗓️ **Productivity** - Finding common free time across multiple calendars.
- **[case_audio_mixing.py](examples/case_audio_mixing.py)**: 🎵 **Audio Engineering** - Frequency masking analysis (Kick vs Bass clash detection).
- **[case_astronomy.py](examples/case_astronomy.py)**: 🔭 **Astronomy** - Multi-telescope sky survey coverage planning.
- **[case_security_audit.py](examples/case_security_audit.py)**: 🔐 **Cybersecurity** - Segregation of Duties (SoD) audit for toxic permission combinations.
- **[case_nlp_stylometry.py](examples/case_nlp_stylometry.py)**: 📜 **NLP** - Vocabulary overlap analysis.
- **[case_genomics.py](examples/case_genomics.py)**: 🧬 **Bioinformatics** - Identify functional genomic regions (e.g., Active Promoters).
- **[case_network_security.py](examples/case_network_security.py)**: 🛡️ **NetOps / Security** - Audit firewall rules using IP ranges.
- **[case_customer_segmentation.py](examples/case_customer_segmentation.py)**: 👥 **Business** - Segment customers by continuous metrics.

How to Contribute
=================

We welcome implementations of the `SetLike` protocol for new domains!
See [Protocol Specification](docs/design/PROTOCOL_SPECIFICATION.md).
