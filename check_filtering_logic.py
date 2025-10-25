#!/usr/bin/env python3
"""Check why we're only getting 2 events from 67"""

import json

with open('SilverFlow/data/out/graph_meetings.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

user_name = "Chin-Yew Lin"
events = data['events']

print(f"Total events: {len(events)}\n")

# Categorize events
included = 0
skipped_no_attendees_field = 0
skipped_empty_after_filtering = 0
skipped_only_self = 0

print("FIRST 10 MEETINGS ANALYSIS:")
print("="*70)

for i, event in enumerate(events[:10], 1):
    subject = event.get('subject', 'No Subject')
    organizer_name = event.get('organizer', {}).get('emailAddress', {}).get('name', 'Unknown')
    attendees_data = event.get('attendees', [])
    
    print(f"\n{i}. {subject}")
    print(f"   Organizer: {organizer_name}")
    
    if attendees_data:
        attendees = [
            att.get('emailAddress', {}).get('name', 'Unknown')
            for att in attendees_data
            if att.get('emailAddress', {}).get('name')
        ]
        print(f"   Attendees (raw): {attendees}")
        
        # Remove self
        attendees = [att for att in attendees if att != user_name]
        print(f"   Attendees (after removing self): {attendees}")
        
        if not attendees:
            print(f"   ❌ SKIP: No collaborators after filtering")
            skipped_empty_after_filtering += 1
        else:
            print(f"   ✅ INCLUDE: Collaborators = {attendees}")
            included += 1
    else:
        print(f"   ❌ SKIP: No attendees field")
        skipped_no_attendees_field += 1

print(f"\n{'='*70}")
print(f"SUMMARY (first 10):")
print(f"   ✅ Included: {included}")
print(f"   ❌ Skipped (empty after filtering): {skipped_empty_after_filtering}")
print(f"   ❌ Skipped (no attendees field): {skipped_no_attendees_field}")
