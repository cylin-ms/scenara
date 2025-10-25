#!/usr/bin/env python3
"""
Show Top 20 Active Collaborators + Dormant Collaborators
Separates active and dormant relationships for better insights
"""

from tools.collaborator_discovery import CollaboratorDiscoveryTool
import json
from datetime import datetime, timedelta
from collections import defaultdict

def detect_dormant_collaborators(calendar_file='my_calendar_events_complete_attendees.json', 
                                 dormant_days=60, high_risk_days=90):
    """
    Fast dormant detection using calendar data with attendees.
    Returns dict of {name: {'last_contact': date, 'meetings': count, 'days_since': int}}
    """
    print(f"\n🔍 Detecting dormant collaborators (>{dormant_days} days since last contact)...")
    
    with open(calendar_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Handle different formats
    if isinstance(data, dict) and 'events' in data:
        events = data['events']
    elif isinstance(data, dict) and 'value' in data:
        events = data['value']
    else:
        events = data
    
    # Track last contact with each person
    last_contact = {}
    meeting_count = defaultdict(int)
    last_meeting = {}
    
    for event in events:
        if 'attendees' not in event:
            continue
        
        subject = event.get('subject', 'N/A')
        date_str = event.get('start', {}).get('dateTime', '')[:10]
        
        for attendee in event.get('attendees', []):
            name = attendee.get('emailAddress', {}).get('name', '')
            if not name or name == 'Chin-Yew Lin':  # Skip self
                continue
            
            meeting_count[name] += 1
            
            # Track most recent contact
            if name not in last_contact or date_str > last_contact[name]:
                last_contact[name] = date_str
                last_meeting[name] = subject
    
    # Calculate dormancy
    today = datetime.now()
    dormant_people = {}
    
    for name, last_date in last_contact.items():
        if meeting_count[name] < 2:  # Need at least 2 meetings to be considered a relationship
            continue
        
        last_dt = datetime.strptime(last_date, '%Y-%m-%d')
        days_since = (today - last_dt).days
        
        if days_since >= dormant_days:
            dormant_people[name] = {
                'last_contact': last_date,
                'days_since': days_since,
                'meetings': meeting_count[name],
                'last_meeting': last_meeting[name],
                'risk_level': 'HIGH' if days_since >= high_risk_days else 'MEDIUM'
            }
    
    print(f"   Found {len(dormant_people)} dormant collaborators (out of {len(last_contact)} total)")
    return dormant_people


def main():
    print("=" * 80)
    print("TOP 20 ACTIVE COLLABORATORS + DORMANT COLLABORATOR ANALYSIS")
    print("=" * 80)
    
    # Step 1: Detect dormant collaborators from calendar
    dormant_people = detect_dormant_collaborators(
        calendar_file='my_calendar_events_complete_attendees.json',
        dormant_days=60,
        high_risk_days=90
    )
    dormant_names = set(dormant_people.keys())
    
    # Step 2: Run collaborator discovery
    print("\n📊 Running Collaborator Discovery...")
    print("Using keyword-based classification (fast, no rate limits)")
    
    tool = CollaboratorDiscoveryTool()
    tool.calendar_data_file = "my_calendar_events_complete_attendees.json"
    tool.use_llm_classifier = False
    tool.llm_classifier_type = "Keyword-based"
    
    results = tool.discover_collaborators()
    all_collaborators = results.get('collaborators', [])
    
    # Step 3: Separate active and dormant
    active_collaborators = []
    dormant_collaborators = []
    
    for collab in all_collaborators:
        name = collab.get('name', '')
        if name in dormant_names:
            # Add dormancy info to collaborator data
            collab['dormancy_info'] = dormant_people[name]
            dormant_collaborators.append(collab)
        else:
            active_collaborators.append(collab)
    
    print(f"\n✅ Active Collaborators: {len(active_collaborators)}")
    print(f"⚠️  Dormant Collaborators: {len(dormant_collaborators)}")
    
    # Step 4: Display Top 20 Active Collaborators
    top_20_active = active_collaborators[:20]
    
    print(f"\n{'=' * 80}")
    print(f"TOP 20 ACTIVE COLLABORATORS (out of {len(active_collaborators)} active)")
    print(f"{'=' * 80}\n")
    
    for i, collab in enumerate(top_20_active, 1):
        print(f"\n{'#' * 80}")
        print(f"RANK #{i}: {collab.get('name', 'Unknown')}")
        print(f"{'#' * 80}")
        
        # Ranking Score
        importance_score = collab.get('importance_score', 0)
        final_score = collab.get('final_score', 0)
        print(f"\n📊 SCORES:")
        print(f"   Importance Score: {importance_score:.2f}")
        print(f"   Final Score: {final_score:.1f}")
        
        # Collaboration Metrics
        total_meetings = collab.get('total_meetings', 0)
        one_on_one = collab.get('one_on_one', 0)
        genuine_collab = collab.get('genuine_collaboration_meetings', 0)
        chat_count = collab.get('chat_count', 0)
        
        print(f"\n📈 COLLABORATION METRICS:")
        print(f"   Total Meetings: {total_meetings}")
        print(f"   Genuine Collaboration: {genuine_collab}")
        print(f"   One-on-One Meetings: {one_on_one}")
        print(f"   Teams Chats: {chat_count}")
        
        # Recent activity indicator
        meeting_details = collab.get('meeting_details', [])
        if meeting_details:
            most_recent = max(meeting_details, key=lambda x: x.get('date', ''))
            last_date = most_recent.get('date', 'N/A')
            print(f"   ✅ Last Meeting: {last_date}")
        
        # Show first 3 meetings
        print(f"\n📋 RECENT MEETING EVIDENCE ({len(meeting_details)} total):")
        for j, meeting in enumerate(meeting_details[:3], 1):
            print(f"   [{j}] {meeting.get('subject', 'No subject')}")
            print(f"       Date: {meeting.get('date', 'N/A')} | Type: {meeting.get('meeting_type', 'Unknown')}")
        
        if len(meeting_details) > 3:
            print(f"   ... and {len(meeting_details) - 3} more meetings")
        
        print(f"\n{'-' * 80}")
    
    # Step 5: Display Dormant Collaborators (sorted by importance)
    if dormant_collaborators:
        print(f"\n{'=' * 80}")
        print(f"⚠️  DORMANT COLLABORATORS - NEEDS ATTENTION ({len(dormant_collaborators)} total)")
        print(f"{'=' * 80}\n")
        print("These collaborators had significant relationships but haven't been contacted in 60+ days\n")
        
        # Sort by final_score to show most important dormant relationships first
        top_dormant = sorted(dormant_collaborators, key=lambda x: x.get('final_score', 0), reverse=True)[:20]
        
        for i, collab in enumerate(top_dormant, 1):
            name = collab.get('name', 'Unknown')
            dormancy = collab.get('dormancy_info', {})
            
            risk_icon = "🚨" if dormancy.get('risk_level') == 'HIGH' else "⚠️"
            print(f"{risk_icon} {i}. {name}")
            print(f"   Importance Score: {collab.get('final_score', 0):.1f}")
            print(f"   Total Meetings: {collab.get('total_meetings', 0)}")
            print(f"   Last Contact: {dormancy.get('last_contact', 'N/A')} ({dormancy.get('days_since', 0)} days ago)")
            print(f"   Last Meeting: {dormancy.get('last_meeting', 'N/A')}")
            print(f"   Risk Level: {dormancy.get('risk_level', 'N/A')}")
            print()
        
        if len(dormant_collaborators) > 20:
            print(f"   ... and {len(dormant_collaborators) - 20} more dormant collaborators")
    
    # Step 6: Summary Statistics
    print(f"\n{'=' * 80}")
    print("SUMMARY STATISTICS")
    print(f"{'=' * 80}")
    print(f"Total Collaborators Found: {len(all_collaborators)}")
    print(f"  ✅ Active Collaborators: {len(active_collaborators)}")
    print(f"  ⚠️  Dormant Collaborators: {len(dormant_collaborators)}")
    print(f"     - Medium Risk (60-89 days): {sum(1 for d in dormant_people.values() if d['risk_level'] == 'MEDIUM')}")
    print(f"     - High Risk (90+ days): {sum(1 for d in dormant_people.values() if d['risk_level'] == 'HIGH')}")
    print(f"\nClassification Method: Keyword-based (70-80% accuracy)")
    print(f"Dormancy Threshold: 60 days since last contact")
    
    # Save detailed results
    output_file = "collaborators_with_dormancy.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            'summary': {
                'total': len(all_collaborators),
                'active': len(active_collaborators),
                'dormant': len(dormant_collaborators),
                'generated': datetime.now().isoformat()
            },
            'top_20_active': top_20_active,
            'dormant_collaborators': dormant_collaborators,
            'classifier': 'Keyword-based',
            'metadata': results.get('metadata', {})
        }, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Detailed results saved to: {output_file}")
    print(f"{'=' * 80}\n")


if __name__ == "__main__":
    main()
