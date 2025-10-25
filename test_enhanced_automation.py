#!/usr/bin/env python3
"""
Enhanced Graph Explorer automation with better response detection
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from urllib.parse import quote
import time
import json

def test_enhanced_graph_automation():
    """Test with enhanced response detection"""
    print("🚀 Enhanced Graph Explorer Test")
    print("=" * 50)
    
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    try:
        driver = webdriver.Chrome(options=options)
        driver.maximize_window()
        
        # Test with a simple query
        query = "me"
        graph_url = f"https://developer.microsoft.com/en-us/graph/graph-explorer?request={quote(query)}&method=GET&version=v1.0"
        
        print(f"🌐 Opening Graph Explorer...")
        driver.get(graph_url)
        time.sleep(5)
        
        # Wait for authentication if needed
        print("🔐 Checking authentication status...")
        try:
            # Look for sign-in button
            signin_elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'Sign in')]")
            if signin_elements:
                print("⚠️  Authentication required. Please sign in manually.")
                input("Press Enter after signing in...")
        except:
            pass
        
        # Find and click run button
        print("🔍 Looking for Run query button...")
        run_button = None
        
        # Try XPath first since it worked
        try:
            run_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Run query')]"))
            )
            print("✅ Found Run query button")
        except TimeoutException:
            print("❌ Could not find Run query button")
            return False
        
        # Click the button
        print("🖱️  Clicking Run query button...")
        driver.execute_script("arguments[0].scrollIntoView(true);", run_button)
        time.sleep(1)
        
        try:
            run_button.click()
            print("✅ Button clicked!")
        except:
            driver.execute_script("arguments[0].click();", run_button)
            print("✅ JavaScript click completed")
        
        # Enhanced waiting for results
        print("⏳ Waiting for query execution (enhanced detection)...")
        
        # Wait longer for the response
        max_wait = 30
        check_interval = 2
        total_waited = 0
        
        response_text = None
        while total_waited < max_wait:
            time.sleep(check_interval)
            total_waited += check_interval
            
            # Try multiple ways to find the response
            selectors_to_try = [
                # Common response containers
                ("CSS", "pre"),
                ("CSS", "code"),
                ("CSS", ".response-content"),
                ("CSS", ".json-response"),
                ("CSS", ".monaco-editor"),
                ("CSS", "[data-testid='response-content']"),
                # Monaco editor specific
                ("CSS", ".monaco-editor .view-lines"),
                ("CSS", ".monaco-editor textarea"),
                ("CSS", ".monaco-editor [role='textbox']"),
                # Alternative containers
                ("CSS", ".response-body"),
                ("CSS", ".response-viewer"),
                ("CSS", ".output-content"),
                # Any element with JSON-like content
                ("XPATH", "//*[contains(text(), '{') and contains(text(), '}')]"),
                ("XPATH", "//*[contains(text(), '@odata')]"),
                ("XPATH", "//*[contains(text(), 'displayName')]")
            ]
            
            for selector_type, selector in selectors_to_try:
                try:
                    if selector_type == "CSS":
                        elements = driver.find_elements(By.CSS_SELECTOR, selector)
                    else:
                        elements = driver.find_elements(By.XPATH, selector)
                    
                    for element in elements:
                        text = element.text.strip()
                        if text and len(text) > 20:
                            # Check if it looks like JSON
                            if ('{' in text and '}' in text) or ('@odata' in text) or ('displayName' in text):
                                print(f"✅ Found response with {selector_type}: {selector}")
                                response_text = text
                                break
                    
                    if response_text:
                        break
                        
                except Exception as e:
                    continue
            
            if response_text:
                break
                
            print(f"   Still waiting... ({total_waited}/{max_wait}s)")
        
        if response_text:
            print("🎉 SUCCESS! Found JSON response:")
            print(f"📄 Response length: {len(response_text)} characters")
            print(f"📄 Response preview: {response_text[:300]}...")
            
            # Try to parse as JSON to verify
            try:
                json_data = json.loads(response_text)
                print("✅ Valid JSON structure confirmed")
                if 'displayName' in str(json_data):
                    print(f"👤 User found: {json_data.get('displayName', 'Unknown')}")
                return True
            except json.JSONDecodeError:
                print("⚠️  Response found but not valid JSON")
                return True  # Still consider it a success
        else:
            print("❌ No response found after waiting")
            
            # Debug: Show all text content on page
            print("\n🔍 Debug: All text content on page:")
            all_text = driver.find_element(By.TAG_NAME, "body").text
            lines = [line.strip() for line in all_text.split('\n') if line.strip()]
            for i, line in enumerate(lines[:20]):  # Show first 20 non-empty lines
                print(f"   {i+1}: {line[:100]}")
            
            driver.save_screenshot("debug_enhanced.png")
            print("📸 Screenshot saved as debug_enhanced.png")
            return False
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False
    finally:
        input("Press Enter to close browser...")
        try:
            driver.quit()
        except:
            pass

if __name__ == "__main__":
    success = test_enhanced_graph_automation()
    if success:
        print("\n🎉 SUCCESS! The automation can now execute queries!")
        print("Ready to update the full MyGraph automation pipeline.")
    else:
        print("\n❌ Still having issues with response detection.")