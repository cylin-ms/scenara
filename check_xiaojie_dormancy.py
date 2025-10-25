"""Quick check for Xiaojie Zhou's dormancy status in the current top collaborators."""

import json
from datetime import datetime
from tools.collaborator_discovery import CollaboratorDiscoveryTool

print("Analyzing Xiaojie Zhou's collaboration status...")
print()

# Run discovery
tool = CollaboratorDiscoveryTool()
tool.calendar_data_file = "my_calendar_events_full.json"
tool.teams_chat_file = "teams_chat_analysis_20251026_002211.json"
tool.document_file = "document_collaboration_analysis_20251026_014224.json"
tool.graph_api_file = "graph_collaboration_analysis_20251025_043301.json"

results = tool.discover_collaborators()
scores = results.get('collaboration_scores', {})

# Find Xiaojie
xiaojie_data = scores.get('Xiaojie Zhou')

if xiaojie_data:
    print(f"✅ Found Xiaojie Zhou in collaboration scores")
    print()
    print(f"  Total meetings: {xiaojie_data.get('total_meetings', 0)}")
    print(f"  Final score: {xiaojie_data.get('final_score', 0):.1f}")
    print()
    
    # Get meeting dates
    meetings = xiaojie_data.get('meeting_details', [])
    if meetings:
        print(f"  Meetings ({len(meetings)} total):")
        dates = []
        for m in meetings:
            subject = m.get('subject', 'No subject')
            start = m.get('start_time', 'N/A')
            print(f"    • {start[:10] if start != 'N/A' else 'N/A'}: {subject}")
            
            if start != 'N/A':
                try:
                    dt = datetime.fromisoformat(start.replace('Z', '+00:00'))
                    dates.append(dt)
                except:
                    pass
        
        if dates:
            most_recent = max(dates)
            days_ago = (datetime.now() - most_recent.replace(tzinfo=None)).days
            print()
            print(f"  📅 Last meeting: {most_recent.strftime('%Y-%m-%d')}")
            print(f"  ⏰ Days since last contact: {days_ago}")
            print()
            
            if days_ago > 90:
                print(f"  🚨 STATUS: HIGH RISK DORMANT ({days_ago} days)")
                print(f"  💡 ACTION: Schedule immediate 1:1 - important relationship at risk!")
            elif days_ago > 60:
                print(f"  ⚠️  STATUS: DORMANT ({days_ago} days)")
                print(f"  💡 ACTION: Send reconnection message or meeting invite")
            elif days_ago > 30:
                print(f"  ⚡ STATUS: COOLING ({days_ago} days)")
                print(f"  💡 ACTION: Touch base before relationship goes dormant")
            else:
                print(f"  ✅ STATUS: ACTIVE")
else:
    print("❌ Xiaojie Zhou not found in collaboration scores")
