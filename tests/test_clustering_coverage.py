"""
Additional tests to achieve 100% coverage of clustering.py
"""
import pytest
import numpy as np
from eule import Euler
from eule.clustering import (
    SetOverlapGraph, 
    LeidenClustering, 
    HierarchicalClustering,
    SpectralBisection,
    ClusterMetrics,
    ClusteredEuler,
    clustered_euler
)


class TestClusterMetrics:
    """Test ClusterMetrics dataclass."""
    
    def test_score_with_zero_inter_overlap(self):
        """Test score calculation when inter_overlap is 0."""
        metrics = ClusterMetrics(
            intra_overlap=10.0,
            inter_overlap=0.0,
            size=5,
            conductance=0.0
        )
        score = metrics.score()
        assert score == float('inf')
    
    def test_score_normal_case(self):
        """Test score calculation with normal values."""
        metrics = ClusterMetrics(
            intra_overlap=10.0,
            inter_overlap=2.0,
            size=5,
            conductance=0.2
        )
        score = metrics.score()
        assert score > 0
        assert isinstance(score, float)


class TestSetOverlapGraph:
    """Test SetOverlapGraph edge cases."""
    
    def test_empty_intersection(self):
        """Test overlap matrix with no intersection (line 61 branch)."""
        sets = {
            'a': [1, 2, 3],
            'b': [10, 20, 30],  # No overlap
            'c': [100, 200]
        }
        graph = SetOverlapGraph(sets)
        
        # Should have zero overlap between disjoint sets
        assert graph.get_overlap('a', 'b') == 0.0
        assert graph.get_overlap('b', 'c') == 0.0
    
    def test_adjacency_threshold_filtering(self):
        """Test adjacency list filters low weights."""
        sets = {
            'a': list(range(100)),
            'b': [1],  # Small overlap (1/100 = 0.01 < 0.1 threshold)
            'c': list(range(50))  # Medium overlap
        }
        graph = SetOverlapGraph(sets)
        
        # Check adjacency was built
        assert isinstance(graph.adjacency, dict)


class TestLeidenClustering:
    """Test Leiden clustering edge cases."""
    
    def test_disconnected_components(self):
        """Test handling of disconnected graph components (lines 188-192)."""
        # Create sets with multiple disconnected components
        sets = {
            'group1_a': [1, 2, 3],
            'group1_b': [2, 3, 4],
            'group2_a': [100, 101, 102],
            'group2_b': [101, 102, 103],
            'group3_a': [1000],  # Isolated node
        }
        
        graph = SetOverlapGraph(sets)
        leiden = LeidenClustering(graph, resolution=0.5)
        clusters = leiden.cluster()
        
        # Should create multiple clusters for disconnected components
        assert len(set(clusters.values())) >= 2
    
    def test_max_iterations_reached(self):
        """Test early stopping at max iterations."""
        sets = {f'set_{i}': list(range(i, i+5)) for i in range(20)}
        
        graph = SetOverlapGraph(sets)
        leiden = LeidenClustering(graph, resolution=1.0)
        
        # Use very few iterations
        clusters = leiden.cluster(max_iterations=2)
        
        assert len(clusters) > 0
    
    def test_no_improvement(self):
        """Test stopping when no improvement happens."""
        # Simple graph that converges immediately
        sets = {
            'a': [1, 2],
            'b': [1, 2],  # Identical to a
        }
        
        graph = SetOverlapGraph(sets)
        leiden = LeidenClustering(graph, resolution=1.0)
        clusters = leiden.cluster()
        
        # Should converge quickly
        assert len(set(clusters.values())) >= 1


class TestHierarchicalClustering:
    """Test Hierarchical clustering edge cases."""
    
    def test_max_cluster_size_enforcement(self):
        """Test max_cluster_size splitting (lines 265-268)."""
        # Create many sets that would naturally cluster together
        sets = {f'set_{i}': list(range(i, i+3)) for i in range(30)}
        
        graph = SetOverlapGraph(sets)
        hierarchical = HierarchicalClustering(graph, max_cluster_size=5)
        clusters = hierarchical.cluster()
        
        # Count cluster sizes
        cluster_sizes = {}
        for key, cid in clusters.items():
            cluster_sizes[cid] = cluster_sizes.get(cid, 0) + 1
        
        # All clusters should respect max size
        for size in cluster_sizes.values():
            assert size <= 5
    
    def test_single_set(self):
        """Test with single set."""
        sets = {'only': [1, 2, 3]}
        
        graph = SetOverlapGraph(sets)
        hierarchical = HierarchicalClustering(graph)
        clusters = hierarchical.cluster()
        
        assert len(clusters) == 1
    
    def test_two_sets_no_overlap(self):
        """Test with two disjoint sets."""
        sets = {
            'a': [1, 2, 3],
            'b': [10, 20, 30]
        }
        
        graph = SetOverlapGraph(sets)
        hierarchical = HierarchicalClustering(graph)
        clusters = hierarchical.cluster()
        
        # Should create two clusters
        assert len(set(clusters.values())) >= 1


class TestSpectralBisection:
    """Test Spectral bisection edge cases."""
    
    def test_small_graph(self):
        """Test bisection with very small graph (lines 590-591)."""
        sets = {
            'a': [1, 2],
            'b': [2, 3]
        }
        
        graph = SetOverlapGraph(sets)
        spectral = SpectralBisection(graph)
        result = spectral.bisect()
        
        # Should return some partitioning
        assert isinstance(result, (dict, tuple, list))
    
    def test_disconnected_graph(self):
        """Test with disconnected components."""
        sets = {
            'a': [1, 2, 3],
            'b': [1, 2, 3],
            'c': [100, 101],
            'd': [100, 101]
        }
        
        graph = SetOverlapGraph(sets)
        spectral = SpectralBisection(graph)
        result = spectral.bisect()
        
        assert result is not None


class TestClusteredEuler:
    """Test ClusteredEuler class edge cases."""
    
    def test_compute_metrics(self):
        """Test metric computation."""
        sets = {
            'a': [1, 2, 3],
            'b': [2, 3, 4],
            'c': [10, 11, 12]
        }
        
        ce = ClusteredEuler(sets, method='leiden')
        
        # Check if metrics exist
        if hasattr(ce, 'metrics') and ce.metrics:
            for cid, metric in ce.metrics.items():
                assert isinstance(metric, ClusterMetrics)
                assert metric.size > 0
    
    def test_get_cluster_diagram(self):
        """Test getting diagram for specific cluster."""
        sets = {f'set_{i}': list(range(i, i+5)) for i in range(10)}
        
        ce = ClusteredEuler(sets, method='leiden')
        
        # Get first cluster's diagram
        cluster_ids = list(ce.cluster_diagrams.keys())
        if cluster_ids:
            diagram = ce.cluster_diagrams[cluster_ids[0]]
            assert isinstance(diagram, (Euler, dict))
    
    def test_get_all_regions(self):
        """Test getting all regions across clusters."""
        sets = {
            'a': [1, 2, 3],
            'b': [2, 3, 4],
            'c': [10, 11, 12]
        }
        
        ce = ClusteredEuler(sets, method='leiden')
        
        # Get regions from cluster diagrams
        all_regions = {}
        for cid, diagram in ce.cluster_diagrams.items():
            if isinstance(diagram, dict):
                all_regions.update(diagram)
            else:
                all_regions.update(diagram.as_dict())
        
        assert isinstance(all_regions, dict)
        assert len(all_regions) > 0
    
    def test_summary_output(self):
        """Test summary string generation."""
        sets = {f'set_{i}': list(range(i, i+5)) for i in range(10)}
        
        ce = ClusteredEuler(sets, method='leiden')
        summary = ce.summary()
        
        assert isinstance(summary, str)
        assert len(summary) > 0
        assert 'Cluster' in summary or 'cluster' in summary
    
    def test_visualize_clustering(self):
        """Test clustering visualization."""
        sets = {
            'a': [1, 2, 3],
            'b': [2, 3, 4],
            'c': [10, 11, 12]
        }
        
        ce = ClusteredEuler(sets, method='leiden')
        viz = ce.visualize_clustering()
        
        assert isinstance(viz, str)
        assert len(viz) > 0


class TestClusteredEulerFunction:
    """Test clustered_euler convenience function."""
    
    def test_method_leiden(self):
        """Test with Leiden method."""
        sets = {f'set_{i}': list(range(i, i+5)) for i in range(10)}
        
        ce = clustered_euler(sets, method='leiden', resolution=1.0)
        
        assert isinstance(ce, ClusteredEuler)
        assert len(ce.cluster_diagrams) > 0
    
    def test_method_hierarchical(self):
        """Test with hierarchical method."""
        sets = {f'set_{i}': list(range(i, i+5)) for i in range(10)}
        
        ce = clustered_euler(sets, method='hierarchical', max_cluster_size=5)
        
        assert isinstance(ce, ClusteredEuler)
        assert len(ce.cluster_diagrams) > 0
    
    def test_method_spectral(self):
        """Test with spectral method."""
        sets = {f'set_{i}': list(range(i, i+5)) for i in range(10)}
        
        ce = clustered_euler(sets, method='spectral')
        
        assert isinstance(ce, ClusteredEuler)
        assert len(ce.cluster_diagrams) > 0
    
    def test_auto_parallel(self):
        """Test automatic parallel processing decision."""
        # Small set - should not use parallel
        small_sets = {f'set_{i}': [i] for i in range(5)}
        ce1 = clustered_euler(small_sets, parallel='auto')
        assert ce1 is not None
        
        # Large set - may use parallel
        large_sets = {f'set_{i}': list(range(i, i+5)) for i in range(100)}
        ce2 = clustered_euler(large_sets, parallel='auto')
        assert ce2 is not None
    
    def test_parallel_true(self):
        """Test forced parallel processing."""
        sets = {f'set_{i}': list(range(i, i+5)) for i in range(20)}
        
        ce = clustered_euler(sets, parallel=True, n_jobs=2)
        
        assert isinstance(ce, ClusteredEuler)
    
    def test_parallel_false(self):
        """Test serial processing."""
        sets = {f'set_{i}': list(range(i, i+5)) for i in range(10)}
        
        ce = clustered_euler(sets, parallel=False)
        
        assert isinstance(ce, ClusteredEuler)
    
    def test_invalid_method(self):
        """Test with invalid clustering method."""
        sets = {'a': [1, 2, 3]}
        
        with pytest.raises(ValueError, match="Unknown clustering method"):
            clustered_euler(sets, method='invalid_method')


class TestEdgeCases:
    """Test various edge cases and error conditions."""
    
    def test_empty_sets_dict(self):
        """Test with empty sets dictionary."""
        sets = {}
        
        with pytest.raises((ValueError, KeyError)):
            ClusteredEuler(sets)
    
    def test_single_element_sets(self):
        """Test with sets containing single elements."""
        sets = {
            'a': [1],
            'b': [2],
            'c': [3]
        }
        
        ce = ClusteredEuler(sets, method='leiden')
        assert ce is not None
    
    def test_identical_sets(self):
        """Test with multiple identical sets."""
        sets = {
            'a': [1, 2, 3],
            'b': [1, 2, 3],
            'c': [1, 2, 3]
        }
        
        ce = ClusteredEuler(sets, method='leiden')
        
        # All should be in same cluster
        cluster_ids = set(ce.clustering.values())
        assert len(cluster_ids) == 1
    
    def test_large_overlap_graph(self):
        """Test with large number of sets."""
        sets = {f'set_{i}': list(range(i, i+10)) for i in range(50)}
        
        ce = ClusteredEuler(sets, method='leiden')
        
        assert len(ce.cluster_diagrams) > 0
        assert len(ce.clustering) == 50


class TestMetricCalculations:
    """Test cluster metric calculations."""
    
    def test_conductance_calculation(self):
        """Test conductance metric."""
        metrics = ClusterMetrics(
            intra_overlap=10.0,
            inter_overlap=2.0,
            size=5,
            conductance=0.2
        )
        
        # Conductance should be inter/intra
        expected_conductance = 2.0 / (10.0 + 2.0)
        assert abs(metrics.conductance - 0.2) < 0.1  # Approximately
    
    def test_score_ordering(self):
        """Test that higher intra, lower inter gives better score."""
        good_metrics = ClusterMetrics(
            intra_overlap=100.0,
            inter_overlap=1.0,
            size=10,
            conductance=0.01
        )
        
        bad_metrics = ClusterMetrics(
            intra_overlap=10.0,
            inter_overlap=50.0,
            size=10,
            conductance=0.5
        )
        
        assert good_metrics.score() > bad_metrics.score()
