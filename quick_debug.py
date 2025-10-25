#!/usr/bin/env python3
"""
Quick Debug Test - Manually run a single query to see what we get
"""

import sys
import json
import os
from datetime import datetime, timedelta

# Add debugging to see what types we actually get
def debug_single_query():
    """Debug a single query execution manually"""
    print("🔍 Manual Debug Test")
    print("=" * 30)
    
    # Example collected data that might be causing the issue
    test_data = {
        "profile": "{}",  # This could be a string instead of dict
        "manager": {},    # This could be a dict
        "calendar_events": {"value": []},  # This could be proper format
    }
    
    print("🧪 Testing data type handling:")
    for key, data in test_data.items():
        print(f"\n📊 {key}: {type(data).__name__}")
        
        # This is the same logic as in process_collected_data
        if key == "profile":
            if isinstance(data, dict):
                print(f"   ✅ Dict: {data}")
                user_id = f"urn:person:me:{data.get('mail', 'unknown')}"
                print(f"   🆔 User ID: {user_id}")
            elif isinstance(data, str):
                print(f"   ❌ String: {data[:100]}...")
                print("   🔧 This would cause 'str' object has no attribute 'get'")
            elif isinstance(data, list):
                print(f"   ❌ List: {len(data)} items")
                print("   🔧 This would cause 'list' object has no attribute 'get'")
        
        elif key == "manager":
            if isinstance(data, dict):
                print(f"   ✅ Dict: {data}")
                if data and not data.get('empty'):
                    print("   ✅ Would process manager data")
                else:
                    print("   ℹ️  Empty or no manager")
            elif isinstance(data, str):
                print(f"   ❌ String: {data[:100]}...")
                print("   🔧 This would cause 'str' object has no attribute 'get'")

if __name__ == "__main__":
    debug_single_query()