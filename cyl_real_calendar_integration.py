#!/usr/bin/env python3
"""
REAL Microsoft Graph Calendar Integration for cyl@microsoft.com
Using actual Azure app registration credentials
App: Me Notes Intelligence (82ec4101-520f-443d-a61e-593dca1f0c95)
"""

import requests
import json
import os
from datetime import datetime, timezone, timedelta
from msal import ConfidentialClientApplication

class CylMicrosoftGraphClient:
    """Real Microsoft Graph API client for cyl@microsoft.com"""
    
    def __init__(self):
        # Your actual Azure app registration details
        self.client_id = "82ec4101-520f-443d-a61e-593dca1f0c95"
        self.tenant_id = "72f988bf-86f1-41af-91ab-2d7cd011db47"
        self.object_id = "006bc003-32ca-46e6-85e8-b3302b4311a9"
        self.app_name = "Me Notes Intelligence"
        
        # These need to be provided
        self.client_secret = None
        self.service_tree_id = None
        self.access_token = None
        self.app = None
        
    def load_config(self):
        """Load configuration from file"""
        try:
            with open('microsoft_graph_config.json', 'r') as f:
                config = json.load(f)
                self.client_secret = config.get('client_secret')
                self.service_tree_id = config.get('service_tree_id')
                print("✅ Configuration loaded from microsoft_graph_config.json")
                return True
        except FileNotFoundError:
            print("❌ Configuration file not found")
            return False
        except Exception as e:
            print(f"❌ Error loading configuration: {e}")
            return False
    
    def setup_remaining_credentials(self):
        """Interactive setup for remaining credentials"""
        print("🔐 SETUP REMAINING CREDENTIALS")
        print("=" * 60)
        print(f"App Name: {self.app_name}")
        print(f"Client ID: {self.client_id}")
        print(f"Tenant ID: {self.tenant_id}")
        print(f"Object ID: {self.object_id}")
        print()
        
        if not self.client_secret:
            print("🔑 CLIENT SECRET NEEDED:")
            print("1. Go to Azure Portal > Your App > 'Certificates & secrets'")
            print("2. Click 'New client secret'")
            print("3. Description: 'Calendar Integration'")
            print("4. Expires: 24 months")
            print("5. Copy the secret value immediately!")
            print()
            
            self.client_secret = input("Enter Client Secret: ").strip()
            
            if not self.client_secret:
                print("❌ Client secret is required")
                return False
        
        if not self.service_tree_id:
            print("\n🌳 SERVICE TREE ID NEEDED:")
            print("1. Go to https://servicetree.msftcloudes.com/")
            print("2. Search for your team/service")
            print("3. Copy the Service Tree ID (GUID format)")
            print("4. Or ask your team lead for the Service Tree ID")
            print()
            
            self.service_tree_id = input("Enter Service Tree ID (or press Enter to skip): ").strip()
        
        # Save updated config
        config = {
            "client_id": self.client_id,
            "tenant_id": self.tenant_id,
            "client_secret": self.client_secret,
            "service_tree_id": self.service_tree_id,
            "user_email": "cyl@microsoft.com",
            "app_name": self.app_name,
            "object_id": self.object_id,
            "created_date": "2025-10-22",
            "environment": "development"
        }
        
        with open('microsoft_graph_config.json', 'w') as f:
            json.dump(config, f, indent=2)
        
        print("✅ Configuration updated and saved")
        return True
    
    def authenticate(self):
        """Authenticate with Microsoft Graph using MSAL"""
        if not self.client_secret:
            print("❌ Client secret required for authentication")
            return False
        
        try:
            # Create MSAL app with your credentials
            authority = f"https://login.microsoftonline.com/{self.tenant_id}"
            self.app = ConfidentialClientApplication(
                client_id=self.client_id,
                client_credential=self.client_secret,
                authority=authority
            )
            
            # Get token for Microsoft Graph
            scopes = ["https://graph.microsoft.com/.default"]
            
            print("🔑 Authenticating with Microsoft Graph...")
            result = self.app.acquire_token_for_client(scopes=scopes)
            
            if "access_token" in result:
                self.access_token = result["access_token"]
                print("✅ Successfully authenticated!")
                return True
            else:
                error = result.get('error_description', 'Unknown error')
                print(f"❌ Authentication failed: {error}")
                print(f"   Error: {result.get('error', 'Unknown')}")
                return False
                
        except Exception as e:
            print(f"❌ Authentication error: {str(e)}")
            return False
    
    def test_connection(self):
        """Test connection and get user info"""
        if not self.access_token:
            return False
        
        try:
            headers = {
                'Authorization': f'Bearer {self.access_token}',
                'Content-Type': 'application/json'
            }
            
            # Test with specific user endpoint
            response = requests.get(
                "https://graph.microsoft.com/v1.0/users/cyl@microsoft.com",
                headers=headers
            )
            
            if response.status_code == 200:
                user_data = response.json()
                print("✅ Connection test successful!")
                print(f"👤 User: {user_data.get('displayName', 'Unknown')}")
                print(f"📧 Email: {user_data.get('mail', user_data.get('userPrincipalName', 'Unknown'))}")
                print(f"🏢 Department: {user_data.get('department', 'Unknown')}")
                print(f"💼 Job Title: {user_data.get('jobTitle', 'Unknown')}")
                return True
            else:
                print(f"❌ Connection test failed: {response.status_code}")
                print(f"Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Connection test error: {str(e)}")
            return False
    
    def get_calendar_events(self, date="2025-10-22"):
        """Get REAL calendar events for cyl@microsoft.com"""
        if not self.access_token:
            return None
        
        try:
            headers = {
                'Authorization': f'Bearer {self.access_token}',
                'Content-Type': 'application/json'
            }
            
            # Query calendar events for specific user and date
            start_time = f"{date}T00:00:00.000Z"
            end_time = f"{date}T23:59:59.999Z"
            
            url = "https://graph.microsoft.com/v1.0/users/cyl@microsoft.com/calendar/events"
            params = {
                '$filter': f"start/dateTime ge '{start_time}' and start/dateTime le '{end_time}'",
                '$select': 'subject,start,end,responseStatus,attendees,location,importance,showAs,body',
                '$orderby': 'start/dateTime asc'
            }
            
            print(f"🔍 Getting real calendar events for cyl@microsoft.com on {date}...")
            response = requests.get(url, headers=headers, params=params)
            
            if response.status_code == 200:
                events_data = response.json()
                events = events_data.get('value', [])
                print(f"✅ Retrieved {len(events)} real calendar events")
                return self.process_real_events(events, date)
            else:
                print(f"❌ Failed to get calendar events: {response.status_code}")
                print(f"Response: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Calendar query error: {str(e)}")
            return None
    
    def process_real_events(self, events, date):
        """Process real calendar events and show RSVP status"""
        if not events:
            print(f"📭 No meetings found for {date}")
            return {
                'events': [],
                'summary': {'accepted': 0, 'tentative': 0, 'declined': 0, 'none': 0},
                'total_events': 0,
                'date': date,
                'user': 'cyl@microsoft.com',
                'source': 'REAL MICROSOFT 365 CALENDAR'
            }
        
        processed_events = []
        rsvp_counts = {'accepted': 0, 'tentative': 0, 'declined': 0, 'none': 0}
        
        print(f"\n📅 CYL'S REAL CALENDAR FOR {date}")
        print("=" * 80)
        print("⚠️  DATA SOURCE: ACTUAL MICROSOFT 365 CALENDAR")
        print(f"👤 User: cyl@microsoft.com")
        print(f"🏢 App: {self.app_name}")
        print("=" * 80)
        
        for i, event in enumerate(events, 1):
            subject = event.get('subject', 'No Subject')
            start = event.get('start', {})
            end = event.get('end', {})
            location = event.get('location', {}).get('displayName', 'No location')
            importance = event.get('importance', 'normal')
            
            # Parse start/end times
            start_time = start.get('dateTime', '')
            end_time = end.get('dateTime', '')
            
            if start_time and end_time:
                start_dt = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
                end_dt = datetime.fromisoformat(end_time.replace('Z', '+00:00'))
                
                # Convert to Pacific Time (UTC-7 for PDT)
                pacific_start = start_dt - timedelta(hours=7)
                pacific_end = end_dt - timedelta(hours=7)
                
                time_display = f"{pacific_start.strftime('%I:%M %p')} - {pacific_end.strftime('%I:%M %p')} PDT"
                duration = end_dt - start_dt
                duration_str = f"{int(duration.total_seconds() / 60)} min"
            else:
                time_display = 'Time not available'
                duration_str = 'Unknown duration'
            
            # Get RSVP status
            response_status = event.get('responseStatus', {})
            rsvp = response_status.get('response', 'none').lower()
            rsvp_counts[rsvp] = rsvp_counts.get(rsvp, 0) + 1
            
            # RSVP emoji and status
            rsvp_emoji = {
                'accepted': '✅', 'tentative': '❓', 'declined': '❌', 'none': '⏳'
            }.get(rsvp, '❔')
            
            # Importance emoji
            importance_emoji = {
                'high': '🔴', 'normal': '🔵', 'low': '🟡'
            }.get(importance, '🔵')
            
            processed_event = {
                'number': i,
                'subject': subject,
                'time_display': time_display,
                'duration': duration_str,
                'location': location,
                'rsvp_status': rsvp,
                'rsvp_emoji': rsvp_emoji,
                'importance': importance,
                'importance_emoji': importance_emoji
            }
            processed_events.append(processed_event)
            
            # Display event
            print(f"\n{i}. {rsvp_emoji} {importance_emoji} {subject}")
            print(f"   ⏰ {time_display} ({duration_str})")
            print(f"   📍 {location}")
            print(f"   📝 RSVP: {rsvp.upper()}")
            print(f"   🔔 Priority: {importance.upper()}")
        
        # Summary with validation
        print(f"\n📊 REAL CALENDAR SUMMARY")
        print("=" * 60)
        print(f"📅 Date: {date}")
        print(f"👤 User: cyl@microsoft.com")
        print(f"📱 Total Meetings: {len(events)}")
        print(f"✅ Accepted: {rsvp_counts['accepted']}")
        print(f"❓ Tentative: {rsvp_counts['tentative']}")
        print(f"❌ Declined: {rsvp_counts['declined']}")
        print(f"⏳ No Response: {rsvp_counts['none']}")
        
        # Validation against expected (1 accepted + 7 tentative)
        expected_accepted = 1
        expected_tentative = 7
        actual_accepted = rsvp_counts['accepted']
        actual_tentative = rsvp_counts['tentative']
        
        print(f"\n🔍 VALIDATION CHECK")
        print("=" * 40)
        print(f"Expected: {expected_accepted} accepted + {expected_tentative} tentative = 8 total")
        print(f"Actual: {actual_accepted} accepted + {actual_tentative} tentative = {len(events)} total")
        
        matches = (actual_accepted == expected_accepted and 
                  actual_tentative == expected_tentative)
        
        if matches:
            print("✅ PERFECT MATCH! Calendar matches your expectation.")
        else:
            print("⚠️  COUNT DIFFERENCE:")
            if actual_accepted != expected_accepted:
                print(f"   Accepted: Expected {expected_accepted}, Got {actual_accepted}")
            if actual_tentative != expected_tentative:
                print(f"   Tentative: Expected {expected_tentative}, Got {actual_tentative}")
        
        return {
            'events': processed_events,
            'summary': rsvp_counts,
            'total_events': len(events),
            'date': date,
            'user': 'cyl@microsoft.com',
            'source': 'REAL MICROSOFT 365 CALENDAR',
            'app_info': {
                'name': self.app_name,
                'client_id': self.client_id,
                'object_id': self.object_id
            },
            'validation': {
                'expected_accepted': expected_accepted,
                'expected_tentative': expected_tentative,
                'actual_accepted': actual_accepted,
                'actual_tentative': actual_tentative,
                'matches_expectation': matches
            }
        }

def main():
    """Main function to get real calendar data for cyl@microsoft.com"""
    print("🚀 REAL MICROSOFT GRAPH CALENDAR FOR CYL@MICROSOFT.COM")
    print("=" * 80)
    print("App: Me Notes Intelligence")
    print("Client ID: 82ec4101-520f-443d-a61e-593dca1f0c95")
    print("Target: October 22, 2025 (Today)")
    print("Expected: 1 accepted + 7 tentative meetings")
    print("=" * 80)
    
    # Initialize client
    client = CylMicrosoftGraphClient()
    
    # Load existing config
    print("\n🔧 STEP 1: Load Configuration")
    client.load_config()
    
    # Setup remaining credentials
    print("\n🔐 STEP 2: Setup Credentials")
    if not client.setup_remaining_credentials():
        print("❌ Credential setup failed")
        return None
    
    # Authenticate
    print("\n🔑 STEP 3: Authenticate")
    if not client.authenticate():
        print("❌ Authentication failed")
        print("💡 Next steps:")
        print("1. Check that you've created a client secret")
        print("2. Ensure API permissions are granted")
        print("3. Verify admin consent was completed")
        return None
    
    # Test connection
    print("\n🔗 STEP 4: Test Connection")
    if not client.test_connection():
        print("❌ Connection test failed")
        return None
    
    # Get real calendar events
    print("\n📅 STEP 5: Get Your Real Calendar")
    calendar_data = client.get_calendar_events("2025-10-22")
    
    if calendar_data:
        # Save the real data
        filename = f"cyl_real_calendar_{calendar_data['date'].replace('-', '_')}.json"
        with open(filename, 'w') as f:
            json.dump(calendar_data, f, indent=2, default=str)
        
        print(f"\n💾 Real calendar data saved to: {filename}")
        print("✅ SUCCESS: Retrieved cyl@microsoft.com's real calendar!")
        
        # Next steps
        print(f"\n🎯 READY FOR FLIGHT CI005 ANALYSIS")
        print("Your real meeting data is now available for flight conflict analysis!")
        
        return calendar_data
    else:
        print("❌ Failed to get real calendar data")
        return None

if __name__ == "__main__":
    result = main()
    
    if result:
        print(f"\n✈️  NEXT: Analyze real meeting conflicts with Flight CI005")
        print("Your 4:25 PM PDT flight departure can now be analyzed against actual meetings!")
    else:
        print(f"\n💡 TROUBLESHOOTING:")
        print("1. Ensure client secret is created in Azure Portal")
        print("2. Grant admin consent for API permissions")
        print("3. Check that Calendar.Read permission is added")
        print("4. Verify your Microsoft account has calendar access")