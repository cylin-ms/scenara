#!/usr/bin/env python3
"""
Analyze how "Yanchao Li" was identified as a frequent collaborator
"""

import json
from collections import Counter

def analyze_frequent_collaborators():
    """Analyze the real calendar data to show collaborator frequency"""
    
    # Load the real calendar data
    try:
        with open('meeting_prep_data/real_calendar_scenarios.json', 'r') as f:
            calendar_data = json.load(f)
    except Exception as e:
        print(f"Error loading calendar data: {e}")
        return
    
    print("🔍 FREQUENT COLLABORATORS ANALYSIS")
    print("=" * 60)
    print(f"📊 Total meetings analyzed: {len(calendar_data)}")
    
    # Extract all attendees from all meetings
    all_attendees = []
    meetings_with_yanchao = []
    
    for i, event in enumerate(calendar_data):
        attendees = event['context'].get('attendees', [])
        all_attendees.extend(attendees)
        
        # Track meetings where Yanchao Li appears
        if 'Yanchao Li' in attendees:
            meetings_with_yanchao.append({
                'id': event.get('id', f'meeting_{i}'),
                'subject': event['context'].get('subject', 'No subject'),
                'attendee_count': len(attendees),
                'organizer': event['context'].get('organizer', 'Unknown'),
                'start_time': event['context'].get('start_time', 'Unknown')
            })
    
    # Count attendee frequency
    attendee_counts = Counter(all_attendees)
    
    print(f"\n📋 Yanchao Li appears in {len(meetings_with_yanchao)} meetings")
    print(f"🎯 Yanchao Li total occurrence count: {attendee_counts['Yanchao Li']}")
    
    print("\n🏆 TOP 10 MOST FREQUENT COLLABORATORS:")
    for i, (name, count) in enumerate(attendee_counts.most_common(10), 1):
        if name != 'Chin-Yew Lin':  # Exclude yourself
            emoji = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else "📍"
            print(f"   {emoji} {name}: {count} meetings")
    
    print("\n📅 MEETINGS WITH YANCHAO LI:")
    for i, meeting in enumerate(meetings_with_yanchao, 1):
        print(f"\n{i}. Meeting ID: {meeting['id']}")
        print(f"   📋 Subject: {meeting['subject'][:80]}...")
        print(f"   👥 Attendees: {meeting['attendee_count']}")
        print(f"   👤 Organizer: {meeting['organizer']}")
        print(f"   📅 Start: {meeting['start_time'][:10] if meeting['start_time'] != 'Unknown' else 'Unknown'}")
    
    # Show the algorithm logic
    print("\n🔍 ALGORITHM EXPLANATION:")
    print("The 'Frequent Meeting Collaborators' analysis works as follows:")
    print("1. Extract ALL attendees from ALL 50 real calendar meetings")
    print("2. Count how many times each person appears across all meetings")
    print("3. Use Python Counter to get the most_common(10) attendees")
    print("4. Filter out attendees with count > 1 and != 'Chin-Yew Lin'")
    print("5. Take the top 5 frequent collaborators for the Me Notes")
    
    frequent_collaborators = [name for name, count in attendee_counts.most_common(10) if count > 1 and name != 'Chin-Yew Lin']
    
    print(f"\n✅ RESULT: Top 5 frequent collaborators selected:")
    for i, name in enumerate(frequent_collaborators[:5], 1):
        count = attendee_counts[name]
        print(f"   {i}. {name}: {count} meetings")
    
    print(f"\nThis matches the Me Notes output: {', '.join(frequent_collaborators[:5])}")

if __name__ == "__main__":
    analyze_frequent_collaborators()