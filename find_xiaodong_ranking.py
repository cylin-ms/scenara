#!/usr/bin/env python3
"""Find Xiaodong Liu in collaborator discovery results"""

import json

# Load the latest results
with open('collaborator_discovery_results_20251026_000755.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

collaborators = data['collaborators']
print(f"📊 Total collaborators found: {len(collaborators)}\n")

# Find Xiaodong Liu
xiaodong_found = False
for i, collab in enumerate(collaborators, 1):
    if 'xiaodong' in collab['name'].lower():
        print(f"🎯 FOUND Xiaodong Liu at rank #{i}")
        print(f"   Name: {collab['name']}")
        print(f"   Importance Score: {collab.get('importance_score', 0):.2f}")
        print(f"   Meetings: {collab.get('total_meetings', 0)}")
        print(f"   Teams Chat: {collab.get('teams_chat', {})}")
        print(f"   Evidence: {collab.get('evidence', [])}")
        print()
        xiaodong_found = True

if not xiaodong_found:
    print("❌ Xiaodong Liu NOT found in ranked collaborators")
    print("\n🔍 Let's check Teams chat data for 'Xiaodong Liu'...")
    
    # Load Teams chat data
    import glob
    chat_files = sorted(glob.glob('data/evaluation_results/teams_chat_analysis_*.json'))
    if chat_files:
        with open(chat_files[-1], 'r', encoding='utf-8') as f:
            chat_data = json.load(f)
        
        for collab in chat_data.get('collaborators', []):
            if 'xiaodong' in collab['name'].lower():
                print(f"✅ Found in Teams chat: {collab}")
                break

# Show top 30 for context
print("\n" + "="*70)
print("TOP 30 COLLABORATORS FOR CONTEXT:")
print("="*70)
for i, collab in enumerate(collaborators[:30], 1):
    meetings = collab.get('total_meetings', 0)
    score = collab.get('importance_score', 0)
    chat = collab.get('teams_chat', {})
    chat_str = f"💬 {chat.get('total_chats', 0)} chats" if chat else ""
    print(f"{i:2d}. {collab['name']:30s} | Score: {score:7.2f} | Meetings: {meetings:3d} | {chat_str}")
