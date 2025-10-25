#!/usr/bin/env python3
"""Debug why Xiaodong Liu is being filtered"""

from tools.collaborator_discovery import CollaboratorDiscoveryTool
import json

# Temporarily patch to see ALL candidates before filtering
tool = CollaboratorDiscoveryTool()
tool.calendar_data_file = 'my_calendar_events_200.json'
tool.use_llm_classifier = False

# Load and process data manually
calendar_data = tool.load_calendar_data()
print(f"Calendar events: {len(calendar_data)}\n")

collaboration_scores = tool.analyze_collaboration_patterns(calendar_data)

# Check Xiaodong specifically
if 'Xiaodong Liu' in collaboration_scores:
    x_data = collaboration_scores['Xiaodong Liu']
    print("="*60)
    print("Xiaodong Liu - RAW DATA BEFORE FILTERING")
    print("="*60)
    print(f"Total Meetings: {x_data.get('total_meetings', 0)}")
    print(f"Genuine Collaboration: {x_data.get('genuine_collaboration', 0)}")
    print(f"One-on-One: {x_data.get('one_on_one', 0)}")
    print(f"Chat Count: {x_data.get('chat_count', 0)}")
    print(f"Chat Score: {x_data.get('chat_collaboration_score', 0):.1f}")
    print(f"Final Score (meetings): {x_data.get('final_score', 0):.1f}")
    print(f"\nHas Calendar Evidence: {x_data.get('has_calendar_evidence', False)}")
    print(f"Has Chat Evidence: {x_data.get('has_chat_evidence', False)}")
    print(f"Has Genuine Collaboration: {x_data.get('has_genuine_collaboration', False)}")
    print(f"Is System Account: {x_data.get('is_system_account', False)}")
    
    # Calculate what importance_score would be
    collaboration_activity_score = x_data.get('genuine_collaboration', 0) * 0.25 * 100
    interaction_quality_score = x_data.get('interaction_quality', 0) * 100 * 0.20
    confidence_factors = x_data.get('confidence', 0)
    confidence_score = confidence_factors * 50 * 0.20
    chat_score = x_data.get('chat_collaboration_score', 0)
    
    importance_score = (
        collaboration_activity_score +
        interaction_quality_score +
        confidence_score +
        chat_score * 0.20  # ENHANCED 20% weight
    )
    
    print(f"\n{'='*60}")
    print("SCORE BREAKDOWN:")
    print(f"{'='*60}")
    print(f"Collaboration Activity: {collaboration_activity_score:.2f} ({x_data.get('genuine_collaboration', 0)} * 0.25 * 100)")
    print(f"Interaction Quality: {interaction_quality_score:.2f} ({x_data.get('interaction_quality', 0)} * 100 * 0.20)")
    print(f"Confidence: {confidence_score:.2f} ({confidence_factors} * 50 * 0.20)")
    print(f"Chat Score: {chat_score * 0.20:.2f} ({chat_score:.1f} * 0.20)")
    print(f"\nImportance Score: {importance_score:.2f}")
    print(f"Final Score: {x_data.get('final_score', 0):.1f}")
    print(f"\nFILTERING CHECK:")
    print(f"  Has genuine collaboration: {x_data.get('has_genuine_collaboration', False)}")
    print(f"  Is system account: {x_data.get('is_system_account', False)}")
    print(f"  Final score > 5: {x_data.get('final_score', 0) > 5}")
    print(f"  Would pass filter: {x_data.get('has_genuine_collaboration', False) and not x_data.get('is_system_account', False) and x_data.get('final_score', 0) > 5}")
else:
    print("❌ Xiaodong Liu not found in collaboration_scores!")
    print("\nAvailable people:")
    for name in list(collaboration_scores.keys())[:20]:
        print(f"  - {name}")
