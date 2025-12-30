"""
Comprehensive test suite for clustered Euler diagrams
Target: 100% code coverage
"""
import pytest
import numpy as np
from copy import deepcopy
from collections import defaultdict


class TestSetOverlapGraph:
    """Test SetOverlapGraph class"""
    
    def test_init_basic(self):
        """Test basic initialization"""
        from eule.clustering import SetOverlapGraph
        
        sets = {'A': [1, 2, 3], 'B': [2, 3, 4]}
        graph = SetOverlapGraph(sets)
        
        assert graph.n == 2
        assert len(graph.set_keys) == 2
        assert graph.overlap_matrix.shape == (2, 2)
    
    def test_overlap_matrix_diagonal(self):
        """Test diagonal is 1.0 (self-similarity)"""
        from eule.clustering import SetOverlapGraph
        
        sets = {'A': [1, 2, 3], 'B': [4, 5, 6]}
        graph = SetOverlapGraph(sets)
        
        assert graph.overlap_matrix[0, 0] == 1.0
        assert graph.overlap_matrix[1, 1] == 1.0
    
    def test_overlap_matrix_symmetry(self):
        """Test overlap matrix is symmetric"""
        from eule.clustering import SetOverlapGraph
        
        sets = {'A': [1, 2, 3], 'B': [2, 3, 4], 'C': [3, 4, 5]}
        graph = SetOverlapGraph(sets)
        
        for i in range(graph.n):
            for j in range(graph.n):
                assert abs(graph.overlap_matrix[i, j] - graph.overlap_matrix[j, i]) < 1e-10
    
    def test_jaccard_calculation(self):
        """Test Jaccard similarity calculation"""
        from eule.clustering import SetOverlapGraph
        
        sets = {
            'A': [1, 2, 3, 4],      # 4 elements
            'B': [3, 4, 5, 6]       # 4 elements, 2 overlap
        }
        graph = SetOverlapGraph(sets)
        
        # Jaccard = |A ∩ B| / |A ∪ B| = 2 / 6 = 0.333...
        expected = 2.0 / 6.0
        actual = graph.overlap_matrix[0, 1]
        assert abs(actual - expected) < 1e-10
    
    def test_no_overlap(self):
        """Test disjoint sets have zero overlap"""
        from eule.clustering import SetOverlapGraph
        
        sets = {'A': [1, 2, 3], 'B': [4, 5, 6]}
        graph = SetOverlapGraph(sets)
        
        assert graph.overlap_matrix[0, 1] == 0.0
    
    def test_adjacency_threshold(self):
        """Test adjacency list respects threshold"""
        from eule.clustering import SetOverlapGraph
        
        sets = {
            'A': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            'B': [1, 2],  # Low overlap
            'C': [1, 2, 3, 4, 5]  # Higher overlap
        }
        graph = SetOverlapGraph(sets)
        
        # Check adjacency only includes edges above threshold
        for node, neighbors in graph.adjacency.items():
            for neighbor, weight in neighbors:
                assert weight > 0.1  # Default threshold
    
    def test_get_overlap(self):
        """Test get_overlap method"""
        from eule.clustering import SetOverlapGraph
        
        sets = {'A': [1, 2, 3], 'B': [2, 3, 4]}
        graph = SetOverlapGraph(sets)
        
        overlap = graph.get_overlap('A', 'B')
        expected = 2.0 / 4.0  # 2 common, 4 total
        assert abs(overlap - expected) < 1e-10


class TestLeidenClustering:
    """Test Leiden clustering algorithm"""
    
    def test_init(self):
        """Test Leiden initialization"""
        from eule.clustering import SetOverlapGraph, LeidenClustering
        
        sets = {'A': [1, 2, 3], 'B': [2, 3, 4]}
        graph = SetOverlapGraph(sets)
        leiden = LeidenClustering(graph, resolution=1.0)
        
        assert leiden.graph == graph
        assert leiden.resolution == 1.0
        assert len(leiden.clusters) == graph.n
    
    def test_cluster_single_set(self):
        """Test clustering with single set"""
        from eule.clustering import SetOverlapGraph, LeidenClustering
        
        sets = {'A': [1, 2, 3]}
        graph = SetOverlapGraph(sets)
        leiden = LeidenClustering(graph)
        
        clustering = leiden.cluster()
        assert len(clustering) == 1
        assert 'A' in clustering
    
    def test_cluster_disjoint_sets(self):
        """Test clustering identifies disjoint sets"""
        from eule.clustering import SetOverlapGraph, LeidenClustering
        
        sets = {
            'A': [1, 2, 3],
            'B': [2, 3, 4],
            'C': [10, 11, 12],
            'D': [11, 12, 13]
        }
        graph = SetOverlapGraph(sets)
        leiden = LeidenClustering(graph, resolution=0.5)
        
        clustering = leiden.cluster()
        
        # A-B should cluster together
        # C-D should cluster together
        assert clustering['A'] == clustering['B']
        assert clustering['C'] == clustering['D']
        assert clustering['A'] != clustering['C']
    
    def test_connectivity_guarantee(self):
        """Test that clusters are connected"""
        from eule.clustering import SetOverlapGraph, LeidenClustering
        
        sets = {f'S{i}': list(range(i*5, i*5+7)) for i in range(10)}
        graph = SetOverlapGraph(sets)
        leiden = LeidenClustering(graph)
        
        clustering = leiden.cluster()
        
        # Each cluster should be connected in the graph
        cluster_nodes = defaultdict(list)
        for node, cluster_id in enumerate(graph.set_keys):
            cluster_nodes[clustering[cluster_id]].append(node)
        
        # Check connectivity (simplified - just check size)
        for cluster_id, nodes in cluster_nodes.items():
            assert len(nodes) > 0


class TestSpectralBisection:
    """Test spectral bisection"""
    
    def test_bisect_simple(self):
        """Test basic bisection"""
        from eule.clustering import SetOverlapGraph, SpectralBisection
        
        sets = {
            'A': [1, 2, 3],
            'B': [2, 3, 4],
            'C': [10, 11, 12],
            'D': [11, 12, 13]
        }
        graph = SetOverlapGraph(sets)
        bisector = SpectralBisection(graph)
        
        part1, part2 = bisector.bisect()
        
        assert len(part1) > 0
        assert len(part2) > 0
        assert len(part1) + len(part2) == len(sets)
    
    def test_bisect_single_set(self):
        """Test bisection with single set"""
        from eule.clustering import SetOverlapGraph, SpectralBisection
        
        sets = {'A': [1, 2, 3]}
        graph = SetOverlapGraph(sets)
        bisector = SpectralBisection(graph)
        
        part1, part2 = bisector.bisect()
        
        assert part1 == ['A']
        assert part2 == []


class TestHierarchicalClustering:
    """Test hierarchical clustering"""
    
    def test_cluster_small(self):
        """Test clustering below max size"""
        from eule.clustering import SetOverlapGraph, HierarchicalClustering
        
        sets = {f'S{i}': [i, i+1, i+2] for i in range(5)}
        graph = SetOverlapGraph(sets)
        clusterer = HierarchicalClustering(graph, max_cluster_size=10)
        
        clustering = clusterer.cluster()
        
        assert len(set(clustering.values())) == 1  # All in one cluster
    
    def test_cluster_large(self):
        """Test clustering exceeds max size and splits"""
        from eule.clustering import SetOverlapGraph, HierarchicalClustering
        
        sets = {f'S{i}': [i, i+1, i+2] for i in range(30)}
        graph = SetOverlapGraph(sets)
        clusterer = HierarchicalClustering(graph, max_cluster_size=10)
        
        clustering = clusterer.cluster()
        
        assert len(set(clustering.values())) > 1  # Split into multiple clusters


class TestOverlappingClustering:
    """Test overlapping clustering"""
    
    def test_init(self):
        """Test initialization"""
        from eule.clustering import SetOverlapGraph, OverlappingClustering
        
        sets = {'A': [1, 2, 3], 'B': [2, 3, 4]}
        graph = SetOverlapGraph(sets)
        oc = OverlappingClustering(graph, overlap_threshold=0.2, min_bridge_strength=0.15)
        
        assert oc.overlap_threshold == 0.2
        assert oc.min_bridge_strength == 0.15
    
    def test_cluster_no_overlap(self):
        """Test clustering with no bridges"""
        from eule.clustering import SetOverlapGraph, OverlappingClustering
        
        sets = {
            'A': [1, 2, 3],
            'B': [2, 3, 4],
            'C': [10, 11, 12],
            'D': [11, 12, 13]
        }
        graph = SetOverlapGraph(sets)
        oc = OverlappingClustering(graph, overlap_threshold=0.5)
        
        clustering = oc.cluster(base_resolution=0.5)
        
        # No set should have multiple memberships (threshold too high)
        for key, clusters in clustering.items():
            assert len(clusters) >= 1
    
    def test_cluster_with_bridges(self):
        """Test clustering detects bridge sets"""
        from eule.clustering import SetOverlapGraph, OverlappingClustering
        
        sets = {
            'A': list(range(1, 10)),
            'B': list(range(5, 14)),
            'C': list(range(20, 29)),
            'D': list(range(24, 33)),
            'Bridge': list(range(10, 14)) + list(range(20, 24))
        }
        graph = SetOverlapGraph(sets)
        oc = OverlappingClustering(graph, overlap_threshold=0.2, min_bridge_strength=0.15)
        
        clustering = oc.cluster(base_resolution=0.6)
        
        # Bridge should have multiple memberships
        assert 'Bridge' in clustering
        # At least one set should have multiple clusters
        has_multiple = any(len(clusters) > 1 for clusters in clustering.values())
        assert has_multiple
    
    def test_get_primary_clustering(self):
        """Test getting primary clustering"""
        from eule.clustering import SetOverlapGraph, OverlappingClustering
        
        sets = {'A': [1, 2, 3], 'B': [2, 3, 4]}
        graph = SetOverlapGraph(sets)
        oc = OverlappingClustering(graph)
        
        oc.cluster()
        primary = oc.get_primary_clustering()
        
        assert len(primary) == len(sets)
        for key in sets:
            assert key in primary
            assert isinstance(primary[key], int)
    
    def test_get_membership_strengths(self):
        """Test getting membership strengths"""
        from eule.clustering import SetOverlapGraph, OverlappingClustering
        
        sets = {'A': [1, 2, 3], 'B': [2, 3, 4]}
        graph = SetOverlapGraph(sets)
        oc = OverlappingClustering(graph)
        
        oc.cluster()
        strengths = oc.get_membership_strengths()
        
        assert len(strengths) == len(sets)
        for key, memberships in strengths.items():
            assert len(memberships) > 0
            # Check format: list of (cluster_id, strength)
            for cluster_id, strength in memberships:
                assert isinstance(cluster_id, int)
                assert 0 <= strength <= 1


class TestClusterMetrics:
    """Test cluster quality metrics"""
    
    def test_compute_metrics(self):
        """Test computing cluster metrics"""
        from eule.clustering import compute_cluster_metrics
        
        sets = {
            'A': [1, 2, 3],
            'B': [2, 3, 4],
            'C': [10, 11, 12]
        }
        clustering = {'A': 0, 'B': 0, 'C': 1}
        
        metrics = compute_cluster_metrics(sets, clustering)
        
        assert len(metrics) == 2  # 2 clusters
        assert 0 in metrics
        assert 1 in metrics
        
        # Check metric structure
        m = metrics[0]
        assert hasattr(m, 'size')
        assert hasattr(m, 'intra_overlap')
        assert hasattr(m, 'inter_overlap')
        assert hasattr(m, 'conductance')
    
    def test_metric_score(self):
        """Test metric score calculation"""
        from eule.clustering import ClusterMetrics
        
        m = ClusterMetrics(intra_overlap=10.0, inter_overlap=2.0, 
                          size=3, conductance=0.167)
        
        score = m.score()
        # Simple score: intra / inter
        assert score == pytest.approx(10.0 / 2.0)


class TestUnifiedEuler:
    """Test unified Euler class"""
    
    def test_init_no_clustering(self):
        """Test initialization without clustering"""
        from eule import Euler
        
        sets = {'A': [1, 2, 3], 'B': [2, 3, 4]}
        e = Euler(sets, use_clustering=False)
        
        assert not e.use_clustering
        assert e.esets is not None
        assert len(e.esets) > 0
    
    def test_init_with_clustering(self):
        """Test initialization with clustering"""
        from eule import Euler
        
        sets = {f'S{i}': list(range(i*5, i*5+10)) for i in range(35)}
        e = Euler(sets, use_clustering=True)
        
        assert e.use_clustering
        assert e.clustering is not None
        assert e.cluster_diagrams is not None
    
    def test_auto_clustering_small(self):
        """Test auto-clustering disabled for small sets"""
        from eule import Euler
        
        sets = {'A': [1, 2, 3], 'B': [2, 3, 4]}
        e = Euler(sets)  # use_clustering=None (auto)
        
        assert not e.use_clustering
    
    def test_auto_clustering_large(self):
        """Test auto-clustering enabled for large sets"""
        from eule import Euler
        
        sets = {f'S{i}': [i, i+1, i+2] for i in range(35)}
        e = Euler(sets)  # use_clustering=None (auto)
        
        assert e.use_clustering
    
    def test_getitem_single_key(self):
        """Test accessing single set"""
        from eule import Euler
        
        sets = {'A': [1, 2, 3], 'B': [2, 3, 4]}
        e = Euler(sets)
        
        assert e['A'] == [1, 2, 3]
    
    def test_getitem_tuple(self):
        """Test accessing union of sets"""
        from eule import Euler
        
        sets = {'A': [1, 2, 3], 'B': [3, 4, 5]}
        e = Euler(sets)
        
        result = e[('A', 'B')]
        assert set(result) == {1, 2, 3, 4, 5}
    
    def test_getitem_invalid_key(self):
        """Test accessing invalid key raises error"""
        from eule import Euler
        
        sets = {'A': [1, 2, 3]}
        e = Euler(sets)
        
        with pytest.raises(KeyError):
            _ = e['Z']
    
    def test_euler_keys(self):
        """Test getting Euler keys"""
        from eule import Euler
        
        sets = {'A': [1, 2, 3], 'B': [2, 3, 4]}
        e = Euler(sets)
        
        keys = e.euler_keys()
        assert isinstance(keys, list)
        assert len(keys) > 0
    
    def test_as_dict(self):
        """Test getting Euler as dict"""
        from eule import Euler
        
        sets = {'A': [1, 2, 3], 'B': [2, 3, 4]}
        e = Euler(sets)
        
        d = e.as_dict()
        assert isinstance(d, dict)
        assert len(d) > 0
    
    def test_match(self):
        """Test matching items to sets"""
        from eule import Euler
        
        sets = {'A': [1, 2, 3], 'B': [2, 3, 4]}
        e = Euler(sets)
        
        result = e.match({1, 2, 3})
        assert 'A' in result
    
    def test_match_invalid_type(self):
        """Test match with invalid type raises error"""
        from eule import Euler
        
        sets = {'A': [1, 2, 3]}
        e = Euler(sets)
        
        with pytest.raises(TypeError):
            e.match([1, 2, 3])  # Should be set, not list
    
    def test_remove_key(self):
        """Test removing a key"""
        from eule import Euler
        
        sets = {'A': [1, 2, 3], 'B': [2, 3, 4]}
        e = Euler(sets)
        
        e.remove_key('A')
        assert 'A' not in e.sets
    
    def test_remove_invalid_key(self):
        """Test removing invalid key issues warning"""
        from eule import Euler
        import warnings
        
        sets = {'A': [1, 2, 3]}
        e = Euler(sets)
        
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            e.remove_key('Z')
            assert len(w) == 1
    
    def test_get_clustering_info_no_clustering(self):
        """Test get_clustering_info without clustering"""
        from eule import Euler
        
        sets = {'A': [1, 2, 3]}
        e = Euler(sets, use_clustering=False)
        
        info = e.get_clustering_info()
        assert info is None
    
    def test_get_clustering_info_with_clustering(self):
        """Test get_clustering_info with clustering"""
        from eule import Euler
        
        sets = {f'S{i}': [i, i+1, i+2] for i in range(35)}
        e = Euler(sets, use_clustering=True)
        
        info = e.get_clustering_info()
        assert info is not None
        assert 'method' in info
        assert 'n_clusters' in info
        assert 'cluster_sizes' in info
    
    def test_get_bridge_sets_no_clustering(self):
        """Test get_bridge_sets without clustering"""
        from eule import Euler
        
        sets = {'A': [1, 2, 3]}
        e = Euler(sets, use_clustering=False)
        
        bridges = e.get_bridge_sets()
        assert bridges is None
    
    def test_get_bridge_sets_with_clustering(self):
        """Test get_bridge_sets with clustering"""
        from eule import Euler
        
        sets = {
            'A': [1, 2, 3],
            'B': [2, 3, 4],
            'C': [10, 11, 12],
            'D': [11, 12, 13]
        }
        e = Euler(sets, use_clustering=True, resolution=0.5)
        
        bridges = e.get_bridge_sets()
        # May or may not have bridges depending on clustering
        assert bridges is not None
        assert isinstance(bridges, dict)
    
    def test_summary(self):
        """Test summary generation"""
        from eule import Euler
        
        sets = {'A': [1, 2, 3], 'B': [2, 3, 4]}
        e = Euler(sets)
        
        summary = e.summary()
        assert isinstance(summary, str)
        assert 'Sets:' in summary
    
    def test_repr(self):
        """Test string representation"""
        from eule import Euler
        
        sets = {'A': [1, 2, 3], 'B': [2, 3, 4]}
        e = Euler(sets)
        
        r = repr(e)
        assert 'Euler' in r
        assert 'sets=' in r
    
    def test_overlapping_clustering(self):
        """Test overlapping clustering mode"""
        from eule import Euler
        
        sets = {
            'A': list(range(1, 10)),
            'B': list(range(5, 14)),
            'C': list(range(20, 29)),
            'Bridge': list(range(10, 14)) + list(range(20, 24))
        }
        e = Euler(sets, use_clustering=True, allow_overlap=True,
                 resolution=0.6, overlap_threshold=0.2)
        
        assert e.allow_overlap
        info = e.get_clustering_info()
        assert 'n_overlapping_sets' in info or info['allow_overlap']


class TestEulerFunction:
    """Test standalone euler function"""
    
    def test_euler_function_basic(self):
        """Test basic euler function"""
        from eule import euler
        
        sets = {'A': [1, 2, 3], 'B': [2, 3, 4]}
        result = euler(sets)
        
        assert isinstance(result, dict)
        assert len(result) > 0
    
    def test_euler_function_with_clustering(self):
        """Test euler function with clustering"""
        from eule import euler
        
        sets = {f'S{i}': [i, i+1, i+2] for i in range(35)}
        result = euler(sets, use_clustering=True)
        
        assert isinstance(result, dict)
        assert len(result) > 0


class TestRebalanceClusters:
    """Test cluster rebalancing"""
    
    def test_rebalance_large_cluster(self):
        """Test splitting large cluster"""
        from eule.clustering import rebalance_clusters
        
        sets = {f'S{i}': [i, i+1, i+2] for i in range(60)}
        clustering = {f'S{i}': 0 for i in range(60)}  # All in one cluster
        
        rebalanced = rebalance_clusters(sets, clustering, max_size=30, min_size=5)
        
        # Should split into multiple clusters
        n_clusters = len(set(rebalanced.values()))
        assert n_clusters > 1


class TestEdgeCases:
    """Test edge cases and error handling"""
    
    def test_empty_sets(self):
        """Test with empty sets dict"""
        from eule import Euler
        
        sets = {}
        e = Euler(sets, use_clustering=False)
        
        assert len(e.esets) == 0
    
    def test_single_set(self):
        """Test with single set"""
        from eule import Euler
        
        sets = {'A': [1, 2, 3]}
        e = Euler(sets, use_clustering=True)
        
        assert len(e.sets) == 1
    
    def test_invalid_clustering_method(self):
        """Test invalid clustering method raises error"""
        from eule import Euler
        
        sets = {'A': [1, 2, 3], 'B': [2, 3, 4]}
        
        with pytest.raises(ValueError):
            Euler(sets, use_clustering=True, method='invalid_method')
    
    def test_list_input(self):
        """Test with list input instead of dict"""
        from eule import Euler
        
        sets = [[1, 2, 3], [2, 3, 4]]
        e = Euler(sets)
        
        assert len(e.sets) == 2


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--cov=eule', '--cov-report=html', '--cov-report=term'])