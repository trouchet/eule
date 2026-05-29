# Changelog

All notable changes to this project will be documented in this file.

## [1.5.0] - 2026-02-06

### Added
- **Spider Logic Extension**: Implementation of Spider Diagrams for formal logical reasoning.
- **Spider Class**: New entity to handle spatial ambiguity, "leg-landing" rationale, and R-sets (complements).
- **Euler.spiders()**: Method to generate the spider-set space ($2^m-1$ cardinality) from an Euler diagram.
- **Generator-based Combinatorics**: Memory-efficient $O(1)$ generation of large combinatorial spaces.
- **New Example**: `case_spider_logic.py` demonstrating formal reasoning and R-set calculation.

## [1.4.0] - 2026-02-01

### Added
- **Universal Adapters**: Eule now supports arbitrary objects via the `SetLike` protocol.
- **Interval Support**: Built-in adapter for `interval-sets` to analyze continuous ranges (timelines, values).
- **Geometry Support**: Built-in adapter for `shapely` to analyze 2D/3D shapes and polygons.
- **3D Box Support**: Adapter for high-dimensional box sets.
- **New Examples**:
  - `case_scatter_hulls.py`: Ecological territory analysis using Convex Hulls.
  - `case_3d_clash_detection.py`: 3D engineering clash detection.
  - `case_scheduling.py`: Team calendar scheduling.
  - `case_nlp_stylometry.py`: Text vocabulary analysis.

### Changed
- Refactored `eule` core to rely on `SetLike` protocol detection.
- Updated documentation to reflect multi-domain capabilities.

## [1.3.0] - Previous
- Initial discrete set support.
