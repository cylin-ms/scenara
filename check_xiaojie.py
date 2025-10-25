import json
from datetime import datetime

# Load data
with open('collaborator_discovery_results_20251026_001606.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Find Xiaojie
xiaojie = None
for c in data['collaborators']:
    name = c.get('name', '')
    if 'xiaojie' in name.lower():
        xiaojie = c
        break

if xiaojie:
    print(f"Found: {xiaojie['name']}")
    print(f"Total meetings: {xiaojie.get('total_meetings', 0)}")
    print(f"Final score: {xiaojie.get('final_score', 0)}")
    print()
    
    # Get meeting dates
    meetings = xiaojie.get('meeting_details', [])
    if meetings:
        print(f"Meeting dates:")
        for m in meetings:
            start = m.get('start_time', 'N/A')
            subject = m.get('subject', 'No subject')
            print(f"  • {start[:10] if start != 'N/A' else 'N/A'}: {subject}")
        
        # Find most recent
        dates = []
        for m in meetings:
            if m.get('start_time'):
                try:
                    dt = datetime.fromisoformat(m['start_time'].replace('Z', '+00:00'))
                    dates.append(dt)
                except:
                    pass
        
        if dates:
            most_recent = max(dates)
            days_ago = (datetime.now() - most_recent.replace(tzinfo=None)).days
            print()
            print(f"Last meeting: {most_recent.strftime('%Y-%m-%d')} ({days_ago} days ago)")
else:
    print("Xiaojie not found in collaborators list")
    print()
    print("Available collaborators:")
    for c in data['collaborators'][:10]:
        print(f"  • {c.get('name', 'Unknown')}")
