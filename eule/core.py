"""Main module."""
from copy import deepcopy
from multiprocessing import Pool
from reprlib import repr
from typing import Dict
from typing import Optional
from typing import Union
from typing import List
from warnings import warn
from collections import defaultdict

from .operations import difference
from .operations import intersection
from .operations import union
from .types import KeyType
from .types import SetsType
from .utils import cleared_set_keys
from .utils import ordered_tuplify
from .utils import update_ordered_tuple
from .validators import validate_euler_generator_input


def euler_generator(
    sets: SetsType
):
    """This generator function returns each tuple (key, elems) of the
    Euler diagram in a generator-wise fashion systematic:

    1. Begin with the available `sets` and their exclusive elements;
    2. Compute complementary elements to the current key-set;
    3. In case complementary set-keys AND current set content are not empty, continue;
    4. Otherwise, go to the next key-set;
    5. Find the euler diagram on complementary sets;
    6. Compute exclusive combination elements;
    7. In case there are exclusive elements to the combination: yield exclusive
       combination elements; Remove exclusive combination elements from the current key-set.

    :param dict sets: array/dict of arrays
    :returns: (key, euler_set) tuple of given sets
    :rtype: tuple
    """
    # Deep copy of sets and validates for List case
    sets_ = deepcopy(sets)
    sets_ = validate_euler_generator_input(sets_)

    # Sets with non-empty elements
    set_keys = cleared_set_keys(sets_)

    # Only a set
    if len(set_keys) == 1:
        comb_key = set_keys[0]
        comb_elements = list(sets_.values())[0]
        yield ((comb_key, ), comb_elements)
    # Traverse the combination lattice
    for set_key in set_keys:
        other_keys = [k for k in set_keys if k != set_key]
        this_set = sets_[set_key]
        if not this_set or not other_keys:
            continue

        # Complementary sets
        csets = { cset_key: sets_[cset_key] for cset_key in other_keys }

        # Instrospective recursion: Exclusive combination elements
        for euler_tuple, celements in euler_generator(csets):

            # Remove current set_key elements
            comb_elems = difference(celements, this_set)

            # Non-empty combination exclusivity case
            if comb_elems:
                # Sort keys to assure deterministic behavior
                sorted_comb_key = ordered_tuplify(euler_tuple)

                # 1. Exclusive elements respective complementary keys
                yield (sorted_comb_key, comb_elems)

                # Remove comb_elems elements from its original sets
                for euler_set_key in sorted_comb_key:
                    sets_[euler_set_key] = difference(sets_[euler_set_key], comb_elems)

            # Retrieve intersection elements
            comb_elems = intersection(celements, sets_[set_key])

            # Non-empty intersection set
            if comb_elems:
                # Sort keys to assure deterministic behavior
                comb_key = update_ordered_tuple(euler_tuple, set_key)

                # 2. Intersection of analysis element and exclusive group:
                yield (comb_key, comb_elems)

                # Remove intersection elements from current key-set and complementary sets
                for euler_set_key in comb_key:
                    sets_[euler_set_key] = difference(sets_[euler_set_key], comb_elems)

                sets_[set_key] = difference(sets_[set_key], comb_elems)

            set_keys = cleared_set_keys(sets_)

        if sets_[set_key]:
            # 3. Remaining exclusive elements
            yield ((set_key, ), sets_[set_key])

            # Remove remaining set elements
            sets_[set_key] = []

        set_keys = cleared_set_keys(sets_)

def euler_generator_worker(args):
    sets, set_keys, set_key = args
    results = []
    this_set = sets[set_key]
    
    if this_set and len(set_keys) == 1:
        sorted_comb_key = ordered_tuplify((set_key, ))
        results.append((sorted_comb_key, this_set))
        return results
    
    # Only a set
    other_keys = [key for key in set_keys if key != set_key]
    if not this_set or not other_keys:
        return results

    # Complementary sets
    csets = {key: sets[key] for key in other_keys}

    for euler_tuple, celements in euler_generator(csets):
        comb_elems = difference(celements, this_set)

        # Non-empty combination exclusivity case
        if comb_elems:
            sorted_comb_key = ordered_tuplify(euler_tuple)
            results.append((sorted_comb_key, comb_elems, ))

            # Update sets
            for euler_set_key in sorted_comb_key:
                sets[euler_set_key] = difference(sets[euler_set_key], comb_elems)

        # Retrieve intersection key elements
        comb_elems = intersection(celements, this_set)

        # Non-empty intersection set
        if comb_elems:
            comb_key = update_ordered_tuple(euler_tuple, set_key)
            results.append((comb_key, comb_elems))

            for euler_set_key in comb_key:
                sets[euler_set_key] = difference(sets[euler_set_key], comb_elems)
            sets[set_key] = difference(sets[set_key], comb_elems)

    # Remaining exclusive elements
    if sets[set_key]:
        results.append(((set_key,), sets[set_key]))
        sets[set_key] = []

    return results

def euler_generator_parallel(sets: SetsType):
    sets_ = deepcopy(sets)
    sets_ = validate_euler_generator_input(sets_)
    set_keys = cleared_set_keys(sets_)

    if len(set_keys) == 1:
        comb_key = set_keys[0]
        comb_elements = list(sets_.values())[0]
        yield ((comb_key,), comb_elements)
        return

    with Pool() as pool:
        results = pool.map(euler_generator_worker, [(sets_, set_keys, key) for key in set_keys])
        for result in results:
            for res in result:
                yield res


def euler_parallel(sets: SetsType):
    return dict(euler_generator_parallel(sets))

def euler_func(sets: SetsType):
    """Euler diagram dictionary of set-dictionary of non-repetitive elements

    :param dict sets: array/dict of arrays
    :returns: euler sets
    :rtype: dict
    """
    return dict(euler_generator(sets))

def euler(sets: SetsType, use_clustering: Optional[bool] = None, **kwargs) -> Dict:
    """
    Compute Euler diagram (original function interface).
    Optionally uses clustering for large set systems.
    
    Args:
        sets: Dictionary or list of sets
        use_clustering: If True, use clustering. If None, auto-decide
        **kwargs: Clustering parameters
    
    Returns:
        Dictionary of Euler diagram regions
    """
    e = Euler(sets, use_clustering=use_clustering, **kwargs)
    return e.as_dict()

def euler_keys(
    sets: SetsType
):
    """Euler diagram keys

    :param dict sets: array/dict of arrays
    :returns: euler sets keys
    :rtype: list
    """
    return list(euler_func(sets).keys())

def euler_boundaries(sets):
    """Euler diagram set boundaries

    :param dict sets: array/dict of arrays
    :returns: euler boundary dict
    :rtype: list
    """

    setsKeys = list(sets.keys())
    eulerSetsKeys = euler_keys(sets)

    boundaries = {setKey: [] for setKey in setsKeys}

    for setKey in setsKeys:
        for eulerSetKeys in eulerSetsKeys:
            if setKey in eulerSetKeys:
                this_boundaries = boundaries[setKey]
                ekeys_not_this = difference(eulerSetKeys, [setKey])
                boundaries[setKey] = union(this_boundaries, ekeys_not_this)

    return {\
        setKey: sorted(neighborsKeys) \
        for setKey, neighborsKeys in boundaries.items()\
    }

class Euler:
    def __init__(self, sets: Union[List, Dict], 
                 use_clustering: Optional[bool] = None,
                 method: str = 'leiden',
                 allow_overlap: bool = False,
                 parallel: Optional[bool] = None,
                 **kwargs):
        """
        Initialize Euler diagram with optional clustering.
        
        Args:
            sets: Dictionary or list of sets
            use_clustering: If True, use graph-based clustering. 
                          If None, auto-decide based on set count (>30 sets)
            method: Clustering method ('leiden', 'spectral', 'hierarchical')
            allow_overlap: If True, allow overlapping clusters (sets in multiple clusters)
            parallel: Use parallel computation. If None, auto-decide based on cluster count
            **kwargs: Additional clustering parameters:
                - resolution: float (leiden, default 0.8)
                - overlap_threshold: float (default 0.18)
                - min_bridge_strength: float (default 0.15)
                - max_cluster_size: int (default 30)
                - min_cluster_size: int (default 3)
        """
        # Store original sets
        self.sets = deepcopy(sets)
        
        # Auto-decide clustering
        n_sets = len(sets)
        if use_clustering is None:
            use_clustering = n_sets > 30
        
        self.use_clustering = use_clustering
        self.method = method
        self.allow_overlap = allow_overlap
        self.kwargs = kwargs
        
        # Clustering state
        self.clustering = None
        self.cluster_diagrams = None
        self.metrics = None
        self.overlapping_clustering = None
        self.membership_strengths = None
        
        # Compute Euler diagram
        if use_clustering:
            self._compute_with_clustering(parallel)
        else:
            self.esets = euler_func(sets)
    
    def _compute_with_clustering(self, parallel: Optional[bool] = None):
        """Compute Euler diagram using clustering approach"""
        from .clustering import (SetOverlapGraph, LeidenClustering, 
                                HierarchicalClustering, SpectralBisection,
                                OverlappingClustering, compute_cluster_metrics,
                                rebalance_clusters)
        
        # Build overlap graph
        graph = SetOverlapGraph(self.sets)
        
        # Perform clustering
        if self.allow_overlap:
            clusterer = OverlappingClustering(
                graph,
                overlap_threshold=self.kwargs.get('overlap_threshold', 0.18),
                min_bridge_strength=self.kwargs.get('min_bridge_strength', 0.15)
            )
            self.overlapping_clustering = clusterer.cluster(
                base_resolution=self.kwargs.get('resolution', 0.8)
            )
            self.membership_strengths = clusterer.get_membership_strengths()
            self.clustering = clusterer.get_primary_clustering()
        else:
            if self.method == 'leiden':
                resolution = self.kwargs.get('resolution', 0.8)
                clusterer = LeidenClustering(graph, resolution=resolution)
                self.clustering = clusterer.cluster()
            elif self.method == 'hierarchical':
                max_size = self.kwargs.get('max_cluster_size', 30)
                clusterer = HierarchicalClustering(graph, max_cluster_size=max_size)
                self.clustering = clusterer.cluster()
            elif self.method == 'spectral':
                max_size = self.kwargs.get('max_cluster_size', 30)
                clusterer = HierarchicalClustering(graph, max_cluster_size=max_size)
                self.clustering = clusterer.cluster()
            else:
                raise ValueError(f"Unknown method: {self.method}")
        
        # Rebalance
        max_size = self.kwargs.get('max_cluster_size', 30)
        min_size = self.kwargs.get('min_cluster_size', 3)
        self.clustering = rebalance_clusters(self.sets, self.clustering, max_size, min_size)
        
        # Compute metrics
        self.metrics = compute_cluster_metrics(self.sets, self.clustering)
        
        # Compute Euler diagrams per cluster
        self._compute_cluster_diagrams(parallel)
        
        # Merge into single esets
        self._merge_cluster_diagrams()

    def _compute_cluster_diagrams(self, parallel: Optional[bool] = None):
        """Compute Euler diagram for each cluster"""
        from multiprocessing import Pool
        
        # Get cluster sets
        cluster_sets = self._get_cluster_sets()
        n_clusters = len(cluster_sets)
        
        # Auto-decide parallel
        if parallel is None:
            parallel = n_clusters > 4 and len(self.sets) > 50
        
        # Compute
        if parallel and n_clusters > 1:
            with Pool() as pool:
                results = pool.starmap(
                    _compute_cluster_worker,
                    [(cid, sets) for cid, sets in cluster_sets.items()]
                )
            self.cluster_diagrams = dict(results)
        else:
            self.cluster_diagrams = {}
            for cluster_id, sets in cluster_sets.items():
                self.cluster_diagrams[cluster_id] = euler_func(sets)
    
    def _get_cluster_sets(self) -> Dict[int, Dict]:
        """Get sets grouped by cluster"""
        if self.allow_overlap and self.overlapping_clustering:
            # Overlapping: sets can appear in multiple clusters
            cluster_sets = defaultdict(dict)
            for key in self.sets.keys():
                cluster_ids = self.overlapping_clustering[key]
                for cluster_id in cluster_ids:
                    cluster_sets[cluster_id][key] = self.sets[key]
            return dict(cluster_sets)
        else:
            # Disjoint: each set in one cluster
            cluster_sets = defaultdict(dict)
            for key, cluster_id in self.clustering.items():
                cluster_sets[cluster_id][key] = self.sets[key]
            return dict(cluster_sets)
    
    def _merge_cluster_diagrams(self):
        """Merge cluster diagrams into single esets dict"""
        # For now, flatten with cluster prefix to avoid collisions
        self.esets = {}
        for cluster_id, diagram in self.cluster_diagrams.items():
            for key_tuple, elements in diagram.items():
                # Use original key if no collision, otherwise prefix
                if key_tuple not in self.esets:
                    self.esets[key_tuple] = elements
                else:
                    # Collision - use cluster prefix
                    self.esets[(cluster_id, key_tuple)] = elements

    def __getitem__(self, keys: KeyType):
        """
        Get the elements from the sets associated with the specified keys.

        Parameters:
        keys (tuple or str): The key or keys for accessing the sets.

        Returns:
        list: The union of sets associated with the specified keys.

        If a single key is provided, it returns the elements of the set associated
        with that key. If a tuple of keys is provided, it returns the union of sets
        associated with those keys.
        """

        if not isinstance(keys, tuple):
            try:
                return self.sets[keys]

            except KeyError as error:
                raise KeyError(keys) from error

        else:
            elements: List = []
            try:
                for key in keys:
                    elements=union(self.sets[key], elements)

                return elements
            except KeyError as err:
                keys=str(keys)
                header=f'The keys must be among keys: ({keys}).'

                msg=f'{header}'

                raise KeyError(msg) from err

    def euler_keys(self):
        """
        Get the keys associated with the Euler set representation.

        Returns:
        list: A list of keys corresponding to the Euler set representation.
        """

        return euler_keys(self.sets)

    def euler_boundaries(self):
        """
        Get the boundaries of the Euler set representation.

        Returns:
        tuple: A tuple containing the lower and upper boundaries of the Euler set representation.
        """
        from .operations import difference, union
        
        sets_keys = list(self.sets.keys())
        euler_sets_keys = self.euler_keys()
        
        boundaries = {set_key: [] for set_key in sets_keys}
        
        for set_key in sets_keys:
            for euler_set_keys in euler_sets_keys:
                # Handle both simple keys and cluster-prefixed keys
                if isinstance(euler_set_keys, tuple) and len(euler_set_keys) == 2:
                    if isinstance(euler_set_keys[1], tuple):
                        # Cluster-prefixed: (cluster_id, (key_tuple,))
                        actual_keys = euler_set_keys[1]
                    else:
                        # Regular tuple of keys
                        actual_keys = euler_set_keys
                else:
                    actual_keys = euler_set_keys
                
                if set_key in actual_keys:
                    this_boundaries = boundaries[set_key]
                    ekeys_not_this = difference(actual_keys, [set_key])
                    boundaries[set_key] = union(this_boundaries, ekeys_not_this)
        
        return {
            set_key: sorted(neighbors_keys)
            for set_key, neighbors_keys in boundaries.items()
        }

    def as_dict(self):
        """
        Get the Euler set representation as a dictionary.

        Returns:
        dict: The Euler set representation as a dictionary.
        """

        return self.esets

    def match(self, items: set):
        """
        Match a set of items to the sets in the Euler representation.

        Parameters:
        items (set): A set of items to match against the sets in the Euler representation.

        Returns:
        set: A set of keys corresponding to sets that are subsets of the provided items.

        It checks which sets in the Euler representation are subsets of the provided items
        and returns their keys.
        """

        if not isinstance(items, set):
            raise TypeError("Items must be of type 'set'")

        # Initial value: Empty set
        set_keys=set()

        # Loop along euler set key tuples
        for key, value in self.sets.items():
            intersection_elems=items.intersection(set(value))

            # Match operator produces the non-repeated union of euler keys which
            # has its value set as items subset.
            if(len(intersection_elems)==len(value)):
                set_keys.add(key)


        return set_keys

    def remove_key(self, key):
        """
        Remove a key from the sets in the Euler representation.

        Parameters:
        key: The key to be removed from the sets.

        If the key exists, it is removed from the sets, and the Euler representation is updated.
        If the key doesn't exist, a warning is issued.

        """

        if(key in list(self.sets.keys())):
            self.sets = {
                key_: value \
                for key_, value in self.sets.items() \
                if key_ is not key
            }

            self.esets=euler_func(self.sets)

        else:
            keys=list(self.sets.keys())

            msg1=f'Key {key} is not available on current set.'
            msg2=f'Available keys are: {keys}'

            warn(msg1+' '+msg2)
    
    def get_clustering_info(self) -> Optional[Dict]:
        """Get clustering information if clustering was used"""
        if not self.use_clustering:
            return None
        
        n_clusters = len(set(self.clustering.values()))
        cluster_sizes = defaultdict(int)
        for cluster_id in self.clustering.values():
            cluster_sizes[cluster_id] += 1
        
        info = {
            'method': self.method,
            'n_clusters': n_clusters,
            'cluster_sizes': dict(cluster_sizes),
            'allow_overlap': self.allow_overlap,
        }
        
        if self.allow_overlap and self.overlapping_clustering:
            n_overlapping = sum(1 for clusters in self.overlapping_clustering.values() 
                               if len(clusters) > 1)
            info['n_overlapping_sets'] = n_overlapping
            info['overlapping_sets'] = [
                key for key, clusters in self.overlapping_clustering.items()
                if len(clusters) > 1
            ]
        
        if self.metrics:
            info['metrics'] = {
                cid: {
                    'size': m.size,
                    'intra_overlap': m.intra_overlap,
                    'inter_overlap': m.inter_overlap,
                    'score': m.score()
                }
                for cid, m in self.metrics.items()
            }
        
        return info
    
    def get_bridge_sets(self) -> Optional[Dict[str, List[int]]]:
        """Get sets that connect multiple clusters"""
        if not self.use_clustering:
            return None
        
        bridges = {}
        
        for key in self.sets.keys():
            set_elements = set(self.sets[key])
            own_cluster = self.clustering[key]
            
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
        """Generate summary (enhanced if clustering used)"""
        lines = [f"Euler Diagram"]
        lines.append(f"  Sets: {len(self.sets)}")
        lines.append(f"  Euler regions: {len(self.esets)}")
        
        if self.use_clustering:
            info = self.get_clustering_info()
            lines.append(f"\nClustering:")
            lines.append(f"  Method: {info['method']}")
            lines.append(f"  Clusters: {info['n_clusters']}")
            lines.append(f"  Cluster sizes: {info['cluster_sizes']}")
            
            if self.allow_overlap and info.get('n_overlapping_sets', 0) > 0:
                lines.append(f"  Overlapping sets: {info['n_overlapping_sets']}")
                lines.append(f"  Sets with multiple memberships: {info['overlapping_sets'][:5]}")
            
            if self.metrics:
                lines.append(f"\nCluster Quality:")
                for cid, metric_info in info['metrics'].items():
                    lines.append(
                        f"  Cluster {cid}: size={metric_info['size']}, "
                        f"score={metric_info['score']:.2f}"
                    )
            
            bridges = self.get_bridge_sets()
            if bridges:
                lines.append(f"\nBridge sets: {len(bridges)}")
                for key, clusters in list(bridges.items())[:5]:
                    lines.append(f"  {key} -> clusters {clusters}")
        
        return "\n".join(lines)

    def __repr__(self) -> str:
        """
        Get a string representation of the Euler object.

        Returns:
        str: A string representation of the Euler object in the
        format "Euler({Euler set representation})".
        """
        if self.use_clustering:
            info = self.get_clustering_info()
            return f"Euler(sets={len(self.sets)}, clusters={info['n_clusters']}, regions={len(self.esets)})"
        else:
            return f"Euler(sets={len(self.sets)}, regions={len(self.esets)})"

def _compute_cluster_worker(cluster_id: int, sets: Dict):
    """Worker function for parallel cluster computation"""
    return (cluster_id, euler_func(sets))