from eule.operations import difference, union, intersection
from .fixtures import arrA, arrB, arrAmB, arrApB, arrAiB

def test_difference():
    """
    tests subtract elements of a list from the other
    """
    assert difference(arrA, arrB) == arrAmB

def test_union():
    """
    tests unite two list with non-repeated elements
    """
    assert union(arrA, arrB) == arrApB

def test_intersection():
    """
    tests intersection elements of a list from the other
    """
    assert intersection(arrA, arrB) == arrAiB