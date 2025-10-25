#!/usr/bin/env python3
"""
Automated Calendar Access Launcher
Choose between different automation approaches for your platform
"""

import sys
import subprocess
import platform


def show_menu():
    """Display the automation options."""
    print("🤖 Automated Microsoft Graph Calendar Access")
    print("=" * 45)
    print()
    print("Choose your automation method:")
    print("1. 🍎 macOS Safari + AppleScript (Recommended for macOS)")
    print("2. 🌐 Microsoft Edge + Selenium (Best Microsoft auth)")
    print("3. 📋 Manual with Parser Tool")
    print("4. ❌ Exit")
    print()


def run_macos_automation():
    """Run the macOS-specific automation."""
    print("🍎 Starting macOS Safari automation...")
    try:
        subprocess.run([sys.executable, 'automated_calendar_macos.py'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ macOS automation failed: {e}")
        fallback_to_manual()
    except FileNotFoundError:
        print("❌ automated_calendar_macos.py not found")
        fallback_to_manual()


def run_selenium_automation():
    """Run the Edge + Selenium-based automation."""
    print("🌐 Starting Microsoft Edge + Selenium automation...")
    try:
        subprocess.run([sys.executable, 'automated_calendar_today.py'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Edge automation failed: {e}")
        fallback_to_manual()
    except FileNotFoundError:
        print("❌ automated_calendar_today.py not found")
        fallback_to_manual()


def fallback_to_manual():
    """Provide manual instructions."""
    print()
    print("💡 Manual Process:")
    print("1. Go to: https://developer.microsoft.com/en-us/graph/graph-explorer")
    print("2. Sign in with your Microsoft account")
    print("3. Execute this query:")
    print("   GET /me/calendarView?startDateTime=2025-10-22T00:00:00.000Z&endDateTime=2025-10-22T23:59:59.999Z&$orderby=start/dateTime")
    print("4. Copy the JSON response")
    print("5. Run: python parse_graph_explorer_response.py")
    print("   (Then paste the JSON when prompted)")


def run_manual_with_parser():
    """Run the manual process with parser."""
    print("📋 Manual process with parser tool...")
    try:
        subprocess.run([sys.executable, 'parse_graph_explorer_response.py'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Parser failed: {e}")
    except FileNotFoundError:
        print("❌ parse_graph_explorer_response.py not found")
        fallback_to_manual()


def main():
    """Main launcher function."""
    while True:
        show_menu()
        
        try:
            choice = input("Enter your choice (1-4): ").strip()
            
            if choice == '1':
                if platform.system() == 'Darwin':  # macOS
                    run_macos_automation()
                else:
                    print("❌ macOS automation only works on macOS")
                    print("💡 Try option 2 (Microsoft Edge + Selenium) instead")
                break
                
            elif choice == '2':
                run_selenium_automation()
                break
                
            elif choice == '3':
                run_manual_with_parser()
                break
                
            elif choice == '4':
                print("👋 Goodbye!")
                sys.exit(0)
                
            else:
                print("❌ Invalid choice. Please enter 1, 2, 3, or 4.")
                print()
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            sys.exit(0)
        except EOFError:
            print("\n👋 Goodbye!")
            sys.exit(0)


if __name__ == "__main__":
    main()