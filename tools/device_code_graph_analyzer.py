#!/usr/bin/env python3
"""
Simple Device Code Graph Collaboration Analyzer

Uses Microsoft's device code flow - no app registration needed!
Just run the script, go to the URL, enter the code, and sign in.

This is the most reliable and hassle-free approach.
"""

import requests
import json
import time
from datetime import datetime, timedelta
from collections import defaultdict, Counter

class DeviceCodeGraphAnalyzer:
    def __init__(self):
        """Initialize with device code flow"""
        # Using Microsoft Graph PowerShell public app
        self.client_id = "14d82eec-204b-4c2f-b7e0-296a0da3eb91"
        self.tenant = "organizations"  # Works better than "common"
        
        self.scopes = [
            "https://graph.microsoft.com/User.Read",
            "https://graph.microsoft.com/Mail.Read", 
            "https://graph.microsoft.com/Chat.Read",
            "https://graph.microsoft.com/Calendars.Read",
            "https://graph.microsoft.com/Files.Read"
        ]
        
        self.access_token = None
        
    def authenticate_device_code(self):
        """Authenticate using device code flow"""
        print("🔐 DEVICE CODE AUTHENTICATION")
        print("-" * 40)
        
        # Start device flow
        device_flow_url = f"https://login.microsoftonline.com/{self.tenant}/oauth2/v2.0/devicecode"
        
        device_data = {
            'client_id': self.client_id,
            'scope': ' '.join(self.scopes)
        }
        
        try:
            device_response = requests.post(device_flow_url, data=device_data)
            device_response.raise_for_status()
            device_info = device_response.json()
            
            print(f"🌐 Go to: {device_info['verification_uri']}")
            print(f"🔑 Enter code: {device_info['user_code']}")
            print("⏳ Waiting for you to complete authentication...")
            print()
            
            # Poll for token
            token_url = f"https://login.microsoftonline.com/{self.tenant}/oauth2/v2.0/token"
            token_data = {
                'grant_type': 'urn:ietf:params:oauth:grant-type:device_code',
                'client_id': self.client_id,
                'device_code': device_info['device_code']
            }
            
            # Poll every 5 seconds
            interval = device_info.get('interval', 5)
            expires_in = device_info.get('expires_in', 900)  # 15 minutes
            start_time = time.time()
            
            while time.time() - start_time < expires_in:
                time.sleep(interval)
                
                token_response = requests.post(token_url, data=token_data)
                token_result = token_response.json()
                
                if 'access_token' in token_result:
                    self.access_token = token_result['access_token']
                    print("✅ Authentication successful!")
                    return True
                elif token_result.get('error') == 'authorization_pending':
                    print("⏳ Still waiting for authentication...")
                    continue
                elif token_result.get('error') == 'slow_down':
                    interval = interval * 2
                    continue
                else:
                    print(f"❌ Authentication error: {token_result.get('error_description', 'Unknown error')}")
                    return False
            
            print("❌ Authentication timeout")
            return False
            
        except Exception as e:
            print(f"❌ Authentication failed: {e}")
            return False
    
    def graph_request(self, endpoint, params=None):
        """Make authenticated request to Microsoft Graph"""
        if not self.access_token:
            return {}
            
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
        
        url = f"https://graph.microsoft.com/v1.0{endpoint}"
        if params:
            url += "?" + "&".join([f"{k}={v}" for k, v in params.items()])
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            if response.status_code == 403:
                print(f"⚠️  Permission needed for {endpoint}")
                return {}
            else:
                print(f"❌ Graph API error for {endpoint}: {e}")
                return {}
        except Exception as e:
            print(f"❌ Request error for {endpoint}: {e}")
            return {}
    
    def analyze_all_collaborations(self):
        """Analyze all collaboration sources"""
        print("\n🔍 ANALYZING COLLABORATION PATTERNS")
        print("-" * 40)
        
        # Get user info
        me = self.graph_request("/me")
        my_email = me.get('mail') or me.get('userPrincipalName', 'unknown')
        print(f"👤 Analyzing for: {my_email}")
        
        all_interactions = []
        
        # 1. Calendar Analysis (most reliable)
        print("\n📅 Analyzing calendar events...")
        events = self.graph_request("/me/events", {
            '$top': '200',
            '$select': 'id,subject,organizer,start,attendees,responseStatus'
        })
        
        meeting_interactions = self.process_meetings(events, my_email)
        all_interactions.extend(meeting_interactions)
        print(f"   ✅ Found {len(meeting_interactions)} meeting interactions")
        
        # 2. Email Analysis  
        print("\n📧 Analyzing emails...")
        try:
            emails = self.graph_request("/me/messages", {
                '$top': '200',
                '$select': 'id,subject,from,toRecipients,ccRecipients,receivedDateTime,sentDateTime'
            })
            
            email_interactions = self.process_emails(emails, my_email)
            all_interactions.extend(email_interactions)
            print(f"   ✅ Found {len(email_interactions)} email interactions")
        except Exception as e:
            print(f"   ⚠️  Email analysis skipped: Limited permissions")
        
        # 3. Chat Analysis
        print("\n💬 Analyzing Teams chats...")
        try:
            chats = self.graph_request("/me/chats", {'$top': '100'})
            
            chat_interactions = self.process_chats(chats, my_email)
            all_interactions.extend(chat_interactions)
            print(f"   ✅ Found {len(chat_interactions)} chat interactions")
        except Exception as e:
            print(f"   ⚠️  Chat analysis skipped: Limited permissions")
        
        return all_interactions
    
    def process_meetings(self, events_data, my_email):
        """Process calendar meetings for collaboration signals"""
        interactions = []
        
        for event in events_data.get('value', []):
            organizer = event.get('organizer', {}).get('emailAddress', {}).get('address')
            attendees = event.get('attendees', [])
            start_time = event.get('start', {}).get('dateTime')
            subject = event.get('subject', '')
            
            # Skip old events (last 90 days)
            if start_time:
                try:
                    event_date = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
                    if (datetime.now().replace(tzinfo=event_date.tzinfo) - event_date).days > 90:
                        continue
                except:
                    continue
            
            attendee_count = len(attendees)
            is_small = attendee_count <= 5
            is_one_on_one = attendee_count == 2
            organized_by_me = organizer == my_email
            
            # Calculate base weight
            base_weight = 15 if is_one_on_one else (8 if is_small else 3)
            if organized_by_me:
                base_weight *= 1.5
            
            # Check for collaboration keywords
            collab_keywords = ['sync', 'discuss', 'review', 'planning', 'working', 'brainstorm', 'design']
            if any(keyword in subject.lower() for keyword in collab_keywords):
                base_weight *= 1.3
            
            # Create interactions for each attendee
            for attendee in attendees:
                addr = attendee.get('emailAddress', {}).get('address')
                if addr and addr != my_email:
                    interactions.append({
                        'type': 'meeting',
                        'person': addr,
                        'timestamp': start_time,
                        'weight': base_weight,
                        'organized_by_me': organized_by_me,
                        'is_one_on_one': is_one_on_one,
                        'attendee_count': attendee_count,
                        'subject': subject
                    })
        
        return interactions
    
    def process_emails(self, emails_data, my_email):
        """Process emails for collaboration signals"""
        interactions = []
        
        for email in emails_data.get('value', []):
            sender = email.get('from', {}).get('emailAddress', {}).get('address')
            timestamp = email.get('receivedDateTime') or email.get('sentDateTime')
            
            # Skip old emails (last 30 days)
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
                    addr = recipient.get('emailAddress', {}).get('address')
                    if addr and addr != my_email:
                        other_person = addr if sender == my_email else sender
                        if other_person and other_person != my_email:
                            interactions.append({
                                'type': 'email',
                                'person': other_person,
                                'timestamp': timestamp,
                                'weight': 2 if field == 'toRecipients' else 1
                            })
        
        return interactions
    
    def process_chats(self, chats_data, my_email):
        """Process Teams chats for collaboration signals"""
        interactions = []
        
        for chat in chats_data.get('value', []):
            chat_id = chat.get('id')
            chat_type = chat.get('chatType', 'unknown')
            
            if not chat_id:
                continue
            
            # Get recent messages
            messages = self.graph_request(f"/chats/{chat_id}/messages", {
                '$top': '50',
                '$select': 'id,from,createdDateTime'
            })
            
            base_weight = 8 if chat_type == 'oneOnOne' else 3
            
            for message in messages.get('value', []):
                sender = message.get('from', {}).get('user', {}).get('email')
                timestamp = message.get('createdDateTime')
                
                # Skip old messages (last 30 days)
                if timestamp:
                    try:
                        msg_date = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                        if (datetime.now().replace(tzinfo=msg_date.tzinfo) - msg_date).days > 30:
                            continue
                    except:
                        continue
                
                if sender and sender != my_email:
                    interactions.append({
                        'type': 'chat',
                        'person': sender,
                        'timestamp': timestamp,
                        'weight': base_weight,
                        'chat_type': chat_type
                    })
        
        return interactions
    
    def compute_collaboration_scores(self, interactions):
        """Compute final collaboration scores"""
        print(f"\n📊 COMPUTING COLLABORATION SCORES")
        print(f"Total interactions found: {len(interactions)}")
        print("-" * 40)
        
        # Group by person
        person_data = defaultdict(lambda: {
            'interactions': [],
            'total_weight': 0,
            'types': Counter(),
            'one_on_ones': 0,
            'organized': 0,
            'timestamps': []
        })
        
        for interaction in interactions:
            person = interaction['person']
            if not person or '@' not in person:  # Basic email validation
                continue
            
            data = person_data[person]
            data['interactions'].append(interaction)
            data['total_weight'] += interaction['weight']
            data['types'][interaction['type']] += 1
            
            if interaction.get('is_one_on_one'):
                data['one_on_ones'] += 1
            if interaction.get('organized_by_me'):
                data['organized'] += 1
            if interaction['timestamp']:
                data['timestamps'].append(interaction['timestamp'])
        
        # Calculate final scores
        scores = {}
        for person, data in person_data.items():
            if len(data['interactions']) < 2:  # Minimum threshold
                continue
            
            # Base score
            base_score = data['total_weight']
            
            # Diversity bonus (multiple interaction types)
            diversity_bonus = len(data['types']) * 15
            
            # Frequency analysis
            frequency_bonus = 0
            if data['timestamps']:
                try:
                    dates = [datetime.fromisoformat(ts.replace('Z', '+00:00')) for ts in data['timestamps']]
                    dates.sort()
                    if len(dates) > 1:
                        duration = (dates[-1] - dates[0]).days
                        if duration > 0:
                            frequency = len(dates) / (duration / 7)  # per week
                            frequency_bonus = min(40, frequency * 3)
                except:
                    pass
            
            # Special bonuses
            one_on_one_bonus = data['one_on_ones'] * 30
            organized_bonus = data['organized'] * 25
            
            final_score = base_score + diversity_bonus + frequency_bonus + one_on_one_bonus + organized_bonus
            
            scores[person] = {
                'score': round(final_score, 1),
                'interactions': len(data['interactions']),
                'total_weight': data['total_weight'],
                'types': dict(data['types']),
                'one_on_ones': data['one_on_ones'],
                'organized': data['organized'],
                'diversity': len(data['types'])
            }
        
        return scores
    
    def display_results(self, scores):
        """Display collaboration results"""
        print("\n🏆 COLLABORATION RANKINGS")
        print("=" * 50)
        
        sorted_people = sorted(scores.items(), key=lambda x: x[1]['score'], reverse=True)
        
        for i, (person, data) in enumerate(sorted_people[:15], 1):
            print(f"{i}. {person}")
            print(f"   🎯 Score: {data['score']}")
            print(f"   📊 {data['interactions']} interactions (weight: {data['total_weight']})")
            print(f"   📱 Types: {', '.join(data['types'].keys())}")
            
            if data['one_on_ones'] > 0:
                print(f"   🤝 1:1 meetings: {data['one_on_ones']}")
            if data['organized'] > 0:
                print(f"   👤 You organized: {data['organized']}")
            print()
        
        return sorted_people
    
    def run_analysis(self):
        """Run complete device code collaboration analysis"""
        print("🚀 DEVICE CODE GRAPH COLLABORATION ANALYZER")
        print("=" * 55)
        print("Simple device code authentication - no app registration!")
        print()
        
        # Authenticate
        if not self.authenticate_device_code():
            return
        
        # Analyze
        interactions = self.analyze_all_collaborations()
        
        if interactions:
            scores = self.compute_collaboration_scores(interactions)
            
            if scores:
                results = self.display_results(scores)
                
                # Save results
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"device_code_collaboration_analysis_{timestamp}.json"
                
                with open(filename, 'w') as f:
                    json.dump({
                        'timestamp': datetime.now().isoformat(),
                        'method': 'device_code_authentication',
                        'total_interactions': len(interactions),
                        'results': dict(scores)
                    }, f, indent=2)
                
                print(f"✅ Results saved to: {filename}")
                print("\n💡 This analysis used real Microsoft Graph data!")
                print("🎯 Now you'll see who your true top collaborators are!")
            else:
                print("❌ No collaboration patterns found")
        else:
            print("❌ No interaction data available")

def main():
    """Run device code collaboration analysis"""
    analyzer = DeviceCodeGraphAnalyzer()
    analyzer.run_analysis()

if __name__ == "__main__":
    main()