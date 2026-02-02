# Eule Examples

This directory contains examples demonstrating how to use the `eule` library for Euler diagram generation and analysis.

## 🚀 Fundamentals

- **[basics.py](basics.py)**: 📚 **Start Here** - Fundamental set operations, generating diagrams from simple discrete sets.
- **[boundaries.py](boundaries.py)**: Demonstrates `euler_boundaries()` to identify which sets share boundaries (topology).

## 🔬 Advanced Library Features

- **[clustering.py](clustering.py)**: Handle large datasets (>30 sets) using the Leiden clustering algorithm.
- **[intervals.py](intervals.py)**: Native integration with `interval-sets` for continuous range analysis.
- **[spatial.py](spatial.py)**: **Multi-dimensional** analyis using 2D/3D `BoxSet` objects to find overlapping spatial zones.

## 💼 Real-World Case Studies

These examples demonstrate the "Hybrid Pattern": **Define** (Intervals) → **Classify** (Discrete) → **Analyze** (Euler).

- **[case_temporal_events.py](case_temporal_events.py)**: 🕐 **Temporal Analysis** - Classify discrete events (logs, logins) into continuous time windows (shifts, maintenance windows) to find coverage gaps and overlaps.
- **[case_customer_segmentation.py](case_customer_segmentation.py)**: 👥 **Business Intelligence** - Segment customers by continuous metrics (Revenue, Tenure) to find "High Value Detractors" or "New Promoters".
- **[case_quality_analysis.py](case_quality_analysis.py)**: 🏭 **Manufacturing** - Analyze production batches against continuous quality control limits (Temp, Pressure) to find correlated defect patterns.
- **[case_genomics.py](case_genomics.py)**: 🧬 **Bioinformatics** - Identify functional genomic regions (e.g., Active Promoters) by finding overlaps between open chromatin, promoters, and enhancers on a chromosome.
- **[case_scatter_hulls.py](case_scatter_hulls.py)**: 🐾 **Ecology / Spatial** - Uses `Shapely` to compute Convex Hulls from scatter points (e.g., animal GPS tracks) and finds territory overlaps (Predation Zones).
- **[case_3d_clash_detection.py](case_3d_clash_detection.py)**: 🏗️ **Engineering / BIM** - Uses 3D `Box` objects to find volumetric collisions between Beams, HVAC, and Zones.
- **[case_scheduling.py](case_scheduling.py)**: 🗓️ **Productivity** - Solves the "common free time" problem across multiple calendars using 1D Intervals.
- **[case_nlp_stylometry.py](case_nlp_stylometry.py)**: 📜 **Data Science / NLP** - Analyzes vocabulary overlap between different texts using standard discrete sets.
- **[case_network_security.py](case_network_security.py)**: 🛡️ **NetOps / Security** - Audit firewall rules by treating IP ranges (CIDR blocks) as intervals. Identifies security risks like "Malicious IPs overlapping with Allowed VPN Access".

## 🧠 Theoretical Background

- **[theory_intervals_vs_sets.py](theory_intervals_vs_sets.py)**: A deep dive into why `interval-sets` (continuous) and `eule` (discrete) are different paradigms and how the adapter bridges them.
- **[custom_protocol_infinite_sets.py](custom_protocol_infinite_sets.py)**: Demonstrates the flexibility of the `SetLike` protocol by implementing infinite sets (Modulo Arithmetic) without using external libraries. Shows how **any** object can be analyzed by `eule` if it implements `union`, `intersection`, and `difference`.

## 🎨 Visualization

These scripts use `matplotlib` to visually demonstrate the Euler diagram outputs:

- **[visualize_spatial.py](visualize_spatial.py)**: Visualizes the `spatial.py` example, plotting original 2D overlapping zones vs computed disjoint regions.
- **[visualize_genomics.py](visualize_genomics.py)**: Visualizes the `case_genomics.py` example, showing genomic tracks (peaks, promoters) and the computed functional annotations.

## 💡 Quick Reference

| Problem Type            | Example Script                  |
| ----------------------- | ------------------------------- |
| **Simple Sets**         | `basics.py`                     |
| **Big Data (>50 sets)** | `clustering.py`                 |
| **Time Windows**        | `case_temporal_events.py`       |
| **Space / Regions**     | `spatial.py`                    |
| **Business Rules**      | `case_customer_segmentation.py` |
| **Visualizations**      | `visualize_*.py`                |
