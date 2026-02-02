#!/usr/bin/env python3
"""
Example: Segregation of Duties (SoD) Audit.

Using discrete sets to find users with "Toxic Combinations" of permissions.
"""

from eule import euler

def main():
    print("🔐 Security Audit: Segregation of Duties")
    print("=========================================\n")

    # Defined Entitlements (Lists of User IDs)
    
    # Can Create Vendor
    users_create_vendor = {
        'alice', 'bob', 'charlie', 'dave', 'intern_grp'
    }
    
    # Can Approve Invoice
    users_approve_invoice = {
        'bob', 'eve', 'frank', 'admin_grp'
    }
    
    # Can Issue Payment (The most sensitive)
    users_issue_payment = {
        'dave', 'frank', 'grace', 'admin_grp'
    }

    roles = {
        'CreateVendor': users_create_vendor,
        'ApproveInvoice': users_approve_invoice,
        'IssuePayment': users_issue_payment
    }
    
    print("Analyzing Access Rights...")
    diagram = euler(roles)
    
    print("\n🚨 Audit Findings:")
    
    violations_found = False
    
    # Helper to check toxic combos
    for keys, user_set in diagram.items():
        if not user_set: continue
        
        roles_held = set(keys)
        users = list(user_set)
        
        # Risk Rule 1: Create Vendor + Issue Payment (Fake Vendor Fraud)
        if {'CreateVendor', 'IssuePayment'}.issubset(roles_held):
             print(f"\n  🔴 CRITICAL RISK: Vendor Fraud Possible")
             print(f"     Users: {users}")
             print(f"     Roles: {list(roles_held)}")
             violations_found = True

        # Risk Rule 2: Approve Invoice + Issue Payment (Unchecked Outflow)
        elif {'ApproveInvoice', 'IssuePayment'}.issubset(roles_held):
             print(f"\n  🟠 HIGH RISK: Unchecked Spending")
             print(f"     Users: {users}")
             print(f"     Roles: {list(roles_held)}")
             violations_found = True
             
    if not violations_found:
        print("\n✅ No SoD violations found.")
    else:
        print("\n⚠️  Immediate remediation required for identified users.")

if __name__ == "__main__":
    main()
