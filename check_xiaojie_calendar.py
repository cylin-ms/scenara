import json
from datetime import datetime

# Load full calendar
with open('my_calendar_events_full.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Handle SilverFlow format (has 'events' key)
if isinstance(data, dict) and 'events' in data:
    events = data['events']
else:
    events = data

# Find Xiaojie meetings
xiaojie_events = []
for e in events:
    attendees = e.get('attendees', [])
    for att in attendees:
        name = att.get('emailAddress', {}).get('name', '')
        if 'xiaojie' in name.lower():
            xiaojie_events.append(e)
            break

print(f"Found {len(xiaojie_events)} events with Xiaojie Zhou")
print()

if xiaojie_events:
    # Get dates
    dates = []
    for e in xiaojie_events:
        subject = e.get('subject', 'No subject')
        start_str = e.get('start', {}).get('dateTime', 'N/A')
        print(f"• {subject}: {start_str[:10] if start_str != 'N/A' else 'N/A'}")
        
        if start_str != 'N/A':
            try:
                dt = datetime.fromisoformat(start_str.replace('Z', '+00:00'))
                dates.append(dt)
            except:
                pass
    
    if dates:
        most_recent = max(dates)
        days_ago = (datetime.now() - most_recent.replace(tzinfo=None)).days
        print()
        print(f"Last meeting: {most_recent.strftime('%Y-%m-%d')} ({days_ago} days ago)")
        print()
        
        if days_ago > 60:
            print(f"⚠️  DORMANT: No meetings in {days_ago} days!")
        elif days_ago > 30:
            print(f"⚡ COOLING: No meetings in {days_ago} days")
        else:
            print("✅ Active")
