# interval-sets Integration Issue

## Problem
The `interval-sets` package (v0.1.2) on PyPI has a broken wheel distribution that only contains metadata without the actual Python modules.

## Root Cause
The wheel file (4.1 KB) only contains:
- `interval_sets-0.1.2.dist-info/METADATA`
- `interval_sets-0.1.2.dist-info/WHEEL`
- `interval_sets-0.1.2.dist-info/top_level.txt`
- `interval_sets-0.1.2.dist-info/RECORD`

But missing all `.py` module files from `src/` directory.

## Workaround
Until the package maintainers fix the PyPI release:

1. Install from GitHub source directly:
   ```bash
   pip install git+https://github.com/ourstudio-se/interval-sets.git
   ```

2. Or use eule with regular Python sets, lists, or other set-like objects

## Status
The eule adapter for interval-sets (`eule/adapters/interval_sets.py`) is implemented and tested, but cannot be demonstrated with the PyPI package until this packaging issue is resolved.

## Related
- PyPI Package: https://pypi.org/project/interval-sets/
- Example: `examples/interval_sets_example.py`
- Adapter: `eule/adapters/interval_sets.py`
