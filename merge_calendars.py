"""
Merge calendar events from multiple time periods and find dormant collaborators.
"""

import json
from collections import defaultdict
from datetime import datetime

# Load all calendar extractions
print("Loading calendar data from multiple periods...")

# April-June (92 events)
with open('my_calendar_events_full.json', 'r', encoding='utf-8') as f:
    april_june = json.load(f)
    if isinstance(april_june, dict) and 'events' in april_june:
        events_1 = april_june['events']
    else:
        events_1 = april_june

# July-September (125 events)
with open('SilverFlow/data/out/graph_meetings.json', 'r', encoding='utf-8') as f:
    july_sep = json.load(f)
    if isinstance(july_sep, dict) and 'events' in july_sep:
        events_2 = july_sep['events']
    else:
        events_2 = july_sep

# Merge all events
all_events = events_1 + events_2

print(f"✅ Total events loaded: {len(all_events)}")
print(f"   April-June: {len(events_1)} events")
print(f"   July-September+: {len(events_2)} events")

# Save merged calendar
merged_data = {'events': all_events}
with open('my_calendar_events_complete.json', 'w', encoding='utf-8') as f:
    json.dump(merged_data, f, indent=2, ensure_ascii=False)

print(f"✅ Saved {len(all_events)} events to my_calendar_events_complete.json")

# Get date range
dates = []
for event in all_events:
    start_str = event.get('start', {}).get('dateTime', '')
    if start_str:
        try:
            dt = datetime.fromisoformat(start_str.replace('Z', '+00:00'))
            dates.append(dt)
        except:
            pass

if dates:
    print(f"📅 Date range: {min(dates).strftime('%Y-%m-%d')} to {max(dates).strftime('%Y-%m-%d')}")
