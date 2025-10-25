#!/usr/bin/env python3
"""
Improved Collaborator Analysis - Remove False Positives
Detect and fix the problem of identifying strangers as frequent collaborators
"""

import json
from collections import Counter, defaultdict

def analyze_collaboration_problem():
    """Analyze the current problem and propose solutions"""
    
    # Load the real calendar data
    try:
        with open('meeting_prep_data/real_calendar_scenarios.json', 'r') as f:
            calendar_data = json.load(f)
    except Exception as e:
        print(f"Error loading calendar data: {e}")
        return
    
    print("🚨 COLLABORATION ANALYSIS PROBLEM DETECTION")
    print("=" * 60)
    
    # Analyze Yanchao Li's meeting patterns
    meetings_with_yanchao = []
    yanchao_meeting_sizes = []
    
    for event in calendar_data:
        attendees = event['context'].get('attendees', [])
        if 'Yanchao Li' in attendees:
            meeting_info = {
                'id': event.get('id'),
                'subject': event['context'].get('subject', 'No subject'),
                'attendee_count': len(attendees),
                'organizer': event['context'].get('organizer', 'Unknown'),
                'is_chin_yew_organizer': event['context'].get('organizer') == 'Chin-Yew Lin'
            }
            meetings_with_yanchao.append(meeting_info)
            yanchao_meeting_sizes.append(len(attendees))
    
    print(f"📊 Yanchao Li appears in {len(meetings_with_yanchao)} meetings")
    print(f"📈 Average meeting size: {sum(yanchao_meeting_sizes)/len(yanchao_meeting_sizes):.1f} attendees")
    print(f"📏 Meeting size range: {min(yanchao_meeting_sizes)} - {max(yanchao_meeting_sizes)} attendees")
    
    # Categorize meetings by size
    small_meetings = [m for m in meetings_with_yanchao if m['attendee_count'] <= 10]
    medium_meetings = [m for m in meetings_with_yanchao if 10 < m['attendee_count'] <= 50]
    large_meetings = [m for m in meetings_with_yanchao if m['attendee_count'] > 50]
    
    print(f"\n🔍 MEETING SIZE BREAKDOWN:")
    print(f"   🟢 Small meetings (≤10 people): {len(small_meetings)}")
    print(f"   🟡 Medium meetings (11-50 people): {len(medium_meetings)}")
    print(f"   🔴 Large meetings (>50 people): {len(large_meetings)}")
    
    print(f"\n🚨 PROBLEM IDENTIFIED:")
    print(f"   • {len(large_meetings)}/{len(meetings_with_yanchao)} meetings with Yanchao Li are LARGE (>50 people)")
    print(f"   • {len(small_meetings)}/{len(meetings_with_yanchao)} meetings are actually small/personal")
    print(f"   • You never organized meetings with Yanchao Li")
    
    # Analyze if you actually interact with Yanchao Li
    chin_yew_organized = [m for m in meetings_with_yanchao if m['is_chin_yew_organizer']]
    print(f"   • Meetings YOU organized with Yanchao Li: {len(chin_yew_organized)}")
    
    print(f"\n📋 DETAILED ANALYSIS:")
    for i, meeting in enumerate(meetings_with_yanchao, 1):
        size_category = "🔴 LARGE" if meeting['attendee_count'] > 50 else "🟡 MEDIUM" if meeting['attendee_count'] > 10 else "🟢 SMALL"
        organizer_note = "👤 YOU" if meeting['is_chin_yew_organizer'] else f"👥 {meeting['organizer']}"
        print(f"   {i:2d}. {size_category} ({meeting['attendee_count']:3d} people) | {organizer_note}")
        print(f"       📋 {meeting['subject'][:60]}...")
    
    return meetings_with_yanchao

def improved_collaborator_algorithm():
    """Implement improved algorithm to identify real collaborators"""
    
    try:
        with open('meeting_prep_data/real_calendar_scenarios.json', 'r') as f:
            calendar_data = json.load(f)
    except Exception as e:
        print(f"Error loading calendar data: {e}")
        return
    
    print("\n" + "=" * 60)
    print("🔧 IMPROVED COLLABORATOR DETECTION ALGORITHM")
    print("=" * 60)
    
    # New algorithm with multiple filters
    collaboration_scores = defaultdict(lambda: {
        'total_meetings': 0,
        'small_meetings': 0,
        'organized_by_me': 0,
        'i_attended_their_meetings': 0,
        'average_meeting_size': 0,
        'meeting_sizes': []
    })
    
    for event in calendar_data:
        attendees = event['context'].get('attendees', [])
        attendee_count = len(attendees)
        organizer = event['context'].get('organizer', 'Unknown')
        is_my_meeting = organizer == 'Chin-Yew Lin'
        
        for attendee in attendees:
            if attendee != 'Chin-Yew Lin':  # Exclude yourself
                collaboration_scores[attendee]['total_meetings'] += 1
                collaboration_scores[attendee]['meeting_sizes'].append(attendee_count)
                
                # Weight small meetings more heavily
                if attendee_count <= 10:
                    collaboration_scores[attendee]['small_meetings'] += 1
                
                # Track meetings you organized
                if is_my_meeting:
                    collaboration_scores[attendee]['organized_by_me'] += 1
                
                # Track meetings they organized that you attended
                if organizer == attendee:
                    collaboration_scores[attendee]['i_attended_their_meetings'] += 1
    
    # Calculate average meeting sizes and collaboration scores
    filtered_collaborators = []
    
    print("🎯 COLLABORATION SCORING CRITERIA:")
    print("   1. Small meetings (≤10 people) weighted 3x")
    print("   2. Meetings you organized with them: +10 bonus")
    print("   3. Their meetings you attended: +5 bonus")
    print("   4. Average meeting size penalty: -1 point per 10 people")
    print("   5. Minimum 2 total meetings to qualify")
    
    print(f"\n📊 DETAILED SCORING ANALYSIS:")
    
    for person, data in collaboration_scores.items():
        if data['total_meetings'] >= 2:  # Minimum threshold
            # Calculate average meeting size
            avg_size = sum(data['meeting_sizes']) / len(data['meeting_sizes'])
            data['average_meeting_size'] = avg_size
            
            # Calculate collaboration score
            score = 0
            score += data['small_meetings'] * 3  # Small meetings are worth more
            score += data['organized_by_me'] * 10  # Meetings you organized
            score += data['i_attended_their_meetings'] * 5  # Their meetings you attended
            score -= avg_size / 10  # Penalty for large average meeting size
            
            # Additional filters
            real_interaction = (
                data['organized_by_me'] > 0 or  # You organized meetings with them
                data['i_attended_their_meetings'] > 0 or  # You attended their meetings
                data['small_meetings'] >= 2 or  # Multiple small meetings
                avg_size <= 15  # Generally small meetings
            )
            
            filtered_collaborators.append({
                'name': person,
                'score': score,
                'total_meetings': data['total_meetings'],
                'small_meetings': data['small_meetings'],
                'organized_by_me': data['organized_by_me'],
                'their_meetings': data['i_attended_their_meetings'],
                'avg_meeting_size': avg_size,
                'real_interaction': real_interaction
            })
    
    # Sort by score
    filtered_collaborators.sort(key=lambda x: x['score'], reverse=True)
    
    print(f"📋 TOP 15 COLLABORATION ANALYSIS:")
    for i, collab in enumerate(filtered_collaborators[:15], 1):
        real_flag = "✅ REAL" if collab['real_interaction'] else "❌ FALSE"
        print(f"{i:2d}. {real_flag} | {collab['name'][:25]:25} | Score: {collab['score']:6.1f}")
        print(f"     📊 {collab['total_meetings']} total, {collab['small_meetings']} small, "
              f"{collab['organized_by_me']} you→them, {collab['their_meetings']} them→you, "
              f"avg_size: {collab['avg_meeting_size']:.1f}")
    
    # Filter to only real collaborators
    real_collaborators = [c for c in filtered_collaborators if c['real_interaction']]
    
    print(f"\n✅ REAL COLLABORATORS (Top 5):")
    for i, collab in enumerate(real_collaborators[:5], 1):
        print(f"   {i}. {collab['name']} (Score: {collab['score']:.1f})")
    
    print(f"\n❌ REMOVED FALSE POSITIVES:")
    false_positives = [c for c in filtered_collaborators[:10] if not c['real_interaction']]
    for collab in false_positives:
        print(f"   • {collab['name']} (avg meeting size: {collab['avg_meeting_size']:.0f} people)")
    
    return real_collaborators[:5]

def generate_improved_algorithm_code():
    """Generate the improved algorithm code for integration"""
    
    print(f"\n🔧 IMPROVED ALGORITHM CODE:")
    print("=" * 60)
    
    code = '''
def analyze_real_collaborators(self):
    """Improved algorithm to identify genuine collaborators, not just meeting attendees"""
    if not self.calendar_data:
        return
        
    print("🤝 Analyzing real collaboration patterns...")
    
    collaboration_scores = defaultdict(lambda: {
        'total_meetings': 0,
        'small_meetings': 0,
        'organized_by_me': 0,
        'i_attended_their_meetings': 0,
        'meeting_sizes': []
    })
    
    for event in self.calendar_data:
        attendees = event['context'].get('attendees', [])
        attendee_count = len(attendees)
        organizer = event['context'].get('organizer', 'Unknown')
        is_my_meeting = organizer == 'Chin-Yew Lin'
        
        for attendee in attendees:
            if attendee != 'Chin-Yew Lin':  # Exclude yourself
                collaboration_scores[attendee]['total_meetings'] += 1
                collaboration_scores[attendee]['meeting_sizes'].append(attendee_count)
                
                # Track small meetings (real collaboration)
                if attendee_count <= 10:
                    collaboration_scores[attendee]['small_meetings'] += 1
                
                # Track meetings you organized (real interaction)
                if is_my_meeting:
                    collaboration_scores[attendee]['organized_by_me'] += 1
                
                # Track their meetings you attended (mutual interest)
                if organizer == attendee:
                    collaboration_scores[attendee]['i_attended_their_meetings'] += 1
    
    # Filter and score real collaborators
    real_collaborators = []
    
    for person, data in collaboration_scores.items():
        if data['total_meetings'] >= 2:  # Minimum threshold
            avg_size = sum(data['meeting_sizes']) / len(data['meeting_sizes'])
            
            # Calculate collaboration score
            score = 0
            score += data['small_meetings'] * 3  # Small meetings weighted heavily
            score += data['organized_by_me'] * 10  # Your meetings = real interaction
            score += data['i_attended_their_meetings'] * 5  # Their meetings = mutual interest
            score -= avg_size / 10  # Penalty for large average meeting size
            
            # Filter criteria for real collaboration
            real_interaction = (
                data['organized_by_me'] > 0 or  # You organized meetings with them
                data['i_attended_their_meetings'] > 0 or  # You attended their meetings  
                data['small_meetings'] >= 2 or  # Multiple small meetings
                avg_size <= 15  # Generally small meetings
            )
            
            if real_interaction:
                real_collaborators.append({
                    'name': person,
                    'score': score,
                    'small_meetings': data['small_meetings'],
                    'organized_by_me': data['organized_by_me'],
                    'avg_meeting_size': avg_size
                })
    
    # Sort by score and take top 5
    real_collaborators.sort(key=lambda x: x['score'], reverse=True)
    top_collaborators = real_collaborators[:5]
    
    if top_collaborators:
        collab_names = [c['name'] for c in top_collaborators]
        self.me_notes.append({
            'category': 'COLLABORATION',
            'title': 'Genuine Meeting Collaborators',
            'note': f'Real collaboration patterns identified: {", ".join(collab_names)}',
            'confidence': 0.95,
            'source': 'improved_collaboration_analysis',
            'timestamp': self.timestamp,
            'algorithm_notes': 'Filtered out large meeting false positives'
        })
'''
    
    print(code)
    return code

def main():
    """Main analysis function"""
    # Detect the problem
    meetings_with_yanchao = analyze_collaboration_problem()
    
    # Run improved algorithm
    real_collaborators = improved_collaborator_algorithm()
    
    # Generate code for integration
    generate_improved_algorithm_code()
    
    print(f"\n🎯 SUMMARY:")
    print(f"   • Problem: Large company meetings creating false 'frequent collaborators'")
    print(f"   • Solution: Weight small meetings, track mutual organization, filter by interaction")
    print(f"   • Result: More accurate identification of genuine work relationships")

if __name__ == "__main__":
    main()