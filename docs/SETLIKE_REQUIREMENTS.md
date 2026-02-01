# SetLike Protocol Requirements for Eule

## TL;DR

For a type to work with eule, it must:

1. **Iterate over discrete, comparable elements** (not continuous ranges or complex objects)
2. **Implement set operations**: `union()`, `intersection()`, `difference()`
3. **Support emptiness check**: `__bool__()`
4. **Be iterable**: `__iter__()`
5. **Have a construction method**: `from_iterable()` (class method)

## Why These Requirements?

Eule generates **Euler diagrams** - visual representations showing how discrete elements are partitioned across overlapping sets. The algorithm:

1. **Iterates over elements** to find which sets contain each element
2. **Performs set operations** to compute overlapping regions
3. **Groups elements** by which set combinations they belong to

This requires **discrete, countable elements**, not continuous ranges or complex nested structures.

## What Types Work with Eule?

### ✅ Compatible Types

| Type | Why It Works | Example |
|------|--------------|---------|
| `set` | Native discrete set | `{1, 2, 3, 4}` |
| `list` | Discrete sequence | `[1, 2, 3, 4]` |
| `tuple` | Discrete sequence | `(1, 2, 3, 4)` |
| `frozenset` | Immutable discrete set | `frozenset([1, 2, 3])` |
| Custom discrete collections | Implements SetLike protocol | See below |

**Common Pattern**: Elements are discrete, comparable items (numbers, strings, objects with `__eq__` and `__hash__`).

### ❌ Incompatible Types

| Type | Why It Doesn't Work | Alternative |
|------|---------------------|-------------|
| `IntervalSet` | Iterates over Interval objects, not discrete points | Use interval-sets directly for continuous analysis |
| Continuous ranges | Represent infinite points | Discretize first (see below) |
| Nested structures | Not discrete elements | Flatten or extract elements |
| Generators | Not reusable (consumed after one pass) | Convert to list/set first |

## The SetLike Protocol in Detail

```python
from typing import Protocol, TypeVar, Iterator

T = TypeVar('T')

class SetLike(Protocol[T]):
    """Required methods for eule compatibility."""
    
    def union(self, other: 'SetLike[T]') -> 'SetLike[T]':
        """Return A ∪ B (all elements in either set)."""
        ...
    
    def intersection(self, other: 'SetLike[T]') -> 'SetLike[T]':
        """Return A ∩ B (elements in both sets)."""
        ...
    
    def difference(self, other: 'SetLike[T]') -> 'SetLike[T]':
        """Return A \ B (elements in A but not in B)."""
        ...
    
    def __bool__(self) -> bool:
        """Return False if empty, True otherwise."""
        ...
    
    def __iter__(self) -> Iterator[T]:
        """Yield discrete elements one by one."""
        ...
    
    @classmethod
    def from_iterable(cls, iterable) -> 'SetLike[T]':
        """Construct instance from iterable of elements."""
        ...
```

### Critical Requirements Explained

#### 1. `__iter__()` Must Yield Discrete Elements

**✅ Correct**:
```python
class DiscreteSet:
    def __iter__(self):
        yield 1
        yield 2
        yield 3
# Elements are discrete, comparable items
```

**❌ Wrong**:
```python
class IntervalSet:
    def __iter__(self):
        yield Interval(0, 10)  # Yields complex object, not discrete elements
        yield Interval(20, 30)
# Eule expects elements, not containers
```

#### 2. Set Operations Must Work on Discrete Elements

**✅ Correct**:
```python
a = {1, 2, 3}
b = {2, 3, 4}
a.union(b)  # {1, 2, 3, 4} - discrete elements combined
```

**❌ Wrong** (Continuous semantics):
```python
a = IntervalSet([Interval(0, 5)])
b = IntervalSet([Interval(3, 8)])
a.union(b)  # [0, 8] - continuous merge, lost {1,2} vs {6,7,8} distinction
```

#### 3. Elements Must Be Comparable/Hashable

Eule needs to:
- Group elements by set membership
- Store elements in dictionaries
- Compare elements for equality

```python
# ✅ Works
{1, 2, 3}           # integers are hashable
{'a', 'b', 'c'}     # strings are hashable
{obj1, obj2}        # custom objects with __hash__

# ❌ Fails
{[1, 2], [3, 4]}    # lists are not hashable
```

## Creating Custom SetLike Types

### Example 1: Sparse Set (Memory-Efficient)

```python
from eule.protocols import SetLike
from typing import Iterator

class SparseSet(SetLike[int]):
    """Memory-efficient set using a bitset."""
    
    def __init__(self, elements=None):
        self._bitset = 0
        if elements:
            for elem in elements:
                self._bitset |= (1 << elem)
    
    def union(self, other):
        result = SparseSet()
        result._bitset = self._bitset | other._bitset
        return result
    
    def intersection(self, other):
        result = SparseSet()
        result._bitset = self._bitset & other._bitset
        return result
    
    def difference(self, other):
        result = SparseSet()
        result._bitset = self._bitset & ~other._bitset
        return result
    
    def __bool__(self):
        return self._bitset != 0
    
    def __iter__(self) -> Iterator[int]:
        bit = 0
        bitset = self._bitset
        while bitset:
            if bitset & 1:
                yield bit
            bitset >>= 1
            bit += 1
    
    @classmethod
    def from_iterable(cls, iterable):
        return cls(iterable)

# Usage (works automatically!)
from eule import euler

sets = {
    'a': SparseSet([1, 2, 3]),
    'b': SparseSet([2, 3, 4]),
}
result = euler(sets)  # Just works!
```

### Example 2: Immutable Frozen Set Wrapper

```python
class ImmutableSet(SetLike[T]):
    """Immutable wrapper around frozenset."""
    
    def __init__(self, elements=None):
        self._data = frozenset(elements or [])
    
    def union(self, other):
        return ImmutableSet(self._data | other._data)
    
    def intersection(self, other):
        return ImmutableSet(self._data & other._data)
    
    def difference(self, other):
        return ImmutableSet(self._data - other._data)
    
    def __bool__(self):
        return bool(self._data)
    
    def __iter__(self):
        return iter(self._data)
    
    @classmethod
    def from_iterable(cls, iterable):
        return cls(iterable)

# Auto-registered and works immediately
from eule import euler
result = euler({'a': ImmutableSet([1,2,3]), 'b': ImmutableSet([2,3,4])})
```

## Common Pitfalls

### ❌ Pitfall 1: Yielding Container Objects

```python
# WRONG
class IntervalSet:
    def __iter__(self):
        yield Interval(0, 10)  # Yields objects, not discrete elements

# Eule expects: 1, 2, 3, 4, ... (discrete elements)
# Not: Interval(0, 10) (container object)
```

### ❌ Pitfall 2: Continuous Semantics

```python
# WRONG for Euler diagrams
a = IntervalSet([Interval(0, 5)])
b = IntervalSet([Interval(3, 8)])

a.union(b)  # [0, 8] - loses partition information
# Eule needs: {0,1,2} only in A, {3,4,5} in both, {6,7,8} only in B
```

**Fix**: Discretize first:
```python
def discretize(iset, step=1.0):
    points = set()
    for interval in iset:
        start = int(interval._start)
        end = int(interval._end) + 1
        points.update(range(start, end))
    return points

# Now works with eule
a_discrete = discretize(a)  # {0, 1, 2, 3, 4, 5}
b_discrete = discretize(b)  # {3, 4, 5, 6, 7, 8}
```

### ❌ Pitfall 3: Non-Reusable Iterators

```python
# WRONG
def gen():
    yield 1
    yield 2

result = euler({'a': gen(), 'b': gen()})  # Fails - generators consumed after first use
```

**Fix**: Convert to list/set first:
```python
result = euler({'a': list(gen()), 'b': list(gen())})  # Works
```

## When to Use Eule vs Other Libraries

| Use Case | Library | Why |
|----------|---------|-----|
| Discrete element partitioning | **eule** | Customer segments, categories, discrete items |
| Continuous range analysis | **interval-sets** | Temperatures, measurements, time ranges |
| Interval arithmetic | **pyinterval** | Error propagation, bounds calculation |
| Geometric regions | **Shapely** | 2D/3D spatial analysis |

**Rule of Thumb**: If you can count and list all elements individually → **use eule**. If elements form continuous ranges → **use a different library**.

## Registration and Adaptation

### Automatic Detection

Eule automatically detects and wraps:
- Built-in `set`, `list`, `tuple`
- Any type implementing the SetLike protocol (duck typing)

### Manual Registration

For types that need special handling:

```python
from eule import register_adapter

class MyWeirdSet:
    # Custom implementation...
    pass

def adapt_weird_set(obj):
    # Convert to SetLike
    return SetAdapter(obj.get_elements())

register_adapter(MyWeirdSet, adapt_weird_set)
```

## See Also

- [Protocol Specification](design/PROTOCOL_SPECIFICATION.md) - Full technical details
- [IntervalSet Compatibility](INTERVALSET_COMPATIBILITY.md) - Why IntervalSet doesn't work
- [Extensibility Guide](design/EXTENSIBILITY_README.md) - How to extend eule
- [Adapter Implementation](design/AUTOMATIC_ADAPTATION_DESIGN.md) - Internal architecture

## Summary

**Eule requires discrete, countable elements** because it partitions elements into overlapping regions. Types must:

1. ✅ Iterate over **discrete elements** (not containers or ranges)
2. ✅ Support **set operations** on discrete elements
3. ✅ Be **comparable/hashable**
4. ✅ Implement **SetLike protocol**

If your type meets these requirements, it will work seamlessly with eule. If not, consider whether eule is the right tool for your use case.
