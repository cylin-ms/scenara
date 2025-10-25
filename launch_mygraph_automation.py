#!/usr/bin/env python3
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
            input("\nPress Enter to continue...")
            
        elif choice == "2":
            print("🧪 Test mode - checking automation readiness...")
            from quick_mygraph_automation import quick_automation_test
            quick_automation_test()
            input("\nPress Enter to continue...")
            
        elif choice == "3":
            view_current_mygraph()
            input("\nPress Enter to continue...")
            
        elif choice == "4":
            open_graph_explorer()
            input("\nPress Enter to continue...")
            
        elif choice == "5":
            print("👋 Goodbye!")
            break
            
        else:
            print("❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
