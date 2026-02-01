# IntervalSet Compatibility Analysis

## Summary

**Conclusion**: IntervalSet from interval-sets library is **not suitable** for eule's Euler diagram generation because they solve fundamentally different problems:

- **eule**: Discrete set partitioning (elements are discrete, countable items)
- **interval-sets**: Continuous range analysis (elements are intervals on the real number line ℝ)

## Why IntervalSet Cannot Work with Eule

### 1. Different Element Types

```python
# Eule expects discrete elements
discrete_set = {1, 2, 3, 4, 5}  # Elements are integers/objects

# IntervalSet contains Interval objects, not discrete elements
interval_set = IntervalSet([Interval(0, 10)])  # Contains one Interval object
list(interval_set)  # Returns: [Interval(0, 10)]  ❌ Not discrete elements
```

### 2. Different Iteration Semantics

```python
# Eule's algorithm iterates over discrete elements
for element in {1, 2, 3}:
    process(element)  # Processes 1, then 2, then 3

# IntervalSet iterates over Interval objects
for interval in IntervalSet([Interval(0, 10)]):
    process(interval)  # Processes Interval(0, 10) as a whole
```

### 3. Different Mathematical Operations

**Eule (Discrete Sets)**:
- Union: `{1, 2} ∪ {2, 3} = {1, 2, 3}`
- Intersection: `{1, 2} ∩ {2, 3} = {2}`
- Elements are discrete, finite, and countable

**IntervalSet (Continuous Ranges)**:
- Union: `[0, 5] ∪ [3, 8] = [0, 8]` (merged continuous range)
- Intersection: `[0, 5] ∩ [3, 8] = [3, 5]` (continuous sub-range)
- Elements are continuous ranges with infinite points

## What Eule's SetLike Protocol Requires

For a type to work with eule, it must:

1. **Iterate over discrete elements**: `__iter__()` must yield individual, comparable elements
2. **Support set operations on discrete elements**: `union()`, `intersection()`, `difference()`
3. **Be countable**: Must have a finite, discrete element space

## IntervalSet's Design vs SetLike Requirements

| Requirement | IntervalSet | Compatible? |
|-------------|-------------|-------------|
| `__iter__()` yields discrete elements | ❌ Yields Interval objects | No |
| Discrete element space | ❌ Represents continuous ranges | No |
| Countable elements | ❌ Infinite points in each interval | No |
| Set operations | ✅ union(), intersection(), difference() | Partial |

## Use Case Separation

### ✅ Use eule for Discrete Element Analysis

```python
from eule import euler

# Customer segments (discrete customer IDs)
segments = {
    'premium': {101, 102, 103, 104},
    'active': {102, 103, 105, 106},
    'recent': {103, 107, 108}
}

result = euler(segments)
# Result shows which customers belong to which segment combinations
```

### ✅ Use interval-sets for Continuous Range Analysis

```python
from interval_sets import Interval, IntervalSet

# Temperature ranges (continuous values)
cold = IntervalSet([Interval(0, 15)])
moderate = IntervalSet([Interval(10, 25)])
hot = IntervalSet([Interval(20, 40)])

# Direct set operations on continuous ranges
cold_only = cold - moderate  # [0, 10)
overlap = cold & moderate    # [10, 15]
```

## Alternative: Discretization (Advanced)

If you need to analyze continuous intervals using eule, you must **discretize** them first:

```python
from interval_sets import Interval, IntervalSet
from eule import euler

def discretize_intervalset(iset: IntervalSet, step: float = 1.0) -> set:
    """
    Convert continuous IntervalSet to discrete set of points.
    
    WARNING: This loses continuous semantics and may be memory-intensive.
    """
    points = set()
    for interval in iset:
        start = int(interval._start) if interval.open_start else int(interval._start)
        end = int(interval._end) if interval.open_end else int(interval._end) + 1
        points.update(range(start, end))
    return points

# Discretize temperature ranges to integer degrees
temps = {
    'cold': discretize_intervalset(IntervalSet([Interval(0, 15)])),
    'moderate': discretize_intervalset(IntervalSet([Interval(10, 25)])),
    'hot': discretize_intervalset(IntervalSet([Interval(20, 40)]))
}

result = euler(temps)
# Now works, but loses continuous semantics (e.g., 10.5°C is not represented)
```

## Technical Limitations Encountered

When attempting to use IntervalSet directly with eule:

1. **Type mismatch**: Eule's algorithm expects elements to be comparable/hashable discrete items, not Interval objects
2. **Iteration incompatibility**: `for elem in IntervalSet([...])` yields Interval objects, not the infinite points within
3. **Semantic mismatch**: Euler diagrams show discrete element partitioning, not continuous range decomposition

## Recommendation

**Do not try to make IntervalSet compatible with eule**. They solve different problems:

- **For discrete analysis** (customers, categories, items): Use **eule**
- **For continuous analysis** (temperatures, measurements, ranges): Use **interval-sets** directly

Both libraries excel in their respective domains. Attempting to bridge them would require fundamental changes that compromise the design of both.

## See Also

- [SetLike Protocol Specification](design/PROTOCOL_SPECIFICATION.md)
- [Custom Adapter Guide](design/ADAPTER_GUIDE.md)
- [interval-sets Documentation](https://github.com/brunolnetto/interval-sets)
