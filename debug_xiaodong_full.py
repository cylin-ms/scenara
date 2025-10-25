#!/usr/bin/env python3
"""Debug Xiaodong's complete scoring"""

from tools.collaborator_discovery import CollaboratorDiscoveryTool

tool = CollaboratorDiscoveryTool()
tool.calendar_data_file = 'my_calendar_events_200.json'
tool.use_llm_classifier = False

# Load all data
calendar_data = tool.load_calendar_data()
collaboration_scores = tool.analyze_collaboration_patterns(calendar_data)

# Enrich
graph_data = tool.load_graph_api_data()
if graph_data:
    collaboration_scores = tool.enrich_with_graph_data(collaboration_scores, graph_data)

chat_data = tool.load_teams_chat_data()
if chat_data:
    collaboration_scores = tool.enrich_with_chat_data(collaboration_scores, chat_data)

doc_data = tool.load_document_collaboration_data()
if doc_data:
    collaboration_scores = tool.enrich_with_document_data(collaboration_scores, doc_data)

# Check Xiaodong after enrichments
if 'Xiaodong Liu' in collaboration_scores:
    x = collaboration_scores['Xiaodong Liu']
    print("\n" + "="*70)
    print("XIAODONG LIU - AFTER ALL ENRICHMENTS")
    print("="*70)
    print(f"Total Meetings: {x.get('total_meetings', 0)}")
    print(f"Chat Count: {x.get('chat_count', 0)}")
    print(f"Chat Score: {x.get('chat_collaboration_score', 0):.1f}")
    print(f"Final Score (from meetings): {sum(d['base_score'] for d in x.get('meeting_details', [])):.1f}")
    print(f"Collaboration Score: {x.get('collaboration_score', 0):.1f}")
    
    # Check filtering conditions
    has_calendar_evidence = x['total_meetings'] >= 2
    has_chat_evidence = x.get('chat_only_collaborator', False)
    has_document_evidence = x.get('document_only_collaborator', False)
    has_graph_api_evidence = x.get('graph_api_matched', False) and x.get('graph_api_rank', 999) <= 10
    has_significant_chat = x.get('chat_count', 0) >= 2
    
    print(f"\n{'='*70}")
    print("FILTERING CONDITIONS:")
    print(f"{'='*70}")
    print(f"Has calendar evidence (≥2 meetings): {has_calendar_evidence}")
    print(f"Has chat evidence (chat_only_collaborator): {has_chat_evidence}")
    print(f"Has document evidence: {has_document_evidence}")
    print(f"Has Graph API evidence: {has_graph_api_evidence}")
    print(f"Has significant chat (≥2 chats): {has_significant_chat}")
    print(f"\nPasses evidence check: {has_calendar_evidence or has_chat_evidence or has_document_evidence or has_graph_api_evidence}")
    
    # Check genuine collaboration
    has_genuine_collaboration = (
        x['one_on_one_meetings'] > 0 or
        x['organized_by_me'] > 0 or
        x['small_working_meetings'] > 0 or
        x['genuine_collaboration_meetings'] >= 2 or
        has_chat_evidence or
        has_document_evidence or
        has_graph_api_evidence or
        has_significant_chat
    )
    
    print(f"Has genuine collaboration: {has_genuine_collaboration}")
    
    # Check final score
    final_score = sum(d['base_score'] for d in x.get('meeting_details', []))
    if final_score == 0 and (has_chat_evidence or has_document_evidence):
        final_score = x.get('collaboration_score', 0)
    graph_api_boost = x.get('graph_api_boost', 0)
    final_score += graph_api_boost
    
    print(f"\nFinal score: {final_score:.1f}")
    print(f"Final score > 5: {final_score > 5}")
    
    is_system_account = False
    print(f"Is system account: {is_system_account}")
    
    # Multi-source check
    is_multi_source_only = (has_chat_evidence or has_document_evidence) and not has_calendar_evidence
    print(f"\nIs multi-source only: {is_multi_source_only}")
    
    if is_multi_source_only:
        passes_filter = has_genuine_collaboration and not is_system_account and final_score > 5
        print(f"Filter (multi-source): has_genuine={has_genuine_collaboration}, not_system={not is_system_account}, score>{final_score:.1f}>5 = {passes_filter}")
    else:
        passes_filter = has_genuine_collaboration and not is_system_account and final_score > 15
        print(f"Filter (calendar): has_genuine={has_genuine_collaboration}, not_system={not is_system_account}, score>{final_score:.1f}>15 = {passes_filter}")
    
    print(f"\n>>> WOULD PASS FILTER: {passes_filter}")
else:
    print("❌ Xiaodong Liu not in collaboration_scores")
