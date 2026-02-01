#!/usr/bin/env python3
"""
Hybrid Example: Temporal Event Analysis with Eule + Interval-Sets

Demonstrates combining:
- Discrete events (sensor readings, user actions, log entries)
- Continuous time windows (maintenance periods, business hours, availability)
  used to CLASSIFY events into categories
- Euler diagrams to reveal OVERLAPPING event patterns

Key insight: interval-sets defines categories, euler reveals intersections.
"""

try:
    from interval_sets import Interval, IntervalSet
    from eule import euler
    
    print("=" * 80)
    print("🕐 Temporal Event Analysis: Discrete Events + Continuous Time Windows")
    print("=" * 80)
    print()
    
    # ============================================================================
    # Example 1: Alert Pattern Analysis
    # ============================================================================
    print("📊 Example 1: Finding Alert Patterns Across Time Windows")
    print("-" * 80)
    print()
    
    # DISCRETE: Individual alert timestamps (hours since midnight)
    alert_ids = list(range(1, 13))  # Alert IDs: 1-12
    alert_times = {
        1: 2.5, 2: 5.0, 3: 8.5, 4: 12.0,
        5: 16.5, 6: 19.0, 7: 21.0, 8: 22.5,
        9: 7.5, 10: 9.0, 11: 13.5, 12: 20.0
    }
    
    # CONTINUOUS: Time window definitions using interval-sets
    time_windows = {
        'morning_shift': IntervalSet([Interval.closed(6, 14)]),
        'evening_shift': IntervalSet([Interval.closed(14, 22)]),
        'maintenance_window': IntervalSet([Interval.closed(8, 10), Interval.closed(19, 23)]),
        'peak_hours': IntervalSet([Interval.closed(9, 11), Interval.closed(16, 18)])
    }
    
    print("Alert Timestamps:")
    for alert_id in sorted(alert_ids):
        print(f"  Alert #{alert_id}: {alert_times[alert_id]:5.1f}h")
    
    print("\nTime Window Definitions (continuous ranges):")
    for name, interval in time_windows.items():
        print(f"  {name:20s}: {interval}")
    
    # CLASSIFY: Map each alert to the windows it falls within
    alert_categories = {
        window_name: {
            alert_id for alert_id in alert_ids
            if alert_times[alert_id] in window_interval
        }
        for window_name, window_interval in time_windows.items()
    }
    
    print("\nAlerts by Time Window:")
    for window, alerts in alert_categories.items():
        if alerts:
            print(f"  {window:20s}: {sorted(alerts)}")
    
    # EULER DIAGRAM: Find non-overlapping regions (alert patterns)
    print("\n📈 Euler Diagram - Alert Patterns:")
    print("   (Which alerts fall into which COMBINATIONS of time windows?)")
    print()
    
    diagram = euler(alert_categories)
    
    for region, alerts in sorted(diagram.items(), key=lambda x: (len(x[0]), x[0])):
        if alerts:
            alert_list = sorted(alerts)
            times = [alert_times[a] for a in alert_list]
            print(f"  Region {region}:")
            print(f"    Alerts: {alert_list} at times {[f'{t:.1f}h' for t in times]}")
    
    print()
    print("💡 Insight: Euler reveals EXACT overlap patterns")
    print("   - Alerts only in morning_shift")
    print("   - Alerts in BOTH evening_shift AND maintenance_window")
    print("   - etc.")
    
    print()
    print("-" * 80)
    
    # ============================================================================
    # Example 2: User Session Pattern Analysis
    # ============================================================================
    print()
    print("📊 Example 2: User Login Patterns Across Work Schedules")
    print("-" * 80)
    print()
    
    # DISCRETE: Individual user sessions (session IDs)
    sessions = list(range(1, 21))  # 20 sessions
    session_times = {
        1: 8.5, 2: 9.0, 3: 10.5, 4: 12.0, 5: 14.5,
        6: 15.0, 7: 17.5, 8: 18.0, 9: 20.0, 10: 22.0,
        11: 8.0, 12: 11.5, 13: 13.0, 14: 16.5, 15: 19.0,
        16: 9.5, 17: 10.0, 18: 14.0, 19: 16.0, 20: 21.5
    }
    
    # CONTINUOUS: Work schedule categories
    schedules = {
        'core_hours': IntervalSet([Interval.closed(9, 17)]),
        'flexible_hours': IntervalSet([Interval.closed(8, 19)]),
        'lunch_time': IntervalSet([Interval.closed(12, 14)]),
        'evening_access': IntervalSet([Interval.closed(17, 23)])
    }
    
    print("Login Sessions:")
    for i, session_id in enumerate(sorted(sessions)[:10], 1):
        print(f"  Session #{session_id:2d}: {session_times[session_id]:5.1f}h", end="")
        if i % 5 == 0:
            print()
    print("  ...")
    
    print("\nWork Schedule Definitions:")
    for name, interval in schedules.items():
        print(f"  {name:15s}: {interval}")
    
    # CLASSIFY: Map sessions to schedule categories
    session_categories = {
        schedule_name: {
            sid for sid in sessions
            if session_times[sid] in schedule_interval
        }
        for schedule_name, schedule_interval in schedules.items()
    }
    
    # EULER DIAGRAM: Find session overlap patterns
    print("\n📈 Euler Diagram - Session Patterns:")
    print()
    
    diagram = euler(session_categories)
    
    for region, sids in sorted(diagram.items(), key=lambda x: (len(x[0]), x[0])):
        if sids:
            print(f"  {region}:")
            print(f"    {len(sids)} sessions: {sorted(list(sids))[:8]}{'...' if len(sids) > 8 else ''}")
    
    print()
    print("💡 Insight: Sessions that are ONLY in core_hours vs")
    print("   sessions in BOTH flexible_hours AND lunch_time, etc.")
    
    print()
    print("-" * 80)
    
    # ============================================================================
    # Example 3: NOT an Euler use case - Gap Analysis (interval-sets only)
    # ============================================================================
    print()
    print("📊 Example 3: Coverage Gap Analysis (interval-sets feature)")
    print("-" * 80)
    print("   Note: This demonstrates interval-sets, NOT euler diagrams")
    print()
    
    # Expected monitoring coverage (continuous)
    expected_coverage = IntervalSet([Interval.closed(0, 24)])
    actual_monitoring = IntervalSet([
        Interval.closed(0, 8),
        Interval.closed(10, 15),
        Interval.closed(17, 24)
    ])
    
    gaps = actual_monitoring.complement(expected_coverage)
    
    print(f"Expected Coverage: {expected_coverage}")
    print(f"Actual Monitoring: {actual_monitoring}")
    print(f"⚠️  Coverage Gaps: {gaps}")
    print(f"   Total gap duration: {gaps.measure():.1f} hours")
    
    print()
    print("💡 This example uses only interval-sets (set operations on ranges)")
    print("   No Euler diagram needed - no discrete elements to classify!")
    
    print()
    print("-" * 80)
    
    print()
    print("=" * 80)
    print("✅ Temporal analysis complete!")
    print()
    print("💡 KEY TAKEAWAY:")
    print("   ┌─────────────────────────────────────────────────────────┐")
    print("   │ interval-sets: Defines CATEGORIES (continuous ranges)  │")
    print("   │ Classification: Maps discrete elements to categories   │")
    print("   │ euler():  Reveals NON-OVERLAPPING category patterns    │")
    print("   └─────────────────────────────────────────────────────────┘")
    print()
    print("   Together, they expose hidden patterns in categorical data!")
    print("=" * 80)
    
except ImportError as e:
    print("❌ Error: Required libraries not installed")
    print()
    print("To run this example:")
    print("  1. Install: uv sync --extra interval")
    print("  2. Or: pip install eule interval-sets")
    print()
    print(f"Error details: {e}")
