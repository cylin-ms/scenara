#!/usr/bin/env python3
"""
Monitor the batch profile generation progress.
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime
import time

def monitor_progress():
    """Monitor the batch profile generation progress."""
    
    output_dir = Path("data/user_profiles/stakeholders")
    log_file = Path("profile_generation.log")
    
    print("🔍 Batch Profile Generation Monitor")
    print("=" * 80)
    
    # Check if process is running
    import subprocess
    try:
        result = subprocess.run(
            ["ps", "aux"],
            capture_output=True,
            text=True
        )
        is_running = "batch_profile_generator.py" in result.stdout
        
        if is_running:
            print("✅ Status: RUNNING")
        else:
            print("⏹️  Status: STOPPED")
    except:
        print("❓ Status: UNKNOWN")
    
    print("=" * 80)
    
    # Count generated profiles
    if output_dir.exists():
        profile_files = [f for f in output_dir.glob("*.json") if not f.name.startswith("_")]
        print(f"✅ Profiles generated: {len(profile_files)}")
        
        # List recent profiles
        if profile_files:
            recent = sorted(profile_files, key=lambda x: x.stat().st_mtime, reverse=True)[:5]
            print(f"\n📄 Recent profiles:")
            for f in recent:
                mtime = datetime.fromtimestamp(f.stat().st_mtime)
                print(f"   - {f.stem.replace('_', ' ').title()} ({mtime.strftime('%H:%M:%S')})")
    else:
        print("⚠️  Output directory not found")
    
    # Show last few lines of log
    if log_file.exists():
        print("\n📋 Recent log output:")
        print("-" * 80)
        with open(log_file, 'r') as f:
            lines = f.readlines()
            for line in lines[-15:]:
                print(f"   {line.rstrip()}")
    else:
        print("⚠️  Log file not found")
    
    print("=" * 80)
    
    # Check summary files
    if output_dir.exists():
        summary_files = list(output_dir.glob("_summary_*.json"))
        if summary_files:
            latest_summary = max(summary_files, key=lambda x: x.stat().st_mtime)
            print(f"\n📊 Latest summary: {latest_summary.name}")
            with open(latest_summary, 'r') as f:
                summary = json.load(f)
                print(f"   Total stakeholders: {summary.get('total_stakeholders', 'N/A')}")
                print(f"   Profiles generated: {summary.get('profiles_generated', 'N/A')}")
                print(f"   Profiles failed: {summary.get('profiles_failed', 'N/A')}")
                print(f"   Total time: {summary.get('total_time_seconds', 0)/60:.1f} minutes")
    
    print("\n💡 Commands:")
    print("   - View log: tail -f profile_generation.log")
    print("   - Stop process: pkill -f batch_profile_generator")
    print("   - Check profiles: ls -lh data/user_profiles/stakeholders/")


if __name__ == "__main__":
    try:
        # Continuous monitoring if --watch flag is provided
        if "--watch" in sys.argv:
            print("👀 Watching progress (Ctrl+C to stop)...\n")
            while True:
                os.system('clear' if os.name == 'posix' else 'cls')
                monitor_progress()
                time.sleep(10)
        else:
            monitor_progress()
    except KeyboardInterrupt:
        print("\n\n👋 Monitoring stopped")
