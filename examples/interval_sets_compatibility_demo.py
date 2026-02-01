"""
Demonstration of IntervalSet compatibility issues with Eule and the adapter solution.

This script shows:
1. Why IntervalSet can't directly satisfy SetLike protocol
2. How the adapter solves these issues
3. Practical usage patterns
"""

import sys

try:
    from interval_sets import Interval, IntervalSet
    HAS_INTERVAL_SETS = True
except ImportError:
    HAS_INTERVAL_SETS = False
    print("⚠️  interval-sets library not installed")
    print("Install it with: uv sync --extra interval")
    sys.exit(1)

print("=" * 80)
print("INTERVALSET COMPATIBILITY DEMONSTRATION")
print("=" * 80)

# ============================================================================
# PART 1: Demonstrate the problems with native IntervalSet
# ============================================================================

print("\n" + "=" * 80)
print("PART 1: Problems with Native IntervalSet")
print("=" * 80)

print("\n1. Inconsistent Return Types")
print("-" * 80)

a = IntervalSet([Interval(0, 5)])
b = IntervalSet([Interval(3, 8)])  # Overlapping
c = IntervalSet([Interval(10, 15)])  # Disjoint

result_continuous = a.union(b)
result_disjoint = a.union(c)

print(f"a = {a}")
print(f"b = {b} (overlaps with a)")
print(f"c = {c} (disjoint from a)")
print()
print(f"a.union(b) = {result_continuous}")
print(f"  → Type: {type(result_continuous).__name__}")
print()
print(f"a.union(c) = {result_disjoint}")
print(f"  → Type: {type(result_disjoint).__name__}")
print()
print("❌ Problem: union() returns different types!")
print("   This breaks type protocol requirements.")

print("\n2. Chaining Operations Fails")
print("-" * 80)

try:
    # This works when both are IntervalSet
    x = IntervalSet([Interval(0, 10)])
    y = IntervalSet([Interval(20, 30)])
    z = IntervalSet([Interval(40, 50)])
    
    result = x.union(y).union(z)
    print(f"✅ x.union(y).union(z) = {result}")
    print(f"   Works because all unions return IntervalSet")
except Exception as e:
    print(f"❌ Failed: {e}")

print()

try:
    # This fails when intermediate result is Interval
    x = IntervalSet([Interval(0, 10)])
    y = IntervalSet([Interval(5, 15)])  # Overlaps → returns Interval
    z = IntervalSet([Interval(20, 30)])
    
    result = x.union(y).union(z)
    print(f"✅ x.union(y).union(z) = {result}")
except AttributeError as e:
    print(f"❌ x.union(y).union(z) failed!")
    print(f"   Reason: x.union(y) returns Interval")
    print(f"           Interval.union(z) expects Interval, not IntervalSet")
    print(f"   Error: {e}")

print("\n3. Missing from_iterable()")
print("-" * 80)

print(f"Has from_iterable: {hasattr(IntervalSet, 'from_iterable')}")
print("❌ Required by SetLike protocol")

print("\n4. Empty Check Issues with Interval")
print("-" * 80)

interval = Interval(0, 10)
empty_interval = Interval(0, 0, open_start=True, open_end=True)

print(f"interval = {interval}")
print(f"bool(interval) = {bool(interval)} (should be True)")
print(f"Has __bool__: {hasattr(interval, '__bool__')}")
print()
print(f"empty_interval = {empty_interval}")
print(f"bool(empty_interval) = {bool(empty_interval)} (should be False!)")
print("❌ Interval doesn't implement __bool__() → always returns True")

# ============================================================================
# PART 2: Show how the adapter solves these issues
# ============================================================================

print("\n" + "=" * 80)
print("PART 2: Adapter Solution")
print("=" * 80)

from eule.adapters.interval_sets import IntervalSetAdapter

print("\n1. Type Consistency")
print("-" * 80)

a_wrapped = IntervalSetAdapter(IntervalSet([Interval(0, 5)]))
b_wrapped = IntervalSetAdapter(IntervalSet([Interval(3, 8)]))
c_wrapped = IntervalSetAdapter(IntervalSet([Interval(10, 15)]))

result_continuous = a_wrapped.union(b_wrapped)
result_disjoint = a_wrapped.union(c_wrapped)

print(f"Wrapped a.union(b) = {result_continuous}")
print(f"  → Type: {type(result_continuous).__name__}")
print()
print(f"Wrapped a.union(c) = {result_disjoint}")
print(f"  → Type: {type(result_disjoint).__name__}")
print()
print("✅ Both return IntervalSetAdapter!")
print("   Type consistency maintained.")

print("\n2. Operation Chaining Works")
print("-" * 80)

x = IntervalSetAdapter(IntervalSet([Interval(0, 10)]))
y = IntervalSetAdapter(IntervalSet([Interval(5, 15)]))
z = IntervalSetAdapter(IntervalSet([Interval(20, 30)]))

result = x.union(y).union(z)
print(f"✅ x.union(y).union(z) = {result}")
print(f"   Chaining works because adapter normalizes return types")

print("\n3. from_iterable() Available")
print("-" * 80)

intervals = [Interval(0, 5), Interval(10, 15), Interval(20, 25)]
created = IntervalSetAdapter.from_iterable(intervals)
print(f"Created from iterable: {created}")
print(f"✅ from_iterable() classmethod works")

print("\n4. Boolean Check Works")
print("-" * 80)

empty_wrapped = IntervalSetAdapter(IntervalSet())
non_empty_wrapped = IntervalSetAdapter(IntervalSet([Interval(0, 5)]))

print(f"empty_wrapped: {empty_wrapped}")
print(f"bool(empty_wrapped) = {bool(empty_wrapped)}")
print()
print(f"non_empty_wrapped: {non_empty_wrapped}")
print(f"bool(non_empty_wrapped) = {bool(non_empty_wrapped)}")
print("✅ Boolean checks work correctly")

# ============================================================================
# PART 3: Using with Eule
# ============================================================================

print("\n" + "=" * 80)
print("PART 3: Usage with Eule")
print("=" * 80)

from eule import euler

print("\n❌ Attempting with native IntervalSet (will fail):")
print("-" * 80)

try:
    native_sets = {
        'cold': IntervalSet([Interval(0, 15)]),
        'moderate': IntervalSet([Interval(10, 25)]),
        'hot': IntervalSet([Interval(20, 40)])
    }
    diagram = euler(native_sets)
    print("✅ Surprisingly worked! (but results may be incorrect)")
    for region, elements in diagram.items():
        print(f"  {region}: {elements}")
except Exception as e:
    print(f"❌ Failed: {type(e).__name__}: {e}")

print("\n✅ Using IntervalSetAdapter:")
print("-" * 80)

try:
    wrapped_sets = {
        'cold': IntervalSetAdapter(IntervalSet([Interval(0, 15)])),
        'moderate': IntervalSetAdapter(IntervalSet([Interval(10, 25)])),
        'hot': IntervalSetAdapter(IntervalSet([Interval(20, 40)]))
    }
    diagram = euler(wrapped_sets)
    print("✅ Success! Euler diagram computed:")
    for region, elements in sorted(diagram.items()):
        print(f"  {region}: {list(elements)}")
except Exception as e:
    print(f"❌ Failed: {type(e).__name__}: {e}")

# ============================================================================
# PART 4: Performance Comparison
# ============================================================================

print("\n" + "=" * 80)
print("PART 4: Adapter Overhead")
print("=" * 80)

import time

# Native operations
sets_native = [IntervalSet([Interval(i, i+10)]) for i in range(0, 100, 5)]

start = time.time()
result = sets_native[0]
for s in sets_native[1:]:
    try:
        result = result.union(s)
        if isinstance(result, Interval):
            result = IntervalSet([result])
    except:
        break
native_time = time.time() - start

# Wrapped operations
sets_wrapped = [IntervalSetAdapter(IntervalSet([Interval(i, i+10)])) for i in range(0, 100, 5)]

start = time.time()
result = sets_wrapped[0]
for s in sets_wrapped[1:]:
    result = result.union(s)
wrapped_time = time.time() - start

print(f"Native operations:  {native_time*1000:.3f} ms")
print(f"Wrapped operations: {wrapped_time*1000:.3f} ms")
print(f"Overhead: {((wrapped_time/native_time - 1) * 100):.1f}%")

print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)
print("""
IntervalSet CANNOT directly implement Eule's SetLike protocol due to:
  1. ❌ Inconsistent return types (Interval vs IntervalSet)
  2. ❌ Missing from_iterable() classmethod
  3. ❌ Interval class lacks __bool__() method
  
The IntervalSetAdapter SOLVES these issues by:
  1. ✅ Normalizing all results to IntervalSetAdapter
  2. ✅ Providing from_iterable() classmethod
  3. ✅ Implementing proper __bool__() behavior
  4. ✅ Enabling operation chaining
  
Use IntervalSetAdapter when working with eule!
""")

print("\nExample usage:")
print("-" * 80)
print("""
from eule import euler
from eule.adapters.interval_sets import IntervalSetAdapter
from interval_sets import Interval, IntervalSet

# Wrap your IntervalSets
sets = {
    'A': IntervalSetAdapter(IntervalSet([Interval(0, 10)])),
    'B': IntervalSetAdapter(IntervalSet([Interval(5, 15)])),
}

# Use with eule
diagram = euler(sets)
""")
