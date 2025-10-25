#!/usr/bin/env python3
"""
Working Graph Collaborator Analyzer
Uses the proven working authentication from daily_meeting_viewer.py
"""

import json
import sys
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any
from collections import defaultdict, Counter

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    import msal
    import requests
except ImportError:
    print("❌ Missing dependencies. Install with:")
    print("   pip install msal requests")
    sys.exit(1)

class WorkingGraphCollaborator:
    """Collaboration analyzer using proven working Graph authentication"""
    
    def __init__(self):
        # Use the exact same configuration that works in daily_meeting_viewer.py
        self.tenant_id = "72f988bf-86f1-41af-91ab-2d7cd011db47"
        self.client_id = "9ce97a32-d9ab-4ab2-aadc-f49b39b94e11"
        
        # Expanded scopes for collaboration analysis
        self.scopes = [
            "Calendars.Read",
            "Mail.Read", 
            "Files.Read",
            "Contacts.Read",
            "User.Read",
            "People.Read"
        ]
        
        self.access_token = None
        
    def authenticate(self) -> str:
        """
        Authenticate with Microsoft Graph using the working method
        """
        print("🔐 Authenticating with Microsoft Graph...")
        
        authority = f"https://login.microsoftonline.com/{self.tenant_id}"
        app = msal.PublicClientApplication(self.client_id, authority=authority)
        
        # Try silent authentication first
        accounts = app.get_accounts()
        result = None
        
        if accounts:
            print("🔑 Attempting silent authentication...")
            result = app.acquire_token_silent(self.scopes, account=accounts[0])
        
        if not result or "access_token" not in result:
            print("🔐 Interactive authentication required...")
            print("   A browser window will open for Microsoft login")
            result = app.acquire_token_interactive(self.scopes)
        
        if "access_token" not in result:
            raise Exception(f"Authentication failed: {result.get('error_description', 'Unknown error')}")
        
        print("✅ Authentication successful!")
        self.access_token = result["access_token"]
        return result["access_token"]
    
    def make_graph_request(self, endpoint: str) -> Dict[str, Any]:
        """Make authenticated request to Microsoft Graph"""
        if not self.access_token:
            self.authenticate()
            
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
        
        url = f"https://graph.microsoft.com/v1.0{endpoint}"
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"❌ Graph API error for {endpoint}: {e}")
            return {}
    
    def get_calendar_collaborators(self, days_back: int = 30) -> Dict[str, Any]:
        """Analyze calendar events for collaboration patterns"""
        print(f"📅 Analyzing calendar collaborators (last {days_back} days)...")
        
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days_back)
        
        # Format dates for Graph API
        start_str = start_date.strftime('%Y-%m-%dT00:00:00Z')
        end_str = end_date.strftime('%Y-%m-%dT23:59:59Z')
        
        endpoint = f"/me/events?$filter=start/dateTime ge '{start_str}' and end/dateTime le '{end_str}'&$select=subject,attendees,organizer,start,end,importance"
        
        events_data = self.make_graph_request(endpoint)
        events = events_data.get('value', [])
        
        collaborator_stats = defaultdict(lambda: {
            'meeting_count': 0,
            'total_duration': 0,
            'as_organizer': 0,
            'as_attendee': 0,
            'importance_high': 0,
            'latest_meeting': None,
            'meetings': []
        })
        
        for event in events:
            # Skip if no attendees
            attendees = event.get('attendees', [])
            if not attendees:
                continue
                
            # Calculate duration
            start_time = datetime.fromisoformat(event['start']['dateTime'].replace('Z', '+00:00'))
            end_time = datetime.fromisoformat(event['end']['dateTime'].replace('Z', '+00:00'))
            duration = (end_time - start_time).total_seconds() / 3600  # hours
            
            # Get organizer
            organizer = event.get('organizer', {})
            organizer_email = organizer.get('emailAddress', {}).get('address', '')
            
            # Process each attendee
            for attendee in attendees:
                email_addr = attendee.get('emailAddress', {})
                email = email_addr.get('address', '')
                name = email_addr.get('name', email)
                
                if not email:
                    continue
                    
                # Skip self
                if 'cyl@microsoft.com' in email.lower():
                    continue
                    
                stats = collaborator_stats[email]
                stats['name'] = name
                stats['email'] = email
                stats['meeting_count'] += 1
                stats['total_duration'] += duration
                
                # Track organizer vs attendee
                if organizer_email == email:
                    stats['as_organizer'] += 1
                else:
                    stats['as_attendee'] += 1
                    
                # Track importance
                if event.get('importance') == 'high':
                    stats['importance_high'] += 1
                    
                # Track latest meeting
                if not stats['latest_meeting'] or start_time > stats['latest_meeting']:
                    stats['latest_meeting'] = start_time
                    
                # Store meeting details
                stats['meetings'].append({
                    'subject': event.get('subject', 'No Subject'),
                    'start': start_time,
                    'duration': duration,
                    'importance': event.get('importance', 'normal')
                })
        
        return dict(collaborator_stats)
    
    def get_email_collaborators(self, days_back: int = 30) -> Dict[str, Any]:
        """Analyze email for collaboration patterns"""
        print(f"📧 Analyzing email collaborators (last {days_back} days)...")
        
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days_back)
        start_str = start_date.strftime('%Y-%m-%dT00:00:00Z')
        
        # Get sent and received emails
        sent_endpoint = f"/me/mailFolders/SentItems/messages?$filter=sentDateTime ge {start_str}&$select=toRecipients,ccRecipients,subject,sentDateTime,importance"
        received_endpoint = f"/me/messages?$filter=receivedDateTime ge {start_str}&$select=from,toRecipients,ccRecipients,subject,receivedDateTime,importance"
        
        sent_data = self.make_graph_request(sent_endpoint)
        received_data = self.make_graph_request(received_endpoint)
        
        email_stats = defaultdict(lambda: {
            'emails_sent_to': 0,
            'emails_received_from': 0,
            'total_emails': 0,
            'latest_contact': None,
            'subjects': []
        })
        
        # Process sent emails
        for email in sent_data.get('value', []):
            sent_time = datetime.fromisoformat(email['sentDateTime'].replace('Z', '+00:00'))
            
            # Process all recipients
            all_recipients = []
            all_recipients.extend(email.get('toRecipients', []))
            all_recipients.extend(email.get('ccRecipients', []))
            
            for recipient in all_recipients:
                addr = recipient.get('emailAddress', {}).get('address', '')
                name = recipient.get('emailAddress', {}).get('name', addr)
                
                if not addr or 'cyl@microsoft.com' in addr.lower():
                    continue
                    
                stats = email_stats[addr]
                stats['name'] = name
                stats['email'] = addr
                stats['emails_sent_to'] += 1
                stats['total_emails'] += 1
                
                if not stats['latest_contact'] or sent_time > stats['latest_contact']:
                    stats['latest_contact'] = sent_time
                    
                stats['subjects'].append(email.get('subject', 'No Subject'))
        
        # Process received emails
        for email in received_data.get('value', []):
            received_time = datetime.fromisoformat(email['receivedDateTime'].replace('Z', '+00:00'))
            
            from_addr = email.get('from', {}).get('emailAddress', {})
            addr = from_addr.get('address', '')
            name = from_addr.get('name', addr)
            
            if not addr or 'cyl@microsoft.com' in addr.lower():
                continue
                
            stats = email_stats[addr]
            stats['name'] = name
            stats['email'] = addr
            stats['emails_received_from'] += 1
            stats['total_emails'] += 1
            
            if not stats['latest_contact'] or received_time > stats['latest_contact']:
                stats['latest_contact'] = received_time
                
            stats['subjects'].append(email.get('subject', 'No Subject'))
        
        return dict(email_stats)
    
    def get_file_collaborators(self) -> Dict[str, Any]:
        """Analyze shared files for collaboration patterns"""
        print("📁 Analyzing file collaboration patterns...")
        
        # Get recent files
        endpoint = "/me/drive/recent?$top=100"
        files_data = self.make_graph_request(endpoint)
        
        file_stats = defaultdict(lambda: {
            'shared_files': 0,
            'files': [],
            'latest_shared': None
        })
        
        for file_item in files_data.get('value', []):
            # Check if file has collaboration info
            shared_info = file_item.get('remoteItem', {}) or file_item
            
            # Try to get last modified by
            last_modified_by = shared_info.get('lastModifiedBy', {})
            user_info = last_modified_by.get('user', {})
            
            email = user_info.get('email', '')
            name = user_info.get('displayName', email)
            
            if not email or 'cyl@microsoft.com' in email.lower():
                continue
                
            modified_time = shared_info.get('lastModifiedDateTime')
            if modified_time:
                modified_time = datetime.fromisoformat(modified_time.replace('Z', '+00:00'))
                
            stats = file_stats[email]
            stats['name'] = name
            stats['email'] = email
            stats['shared_files'] += 1
            stats['files'].append({
                'name': shared_info.get('name', 'Unknown File'),
                'modified': modified_time,
                'type': shared_info.get('name', '').split('.')[-1] if '.' in shared_info.get('name', '') else 'unknown'
            })
            
            if not stats['latest_shared'] or (modified_time and modified_time > stats['latest_shared']):
                stats['latest_shared'] = modified_time
        
        return dict(file_stats)
    
    def analyze_comprehensive_collaboration(self) -> Dict[str, Any]:
        """Run comprehensive collaboration analysis"""
        print("\n🚀 COMPREHENSIVE COLLABORATION ANALYSIS")
        print("=" * 50)
        print("Using proven working Microsoft Graph authentication")
        print()
        
        # Get all collaboration data
        calendar_data = self.get_calendar_collaborators()
        email_data = self.get_email_collaborators()
        file_data = self.get_file_collaborators()
        
        # Combine all collaboration signals
        all_collaborators = {}
        
        # Start with calendar data
        for email, cal_stats in calendar_data.items():
            all_collaborators[email] = {
                'name': cal_stats['name'],
                'email': email,
                'calendar': cal_stats,
                'email': {},
                'files': {},
                'total_score': 0
            }
        
        # Add email data
        for email, email_stats in email_data.items():
            if email not in all_collaborators:
                all_collaborators[email] = {
                    'name': email_stats['name'],
                    'email': email,
                    'calendar': {},
                    'email': email_stats,
                    'files': {},
                    'total_score': 0
                }
            else:
                all_collaborators[email]['email'] = email_stats
        
        # Add file data
        for email, file_stats in file_data.items():
            if email not in all_collaborators:
                all_collaborators[email] = {
                    'name': file_stats['name'],
                    'email': email,
                    'calendar': {},
                    'email': {},
                    'files': file_stats,
                    'total_score': 0
                }
            else:
                all_collaborators[email]['files'] = file_stats
        
        # Calculate comprehensive collaboration scores
        for email, collab in all_collaborators.items():
            score = 0
            
            # Calendar signals (weight: 3)
            cal = collab['calendar']
            if cal:
                score += cal.get('meeting_count', 0) * 3
                score += cal.get('total_duration', 0) * 2
                score += cal.get('importance_high', 0) * 5
            
            # Email signals (weight: 2)
            email_stats = collab['email']
            if email_stats:
                score += email_stats.get('total_emails', 0) * 2
            
            # File signals (weight: 4 - indicates deep collaboration)
            files = collab['files']
            if files:
                score += files.get('shared_files', 0) * 4
            
            collab['total_score'] = score
        
        # Sort by collaboration score
        sorted_collaborators = sorted(
            all_collaborators.items(),
            key=lambda x: x[1]['total_score'],
            reverse=True
        )
        
        # Display results
        print("\n📊 TOP COLLABORATORS (Real Microsoft Graph Data)")
        print("-" * 70)
        
        for i, (email, collab) in enumerate(sorted_collaborators[:20], 1):
            print(f"\n{i:2d}. {collab['name']} ({email})")
            print(f"    🎯 Total Score: {collab['total_score']:.1f}")
            
            # Calendar details
            cal = collab['calendar']
            if cal:
                print(f"    📅 Meetings: {cal.get('meeting_count', 0)} meetings, {cal.get('total_duration', 0):.1f}h total")
                if cal.get('importance_high', 0) > 0:
                    print(f"        ⚡ {cal['importance_high']} high-importance meetings")
            
            # Email details  
            email_stats = collab['email']
            if email_stats:
                sent = email_stats.get('emails_sent_to', 0)
                received = email_stats.get('emails_received_from', 0)
                print(f"    📧 Emails: {sent} sent to, {received} received from")
            
            # File details
            files = collab['files']
            if files:
                print(f"    📁 Files: {files.get('shared_files', 0)} shared files")
        
        # Save results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"comprehensive_collaboration_analysis_{timestamp}.json"
        
        results = {
            'timestamp': timestamp,
            'analysis_type': 'comprehensive_graph_collaboration',
            'data_sources': ['calendar', 'email', 'files'],
            'collaborators': dict(sorted_collaborators),
            'summary': {
                'total_collaborators': len(all_collaborators),
                'with_meetings': len([c for c in all_collaborators.values() if c['calendar']]),
                'with_emails': len([c for c in all_collaborators.values() if c['email']]),
                'with_files': len([c for c in all_collaborators.values() if c['files']])
            }
        }
        
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        print(f"\n💾 Results saved to: {output_file}")
        print(f"\n✅ Analysis complete! Found {len(all_collaborators)} total collaborators")
        print("\n💡 This analysis used REAL Microsoft Graph data:")
        print("   • Calendar events and meeting patterns")  
        print("   • Email communication history")
        print("   • Shared file collaboration")
        print("   • Multi-modal collaboration scoring")
        
        return results

def main():
    """Main execution function"""
    try:
        analyzer = WorkingGraphCollaborator()
        results = analyzer.analyze_comprehensive_collaboration()
        
        # Check for Haidong specifically
        haidong_variants = ['haidong', 'hai dong', 'haodong', 'dongmei zhang']
        print(f"\n🔍 CHECKING FOR HAIDONG ZHANG:")
        
        found_haidong = False
        for email, collab in results['collaborators'].items():
            name = collab['name'].lower()
            if any(variant in name for variant in haidong_variants):
                print(f"   ✅ Found: {collab['name']} ({email}) - Score: {collab['total_score']}")
                found_haidong = True
        
        if not found_haidong:
            print("   ⚠️  Haidong Zhang not found in current collaboration data")
            print("   💡 This suggests missing Teams chat and document co-authoring data")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return

if __name__ == "__main__":
    main()