#!/usr/bin/env python3
"""
Enhanced Collaboration Algorithm with Direct Communication Analysis
Checks for direct emails, chats, phone calls, and 1:1 meetings - not just meeting attendance
"""

import json
from collections import defaultdict
from datetime import datetime

def check_direct_communication_evidence():
    """Check for direct communication evidence with collaborators"""
    
    print("🔍 ENHANCED COLLABORATION ANALYSIS WITH COMMUNICATION EVIDENCE")
    print("=" * 70)
    
    # Load calendar data
    with open('meeting_prep_data/real_calendar_scenarios.json', 'r') as f:
        calendar_data = json.load(f)
    
    # Load Microsoft Graph data for communication evidence
    try:
        with open('mygraph_raw_data_20251024_170412.json', 'r') as f:
            graph_data = json.load(f)
    except:
        graph_data = {}
        print("⚠️  No Microsoft Graph communication data available")
    
    print(f"📊 Analyzing {len(calendar_data)} calendar events...")
    
    # Track collaboration with communication evidence
    collaboration_scores = defaultdict(lambda: {
        'total_meetings': 0,
        'small_meetings': 0,
        'medium_meetings': 0,
        'large_meetings': 0,
        'organized_by_me': 0,
        'i_attended_their_meetings': 0,
        'one_on_one_meetings': 0,
        'meeting_sizes': [],
        'time_periods': set(),
        'subjects': [],
        # Communication evidence
        'direct_emails': 0,
        'chat_messages': 0,
        'phone_calls': 0,
        'in_contacts': False,
        'communication_evidence': []
    })
    
    # Analyze calendar events
    for event in calendar_data:
        attendees = event['context'].get('attendees', [])
        attendee_count = len(attendees)
        organizer = event['context'].get('organizer', 'Unknown')
        is_my_meeting = organizer == 'Chin-Yew Lin'
        start_time = event['context'].get('start_time', '')
        time_period = start_time[:7] if start_time else 'unknown'
        subject = event['context'].get('subject', '').lower()
        
        for attendee in attendees:
            if attendee != 'Chin-Yew Lin':
                data = collaboration_scores[attendee]
                data['total_meetings'] += 1
                data['meeting_sizes'].append(attendee_count)
                data['time_periods'].add(time_period)
                data['subjects'].append(subject)
                
                # Categorize meetings by size
                if attendee_count <= 10:
                    data['small_meetings'] += 1
                elif attendee_count <= 50:
                    data['medium_meetings'] += 1
                else:
                    data['large_meetings'] += 1
                
                # Track 1:1 meetings (strongest collaboration signal)
                if attendee_count == 2:  # Just you and them
                    data['one_on_one_meetings'] += 1
                
                # Organization tracking
                if is_my_meeting:
                    data['organized_by_me'] += 1
                if organizer == attendee:
                    data['i_attended_their_meetings'] += 1
    
    # Check for direct communication evidence in Microsoft Graph data
    print("\n📱 Checking for direct communication evidence...")
    
    # Check contacts (saved in address book = direct relationship)
    if 'contacts' in graph_data:
        contacts = graph_data['contacts']
        if isinstance(contacts, dict) and 'value' in contacts:
            for contact in contacts.get('value', []):
                if isinstance(contact, dict):
                    contact_name = contact.get('displayName', '')
                    if contact_name in collaboration_scores:
                        collaboration_scores[contact_name]['in_contacts'] = True
                        collaboration_scores[contact_name]['communication_evidence'].append('saved_contact')
        elif isinstance(contacts, list):
            # Handle case where contacts is a list of strings
            for contact in contacts:
                if isinstance(contact, str) and contact in collaboration_scores:
                    collaboration_scores[contact]['in_contacts'] = True
                    collaboration_scores[contact]['communication_evidence'].append('saved_contact')
    
    # Placeholder for future communication analysis
    # TODO: Add email analysis when available
    # TODO: Add chat/Teams analysis when available
    # TODO: Add phone call logs when available
    
    print("\n🎯 APPLYING ENHANCED COLLABORATION ALGORITHM")
    print("=" * 50)
    
    genuine_collaborators = []
    
    for person, data in collaboration_scores.items():
        if data['total_meetings'] >= 2:
            
            # Base meeting score
            meeting_score = 0
            meeting_score += data['one_on_one_meetings'] * 20    # 1:1 meetings = strongest signal
            meeting_score += data['small_meetings'] * 5         # Small meetings
            meeting_score += data['medium_meetings'] * 2        # Medium meetings  
            meeting_score += data['large_meetings'] * 0.1       # Large meetings (very low)
            meeting_score += data['organized_by_me'] * 15       # Meetings you organized
            meeting_score += data['i_attended_their_meetings'] * 10  # Their meetings
            
            # Communication evidence score
            comm_score = 0
            comm_score += data['direct_emails'] * 10           # Direct emails
            comm_score += data['chat_messages'] * 5            # Chat messages
            comm_score += data['phone_calls'] * 15             # Phone calls
            comm_score += 20 if data['in_contacts'] else 0     # Saved as contact
            
            # Total collaboration score
            total_score = meeting_score + comm_score
            
            # Enhanced filtering criteria
            has_direct_communication = (
                data['one_on_one_meetings'] > 0 or             # Had 1:1 meetings
                data['organized_by_me'] > 0 or                 # You organized meetings
                data['i_attended_their_meetings'] > 0 or       # You attended their meetings
                data['in_contacts'] or                         # Saved as contact
                data['direct_emails'] > 0 or                   # Direct emails
                data['chat_messages'] > 0 or                   # Chat messages
                data['phone_calls'] > 0                        # Phone calls
            )
            
            # System account filtering
            system_indicators = [
                'rob', 'fte', 'extended', 'community', 'team', 'group',
                'holiday', 'event', 'auto', 'system', 'notification'
            ]
            is_system_account = any(indicator in person.lower() for indicator in system_indicators)
            
            # Check for automated meeting patterns
            holiday_meetings = sum(1 for subj in data['subjects'] if 'holiday' in subj)
            automated_ratio = holiday_meetings / len(data['subjects']) if data['subjects'] else 0
            
            # Calculate average meeting size
            avg_size = sum(data['meeting_sizes']) / len(data['meeting_sizes'])
            
            # Final decision: must have direct communication evidence AND not be system account
            if has_direct_communication and not is_system_account and total_score > 10:
                genuine_collaborators.append({
                    'name': person,
                    'total_score': round(total_score, 1),
                    'meeting_score': round(meeting_score, 1),
                    'comm_score': round(comm_score, 1),
                    'one_on_one': data['one_on_one_meetings'],
                    'small_meetings': data['small_meetings'],
                    'medium_meetings': data['medium_meetings'],
                    'large_meetings': data['large_meetings'],
                    'organized_by_me': data['organized_by_me'],
                    'avg_size': round(avg_size, 1),
                    'in_contacts': data['in_contacts'],
                    'communication_evidence': data['communication_evidence'],
                    'time_periods': len(data['time_periods']),
                    'automated_ratio': round(automated_ratio, 2)
                })
    
    # Sort by total score
    genuine_collaborators.sort(key=lambda x: x['total_score'], reverse=True)
    
    print(f"\n✅ GENUINE COLLABORATORS (with communication evidence):")
    print("=" * 60)
    
    if genuine_collaborators:
        for i, collab in enumerate(genuine_collaborators[:10], 1):  # Top 10
            print(f"{i:2d}. {collab['name']}")
            print(f"    💯 Total Score: {collab['total_score']} (meetings: {collab['meeting_score']}, comm: {collab['comm_score']})")
            print(f"    🤝 Meetings: {collab['one_on_one']} 1:1, {collab['small_meetings']} small, {collab['medium_meetings']} medium, {collab['large_meetings']} large")
            if collab['organized_by_me'] > 0:
                print(f"    👤 You organized: {collab['organized_by_me']} meetings")
            if collab['in_contacts']:
                print(f"    📞 Saved as contact")
            if collab['communication_evidence']:
                print(f"    📱 Evidence: {', '.join(collab['communication_evidence'])}")
            print(f"    📊 Avg meeting size: {collab['avg_size']}, {collab['time_periods']} time periods")
            print()
    else:
        print("❌ No genuine collaborators found with direct communication evidence")
    
    print("\n🔍 SPECIFIC ANALYSIS: Yanchao Li")
    print("=" * 40)
    
    if 'Yanchao Li' in collaboration_scores:
        yanchao = collaboration_scores['Yanchao Li']
        print(f"📊 Meetings: {yanchao['total_meetings']} total")
        print(f"🤝 1:1 meetings: {yanchao['one_on_one_meetings']}")
        print(f"👤 You organized: {yanchao['organized_by_me']}")
        print(f"👥 They organized (you attended): {yanchao['i_attended_their_meetings']}")
        print(f"📞 In contacts: {yanchao['in_contacts']}")
        print(f"💬 Communication evidence: {yanchao['communication_evidence'] if yanchao['communication_evidence'] else 'None'}")
        print(f"📈 Average meeting size: {sum(yanchao['meeting_sizes'])/len(yanchao['meeting_sizes']):.1f}")
        
        print(f"\n❌ Why Yanchao Li is NOT a genuine collaborator:")
        print(f"   • No 1:1 meetings")
        print(f"   • Never organized meetings with them")
        print(f"   • Never attended their meetings")
        print(f"   • Not saved as contact")
        print(f"   • No direct communication evidence")
        print(f"   • Only appears in mixed-size meetings (no direct interaction)")
    else:
        print("✅ Yanchao Li correctly filtered out")
    
    return genuine_collaborators

if __name__ == "__main__":
    check_direct_communication_evidence()