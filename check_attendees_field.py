#!/usr/bin/env python3
"""Check if attendees field exists in SilverFlow calendar data"""

import json

with open('SilverFlow/data/out/graph_meetings.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

events = data['events']
print(f"Total events: {len(events)}\n")

# Check Meeting #22 (Xiaodong 1:1)
meeting22 = events[21]
print(f"Meeting #22: {meeting22['subject']}")
print(f"Organizer: {meeting22.get('organizer', {})}")
print(f"\n📋 All fields in this meeting:")
for key in sorted(meeting22.keys()):
    print(f"  • {key}")

print(f"\n🔍 Checking for 'attendees' field:")
if 'attendees' in meeting22:
    print(f"✅ YES - attendees field exists")
    print(f"   Attendees: {meeting22['attendees']}")
else:
    print(f"❌ NO - attendees field is missing!")
    print(f"   This is why Xiaodong Liu wasn't extracted from calendar data")
    print(f"   We only see organizer: {meeting22.get('organizer', {})}")
