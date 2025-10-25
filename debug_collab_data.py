"""
Debug script to check what's in collaboration_scores before ranking
"""
import json
from tools.collaborator_discovery import CollaboratorDiscoveryTool

# Initialize tool
tool = CollaboratorDiscoveryTool()
tool.use_llm_classifier = False  # Use keyword-based (fast)

# Load all data
calendar_data = tool.load_calendar_data()
collaboration_scores = tool.analyze_collaboration_patterns(calendar_data)

# Enrich with other sources
graph_data = tool.load_graph_api_data()
if graph_data:
    collaboration_scores = tool.enrich_with_graph_data(collaboration_scores, graph_data)

chat_data = tool.load_teams_chat_data()
if chat_data:
    collaboration_scores = tool.enrich_with_chat_data(collaboration_scores, chat_data)

doc_data = tool.load_document_collaboration_data()
if doc_data:
    collaboration_scores = tool.enrich_with_document_data(collaboration_scores, doc_data)

# Check a few chat-only collaborators
print("\n" + "="*80)
print("CHECKING CHAT-ONLY COLLABORATORS")
print("="*80)

chat_only_count = 0
for person, data in collaboration_scores.items():
    if data.get('chat_only_collaborator', False):
        chat_only_count += 1
        if chat_only_count <= 5:  # Show first 5
            print(f"\nPerson: {person}")
            print(f"  total_meetings: {data['total_meetings']}")
            print(f"  chat_only_collaborator: {data.get('chat_only_collaborator', False)}")
            print(f"  chat_count: {data.get('chat_count', 0)}")
            print(f"  chat_collaboration_score: {data.get('chat_collaboration_score', 0)}")
            print(f"  collaboration_score: {data.get('collaboration_score', 0)}")

print(f"\n✅ Found {chat_only_count} chat-only collaborators total")

# Check document-only
doc_only_count = 0
for person, data in collaboration_scores.items():
    if data.get('document_only_collaborator', False):
        doc_only_count += 1
        print(f"\nDocument-only: {person}")
        print(f"  total_meetings: {data['total_meetings']}")
        print(f"  document_only_collaborator: {data.get('document_only_collaborator', False)}")
        print(f"  total_document_shares: {data.get('total_document_shares', 0)}")

print(f"\n✅ Found {doc_only_count} document-only collaborators total")
