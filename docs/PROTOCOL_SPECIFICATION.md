# Eule Protocol Specification

## Overview

This document defines the **minimal protocol requirements** for any data structure to work with eule's Euler diagram algorithm. By satisfying these requirements, eule can be extended to work with custom set-like objects beyond Python's built-in `list`, `tuple`, and `set`.

## Motivation

Currently, eule hardcodes support for `list`, `tuple`, and `set`. However, the algorithm itself only requires a small subset of operations. By defining a **SetLike Protocol**, eule can support:
- Custom interval sets (from `interval-sets` library)
- Sparse sets
- Lazy/generator-based sets
- Immutable frozen structures
- Database-backed sets
- Distributed sets

## Analysis of Current Implementation

### Operations Used by Eule Algorithm

From analyzing `eule/core.py` and `eule/operations.py`, the algorithm requires:

#### 1. **Set Operations** (from `operations.py`)
- `union(A, B)` → A ∪ B
- `intersection(A, B)` → A ∩ B  
- `difference(A, B)` → A \ B

#### 2. **Predicates/Checks**
- Truthiness check: `if set_obj:` (emptiness check)
- Length: `len(set_obj)` (optional, for optimization)

#### 3. **Conversion**
- Convertible to Python `set` (currently via `sequence_to_set()`)
- Preservable type: `type_A = type(sequence_A)` → `type_A(result)`

#### 4. **Iteration** (implicit)
- Iterable: `for elem in set_obj:`
- Set construction from iterable: `set(iterable)`

### Current Type System

```python
# From eule/types.py
KeyType = str | Tuple
SetType = List | Set
SetsType = List[SetType] | Dict[KeyType, SetType]
SequenceType = List | Tuple | Set
```

## Proposed Protocol

### Core Protocol: `SetLike`

```python
from typing import Protocol, TypeVar, Iterator, runtime_checkable

T = TypeVar('T')

@runtime_checkable
class SetLike(Protocol[T]):
    """
    Minimal protocol for objects to work with eule's Euler diagram algorithm.
    
    Any type implementing this protocol can be used as a set in eule operations.
    """
    
    # Core Set Operations
    def union(self, other: 'SetLike[T]') -> 'SetLike[T]':
        """Return the union of this set with another."""
        ...
    
    def intersection(self, other: 'SetLike[T]') -> 'SetLike[T]':
        """Return the intersection of this set with another."""
        ...
    
    def difference(self, other: 'SetLike[T]') -> 'SetLike[T]':
        """Return the set difference (elements in self but not in other)."""
        ...
    
    # Predicates
    def __bool__(self) -> bool:
        """Return False if set is empty, True otherwise."""
        ...
    
    # Conversion & Construction
    def __iter__(self) -> Iterator[T]:
        """Return an iterator over elements."""
        ...
    
    @classmethod
    def from_iterable(cls, iterable) -> 'SetLike[T]':
        """
        Construct a new instance from an iterable.
        Alternative: Make constructor accept iterables.
        """
        ...
```

### Optional Protocol Extensions

```python
@runtime_checkable
class CountableSetLike(SetLike[T], Protocol):
    """Extended protocol with size information for optimizations."""
    
    def __len__(self) -> int:
        """Return the number of elements in the set."""
        ...


@runtime_checkable  
class HashableSetLike(SetLike[T], Protocol):
    """Extended protocol for sets that can be used as dict keys."""
    
    def __hash__(self) -> int:
        """Return hash value for immutable sets."""
        ...
    
    def __eq__(self, other) -> bool:
        """Check equality with another set."""
        ...
```

## Implementation Strategy

### Phase 1: Define Protocols

Create `eule/protocols.py`:

```python
"""Protocol definitions for extensible set operations."""

from typing import Protocol, TypeVar, Iterator, Union, runtime_checkable
from abc import abstractmethod

T = TypeVar('T')

@runtime_checkable
class SetLike(Protocol[T]):
    """Minimal protocol for set-like objects in eule."""
    
    @abstractmethod
    def union(self, other: 'SetLike[T]') -> 'SetLike[T]':
        """A ∪ B"""
        ...
    
    @abstractmethod
    def intersection(self, other: 'SetLike[T]') -> 'SetLike[T]':
        """A ∩ B"""
        ...
    
    @abstractmethod
    def difference(self, other: 'SetLike[T]') -> 'SetLike[T]':
        """A \ B"""
        ...
    
    @abstractmethod
    def __bool__(self) -> bool:
        """Emptiness check"""
        ...
    
    @abstractmethod
    def __iter__(self) -> Iterator[T]:
        """Iteration support"""
        ...
    
    @classmethod
    @abstractmethod
    def from_iterable(cls, iterable) -> 'SetLike[T]':
        """Construction from iterable"""
        ...
```

### Phase 2: Refactor Operations Module

Modify `eule/operations.py` to use protocols:

```python
from typing import TypeVar
from .protocols import SetLike

T = TypeVar('T', bound=SetLike)

def union(set_a: T, set_b: T) -> T:
    """Generic union operation for any SetLike object."""
    return set_a.union(set_b)

def difference(set_a: T, set_b: T) -> T:
    """Generic difference operation for any SetLike object."""
    return set_a.difference(set_b)

def intersection(set_a: T, set_b: T) -> T:
    """Generic intersection operation for any SetLike object."""
    return set_a.intersection(set_b)
```

### Phase 3: Adapter Pattern for Built-in Types

Create `eule/adapters.py` to wrap built-in types:

```python
"""Adapters to make built-in types conform to SetLike protocol."""

from typing import TypeVar, Iterator, Iterable, Set as PySet, List, Tuple
from .protocols import SetLike

T = TypeVar('T')

class SetAdapter(SetLike[T]):
    """Adapter for Python's built-in set."""
    
    def __init__(self, elements: Iterable[T] = None):
        self._data: PySet[T] = set(elements) if elements else set()
    
    def union(self, other: SetLike[T]) -> 'SetAdapter[T]':
        if isinstance(other, SetAdapter):
            return SetAdapter(self._data | other._data)
        return SetAdapter(self._data | set(other))
    
    def intersection(self, other: SetLike[T]) -> 'SetAdapter[T]':
        if isinstance(other, SetAdapter):
            return SetAdapter(self._data & other._data)
        return SetAdapter(self._data & set(other))
    
    def difference(self, other: SetLike[T]) -> 'SetAdapter[T]':
        if isinstance(other, SetAdapter):
            return SetAdapter(self._data - other._data)
        return SetAdapter(self._data - set(other))
    
    def __bool__(self) -> bool:
        return bool(self._data)
    
    def __iter__(self) -> Iterator[T]:
        return iter(self._data)
    
    @classmethod
    def from_iterable(cls, iterable: Iterable[T]) -> 'SetAdapter[T]':
        return cls(iterable)
    
    def to_native(self) -> PySet[T]:
        """Convert back to native Python set."""
        return self._data.copy()


class ListAdapter(SetLike[T]):
    """Adapter for list-like sequences (removes duplicates)."""
    
    def __init__(self, elements: Iterable[T] = None):
        # Preserve order while removing duplicates
        if elements:
            seen = set()
            self._data: List[T] = []
            for elem in elements:
                if elem not in seen:
                    seen.add(elem)
                    self._data.append(elem)
        else:
            self._data = []
    
    def union(self, other: SetLike[T]) -> 'ListAdapter[T]':
        combined = list(self._data) + list(other)
        return ListAdapter(combined)  # Deduplicates
    
    def intersection(self, other: SetLike[T]) -> 'ListAdapter[T]':
        other_set = set(other)
        return ListAdapter(elem for elem in self._data if elem in other_set)
    
    def difference(self, other: SetLike[T]) -> 'ListAdapter[T]':
        other_set = set(other)
        return ListAdapter(elem for elem in self._data if elem not in other_set)
    
    def __bool__(self) -> bool:
        return bool(self._data)
    
    def __iter__(self) -> Iterator[T]:
        return iter(self._data)
    
    @classmethod
    def from_iterable(cls, iterable: Iterable[T]) -> 'ListAdapter[T]':
        return cls(iterable)
    
    def to_native(self) -> List[T]:
        """Convert back to native Python list."""
        return self._data.copy()
```

### Phase 4: Update Type System

Modify `eule/types.py`:

```python
from typing import Dict, List, Set, Tuple, Union
from .protocols import SetLike

KeyType = str | Tuple
# Now accepts any SetLike object
SetType = SetLike | List | Set  
SetsType = List[SetType] | Dict[KeyType, SetType]
```

### Phase 5: Factory Function

Create `eule/factory.py` for automatic adapter selection:

```python
"""Factory functions for creating SetLike objects."""

from typing import Any, TypeVar
from .protocols import SetLike
from .adapters import SetAdapter, ListAdapter

T = TypeVar('T')

def make_setlike(obj: Any) -> SetLike:
    """
    Convert an object to SetLike protocol.
    
    - If already SetLike: return as-is
    - If set: wrap in SetAdapter
    - If list/tuple: wrap in ListAdapter
    - Otherwise: try to iterate and wrap in SetAdapter
    """
    if isinstance(obj, SetLike):
        return obj
    
    if isinstance(obj, set):
        return SetAdapter(obj)
    
    if isinstance(obj, (list, tuple)):
        return ListAdapter(obj)
    
    # Try to treat as iterable
    try:
        return SetAdapter(iter(obj))
    except TypeError:
        raise TypeError(f"Cannot convert {type(obj)} to SetLike")
```

## Integration with interval-sets

Example adapter for `IntervalSet` from the `interval-sets` library:

```python
"""Adapter for interval-sets library."""

from typing import Iterator, TypeVar
from interval_sets import IntervalSet, Interval
from eule.protocols import SetLike

T = TypeVar('T')

class IntervalSetAdapter(SetLike[Interval]):
    """Adapter to use IntervalSet with eule."""
    
    def __init__(self, intervals: IntervalSet = None):
        self._intervals = intervals if intervals else IntervalSet([])
    
    def union(self, other: 'IntervalSetAdapter') -> 'IntervalSetAdapter':
        result = self._intervals | other._intervals
        return IntervalSetAdapter(result)
    
    def intersection(self, other: 'IntervalSetAdapter') -> 'IntervalSetAdapter':
        result = self._intervals & other._intervals
        return IntervalSetAdapter(result)
    
    def difference(self, other: 'IntervalSetAdapter') -> 'IntervalSetAdapter':
        result = self._intervals - other._intervals
        return IntervalSetAdapter(result)
    
    def __bool__(self) -> bool:
        return not self._intervals.is_empty()
    
    def __iter__(self) -> Iterator[Interval]:
        # Iterate over component intervals
        return iter(self._intervals.intervals)
    
    @classmethod
    def from_iterable(cls, iterable) -> 'IntervalSetAdapter':
        intervals = list(iterable)
        return cls(IntervalSet(intervals))
    
    @property
    def measure(self) -> float:
        """Total measure (length) of all intervals."""
        return self._intervals.measure()
```

## Usage Examples

### Example 1: Using Built-in Types (Current Behavior)

```python
from eule import euler

sets = {
    'a': [1, 2, 3],
    'b': [2, 3, 4],
    'c': [3, 4, 5]
}

diagram = euler(sets)
# {('a',): [1], ('b', 'c'): [4], ('a', 'b', 'c'): [3], ('c',): [5], ('b',): [2]}
```

### Example 2: Using interval-sets

```python
from eule import euler
from interval_sets import Interval, IntervalSet
from eule.adapters.interval_adapter import IntervalSetAdapter

# Temperature ranges
sets = {
    'cold': IntervalSetAdapter(IntervalSet([Interval(0, 15)])),
    'moderate': IntervalSetAdapter(IntervalSet([Interval(10, 25)])),
    'hot': IntervalSetAdapter(IntervalSet([Interval(20, 40)]))
}

diagram = euler(sets)
# Returns Euler diagram with disjoint interval regions:
# {
#   ('cold',): IntervalSet([Interval(0, 10)]),
#   ('cold', 'moderate'): IntervalSet([Interval(10, 15)]),
#   ('moderate',): IntervalSet([Interval(15, 20)]),
#   ('moderate', 'hot'): IntervalSet([Interval(20, 25)]),
#   ('hot',): IntervalSet([Interval(25, 40)])
# }
```

### Example 3: Custom Sparse Set Implementation

```python
from eule import euler
from eule.protocols import SetLike

class SparseSet(SetLike[int]):
    """Memory-efficient set for sparse integer ranges."""
    
    def __init__(self, ranges: list[tuple[int, int]] = None):
        self.ranges = ranges or []  # List of (start, end) tuples
    
    def union(self, other):
        # Implement range merging logic
        ...
    
    def intersection(self, other):
        # Implement range intersection logic
        ...
    
    def difference(self, other):
        # Implement range subtraction logic
        ...
    
    def __bool__(self):
        return bool(self.ranges)
    
    def __iter__(self):
        for start, end in self.ranges:
            yield from range(start, end + 1)
    
    @classmethod
    def from_iterable(cls, iterable):
        # Convert iterable to range representation
        ...

# Use with eule
sets = {
    'group_a': SparseSet([(1, 1000), (10000, 11000)]),
    'group_b': SparseSet([(500, 1500), (10500, 11500)]),
}

diagram = euler(sets)
```

## Migration Path

### Backward Compatibility

To maintain backward compatibility, eule should:

1. **Continue supporting built-in types** directly
2. **Auto-wrap** built-in types when needed
3. **Detect** if object already implements protocol

```python
# In eule/operations.py
def union(sequence_a, sequence_b):
    """Union operation with automatic type detection."""
    # Try protocol first
    if hasattr(sequence_a, 'union') and callable(sequence_a.union):
        return sequence_a.union(sequence_b)
    
    # Fall back to current implementation
    set_a, set_b = setify_sequences([sequence_a, sequence_b])
    union_set = set_a.union(set_b)
    return type(sequence_a)(union_set)
```

### Testing Strategy

1. **Protocol Compliance Tests**: Verify all adapters satisfy protocol
2. **Regression Tests**: Ensure existing functionality unchanged
3. **Integration Tests**: Test with interval-sets and custom types
4. **Performance Tests**: Measure overhead of protocol dispatch

## Benefits

1. **Extensibility**: Support any set-like structure (intervals, ranges, database sets)
2. **Type Safety**: Protocols provide compile-time checking with mypy
3. **Performance**: Custom types can optimize operations (e.g., interval merging)
4. **Composability**: Mix different set types in same diagram
5. **Interoperability**: Easy integration with other libraries

## Open Questions

1. **Should we support heterogeneous sets?** (mixing intervals with discrete elements)
2. **How to handle infinite sets?** (e.g., `Interval(-∞, ∞)`)
3. **Should protocols be runtime-checkable?** (performance vs flexibility)
4. **What about symmetric_difference and other operations?** (XOR, etc.)

## References

- PEP 544: Protocols (Structural Subtyping)
- Python `typing.Protocol` documentation
- `collections.abc` abstract base classes
- `interval-sets` library implementation

## Next Steps

1. ✅ Define core `SetLike` protocol
2. ⬜ Implement adapters for built-in types
3. ⬜ Refactor operations module to use protocols
4. ⬜ Create comprehensive test suite
5. ⬜ Update documentation and examples
6. ⬜ Implement interval-sets adapter as proof-of-concept
7. ⬜ Benchmark performance impact
8. ⬜ Release as minor version (backward compatible)
