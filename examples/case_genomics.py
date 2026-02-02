#!/usr/bin/env python3
"""
Scientific Case Study: Genomic Feature Analysis

Demonstrates using eule + interval-sets to identify functional genomic regions.
Biological data is naturally interval-based (Chromosome start/end positions).

Scenario:
We want to find "Active Regulatory Regions" on a specific chromosome segment.
An active region is defined as having:
1. An open chromatin structure (ATAC-seq peak)
2. A promoter region (H3K4me3)
3. An enhancer region (H3K27ac)

Finding the exact range where ALL THREE overlap pinpoints the functional regulatory element.
"""

try:
    from interval_sets import Interval, IntervalSet
    from eule import euler
except ImportError:
    print("Requires: pip install interval-sets eule")
    exit(1)

def main():
    print("=" * 60)
    print("🧬 Genomic Feature Analysis: Finding Regulatory Elements")
    print("=" * 60)

    # Simulated Genomic Coordinates (Base Pairs on Chromosome 1)
    # Range of interest: 10,000 - 20,000 bp

    # 1. ATAC-seq peaks (Open Chromatin - accessible DNA)
    atac_peaks = IntervalSet([
        Interval(10500, 11500),  # Peak A
        Interval(14000, 16000),  # Peak B (Large open region)
        Interval(18000, 19000)   # Peak C
    ])

    # 2. H3K4me3 marks (Promoters - start of genes)
    promoters = IntervalSet([
        Interval(11000, 12000),  # Promoter 1
        Interval(14500, 15500)   # Promoter 2
    ])

    # 3. H3K27ac marks (Enhancers - boost expression)
    enhancers = IntervalSet([
        Interval(10000, 13000),  # Super-Enhancer region 1
        Interval(14800, 15200),  # Specific Enhancer 2
        Interval(18500, 19500)   # Enhancer 3
    ])

    genomic_features = {
        'Open_Chromatin': atac_peaks,
        'Promoter': promoters,
        'Enhancer': enhancers
    }

    print("\n📍 Genomic Features (Coordinates in bp):")
    for name, feature in genomic_features.items():
        print(f"  {name:15s}: {feature}")

    # 4. Use Euler to find combinations
    print("\n🔍 Analyzing Feature Overlaps...")
    diagram = euler(genomic_features)

    # 5. Interpret Biology
    print("\n🧬 Functional Annotation Results:")
    
    # Sort by complexity (most overlapping features first)
    for keys, region in sorted(diagram.items(), key=lambda x: -len(x[0])):
        if not region: continue
        
        # Convert tuple keys to set for easy checking
        features = set(keys)
        
        # Define biological logic
        annotation = "Unknown"
        
        if features == {'Open_Chromatin', 'Promoter', 'Enhancer'}:
            annotation = "🔥 ACTIVE PROMOTER (High Confidence)"
        elif features == {'Open_Chromatin', 'Enhancer'} and 'Promoter' not in features:
            annotation = "⚡ DISTAL ENHANCER"
        elif features == {'Open_Chromatin', 'Promoter'}:
            annotation = "💤 POISED PROMOTER (Inactive)"
        elif len(features) == 1:
            annotation = "Background / Noise"
            
        print(f"\n  Feature Set: {list(features)}")
        print(f"  Annotation:  {annotation}")
        print(f"  Coordinates: {region}")
        
        # Calculate total length of this functional class
        total_bp = sum(i.length() for i in region)
        print(f"  Total Size:  {total_bp:.0f} bp")

    print("\n" + "="*60)
    print("✅ Genomic analysis complete.")

if __name__ == "__main__":
    main()
