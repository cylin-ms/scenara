#!/usr/bin/env python3
"""Quick check for Xiaodong Liu's ranking"""

from tools.collaborator_discovery import CollaboratorDiscoveryTool
import json

# Run discovery with new calendar data and enhanced chat weight
tool = CollaboratorDiscoveryTool()
tool.calendar_data_file = 'my_calendar_events_200.json'
tool.use_llm_classifier = False

print("Running collaborator discovery...")
results = tool.discover_collaborators()

collabs = results.get('collaborators', [])
print(f"\nTotal collaborators: {len(collabs)}")

# Find Xiaodong
xiaodong = [c for c in collabs if 'Xiaodong' in c.get('name', '')]

if xiaodong:
    x = xiaodong[0]
    rank = collabs.index(x) + 1
    print(f"\n{'='*60}")
    print(f"Xiaodong Liu - Rank #{rank}")
    print(f"{'='*60}")
    print(f"  Final Score: {x.get('final_score', 0):.1f}")
    print(f"  Importance Score: {x.get('importance_score', 0):.2f}")
    print(f"  Confidence: {x.get('confidence', 0):.2f}")
    print(f"  Meetings: {x.get('total_meetings', 0)}")
    print(f"  Chats: {x.get('chat_count', 0)}")
    print(f"  Chat Score: {x.get('chat_collaboration_score', 0):.1f}")
    print(f"  Chat Weight Applied: {x.get('chat_collaboration_score', 0) * 0.20:.1f}")
    print(f"  Has Chat Evidence: {x.get('has_chat_evidence', False)}")
    print(f"  Has Calendar Evidence: {x.get('has_calendar_evidence', False)}")
    
    # Show top 10 for comparison
    print(f"\n{'='*60}")
    print("Top 10 for comparison:")
    print(f"{'='*60}")
    for i, c in enumerate(collabs[:10], 1):
        print(f"{i:2}. {c.get('name', 'Unknown'):30} - {c.get('final_score', 0):6.1f} pts (meetings: {c.get('total_meetings', 0)}, chats: {c.get('chat_count', 0)})")
else:
    print("\n❌ Xiaodong Liu not found in collaborators!")
