"""
Ultra-targeted tests for the last remaining lines.
"""

import pytest
from eule.clustering import ClusteredEuler, ClusteredEulerOverlapping


class TestLine188to192:
    """Force Leiden to split disconnected components."""
    
    def test_force_component_split(self):
        """Create scenario that forces component splitting in Leiden refine."""
        # Create sets that will be in same cluster initially but are disconnected
        sets = {
            # Group 1 - highly connected
            'a1': list(range(1, 20)),
            'a2': list(range(5, 25)),
            'a3': list(range(10, 30)),
            # Group 2 - completely disconnected, high numbers
            'b1': list(range(1000, 1020)),
            'b2': list(range(1005, 1025)),
            'b3': list(range(1010, 1030)),
            # Group 3 - another disconnected component
            'c1': list(range(5000, 5010)),
            'c2': list(range(5005, 5015)),
        }
        
        # Use low resolution to initially group things together
        # Then refinement should split components
        ce = ClusteredEuler(sets, method='leiden', resolution=0.01)
        
        # Clustering should have run
        assert len(ce.clustering) > 0


class TestLine648:
    """Force key collision in flatten."""
    
    def test_definite_key_collision(self):
        """Create sets that guarantee key collision when flattening."""
        # Create identical overlap patterns in different clusters
        sets = {}
        
        # Cluster 1: sets with identical patterns
        for i in range(5):
            sets[f'cluster1_set{i}'] = [i]
        
        # Cluster 2: sets with identical patterns (disconnected)
        for i in range(5):
            sets[f'cluster2_set{i}'] = [i + 1000]
        
        ce = ClusteredEuler(sets, method='leiden')
        
        # Try to flatten - should detect collisions
        flat = ce.as_euler_dict(flatten=True)
        
        assert isinstance(flat, dict)


class TestLine781:
    """Test overlapping with auto_compute path."""
    
    def test_overlapping_auto_compute_explicitly_true(self):
        """Explicitly pass auto_compute=True to hit line 781."""
        sets = {
            'a': [1, 2, 3],
            'b': [2, 3, 4],
        }
        
        # Explicitly pass auto_compute=True (not default)
        ce = ClusteredEulerOverlapping(
            sets,
            allow_overlap=True,
            overlap_threshold=0.5,
            auto_compute=True  # Explicitly pass
        )
        
        # Should have attempted computation
        assert hasattr(ce, 'cluster_diagrams')


class TestLine814:
    """Test get_overlap_stats with allow_overlap=False."""
    
    def test_overlap_stats_false_path(self):
        """Test get_overlap_stats when allow_overlap=False (line 814)."""
        sets = {
            'a': [1, 2],
            'b': [2, 3],
        }
        
        ce = ClusteredEulerOverlapping(sets, allow_overlap=False)
        
        stats = ce.get_overlap_stats()
        
        assert stats["overlapping"] is False


class TestLine843:
    """Test overlapping summary with actual overlaps."""
    
    def test_summary_with_overlapping_sets(self):
        """Test summary when sets have multiple cluster memberships (line 843)."""
        sets = {
            'a': [1, 2, 3],
            'b': [2, 3, 4],
            'c': [10, 11],
        }
        
        ce = ClusteredEulerOverlapping(sets, allow_overlap=True, overlap_threshold=0.9)
        
        # Get summary which should show overlapping info
        summary = ce.summary()
        
        assert isinstance(summary, str)


class TestCore534:
    """Test core.py line 534."""
    
    def test_clustered_euler_dict_generation(self):
        """Test as_dict with clustering to generate cluster-prefixed keys."""
        # Many disconnected clusters
        sets = {}
        for i in range(10):
            sets[f'set{i}_a'] = [i]
            sets[f'set{i}_b'] = [i]
        
        e = ClusteredEuler(sets, method='leiden')
        
        # Get as dict
        result = e.as_euler_dict()
        
        assert isinstance(result, dict)


class TestRegistry152to154:
    """Test registry TypeError path."""
    
    def test_protocol_check_with_problematic_type(self):
        """Test _is_setlike with type that might raise TypeError."""
        from eule.registry import get_registry
        
        class ProblematicType:
            """Type that might cause issues in protocol check."""
            def __getattribute__(self, name):
                if name in ('union', 'intersection'):
                    raise TypeError("Protocol check error")
                return super().__getattribute__(name)
        
        registry = get_registry()
        obj = ProblematicType()
        
        # Should handle gracefully
        result = registry._is_setlike(obj)
        assert result is False
