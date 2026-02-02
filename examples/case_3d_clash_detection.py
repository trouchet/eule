#!/usr/bin/env python3
"""
Example: 3D Clash Detection (Volumetric Analysis).

Demonstrates using 3D Boxes to find physical collisions between objects.
This mimics a simplified CAD/BIM "Clash Detection" check.

We defined 3 types of objects in a room:
1. Structural Beams (Static, heavy)
2. HVAC Ducts (Running through the ceiling)
3. WiFi Signal Zones (Abstract volumes)
"""

try:
    from interval_sets import Interval, Box, BoxSet
    from eule import euler
except ImportError:
    print("pip install interval-sets eule")
    exit(1)

def main():
    print("🏗️  3D Clash Detection Simulation")
    print("===================================\n")

    # 1. Define 3D Objects as BoxSets
    # Coordinate System: X (Width), Y (Depth), Z (Height)

    # Beam: A horizontal structural beam at height Z=10
    # Spans X=[0, 20], Y=[5, 6] (thin), Z=[10, 11]
    beam = BoxSet([
        Box([Interval(0, 20), Interval(5, 6), Interval(10, 11)])
    ])

    # HVAC Duct: A pipe running crosses the beam
    # Spans X=[10, 12] (width 2), Y=[0, 15] (long), Z=[10.5, 11.5]
    # Note: It intersects the beam in Z!
    hvac = BoxSet([
        Box([Interval(10, 12), Interval(0, 15), Interval(10.5, 11.5)])
    ])

    # WiFi Zone: A service volume in the room
    # Covers a large area below the ceiling
    # X=[0, 15], Y=[0, 10], Z=[0, 12]
    wifi = BoxSet([
        Box([Interval(0, 15), Interval(0, 10), Interval(0, 12)])
    ])

    objects = {
        'Beam': beam,
        'HVAC': hvac,
        'WiFi': wifi
    }

    print("Defined Objects:")
    for name, obj in objects.items():
        # Approx volume check
        vol = sum(b.intervals[0].length() * b.intervals[1].length() * b.intervals[2].length() for b in obj.boxes)
        print(f"  {name}: {vol:.1f} m³")

    # 2. Run Analysis
    print("\n🔍 Detect Clashes (Intersections)...")
    diagram = euler(objects)

    # 3. Report Results
    clashes_found = False
    
    print("\n📊 Volumetric Report:")
    for keys, region in sorted(diagram.items(), key=lambda x: -len(x[0])):
        # Calculate volume of this region
        volume = 0.0
        for box in region.boxes:
            lx = box.intervals[0].length()
            ly = box.intervals[1].length()
            lz = box.intervals[2].length()
            volume += lx * ly * lz
        
        if volume < 0.001: continue

        feature_set = set(keys)
        # Interpretation
        if "Beam" in feature_set and "HVAC" in feature_set:
            status = "🚨 CRITICAL CLASH"
            clashes_found = True
        elif len(feature_set) > 1:
            status = "ℹ️  Overlap"
        else:
            status = "ok"

        print(f"  Region {list(feature_set)}:")
        print(f"    Status: {status}")
        print(f"    Volume: {volume:.2f} m³")
        
        # Detail the clash space
        if status.startswith("🚨"):
            print("    -> ACTION REQUIRED: Re-route HVAC or notch Beam.")

    if not clashes_found:
        print("\n✅ Design Validated: No physical clashes found.")
    else:
        print("\n❌ Design Errors Detected!")

if __name__ == "__main__":
    main()
