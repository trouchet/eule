"""Adapters to make built-in types conform to SetLike protocol."""

from typing import TypeVar, Iterator, Iterable, Set as PySet, List as PyList
from ..protocols import SetLike

__all__ = ['SetAdapter', 'ListAdapter']

T = TypeVar('T')


class SetAdapter(SetLike[T]):
    """
    Adapter for Python's built-in set.
    
    Wraps a Python set to provide the SetLike protocol interface.
    
    Example:
        >>> adapter = SetAdapter([1, 2, 3])
        >>> adapter.union(SetAdapter([3, 4, 5]))
        SetAdapter({1, 2, 3, 4, 5})
    """
    
    def __init__(self, elements: Iterable[T] = None):
        """
        Create a SetAdapter.
        
        Args:
            elements: Iterable of elements to include in the set
        """
        self._data: PySet[T] = set(elements) if elements is not None else set()
    
    def union(self, other: SetLike[T]) -> 'SetAdapter[T]':
        """Return the union of this set with another."""
        if isinstance(other, SetAdapter):
            return SetAdapter(self._data | other._data)
        return SetAdapter(self._data | set(other))
    
    def intersection(self, other: SetLike[T]) -> 'SetAdapter[T]':
        """Return the intersection of this set with another."""
        if isinstance(other, SetAdapter):
            return SetAdapter(self._data & other._data)
        return SetAdapter(self._data & set(other))
    
    def difference(self, other: SetLike[T]) -> 'SetAdapter[T]':
        """Return the set difference."""
        if isinstance(other, SetAdapter):
            return SetAdapter(self._data - other._data)
        return SetAdapter(self._data - set(other))
    
    def __bool__(self) -> bool:
        """Return False if empty, True otherwise."""
        return bool(self._data)
    
    def __iter__(self) -> Iterator[T]:
        """Iterate over elements."""
        return iter(self._data)
    
    def __len__(self) -> int:
        """Return the number of elements."""
        return len(self._data)
    
    def __repr__(self) -> str:
        """Return string representation."""
        return f"SetAdapter({self._data!r})"
    
    def __eq__(self, other) -> bool:
        """Check equality."""
        if isinstance(other, SetAdapter):
            return self._data == other._data
        return False
    
    @classmethod
    def from_iterable(cls, iterable: Iterable[T]) -> 'SetAdapter[T]':
        """Construct from iterable."""
        return cls(iterable)
    
    def to_native(self) -> PySet[T]:
        """Convert back to native Python set."""
        return self._data.copy()


class ListAdapter(SetLike[T]):
    """
    Adapter for list-like sequences.
    
    Preserves order while removing duplicates for set operations.
    
    Example:
        >>> adapter = ListAdapter([1, 2, 3, 2])
        >>> list(adapter)
        [1, 2, 3]
    """
    
    def __init__(self, elements: Iterable[T] = None):
        """
        Create a ListAdapter.
        
        Args:
            elements: Iterable of elements (duplicates will be removed)
        """
        # Preserve order while removing duplicates
        if elements is not None:
            seen = set()
            self._data: PyList[T] = []
            for elem in elements:
                if elem not in seen:
                    seen.add(elem)
                    self._data.append(elem)
        else:
            self._data = []
    
    def union(self, other: SetLike[T]) -> 'ListAdapter[T]':
        """Return the union (preserves order, removes duplicates)."""
        combined = list(self._data) + list(other)
        return ListAdapter(combined)  # Constructor deduplicates
    
    def intersection(self, other: SetLike[T]) -> 'ListAdapter[T]':
        """Return the intersection (preserves order from self)."""
        other_set = set(other)
        return ListAdapter(elem for elem in self._data if elem in other_set)
    
    def difference(self, other: SetLike[T]) -> 'ListAdapter[T]':
        """Return the set difference (preserves order from self)."""
        other_set = set(other)
        return ListAdapter(elem for elem in self._data if elem not in other_set)
    
    def __bool__(self) -> bool:
        """Return False if empty, True otherwise."""
        return bool(self._data)
    
    def __iter__(self) -> Iterator[T]:
        """Iterate over elements."""
        return iter(self._data)
    
    def __len__(self) -> int:
        """Return the number of elements."""
        return len(self._data)
    
    def __repr__(self) -> str:
        """Return string representation."""
        return f"ListAdapter({self._data!r})"
    
    def __eq__(self, other) -> bool:
        """Check equality."""
        if isinstance(other, ListAdapter):
            return self._data == other._data
        return False
    
    @classmethod
    def from_iterable(cls, iterable: Iterable[T]) -> 'ListAdapter[T]':
        """Construct from iterable."""
        return cls(iterable)
    
    def to_native(self) -> PyList[T]:
        """Convert back to native Python list."""
        return self._data.copy()
