#!/usr/bin/env python3
"""
Debug extraction - See exactly what text is found
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def debug_extraction():
    """Debug what text we're actually finding"""
    print("🔍 DEBUG EXTRACTION")
    print("=" * 20)
    
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options)
    
    try:
        print("1. Sign in to Graph Explorer...")
        driver.get("https://developer.microsoft.com/en-us/graph/graph-explorer?request=me&method=GET&version=v1.0")
        input("   Sign in, run the query, wait for response, then press Enter...")
        
        print("\n2. 🔍 Analyzing page content...")
        
        # Check all possible selectors
        selectors = [
            ("pre tags", "pre"),
            ("code tags", "code"),
            ("monaco editor lines", ".monaco-editor .view-lines"),
            ("monaco editor", ".monaco-editor"),
            ("tabpanel pre", "div[role='tabpanel'] pre"),
            ("tabpanel code", "div[role='tabpanel'] code"),
            ("any div with json-like content", "div")
        ]
        
        for name, selector in selectors:
            print(f"\n🔍 Checking {name} ({selector}):")
            elements = driver.find_elements(By.CSS_SELECTOR, selector)
            print(f"   Found {len(elements)} elements")
            
            for i, element in enumerate(elements[:3]):  # Check first 3
                try:
                    text = element.text.strip()
                    if text:
                        print(f"   Element {i+1}: {len(text)} chars")
                        print(f"   Preview: {text[:100]}...")
                        if '{' in text or '[' in text or '@odata' in text:
                            print(f"   ✅ Contains JSON-like content!")
                            print(f"   Full text: {text}")
                            break
                except Exception as e:
                    print(f"   Error reading element {i+1}: {e}")
        
        # Also check page source for any hidden JSON
        print(f"\n🔍 Page source analysis:")
        page_source = driver.page_source
        if '"displayName"' in page_source:
            print("   ✅ Found displayName in page source")
        if '"@odata.context"' in page_source:
            print("   ✅ Found @odata.context in page source")
        if '"businessPhones"' in page_source:
            print("   ✅ Found businessPhones in page source")
        
        print("\n💡 Manual inspection:")
        print("   Look at the browser window - can you see the JSON response?")
        print("   Right-click on the JSON and 'Inspect Element'")
        input("   Press Enter when done inspecting...")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    debug_extraction()