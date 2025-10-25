#!/usr/bin/env python3
"""
Manual Graph Explorer Collaboration Analyzer
Simple copy-paste approach that works reliably
"""

import json
import os
from datetime import datetime
from typing import Dict, Any, List

class ManualGraphCollaborationAnalyzer:
    def __init__(self):
        self.collaboration_queries = {
            "calendar_meetings": {
                "query": "me/calendarView?startDateTime=2025-09-01T00:00:00Z&endDateTime=2025-10-25T23:59:59Z&$select=subject,organizer,attendees,start,end",
                "description": "Recent calendar meetings with attendees"
            },
            "chat_messages": {
                "query": "me/chats?$expand=members&$top=20",
                "description": "Teams chat conversations"
            },
            "recent_emails": {
                "query": "me/messages?$top=50&$select=sender,toRecipients,ccRecipients,subject,receivedDateTime",
                "description": "Recent email communications"
            },
            "people_api": {
                "query": "me/people?$top=50",
                "description": "People you work with most"
            },
            "shared_files": {
                "query": "me/drive/sharedWithMe?$top=20",
                "description": "Files shared with you"
            },
            "teams": {
                "query": "me/joinedTeams",
                "description": "Teams you're member of"
            }
        }
    
    def collect_data_manually(self) -> Dict[str, Any]:
        """Collect data by asking user to copy-paste from Graph Explorer"""
        print("🚀 MANUAL GRAPH EXPLORER COLLABORATION ANALYZER")
        print("=" * 70)
        print("This tool will guide you through collecting collaboration data manually")
        print("from Microsoft Graph Explorer. More reliable than automation!")
        print()
        
        collected_data = {}
        
        print("📋 INSTRUCTIONS:")
        print("1. Open https://developer.microsoft.com/en-us/graph/graph-explorer")
        print("2. Sign in with your Microsoft account")
        print("3. For each query below, copy the query, run it, and paste the result")
        print()
        
        input("Press ENTER when you're ready to start...")
        print()
        
        for query_name, query_info in self.collaboration_queries.items():
            print(f"\n📡 DATA SOURCE: {query_info['description']}")
            print("=" * 60)
            print(f"🔍 Query to run: {query_info['query']}")
            print()
            print("STEPS:")
            print("1. Copy the query above")
            print("2. Paste it in Graph Explorer query box")
            print("3. Click 'Run query'")
            print("4. Copy the entire JSON response from the Response Preview")
            print("5. Paste it below")
            print()
            
            response_data = input("📋 Paste the JSON response here (or press ENTER to skip): ").strip()
            
            if response_data:
                try:
                    # Try to parse as JSON to validate
                    parsed_data = json.loads(response_data)
                    collected_data[query_name] = parsed_data
                    print("✅ Data collected successfully!")
                except json.JSONDecodeError:
                    print("⚠️  Invalid JSON format, saving as text...")
                    collected_data[query_name] = response_data
            else:
                print("⏭️  Skipped")
                collected_data[query_name] = None
        
        return collected_data
    
    def analyze_collaboration_from_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze collaboration patterns from collected data"""
        print("\n🔍 ANALYZING COLLABORATION PATTERNS")
        print("=" * 50)
        
        collaborators = {}
        analysis = {
            "top_collaborators": [],
            "collaboration_insights": [],
            "data_summary": {},
            "meeting_frequency": {},
            "communication_patterns": {}
        }
        
        # Analyze calendar meetings
        if data.get("calendar_meetings") and isinstance(data["calendar_meetings"], dict):
            meetings_data = data["calendar_meetings"]
            if "value" in meetings_data:
                meetings = meetings_data["value"]
                analysis["data_summary"]["calendar_meetings"] = len(meetings)
                print(f"📅 Found {len(meetings)} calendar meetings")
                
                # Extract attendees and organizers
                meeting_collaborators = {}
                for meeting in meetings:
                    if isinstance(meeting, dict):
                        # Get organizer
                        organizer = meeting.get("organizer", {})
                        if isinstance(organizer, dict) and "emailAddress" in organizer:
                            email = organizer["emailAddress"].get("address", "")
                            if email:
                                meeting_collaborators[email] = meeting_collaborators.get(email, 0) + 1
                        
                        # Get attendees
                        attendees = meeting.get("attendees", [])
                        if isinstance(attendees, list):
                            for attendee in attendees:
                                if isinstance(attendee, dict) and "emailAddress" in attendee:
                                    email = attendee["emailAddress"].get("address", "")
                                    if email:
                                        meeting_collaborators[email] = meeting_collaborators.get(email, 0) + 1
                
                # Sort by frequency
                sorted_meeting_collaborators = sorted(meeting_collaborators.items(), key=lambda x: x[1], reverse=True)
                analysis["meeting_frequency"] = dict(sorted_meeting_collaborators[:10])
                analysis["collaboration_insights"].append(f"Calendar analysis: {len(sorted_meeting_collaborators)} unique meeting collaborators")
        
        # Analyze email communications
        if data.get("recent_emails") and isinstance(data["recent_emails"], dict):
            emails_data = data["recent_emails"]
            if "value" in emails_data:
                emails = emails_data["value"]
                analysis["data_summary"]["recent_emails"] = len(emails)
                print(f"📧 Found {len(emails)} recent emails")
                
                email_collaborators = {}
                for email in emails:
                    if isinstance(email, dict):
                        # Get sender
                        sender = email.get("sender", {})
                        if isinstance(sender, dict) and "emailAddress" in sender:
                            sender_email = sender["emailAddress"].get("address", "")
                            if sender_email:
                                email_collaborators[sender_email] = email_collaborators.get(sender_email, 0) + 1
                        
                        # Get recipients
                        for recipient_type in ["toRecipients", "ccRecipients"]:
                            recipients = email.get(recipient_type, [])
                            if isinstance(recipients, list):
                                for recipient in recipients:
                                    if isinstance(recipient, dict) and "emailAddress" in recipient:
                                        rec_email = recipient["emailAddress"].get("address", "")
                                        if rec_email:
                                            email_collaborators[rec_email] = email_collaborators.get(rec_email, 0) + 1
                
                sorted_email_collaborators = sorted(email_collaborators.items(), key=lambda x: x[1], reverse=True)
                analysis["communication_patterns"] = dict(sorted_email_collaborators[:10])
                analysis["collaboration_insights"].append(f"Email analysis: {len(sorted_email_collaborators)} unique email collaborators")
        
        # Analyze People API data
        if data.get("people_api") and isinstance(data["people_api"], dict):
            people_data = data["people_api"]
            if "value" in people_data:
                people = people_data["value"]
                analysis["data_summary"]["people_api"] = len(people)
                print(f"👥 Found {len(people)} people from People API")
                
                people_scores = []
                for person in people:
                    if isinstance(person, dict):
                        name = person.get("displayName", "Unknown")
                        email = ""
                        if "scoredEmailAddresses" in person and person["scoredEmailAddresses"]:
                            email = person["scoredEmailAddresses"][0].get("address", "")
                        score = person.get("personType", {}).get("subclass", "Unknown")
                        people_scores.append({"name": name, "email": email, "type": score})
                
                analysis["top_collaborators"] = people_scores[:10]
                analysis["collaboration_insights"].append(f"People API: {len(people_scores)} ranked collaborators")
        
        # Analyze Teams data
        if data.get("teams") and isinstance(data["teams"], dict):
            teams_data = data["teams"]
            if "value" in teams_data:
                teams = teams_data["value"]
                analysis["data_summary"]["teams"] = len(teams)
                print(f"🏢 Found {len(teams)} Teams")
                analysis["collaboration_insights"].append(f"Teams membership: {len(teams)} teams")
        
        # Analyze shared files
        if data.get("shared_files") and isinstance(data["shared_files"], dict):
            files_data = data["shared_files"]
            if "value" in files_data:
                files = files_data["value"]
                analysis["data_summary"]["shared_files"] = len(files)
                print(f"📄 Found {len(files)} shared files")
                analysis["collaboration_insights"].append(f"File collaboration: {len(files)} shared files")
        
        return analysis
    
    def run_manual_analysis(self) -> Dict[str, Any]:
        """Run the complete manual analysis process"""
        # Collect data manually
        raw_data = self.collect_data_manually()
        
        # Analyze the data
        analysis = self.analyze_collaboration_from_data(raw_data)
        
        # Combine results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results = {
            "timestamp": timestamp,
            "method": "manual_graph_explorer",
            "raw_data": raw_data,
            "analysis": analysis
        }
        
        # Save results
        output_file = f"manual_collaboration_analysis_{timestamp}.json"
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        return results, output_file


def main():
    """Main execution function"""
    analyzer = ManualGraphCollaborationAnalyzer()
    
    try:
        results, output_file = analyzer.run_manual_analysis()
        
        print("\n🎊 COLLABORATION ANALYSIS COMPLETE!")
        print("=" * 50)
        
        analysis = results["analysis"]
        
        # Show summary
        print("\n📊 DATA COLLECTION SUMMARY:")
        for source, count in analysis.get("data_summary", {}).items():
            print(f"   • {source}: {count} items")
        
        # Show insights
        if analysis.get("collaboration_insights"):
            print("\n💡 KEY INSIGHTS:")
            for insight in analysis["collaboration_insights"]:
                print(f"   • {insight}")
        
        # Show top meeting collaborators
        if analysis.get("meeting_frequency"):
            print("\n📅 TOP MEETING COLLABORATORS:")
            for email, count in list(analysis["meeting_frequency"].items())[:5]:
                print(f"   • {email}: {count} meetings")
        
        # Show top email collaborators
        if analysis.get("communication_patterns"):
            print("\n📧 TOP EMAIL COLLABORATORS:")
            for email, count in list(analysis["communication_patterns"].items())[:5]:
                print(f"   • {email}: {count} emails")
        
        # Show People API results
        if analysis.get("top_collaborators"):
            print("\n👥 TOP PEOPLE API COLLABORATORS:")
            for person in analysis["top_collaborators"][:5]:
                print(f"   • {person['name']} ({person.get('email', 'No email')}) - {person.get('type', 'Unknown type')}")
        
        print(f"\n📄 Complete results saved to: {output_file}")
        
    except KeyboardInterrupt:
        print("\n⏹️  Analysis interrupted by user")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


if __name__ == "__main__":
    main()