
"""
Visualizes Genomic Feature overlaps using Matplotlib (Swimlane Chart).
Demonstrates how to visualize 1D biological interval data analyzed by eule.
"""
try:
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    from interval_sets import Interval, IntervalSet
    from eule import euler
except ImportError:
    print("Requires: pip install matplotlib interval-sets eule")
    exit(1)

def main():
    print("Generating Genomic Visualization...")

    # 1. Define Data (Same as case_genomics.py)
    # Scale down or shift for better plotting if needed, but we'll use raw bp
    
    atac_peaks = IntervalSet([
        Interval(10500, 11500),  # Peak A
        Interval(14000, 16000),  # Peak B
        Interval(18000, 19000)   # Peak C
    ])

    promoters = IntervalSet([
        Interval(11000, 12000),  # Promoter 1
        Interval(14500, 15500)   # Promoter 2
    ])

    enhancers = IntervalSet([
        Interval(10000, 13000),  # Super-Enhancer 1
        Interval(14800, 15200),  # Specific Enhancer 2
        Interval(18500, 19500)   # Enhancer 3
    ])

    genomic_features = {
        'Open Chromatin': atac_peaks,
        'Promoter': promoters,
        'Enhancer': enhancers
    }

    # 2. Compute Euler Logic
    # We use this to identify and color-code the "Active" regions
    diagram = euler(genomic_features)

    # 3. Visualization
    fig, ax = plt.subplots(figsize=(15, 6))

    # Y-positions for tracks
    y_positions = {
        'Open Chromatin': 3,
        'Promoter': 2,
        'Enhancer': 1,
        'Analysis': 0  # Result track
    }
    
    colors = {
        'Open Chromatin': 'skyblue',
        'Promoter': 'salmon',
        'Enhancer': 'gold'
    }

    # Plot Input Tracks
    for name, feature_set in genomic_features.items():
        y = y_positions[name]
        color = colors[name]
        
        # Draw baseline
        ax.hlines(y, 9000, 20000, color='gray', alpha=0.2, linewidth=1)
        
        for interval in feature_set:
            width = interval.length()
            # Rectangle(xy, width, height)
            rect = patches.Rectangle(
                (interval.start, y - 0.25), 
                width, 
                0.5, 
                facecolor=color, 
                edgecolor='black',
                alpha=0.8,
                label=name if interval == list(feature_set)[0] else None 
            )
            ax.add_patch(rect)

    # Plot Analysis Track (The Euler Result)
    # We want to highlight specific functional annotations
    ax.hlines(0, 9000, 20000, color='gray', alpha=0.2, linewidth=1)
    
    for keys, region in diagram.items():
        if not region or len(keys) < 2: continue # Skip single/empty regions for clarity

        # Determine annotation style
        feature_set = set(keys)
        
        annot_color = 'gray'
        annot_label = None
        
        if feature_set == {'Open Chromatin', 'Promoter', 'Enhancer'}:
            annot_color = 'red' 
            annot_label = 'ACTIVE PROMOTER'
        elif feature_set == {'Open Chromatin', 'Enhancer'}:
            annot_color = 'orange'
            annot_label = 'DISTAL ENHANCER'
        elif feature_set == {'Open Chromatin', 'Promoter'}:
            annot_color = 'purple'
            annot_label = 'POISED PROMOTER'

        if annot_label:
            for interval in region:
                rect = patches.Rectangle(
                    (interval.start, -0.25),
                    interval.length(),
                    0.5,
                    facecolor=annot_color,
                    edgecolor='black',
                    label=annot_label # Legend will dedup
                )
                ax.add_patch(rect)
                
                # Add Text Label above block
                ax.text(
                    interval.start + interval.length()/2, 
                    -0.4, 
                    annot_label,
                    ha='center', va='top', fontsize=8, rotation=0, color=annot_color, fontweight='bold'
                )

    # Formatting
    ax.set_yticks(list(y_positions.values()))
    ax.set_yticklabels(list(y_positions.keys()))
    ax.set_xlim(9500, 20000)
    ax.set_ylim(-1, 4)
    ax.set_xlabel("Genomic Position (bp)")
    ax.set_title("Genomic Feature Overlap Analysis (Chromosome 1)")
    
    # Custom legend handling to avoid duplicates
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    ax.legend(by_label.values(), by_label.keys(), loc='upper right')

    plt.tight_layout()
    plt.savefig("euler_genomics_viz.png")
    print("Saved visualization to euler_genomics_viz.png")

if __name__ == "__main__":
    main()
