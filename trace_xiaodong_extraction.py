#!/usr/bin/env python3
"""Trace extraction of Xiaodong Liu to find where it's getting lost"""

import json
from datetime import datetime

# Load SilverFlow calendar
with open('SilverFlow/data/out/graph_meetings.json', 'r', encoding='utf-8') as f:
    silverflow = json.load(f)

user_name = "Chin-Yew Lin"

print("="*70)
print("TRACING XIAODONG LIU EXTRACTION")
print("="*70)

# Find all meetings with Xiaodong
xiaodong_meetings = []
for i, event in enumerate(silverflow['events'], 1):
    subject = event.get('subject', '')
    attendees_data = event.get('attendees', [])
    
    # Check if Xiaodong is in attendees
    for att in attendees_data:
        email_data = att.get('emailAddress', {})
        name = email_data.get('name', '')
        if 'xiaodong' in name.lower():
            xiaodong_meetings.append((i, event))
            break

print(f"\n🔍 Found {len(xiaodong_meetings)} meetings with Xiaodong Liu:\n")

for idx, (meeting_num, event) in enumerate(xiaodong_meetings, 1):
    print(f"Meeting #{meeting_num}: {event.get('subject', 'No Subject')}")
    print(f"   Start: {event.get('start', {}).get('dateTime', '')}")
    
    # Extract attendees using same logic as collaborator_discovery.py
    attendees_data = event.get('attendees', [])
    if attendees_data:
        attendees = [
            att.get('emailAddress', {}).get('name', 'Unknown')
            for att in attendees_data
            if att.get('emailAddress', {}).get('name')
        ]
        print(f"   Attendees BEFORE filtering: {attendees}")
        
        # Remove self (as the fix does)
        attendees = [att for att in attendees if att != user_name]
        print(f"   Attendees AFTER removing self: {attendees}")
        
        if not attendees:
            print(f"   ❌ SKIPPED: No collaborators after filtering")
        else:
            print(f"   ✅ EXTRACTED: {attendees}")
    print()

# Now check if these meetings make it into the converted scenarios
print("\n" + "="*70)
print("CHECKING CONVERSION TO SCENARA FORMAT")
print("="*70)

# Simulate the conversion logic from load_calendar_data()
scenara_events = []
for idx, event in enumerate(silverflow['events'], 1):
    # Extract organizer
    organizer_data = event.get('organizer', {})
    organizer_email = organizer_data.get('emailAddress', {})
    organizer_name = organizer_email.get('name', 'Unknown')
    organizer_address = organizer_email.get('address', '')
    
    # Extract attendees (NEW LOGIC with self-filtering)
    attendees_data = event.get('attendees', [])
    if attendees_data:
        attendees = [
            att.get('emailAddress', {}).get('name', 'Unknown')
            for att in attendees_data
            if att.get('emailAddress', {}).get('name')
        ]
        # IMPORTANT: Remove self from attendees to get collaborators
        attendees = [att for att in attendees if att != user_name]
    else:
        # No attendees in API response - use organizer as collaborator
        attendees = [organizer_name] if organizer_name != user_name else []
    
    # Skip if no collaborators (after removing self)
    if not attendees:
        continue
    
    # Check if this is one of Xiaodong's meetings
    if any('xiaodong' in att.lower() for att in attendees):
        print(f"\n✅ Meeting #{idx} WILL BE INCLUDED:")
        print(f"   Subject: {event.get('subject', '')}")
        print(f"   Collaborators: {attendees}")
        scenara_events.append({
            'id': f"silverflow_{idx:03d}",
            'subject': event.get('subject', ''),
            'attendees': attendees
        })

print(f"\n📊 Total Scenara events with Xiaodong: {sum(1 for e in scenara_events if any('xiaodong' in att.lower() for att in e['attendees']))}")
print(f"📊 Total Scenara events overall: {len(scenara_events)} (from {len(silverflow['events'])} original)")

if scenara_events:
    print(f"\n🎯 Xiaodong meetings that should be analyzed:")
    for event in scenara_events:
        if any('xiaodong' in att.lower() for att in event['attendees']):
            print(f"   • {event['subject']}: {event['attendees']}")
