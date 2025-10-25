#!/usr/bin/env python3
"""
Microsoft Graph API Client using MSAL
More reliable authentication for calendar access
"""

import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import msal
import requests

class MSALMeetingClient:
    def __init__(self):
        # Azure CLI client ID (widely supported)
        self.client_id = "04b07795-8ddb-461a-bbee-02f9e1bf7b46"
        self.scopes = [
            "https://graph.microsoft.com/User.Read",
            "https://graph.microsoft.com/Calendars.Read"
        ]
        self.access_token = None
        
        # Create MSAL app
        self.app = msal.PublicClientApplication(
            client_id=self.client_id,
            authority="https://login.microsoftonline.com/common"
        )
    
    def authenticate(self) -> bool:
        """Authenticate using MSAL device flow"""
        print("🔐 Authenticating with Microsoft Graph (MSAL)...")
        print("This will open a browser for you to sign in with your Microsoft account")
        
        try:
            # Try interactive authentication first
            print("🌐 Opening browser for interactive authentication...")
            
            result = self.app.acquire_token_interactive(
                scopes=self.scopes,
                prompt="select_account"
            )
            
            if "access_token" in result:
                self.access_token = result["access_token"]
                print("✅ Interactive authentication successful!")
                return True
            else:
                print("⚠️ Interactive auth failed, trying device flow...")
                return self.authenticate_device_flow()
                
        except Exception as e:
            print(f"⚠️ Interactive auth not available: {e}")
            print("🔄 Falling back to device flow...")
            return self.authenticate_device_flow()
    
    def authenticate_device_flow(self) -> bool:
        """Fallback device flow authentication"""
        try:
            # Initiate device flow
            flow = self.app.initiate_device_flow(scopes=self.scopes)
            
            if "user_code" not in flow:
                print("❌ Failed to create device flow")
                return False
            
            print(f"\n📱 Please visit: {flow['verification_uri']}")
            print(f"🔢 Enter code: {flow['user_code']}")
            print("⏳ Waiting for you to complete authentication...")
            
            # Complete device flow
            result = self.app.acquire_token_by_device_flow(flow)
            
            if "access_token" in result:
                self.access_token = result["access_token"]
                print("✅ Device flow authentication successful!")
                return True
            else:
                print(f"❌ Authentication failed: {result.get('error_description', 'Unknown error')}")
                return False
                
        except Exception as e:
            print(f"❌ Device flow authentication failed: {e}")
            return False
    
    def test_connection(self) -> bool:
        """Test the Graph API connection"""
        if not self.access_token:
            print("❌ No access token. Please authenticate first.")
            return False
        
        try:
            headers = {"Authorization": f"Bearer {self.access_token}"}
            response = requests.get("https://graph.microsoft.com/v1.0/me", headers=headers)
            
            if response.status_code == 200:
                user_data = response.json()
                print(f"✅ Connected as: {user_data.get('displayName')} ({user_data.get('mail')})")
                return True
            else:
                print(f"❌ Connection test failed: {response.status_code}")
                print(response.text)
                return False
                
        except Exception as e:
            print(f"❌ Connection test error: {e}")
            return False
    
    def get_calendar_events(self, days_back: int = 90, max_events: int = 250) -> List[Dict]:
        """Get calendar events from the last N days"""
        if not self.access_token:
            print("❌ No access token. Please authenticate first.")
            return []
        
        try:
            headers = {"Authorization": f"Bearer {self.access_token}"}
            
            # Calculate date range
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days_back)
            
            all_events = []
            page_size = 50
            skip = 0
            
            print(f"📅 Fetching calendar events from last {days_back} days...")
            
            while len(all_events) < max_events:
                params = {
                    '$top': min(page_size, max_events - len(all_events)),
                    '$skip': skip,
                    '$orderby': 'start/dateTime desc',
                    '$filter': f"start/dateTime ge '{start_date.isoformat()}Z'",
                    '$select': 'subject,bodyPreview,start,end,attendees,organizer,isOnlineMeeting,onlineMeetingProvider,location,recurrence,importance,sensitivity'
                }
                
                print(f"📥 Fetching page {(skip // page_size) + 1}...")
                
                response = requests.get(
                    "https://graph.microsoft.com/v1.0/me/events",
                    headers=headers,
                    params=params
                )
                
                if response.status_code == 200:
                    events_data = response.json()
                    page_events = events_data.get('value', [])
                    
                    if not page_events:
                        print(f"📄 No more events found")
                        break
                    
                    all_events.extend(page_events)
                    skip += len(page_events)
                    
                    print(f"✅ Retrieved {len(page_events)} events (Total: {len(all_events)})")
                    
                    if len(page_events) < page_size:
                        break
                        
                else:
                    print(f"❌ Failed to get calendar events: {response.status_code}")
                    if response.status_code == 401:
                        print("🔄 Token may have expired. Please re-authenticate.")
                    print(response.text)
                    break
            
            print(f"🎯 Final result: Retrieved {len(all_events)} real calendar events")
            return all_events
                
        except Exception as e:
            print(f"❌ Error getting calendar events: {e}")
            return []
    
    def format_for_promptcot(self, events: List[Dict]) -> List[Dict]:
        """Convert Graph API events to Meeting PromptCoT format"""
        formatted_scenarios = []
        
        for i, event in enumerate(events):
            try:
                # Extract attendee information
                attendees = []
                attendee_emails = []
                if event.get('attendees'):
                    for attendee in event['attendees']:
                        if attendee.get('emailAddress'):
                            name = attendee['emailAddress'].get('name', 'Unknown')
                            email = attendee['emailAddress'].get('address', '')
                            attendees.append(name)
                            attendee_emails.append(email)
                
                # Calculate meeting duration
                duration_minutes = 60  # default
                if event.get('start') and event.get('end'):
                    try:
                        start_time = datetime.fromisoformat(event['start']['dateTime'].replace('Z', '+00:00'))
                        end_time = datetime.fromisoformat(event['end']['dateTime'].replace('Z', '+00:00'))
                        duration_minutes = int((end_time - start_time).total_seconds() / 60)
                    except:
                        pass
                
                # Classify meeting type based on subject and content
                meeting_type = self.classify_meeting_type(event.get('subject', ''), event.get('bodyPreview', ''))
                
                # Analyze preparation needs
                prep_requirements = self.analyze_preparation_needs(event, attendees, duration_minutes)
                
                formatted_scenario = {
                    'id': f"real_calendar_{i+1:03d}",
                    'source': 'microsoft_calendar_msal',
                    'context': {
                        'subject': event.get('subject', 'No Subject'),
                        'description': event.get('bodyPreview', ''),
                        'attendees': attendees,
                        'attendee_count': len(attendees),
                        'attendee_emails': attendee_emails,
                        'organizer': event.get('organizer', {}).get('emailAddress', {}).get('name', 'Unknown'),
                        'duration_minutes': duration_minutes,
                        'start_time': event.get('start', {}).get('dateTime', ''),
                        'end_time': event.get('end', {}).get('dateTime', ''),
                        'is_online_meeting': event.get('isOnlineMeeting', False),
                        'meeting_provider': event.get('onlineMeetingProvider', ''),
                        'location': event.get('location', {}).get('displayName', ''),
                        'importance': event.get('importance', 'normal'),
                        'is_recurring': event.get('recurrence') is not None
                    },
                    'meeting_type': meeting_type,
                    'preparation_requirements': prep_requirements,
                    'complexity': self.assess_complexity(event, attendees, duration_minutes),
                    'quality_score': self.calculate_quality_score(event, attendees),
                    'extracted_date': datetime.now().isoformat()
                }
                
                formatted_scenarios.append(formatted_scenario)
                
            except Exception as e:
                print(f"⚠️ Warning: Error formatting event {i+1}: {e}")
                continue
        
        print(f"✅ Formatted {len(formatted_scenarios)} real meeting scenarios")
        return formatted_scenarios
    
    def classify_meeting_type(self, subject: str, description: str) -> str:
        """Classify meeting type based on subject and description"""
        text = f"{subject} {description}".lower()
        
        type_keywords = {
            'Technical Design Review': ['design', 'architecture', 'technical', 'system', 'api', 'infrastructure', 'code'],
            'Product Strategy Session': ['strategy', 'roadmap', 'product', 'vision', 'planning', 'goals', 'feature'],
            'Team Retrospective': ['retro', 'retrospective', 'sprint review', 'reflection', 'lessons', 'standup'],
            'Budget Planning Meeting': ['budget', 'financial', 'cost', 'funding', 'investment', 'allocation'],
            'Customer Discovery Call': ['customer', 'user', 'feedback', 'discovery', 'interview', 'research'],
            'Cross-team Collaboration': ['sync', 'alignment', 'coordination', 'cross-team', 'collaboration'],
            'Training Session': ['training', 'workshop', 'learning', 'education', 'tutorial', 'onboarding'],
            'Performance Review': ['performance', 'review', 'evaluation', 'assessment', 'metrics', '1:1'],
            'Vendor Evaluation': ['vendor', 'supplier', 'evaluation', 'procurement', 'rfp', 'selection'],
            'Project Status Update': ['status', 'update', 'progress', 'checkpoint', 'milestone', 'tracking']
        }
        
        for meeting_type, keywords in type_keywords.items():
            if any(keyword in text for keyword in keywords):
                return meeting_type
        
        return 'General Business Meeting'
    
    def analyze_preparation_needs(self, event: Dict, attendees: List[str], duration: int) -> List[str]:
        """Analyze what preparation is needed for this meeting"""
        requirements = ["Review agenda and objectives"]
        
        # Base on attendee count
        if len(attendees) > 8:
            requirements.extend([
                "Coordinate schedules across teams",
                "Prepare executive summary",
                "Set up meeting recording"
            ])
        elif len(attendees) > 5:
            requirements.append("Prepare stakeholder updates")
        
        # Base on duration
        if duration > 120:
            requirements.extend([
                "Prepare detailed presentation",
                "Plan break schedules"
            ])
        elif duration > 60:
            requirements.append("Prepare comprehensive materials")
        
        # Base on meeting content
        subject = event.get('subject', '').lower()
        description = event.get('bodyPreview', '').lower()
        text = f"{subject} {description}"
        
        if any(word in text for word in ['budget', 'financial', 'cost']):
            requirements.extend(["Gather financial reports", "Prepare budget analysis"])
        
        if any(word in text for word in ['technical', 'system', 'architecture']):
            requirements.extend(["Review technical documentation", "Prepare system diagrams"])
        
        return list(set(requirements))
    
    def assess_complexity(self, event: Dict, attendees: List[str], duration: int) -> str:
        """Assess meeting complexity"""
        complexity_score = 0
        
        if len(attendees) > 8:
            complexity_score += 3
        elif len(attendees) > 5:
            complexity_score += 2
        elif len(attendees) > 2:
            complexity_score += 1
        
        if duration > 180:
            complexity_score += 3
        elif duration > 120:
            complexity_score += 2
        elif duration > 60:
            complexity_score += 1
        
        if event.get('importance') == 'high':
            complexity_score += 2
        
        if complexity_score >= 6:
            return 'critical'
        elif complexity_score >= 4:
            return 'high'
        elif complexity_score >= 2:
            return 'medium'
        else:
            return 'low'
    
    def calculate_quality_score(self, event: Dict, attendees: List[str]) -> float:
        """Calculate quality score for real meeting data"""
        score = 7.0  # Higher base for real data
        
        if event.get('subject') and len(event['subject']) > 10:
            score += 1.0
        
        if event.get('bodyPreview') and len(event['bodyPreview']) > 50:
            score += 0.5
        
        if len(attendees) >= 3:
            score += 0.5
        
        if event.get('isOnlineMeeting'):
            score += 0.5
        
        if event.get('importance') == 'high':
            score += 0.5
        
        return min(score, 10.0)
    
    def save_meeting_data(self, scenarios: List[Dict], output_path: str = "meeting_prep_data/real_calendar_scenarios.json"):
        """Save real meeting data to file"""
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(scenarios, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Saved {len(scenarios)} real meeting scenarios to {output_path}")

def main():
    """Main execution function"""
    print("🚀 Real Calendar Data Extractor (MSAL)")
    print("Extract YOUR actual meeting data from Microsoft Calendar")
    print("-" * 60)
    
    client = MSALMeetingClient()
    
    # Step 1: Authenticate
    print("\n🔐 Step 1: Authentication")
    if not client.authenticate():
        print("❌ Authentication failed. Exiting.")
        return
    
    # Step 2: Test connection
    print("\n🔗 Step 2: Testing connection")
    if not client.test_connection():
        print("❌ Connection test failed. Exiting.")
        return
    
    # Step 3: Get real calendar events
    print("\n📅 Step 3: Extracting YOUR real calendar events")
    events = client.get_calendar_events(days_back=90, max_events=250)
    
    if not events:
        print("❌ No events found or extraction failed.")
        print("💡 Make sure you have calendar events in the last 90 days")
        return
    
    # Step 4: Format for PromptCoT
    print("\n🔄 Step 4: Formatting for Meeting PromptCoT")
    scenarios = client.format_for_promptcot(events)
    
    # Step 5: Save data
    print("\n💾 Step 5: Saving real meeting data")
    client.save_meeting_data(scenarios)
    
    # Summary
    print("\n📊 Real Calendar Data Summary:")
    print(f"Calendar events extracted: {len(events)}")
    print(f"Formatted scenarios: {len(scenarios)}")
    
    if scenarios:
        avg_quality = sum(s.get('quality_score', 0) for s in scenarios) / len(scenarios)
        print(f"Average quality score: {avg_quality:.2f}/10.0")
        
        meeting_types = {}
        for scenario in scenarios:
            mt = scenario.get('meeting_type', 'Unknown')
            meeting_types[mt] = meeting_types.get(mt, 0) + 1
        
        print(f"Meeting types found: {len(meeting_types)}")
        for mt, count in meeting_types.items():
            print(f"  - {mt}: {count}")
    
    print("\n🎯 SUCCESS! Your real meeting data is ready.")
    print("Next steps:")
    print("1. Run: python update_training_data.py")
    print("2. Launch: streamlit run meeting_data_explorer.py")
    print("3. Access: http://localhost:8501")

if __name__ == "__main__":
    main()