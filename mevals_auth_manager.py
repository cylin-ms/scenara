#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cross-Platform Authentication Manager for MEvals macOS Integration
Handles Microsoft Graph authentication without Windows Broker dependency
"""

import os
import sys
import platform
import json
import logging
from typing import Optional, Dict, Any
from pathlib import Path

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

try:
    import msal
    import requests
except ImportError as e:
    print(f"❌ Missing required dependencies: {e}")
    print("Please install: pip install msal requests")
    sys.exit(1)

class CrossPlatformAuthManager:
    """
    Cross-platform Microsoft Graph authentication manager
    Adapted from MEvals Windows-specific authentication for macOS compatibility
    """
    
    def __init__(self, tenant_id: str, client_id: str, scopes: list):
        self.tenant_id = tenant_id
        self.client_id = client_id
        self.scopes = scopes
        self.platform = self._detect_platform()
        self.cache_file = Path.home() / ".mevals_token_cache.json"
        
        logger.info(f"Initialized CrossPlatformAuthManager for {self.platform}")
    
    def _detect_platform(self) -> str:
        """Detect the current platform"""
        return platform.system().lower()
    
    def _can_use_broker(self) -> bool:
        """Check if Windows Broker authentication can be used"""
        return self.platform == "windows"
        
    def get_msal_app(self) -> msal.PublicClientApplication:
        """Create MSAL app with platform-appropriate settings"""
        authority = f"https://login.microsoftonline.com/{self.tenant_id}"
        
        # Load token cache if it exists
        token_cache = msal.SerializableTokenCache()
        if self.cache_file.exists():
            try:
                with open(self.cache_file, 'r') as f:
                    token_cache.deserialize(f.read())
            except Exception as e:
                print(f"⚠️ Warning: Could not load token cache: {e}")
        
        if self.platform == "windows":
            # Use Windows Broker if available (original MEvals behavior)
            return msal.PublicClientApplication(
                self.client_id,
                authority=authority,
                enable_broker_on_windows=True,
                token_cache=token_cache
            )
        else:
            # Standard MSAL for macOS/Linux (adapted for cross-platform)
            return msal.PublicClientApplication(
                self.client_id,
                authority=authority,
                token_cache=token_cache
            )
    
    def acquire_token(self) -> Optional[Dict[str, Any]]:
        """Acquire token using platform-appropriate method"""
        app = self.get_msal_app()
        
        # Try silent authentication first
        accounts = app.get_accounts()
        if accounts:
            print("🔄 Attempting silent authentication...")
            result = app.acquire_token_silent(self.scopes, account=accounts[0])
            if result and "access_token" in result:
                print("✅ Silent authentication successful")
                self._save_token_cache(app)
                return result
        
        # Platform-specific interactive authentication
        print(f"🔐 Starting interactive authentication on {self.platform.title()}...")
        
        if self.platform == "windows":
            result = self._acquire_token_windows(app)
        elif self.platform == "darwin":  # macOS
            result = self._acquire_token_macos(app)
        else:  # Linux and others
            result = self._acquire_token_linux(app)
        
        if result and "access_token" in result:
            print("✅ Interactive authentication successful")
            self._save_token_cache(app)
        else:
            print("❌ Authentication failed")
            if result and "error" in result:
                print(f"Error: {result['error']}")
                print(f"Description: {result.get('error_description', 'No description')}")
        
        return result
    
    def _acquire_token_windows(self, app: msal.PublicClientApplication) -> Optional[Dict[str, Any]]:
        """Windows-specific authentication with WAM (original MEvals behavior)"""
        login_hint = self._get_login_hint()
        return app.acquire_token_interactive(
            self.scopes,
            login_hint=login_hint,
            # parent_window_handle=None  # Let MSAL handle the window
        )
    
    def _acquire_token_macos(self, app: msal.PublicClientApplication) -> Optional[Dict[str, Any]]:
        """macOS-specific authentication (adapted for macOS)"""
        login_hint = self._get_login_hint()
        
        # Try interactive browser flow first (best user experience on macOS)
        try:
            print("🌐 Opening browser for authentication...")
            return app.acquire_token_interactive(
                self.scopes,
                login_hint=login_hint
            )
        except Exception as e:
            print(f"⚠️ Browser authentication failed: {e}")
            print("🔄 Falling back to device code flow...")
            return self._acquire_token_device_flow(app)
    
    def _acquire_token_linux(self, app: msal.PublicClientApplication) -> Optional[Dict[str, Any]]:
        """Linux-specific authentication (device flow preferred)"""
        return self._acquire_token_device_flow(app)
    
    def _acquire_token_device_flow(self, app: msal.PublicClientApplication) -> Optional[Dict[str, Any]]:
        """Device code flow for headless or problematic environments"""
        flow = app.initiate_device_flow(scopes=self.scopes)
        if "user_code" in flow:
            print(f"\n📱 Please visit: {flow['verification_uri']}")
            print(f"🔑 Enter this code: {flow['user_code']}")
            print("⏳ Waiting for authentication...")
            
            result = app.acquire_token_by_device_flow(flow)
            return result
        return None
    
    def _get_login_hint(self) -> Optional[str]:
        """Get login hint from various sources"""
        # Try environment variables (cross-platform)
        user = (os.getenv("USERNAME") or  # Windows
                os.getenv("USER") or      # Unix/macOS
                os.getenv("LOGNAME"))     # Alternative
        
        if user:
            return f"{user}@microsoft.com"
        
        # Try git config (common on developer machines)
        try:
            import subprocess
            result = subprocess.run(['git', 'config', 'user.email'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                email = result.stdout.strip()
                if '@microsoft.com' in email:
                    return email
        except Exception:
            pass
        
        return None
    
    def _save_token_cache(self, app: msal.PublicClientApplication) -> None:
        """Save token cache to disk for future silent authentication"""
        try:
            if app.token_cache.has_state_changed:
                with open(self.cache_file, 'w') as f:
                    f.write(app.token_cache.serialize())
        except Exception as e:
            print(f"⚠️ Warning: Could not save token cache: {e}")
    
    def test_graph_access(self, access_token: str) -> bool:
        """Test if the access token works with Microsoft Graph"""
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        try:
            # Test with a simple Graph API call
            response = requests.get(
                "https://graph.microsoft.com/v1.0/me",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                user_info = response.json()
                print(f"✅ Graph API access verified for: {user_info.get('displayName', 'Unknown')}")
                return True
            else:
                print(f"❌ Graph API access failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Graph API test error: {e}")
            return False


def main():
    """Test the cross-platform authentication"""
    print("🧪 Testing MEvals Cross-Platform Authentication")
    print("==============================================")
    
    # MEvals configuration (from original Windows version)
    TENANT_ID = "72f988bf-86f1-41af-91ab-2d7cd011db47"
    CLIENT_ID = "9ce97a32-d9ab-4ab2-aadc-f49b39b94e11"
    GRAPH_SCOPES = ["Calendars.Read", "offline_access", "openid", "profile"]
    
    # Initialize authentication manager
    auth_manager = CrossPlatformAuthManager(TENANT_ID, CLIENT_ID, GRAPH_SCOPES)
    
    print(f"🖥️ Platform: {platform.system()} {platform.release()}")
    print(f"🐍 Python: {sys.version}")
    
    # Attempt authentication
    token_result = auth_manager.acquire_token()
    
    if token_result and "access_token" in token_result:
        print("✅ Authentication successful!")
        
        # Test Graph API access
        if auth_manager.test_graph_access(token_result["access_token"]):
            print("🎉 MEvals authentication setup complete!")
            print("\n🚀 Ready to collect real meeting data for Scenara 2.0 training")
        else:
            print("❌ Graph API access failed - check permissions")
            return 1
    else:
        print("❌ Authentication failed")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())