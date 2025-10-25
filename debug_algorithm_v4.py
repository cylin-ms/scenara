#!/usr/bin/env python3
"""
Debug Enhanced Algorithm v4.0
Check why no collaborators are being identified and adjust thresholds
"""

import json
from collections import defaultdict
from datetime import datetime

def debug_algorithm_v4():
    """Debug the enhanced algorithm to see why no collaborators found"""
    
    print("🔍 DEBUGGING ENHANCED ALGORITHM V4.0")
    print("=" * 50)
    
    # Load calendar data
    with open('meeting_prep_data/real_calendar_scenarios.json', 'r') as f:
        calendar_data = json.load(f)
    
    collaboration_scores = defaultdict(lambda: {
        'total_meetings': 0,
        'one_on_one_meetings': 0,
        'small_meetings': 0,
        'organized_by_me': 0,
        'i_attended_their_meetings': 0,
        'subjects': []
    })
    
    print(f"📊 Processing {len(calendar_data)} calendar events...")
    
    # Simplified processing to debug
    for event in calendar_data:
        attendees = event['context'].get('attendees', [])
        attendee_count = len(attendees)
        organizer = event['context'].get('organizer', 'Unknown')
        is_my_meeting = organizer == 'Chin-Yew Lin'
        subject = event['context'].get('subject', '').lower()
        
        for attendee in attendees:
            if attendee != 'Chin-Yew Lin':
                data = collaboration_scores[attendee]
                data['total_meetings'] += 1
                data['subjects'].append(subject)
                
                if attendee_count == 2:
                    data['one_on_one_meetings'] += 1
                elif attendee_count <= 10:
                    data['small_meetings'] += 1
                
                if is_my_meeting:
                    data['organized_by_me'] += 1
                if organizer == attendee:
                    data['i_attended_their_meetings'] += 1
    
    print(f"\n📋 COLLABORATION ANALYSIS:")
    
    candidates = []
    for person, data in collaboration_scores.items():
        if data['total_meetings'] >= 2:
            
            # Check evidence criteria
            has_strong_evidence = (
                data['one_on_one_meetings'] > 0 or
                data['organized_by_me'] > 0 or
                data['i_attended_their_meetings'] > 0 or
                (data['small_meetings'] >= 3)
            )
            
            # System account check
            system_indicators = ['rob', 'fte', 'extended', 'holiday', 'event']
            is_system = any(indicator in person.lower() for indicator in system_indicators)
            
            # Simple score
            score = (
                data['one_on_one_meetings'] * 25 +
                data['organized_by_me'] * 18 +
                data['i_attended_their_meetings'] * 12 +
                data['small_meetings'] * 6
            )
            
            candidate = {
                'name': person,
                'score': score,
                'meetings': data['total_meetings'],
                'one_on_one': data['one_on_one_meetings'],
                'organized': data['organized_by_me'],
                'attended_their': data['i_attended_their_meetings'],
                'small': data['small_meetings'],
                'has_evidence': has_strong_evidence,
                'is_system': is_system
            }
            
            candidates.append(candidate)
    
    # Sort by score
    candidates.sort(key=lambda x: x['score'], reverse=True)
    
    print(f"\n🎯 TOP CANDIDATES (including filtered ones):")
    print("-" * 60)
    
    for i, candidate in enumerate(candidates[:10], 1):
        status = "✅" if candidate['has_evidence'] and not candidate['is_system'] and candidate['score'] > 15 else "❌"
        reason = []
        
        if not candidate['has_evidence']:
            reason.append("no evidence")
        if candidate['is_system']:
            reason.append("system account")
        if candidate['score'] <= 15:
            reason.append("low score")
        
        reason_str = f" ({', '.join(reason)})" if reason else ""
        
        print(f"{i:2d}. {status} {candidate['name']} - Score: {candidate['score']}")
        print(f"       Evidence: {candidate['one_on_one']} 1:1, {candidate['organized']} org, {candidate['attended_their']} attend")
        print(f"       Meetings: {candidate['meetings']} total, {candidate['small']} small")
        if reason_str:
            print(f"       Filter: {reason_str}")
        print()
    
    print(f"\n💡 DIAGNOSIS:")
    total_with_evidence = sum(1 for c in candidates if c['has_evidence'])
    total_non_system = sum(1 for c in candidates if not c['is_system'])
    total_good_score = sum(1 for c in candidates if c['score'] > 15)
    
    print(f"   📊 {len(candidates)} total candidates")
    print(f"   🤝 {total_with_evidence} with evidence")
    print(f"   👤 {total_non_system} non-system accounts")
    print(f"   📈 {total_good_score} with score > 15")
    
    # Check specific thresholds
    print(f"\n🔧 THRESHOLD ANALYSIS:")
    score_thresholds = [5, 10, 15, 20, 25]
    for threshold in score_thresholds:
        count = sum(1 for c in candidates if c['score'] > threshold and c['has_evidence'] and not c['is_system'])
        print(f"   Score > {threshold}: {count} candidates")

if __name__ == "__main__":
    debug_algorithm_v4()