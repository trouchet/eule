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
