#!/usr/bin/env python3
"""
Hybrid Example: Manufacturing Quality Analysis

Demonstrates:
- Discrete production batches classified by quality metrics
- Continuous quality zones define pass/fail criteria via interval-sets
- Euler diagrams reveal defect patterns across multiple dimensions

Pattern: interval-sets → classify → euler → root cause analysis
"""

try:
    from interval_sets import Interval, IntervalSet
    from eule import euler
    
    print("=" * 80)
    print("🏭 Quality Analysis: Batches × Continuous Quality Metrics")
    print("=" * 80)
    print()
    
    # ============================================================================
    # DISCRETE ELEMENTS: Production Batches
    # ============================================================================
    batches = [f"batch_{i:04d}" for i in range(1, 101)]
    
    # Quality metrics (continuous measurements)
    import random
    random.seed(42)
    batch_temperature = {b: random.uniform(15, 35) for b in batches}
    batch_pressure = {b: random.uniform(95, 105) for b in batches}
    batch_ph_level = {b: random.uniform(6.5, 8.5) for b in batches}
    batch_viscosity = {b: random.uniform(80, 120) for b in batches}
    
    # ============================================================================
    # CONTINUOUS QUALITY ZONES: Defined using interval-sets
    # ============================================================================
    quality_zones = {
        # Temperature (Celsius)
        'temp_optimal': IntervalSet([Interval.closed(20, 25)]),
        'temp_acceptable': IntervalSet([Interval.closed(18, 28)]),
        'temp_warning': IntervalSet([
            Interval.closed(15, 18), Interval.closed(28, 35)
        ]),
        
        # Pressure (PSI)
        'pressure_optimal': IntervalSet([Interval.closed(98, 102)]),
        'pressure_warning': IntervalSet([
            Interval.closed(95, 98), Interval.closed(102, 105)
        ]),
        
        # pH Level
        'ph_optimal': IntervalSet([Interval.closed(7.0, 7.5)]),
        'ph_acidic': IntervalSet([Interval.closed(6.5, 7.0)]),
        'ph_basic': IntervalSet([Interval.closed(7.5, 8.5)]),
        
        # Viscosity
        'viscosity_optimal': IntervalSet([Interval.closed(95, 105)])
    }
    
    print("Sample Batch Measurements:")
    for batch in batches[:5]:
        print(f"  {batch}: Temp={batch_temperature[batch]:.1f}°C, "
              f"Pressure={batch_pressure[batch]:.1f}PSI, "
              f"pH={batch_ph_level[batch]:.2f}, "
              f"Viscosity={batch_viscosity[batch]:.1f}")
    print(f"  ... ({len(batches)} batches total)")
    
    print("\nQuality Zone Definitions:")
    print("  Temperature Zones:")
    for zone in ['temp_optimal', 'temp_acceptable', 'temp_warning']:
        print(f"    {zone:20s}: {quality_zones[zone]}")
    
    # ============================================================================
    # CLASSIFICATION: Map batches to quality zones
    # ============================================================================
    def classify_batches(batches_list, metric_values, zones_dict):
        """Classify batches into quality zones based on measurements."""
        return {
            zone_name: {
                batch for batch in batches_list
                if metric_values[batch] in zone_range
            }
            for zone_name, zone_range in zones_dict.items()
        }
    
    # Classify by each metric
    temp_classification = {
        'temp_optimal': {b for b in batches if batch_temperature[b] in quality_zones['temp_optimal']},
        'temp_warning': {b for b in batches if batch_temperature[b] in quality_zones['temp_warning']}
    }
    
    pressure_classification = {
        'pressure_optimal': {b for b in batches if batch_pressure[b] in quality_zones['pressure_optimal']},
        'pressure_warning': {b for b in batches if batch_pressure[b] in quality_zones['pressure_warning']}
    }
    
    ph_classification = {
        'ph_optimal': {b for b in batches if batch_ph_level[b] in quality_zones['ph_optimal']},
        'ph_acidic': {b for b in batches if batch_ph_level[b] in quality_zones['ph_acidic']},
        'ph_basic': {b for b in batches if batch_ph_level[b] in quality_zones['ph_basic']}
    }
    
    viscosity_classification = {
        'viscosity_optimal': {b for b in batches if batch_viscosity[b] in quality_zones['viscosity_optimal']}
    }
    
    # Combine all classifications
    all_quality_zones = {
        **temp_classification,
        **pressure_classification,
        **ph_classification,
        **viscosity_classification
    }
    
    # ============================================================================
    # EULER DIAGRAM: Find defect patterns
    # ============================================================================
    print("\n📈 Euler Diagram - Quality Defect Patterns:")
    print("   (Which batches fail which combinations of quality checks?)")
    print()
    
    diagram = euler(all_quality_zones)
    
    # Identify defect patterns
    print("  Defect Pattern Analysis:")
    defect_patterns = []
    
    for region, batch_set in sorted(diagram.items(), key=lambda x: (-len(x[1]), x[0])):
        if len(batch_set) >= 3:  # At least 3 batches
            has_warnings = any('warning' in dim or 'acidic' in dim or 'basic' in dim 
                              for dim in region)
            all_optimal = all('optimal' in dim for dim in region)
            
            if has_warnings:
                print(f"\n  ⚠️  {region}:")
                print(f"    {len(batch_set)} batches with issues: "
                      f"{sorted(list(batch_set))[:5]}{'...' if len(batch_set) > 5 else ''}")
                
                # Root cause hints
                warning_dims = [dim for dim in region if 'warning' in dim or 'acidic' in dim or 'basic' in dim]
                print(f"    Failed dimensions: {warning_dims}")
                
                defect_patterns.append((region, len(batch_set)))
                
            elif all_optimal and len(region) >= 3:
                print(f"\n  ✅ {region}:")
                print(f"    {len(batch_set)} perfect batches!")
    
    # ============================================================================
    # ROOT CAUSE ANALYSIS from patterns
    # ============================================================================
    print()
    print("-" * 80)
    print()
    print("🔍 Root Cause Analysis (from Euler patterns):")
    print()
    
    # Find correlated defects (batches with multiple warnings)
    multi_defect = [region for region, _ in defect_patterns 
                    if sum(1 for dim in region if 'warning' in dim) >= 2]
    
    if multi_defect:
        print(f"  🚨 Correlated Defects Detected:")
        for region in multi_defect[:3]:
            batch_count = len(diagram[region])
            print(f"    {region}")
            print(f"      → {batch_count} batches affected")
            print(f"      → Suggests systemic issue, not random variation")
    
    # Temperature + pH correlation
    temp_ph_issues = [region for region in diagram.keys() 
                      if 'temp_warning' in region and ('ph_acidic' in region or 'ph_basic' in region)]
    if temp_ph_issues:
        print(f"\n  💡 Temperature ↔ pH Correlation:")
        for region in temp_ph_issues:
            print(f"    {len(diagram[region])} batches: {region}")
        print(f"      → Check cooling system impact on pH control")
    
    # Optimal across all dimensions
    all_optimal_count = sum(len(batches_set) for region, batches_set in diagram.items()
                            if all('optimal' in dim for dim in region) and len(region) >= 2)
    
    print(f"\n  📊 Quality Metrics:")
    print(f"    Fully optimal batches: {all_optimal_count}/{len(batches)} "
          f"({all_optimal_count/len(batches)*100:.1f}%)")
    
    total_defects = sum(count for region, count in defect_patterns)
    print(f"    Batches with defects: {total_defects}/{len(batches)} "
          f"({total_defects/len(batches)*100:.1f}%)")
    
    print()
    print("=" * 80)
    print("✅ Quality analysis complete!")
    print()
    print("💡 KEY TAKEAWAY:")
    print("   ┌───────────────────────────────────────────────────────────┐")
    print("   │ interval-sets: Defines quality zones (continuous ranges) │")
    print("   │ Classification: Maps batches to quality zones            │")
    print("   │ euler(): Reveals CORRELATED defect patterns              │")
    print("   │ → Root cause analysis & process improvement!             │")
    print("   └───────────────────────────────────────────────────────────┘")
    print("=" * 80)
    
except ImportError as e:
    print("❌ Error: Required libraries not installed")
    print()
    print("To run this example:")
    print("  1. Install: uv sync --extra interval")
    print("  2. Or: pip install eule interval-sets")
    print()
    print(f"Error details: {e}")
