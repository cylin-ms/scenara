#!/usr/bin/env python3
"""Debug attendee extraction from Xiaodong meeting"""

import json

with open('SilverFlow/data/out/graph_meetings.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Meeting #22: Xiaodong 1:1
meeting = data['events'][21]
print(f"Meeting: {meeting['subject']}\n")

# Simulate extraction logic
organizer_data = meeting.get('organizer', {})
organizer_email = organizer_data.get('emailAddress', {})
organizer_name = organizer_email.get('name', 'Unknown')
print(f"Organizer: {organizer_name}")

attendees_data = meeting.get('attendees', [])
print(f"\nRaw attendees data ({len(attendees_data)} attendees):")
for i, att in enumerate(attendees_data, 1):
    email_data = att.get('emailAddress', {})
    print(f"  {i}. {email_data.get('name', 'Unknown')} <{email_data.get('address', '')}>")

# Current logic (from collaborator_discovery.py lines 924-933)
if attendees_data:
    attendees = [
        att.get('emailAddress', {}).get('name', 'Unknown')
        for att in attendees_data
        if att.get('emailAddress', {}).get('name')
    ]
    print(f"\n✅ Extracted attendees list: {attendees}")
else:
    attendees = [organizer_name]
    print(f"\n⚠️  No attendees - using organizer: {attendees}")

# The PROBLEM:
user_name = "Chin-Yew Lin"
print(f"\n🔍 Checking against user: {user_name}")
print(f"   Attendees before filtering: {attendees}")

# This is what we SHOULD do:
# Remove self from attendees to get collaborators
collaborators = [att for att in attendees if att != user_name]
print(f"   Collaborators after removing self: {collaborators}")

if collaborators:
    print(f"\n✅ SHOULD EXTRACT: {collaborators}")
else:
    print(f"\n❌ PROBLEM: No collaborators left after filtering")
