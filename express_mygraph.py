#!/usr/bin/env python3
"""
Express MyGraph - Ultra-fast data collection (under 60 seconds)
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import json
from urllib.parse import quote

def express_collect():
    """Ultra-fast data collection"""
    print("🚀 EXPRESS MYGRAPH COLLECTION")
    print("Target: Under 60 seconds")
    print("=" * 35)
    
    # Quick browser setup
    print("⚡ Starting browser...")
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-logging')
    options.add_argument('--silent')
    driver = webdriver.Chrome(options=options)
    
    results = {}
    
    try:
        # Essential queries (most important first)
        queries = [
            ("me", "profile"),
            ("me/calendarView?startDateTime=2025-10-24T00:00:00Z&endDateTime=2025-11-24T00:00:00Z", "calendar"),
            ("me/manager", "manager"),
            ("me/directReports", "reports")
        ]
        
        print("🔐 Sign in and press Enter...")
        driver.get("https://developer.microsoft.com/en-us/graph/graph-explorer")
        input()  # User signs in
        
        start_time = time.time()
        
        for query, name in queries:
            print(f"⚡ {name}...", end="")
            
            # Navigate with query
            url = f"https://developer.microsoft.com/en-us/graph/graph-explorer?request={quote(query)}&method=GET&version=v1.0"
            driver.get(url)
            time.sleep(0.5)
            
            # Quick run button click
            buttons = driver.find_elements(By.TAG_NAME, "button")
            for btn in buttons:
                if "run" in btn.text.lower():
                    btn.click()
                    break
            
            time.sleep(2)  # Quick wait for response
            
            # Fast extraction
            for element in driver.find_elements(By.CSS_SELECTOR, "pre, code"):
                text = element.text.strip()
                if len(text) > 20 and '{' in text:
                    try:
                        data = json.loads(text)
                        results[name] = data
                        print(" ✅")
                        break
                    except:
                        continue
            else:
                print(" ⚠️")
        
        elapsed = time.time() - start_time
        print(f"\n⏱️  Completed in {elapsed:.1f} seconds")
        
        if results:
            filename = f"express_mygraph_{int(time.time())}.json"
            with open(filename, 'w') as f:
                json.dump(results, f, indent=2)
            print(f"💾 Saved to {filename}")
            print(f"📊 Collected: {list(results.keys())}")
        
        return results
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return {}
    finally:
        driver.quit()

if __name__ == "__main__":
    results = express_collect()
    if results:
        print("🎉 Express collection successful!")
    else:
        print("❌ Express collection failed!")