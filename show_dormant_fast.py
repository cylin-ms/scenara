"""
Fast dormant collaborator detection using pre-computed results.

This script loads the already-computed collaboration scores and quickly
identifies dormant relationships without re-analyzing all the data.
"""

import json
from datetime import datetime, timedelta

def load_collaboration_data():
    """Load pre-computed collaboration scores."""
    
    # Try to load from recent results file
    result_files = [
        "collaborator_discovery_results_20251026_001606.json",  # 49 collaborators
        "collaborator_discovery_results_20251026_001748.json",  # 49 collaborators
        "collaborator_discovery_results_20251026_002212.json",  # 30 collaborators
        "collaborator_discovery_results_20251026_001407.json",  # 30 collaborators
        "collaborator_discovery_results_20251026_021309.json"
    ]
    
    for filename in result_files:
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                # Check for collaboration_scores (old format)
                if 'collaboration_scores' in data:
                    print(f"✅ Loaded data from: {filename}")
                    return data['collaboration_scores']
                
                # Check for collaborators list (new format)
                if 'collaborators' in data:
                    print(f"✅ Loaded data from: {filename} (new format)")
                    # Convert to dict keyed by name
                    collab_dict = {}
                    for c in data['collaborators']:
                        name = c.get('name')
                        if name:
                            collab_dict[name] = c
                    return collab_dict
        except:
            continue
    
    return None

def detect_dormant(collaboration_scores, threshold_days=60, min_score=50.0):
    """Detect dormant collaborators from pre-computed scores."""
    
    dormant = []
    current_time = datetime.now()
    
    for person, data in collaboration_scores.items():
        # Calculate historical importance
        historical_score = sum(detail.get('base_score', 0) 
                              for detail in data.get('meeting_details', []))
        
        # Skip if below minimum threshold
        if historical_score < min_score:
            continue
        
        # Check last interaction dates
        last_meeting = None
        last_chat = None
        
        # Get most recent meeting
        if data.get('meeting_details'):
            meeting_dates = []
            for m in data['meeting_details']:
                if m.get('start_time'):
                    try:
                        dt = datetime.fromisoformat(m['start_time'].replace('Z', '+00:00'))
                        meeting_dates.append(dt)
                    except:
                        pass
            
            if meeting_dates:
                last_meeting = max(meeting_dates)
        
        # Get last chat date
        if data.get('days_since_last_chat') is not None:
            days_since_chat = data['days_since_last_chat']
            last_chat = current_time - timedelta(days=days_since_chat)
        
        # Find most recent interaction
        interaction_dates = [d for d in [last_meeting, last_chat] if d is not None]
        
        if not interaction_dates:
            continue
        
        most_recent_interaction = max(interaction_dates)
        days_since_interaction = (current_time - most_recent_interaction).days
        
        # Check if dormant
        if days_since_interaction >= threshold_days:
            interaction_type = []
            if last_meeting == most_recent_interaction:
                interaction_type.append(f"meeting")
            if last_chat == most_recent_interaction:
                interaction_type.append(f"chat")
            
            dormant.append({
                'name': person,
                'historical_score': round(historical_score, 1),
                'final_score': data.get('final_score', 0),
                'days_since_last_interaction': days_since_interaction,
                'last_interaction_date': most_recent_interaction.strftime('%Y-%m-%d'),
                'last_interaction_type': ', '.join(interaction_type),
                'total_meetings': data.get('total_meetings', 0),
                'total_chats': data.get('chat_count', 0),
                'one_on_one': data.get('one_on_one_meetings', 0),
                'last_meeting_date': last_meeting.strftime('%Y-%m-%d') if last_meeting else 'N/A',
                'last_chat_date': last_chat.strftime('%Y-%m-%d') if last_chat else 'N/A',
                'job_title': data.get('job_title', 'N/A'),
                'dormancy_risk': 'HIGH' if days_since_interaction > 120 else 
                                'MEDIUM' if days_since_interaction > 90 else 'LOW'
            })
    
    # Sort by historical importance
    dormant.sort(key=lambda x: x['historical_score'], reverse=True)
    
    return dormant

def suggest_action(person):
    """Suggest re-engagement action."""
    
    days = person['days_since_last_interaction']
    one_on_one = person['one_on_one']
    
    if days > 120:
        return "🚨 URGENT: Schedule 1:1 meeting - relationship at critical risk"
    elif days > 90:
        return "⚠️  Schedule catch-up meeting soon"
    elif one_on_one > 0:
        return "📅 Send 1:1 meeting invite"
    else:
        return "💬 Send Teams message to reconnect"

def main():
    print("=" * 80)
    print("DORMANT COLLABORATOR DETECTION (Fast)")
    print("=" * 80)
    print()
    
    # Load pre-computed data
    print("📂 Loading pre-computed collaboration data...")
    collaboration_scores = load_collaboration_data()
    
    if not collaboration_scores:
        print("❌ Could not find pre-computed collaboration data")
        print("   Run show_top_20_fast.py first to generate results")
        return
    
    print(f"✅ Loaded {len(collaboration_scores)} collaborators")
    print()
    
    # Detect at different thresholds
    thresholds = [
        (30, "⚡ Recently Inactive (30-59 days)"),
        (60, "⚠️  Dormant (60-89 days)"),
        (90, "🚨 High Risk (90+ days)")
    ]
    
    all_dormant_by_threshold = {}
    
    for days, label in thresholds:
        print(f"\n{label}")
        print("-" * 80)
        
        dormant = detect_dormant(collaboration_scores, threshold_days=days, min_score=20.0)
        all_dormant_by_threshold[days] = dormant
        
        # Filter to show only this range
        if days == 30:
            range_dormant = [d for d in dormant if d['days_since_last_interaction'] < 60]
        elif days == 60:
            range_dormant = [d for d in dormant if 60 <= d['days_since_last_interaction'] < 90]
        else:  # 90+
            range_dormant = [d for d in dormant if d['days_since_last_interaction'] >= 90]
        
        if not range_dormant:
            print(f"✅ No collaborators in this range")
            continue
        
        # Display
        for i, person in enumerate(range_dormant[:10], 1):  # Top 10 per range
            print(f"\n{i}. {person['name']}")
            print(f"   📊 Historical: {person['historical_score']:.0f} pts | "
                  f"Current: {person['final_score']:.0f} pts")
            print(f"   ⏰ Inactive: {person['days_since_last_interaction']} days "
                  f"(last: {person['last_interaction_date']})")
            
            # History
            history = []
            if person['total_meetings'] > 0:
                history.append(f"{person['total_meetings']} meetings")
                if person['one_on_one'] > 0:
                    history.append(f"{person['one_on_one']} were 1:1")
            if person['total_chats'] > 0:
                history.append(f"{person['total_chats']} chats")
            
            print(f"   📝 History: {', '.join(history)}")
            
            # Last dates
            if person['last_meeting_date'] != 'N/A':
                print(f"   🗓️  Last meeting: {person['last_meeting_date']}")
            if person['last_chat_date'] != 'N/A':
                print(f"   💬 Last chat: {person['last_chat_date']}")
            
            if person.get('job_title') and person['job_title'] != 'N/A':
                print(f"   💼 {person['job_title']}")
            
            # Action
            print(f"   💡 {suggest_action(person)}")
    
    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    
    recent = [d for d in all_dormant_by_threshold.get(30, []) 
              if d['days_since_last_interaction'] < 60]
    medium = [d for d in all_dormant_by_threshold.get(60, []) 
              if 60 <= d['days_since_last_interaction'] < 90]
    high_risk = [d for d in all_dormant_by_threshold.get(90, []) 
                 if d['days_since_last_interaction'] >= 90]
    
    print(f"\n⚡ Recently Inactive (30-59 days): {len(recent)}")
    print(f"⚠️  Dormant (60-89 days): {len(medium)}")
    print(f"🚨 High Risk (90+ days): {len(high_risk)}")
    print()
    
    total = len(recent) + len(medium) + len(high_risk)
    if total > 0:
        print(f"📊 Total dormant relationships needing attention: {total}")
        print()
        print("RECOMMENDED ACTIONS:")
        if high_risk:
            print(f"  🚨 {len(high_risk)} high-risk: Schedule immediate 1:1 meetings")
        if medium:
            print(f"  ⚠️  {len(medium)} dormant: Send reconnection emails/messages")
        if recent:
            print(f"  ⚡ {len(recent)} cooling: Touch base before they go fully dormant")
    else:
        print("✅ No dormant collaborators detected - all relationships active!")

if __name__ == "__main__":
    main()
