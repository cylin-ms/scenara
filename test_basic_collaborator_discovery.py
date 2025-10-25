"""
Test basic collaborator discovery WITHOUT LLM classification
Goes back to the working baseline before meeting type classification integration
"""
import sys
sys.path.insert(0, 'c:/Users/cyl/Projects/Scenara_v6.0_checkpoint/Scenara')

from tools.collaborator_discovery import CollaboratorDiscoveryTool

print("="*80)
print("BASIC COLLABORATOR DISCOVERY TEST (NO LLM CLASSIFICATION)")
print("="*80)

# Initialize WITHOUT LLM classifier
tool = CollaboratorDiscoveryTool(
    calendar_data_file="meeting_prep_data/real_calendar_scenarios.json"
)

# Override user name
tool.user_name = "Chin-Yew Lin"

# Disable LLM classification
tool.use_llm_classifier = False
print(f"\n✅ LLM Classifier Disabled: use_llm_classifier = {tool.use_llm_classifier}")
print(f"✅ Using keyword-based classification (fast, reliable)\n")

# Run discovery
print("Running basic discovery...")
print("-" * 80)

results = tool.discover_collaborators(limit=20)

print("\n" + "="*80)
print(f"TOP 20 COLLABORATORS (out of {results['total_collaborators_found']} total)")
print("="*80)

for i, collab in enumerate(results.get('collaborators', [])[:20], 1):
    print(f"\n{i}. {collab['name']}")
    print(f"   Importance Score: {collab['importance_score']:.2f}")
    print(f"   Final Score: {collab['final_score']:.2f}")
    print(f"   Confidence: {collab['confidence']*100:.1f}%")
    print(f"   Meetings: {collab['total_meetings']} total")
    print(f"   - 1:1 meetings: {collab['one_on_one']}")
    print(f"   - Organized by me: {collab['organized_by_me']}")
    print(f"   - Genuine collaboration: {collab['genuine_collaboration_meetings']}")
    
    # Show Graph API verification if available
    if collab.get('graph_api_verified'):
        print(f"   ✅ Graph API Rank: #{collab['graph_api_rank']}")
    
    # Show chat data if available
    if collab.get('chat_count', 0) > 0:
        print(f"   💬 Teams Chats: {collab['chat_count']}")
    
    # Show document data if available  
    if collab.get('total_document_shares', 0) > 0:
        print(f"   📄 Document Shares: {collab['total_document_shares']}")
    
    # Show evidence
    if collab.get('collaboration_evidence'):
        print(f"   Evidence: {', '.join(collab['collaboration_evidence'][:2])}")

print("\n" + "="*80)
print("SUMMARY")
print("="*80)
print(f"Total Collaborators: {results['total_collaborators_found']}")
print(f"Algorithm Version: {results.get('algorithm_version', 'N/A')}")
print(f"Graph API Integrated: {results.get('graph_api_integrated', False)}")
print(f"Teams Chat Integrated: {results.get('teams_chat_integrated', False)}")
print(f"Document Sharing Integrated: {results.get('document_sharing_integrated', False)}")
print("="*80)
