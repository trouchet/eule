# Automatic Type Adaptation Design for Eule

## Overview

This document details the design for **transparent automatic type adaptation** in eule. Users should never need to manually wrap their set-like objects - the library handles this internally.

## Design Principle

**Zero-friction extensibility**: Users pass in their custom set types, and eule automatically detects and adapts them without any manual wrapping.

```python
# ✅ GOOD - User never wraps anything
from eule import euler
from interval_sets import Interval, IntervalSet

sets = {
    'cold': IntervalSet([Interval(0, 15)]),      # Just pass the object
    'warm': IntervalSet([Interval(10, 25)]),     # No wrapping needed
    'hot': IntervalSet([Interval(20, 40)])
}

diagram = euler(sets)  # Library handles adaptation internally
```

```python
# ❌ BAD - Requiring manual wrapping (what we want to AVOID)
from eule.adapters import IntervalSetAdapter

sets = {
    'cold': IntervalSetAdapter(IntervalSet([...])),  # Too much boilerplate
    'warm': IntervalSetAdapter(IntervalSet([...])),
}
```

## Implementation Strategy

### Architecture Overview

```
User Code
    ↓
euler(sets) / Euler(sets)
    ↓
[Type Detection Layer]  ← Automatic adaptation happens here
    ↓
euler_generator(adapted_sets)
    ↓
operations.py (union/intersection/difference)
    ↓
SetLike Protocol operations
```

### Core Components

#### 1. Type Registry (Extensible Plugin System)

```python
# eule/registry.py
"""Type adapter registry for automatic type detection."""

from typing import Type, Callable, Any, Optional
from .protocols import SetLike

class TypeRegistry:
    """
    Registry for automatic type adaptation.
    
    Allows registering custom adapters for specific types or detection functions.
    """
    
    def __init__(self):
        # Type-specific adapters: {type: adapter_factory}
        self._type_adapters: dict[Type, Callable[[Any], SetLike]] = {}
        
        # Detection functions: [(predicate, adapter_factory)]
        self._detection_rules: list[tuple[Callable[[Any], bool], Callable[[Any], SetLike]]] = []
    
    def register_type(self, target_type: Type, adapter_factory: Callable[[Any], SetLike]):
        """
        Register an adapter for a specific type.
        
        Example:
            registry.register_type(IntervalSet, IntervalSetAdapter)
        """
        self._type_adapters[target_type] = adapter_factory
    
    def register_detector(
        self, 
        predicate: Callable[[Any], bool], 
        adapter_factory: Callable[[Any], SetLike]
    ):
        """
        Register a detection rule based on a predicate function.
        
        Example:
            registry.register_detector(
                lambda obj: hasattr(obj, 'measure') and hasattr(obj, 'intervals'),
                IntervalSetAdapter
            )
        """
        self._detection_rules.append((predicate, adapter_factory))
    
    def adapt(self, obj: Any) -> SetLike:
        """
        Automatically adapt an object to SetLike protocol.
        
        Detection order:
        1. Already SetLike → return as-is
        2. Exact type match → use registered adapter
        3. Detection rules → first matching rule
        4. Built-in types → use default adapters
        5. Duck-typing → check for protocol methods
        6. Fallback → convert to set
        """
        # 1. Already protocol-compliant
        if self._is_setlike(obj):
            return obj
        
        # 2. Exact type match
        obj_type = type(obj)
        if obj_type in self._type_adapters:
            return self._type_adapters[obj_type](obj)
        
        # 3. Detection rules (in registration order)
        for predicate, adapter_factory in self._detection_rules:
            if predicate(obj):
                return adapter_factory(obj)
        
        # 4. Built-in types
        if isinstance(obj, set):
            from .adapters import SetAdapter
            return SetAdapter(obj)
        
        if isinstance(obj, (list, tuple)):
            from .adapters import ListAdapter
            return ListAdapter(obj)
        
        # 5. Duck-typing: check if it already implements the protocol methods
        if self._has_protocol_methods(obj):
            return obj  # Treat as SetLike
        
        # 6. Fallback: try to convert to iterable
        if hasattr(obj, '__iter__'):
            from .adapters import SetAdapter
            return SetAdapter(obj)
        
        raise TypeError(
            f"Cannot adapt {type(obj).__name__} to SetLike protocol. "
            f"Please implement union(), intersection(), difference(), __bool__(), and __iter__() methods, "
            f"or register a custom adapter."
        )
    
    def _is_setlike(self, obj: Any) -> bool:
        """Check if object satisfies SetLike protocol."""
        from .protocols import SetLike
        try:
            return isinstance(obj, SetLike)
        except TypeError:
            return False
    
    def _has_protocol_methods(self, obj: Any) -> bool:
        """Check if object has all required protocol methods."""
        required_methods = ['union', 'intersection', 'difference', '__bool__', '__iter__']
        return all(
            hasattr(obj, method) and callable(getattr(obj, method, None))
            for method in required_methods
        )


# Global registry instance
_global_registry = TypeRegistry()


def get_registry() -> TypeRegistry:
    """Get the global type registry."""
    return _global_registry


def register_adapter(target_type: Type, adapter_factory: Callable[[Any], SetLike]):
    """
    Convenience function to register an adapter globally.
    
    Example:
        from eule import register_adapter
        from interval_sets import IntervalSet
        from my_adapters import IntervalSetAdapter
        
        register_adapter(IntervalSet, IntervalSetAdapter)
    """
    _global_registry.register_type(target_type, adapter_factory)


def register_detector(predicate: Callable[[Any], bool], adapter_factory: Callable[[Any], SetLike]):
    """
    Convenience function to register a detector globally.
    
    Example:
        from eule import register_detector
        
        register_detector(
            lambda obj: hasattr(obj, 'is_interval_set'),
            IntervalSetAdapter
        )
    """
    _global_registry.register_detector(predicate, adapter_factory)
```

#### 2. Adaptation Layer

```python
# eule/adaptation.py
"""Automatic type adaptation layer."""

from typing import Dict, Any
from copy import deepcopy
from .types import SetsType, KeyType, SetType
from .registry import get_registry
from .protocols import SetLike

def adapt_sets(sets: SetsType) -> Dict[KeyType, SetLike]:
    """
    Automatically adapt all sets in the input to SetLike protocol.
    
    Args:
        sets: Dictionary or list of sets (can be any type)
    
    Returns:
        Dictionary with all values adapted to SetLike protocol
    
    Examples:
        # Built-in types
        adapt_sets({'a': [1, 2, 3], 'b': {2, 3, 4}})
        
        # Custom types (automatically detected)
        adapt_sets({'a': IntervalSet([...]), 'b': SparseSet([...])})
        
        # Mixed types
        adapt_sets({'a': [1, 2], 'b': IntervalSet([...])})
    """
    registry = get_registry()
    
    # Handle list input (convert to dict with numeric keys)
    if isinstance(sets, list):
        sets = {i: set_val for i, set_val in enumerate(sets)}
    
    # Deep copy to avoid modifying original
    sets_copy = deepcopy(sets)
    
    # Adapt each set value
    adapted = {}
    for key, value in sets_copy.items():
        try:
            adapted[key] = registry.adapt(value)
        except TypeError as e:
            raise TypeError(
                f"Failed to adapt set '{key}': {e}"
            ) from e
    
    return adapted


def unwrap_sets(adapted_sets: Dict[KeyType, SetLike]) -> Dict[KeyType, Any]:
    """
    Convert adapted sets back to their original types if possible.
    
    This preserves the user's original types in the output.
    """
    unwrapped = {}
    for key, value in adapted_sets.items():
        # Try to unwrap adapters
        if hasattr(value, 'to_native'):
            unwrapped[key] = value.to_native()
        # Try to get internal data
        elif hasattr(value, '_data'):
            unwrapped[key] = value._data
        # Return as-is if no unwrapping method
        else:
            unwrapped[key] = value
    
    return unwrapped
```

#### 3. Modified Core Module

```python
# eule/core.py (modifications)

from .adaptation import adapt_sets, unwrap_sets

def euler_generator(sets: SetsType):
    """
    Generator for Euler diagram regions.
    
    Now automatically adapts input types!
    """
    # NEW: Automatic adaptation layer
    adapted_sets = adapt_sets(sets)
    
    # Deep copy of adapted sets
    sets_ = deepcopy(adapted_sets)
    # ... rest of existing algorithm unchanged ...
    
    # The algorithm now works with SetLike objects
    # operations.py functions will use .union(), .intersection(), .difference()
```

#### 4. Enhanced Operations Module

```python
# eule/operations.py (refactored)

from typing import TypeVar
from .protocols import SetLike

T = TypeVar('T', bound=SetLike)

def union(set_a: T, set_b: T) -> T:
    """
    Generic union operation.
    
    Automatically uses the appropriate method:
    - If SetLike: calls set_a.union(set_b)
    - Otherwise: falls back to set operations
    """
    # Try protocol method first
    if hasattr(set_a, 'union') and callable(set_a.union):
        return set_a.union(set_b)
    
    # Fallback to old behavior for backward compatibility
    from .utils import setify_sequences
    set_a_converted, set_b_converted = setify_sequences([set_a, set_b])
    union_set = set_a_converted.union(set_b_converted)
    return type(set_a)(union_set)


def intersection(set_a: T, set_b: T) -> T:
    """Generic intersection operation."""
    if hasattr(set_a, 'intersection') and callable(set_a.intersection):
        return set_a.intersection(set_b)
    
    from .utils import setify_sequences
    set_a_converted, set_b_converted = setify_sequences([set_a, set_b])
    intersec_set = set_a_converted.intersection(set_b_converted)
    return type(set_a)(intersec_set)


def difference(set_a: T, set_b: T) -> T:
    """Generic difference operation."""
    if hasattr(set_a, 'difference') and callable(set_a.difference):
        return set_a.difference(set_b)
    
    from .utils import setify_sequences
    set_a_converted, set_b_converted = setify_sequences([set_a, set_b])
    diff_set = set_a_converted - set_b_converted
    return type(set_a)(diff_set)
```

### Pre-registered Adapters

```python
# eule/adapters/__init__.py
"""Pre-built adapters for common types."""

from .builtin_adapters import SetAdapter, ListAdapter, TupleAdapter
from .interval_adapter import IntervalSetAdapter  # Optional, if interval-sets installed

# Auto-register built-in adapters
from ..registry import register_adapter

# These are already handled in the registry's adapt() method,
# but we can explicitly register them for clarity
register_adapter(set, lambda s: SetAdapter(s))
register_adapter(list, lambda l: ListAdapter(l))
register_adapter(tuple, lambda t: ListAdapter(t))

# Try to register interval-sets adapter if available
try:
    from interval_sets import IntervalSet
    register_adapter(IntervalSet, lambda i: IntervalSetAdapter(i))
except ImportError:
    pass  # interval-sets not installed

__all__ = ['SetAdapter', 'ListAdapter', 'TupleAdapter', 'IntervalSetAdapter']
```

## User Experience

### Example 1: Built-in Types (No Change)

```python
from eule import euler

# Works exactly as before - no changes needed
sets = {
    'a': [1, 2, 3],
    'b': [2, 3, 4],
    'c': [3, 4, 5]
}

diagram = euler(sets)
# Automatically adapts lists → continues working
```

### Example 2: IntervalSet (Zero Configuration)

```python
from eule import euler
from interval_sets import Interval, IntervalSet

# Just use IntervalSet directly - no wrapping!
sets = {
    'cold': IntervalSet([Interval(0, 15)]),
    'warm': IntervalSet([Interval(10, 25)]),
    'hot': IntervalSet([Interval(20, 40)])
}

diagram = euler(sets)
# Automatically detects and adapts IntervalSet
# Returns: {
#   ('cold',): IntervalSet([Interval(0, 10)]),
#   ('cold', 'warm'): IntervalSet([Interval(10, 15)]),
#   ...
# }
```

### Example 3: Custom Type (With Registration)

```python
from eule import euler, register_adapter
from eule.protocols import SetLike

class MyCustomSet:
    def __init__(self, data):
        self.data = set(data)
    
    def union(self, other):
        return MyCustomSet(self.data | other.data)
    
    def intersection(self, other):
        return MyCustomSet(self.data & other.data)
    
    def difference(self, other):
        return MyCustomSet(self.data - other.data)
    
    def __bool__(self):
        return bool(self.data)
    
    def __iter__(self):
        return iter(self.data)

# Option 1: Register once globally (recommended for libraries)
register_adapter(MyCustomSet, lambda x: x)  # Already protocol-compliant

# Option 2: Just use it (duck-typing detection)
sets = {
    'a': MyCustomSet([1, 2, 3]),
    'b': MyCustomSet([2, 3, 4])
}

diagram = euler(sets)
# Works! Auto-detected via duck-typing
```

### Example 4: Mixed Types

```python
from eule import euler
from interval_sets import Interval, IntervalSet

# Mix different types in the same diagram!
sets = {
    'discrete': [1, 2, 3, 4, 5],                    # Built-in list
    'continuous': IntervalSet([Interval(2.5, 4.5)]) # IntervalSet
}

diagram = euler(sets)
# Both types automatically adapted and work together
```

## Advanced: Plugin Registration

### Third-party Library Integration

A third-party library can register its own adapters:

```python
# In interval-sets library (optional integration module)
# interval_sets/eule_integration.py

def register_with_eule():
    """Register IntervalSet with eule automatically."""
    try:
        from eule import register_adapter
        from .intervals import IntervalSet
        from .eule_adapter import IntervalSetAdapter
        
        register_adapter(IntervalSet, IntervalSetAdapter)
        return True
    except ImportError:
        return False  # eule not installed

# Auto-register on import (optional)
register_with_eule()
```

Users can then just:
```python
import interval_sets.eule_integration  # Auto-registers
from eule import euler
from interval_sets import IntervalSet

# Now IntervalSet works automatically!
```

### Detection-based Registration

For types from libraries you don't control:

```python
from eule import register_detector

# Register based on duck-typing
register_detector(
    lambda obj: hasattr(obj, 'measure') and hasattr(obj, 'intervals'),
    lambda obj: IntervalSetAdapter(obj)
)

# Now any object with .measure and .intervals attributes will be adapted
```

## Implementation Checklist

### Phase 1: Core Infrastructure ✅
- [x] Define `SetLike` protocol in `protocols.py`
- [ ] Implement `TypeRegistry` in `registry.py`
- [ ] Implement `adapt_sets()` and `unwrap_sets()` in `adaptation.py`

### Phase 2: Adapters
- [ ] Implement `SetAdapter`, `ListAdapter`, `TupleAdapter` in `adapters/builtin_adapters.py`
- [ ] Implement `IntervalSetAdapter` in `adapters/interval_adapter.py` (optional)
- [ ] Add adapter tests

### Phase 3: Core Integration
- [ ] Modify `euler_generator()` to use `adapt_sets()`
- [ ] Modify `operations.py` to use protocol methods
- [ ] Ensure backward compatibility

### Phase 4: Testing
- [ ] Test with built-in types (regression)
- [ ] Test with IntervalSet
- [ ] Test with custom types
- [ ] Test mixed types
- [ ] Test registration API
- [ ] Performance benchmarks

### Phase 5: Documentation
- [ ] Update README with new capabilities
- [ ] Add tutorial for custom types
- [ ] Add API documentation for registration
- [ ] Add examples for interval-sets integration

## Performance Considerations

### Minimal Overhead
- Type detection happens **once** at entry (in `adapt_sets()`)
- Algorithm execution uses native protocol methods (no conversion)
- Zero overhead for already-compliant types

### Optimization Strategy
```python
# Cached type detection
class TypeRegistry:
    def __init__(self):
        self._cache: dict[Type, Callable] = {}  # Cache detection results
    
    def adapt(self, obj):
        obj_type = type(obj)
        
        # Check cache first
        if obj_type in self._cache:
            return self._cache[obj_type](obj)
        
        # ... detection logic ...
        
        # Cache the adapter factory
        self._cache[obj_type] = adapter_factory
        return adapter_factory(obj)
```

## Backward Compatibility

### 100% Backward Compatible
- All existing code continues to work
- Lists, tuples, sets work as before
- Output types preserved when possible
- No breaking changes

### Migration Path
```python
# Old code (still works)
sets = {'a': [1, 2, 3], 'b': [2, 3, 4]}
euler(sets)  # ✅ Works

# New code (just works)
sets = {'a': IntervalSet([...]), 'b': IntervalSet([...])}
euler(sets)  # ✅ Works without any changes!
```

## Conclusion

This design provides **zero-friction extensibility** while maintaining **100% backward compatibility**. Users never need to wrap their objects - eule handles everything automatically through:

1. **Smart type detection** (exact match → duck-typing → fallback)
2. **Extensible registry** (libraries can register their types)
3. **Protocol-based operations** (native performance for custom types)
4. **Graceful degradation** (falls back to conversion when needed)

The user experience is seamless: just pass in your objects, and eule figures out the rest!
