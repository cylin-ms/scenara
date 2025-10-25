#!/usr/bin/env python3
"""
Display Full Top 20 Active Collaborators Report
Clean, comprehensive view of all 20 active collaborators
"""

import json

def main():
    # Load the results
    with open('collaborators_with_dormancy.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    top_20 = data.get('top_20_active', [])
    
    print("=" * 100)
    print("TOP 20 ACTIVE COLLABORATORS - FULL REPORT")
    print("=" * 100)
    print(f"Generated: {data['summary']['generated']}")
    print(f"Total Active Collaborators: {data['summary']['active']}")
    print(f"Dormant Collaborators (excluded): {data['summary']['dormant']}")
    print("=" * 100)
    print()
    
    # Create clean table
    print(f"{'RANK':<6} {'NAME':<35} {'SCORE':<10} {'MEETINGS':<10} {'1:1s':<8} {'CHATS':<8} {'LAST CONTACT':<15}")
    print("-" * 100)
    
    for i, collab in enumerate(top_20, 1):
        name = collab.get('name', 'Unknown')[:34]
        score = f"{collab.get('final_score', 0):.1f}"
        meetings = collab.get('total_meetings', 0)
        one_on_one = collab.get('one_on_one', 0)
        chats = collab.get('chat_count', 0)
        
        # Get last meeting date
        meeting_details = collab.get('meeting_details', [])
        if meeting_details:
            last_date = max(m.get('date', '') for m in meeting_details)[:10]
        else:
            last_date = 'N/A'
        
        print(f"{i:<6} {name:<35} {score:<10} {meetings:<10} {one_on_one:<8} {chats:<8} {last_date:<15}")
    
    print("=" * 100)
    print()
    
    # Detailed breakdown for each
    for i, collab in enumerate(top_20, 1):
        print("\n" + "=" * 100)
        print(f"#{i}: {collab.get('name', 'Unknown')}")
        print("=" * 100)
        
        # Scores
        print(f"\n📊 IMPORTANCE METRICS:")
        print(f"   Final Score:       {collab.get('final_score', 0):.1f}")
        print(f"   Importance Score:  {collab.get('importance_score', 0):.2f}")
        print(f"   Confidence:        {collab.get('confidence', 0):.2f}")
        
        # Collaboration metrics
        print(f"\n📈 COLLABORATION BREAKDOWN:")
        print(f"   Total Meetings:              {collab.get('total_meetings', 0)}")
        print(f"   Genuine Collaboration:       {collab.get('genuine_collaboration_meetings', 0)}")
        print(f"   One-on-One Meetings:         {collab.get('one_on_one', 0)}")
        print(f"   Teams Chats:                 {collab.get('chat_count', 0)}")
        print(f"   Shared Documents:            {collab.get('shared_documents', 0)}")
        
        # Multi-source indicators
        is_chat_only = collab.get('chat_only_collaborator', False)
        is_doc_only = collab.get('document_only_collaborator', False)
        if is_chat_only:
            print(f"   Type: 💬 Chat-Only Collaborator")
        elif is_doc_only:
            print(f"   Type: 📄 Document-Only Collaborator")
        else:
            print(f"   Type: Calendar + Multi-source")
        
        # Recent activity
        meeting_details = collab.get('meeting_details', [])
        if meeting_details:
            # Sort by date descending
            sorted_meetings = sorted(meeting_details, key=lambda x: x.get('date', ''), reverse=True)
            last_meeting = sorted_meetings[0]
            
            print(f"\n📅 RECENT ACTIVITY:")
            print(f"   Last Meeting Date:  {last_meeting.get('date', 'N/A')[:10]}")
            print(f"   Last Meeting:       {last_meeting.get('subject', 'N/A')}")
            print(f"   Meeting Type:       {last_meeting.get('meeting_type', 'Unknown')}")
            
            # Show last 5 meetings
            print(f"\n📋 LAST 5 MEETINGS:")
            for j, meeting in enumerate(sorted_meetings[:5], 1):
                date = meeting.get('date', 'N/A')[:10]
                subject = meeting.get('subject', 'No subject')[:60]
                mtype = meeting.get('meeting_type', 'Unknown')[:30]
                print(f"   [{j}] {date}: {subject}")
                print(f"       Type: {mtype}")
        
        # Graph API data
        graph_verified = collab.get('graph_api_verified', False)
        if graph_verified:
            print(f"\n🔍 GRAPH API VERIFICATION:")
            print(f"   Verified Name:  {collab.get('verified_name', 'N/A')}")
            print(f"   Graph Rank:     #{collab.get('graph_api_rank', 'N/A')}")
            job_title = collab.get('job_title', '')
            if job_title:
                print(f"   Job Title:      {job_title}")
        
        # Chat details
        if collab.get('chat_count', 0) > 0:
            print(f"\n💬 TEAMS CHAT DETAILS:")
            print(f"   Total Chats:       {collab.get('chat_count', 0)}")
            print(f"   Chat Type:         {collab.get('chat_type', 'N/A')}")
            days_since = collab.get('days_since_last_chat', 'N/A')
            if isinstance(days_since, int):
                print(f"   Last Chat:         {days_since} days ago")
            else:
                print(f"   Last Chat:         {days_since}")
        
        # Document sharing
        if collab.get('shared_documents', 0) > 0:
            print(f"\n📄 DOCUMENT SHARING:")
            print(f"   Shared Documents:  {collab.get('shared_documents', 0)}")
            print(f"   Doc Collab Score:  {collab.get('document_collaboration_score', 0)}")
            print(f"   Last Share:        {collab.get('document_recency_label', 'N/A')}")
    
    print("\n" + "=" * 100)
    print("END OF REPORT")
    print("=" * 100)

if __name__ == "__main__":
    main()
