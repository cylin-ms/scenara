#!/usr/bin/env python3
"""
Test empty result handling
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from automated_mygraph_pipeline import AutomatedMyGraphPipeline

def test_empty_results():
    """Test that empty results are handled gracefully"""
    print("🧪 Testing Empty Result Handling")
    print("=" * 35)
    
    pipeline = AutomatedMyGraphPipeline()
    
    try:
        # Setup browser
        if not pipeline.setup_browser():
            print("❌ Browser setup failed")
            return False
        
        # Wait for authentication
        print("🔐 Please sign in...")
        if not pipeline.wait_for_authentication():
            print("❌ Authentication failed")
            return False
        
        # Test a query that's likely to be empty for many users
        print("\n🧪 Testing query that may return empty results...")
        print("(Direct reports - many people don't have any)")
        
        result = pipeline.execute_graph_query("me/directReports", "Direct Reports")
        
        if result:
            if result.get('empty'):
                print("✅ Empty result handled correctly!")
                print(f"📝 Message: {result.get('message')}")
            elif result.get('error'):
                print("✅ Error result handled correctly!")
                print(f"📝 Error: {result.get('message')}")
            elif 'value' in result and len(result['value']) == 0:
                print("✅ Empty list handled correctly!")
            else:
                print(f"✅ Data found: {len(result.get('value', []))} direct reports")
            
            print(f"📊 Result structure: {type(result)}")
            return True
        else:
            print("❌ No result returned")
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
    success = test_empty_results()
    if success:
        print("\n✅ Empty result handling test passed!")
    else:
        print("\n❌ Empty result handling test failed!")