#!/usr/bin/env python3
"""
Improved MyGraph automation with better debugging and timeout handling
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.keys import Keys
import time
import json
from urllib.parse import quote

class ImprovedMyGraphAutomation:
    def __init__(self):
        self.driver = None
        self.base_url = "https://developer.microsoft.com/en-us/graph/graph-explorer"
    
    def setup_browser(self):
        """Setup Chrome browser with better error handling"""
        print("🌐 Setting up browser...")
        
        try:
            options = webdriver.ChromeOptions()
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            
            print("🚀 Starting Chrome browser...")
            self.driver = webdriver.Chrome(options=options)
            self.driver.maximize_window()
            
            # Test basic navigation
            print("🧪 Testing browser navigation...")
            self.driver.get("https://www.google.com")
            time.sleep(2)
            
            print("✅ Browser setup successful")
            return True
            
        except Exception as e:
            print(f"❌ Browser setup failed: {e}")
            return False
    
    def navigate_to_graph_explorer(self):
        """Navigate to Graph Explorer with timeout"""
        print("🌐 Navigating to Graph Explorer...")
        
        try:
            self.driver.get(self.base_url)
            
            # Wait for page to load with timeout
            print("⏳ Waiting for page to load...")
            WebDriverWait(self.driver, 30).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            
            # Check if we can see the page title
            print(f"📄 Page title: {self.driver.title}")
            
            # Look for key elements that indicate the page loaded
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.any_of(
                        EC.presence_of_element_located((By.TAG_NAME, "button")),
                        EC.presence_of_element_located((By.TAG_NAME, "input")),
                        EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid]"))
                    )
                )
                print("✅ Graph Explorer loaded successfully")
                return True
                
            except TimeoutException:
                print("⚠️  Page loaded but no interactive elements found")
                return False
                
        except Exception as e:
            print(f"❌ Navigation failed: {e}")
            return False
    
    def check_authentication_status(self):
        """Check if user is authenticated with multiple methods"""
        print("🔐 Checking authentication status...")
        
        # Look for signs that user is signed in
        auth_indicators = [
            # Signed in indicators
            ("[aria-label*='Sign out']", "Sign out button"),
            (".ms-Persona", "User persona"),
            ("[data-testid='persona']", "User persona testid"),
            ("img[alt*='avatar']", "User avatar"),
            # Sign in indicators
            ("[aria-label*='Sign in']", "Sign in button"),
            ("button:contains('Sign in')", "Sign in text"),
            (".sign-in", "Sign in class")
        ]
        
        for selector, description in auth_indicators:
            try:
                if selector.startswith("button:contains"):
                    # Skip CSS contains selector (not supported)
                    continue
                    
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    print(f"🔍 Found: {description}")
                    if "sign out" in description.lower() or "persona" in description.lower() or "avatar" in description.lower():
                        print("✅ User appears to be signed in")
                        return True
                    elif "sign in" in description.lower():
                        print("⚠️  User needs to sign in")
                        return False
            except Exception as e:
                continue
        
        # Check page content for authentication clues
        try:
            page_text = self.driver.find_element(By.TAG_NAME, "body").text.lower()
            if any(phrase in page_text for phrase in ["sign out", "signed in", "profile", "welcome"]):
                print("✅ Authentication detected in page content")
                return True
            elif any(phrase in page_text for phrase in ["sign in", "login", "authenticate"]):
                print("⚠️  Sign in required based on page content")
                return False
        except:
            pass
        
        print("❓ Authentication status unclear")
        return None
    
    def test_simple_query(self):
        """Test a simple query execution with detailed steps"""
        print("\n🧪 Testing Simple Query Execution")
        print("=" * 40)
        
        try:
            # Navigate to a pre-filled query
            query_url = f"{self.base_url}?request=me&method=GET&version=v1.0"
            print(f"🌐 Loading query URL...")
            self.driver.get(query_url)
            
            # Wait for page load
            time.sleep(3)
            print("✅ Query URL loaded")
            
            # Look for the run button with multiple strategies
            print("🔍 Looking for Run query button...")
            
            # Strategy 1: Find by text content
            buttons = self.driver.find_elements(By.TAG_NAME, "button")
            run_button = None
            
            for button in buttons:
                try:
                    button_text = button.text.strip().lower()
                    if "run" in button_text and "query" in button_text:
                        print(f"✅ Found Run button with text: '{button.text}'")
                        run_button = button
                        break
                except:
                    continue
            
            if not run_button:
                print("❌ Could not find Run query button")
                return False
            
            # Try to click the button
            print("🖱️  Attempting to click Run query button...")
            try:
                run_button.click()
                print("✅ Button clicked successfully")
            except Exception as e:
                print(f"❌ Click failed: {e}")
                return False
            
            # Wait for response
            print("⏳ Waiting for response...")
            time.sleep(5)
            
            # Look for response content
            print("🔍 Looking for response content...")
            
            # Check for any text areas, pre tags, or code blocks
            content_selectors = ["pre", "textarea", "code", ".monaco-editor"]
            
            for selector in content_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for element in elements:
                        text = element.text.strip()
                        if len(text) > 50:  # Some substantial content
                            print(f"📄 Found content in {selector}: {text[:100]}...")
                            if "{" in text or "@odata" in text:
                                print("✅ JSON response detected!")
                                return True
                except:
                    continue
            
            print("⚠️  No clear JSON response found")
            return False
            
        except Exception as e:
            print(f"❌ Query test failed: {e}")
            return False
    
    def interactive_debug(self):
        """Interactive debugging session"""
        print("\n🔧 Interactive Debug Mode")
        print("=" * 30)
        print("Browser is open. You can:")
        print("1. Manually sign in if needed")
        print("2. Navigate to Graph Explorer")
        print("3. Try running a query manually")
        print("4. Check what's on the page")
        print()
        
        while True:
            action = input("Choose action (auth/query/content/quit): ").lower().strip()
            
            if action == "quit":
                break
            elif action == "auth":
                self.check_authentication_status()
            elif action == "query":
                self.test_simple_query()
            elif action == "content":
                try:
                    print("📄 Page title:", self.driver.title)
                    print("🌐 Current URL:", self.driver.current_url)
                    buttons = self.driver.find_elements(By.TAG_NAME, "button")
                    print(f"🔘 Found {len(buttons)} buttons on page")
                    for i, btn in enumerate(buttons[:5]):
                        print(f"   Button {i+1}: '{btn.text.strip()}'")
                except Exception as e:
                    print(f"❌ Error: {e}")
            else:
                print("Unknown action. Use: auth, query, content, or quit")
    
    def cleanup(self):
        """Clean up browser"""
        if self.driver:
            self.driver.quit()

def main():
    """Main function"""
    automation = ImprovedMyGraphAutomation()
    
    try:
        # Setup browser
        if not automation.setup_browser():
            return
        
        # Navigate to Graph Explorer
        if not automation.navigate_to_graph_explorer():
            return
        
        # Check authentication
        auth_status = automation.check_authentication_status()
        if auth_status is False:
            print("⚠️  Please sign in to Graph Explorer manually")
        
        # Interactive debug mode
        automation.interactive_debug()
        
    except KeyboardInterrupt:
        print("\n👋 User interrupted")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    finally:
        automation.cleanup()

if __name__ == "__main__":
    main()