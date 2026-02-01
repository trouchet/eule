#!/usr/bin/env python3
"""
Working Example: Using interval-sets with eule.

This demonstrates how to use IntervalSet objects with eule's Euler diagram
generation through AUTOMATIC adapter integration - no manual wrapping needed!

Requirements:
    - Python 3.11+
    - interval-sets package

Installation:
    uv sync --extra interval
"""

try:
    from interval_sets import Interval, IntervalSet
    from eule import euler
    
    print("=" * 70)
    print("🎯 IntervalSet + Eule Automatic Integration")
    print("=" * 70)
    print()
    print("ℹ️  No manual wrapping needed - eule automatically handles IntervalSets!")
    print()
    
    # Example 1: Temperature ranges with automatic adaptation
    print("📊 Example 1: Temperature Ranges (Automatic)")
    print("-" * 70)
    
    # Create temperature ranges as IntervalSet objects - no wrapping needed!
    temp_ranges = {
        'cold': IntervalSet([Interval.closed(0, 15)]),
        'moderate': IntervalSet([Interval.closed(10, 25)]),
        'hot': IntervalSet([Interval.closed(20, 40)])
    }
    
    print(f"Cold:     {temp_ranges['cold']}")
    print(f"Moderate: {temp_ranges['moderate']}")
    print(f"Hot:      {temp_ranges['hot']}")
    print()
    
    print("🔧 Generating Euler diagram...")
    print("   (eule automatically detects and adapts IntervalSet objects)")
    result = euler(temp_ranges)
    
    print()
    print("📈 Euler Diagram Regions:")
    for region, interval_set in sorted(result.items(), key=lambda x: str(x[0])):
        print(f"  {region}: {interval_set}")
    
    print()
    print("-" * 70)
    
    # Example 2: Mixed interval types
    print()
    print("📊 Example 2: Time Periods (Open/Closed Intervals)")
    print("-" * 70)
    
    # Demonstrate different interval types - all work automatically!
    time_periods = {
        'morning': IntervalSet([Interval.closed(6, 12)]),      # [6, 12]
        'afternoon': IntervalSet([Interval.open(12, 18)]),     # (12, 18)
        'evening': IntervalSet([Interval.right_open(18, 24)])  # [18, 24)
    }
    
    print(f"Morning:   {time_periods['morning']}")
    print(f"Afternoon: {time_periods['afternoon']}")
    print(f"Evening:   {time_periods['evening']}")
    print()
    
    result2 = euler(time_periods)
    
    print("📈 Euler Diagram Regions:")
    for region, interval_set in sorted(result2.items(), key=lambda x: str(x[0])):
        print(f"  {region}: {interval_set}")
    
    print()
    print("-" * 70)
    
    # Example 3: Complex overlapping intervals
    print()
    print("📊 Example 3: Project Timelines (Complex Overlaps)")
    print("-" * 70)
    
    projects = {
        'Project A': IntervalSet([Interval.closed(0, 30)]),
        'Project B': IntervalSet([Interval.closed(15, 45)]),
        'Project C': IntervalSet([Interval.closed(25, 60)])
    }
    
    for name, timeline in projects.items():
        print(f"{name}: {timeline}")
    print()
    
    result3 = euler(projects)
    
    print("📈 Euler Diagram Regions (days):")
    for region, interval_set in sorted(result3.items(), key=lambda x: str(x[0])):
        print(f"  {region}: {interval_set}")
    
    print()
    print("=" * 70)
    print("✅ Success! IntervalSet objects work seamlessly with eule!")
    print("   No manual wrapping or adapter code needed!")
    print("=" * 70)
    
except ImportError as e:
    print("❌ Error: interval-sets library not installed")
    print()
    print("To use this example:")
    print("  1. Install: uv sync --extra interval")
    print("  2. Or: pip install interval-sets")
    print()
    print(f"Error details: {e}")
