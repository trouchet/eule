#!/usr/bin/env python3
"""
Example: Audio Frequency Masking Analysis.

Using IntervalSets to analyze frequency clashes in a music mix.
Demonstrates non-temporal use of continuous intervals.
"""

try:
    from interval_sets import Interval, IntervalSet
    from eule import euler
except ImportError:
    print("pip install interval-sets eule")
    exit(1)

def main():
    print("🎵 Audio Engineer Assistant: Frequency Clash Detection")
    print("====================================================\n")

    # Defined core frequency ranges for instruments (in Hz)
    # Human hearing: 20Hz - 20kHz
    
    # Kick Drum: Deep sub (40-80) and "knock" (2.5k-4k), plus body
    # Let's simplify: 40-200 Hz
    eq_kick = IntervalSet([Interval(40, 200)])
    
    # Bass Guitar: Fundamentals overlap kick significantly
    # 60-300 Hz
    eq_bass = IntervalSet([Interval(60, 300)])
    
    # Synths/Pads: Low-mids can muddy the mix
    # 150-5000 Hz
    eq_synth = IntervalSet([Interval(150, 5000)])

    instruments = {
        'Kick': eq_kick,
        'Bass': eq_bass,
        'Synth': eq_synth
    }
    
    # 1. Analyze Overlap
    print("🔍 Analyzing Frequency Spectrum...")
    diagram = euler(instruments)
    
    # 2. Report Findings
    print("\n📊 Mixing Report:")
    
    # We are looking for "Mud" (Low-end clashes)
    clash_found = False
    
    for keys, region in sorted(diagram.items(), key=lambda x: -len(x[0])): # Most overlapping first
        # IntervalSet can be disjoint, flatten to list of intervals
        ranges = list(region)
        if not ranges: continue
        
        # Format string "40-60Hz"
        range_strs = [f"{int(r.start)}-{int(r.end)}Hz" for r in ranges]
        desc = ", ".join(range_strs)
        
        feature_set = set(keys)
        
        print(f"\n  Region {list(feature_set)}:")
        print(f"    Range: {desc}")
        
        # Expert System Logic
        if {'Kick', 'Bass'}.issubset(feature_set):
            # Intersection of Kick and Bass is critical
            print("    ⚠️  LOW END CLASH: Kick & Bass fighting here.")
            print("       -> Suggest: Sidechain compression or EQ cut on Bass.")
            clash_found = True
            
        elif {'Bass', 'Synth'}.issubset(feature_set):
            # Check if this overlap is in the "Mud" zone (200-500Hz)
            # Simple check: does any interval overlap 200-500?
            is_muddy = False
            for r in ranges:
                if max(r.start, 200) < min(r.end, 500):
                    is_muddy = True
            
            if is_muddy:
                print("    ⚠️  MUD WARNING: Synth masking Bass clarity.")
                print("       -> Suggest: High-pass filter Synth above 300Hz.")

    if not clash_found:
        print("\n✅ Mix is clean!")

if __name__ == "__main__":
    main()
