"""Check which calendar files have attendees data"""
import json
import os

files_to_check = [
    'my_calendar_events_latest.json',
    'my_calendar_events.json',
    'my_calendar_events_50.json',
]

for filename in files_to_check:
    if not os.path.exists(filename):
        print(f"❌ {filename} - File not found")
        continue
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Handle different formats
        if isinstance(data, list):
            events = data
        elif isinstance(data, dict):
            events = data.get('events', data.get('value', []))
        else:
            events = []
        
        if not events:
            print(f"⚠️  {filename} - No events found")
            continue
        
        has_attendees = 'attendees' in events[0]
        print(f"{'✅' if has_attendees else '❌'} {filename} - {len(events)} events, attendees={'YES' if has_attendees else 'NO'}")
        
        if has_attendees and events[0].get('attendees'):
            print(f"   Sample: {len(events[0]['attendees'])} attendees in first event")
    
    except Exception as e:
        print(f"❌ {filename} - Error: {e}")

print("\n" + "="*80)
print("Checking SilverFlow extracted data...")
print("="*80)

# Check SilverFlow
sf_file = 'SilverFlow/data/out/graph_meetings.json'
if os.path.exists(sf_file):
    with open(sf_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    events = data.get('events', data) if isinstance(data, dict) else data
    has_attendees = 'attendees' in events[0] if events else False
    print(f"{'✅' if has_attendees else '❌'} {sf_file} - {len(events)} events, attendees={'YES' if has_attendees else 'NO'}")
