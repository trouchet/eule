"""
Basic usage of Eule library demonstrating Euler diagram generation and set operations.
"""
from eule import euler, euler_keys, euler_boundaries

def main():
    # 1. Define your sets
    # Sets can be lists, tuples, or sets of discrete elements
    sets = {
        'fruits': {'apple', 'banana', 'orange', 'pear'},
        'red_items': {'apple', 'cherry', 'strawberry', 'blood_orange'},
        'sour_items': {'lemon', 'lime', 'blood_orange', 'cherry'}
    }

    print("--- Original Sets ---")
    for name, items in sets.items():
        print(f"{name}: {items}")
    print("\n")

    # 2. Generate Euler Diagram
    # keys represented as tuples indicating the intersection
    diagram = euler(sets)

    print("--- Euler Diagram (Non-overlapping regions) ---")
    for key, elements in diagram.items():
        # key is a tuple of set names that strictly contain these elements
        print(f"Region {key}: {elements}")
    
    # Example interpretation:
    # ('fruits', 'red_items') -> items that are strictly in fruits AND red_items (and NOT in sour_items)

    print("\n")

    # 3. Get existing Euler keys (valid intersections)
    keys = euler_keys(sets)
    print("--- Euler Keys ---")
    print(keys)
    print("\n")

    # 4. Calculate Boundaries
    # Shows which sets are 'neighbors' in the diagram
    boundaries = euler_boundaries(sets)
    print("--- Boundaries (Neighbors) ---")
    for key, neighbors in boundaries.items():
        print(f"{key} neighbors: {neighbors}")

if __name__ == "__main__":
    main()
