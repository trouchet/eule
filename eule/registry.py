"""Type adapter registry for automatic type detection.

This module provides a registry system for registering custom adapters
for any set-like type to work with eule.
"""

from typing import Type, Callable, Any, Dict, List, Tuple
from .protocols import SetLike

__all__ = ['TypeRegistry', 'get_registry', 'register_adapter', 'register_detector']


class TypeRegistry:
    """
    Registry for automatic type adaptation.
    
    Allows registering custom adapters for specific types or detection functions.
    
    Example:
        >>> registry = TypeRegistry()
        >>> registry.register_type(MyCustomSet, lambda x: x)
        >>> adapted = registry.adapt(MyCustomSet([1, 2, 3]))
    """
    
    def __init__(self):
        # Type-specific adapters: {type: adapter_factory}
        self._type_adapters: Dict[Type, Callable[[Any], SetLike]] = {}
        
        # Detection functions: [(predicate, adapter_factory)]
        self._detection_rules: List[Tuple[Callable[[Any], bool], Callable[[Any], SetLike]]] = []
        
        # Cache for performance: {type: adapter_factory}
        self._cache: Dict[Type, Callable[[Any], SetLike]] = {}
    
    def register_type(self, target_type: Type, adapter_factory: Callable[[Any], SetLike]) -> None:
        """
        Register an adapter for a specific type.
        
        Args:
            target_type: The type to register
            adapter_factory: A function that takes an instance and returns a SetLike object
            
        Example:
            >>> from interval_sets import IntervalSet
            >>> registry.register_type(IntervalSet, lambda x: x)
        """
        self._type_adapters[target_type] = adapter_factory
        # Clear cache for this type
        if target_type in self._cache:
            del self._cache[target_type]
    
    def register_detector(
        self, 
        predicate: Callable[[Any], bool], 
        adapter_factory: Callable[[Any], SetLike]
    ) -> None:
        """
        Register a detection rule based on a predicate function.
        
        Args:
            predicate: Function that returns True if the adapter should be used
            adapter_factory: Function that converts object to SetLike
            
        Example:
            >>> registry.register_detector(
            ...     lambda obj: hasattr(obj, 'measure'),
            ...     IntervalSetAdapter
            ... )
        """
        self._detection_rules.append((predicate, adapter_factory))
    
    def adapt(self, obj: Any) -> SetLike:
        """
        Automatically adapt an object to SetLike protocol.
        
        Detection order:
        1. Already SetLike → return as-is
        2. Cached type → use cached adapter
        3. Exact type match → use registered adapter
        4. Detection rules → first matching rule
        5. Built-in types → use default adapters
        6. Duck-typing → check for protocol methods
        7. Fallback → convert to iterable
        
        Args:
            obj: The object to adapt
            
        Returns:
            A SetLike object
            
        Raises:
            TypeError: If the object cannot be adapted
        """
        # 1. Already protocol-compliant
        if self._is_setlike(obj):
            return obj
        
        obj_type = type(obj)
        
        # 2. Check cache first
        if obj_type in self._cache:
            return self._cache[obj_type](obj)
        
        # 3. Exact type match
        if obj_type in self._type_adapters:
            adapter_factory = self._type_adapters[obj_type]
            self._cache[obj_type] = adapter_factory
            return adapter_factory(obj)
        
        # 4. Detection rules (in registration order)
        for predicate, adapter_factory in self._detection_rules:
            if predicate(obj):
                self._cache[obj_type] = adapter_factory
                return adapter_factory(obj)
        
        # 5. Built-in types
        if isinstance(obj, set):
            from .adapters import SetAdapter
            adapter_factory = SetAdapter
            self._cache[obj_type] = adapter_factory
            return adapter_factory(obj)
        
        if isinstance(obj, (list, tuple)):
            from .adapters import ListAdapter
            adapter_factory = ListAdapter
            self._cache[obj_type] = adapter_factory
            return adapter_factory(obj)
        
        # 6. Duck-typing: check if it already implements the protocol methods
        if self._has_protocol_methods(obj):
            # Cache identity function for this type
            self._cache[obj_type] = lambda x: x
            return obj
        
        # 7. Fallback: try to convert to iterable
        if hasattr(obj, '__iter__'):
            from .adapters import SetAdapter
            adapter_factory = SetAdapter
            self._cache[obj_type] = adapter_factory
            return adapter_factory(obj)
        
        raise TypeError(
            f"Cannot adapt {type(obj).__name__} to SetLike protocol. "
            f"Please implement union(), intersection(), difference(), __bool__(), and __iter__() methods, "
            f"or register a custom adapter using register_adapter()."
        )
    
    def _is_setlike(self, obj: Any) -> bool:
        """Check if object satisfies SetLike protocol."""
        try:
            return isinstance(obj, SetLike)
        except TypeError:
            # Protocol check can raise TypeError in some cases
            return False
    
    def _has_protocol_methods(self, obj: Any) -> bool:
        """Check if object has all required protocol methods."""
        required_methods = ['union', 'intersection', 'difference', '__bool__', '__iter__']
        return all(
            hasattr(obj, method) and callable(getattr(obj, method, None))
            for method in required_methods
        )
    
    def clear_cache(self) -> None:
        """Clear the adapter cache."""
        self._cache.clear()


# Global registry instance
_global_registry = TypeRegistry()


def get_registry() -> TypeRegistry:
    """
    Get the global type registry.
    
    Returns:
        The global TypeRegistry instance
    """
    return _global_registry


def register_adapter(target_type: Type, adapter_factory: Callable[[Any], SetLike]) -> None:
    """
    Convenience function to register an adapter globally.
    
    Args:
        target_type: The type to register
        adapter_factory: Function to convert instances to SetLike
        
    Example:
        >>> from eule import register_adapter
        >>> from interval_sets import IntervalSet
        >>> 
        >>> register_adapter(IntervalSet, lambda x: x)  # If already compatible
    """
    _global_registry.register_type(target_type, adapter_factory)


def register_detector(predicate: Callable[[Any], bool], adapter_factory: Callable[[Any], SetLike]) -> None:
    """
    Convenience function to register a detector globally.
    
    Args:
        predicate: Function that returns True if adapter should be used
        adapter_factory: Function to convert to SetLike
        
    Example:
        >>> from eule import register_detector
        >>> 
        >>> register_detector(
        ...     lambda obj: hasattr(obj, 'is_interval_set'),
        ...     IntervalSetAdapter
        ... )
    """
    _global_registry.register_detector(predicate, adapter_factory)
