# IntervalSet Compatibility Analysis with Eule

## Executive Summary

**IntervalSet** from the `interval-sets` library **cannot fully satisfy** Eule's `SetLike` protocol due to fundamental design differences. While IntervalSet provides all required operations (union, intersection, difference), it has **incompatible return type semantics** that violate the protocol's type consistency requirements.

## Current Status

✅ **Partial adapter exists**: `eule/adapters/interval_sets.py`  
⚠️ **Coverage**: 30% (39 of 59 lines uncovered)  
❌ **Full compatibility**: Not achievable without wrapper

---

## Critical Limitations

### 1. **Inconsistent Return Types** ❌ BLOCKING

**Problem**: IntervalSet operations return different types depending on the result:

```python
from interval_sets import Interval, IntervalSet

# Case 1: Continuous result → Returns Interval
a = IntervalSet([Interval(0, 5)])
b = IntervalSet([Interval(3, 8)])
result = a.union(b)
# Returns: Interval([0.0, 8.0])  ← Single Interval object

# Case 2: Disjoint result → Returns IntervalSet
c = IntervalSet([Interval(0, 5)])
d = IntervalSet([Interval(10, 15)])
result = c.union(d)
# Returns: IntervalSet({[0.0, 5.0], [10.0, 15.0]})  ← IntervalSet object
```

**Why this breaks Eule**:
- Eule's `SetLike` protocol expects `union(other: SetLike[T]) -> SetLike[T]`
- Type must remain consistent across operations
- Operations must be chainable: `a.union(b).union(c).intersection(d)`
- With IntervalSet, chaining breaks because returned type changes unpredictably

**Root cause**: Mathematical correctness vs. type safety
- IntervalSet optimizes for mathematical semantics
- Returns the most specific type for each result
- This is correct mathematically but incompatible with type protocols

---

### 2. **Missing `from_iterable()` Classmethod** ❌ BLOCKING

**Problem**: IntervalSet lacks the `from_iterable()` classmethod required by the protocol.

```python
# SetLike protocol requires:
class SetLike(Protocol[T]):
    @classmethod
    def from_iterable(cls, iterable) -> 'SetLike[T]':
        ...

# IntervalSet has:
class IntervalSet:
    def __init__(self, elements: Optional[Iterable[...]] = None):
        ...
    # ❌ No from_iterable() classmethod
```

**Why Eule needs this**:
- Used to construct new instances from algorithm results
- Must be a classmethod for proper subclass support
- Cannot use `__init__()` directly in generic protocol code

**Workaround**: Can be added via adapter or monkey-patching:
```python
@classmethod
def from_iterable(cls, iterable):
    return cls(iterable)
```

---

### 3. **Iterator Semantics Mismatch** ⚠️ DESIGN DIFFERENCE

**Problem**: IntervalSet iteration yields `Interval` objects, not individual elements.

```python
s = IntervalSet([Interval(0, 5), Interval(10, 15)])

# Iterating over IntervalSet yields Intervals:
for item in s:
    print(item)
# Output:
#   [0.0, 5.0]     ← Interval object
#   [10.0, 15.0]   ← Interval object

# Iterating over regular set yields elements:
s = {1, 2, 3, 4, 5}
for item in s:
    print(item)
# Output: 1, 2, 3, 4, 5
```

**Why this matters**:
- Regular sets iterate over discrete elements
- IntervalSet iterates over continuous interval components
- This is mathematically correct (continuous sets are uncountable)
- BUT: Different semantics from Eule's typical use case

**Impact on Eule**:
- If Eule tries to iterate "elements" from results, it gets Intervals instead
- May or may not be an issue depending on use case
- Works fine if user wants to work with interval components

---

### 4. **Missing `__bool__()` on Interval Class** ⚠️ PARTIAL ISSUE

**Problem**: The `Interval` class doesn't implement `__bool__()`:

```python
interval = Interval(0, 10)
bool(interval)  # Uses default object.__bool__() → always True

interval_set = IntervalSet([Interval(0, 10)])
bool(interval_set)  # ✅ Correctly checks is_empty()
```

**Why this matters**:
- When operations return `Interval` (not `IntervalSet`), emptiness checks fail
- Eule's algorithm relies on `if result:` checks to detect empty sets
- Empty intervals would be treated as non-empty

---

## Technical Deep Dive

### The Type Return Problem in Detail

IntervalSet's operation behavior:

| Operation | Operands | Result Type | Example |
|-----------|----------|-------------|---------|
| `union()` | Overlapping | `Interval` | `[0,5] ∪ [3,8] → [0,8]` |
| `union()` | Adjacent | `Interval` | `[0,5] ∪ [5,10] → [0,10]` |
| `union()` | Disjoint | `IntervalSet` | `[0,5] ∪ [10,15] → {[0,5], [10,15]}` |
| `intersection()` | Overlapping | `Interval` | `[0,10] ∩ [5,15] → [5,10]` |
| `intersection()` | Disjoint | `IntervalSet` (empty) | `[0,5] ∩ [10,15] → ∅` |
| `difference()` | Subset | `Interval` | `[0,10] \ [3,7] → [0,3)` |
| `difference()` | Split result | `IntervalSet` | `[0,10] \ [3,7] → {[0,3), (7,10]}` |

**The problem**: Return type depends on geometric relationship between operands, which cannot be statically determined.

### Why This Breaks Eule's Algorithm

Eule's internal pseudo-code:
```python
def euler(sets: dict[str, SetLike]) -> dict:
    result = {}
    for combination in powerset(sets.keys()):
        # Start with intersection of all sets in combination
        region = sets[combination[0]]
        for key in combination[1:]:
            region = region.intersection(sets[key])  # ← May return Interval!
        
        # Subtract overlaps
        for other_key in other_keys:
            region = region.difference(sets[other_key])  # ← Fails if region is Interval!
        
        if region:  # ← Fails if region is Interval (no __bool__)
            result[combination] = list(region)  # ← What does list() of Interval do?
    
    return result
```

**Failure points**:
1. `intersection()` may return `Interval` instead of `IntervalSet`
2. Next `difference()` call tries to call `.difference()` on `Interval`
3. Result might be `Interval` or `IntervalSet` unpredictably
4. `bool(interval)` always returns `True` (no `__bool__()` implementation)
5. `list(interval)` fails (no `__iter__()` on `Interval`)

---

## Possible Solutions

### Solution 1: **Wrapper Adapter (Current Implementation)** ⭐ RECOMMENDED

**Approach**: Wrap IntervalSet in an adapter that enforces type consistency.

```python
class IntervalSetAdapter:
    def __init__(self, interval_set: IntervalSet):
        self._data = interval_set
    
    def union(self, other):
        result = self._data.union(other._data)
        # Always wrap result in adapter
        if isinstance(result, Interval):
            result = IntervalSet([result])
        return IntervalSetAdapter(result)
    
    def intersection(self, other):
        result = self._data.intersection(other._data)
        if isinstance(result, Interval):
            result = IntervalSet([result])
        return IntervalSetAdapter(result)
    
    def difference(self, other):
        result = self._data.difference(other._data)
        if isinstance(result, Interval):
            result = IntervalSet([result])
        return IntervalSetAdapter(result)
    
    def __bool__(self):
        return not self._data.is_empty()
    
    def __iter__(self):
        return iter(self._data)
    
    @classmethod
    def from_iterable(cls, iterable):
        return cls(IntervalSet(iterable))
```

**Pros**:
- ✅ Ensures type consistency
- ✅ Adds missing `from_iterable()`
- ✅ Maintains all IntervalSet functionality
- ✅ No changes to interval-sets library needed

**Cons**:
- ⚠️ Extra wrapping/unwrapping overhead
- ⚠️ Users must explicitly use adapter
- ⚠️ Results are wrapped, not native IntervalSet

---

### Solution 2: **Monkey-Patching** ⚠️ FRAGILE

**Approach**: Modify IntervalSet class at runtime.

```python
def _ensure_interval_set(result):
    if isinstance(result, Interval):
        return IntervalSet([result])
    return result

# Monkey-patch the class
_original_union = IntervalSet.union
def _wrapped_union(self, other):
    return _ensure_interval_set(_original_union(self, other))

IntervalSet.union = _wrapped_union
IntervalSet.from_iterable = classmethod(lambda cls, it: cls(it))
```

**Pros**:
- ✅ Transparent to users
- ✅ Works with existing code

**Cons**:
- ❌ Breaks library semantics
- ❌ Affects all code using interval-sets
- ❌ Fragile across library versions
- ❌ May break other interval-sets users

---

### Solution 3: **Fork/Extend interval-sets** ❌ NOT RECOMMENDED

**Approach**: Create a subclass or fork that enforces consistent types.

```python
class EuleIntervalSet(IntervalSet):
    def union(self, other):
        result = super().union(other)
        if isinstance(result, Interval):
            return EuleIntervalSet([result])
        return result
    
    @classmethod
    def from_iterable(cls, iterable):
        return cls(iterable)
```

**Pros**:
- ✅ Clean separation of concerns
- ✅ No monkey-patching

**Cons**:
- ❌ Requires maintaining separate class
- ❌ Users must use EuleIntervalSet, not IntervalSet
- ❌ Loses ability to use native IntervalSet objects

---

### Solution 4: **Upstream Contribution** 🌟 IDEAL (LONG-TERM)

**Approach**: Add an option to interval-sets for consistent return types.

```python
# Proposed addition to interval-sets
class IntervalSet:
    def __init__(self, ..., *, always_return_set=False):
        self._always_return_set = always_return_set
    
    def union(self, other):
        result = ...  # existing logic
        if self._always_return_set and isinstance(result, Interval):
            return IntervalSet([result])
        return result
    
    @classmethod
    def from_iterable(cls, iterable):
        return cls(iterable)
```

**Pros**:
- ✅ Benefits entire ecosystem
- ✅ Opt-in, doesn't break existing behavior
- ✅ Proper upstream support

**Cons**:
- ⏱️ Requires upstream approval
- ⏱️ Takes time to implement and release
- ⏱️ May not align with library's design philosophy

---

## Recommendations

### For Eule Maintainers

1. **Keep the adapter approach** (Solution 1)
   - It's the safest and most maintainable
   - Document the limitations clearly
   - Provide clear examples in documentation

2. **Improve adapter coverage**
   - Current coverage: 30%
   - Add comprehensive tests for edge cases
   - Test with various interval configurations

3. **Document the mismatch**
   - Explain why direct IntervalSet use doesn't work
   - Show adapter usage patterns
   - Provide migration guide

4. **Consider upstreaming** (long-term)
   - Open discussion with interval-sets maintainers
   - Propose `from_iterable()` addition
   - Discuss optional type consistency mode

### For interval-sets Maintainers (Me! 👋)

1. **Add `from_iterable()` classmethod**
   - This is non-breaking and useful
   - Improves protocol compatibility
   - Simple addition:
     ```python
     @classmethod
     def from_iterable(cls, iterable):
         return cls(iterable)
     ```

2. **Consider type consistency option**
   - Add optional `always_return_set` parameter
   - Maintains backward compatibility
   - Enables protocol compliance

3. **Add `__bool__()` to Interval**
   - Should return `not self.is_empty()`
   - Fixes emptiness checking issue
   - Semantically correct behavior

---

## Conclusion

**Bottom Line**: IntervalSet cannot directly implement Eule's SetLike protocol due to fundamental design incompatibilities around return type consistency. The **adapter pattern is the correct solution** and should be maintained and improved.

The incompatibility stems from different design goals:
- **interval-sets**: Mathematical correctness, returning most specific type
- **eule**: Type protocol compliance, consistent return types for chaining

Both designs are valid for their use cases, and the adapter pattern is the appropriate bridge between them.

### Compatibility Matrix

| Feature | IntervalSet | Eule SetLike | Compatible? | Solution |
|---------|-------------|--------------|-------------|----------|
| `union()` | ✅ | ✅ | ⚠️ Type varies | Adapter wraps results |
| `intersection()` | ✅ | ✅ | ⚠️ Type varies | Adapter wraps results |
| `difference()` | ✅ | ✅ | ⚠️ Type varies | Adapter wraps results |
| `__bool__()` | ✅ (IntervalSet) | ✅ | ⚠️ Interval lacks it | Adapter implements |
| `__iter__()` | ✅ | ✅ | ⚠️ Different semantics | Works, but different meaning |
| `from_iterable()` | ❌ | ✅ | ❌ | Adapter adds it |

**Final Verdict**: ✅ **Usable via adapter**, ❌ **Not natively compatible**
