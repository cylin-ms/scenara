#!/usr/bin/env python3
"""
MEvals Permission Diagnostic Tool
Helps diagnose and resolve Error 530033
"""

import json
import os
import sys
from datetime import datetime

def check_mevals_config():
    """Check MEvals configuration files"""
    print("🔍 MEvals Configuration Check")
    print("=" * 50)
    
    config_files = [
        'config.json',
        'settings.json', 
        'app_config.json',
        '.env'
    ]
    
    for config_file in config_files:
        if os.path.exists(config_file):
            print(f"✅ Found: {config_file}")
            if config_file.endswith('.json'):
                try:
                    with open(config_file, 'r') as f:
                        config = json.load(f)
                        if 'client_id' in config:
                            print(f"   Client ID: {config['client_id']}")
                        if 'scopes' in config:
                            print(f"   Scopes: {config['scopes']}")
                except Exception as e:
                    print(f"   ⚠️ Error reading {config_file}: {e}")
        else:
            print(f"❌ Missing: {config_file}")
    
    print()

def analyze_error_530033():
    """Analyze the specific error details"""
    print("🚨 Error 530033 Analysis")
    print("=" * 50)
    
    error_details = {
        "Error Code": "530033",
        "App Name": "Meeting Catchup Player", 
        "App ID": "9ce97a32-d9ab-4ab2-aadc-f49b39b94e11",
        "Device State": "Compliant ✅",
        "Device Platform": "macOS ✅",
        "Issue": "App needs admin consent for tenant"
    }
    
    for key, value in error_details.items():
        print(f"{key}: {value}")
    
    print("\n💡 Solutions:")
    print("1. Contact Microsoft IT for admin consent")
    print("2. Use Microsoft Graph Explorer for testing")
    print("3. Create new app registration with proper permissions")
    print("4. Continue development with existing Meeting PromptCoT data")
    print()

def check_alternatives():
    """Check alternative data sources"""
    print("🎯 Alternative Data Sources")
    print("=" * 50)
    
    # Check if we have existing Meeting PromptCoT data
    data_files = [
        '../meeting_prep_test/test_scenarios.jsonl',
        '../meeting_prep_data/real_scenarios.jsonl',
        '../data/promptcot2_meeting_prep.jsonl'
    ]
    
    for data_file in data_files:
        if os.path.exists(data_file):
            print(f"✅ Available: {data_file}")
            try:
                with open(data_file, 'r') as f:
                    lines = f.readlines()
                    print(f"   📊 {len(lines)} scenarios available")
            except Exception as e:
                print(f"   ⚠️ Error reading: {e}")
        else:
            print(f"❌ Not found: {data_file}")
    
    print()

def generate_it_request():
    """Generate email template for IT request"""
    print("📧 IT Request Template")
    print("=" * 50)
    
    template = f"""
Subject: Request Admin Consent for MEvals App - Calendar Access

Hi Microsoft IT Team,

I'm working on a meeting preparation AI research project and need admin consent 
for the following application to access Microsoft Graph:

App Details:
- App Name: Meeting Catchup Player
- App ID: 9ce97a32-d9ab-4ab2-aadc-f49b39b94e11
- Required Permissions: 
  * Calendars.Read (to access meeting information)
  * User.Read (for user profile)
- Purpose: Research on AI-enhanced meeting preparation
- Device: Compliant macOS (verified as compliant)

Current Status:
- Authentication: Working ✅
- Device Compliance: Passed ✅  
- Error: 530033 (App needs admin consent)

The app is used for legitimate research purposes to improve meeting preparation 
workflows. All data access is read-only and used only for AI training.

Request: Please grant admin consent for this app in our tenant.

Thanks!
{os.getenv('USER', 'Developer')}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    """.strip()
    
    print(template)
    print()
    
    # Save to file
    with open('it_request_template.txt', 'w') as f:
        f.write(template)
    print(f"💾 Saved to: it_request_template.txt")
    print()

def test_graph_explorer_access():
    """Instructions for testing Graph Explorer"""
    print("🌐 Microsoft Graph Explorer Test")
    print("=" * 50)
    
    instructions = """
1. Open: https://developer.microsoft.com/en-us/graph/graph-explorer
2. Sign in with: cyl@microsoft.com
3. Try this query: GET https://graph.microsoft.com/v1.0/me
4. If successful, try: GET https://graph.microsoft.com/v1.0/me/events?$top=5
5. Check what permissions are granted vs needed

Expected Results:
- User profile access: Should work ✅
- Calendar access: May need consent ⚠️

If calendar access works in Graph Explorer but not in MEvals,
the issue is specifically with the MEvals app registration.
    """.strip()
    
    print(instructions)
    print()

def main():
    """Main diagnostic function"""
    print("🔧 MEvals Error 530033 Diagnostic Tool")
    print("=" * 60)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Change to MEvals directory if it exists
    if os.path.exists('MEvals'):
        os.chdir('MEvals')
        print(f"📁 Working directory: {os.getcwd()}")
    elif os.path.exists('../MEvals'):
        os.chdir('../MEvals')
        print(f"📁 Working directory: {os.getcwd()}")
    else:
        print("⚠️ MEvals directory not found, running from current location")
    print()
    
    # Run diagnostics
    check_mevals_config()
    analyze_error_530033()
    check_alternatives()
    generate_it_request()
    test_graph_explorer_access()
    
    print("🎉 Diagnostic Complete!")
    print("=" * 60)
    print("Next Steps:")
    print("1. Test Graph Explorer access")
    print("2. Send IT request if needed")
    print("3. Continue with Meeting PromptCoT using existing data")
    print("4. Launch Streamlit interface: streamlit run ../meeting_data_explorer.py")

if __name__ == "__main__":
    main()