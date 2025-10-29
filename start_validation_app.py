"""
Quick Start Script for Meeting Classification Validation App
=============================================================

This script:
1. Checks if Flask is installed (installs if needed)
2. Starts the validation web server
3. Opens your browser to the app

Usage: 
  python start_validation_app.py [date]
  
  date: Optional target date in YYYY-MM-DD format (default: today)
  
Examples:
  python start_validation_app.py              # Today's meetings
  python start_validation_app.py 2025-10-29  # Specific date
"""

import subprocess
import sys
import time
import webbrowser
from pathlib import Path
from datetime import datetime

def check_and_install_flask():
    """Check if Flask is installed, install if needed."""
    try:
        import flask
        print("✓ Flask is already installed")
        return True
    except ImportError:
        print("⚠ Flask not found. Installing...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "flask"])
            print("✓ Flask installed successfully")
            return True
        except subprocess.CalledProcessError:
            print("✗ Failed to install Flask")
            print("\nPlease install manually:")
            print("  pip install flask")
            return False

def start_app(target_date: str):
    """Start the validation app."""
    print("\n" + "="*70)
    print("  MEETING CLASSIFICATION VALIDATION APP")
    print("="*70)
    print(f"\n� Target Date: {target_date}")
    print("\n�🚀 Starting validation server...")
    print("📁 Working directory:", Path.cwd())
    print("\n🌐 The app will open in your browser at: http://localhost:5000")
    print("\n⌨️  Press Ctrl+C to stop the server when done")
    print("="*70 + "\n")
    
    # Give user time to read
    time.sleep(2)
    
    # Open browser after a short delay
    def open_browser():
        time.sleep(1.5)
        webbrowser.open('http://localhost:5000')
    
    import threading
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    # Start Flask app with target date
    from validation_app import app, configure_app
    configure_app(target_date)
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)

if __name__ == '__main__':
    print("\n🎯 Meeting Classification Validation - Quick Start\n")
    
    # Parse command line arguments
    if len(sys.argv) > 1:
        target_date = sys.argv[1]
    else:
        target_date = datetime.now().strftime('%Y-%m-%d')
    
    print(f"📅 Target Date: {target_date}")
    
    # Check Flask
    if not check_and_install_flask():
        sys.exit(1)
    
    # Start app
    try:
        start_app(target_date)
    except KeyboardInterrupt:
        print("\n\n✓ Server stopped. Validation results saved!")
        print(f"📊 Check: experiments/{target_date}/human_validation_results.json")
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ Error: {e}")
        sys.exit(1)
