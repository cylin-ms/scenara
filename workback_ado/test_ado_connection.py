#!/usr/bin/env python3
"""Quick test to verify ADO connection"""
import os
from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication

# Get token from environment
PAT = os.environ.get('ADO_PAT')
if not PAT:
    print("❌ ERROR: ADO_PAT environment variable not set")
    exit(1)

# Office organization (legacy URL format)
ORG_URL = "https://office.visualstudio.com"

print(f"🔗 Connecting to: {ORG_URL}")
print(f"🔑 Using PAT token: {PAT[:10]}...{PAT[-4:]}")

try:
    # Authenticate
    credentials = BasicAuthentication('', PAT)
    connection = Connection(base_url=ORG_URL, creds=credentials)
    
    # Get work item tracking client
    wit_client = connection.clients.get_work_item_tracking_client()
    
    # Try to get projects (this will fail if no permission, but connection works)
    print("\n✅ Connection successful!")
    print("\nTrying to list projects...")
    
    try:
        projects = wit_client.get_projects()
        print(f"📁 Found {len(projects.value)} accessible projects:")
        for p in list(projects.value)[:5]:
            print(f"   - {p.name}")
        if len(projects.value) > 5:
            print(f"   ... and {len(projects.value) - 5} more")
    except Exception as e:
        print(f"⚠️  Could not list projects: {e}")
        print("   (This is OK if you don't have project listing permission)")
    
    print("\n✅ ADO connection test PASSED!")
    print("\n📝 Next step: Run the extraction script with your project name")
    
except Exception as e:
    print(f"\n❌ Connection FAILED: {e}")
    print("\nTroubleshooting:")
    print("1. Check token is valid and not expired")
    print("2. Verify token has 'Work Items (Read)' permission")
    print("3. Check organization URL is correct")
    exit(1)
