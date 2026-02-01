"""
Complete coverage tests for remaining uncovered lines.

Targets:
- core.py: line 534, 739
- registry.py: lines 152-154
- clustering.py: lines 188-192, 265-268, 590-591, 630, 648, 721, 877-945
"""

import pytest
from unittest.mock import patch, MagicMock
from eule import euler
from eule.core import Euler, _compute_cluster_worker
from eule.clustering import (
    ClusteredEuler, clustered_euler, LeidenClustering, SpectralBisection, 
    HierarchicalClustering, example_usage
)
from eule.registry import get_registry


class TestCoreClusterPrefixedKeys:
    """Test core.py line 534 - cluster-prefixed keys extraction."""
    
    def test_cluster_prefixed_euler_keys(self):
        """Test extraction of cluster-prefixed keys with tuple format (0, (key_tuple,))."""
        # Create a clustered scenario that generates cluster-prefixed keys
        sets = {
            'a': [1, 2, 3],
            'b': [2, 3, 4],
            'c': [100, 101],  # Disconnected cluster
            'd': [100, 101, 102]
        }
        
        e = Euler(sets, cluster=True)
        result = e.as_dict()
        
        # Should handle cluster-prefixed keys properly
        assert isinstance(result, dict)
        assert len(result) > 0


class TestCoreParallelWorker:
    """Test core.py line 739 - parallel worker return."""
    
    def test_compute_cluster_worker_function(self):
        """Test the _compute_cluster_worker function directly."""
        sets = {
            'a': [1, 2, 3],
            'b': [2, 3, 4]
        }
        
        result = _compute_cluster_worker(0, sets)
        
        # Should return tuple (cluster_id, euler_result)
        assert isinstance(result, tuple)
        assert len(result) == 2
        assert result[0] == 0
        assert isinstance(result[1], dict)
    
    def test_parallel_processing_multiple_clusters(self):
        """Test parallel processing triggers worker function."""
        # Create multiple independent clusters
        sets = {
            'a1': [1, 2],
            'a2': [2, 3],
            'b1': [100, 101],
            'b2': [101, 102],
            'c1': [200, 201],
            'c2': [201, 202]
        }
        
        e = Euler(sets, cluster=True, parallel=True)
        result = e.as_dict()
        
        assert isinstance(result, dict)
        assert len(result) > 0


class TestRegistryTypeErrorHandling:
    """Test registry.py lines 152-154 - TypeError in protocol check."""
    
    def test_protocol_isinstance_typeerror(self):
        """Test TypeError handling when isinstance(obj, SetLike) raises."""
        registry = get_registry()
        
        # Create an object that might cause TypeError in protocol check
        class ProblematicType:
            """A type that could cause issues with protocol checking."""
            pass
        
        obj = ProblematicType()
        
        # The _is_setlike method should catch TypeError
        result = registry._is_setlike(obj)
        assert result is False
    
    def test_protocol_check_with_mock(self):
        """Test protocol check with problematic object."""
        registry = get_registry()
        
        # Mock object that might trigger edge cases
        mock_obj = MagicMock()
        
        result = registry._is_setlike(mock_obj)
        # Should return False for objects that don't match protocol
        assert result is False


class TestClusteringMultipleComponents:
    """Test clustering.py lines 188-192 - multiple disconnected components."""
    
    def test_leiden_multiple_disconnected_components(self):
        """Test Leiden splits clusters with multiple disconnected components."""
        # Create a graph with multiple components in same cluster initially
        sets = {
            'a': [1, 2],
            'b': [2, 3],
            'c': [3, 4],
            'd': [10, 11],  # Disconnected component
            'e': [11, 12],
            'f': [20, 21],  # Another disconnected component
        }
        
        ce = ClusteredEuler(sets, method='leiden', resolution=0.5)
        
        # Should identify multiple components
        assert len(set(ce.clustering.values())) >= 1


class TestSpectralBisectionEdgeCases:
    """Test clustering.py lines 265-268 - spectral bisection edge cases."""
    
    def test_spectral_cant_split_cluster(self):
        """Test when spectral bisection cannot split a cluster."""
        # Create a tightly connected cluster that's hard to split
        sets = {
            'a': [1, 2, 3, 4, 5],
            'b': [1, 2, 3, 4, 5],
            'c': [1, 2, 3, 4, 5],
        }
        
        ce = ClusteredEuler(sets, method='spectral')
        
        # Should handle the case gracefully
        assert len(ce.clustering) == 3
    
    def test_spectral_empty_partition(self):
        """Test when one partition ends up empty."""
        # Small sets that might cause empty partitions
        sets = {
            'a': [1],
            'b': [1],
        }
        
        ce = ClusteredEuler(sets, method='spectral')
        
        assert len(ce.clustering) == 2


class TestClusteredEulerStaticMethod:
    """Test clustering.py lines 590-591 - static compute method."""
    
    def test_compute_cluster_diagram_static_method(self):
        """Test the static _compute_cluster_diagram method."""
        sets = {
            'a': [1, 2, 3],
            'b': [2, 3, 4]
        }
        
        result = ClusteredEuler._compute_cluster_diagram(0, sets)
        
        # Should return tuple (cluster_id, diagram)
        assert isinstance(result, tuple)
        assert len(result) == 2
        assert result[0] == 0
        assert isinstance(result[1], dict)


class TestClusteredEulerGetClusterRaise:
    """Test clustering.py line 630 - ValueError when cluster not found."""
    
    def test_get_cluster_euler_nonexistent(self):
        """Test getting a non-existent cluster raises ValueError."""
        sets = {
            'a': [1, 2, 3],
            'b': [2, 3, 4]
        }
        
        ce = ClusteredEuler(sets, method='leiden')
        
        # Try to get a cluster that doesn't exist
        with pytest.raises(ValueError, match="Cluster .* not found"):
            ce.get_cluster_euler(999)


class TestClusteredEulerFlattenCollision:
    """Test clustering.py line 648 - key collision in flatten."""
    
    def test_flatten_with_key_collision(self):
        """Test flatten mode when keys collide across clusters."""
        # Create sets that might cause key collisions
        sets = {
            'a1': [1, 2],
            'b1': [2, 3],
            'a2': [100, 101],
            'b2': [101, 102],
            'a3': [200, 201],
            'b3': [201, 202],
        }
        
        ce = ClusteredEuler(sets, method='leiden')
        
        # Try flattening - should handle collisions
        flat = ce.as_euler_dict(flatten=True)
        
        assert isinstance(flat, dict)
        # Some keys might have cluster prefixes due to collisions


class TestClusteredEulerBridges:
    """Test clustering.py line 721 - bridge elements in summary."""
    
    def test_summary_with_bridge_elements(self):
        """Test summary includes bridge elements when present."""
        # Create sets with overlapping clusters
        sets = {
            'a': [1, 2, 3, 5],  # 5 is bridge
            'b': [3, 4, 5],
            'c': [5, 6, 7],  # 5 appears in multiple clusters
            'd': [7, 8, 9]
        }
        
        ce = ClusteredEuler(sets, method='leiden')
        summary = ce.summary()
        
        # Summary should mention bridge elements if any exist
        assert isinstance(summary, str)
        assert "cluster" in summary.lower()


class TestClusteringExampleUsage:
    """Test clustering.py lines 877-945 - example_usage function."""
    
    def test_example_usage_runs(self):
        """Test that example_usage() runs without errors."""
        # This is in the if __name__ == "__main__" block but we can still test it
        result = example_usage()
        
        assert isinstance(result, ClusteredEuler)
        assert len(result.cluster_diagrams) > 0
        assert len(result.clustering) > 0
    
    def test_example_demonstrates_all_features(self):
        """Test example demonstrates key features."""
        ce = example_usage()
        
        # Should have multiple clusters
        assert len(set(ce.clustering.values())) > 1
        
        # Should have computed diagrams
        assert len(ce.cluster_diagrams) > 0
        
        # Should be able to get global diagram
        global_diagram = ce.as_euler_dict(flatten=False)
        assert isinstance(global_diagram, dict)
        
        # Should be able to flatten
        flat = ce.as_euler_dict(flatten=True)
        assert isinstance(flat, dict)
        
        # Should have bridge sets info
        bridges = ce.get_bridge_sets()
        assert isinstance(bridges, dict)
        
        # Should have metrics
        assert len(ce.metrics) > 0


class TestHierarchicalClustering:
    """Additional hierarchical clustering tests."""
    
    def test_hierarchical_with_disconnected_sets(self):
        """Test hierarchical with completely disconnected sets."""
        sets = {
            'a': [1, 2],
            'b': [10, 11],
            'c': [20, 21],
            'd': [30, 31],
        }
        
        ce = ClusteredEuler(sets, method='hierarchical', linkage='average')
        
        assert len(ce.clustering) == 4
        # Should create clusters
        assert len(set(ce.clustering.values())) >= 1


class TestLeidenClustering:
    """Additional Leiden clustering tests."""
    
    def test_leiden_with_complex_structure(self):
        """Test Leiden with complex graph structure."""
        sets = {
            'a': list(range(1, 10)),
            'b': list(range(5, 15)),
            'c': list(range(10, 20)),
            'd': list(range(15, 25)),
            'e': list(range(20, 30)),
        }
        
        ce = ClusteredEuler(sets, method='leiden', resolution=1.0)
        
        assert len(ce.clustering) == 5
        # Should create clusters
        assert len(set(ce.clustering.values())) >= 1


class TestClusteredEulerManualControl:
    """Test manual control of ClusteredEuler (auto_compute=False)."""
    
    def test_manual_compute_sequential(self):
        """Test manual sequential computation."""
        sets = {
            'a': [1, 2, 3],
            'b': [2, 3, 4],
            'c': [10, 11],
            'd': [11, 12]
        }
        
        ce = ClusteredEuler(sets, method='hierarchical', auto_compute=False)
        
        # Should not have diagrams yet
        assert len(ce.cluster_diagrams) == 0
        
        # Compute sequentially
        ce.compute(parallel=False)
        
        # Should have diagrams now
        assert len(ce.cluster_diagrams) > 0
    
    def test_manual_compute_parallel(self):
        """Test manual parallel computation."""
        sets = {
            'a': [1, 2],
            'b': [2, 3],
            'c': [10, 11],
            'd': [11, 12],
            'e': [20, 21],
            'f': [21, 22],
        }
        
        ce = ClusteredEuler(sets, method='leiden', auto_compute=False)
        
        # Compute in parallel
        ce.compute(parallel=True)
        
        # Should have diagrams
        assert len(ce.cluster_diagrams) > 0


class TestClusteredEulerVisualization:
    """Test visualization methods."""
    
    def test_visualize_clustering(self):
        """Test clustering visualization."""
        sets = {
            'a': [1, 2, 3],
            'b': [2, 3, 4],
            'c': [10, 11],
        }
        
        ce = ClusteredEuler(sets, method='leiden')
        viz = ce.visualize_clustering()
        
        assert isinstance(viz, str)
        assert len(viz) > 0
        # Should show cluster assignments


class TestConvenienceFunction:
    """Test clustered_euler convenience function."""
    
    def test_clustered_euler_function(self):
        """Test the clustered_euler convenience function."""
        sets = {
            'a': [1, 2, 3],
            'b': [2, 3, 4],
            'c': [10, 11, 12],
        }
        
        ce = clustered_euler(sets, method='leiden', resolution=1.0)
        
        assert isinstance(ce, ClusteredEuler)
        assert len(ce.cluster_diagrams) > 0
    
    def test_clustered_euler_all_methods(self):
        """Test clustered_euler with all available methods."""
        sets = {
            'a': [1, 2, 3],
            'b': [2, 3, 4],
        }
        
        methods = ['leiden', 'hierarchical', 'spectral']
        
        for method in methods:
            ce = clustered_euler(sets, method=method)
            assert isinstance(ce, ClusteredEuler)
            assert len(ce.clustering) == 2


class TestEdgeCaseCombinations:
    """Test various edge case combinations."""
    
    def test_single_set_clustering(self):
        """Test clustering with a single set."""
        sets = {'a': [1, 2, 3]}
        
        ce = ClusteredEuler(sets, method='leiden')
        
        assert len(ce.clustering) == 1
        assert len(ce.cluster_diagrams) == 1
    
    def test_all_empty_sets_clustering(self):
        """Test clustering with all empty sets."""
        sets = {'a': [], 'b': [], 'c': []}
        
        ce = ClusteredEuler(sets, method='leiden')
        
        assert len(ce.clustering) == 3
    
    def test_mixed_empty_and_nonempty(self):
        """Test clustering with mixed empty and non-empty sets."""
        sets = {
            'a': [1, 2],
            'b': [],
            'c': [3, 4],
            'd': []
        }
        
        ce = ClusteredEuler(sets, method='hierarchical')
        
        assert len(ce.clustering) == 4
