#!/usr/bin/env python3
"""
Simple Browser-Based Graph Collaboration Analyzer

Uses web browser authentication - no Azure app registration required!
Just opens browser, user signs in, and we get the data directly.

Much simpler than the app registration approach.
"""

import webbrowser
import urllib.parse
import json
import requests
from datetime import datetime, timedelta
from collections import defaultdict, Counter
import base64
import hashlib
import secrets
import http.server
import socketserver
import threading
import time

class BrowserGraphAnalyzer:
    def __init__(self):
        """Initialize with browser-based authentication"""
        # Microsoft Graph Explorer public client ID (widely available)
        self.client_id = "de8bc8b5-d9f9-48b1-a8ad-b748da725064"  # Graph Explorer
        # Alternative options:
        # "1950a258-227b-4e31-a9cf-717495945fc2"  # Another Graph Explorer ID
        # "1fec8e78-bce4-4aaf-ab1b-5451cc387264"  # Teams client
        
        self.tenant = "common"  # Works for any Microsoft tenant
        self.redirect_uri = "http://localhost:8080/callback"
        self.scopes = [
            "https://graph.microsoft.com/User.Read",
            "https://graph.microsoft.com/Mail.Read", 
            "https://graph.microsoft.com/Chat.Read",
            "https://graph.microsoft.com/Calendars.Read",
            "https://graph.microsoft.com/Files.Read"
        ]
        
        self.access_token = None
        self.auth_server = None
        
    def generate_pkce_challenge(self):
        """Generate PKCE code verifier and challenge"""
        code_verifier = base64.urlsafe_b64encode(secrets.token_bytes(32)).decode('utf-8').rstrip('=')
        code_challenge = base64.urlsafe_b64encode(
            hashlib.sha256(code_verifier.encode('utf-8')).digest()
        ).decode('utf-8').rstrip('=')
        return code_verifier, code_challenge
    
    def start_auth_server(self):
        """Start local server to receive OAuth callback"""
        class AuthHandler(http.server.BaseHTTPRequestHandler):
            def __init__(self, analyzer, *args, **kwargs):
                self.analyzer = analyzer
                super().__init__(*args, **kwargs)
                
            def do_GET(self):
                if self.path.startswith('/callback'):
                    # Parse authorization code from callback
                    query = urllib.parse.urlparse(self.path).query
                    params = urllib.parse.parse_qs(query)
                    
                    if 'code' in params:
                        self.analyzer.auth_code = params['code'][0]
                        self.send_response(200)
                        self.send_header('Content-type', 'text/html')
                        self.end_headers()
                        response_html = """
                        <html><body>
                        <h2>✅ Authentication Successful!</h2>
                        <p>You can close this window and return to the terminal.</p>
                        <script>setTimeout(() => window.close(), 3000);</script>
                        </body></html>
                        """
                        self.wfile.write(response_html.encode('utf-8'))
                    else:
                        self.send_error(400, "No authorization code received")
                        
            def log_message(self, format, *args):
                pass  # Suppress server logs
        
        # Create handler with reference to analyzer
        handler = lambda *args, **kwargs: AuthHandler(self, *args, **kwargs)
        
        self.auth_server = socketserver.TCPServer(("localhost", 8080), handler)
        self.auth_code = None
        
        # Start server in background thread
        server_thread = threading.Thread(target=self.auth_server.serve_forever)
        server_thread.daemon = True
        server_thread.start()
        
        return server_thread
    
    def authenticate_browser(self):
        """Authenticate using browser-based OAuth flow"""
        print("🌐 BROWSER-BASED AUTHENTICATION")
        print("-" * 40)
        print("Opening web browser for Microsoft sign-in...")
        
        # Generate PKCE challenge
        code_verifier, code_challenge = self.generate_pkce_challenge()
        
        # Start local callback server
        server_thread = self.start_auth_server()
        
        # Build authorization URL
        auth_params = {
            'client_id': self.client_id,
            'response_type': 'code',
            'redirect_uri': self.redirect_uri,
            'scope': ' '.join(self.scopes),
            'response_mode': 'query',
            'code_challenge': code_challenge,
            'code_challenge_method': 'S256'
        }
        
        auth_url = f"https://login.microsoftonline.com/{self.tenant}/oauth2/v2.0/authorize"
        auth_url += "?" + urllib.parse.urlencode(auth_params)
        
        # Open browser
        webbrowser.open(auth_url)
        print("🔑 Please sign in with your Microsoft account in the browser...")
        
        # Wait for callback
        timeout = 120  # 2 minutes
        start_time = time.time()
        
        while not self.auth_code and (time.time() - start_time) < timeout:
            time.sleep(1)
        
        # Stop server
        self.auth_server.shutdown()
        self.auth_server.server_close()
        
        if not self.auth_code:
            print("❌ Authentication timeout or cancelled")
            return False
        
        # Exchange code for token
        token_data = {
            'client_id': self.client_id,
            'grant_type': 'authorization_code',
            'code': self.auth_code,
            'redirect_uri': self.redirect_uri,
            'code_verifier': code_verifier
        }
        
        token_url = f"https://login.microsoftonline.com/{self.tenant}/oauth2/v2.0/token"
        
        try:
            response = requests.post(token_url, data=token_data)
            response.raise_for_status()
            
            token_response = response.json()
            self.access_token = token_response.get('access_token')
            
            if self.access_token:
                print("✅ Authentication successful!")
                return True
            else:
                print("❌ Failed to get access token")
                return False
                
        except Exception as e:
            print(f"❌ Token exchange failed: {e}")
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
            url += "?" + urllib.parse.urlencode(params)
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"❌ Graph API error for {endpoint}: {e}")
            return {}
    
    def analyze_collaboration_patterns(self):
        """Analyze collaboration using real Graph data"""
        print("\n🔍 ANALYZING COLLABORATION PATTERNS")
        print("-" * 40)
        
        # Get user profile
        me = self.graph_request("/me")
        my_email = me.get('mail') or me.get('userPrincipalName', 'unknown')
        print(f"👤 Analyzing for: {my_email}")
        
        all_interactions = []
        
        # 1. Email Analysis
        print("📧 Analyzing emails...")
        emails = self.graph_request("/me/messages", {
            '$top': 100,
            '$select': 'id,subject,from,toRecipients,ccRecipients,receivedDateTime,sentDateTime'
        })
        
        email_count = 0
        for email in emails.get('value', []):
            sender = email.get('from', {}).get('emailAddress', {}).get('address')
            timestamp = email.get('receivedDateTime') or email.get('sentDateTime')
            
            # Process recipients
            for field in ['toRecipients', 'ccRecipients']:
                recipients = email.get(field, [])
                for recipient in recipients:
                    addr = recipient.get('emailAddress', {}).get('address')
                    if addr and addr != my_email and sender != addr:
                        all_interactions.append({
                            'type': 'email',
                            'person': addr if sender == my_email else sender,
                            'timestamp': timestamp,
                            'weight': 2 if field == 'toRecipients' else 1
                        })
                        email_count += 1
        
        print(f"   Found {email_count} email interactions")
        
        # 2. Chat Analysis
        print("💬 Analyzing Teams chats...")
        chats = self.graph_request("/me/chats", {'$top': 50})
        
        chat_count = 0
        for chat in chats.get('value', []):
            chat_id = chat.get('id')
            chat_type = chat.get('chatType', 'unknown')
            
            if chat_id:
                messages = self.graph_request(f"/chats/{chat_id}/messages", {
                    '$top': 50,
                    '$select': 'id,from,createdDateTime,mentions'
                })
                
                for message in messages.get('value', []):
                    sender = message.get('from', {}).get('user', {}).get('email')
                    timestamp = message.get('createdDateTime')
                    
                    # Weight based on chat type
                    base_weight = 5 if chat_type == 'oneOnOne' else 2
                    
                    if sender and sender != my_email:
                        all_interactions.append({
                            'type': 'chat',
                            'person': sender,
                            'timestamp': timestamp,
                            'weight': base_weight,
                            'chat_type': chat_type
                        })
                        chat_count += 1
                    
                    # Process mentions (high value)
                    mentions = message.get('mentions', [])
                    for mention in mentions:
                        mentioned = mention.get('mentioned', {}).get('user', {}).get('email')
                        if mentioned and mentioned != sender:
                            all_interactions.append({
                                'type': 'chat_mention',
                                'person': mentioned if sender == my_email else sender,
                                'timestamp': timestamp,
                                'weight': base_weight * 2
                            })
                            chat_count += 1
        
        print(f"   Found {chat_count} chat interactions")
        
        # 3. Calendar Analysis
        print("📅 Analyzing calendar events...")
        events = self.graph_request("/me/events", {
            '$top': 100,
            '$select': 'id,subject,organizer,start,attendees,responseStatus'
        })
        
        meeting_count = 0
        for event in events.get('value', []):
            organizer = event.get('organizer', {}).get('emailAddress', {}).get('address')
            attendees = event.get('attendees', [])
            start_time = event.get('start', {}).get('dateTime')
            subject = event.get('subject', '')
            
            attendee_count = len(attendees)
            is_small = attendee_count <= 5
            is_one_on_one = attendee_count == 2
            
            # Base weight by meeting size
            base_weight = 15 if is_one_on_one else (8 if is_small else 3)
            
            # Bonus for organizing
            if organizer == my_email:
                base_weight *= 1.5
            
            # Bonus for collaboration keywords
            collab_keywords = ['sync', 'discuss', 'review', 'planning', 'working']
            if any(keyword in subject.lower() for keyword in collab_keywords):
                base_weight *= 1.3
            
            for attendee in attendees:
                addr = attendee.get('emailAddress', {}).get('address')
                if addr and addr != my_email:
                    all_interactions.append({
                        'type': 'meeting',
                        'person': addr,
                        'timestamp': start_time,
                        'weight': base_weight,
                        'organized_by_me': organizer == my_email,
                        'is_one_on_one': is_one_on_one,
                        'attendee_count': attendee_count
                    })
                    meeting_count += 1
        
        print(f"   Found {meeting_count} meeting interactions")
        
        # 4. Compute collaboration scores
        return self.compute_scores(all_interactions)
    
    def compute_scores(self, interactions):
        """Compute final collaboration scores"""
        print("\n📊 COMPUTING COLLABORATION SCORES")
        print("-" * 40)
        
        # Group by person
        person_data = defaultdict(lambda: {
            'interactions': [],
            'total_weight': 0,
            'types': Counter(),
            'timestamps': []
        })
        
        for interaction in interactions:
            person = interaction['person']
            if not person:
                continue
                
            person_data[person]['interactions'].append(interaction)
            person_data[person]['total_weight'] += interaction['weight']
            person_data[person]['types'][interaction['type']] += 1
            
            if interaction['timestamp']:
                person_data[person]['timestamps'].append(interaction['timestamp'])
        
        # Calculate final scores
        scores = {}
        for person, data in person_data.items():
            if len(data['interactions']) < 3:  # Minimum threshold
                continue
            
            # Base score from weights
            base_score = data['total_weight']
            
            # Diversity bonus (multiple interaction types)
            diversity_bonus = len(data['types']) * 20
            
            # Frequency analysis
            timestamps = data['timestamps']
            if timestamps:
                try:
                    dates = [datetime.fromisoformat(ts.replace('Z', '+00:00')) for ts in timestamps]
                    dates.sort()
                    if len(dates) > 1:
                        duration = (dates[-1] - dates[0]).days
                        frequency = len(dates) / max(1, duration / 7)  # per week
                        frequency_bonus = min(50, frequency * 5)
                    else:
                        frequency_bonus = 0
                except:
                    frequency_bonus = 0
            else:
                frequency_bonus = 0
            
            # Special interaction bonuses
            one_on_ones = len([i for i in data['interactions'] if i.get('is_one_on_one')])
            organized = len([i for i in data['interactions'] if i.get('organized_by_me')])
            
            special_bonus = (one_on_ones * 25) + (organized * 20)
            
            final_score = base_score + diversity_bonus + frequency_bonus + special_bonus
            
            scores[person] = {
                'score': round(final_score, 1),
                'interactions': len(data['interactions']),
                'total_weight': data['total_weight'],
                'types': dict(data['types']),
                'diversity': len(data['types']),
                'one_on_ones': one_on_ones,
                'organized': organized,
                'frequency_per_week': round(frequency if 'frequency' in locals() else 0, 2)
            }
        
        return scores
    
    def display_results(self, scores):
        """Display collaboration analysis results"""
        print("\n🏆 COLLABORATION RANKINGS (Real Graph Data)")
        print("=" * 60)
        
        sorted_people = sorted(scores.items(), key=lambda x: x[1]['score'], reverse=True)
        
        for i, (person, data) in enumerate(sorted_people[:10], 1):
            print(f"{i}. {person}")
            print(f"   🎯 Score: {data['score']}")
            print(f"   📊 Interactions: {data['interactions']} ({data['total_weight']} weighted)")
            print(f"   📱 Types: {', '.join(data['types'].keys())}")
            
            if data['one_on_ones'] > 0:
                print(f"   🤝 1:1 meetings: {data['one_on_ones']}")
            if data['organized'] > 0:
                print(f"   👤 Organized by you: {data['organized']}")
            if data['frequency_per_week'] > 0:
                print(f"   🔄 Frequency: {data['frequency_per_week']}/week")
            print()
        
        return sorted_people
    
    def run_analysis(self):
        """Run complete browser-based collaboration analysis"""
        print("🚀 BROWSER-BASED GRAPH COLLABORATION ANALYZER")
        print("=" * 55)
        print("No Azure app registration needed - just sign in!")
        print()
        
        # Authenticate
        if not self.authenticate_browser():
            return
        
        # Analyze
        scores = self.analyze_collaboration_patterns()
        
        if scores:
            results = self.display_results(scores)
            
            # Save results
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"browser_collaboration_analysis_{timestamp}.json"
            
            with open(filename, 'w') as f:
                json.dump({
                    'timestamp': datetime.now().isoformat(),
                    'method': 'browser_authentication',
                    'results': dict(scores)
                }, f, indent=2)
            
            print(f"✅ Results saved to: {filename}")
            print("\n💡 This uses REAL Microsoft Graph data:")
            print("   • Your actual emails and recipients")
            print("   • Real Teams chat messages and mentions")  
            print("   • Calendar meetings you organize/attend")
            print("   • Temporal patterns and interaction frequency")
            print("\n🎯 Much more accurate than static calendar analysis!")
        else:
            print("❌ No collaboration data found")

def main():
    """Run browser-based collaboration analysis"""
    analyzer = BrowserGraphAnalyzer()
    analyzer.run_analysis()

if __name__ == "__main__":
    main()