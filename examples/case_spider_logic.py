from eule import Euler

def run_spider_example():
    print("--- Eule Spider Diagram Example ---")
    
    # Define some overlapping sets
    sets = {
        'A': {1, 2, 3},
        'B': {2, 3, 4},
        'C': {3, 4, 5}
    }
    
    # Initialize Euler object
    eu = Euler(sets)
    
    print(f"Exclusive Regions (m={len(eu.euler_keys())}):")
    for region in eu.euler_keys():
        print(f"  - {region}")
    
    print("\nGenerating Spiders with k=2 legs:")
    # Using the new .spiders() method on the Euler class
    for spider in eu.spiders(k=2):
        print(f"\nSpider Habitat: {spider.legs}")
        print(f"Rationale: {spider.description()}")
        print(f"R-set (Complement): {spider.r_set}")

    # Theoretical maximum cardinality verification
    m = len(eu.euler_keys())
    k_max = (m + 1) // 2
    max_spiders = list(eu.spiders(k=k_max))
    print(f"\nMax variety occurs at k={k_max}. Count: {len(max_spiders)}")

if __name__ == "__main__":
    run_spider_example()
