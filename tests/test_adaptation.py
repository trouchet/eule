"""Tests for adaptation module."""

import pytest
from eule.adaptation import adapt_sets, unwrap_result
from eule.adapters import SetAdapter, ListAdapter
from eule.protocols import SetLike


class TestAdaptSets:
    """Test adapt_sets function."""
    
    def test_adapt_dict_with_lists(self):
        """Test adapting dict with list values."""
        sets = {'a': [1, 2, 3], 'b': [2, 3, 4]}
        result = adapt_sets(sets)
        
        assert 'a' in result
        assert 'b' in result
        assert isinstance(result['a'], ListAdapter)
        assert isinstance(result['b'], ListAdapter)
    
    def test_adapt_dict_with_sets(self):
        """Test adapting dict with set values."""
        sets = {'a': {1, 2, 3}, 'b': {2, 3, 4}}
        result = adapt_sets(sets)
        
        assert isinstance(result['a'], SetAdapter)
        assert isinstance(result['b'], SetAdapter)
    
    def test_adapt_list_input(self):
        """Test adapting list input (converts to dict)."""
        sets = [[1, 2, 3], [2, 3, 4]]
        result = adapt_sets(sets)
        
        assert isinstance(result, dict)
        assert 0 in result
        assert 1 in result
        assert isinstance(result[0], ListAdapter)
    
    def test_adapt_invalid_input_string(self):
        """Test that string input raises TypeError."""
        with pytest.raises(TypeError, match='Ill-conditioned input'):
            adapt_sets("invalid")
    
    def test_adapt_invalid_input_int(self):
        """Test that int input raises TypeError."""
        with pytest.raises(TypeError, match='Ill-conditioned input'):
            adapt_sets(42)
    
    def test_adapt_invalid_set_value(self):
        """Test that invalid set value raises TypeError."""
        class UnsupportedType:
            pass
        
        with pytest.raises(TypeError, match="Failed to adapt set 'a'"):
            adapt_sets({'a': UnsupportedType()})
    
    def test_adapt_mixed_types(self):
        """Test adapting dict with mixed types."""
        sets = {'a': [1, 2, 3], 'b': {2, 3, 4}, 'c': (3, 4, 5)}
        result = adapt_sets(sets)
        
        assert isinstance(result['a'], ListAdapter)
        assert isinstance(result['b'], SetAdapter)
        assert isinstance(result['c'], ListAdapter)
    
    def test_adapt_already_adapted(self):
        """Test adapting already adapted sets."""
        sets = {'a': SetAdapter([1, 2, 3])}
        result = adapt_sets(sets)
        
        # Should return as-is
        assert isinstance(result['a'], SetAdapter)
    
    def test_adapt_deep_copy(self):
        """Test that adapt_sets doesn't modify original."""
        original = {'a': [1, 2, 3]}
        result = adapt_sets(original)
        
        # Original should be unchanged
        assert isinstance(original['a'], list)
        assert isinstance(result['a'], ListAdapter)


class TestUnwrapResult:
    """Test unwrap_result function."""
    
    def test_unwrap_with_to_native(self):
        """Test unwrapping adapters with to_native method."""
        adapted = {
            ('a',): SetAdapter([1, 2, 3]),
            ('b',): ListAdapter([2, 3, 4])
        }
        result = unwrap_result(adapted)
        
        assert isinstance(result[('a',)], set)
        assert isinstance(result[('b',)], list)
        assert result[('a',)] == {1, 2, 3}
        assert result[('b',)] == [2, 3, 4]
    
    def test_unwrap_with_data_attribute(self):
        """Test unwrapping objects with _data attribute."""
        class WithDataAttr:
            def __init__(self, data):
                self._data = data
        
        adapted = {('a',): WithDataAttr([1, 2, 3])}
        result = unwrap_result(adapted)
        
        assert result[('a',)] == [1, 2, 3]
    
    def test_unwrap_without_unwrap_methods(self):
        """Test unwrapping objects without unwrap methods (return as-is)."""
        class CustomType:
            def __init__(self, data):
                self.data = data
        
        obj = CustomType([1, 2, 3])
        adapted = {('a',): obj}
        result = unwrap_result(adapted)
        
        # Should return as-is
        assert result[('a',)] is obj
    
    def test_unwrap_empty_dict(self):
        """Test unwrapping empty dict."""
        result = unwrap_result({})
        assert result == {}
    
    def test_unwrap_mixed_types(self):
        """Test unwrapping mixed adapter types."""
        class NoUnwrap:
            pass
        
        adapted = {
            ('a',): SetAdapter([1, 2, 3]),
            ('b',): ListAdapter([4, 5]),
            ('c',): NoUnwrap()
        }
        result = unwrap_result(adapted)
        
        assert isinstance(result[('a',)], set)
        assert isinstance(result[('b',)], list)
        assert isinstance(result[('c',)], NoUnwrap)


class TestAdaptationIntegration:
    """Integration tests for adaptation layer."""
    
    def test_adapt_and_unwrap_roundtrip(self):
        """Test adapt -> unwrap roundtrip."""
        original = {'a': [1, 2, 3], 'b': {2, 3, 4}}
        
        adapted = adapt_sets(original)
        result_dict = {k: v for k, v in adapted.items()}
        unwrapped = unwrap_result(result_dict)
        
        assert isinstance(unwrapped['a'], list)
        assert isinstance(unwrapped['b'], set)
        assert set(unwrapped['a']) == {1, 2, 3}
        assert unwrapped['b'] == {2, 3, 4}
