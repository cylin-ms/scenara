#!/usr/bin/env python3
"""
SIMPLIFIED Microsoft Graph Calendar Integration using Device Flow
Easier authentication for personal Microsoft accounts
"""

import requests
import json
import os
from datetime import datetime, timezone, timedelta
from msal import PublicClientApplication

class SimplifiedGraphClient:
    """Simplified Microsoft Graph client using device flow authentication"""
    
    def __init__(self):
        # Using Microsoft Graph's public client for device flow
        self.client_id = "14d82eec-204b-4c2f-b7e0-296602ddecd0"  # Microsoft Graph CLI client ID
        self.authority = "https://login.microsoftonline.com/common"
        self.scopes = ["User.Read", "Calendars.Read"]
        self.access_token = None
        self.app = None
        
    def authenticate_device_flow(self):
        """Authenticate using device flow (user-friendly)"""
        try:
            print("🔑 SIMPLIFIED AUTHENTICATION (Device Flow)")
            print("=" * 60)
            
            # Create MSAL public client app
            self.app = PublicClientApplication(
                client_id=self.client_id,
                authority=self.authority
            )
            
            # Try cached token first
            accounts = self.app.get_accounts()
            if accounts:
                print("🔄 Checking for cached authentication...")
                result = self.app.acquire_token_silent(self.scopes, account=accounts[0])
                if result and "access_token" in result:
                    self.access_token = result["access_token"]
                    print("✅ Using cached authentication")
                    return True
            
            # Start device flow
            print("🔐 Starting device code flow authentication...")
            flow = self.app.initiate_device_flow(scopes=self.scopes)
            
            if "user_code" not in flow:
                print("❌ Failed to create device flow")
                return False
            
            # Display instructions to user
            print("\n" + "="*60)
            print("📱 AUTHENTICATION REQUIRED")
            print("="*60)
            print(flow['message'])
            print("="*60)
            print("\n⏳ Waiting for you to complete authentication in browser...")
            print("   (This will timeout in a few minutes if not completed)")
            
            # Poll for completion
            result = self.app.acquire_token_by_device_flow(flow)
            
            if "access_token" in result:
                self.access_token = result["access_token"]
                print("\n✅ Authentication successful!")
                return True
            else:
                error = result.get('error_description', 'Unknown error')
                print(f"\n❌ Authentication failed: {error}")
                return False
                
        except Exception as e:
            print(f"❌ Authentication error: {str(e)}")
            return False
    
    def test_connection(self):
        """Test connection and show user info"""
        if not self.access_token:
            return False
        
        try:
            headers = {'Authorization': f'Bearer {self.access_token}'}
            response = requests.get("https://graph.microsoft.com/v1.0/me", headers=headers)
            
            if response.status_code == 200:
                user_data = response.json()
                print(f"\n✅ Connected successfully!")
                print(f"👤 User: {user_data.get('displayName', 'Unknown')}")
                print(f"📧 Email: {user_data.get('mail', user_data.get('userPrincipalName', 'Unknown'))}")
                return True
            else:
                print(f"❌ Connection test failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Connection test error: {str(e)}")
            return False
    
    def get_calendar_events(self, date="2025-10-22"):
        """Get real calendar events for the specified date"""
        if not self.access_token:
            print("❌ Not authenticated")
            return None
        
        try:
            headers = {'Authorization': f'Bearer {self.access_token}'}
            
            # Query for calendar events on specific date
            start_time = f"{date}T00:00:00.000Z"
            end_time = f"{date}T23:59:59.999Z"
            
            url = "https://graph.microsoft.com/v1.0/me/calendar/events"
            params = {
                '$filter': f"start/dateTime ge '{start_time}' and start/dateTime le '{end_time}'",
                '$select': 'subject,start,end,responseStatus,attendees,location,importance',
                '$orderby': 'start/dateTime asc'
            }
            
            print(f"\n📅 Fetching real calendar events for {date}...")
            response = requests.get(url, headers=headers, params=params)
            
            if response.status_code == 200:
                data = response.json()
                events = data.get('value', [])
                print(f"✅ Found {len(events)} real calendar events")
                return self.process_events(events, date)
            elif response.status_code == 403:
                print("❌ Access denied. You may need Calendar.Read permissions.")
                print("   Try using an organizational account with proper permissions.")
                return None
            else:
                print(f"❌ Failed to get calendar events: {response.status_code}")
                print(f"   Response: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Error getting calendar events: {str(e)}")
            return None
    
    def process_events(self, events, date):
        """Process and display real calendar events"""
        if not events:
            print(f"📭 No meetings found for {date}")
            return {
                'events': [],
                'summary': {'accepted': 0, 'tentative': 0, 'declined': 0, 'none': 0},
                'total_events': 0,
                'date': date,
                'source': 'REAL MICROSOFT 365 CALENDAR'
            }
        
        processed_events = []
        rsvp_counts = {'accepted': 0, 'tentative': 0, 'declined': 0, 'none': 0}
        
        print(f"\n📅 YOUR REAL CALENDAR FOR {date}")
        print("=" * 60)
        print("⚠️  DATA SOURCE: ACTUAL MICROSOFT 365 CALENDAR")
        print("=" * 60)
        
        for i, event in enumerate(events, 1):
            subject = event.get('subject', 'No Subject')
            start = event.get('start', {})
            location = event.get('location', {}).get('displayName', 'No location')
            
            # Parse start time
            start_time = start.get('dateTime', '')
            if start_time:
                # Convert from UTC to Pacific Time
                dt = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
                pacific_time = dt - timedelta(hours=7)  # PDT is UTC-7
                time_display = pacific_time.strftime('%I:%M %p PDT')
            else:
                time_display = 'Time not available'
            
            # Get RSVP status
            response_status = event.get('responseStatus', {})
            rsvp = response_status.get('response', 'none').lower()
            rsvp_counts[rsvp] = rsvp_counts.get(rsvp, 0) + 1
            
            # RSVP emoji
            rsvp_emoji = {
                'accepted': '✅', 'tentative': '❓', 'declined': '❌', 'none': '⏳'
            }.get(rsvp, '❔')
            
            processed_event = {
                'number': i,
                'subject': subject,
                'time_display': time_display,
                'location': location,
                'rsvp_status': rsvp,
                'rsvp_emoji': rsvp_emoji
            }
            processed_events.append(processed_event)
            
            # Display
            print(f"\n{i}. {rsvp_emoji} {subject}")
            print(f"   ⏰ {time_display}")
            print(f"   📍 {location}")
            print(f"   📝 RSVP: {rsvp.upper()}")
        
        # Summary
        print(f"\n📊 SUMMARY")
        print("=" * 40)
        print(f"Total Meetings: {len(events)}")
        print(f"✅ Accepted: {rsvp_counts['accepted']}")
        print(f"❓ Tentative: {rsvp_counts['tentative']}")
        print(f"❌ Declined: {rsvp_counts['declined']}")
        print(f"⏳ No Response: {rsvp_counts['none']}")
        
        # Validation
        expected_accepted, expected_tentative = 1, 7
        actual_accepted = rsvp_counts['accepted']
        actual_tentative = rsvp_counts['tentative']
        
        print(f"\n🔍 VALIDATION")
        print("=" * 40)
        print(f"Expected: {expected_accepted} accepted + {expected_tentative} tentative")
        print(f"Actual: {actual_accepted} accepted + {actual_tentative} tentative")
        
        if actual_accepted == expected_accepted and actual_tentative == expected_tentative:
            print("✅ PERFECT MATCH!")
        else:
            print("⚠️  COUNT MISMATCH")
        
        return {
            'events': processed_events,
            'summary': rsvp_counts,
            'total_events': len(events),
            'date': date,
            'source': 'REAL MICROSOFT 365 CALENDAR',
            'validation': {
                'expected_accepted': expected_accepted,
                'expected_tentative': expected_tentative,
                'actual_accepted': actual_accepted,
                'actual_tentative': actual_tentative,
                'matches_expectation': (actual_accepted == expected_accepted and 
                                      actual_tentative == expected_tentative)
            }
        }

def main():
    """Main function for simplified authentication"""
    print("🚀 SIMPLIFIED MICROSOFT GRAPH CALENDAR ACCESS")
    print("=" * 80)
    print("Using device flow authentication (easier for personal accounts)")
    print("Target: Your real calendar for October 22, 2025")
    print("=" * 80)
    
    client = SimplifiedGraphClient()
    
    # Authenticate
    print("\n🔑 STEP 1: Authenticate")
    if not client.authenticate_device_flow():
        print("❌ Authentication failed")
        return None
    
    # Test connection
    print("\n🔗 STEP 2: Test Connection")
    if not client.test_connection():
        print("❌ Connection test failed")
        return None
    
    # Get calendar events
    print("\n📅 STEP 3: Get Your Real Calendar")
    calendar_data = client.get_calendar_events("2025-10-22")
    
    if calendar_data:
        # Save the data
        with open('real_calendar_simplified.json', 'w') as f:
            json.dump(calendar_data, f, indent=2, default=str)
        
        print(f"\n💾 Data saved to: real_calendar_simplified.json")
        print("✅ SUCCESS: Retrieved your real calendar data!")
        
        return calendar_data
    else:
        print("❌ Failed to get calendar data")
        return None

if __name__ == "__main__":
    result = main()
    
    if result:
        print(f"\n🎯 NEXT STEP: Flight CI005 Conflict Analysis")
        print("Now we can analyze real conflicts with your 4:25 PM PDT flight!")
    else:
        print(f"\n💡 If authentication failed, you may need:")
        print("   - Organizational Microsoft account")
        print("   - Calendar permissions enabled")
        print("   - Azure app registration (use the other script)")