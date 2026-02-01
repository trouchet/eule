"""Tests for the TypeRegistry."""

import pytest
from eule.registry import TypeRegistry, get_registry, register_adapter, register_detector
from eule.protocols import SetLike
from eule.adapters import SetAdapter, ListAdapter


class CustomSetLike:
    """A custom set-like class for testing."""
    
    def __init__(self, data):
        self._data = set(data)
    
    def union(self, other):
        return CustomSetLike(self._data | set(other))
    
    def intersection(self, other):
        return CustomSetLike(self._data & set(other))
    
    def difference(self, other):
        return CustomSetLike(self._data - set(other))
    
    def __bool__(self):
        return bool(self._data)
    
    def __iter__(self):
        return iter(self._data)
    
    @classmethod
    def from_iterable(cls, iterable):
        return cls(iterable)


class IncompleteSe:
    """A class that doesn't implement the full protocol."""
    
    def __init__(self, data):
        self._data = set(data)
    
    def union(self, other):
        return IncompleteSe(self._data | set(other))
    
    # Missing: intersection, difference, __bool__, __iter__


class TestTypeRegistry:
    """Test TypeRegistry functionality."""
    
    def test_init(self):
        """Test registry initialization."""
        registry = TypeRegistry()
        assert registry._type_adapters == {}
        assert registry._detection_rules == []
        assert registry._cache == {}
    
    def test_register_type(self):
        """Test registering a specific type."""
        registry = TypeRegistry()
        registry.register_type(CustomSetLike, lambda x: x)
        assert CustomSetLike in registry._type_adapters
    
    def test_register_detector(self):
        """Test registering a detector function."""
        registry = TypeRegistry()
        predicate = lambda obj: hasattr(obj, 'custom_method')
        adapter = lambda obj: SetAdapter(obj)
        registry.register_detector(predicate, adapter)
        assert len(registry._detection_rules) == 1
    
    def test_adapt_already_setlike(self):
        """Test adapting an object that's already SetLike."""
        registry = TypeRegistry()
        adapter = SetAdapter([1, 2, 3])
        result = registry.adapt(adapter)
        assert result is adapter  # Should return as-is
    
    def test_adapt_registered_type(self):
        """Test adapting a registered custom type."""
        registry = TypeRegistry()
        registry.register_type(CustomSetLike, lambda x: x)
        
        custom = CustomSetLike([1, 2, 3])
        result = registry.adapt(custom)
        assert result is custom
        assert isinstance(result, SetLike)
    
    def test_adapt_builtin_set(self):
        """Test adapting Python's built-in set."""
        registry = TypeRegistry()
        s = {1, 2, 3}
        result = registry.adapt(s)
        assert isinstance(result, SetAdapter)
        assert set(result) == {1, 2, 3}
    
    def test_adapt_builtin_list(self):
        """Test adapting Python's built-in list."""
        registry = TypeRegistry()
        l = [1, 2, 3]
        result = registry.adapt(l)
        assert isinstance(result, ListAdapter)
        assert list(result) == [1, 2, 3]
    
    def test_adapt_builtin_tuple(self):
        """Test adapting Python's built-in tuple."""
        registry = TypeRegistry()
        t = (1, 2, 3)
        result = registry.adapt(t)
        assert isinstance(result, ListAdapter)
        assert list(result) == [1, 2, 3]
    
    def test_adapt_duck_typing(self):
        """Test adapting object via duck-typing (has all protocol methods)."""
        registry = TypeRegistry()
        custom = CustomSetLike([1, 2, 3])
        result = registry.adapt(custom)
        # Should be recognized as already implementing protocol
        assert isinstance(result, SetLike)
    
    def test_adapt_with_detector(self):
        """Test adaptation using detection rule."""
        registry = TypeRegistry()
        
        class SpecialSet:
            special_marker = True
            
            def __init__(self, data):
                self._data = set(data)
            
            def union(self, other):
                return SpecialSet(self._data | set(other))
            
            def intersection(self, other):
                return SpecialSet(self._data & set(other))
            
            def difference(self, other):
                return SpecialSet(self._data - set(other))
            
            def __bool__(self):
                return bool(self._data)
            
            def __iter__(self):
                return iter(self._data)
            
            @classmethod
            def from_iterable(cls, iterable):
                return cls(iterable)
        
        registry.register_detector(
            lambda obj: hasattr(obj, 'special_marker'),
            lambda obj: obj  # Already implements protocol
        )
        
        special = SpecialSet([1, 2, 3])
        result = registry.adapt(special)
        assert result is special
    
    def test_adapt_iterable_fallback(self):
        """Test fallback to treating as iterable."""
        registry = TypeRegistry()
        # A simple iterable without set operations
        result = registry.adapt(range(5))
        assert isinstance(result, SetAdapter)
        assert set(result) == {0, 1, 2, 3, 4}
    
    def test_adapt_unsupported_type_raises(self):
        """Test that unsupported types raise TypeError."""
        registry = TypeRegistry()
        
        class UnsupportedType:
            pass
        
        with pytest.raises(TypeError) as exc_info:
            registry.adapt(UnsupportedType())
        
        assert "Cannot adapt" in str(exc_info.value)
        assert "UnsupportedType" in str(exc_info.value)
    
    def test_cache_functionality(self):
        """Test that adapter lookups are cached."""
        registry = TypeRegistry()
        call_count = {'value': 0}
        
        def counting_adapter(obj):
            call_count['value'] += 1
            return SetAdapter(obj)
        
        registry.register_type(list, counting_adapter)
        
        # First call
        l1 = [1, 2, 3]
        result1 = registry.adapt(l1)
        assert call_count['value'] == 1
        
        # Second call with same type
        l2 = [4, 5, 6]
        result2 = registry.adapt(l2)
        assert call_count['value'] == 2  # Cached adapter used
        
        # Cache should have list type
        assert list in registry._cache
    
    def test_clear_cache(self):
        """Test clearing the cache."""
        registry = TypeRegistry()
        registry.register_type(list, SetAdapter)
        registry.adapt([1, 2, 3])
        assert len(registry._cache) > 0
        
        registry.clear_cache()
        assert len(registry._cache) == 0
    
    def test_register_type_clears_cache(self):
        """Test that registering a type clears its cache entry."""
        registry = TypeRegistry()
        registry.register_type(list, SetAdapter)
        registry.adapt([1, 2, 3])
        assert list in registry._cache
        
        # Re-register
        registry.register_type(list, lambda x: ListAdapter(x))
        assert list not in registry._cache


class TestGlobalRegistry:
    """Test global registry functions."""
    
    def test_get_registry_returns_singleton(self):
        """Test that get_registry returns the same instance."""
        reg1 = get_registry()
        reg2 = get_registry()
        assert reg1 is reg2
    
    def test_register_adapter_global(self):
        """Test global register_adapter function."""
        # Clear any previous registrations
        registry = get_registry()
        registry.clear_cache()
        
        class TestType:
            def __init__(self, data):
                self._data = set(data)
            
            def union(self, other):
                return TestType(self._data | set(other))
            
            def intersection(self, other):
                return TestType(self._data & set(other))
            
            def difference(self, other):
                return TestType(self._data - set(other))
            
            def __bool__(self):
                return bool(self._data)
            
            def __iter__(self):
                return iter(self._data)
            
            @classmethod
            def from_iterable(cls, iterable):
                return cls(iterable)
        
        register_adapter(TestType, lambda x: x)
        
        test_obj = TestType([1, 2, 3])
        result = registry.adapt(test_obj)
        assert result is test_obj
    
    def test_register_detector_global(self):
        """Test global register_detector function."""
        registry = get_registry()
        
        initial_rules = len(registry._detection_rules)
        
        register_detector(
            lambda obj: hasattr(obj, 'test_marker'),
            lambda obj: SetAdapter(obj)
        )
        
        assert len(registry._detection_rules) == initial_rules + 1


class TestRegistryDetectionOrder:
    """Test the detection order priority."""
    
    def test_detection_order_already_setlike(self):
        """Already SetLike objects are returned as-is (highest priority)."""
        registry = TypeRegistry()
        adapter = SetAdapter([1, 2, 3])
        
        # Even if we register it, should return as-is
        registry.register_type(SetAdapter, lambda x: ListAdapter(x))
        result = registry.adapt(adapter)
        
        # Should not convert to ListAdapter
        assert isinstance(result, SetAdapter)
    
    def test_detection_order_registered_over_builtin(self):
        """Registered types take priority over built-in handling."""
        registry = TypeRegistry()
        
        # Register list to use SetAdapter instead of ListAdapter
        registry.register_type(list, SetAdapter)
        
        result = registry.adapt([1, 2, 3])
        assert isinstance(result, SetAdapter)
        assert not isinstance(result, ListAdapter)
    
    def test_detection_order_detector_over_builtin(self):
        """Detection rules take priority over built-in type handling."""
        registry = TypeRegistry()
        
        # Register detector for lists
        registry.register_detector(
            lambda obj: isinstance(obj, list),
            lambda obj: SetAdapter([x * 2 for x in obj])  # Custom transformation
        )
        
        result = registry.adapt([1, 2, 3])
        assert set(result) == {2, 4, 6}
    
    def test_detection_order_first_detector_wins(self):
        """First matching detector is used."""
        registry = TypeRegistry()
        
        registry.register_detector(
            lambda obj: isinstance(obj, list),
            lambda obj: SetAdapter([1])  # First detector
        )
        registry.register_detector(
            lambda obj: isinstance(obj, list),
            lambda obj: SetAdapter([2])  # Second detector (won't be used)
        )
        
        result = registry.adapt([5, 6, 7])
        assert set(result) == {1}  # First detector was used


class TestRegistryEdgeCases:
    """Test edge cases and error conditions."""
    
    def test_adapt_none_raises(self):
        """Test that adapting None raises TypeError."""
        registry = TypeRegistry()
        with pytest.raises(TypeError):
            registry.adapt(None)
    
    def test_adapt_int_raises(self):
        """Test that adapting non-iterable raises TypeError."""
        registry = TypeRegistry()
        with pytest.raises(TypeError):
            registry.adapt(42)
    
    def test_adapt_string_treated_as_iterable(self):
        """Test that strings are adapted as iterable of characters."""
        registry = TypeRegistry()
        result = registry.adapt("abc")
        assert isinstance(result, SetAdapter)
        assert set(result) == {'a', 'b', 'c'}
    
    def test_adapter_factory_exception_propagates(self):
        """Test that exceptions in adapter factories propagate."""
        registry = TypeRegistry()
        
        def failing_adapter(obj):
            raise ValueError("Intentional failure")
        
        registry.register_type(list, failing_adapter)
        
        with pytest.raises(ValueError) as exc_info:
            registry.adapt([1, 2, 3])
        
        assert "Intentional failure" in str(exc_info.value)


class TestRegistryMissingCoverage:
    """Tests for missing coverage in registry."""
    
    def test_adapt_list_to_list_adapter(self):
        """Test adapting list uses ListAdapter."""
        registry = TypeRegistry()
        result = registry.adapt([1, 2, 3])
        assert isinstance(result, ListAdapter)
    
    def test_adapt_tuple_to_list_adapter(self):
        """Test adapting tuple uses ListAdapter."""
        registry = TypeRegistry()
        result = registry.adapt((1, 2, 3))
        assert isinstance(result, ListAdapter)
    
    def test_protocol_isinstance_error_handling(self):
        """Test _is_setlike handles isinstance TypeErrors gracefully."""
        registry = TypeRegistry()
        
        # Create object that will cause isinstance to fail
        class BadProto:
            pass
        
        obj = BadProto()
        # This should not raise, should return False
        result = registry._is_setlike(obj)
        assert result == False

    def test_detector_before_builtin_list(self):
        """Test that detector rules run before built-in type checks."""
        registry = TypeRegistry()
        
        # Register detector for lists
        def custom_list_adapter(obj):
            return SetAdapter([x * 2 for x in obj])
        
        registry.register_detector(
            lambda obj: isinstance(obj, list),
            custom_list_adapter
        )
        
        # This should use the detector, not built-in list handling
        result = registry.adapt([1, 2, 3])
        assert set(result) == {2, 4, 6}
