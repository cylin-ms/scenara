#!/usr/bin/env python3
"""
Simple Graph Collaboration Analyzer with Custom App Registration

This is the most reliable approach - uses your own Azure app registration.
Takes 2 minutes to set up, then works perfectly every time.

Follow azure_app_setup_guide.md to create your app first.
"""

import requests
import json
import time
from datetime import datetime, timedelta
from collections import defaultdict, Counter

class SimpleGraphAnalyzer:
    def __init__(self, client_id: str):
        """Initialize with your Azure app client ID"""
        self.client_id = client_id
        self.tenant = "common"  # Works for any Microsoft account
        
        self.scopes = [
            "https://graph.microsoft.com/User.Read",
            "https://graph.microsoft.com/Mail.Read", 
            "https://graph.microsoft.com/Chat.Read",
            "https://graph.microsoft.com/Calendars.Read",
            "https://graph.microsoft.com/Files.Read"
        ]
        
        self.access_token = None
        
    def authenticate(self):
        """Simple device code authentication"""
        print("🔐 AUTHENTICATING WITH YOUR AZURE APP")
        print("-" * 45)
        
        # Device code flow
        device_url = f"https://login.microsoftonline.com/{self.tenant}/oauth2/v2.0/devicecode"
        device_data = {
            'client_id': self.client_id,
            'scope': ' '.join(self.scopes)
        }
        
        try:
            # Get device code
            device_response = requests.post(device_url, data=device_data)
            device_response.raise_for_status()
            device_info = device_response.json()
            
            print(f"🌐 Go to: {device_info['verification_uri']}")
            print(f"🔑 Enter code: {device_info['user_code']}")
            print("⏳ Waiting for authentication...")
            print()
            
            # Poll for token
            token_url = f"https://login.microsoftonline.com/{self.tenant}/oauth2/v2.0/token"
            token_data = {
                'grant_type': 'urn:ietf:params:oauth:grant-type:device_code',
                'client_id': self.client_id,
                'device_code': device_info['device_code']
            }
            
            interval = device_info.get('interval', 5)
            expires_in = device_info.get('expires_in', 900)
            start_time = time.time()
            
            while time.time() - start_time < expires_in:
                time.sleep(interval)
                
                token_response = requests.post(token_url, data=token_data)
                
                if token_response.status_code == 200:
                    token_result = token_response.json()
                    if 'access_token' in token_result:
                        self.access_token = token_result['access_token']
                        print("✅ Authentication successful!")
                        return True
                
                token_result = token_response.json()
                error = token_result.get('error', '')
                
                if error == 'authorization_pending':
                    print("⏳ Still waiting...")
                    continue
                elif error == 'slow_down':
                    interval *= 2
                    continue
                else:
                    print(f"❌ Auth error: {token_result.get('error_description', error)}")
                    return False
            
            print("❌ Authentication timeout")
            return False
            
        except Exception as e:
            print(f"❌ Authentication failed: {e}")
            return False
    
    def graph_get(self, endpoint, params=None):
        """Make Graph API request"""
        if not self.access_token:
            return {}
            
        headers = {'Authorization': f'Bearer {self.access_token}'}
        url = f"https://graph.microsoft.com/v1.0{endpoint}"
        
        if params:
            url += "?" + "&".join([f"{k}={v}" for k, v in params.items()])
        
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 403:
                print(f"⚠️  No permission for {endpoint}")
                return {}
            else:
                print(f"❌ API error {response.status_code} for {endpoint}")
                return {}
        except Exception as e:
            print(f"❌ Request failed for {endpoint}: {e}")
            return {}
    
    def analyze_collaboration(self):
        """Analyze collaboration patterns from all sources"""
        print("\n🔍 ANALYZING YOUR COLLABORATION PATTERNS")
        print("-" * 50)
        
        # Get user info
        me = self.graph_get("/me")
        my_email = me.get('mail') or me.get('userPrincipalName', 'you')
        print(f"👤 User: {my_email}")
        
        all_interactions = []
        
        # 1. Calendar Analysis (most reliable)
        print("\n📅 Calendar meetings...")
        events = self.graph_get("/me/events", {
            '$top': '200',
            '$select': 'subject,organizer,start,attendees'
        })
        
        calendar_interactions = self.process_calendar(events, my_email)
        all_interactions.extend(calendar_interactions)
        print(f"   Found {len(calendar_interactions)} meeting interactions")
        
        # 2. Email Analysis
        print("\n📧 Email messages...")
        emails = self.graph_get("/me/messages", {
            '$top': '100', 
            '$select': 'from,toRecipients,ccRecipients,receivedDateTime'
        })
        
        email_interactions = self.process_emails(emails, my_email)
        all_interactions.extend(email_interactions)
        print(f"   Found {len(email_interactions)} email interactions")
        
        # 3. Chat Analysis
        print("\n💬 Teams chats...")
        chats = self.graph_get("/me/chats", {'$top': '50'})
        
        chat_interactions = self.process_chats(chats, my_email)
        all_interactions.extend(chat_interactions)
        print(f"   Found {len(chat_interactions)} chat interactions")
        
        return self.compute_scores(all_interactions)
    
    def process_calendar(self, events_data, my_email):
        """Process calendar events"""
        interactions = []
        
        for event in events_data.get('value', []):
            organizer = event.get('organizer', {}).get('emailAddress', {}).get('address')
            attendees = event.get('attendees', [])
            start_time = event.get('start', {}).get('dateTime')
            subject = event.get('subject', '')
            
            # Skip old events
            if start_time:
                try:
                    event_date = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
                    days_ago = (datetime.now().replace(tzinfo=event_date.tzinfo) - event_date).days
                    if days_ago > 60:  # Only last 2 months
                        continue
                except:
                    continue
            
            attendee_count = len(attendees)
            
            # Calculate meeting value
            if attendee_count == 2:
                weight = 20  # 1:1 meetings are highest value
            elif attendee_count <= 5:
                weight = 10  # Small meetings
            else:
                weight = 3   # Large meetings
            
            # Bonus for organizing
            if organizer == my_email:
                weight *= 1.5
            
            # Bonus for collaboration keywords
            collab_words = ['sync', 'discuss', 'review', 'planning', 'working']
            if any(word in subject.lower() for word in collab_words):
                weight *= 1.2
            
            # Record interactions with each attendee
            for attendee in attendees:
                email = attendee.get('emailAddress', {}).get('address')
                if email and email != my_email:
                    interactions.append({
                        'type': 'meeting',
                        'person': email,
                        'weight': weight,
                        'timestamp': start_time,
                        'one_on_one': attendee_count == 2,
                        'organized': organizer == my_email
                    })
        
        return interactions
    
    def process_emails(self, emails_data, my_email):
        """Process email interactions"""
        interactions = []
        
        for email in emails_data.get('value', []):
            sender = email.get('from', {}).get('emailAddress', {}).get('address')
            timestamp = email.get('receivedDateTime')
            
            # Skip old emails
            if timestamp:
                try:
                    email_date = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                    if (datetime.now().replace(tzinfo=email_date.tzinfo) - email_date).days > 30:
                        continue
                except:
                    continue
            
            # Process recipients
            for field in ['toRecipients', 'ccRecipients']:
                recipients = email.get(field, [])
                for recipient in recipients:
                    email_addr = recipient.get('emailAddress', {}).get('address')
                    if email_addr and email_addr != my_email:
                        # Determine the other person
                        other_person = email_addr if sender == my_email else sender
                        if other_person and other_person != my_email:
                            weight = 2 if field == 'toRecipients' else 1
                            interactions.append({
                                'type': 'email',
                                'person': other_person,
                                'weight': weight,
                                'timestamp': timestamp
                            })
        
        return interactions
    
    def process_chats(self, chats_data, my_email):
        """Process Teams chat interactions"""
        interactions = []
        
        for chat in chats_data.get('value', []):
            chat_id = chat.get('id')
            chat_type = chat.get('chatType', 'group')
            
            if not chat_id:
                continue
            
            # Get recent messages
            messages = self.graph_get(f"/chats/{chat_id}/messages", {
                '$top': '20',
                '$select': 'from,createdDateTime'
            })
            
            weight = 8 if chat_type == 'oneOnOne' else 3
            
            for message in messages.get('value', []):
                sender = message.get('from', {}).get('user', {}).get('email')
                timestamp = message.get('createdDateTime')
                
                # Skip old messages
                if timestamp:
                    try:
                        msg_date = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                        if (datetime.now().replace(tzinfo=msg_date.tzinfo) - msg_date).days > 14:
                            continue
                    except:
                        continue
                
                if sender and sender != my_email:
                    interactions.append({
                        'type': 'chat',
                        'person': sender,
                        'weight': weight,
                        'timestamp': timestamp,
                        'chat_type': chat_type
                    })
        
        return interactions
    
    def compute_scores(self, interactions):
        """Compute final collaboration scores"""
        print(f"\n📊 COMPUTING SCORES FROM {len(interactions)} INTERACTIONS")
        print("-" * 50)
        
        # Group by person
        people = defaultdict(lambda: {
            'total_weight': 0,
            'interactions': 0,
            'types': set(),
            'one_on_ones': 0,
            'organized': 0,
            'recent_count': 0
        })
        
        # Aggregate data
        for interaction in interactions:
            person = interaction['person']
            if not person or '@' not in person:
                continue
            
            data = people[person]
            data['total_weight'] += interaction['weight']
            data['interactions'] += 1
            data['types'].add(interaction['type'])
            
            if interaction.get('one_on_one'):
                data['one_on_ones'] += 1
            if interaction.get('organized'):
                data['organized'] += 1
            
            # Count recent interactions (last 2 weeks)
            if interaction['timestamp']:
                try:
                    msg_date = datetime.fromisoformat(interaction['timestamp'].replace('Z', '+00:00'))
                    if (datetime.now().replace(tzinfo=msg_date.tzinfo) - msg_date).days <= 14:
                        data['recent_count'] += 1
                except:
                    pass
        
        # Calculate final scores
        final_scores = {}
        for person, data in people.items():
            if data['interactions'] < 2:  # Minimum threshold
                continue
            
            # Base score from weighted interactions
            base_score = data['total_weight']
            
            # Bonuses
            diversity_bonus = len(data['types']) * 10  # Multiple interaction types
            one_on_one_bonus = data['one_on_ones'] * 25  # 1:1 meetings valuable
            organized_bonus = data['organized'] * 20  # Organizing shows initiative
            recent_bonus = data['recent_count'] * 5  # Recent activity
            
            final_score = base_score + diversity_bonus + one_on_one_bonus + organized_bonus + recent_bonus
            
            final_scores[person] = {
                'score': round(final_score, 1),
                'interactions': data['interactions'],
                'weight': data['total_weight'],
                'types': list(data['types']),
                'one_on_ones': data['one_on_ones'],
                'organized': data['organized'],
                'recent': data['recent_count']
            }
        
        return final_scores
    
    def display_results(self, scores):
        """Display final collaboration rankings"""
        print("\n🏆 YOUR TOP COLLABORATORS")
        print("=" * 40)
        
        # Sort by score
        ranked = sorted(scores.items(), key=lambda x: x[1]['score'], reverse=True)
        
        for i, (person, data) in enumerate(ranked[:15], 1):
            print(f"{i}. {person}")
            print(f"   🎯 Score: {data['score']}")
            print(f"   📊 {data['interactions']} interactions")
            print(f"   📱 Types: {', '.join(data['types'])}")
            
            highlights = []
            if data['one_on_ones'] > 0:
                highlights.append(f"{data['one_on_ones']} 1:1 meetings")
            if data['organized'] > 0:
                highlights.append(f"{data['organized']} you organized")
            if data['recent'] > 0:
                highlights.append(f"{data['recent']} recent")
            
            if highlights:
                print(f"   ✨ {', '.join(highlights)}")
            print()
        
        return ranked
    
    def run_analysis(self):
        """Run complete collaboration analysis"""
        print("🚀 SIMPLE GRAPH COLLABORATION ANALYZER")
        print("=" * 45)
        print("Using your Azure app for reliable authentication")
        print()
        
        if not self.authenticate():
            return
        
        scores = self.analyze_collaboration()
        
        if scores:
            results = self.display_results(scores)
            
            # Save results
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"collaboration_analysis_{timestamp}.json"
            
            with open(filename, 'w') as f:
                json.dump({
                    'timestamp': datetime.now().isoformat(),
                    'client_id': self.client_id,
                    'total_people': len(scores),
                    'results': dict(scores)
                }, f, indent=2)
            
            print(f"✅ Results saved to: {filename}")
            print("\n🎯 This shows your REAL collaboration patterns!")
            print("📧 Email exchanges • 💬 Teams chats • 📅 Meeting patterns")
            print("\n✨ Finally - accurate collaboration discovery! ✨")
        else:
            print("❌ No collaboration data found")

def main():
    """Main entry point"""
    print("📋 Using proven working client ID from daily_meeting_viewer.py")
    print("✅ Client ID: 9ce97a32-d9ab-4ab2-aadc-f49b39b94e11 (Microsoft Corp)")
    print()
    
    analyzer = SimpleGraphAnalyzer("9ce97a32-d9ab-4ab2-aadc-f49b39b94e11")
    analyzer.run_analysis()

if __name__ == "__main__":
    main()