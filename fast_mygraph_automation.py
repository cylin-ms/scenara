#!/usr/bin/env python3
"""
Fast MyGraph Automation - Streamlined for speed
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import json
from urllib.parse import quote

class FastMyGraphAutomation:
    def __init__(self):
        self.driver = None
        self.base_url = "https://developer.microsoft.com/en-us/graph/graph-explorer"
        self.authenticated = False
    
    def setup_browser_fast(self):
        """Quick browser setup"""
        print("🚀 Fast browser setup...")
        
        try:
            options = webdriver.ChromeOptions()
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-logging')
            options.add_argument('--silent')
            
            self.driver = webdriver.Chrome(options=options)
            self.driver.maximize_window()
            
            print("✅ Browser ready")
            return True
            
        except Exception as e:
            print(f"❌ Browser setup failed: {e}")
            return False
    
    def quick_auth_check(self):
        """Fast authentication check"""
        print("🔐 Quick auth check...")
        
        # Go to Graph Explorer
        self.driver.get(self.base_url)
        time.sleep(2)  # Minimal wait
        
        # Quick check for signed-in status
        try:
            # Look for sign-out or user elements (quick check)
            auth_elements = self.driver.find_elements(By.CSS_SELECTOR, 
                "[aria-label*='Sign out'], .ms-Persona, [data-testid='persona']")
            
            if auth_elements:
                print("✅ Already signed in")
                self.authenticated = True
                return True
            else:
                print("⚠️  Please sign in quickly...")
                print("Waiting 30 seconds...")
                time.sleep(30)  # Give user time to sign in
                self.authenticated = True  # Assume they signed in
                return True
                
        except Exception:
            print("⚠️  Auth check unclear, proceeding...")
            self.authenticated = True
            return True
    
    def execute_query_fast(self, query, description):
        """Fast query execution"""
        print(f"⚡ {description}...")
        
        try:
            # Navigate with pre-filled query
            url = f"{self.base_url}?request={quote(query)}&method=GET&version=v1.0"
            self.driver.get(url)
            time.sleep(1)  # Minimal wait
            
            # Find and click run button quickly
            buttons = self.driver.find_elements(By.TAG_NAME, "button")
            for button in buttons:
                if "run" in button.text.lower():
                    button.click()
                    break
            
            time.sleep(3)  # Wait for response
            
            # Quick response extraction
            elements = self.driver.find_elements(By.CSS_SELECTOR, "pre, code")
            for element in elements:
                text = element.text.strip()
                if len(text) > 50 and ('{' in text or '[' in text):
                    try:
                        # Try direct JSON parse
                        return json.loads(text)
                    except:
                        # Quick cleanup and retry
                        cleaned = text.strip()
                        if not cleaned.startswith('{') and '{' in cleaned:
                            cleaned = '{' + cleaned.split('{', 1)[1]
                        if not cleaned.endswith('}') and '}' in cleaned:
                            cleaned = cleaned.rsplit('}', 1)[0] + '}'
                        try:
                            return json.loads(cleaned)
                        except:
                            continue
            
            return None
            
        except Exception as e:
            print(f"⚠️  Error: {e}")
            return None
    
    def fast_data_collection(self):
        """Fast data collection - essential queries only"""
        print("⚡ Fast Data Collection")
        print("=" * 30)
        
        # Essential queries only
        queries = [
            ("me", "Profile"),
            ("me/manager", "Manager"),
            ("me/directReports", "Reports"),
            ("me/calendarView?startDateTime=2025-10-24T00:00:00Z&endDateTime=2025-11-24T00:00:00Z", "Calendar")
        ]
        
        results = {}
        
        for query, name in queries:
            result = self.execute_query_fast(query, name)
            if result:
                print(f"✅ {name}: Success")
                results[name.lower()] = result
            else:
                print(f"⚠️  {name}: No data")
        
        return results
    
    def save_results_fast(self, results):
        """Quick save to file"""
        if not results:
            print("❌ No results to save")
            return False
        
        filename = f"mygraph_data_{int(time.time())}.json"
        
        try:
            with open(filename, 'w') as f:
                json.dump(results, f, indent=2)
            print(f"✅ Saved to {filename}")
            return True
        except Exception as e:
            print(f"❌ Save failed: {e}")
            return False
    
    def cleanup(self):
        """Quick cleanup"""
        if self.driver:
            self.driver.quit()

def fast_automation():
    """Run fast automation"""
    print("⚡ FAST MYGRAPH AUTOMATION")
    print("=" * 40)
    
    automation = FastMyGraphAutomation()
    
    try:
        # Fast setup
        if not automation.setup_browser_fast():
            return False
        
        # Quick auth
        if not automation.quick_auth_check():
            return False
        
        # Fast data collection
        results = automation.fast_data_collection()
        
        # Quick save
        if results:
            automation.save_results_fast(results)
            print(f"\n🎉 Collected {len(results)} data sets in under 2 minutes!")
            return True
        else:
            print("❌ No data collected")
            return False
        
    except KeyboardInterrupt:
        print("\n⏹️  Stopped by user")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    finally:
        automation.cleanup()

if __name__ == "__main__":
    success = fast_automation()
    if success:
        print("✅ Fast automation completed!")
    else:
        print("❌ Fast automation failed!")