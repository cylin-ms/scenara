#!/usr/bin/env python3
"""
Quick Top 20 Summary - Clean List
"""

import json

with open('collaborators_with_dormancy.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

top_20 = data.get('top_20_active', [])

print("=" * 100)
print("TOP 20 ACTIVE COLLABORATORS (Conference Rooms Excluded)")
print("=" * 100)
print(f"\n{'RANK':<6} {'NAME':<40} {'SCORE':<10} {'MEETINGS':<10} {'1:1s':<8} {'CHATS':<8}")
print("-" * 100)

for i, collab in enumerate(top_20, 1):
    name = collab.get('name', 'Unknown')[:39]
    score = f"{collab.get('final_score', 0):.1f}"
    meetings = collab.get('total_meetings', 0)
    one_on_one = collab.get('one_on_one', 0)
    chats = collab.get('chat_count', 0)
    
    print(f"{i:<6} {name:<40} {score:<10} {meetings:<10} {one_on_one:<8} {chats:<8}")

print("=" * 100)
print(f"\nTotal Active: {data['summary']['active']}")
print(f"Total Dormant: {data['summary']['dormant']}")
print(f"Total: {data['summary']['total']}")
print("\n✅ Conference rooms filtered using attendee 'type' field (resource detection)")
print("=" * 100)
