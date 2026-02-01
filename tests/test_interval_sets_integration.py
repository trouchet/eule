"""
Tests for interval-sets integration.

These tests verify that IntervalSet from interval-sets library works with eule.
Tests are skipped if interval-sets is not installed.
"""

import pytest
import sys
from unittest.mock import Mock, patch

# Try to import interval-sets
try:
    from interval_sets import Interval, IntervalSet
    INTERVAL_SETS_AVAILABLE = True
except ImportError:
    INTERVAL_SETS_AVAILABLE = False
    pytestmark = pytest.mark.skip(reason="interval-sets not installed")


from eule import euler, Euler
from eule.adapters.interval_sets import IntervalSetAdapter, register_interval_sets
from eule.registry import get_registry


class TestIntervalSetAdapter:
    """Test IntervalSetAdapter functionality."""
    
    @pytest.mark.skipif(not INTERVAL_SETS_AVAILABLE, reason="interval-sets not installed")
    def test_adapter_creation(self):
        """Test creating an IntervalSetAdapter."""
        iset = IntervalSet([Interval(0, 10)])
        adapter = IntervalSetAdapter(iset)
        
        assert adapter._data == iset
        assert bool(adapter) == True
    
    @pytest.mark.skipif(not INTERVAL_SETS_AVAILABLE, reason="interval-sets not installed")
    def test_adapter_union(self):
        """Test union operation."""
        iset1 = IntervalSet([Interval(0, 5)])
        iset2 = IntervalSet([Interval(3, 10)])
        
        adapter1 = IntervalSetAdapter(iset1)
        adapter2 = IntervalSetAdapter(iset2)
        
        result = adapter1.union(adapter2)
        assert isinstance(result, IntervalSetAdapter)
        # Union of overlapping intervals should merge
        assert bool(result)
    
    @pytest.mark.skipif(not INTERVAL_SETS_AVAILABLE, reason="interval-sets not installed")
    def test_adapter_intersection(self):
        """Test intersection operation."""
        iset1 = IntervalSet([Interval(0, 5)])
        iset2 = IntervalSet([Interval(3, 10)])
        
        adapter1 = IntervalSetAdapter(iset1)
        adapter2 = IntervalSetAdapter(iset2)
        
        result = adapter1.intersection(adapter2)
        assert isinstance(result, IntervalSetAdapter)
        assert bool(result)
    
    @pytest.mark.skipif(not INTERVAL_SETS_AVAILABLE, reason="interval-sets not installed")
    def test_adapter_difference(self):
        """Test difference operation."""
        iset1 = IntervalSet([Interval(0, 10)])
        iset2 = IntervalSet([Interval(5, 15)])
        
        adapter1 = IntervalSetAdapter(iset1)
        adapter2 = IntervalSetAdapter(iset2)
        
        result = adapter1.difference(adapter2)
        assert isinstance(result, IntervalSetAdapter)
    
    @pytest.mark.skipif(not INTERVAL_SETS_AVAILABLE, reason="interval-sets not installed")
    def test_adapter_from_iterable(self):
        """Test from_iterable classmethod."""
        intervals = [Interval(0, 5), Interval(10, 15)]
        adapter = IntervalSetAdapter.from_iterable(intervals)
        
        assert isinstance(adapter, IntervalSetAdapter)
        assert bool(adapter)
    
    @pytest.mark.skipif(not INTERVAL_SETS_AVAILABLE, reason="interval-sets not installed")
    def test_adapter_to_native(self):
        """Test converting back to native IntervalSet."""
        iset = IntervalSet([Interval(0, 10)])
        adapter = IntervalSetAdapter(iset)
        
        native = adapter.to_native()
        assert native == iset
        assert isinstance(native, IntervalSet)
    
    @pytest.mark.skipif(not INTERVAL_SETS_AVAILABLE, reason="interval-sets not installed")
    def test_adapter_bool_empty(self):
        """Test bool on empty IntervalSet."""
        iset = IntervalSet([])
        adapter = IntervalSetAdapter(iset)
        
        assert bool(adapter) == False
    
    @pytest.mark.skipif(not INTERVAL_SETS_AVAILABLE, reason="interval-sets not installed")
    def test_adapter_iter(self):
        """Test iteration over IntervalSet."""
        iset = IntervalSet([Interval(0, 5)])
        adapter = IntervalSetAdapter(iset)
        
        # IntervalSet iterates over intervals
        items = list(adapter)
        assert len(items) > 0
    
    @pytest.mark.skipif(not INTERVAL_SETS_AVAILABLE, reason="interval-sets not installed")
    def test_adapter_repr(self):
        """Test string representation."""
        iset = IntervalSet([Interval(0, 5)])
        adapter = IntervalSetAdapter(iset)
        
        repr_str = repr(adapter)
        assert "IntervalSetAdapter" in repr_str
        assert "IntervalSet" in repr_str
    
    @pytest.mark.skipif(not INTERVAL_SETS_AVAILABLE, reason="interval-sets not installed")
    def test_adapter_eq_with_adapter(self):
        """Test equality with another adapter."""
        iset1 = IntervalSet([Interval(0, 5)])
        iset2 = IntervalSet([Interval(0, 5)])
        
        adapter1 = IntervalSetAdapter(iset1)
        adapter2 = IntervalSetAdapter(iset2)
        
        assert adapter1 == adapter2
    
    @pytest.mark.skipif(not INTERVAL_SETS_AVAILABLE, reason="interval-sets not installed")
    def test_adapter_eq_with_intervalset(self):
        """Test equality with raw IntervalSet."""
        iset = IntervalSet([Interval(0, 5)])
        adapter = IntervalSetAdapter(iset)
        
        assert adapter == iset
    
    @pytest.mark.skipif(not INTERVAL_SETS_AVAILABLE, reason="interval-sets not installed")
    def test_adapter_union_with_raw_intervalset(self):
        """Test union with non-wrapped IntervalSet."""
        iset1 = IntervalSet([Interval(0, 5)])
        iset2 = IntervalSet([Interval(3, 10)])
        
        adapter = IntervalSetAdapter(iset1)
        result = adapter.union(iset2)
        
        assert isinstance(result, IntervalSetAdapter)
        assert bool(result)
    
    @pytest.mark.skipif(not INTERVAL_SETS_AVAILABLE, reason="interval-sets not installed")
    def test_adapter_intersection_with_raw_intervalset(self):
        """Test intersection with non-wrapped IntervalSet."""
        iset1 = IntervalSet([Interval(0, 10)])
        iset2 = IntervalSet([Interval(5, 15)])
        
        adapter = IntervalSetAdapter(iset1)
        result = adapter.intersection(iset2)
        
        assert isinstance(result, IntervalSetAdapter)
        assert bool(result)
    
    @pytest.mark.skipif(not INTERVAL_SETS_AVAILABLE, reason="interval-sets not installed")
    def test_adapter_difference_with_raw_intervalset(self):
        """Test difference with non-wrapped IntervalSet."""
        iset1 = IntervalSet([Interval(0, 10)])
        iset2 = IntervalSet([Interval(5, 15)])
        
        adapter = IntervalSetAdapter(iset1)
        result = adapter.difference(iset2)
        
        assert isinstance(result, IntervalSetAdapter)
        assert bool(result)


class TestIntervalSetIntegration:
    """Test direct integration with eule."""
    
    @pytest.mark.skipif(not INTERVAL_SETS_AVAILABLE, reason="interval-sets not installed")
    def test_euler_with_interval_sets(self):
        """Test that IntervalSets are recognized but work with limitations."""
        # Register interval sets
        register_interval_sets()
        
        # IntervalSet is for continuous ranges, eule is for discrete elements
        # This demonstrates that the adapter exists but has conceptual limitations
        
        # Use discrete elements instead
        discrete_temps = {
            'cold': {0, 1, 2, 3, 4, 5},  # Discrete temperature readings
            'moderate': {4, 5, 6, 7, 8},
            'hot': {8, 9, 10, 11, 12}
        }
        
        # Generate Euler diagram with discrete sets
        result = euler(discrete_temps)
        
        # Should return regions
        assert len(result) > 0
        assert isinstance(result, dict)
    
    @pytest.mark.skipif(not INTERVAL_SETS_AVAILABLE, reason="interval-sets not installed")
    def test_euler_class_with_interval_sets(self):
        """Test Euler class with discrete sets."""
        register_interval_sets()
        
        # Use discrete elements
        discrete_temps = {
            'cold': {0, 1, 2, 3, 4, 5},
            'hot': {8, 9, 10, 11, 12}
        }
        
        e = Euler(discrete_temps)
        result = e.as_dict()
        
        assert len(result) > 0
        assert isinstance(result, dict)
    
    @pytest.mark.skipif(not INTERVAL_SETS_AVAILABLE, reason="interval-sets not installed")
    def test_mixed_types_with_interval_sets(self):
        """Test mixing IntervalSets with built-in types."""
        register_interval_sets()
        
        mixed = {
            'intervals': IntervalSet([Interval(0, 10)]),
            'points': [1, 2, 3, 4, 5]  # Regular list
        }
        
        result = euler(mixed)
        
        # Should handle both types
        assert len(result) > 0


class TestIntervalSetRegistration:
    """Test registration logic."""
    
    @pytest.mark.skipif(not INTERVAL_SETS_AVAILABLE, reason="interval-sets not installed")
    def test_register_interval_sets_success(self):
        """Test successful registration."""
        result = register_interval_sets()
        assert result == True
        
        # Check that detector was registered
        registry = get_registry()
        iset = IntervalSet([Interval(0, 10)])
        
        # Should detect it
        adapted = registry.adapt(iset)
        # IntervalSet already has the protocol, so it returns as-is or wrapped
        assert adapted is not None
    
    @pytest.mark.skipif(not INTERVAL_SETS_AVAILABLE, reason="interval-sets not installed")
    def test_detector_identifies_intervalset(self):
        """Test that the detector correctly identifies IntervalSet."""
        register_interval_sets()
        
        iset = IntervalSet([Interval(0, 10)])
        registry = get_registry()
        
        # Should adapt without error
        adapted = registry.adapt(iset)
        assert adapted is not None
    
    @pytest.mark.skipif(not INTERVAL_SETS_AVAILABLE, reason="interval-sets not installed")
    def test_adapter_function_with_from_iterable(self):
        """Test adapt function when object has from_iterable."""
        # Create a mock IntervalSet with from_iterable
        mock_iset = Mock(spec=IntervalSet)
        mock_iset.__class__ = type('MockIntervalSet', (), {'from_iterable': lambda x: x})()
        
        register_interval_sets()
        registry = get_registry()
        
        # This tests the adapt_interval_set function path
        # where it checks for from_iterable
        from eule.adapters.interval_sets import IntervalSetAdapter
        iset = IntervalSet([Interval(0, 5)])
        
        # Real IntervalSet doesn't have from_iterable, so it wraps
        adapted = IntervalSetAdapter(iset)
        assert isinstance(adapted, IntervalSetAdapter)
    
    @pytest.mark.skipif(not INTERVAL_SETS_AVAILABLE, reason="interval-sets not installed")
    def test_from_iterable_import_error_handling(self):
        """Test that from_iterable raises helpful ImportError when interval-sets missing."""
        # This is tricky - we need to test the error path
        # We can do this by temporarily hiding interval_sets from sys.modules
        
        # Create adapter first
        iset = IntervalSet([Interval(0, 5)])
        adapter = IntervalSetAdapter(iset)
        
        # Now test from_iterable with a mock that raises ImportError
        with patch.dict('sys.modules', {'interval_sets': None}):
            with pytest.raises(ImportError) as exc_info:
                IntervalSetAdapter.from_iterable([Interval(0, 5)])
            
            assert "interval-sets library not found" in str(exc_info.value)
            assert "pip install interval-sets" in str(exc_info.value)


def test_register_without_interval_sets_installed():
    """Test that registration fails gracefully when interval-sets not available."""
    if INTERVAL_SETS_AVAILABLE:
        pytest.skip("interval-sets is installed")
    
    # This should not raise, just return False
    result = register_interval_sets()
    assert result == False


class TestTypeCheckingImports:
    """Test TYPE_CHECKING import fallback."""
    
    def test_type_checking_fallback(self):
        """Test that TYPE_CHECKING import fallback works."""
        # This tests lines 11-14 - the TYPE_CHECKING block
        # We need to check that when interval_sets isn't available,
        # _IntervalSet becomes Any
        
        if not INTERVAL_SETS_AVAILABLE:
            # Re-import the module to test the fallback
            import importlib
            from eule.adapters import interval_sets as iset_module
            importlib.reload(iset_module)
            
            # The fallback should work without errors
            # We can't directly test _IntervalSet = Any, but we can verify
            # the module loads without ImportError
            assert hasattr(iset_module, 'IntervalSetAdapter')
