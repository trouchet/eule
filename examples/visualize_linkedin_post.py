#!/usr/bin/env python3
"""
LinkedIn Showcase: Eule Capabilities
Combines Spatial Analysis (Boxes) and Ecological Analysis (Convex Hulls) into one summary image.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.colors as mcolors
from matplotlib.collections import PatchCollection
from matplotlib.patches import Polygon as MplPolygon
import matplotlib.patches as mpatches

try:
    from interval_sets import Interval, Box, BoxSet
    from shapely.geometry import MultiPoint
    from eule.adapters.shapely_geom import ShapelyAdapter
    from eule import euler
except ImportError:
    print("Requires: pip install shapely matplotlib interval-sets numpy eule")
    exit(1)

# ==========================================
# PART 1: Helpers for Spatial (Boxes)
# ==========================================

def is_close(a, b, tol=1e-5):
    return abs(a - b) < tol

def is_on_boundary(val, range_start, range_end, intervals, axis_idx):
    """Check if segment lies on the boundary of any original box."""
    for box in intervals:
        fixed_int = box.intervals[axis_idx]
        spanning_int = box.intervals[1-axis_idx]
        
        if is_close(val, fixed_int.start) or is_close(val, fixed_int.end):
            if (range_start >= spanning_int.start - 1e-5) and (range_end <= spanning_int.end + 1e-5):
                return True
    return False

def plot_smart_box(ax, box, color, parent_boxes_map, region_keys, alpha=0.5):
    """Plots box with dashed internal lines and solid external lines."""
    x_int = box.intervals[0]
    y_int = box.intervals[1]
    
    # Fill
    rect = patches.Rectangle(
        (x_int.start, y_int.start), x_int.length(), y_int.length(), 
        linewidth=0, facecolor=color, alpha=alpha
    )
    ax.add_patch(rect)
    
    # Get original boxes for this region's parents
    relevant_original_boxes = []
    for k in region_keys:
        if k in parent_boxes_map:
            relevant_original_boxes.extend(parent_boxes_map[k].boxes)
            
    # Draw Edges
    def draw_edge(x1, y1, x2, y2, is_vertical):
        if is_vertical:
            val, r_start, r_end, axis = x1, min(y1, y2), max(y1, y2), 0
        else:
            val, r_start, r_end, axis = y1, min(x1, x2), max(x1, x2), 1
            
        is_solid = is_on_boundary(val, r_start, r_end, relevant_original_boxes, axis)
        style = '-' if is_solid else '--'
        width = 1.5 if is_solid else 0.8
        alpha_line = 1.0 if is_solid else 0.6
        ax.plot([x1, x2], [y1, y2], color='black', linestyle=style, linewidth=width, alpha=alpha_line)

    draw_edge(x_int.start, y_int.start, x_int.end, y_int.start, False) # Bottom
    draw_edge(x_int.start, y_int.end, x_int.end, y_int.end, False)     # Top
    draw_edge(x_int.start, y_int.start, x_int.start, y_int.end, True)  # Left
    draw_edge(x_int.end, y_int.start, x_int.end, y_int.end, True)      # Right

# ==========================================
# PART 2: Helpers for Scatter (Polygons)
# ==========================================

def generate_cluster(center, spread, count=30, seed=None):
    if seed: np.random.seed(seed)
    return np.random.normal(loc=center, scale=spread, size=(count, 2))

def plot_polygon(ax, geom, color, alpha=0.5, label=None):
    if geom.is_empty or geom.area < 1e-6: return
        
    patches = []
    geoms = [geom] if geom.geom_type == 'Polygon' else geom.geoms
    
    for poly in geoms:
        if poly.area < 1e-6: continue
        x, y = poly.exterior.xy
        patches.append(MplPolygon(list(zip(x, y)), closed=True))

    if not patches: return
    p = PatchCollection(patches, facecolor=color, alpha=alpha, edgecolor='white', linewidth=0.5, label=label)
    ax.add_collection(p)

# ==========================================
# MAIN
# ==========================================

def main():
    print("Generating LinkedIn Showcase Image...")
    
    fig, axes = plt.subplots(2, 2, figsize=(12, 12))
    (ax1, ax2), (ax3, ax4) = axes
    
    plt.suptitle("Eule: Universal Logic For Sets, Intervals, and Shapes", fontsize=20, fontweight='bold', y=0.96)
    
    # -----------------------------
    # ROW 1: SPATIAL (BOXES)
    # -----------------------------
    print("Processing Row 1: Spatial Boxes...")
    
    # Data
    zone_a = BoxSet([Box([Interval(0, 10), Interval(0, 10)])])  
    zone_b = BoxSet([Box([Interval(5, 15), Interval(5, 15)])])  
    zone_c = BoxSet([Box([Interval(8, 12), Interval(0, 20)])])  
    spatial_zones = {'Zone A': zone_a, 'Zone B': zone_b, 'Zone C': zone_c}
    
    # Diagram
    diagram_box = euler(spatial_zones)
    
    # Plot Input
    ax1.set_title("1A. Input: Overlapping 2D Zones (BoxSet)", fontweight='bold')
    colors = ['r', 'g', 'b']
    for (name, zone), color in zip(spatial_zones.items(), colors):
        for box in zone.boxes:
            rect = patches.Rectangle((box.intervals[0].start, box.intervals[1].start), 
                                   box.intervals[0].length(), box.intervals[1].length(),
                                   linewidth=1, edgecolor='black', facecolor=color, alpha=0.3, label=name)
            ax1.add_patch(rect)
            
    # Legend outside
    ax1.legend(loc='upper left', bbox_to_anchor=(1.02, 1), borderaxespad=0.)
    ax1.set_xlim(-2, 18); ax1.set_ylim(-2, 22)
    ax1.grid(True, linestyle='--', alpha=0.3)
    
    # Plot Output
    ax2.set_title("1B. Output: Exact Disjoint Decomposition (Dashed=Internal)", fontweight='bold')
    region_colors = list(mcolors.TABLEAU_COLORS.values())
    legend_patches = []
    
    for i, (region_keys, box_set) in enumerate(sorted(diagram_box.items(), key=lambda x: str(x[0]))):
        if not box_set: continue
        color = region_colors[i % len(region_colors)]
        short_keys = [k.replace("Zone ", "") for k in region_keys]
        label = " & ".join(sorted(short_keys))
        
        for box in box_set:
            plot_smart_box(ax2, box, color, spatial_zones, region_keys, alpha=0.7)
            
        legend_patches.append(patches.Patch(color=color, label=label, alpha=0.7))
        
    ax2.legend(handles=legend_patches, loc='upper left', bbox_to_anchor=(1.02, 1), borderaxespad=0.)
    ax2.set_xlim(-2, 18); ax2.set_ylim(-2, 22)
    ax2.grid(True, linestyle='--', alpha=0.3)

    # -----------------------------
    # ROW 2: ECOLOGY (SCATTER/POLYGON)
    # -----------------------------
    print("Processing Row 2: Ecological Polygons...")
    
    # Data
    wolves_pts = generate_cluster([3, 7], 1.2, seed=42)
    bears_pts = generate_cluster([7, 7], 1.2, seed=43)
    deer_pts = generate_cluster([5, 4], 1.8, seed=44)
    
    wolves_poly = MultiPoint(wolves_pts).convex_hull
    bears_poly = MultiPoint(bears_pts).convex_hull
    deer_poly = MultiPoint(deer_pts).convex_hull
    
    territories = {'Wolves': wolves_poly, 'Bears': bears_poly, 'Deer': deer_poly}
    diagram_poly = euler(territories)
    
    # Plot Input
    ax3.set_title("2A. Input: GPS Scatter -> Convex Hulls", fontweight='bold')
    clrs = {'Wolves': 'grey', 'Bears': 'brown', 'Deer': 'green'}
    
    ax3.scatter(wolves_pts[:,0], wolves_pts[:,1], c=clrs['Wolves'], s=15, alpha=0.6)
    ax3.scatter(bears_pts[:,0], bears_pts[:,1], c=clrs['Bears'], s=15, alpha=0.6)
    ax3.scatter(deer_pts[:,0], deer_pts[:,1], c=clrs['Deer'], s=15, alpha=0.6)
    
    for name, poly in territories.items():
        x, y = poly.exterior.xy
        ax3.plot(x, y, color=clrs[name], linewidth=2, linestyle='--')
        plot_polygon(ax3, poly, clrs[name], alpha=0.1, label=name)
        
    # Manual legend for ax3 shapes + scatter
    handles = [
        mpatches.Patch(color=clrs['Wolves'], label='Wolves', alpha=0.5),
        mpatches.Patch(color=clrs['Bears'], label='Bears', alpha=0.5),
        mpatches.Patch(color=clrs['Deer'], label='Deer', alpha=0.5)
    ]
    ax3.legend(handles=handles, loc='upper left', bbox_to_anchor=(1.02, 1), borderaxespad=0.)
    ax3.grid(True, alpha=0.3)

    # Plot Output
    ax4.set_title("2B. Output: Disjoint Interaction Zones", fontweight='bold')
    try:
        cmap = plt.get_cmap('tab10')
    except AttributeError:
        import matplotlib.cm as cm
        cmap = cm.get_cmap('tab10')

    legend_handles_poly = []
    
    # Sort for consistent colors
    sorted_poly_items = sorted(diagram_poly.items(), key=lambda x: str(x[0]))
    
    for i, (keys, region_adapter) in enumerate(sorted_poly_items):
        region = region_adapter.geometry
        if region.is_empty or region.area < 1e-4: continue
        
        color = cmap(i % 10)
        label = " & ".join(sorted(list(keys)))
        
        plot_polygon(ax4, region, color, alpha=0.7)
        legend_handles_poly.append(mpatches.Patch(color=color, label=label, alpha=0.7))
        
        pt = region.centroid
        ax4.text(pt.x, pt.y, str(len(keys)), fontsize=9, ha='center', fontweight='bold', color='white')
        
    ax4.legend(handles=legend_handles_poly, loc='upper left', bbox_to_anchor=(1.02, 1), borderaxespad=0.)
    
    # Match limits
    ax4.set_xlim(ax3.get_xlim())
    ax4.set_ylim(ax3.get_ylim())
    ax4.grid(True, alpha=0.3)

    # Final Layout
    for ax in axes.flat:
        ax.set_aspect('equal')
        
    plt.tight_layout(rect=[0, 0.03, 1, 0.95]) # Make room for suptitle
    plt.subplots_adjust(wspace=0.1, hspace=0.25) # Less whitespace
    
    outfile = "linkedin_eule_showcase.png"
    plt.savefig(outfile, dpi=150, bbox_inches='tight')
    print(f"Saved {outfile}")

if __name__ == "__main__":
    main()
