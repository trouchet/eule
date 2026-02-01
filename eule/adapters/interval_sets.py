"""
Adapter for interval-sets library integration.

This module provides automatic integration between eule and the interval-sets library,
allowing IntervalSet objects to work seamlessly with eule's Euler diagram generation.
"""

from typing import TYPE_CHECKING, Any, Iterator

if TYPE_CHECKING:
    try:
        from interval_sets import IntervalSet as _IntervalSet
    except ImportError:
        _IntervalSet = Any  # type: ignore


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
    
    def __init__(self, interval_set: '_IntervalSet'):
        """
        Wrap an IntervalSet or Interval.
        
        Args:
            interval_set: The IntervalSet or Interval to wrap
        """
        try:
            from interval_sets import Interval, IntervalSet
            # Normalize: always store as IntervalSet for consistency
            if isinstance(interval_set, Interval):
                self._data = IntervalSet([interval_set])
            else:
                self._data = interval_set
        except ImportError:
            self._data = interval_set
    
    def union(self, other: 'IntervalSetAdapter') -> 'IntervalSetAdapter':
        """Return the union of this set with another."""
        try:
            from interval_sets import Interval, IntervalSet
            # Extract the underlying data, normalizing to IntervalSet
            if isinstance(other, IntervalSetAdapter):
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
    
    def intersection(self, other: 'IntervalSetAdapter') -> 'IntervalSetAdapter':
        """Return the intersection of this set with another."""
        try:
            from interval_sets import Interval, IntervalSet
            # Extract the underlying data, normalizing to IntervalSet
            if isinstance(other, IntervalSetAdapter):
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
    
    def difference(self, other: 'IntervalSetAdapter') -> 'IntervalSetAdapter':
        """Return the difference of this set minus another."""
        try:
            from interval_sets import Interval, IntervalSet
            # Extract the underlying data, normalizing to IntervalSet
            if isinstance(other, IntervalSetAdapter):
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
    
    def __bool__(self) -> bool:
        """Return False if the set is empty, True otherwise."""
        return bool(self._data)
    
    def __iter__(self) -> Iterator:
        """Return an iterator over elements in the set."""
        return iter(self._data)
    
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
        if isinstance(other, IntervalSetAdapter):
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
            """Check if object is an IntervalSet or Interval."""
            return isinstance(obj, (IntervalSet, Interval))
        
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
