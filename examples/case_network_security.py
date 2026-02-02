#!/usr/bin/env python3
"""
NetOps Case Study: Firewall Rule Analysis

Demonstrates using eule + interval-sets to analyze IP ranges (CIDR).
While interval-sets is continuous, we can map IP addresses to integers.
0.0.0.0   = 0
255.255.255.255 = 4,294,967,295

Scenario:
Analyze overlap between:
1. "Trusted" Subnets (Office VPN)
2. "Blocked" Subnets (Known Botnets)
3. "Public" Access (Web Traffic)

Goal: Find configuration errors where Blocked ranges are inadvertently allowed via Public access.
"""

import socket
import struct

try:
    from interval_sets import Interval, IntervalSet
    from eule import euler
except ImportError:
    print("Requires: pip install interval-sets eule")
    exit(1)

def ip_to_int(ip_str):
    """Convert IP string to integer."""
    return struct.unpack("!I", socket.inet_aton(ip_str))[0]

def int_to_ip(ip_int):
    """Convert integer to IP string."""
    return socket.inet_ntoa(struct.pack("!I", int(ip_int)))

def cidr_to_interval(cidr):
    """Convert CIDR (e.g., '192.168.1.0/24') to an Interval."""
    ip, prefix = cidr.split('/')
    start_int = ip_to_int(ip)
    mask = (0xFFFFFFFF << (32 - int(prefix))) & 0xFFFFFFFF
    
    # Start is just the IP (assuming it's a network address)
    # End is Start | (inverse of mask)
    end_int = start_int | (0xFFFFFFFF ^ mask)
    
    # IntervalSet is continuous/float based.
    # IP space is discrete, but dense enough to treat as continuous range [Start, End]
    return Interval(start_int, end_int)

def format_ip_range(interval):
    """Format an interval back to IP range string."""
    s = int_to_ip(int(interval.start))
    e = int_to_ip(int(interval.end))
    return f"{s} - {e}"

def main():
    print("=" * 60)
    print("🛡️  NetOps: Firewall Rule Analysis")
    print("=" * 60)

    # 1. Define Network Segments using CIDR notation
    
    # CORP_VPN: 10.0.0.0/16 (Internal Employees)
    corp_vpn = IntervalSet([cidr_to_interval("10.0.0.0/16")])
    
    # PUBLIC_WEB: 0.0.0.0/0 (The Internet) - usually allowed on port 80/443
    # Let's say we have an ALLOW ALL rule, but we carve out exceptions
    # public_web = IntervalSet([cidr_to_interval("0.0.0.0/0")]) # Too big for display, let's limit
    # Let's simulate a specific cloud subnet: 10.0.0.0/8
    cloud_net = IntervalSet([cidr_to_interval("10.0.0.0/8")])

    # DENY_LIST: Known malicious IPs (simulated)
    # 10.0.50.0/24 - Malicious Botnet
    # 10.1.0.0/20 - Suspicious Region
    deny_list = IntervalSet([
        cidr_to_interval("10.0.50.0/24"),
        cidr_to_interval("10.1.0.0/20")
    ])

    # SENSITIVE_DB: 10.0.10.0/24 (Database subnet - Should be VPN ONLY)
    sensitive_db = IntervalSet([cidr_to_interval("10.0.10.0/24")])

    rules = {
        'Cloud_Net': cloud_net,
        'VPN_Access': corp_vpn,
        'Malicious_IPs': deny_list,
        'Sensitive_DB': sensitive_db
    }

    print("\n📍 Network Definitions:")
    for name, ranges in rules.items():
        # Just show count for brevity
        print(f"  {name:15s}: covers {len(list(ranges))} contiguous ranges")

    # 2. Analyze Overlaps
    print("\n🔍 Auditing Access Control Lists...")
    diagram = euler(rules)

    # 3. Security Audit Logic
    print("\n🚨 Security Audit Report:")

    for keys, ips in sorted(diagram.items(), key=lambda x: str(x[0])):
        if ips.is_empty(): continue
        
        rule_set = set(keys)
        
        # Security Policy Violation Checks
        
        # Policy 1: Malicious IPs overlapping with Allow rules?
        if 'Malicious_IPs' in rule_set:
            if 'VPN_Access' in rule_set or 'Cloud_Net' in rule_set:
                print(f"\n[CRITICAL] Malicious Block overlapping with Allowed Network!")
                print(f"  Rules: {rule_set}")
                print(f"  Range: {format_ip_range(list(ips)[0])}")
                print(f"  -> ACTION: Ensure DENY rule has higher priority than ALLOW.")
                continue

        # Policy 2: DB accessible from outside VPN?
        if 'Sensitive_DB' in rule_set:
            if 'Cloud_Net' in rule_set and 'VPN_Access' not in rule_set:
                 print(f"\n[HIGH] DB Exposed to Cloud Network without VPN!")
                 print(f"  Rules: {rule_set}")
                 print(f"  Range: {format_ip_range(list(ips)[0])}")
            elif len(rule_set) == 1:
                # Just Sensitive_DB, no access?
                print(f"\n[INFO] Isolated DB Segment (No Route?)")
                print(f"  Rules: {rule_set}")
                print(f"  Range: {format_ip_range(list(ips)[0])}")

        # Info: Valid VPN access
        if 'Sensitive_DB' in rule_set and 'VPN_Access' in rule_set:
             print(f"\n[OK] Authorized DB Access via VPN")
             print(f"  Rules: {rule_set}")

    print("\n" + "="*60)
    print("✅ Network audit complete.")

if __name__ == "__main__":
    main()
