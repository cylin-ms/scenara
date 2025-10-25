"""
Verify dormant detection results by checking specific collaborators
"""

import json
from datetime import datetime
from collections import defaultdict

def check_person(events, person_name):
    """Check meeting history for a specific person"""
    meetings = []
    
    for event in events:
        attendees = event.get('attendees', [])
        subject = event.get('subject', 'No subject')
        start_str = event.get('start', {}).get('dateTime', '')
        
        if not start_str:
            continue
        
        # Check if person is in attendees
        found = False
        for attendee in attendees:
            name = attendee.get('emailAddress', {}).get('name', '')
            if person_name.lower() in name.lower():
                found = True
                break
        
        if found:
            try:
                start_dt = datetime.fromisoformat(start_str.replace('Z', '+00:00'))
                meetings.append({
                    'date': start_dt,
                    'subject': subject,
                    'date_str': start_dt.strftime('%Y-%m-%d')
                })
            except:
                pass
    
    return sorted(meetings, key=lambda x: x['date'])

def main():
    # Load complete dataset
    with open('my_calendar_events_complete.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    if isinstance(data, dict) and 'events' in data:
        events = data['events']
    else:
        events = data
    
    print("=" * 80)
    print(f"DORMANCY VERIFICATION - {len(events)} events loaded")
    print("=" * 80)
    print()
    
    # Check specific people mentioned by user
    people_to_check = [
        'Haidong Zhang',
        'Xiaodong Liu', 
        'Xiaojie Zhou'
    ]
    
    now = datetime.now()
    
    for person in people_to_check:
        print(f"🔍 {person}")
        print("-" * 80)
        
        meetings = check_person(events, person)
        
        if not meetings:
            print(f"   ❌ No meetings found")
            print()
            continue
        
        print(f"   📊 Total meetings: {len(meetings)}")
        
        # Most recent
        most_recent = meetings[-1]
        days_since = (now - most_recent['date'].replace(tzinfo=None)).days
        print(f"   📅 Last meeting: {most_recent['date_str']} ({days_since} days ago)")
        print(f"   📝 Subject: {most_recent['subject']}")
        
        # Show recent meetings (last 5)
        print(f"\n   Recent meetings:")
        for meeting in meetings[-5:]:
            print(f"      • {meeting['date_str']}: {meeting['subject']}")
        
        # Dormancy status
        print()
        if days_since >= 90:
            print(f"   🚨 HIGH RISK DORMANT ({days_since} days)")
        elif days_since >= 60:
            print(f"   ⚠️  DORMANT ({days_since} days)")
        elif days_since >= 30:
            print(f"   ⚡ RECENTLY INACTIVE ({days_since} days)")
        else:
            print(f"   ✅ ACTIVE ({days_since} days)")
        
        print()
        print()

if __name__ == "__main__":
    main()
