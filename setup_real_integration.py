#!/usr/bin/env python3
"""
Microsoft Graph Configuration Setup
Helps configure Microsoft Graph API integration for real Me Notes data
"""

import json
import os
from pathlib import Path

def create_configuration_guide():
    """Create a comprehensive configuration guide"""
    
    print("🚀 Microsoft Graph API Configuration Guide")
    print("=" * 60)
    print()
    print("To use real Microsoft 365 data with Me Notes, you need to:")
    print()
    
    print("📋 **Step 1: Create App Registration in Azure Portal**")
    print("   1. Go to: https://portal.azure.com")
    print("   2. Navigate to: Azure Active Directory > App registrations")
    print("   3. Click: 'New registration'")
    print("   4. Name: 'Me Notes Intelligence'")
    print("   5. Account types: 'Single tenant'")
    print("   6. Click: 'Register'")
    print()
    
    print("🔑 **Step 2: Configure API Permissions**")
    print("   1. In your app registration, go to: 'API permissions'")
    print("   2. Click: 'Add a permission' > 'Microsoft Graph'")
    print("   3. Select: 'Application permissions' (for server-to-server)")
    print("   4. Add these permissions:")
    print("      ✅ User.Read.All")
    print("      ✅ Mail.Read")
    print("      ✅ Calendars.Read")
    print("      ✅ Files.Read.All")
    print("      ✅ Sites.Read.All")
    print("   5. Click: 'Grant admin consent for [Tenant]'")
    print()
    
    print("🔐 **Step 3: Create Client Secret**")
    print("   1. Go to: 'Certificates & secrets'")
    print("   2. Click: 'New client secret'")
    print("   3. Description: 'Me Notes Integration'")
    print("   4. Expires: Choose appropriate duration")
    print("   5. Click: 'Add'")
    print("   6. ⚠️ IMPORTANT: Copy the secret value immediately!")
    print()
    
    print("📝 **Step 4: Gather Required Information**")
    print("   You'll need these values from your app registration:")
    print("   📌 Application (client) ID")
    print("   📌 Directory (tenant) ID") 
    print("   📌 Client secret value")
    print()
    
    return True

def create_sample_config():
    """Create a sample configuration file"""
    
    sample_config = {
        "client_id": "YOUR_CLIENT_ID_HERE",
        "client_secret": "YOUR_CLIENT_SECRET_HERE", 
        "tenant_id": "YOUR_TENANT_ID_HERE",
        "user_email": "cyl@microsoft.com",
        "permissions": [
            "User.Read.All",
            "Mail.Read", 
            "Calendars.Read",
            "Files.Read.All",
            "Sites.Read.All"
        ],
        "configuration_notes": [
            "Replace the placeholder values with your actual Azure app registration details",
            "Keep this file secure and do not commit to version control",
            "Use environment variables in production"
        ]
    }
    
    config_file = Path("microsoft_graph_config_sample.json")
    with open(config_file, 'w') as f:
        json.dump(sample_config, f, indent=2)
    
    print(f"📄 Sample configuration saved to: {config_file}")
    print(f"📝 Edit this file with your actual values and rename to 'microsoft_graph_config.json'")
    return str(config_file)

def create_env_setup_script():
    """Create environment variable setup script"""
    
    env_script = """#!/bin/bash
# Microsoft Graph Environment Variables
# Set these with your actual values from Azure app registration

export MICROSOFT_CLIENT_ID="your-client-id-here"
export MICROSOFT_CLIENT_SECRET="your-client-secret-here"  
export MICROSOFT_TENANT_ID="your-tenant-id-here"

# To use this script:
# 1. Replace the placeholder values with your actual values
# 2. Run: source setup_env.sh
# 3. Verify: echo $MICROSOFT_CLIENT_ID

echo "✅ Microsoft Graph environment variables set"
echo "🔧 Client ID: $MICROSOFT_CLIENT_ID"
echo "🏢 Tenant ID: $MICROSOFT_TENANT_ID"
echo "🔐 Secret: [HIDDEN]"
"""
    
    env_file = Path("setup_env.sh")
    with open(env_file, 'w') as f:
        f.write(env_script)
    
    # Make executable
    os.chmod(env_file, 0o755)
    
    print(f"🛠️ Environment setup script saved to: {env_file}")
    print(f"📝 Edit with your values and run: source {env_file}")
    return str(env_file)

def test_current_setup():
    """Test if configuration is already set up"""
    
    print("🔍 **Testing Current Configuration**")
    print("-" * 40)
    
    # Check environment variables
    env_vars = {
        "MICROSOFT_CLIENT_ID": os.getenv("MICROSOFT_CLIENT_ID"),
        "MICROSOFT_CLIENT_SECRET": os.getenv("MICROSOFT_CLIENT_SECRET"), 
        "MICROSOFT_TENANT_ID": os.getenv("MICROSOFT_TENANT_ID")
    }
    
    print("📊 Environment Variables:")
    all_set = True
    for var, value in env_vars.items():
        status = "✅ SET" if value else "❌ NOT SET"
        masked_value = f"{value[:8]}..." if value and len(value) > 8 else value
        print(f"   {var}: {status} {masked_value if value else ''}")
        if not value:
            all_set = False
    
    # Check config file
    config_file = Path("microsoft_graph_config.json")
    print(f"\n📄 Config File ({config_file}):")
    if config_file.exists():
        try:
            with open(config_file) as f:
                config = json.load(f)
            
            has_values = all(
                config.get(key) and config.get(key) != f"YOUR_{key.upper()}_HERE"
                for key in ["client_id", "client_secret", "tenant_id"]
            )
            
            status = "✅ CONFIGURED" if has_values else "⚠️ NEEDS VALUES"
            print(f"   Status: {status}")
            
            if has_values:
                print(f"   Client ID: {config['client_id'][:8]}...")
                print(f"   Tenant ID: {config['tenant_id'][:8]}...")
                all_set = True
                
        except Exception as e:
            print(f"   Status: ❌ INVALID ({e})")
            all_set = False
    else:
        print("   Status: ❌ NOT FOUND")
        all_set = False
    
    print(f"\n🎯 **Overall Status:** {'✅ READY' if all_set else '⚠️ NEEDS CONFIGURATION'}")
    
    if not all_set:
        print("\n💡 **Next Steps:**")
        print("   1. Complete Azure app registration (see guide above)")
        print("   2. Set environment variables OR create config file")
        print("   3. Test with: python real_me_notes_integration.py")
    
    return all_set

def create_test_script():
    """Create a test script for the integration"""
    
    test_script = """#!/usr/bin/env python3
import asyncio
from real_me_notes_integration import RealMeNotesAPI, load_config

async def test_integration():
    print("🧪 Testing Real Me Notes Integration")
    print("=" * 40)
    
    # Load config
    config = load_config()
    
    # Test API
    api = RealMeNotesAPI(
        user_email="cyl@microsoft.com",
        client_id=config.get("client_id"),
        client_secret=config.get("client_secret"),
        tenant_id=config.get("tenant_id")
    )
    
    # Fetch notes
    notes = await api.fetch_real_me_notes()
    
    print(f"✅ Successfully retrieved {len(notes)} Me Notes")
    
    if notes:
        print("\\n📋 Sample Note:")
        note = notes[0]
        print(f"   Category: {note.category.value}")
        print(f"   Note: {note.note}")
        print(f"   Source: {note.source}")

if __name__ == "__main__":
    asyncio.run(test_integration())
"""
    
    test_file = Path("test_real_integration.py")
    with open(test_file, 'w') as f:
        f.write(test_script)
    
    print(f"🧪 Test script saved to: {test_file}")
    print(f"🚀 Run test with: python {test_file}")
    return str(test_file)

def main():
    """Main configuration setup"""
    
    print()
    create_configuration_guide()
    
    print("🛠️ **Setting Up Configuration Files**")
    print("-" * 40)
    
    # Create sample files
    config_file = create_sample_config()
    env_file = create_env_setup_script()
    test_file = create_test_script()
    
    print()
    
    # Test current setup
    is_configured = test_current_setup()
    
    print()
    print("🎯 **Quick Start Summary**")
    print("-" * 40)
    
    if is_configured:
        print("✅ Configuration appears to be complete!")
        print("🚀 Run the real integration with:")
        print("   python real_me_notes_integration.py")
    else:
        print("📋 To complete setup:")
        print("   1. Follow the Azure app registration guide above")
        print(f"   2. Edit {config_file} with your values")
        print(f"   3. OR set environment variables using {env_file}")
        print(f"   4. Test with: python {test_file}")
    
    print()
    print("📚 **Additional Resources:**")
    print("   🔗 Microsoft Graph Explorer: https://developer.microsoft.com/graph/graph-explorer")
    print("   📖 Graph API Docs: https://docs.microsoft.com/graph/")
    print("   🛡️ App Registration Guide: https://docs.microsoft.com/azure/active-directory/develop/quickstart-register-app")

if __name__ == "__main__":
    main()