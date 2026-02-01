"""Protocol definitions for extensible set operations.

This module defines the SetLike protocol that any custom type must implement
to work with eule's Euler diagram algorithm.
"""

from typing import Protocol, TypeVar, Iterator, runtime_checkable

__all__ = ['SetLike', 'T']

T = TypeVar('T')


@runtime_checkable
class SetLike(Protocol[T]):
    """
    Minimal protocol for set-like objects in eule.
    
    Any type implementing this protocol can be used with eule's algorithm
    without requiring manual wrapping or adaptation.
    
    Required Methods:
        - union(other): Return A ∪ B
        - intersection(other): Return A ∩ B
        - difference(other): Return A \\ B
        - __bool__(): Return False if empty, True otherwise
        - __iter__(): Iterate over elements
        - from_iterable(iterable): Construct from iterable (class method)
    
    Example:
        >>> class MySet(SetLike[int]):
        ...     def __init__(self, data):
        ...         self._data = set(data)
        ...     
        ...     def union(self, other):
        ...         return MySet(self._data | set(other))
        ...     
        ...     def intersection(self, other):
        ...         return MySet(self._data & set(other))
        ...     
        ...     def difference(self, other):
        ...         return MySet(self._data - set(other))
        ...     
        ...     def __bool__(self):
        ...         return bool(self._data)
        ...     
        ...     def __iter__(self):
        ...         return iter(self._data)
        ...     
        ...     @classmethod
        ...     def from_iterable(cls, iterable):
        ...         return cls(iterable)
        
        >>> from eule import euler
        >>> sets = {'a': MySet([1, 2, 3]), 'b': MySet([2, 3, 4])}
        >>> diagram = euler(sets)  # Works automatically!
    """
    
    def union(self, other: 'SetLike[T]') -> 'SetLike[T]':  # pragma: no cover
        """
        Return the union of this set with another.
        
        Args:
            other: Another SetLike object
            
        Returns:
            A new SetLike object containing all elements from both sets
            
        Example:
            >>> a = MySet([1, 2, 3])
            >>> b = MySet([2, 3, 4])
            >>> a.union(b)
            MySet([1, 2, 3, 4])
        """
        ...  # pragma: no cover
    
    def intersection(self, other: 'SetLike[T]') -> 'SetLike[T]':  # pragma: no cover
        """
        Return the intersection of this set with another.
        
        Args:
            other: Another SetLike object
            
        Returns:
            A new SetLike object containing only elements in both sets
            
        Example:
            >>> a = MySet([1, 2, 3])
            >>> b = MySet([2, 3, 4])
            >>> a.intersection(b)
            MySet([2, 3])
        """
        ...  # pragma: no cover
    
    def difference(self, other: 'SetLike[T]') -> 'SetLike[T]':  # pragma: no cover
        """
        Return the set difference (elements in self but not in other).
        
        Args:
            other: Another SetLike object
            
        Returns:
            A new SetLike object containing elements only in self
            
        Example:
            >>> a = MySet([1, 2, 3])
            >>> b = MySet([2, 3, 4])
            >>> a.difference(b)
            MySet([1])
        """
        ...  # pragma: no cover
    
    def __bool__(self) -> bool:  # pragma: no cover
        """
        Return False if the set is empty, True otherwise.
        
        This is used for emptiness checks in the algorithm.
        
        Returns:
            False if empty, True if has elements
            
        Example:
            >>> bool(MySet([]))
            False
            >>> bool(MySet([1, 2, 3]))
            True
        """
        ...  # pragma: no cover
    
    def __iter__(self) -> Iterator[T]:  # pragma: no cover
        """
        Return an iterator over elements in the set.
        
        Returns:
            An iterator yielding elements
            
        Example:
            >>> list(MySet([1, 2, 3]))
            [1, 2, 3]
        """
        ...  # pragma: no cover
    
    @classmethod
    def from_iterable(cls, iterable) -> 'SetLike[T]':  # pragma: no cover
        """
        Construct a new instance from an iterable.
        
        This is used when the algorithm needs to create new instances
        of your type from a collection of elements.
        
        Args:
            iterable: Any iterable of elements
            
        Returns:
            A new instance of the SetLike type
            
        Example:
            >>> MySet.from_iterable([1, 2, 3])
            MySet([1, 2, 3])
        """
        ...  # pragma: no cover
