#!/usr/bin/env python3
"""
Fast MyGraph Tester - Quick response detection
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from automated_mygraph_pipeline import AutomatedMyGraphPipeline

def fast_test():
    """Test with much faster response detection"""
    print("⚡ FAST RESPONSE DETECTION TEST")
    print("=" * 35)
    
    pipeline = AutomatedMyGraphPipeline()
    
    try:
        # Setup browser
        if not pipeline.setup_browser():
            print("❌ Browser setup failed")
            return False
        
        # Quick auth check
        print("🔐 Please sign in quickly...")
        if not pipeline.wait_for_authentication():
            print("❌ Authentication failed")
            return False
        
        print("\n⚡ Testing FAST query execution...")
        print("We'll try to detect results as soon as they appear!")
        
        # Test a simple query
        result = pipeline.execute_graph_query("me", "User Profile")
        
        if result:
            if result.get('empty'):
                print("✅ Empty result detected quickly!")
                print(f"📝 Message: {result.get('message')}")
            elif result.get('error'):
                print("✅ Error detected quickly!")
                print(f"📝 Error: {result.get('message')}")
            else:
                print("✅ Data detected quickly!")
                if isinstance(result, dict) and 'displayName' in result:
                    print(f"👤 User: {result['displayName']}")
                print(f"📊 Data type: {type(result)}")
            
            return True
        else:
            print("❌ No result - may need more optimization")
            return False
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False
    finally:
        try:
            pipeline.cleanup()
        except:
            pass

if __name__ == "__main__":
    print("🎯 This test focuses on speed - detecting results as soon as they appear")
    print("💡 If results appear but we're still 'looking', we need to optimize further")
    print()
    
    success = fast_test()
    if success:
        print("\n⚡ Fast detection test successful!")
    else:
        print("\n❌ Still too slow - needs more optimization")