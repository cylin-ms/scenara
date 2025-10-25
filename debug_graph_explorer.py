#!/usr/bin/env python3
"""
Graph Explorer Button Inspector
Debug tool to find the correct selectors for the Run query button
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

def inspect_graph_explorer():
    """Inspect Graph Explorer to find the correct button selectors"""
    print("🔍 Graph Explorer Button Inspector")
    print("=" * 50)
    
    # Setup Chrome browser
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    # Don't use headless mode so we can see what's happening
    # options.add_argument('--headless')
    
    try:
        driver = webdriver.Chrome(options=options)
        driver.maximize_window()
        
        print("🌐 Opening Graph Explorer...")
        driver.get("https://developer.microsoft.com/en-us/graph/graph-explorer?request=me&method=GET&version=v1.0")
        
        print("⏳ Waiting for page to load...")
        time.sleep(5)
        
        print("\n🔍 Looking for buttons on the page...")
        
        # Find all buttons
        buttons = driver.find_elements(By.TAG_NAME, "button")
        print(f"📊 Found {len(buttons)} buttons on the page")
        
        print("\n🎯 Button Analysis:")
        for i, button in enumerate(buttons[:20]):  # Check first 20 buttons
            try:
                text = button.text.strip()
                aria_label = button.get_attribute("aria-label") or ""
                class_name = button.get_attribute("class") or ""
                data_testid = button.get_attribute("data-testid") or ""
                
                if any(keyword in (text + aria_label + data_testid).lower() for keyword in ['run', 'execute', 'send', 'submit']):
                    print(f"\n   Button {i+1}:")
                    print(f"      Text: '{text}'")
                    print(f"      Aria-label: '{aria_label}'")
                    print(f"      Class: '{class_name}'")
                    print(f"      Data-testid: '{data_testid}'")
                    print(f"      Visible: {button.is_displayed()}")
                    print(f"      Enabled: {button.is_enabled()}")
                    
            except Exception as e:
                continue
        
        print("\n🔍 Looking for specific selectors...")
        
        # Try common selectors
        selectors_to_try = [
            ("CSS", "button[data-testid*='run']"),
            ("CSS", "button[aria-label*='Run']"),
            ("CSS", "button[aria-label*='Execute']"),
            ("CSS", "button.ms-Button--primary"),
            ("CSS", ".run-query-button"),
            ("CSS", "button:contains('Run')"),
            ("XPATH", "//button[contains(text(), 'Run')]"),
            ("XPATH", "//button[contains(@aria-label, 'Run')]"),
            ("XPATH", "//button[contains(@data-testid, 'run')]"),
        ]
        
        for selector_type, selector in selectors_to_try:
            try:
                if selector_type == "CSS":
                    elements = driver.find_elements(By.CSS_SELECTOR, selector)
                else:
                    elements = driver.find_elements(By.XPATH, selector)
                
                if elements:
                    print(f"✅ Found {len(elements)} elements with {selector_type}: {selector}")
                    for j, elem in enumerate(elements):
                        try:
                            print(f"      Element {j+1}: '{elem.text}' (visible: {elem.is_displayed()})")
                        except:
                            pass
                else:
                    print(f"❌ No elements found with {selector_type}: {selector}")
            except Exception as e:
                print(f"⚠️  Error with {selector_type} {selector}: {e}")
        
        print("\n💡 Manual Instructions:")
        print("1. The browser window should be open with Graph Explorer")
        print("2. Look for the 'Run query' button")
        print("3. Right-click the button and select 'Inspect Element'")
        print("4. Look at the HTML attributes (class, data-testid, aria-label)")
        print("5. We'll use this info to fix the automation")
        
        input("\nPress Enter when you've inspected the button...")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        try:
            driver.quit()
        except:
            pass

if __name__ == "__main__":
    inspect_graph_explorer()