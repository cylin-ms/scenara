#!/usr/bin/env python3
"""
Interactive Microsoft Graph Setup for cyl@microsoft.com
Guided setup for real calendar access with multiple authentication options
"""

import requests
import json
import os
import webbrowser
from datetime import datetime, timedelta

def check_existing_setup():
    """Check if we have any existing authentication setup"""
    print("🔍 CHECKING EXISTING SETUP")
    print("=" * 50)
    
    config_files = [
        'real_graph_config.json',
        'graph_credentials.json', 
        '.env',
        'config.json'
    ]
    
    found_configs = []
    for config_file in config_files:
        if os.path.exists(config_file):
            found_configs.append(config_file)
            print(f"✅ Found: {config_file}")
    
    if not found_configs:
        print("❌ No existing configuration found")
    
    return found_configs

def guide_azure_setup():
    """Interactive guide for Azure app registration"""
    print("\n🔧 AZURE APP REGISTRATION GUIDE")
    print("=" * 50)
    print("We need to set up an Azure app registration for calendar access.")
    print("This is a one-time setup that takes about 5 minutes.")
    print()
    
    proceed = input("Do you want to proceed with Azure setup? (y/n): ").lower().strip()
    if proceed != 'y':
        print("❌ Setup cancelled")
        return False
    
    print("\n📝 STEP-BY-STEP AZURE SETUP:")
    print("=" * 50)
    
    steps = [
        "1. Open Azure Portal (https://portal.azure.com)",
        "2. Sign in with your cyl@microsoft.com account", 
        "3. Navigate to: Azure Active Directory → App registrations",
        "4. Click 'New registration'",
        "5. Name: 'Calendar Meeting Intelligence'",
        "6. Account types: 'Accounts in this organizational directory only'",
        "7. Click 'Register'"
    ]
    
    for step in steps:
        print(f"   {step}")
    
    print(f"\n🌐 Opening Azure Portal for you...")
    try:
        webbrowser.open("https://portal.azure.com/#view/Microsoft_AAD_RegisteredApps/ApplicationsListBlade")
        print("✅ Azure Portal opened in browser")
    except:
        print("❌ Could not open browser. Please navigate manually.")
    
    print(f"\n⏳ Complete the app registration, then return here...")
    input("Press ENTER when you've completed the app registration...")
    
    return get_azure_credentials()

def get_azure_credentials():
    """Get Azure credentials from user"""
    print("\n📋 ENTER AZURE APP CREDENTIALS")
    print("=" * 50)
    print("Please enter the values from your Azure app registration:")
    print()
    
    client_id = input("Application (Client) ID: ").strip()
    tenant_id = input("Directory (Tenant) ID: ").strip()
    
    print(f"\n🔑 For Client Secret:")
    print("   1. In Azure portal, go to your app → 'Certificates & secrets'")
    print("   2. Click 'New client secret'")
    print("   3. Description: 'Calendar Access', Expires: 24 months")
    print("   4. Click 'Add' and COPY THE VALUE immediately")
    print()
    
    client_secret = input("Client Secret: ").strip()
    
    if not all([client_id, tenant_id, client_secret]):
        print("❌ Missing required credentials")
        return None
    
    # Save credentials
    credentials = {
        'client_id': client_id,
        'tenant_id': tenant_id,
        'client_secret': client_secret,
        'created_at': datetime.now().isoformat(),
        'user_account': 'cyl@microsoft.com'
    }
    
    with open('real_graph_config.json', 'w') as f:
        json.dump(credentials, f, indent=2)
    
    print("✅ Credentials saved to real_graph_config.json")
    return credentials

def setup_api_permissions():
    """Guide user through API permissions setup"""
    print("\n🔐 API PERMISSIONS SETUP")
    print("=" * 50)
    print("Now we need to set up the required permissions:")
    print()
    
    permissions = [
        "Calendars.Read - Read user calendars",
        "User.Read - Read user profile",
        "Calendars.ReadWrite - Full calendar access (optional)"
    ]
    
    print("Required permissions:")
    for perm in permissions:
        print(f"   ✅ {perm}")
    
    print(f"\n📝 Steps in Azure Portal:")
    steps = [
        "1. Go to your app → 'API permissions'",
        "2. Click 'Add a permission'", 
        "3. Select 'Microsoft Graph'",
        "4. Choose 'Application permissions'",
        "5. Search and add: Calendars.Read, User.Read",
        "6. Click 'Grant admin consent for [organization]'",
        "7. Ensure status shows 'Granted'"
    ]
    
    for step in steps:
        print(f"   {step}")
    
    print(f"\n⏳ Set up the permissions, then return here...")
    input("Press ENTER when permissions are granted...")
    
    return True

def test_connection_with_credentials(credentials):
    """Test connection using provided credentials"""
    print("\n🔗 TESTING CONNECTION")
    print("=" * 50)
    
    try:
        from msal import ConfidentialClientApplication
        
        # Create MSAL app
        authority = f"https://login.microsoftonline.com/{credentials['tenant_id']}"
        app = ConfidentialClientApplication(
            client_id=credentials['client_id'],
            client_credential=credentials['client_secret'],
            authority=authority
        )
        
        # Get token
        scopes = ["https://graph.microsoft.com/.default"]
        result = app.acquire_token_for_client(scopes=scopes)
        
        if "access_token" not in result:
            print(f"❌ Token acquisition failed: {result.get('error_description', 'Unknown error')}")
            return False
        
        # Test API call
        headers = {'Authorization': f'Bearer {result["access_token"]}'}
        response = requests.get("https://graph.microsoft.com/v1.0/users/cyl@microsoft.com", headers=headers)
        
        if response.status_code == 200:
            user_data = response.json()
            print("✅ Connection successful!")
            print(f"👤 Connected as: {user_data.get('displayName', 'Unknown')}")
            print(f"📧 Email: {user_data.get('mail', 'Unknown')}")
            return True
        else:
            print(f"❌ API test failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Connection test error: {str(e)}")
        return False

def alternative_approaches():
    """Show alternative approaches if main setup fails"""
    print("\n🔄 ALTERNATIVE APPROACHES")
    print("=" * 50)
    
    alternatives = [
        {
            "name": "Microsoft Graph Postman Collection",
            "description": "Use Microsoft's pre-built Postman collection for Graph API",
            "url": "https://www.postman.com/microsoftgraph/workspace/microsoft-graph/collection/455214-085f7047-1bbc-4545-9596-cf2d718b2bb8"
        },
        {
            "name": "Graph Explorer",
            "description": "Use Microsoft's web-based Graph Explorer tool",
            "url": "https://developer.microsoft.com/en-us/graph/graph-explorer"
        },
        {
            "name": "PowerShell with Microsoft.Graph module",
            "description": "Use PowerShell cmdlets for calendar access",
            "command": "Install-Module Microsoft.Graph -Scope CurrentUser"
        }
    ]
    
    print("If the main setup doesn't work, try these alternatives:")
    print()
    
    for i, alt in enumerate(alternatives, 1):
        print(f"{i}. {alt['name']}")
        print(f"   Description: {alt['description']}")
        if 'url' in alt:
            print(f"   URL: {alt['url']}")
        if 'command' in alt:
            print(f"   Command: {alt['command']}")
        print()

def main():
    """Main interactive setup function"""
    print("🚀 MICROSOFT GRAPH SETUP FOR cyl@microsoft.com")
    print("=" * 80)
    print("Interactive setup for real calendar access")
    print("Target: Get your actual 8 meetings for October 22, 2025")
    print("=" * 80)
    
    # Check existing setup
    existing_configs = check_existing_setup()
    
    if existing_configs:
        use_existing = input(f"\nUse existing configuration? (y/n): ").lower().strip()
        if use_existing == 'y':
            try:
                with open(existing_configs[0], 'r') as f:
                    credentials = json.load(f)
                print(f"✅ Loaded configuration from {existing_configs[0]}")
                
                if test_connection_with_credentials(credentials):
                    print("\n🎯 Ready to get your real calendar data!")
                    return credentials
            except Exception as e:
                print(f"❌ Error loading existing config: {e}")
    
    # New setup
    print(f"\n🔧 Setting up new Microsoft Graph connection...")
    
    credentials = guide_azure_setup()
    if not credentials:
        print("\n❌ Setup failed")
        alternative_approaches()
        return None
    
    # Setup permissions
    if not setup_api_permissions():
        print("❌ Permissions setup failed")
        return None
    
    # Test connection
    if test_connection_with_credentials(credentials):
        print("\n✅ SETUP COMPLETE!")
        print("Ready to access your real calendar data.")
        return credentials
    else:
        print("\n❌ Setup completed but connection test failed")
        alternative_approaches()
        return None

if __name__ == "__main__":
    result = main()
    
    if result:
        print(f"\n🎯 NEXT STEPS:")
        print("1. Run: python real_microsoft_graph_calendar.py")
        print("2. Get your actual 8 meetings for tomorrow")
        print("3. Analyze real conflicts with Flight CI005")
    else:
        print(f"\n💡 NEED HELP?")
        print("Contact your IT admin or try the alternative approaches listed above.")