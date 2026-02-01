# Eule Examples

This directory contains examples demonstrating how to use the `eule` library for Euler diagram generation and analysis.

## 🚀 Getting Started

**New to eule?** Start with [basic_operations.py](basic_operations.py) to learn the fundamentals.

## Core Functionality

- **[basic_operations.py](basic_operations.py)**: 📚 **START HERE** - Shows the fundamental `euler()` function, generating diagrams from simple discrete sets
- **[set_boundaries.py](set_boundaries.py)**: Demonstrates `euler_boundaries()` to identify which sets share boundaries (neighbors)
- **[advanced_clustering.py](advanced_clustering.py)**: Handle large numbers of sets using clustering (Leiden algorithm) for scalability

## 🌟 Hybrid Analysis Examples (Discrete + Continuous)

These examples demonstrate the powerful combination of **eule** (discrete set analysis) with **interval-sets** (continuous ranges):

### Core Pattern: interval-sets → classify → euler → insights

All hybrid examples follow this pattern:
1. **interval-sets** defines categories using continuous ranges (time windows, value thresholds, quality zones)
2. **Classification** maps discrete elements into these categories
3. **euler()** reveals non-overlapping patterns of category membership
4. **Insights** emerge from understanding which elements share which exact combinations of categories

### 🕐 [hybrid_temporal_events.py](hybrid_temporal_events.py)
**Temporal Pattern Analysis**: Classify discrete events/sessions by continuous time windows

**Examples:**
- Alert Pattern Detection: Which alerts fall into which combinations of time windows (morning shift + maintenance + peak hours)?
- Login Pattern Analysis: User session patterns across work schedule categories
- Fraud Detection: Transaction risk patterns by time + amount thresholds

**Use Cases**: Event analysis, anomaly detection, behavioral patterns

### 💼 [hybrid_customer_segmentation.py](hybrid_customer_segmentation.py)
**Customer Segmentation**: Classify customers by continuous metrics (revenue, satisfaction, tenure)

**Key Insight:** Euler reveals exact multi-dimensional segments:
- High-value detractors (churn risk!)
- New promoters (growth opportunity)
- Stable mid-tier (upsell targets)

**Use Cases**: CRM, marketing automation, retention strategies

### 🏭 [hybrid_quality_analysis.py](hybrid_quality_analysis.py)
**Manufacturing Quality**: Classify production batches by continuous quality metrics

**Key Insight:** Euler reveals correlated defect patterns:
- Which batches fail multiple quality checks simultaneously?
- Are temperature + pH issues correlated?
- Root cause analysis from pattern detection

**Use Cases**: Quality control, process optimization, defect analysis

## Integration with interval-sets

- **[interval_sets_example.py](interval_sets_example.py)**: Basic integration showing temperature ranges, time periods, and project timelines with automatic IntervalSet adaptation

## Running Examples

### Basic Examples (no extra dependencies)
```bash
python examples/basic_operations.py
python examples/set_boundaries.py
python examples/simple_example.py
```

### Clustering Examples (requires numpy)
```bash
pip install numpy
python examples/advanced_clustering.py
```

### Hybrid Examples (requires interval-sets)
```bash
pip install interval-sets
# Or use uv:
uv sync --extra interval

python examples/hybrid_temporal_events.py
python examples/hybrid_customer_segmentation.py
python examples/hybrid_quality_analysis.py
```

## 💡 When to Use Which Approach

| Problem Type | Use | Example |
|-------------|-----|---------|
| Discrete elements only | `eule` alone | Customer categories, product features |
| Continuous ranges only | `interval-sets` alone | Temperature monitoring, time periods |
| **Discrete + Continuous** | **Both together** | Events during time windows, customers by value tiers |
| Large datasets (>30 sets) | `eule` with clustering | Complex category overlaps |
| Spatial regions (2D/3D) | `interval-sets` Box/BoxSet | Geographic boundaries, 3D spaces |

## 📖 Key Concepts

### Why Euler Diagrams?

Euler diagrams partition elements into **non-overlapping regions** based on exact set membership:
```python
euler({'a': [1,2,3], 'b': [2,3,4], 'c': [3,4,5]})
# → {
#     ('a',): [1],           # only in 'a'
#     ('a','b'): [2],        # in 'a' AND 'b', but NOT 'c'
#     ('a','b','c'): [3],    # in all three
#     ('b','c'): [4],        # in 'b' AND 'c', but NOT 'a'
#     ('c',): [5]            # only in 'c'
#   }
```

This reveals **exact overlap patterns** - which combinations of sets actually exist in your data.

### Why Combine with interval-sets?

interval-sets lets you define categories using continuous ranges:
```python
time_windows = {
    'morning': IntervalSet([Interval.closed(6, 14)]),
    'peak': IntervalSet([Interval.closed(9, 11)])
}

# Classify discrete events: which events fall in which windows?
events_by_window = {
    'morning': {event_id for event_id in events if event_times[event_id] in time_windows['morning']},
    'peak': {event_id for event_id in events if event_times[event_id] in time_windows['peak']}
}

# Euler reveals patterns: events ONLY in morning vs events in BOTH morning AND peak
euler(events_by_window)
```

## 📖 Further Reading

- [SetLike Protocol Requirements](../docs/SETLIKE_REQUIREMENTS.md)
- [IntervalSet Compatibility Analysis](../docs/INTERVALSET_COMPATIBILITY.md)
- [Main Documentation](https://eule.readthedocs.io)

