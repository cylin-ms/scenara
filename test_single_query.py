#!/usr/bin/env python3
"""
Test a single query execution with the improved automation
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from automated_mygraph_pipeline import AutomatedMyGraphPipeline

def test_single_query():
    """Test executing a single query with full automation"""
    print("🧪 Testing Single Query Execution")
    print("=" * 40)
    
    pipeline = AutomatedMyGraphPipeline()
    
    try:
        # Setup browser
        if not pipeline.setup_browser():
            print("❌ Browser setup failed")
            return False
        
        # Wait for authentication
        print("🔐 Please complete authentication...")
        if not pipeline.wait_for_authentication():
            print("❌ Authentication failed")
            return False
        
        # Test executing a simple query
        print("\n🧪 Testing query execution...")
        result = pipeline.execute_graph_query("me", "User Profile")
        
        if result:
            print("✅ Query execution successful!")
            print(f"📊 Result type: {type(result)}")
            print(f"📝 Result preview: {str(result)[:300]}...")
            
            # Check if it looks like valid user data
            if isinstance(result, dict):
                if 'displayName' in result:
                    print(f"👤 User: {result['displayName']}")
                if 'jobTitle' in result:
                    print(f"💼 Job: {result['jobTitle']}")
                if 'mail' in result:
                    print(f"📧 Email: {result['mail']}")
            
            return True
        else:
            print("❌ Query execution failed")
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
    success = test_single_query()
    if success:
        print("\n🎉 Single query test completed successfully!")
        print("💡 The automation should now work for full data collection!")
    else:
        print("\n❌ Single query test failed!")
        print("💡 May need further debugging of the automation")