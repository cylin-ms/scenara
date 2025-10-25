#!/usr/bin/env python3
"""
Personal Microsoft Graph Setup for cyl@microsoft.com
Step-by-step interactive setup for real Microsoft 365 data integration
"""

import os
import json
import webbrowser
from pathlib import Path
from datetime import datetime

def print_header():
    """Print setup header"""
    print("\n" + "="*70)
    print("🚀 MICROSOFT GRAPH SETUP FOR cyl@microsoft.com")
    print("="*70)
    print("📅 Setting up real Microsoft 365 data integration")
    print("🕒 Setup Time:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("="*70)

def step_1_azure_portal():
    """Guide through Azure portal setup"""
    print("\n📋 STEP 1: Azure App Registration")
    print("-" * 50)
    
    print("🌐 Opening Azure Portal for you...")
    try:
        webbrowser.open("https://portal.azure.com/#view/Microsoft_AAD_RegisteredApps/ApplicationsListBlade")
        print("✅ Azure Portal opened in browser")
    except:
        print("⚠️ Please manually open: https://portal.azure.com")
    
    print("\n📝 **Follow these steps in Azure Portal:**")
    print("   1. Click 'New registration'")
    print("   2. Name: 'Me Notes Intelligence - cyl@microsoft.com'")
    print("   3. Account types: 'Accounts in this organizational directory only'")
    print("   4. Redirect URI: Leave blank")
    print("   5. Click 'Register'")
    
    print("\n⚠️  **IMPORTANT: Save these values!**")
    print("   📌 Application (client) ID")
    print("   📌 Directory (tenant) ID")
    
    input("\n🔵 Press Enter when you've completed the app registration...")
    return True

def step_2_permissions():
    """Guide through permission setup"""
    print("\n🔑 STEP 2: Configure API Permissions")
    print("-" * 50)
    
    print("📝 **In your app registration:**")
    print("   1. Go to 'API permissions'")
    print("   2. Click 'Add a permission'")
    print("   3. Select 'Microsoft Graph'")
    print("   4. Choose 'Application permissions'")
    print("   5. Add these permissions:")
    
    permissions = [
        "User.Read.All (Read all users' full profiles)",
        "Mail.Read (Read mail in all mailboxes)", 
        "Calendars.Read (Read calendars in all mailboxes)",
        "Files.Read.All (Read all files)",
        "Sites.Read.All (Read items in all site collections)"
    ]
    
    for i, perm in enumerate(permissions, 1):
        print(f"      ✅ {i}. {perm}")
    
    print("\n   6. Click 'Grant admin consent for [Your Tenant]'")
    print("   7. Verify all permissions show 'Granted for [Tenant]'")
    
    input("\n🔵 Press Enter when permissions are configured...")
    return True

def step_3_client_secret():
    """Guide through client secret creation"""
    print("\n🔐 STEP 3: Create Client Secret")
    print("-" * 50)
    
    print("📝 **In your app registration:**")
    print("   1. Go to 'Certificates & secrets'")
    print("   2. Click 'New client secret'")
    print("   3. Description: 'Me Notes Integration - cyl@microsoft.com'")
    print("   4. Expires: '24 months' (recommended)")
    print("   5. Click 'Add'")
    
    print("\n⚠️  **CRITICAL: Copy the secret value NOW!**")
    print("   🔴 The secret value will only be shown once")
    print("   📋 Copy it immediately and keep it secure")
    
    input("\n🔵 Press Enter when you've copied the client secret...")
    return True

def step_4_collect_credentials():
    """Collect the credentials from user"""
    print("\n📝 STEP 4: Enter Your Credentials")
    print("-" * 50)
    
    print("🔑 Please enter the values from your Azure app registration:")
    print()
    
    client_id = input("📌 Application (client) ID: ").strip()
    tenant_id = input("📌 Directory (tenant) ID: ").strip()
    client_secret = input("📌 Client secret value: ").strip()
    
    if not all([client_id, tenant_id, client_secret]):
        print("❌ All fields are required. Please try again.")
        return step_4_collect_credentials()
    
    # Validate format (basic check)
    if len(client_id) < 30 or len(tenant_id) < 30 or len(client_secret) < 30:
        print("⚠️ The values seem too short. Please double-check.")
        retry = input("Continue anyway? (y/n): ").lower()
        if retry != 'y':
            return step_4_collect_credentials()
    
    return {
        "client_id": client_id,
        "tenant_id": tenant_id,
        "client_secret": client_secret
    }

def step_5_save_configuration(credentials):
    """Save the configuration"""
    print("\n💾 STEP 5: Save Configuration")
    print("-" * 50)
    
    # Create config file
    config = {
        "client_id": credentials["client_id"],
        "client_secret": credentials["client_secret"],
        "tenant_id": credentials["tenant_id"],
        "user_email": "cyl@microsoft.com",
        "permissions": [
            "User.Read.All",
            "Mail.Read",
            "Calendars.Read", 
            "Files.Read.All",
            "Sites.Read.All"
        ],
        "setup_date": datetime.now().isoformat(),
        "setup_notes": [
            "Configured for cyl@microsoft.com",
            "Production Microsoft Graph integration",
            "Keep this file secure and private"
        ]
    }
    
    config_file = Path("microsoft_graph_config.json")
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"✅ Configuration saved to: {config_file}")
    
    # Also create environment script
    env_script = f"""#!/bin/bash
# Microsoft Graph Environment Variables for cyl@microsoft.com
# Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

export MICROSOFT_CLIENT_ID="{credentials['client_id']}"
export MICROSOFT_CLIENT_SECRET="{credentials['client_secret']}"
export MICROSOFT_TENANT_ID="{credentials['tenant_id']}"

echo "✅ Microsoft Graph environment variables set for cyl@microsoft.com"
echo "🔧 Client ID: $MICROSOFT_CLIENT_ID"
echo "🏢 Tenant ID: $MICROSOFT_TENANT_ID"
echo "🔐 Secret: [CONFIGURED]"
"""
    
    env_file = Path("setup_env_cyl.sh")
    with open(env_file, 'w') as f:
        f.write(env_script)
    
    os.chmod(env_file, 0o755)
    
    print(f"✅ Environment script saved to: {env_file}")
    print("📝 Run with: source setup_env_cyl.sh")
    
    return config_file

def step_6_test_integration():
    """Test the integration"""
    print("\n🧪 STEP 6: Test Integration")
    print("-" * 50)
    
    print("🔄 Testing your Microsoft Graph connection...")
    
    # Run test
    import subprocess
    try:
        result = subprocess.run(
            ["python", "test_real_integration.py"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            print("✅ Integration test PASSED!")
            print("🎉 Your Microsoft Graph connection is working!")
            print("\n📊 Test Output:")
            print(result.stdout)
        else:
            print("❌ Integration test FAILED")
            print("🔍 Error details:")
            print(result.stderr)
            print("\n💡 Common fixes:")
            print("   - Verify admin consent was granted")
            print("   - Check credentials are correct")
            print("   - Ensure permissions are properly configured")
            
    except Exception as e:
        print(f"⚠️ Could not run test automatically: {e}")
        print("📝 Please run manually: python test_real_integration.py")

def step_7_run_real_data():
    """Run real data integration"""
    print("\n🚀 STEP 7: Fetch Your Real Microsoft 365 Data")
    print("-" * 50)
    
    run_now = input("🔵 Fetch your real Me Notes data now? (y/n): ").lower()
    
    if run_now == 'y':
        print("🔄 Fetching your real Microsoft 365 data...")
        
        import subprocess
        try:
            result = subprocess.run(
                ["python", "real_me_notes_integration.py"],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                print("✅ SUCCESS! Your real Me Notes data has been fetched!")
                print("\n📊 Results:")
                print(result.stdout)
            else:
                print("❌ Error fetching data:")
                print(result.stderr)
                
        except Exception as e:
            print(f"⚠️ Could not run automatically: {e}")
            print("📝 Please run manually: python real_me_notes_integration.py")
    else:
        print("📝 You can fetch real data later with:")
        print("   python real_me_notes_integration.py")

def step_8_next_steps():
    """Show next steps"""
    print("\n🎯 STEP 8: Next Steps & Usage")
    print("-" * 50)
    
    print("🎉 **Setup Complete!** Here's how to use your real data:")
    print()
    print("📊 **View your real Me Notes:**")
    print("   python real_me_notes_integration.py")
    print()
    print("📈 **Generate analytics dashboard:**")
    print("   python me_notes_analytics.py")
    print()
    print("🔄 **Schedule daily refresh:**")
    print("   # Add to crontab:")
    print("   0 8 * * * cd /Users/cyl/projects/PromptCoT && python real_me_notes_integration.py")
    print()
    print("🔗 **Integration with Priority Calendar:**")
    print("   python meeting_intelligence_suite_demo.py")
    print()
    print("🛡️ **Security notes:**")
    print("   - Keep microsoft_graph_config.json secure")
    print("   - Rotate client secret every 24 months")
    print("   - Monitor usage in Azure portal")

def main():
    """Run complete setup process"""
    print_header()
    
    try:
        # Step by step setup
        step_1_azure_portal()
        step_2_permissions()
        step_3_client_secret()
        
        credentials = step_4_collect_credentials()
        config_file = step_5_save_configuration(credentials)
        
        step_6_test_integration()
        step_7_run_real_data()
        step_8_next_steps()
        
        print("\n" + "="*70)
        print("✨ MICROSOFT GRAPH SETUP COMPLETE FOR cyl@microsoft.com ✨")
        print("🚀 You can now access your real Microsoft 365 data!")
        print("📖 Configuration saved in:", config_file)
        print("="*70)
        
    except KeyboardInterrupt:
        print("\n\n⚠️ Setup interrupted by user")
        print("📝 You can restart with: python setup_microsoft_graph_cyl.py")
    except Exception as e:
        print(f"\n❌ Setup error: {e}")
        print("📝 Please check the error and try again")

if __name__ == "__main__":
    main()