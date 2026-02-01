"""Automatic type adaptation layer.

This module provides automatic conversion of input sets to SetLike protocol
objects, enabling seamless integration with custom types.
"""

from typing import Dict, Any
from copy import deepcopy
from .types import SetsType, KeyType
from .protocols import SetLike
from .registry import get_registry

__all__ = ['adapt_sets', 'unwrap_result']


def adapt_sets(sets: SetsType) -> Dict[KeyType, SetLike]:
    """
    Automatically adapt all sets in the input to SetLike protocol.
    
    This function is the main entry point for automatic type adaptation.
    It handles both dict and list inputs and adapts each set value to
    the SetLike protocol using the global type registry.
    
    Args:
        sets: Dictionary or list of sets (can be any type)
    
    Returns:
        Dictionary with all values adapted to SetLike protocol
    
    Raises:
        TypeError: If sets is not a dict or list, or if a set cannot be adapted
    
    Examples:
        >>> # Built-in types
        >>> adapt_sets({'a': [1, 2, 3], 'b': {2, 3, 4}})
        {'a': ListAdapter([1, 2, 3]), 'b': SetAdapter({2, 3, 4})}
        
        >>> # Custom types (automatically detected)
        >>> adapt_sets({'a': IntervalSet([...]), 'b': SparseSet([...])})
        {'a': IntervalSet([...]), 'b': SparseSet([...])}
        
        >>> # Mixed types
        >>> adapt_sets({'a': [1, 2], 'b': IntervalSet([...])})
        {'a': ListAdapter([1, 2]), 'b': IntervalSet([...])}
    """
    registry = get_registry()
    
    # Validate input type
    if not isinstance(sets, (list, dict)):
        raise TypeError(
            'Ill-conditioned input.'
            'It must be either a dict or array of arrays object!'
        )
    
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


def unwrap_result(euler_dict: Dict[KeyType, SetLike]) -> Dict[KeyType, Any]:
    """
    Convert adapted sets back to their original types if possible.
    
    This preserves the user's original types in the output, providing
    a seamless experience where input and output types match.
    
    Args:
        euler_dict: Dictionary with SetLike values (result from euler_generator)
    
    Returns:
        Dictionary with values converted back to native types
    
    Examples:
        >>> result = {('a',): ListAdapter([1, 2, 3])}
        >>> unwrap_result(result)
        {('a',): [1, 2, 3]}
    """
    unwrapped = {}
    for key, value in euler_dict.items():
        # Try to unwrap adapters
        if hasattr(value, 'to_native'):
            unwrapped[key] = value.to_native()
        # Try to get internal data
        elif hasattr(value, '_data'):
            unwrapped[key] = value._data
        # For custom types that don't have unwrap methods, return as-is
        else:
            unwrapped[key] = value
    
    return unwrapped
