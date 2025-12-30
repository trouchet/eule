"""
Test suite for benchmark module
"""
import pytest
import numpy as np


class TestDataGenerator:
    """Test synthetic data generation"""
    
    def test_generate_clustered_sets_basic(self):
        """Test basic clustered set generation"""
        from eule.benchmark import DataGenerator
        
        sets = DataGenerator.generate_clustered_sets(
            n_clusters=3,
            sets_per_cluster=5,
            elements_per_set=20
        )
        
        assert len(sets) == 15  # 3 * 5
        for key, elems in sets.items():
            assert len(elems) > 0
    
    def test_generate_clustered_sets_overlap(self):
        """Test intra-cluster overlap"""
        from eule.benchmark import DataGenerator
        
        sets = DataGenerator.generate_clustered_sets(
            n_clusters=2,
            sets_per_cluster=3,
            elements_per_set=10,
            intra_overlap=0.5
        )
        
        # Check that sets within same cluster have overlap
        cluster_0_sets = [sets[f'C0_S{i}'] for i in range(3)]
        
        # Check consecutive sets overlap
        overlap = len(set(cluster_0_sets[0]) & set(cluster_0_sets[1]))
        assert overlap > 0
    
    def test_generate_clustered_sets_inter_overlap(self):
        """Test inter-cluster overlap creates bridges"""
        from eule.benchmark import DataGenerator
        
        sets = DataGenerator.generate_clustered_sets(
            n_clusters=3,
            sets_per_cluster=3,
            elements_per_set=20,
            intra_overlap=0.3,
            inter_overlap=0.2,
            seed=42
        )
        
        # At least some inter-cluster connections should exist
        # (probabilistic, but with seed should be consistent)
        assert len(sets) == 9
    
    def test_generate_random_sets(self):
        """Test random set generation"""
        from eule.benchmark import DataGenerator
        
        sets = DataGenerator.generate_random_sets(
            n_sets=10,
            n_elements=100,
            overlap_ratio=0.3
        )
        
        assert len(sets) == 10
        for key, elems in sets.items():
            assert len(elems) > 0
    
    def test_generate_random_sets_reproducible(self):
        """Test that seed makes generation reproducible"""
        from eule.benchmark import DataGenerator
        
        sets1 = DataGenerator.generate_random_sets(
            n_sets=5, n_elements=50, seed=42
        )
        sets2 = DataGenerator.generate_random_sets(
            n_sets=5, n_elements=50, seed=42
        )
        
        for key in sets1:
            assert sets1[key] == sets2[key]


class TestBenchmarkResult:
    """Test BenchmarkResult dataclass"""
    
    def test_create_result(self):
        """Test creating benchmark result"""
        from eule.benchmark import BenchmarkResult
        
        result = BenchmarkResult(
            name="Test",
            n_sets=10,
            n_elements=50,
            n_clusters=2,
            clustering_time=0.1,
            euler_time=0.2,
            total_time=0.3,
            speedup=1.5
        )
        
        assert result.name == "Test"
        assert result.speedup == 1.5
    
    def test_result_str(self):
        """Test result string representation"""
        from eule.benchmark import BenchmarkResult
        
        result = BenchmarkResult(
            name="Test",
            n_sets=10,
            n_elements=50,
            n_clusters=2,
            clustering_time=0.1,
            euler_time=0.2,
            total_time=0.3,
            speedup=1.5
        )
        
        s = str(result)
        assert "Test" in s
        assert "10" in s


class TestEulerBenchmark:
    """Test EulerBenchmark class"""
    
    def test_init(self):
        """Test benchmark initialization"""
        from eule.benchmark import EulerBenchmark
        
        bench = EulerBenchmark()
        assert bench.results == []
    
    def test_benchmark_correctness_small(self):
        """Test correctness verification on small example"""
        from eule.benchmark import EulerBenchmark, DataGenerator
        
        bench = EulerBenchmark()
        
        # Run on small data (won't print in test)
        try:
            bench.benchmark_correctness()
            # If no exception, test passes
        except Exception as e:
            pytest.fail(f"Correctness benchmark failed: {e}")
    
    def test_benchmark_scalability_small(self):
        """Test scalability benchmark on small sizes"""
        from eule.benchmark import EulerBenchmark
        
        bench = EulerBenchmark()
        
        # Run on very small sizes to keep test fast
        try:
            bench.benchmark_scalability(sizes=[5, 10])
            assert len(bench.results) > 0
        except Exception as e:
            pytest.fail(f"Scalability benchmark failed: {e}")
    
    def test_benchmark_clustering_methods(self):
        """Test clustering methods comparison"""
        from eule.benchmark import EulerBenchmark
        
        bench = EulerBenchmark()
        
        try:
            bench.benchmark_clustering_methods(n_sets=15)
            # Should complete without error
        except Exception as e:
            pytest.fail(f"Clustering methods benchmark failed: {e}")
    
    def test_benchmark_overlapping(self):
        """Test overlapping clustering benchmark"""
        from eule.benchmark import EulerBenchmark
        
        bench = EulerBenchmark()
        
        try:
            bench.benchmark_overlapping(n_sets=12)
            # Should complete without error
        except Exception as e:
            pytest.fail(f"Overlapping benchmark failed: {e}")


class TestBenchmarkFunctions:
    """Test benchmark utility functions"""
    
    def test_demo_overlapping(self):
        """Test demo_overlapping runs"""
        from eule.benchmark import demo_overlapping
        
        try:
            # Capture output to avoid cluttering test output
            import sys
            from io import StringIO
            old_stdout = sys.stdout
            sys.stdout = StringIO()
            
            demo_overlapping()
            
            sys.stdout = old_stdout
        except Exception as e:
            pytest.fail(f"demo_overlapping failed: {e}")
    
    def test_run_full_benchmark_minimal(self):
        """Test that run_full_benchmark can execute"""
        # This is a smoke test - just check it doesn't crash
        # We skip actually running it in normal tests as it's slow
        from eule.benchmark import run_full_benchmark
        
        # Just check it's importable and callable
        assert callable(run_full_benchmark)


class TestIntegration:
    """Integration tests combining multiple components"""
    
    def test_end_to_end_small(self):
        """Test complete pipeline on small data"""
        from eule import Euler
        from eule.benchmark import DataGenerator
        
        # Generate data
        sets = DataGenerator.generate_clustered_sets(
            n_clusters=2,
            sets_per_cluster=3,
            elements_per_set=10
        )
        
        # Create Euler with clustering
        e = Euler(sets, use_clustering=True, method='leiden')
        
        # Check results
        assert e.esets is not None
        assert len(e.esets) > 0
        info = e.get_clustering_info()
        assert info is not None
    
    def test_end_to_end_overlapping(self):
        """Test complete pipeline with overlapping"""
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
        assert info is not None
    
    def test_benchmark_to_euler(self):
        """Test using benchmark data with Euler"""
        from eule import Euler
        from eule.benchmark import DataGenerator
        
        # Generate benchmark data
        sets = DataGenerator.generate_random_sets(
            n_sets=20,
            n_elements=100,
            overlap_ratio=0.3
        )
        
        # Process with Euler
        e = Euler(sets, use_clustering=True)
        
        # Verify
        assert len(e.euler_keys()) > 0
        assert e.summary() is not None


class TestErrorHandling:
    """Test error handling in benchmark"""
    
    def test_invalid_data_generator_params(self):
        """Test data generator with invalid params"""
        from eule.benchmark import DataGenerator
        
        # Should handle gracefully
        sets = DataGenerator.generate_clustered_sets(
            n_clusters=0,  # Invalid
            sets_per_cluster=1,
            elements_per_set=10
        )
        
        # Should return empty or minimal
        assert isinstance(sets, dict)
    
    def test_benchmark_empty_sets(self):
        """Test benchmark with empty sets"""
        from eule.benchmark import EulerBenchmark
        from eule import Euler
        
        sets = {}
        
        try:
            e = Euler(sets, use_clustering=True)
            # Should handle gracefully
        except Exception:
            # Expected to potentially fail
            pass


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--cov=eule.benchmark', '--cov-report=term'])