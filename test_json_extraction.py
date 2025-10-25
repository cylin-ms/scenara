#!/usr/bin/env python3
"""
Quick test of the improved JSON extraction from Response preview tab
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from automated_mygraph_pipeline import AutomatedMyGraphPipeline

def test_json_extraction():
    """Test JSON extraction from Response preview tab"""
    print("🧪 Testing JSON Extraction from Response Preview")
    print("=" * 50)
    
    pipeline = AutomatedMyGraphPipeline()
    
    try:
        # Setup browser
        if not pipeline.setup_browser():
            print("❌ Browser setup failed")
            return False
        
        print("🔐 Please sign in to Graph Explorer and run a simple query (like 'me')")
        print("Then press Enter here when the response is visible...")
        input()
        
        # Try to extract the current response
        print("🔍 Attempting to extract JSON response...")
        
        # Use the same extraction logic as in the automation
        json_selectors = [
            # Response preview tab content (most likely location)
            "div[role='tabpanel'] pre",
            "div[role='tabpanel'] code", 
            "[aria-labelledby*='Response'] pre",
            "[aria-labelledby*='response'] pre",
            # Monaco editor in response tab
            "div[role='tabpanel'] .monaco-editor .view-lines",
            "div[role='tabpanel'] .monaco-editor",
            # General response containers
            ".tab-content pre",
            ".response-preview pre", 
            ".preview-content",
            "pre",
            "code"
        ]
        
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.common.exceptions import TimeoutException
        
        response_text = None
        found_selector = None
        
        for selector in json_selectors:
            try:
                elements = WebDriverWait(pipeline.driver, 3).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector))
                )
                
                for element in elements:
                    text = element.text.strip()
                    if text and len(text) > 20:
                        # Check if it looks like JSON
                        if ('{' in text and '}' in text) or ('@odata' in text) or ('value' in text):
                            response_text = text
                            found_selector = selector
                            print(f"✅ Found JSON in: {selector}")
                            break
                
                if response_text:
                    break
                    
            except TimeoutException:
                continue
            except Exception as e:
                print(f"⚠️  Error with {selector}: {e}")
                continue
        
        if response_text:
            print("🎉 Successfully extracted JSON!")
            print(f"📊 Selector used: {found_selector}")
            print(f"📝 Response length: {len(response_text)} characters")
            print(f"📄 Preview: {response_text[:200]}...")
            
            # Try to parse as JSON
            try:
                import json
                parsed = json.loads(response_text)
                print("✅ JSON is valid!")
                if 'displayName' in parsed:
                    print(f"👤 User: {parsed['displayName']}")
                if 'jobTitle' in parsed:
                    print(f"💼 Job: {parsed['jobTitle']}")
                return True
            except json.JSONDecodeError as e:
                print(f"⚠️  JSON parsing failed: {e}")
                return False
        else:
            print("❌ No JSON response found")
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
    success = test_json_extraction()
    if success:
        print("\n✅ JSON extraction test successful!")
    else:
        print("\n❌ JSON extraction test failed!")