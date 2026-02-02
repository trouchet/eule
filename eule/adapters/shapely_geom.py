"""
Adapter for integration between eule and Shapely geometries (Polygons).
Allows arbitrary 2D shapes to be used in Euler diagrams.
"""

from typing import TYPE_CHECKING, Any, Iterator, Union, List

if TYPE_CHECKING:
    try:
        from shapely.geometry.base import BaseGeometry
        from shapely.geometry import Polygon, MultiPolygon
    except ImportError:
        BaseGeometry = Any
        Polygon = Any
        MultiPolygon = Any

class ShapelyAdapter:
    """
    Adapter to make Shapely geometries compatible with eule's SetLike protocol.
    """
    
    def __init__(self, geom: 'BaseGeometry'):
        """Wrap a Shapely geometry."""
        self._geom = geom
        # clean up any invalid topology immediately
        if not self._geom.is_valid:
            self._geom = self._geom.buffer(0)

    def union(self, other: 'ShapelyAdapter') -> 'ShapelyAdapter':
        """Return the union (A ∪ B)."""
        res = self._geom.union(other._geom)
        return ShapelyAdapter(res)
    
    def intersection(self, other: 'ShapelyAdapter') -> 'ShapelyAdapter':
        """Return the intersection (A ∩ B)."""
        res = self._geom.intersection(other._geom)
        return ShapelyAdapter(res)
    
    def difference(self, other: 'ShapelyAdapter') -> 'ShapelyAdapter':
        """Return the difference (A - B)."""
        res = self._geom.difference(other._geom)
        
        # Clean artifacts: remove tiny fragments
        if not res.is_empty and res.area < 1e-9:
            from shapely.geometry import Polygon
            res = Polygon() # Empty
            
        return ShapelyAdapter(res)
    
    def __bool__(self) -> bool:
        """Return True if geometry is not empty."""
        return not self._geom.is_empty
    
    def __iter__(self) -> Iterator['BaseGeometry']:
        """
        Iterate over disjoint components.
        If geometry is a MultiPolygon, yield individual Polygons.
        If Polygon, yield self (as single geometries).
        """
        from shapely.geometry import MultiPolygon, GeometryCollection
        
        if isinstance(self._geom, MultiPolygon):
            return iter(self._geom.geoms)
        elif isinstance(self._geom, GeometryCollection):
             return iter(self._geom.geoms)
        else:
            yield self._geom
            
    def __repr__(self) -> str:
        return f"ShapelyAdapter({self._geom.geom_type}, area={self._geom.area:.2f})"
        
    @property
    def geometry(self):
        return self._geom

def register_shapely():
    """Register Shapely geometries with eule's type registry."""
    try:
        from shapely.geometry.base import BaseGeometry
        from ..registry import get_registry
        
        registry = get_registry()
        
        def is_shapely_geom(obj):
            return isinstance(obj, BaseGeometry)
        
        def adapt_shapely(obj):
            return ShapelyAdapter(obj)
        
        registry.register_detector(is_shapely_geom, adapt_shapely)
        return True
        
    except ImportError:
        return False

# Auto-register
register_shapely()
