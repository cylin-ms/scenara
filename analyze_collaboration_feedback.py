#!/usr/bin/env python3
"""
Analyze the remaining algorithm problems with specific people
"""

import json
from collections import defaultdict

def analyze_specific_collaborators():
    """Analyze the specific people mentioned by the user"""
    
    try:
        with open('meeting_prep_data/real_calendar_scenarios.json', 'r') as f:
            calendar_data = json.load(f)
    except Exception as e:
        print(f"Error loading calendar data: {e}")
        return
    
    print("🔍 SPECIFIC COLLABORATOR ANALYSIS")
    print("=" * 60)
    
    # People to analyze
    people_to_analyze = [
        "Balaji Shyamkumar",  # User says: good connection (was removed)
        "Xintao Ren",        # User says: good connection (was removed)  
        "Charlie Chung",     # User says: good connection (was removed)
        "Bing ROB",          # User says: not a connection (was added)
        "Kun Wu Extended - FTE"  # User says: not a connection (was added)
    ]
    
    for person in people_to_analyze:
        print(f"\n👤 ANALYZING: {person}")
        print("-" * 40)
        
        meetings_with_person = []
        
        for event in calendar_data:
            attendees = event['context'].get('attendees', [])
            if person in attendees:
                meeting_info = {
                    'id': event.get('id'),
                    'subject': event['context'].get('subject', 'No subject'),
                    'attendee_count': len(attendees),
                    'organizer': event['context'].get('organizer', 'Unknown'),
                    'is_chin_yew_organizer': event['context'].get('organizer') == 'Chin-Yew Lin',
                    'is_their_meeting': event['context'].get('organizer') == person,
                    'start_time': event['context'].get('start_time', '')[:10]
                }
                meetings_with_person.append(meeting_info)
        
        if not meetings_with_person:
            print("   ❌ No meetings found")
            continue
            
        # Calculate metrics
        total_meetings = len(meetings_with_person)
        small_meetings = [m for m in meetings_with_person if m['attendee_count'] <= 10]
        medium_meetings = [m for m in meetings_with_person if 10 < m['attendee_count'] <= 50]
        large_meetings = [m for m in meetings_with_person if m['attendee_count'] > 50]
        organized_by_you = [m for m in meetings_with_person if m['is_chin_yew_organizer']]
        organized_by_them = [m for m in meetings_with_person if m['is_their_meeting']]
        avg_size = sum(m['attendee_count'] for m in meetings_with_person) / total_meetings
        
        print(f"   📊 Total meetings: {total_meetings}")
        print(f"   🟢 Small (≤10): {len(small_meetings)}")
        print(f"   🟡 Medium (11-50): {len(medium_meetings)}")
        print(f"   🔴 Large (>50): {len(large_meetings)}")
        print(f"   👤 You organized: {len(organized_by_you)}")
        print(f"   👥 They organized: {len(organized_by_them)}")
        print(f"   📏 Average size: {avg_size:.1f}")
        
        # Show meeting details
        print(f"   📋 Meeting breakdown:")
        for i, meeting in enumerate(meetings_with_person, 1):
            size_emoji = "🟢" if meeting['attendee_count'] <= 10 else "🟡" if meeting['attendee_count'] <= 50 else "🔴"
            org_emoji = "👤" if meeting['is_chin_yew_organizer'] else "👥" if meeting['is_their_meeting'] else "🏢"
            print(f"      {i:2d}. {size_emoji} {org_emoji} ({meeting['attendee_count']:3d}) {meeting['subject'][:40]}...")
    
    return people_to_analyze

def create_hybrid_algorithm():
    """Create a hybrid algorithm that considers both patterns and user feedback"""
    
    print("\n" + "=" * 60)
    print("🔧 HYBRID COLLABORATION ALGORITHM")
    print("=" * 60)
    
    print("""
    🎯 PROBLEMS WITH CURRENT ALGORITHMS:
    
    OLD ALGORITHM (Simple Frequency):
    ❌ Included strangers from large meetings (Yanchao Li)
    ✅ Correctly identified some genuine collaborators (Balaji, Xintao, Charlie)
    
    NEW ALGORITHM (Small Meeting Focus):
    ✅ Removed strangers from large meetings  
    ❌ Removed genuine collaborators who appear in medium/large meetings
    ❌ Added system accounts and automatic meeting participants
    
    🎯 HYBRID SOLUTION:
    
    1. START with small meeting analysis (genuine collaboration signal)
    2. ADD back people who have meaningful interaction patterns:
       - Multiple meetings across different time periods
       - Mix of meeting sizes (not just large events)
       - Professional relationship indicators
    3. FILTER OUT system accounts and automatic participants:
       - Names ending in "ROB", "- FTE", etc.
       - Organizers of holiday/system meetings
       - People who only appear in automated meetings
    
    4. WEIGHT FACTORS:
       - Small meetings (≤10): +5 points each
       - Medium meetings (11-50): +2 points each  
       - Large meetings (>50): +0.5 points each
       - You organized: +10 bonus
       - They organized: +5 bonus
       - Multiple time periods: +5 bonus
       - Professional name format: +3 bonus
       - System account indicators: -20 penalty
    """)

def generate_improved_hybrid_code():
    """Generate the improved hybrid algorithm"""
    
    print("\n🔧 HYBRID ALGORITHM CODE:")
    print("=" * 60)
    
    code = '''
def analyze_hybrid_collaborators(self):
    """Hybrid algorithm combining pattern analysis with relationship validation"""
    
    collaboration_scores = defaultdict(lambda: {
        'total_meetings': 0,
        'small_meetings': 0,
        'medium_meetings': 0,
        'large_meetings': 0,
        'organized_by_me': 0,
        'i_attended_their_meetings': 0,
        'meeting_sizes': [],
        'time_periods': set(),
        'subjects': []
    })
    
    for event in self.calendar_data:
        attendees = event['context'].get('attendees', [])
        attendee_count = len(attendees)
        organizer = event['context'].get('organizer', 'Unknown')
        is_my_meeting = organizer == 'Chin-Yew Lin'
        start_time = event['context'].get('start_time', '')
        time_period = start_time[:7] if start_time else 'unknown'  # YYYY-MM
        subject = event['context'].get('subject', '').lower()
        
        for attendee in attendees:
            if attendee != 'Chin-Yew Lin':
                data = collaboration_scores[attendee]
                data['total_meetings'] += 1
                data['meeting_sizes'].append(attendee_count)
                data['time_periods'].add(time_period)
                data['subjects'].append(subject)
                
                # Categorize by meeting size
                if attendee_count <= 10:
                    data['small_meetings'] += 1
                elif attendee_count <= 50:
                    data['medium_meetings'] += 1
                else:
                    data['large_meetings'] += 1
                
                # Track meeting organization
                if is_my_meeting:
                    data['organized_by_me'] += 1
                if organizer == attendee:
                    data['i_attended_their_meetings'] += 1
    
    # Score and filter collaborators
    real_collaborators = []
    
    for person, data in collaboration_scores.items():
        if data['total_meetings'] >= 2:
            
            # Calculate base collaboration score
            score = 0
            score += data['small_meetings'] * 5      # Small meetings highly weighted
            score += data['medium_meetings'] * 2     # Medium meetings moderately weighted  
            score += data['large_meetings'] * 0.5    # Large meetings low weight
            score += data['organized_by_me'] * 10    # Meetings you organized
            score += data['i_attended_their_meetings'] * 5  # Their meetings
            score += len(data['time_periods']) * 2   # Multiple time periods
            
            # Professional relationship indicators
            if len(data['time_periods']) > 1:
                score += 5  # Ongoing relationship across time
            
            # System account and automation penalties
            system_indicators = [
                'rob', 'fte', 'extended', 'community', 'team', 'group',
                'holiday', 'event', 'auto', 'system'
            ]
            
            is_system_account = any(indicator in person.lower() for indicator in system_indicators)
            
            # Check if mostly automated meetings
            holiday_meetings = sum(1 for subj in data['subjects'] if 'holiday' in subj)
            automated_ratio = holiday_meetings / len(data['subjects']) if data['subjects'] else 0
            
            if is_system_account:
                score -= 20
            if automated_ratio > 0.5:
                score -= 10
            
            # Minimum viable relationship threshold
            viable_relationship = (
                data['small_meetings'] >= 2 or           # Multiple small meetings
                data['organized_by_me'] > 0 or           # You organized together
                data['i_attended_their_meetings'] > 0 or # You attended their meetings
                (data['medium_meetings'] >= 3 and len(data['time_periods']) > 1)  # Ongoing medium meetings
            )
            
            if viable_relationship and score > 5 and not is_system_account:
                real_collaborators.append({
                    'name': person,
                    'score': score,
                    'small_meetings': data['small_meetings'],
                    'medium_meetings': data['medium_meetings'],
                    'large_meetings': data['large_meetings'],
                    'organized_by_me': data['organized_by_me'],
                    'time_periods': len(data['time_periods']),
                    'is_system': is_system_account,
                    'automated_ratio': automated_ratio
                })
    
    # Sort by score and return top collaborators
    real_collaborators.sort(key=lambda x: x['score'], reverse=True)
    return real_collaborators[:5]
'''
    
    print(code)

def main():
    """Main analysis function"""
    analyze_specific_collaborators()
    create_hybrid_algorithm()
    generate_improved_hybrid_code()

if __name__ == "__main__":
    main()