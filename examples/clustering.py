"""
Advanced usage of Eule demonstrating built-in clustering capabilities for large numbers of sets.
This utilizes the internal graph-based clustering (Leiden algorithm implementation) to handle complex set relationships.
"""
import random
try:
    import numpy as np
except ImportError:
    print("This example requires numpy. Please install it: pip install numpy")
    exit(1)

from eule import Euler

def generate_random_sets(n_sets=40, universe_size=100):
    """Generates random sets for demonstration."""
    sets = {}
    universe = list(range(universe_size))
    for i in range(n_sets):
        # Create random overlapping sets
        sample_size = random.randint(5, 20)
        # Use simple names
        sets[f'S{i}'] = random.sample(universe, sample_size)
    return sets

def main():
    print("1. Generating 50 random sets...")
    sets = generate_random_sets(n_sets=50, universe_size=200)
    
    print(f"   Created {len(sets)} sets with random overlaps.")
    
    # Initialize Euler with clustering
    # method can be 'leiden' (default), 'hierarchical', or 'spectral'
    print("\n2. Computing Euler diagram with Leiden clustering...")
    try:
        e = Euler(sets, use_clustering=True, method='leiden', resolution=1.0)
    except Exception as err:
        print(f"Error during clustering: {err}")
        return
    
    print("\n" + "="*40)
    print(" Clustered Euler Diagram Summary")
    print("="*40)
    
    # The summary method provides a concise overview of clusters and regions
    print(e.summary())
    
    print("\n" + "="*40)
    print(" Detailed Clustering Analysis")
    print("="*40)
    
    # We can inspect the clustering details manually
    info = e.get_clustering_info()
    if info:
        print(f"Method Used: {info.get('method')}")
        print(f"Total Clusters: {info.get('n_clusters')}")
        
        # Check for bridge sets (connecting multiple clusters)
        bridges = e.get_bridge_sets()
        if bridges:
            print(f"\nFound {len(bridges)} bridge sets (connecting disparate clusters):")
            # Show first 5 bridges
            for key, connected_clusters in list(bridges.items())[:5]:
                print(f"  Set '{key}' connects clusters {connected_clusters}")
            if len(bridges) > 5:
                print("  ...")

    # Accessing specific cluster diagrams
    # The Euler object manages sub-diagrams for each cluster
    if e.cluster_diagrams:
        print(f"\nGenerated {len(e.cluster_diagrams)} sub-diagrams.")
        first_cluster_id = list(e.cluster_diagrams.keys())[0]
        first_c_regions = e.cluster_diagrams[first_cluster_id]
        print(f"Cluster {first_cluster_id} has {len(first_c_regions)} regions.")

if __name__ == "__main__":
    main()
