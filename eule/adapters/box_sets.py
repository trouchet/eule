"""
Adapter for integration between eule and interval-sets Box/BoxSet.
Allows multi-dimensional BoxSet objects to be used directly in Euler diagrams.
"""

from typing import TYPE_CHECKING, Any, Iterator, Union

if TYPE_CHECKING:  # pragma: no cover
    try:  # pragma: no cover
        from interval_sets import Box, BoxSet  # pragma: no cover
    except ImportError:  # pragma: no cover
        Box = Any  # pragma: no cover
        BoxSet = Any  # pragma: no cover


class BoxSetAdapter:
    """
    Adapter to make BoxSet compatible with eule's SetLike protocol.
    
    BoxSet naturally implements union, intersection, difference, and bool.
    This wrapper normalizes the interface for eule's consumption.
    """
    
    def __init__(self, box_set: Union['Box', 'BoxSet', Any]):
        """
        Wrap a BoxSet or Box.
        """
        self._data = box_set
        
        # Try to normalize if possible
        try:
            from interval_sets import Box, BoxSet
            if isinstance(box_set, Box) or type(box_set).__name__ == 'Box':
                self._data = BoxSet([box_set])
        except ImportError:
            pass

    def union(self, other: Union['BoxSetAdapter', 'Box', 'BoxSet']) -> 'BoxSetAdapter':
        """Return the union of this set with another."""
        try:
            from interval_sets import Box, BoxSet
            
            if hasattr(other, '_data'):
                other_data = other._data
            elif isinstance(other, Box):
                other_data = BoxSet([other])
            elif isinstance(other, BoxSet):
                other_data = other
            else:
                other_data = other
                
            return self._wrap_result(self._data.union(other_data))
        except ImportError:
            # Fallback for when library is missing but we're operating on dummy data
            other_data = other._data if hasattr(other, '_data') else other
            return self._wrap_result(self._data.union(other_data))
    
    def intersection(self, other: Union['BoxSetAdapter', 'Box', 'BoxSet']) -> 'BoxSetAdapter':
        """Return the intersection of this set with another."""
        try:
            from interval_sets import Box, BoxSet
            
            if hasattr(other, '_data'):
                other_data = other._data
            elif isinstance(other, Box):
                other_data = BoxSet([other])
            elif isinstance(other, BoxSet):
                other_data = other
            else:
                other_data = other
                
            return self._wrap_result(self._data.intersection(other_data))
        except ImportError:
            other_data = other._data if hasattr(other, '_data') else other
            return self._wrap_result(self._data.intersection(other_data))
    
    def difference(self, other: Union['BoxSetAdapter', 'Box', 'BoxSet']) -> 'BoxSetAdapter':
        """Return the difference of this set minus another."""
        try:
            from interval_sets import Box, BoxSet
            
            if hasattr(other, '_data'):
                other_data = other._data
            elif isinstance(other, Box):
                other_data = BoxSet([other])
            elif isinstance(other, BoxSet):
                other_data = other
            else:
                other_data = other
                
            return self._wrap_result(self._data.difference(other_data))
        except ImportError:
            other_data = other._data if hasattr(other, '_data') else other
            return self._wrap_result(self._data.difference(other_data))
    
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

    def is_empty(self) -> bool:
        """Return True if the set is empty."""
        try:
            return self._data.is_empty()
        except (AttributeError, TypeError):
            return not bool(list(self._data.boxes))

    def __bool__(self) -> bool:
        """Return False if the set is empty."""
        return not self.is_empty()
    
    def __iter__(self) -> Iterator:
        """Iterate over the disjoint boxes in the set."""
        return iter(self._data.boxes)

    def __getattr__(self, name):
        """Proxy missing attributes (e.g., _boxes) to the underlying data."""
        if name.startswith('_') and name != '_data':
             data = self.__dict__.get('_data')
             if data is not None:
                 return getattr(data, name)
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")
    
    def __repr__(self) -> str:
        return f"BoxSetAdapter({self._data})"

    def __eq__(self, other) -> bool:
        if hasattr(other, '_data'):
            return self._data == other._data
        return self._data == other

def register_box_sets():
    """Register Box/BoxSet with eule's type registry."""
    try:
        from interval_sets import Box, BoxSet
        from ..registry import get_registry
        
        registry = get_registry()
        
        def is_box_type(obj):
            """Check if object is Box or BoxSet (robust to reloads)."""
            return (
                isinstance(obj, (Box, BoxSet)) or 
                type(obj).__name__ in ('Box', 'BoxSet') or
                hasattr(obj, 'boxes')
            )
        
        def adapt_box_type(obj):
            """Adapt Box/BoxSet."""
            return BoxSetAdapter(obj)
        
        registry.register_detector(is_box_type, adapt_box_type)
        return True
        
    except ImportError:
        return False

# Auto-register
register_box_sets()
