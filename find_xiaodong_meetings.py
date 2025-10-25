#!/usr/bin/env python3
"""
Find Xiaodong Liu meetings in fresh calendar data
"""
import json

# Load fresh SilverFlow data
with open('SilverFlow/data/out/graph_meetings.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

events = data.get('events', [])

# Find Xiaodong meetings
xiaodong_meetings = []
for event in events:
    subject = event.get('subject', '')
    organizer = event.get('organizer', {}).get('emailAddress', {}).get('name', '')
    
    if 'Xiaodong' in subject or 'Xiaodong' in organizer or 'xiaodl@microsoft.com' in str(event):
        xiaodong_meetings.append(event)

print(f"✅ Found {len(xiaodong_meetings)} Xiaodong Liu meeting(s):\n")
for event in xiaodong_meetings:
    print(f"📅 {event['subject']}")
    print(f"   Organizer: {event.get('organizer', {}).get('emailAddress', {}).get('name', 'N/A')}")
    print(f"   When: {event['start']['dateTime']}")
    print()

# Also find Agentic Memory meetings
print("\n🔍 Searching for Agentic Memory meetings:")
for event in events:
    subject = event.get('subject', '')
    if 'Agentic' in subject and 'Memory' in subject:
        print(f"📅 {subject}")
        print(f"   Organizer: {event.get('organizer', {}).get('emailAddress', {}).get('name', 'N/A')}")
        print(f"   When: {event['start']['dateTime']}")
        print()
