"""
Adapter for interval-sets library integration.

This module provides automatic integration between eule and the interval-sets library,
allowing IntervalSet objects to work seamlessly with eule's Euler diagram generation.
"""

from typing import TYPE_CHECKING, Any, Iterator

if TYPE_CHECKING:  # pragma: no cover
    try:  # pragma: no cover
        from interval_sets import IntervalSet as _IntervalSet  # pragma: no cover
    except ImportError:  # pragma: no cover
        _IntervalSet = Any  # type: ignore  # pragma: no cover


class IntervalSetAdapter:
    """
    Adapter to make IntervalSet compatible with eule's SetLike protocol.
    
    IntervalSet already implements most of the protocol naturally:
    - union(), intersection(), difference() ✅
    - __bool__(), __iter__() ✅
    
    This adapter just adds from_iterable() for compatibility.
    
    Examples:
        >>> from interval_sets import Interval, IntervalSet
        >>> from eule import euler
        >>> 
        >>> # Works automatically - no wrapping needed!
        >>> temps = {
        ...     'cold': IntervalSet([Interval(0, 15)]),
        ...     'moderate': IntervalSet([Interval(10, 25)]),
        ...     'hot': IntervalSet([Interval(20, 40)])
        ... }
        >>> diagram = euler(temps)
    """
    
    def __init__(self, interval_set: Any):
        """
        Wrap an IntervalSet or Interval.
        """
        self._data = interval_set
        
        # Try to normalize if possible
        try:
            from interval_sets import Interval, IntervalSet
            if isinstance(interval_set, Interval) or type(interval_set).__name__ == 'Interval':
                self._data = IntervalSet([interval_set])
        except ImportError:
            pass
    
    def union(self, other: Any) -> 'IntervalSetAdapter':
        """Return the union of this set with another."""
        try:
            from interval_sets import Interval, IntervalSet
            
            # Use hasattr check to handle reloaded adapter classes
            if hasattr(other, '_data'):
                other_data = other._data
            elif isinstance(other, Interval):
                other_data = IntervalSet([other])
            elif isinstance(other, IntervalSet):
                other_data = other
            else:
                other_data = other
                
            result = self._data.union(other_data)
            # Normalize result to IntervalSet
            if isinstance(result, Interval):
                result = IntervalSet([result])
            return IntervalSetAdapter(result)
        except ImportError:
            raise ImportError("interval-sets library required")
    
    def intersection(self, other: Any) -> 'IntervalSetAdapter':
        """Return the intersection of this set with another."""
        try:
            from interval_sets import Interval, IntervalSet
            
            if hasattr(other, '_data'):
                other_data = other._data
            elif isinstance(other, Interval):
                other_data = IntervalSet([other])
            elif isinstance(other, IntervalSet):
                other_data = other
            else:
                other_data = other
                
            result = self._data.intersection(other_data)
            # Normalize result to IntervalSet
            if isinstance(result, Interval):
                result = IntervalSet([result])
            return IntervalSetAdapter(result)
        except ImportError:
            raise ImportError("interval-sets library required")
    
    def difference(self, other: Any) -> 'IntervalSetAdapter':
        """Return the difference of this set minus another."""
        try:
            from interval_sets import Interval, IntervalSet
            
            if hasattr(other, '_data'):
                other_data = other._data
            elif isinstance(other, Interval):
                other_data = IntervalSet([other])
            elif isinstance(other, IntervalSet):
                other_data = other
            else:
                other_data = other
                
            result = self._data.difference(other_data)
            # Normalize result to IntervalSet
            if isinstance(result, Interval):
                result = IntervalSet([result])
            return IntervalSetAdapter(result)
        except ImportError:
            raise ImportError("interval-sets library required")
    
    def is_empty(self) -> bool:
        """Return True if the set is empty."""
        return not bool(self._data)

    def __bool__(self) -> bool:
        """Return False if the set is empty, True otherwise."""
        return not self.is_empty()
    
    def __iter__(self) -> Iterator:
        """Return an iterator over elements in the set."""
        return iter(self._data)

    def __getattr__(self, name):
        """Proxy missing attributes (e.g., _intervals, _intervals_count) to underlying data."""
        if name.startswith('_') and name != '_data':
             # Use __dict__ to avoid infinite recursion
             data = self.__dict__.get('_data')
             if data is not None:
                 return getattr(data, name)
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")
    
    @classmethod
    def from_iterable(cls, iterable) -> 'IntervalSetAdapter':
        """
        Construct a new IntervalSet from an iterable.
        
        Args:
            iterable: An iterable of Interval objects
            
        Returns:
            A new IntervalSetAdapter wrapping the created IntervalSet
        """
        try:
            from interval_sets import IntervalSet
        except ImportError:
            raise ImportError(
                "interval-sets library not found. Install it with: pip install interval-sets"
            )
        
        return cls(IntervalSet(iterable))
    
    def to_native(self) -> '_IntervalSet':
        """
        Return the underlying IntervalSet.
        
        Returns:
            The wrapped IntervalSet object
        """
        return self._data
    
    def __repr__(self) -> str:
        return f"IntervalSetAdapter({self._data!r})"
    
    def __eq__(self, other) -> bool:
        if hasattr(other, '_data'):
            return self._data == other._data
        return self._data == other


def register_interval_sets():
    """
    Register IntervalSet and Interval with eule's type registry.
    
    This function is called automatically when the adapter module is imported,
    but can also be called manually if needed.
    
    Note: IntervalSet operations often return Interval objects instead of
    IntervalSet, so we need to handle both types.
    
    Returns:
        bool: True if registration succeeded, False if interval-sets not available
    """
    try:
        from interval_sets import Interval, IntervalSet
        from ..registry import get_registry
        
        registry = get_registry()
        
        # Register both IntervalSet and Interval
        # Both need to be wrapped because:
        # 1. They lack from_iterable() class method
        # 2. Operations return Interval, not IntervalSet (normalization needed)
        
        def is_interval_or_intervalset(obj):
            """Check if object is an IntervalSet or Interval (robust to reloads)."""
            return (
                isinstance(obj, (IntervalSet, Interval)) or 
                type(obj).__name__ in ('Interval', 'IntervalSet') or
                hasattr(obj, 'intervals')
            )
        
        def adapt_interval_types(obj):
            """Adapt IntervalSet or Interval by wrapping with adapter."""
            return IntervalSetAdapter(obj)
        
        registry.register_detector(is_interval_or_intervalset, adapt_interval_types)
        
        return True
        
    except ImportError:
        # interval-sets not installed - that's okay
        return False


# Auto-register on import
register_interval_sets()
