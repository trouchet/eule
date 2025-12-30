"""
Clustered Euler Diagram System
Implements graph-based clustering for parallel Euler diagram construction
Fully integrated with the euler module
"""
from copy import deepcopy
from typing import Dict, List, Tuple, Set, Optional, Union
from collections import defaultdict
import numpy as np
from dataclasses import dataclass
from multiprocessing import Pool

# Import your euler module functions
from .operations import difference, intersection, union
from .types import SetsType
from .utils import cleared_set_keys, ordered_tuplify
from .core import euler, euler_generator, Euler


@dataclass
class ClusterMetrics:
    """Metrics for evaluating cluster quality"""
    intra_overlap: float  # Sum of overlaps within cluster
    inter_overlap: float  # Sum of overlaps between clusters
    size: int  # Number of sets in cluster
    conductance: float  # Inter/Intra ratio
    
    def score(self) -> float:
        """Higher is better - maximize internal, minimize external"""
        if self.inter_overlap == 0:
            return float('inf')
        return self.intra_overlap / (self.inter_overlap + 1e-10)


class SetOverlapGraph:
    """Represents sets as a weighted overlap graph"""
    
    def __init__(self, sets: Dict):
        self.sets = deepcopy(sets)
        self.set_keys = list(sets.keys())
        self.n = len(self.set_keys)
        self.overlap_matrix = self._compute_overlap_matrix()
        self.adjacency = self._build_adjacency()
        
    def _compute_overlap_matrix(self) -> np.ndarray:
        """Compute pairwise Jaccard similarity between sets"""
        n = self.n
        overlap = np.zeros((n, n))
        
        for i, key_i in enumerate(self.set_keys):
            set_i = set(self.sets[key_i])
            for j in range(i, n):
                key_j = self.set_keys[j]
                set_j = set(self.sets[key_j])
                
                if i == j:
                    overlap[i, j] = 1.0
                else:
                    intersection = len(set_i & set_j)
                    union = len(set_i | set_j)
                    if union > 0:
                        jaccard = intersection / union
                        overlap[i, j] = overlap[j, i] = jaccard
        
        return overlap
    
    def _build_adjacency(self, threshold: float = 0.1) -> Dict[int, List[Tuple[int, float]]]:
        """Build adjacency list with threshold pruning"""
        adj = defaultdict(list)
        for i in range(self.n):
            for j in range(i + 1, self.n):
                weight = self.overlap_matrix[i, j]
                if weight > threshold:
                    adj[i].append((j, weight))
                    adj[j].append((i, weight))
        return adj
    
    def get_overlap(self, key_i: str, key_j: str) -> float:
        """Get overlap between two sets by key"""
        i = self.set_keys.index(key_i)
        j = self.set_keys.index(key_j)
        return self.overlap_matrix[i, j]


class LeidenClustering:
    """Simplified Leiden-style community detection for set clustering"""
    
    def __init__(self, graph: SetOverlapGraph, resolution: float = 1.0):
        self.graph = graph
        self.resolution = resolution
        self.clusters = list(range(graph.n))  # Initial: each node in own cluster
        
    def cluster(self, max_iterations: int = 100) -> Dict[str, int]:
        """Run clustering algorithm"""
        improved = True
        iteration = 0
        
        while improved and iteration < max_iterations:
            improved = self._local_moving()
            iteration += 1
        
        # Ensure connected clusters
        self._ensure_connectivity()
        
        # Map to set keys
        return {self.graph.set_keys[i]: self.clusters[i] for i in range(self.graph.n)}
    
    def _local_moving(self) -> bool:
        """Move nodes to improve modularity"""
        improved = False
        
        for node in range(self.graph.n):
            current_cluster = self.clusters[node]
            best_cluster = current_cluster
            best_delta = 0
            
            # Consider neighbor clusters
            neighbor_clusters = set()
            for neighbor, weight in self.graph.adjacency[node]:
                neighbor_clusters.add(self.clusters[neighbor])
            
            for candidate_cluster in neighbor_clusters:
                if candidate_cluster == current_cluster:
                    continue
                
                delta = self._modularity_delta(node, current_cluster, candidate_cluster)
                if delta > best_delta:
                    best_delta = delta
                    best_cluster = candidate_cluster
            
            if best_cluster != current_cluster:
                self.clusters[node] = best_cluster
                improved = True
        
        return improved
    
    def _modularity_delta(self, node: int, from_cluster: int, to_cluster: int) -> float:
        """Compute change in modularity from moving node"""
        # Sum of weights to nodes in each cluster
        weight_to_from = 0
        weight_to_to = 0
        
        for neighbor, weight in self.graph.adjacency[node]:
            if self.clusters[neighbor] == from_cluster:
                weight_to_from += weight
            elif self.clusters[neighbor] == to_cluster:
                weight_to_to += weight
        
        return self.resolution * (weight_to_to - weight_to_from)
    
    def _ensure_connectivity(self):
        """Ensure each cluster forms a connected component"""
        cluster_nodes = defaultdict(list)
        for i, cluster in enumerate(self.clusters):
            cluster_nodes[cluster].append(i)
        
        new_cluster_id = max(self.clusters) + 1
        
        for cluster_id, nodes in cluster_nodes.items():
            if len(nodes) <= 1:
                continue
            
            # BFS to find connected components
            visited = set()
            components = []
            
            for start in nodes:
                if start in visited:
                    continue
                
                component = []
                queue = [start]
                visited.add(start)
                
                while queue:
                    node = queue.pop(0)
                    component.append(node)
                    
                    for neighbor, _ in self.graph.adjacency[node]:
                        if neighbor in nodes and neighbor not in visited:
                            visited.add(neighbor)
                            queue.append(neighbor)
                
                components.append(component)
            
            # Keep largest component in original cluster, reassign others
            if len(components) > 1:
                components.sort(key=len, reverse=True)
                for comp in components[1:]:
                    for node in comp:
                        self.clusters[node] = new_cluster_id
                    new_cluster_id += 1


class SpectralBisection:
    """Spectral clustering for balanced bisection"""
    
    def __init__(self, graph: SetOverlapGraph):
        self.graph = graph
    
    def bisect(self) -> Tuple[List[str], List[str]]:
        """Bisect graph into two balanced parts"""
        if self.graph.n <= 1:
            return [self.graph.set_keys[0]], []
        
        # Compute Laplacian
        L = self._compute_laplacian()
        
        # Find Fiedler vector (second smallest eigenvector)
        eigenvalues, eigenvectors = np.linalg.eigh(L)
        fiedler = eigenvectors[:, 1]  # Second eigenvector
        
        # Bisect by median
        median = np.median(fiedler)
        partition_1 = [self.graph.set_keys[i] for i in range(self.graph.n) if fiedler[i] <= median]
        partition_2 = [self.graph.set_keys[i] for i in range(self.graph.n) if fiedler[i] > median]
        
        return partition_1, partition_2
    
    def _compute_laplacian(self) -> np.ndarray:
        """Compute normalized graph Laplacian"""
        n = self.graph.n
        A = self.graph.overlap_matrix.copy()
        np.fill_diagonal(A, 0)  # No self-loops
        
        # Degree matrix
        D = np.diag(A.sum(axis=1))
        
        # Normalized Laplacian: L = D^(-1/2) (D - A) D^(-1/2)
        D_inv_sqrt = np.diag(1.0 / np.sqrt(np.diag(D) + 1e-10))
        L = np.eye(n) - D_inv_sqrt @ A @ D_inv_sqrt
        
        return L


class HierarchicalClustering:
    """Recursive bisection for hierarchical clustering"""
    
    def __init__(self, graph: SetOverlapGraph, max_cluster_size: int = 20):
        self.graph = graph
        self.max_cluster_size = max_cluster_size
    
    def cluster(self) -> Dict[str, int]:
        """Recursively bisect until clusters are small enough"""
        clusters = {}
        cluster_id = 0
        
        def recursive_bisect(keys: List[str]):
            nonlocal cluster_id
            
            if len(keys) <= self.max_cluster_size:
                for key in keys:
                    clusters[key] = cluster_id
                cluster_id += 1
                return
            
            # Create subgraph
            subsets = {k: self.graph.sets[k] for k in keys}
            subgraph = SetOverlapGraph(subsets)
            bisector = SpectralBisection(subgraph)
            part1, part2 = bisector.bisect()
            
            if len(part1) == 0 or len(part2) == 0:
                # Couldn't split, accept as is
                for key in keys:
                    clusters[key] = cluster_id
                cluster_id += 1
                return
            
            recursive_bisect(part1)
            recursive_bisect(part2)
        
        recursive_bisect(self.graph.set_keys)
        return clusters


class OverlappingClustering:
    """
    Overlapping clustering that allows sets to belong to multiple clusters.
    Uses enhanced detection of bridge sets with multiple strategies.
    """
    
    def __init__(self, graph, 
                 overlap_threshold: float = 0.18,
                 min_bridge_strength: float = 0.15):
        """
        Args:
            graph: SetOverlapGraph instance
            overlap_threshold: Minimum Jaccard overlap to consider secondary membership
            min_bridge_strength: Minimum strength for bridge membership (relative to primary)
        """
        self.graph = graph
        self.overlap_threshold = overlap_threshold
        self.min_bridge_strength = min_bridge_strength
        self.memberships = {}  # set_key -> [(cluster_id, strength)]
    
    def cluster(self, base_resolution: float = 0.8):
        """
        Perform overlapping clustering
        
        Args:
            base_resolution: Resolution parameter for base Leiden clustering
        
        Returns:
            Dict mapping set keys to list of cluster IDs they belong to
        """
        # Start with disjoint clusters
        leiden = LeidenClustering(self.graph, resolution=base_resolution)
        base_clustering = leiden.cluster()
        
        # Count sets per cluster
        cluster_sizes = defaultdict(int)
        for cluster_id in base_clustering.values():
            cluster_sizes[cluster_id] += 1
        
        # Initialize memberships
        for key, cluster_id in base_clustering.items():
            self.memberships[key] = [(cluster_id, 1.0)]
        
        # Find additional memberships using multiple strategies
        for i, key_i in enumerate(self.graph.set_keys):
            set_i = set(self.graph.sets[key_i])
            primary_cluster = base_clustering[key_i]
            
            # Strategy 1: Strong individual connections
            cluster_connections = defaultdict(list)
            for j, key_j in enumerate(self.graph.set_keys):
                if i == j:
                    continue
                cluster_j = base_clustering[key_j]
                if cluster_j == primary_cluster:
                    continue
                
                overlap = self.graph.overlap_matrix[i, j]
                if overlap > self.overlap_threshold:
                    cluster_connections[cluster_j].append((key_j, overlap))
            
            # Strategy 2: Aggregate cluster affinity
            cluster_affinities = {}
            for cluster_id, connections in cluster_connections.items():
                # Weighted average of connections to this cluster
                if len(connections) > 0:
                    weights = [overlap for _, overlap in connections]
                    # Affinity considers both strength and number of connections
                    avg_strength = np.mean(weights)
                    # Boost for multiple connections (up to 3)
                    connection_factor = min(1.0, len(connections) / 3.0)
                    affinity = avg_strength * (0.7 + 0.3 * connection_factor)
                    cluster_affinities[cluster_id] = affinity
            
            # Strategy 3: Check if set is roughly equidistant between clusters
            if len(cluster_affinities) > 0:
                primary_strength = 1.0
                
                for cluster_id, affinity in cluster_affinities.items():
                    # Add secondary membership if affinity is significant
                    relative_strength = affinity / primary_strength
                    
                    if relative_strength > self.min_bridge_strength:
                        # Don't add if already present
                        cluster_ids = [c for c, _ in self.memberships[key_i]]
                        if cluster_id not in cluster_ids:
                            self.memberships[key_i].append((cluster_id, affinity))
        
        # Sort memberships by strength
        for key in self.memberships:
            self.memberships[key].sort(key=lambda x: x[1], reverse=True)
        
        # Convert to simple format
        result = {}
        for key, memberships in self.memberships.items():
            result[key] = [cid for cid, _ in memberships]
        
        return result
    
    def get_primary_clustering(self):
        """Get primary (strongest) cluster for each set"""
        return {key: clusters[0][0] for key, clusters in self.memberships.items()}
    
    def get_membership_strengths(self):
        """Get full membership information with strengths"""
        return dict(self.memberships)


def compute_cluster_metrics(sets: Dict, clustering: Dict[str, int]) -> Dict[int, ClusterMetrics]:
    """Compute quality metrics for each cluster"""
    cluster_sets = defaultdict(list)
    for key, cluster_id in clustering.items():
        cluster_sets[cluster_id].append(key)
    
    metrics = {}
    for cluster_id, keys in cluster_sets.items():
        intra = 0
        inter = 0
        
        # Intra-cluster overlap
        for i, key_i in enumerate(keys):
            set_i = set(sets[key_i])
            for key_j in keys[i+1:]:
                set_j = set(sets[key_j])
                intra += len(set_i & set_j)
        
        # Inter-cluster overlap
        other_keys = [k for k in sets.keys() if k not in keys]
        for key_i in keys:
            set_i = set(sets[key_i])
            for key_j in other_keys:
                set_j = set(sets[key_j])
                inter += len(set_i & set_j)
        
        conductance = inter / (intra + inter + 1) if (intra + inter) > 0 else 1.0
        
        metrics[cluster_id] = ClusterMetrics(
            intra_overlap=intra,
            inter_overlap=inter,
            size=len(keys),
            conductance=conductance
        )
    
    return metrics


def rebalance_clusters(sets: Dict, clustering: Dict[str, int], 
                       max_size: int = 50, min_size: int = 5) -> Dict[str, int]:
    """Rebalance clusters that are too large or too small"""
    cluster_sets = defaultdict(list)
    for key, cluster_id in clustering.items():
        cluster_sets[cluster_id].append(key)
    
    new_clustering = {}
    next_id = max(clustering.values()) + 1
    
    for cluster_id, keys in cluster_sets.items():
        if len(keys) <= max_size:
            # Accept as is
            for key in keys:
                new_clustering[key] = cluster_id
        else:
            # Split large cluster
            subsets = {k: sets[k] for k in keys}
            subgraph = SetOverlapGraph(subsets)
            bisector = SpectralBisection(subgraph)
            part1, part2 = bisector.bisect()
            
            for key in part1:
                new_clustering[key] = cluster_id
            for key in part2:
                new_clustering[key] = next_id
            next_id += 1
    
    return new_clustering


class ClusteredEuler:
    """
    Clustered Euler diagram with full integration.
    
    This class combines graph-based clustering with Euler diagram construction
    to enable divide-and-conquer computation and improved visualization.
    """
    
    def __init__(self, sets: SetsType, method: str = 'leiden', 
                 auto_compute: bool = True, **kwargs):
        """
        Initialize clustered Euler diagram
        
        Args:
            sets: Dictionary or list of sets
            method: Clustering method ('leiden', 'spectral', 'hierarchical')
            auto_compute: If True, automatically compute Euler diagrams after clustering
            **kwargs: Additional parameters:
                - resolution: float (leiden only, default 1.0)
                - max_cluster_size: int (default 30)
                - min_cluster_size: int (default 3)
                - overlap_threshold: float (default 0.1)
                - use_parallel: bool (default True for >4 clusters)
        """
        self.original_sets = deepcopy(sets)
        
        # Convert to dict if list
        if isinstance(sets, list):
            self.sets = {i: s for i, s in enumerate(sets)}
        else:
            self.sets = deepcopy(sets)
        
        self.method = method
        self.kwargs = kwargs
        
        # Clustering results
        self.graph = SetOverlapGraph(self.sets)
        self.clustering = None
        self.metrics = {}
        
        # Euler diagram results
        self.cluster_diagrams = {}
        self.global_euler = None
        self.bridge_elements = {}
        
        # Perform clustering
        self._cluster(**kwargs)
        
        # Optionally compute diagrams
        if auto_compute:
            self.compute()
    
    def _cluster(self, **kwargs):
        """Execute clustering algorithm"""
        if self.method == 'leiden':
            resolution = kwargs.get('resolution', 1.0)
            clusterer = LeidenClustering(self.graph, resolution=resolution)
            self.clustering = clusterer.cluster()
            
        elif self.method == 'spectral':
            max_size = kwargs.get('max_cluster_size', 20)
            clusterer = HierarchicalClustering(self.graph, max_cluster_size=max_size)
            self.clustering = clusterer.cluster()
            
        elif self.method == 'hierarchical':
            max_size = kwargs.get('max_cluster_size', 20)
            clusterer = HierarchicalClustering(self.graph, max_cluster_size=max_size)
            self.clustering = clusterer.cluster()
        
        else:
            raise ValueError(f"Unknown clustering method: {self.method}")
        
        # Rebalance if needed
        max_size = kwargs.get('max_cluster_size', 30)
        min_size = kwargs.get('min_cluster_size', 3)
        self.clustering = rebalance_clusters(self.sets, self.clustering, max_size, min_size)
        
        # Compute metrics
        self.metrics = compute_cluster_metrics(self.sets, self.clustering)
    
    def get_cluster_sets(self) -> Dict[int, Dict]:
        """Get sets grouped by cluster"""
        cluster_sets = defaultdict(dict)
        for key, cluster_id in self.clustering.items():
            cluster_sets[cluster_id][key] = self.sets[key]
        return dict(cluster_sets)
    
    def compute(self, parallel: Optional[bool] = None):
        """
        Compute Euler diagrams for each cluster and merge results
        
        Args:
            parallel: If True, use parallel computation. If None, auto-decide based on cluster count.
        """
        n_clusters = len(set(self.clustering.values()))
        
        # Auto-decide parallel based on cluster count
        if parallel is None:
            parallel = self.kwargs.get('use_parallel', n_clusters > 4)
        
        # Compute cluster diagrams
        if parallel:
            self._compute_parallel()
        else:
            self._compute_sequential()
        
        # Identify and handle bridge elements
        self._identify_bridges()
        
        # Merge into global Euler diagram
        self._merge_diagrams()
        
        return self.global_euler
    
    def _compute_sequential(self):
        """Compute Euler diagrams for each cluster sequentially"""
        cluster_sets = self.get_cluster_sets()
        
        for cluster_id, sets in cluster_sets.items():
            self.cluster_diagrams[cluster_id] = euler(sets)
    
    def _compute_parallel(self):
        """Compute Euler diagrams for each cluster in parallel"""
        cluster_sets = self.get_cluster_sets()
        
        with Pool() as pool:
            results = pool.starmap(
                self._compute_cluster_diagram,
                [(cluster_id, sets) for cluster_id, sets in cluster_sets.items()]
            )
        
        self.cluster_diagrams = dict(results)
    
    @staticmethod
    def _compute_cluster_diagram(cluster_id: int, sets: Dict):
        """Worker function for parallel computation"""
        diagram = euler(sets)
        return (cluster_id, diagram)
    
    def _identify_bridges(self):
        """Identify elements that exist in multiple clusters (bridge elements)"""
        element_clusters = defaultdict(set)
        
        # Map each element to clusters it appears in
        for key, cluster_id in self.clustering.items():
            for elem in self.sets[key]:
                element_clusters[elem].add(cluster_id)
        
        # Store elements that appear in multiple clusters
        for elem, clusters in element_clusters.items():
            if len(clusters) > 1:
                self.bridge_elements[elem] = list(clusters)
    
    def _merge_diagrams(self):
        """
        Merge cluster diagrams into a global Euler representation
        
        Strategy:
        1. Each cluster diagram provides local Euler regions
        2. Prefix region keys with cluster ID to avoid collisions
        3. Bridge elements are tracked for cross-cluster visualization
        """
        self.global_euler = {}
        
        for cluster_id, diagram in self.cluster_diagrams.items():
            for key_tuple, elements in diagram.items():
                # Create global key: (cluster_id, original_key_tuple)
                global_key = (cluster_id, key_tuple)
                self.global_euler[global_key] = elements
        
        return self.global_euler
    
    def get_cluster_euler(self, cluster_id: int) -> Dict:
        """Get Euler diagram for a specific cluster"""
        if cluster_id not in self.cluster_diagrams:
            raise ValueError(f"Cluster {cluster_id} not found")
        return self.cluster_diagrams[cluster_id]
    
    def as_euler_dict(self, flatten: bool = False) -> Dict:
        """
        Get Euler diagram in standard format
        
        Args:
            flatten: If True, merge cluster prefixes and return flat dict.
                    If False, return with cluster prefixes (default).
        """
        if flatten:
            # Attempt to merge: if keys collide, keep separate
            flat = {}
            for (cluster_id, key_tuple), elements in self.global_euler.items():
                if key_tuple not in flat:
                    flat[key_tuple] = elements
                else:
                    # Collision - keep cluster prefix
                    flat[(cluster_id, key_tuple)] = elements
            return flat
        else:
            return self.global_euler
    
    def to_euler(self, flatten: bool = True):
        """
        Convert to standard Euler object (from your euler module)
        
        Args:
            flatten: If True, attempt to create flat Euler dict
        """
        euler_dict = self.as_euler_dict(flatten=flatten)
        return Euler(euler_dict)
    
    def get_bridge_sets(self) -> Dict[str, List[int]]:
        """
        Identify sets that connect multiple clusters
        
        Returns:
            Dict mapping set keys to list of connected cluster IDs
        """
        bridges = {}
        
        for key in self.sets.keys():
            set_elements = set(self.sets[key])
            own_cluster = self.clustering[key]
            
            # Check overlap with other clusters
            connected_clusters = set()
            for other_key in self.sets.keys():
                if key == other_key:
                    continue
                other_cluster = self.clustering[other_key]
                if other_cluster == own_cluster:
                    continue
                
                other_elements = set(self.sets[other_key])
                overlap = len(set_elements & other_elements)
                if overlap > 0:
                    connected_clusters.add(other_cluster)
            
            if connected_clusters:
                bridges[key] = sorted(list(connected_clusters))
        
        return bridges
    
    def summary(self) -> str:
        """Generate comprehensive summary of clustering and diagrams"""
        n_clusters = len(set(self.clustering.values()))
        cluster_sizes = defaultdict(int)
        for cluster_id in self.clustering.values():
            cluster_sizes[cluster_id] += 1
        
        lines = [
            f"Clustered Euler Diagram Summary",
            f"================================",
            f"Method: {self.method}",
            f"Total sets: {len(self.sets)}",
            f"Number of clusters: {n_clusters}",
            f"Cluster sizes: {dict(sorted(cluster_sizes.items()))}",
            f"",
            f"Cluster Metrics:",
        ]
        
        for cluster_id, metric in sorted(self.metrics.items()):
            lines.append(
                f"  Cluster {cluster_id}: size={metric.size}, "
                f"intra={metric.intra_overlap:.1f}, inter={metric.inter_overlap:.1f}, "
                f"conductance={metric.conductance:.3f}, score={metric.score():.2f}"
            )
        
        if self.bridge_elements:
            lines.append(f"\nBridge elements (span multiple clusters): {len(self.bridge_elements)}")
        
        if self.cluster_diagrams:
            lines.append(f"\nEuler Diagrams Computed:")
            for cluster_id in sorted(self.cluster_diagrams.keys()):
                n_regions = len(self.cluster_diagrams[cluster_id])
                lines.append(f"  Cluster {cluster_id}: {n_regions} Euler regions")
        
        bridge_sets = self.get_bridge_sets()
        if bridge_sets:
            lines.append(f"\nBridge sets (connect clusters):")
            for key, clusters in sorted(bridge_sets.items()):
                lines.append(f"  Set '{key}' connects clusters: {clusters}")
        
        return "\n".join(lines)
    
    def visualize_clustering(self) -> str:
        """Simple text visualization of clustering"""
        lines = ["Clustering Visualization:", ""]
        
        cluster_sets = self.get_cluster_sets()
        for cluster_id in sorted(cluster_sets.keys()):
            sets = cluster_sets[cluster_id]
            lines.append(f"Cluster {cluster_id}:")
            for key in sorted(sets.keys()):
                lines.append(f"  {key}: {sets[key]}")
            lines.append("")
        
        return "\n".join(lines)


class ClusteredEulerOverlapping(ClusteredEuler):
    """
    Extended ClusteredEuler that supports overlapping clusters.
    Sets can belong to multiple clusters, appearing in multiple subdiagrams.
    """
    
    def __init__(self, sets, method='leiden', allow_overlap=False, 
                 overlap_threshold=0.3, **kwargs):
        """
        Args:
            sets: Dictionary of sets
            method: Clustering method
            allow_overlap: If True, use overlapping clustering
            overlap_threshold: Threshold for overlapping membership
            **kwargs: Other parameters
        """
        self.allow_overlap = allow_overlap
        self.overlap_threshold = overlap_threshold
        self.overlapping_clustering = None
        
        if allow_overlap:
            # Don't auto-compute yet - we need custom clustering
            kwargs['auto_compute'] = False
        
        super().__init__(sets, method=method, **kwargs)
        
        if allow_overlap:
            self._cluster_overlapping()
            if kwargs.get('auto_compute', True):
                self.compute()
    
    def _cluster_overlapping(self):
        """Perform overlapping clustering"""
        oc = OverlappingClustering(self.graph, self.overlap_threshold)
        self.overlapping_clustering = oc.cluster()
        
        # For compatibility, store primary clustering
        self.clustering = oc.get_primary_clustering()
        
        # Recompute metrics based on primary clustering
        from .clustering import compute_cluster_metrics
        self.metrics = compute_cluster_metrics(self.sets, self.clustering)
    
    def get_cluster_sets(self) -> Dict[int, Dict]:
        """
        Get sets grouped by cluster.
        In overlapping mode, sets can appear in multiple clusters.
        """
        if not self.allow_overlap:
            return super().get_cluster_sets()
        
        cluster_sets = defaultdict(dict)
        for key in self.sets.keys():
            cluster_ids = self.overlapping_clustering[key]
            for cluster_id in cluster_ids:
                cluster_sets[cluster_id][key] = self.sets[key]
        
        return dict(cluster_sets)
    
    def get_overlap_stats(self) -> Dict:
        """Get statistics about overlapping memberships"""
        if not self.allow_overlap:
            return {"overlapping": False}
        
        n_overlapping = sum(1 for clusters in self.overlapping_clustering.values() 
                           if len(clusters) > 1)
        max_overlap = max(len(clusters) for clusters in self.overlapping_clustering.values())
        
        return {
            "overlapping": True,
            "n_overlapping_sets": n_overlapping,
            "max_memberships": max_overlap,
            "avg_memberships": np.mean([len(c) for c in self.overlapping_clustering.values()])
        }
    
    def summary(self) -> str:
        """Extended summary with overlap information"""
        base = super().summary()
        
        if self.allow_overlap:
            stats = self.get_overlap_stats()
            overlap_info = [
                "\nOverlapping Clustering:",
                f"  Sets with multiple memberships: {stats['n_overlapping_sets']}",
                f"  Max memberships per set: {stats['max_memberships']}",
                f"  Avg memberships per set: {stats['avg_memberships']:.2f}",
                "\nOverlapping set assignments:"
            ]
            
            for key, clusters in sorted(self.overlapping_clustering.items()):
                if len(clusters) > 1:
                    overlap_info.append(f"  {key} -> clusters {clusters}")
            
            return base + "\n" + "\n".join(overlap_info)
        
        return base


# Convenience function
def clustered_euler(sets: SetsType, method: str = 'leiden', **kwargs) -> ClusteredEuler:
    """
    Convenience function to create a clustered Euler diagram
    
    Args:
        sets: Dictionary or list of sets
        method: Clustering method ('leiden', 'spectral', 'hierarchical')
        **kwargs: Additional parameters for ClusteredEuler
    
    Returns:
        ClusteredEuler object with computed diagrams
    
    Example:
        >>> sets = {'A': [1,2,3], 'B': [2,3,4], 'C': [5,6,7]}
        >>> ce = clustered_euler(sets, method='leiden')
        >>> print(ce.summary())
        >>> euler_dict = ce.as_euler_dict()
    """
    return ClusteredEuler(sets, method=method, **kwargs)


# Example usage
def example_usage():
    """Comprehensive example demonstrating all features"""
    
    # Example sets with clear cluster structure
    sets = {
        'A': [1, 2, 3, 4, 5],
        'B': [3, 4, 5, 6, 7],
        'C': [5, 6, 7, 8, 9],
        'D': [10, 11, 12, 13],
        'E': [12, 13, 14, 15],
        'F': [20, 21, 22],
        'G': [21, 22, 23, 24],
    }
    
    print("=" * 60)
    print("EXAMPLE: Clustered Euler Diagram System")
    print("=" * 60)
    
    # Method 1: Using the convenience function
    print("\n1. Creating clustered Euler diagram...")
    ce = clustered_euler(sets, method='leiden', resolution=1.0)
    
    # Print summary
    print("\n" + ce.summary())
    
    # Show clustering visually
    print("\n" + ce.visualize_clustering())
    
    # Access cluster-specific diagrams
    print("\n2. Accessing cluster-specific Euler diagrams:")
    for cluster_id in sorted(ce.cluster_diagrams.keys()):
        diagram = ce.get_cluster_euler(cluster_id)
        print(f"\nCluster {cluster_id} Euler diagram:")
        for key, elems in sorted(diagram.items()):
            print(f"  {key}: {elems}")
    
    # Get global merged diagram
    print("\n3. Global merged Euler diagram:")
    global_diagram = ce.as_euler_dict(flatten=False)
    for key, elems in sorted(global_diagram.items(), key=str):
        print(f"  {key}: {elems}")
    
    # Get bridge information
    bridges = ce.get_bridge_sets()
    print("Sets connecting clusters:", bridges)

    # Get metrics
    for cluster_id, metric in ce.metrics.items():
        print(f"Cluster {cluster_id} score: {metric.score()}")
    
    # Try flattened version
    print("\n4. Flattened Euler diagram (cluster prefixes removed where possible):")
    flat = ce.as_euler_dict(flatten=True)
    for key, elems in sorted(flat.items(), key=str):
        print(f"  {key}: {elems}")
    
    # Method 2: Manual control
    print("\n" + "=" * 60)
    print("5. Manual control example (no auto-compute):")
    print("=" * 60)
    
    ce2 = ClusteredEuler(sets, method='hierarchical', 
                         max_cluster_size=2, auto_compute=False)
    print(f"\nClustered into {len(set(ce2.clustering.values()))} clusters")
    print("Clusters:", ce2.get_cluster_sets())
    
    # Compute sequentially
    print("\nComputing Euler diagrams sequentially...")
    ce2.compute(parallel=False)
    print(f"Computed {len(ce2.cluster_diagrams)} cluster diagrams")
    print(f"Cluster diagrams: {ce2.cluster_diagrams[0]}")

    return ce


if __name__ == "__main__":
    example_usage()