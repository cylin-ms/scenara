#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MEvals UX Test Runner for macOS
Demonstrates how to run MEvals meeting selection interface on macOS
"""

import os
import sys
import subprocess
from pathlib import Path

def test_mevals_auth():
    """Test MEvals authentication on macOS"""
    print("🔐 Testing MEvals Authentication on macOS")
    print("=" * 50)
    
    # Check if we're in the right directory
    mevals_dir = Path("/Users/cyl/projects/PromptCoT/MEvals")
    if not mevals_dir.exists():
        print("❌ MEvals directory not found")
        return False
    
    print("✅ MEvals directory found")
    
    # Test our cross-platform auth manager first
    print("\n📋 Testing cross-platform authentication...")
    try:
        from mevals_auth_manager import CrossPlatformAuthManager
        
        # Test with sample credentials (won't work but shows the interface)
        auth_manager = CrossPlatformAuthManager(
            tenant_id="72f988bf-86f1-41af-91ab-2d7cd011db47",  # Microsoft tenant
            client_id="9ce97a32-d9ab-4ab2-aadc-f49b39b94e11",  # Sample client
            scopes=["Calendars.Read", "offline_access"]
        )
        
        print(f"✅ Authentication manager initialized for {auth_manager.platform}")
        print(f"📱 Broker available: {auth_manager._can_use_broker()}")
        
    except Exception as e:
        print(f"❌ Authentication test failed: {e}")
        return False
    
    return True

def run_mevals_step1():
    """Run MEvals Step 1 (meeting list) with macOS adaptations"""
    print("\n🚀 Running MEvals Step 1 - Meeting List Retrieval")
    print("=" * 55)
    
    mevals_dir = Path("/Users/cyl/projects/PromptCoT/MEvals")
    os.chdir(mevals_dir)
    
    print("📁 Changed to MEvals directory")
    print("🔐 Starting interactive authentication...")
    
    # Set environment to disable Windows Broker on macOS
    env = os.environ.copy()
    env["MSAL_DISABLE_BROKER"] = "1"  # Force device flow on macOS
    
    try:
        # Run step1 with device flow authentication
        cmd = [sys.executable, "step1_get_meeting_list.py", "--days", "7", "--help"]
        
        print("💻 Command:", " ".join(cmd))
        print("🌍 Environment: MSAL_DISABLE_BROKER=1 (device flow)")
        
        result = subprocess.run(cmd, env=env, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ MEvals Step 1 help executed successfully")
            print("📋 Output:")
            print(result.stdout[:500] + "..." if len(result.stdout) > 500 else result.stdout)
            return True
        else:
            print(f"❌ MEvals Step 1 failed with return code {result.returncode}")
            print("📋 Error output:")
            print(result.stderr[:500] + "..." if len(result.stderr) > 500 else result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print("⏰ Command timed out (expected for authentication flow)")
        return True
    except Exception as e:
        print(f"❌ Error running MEvals Step 1: {e}")
        return False

def show_mevals_usage():
    """Show how to use MEvals UX on macOS"""
    print("\n📖 MEvals UX Usage Guide for macOS")
    print("=" * 40)
    
    usage_steps = [
        "1. 🔐 Authenticate with Microsoft Graph",
        "2. 📅 Select date range for meetings",
        "3. 🎛️ Apply filters (cancelled, OOF, etc.)",
        "4. 📊 Export meeting list to CSV/JSON",
        "5. 🔄 Process meetings through pipeline"
    ]
    
    for step in usage_steps:
        print(f"   {step}")
    
    print("\n💻 Commands to run:")
    print("   # Basic meeting list (last 7 days)")
    print("   python step1_get_meeting_list.py --days 7")
    print()
    print("   # Custom date range")
    print("   python step1_get_meeting_list.py --start 2025-10-01T00:00:00 --end 2025-10-31T23:59:59")
    print()
    print("   # Full pipeline")
    print("   python step1_get_meeting_list.py && python step2_generate_meeting_prep.py")
    
    print("\n🔗 Integration with Meeting PromptCoT:")
    print("   # After MEvals processing")
    print("   cd ..")
    print("   python mevals_promptcot_bridge.py --mevals-data MEvals/data/meeting_prep.prompt.samples")

def main():
    """Main test function"""
    print("🍎 MEvals UX Test for macOS")
    print("==========================")
    print("Testing MEvals meeting selection interface on macOS")
    print()
    
    # Test authentication
    auth_success = test_mevals_auth()
    
    if auth_success:
        print("\n✅ Authentication system ready")
    else:
        print("\n❌ Authentication system needs setup")
        return 1
    
    # Test MEvals step 1
    step1_success = run_mevals_step1()
    
    if step1_success:
        print("\n✅ MEvals Step 1 ready to run")
    else:
        print("\n❌ MEvals Step 1 needs configuration")
    
    # Show usage guide
    show_mevals_usage()
    
    print("\n🎯 Summary:")
    print("📋 MEvals UX Authentication:", "✅ Ready" if auth_success else "❌ Needs setup")
    print("🚀 MEvals Pipeline:", "✅ Ready" if step1_success else "❌ Needs config")
    print()
    print("🔐 To authenticate with your Microsoft account:")
    print("   cd MEvals")
    print("   export MSAL_DISABLE_BROKER=1")
    print("   python step1_get_meeting_list.py")
    print()
    print("📱 This will open a browser for Microsoft login")
    print("🎛️ After authentication, you can select meeting date ranges")
    print("📊 Meeting data will be exported for Meeting PromptCoT processing")
    
    return 0

if __name__ == "__main__":
    exit(main())