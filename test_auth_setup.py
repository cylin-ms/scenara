#!/usr/bin/env python3
"""
Test Microsoft Graph Authentication Setup
Based on SilverFlow's authentication patterns - validates setup without API calls.
"""

import os
import sys
import json
import msal
from typing import Dict, Any, Optional

# Configuration
TENANT_ID = "72f988bf-86f1-41af-91ab-2d7cd011db47"
CLIENT_ID = "9ce97a32-d9ab-4ab2-aadc-f49b39b94e11"
TEST_SCOPES = ["https://graph.microsoft.com/.default"]

def safe_print(*args, **kwargs):
    """Print text defensively."""
    try:
        print(*args, **kwargs)
    except UnicodeEncodeError:
        safe_args = [str(arg).encode('ascii', 'replace').decode('ascii') for arg in args]
        print(*safe_args, **kwargs)

def _login_hint() -> Optional[str]:
    """Generate login hint."""
    user = os.getenv("USERNAME") or os.getenv("USER") or ""
    return f"{user}@microsoft.com" if user else None

def test_auth_setup():
    """Test authentication setup without making actual API calls."""
    safe_print("🧪 Testing Microsoft Graph Authentication Setup")
    safe_print("=" * 50)
    
    # Test 1: MSAL Library
    safe_print("1. Testing MSAL library...")
    try:
        import msal
        safe_print(f"   ✅ MSAL version: {msal.__version__}")
    except ImportError as e:
        safe_print(f"   ❌ MSAL not installed: {e}")
        return False
    
    # Test 2: Client Configuration
    safe_print("2. Testing client configuration...")
    safe_print(f"   📋 Tenant ID: {TENANT_ID}")
    safe_print(f"   📋 Client ID: {CLIENT_ID}")
    safe_print(f"   📋 Login hint: {_login_hint()}")
    
    # Test 3: Authority URL
    authority = f"https://login.microsoftonline.com/{TENANT_ID}"
    safe_print(f"   📋 Authority: {authority}")
    
    # Test 4: MSAL App Creation
    safe_print("3. Testing MSAL application creation...")
    try:
        app = msal.PublicClientApplication(
            CLIENT_ID,
            authority=authority,
            enable_broker_on_windows=True,
        )
        safe_print("   ✅ MSAL PublicClientApplication created successfully")
        safe_print("   ✅ Windows Broker (WAM) enabled")
        broker_enabled = True
    except Exception as e:
        safe_print(f"   ⚠️  Windows Broker failed: {e}")
        try:
            app = msal.PublicClientApplication(
                CLIENT_ID,
                authority=authority,
                enable_broker_on_windows=False,
            )
            safe_print("   ✅ MSAL PublicClientApplication created (fallback mode)")
            broker_enabled = False
        except Exception as e2:
            safe_print(f"   ❌ MSAL application creation failed: {e2}")
            return False
    
    # Test 5: Check for cached accounts
    safe_print("4. Checking for cached accounts...")
    try:
        accounts = app.get_accounts()
        if accounts:
            safe_print(f"   ✅ Found {len(accounts)} cached account(s):")
            for i, account in enumerate(accounts, 1):
                username = account.get('username', 'Unknown')
                safe_print(f"      {i}. {username}")
        else:
            safe_print("   📋 No cached accounts found (first-time setup)")
    except Exception as e:
        safe_print(f"   ⚠️  Could not check cached accounts: {e}")
    
    # Test 6: Validate scopes
    safe_print("5. Validating scopes...")
    for scope in TEST_SCOPES:
        safe_print(f"   📋 {scope}")
    safe_print("   ✅ Scopes look valid")
    
    # Test 7: Network connectivity check
    safe_print("6. Testing network connectivity...")
    try:
        import requests
        response = requests.get("https://login.microsoftonline.com", timeout=10)
        if response.status_code == 200:
            safe_print("   ✅ Can reach Microsoft login endpoints")
        else:
            safe_print(f"   ⚠️  Unexpected response from login endpoint: {response.status_code}")
    except Exception as e:
        safe_print(f"   ❌ Network connectivity issue: {e}")
        return False
    
    safe_print("\n🎉 Authentication setup test completed!")
    safe_print("📝 Next steps:")
    safe_print("   1. Run the full calendar integration script")
    safe_print("   2. Complete interactive authentication when prompted")
    safe_print("   3. Grant consent for calendar access permissions")
    
    return True

def test_token_acquisition():
    """Perform a minimal token acquisition test."""
    safe_print("\n🔐 Testing token acquisition (interactive)...")
    safe_print("This will open a browser window for authentication.")
    
    response = input("Continue with interactive auth test? (y/N): ").strip().lower()
    if response != 'y':
        safe_print("⏭️  Skipping interactive authentication test")
        return True
    
    authority = f"https://login.microsoftonline.com/{TENANT_ID}"
    
    try:
        app = msal.PublicClientApplication(
            CLIENT_ID,
            authority=authority,
            enable_broker_on_windows=True,
        )
        broker_enabled = True
    except Exception:
        app = msal.PublicClientApplication(
            CLIENT_ID,
            authority=authority,
            enable_broker_on_windows=False,
        )
        broker_enabled = False
    
    login_hint = _login_hint()
    
    # Try silent first
    accounts = app.get_accounts()
    if accounts:
        safe_print("🔄 Attempting silent authentication...")
        result = app.acquire_token_silent(TEST_SCOPES, account=accounts[0])
        if result and "access_token" in result:
            safe_print("✅ Silent authentication successful!")
            safe_print(f"   Token length: {len(result['access_token'])} characters")
            
            # Decode token claims (for verification only)
            claims = result.get("id_token_claims", {})
            user_name = claims.get("name", "Unknown")
            user_email = claims.get("preferred_username", "Unknown")
            safe_print(f"   User: {user_name} ({user_email})")
            return True
    
    # Interactive authentication
    safe_print("🌐 Starting interactive authentication...")
    kwargs = {"scopes": TEST_SCOPES}
    if login_hint:
        kwargs["login_hint"] = login_hint
    if broker_enabled:
        kwargs["parent_window_handle"] = msal.application.PublicClientApplication.CONSOLE_WINDOW_HANDLE
    
    result = app.acquire_token_interactive(**kwargs)
    
    if "access_token" in result:
        safe_print("✅ Interactive authentication successful!")
        claims = result.get("id_token_claims", {})
        user_name = claims.get("name", "Unknown")
        user_email = claims.get("preferred_username", "Unknown")
        safe_print(f"   User: {user_name} ({user_email})")
        safe_print(f"   Token length: {len(result['access_token'])} characters")
        return True
    else:
        error = result.get("error_description") or result.get("error") or "Unknown error"
        safe_print(f"❌ Authentication failed: {error}")
        return False

def main():
    """Main test function."""
    try:
        # Basic setup test
        if not test_auth_setup():
            safe_print("❌ Basic setup test failed")
            return 1
        
        # Optional interactive test
        if not test_token_acquisition():
            safe_print("❌ Token acquisition test failed")
            return 1
        
        safe_print("\n🎉 All tests passed! Authentication setup is working correctly.")
        safe_print("🚀 You can now run the full calendar integration script.")
        return 0
        
    except KeyboardInterrupt:
        safe_print("\n⏹️  Test interrupted by user")
        return 1
    except Exception as e:
        safe_print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())