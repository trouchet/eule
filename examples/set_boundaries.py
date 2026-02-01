"""
Example demonstrating how to calculate set boundaries and visualize adjacency.
Boundaries help identify which sets are 'neighbors' in the Euler diagram topology.
"""
from eule import euler_boundaries

def main():
    # Define sets with some overlaps and some disjoints
    sets = {
        'A': {1, 2, 3, 4},       # Overlaps with B
        'B': {3, 4, 5, 6},       # Overlaps with A and C
        'C': {5, 6, 7, 8},       # Overlaps with B
        'D': {9, 10},            # Disjoint
        'E': {1, 2, 9, 10}       # Overlaps with A and D
    }

    print("--- Input Sets ---")
    for k, v in sets.items():
        print(f"  {k}: {v}")

    # Calculate boundaries
    # Returns a dictionary mapping each set to its neighbors in the Euler diagram
    # Two sets are boundaries if they share a margin in the visual diagram
    boundaries = euler_boundaries(sets)

    print("\n--- Calculated Boundaries ---")
    print("Which sets share a boundary in the Euler diagram representation?")
    for key, neighbors in boundaries.items():
        if neighbors:
            print(f"  Set '{key}' shares boundary with: {neighbors}")
        else:
            print(f"  Set '{key}' has no boundaries (might be isolated or fully contained)")

if __name__ == "__main__":
    main()
