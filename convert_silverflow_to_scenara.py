#!/usr/bin/env python3
"""
Convert SilverFlow calendar format to Scenara format
"""
import json
import sys

# Read SilverFlow format
with open('SilverFlow/data/out/graph_meetings.json', 'r', encoding='utf-8') as f:
    silverflow_data = json.load(f)

# Extract events
events = silverflow_data.get('events', [])

# Convert to Scenara format - wrap in scenarios array
scenara_data = {
    "scenarios": events,
    "metadata": {
        "generated_at": silverflow_data.get('generatedAt'),
        "total_events": silverflow_data.get('totalEvents'),
        "time_zone": silverflow_data.get('timeZone'),
        "source": "SilverFlow graph_get_meetings.py"
    }
}

# Save
with open('meeting_prep_data/real_calendar_scenarios_fresh.json', 'w', encoding='utf-8') as f:
    json.dump(scenara_data, f, indent=2)

print(f"✅ Converted {len(events)} meetings to Scenara format")
print(f"📁 Saved to: meeting_prep_data/real_calendar_scenarios_fresh.json")
