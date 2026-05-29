import itertools
from typing import Dict, List, Tuple, Union, Iterator, Any
from .core import euler_keys

class Spider:
    """
    Represents a 'Spider' in a formal Spider Diagram.
    A spider has a 'habitat' consisting of one or more exclusive zones (legs).
    """
    def __init__(self, legs: Tuple[Tuple[str, ...], ...], universe_regions: List[Tuple[str, ...]]):
        self._legs = legs  # The zones the spider touches
        self._universe = universe_regions
        
    @property
    def legs(self) -> Tuple[Tuple[str, ...], ...]:
        """The zones (Euler regions) the spider touches."""
        return self._legs

    @property
    def cardinality(self) -> int:
        """Number of zones (legs) in the spider's habitat."""
        return len(self._legs)
    
    @property
    def r_set(self) -> List[Tuple[str, ...]]:
        """
        The Complement (R-set). 
        Rationale: E = S + R, where E is the non-empty universe Euler set.
        """
        return [r for r in self._universe if r not in self._legs]

    def description(self) -> str:
        """
        Rationale: Human-readable description of the spider's habitat.
        """
        if self.cardinality == 1:
            return f"Exclusively in {self._legs[0]}"
        
        # Group legs by common set members
        all_sets = set()
        for leg in self._legs:
            all_sets.update(leg)
            
        common_sets = set(self._legs[0])
        for leg in self._legs[1:]:
            common_sets &= set(leg)
        
        if common_sets:
            remaining = all_sets - common_sets
            return f"Ambiguous element of {tuple(sorted(common_sets))}, potentially overlapping with {tuple(sorted(remaining)) if remaining else 'nothing'}"
        
        return f"Ambiguous element across {len(self._legs)} disjoint zones: {self._legs}"

    def __repr__(self):
        return f"Spider(legs={len(self._legs)}, habitat={self._legs})"

def spider_sets(sets: Union[Dict, Any], k: int = None) -> Iterator[Spider]:
    """
    Universal Logic Engine - Spider Space Generator.
    
    Implements the spider-set space {S} where s = 2^m - 1.
    
    :param sets: The input sets or an Euler object.
    :param k: Optional constraint. Returns spiders with exactly k legs.
    :return: An iterator of Spider objects.
    """
    if hasattr(sets, 'euler_keys') and callable(getattr(sets, 'euler_keys')):
        m_regions = sets.euler_keys()
    else:
        m_regions = euler_keys(sets)
        
    m = len(m_regions)

    if k is not None:
        if not (1 <= k <= m):
            return
        for combo in itertools.combinations(m_regions, k):
            yield Spider(combo, m_regions)
    else:
        for r in range(1, m + 1):
            for combo in itertools.combinations(m_regions, r):
                yield Spider(combo, m_regions)

def spider_generator(sets: Union[Dict, Any], k: int = None) -> Iterator[Tuple[Tuple[Tuple[str, ...], ...], List[Tuple[str, ...]]]]:
    """
    Generator that yields (habitat, r_set) tuples for backward compatibility
    and low-level access.
    
    :param sets: The input sets or an Euler object.
    :param k: Optional constraint.
    :yields: (legs, r_set)
    """
    for spider in spider_sets(sets, k=k):
        yield (spider.legs, spider.r_set)
