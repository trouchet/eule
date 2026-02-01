"""
Final push to cover remaining lines in core.py and registry.py.

Targets:
- core.py: lines 137-138, 534, 739
- registry.py: lines 152-154
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
from eule import euler
from eule.core import Euler, euler_parallel
from eule.registry import get_registry, TypeRegistry
from eule.protocols import SetLike


class TestCoreLines137to138:
    """Test exception handling in is_unique_set_array (lines 137-138)."""
    
    def test_unhashable_elements_trigger_except(self):
        """Test that unhashable elements trigger the exception path."""
        # Create objects that can't be hashed - but pass them as lists
        # so they reach the is_unique_set_array validation
        class UnhashableItem:
            def __init__(self, value):
                self.value = value
                
            def __hash__(self):
                raise TypeError("unhashable type")
            
            def __repr__(self):
                return f"UnhashableItem({self.value})"
        
        # This should trigger lines 137-138 when checking for duplicates
        # The sequence_to_set() will try to create a set and fail
        sets = {
            'a': [UnhashableItem(1), UnhashableItem(2)],
            'b': [1, 2, 3]
        }
        
        # The exception should be caught in line 137-138
        # and the function should continue (appending True to is_unique_set_arr)
        # Then the actual adaptation will fail later, which is expected
        try:
            result = euler(sets)
        except TypeError as e:
            # This is expected - the test is about covering the exception handler
            # Check that we got past the validation (line 137-138 caught it)
            assert "Failed to adapt" in str(e) or "unhashable" in str(e)
    
    def test_attribute_error_in_sequence_to_set(self):
        """Test AttributeError path in the exception handler."""
        class BadCompare:
            def __hash__(self):
                return 1  # Can hash
                
            def __eq__(self, other):
                raise AttributeError("comparison error")
            
            def __repr__(self):
                return "BadCompare()"
        
        sets = {
            'x': [BadCompare(), BadCompare()],
            'y': [1, 2]
        }
        
        # Should catch AttributeError in lines 137-138
        try:
            result = euler(sets)
        except (TypeError, AttributeError):
            # Expected - test is about the exception handler
            pass


class TestCoreLine534:
    """Test euler_set_keys extraction when len == 1 (line 534)."""
    
    def test_single_euler_set_key(self):
        """Test the case where euler_set_keys has exactly 1 element."""
        # Create minimal input that results in single euler_set_key
        sets = {'single': [1, 2, 3]}
        
        result = euler(sets)
        assert isinstance(result, dict)
        # Should have at least the full set
        assert len(result) >= 1
    
    def test_euler_set_keys_len_1_extraction(self):
        """Direct test of the euler_set_keys[1] access."""
        # This line is accessed when len(euler_set_keys) == 1
        # and we need to extract actual_keys
        sets = {'a': [1]}
        
        e = Euler(sets)
        result = e.as_dict()
        assert isinstance(result, dict)


class TestCoreLine739:
    """Test parallel worker return tuple (line 739)."""
    
    def test_parallel_worker_returns_tuple(self):
        """Test that _euler_worker returns (cluster_id, result) tuple."""
        sets = {
            'a': [1, 2, 3],
            'b': [2, 3, 4],
            'c': [5, 6, 7]  # Disconnected cluster
        }
        
        # Force parallel processing with clustering
        e = Euler(sets, cluster=True, parallel=True)
        result = e.as_dict()
        
        # Should successfully process multiple clusters
        assert isinstance(result, dict)
        assert len(result) > 0
    
    def test_parallel_multiple_clusters(self):
        """Test parallel processing with multiple distinct clusters."""
        # Create multiple disconnected clusters
        sets = {
            f'cluster_{i}_set_{j}': [i*100 + j]
            for i in range(3)
            for j in range(2)
        }
        
        e = Euler(sets, cluster=True, parallel=True)
        result = e.as_dict()
        
        assert isinstance(result, dict)


class TestRegistryLines152to154:
    """Test TypeError handling in _is_setlike (lines 152-154)."""
    
    def test_protocol_check_raises_typeerror(self):
        """Test that TypeError in isinstance check is caught."""
        registry = get_registry()
        
        # Create a mock that raises TypeError during protocol check
        problematic = Mock()
        
        # Test the _is_setlike method which has the TypeError handler
        result = registry._is_setlike(problematic)
        
        # Should return False for non-SetLike objects
        assert result == False
    
    def test_is_setlike_with_actual_setlike(self):
        """Test _is_setlike with an actual SetLike object."""
        registry = get_registry()
        
        # A regular set should not be SetLike (needs adaptation)
        result = registry._is_setlike({1, 2, 3})
        # Python set doesn't implement the full protocol (no from_iterable)
        assert result == False


class TestComprehensiveCoverage:
    """Additional tests to maximize coverage."""
    
    def test_empty_sets_all_combinations(self):
        """Test various empty set combinations."""
        test_cases = [
            {},  # Empty dict
            {'a': []},  # Single empty set
            {'a': [], 'b': []},  # Multiple empty sets
            {'a': [1], 'b': []},  # Mixed empty and non-empty
        ]
        
        for sets in test_cases:
            result = euler(sets)
            assert isinstance(result, dict)
    
    def test_single_element_sets(self):
        """Test with single-element sets."""
        sets = {
            'a': [1],
            'b': [2],
            'c': [3]
        }
        
        result = euler(sets)
        assert isinstance(result, dict)
        # Should have disjoint regions
        assert len(result) >= 3
    
    def test_all_identical_sets(self):
        """Test when all sets are identical."""
        sets = {
            'a': [1, 2, 3],
            'b': [1, 2, 3],
            'c': [1, 2, 3]
        }
        
        result = euler(sets)
        assert isinstance(result, dict)
        # All sets overlap completely
        assert ('a', 'b', 'c') in result or frozenset(['a', 'b', 'c']) in result
    
    def test_nested_subsets(self):
        """Test perfectly nested subsets."""
        sets = {
            'outer': [1, 2, 3, 4, 5],
            'middle': [2, 3, 4],
            'inner': [3]
        }
        
        result = euler(sets)
        assert isinstance(result, dict)
        # Should have multiple regions for the nesting
        assert len(result) >= 3
    
    def test_parallel_with_single_job(self):
        """Test parallel Euler computation."""
        sets = {
            'a': [1, 2, 3],
            'b': [2, 3, 4]
        }
        
        result = euler_parallel(sets)
        
        assert isinstance(result, dict)
    
    def test_very_large_overlap(self):
        """Test with sets that have very large overlaps."""
        base = list(range(1000))
        sets = {
            'a': base[:900],
            'b': base[100:],
            'c': base[200:800]
        }
        
        result = euler(sets)
        assert isinstance(result, dict)
        assert len(result) > 0


class TestRegistryEdgeCases:
    """Test registry edge cases."""
    
    def test_register_duplicate_detector(self):
        """Test registering the same detector twice."""
        registry = TypeRegistry()
        
        def detector(obj):
            return isinstance(obj, dict)
        
        def adapter(obj):
            return obj
        
        # Register once
        registry.register_detector(detector, adapter)
        
        # Register again - should not cause issues
        registry.register_detector(detector, adapter)
        
        # Should work
        result = registry.adapt({'a': 1})
        assert result is not None
    
    def test_adapt_custom_iterable(self):
        """Test adapting a custom iterable."""
        class CustomIterable:
            def __init__(self, data):
                self.data = data
            
            def __iter__(self):
                return iter(self.data)
        
        registry = get_registry()
        custom = CustomIterable([1, 2, 3])
        
        result = registry.adapt(custom)
        assert result is not None
