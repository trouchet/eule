#!/usr/bin/env python3
"""
Example: Using eule with interval-sets library.

This example demonstrates how eule can work with the interval-sets library
to perform Euler diagram operations on interval objects.

Requirements:
    - Python 3.11+
    - interval-sets package: pip install interval-sets

Installation:
    uv sync --extra interval

Note: The interval-sets library requires Python 3.11+. If you're using Python 3.9 or 3.10,
      this example won't work, but you can still use eule with regular sets, lists, and
      custom set-like objects.
"""

try:
    from interval_sets import IntInterval
    from eule import euler

    # Create interval sets
    # IntInterval.closed(a, b) creates an interval [a, b] (inclusive on both ends)
    intervals_a = IntInterval.closed(1, 5) | IntInterval.closed(10, 15)
    intervals_b = IntInterval.closed(3, 7) | IntInterval.closed(12, 20)
    intervals_c = IntInterval.closed(2, 4) | IntInterval.closed(14, 16)

    print("Interval-Sets Integration Example")
    print("=" * 60)
    print()
    print("Interval Set A:", intervals_a)
    print("Interval Set B:", intervals_b)
    print("Interval Set C:", intervals_c)
    print()

    # Use eule's adaptation system to work with interval-sets
    print("Computing Euler diagram with interval-sets...")
    result = euler([intervals_a, intervals_b, intervals_c])
    
    print()
    print("Result:")
    for region, elements in result.items():
        print(f"  Region {region}: {elements}")
    
    print()
    print("✅ Interval-sets integration working!")
    print()
    print("The adaptation system automatically detected that interval-sets")
    print("objects implement the SetLike protocol and used them directly")
    print("without any explicit conversion.")

except ImportError as e:
    print("⚠️  interval-sets library not installed")
    print()
    print("To use this example, you need:")
    print("  1. Python 3.11 or higher")
    print("  2. Install interval-sets: uv sync --extra interval")
    print()
    print("Alternative: Use eule with other set-like objects:")
    print()
    
    from eule import euler
    
    # Demonstrate with regular sets
    print("Example with regular sets:")
    sets = [
        {1, 2, 3, 4, 5, 10, 11, 12, 13, 14, 15},
        {3, 4, 5, 6, 7, 12, 13, 14, 15, 16, 17, 18, 19, 20},
        {2, 3, 4, 14, 15, 16}
    ]
    result = euler(sets)
    print(f"Result: {result}")
    print()
    print("✅ Regular sets work without any additional dependencies!")
