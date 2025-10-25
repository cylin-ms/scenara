#!/usr/bin/env python3
"""
REAL Microsoft Graph Calendar Integration for cyl@microsoft.com
Connecting to actual Microsoft 365 calendar to get real meeting data for October 22, 2025
"""

import requests
import json
import os
from datetime import datetime, timezone, timedelta
from msal import ConfidentialClientApplication, PublicClientApplication

class RealMicrosoftGraphClient:
    """Real Microsoft Graph API client for actual calendar data"""
    
    def __init__(self):
        self.client_id = None
        self.client_secret = None
        self.tenant_id = None
        self.access_token = None
        self.app = None
        
    def setup_credentials(self):
        """Interactive setup for Microsoft Graph credentials"""
        print("🔐 REAL MICROSOFT GRAPH SETUP")
        print("=" * 60)
        print("We need to connect to your actual Microsoft 365 account.")
        print("This requires Azure app registration credentials.")
        print()
        
        # Check for existing config
        config_file = 'real_graph_config.json'
        if os.path.exists(config_file):
            print("📁 Found existing configuration file.")
            use_existing = input("Use existing credentials? (y/n): ").lower().strip()
            if use_existing == 'y':
                with open(config_file, 'r') as f:
                    config = json.load(f)
                    self.client_id = config.get('client_id')
                    self.client_secret = config.get('client_secret') 
                    self.tenant_id = config.get('tenant_id')
                    print("✅ Loaded existing credentials")
                    return True
        
        print("\n🔧 Azure App Registration Required")
        print("Please provide your Azure app registration details:")
        print("(If you don't have these, we'll guide you through creating them)")
        print()
        
        # Get credentials interactively
        self.client_id = input("Client ID (Application ID): ").strip()
        self.client_secret = input("Client Secret: ").strip()
        self.tenant_id = input("Tenant ID (Directory ID): ").strip()
        
        # Save credentials
        config = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'tenant_id': self.tenant_id
        }
        
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"✅ Credentials saved to {config_file}")
        return True
    
    def authenticate(self):
        """Authenticate with Microsoft Graph using MSAL"""
        if not all([self.client_id, self.client_secret, self.tenant_id]):
            print("❌ Missing credentials. Please run setup_credentials() first.")
            return False
        
        try:
            # Create MSAL app
            authority = f"https://login.microsoftonline.com/{self.tenant_id}"
            self.app = ConfidentialClientApplication(
                client_id=self.client_id,
                client_credential=self.client_secret,
                authority=authority
            )
            
            # Get token for Microsoft Graph
            scopes = ["https://graph.microsoft.com/.default"]
            
            # Try to get cached token first
            accounts = self.app.get_accounts()
            if accounts:
                print("🔄 Attempting to use cached token...")
                result = self.app.acquire_token_silent(scopes, account=accounts[0])
            else:
                result = None
            
            # If no cached token, get new one
            if not result:
                print("🔑 Acquiring new access token...")
                result = self.app.acquire_token_for_client(scopes=scopes)
            
            if "access_token" in result:
                self.access_token = result["access_token"]
                print("✅ Successfully authenticated with Microsoft Graph")
                return True
            else:
                print(f"❌ Authentication failed: {result.get('error_description', 'Unknown error')}")
                return False
                
        except Exception as e:
            print(f"❌ Authentication error: {str(e)}")
            return False
    
    def test_connection(self):
        """Test the connection by getting user info"""
        if not self.access_token:
            print("❌ No access token. Please authenticate first.")
            return False
        
        try:
            headers = {
                'Authorization': f'Bearer {self.access_token}',
                'Content-Type': 'application/json'
            }
            
            # Test with user info endpoint
            response = requests.get(
                "https://graph.microsoft.com/v1.0/me",
                headers=headers
            )
            
            if response.status_code == 200:
                user_data = response.json()
                print("✅ Connection test successful!")
                print(f"👤 Connected as: {user_data.get('displayName', 'Unknown')}")
                print(f"📧 Email: {user_data.get('mail', user_data.get('userPrincipalName', 'Unknown'))}")
                return True
            else:
                print(f"❌ Connection test failed: {response.status_code}")
                print(f"Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Connection test error: {str(e)}")
            return False
    
    def get_real_calendar_events(self, date="2025-10-22"):
        """Get REAL calendar events for the specified date"""
        if not self.access_token:
            print("❌ No access token. Please authenticate first.")
            return None
        
        try:
            headers = {
                'Authorization': f'Bearer {self.access_token}',
                'Content-Type': 'application/json'
            }
            
            # Format date range for the specific day
            start_time = f"{date}T00:00:00.000Z"
            end_time = f"{date}T23:59:59.999Z"
            
            # Graph API query for calendar events
            url = "https://graph.microsoft.com/v1.0/me/calendar/events"
            params = {
                '$filter': f"start/dateTime ge '{start_time}' and start/dateTime le '{end_time}'",
                '$select': 'subject,start,end,responseStatus,attendees,location,body,importance,showAs',
                '$orderby': 'start/dateTime asc'
            }
            
            print(f"🔍 Querying real calendar events for {date}...")
            response = requests.get(url, headers=headers, params=params)
            
            if response.status_code == 200:
                events_data = response.json()
                events = events_data.get('value', [])
                
                print(f"✅ Successfully retrieved {len(events)} real calendar events")
                return self.process_real_events(events, date)
            else:
                print(f"❌ Failed to get calendar events: {response.status_code}")
                print(f"Response: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Calendar query error: {str(e)}")
            return None
    
    def process_real_events(self, events, date):
        """Process real calendar events and extract RSVP information"""
        processed_events = []
        
        rsvp_counts = {
            'accepted': 0,
            'tentative': 0,
            'declined': 0,
            'none': 0
        }
        
        print(f"\n📅 REAL CALENDAR EVENTS FOR {date}")
        print("=" * 60)
        print("⚠️  DATA SOURCE: ACTUAL MICROSOFT 365 CALENDAR")
        print("=" * 60)
        
        for i, event in enumerate(events, 1):
            # Extract basic info
            subject = event.get('subject', 'No Subject')
            start_time = event.get('start', {}).get('dateTime', '')
            end_time = event.get('end', {}).get('dateTime', '')
            location = event.get('location', {}).get('displayName', 'No location')
            
            # Extract RSVP status
            response_status = event.get('responseStatus', {})
            rsvp_response = response_status.get('response', 'none').lower()
            rsvp_counts[rsvp_response] = rsvp_counts.get(rsvp_response, 0) + 1
            
            # Format time for display (convert from UTC if needed)
            if start_time:
                start_dt = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
                # Convert to Pacific Time (UTC-7)
                pacific_time = start_dt - timedelta(hours=7)
                time_display = pacific_time.strftime('%I:%M %p PDT')
            else:
                time_display = 'Time not available'
            
            # RSVP status emoji
            rsvp_emoji = {
                'accepted': '✅',
                'tentative': '❓', 
                'declined': '❌',
                'none': '⏳'
            }.get(rsvp_response, '❔')
            
            processed_event = {
                'number': i,
                'subject': subject,
                'start_time': start_time,
                'end_time': end_time,
                'time_display': time_display,
                'location': location,
                'rsvp_status': rsvp_response,
                'rsvp_emoji': rsvp_emoji,
                'raw_event': event
            }
            
            processed_events.append(processed_event)
            
            # Display event
            print(f"\n{i}. {rsvp_emoji} **{subject}**")
            print(f"   ⏰ Time: {time_display}")
            print(f"   📍 Location: {location}")
            print(f"   📝 RSVP Status: {rsvp_response.upper()}")
        
        # Summary
        print(f"\n📊 REAL CALENDAR SUMMARY FOR {date}")
        print("=" * 60)
        print(f"   📅 Total Meetings: {len(events)}")
        print(f"   ✅ Accepted: {rsvp_counts['accepted']}")
        print(f"   ❓ Tentative: {rsvp_counts['tentative']}")
        print(f"   ❌ Declined: {rsvp_counts['declined']}")
        print(f"   ⏳ No Response: {rsvp_counts['none']}")
        
        # Validation against user expectation
        print(f"\n🔍 VALIDATION CHECK:")
        expected_accepted = 1
        expected_tentative = 7
        
        if rsvp_counts['accepted'] == expected_accepted and rsvp_counts['tentative'] == expected_tentative:
            print("✅ PERFECT MATCH: Calendar matches your expectation!")
            print(f"   Expected: {expected_accepted} accepted + {expected_tentative} tentative")
            print(f"   Actual: {rsvp_counts['accepted']} accepted + {rsvp_counts['tentative']} tentative")
        else:
            print("⚠️  MISMATCH: Calendar doesn't match expectation")
            print(f"   Expected: {expected_accepted} accepted + {expected_tentative} tentative") 
            print(f"   Actual: {rsvp_counts['accepted']} accepted + {rsvp_counts['tentative']} tentative")
        
        return {
            'events': processed_events,
            'summary': rsvp_counts,
            'total_events': len(events),
            'date': date,
            'source': 'REAL MICROSOFT 365 CALENDAR',
            'validation': {
                'expected_accepted': expected_accepted,
                'expected_tentative': expected_tentative,
                'actual_accepted': rsvp_counts['accepted'],
                'actual_tentative': rsvp_counts['tentative'],
                'matches_expectation': (rsvp_counts['accepted'] == expected_accepted and 
                                      rsvp_counts['tentative'] == expected_tentative)
            }
        }

def main():
    """Main function to set up and test real Microsoft Graph connection"""
    print("🚀 REAL MICROSOFT GRAPH CALENDAR INTEGRATION")
    print("=" * 80)
    print("Connecting to cyl@microsoft.com's actual Microsoft 365 calendar")
    print("Target Date: October 22, 2025 (Tomorrow)")
    print("Expected: 1 accepted + 7 tentative meetings")
    print("=" * 80)
    
    # Initialize client
    client = RealMicrosoftGraphClient()
    
    # Setup credentials
    print("\n🔐 STEP 1: Setup Credentials")
    if not client.setup_credentials():
        print("❌ Failed to setup credentials")
        return False
    
    # Authenticate
    print("\n🔑 STEP 2: Authenticate with Microsoft Graph")
    if not client.authenticate():
        print("❌ Authentication failed")
        return False
    
    # Test connection
    print("\n🔗 STEP 3: Test Connection")
    if not client.test_connection():
        print("❌ Connection test failed")
        return False
    
    # Get real calendar events
    print("\n📅 STEP 4: Get Real Calendar Events")
    calendar_data = client.get_real_calendar_events("2025-10-22")
    
    if calendar_data:
        # Save the real data
        with open('real_calendar_oct_22_2025.json', 'w') as f:
            json.dump(calendar_data, f, indent=2, default=str)
        
        print(f"\n💾 Real calendar data saved to: real_calendar_oct_22_2025.json")
        print("✅ REAL MICROSOFT GRAPH INTEGRATION COMPLETE!")
        
        # Next step hint
        print(f"\n🎯 NEXT: Flight CI005 Conflict Analysis")
        print("Now we can analyze real meeting conflicts with your 4:25 PM PDT flight!")
        
        return calendar_data
    else:
        print("❌ Failed to get real calendar events")
        return False

if __name__ == "__main__":
    main()