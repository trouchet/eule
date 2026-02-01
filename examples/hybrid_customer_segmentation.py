#!/usr/bin/env python3
"""
Hybrid Example: Customer Segmentation with Continuous Metrics

Demonstrates:
- Discrete customers classified into overlapping categories
- Continuous metrics (revenue, scores) define category membership via interval-sets
- Euler diagrams reveal exact customer segment overlaps

Pattern: interval-sets → classify → euler → insights
"""

try:
    from interval_sets import Interval, IntervalSet
    from eule import euler
    
    print("=" * 80)
    print("📊 Customer Segmentation: Categories × Continuous Metrics")
    print("=" * 80)
    print()
    
    # ============================================================================
    # DISCRETE ELEMENTS: Individual Customers
    # ============================================================================
    customers = [f"customer_{i:03d}" for i in range(1, 51)]
    
    # Customer metrics (continuous values)
    import random
    random.seed(42)
    customer_revenue = {c: random.uniform(50, 5000) for c in customers}
    customer_satisfaction = {c: random.uniform(1, 10) for c in customers}
    customer_tenure_months = {c: random.randint(1, 60) for c in customers}
    
    # ============================================================================
    # CONTINUOUS CATEGORIES: Defined using interval-sets
    # ============================================================================
    revenue_tiers = {
        'high_value': IntervalSet([Interval.closed(2000, float('inf'))]),
        'mid_value': IntervalSet([Interval.closed(500, 2000)]),
        'low_value': IntervalSet([Interval.closed(0, 500)])
    }
    
    satisfaction_tiers = {
        'promoters': IntervalSet([Interval.closed(9, 10)]),      # NPS promoters
        'passives': IntervalSet([Interval.closed(7, 9)]),         # NPS passives
        'detractors': IntervalSet([Interval.closed(0, 7)])        # NPS detractors
    }
    
    tenure_tiers = {
        'long_term': IntervalSet([Interval.closed(24, float('inf'))]),
        'established': IntervalSet([Interval.closed(6, 24)]),
        'new_customer': IntervalSet([Interval.closed(0, 6)])
    }
    
    print("Sample Customer Metrics:")
    for customer in customers[:5]:
        print(f"  {customer}: ${customer_revenue[customer]:7.2f}, "
              f"satisfaction={customer_satisfaction[customer]:.1f}, "
              f"tenure={customer_tenure_months[customer]}mo")
    print(f"  ... ({len(customers)} customers total)")
    
    print("\nCategory Definitions (continuous ranges):")
    print("  Revenue Tiers:")
    for tier, range_val in revenue_tiers.items():
        print(f"    {tier:15s}: {range_val}")
    print("  Satisfaction (NPS):")
    for tier, range_val in satisfaction_tiers.items():
        print(f"    {tier:15s}: {range_val}")
    
    # ============================================================================
    # CLASSIFICATION: Map customers to categories
    # ============================================================================
    def classify_by_metric(customers_dict, metric_values, tiers):
        """Classify customers into tiers based on continuous metrics."""
        return {
            tier_name: {
                cust for cust in customers_dict
                if metric_values[cust] in tier_range
            }
            for tier_name, tier_range in tiers.items()
        }
    
    revenue_classification = classify_by_metric(customers, customer_revenue, revenue_tiers)
    satisfaction_classification = classify_by_metric(customers, customer_satisfaction, satisfaction_tiers)
    tenure_classification = classify_by_metric(customers, customer_tenure_months, tenure_tiers)
    
    # Combine all classifications
    all_segments = {
        **revenue_classification,
        **satisfaction_classification,
        **tenure_classification
    }
    
    # ============================================================================
    # EULER DIAGRAM: Find exact segment overlaps
    # ============================================================================
    print("\n📈 Euler Diagram - Customer Segment Patterns:")
    print()
    
    diagram = euler(all_segments)
    
    # Focus on actionable multi-category segments
    print("  Key Segment Overlaps:")
    for region, custs in sorted(diagram.items(), key=lambda x: (-len(x[1]), x[0])):
        if len(custs) >= 2 and len(region) >= 2:  # At least 2 customers, 2 categories
            print(f"\n  {region}:")
            print(f"    {len(custs)} customers: {sorted(list(custs))[:5]}{'...' if len(custs) > 5 else ''}")
            
            # Calculate segment metrics
            avg_rev = sum(customer_revenue[c] for c in custs) / len(custs)
            avg_sat = sum(customer_satisfaction[c] for c in custs) / len(custs)
            print(f"    Avg Revenue: ${avg_rev:.2f}, Avg Satisfaction: {avg_sat:.1f}")
            
            # Business insights
            if 'high_value' in region and 'detractors' in region:
                print(f"    🚨 URGENT: High-value customers at churn risk!")
            elif 'high_value' in region and 'promoters' in region:
                print(f"    ✨ VIP segment - prioritize retention")
            elif 'new_customer' in region and 'promoters' in region:
                print(f"    🎯 Growth opportunity - convert to long-term")
    
    print()
    print("-" * 80)
    
    # ============================================================================
    # BUSINESS INSIGHTS from Euler patterns
    # ============================================================================
    print()
    print("💡 Business Insights from Euler Patterns:")
    print()
    
    # At-risk high-value customers
    at_risk_hvl = diagram.get(('detractors', 'high_value'), set()) | \
                  diagram.get(('detractors', 'high_value', 'established'), set()) | \
                  diagram.get(('detractors', 'high_value', 'long_term'), set())
    
    if at_risk_hvl:
        print(f"  🚨 {len(at_risk_hvl)} high-value detractors need intervention")
    
    # Growth champions
    new_promoters = diagram.get(('new_customer', 'promoters'), set())
    if new_promoters:
        print(f"  🎯 {len(new_promoters)} new promoters - fast-track to loyalty program")
    
    # Stable mid-tier
    stable_mid = diagram.get(('established', 'mid_value', 'passives'), set()) | \
                 diagram.get(('long_term', 'mid_value', 'passives'), set())
    if stable_mid:
        print(f"  📊 {len(stable_mid)} stable mid-tier - upsell opportunity")
    
    print()
    print("=" * 80)
    print("✅ Customer segmentation analysis complete!")
    print()
    print("💡 KEY TAKEAWAY:")
    print("   ┌──────────────────────────────────────────────────────────┐")
    print("   │ interval-sets: Defines segment boundaries (continuous)  │")
    print("   │ Classification: Maps customers to segments              │")
    print("   │ euler(): Reveals EXACT multi-segment overlaps           │")
    print("   │ → Actionable business insights!                         │")
    print("   └──────────────────────────────────────────────────────────┘")
    print("=" * 80)
    
except ImportError as e:
    print("❌ Error: Required libraries not installed")
    print()
    print("To run this example:")
    print("  1. Install: uv sync --extra interval")
    print("  2. Or: pip install eule interval-sets")
    print()
    print(f"Error details: {e}")
