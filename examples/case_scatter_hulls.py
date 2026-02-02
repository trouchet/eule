#!/usr/bin/env python3
"""
Advanced Case Study: Scatter Point Analysis via Convex Hulls.

Demonstrates using eule + Shapely to analyze relationships between groups of 2D data points.
Instead of arbitrary boxes, we compute the Convex Hull (polygon) of scattered data.

Scenario:
We have 3 animal species observed in a territory (GPS points).
We want to:
1. Define their territories (Convex Hull of observations).
2. Find the intersection zones (Where do species coexist?).
3. Calculate the area of exclusive vs shared territory.
"""

import numpy as np

try:
    from shapely.geometry import Point, Polygon, MultiPoint
    from eule import euler
    import matplotlib.pyplot as plt
    from matplotlib.collections import PatchCollection
    from matplotlib.patches import Polygon as MplPolygon
    import matplotlib.patches as mpatches
    import matplotlib.cm as cm
except ImportError:
    print("Requires: pip install shapely matplotlib numpy eule")
    exit(1)

def generate_cluster(center, spread, count=30, seed=None):
    """Generate a random cluster of points."""
    if seed: np.random.seed(seed)
    return np.random.normal(loc=center, scale=spread, size=(count, 2))

def plot_polygon(ax, geom, color, alpha=0.5, label=None):
    """Plot a Shapely geometry."""
    # Filter tiny noise polygons
    if geom.is_empty or geom.area < 1e-6:
        return
        
    patches = []
    if geom.geom_type == 'Polygon':
        geoms = [geom]
    elif geom.geom_type == 'MultiPolygon':
        geoms = geom.geoms
    else:
        return

    for poly in geoms:
        if poly.area < 1e-6: continue # Skip noise slivers
        x, y = poly.exterior.xy
        patches.append(MplPolygon(list(zip(x, y)), closed=True))

    if not patches: return

    p = PatchCollection(patches, facecolor=color, alpha=alpha, edgecolor='white', linewidth=0.5, label=label)
    ax.add_collection(p)

def main():
    print("=" * 60)
    print("🐾 Territory Analysis: Scatter Points -> Convex Hulls")
    print("=" * 60)

    # 1. Generate Data (GPS Observations)
    # Adjusted centers/spread to ensure nice overlaps AND exclusive zones
    # Wolves: Top Left
    wolves_pts = generate_cluster([3, 7], 1.2, seed=42)
    # Bears: Top Right
    bears_pts = generate_cluster([7, 7], 1.2, seed=43)
    # Deer: Center/Bottom (Prey, overlaps both)
    deer_pts = generate_cluster([5, 4], 1.8, seed=44)

    # 2. Compute Convex Hulls (The "Territories")
    wolves_poly = MultiPoint(wolves_pts).convex_hull
    bears_poly = MultiPoint(bears_pts).convex_hull
    deer_poly = MultiPoint(deer_pts).convex_hull

    territories = {
        'Wolves': wolves_poly,
        'Bears': bears_poly,
        'Deer': deer_poly
    }

    print("\n📍 Computed Territories (Polygon Areas):")
    for name, poly in territories.items():
        print(f"  {name:10s}: {poly.area:.2f} sq km units")

    # 3. Compute Euler Diagram
    print("\n🔍 Analyzing Ecological Overlap...")
    diagram = euler(territories)

    print("\n📈 Interaction Zones:")
    # Sort to show largest regions first
    for keys, region_adapter in sorted(diagram.items(), key=lambda x: -x[1].geometry.area):
        region = region_adapter.geometry 
        if region.is_empty or region.area < 1e-4: continue
        
        feature_set = set(keys)
        desc = "Unknown"
        
        if feature_set == {'Wolves', 'Bears', 'Deer'}:
            desc = "⚠️ HIGH CONFLICT ZONE (All species)"
        elif {'Wolves', 'Deer'}.issubset(feature_set):
            desc = "🥩 Predation Zone (Wolves hunting Deer)"
        elif {'Bears', 'Deer'}.issubset(feature_set):
            desc = "🥩 Predation Zone (Bears hunting Deer)"
        elif len(feature_set) == 1:
            desc = "🏡 Safe Home Range"

        print(f"\n  Region {list(feature_set)}:")
        print(f"    Desc: {desc}")
        print(f"    Area: {region.area:.2f}")

    # 4. Visualization
    print("\n🎨 Generating Visualization...")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))

    # Plot 1: Raw Points + Hulls
    ax1.set_title("1. Raw Data (GPS Points & Convex Hulls)")
    clrs = {'Wolves': 'grey', 'Bears': 'brown', 'Deer': 'green'}
    
    # Plot points
    ax1.scatter(wolves_pts[:,0], wolves_pts[:,1], c=clrs['Wolves'], s=15, label='Wolves (Pts)')
    ax1.scatter(bears_pts[:,0], bears_pts[:,1], c=clrs['Bears'], s=15, label='Bears (Pts)')
    ax1.scatter(deer_pts[:,0], deer_pts[:,1], c=clrs['Deer'], s=15, label='Deer (Pts)')
    
    # Plot Hulls (Outlines)
    for name, poly in territories.items():
        x, y = poly.exterior.xy
        ax1.plot(x, y, color=clrs[name], linewidth=2, linestyle='--')
        plot_polygon(ax1, poly, clrs[name], alpha=0.1)

    ax1.legend(loc='upper right')
    ax1.grid(True, alpha=0.2)

    # Plot 2: Euler Regions
    ax2.set_title("2. Computed Disjoint Interaction Zones")
    
    # Use matplotlib.colormaps if available (Matplotlib 3.7+), else fallback
    try:
        cmap = plt.get_cmap('tab10')
    except AttributeError:
        cmap = cm.get_cmap('tab10')
    
    legend_handles = []
    
    # Plot regions
    # Sort by key length to maybe plot simpler ones first? 
    # Actually sort by area is better? No, they are disjoint. Check order.
    # We want consistent colors.
    
    sorted_items = sorted(diagram.items(), key=lambda x: str(x[0]))
    
    i = 0
    for keys, region_adapter in sorted_items:
        region = region_adapter.geometry
        if region.is_empty or region.area < 1e-4: continue
        
        color = cmap(i % 10)
        i += 1
        
        label = " & ".join(sorted(list(keys)))
        
        plot_polygon(ax2, region, color, alpha=0.7)
        legend_handles.append(mpatches.Patch(color=color, label=label, alpha=0.7))

        # Annotate centroid
        pt = region.centroid
        ax2.text(pt.x, pt.y, str(len(keys)), fontsize=8, ha='center', fontweight='bold', color='white')

    ax2.legend(handles=legend_handles, loc='upper right')
    ax2.grid(True, alpha=0.2)
    
    # Match axes
    xl = ax1.get_xlim()
    yl = ax1.get_ylim()
    ax2.set_xlim(xl)
    ax2.set_ylim(yl)

    plt.tight_layout()
    plt.savefig("euler_scatter_hulls.png")
    print("Saved visualization to euler_scatter_hulls.png")

if __name__ == "__main__":
    main()
