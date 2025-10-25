#!/usr/bin/env python3
"""
Direct Graph API Extractor with Device Code Authentication

Uses MSAL for direct authentication (bypasses Graph Explorer tenant restrictions).
Requests Chat.Read permission along with other collaboration scopes.

This approach:
- Uses your personal authentication (not third-party Graph Explorer app)
- Requests permissions directly from Microsoft Graph
- Should work even if Graph Explorer is blocked by org policy
"""

import json
import requests
from datetime import datetime
from pathlib import Path
import msal

class DirectGraphAPIExtractor:
    def __init__(self):
        # Using Scenara project's registered app (MEvals/SilverFlow)
        # Service Tree ID: 1a0be78a-5efe-4f33-a6d0-2872c428dcf7
        self.client_id = "9ce97a32-d9ab-4ab2-aadc-f49b39b94e11"
        
        # Requested scopes including Chat.Read
        self.scopes = [
            "User.Read",
            "People.Read", 
            "Calendars.Read",
            "Mail.Read",
            "Files.Read.All",
            "Sites.Read.All",
            "Chat.Read",  # <-- Teams chat access
            "Chat.ReadBasic"  # <-- Basic chat metadata
        ]
        
        # Microsoft tenant ID (from mevals_auth_manager.py and daily_meeting_viewer.py)
        self.authority = "https://login.microsoftonline.com/72f988bf-86f1-41af-91ab-2d7cd011db47"
        self.graph_endpoint = "https://graph.microsoft.com/v1.0"
        
        # Initialize MSAL public client
        self.app = msal.PublicClientApplication(
            client_id=self.client_id,
            authority=self.authority
        )
        
        self.access_token = None
        
    def authenticate(self):
        """
        Authenticate using device code flow.
        User will see a code to enter at microsoft.com/devicelogin
        """
        print("🔐 Starting authentication...")
        print("=" * 70)
        
        # Initiate device flow
        flow = self.app.initiate_device_flow(scopes=self.scopes)
        
        if "user_code" not in flow:
            raise ValueError(f"Failed to create device flow: {flow}")
        
        # Show user instructions
        print(f"\n📱 To sign in:")
        print(f"   1. Open: {flow['verification_uri']}")
        print(f"   2. Enter code: {flow['user_code']}")
        print(f"   3. Sign in with your Microsoft account")
        print(f"\n⏳ Waiting for authentication...")
        print("=" * 70)
        
        # Wait for user to authenticate
        result = self.app.acquire_token_by_device_flow(flow)
        
        if "access_token" in result:
            self.access_token = result["access_token"]
            print("\n✅ Authentication successful!")
            return True
        else:
            error = result.get("error_description", result.get("error"))
            print(f"\n❌ Authentication failed: {error}")
            return False
    
    def query_graph_api(self, endpoint, description=""):
        """Execute a Graph API query"""
        if not self.access_token:
            raise ValueError("Not authenticated. Call authenticate() first.")
        
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
        url = f"{self.graph_endpoint}/{endpoint}" if not endpoint.startswith("http") else endpoint
        
        print(f"\n📊 Querying: {description or endpoint}")
        
        try:
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                print(f"   ✅ Success ({len(response.content)} bytes)")
                return response.json()
            else:
                print(f"   ❌ Error {response.status_code}: {response.text[:200]}")
                return {"error": response.json() if response.text else {"message": "Unknown error"}}
                
        except Exception as e:
            print(f"   ❌ Exception: {e}")
            return {"error": {"message": str(e)}}
    
    def collect_collaboration_data(self):
        """Collect all collaboration data including Teams chat"""
        
        queries = [
            {
                "name": "People API - Microsoft ML Collaboration Rankings",
                "endpoint": "me/people",
                "description": "Graph API People rankings"
            },
            {
                "name": "Calendar Meetings Analysis",
                "endpoint": "me/calendar/events?$select=subject,organizer,attendees,start,end&$top=100",
                "description": "Recent calendar meetings"
            },
            {
                "name": "Email Communication Patterns",
                "endpoint": "me/messages?$select=from,toRecipients,subject,receivedDateTime&$top=100",
                "description": "Recent email communications"
            },
            {
                "name": "Recent Collaboration Items",
                "endpoint": "me/insights/shared?$top=50",
                "description": "Shared documents and files"
            },
            {
                "name": "Teams Chat Collaboration",
                "endpoint": "me/chats?$expand=members&$top=50",
                "description": "Teams chat conversations"
            }
        ]
        
        results = {
            "timestamp": datetime.now().isoformat(),
            "authentication_method": "MSAL Device Code Flow",
            "scopes_requested": self.scopes,
            "responses": {}
        }
        
        print("\n" + "=" * 70)
        print("🔍 COLLECTING COLLABORATION DATA")
        print("=" * 70)
        
        for query in queries:
            response = self.query_graph_api(query["endpoint"], query["description"])
            results["responses"][query["name"]] = response
            
            # Brief pause between requests
            import time
            time.sleep(0.5)
        
        return results
    
    def save_results(self, results):
        """Save results to JSON file"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_dir = Path("data/evaluation_results")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        output_file = output_dir / f"graph_collaboration_analysis_{timestamp}.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Results saved to: {output_file}")
        return str(output_file)
    
    def print_summary(self, results):
        """Print summary of collected data"""
        print("\n" + "=" * 70)
        print("📈 COLLECTION SUMMARY")
        print("=" * 70)
        
        for query_name, response in results["responses"].items():
            if "error" in response:
                error_msg = response["error"].get("message", "Unknown error")
                print(f"❌ {query_name}: {error_msg}")
            elif "value" in response:
                count = len(response["value"])
                print(f"✅ {query_name}: {count} items")
            else:
                print(f"⚠️  {query_name}: Unexpected response format")
        
        print("=" * 70)

def main():
    """Main execution"""
    print("\n🚀 Direct Graph API Collaboration Data Extractor")
    print("=" * 70)
    print("This tool uses device code authentication to collect collaboration data")
    print("including Teams chat, without requiring Graph Explorer access.")
    print("=" * 70)
    
    extractor = DirectGraphAPIExtractor()
    
    # Step 1: Authenticate
    if not extractor.authenticate():
        print("\n❌ Authentication failed. Exiting.")
        return 1
    
    # Step 2: Collect data
    results = extractor.collect_collaboration_data()
    
    # Step 3: Save results
    output_file = extractor.save_results(results)
    
    # Step 4: Print summary
    extractor.print_summary(results)
    
    print(f"\n✅ Complete! Data saved to: {output_file}")
    print("\n💡 Next steps:")
    print("   1. Run: python tools/collaborator_discovery.py --limit 15")
    print("   2. Check if Vani Soff and others moved up with Teams chat data")
    
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())
