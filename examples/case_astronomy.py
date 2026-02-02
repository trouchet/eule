#!/usr/bin/env python3
"""
Example: Astronomy Observation Planning.

Using Shapely Polygons to coordinate multi-telescope observations.
Finds regions of the sky covered by ALL instruments for Deep Field studies.
"""

try:
    from shapely.geometry import Point, Polygon
    from eule import euler
    import math
except ImportError:
    print("pip install shapely eule")
    exit(1)

def main():
    print("🔭 Astronomy Survey Planner")
    print("===========================\n")

    # Define Field of View (FOV) on sky map (simplified 2D coords)
    
    # 1. Broad Survey (Wide Field Telescope) - e.g. LSST/Rubin
    # Large rectangle: 0-10 deg RA, 0-10 deg Dec
    fov_survey = Polygon([(0,0), (10,0), (10,10), (0,10)])
    
    # 2. Space Telescope A (e.g. Hubble) - High resolution, distinct pointing
    # Rotated square centered at (5, 5)
    # Let's approximate a diamond shape
    fov_hubble = Polygon([(5, 2), (8, 5), (5, 8), (2, 5)])
    
    # 3. Space Telescope B (e.g. JWST) - Infrared, specific target
    # Offset square: 4-7 RA, 4-7 Dec
    fov_jwst = Polygon([(4, 4), (7, 4), (7, 7), (4, 7)])

    instruments = {
        'Survey': fov_survey,
        'HST': fov_hubble,
        'JWST': fov_jwst
    }
    
    print("Computing Sky Coverage Overlaps...")
    diagram = euler(instruments)
    
    # Analyze
    print("\n🌌 Observation Zones:")
    
    # Sort by overlap depth (more instruments = higher priority for data fusion)
    for keys, region_adapter in sorted(diagram.items(), key=lambda x: -len(x[0])):
        if region_adapter.geometry.is_empty: continue
        
        area = region_adapter.geometry.area
        feature_set = set(keys)
        
        print(f"\n  Instruments: {list(feature_set)}")
        print(f"    Sky Area: {area:.2f} sq deg")
        
        if len(feature_set) == 3:
            print("    🎯 GOLDEN TARGET: Multi-Wavelength Deep Field Candidate!")
            print("       (Visible + IR + Wide Context available)")
        elif 'HST' in feature_set and 'JWST' in feature_set:
            print("    💎 High-Res Priority: HST + JWST overlap.")

if __name__ == "__main__":
    main()
