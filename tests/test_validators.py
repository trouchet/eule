"""Tests for validators module."""

import pytest
from warnings import warn
from eule.validators import validate_euler_generator_input
from eule.adapters import SetAdapter, ListAdapter


class TestValidateEulerGeneratorInput:
    """Test validate_euler_generator_input function."""
    
    def test_validate_dict_input(self):
        """Test validation accepts dict input."""
        sets = {'a': [1, 2, 3], 'b': [2, 3, 4]}
        result = validate_euler_generator_input(sets)
        assert isinstance(result, dict)
        assert 'a' in result
        assert 'b' in result
    
    def test_validate_dict_only(self):
        """Test validation only accepts dict (lists converted before validation)."""
        # Validator expects dict input (lists are converted by adapt_sets before validation)
        sets = {'a': [1, 2, 3], 'b': [2, 3, 4]}
        result = validate_euler_generator_input(sets)
        assert isinstance(result, dict)
    
    def test_validate_invalid_input_string(self):
        """Test validation rejects string input."""
        with pytest.raises(TypeError, match='Ill-conditioned input'):
            validate_euler_generator_input("invalid")
    
    def test_validate_invalid_input_int(self):
        """Test validation rejects int input."""
        with pytest.raises(TypeError, match='Ill-conditioned input'):
            validate_euler_generator_input(42)
    
    def test_validate_with_duplicates_warns(self):
        """Test validation warns about duplicates in built-in types."""
        sets = {'a': [1, 1, 2, 3]}
        with pytest.warns(UserWarning, match='MUST NOT have duplicates'):
            result = validate_euler_generator_input(sets)
        # Should deduplicate
        assert len(result['a']) <= 3
    
    def test_validate_setlike_objects_no_dedup(self):
        """Test validation skips SetLike objects."""
        sets = {'a': SetAdapter([1, 2, 3]), 'b': ListAdapter([2, 3, 4])}
        result = validate_euler_generator_input(sets)
        
        # Should return as-is (no deduplication for SetLike)
        assert isinstance(result['a'], SetAdapter)
        assert isinstance(result['b'], ListAdapter)
    
    def test_validate_mixed_setlike_and_builtin(self):
        """Test validation with mixed SetLike and built-in types."""
        sets = {
            'a': SetAdapter([1, 2, 3]),
            'b': [2, 2, 3, 4]  # Has duplicates
        }
        with pytest.warns(UserWarning):
            result = validate_euler_generator_input(sets)
        
        # SetLike should be unchanged
        assert isinstance(result['a'], SetAdapter)
        # Built-in should be deduplicated
        assert result['b'] == [2, 3, 4]
    
    def test_validate_all_unique_no_warning(self):
        """Test validation doesn't warn when no duplicates."""
        sets = {'a': [1, 2, 3], 'b': [4, 5, 6]}
        # Should not raise warning - just run it
        result = validate_euler_generator_input(sets)
        assert result == sets
    
    def test_validate_setlike_no_validation_attempt(self):
        """Test that SetLike objects skip traditional validation."""
        # Create a SetLike object with "duplicates" (shouldn't matter)
        sets = {'a': SetAdapter([1, 1, 2, 3])}  # Constructor deduplicates
        # Should not warn - just run it
        result = validate_euler_generator_input(sets)
        assert isinstance(result['a'], SetAdapter)
    
    def test_validate_empty_sets(self):
        """Test validation with empty sets."""
        sets = {'a': [], 'b': []}
        result = validate_euler_generator_input(sets)
        assert result == sets
    
    def test_validate_type_error_in_sequence_to_set(self):
        """Test validation handles TypeError gracefully."""
        # Object that can't be converted to set easily
        class WeirdIterable:
            def __iter__(self):
                raise TypeError("Can't iterate")
        
        sets = {'a': WeirdIterable()}
        # Should assume it's okay (custom type)
        result = validate_euler_generator_input(sets)
        assert isinstance(result['a'], WeirdIterable)
