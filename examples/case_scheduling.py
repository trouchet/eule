#!/usr/bin/env python3
"""
Example: Intelligent Scheduling (1D Intervals).

Finds common meeting slots across multiple busy calendars.
Use De Morgan's Law logic: Free Time = Universe - Union(Busy Times).
"""

try:
    from interval_sets import Interval, IntervalSet
    from eule import euler
except ImportError:
    print("pip install interval-sets eule")
    exit(1)

def main():
    print("🗓️  Team Scheduling Assistant")
    print("===================================\n")

    # The "Universe": A Standard Work Day (9:00 to 17:00) -> Minutes 0 to 480
    work_day = IntervalSet([Interval(0, 480)]) # 8 hours
    
    # Defined Busy Slots (in minutes from 9:00 AM)
    # Alice: Busy morning (9-11) and late afternoon (16-17)
    # 0-120, 420-480
    cal_alice = IntervalSet([Interval(0, 120), Interval(420, 480)])
    
    # Bob: Busy around lunch (12-13) and early afternoon check-in (14-14:30)
    # 180-240, 300-330
    cal_bob = IntervalSet([Interval(180, 240), Interval(300, 330)])
    
    # Charlie: Busy with deep work mid-morning (10-12)
    # 60-180
    cal_charlie = IntervalSet([Interval(60, 180)])

    input_sets = {
        'Alice': cal_alice,
        'Bob': cal_bob,
        'Charlie': cal_charlie
    }

    print("🚫 Busy Schedules:")
    for name, cal in input_sets.items():
        print(f"  {name}: {cal}")

    # 1. Compute the Union of ALL Busy times
    # We can use eule to find the union region, or just use Set logic directly.
    # Let's use eule to see *who* causes the blocks.
    diagram = euler(input_sets)
    
    # 2. Reconstruct the Union of Busy intervals from the disjoint pieces
    all_intervals = []
    for keys, region in diagram.items():
        # Iterate over region (works for both IntervalSet and Adapter) to get Intervals
        all_intervals.extend(list(region))
        
    all_busy = IntervalSet(all_intervals)
        
    # 3. Calculate Free Time
    # Free = WorkDay - AllBusy
    free_time = work_day.difference(all_busy)
    
    print("\n✅ Available Meeting Slots (Free Time):")
    if not free_time:
        print("  No common time found! 😱")
    else:
        for interval in free_time:
            # Convert back to readable time
            start_min = interval.start
            end_min = interval.end
            
            s_hr = 9 + int(start_min // 60)
            s_mm = int(start_min % 60)
            e_hr = 9 + int(end_min // 60)
            e_mm = int(end_min % 60)
            
            print(f"  • {s_hr:02d}:{s_mm:02d} - {e_hr:02d}:{e_mm:02d} ({int(interval.length())} mins)")

    # 4. Optional: "Best bad option" (Who to exclude?)
    # We can inspect the 2-person intersections to see if excluding one person opens up time.
    print("\n🧐 Analysis of Conflicts:")
    for keys, region in diagram.items():
        # Only interested in overlaps (len > 1)
        if len(keys) > 1:
            r_str = str(region).replace("IntervalSet", "")
            print(f"  Conflict {list(keys)}: during {r_str}")

if __name__ == "__main__":
    main()
