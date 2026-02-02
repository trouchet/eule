"""
Example: Multi-dimensional Spatial Analysis using BoxSets + Eule.

This demonstrates how to use 2D/3D Boxes (through the eule adapter) to find overlapping spatial regions.

Problem Domain:
- We have defined "zones" in a 2D space (e.g., a factory floor, a map).
- We have object locations (points or bounding boxes).
- We want to classify objects into zones and find intersection patterns.
"""

try:
    from interval_sets import Interval, Box, BoxSet
    from eule import euler
except ImportError:
    print("This example requires interval-sets library.")
    exit(1)

def main():
    print("=" * 60)
    print("🗺️  Spatial Analysis: 2D Zones and Objects")
    print("=" * 60)

    # 1. Define Spatial Zones (2D Boxes)
    # Zone A: Top-Left square [0,10] x [0,10]
    zone_a = BoxSet([Box([Interval(0, 10), Interval(0, 10)])])
    
    # Zone B: Bottom-Right square [5,15] x [5,15]
    # Overlaps with A in [5,10]x[5,10]
    zone_b = BoxSet([Box([Interval(5, 15), Interval(5, 15)])])
    
    # Zone C: Vertical strip [8, 12] x [0, 20]
    # Overlaps A and B
    zone_c = BoxSet([Box([Interval(8, 12), Interval(0, 20)])])

    spatial_zones = {
        'Zone A': zone_a,
        'Zone B': zone_b,
        'Zone C': zone_c
    }

    print("\n📍 Defined Zones:")
    for name, zone in spatial_zones.items():
        print(f"  {name}: {zone}")

    # 2. Compute Euler Diagram of the Space
    # This finds the disjoint regions formed by the overlapping zones
    print("\n🔍 Computing Spatial Intersections...")
    diagram = euler(spatial_zones)

    print("\n📈 Disjoint Spatial Regions:")
    for region_keys, box_set in sorted(diagram.items(), key=lambda x: str(x[0])):
        # box_set is a BoxSetAdapter, iterate to get Boxes
        boxes = list(box_set)
        if not boxes: continue
        
        print(f"\n  Region {region_keys}:")
        for b in boxes:
            # Format nicely: [x1, x2] x [y1, y2]
            int_strs = [f"[{i.start:.1f}, {i.end:.1f}]" for i in b.intervals]
            print(f"    {' x '.join(int_strs)}")
            
            # Calculate area of this region segment
            print(f"    Area: {b.volume():.2f}")

    print("\n" + "="*60)
    print("✅ Success! 2D BoxSets are automatically handled.")
    print("="*60)

if __name__ == "__main__":
    main()
