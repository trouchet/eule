# Hybrid Examples Guide: Combining Eule + Interval-Sets

## 🎯 Overview

This guide explains how to leverage both **eule** (discrete set analysis) and **interval-sets** (continuous range operations) together to solve complex real-world problems.

## 🧩 The Power of Combination

| Library | Strengths | Best For |
|---------|-----------|----------|
| **eule** | Discrete set partitioning, overlap detection | Categories, groups, items you can list |
| **interval-sets** | Continuous ranges, boundary precision | Thresholds, time windows, measurements |
| **Both Together** | Hybrid classification & analysis | Events in time, categories with metrics |

## 📚 Implemented Examples

### 1. Temporal Event Analysis 🕐
**File**: `examples/hybrid_temporal_events.py`

**Scenario**: You have discrete events happening at specific times, and continuous time windows representing availability, maintenance, or business hours.

**Examples in the file**:
- **Sensor Events**: Classify temperature/pressure alerts by maintenance window
- **User Activity**: Analyze actions during business vs off-hours
- **Coverage Gaps**: Detect events that fell during monitoring outages  
- **Meeting Scheduling**: Check attendee availability for proposed meetings

**Key Pattern**:
```python
# Discrete events
events = {'sensor_a': {2.5, 8.5, 16.5, 22.0}}

# Continuous windows
windows = {
    'morning': IntervalSet([Interval(6, 10)]),
    'evening': IntervalSet([Interval(18, 22)])
}

# Classify: which events happened when?
def classify(events, windows):
    result = {}
    for event_type, times in events.items():
        for window_name, window_range in windows.items():
            in_window = {t for t in times if t in window_range}
            if in_window:
                result[f"{event_type}_during_{window_name}"] = in_window
    return result
```

**When to use**: Time-series analysis, activity tracking, schedule optimization

---

### 2. Categorical + Continuous Classification 📊
**File**: `examples/hybrid_categorical_continuous.py`

**Scenario**: You have discrete categories (customer groups, product features) and continuous metrics (prices, scores, ratings) that define thresholds.

**Examples in the file**:
- **Customer Segmentation**: Electronics/books buyers × premium/standard/budget tiers
- **Product Recommendations**: Laptop features × price ranges
- **Student Performance**: Course enrollment × test score thresholds

**Key Pattern**:
```python
# Discrete categories
customers = {
    'electronics': {'alice', 'bob', 'emma'},
    'books': {'alice', 'carol', 'frank'}
}

# Customer values (continuous)
values = {'alice': 1250, 'bob': 380, ...}

# Value tiers (continuous ranges)
tiers = {
    'premium': IntervalSet([Interval(1000, inf)]),
    'standard': IntervalSet([Interval(100, 1000)])
}

# Classify customers by tier
tier_classification = {}
for tier_name, tier_range in tiers.items():
    tier_classification[tier_name] = {
        c for c, v in values.items() if v in tier_range
    }

# Combine and analyze overlaps
combined = {**customers, **tier_classification}
diagram = euler(combined)
```

**When to use**: Business intelligence, segmentation, recommendation engines

---

### 3. Coverage & Gap Analysis 📈
**File**: `examples/hybrid_coverage_analysis.py`

**Scenario**: You have discrete data points (customers, sensor readings, requests) and continuous coverage regions (service areas, monitoring periods, quality zones).

**Examples in the file**:
- **Service Coverage**: Postal codes × provider coverage areas
- **Data Quality**: Sensor readings × monitoring uptime windows
- **Manufacturing QA**: Temperature readings × quality zones

**Key Pattern**:
```python
# Expected coverage (continuous)
expected = IntervalSet([Interval(0, 24)])

# Actual coverage (continuous with gaps)
actual = IntervalSet([
    Interval(0, 8),
    Interval(10, 15),
    Interval(17, 24)
])

# Find gaps
gaps = actual.complement(expected)

# Discrete events
events = {2, 5, 7, 9, 11, 14, 16, 18, 22}

# Check which events fell in gaps
missed = {e for e in events if e in gaps}
captured = {e for e in events if e in actual}

print(f"Coverage: {actual.measure() / expected.measure() * 100:.1f}%")
print(f"Missed events: {missed}")
```

**When to use**: Quality assurance, operational monitoring, compliance validation

## 🔧 Common Helper Patterns

### Pattern 1: Classify Discrete Elements by Continuous Ranges
```python
def classify_by_ranges(elements, element_values, ranges):
    """Map discrete elements to continuous range categories."""
    classification = {}
    for range_name, range_set in ranges.items():
        classification[range_name] = {
            elem for elem, val in element_values.items()
            if val in range_set
        }
    return classification

# Usage
customers = {'alice': 1500, 'bob': 250, 'carol': 50}
tiers = {
    'premium': IntervalSet([Interval(1000, inf)]),
    'budget': IntervalSet([Interval(0, 100)])
}
result = classify_by_ranges(customers.keys(), customers, tiers)
# {'premium': {'alice'}, 'budget': {'carol'}}
```

### Pattern 2: Filter Discrete Events by Continuous Windows
```python
def events_in_windows(event_dict, window_dict):
    """Classify discrete events by which windows they fall in."""
    result = {}
    for event_name, event_times in event_dict.items():
        for window_name, window_range in window_dict.items():
            times_in_window = {t for t in event_times if t in window_range}
            if times_in_window:
                key = f"{event_name}_during_{window_name}"
                result[key] = times_in_window
    return result

# Usage
events = {'alerts': {2, 8, 16, 22}}
windows = {
    'morning': IntervalSet([Interval(6, 12)]),
    'evening': IntervalSet([Interval(18, 24)])
}
result = events_in_windows(events, windows)
# {'alerts_during_morning': {8}, 'alerts_during_evening': {22}}
```

### Pattern 3: Coverage Gap Analysis
```python
def analyze_coverage(discrete_points, actual_coverage, expected_coverage):
    """Analyze coverage quality for discrete points."""
    gaps = actual_coverage.complement(expected_coverage)
    
    covered = {p for p in discrete_points if p in actual_coverage}
    in_gaps = {p for p in discrete_points if p in gaps}
    
    coverage_pct = (actual_coverage.measure() / expected_coverage.measure()) * 100
    
    return {
        'coverage_percent': coverage_pct,
        'gaps': gaps,
        'gap_duration': gaps.measure(),
        'points_covered': covered,
        'points_missed': in_gaps,
        'quality_score': len(covered) / len(discrete_points) * 100
    }

# Usage
points = {2, 5, 9, 11, 16, 18, 22}
actual = IntervalSet([Interval(0, 8), Interval(10, 15), Interval(17, 24)])
expected = IntervalSet([Interval(0, 24)])

metrics = analyze_coverage(points, actual, expected)
# {'coverage_percent': 70.8, 'points_missed': {9, 16}, ...}
```

## 🚀 Quick Start Examples

### Example A: Time-Based Event Classification
```python
from interval_sets import Interval, IntervalSet
from eule import euler

# Events at specific times
alerts = {
    'critical': {2.5, 8.5, 22.0},
    'warning': {5.0, 12.0, 16.5}
}

# Time windows
periods = {
    'maintenance': IntervalSet([Interval(6, 10), Interval(18, 22)])
}

# Classify
classified = {}
for alert_type, times in alerts.items():
    for period_name, period_range in periods.items():
        in_period = {t for t in times if t in period_range}
        if in_period:
            classified[f"{alert_type}_{period_name}"] = in_period

print(classified)
# {'critical_maintenance': {8.5, 22.0}, 'warning_maintenance': {5.0}}
```

### Example B: Threshold-Based Segmentation
```python
from interval_sets import Interval, IntervalSet
from eule import euler

# Products with features
products = {
    'wireless': {'laptop_a', 'laptop_b'},
    'gaming': {'laptop_a', 'laptop_c'}
}

# Prices
prices = {'laptop_a': 1599, 'laptop_b': 899, 'laptop_c': 2199}

# Price tiers
tiers = {
    'premium': IntervalSet([Interval(1500, float('inf'))]),
    'mid_range': IntervalSet([Interval(800, 1500)])
}

# Classify by price
price_segments = {
    tier: {p for p, price in prices.items() if price in range_}
    for tier, range_ in tiers.items()
}

# Combine
all_segments = {**products, **price_segments}
diagram = euler(all_segments)

# Find premium wireless laptops
premium_wireless = diagram.get(('wireless', 'premium'), set())
print(f"Premium wireless: {premium_wireless}")
```

### Example C: Coverage Validation
```python
from interval_sets import Interval, IntervalSet

# Expected 24-hour coverage
expected = IntervalSet([Interval(0, 24)])

# Actual uptime (with gaps)
actual = IntervalSet([Interval(0, 8), Interval(10, 20)])

# Data collected
readings = {1, 3, 5, 7, 9, 11, 15, 18, 21, 23}

# Find gaps
gaps = actual.complement(expected)

# Analyze
covered = {r for r in readings if r in actual}
missed = {r for r in readings if r in gaps}

print(f"Uptime: {actual.measure()/24*100:.1f}%")
print(f"Readings: {len(covered)}/{len(readings)} captured")
print(f"Gaps: {gaps}")
print(f"Missed readings: {sorted(missed)}")
# Uptime: 75.0%
# Readings: 7/10 captured  
# Gaps: {(8, 10), (20, 24]}
# Missed readings: [9, 21, 23]
```

## 📖 Best Practices

### ✅ DO
- Use eule for discrete category overlaps
- Use interval-sets for continuous range operations
- Combine for hybrid discrete+continuous problems
- Create clear helper functions for common patterns
- Document which domain each variable belongs to

### ❌ DON'T
- Try to enumerate elements from IntervalSet
- Use eule alone for pure continuous analysis
- Over-discretize continuous data (loses precision)
- Mix discrete and continuous without clear conversion

## 🎓 Learning Path

1. **Start simple**: Run `basic_operations.py` to learn eule basics
2. **Add intervals**: Try `interval_sets_example.py` for basic integration
3. **Go hybrid**: Choose one of the 3 hybrid examples matching your use case
4. **Adapt**: Modify the example pattern for your specific problem
5. **Optimize**: Use helper functions to keep code clean

## 📊 Choosing the Right Approach

```
Your Problem
    |
    ├─ Only discrete elements? 
    |    └─> Use eule alone
    |
    ├─ Only continuous ranges?
    |    └─> Use interval-sets alone
    |
    └─ Both discrete AND continuous?
         |
         ├─ Events in time windows?
         |    └─> Use hybrid_temporal_events.py pattern
         |
         ├─ Categories with metric thresholds?
         |    └─> Use hybrid_categorical_continuous.py pattern
         |
         └─ Coverage/gap analysis?
              └─> Use hybrid_coverage_analysis.py pattern
```

## 🔗 Additional Resources

- [Integration Opportunities Document](INTEGRATION_OPPORTUNITIES.md)
- [SetLike Protocol Requirements](SETLIKE_REQUIREMENTS.md)
- [IntervalSet Compatibility Analysis](INTERVALSET_COMPATIBILITY.md)
- [Eule Documentation](https://eule.readthedocs.io)
- [Interval-Sets Repository](https://github.com/brunolnetto/interval-sets)

## 💬 Support

Questions? Check:
1. The example files for complete working code
2. The integration opportunities document for design patterns
3. GitHub issues for both repositories
4. Documentation sites for API reference

---

**Remember**: The power comes from using each library for what it does best, then combining their results for comprehensive analysis.
