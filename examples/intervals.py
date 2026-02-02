#!/usr/bin/env python3
"""
Interval-Sets Integration Example

This example demonstrates how the `eule` library automatically adapts `interval-sets` objects.
You can pass Interval objects directly to `euler()`, and they will be converted 
into compatible set-like objects automatically.
"""

try:
    from interval_sets import Interval, IntervalSet
    from eule import euler
except ImportError:
    print("This example requires the 'interval-sets' library.")
    print("Install it with: pip install interval-sets")
    exit(1)

def main():
    print("=" * 60)
    print("🔗 Integration: Eule + Interval-Sets")
    print("=" * 60)

    # 1. Define sets using Intervals
    # eule will use the registered adapter to handle these
    intervals = {
        'Morning': IntervalSet([Interval(6, 12)]),
        'WorkDay': IntervalSet([Interval(9, 17)]),
        'Evening': IntervalSet([Interval(17, 22)])
    }

    print("\nInput Intervals:")
    for k, v in intervals.items():
        print(f"  {k}: {v}")

    # 2. Generate Euler Diagram
    # The adapter wraps IntervalSet so eule can call .union(), .intersection(), etc.
    diagram = euler(intervals)

    print("\nEuler Diagram Results (Disjoint Intervals):")
    # The keys of the diagram are tuples representing the set intersections
    # The values are IntervalSetAdapter objects
    for keys, overlap_region in diagram.items():
        # Convert adapter back to string/native for display
        region_str = str(overlap_region)
        print(f"  Region {keys}: {region_str}")

    print("\n" + "=" * 60)
    print("✅ Integration successful!")

if __name__ == "__main__":
    main()
