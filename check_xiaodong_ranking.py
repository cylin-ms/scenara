#!/usr/bin/env python3
"""Quick check of Xiaodong Liu's ranking"""

from tools.collaborator_discovery import CollaboratorDiscoveryTool

tool = CollaboratorDiscoveryTool()
tool.calendar_data_file = 'my_calendar_events_200.json'
tool.use_llm_classifier = False
results = tool.discover_collaborators()

collabs = results.get('collaborators', [])
print(f'Total collaborators: {len(collabs)}')

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
    print(f"  1:1 Meetings: {x.get('one_on_one_count', 0)}")
    print(f"  Chats: {x.get('chat_count', 0)}")
    print(f"  Chat Score: {x.get('chat_collaboration_score', 0):.1f}")
    print(f"  Chat Type: {x.get('chat_type', 'unknown')}")
    print(f"  Has chat evidence: {x.get('has_chat_evidence', False)}")
    print(f"  Has calendar evidence: {x.get('has_calendar_evidence', False)}")
    print(f"\nImportance Score Breakdown:")
    print(f"  collaboration_activity: {x.get('collaboration_activity_score', 0):.2f}")
    print(f"  interaction_quality: {x.get('interaction_quality_score', 0):.2f}")
    print(f"  confidence_score: {x.get('confidence_score', 0):.2f}")
    print(f"  chat_collaboration_score * 0.20: {x.get('chat_collaboration_score', 0) * 0.20:.2f}")
else:
    print('\nXiaodong Liu not found in collaborators!')
