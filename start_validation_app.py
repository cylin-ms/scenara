"""
Quick Start Script for Meeting Classification Validation App
=============================================================

This script:
1. Checks if Flask is installed (installs if needed)
2. Starts the validation web server
3. Opens your browser to the app

Just run: python start_validation_app.py
"""

import subprocess
import sys
import time
import webbrowser
from pathlib import Path

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

def start_app():
    """Start the validation app."""
    print("\n" + "="*70)
    print("  MEETING CLASSIFICATION VALIDATION APP")
    print("="*70)
    print("\n🚀 Starting validation server...")
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
    
    # Start Flask app
    from validation_app import app
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)

if __name__ == '__main__':
    print("\n🎯 Meeting Classification Validation - Quick Start\n")
    
    # Check Flask
    if not check_and_install_flask():
        sys.exit(1)
    
    # Start app
    try:
        start_app()
    except KeyboardInterrupt:
        print("\n\n✓ Server stopped. Validation results saved!")
        print("📊 Check: experiments/2025-10-28/human_validation_results.json")
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ Error: {e}")
        sys.exit(1)
