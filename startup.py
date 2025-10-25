#!/usr/bin/env python3
"""
Scenara 2.0 Startup Script
Automatically detects platform and provides appropriate tool recommendations
"""

import sys
import os
from pathlib import Path

# Add tools directory to path
tools_dir = Path(__file__).parent / "tools"
if tools_dir.exists():
    sys.path.insert(0, str(tools_dir))

try:
    from platform_detection import PlatformDetector
except ImportError:
    print("⚠️  Platform detection not available - using basic startup")
    print("🎯 Scenara 2.0: Enterprise Meeting Intelligence System")
    print("📁 Project root:", Path.cwd())
    sys.exit(1)

def main():
    """Main startup function"""
    project_root = Path.cwd()
    
    # Check if we're in the right directory
    if not (project_root / ".cursorrules").exists():
        print("⚠️  Not in Scenara 2.0 project directory or .cursorrules not found")
        print("📁 Current directory:", project_root)
        return
    
    print("🚀 Starting Scenara 2.0 Platform Detection...")
    print()
    
    detector = PlatformDetector(project_root)
    
    try:
        recommendations = detector.generate_startup_recommendations()
        print(recommendations)
        
        # Save detection results for reference
        results_path = detector.save_detection_results()
        print(f"\n💾 Detection results saved to: {results_path}")
        
        # Check if Python environment is properly configured
        info = detector.platform_info
        if info and not info["python_environment"]["venv_exists"]:
            print("\n⚠️  SETUP REQUIRED:")
            print("   Python virtual environment not found.")
            print("   Run: python -m venv venv && source venv/bin/activate")
            print("   Then: pip install -r requirements_meeting_prep.txt")
        
        print("\n✨ Platform detection complete! Ready to work on Scenara 2.0.")
        
    except Exception as e:
        print(f"❌ Error during platform detection: {e}")
        print("🔧 Manual setup may be required")

if __name__ == "__main__":
    main()