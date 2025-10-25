#!/usr/bin/env python3
"""
Test the improved automation with Response Preview tab handling
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from automated_mygraph_pipeline import AutomatedMyGraphPipeline

def test_response_preview():
    """Test the automation with Response Preview tab"""
    print("🧪 Testing Response Preview Tab Automation")
    print("=" * 50)
    
    pipeline = AutomatedMyGraphPipeline()
    
    try:
        # Setup browser
        if not pipeline.setup_browser():
            print("❌ Browser setup failed")
            return False
        
        # Wait for authentication
        print("🔐 Please complete authentication in the browser...")
        if not pipeline.wait_for_authentication():
            print("❌ Authentication failed")
            return False
        
        # Test a simple query
        print("\n🧪 Testing single query execution...")
        result = pipeline.execute_graph_query("me", "User Profile Test")
        
        if result:
            print("✅ Query execution successful!")
            print(f"📊 Response preview: {str(result)[:200]}...")
        else:
            print("❌ Query execution failed")
        
        return result is not None
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False
    finally:
        try:
            pipeline.cleanup()
        except:
            pass

if __name__ == "__main__":
    success = test_response_preview()
    if success:
        print("\n✅ Test completed successfully!")
    else:
        print("\n❌ Test failed!")