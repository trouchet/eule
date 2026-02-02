"""
Adapter for integration between eule and interval-sets Box/BoxSet.
Allows multi-dimensional BoxSet objects to be used directly in Euler diagrams.
"""

from typing import TYPE_CHECKING, Any, Iterator, Union

if TYPE_CHECKING:
    try:
        from interval_sets import Box, BoxSet
    except ImportError:
        Box = Any
        BoxSet = Any


class BoxSetAdapter:
    """
    Adapter to make BoxSet compatible with eule's SetLike protocol.
    
    BoxSet naturally implements union, intersection, difference, and bool.
    This wrapper normalizes the interface for eule's consumption.
    """
    
    def __init__(self, box_set: Union['Box', 'BoxSet']):
        """
        Wrap a BoxSet or Box.
        """
        try:
            from interval_sets import Box, BoxSet
            # Normalize to BoxSet
            if isinstance(box_set, Box):
                self._data = BoxSet([box_set])
            elif hasattr(box_set, 'dimension'): # Duck typing for BoxSet
                self._data = box_set
            else:
                 # Fallback, try to treat as iterable of intervals if list?
                 # Actually BoxSet constructor takes iterable.
                 # But let's assume we are passed a Box/BoxSet instance
                 raise TypeError(f"Expected Box or BoxSet, got {type(box_set)}")
                 
        except ImportError:
             self._data = box_set

    def union(self, other: 'BoxSetAdapter') -> 'BoxSetAdapter':
        """Return the union of this set with another."""
        return self._wrap_result(self._data.union(other._data))
    
    def intersection(self, other: 'BoxSetAdapter') -> 'BoxSetAdapter':
        """Return the intersection of this set with another."""
        # Boxset intersection returns BoxSet
        return self._wrap_result(self._data.intersection(other._data))
    
    def difference(self, other: 'BoxSetAdapter') -> 'BoxSetAdapter':
        """Return the difference of this set minus another."""
        return self._wrap_result(self._data.difference(other._data))
    
    def _wrap_result(self, result) -> 'BoxSetAdapter':
        """Helper to wrap result back into adapter"""
        try:
            from interval_sets import Box
            if isinstance(result, Box):
                # Should normally return BoxSet, but handle Box just in case
                from interval_sets import BoxSet
                result = BoxSet([result])
            return BoxSetAdapter(result)
        except ImportError:
            return BoxSetAdapter(result)

    def __bool__(self) -> bool:
        """Return False if the set is empty."""
        return not self._data.is_empty()
    
    def __iter__(self) -> Iterator:
        """
        Iterate over the disjoint boxes in the set.
        Eule iterates over elements of a set.
        For discrete sets, these are items.
        For usage in Eule, we want the 'element' to be something hashable/comparable?
        Wait, eule is Set -> Power Set of disjoint regions.
        If we return Boxes, eule will treat each Box as an element?
        
        CRITICAL: Eule's core logic 'difference(set, element)' expects 
        that elements can be removed from sets.
        But 'BoxSet' is a continuous set. It doesn't have 'elements' in the discrete sense.
        
        However, Eule's 'difference' operation is polymorphic.
        If 'BoxSetAdapter' implements 'diff(BoxSetAdapter)', then eule.core will call:
        sets[key] = difference(sets[key], comb_elems)
        
        So what does __iter__ need to yield?
        In eule logic:
        tuple_keys, celements = _euler_generator(csets)
        
        The generator yields 'celements', which is an intersection of sets.
        For BoxSet usage, 'celements' will be a BoxSetAdapter representing a region.
        
        It doesn't iteration over 'elements' in the standard sense unless 
        we fall back to standard set operations. 
        But eule adapter logic bypasses standard set ops if the object supports the protocol.
        
        However, verify eule/core.py usage of iter.
        It seems eule core doesn't strictly iterate if it uses the SetLike protocol...
        EXCEPT: Eule typically returns a dictionary where values are lists/sets.
        
        If we return a BoxSetAdapter, the final user sees this object.
        They can iterate it (getting Boxes).
        """
        return iter(self._data.boxes)
    
    def __repr__(self) -> str:
        return f"BoxSetAdapter({self._data})"

    def __eq__(self, other) -> bool:
        if isinstance(other, BoxSetAdapter):
            return self._data == other._data
        return self._data == other

def register_box_sets():
    """Register Box/BoxSet with eule's type registry."""
    try:
        from interval_sets import Box, BoxSet
        from ..registry import get_registry
        
        registry = get_registry()
        
        def is_box_type(obj):
            """Check if object is Box or BoxSet."""
            return isinstance(obj, (Box, BoxSet))
        
        def adapt_box_type(obj):
            """Adapt Box/BoxSet."""
            return BoxSetAdapter(obj)
        
        registry.register_detector(is_box_type, adapt_box_type)
        return True
        
    except ImportError:
        return False

# Auto-register
register_box_sets()
