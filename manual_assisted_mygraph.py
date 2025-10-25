#!/usr/bin/env python3
"""
Manual-Assisted MyGraph - Super fast with user help
User controls timing, automation handles the technical parts
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import time
from urllib.parse import quote

def manual_assisted_collection():
    """Super fast collection with manual timing"""
    print("🤝 MANUAL-ASSISTED COLLECTION")
    print("You control timing, automation handles extraction")
    print("=" * 45)
    
    # Setup
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-logging')
    driver = webdriver.Chrome(options=options)
    
    results = {}
    
    try:
        # User signs in
        print("1. 🔐 Opening Graph Explorer...")
        driver.get("https://developer.microsoft.com/en-us/graph/graph-explorer")
        input("   Sign in, then press Enter...")
        
        # Queries to run
        queries = [
            ("me", "profile", "Your user profile"),
            ("me/calendarView?startDateTime=2025-10-20T00:00:00Z&endDateTime=2025-11-20T00:00:00Z", "calendar", "Calendar events"),
            ("me/manager", "manager", "Your manager"),
            ("me/directReports", "reports", "Your direct reports")
        ]
        
        for i, (query, key, description) in enumerate(queries, 2):
            print(f"\n{i}. 📡 {description}")
            
            # Navigate to pre-filled query
            url = f"https://developer.microsoft.com/en-us/graph/graph-explorer?request={quote(query)}&method=GET&version=v1.0"
            driver.get(url)
            
            print(f"   🔗 Query loaded: {query}")
            input("   Click 'Run query', wait for response, then press Enter...")
            
            # Extract response
            print("   🔍 Extracting response...")
            extracted = False
            
            # Look for JSON in common places
            selectors = ["pre", "code", ".monaco-editor"]
            for selector in selectors:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                for element in elements:
                    text = element.text.strip()
                    if len(text) > 50 and ('{' in text or '[' in text):
                        try:
                            # Try to parse JSON
                            data = json.loads(text)
                            results[key] = data
                            print(f"   ✅ {description} extracted!")
                            extracted = True
                            break
                        except json.JSONDecodeError:
                            # Try to clean up the JSON
                            try:
                                # Remove common prefixes/suffixes
                                cleaned = text.strip()
                                if cleaned.startswith('```'):
                                    cleaned = cleaned.split('\n', 1)[1]
                                if cleaned.endswith('```'):
                                    cleaned = cleaned.rsplit('\n', 1)[0]
                                
                                data = json.loads(cleaned)
                                results[key] = data
                                print(f"   ✅ {description} extracted (cleaned)!")
                                extracted = True
                                break
                            except:
                                continue
                
                if extracted:
                    break
            
            if not extracted:
                print(f"   ⚠️  Could not extract {description}")
        
        # Save results
        if results:
            filename = f"manual_assisted_{int(time.time())}.json"
            with open(filename, 'w') as f:
                json.dump(results, f, indent=2)
            
            print(f"\n🎉 SUCCESS!")
            print(f"💾 Saved to: {filename}")
            print(f"📊 Collected: {list(results.keys())}")
            
            # Show summary
            for key, data in results.items():
                if isinstance(data, dict):
                    if 'displayName' in data:
                        print(f"   👤 {key}: {data['displayName']}")
                    elif 'value' in data:
                        print(f"   📊 {key}: {len(data['value'])} items")
                    else:
                        print(f"   📄 {key}: {len(str(data))} chars")
        else:
            print("\n❌ No data collected")
        
        return results
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return {}
    finally:
        driver.quit()

if __name__ == "__main__":
    results = manual_assisted_collection()
    if results:
        print(f"\n🎯 Collection complete! Got {len(results)} datasets")
    else:
        print("\n💡 Try again - make sure to wait for responses to load")