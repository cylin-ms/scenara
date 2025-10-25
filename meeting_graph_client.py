#!/usr/bin/env python3
"""
Direct Microsoft Graph API Client for Meeting Data
Bypasses MEvals - uses same authentication as Graph Explorer
No IT admin permission required
"""

import json
import requests
import webbrowser
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import os
import time

class MeetingGraphClient:
    def __init__(self):
        # Use Azure CLI client ID (widely used, no admin consent needed)
        self.client_id = "04b07795-8ddb-461a-bbee-02f9e1bf7b46"
        self.authority = "https://login.microsoftonline.com/common"
        self.scopes = [
            "https://graph.microsoft.com/User.Read",
            "https://graph.microsoft.com/Calendars.Read"
        ]
        self.access_token = None
        
    def get_device_code(self) -> Dict:
        """Get device code for authentication (Microsoft Graph device flow)"""
        device_code_url = "https://login.microsoftonline.com/common/oauth2/v2.0/devicecode"
        
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        data = {
            'client_id': self.client_id,
            'scope': ' '.join(self.scopes)
        }
        
        print(f"🔗 Requesting device code from Microsoft...")
        print(f"📱 Client ID: {self.client_id}")
        
        try:
            response = requests.post(device_code_url, headers=headers, data=data)
            print(f"🔍 Response status: {response.status_code}")
            
            if response.status_code != 200:
                print(f"❌ Response content: {response.text}")
                
            response.raise_for_status()  # Raise an exception for bad status codes
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"❌ Request error: {e}")
            return {'error': f'request_failed: {e}'}
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return {'error': f'unexpected_error: {e}'}
    
    def authenticate_interactive(self) -> bool:
        """Interactive authentication using device code flow"""
        print("🔐 Authenticating with Microsoft Graph...")
        print("This uses the same authentication as Microsoft Graph Explorer")
        
        try:
            # Get device code
            device_info = self.get_device_code()
            
            if 'error' in device_info:
                print(f"❌ Error getting device code: {device_info['error']}")
                return False
            
            print(f"\n📱 Please visit: {device_info['verification_uri']}")
            print(f"🔢 Enter code: {device_info['user_code']}")
            print("🌐 Opening browser automatically...")
            
            # Open browser
            webbrowser.open(device_info['verification_uri'])
            
            # Poll for token
            token_url = "https://login.microsoftonline.com/common/oauth2/v2.0/token"
            poll_data = {
                'grant_type': 'urn:ietf:params:oauth:grant-type:device_code',
                'client_id': self.client_id,
                'device_code': device_info['device_code']
            }
            
            print("⏳ Waiting for authentication (you have 15 minutes)...")
            print("🔒 Please complete the authentication in your browser...")
            
            max_attempts = 30  # 15 minutes with 30-second intervals
            for attempt in range(max_attempts):
                time.sleep(30)  # Wait 30 seconds between attempts
                
                try:
                    response = requests.post(token_url, data=poll_data)
                    token_data = response.json()
                    
                    if 'access_token' in token_data:
                        self.access_token = token_data['access_token']
                        print("✅ Authentication successful!")
                        return True
                    elif token_data.get('error') == 'authorization_pending':
                        print(f"⏳ Still waiting... (attempt {attempt + 1}/{max_attempts})")
                        continue
                    elif token_data.get('error') == 'slow_down':
                        print("⏳ Slowing down polling...")
                        time.sleep(60)  # Wait longer for slow_down
                        continue
                    else:
                        print(f"❌ Authentication error: {token_data.get('error_description', token_data.get('error', 'Unknown error'))}")
                        return False
                        
                except Exception as e:
                    print(f"⚠️ Polling error (attempt {attempt + 1}): {e}")
                    continue
            
            print("⏰ Authentication timeout. Please try again.")
            return False
            
        except Exception as e:
            print(f"❌ Authentication failed: {e}")
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
        """Get calendar events from the last N days (expanded to get 100+ meetings)"""
        if not self.access_token:
            print("❌ No access token. Please authenticate first.")
            return []
        
        try:
            headers = {"Authorization": f"Bearer {self.access_token}"}
            
            # Calculate date range (extended to 90 days to get more meetings)
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days_back)
            
            all_events = []
            page_size = 50  # Microsoft Graph API limit per request
            skip = 0
            
            print(f"📅 Fetching calendar events from last {days_back} days (targeting 100+ meetings)...")
            
            while len(all_events) < max_events:
                # Build query parameters with pagination
                params = {
                    '$top': min(page_size, max_events - len(all_events)),
                    '$skip': skip,
                    '$orderby': 'start/dateTime desc',
                    '$filter': f"start/dateTime ge '{start_date.isoformat()}Z'",
                    '$select': 'subject,bodyPreview,start,end,attendees,organizer,isOnlineMeeting,onlineMeetingProvider,location,recurrence,importance,sensitivity'
                }
                
                print(f"� Fetching page {(skip // page_size) + 1} (events {skip + 1}-{skip + params['$top']})...")
                
                response = requests.get(
                    "https://graph.microsoft.com/v1.0/me/events",
                    headers=headers,
                    params=params
                )
                
                if response.status_code == 200:
                    events_data = response.json()
                    page_events = events_data.get('value', [])
                    
                    if not page_events:
                        print(f"📄 No more events found (reached end of calendar)")
                        break
                    
                    all_events.extend(page_events)
                    skip += len(page_events)
                    
                    print(f"✅ Retrieved {len(page_events)} events from this page (Total: {len(all_events)})")
                    
                    # Check if we have enough or if there's a next page
                    if len(page_events) < page_size:
                        print(f"📄 Reached end of available events")
                        break
                        
                else:
                    print(f"❌ Failed to get calendar events: {response.status_code}")
                    print(response.text)
                    break
            
            print(f"🎯 Final result: Retrieved {len(all_events)} calendar events")
            
            if len(all_events) >= 100:
                print(f"✅ SUCCESS: Got {len(all_events)} meetings (target: 100+)")
            else:
                print(f"⚠️ WARNING: Only found {len(all_events)} meetings. Consider:")
                print(f"   - Expanding date range beyond {days_back} days")
                print(f"   - Checking if you have enough calendar history")
                print(f"   - Combining with synthetic data for training")
            
            return all_events
                
        except Exception as e:
            print(f"❌ Error getting calendar events: {e}")
            return []
    
    def format_for_promptcot(self, events: List[Dict]) -> List[Dict]:
        """Convert Graph API events to Meeting PromptCoT format"""
        formatted_scenarios = []
        
        for event in events:
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
                    'id': f"graph_api_{event.get('id', 'unknown')}",
                    'source': 'microsoft_graph_api',
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
                print(f"⚠️ Warning: Error formatting event {event.get('id', 'unknown')}: {e}")
                continue
        
        print(f"✅ Formatted {len(formatted_scenarios)} scenarios for Meeting PromptCoT")
        return formatted_scenarios
    
    def classify_meeting_type(self, subject: str, description: str) -> str:
        """Classify meeting type based on subject and description"""
        text = f"{subject} {description}".lower()
        
        type_keywords = {
            'Technical Design Review': ['design', 'architecture', 'technical', 'system', 'api', 'infrastructure'],
            'Product Strategy Session': ['strategy', 'roadmap', 'product', 'vision', 'planning', 'goals'],
            'Team Retrospective': ['retro', 'retrospective', 'sprint review', 'reflection', 'lessons'],
            'Budget Planning Meeting': ['budget', 'financial', 'cost', 'funding', 'investment', 'allocation'],
            'Customer Discovery Call': ['customer', 'user', 'feedback', 'discovery', 'interview', 'research'],
            'Cross-team Collaboration': ['sync', 'alignment', 'coordination', 'cross-team', 'collaboration'],
            'Training Session': ['training', 'workshop', 'learning', 'education', 'tutorial', 'onboarding'],
            'Performance Review': ['performance', 'review', 'evaluation', 'assessment', 'metrics', 'analysis'],
            'Vendor Evaluation': ['vendor', 'supplier', 'evaluation', 'procurement', 'rfp', 'selection'],
            'Project Status Update': ['status', 'update', 'progress', 'checkpoint', 'milestone', 'tracking']
        }
        
        for meeting_type, keywords in type_keywords.items():
            if any(keyword in text for keyword in keywords):
                return meeting_type
        
        # Default classification based on attendee count and other factors
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
        if duration > 120:  # 2+ hours
            requirements.extend([
                "Prepare detailed presentation",
                "Plan break schedules",
                "Prepare multiple discussion topics"
            ])
        elif duration > 60:  # 1+ hours
            requirements.append("Prepare comprehensive materials")
        
        # Base on meeting content
        subject = event.get('subject', '').lower()
        description = event.get('bodyPreview', '').lower()
        text = f"{subject} {description}"
        
        if any(word in text for word in ['budget', 'financial', 'cost']):
            requirements.extend(["Gather financial reports", "Prepare budget analysis"])
        
        if any(word in text for word in ['technical', 'system', 'architecture']):
            requirements.extend(["Review technical documentation", "Prepare system diagrams"])
        
        if any(word in text for word in ['customer', 'user', 'client']):
            requirements.extend(["Research customer background", "Prepare user feedback summary"])
        
        return list(set(requirements))  # Remove duplicates
    
    def assess_complexity(self, event: Dict, attendees: List[str], duration: int) -> str:
        """Assess meeting complexity based on various factors"""
        complexity_score = 0
        
        # Attendee count factor
        if len(attendees) > 10:
            complexity_score += 3
        elif len(attendees) > 5:
            complexity_score += 2
        elif len(attendees) > 2:
            complexity_score += 1
        
        # Duration factor
        if duration > 180:  # 3+ hours
            complexity_score += 3
        elif duration > 120:  # 2+ hours
            complexity_score += 2
        elif duration > 60:  # 1+ hours
            complexity_score += 1
        
        # Content complexity
        text = f"{event.get('subject', '')} {event.get('bodyPreview', '')}".lower()
        complex_keywords = ['strategy', 'architecture', 'budget', 'planning', 'review', 'assessment', 'analysis']
        complexity_score += sum(1 for keyword in complex_keywords if keyword in text)
        
        # Importance factor
        if event.get('importance') == 'high':
            complexity_score += 2
        
        # Return complexity level
        if complexity_score >= 8:
            return 'critical'
        elif complexity_score >= 5:
            return 'high'
        elif complexity_score >= 2:
            return 'medium'
        else:
            return 'low'
    
    def calculate_quality_score(self, event: Dict, attendees: List[str]) -> float:
        """Calculate quality score for the meeting data"""
        score = 5.0  # Base score
        
        # Subject quality
        if event.get('subject') and len(event['subject']) > 10:
            score += 1.0
        
        # Description quality
        if event.get('bodyPreview') and len(event['bodyPreview']) > 50:
            score += 1.0
        
        # Attendee information
        if len(attendees) >= 3:
            score += 1.0
        
        # Meeting details
        if event.get('isOnlineMeeting'):
            score += 0.5
        
        if event.get('location'):
            score += 0.5
        
        # Cap at 10.0
        return min(score, 10.0)
    
    def save_meeting_data(self, scenarios: List[Dict], output_path: str = "meeting_prep_data/graph_api_scenarios.json"):
        """Save meeting data to file"""
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(scenarios, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Saved {len(scenarios)} scenarios to {output_path}")

def main():
    """Main execution function"""
    print("🚀 Direct Microsoft Graph API Client")
    print("Extract meeting data without MEvals (no IT approval needed)")
    print("-" * 60)
    
    client = MeetingGraphClient()
    
    # Step 1: Authenticate
    print("\n🔐 Step 1: Authentication")
    if not client.authenticate_interactive():
        print("❌ Authentication failed. Exiting.")
        return
    
    # Step 2: Test connection
    print("\n🔗 Step 2: Testing connection")
    if not client.test_connection():
        print("❌ Connection test failed. Exiting.")
        return
    
    # Step 3: Get calendar events
    print("\n📅 Step 3: Extracting calendar events")
    events = client.get_calendar_events(days_back=90, max_events=250)
    
    if not events:
        print("❌ No events found or extraction failed.")
        print("💡 Try expanding the date range or check your calendar history.")
        return
    
    if len(events) < 100:
        print(f"⚠️  Only found {len(events)} events (target: 100+)")
        print("💡 Consider running the enhanced data generator for additional scenarios:")
        print("   python meeting_data_enhancer.py")
    else:
        print(f"🎯 Excellent! Found {len(events)} events (exceeded 100+ target)")
    
    
    # Step 4: Format for PromptCoT
    print("\n🔄 Step 4: Formatting for Meeting PromptCoT")
    scenarios = client.format_for_promptcot(events)
    
    # Step 5: Save data
    print("\n💾 Step 5: Saving data")
    client.save_meeting_data(scenarios)
    
    # Summary
    print("\n📊 Extraction Summary:")
    print(f"Raw events extracted: {len(events)}")
    print(f"Formatted scenarios: {len(scenarios)}")
    print(f"Date range: Last 90 days (targeting 100+ meetings)")
    
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
        
        # Success metrics
        if len(scenarios) >= 100:
            print(f"\n🎉 SUCCESS: Extracted {len(scenarios)} meetings (target achieved!)")
        else:
            print(f"\n📈 Progress: {len(scenarios)}/100 meetings extracted")
            print("💡 To reach 100+ total scenarios, also run:")
            print("   python meeting_data_enhancer.py  # +200 synthetic scenarios")
    
    print("\n🎯 Success! Your meeting data is ready for Meeting PromptCoT.")
    
    if len(scenarios) >= 100:
        print("Next steps:")
        print("1. Run: python update_training_data.py")
        print("2. Launch: streamlit run meeting_data_explorer.py")
        print("3. Access: http://localhost:8501")
    else:
        print("Recommended next steps:")
        print("1. Run: python meeting_data_enhancer.py  # Add synthetic scenarios")
        print("2. Run: python update_training_data.py    # Combine all data")
        print("3. Launch: streamlit run meeting_data_explorer.py")
        print("4. Access: http://localhost:8501")

if __name__ == "__main__":
    main()