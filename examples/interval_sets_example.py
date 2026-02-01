#!/usr/bin/env python3
"""
Example: Understanding interval-sets vs discrete sets.

This example demonstrates the difference between continuous intervals
(interval-sets library) and discrete sets (eule's primary use case).

Requirements:
    - Python 3.11+
    - interval-sets package: pip install interval-sets

Installation:
    uv sync --extra interval

Note: interval-sets works with continuous ranges, while eule works with discrete elements.
      For continuous analysis, use interval-sets directly. For discrete set analysis, use eule.
"""

try:
    from interval_sets import Interval, IntervalSet
    from eule import euler

    print("Interval-Sets Library Demonstration")
    print("=" * 60)
    print()
    print("⚠️  IMPORTANT: Different Use Cases")
    print()
    print("interval-sets: Works with continuous ranges (e.g., temperature ranges)")
    print("eule: Works with discrete elements (e.g., individual items)")
    print()
    
    # Demonstrate interval-sets directly (continuous analysis)
    print("1. Continuous Analysis with interval-sets (native):")
    print("-" * 60)
    
    # Create temperature ranges
    cold = IntervalSet([Interval.closed(0, 15)])
    moderate = IntervalSet([Interval.closed(10, 25)])
    hot = IntervalSet([Interval.closed(20, 40)])
    
    print(f"Cold temps:     {cold}")
    print(f"Moderate temps: {moderate}")
    print(f"Hot temps:      {hot}")
    print()
    
    # Perform set operations directly
    print("Regions (using interval-sets directly):")
    print(f"  Cold only:         {cold - moderate}")
    print(f"  Cold & Moderate:   {cold & moderate}")
    print(f"  Moderate only:     {moderate - (cold | hot)}")
    print(f"  Moderate & Hot:    {moderate & hot}")
    print(f"  Hot only:          {hot - moderate}")
    print()
    
    # Demonstrate discrete analysis with eule
    print("2. Discrete Analysis with eule:")
    print("-" * 60)
    
    # For discrete elements, use regular sets
    discrete_sets = {
        'category_a': {1, 2, 3, 4, 5},
        'category_b': {3, 4, 5, 6, 7},
        'category_c': {2, 4, 6, 8}
    }
    
    result = euler(discrete_sets)
    
    print("Sets:")
    for name, elements in discrete_sets.items():
        print(f"  {name}: {sorted(elements)}")
    print()
    
    print("Euler Diagram Regions:")
    for region, elements in sorted(result.items(), key=lambda x: str(x[0])):
        print(f"  {region}: {sorted(elements)}")
    
    print()
    print("✅ Both libraries work correctly in their respective domains!")
    print()
    print("Key Takeaway:")
    print("  - Use interval-sets for continuous ranges (intervals on ℝ)")
    print("  - Use eule for discrete elements (finite sets)")
    print("  - Both libraries excel at different types of analysis")
    print()
    print("For eule extension with custom discrete set types:")
    print("  - Implement SetLike protocol (union, intersection, difference, __iter__, __bool__)")
    print("  - Register with: from eule import register_adapter")
    print("  - See docs/design/PROTOCOL_SPECIFICATION.md for details")

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
