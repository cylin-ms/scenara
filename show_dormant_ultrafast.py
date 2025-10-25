"""
Ultra-fast dormant detection - directly scans calendar file.
No collaboration scoring, just finds people with meetings who've gone quiet.
"""

import json
from datetime import datetime
from collections import defaultdict

def main():
    print("🚀 Fast Dormant Detection (Calendar Scan Only)")
    print("=" * 80)
    
    start_time = datetime.now()
    
    # Load calendar with attendees data
    # Use complete dataset with attendees from April-October 2025 (267 events)
    with open('my_calendar_events_complete_attendees.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Handle different formats
    if isinstance(data, dict) and 'events' in data:
        events = data['events']
    elif isinstance(data, dict) and 'value' in data:
        events = data['value']
    else:
        events = data
    
    print(f"📅 Loaded {len(events)} calendar events (April-October 2025 with attendees)")
    
    # Track each person's meetings
    person_meetings = defaultdict(list)
    
    for event in events:
        attendees = event.get('attendees', [])
        subject = event.get('subject', 'No subject')
        start_str = event.get('start', {}).get('dateTime', '')
        
        if not start_str:
            continue
        
        try:
            start_dt = datetime.fromisoformat(start_str.replace('Z', '+00:00'))
        except:
            continue
        
        # Add to each attendee's list
        for att in attendees:
            name = att.get('emailAddress', {}).get('name', '')
            if name and 'chin-yew' not in name.lower() and 'cyl@' not in name.lower():
                person_meetings[name].append({
                    'subject': subject,
                    'date': start_dt,
                    'date_str': start_dt.strftime('%Y-%m-%d')
                })
    
    # Find dormant collaborators
    now = datetime.now()
    dormant_results = []
    
    for person, meetings in person_meetings.items():
        if len(meetings) < 2:  # Skip if only 1 meeting
            continue
        
        # Find most recent meeting
        most_recent = max(meetings, key=lambda m: m['date'])
        days_since = (now - most_recent['date'].replace(tzinfo=None)).days
        
        # Check if dormant (60+ days)
        if days_since >= 60:
            dormant_results.append({
                'name': person,
                'total_meetings': len(meetings),
                'last_meeting_date': most_recent['date_str'],
                'last_meeting_subject': most_recent['subject'],
                'days_since': days_since,
                'risk': 'HIGH' if days_since >= 90 else 'MEDIUM'
            })
    
    # Sort by number of meetings (most important first)
    dormant_results.sort(key=lambda x: x['total_meetings'], reverse=True)
    
    elapsed = (datetime.now() - start_time).total_seconds()
    
    print(f"⏱️  Analysis completed in {elapsed:.2f} seconds")
    print()
    
    # Display results
    if dormant_results:
        print(f"⚠️  Found {len(dormant_results)} dormant collaborators:")
        print()
        
        for i, person in enumerate(dormant_results[:20], 1):
            risk_icon = "🚨" if person['risk'] == 'HIGH' else "⚠️"
            print(f"{risk_icon} {i}. {person['name']}")
            print(f"   📊 {person['total_meetings']} meetings in history")
            print(f"   ⏰ Last contact: {person['days_since']} days ago ({person['last_meeting_date']})")
            print(f"   📝 Last meeting: {person['last_meeting_subject']}")
            print()
    else:
        print("✅ No dormant collaborators found")
    
    print(f"\n⏱️  Total time: {elapsed:.2f} seconds")

if __name__ == "__main__":
    main()
