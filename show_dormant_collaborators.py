"""
Display dormant collaborators - previously active relationships that have gone quiet.

This script identifies collaborators who:
- Had significant collaboration history (high historical scores)
- Haven't had meetings, chats, or document sharing recently
- May need re-engagement to maintain important relationships
"""

import json
import sys
from datetime import datetime
from tools.collaborator_discovery import CollaboratorDiscoveryTool

def main():
    """Run dormant collaborator detection and display results."""
    
    print("=" * 80)
    print("DORMANT COLLABORATOR DETECTION")
    print("=" * 80)
    print()
    
    # Initialize the discovery tool
    tool = CollaboratorDiscoveryTool()
    
    # Use full calendar dataset
    tool.calendar_data_file = "my_calendar_events_full.json"
    tool.teams_chat_file = "teams_chat_analysis_20251026_002211.json"
    tool.document_file = "document_collaboration_analysis_20251026_014224.json"
    tool.graph_api_file = "graph_collaboration_analysis_20251025_043301.json"
    
    print(f"📂 Data Sources:")
    print(f"   Calendar: {tool.calendar_data_file}")
    print(f"   Teams Chat: {tool.teams_chat_file}")
    print(f"   Documents: {tool.document_file}")
    print(f"   Graph API: {tool.graph_api_file}")
    print()
    
    # Discover all collaborators first
    print("🔍 Step 1: Discovering all collaborators...")
    results = tool.discover_collaborators()
    
    collaboration_scores = results.get('collaboration_scores', {})
    print(f"✅ Found {len(collaboration_scores)} total collaborators")
    print()
    
    # Detect dormant collaborators at different thresholds
    thresholds = [
        (30, "⚡ Recently Inactive"),
        (60, "⚠️  Dormant"),
        (90, "🚨 High Risk")
    ]
    
    all_dormant = {}
    
    for days, label in thresholds:
        print(f"\n{label} (No interaction in {days}+ days)")
        print("-" * 80)
        
        dormant = tool.detect_dormant_collaborators(
            collaboration_scores,
            dormancy_threshold_days=days,
            min_historical_score=50.0
        )
        
        all_dormant[days] = dormant
        
        if not dormant:
            print(f"✅ No dormant collaborators at {days}-day threshold")
            continue
        
        # Display dormant collaborators
        for i, person in enumerate(dormant, 1):
            print(f"\n{i}. {person['name']}")
            print(f"   📊 Historical Score: {person['historical_score']:.0f}")
            print(f"   ⏰ Last Contact: {person['days_since_last_interaction']} days ago")
            print(f"   📅 Last Activity: {person['last_interaction_type']}")
            
            # Show collaboration history
            history_parts = []
            if person['total_meetings'] > 0:
                history_parts.append(f"{person['total_meetings']} meetings")
            if person['total_chats'] > 0:
                history_parts.append(f"{person['total_chats']} chats")
            if person['total_documents'] > 0:
                history_parts.append(f"{person['total_documents']} documents")
            
            print(f"   📝 History: {', '.join(history_parts)}")
            
            if person.get('job_title') and person['job_title'] != 'N/A':
                print(f"   💼 Role: {person['job_title']}")
            
            # Show specific last dates
            if person.get('last_meeting_date'):
                last_meeting = datetime.fromisoformat(person['last_meeting_date'])
                print(f"   🗓️  Last Meeting: {last_meeting.strftime('%Y-%m-%d')}")
            
            if person.get('last_chat_date'):
                last_chat = datetime.fromisoformat(person['last_chat_date'])
                print(f"   💬 Last Chat: {last_chat.strftime('%Y-%m-%d')}")
            
            if person.get('last_document_date'):
                last_doc = datetime.fromisoformat(person['last_document_date'])
                print(f"   📄 Last Document: {last_doc.strftime('%Y-%m-%d')}")
            
            # Suggest re-engagement action
            action = suggest_reengagement(person)
            print(f"   💡 Suggestion: {action}")
    
    # Summary
    print("\n" + "=" * 80)
    print("DORMANCY SUMMARY")
    print("=" * 80)
    print()
    
    total_dormant = len(all_dormant.get(60, []))
    recent_inactive = len(all_dormant.get(30, []))
    high_risk = len(all_dormant.get(90, []))
    
    print(f"Total Dormant (60+ days): {total_dormant}")
    print(f"Recently Inactive (30-59 days): {recent_inactive - total_dormant}")
    print(f"High Risk (90+ days): {high_risk}")
    print()
    
    # Action recommendations
    if high_risk > 0:
        print("🚨 PRIORITY ACTIONS:")
        print("   Schedule immediate 1:1 check-ins with high-risk dormant collaborators")
        print()
    
    if total_dormant > 0:
        print("⚠️  RECOMMENDED ACTIONS:")
        print("   Send reconnection emails or schedule casual catch-ups")
        print()
    
    if recent_inactive > 0:
        print("⚡ PREVENTIVE ACTIONS:")
        print("   Touch base with recently inactive collaborators before relationships cool")
        print()

def suggest_reengagement(person: dict) -> str:
    """Suggest appropriate re-engagement action based on collaboration history."""
    
    days = person['days_since_last_interaction']
    total_meetings = person['total_meetings']
    total_chats = person['total_chats']
    
    # High urgency for long dormancy
    if days > 90:
        return "🚨 Schedule 1:1 meeting immediately - relationship at risk"
    
    # Medium urgency
    if days > 60:
        if total_meetings > total_chats:
            return "📅 Send meeting invite for catch-up - was primarily meeting-based collaboration"
        else:
            return "💬 Send Teams message to reconnect - was primarily chat-based collaboration"
    
    # Low urgency
    if total_meetings >= 5:
        return "📧 Send casual check-in email or meeting invite"
    else:
        return "💬 Send Teams message to touch base"

if __name__ == "__main__":
    main()
