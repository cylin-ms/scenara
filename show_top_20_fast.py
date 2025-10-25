#!/usr/bin/env python3
"""
Show Top 20 Collaborators - Keyword-Based Classification
Fast execution without LLM rate limiting issues
"""

from tools.collaborator_discovery import CollaboratorDiscoveryTool
import json

def main():
    print("=" * 80)
    print("TOP 20 COLLABORATORS - Fast Keyword-Based Classification")
    print("=" * 80)
    
    # Initialize WITHOUT LLM to avoid rate limiting
    print("\nInitializing Collaborator Discovery Tool...")
    print("Using keyword-based classification (fast, no rate limits)")
    
    # Create tool and disable LLM, use full calendar data
    tool = CollaboratorDiscoveryTool()
    tool.calendar_data_file = "my_calendar_events_full.json"  # Use full 88-event SilverFlow dataset
    tool.use_llm_classifier = False  # Force keyword-based
    tool.llm_classifier_type = "Keyword-based"
    
    print(f"\nRunning discovery with {tool.llm_classifier_type}...")
    print("-" * 80)
    
    # Run discovery
    results = tool.discover_collaborators()
    
    # Get top collaborators
    top_collaborators = results.get('collaborators', [])[:20]
    
    print(f"\n{'=' * 80}")
    print(f"TOP 20 COLLABORATORS (out of {len(results.get('collaborators', []))} total)")
    print(f"{'=' * 80}\n")
    
    for i, collab in enumerate(top_collaborators, 1):
        print(f"\n{'#' * 80}")
        print(f"RANK #{i}: {collab.get('name', 'Unknown')}")
        print(f"{'#' * 80}")
        
        # Ranking Score
        importance_score = collab.get('importance_score', 0)
        final_score = collab.get('final_score', 0)
        confidence = collab.get('confidence', 0)
        print(f"\n📊 SCORES:")
        print(f"   Importance Score: {importance_score:.2f}")
        print(f"   Final Score: {final_score:.1f}")
        print(f"   Confidence: {confidence:.2f}")
        
        # Collaboration Metrics
        total_meetings = collab.get('total_meetings', 0)
        one_on_one = collab.get('one_on_one', 0)
        genuine_collab = collab.get('genuine_collaboration_meetings', 0)
        chat_count = collab.get('chat_count', 0)
        shared_docs = collab.get('shared_documents', 0)
        
        print(f"\n📈 COLLABORATION METRICS:")
        print(f"   Total Meetings: {total_meetings}")
        print(f"   Genuine Collaboration: {genuine_collab}")
        print(f"   One-on-One Meetings: {one_on_one}")
        print(f"   Teams Chats: {chat_count}")
        print(f"   Shared Documents: {shared_docs}")
        
        # Multi-source indicators
        is_chat_only = collab.get('chat_only_collaborator', False)
        is_doc_only = collab.get('document_only_collaborator', False)
        if is_chat_only:
            print(f"   💬 Chat-Only Collaborator (no calendar meetings)")
        if is_doc_only:
            print(f"   📄 Document-Only Collaborator (no meetings/chats)")
        
        # Evidence
        meeting_details = collab.get('meeting_details', [])
        print(f"\n📋 MEETING EVIDENCE ({len(meeting_details)} meetings):")
        
        for j, meeting in enumerate(meeting_details[:5], 1):  # Show first 5 meetings
            print(f"\n   [{j}] {meeting.get('subject', 'No subject')}")
            print(f"       Date: {meeting.get('date', 'N/A')}")
            print(f"       Type: {meeting.get('meeting_type', 'Unknown')}")
            print(f"       Category: {meeting.get('taxonomy_category', 'Unknown')}")
            print(f"       Attendees: {meeting.get('size', 0)} people")
            print(f"       Score: +{meeting.get('base_score', 0)} points")
            
            # Show collaboration evidence
            collab_evidence = meeting.get('collaboration_evidence', [])
            if collab_evidence:
                print(f"       Evidence: {', '.join(collab_evidence[:2])}")
        
        if len(meeting_details) > 5:
            print(f"\n   ... and {len(meeting_details) - 5} more meetings")
        
        # Additional data sources
        graph_rank = collab.get('graph_api_rank')
        graph_verified = collab.get('graph_api_verified', False)
        job_title = collab.get('job_title', '')
        
        if graph_verified and graph_rank:
            print(f"\n🔍 GRAPH API DATA:")
            print(f"   Verified Name: {collab.get('verified_name', 'N/A')}")
            print(f"   Graph Rank: #{graph_rank}")
            if job_title:
                print(f"   Job Title: {job_title}")
        
        # Document sharing info
        if shared_docs > 0:
            doc_score = collab.get('document_collaboration_score', 0)
            last_share = collab.get('document_recency_label', 'N/A')
            print(f"\n📄 DOCUMENT SHARING:")
            print(f"   Total Shares: {shared_docs}")
            print(f"   Collaboration Score: {doc_score}")
            print(f"   Last Share: {last_share} ago")
        
        # Chat collaboration info
        if chat_count > 0:
            chat_type = collab.get('chat_type', 'N/A')
            days_since_chat = collab.get('days_since_last_chat', 'N/A')
            print(f"\n💬 TEAMS CHAT:")
            print(f"   Chat Count: {chat_count}")
            print(f"   Chat Type: {chat_type}")
            print(f"   Last Chat: {days_since_chat} days ago" if isinstance(days_since_chat, int) else f"   Last Chat: {days_since_chat}")
        
        # Collaboration Strength (removed - not in data)
        # strength = collab.get('collaboration_strength', 'N/A')
        # print(f"\n💪 COLLABORATION STRENGTH: {strength}")
        
        # Recommended Actions (removed - not in data)
        # recommendations = collab.get('recommendations', [])
        # if recommendations:
        #     print(f"\n💡 RECOMMENDATIONS:")
        #     for rec in recommendations[:3]:
        #         print(f"   • {rec}")
        
        print(f"\n{'-' * 80}")
    
    # Summary Statistics
    print(f"\n{'=' * 80}")
    print("SUMMARY STATISTICS")
    print(f"{'=' * 80}")
    print(f"Total Collaborators Found: {len(results.get('collaborators', []))}")
    print(f"Classification Method: Keyword-based (70-80% accuracy)")
    print(f"Note: LLM classification would provide 95-99% accuracy but hits rate limits")
    
    # Save detailed results
    output_file = "top_20_collaborators_keyword.json"
    with open(output_file, 'w') as f:
        json.dump({
            'top_20': top_collaborators,
            'classifier': 'Keyword-based',
            'total_found': len(results.get('collaborators', [])),
            'metadata': results.get('metadata', {})
        }, f, indent=2)
    
    print(f"\nDetailed results saved to: {output_file}")
    print(f"{'=' * 80}\n")


if __name__ == "__main__":
    main()
