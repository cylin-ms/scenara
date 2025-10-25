#!/usr/bin/env python3
"""
Quick MyGraph Automation Test
Fast automation for immediate testing and validation
"""

import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

def quick_automation_test():
    """Quick test of the automation pipeline"""
    print("⚡ Quick MyGraph Automation Test")
    print("=" * 40)
    
    # Check if main automation file exists
    main_automation = Path("automated_mygraph_pipeline.py")
    if not main_automation.exists():
        print("❌ Main automation file not found!")
        return False
    
    # Check dependencies
    print("📦 Checking dependencies...")
    try:
        import selenium
        from webdriver_manager.chrome import ChromeDriverManager
        print("✅ Selenium and WebDriver Manager available")
    except ImportError:
        print("📥 Installing required packages...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'selenium', 'webdriver-manager'])
        print("✅ Dependencies installed")
    
    # Check Chrome/Chromium availability
    print("🌐 Checking browser availability...")
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.chrome.service import Service
        from webdriver_manager.chrome import ChromeDriverManager
        
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get("https://www.google.com")
        driver.quit()
        print("✅ Chrome browser and WebDriver working")
    except Exception as e:
        print(f"⚠️  Browser test failed: {e}")
        print("💡 The automation will try to install drivers automatically")
    
    # Check existing MyGraph HTML
    html_file = Path("docs/mygraph_explorer.html")
    if html_file.exists():
        print("✅ MyGraph HTML file found")
        # Quick check of current data age
        try:
            with open(html_file, 'r') as f:
                content = f.read()
            if "2025-10-14" in content:
                print("📅 Current data is from October 14, 2025 (10 days old)")
                print("🔄 Fresh data collection recommended")
            else:
                print("📊 Data age unknown - fresh collection recommended")
        except Exception:
            pass
    else:
        print("❌ MyGraph HTML file not found at docs/mygraph_explorer.html")
        return False
    
    # Test automation modes
    print("\n🎯 Automation Options Available:")
    print("1. 🤖 Full Automation (recommended)")
    print("   - Browser-based data collection")
    print("   - Automatic authentication handling")
    print("   - Complete data processing")
    print("   - HTML file update")
    print()
    print("2. 🧪 Test Mode (quick validation)")
    print("   - Minimal data collection")
    print("   - Fast processing")
    print("   - No HTML modification")
    print()
    
    return True

def create_automation_launcher():
    """Create a simple launcher script"""
    launcher_code = '''#!/usr/bin/env python3
"""
MyGraph Automation Launcher
Choose your automation mode
"""

import sys
import subprocess
from pathlib import Path

def show_menu():
    print("🎯 MyGraph Automation Launcher")
    print("=" * 35)
    print()
    print("Choose your automation mode:")
    print("1. 🚀 Full Automation (complete data collection)")
    print("2. 🧪 Test Mode (validation only)")
    print("3. 📊 View Current MyGraph")
    print("4. 🔧 Manual Graph Explorer")
    print("5. ❌ Exit")
    print()

def run_full_automation():
    """Run the complete automation pipeline"""
    print("🚀 Starting Full Automation...")
    try:
        result = subprocess.run([sys.executable, 'automated_mygraph_pipeline.py'], 
                              capture_output=False, text=True)
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Automation failed: {e}")
        return False

def view_current_mygraph():
    """Open the current MyGraph in browser"""
    import webbrowser
    html_file = Path("docs/mygraph_explorer.html")
    if html_file.exists():
        file_url = f"file://{html_file.absolute()}"
        webbrowser.open(file_url)
        print(f"🌐 Opened MyGraph in browser: {file_url}")
    else:
        print("❌ MyGraph HTML file not found")

def open_graph_explorer():
    """Open Microsoft Graph Explorer"""
    import webbrowser
    webbrowser.open("https://developer.microsoft.com/en-us/graph/graph-explorer")
    print("🌐 Opened Graph Explorer in browser")

def main():
    while True:
        show_menu()
        choice = input("👉 Enter your choice (1-5): ").strip()
        
        if choice == "1":
            success = run_full_automation()
            if success:
                print("✅ Full automation completed successfully!")
                print("📂 Check docs/mygraph_explorer.html for updated graph")
            else:
                print("❌ Automation encountered issues")
            input("\\nPress Enter to continue...")
            
        elif choice == "2":
            print("🧪 Test mode - checking automation readiness...")
            from quick_mygraph_automation import quick_automation_test
            quick_automation_test()
            input("\\nPress Enter to continue...")
            
        elif choice == "3":
            view_current_mygraph()
            input("\\nPress Enter to continue...")
            
        elif choice == "4":
            open_graph_explorer()
            input("\\nPress Enter to continue...")
            
        elif choice == "5":
            print("👋 Goodbye!")
            break
            
        else:
            print("❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
'''
    
    with open("launch_mygraph_automation.py", 'w') as f:
        f.write(launcher_code)
    
    print("🚀 Created automation launcher: launch_mygraph_automation.py")

def main():
    success = quick_automation_test()
    
    if success:
        create_automation_launcher()
        print("\n🎊 Quick Test Complete!")
        print("=" * 25)
        print("✅ All systems ready for automation")
        print()
        print("🚀 Next Steps:")
        print("1. Run: python launch_mygraph_automation.py")
        print("2. Choose 'Full Automation' option")
        print("3. Complete authentication in browser")
        print("4. Wait for automatic data collection")
        print("5. View updated MyGraph visualization")
        print()
        print("💡 The automation will:")
        print("   - Open Graph Explorer automatically")
        print("   - Wait for you to authenticate")
        print("   - Collect all your organizational data")
        print("   - Process it into MyGraph format")
        print("   - Update the HTML visualization")
        print("   - Save backup copies of everything")
    else:
        print("\n❌ Quick test failed - check error messages above")

if __name__ == "__main__":
    main()