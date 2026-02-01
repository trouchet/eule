# Coverage Gaps Analysis: clustering.py, core.py, registry.py

**Date**: February 1, 2026  
**Current Coverage**: clustering.py (85%), core.py (99%), registry.py (96%)

---

## 1. core.py (99% - Missing 4 statements, 3 branches)

### Gap 1: Lines 137-138 - Exception Handling in Deduplication
```python
137.    except (TypeError, AttributeError):
138.        is_unique_set_arr.append(True)
```

**Context**: Hash-checking for deduplication when objects aren't hashable  
**Reason Uncovered**: Rare case where objects can't be hashed  
**To Cover**: Pass non-hashable objects that raise TypeError/AttributeError on hash()

### Gap 2: Line 534 - Alternative Key Path
```python
534.    actual_keys = euler_set_keys[1]
```

**Context**: Inside complex conditional in euler_generator  
**Reason Uncovered**: Specific branch in key handling logic  
**To Cover**: Test case where euler_set_keys has specific structure

### Gap 3: Line 739 - Parallel Helper Function
```python
739.    return (cluster_id, euler_func(sets))
```

**Context**: Worker function for parallel processing  
**Reason Uncovered**: Parallel execution path not directly called  
**To Cover**: Already tested via parallel execution, branch coverage issue

### Gap 4: Lines 648-659, 707-715 - Metrics Display
```python
648-659.    if self.metrics:
                # Display metrics info
707-715.    if self.metrics:
                # Format metrics for summary
```

**Context**: Clustering metrics display in info/summary  
**Reason Uncovered**: Tests don't access metrics property  
**To Cover**: Test ClusteredEuler.info() and .summary() with metrics

**Severity**: LOW - All are edge cases or already indirectly tested

---

## 2. registry.py (96% - Missing 2 statements, 1 branch)

### Gap 1: Lines 112-114 - Detection Rule Match
```python
112.    if predicate(obj):
113.        self._cache[obj_type] = adapter_factory
114.        return adapter_factory(obj)
```

**Context**: When a custom detection rule matches  
**Reason Uncovered**: Tests don't register custom detection rules  
**To Cover**: Test register_detector() with a custom detector

### Gap 2: Lines 152-154 - Protocol Check TypeError
```python
152.    except TypeError:
153.        # Protocol check can raise TypeError in some cases
154.        return False
```

**Context**: Edge case in protocol checking  
**Reason Uncovered**: Rare TypeError during isinstance check with Protocol  
**To Cover**: Pass object that raises TypeError in isinstance()

**Severity**: LOW - Error handling paths for rare cases

---

## 3. clustering.py (85% - Missing 70 statements, 16 branches)

### High-Value Gaps (Can be easily covered)

#### Gap 1: Lines 188-192 - Disconnected Component Handling
```python
188.    components.sort(key=len, reverse=True)
189.    for comp in components[1:]:
190.        for node in comp:
191.            self.clusters[node] = new_cluster_id
192.        new_cluster_id += 1
```

**Context**: Leiden clustering with multiple disconnected components  
**Reason Uncovered**: Tests don't create graphs with 2+ disconnected components  
**To Cover**: Create graph with 3+ separate components, trigger sorting

#### Gap 2: Lines 265-268 - Max Cluster Size Splitting
```python
265.    for key in keys:
266.        clusters[key] = cluster_id
267.    cluster_id += 1
268.    return
```

**Context**: Hierarchical clustering splitting oversized clusters  
**Reason Uncovered**: Tests don't trigger the split path with early return  
**To Cover**: Create cluster that needs splitting with max_cluster_size

#### Gap 3: Line 482 - List Input Conversion
```python
482.    self.sets = {i: s for i, s in enumerate(sets)}
```

**Context**: ClusteredEuler receiving list instead of dict  
**Reason Uncovered**: All tests pass dicts  
**To Cover**: Pass list to ClusteredEuler

#### Gap 4: Lines 590-591 - Parallel Worker Path
```python
590.    diagram = euler(sets)
591.    return (cluster_id, diagram)
```

**Context**: Worker function for parallel diagram computation  
**Reason Uncovered**: Branch not directly executed in tests  
**To Cover**: Already tested via parallel=True, branch coverage issue

#### Gap 5: Lines 628-630 - Invalid Cluster ID
```python
628.    if cluster_id not in self.cluster_diagrams:
629.        raise ValueError(f"Cluster {cluster_id} not found")
630.    return self.cluster_diagrams[cluster_id]
```

**Context**: Error handling in get_cluster_euler  
**Reason Uncovered**: Tests don't request invalid cluster IDs  
**To Cover**: Call get_cluster_euler(999) with non-existent ID

#### Gap 6: Lines 648-651 - Euler Dict Formatting
```python
648.    flat[(cluster_id, key_tuple)] = elements
649.    return flat
650.else:
651.    return self.global_euler
```

**Context**: as_euler_dict with flatten=True/False  
**Reason Uncovered**: Tests don't call as_euler_dict  
**To Cover**: Test both flatten modes

#### Gap 7: Lines 660-661 - Euler Object Conversion
```python
660.    euler_dict = self.as_euler_dict(flatten=flatten)
661.    return Euler(euler_dict)
```

**Context**: as_euler() method  
**Reason Uncovered**: Tests don't call as_euler()  
**To Cover**: Call ce.as_euler()

#### Gap 8: Line 721 - Bridge Elements Display
```python
721.    lines.append(f"\nBridge elements: {len(self.bridge_elements)}")
```

**Context**: Summary with bridge elements  
**Reason Uncovered**: Tests check summary exists but not this specific path  
**To Cover**: Test summary() when bridge_elements exist

### Low-Value Gaps (Example/Demo code)

#### Gap 9: Lines 800-809 - Overlapping Clustering
```python
800-809.    if not self.allow_overlap:
                return super().get_cluster_sets()
            # Overlapping cluster logic
```

**Context**: ClusteredEulerOverlapping class features  
**Reason Uncovered**: Advanced feature, tests don't use overlapping mode  
**To Cover**: Test ClusteredEulerOverlapping class

#### Gap 10: Lines 814, 843, 847 - Overlapping Info
```python
814.    return {"overlapping": False}
843.    overlap_info.append(...)
847.    return base
```

**Context**: Info/summary for overlapping clustering  
**Reason Uncovered**: Advanced feature not tested  
**To Cover**: Test ClusteredEulerOverlapping.info()

#### Gap 11: Lines 877-945 - Example Usage Function ⚠️
```python
877-945.    def example_usage():
                """Complete example demonstrating the system"""
                # 70 lines of demo code
```

**Context**: Demonstration/documentation function  
**Reason Uncovered**: Not production code, just examples  
**Severity**: N/A - Should add `# pragma: no cover`

#### Gap 12: Line 949 - Main Block
```python
949.    example_usage()
```

**Context**: if __name__ == '__main__' block  
**Reason Uncovered**: Not executed during tests  
**Severity**: N/A - Should add `# pragma: no cover`

---

## Summary Table

| File | Current | Gaps | Easy Fixes | Impact |
|------|---------|------|------------|--------|
| **core.py** | 99% | 4 lines | 2-3 tests | +0.5% → 99.5% |
| **registry.py** | 96% | 3 lines | 2 tests | +3% → 99% |
| **clustering.py** | 85% | 70 lines | 10 tests | +8% → 93% |

### High-Value Targets (Best ROI)

1. **registry.py** - 2 simple tests → +3% coverage
2. **clustering.py (lines 265-268, 482, 628-630, 648-661, 721)** - 5 tests → +5% coverage
3. **clustering.py (lines 877-945, 949)** - Add pragma: no cover → +5% coverage
4. **core.py (lines 137-138, 534)** - 2 tests → +0.5% coverage

### Expected Results After Fixes

| Module | Before | After | Effort |
|--------|--------|-------|--------|
| registry.py | 96% | 99% | 10 min |
| clustering.py | 85% | 93% | 20 min |
| core.py | 99% | 99.5% | 10 min |
| **Overall** | **88%** | **~92%** | **40 min** |

---

## Recommendations

### Priority 1: Quick Wins (15 minutes)
1. Add `# pragma: no cover` to example_usage() function
2. Add `# pragma: no cover` to if __name__ == '__main__' block
   → **Instant +5% clustering coverage**

### Priority 2: High-Value Tests (25 minutes)
3. Test registry.register_detector() with custom rule
4. Test ClusteredEuler with list input (not dict)
5. Test ClusteredEuler.get_cluster_euler() with invalid ID
6. Test ClusteredEuler.as_euler_dict(flatten=True/False)
7. Test ClusteredEuler.as_euler() method
8. Test max_cluster_size splitting with early return
   → **+7% coverage across files**

### Priority 3: Edge Cases (Optional)
9. Test non-hashable object deduplication in core.py
10. Test protocol TypeError exception in registry.py
11. Test ClusteredEulerOverlapping features
    → **+1% coverage, diminishing returns**

---

## Next Steps

Would you like me to:
1. ✅ **Add pragma: no cover to example code** (instant +5%)
2. ✅ **Implement Priority 2 tests** (20 min, +7%)
3. ⏸️  **Implement Priority 3 edge cases** (optional)

This would bring us to **~92% overall coverage** with minimal effort!
