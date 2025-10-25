#!/usr/bin/env python3
"""
Test Edge WebDriver setup for Graph Explorer
"""

import sys
import time

def test_edge_webdriver():
    """Test if Edge WebDriver is working"""
    print("🧪 Testing Edge WebDriver Setup")
    print("=" * 40)
    
    try:
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        
        print("✅ Selenium imports successful")
        
        # Test Edge WebDriver
        print("🌐 Starting Microsoft Edge...")
        
        options = webdriver.EdgeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        driver = webdriver.Edge(options=options)
        print("✅ Edge WebDriver started successfully")
        
        # Test navigation
        print("🌐 Testing navigation to Graph Explorer...")
        driver.get("https://developer.microsoft.com/en-us/graph/graph-explorer")
        
        # Wait for page load
        WebDriverWait(driver, 30).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        
        print(f"✅ Page loaded: {driver.title}")
        print(f"🌐 Current URL: {driver.current_url}")
        
        # Look for buttons (basic functionality test)
        buttons = driver.find_elements(By.TAG_NAME, "button")
        print(f"🔘 Found {len(buttons)} buttons on page")
        
        # Look specifically for Run query button
        run_buttons = []
        for button in buttons:
            try:
                text = button.text.strip().lower()
                if "run" in text:
                    run_buttons.append(button.text.strip())
            except:
                continue
        
        if run_buttons:
            print(f"✅ Found potential Run buttons: {run_buttons}")
        else:
            print("⚠️  No obvious Run buttons found (may need authentication)")
        
        # Keep browser open for manual inspection
        print("\n🔍 Browser is open for manual inspection...")
        print("💡 You can:")
        print("   1. Sign in to Microsoft Graph Explorer")
        print("   2. Try running a query manually")
        print("   3. Check if everything looks normal")
        print("\nPress Enter when done inspecting...")
        
        input()
        
        driver.quit()
        print("✅ Test completed successfully!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Install selenium: pip install selenium")
        return False
        
    except Exception as e:
        print(f"❌ Error: {e}")
        
        if "msedgedriver" in str(e).lower() or "webdriver" in str(e).lower():
            print("\n💡 Edge WebDriver not found. Install it with:")
            print("   brew install --cask microsoft-edge")
            print("   Or download from: https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/")
        
        return False

if __name__ == "__main__":
    success = test_edge_webdriver()
    if not success:
        sys.exit(1)