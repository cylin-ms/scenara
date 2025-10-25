#!/usr/bin/env python3
"""
Optimized MyGraph - Fast + Reliable
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import re

class OptimizedMyGraph:
    def __init__(self):
        self.driver = None
        self.base_url = "https://developer.microsoft.com/en-us/graph/graph-explorer"
    
    def setup(self):
        """Quick setup"""
        print("🚀 Quick setup...")
        options = webdriver.ChromeOptions()
        options.add_argument('--disable-logging')
        self.driver = webdriver.Chrome(options=options)
        return True
    
    def run_query_optimized(self, query, name):
        """Optimized query execution"""
        print(f"⚡ {name}...", end="", flush=True)
        
        try:
            # Navigate
            url = f"{self.base_url}?request={query}&method=GET&version=v1.0"
            self.driver.get(url)
            
            # Wait and click run button (more reliable)
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.TAG_NAME, "button"))
            )
            
            buttons = self.driver.find_elements(By.TAG_NAME, "button")
            for btn in buttons:
                if "run" in btn.text.lower() and "query" in btn.text.lower():
                    btn.click()
                    break
            
            # Wait for response with timeout
            time.sleep(3)
            
            # Try multiple extraction methods quickly
            selectors = [
                "pre",
                "code", 
                ".monaco-editor .view-lines",
                "div[role='tabpanel'] pre"
            ]
            
            for selector in selectors:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                for element in elements:
                    text = element.text.strip()
                    if len(text) > 30:
                        # Quick JSON detection and extraction
                        json_data = self.extract_json_fast(text)
                        if json_data:
                            print(" ✅")
                            return json_data
            
            print(" ❌")
            return None
            
        except Exception as e:
            print(f" ❌ ({str(e)[:20]})")
            return None
    
    def extract_json_fast(self, text):
        """Fast JSON extraction"""
        try:
            # Try direct parse first
            return json.loads(text)
        except:
            pass
        
        # Quick regex to find JSON blocks
        json_patterns = [
            r'\{.*\}',
            r'\[.*\]'
        ]
        
        for pattern in json_patterns:
            matches = re.findall(pattern, text, re.DOTALL)
            for match in matches:
                try:
                    return json.loads(match)
                except:
                    continue
        
        return None
    
    def collect_essential_data(self):
        """Collect only the most essential data quickly"""
        print("⚡ OPTIMIZED COLLECTION")
        print("=" * 25)
        
        # Login once
        print("🔐 Please sign in...")
        self.driver.get(self.base_url)
        input("Press Enter after signing in...")
        
        # Essential queries only
        queries = [
            ("me", "Profile"),
            ("me/calendarView?startDateTime=2025-10-20T00:00:00Z&endDateTime=2025-11-20T00:00:00Z", "Calendar"),
            ("me/manager", "Manager")
        ]
        
        results = {}
        start_time = time.time()
        
        for query, name in queries:
            result = self.run_query_optimized(query, name)
            if result:
                results[name.lower()] = result
        
        elapsed = time.time() - start_time
        print(f"\n⏱️  Data collection: {elapsed:.1f}s")
        
        return results
    
    def save_and_cleanup(self, results):
        """Quick save and cleanup"""
        if results:
            filename = f"optimized_mygraph_{int(time.time())}.json"
            with open(filename, 'w') as f:
                json.dump(results, f, indent=2)
            print(f"💾 Saved: {filename}")
            print(f"📊 Data: {list(results.keys())}")
        
        self.driver.quit()
        return len(results) > 0

def main():
    """Main optimized automation"""
    automation = OptimizedMyGraph()
    
    try:
        automation.setup()
        results = automation.collect_essential_data()
        success = automation.save_and_cleanup(results)
        
        if success:
            print("🎉 Optimized collection successful!")
        else:
            print("❌ No data collected")
        
        return success
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    main()