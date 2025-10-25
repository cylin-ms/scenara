#!/usr/bin/env python3
"""Find Xiaodong Liu in latest results"""

import json
import glob

# Get latest results file
files = sorted(glob.glob('collaborator_discovery_results_*.json'))
if not files:
    print("No results files found")
    exit(1)

latest = files[-1]
print(f"📁 Loading: {latest}\n")

with open(latest, 'r', encoding='utf-8') as f:
    data = json.load(f)

collaborators = data['collaborators']
print(f"Total collaborators: {len(collaborators)}\n")

# Find Xiaodong Liu
found = False
for i, c in enumerate(collaborators, 1):
    if 'xiaodong' in c['name'].lower():
        print(f"🎯 FOUND: Rank #{i}")
        print(f"   Name: {c['name']}")
        print(f"   Importance Score: {c.get('importance_score', 0):.2f}")
        print(f"   Total Meetings: {c.get('total_meetings', 0)}")
        print(f"   Genuine Meetings: {c.get('genuine_collaboration_meetings', 0)}")
        print(f"   1:1 Meetings: {c.get('one_on_one_meetings', 0)}")
        print(f"   Teams Chat: {c.get('teams_chat', {})}")
        print(f"   Evidence: {c.get('collaboration_evidence', [])}")
        found = True
        break

if not found:
    print("❌ Xiaodong Liu NOT in collaborators list!")
    print("\nChecking top 30 for context:")
    for i, c in enumerate(collaborators[:30], 1):
        meetings = c.get('total_meetings', 0)
        chats = c.get('teams_chat', {}).get('total_chats', 0)
        score = c.get('importance_score', 0)
        print(f"{i:2d}. {c['name']:30s} | Score: {score:7.2f} | Meetings: {meetings:3d} | Chats: {chats:2d}")
