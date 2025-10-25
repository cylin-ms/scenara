"""Quick check of merged calendar structure"""
import json

with open('my_calendar_events_complete.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

if isinstance(data, dict) and 'events' in data:
    events = data['events']
else:
    events = data

print(f"Total events: {len(events)}")
print()

if events:
    sample = events[0]
    print("Sample event keys:", list(sample.keys()))
    print()
    
    if 'attendees' in sample and sample['attendees']:
        print("Sample attendee:", sample['attendees'][0])
    print()
    
    if 'subject' in sample:
        print("Sample subject:", sample['subject'])
    print()
    
    # Check for Haidong in first 50 events
    print("Searching for 'Haidong' in first 50 events...")
    for i, event in enumerate(events[:50]):
        attendees = event.get('attendees', [])
        for att in attendees:
            name = att.get('emailAddress', {}).get('name', '')
            if 'haidong' in name.lower():
                print(f"  Found in event {i}: {event.get('subject', 'No subject')}")
                print(f"  Attendee: {name}")
                break
