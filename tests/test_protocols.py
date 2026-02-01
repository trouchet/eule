"""Tests for the SetLike protocol and adapters."""

import pytest
from eule.protocols import SetLike
from eule.adapters import SetAdapter, ListAdapter


class TestSetLikeProtocol:
    """Test that the SetLike protocol works correctly."""
    
    def test_protocol_instance_check_set_adapter(self):
        """SetAdapter should be recognized as SetLike."""
        adapter = SetAdapter([1, 2, 3])
        assert isinstance(adapter, SetLike)
    
    def test_protocol_instance_check_list_adapter(self):
        """ListAdapter should be recognized as SetLike."""
        adapter = ListAdapter([1, 2, 3])
        assert isinstance(adapter, SetLike)
    
    def test_custom_type_implements_protocol(self):
        """Custom type implementing protocol should be recognized."""
        class CustomSet:
            def __init__(self, data):
                self._data = set(data)
            
            def union(self, other):
                return CustomSet(self._data | set(other))
            
            def intersection(self, other):
                return CustomSet(self._data & set(other))
            
            def difference(self, other):
                return CustomSet(self._data - set(other))
            
            def __bool__(self):
                return bool(self._data)
            
            def __iter__(self):
                return iter(self._data)
            
            @classmethod
            def from_iterable(cls, iterable):
                return cls(iterable)
        
        custom = CustomSet([1, 2, 3])
        assert isinstance(custom, SetLike)


class TestSetAdapter:
    """Test SetAdapter implementation."""
    
    def test_init_empty(self):
        """Test creating an empty SetAdapter."""
        adapter = SetAdapter()
        assert not adapter
        assert len(adapter) == 0
        assert list(adapter) == []
    
    def test_init_with_elements(self):
        """Test creating SetAdapter with elements."""
        adapter = SetAdapter([1, 2, 3])
        assert adapter
        assert len(adapter) == 3
        assert set(adapter) == {1, 2, 3}
    
    def test_init_removes_duplicates(self):
        """Test that SetAdapter removes duplicates."""
        adapter = SetAdapter([1, 2, 2, 3, 3, 3])
        assert len(adapter) == 3
        assert set(adapter) == {1, 2, 3}
    
    def test_union(self):
        """Test union operation."""
        a = SetAdapter([1, 2, 3])
        b = SetAdapter([3, 4, 5])
        result = a.union(b)
        assert isinstance(result, SetAdapter)
        assert set(result) == {1, 2, 3, 4, 5}
    
    def test_union_with_non_adapter(self):
        """Test union with a non-adapter SetLike."""
        a = SetAdapter([1, 2, 3])
        b = ListAdapter([3, 4, 5])
        result = a.union(b)
        assert isinstance(result, SetAdapter)
        assert set(result) == {1, 2, 3, 4, 5}
    
    def test_intersection(self):
        """Test intersection operation."""
        a = SetAdapter([1, 2, 3, 4])
        b = SetAdapter([3, 4, 5, 6])
        result = a.intersection(b)
        assert isinstance(result, SetAdapter)
        assert set(result) == {3, 4}
    
    def test_intersection_empty(self):
        """Test intersection with no overlap."""
        a = SetAdapter([1, 2])
        b = SetAdapter([3, 4])
        result = a.intersection(b)
        assert not result
        assert set(result) == set()
    
    def test_difference(self):
        """Test difference operation."""
        a = SetAdapter([1, 2, 3, 4])
        b = SetAdapter([3, 4, 5])
        result = a.difference(b)
        assert isinstance(result, SetAdapter)
        assert set(result) == {1, 2}
    
    def test_difference_empty(self):
        """Test difference resulting in empty set."""
        a = SetAdapter([1, 2])
        b = SetAdapter([1, 2, 3])
        result = a.difference(b)
        assert not result
    
    def test_bool_empty(self):
        """Test __bool__ for empty set."""
        adapter = SetAdapter()
        assert not bool(adapter)
    
    def test_bool_non_empty(self):
        """Test __bool__ for non-empty set."""
        adapter = SetAdapter([1])
        assert bool(adapter)
    
    def test_iter(self):
        """Test iteration."""
        adapter = SetAdapter([1, 2, 3])
        items = list(adapter)
        assert set(items) == {1, 2, 3}
    
    def test_from_iterable(self):
        """Test from_iterable class method."""
        adapter = SetAdapter.from_iterable([1, 2, 3])
        assert isinstance(adapter, SetAdapter)
        assert set(adapter) == {1, 2, 3}
    
    def test_to_native(self):
        """Test conversion back to native set."""
        adapter = SetAdapter([1, 2, 3])
        native = adapter.to_native()
        assert isinstance(native, set)
        assert native == {1, 2, 3}
    
    def test_equality(self):
        """Test equality comparison."""
        a = SetAdapter([1, 2, 3])
        b = SetAdapter([1, 2, 3])
        c = SetAdapter([1, 2, 4])
        assert a == b
        assert a != c
        # Test with non-SetAdapter
        assert a != [1, 2, 3]
        assert a != "not a set"
    
    def test_repr(self):
        """Test string representation."""
        adapter = SetAdapter([1, 2, 3])
        assert 'SetAdapter' in repr(adapter)


class TestListAdapter:
    """Test ListAdapter implementation."""
    
    def test_init_empty(self):
        """Test creating an empty ListAdapter."""
        adapter = ListAdapter()
        assert not adapter
        assert len(adapter) == 0
        assert list(adapter) == []
    
    def test_init_with_elements(self):
        """Test creating ListAdapter with elements."""
        adapter = ListAdapter([1, 2, 3])
        assert adapter
        assert len(adapter) == 3
        assert list(adapter) == [1, 2, 3]
    
    def test_init_preserves_order(self):
        """Test that ListAdapter preserves insertion order."""
        adapter = ListAdapter([3, 1, 2])
        assert list(adapter) == [3, 1, 2]
    
    def test_init_removes_duplicates(self):
        """Test that ListAdapter removes duplicates while preserving order."""
        adapter = ListAdapter([1, 2, 2, 3, 1, 4])
        assert list(adapter) == [1, 2, 3, 4]
    
    def test_union_preserves_order(self):
        """Test union preserves order and removes duplicates."""
        a = ListAdapter([1, 2, 3])
        b = ListAdapter([3, 4, 5])
        result = a.union(b)
        assert isinstance(result, ListAdapter)
        # Should be [1, 2, 3, 4, 5] - preserving order, removing duplicate 3
        assert list(result) == [1, 2, 3, 4, 5]
    
    def test_intersection_preserves_order_from_first(self):
        """Test intersection preserves order from first operand."""
        a = ListAdapter([1, 2, 3, 4])
        b = ListAdapter([4, 3, 2])  # Different order
        result = a.intersection(b)
        assert isinstance(result, ListAdapter)
        # Should follow order of 'a'
        assert list(result) == [2, 3, 4]
    
    def test_intersection_empty(self):
        """Test intersection with no overlap."""
        a = ListAdapter([1, 2])
        b = ListAdapter([3, 4])
        result = a.intersection(b)
        assert not result
        assert list(result) == []
    
    def test_difference_preserves_order(self):
        """Test difference preserves order from first operand."""
        a = ListAdapter([1, 2, 3, 4, 5])
        b = ListAdapter([3, 4])
        result = a.difference(b)
        assert isinstance(result, ListAdapter)
        assert list(result) == [1, 2, 5]
    
    def test_difference_empty(self):
        """Test difference resulting in empty."""
        a = ListAdapter([1, 2])
        b = ListAdapter([1, 2, 3])
        result = a.difference(b)
        assert not result
    
    def test_bool_empty(self):
        """Test __bool__ for empty list."""
        adapter = ListAdapter()
        assert not bool(adapter)
    
    def test_bool_non_empty(self):
        """Test __bool__ for non-empty list."""
        adapter = ListAdapter([1])
        assert bool(adapter)
    
    def test_iter(self):
        """Test iteration."""
        adapter = ListAdapter([1, 2, 3])
        items = list(adapter)
        assert items == [1, 2, 3]
    
    def test_from_iterable(self):
        """Test from_iterable class method."""
        adapter = ListAdapter.from_iterable([1, 2, 3])
        assert isinstance(adapter, ListAdapter)
        assert list(adapter) == [1, 2, 3]
    
    def test_to_native(self):
        """Test conversion back to native list."""
        adapter = ListAdapter([1, 2, 3])
        native = adapter.to_native()
        assert isinstance(native, list)
        assert native == [1, 2, 3]
    
    def test_equality(self):
        """Test equality comparison."""
        a = ListAdapter([1, 2, 3])
        b = ListAdapter([1, 2, 3])
        c = ListAdapter([1, 2, 4])
        d = ListAdapter([3, 2, 1])  # Different order
        assert a == b
        assert a != c
        assert a != d  # Order matters
        # Test with non-ListAdapter
        assert a != [1, 2, 3]
        assert a != "not a list"
    
    def test_repr(self):
        """Test string representation."""
        adapter = ListAdapter([1, 2, 3])
        assert 'ListAdapter' in repr(adapter)


class TestAdapterInteroperability:
    """Test that different adapters can work together."""
    
    def test_set_union_list(self):
        """SetAdapter can union with ListAdapter."""
        s = SetAdapter([1, 2, 3])
        l = ListAdapter([3, 4, 5])
        result = s.union(l)
        assert isinstance(result, SetAdapter)
        assert set(result) == {1, 2, 3, 4, 5}
    
    def test_list_union_set(self):
        """ListAdapter can union with SetAdapter."""
        l = ListAdapter([1, 2, 3])
        s = SetAdapter([3, 4, 5])
        result = l.union(s)
        assert isinstance(result, ListAdapter)
        # Result type matches first operand
        assert set(result) == {1, 2, 3, 4, 5}
    
    def test_set_intersection_list(self):
        """SetAdapter can intersect with ListAdapter."""
        s = SetAdapter([1, 2, 3, 4])
        l = ListAdapter([3, 4, 5])
        result = s.intersection(l)
        assert set(result) == {3, 4}
    
    def test_set_difference_list(self):
        """SetAdapter can difference with ListAdapter."""
        s = SetAdapter([1, 2, 3, 4])
        l = ListAdapter([3, 4])
        result = s.difference(l)
        assert set(result) == {1, 2}
