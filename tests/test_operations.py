from eule.operations import difference
from eule.operations import intersection
from eule.operations import union


def test_difference(arrA, arrB, arrAmB):
    """
    tests subtract elements of a list from the other
    """
    assert difference(arrA, arrB) == arrAmB

def test_union(arrA, arrB, arrApB):
    """
    tests unite two list with non-repeated elements
    """
    assert union(arrA, arrB) == arrApB

def test_intersection(arrA, arrB, arrAiB):
    """
    tests intersection elements of a list from the other
    """
    assert intersection(arrA, arrB) == arrAiB


def test_union_with_setlike():
    """Test union with SetLike objects using protocol methods."""
    from eule.adapters import SetAdapter
    a = SetAdapter([1, 2, 3])
    b = SetAdapter([3, 4, 5])
    result = union(a, b)
    
    assert isinstance(result, SetAdapter)
    assert set(result) == {1, 2, 3, 4, 5}


def test_intersection_with_setlike():
    """Test intersection with SetLike objects using protocol methods."""
    from eule.adapters import SetAdapter
    a = SetAdapter([1, 2, 3, 4])
    b = SetAdapter([3, 4, 5])
    result = intersection(a, b)
    
    assert isinstance(result, SetAdapter)
    assert set(result) == {3, 4}


def test_difference_with_setlike():
    """Test difference with SetLike objects using protocol methods."""
    from eule.adapters import SetAdapter
    a = SetAdapter([1, 2, 3, 4])
    b = SetAdapter([3, 4])
    result = difference(a, b)
    
    assert isinstance(result, SetAdapter)
    assert set(result) == {1, 2}
