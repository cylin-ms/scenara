#!/usr/bin/env python3
"""
Debug Data Types Test
Test what data types are being returned from the collection process
"""

import sys
import json
from automated_mygraph_pipeline import MyGraphAutomator

def debug_data_types():
    """Debug the data types being returned"""
    print("🔍 DEBUG: Data Types Analysis")
    print("=" * 40)
    
    # Create automator instance
    automator = MyGraphAutomator()
    
    # Set up browser (we'll skip this for debugging)
    print("⚠️  This test requires manual setup:")
    print("1. Run the full automation once")
    print("2. Check the saved raw data files")
    
    # Instead, let's check existing saved data if any
    import glob
    raw_files = glob.glob("mygraph_raw_data_*.json")
    
    if raw_files:
        latest_file = max(raw_files)
        print(f"📂 Found raw data file: {latest_file}")
        
        with open(latest_file, 'r') as f:
            raw_data = json.load(f)
        
        print("\n🔍 Data Type Analysis:")
        for key, data in raw_data.items():
            data_type = type(data).__name__
            if isinstance(data, dict):
                has_value = 'value' in data
                has_empty = 'empty' in data
                has_error = 'error' in data
                print(f"   📊 {key}: {data_type} (value:{has_value}, empty:{has_empty}, error:{has_error})")
                if has_value and isinstance(data['value'], list):
                    print(f"      └─ value contains {len(data['value'])} items")
            elif isinstance(data, list):
                print(f"   📊 {key}: {data_type} with {len(data)} items")
                if len(data) > 0:
                    first_item_type = type(data[0]).__name__
                    print(f"      └─ first item is {first_item_type}")
            else:
                print(f"   📊 {key}: {data_type}")
                if isinstance(data, str):
                    print(f"      └─ content preview: {data[:100]}...")
    else:
        print("❌ No raw data files found. Run the automation first.")

if __name__ == "__main__":
    debug_data_types()