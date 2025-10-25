#!/usr/bin/env python3
"""
Quick test of the improved Graph Explorer automation
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from urllib.parse import quote
import time

def test_graph_query_execution():
    """Test executing a single query with the improved selectors"""
    print("🧪 Testing Graph Query Execution")
    print("=" * 50)
    
    # Setup Chrome browser
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    try:
        driver = webdriver.Chrome(options=options)
        driver.maximize_window()
        
        # Test with a simple query
        query = "me"
        graph_url = f"https://developer.microsoft.com/en-us/graph/graph-explorer?request={quote(query)}&method=GET&version=v1.0"
        
        print(f"🌐 Opening Graph Explorer with query: {query}")
        driver.get(graph_url)
        
        print("⏳ Waiting for page to load...")
        time.sleep(5)
        
        print("🔍 Looking for Run query button...")
        
        # Try the new selectors
        run_button = None
        selectors_to_try = [
            ("CSS", "span.___1ej4kmx.f22iagw.f122n59.fkln5zr"),
            ("CSS", "span[class*='___1ej4kmx'][class*='f22iagw']"),
            ("XPATH", "//span[contains(text(), 'Run query')]"),
            ("XPATH", "//button[contains(., 'Run query')]"),
            ("XPATH", "//span[contains(@class, '___1ej4kmx') and contains(text(), 'Run query')]"),
            ("XPATH", "//button[contains(text(), 'Run')]")
        ]
        
        for selector_type, selector in selectors_to_try:
            try:
                print(f"   Trying {selector_type}: {selector}")
                if selector_type == "CSS":
                    run_button = WebDriverWait(driver, 3).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                    )
                else:
                    run_button = WebDriverWait(driver, 3).until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                print(f"   ✅ Found button!")
                break
            except TimeoutException:
                print(f"   ❌ Not found")
                continue
        
        if not run_button:
            print("❌ Could not find Run query button")
            # Take screenshot for debugging
            driver.save_screenshot("debug_no_button.png")
            print("📸 Screenshot saved as debug_no_button.png")
            return False
        
        # Try to click the button
        print("🖱️  Attempting to click Run query button...")
        try:
            # Scroll into view
            driver.execute_script("arguments[0].scrollIntoView(true);", run_button)
            time.sleep(1)
            
            # Click
            run_button.click()
            print("✅ Button clicked successfully!")
            
        except Exception as e:
            print(f"⚠️  Regular click failed: {e}")
            print("🔄 Trying JavaScript click...")
            driver.execute_script("arguments[0].click();", run_button)
            print("✅ JavaScript click attempted")
        
        # Wait for results
        print("⏳ Waiting for query execution...")
        time.sleep(3)
        
        # Look for loading spinner
        try:
            print("🔄 Checking for loading spinner...")
            spinner = driver.find_element(By.CSS_SELECTOR, ".fui-Spinner")
            print("   Loading spinner found, waiting for completion...")
            WebDriverWait(driver, 20).until_not(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".fui-Spinner"))
            )
            print("   ✅ Loading completed!")
        except:
            print("   No spinner found or already completed")
        
        # Look for results
        print("🔍 Looking for JSON response...")
        time.sleep(2)
        
        # Try to find response content
        response_selectors = [
            "pre",
            ".response-content",
            ".monaco-editor .view-lines",
            "code"
        ]
        
        response_found = False
        for selector in response_selectors:
            try:
                response_element = driver.find_element(By.CSS_SELECTOR, selector)
                response_text = response_element.text
                if response_text and len(response_text) > 10:
                    print(f"✅ Found response content!")
                    print(f"📄 Response preview: {response_text[:200]}...")
                    response_found = True
                    break
            except:
                continue
        
        if not response_found:
            print("❌ No response content found")
            driver.save_screenshot("debug_no_response.png")
            print("📸 Screenshot saved as debug_no_response.png")
        
        print("\n💡 Test completed!")
        input("Press Enter to close browser...")
        
        return response_found
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False
    finally:
        try:
            driver.quit()
        except:
            pass

if __name__ == "__main__":
    success = test_graph_query_execution()
    if success:
        print("🎉 Test PASSED - Ready to update full automation!")
    else:
        print("❌ Test FAILED - Need more debugging")