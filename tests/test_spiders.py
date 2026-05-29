import pytest
import math
from eule import Euler, spider_sets, spider_generator, Spider

def test_spider_initialization():
    """Test Spider object properties."""
    universe = [('A',), ('A', 'B'), ('B',)]
    legs = (('A',), ('A', 'B'))
    spider = Spider(legs, universe)
    
    assert spider.legs == legs
    assert spider.cardinality == 2
    assert spider.r_set == [('B',)]

def test_spider_description_monopod():
    """Test rationale for single zone spiders."""
    universe = [('A',), ('A', 'B'), ('B',)]
    spider = Spider((('A',),), universe)
    assert spider.description() == "Exclusively in ('A',)"

def test_spider_description_multipod_common():
    """Test rationale for spiders with common set membership."""
    universe = [('A',), ('A', 'B'), ('B',)]
    # Habitat: ('A',) and ('A', 'B') -> Common: 'A'
    spider = Spider((('A',), ('A', 'B')), universe)
    assert "Ambiguous element of ('A',)" in spider.description()
    assert "potentially overlapping with ('B',)" in spider.description()

def test_spider_description_disjoint():
    """Test rationale for spiders with no common overlap in habitat."""
    universe = [('A',), ('B',), ('C',)]
    spider = Spider((('A',), ('C',)), universe)
    assert spider.description() == "Ambiguous element across 2 disjoint zones: (('A',), ('C',))"

def test_spider_sets_generator():
    """Test the main spider_sets generator with different k values."""
    sets = {'A': {1, 2}, 'B': {2, 3}}
    # m = 3 regions: ('A',), ('A', 'B'), ('B',)
    
    # Test k=1
    spiders_k1 = list(spider_sets(sets, k=1))
    assert len(spiders_k1) == 3
    
    # Test k=2
    spiders_k2 = list(spider_sets(sets, k=2))
    assert len(spiders_k2) == 3 # 3C2 = 3
    
    # Test full space (2^3 - 1 = 7)
    all_spiders = list(spider_sets(sets))
    assert len(all_spiders) == 7

def test_euler_class_integration():
    """Test the .spiders() method on Euler class."""
    eu = Euler({'A': [1], 'B': [2]})
    # Regions: ('A',), ('B',) -> m=2
    spiders = list(eu.spiders())
    assert len(spiders) == 3 # 2^2 - 1
    assert all(isinstance(s, Spider) for s in spiders)

def test_spider_generator_tuples():
    """Test spider_generator yields tuples correctly."""
    sets = {'A': [1]}
    # m=1 -> 2^1 - 1 = 1 spider
    gen = list(spider_generator(sets))
    assert len(gen) == 1
    habitat, r_set = gen[0]
    assert habitat == (('A',),)
    assert r_set == []

def test_spider_cardinality_peak():
    """Verify nCk peak logic for m=5."""
    # System with 5 disjoint regions
    eu = Euler({str(i): {i} for i in range(5)})
    m = 5
    # Max variety should be at k=3 (5C3=10)
    k3_spiders = list(eu.spiders(k=3))
    assert len(k3_spiders) == 10
    assert len(list(eu.spiders(k=2))) == 10
    assert len(list(eu.spiders(k=1))) == 5

def test_edge_cases():
    """Test invalid k and empty inputs."""
    sets = {'A': [1]}
    
    # k out of range
    assert list(spider_sets(sets, k=0)) == []
    assert list(spider_sets(sets, k=10)) == []
    
    # Empty sets
    empty_eu = Euler({})
    assert list(empty_eu.spiders()) == []

def test_spider_repr():
    """Test string representation."""
    spider = Spider((('A',),), [('A',)])
    assert "Spider(legs=1" in repr(spider)
