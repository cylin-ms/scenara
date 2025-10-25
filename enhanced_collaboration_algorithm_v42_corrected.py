#!/usr/bin/env python3
"""
Enhanced Collaboration Algorithm v4.2 - Enterprise Taxonomy Integration
Scenara 2.0 - Meeting Intelligence System

CRITICAL CORRECTION: Jason Virtue false positive identified
- All meetings are Informational/Broadcast type (low collaboration value)
- Invited via email list (EventsOnly_AIML-CC), not personal invitation
- No genuine collaboration evidence according to Enterprise Meeting Taxonomy

This version integrates the Enterprise Meeting Taxonomy to properly
distinguish between genuine collaboration and information consumption.
"""

import json
from datetime import datetime, timedelta
from collections import defaultdict

def analyze_collaboration_with_taxonomy(calendar_data):
    """
    Enhanced collaboration analysis using Enterprise Meeting Taxonomy
    to distinguish genuine collaboration from information consumption
    """
    
    print("🔬 Enhanced Collaboration Algorithm v4.2 (Enterprise Taxonomy)")
    print("=" * 70)
    
    collaboration_scores = defaultdict(lambda: {
        'total_meetings': 0,
        'genuine_collaboration_meetings': 0,
        'informational_meetings': 0,
        'broadcast_meetings': 0,
        'one_on_one_meetings': 0,
        'small_working_meetings': 0,
        'organized_by_me': 0,
        'i_attended_their_meetings': 0,
        'email_list_meetings': 0,
        'meeting_details': [],
        'time_periods': set(),
        'taxonomy_classifications': [],
        'collaboration_evidence': [],
        'information_consumption_evidence': []
    })
    
    # Enhanced scoring weights based on Enterprise Taxonomy
    taxonomy_weights = {
        # GENUINE COLLABORATION (High weight)
        'one_on_one': 30,
        'organized_by_me': 25,
        'attended_their_working_meetings': 20,
        'small_collaborative_working': 15,
        
        # MODERATE COLLABORATION (Medium weight)
        'small_internal_recurring': 8,
        'planning_decision_meetings': 12,
        
        # INFORMATION CONSUMPTION (Very low weight)
        'informational_briefing': 1,
        'broadcast_webinar': 0.1,
        'training_education': 2,
        
        # EMAIL LIST PENALTY
        'email_list_penalty': -5
    }
    
    # Email list patterns
    email_list_patterns = [
        'EventsOnly', '@service.microsoft.com', 'AllHands', 'Everyone',
        'Distribution', 'DL-', 'Team-All', 'Broadcast'
    ]
    
    # Meeting type classification keywords
    collaboration_keywords = [
        'planning', 'design', 'workshop', 'brainstorm', 'decision',
        'review', 'working', 'sync', 'alignment', 'strategy'
    ]
    
    informational_keywords = [
        'update', 'briefing', 'announcement', 'what\'s new', 'research update',
        'training', 'education', 'demo', 'presentation', 'showcase'
    ]
    
    broadcast_keywords = [
        'all-hands', 'town hall', 'webinar', 'broadcast', 'announcement',
        'launch', 'kickoff', 'intro'
    ]
    
    current_date = datetime.now()
    
    for event in calendar_data:
        attendees = event['context'].get('attendees', [])
        attendee_count = len(attendees)
        organizer = event['context'].get('organizer', 'Unknown')
        is_my_meeting = organizer == 'Chin-Yew Lin'
        start_time = event['context'].get('start_time', '')
        subject = event['context'].get('subject', '').lower()
        
        # Parse meeting date
        try:
            if start_time:
                meeting_date = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
            else:
                meeting_date = current_date - timedelta(days=30)
        except:
            meeting_date = current_date - timedelta(days=30)
        
        time_period = start_time[:7] if start_time else 'unknown'
        
        # Check for email list invitations
        has_email_list = any(
            any(pattern in attendee for pattern in email_list_patterns)
            for attendee in attendees
        )
        
        # Classify meeting type using Enterprise Taxonomy
        def classify_meeting_type(subject, attendee_count, organizer, has_email_list):
            subject_lower = subject.lower()
            
            # 1. Broadcast Meetings (Informational & Broadcast category)
            if attendee_count > 50 or any(keyword in subject_lower for keyword in broadcast_keywords):
                return 'broadcast_webinar', 'Informational & Broadcast - Webinars and Broadcasts'
            
            # 2. Informational Briefings
            if (any(keyword in subject_lower for keyword in informational_keywords) or
                has_email_list):
                return 'informational_briefing', 'Informational & Broadcast - Informational Briefings'
            
            # 3. Training/Education
            if 'research' in subject_lower or 'training' in subject_lower or 'education' in subject_lower:
                return 'training_education', 'Informational & Broadcast - Training & Education Sessions'
            
            # 4. One-on-One (highest collaboration value)
            if attendee_count == 2:
                return 'one_on_one', 'Internal Recurring - One-on-One Meetings'
            
            # 5. Strategic Planning & Decision Meetings
            if any(keyword in subject_lower for keyword in collaboration_keywords):
                if attendee_count <= 10:
                    return 'small_collaborative_working', 'Strategic Planning & Decision - Planning/Workshop Sessions'
                else:
                    return 'planning_decision_meetings', 'Strategic Planning & Decision - Planning Sessions'
            
            # 6. Internal Recurring (Status Updates)
            if attendee_count <= 10:
                return 'small_internal_recurring', 'Internal Recurring - Team Status Update Meetings'
            else:
                return 'informational_briefing', 'Internal Recurring - Progress Review Meetings'
        
        for attendee in attendees:
            if attendee != 'Chin-Yew Lin':
                data = collaboration_scores[attendee]
                
                # Basic tracking
                data['total_meetings'] += 1
                data['time_periods'].add(time_period)
                
                # Classify meeting type
                meeting_type, taxonomy_category = classify_meeting_type(subject, attendee_count, organizer, has_email_list)
                data['taxonomy_classifications'].append(taxonomy_category)
                
                # Track email list meetings
                if has_email_list:
                    data['email_list_meetings'] += 1
                
                # Calculate base meeting score based on taxonomy
                base_meeting_score = 0
                collaboration_evidence = []
                information_evidence = []
                
                if meeting_type == 'one_on_one':
                    data['one_on_one_meetings'] += 1
                    data['genuine_collaboration_meetings'] += 1
                    base_meeting_score = taxonomy_weights['one_on_one']
                    collaboration_evidence.append('1:1 meeting - direct collaboration')
                    
                elif meeting_type == 'small_collaborative_working':
                    data['small_working_meetings'] += 1
                    data['genuine_collaboration_meetings'] += 1
                    base_meeting_score = taxonomy_weights['small_collaborative_working']
                    collaboration_evidence.append('Small collaborative working session')
                    
                elif meeting_type == 'planning_decision_meetings':
                    data['genuine_collaboration_meetings'] += 1
                    base_meeting_score = taxonomy_weights['planning_decision_meetings']
                    collaboration_evidence.append('Planning/decision meeting participation')
                    
                elif meeting_type == 'small_internal_recurring':
                    base_meeting_score = taxonomy_weights['small_internal_recurring']
                    collaboration_evidence.append('Small internal recurring meeting')
                    
                elif meeting_type == 'informational_briefing':
                    data['informational_meetings'] += 1
                    base_meeting_score = taxonomy_weights['informational_briefing']
                    information_evidence.append('Informational briefing attendance')
                    
                elif meeting_type == 'broadcast_webinar':
                    data['broadcast_meetings'] += 1
                    base_meeting_score = taxonomy_weights['broadcast_webinar']
                    information_evidence.append('Broadcast/webinar attendance')
                    
                elif meeting_type == 'training_education':
                    data['informational_meetings'] += 1
                    base_meeting_score = taxonomy_weights['training_education']
                    information_evidence.append('Training/education session attendance')
                
                # Apply email list penalty
                if has_email_list:
                    base_meeting_score += taxonomy_weights['email_list_penalty']
                    information_evidence.append('Email list invitation (bulk invite)')
                
                # Organization tracking (strong collaboration signal)
                if is_my_meeting:
                    data['organized_by_me'] += 1
                    data['genuine_collaboration_meetings'] += 1
                    org_score = taxonomy_weights['organized_by_me']
                    base_meeting_score += org_score
                    collaboration_evidence.append('Meeting you organized together')
                
                if organizer == attendee and meeting_type in ['small_collaborative_working', 'planning_decision_meetings']:
                    data['i_attended_their_meetings'] += 1
                    data['genuine_collaboration_meetings'] += 1
                    attend_score = taxonomy_weights['attended_their_working_meetings']
                    base_meeting_score += attend_score
                    collaboration_evidence.append('Attended their working meeting')
                elif organizer == attendee:
                    # Informational meeting organized by them
                    information_evidence.append('Attended their informational meeting')
                
                # Store evidence
                data['collaboration_evidence'].extend(collaboration_evidence)
                data['information_consumption_evidence'].extend(information_evidence)
                
                # Meeting details for analysis
                meeting_detail = {
                    'date': meeting_date,
                    'size': attendee_count,
                    'subject': subject,
                    'organizer': organizer,
                    'meeting_type': meeting_type,
                    'taxonomy_category': taxonomy_category,
                    'has_email_list': has_email_list,
                    'base_score': base_meeting_score,
                    'collaboration_evidence': collaboration_evidence,
                    'information_evidence': information_evidence
                }
                data['meeting_details'].append(meeting_detail)
    
    # Final filtering and ranking with Enterprise Taxonomy requirements
    genuine_collaborators = []
    
    for person, data in collaboration_scores.items():
        if data['total_meetings'] >= 2:
            
            # ENHANCED EVIDENCE REQUIREMENTS based on Enterprise Taxonomy
            has_genuine_collaboration = (
                data['one_on_one_meetings'] > 0 or
                data['organized_by_me'] > 0 or
                data['small_working_meetings'] > 0 or
                data['genuine_collaboration_meetings'] >= 2
            )
            
            # Calculate collaboration ratio
            total_meetings = data['total_meetings']
            genuine_ratio = data['genuine_collaboration_meetings'] / total_meetings
            informational_ratio = data['informational_meetings'] / total_meetings
            email_list_ratio = data['email_list_meetings'] / total_meetings
            
            # Enhanced system account detection
            system_indicators = [
                'rob', 'fte', 'extended', 'community', 'team', 'group',
                'holiday', 'event', 'auto', 'system', 'notification',
                'bot', 'service', 'admin', 'learning', 'events'
            ]
            
            person_lower = person.lower()
            is_system_account = any(indicator in person_lower for indicator in system_indicators)
            
            # Calculate final score from meeting details
            final_score = sum(detail['base_score'] for detail in data['meeting_details'])
            
            # Calculate confidence level based on collaboration evidence quality
            confidence_factors = 0
            if data['one_on_one_meetings'] > 0:
                confidence_factors += 0.4
            if data['organized_by_me'] > 0:
                confidence_factors += 0.4
            if data['small_working_meetings'] > 0:
                confidence_factors += 0.3
            if genuine_ratio > 0.5:
                confidence_factors += 0.2
            if email_list_ratio < 0.3:  # Less than 30% email list meetings
                confidence_factors += 0.2
            
            confidence = min(confidence_factors, 1.0)
            
            # STRICT FILTERING: Must have genuine collaboration AND low information-only ratio
            if (has_genuine_collaboration and 
                not is_system_account and 
                final_score > 15 and 
                confidence > 0.6 and
                genuine_ratio > 0.3 and  # At least 30% genuine collaboration meetings
                email_list_ratio < 0.7):  # Less than 70% email list meetings
                
                genuine_collaborators.append({
                    'name': person,
                    'final_score': round(final_score, 2),
                    'confidence': round(confidence, 3),
                    'genuine_collaboration_meetings': data['genuine_collaboration_meetings'],
                    'informational_meetings': data['informational_meetings'],
                    'broadcast_meetings': data['broadcast_meetings'],
                    'email_list_meetings': data['email_list_meetings'],
                    'genuine_ratio': round(genuine_ratio, 3),
                    'informational_ratio': round(informational_ratio, 3),
                    'email_list_ratio': round(email_list_ratio, 3),
                    'one_on_one': data['one_on_one_meetings'],
                    'organized_by_me': data['organized_by_me'],
                    'small_working_meetings': data['small_working_meetings'],
                    'time_periods': len(data['time_periods']),
                    'total_meetings': data['total_meetings'],
                    'collaboration_evidence': list(set(data['collaboration_evidence'])),
                    'information_evidence': list(set(data['information_consumption_evidence'])),
                    'algorithm_version': '4.2_enterprise_taxonomy'
                })
    
    # Sort by genuine collaboration quality (not just score)
    genuine_collaborators.sort(key=lambda x: (x['genuine_ratio'], x['final_score']), reverse=True)
    
    return genuine_collaborators

def main():
    """Test the corrected algorithm"""
    
    # Load calendar data
    with open('meeting_prep_data/real_calendar_scenarios.json', 'r') as f:
        calendar_data = json.load(f)
    
    collaborators = analyze_collaboration_with_taxonomy(calendar_data)
    
    print(f"\n🎯 CORRECTED COLLABORATION ANALYSIS RESULTS")
    print("=" * 50)
    print(f"Found {len(collaborators)} genuine collaborators")
    print()
    
    for collab in collaborators:
        print(f"👤 {collab['name']}")
        print(f"   📊 Score: {collab['final_score']} | Confidence: {collab['confidence']:.1%}")
        print(f"   🤝 Genuine Collaboration: {collab['genuine_collaboration_meetings']} meetings ({collab['genuine_ratio']:.1%})")
        print(f"   📋 Information Consumption: {collab['informational_meetings']} meetings ({collab['informational_ratio']:.1%})")
        print(f"   📧 Email List Meetings: {collab['email_list_meetings']} meetings ({collab['email_list_ratio']:.1%})")
        print(f"   ✅ Collaboration Evidence: {', '.join(collab['collaboration_evidence'][:3])}...")
        print()
    
    # Specific check for Jason Virtue
    print("🔍 SPECIFIC CHECK: Jason Virtue")
    print("-" * 35)
    
    # Find Jason Virtue in the data
    jason_found = False
    for event in calendar_data:
        attendees = event['context'].get('attendees', [])
        if 'Jason Virtue' in attendees:
            jason_found = True
            break
    
    if jason_found:
        # Check if Jason made it through the filtering
        jason_in_results = any(collab['name'] == 'Jason Virtue' for collab in collaborators)
        
        if jason_in_results:
            print("❌ ERROR: Jason Virtue still appears as collaborator!")
            jason_data = next(collab for collab in collaborators if collab['name'] == 'Jason Virtue')
            print(f"   Details: {jason_data}")
        else:
            print("✅ CORRECT: Jason Virtue properly filtered out")
            print("   Reason: All meetings are informational/broadcast type with email list invitations")
    else:
        print("ℹ️  Jason Virtue not found in calendar data")
    
    # Save results
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    results = {
        'analysis_timestamp': datetime.now().isoformat(),
        'algorithm_version': '4.2_enterprise_taxonomy_corrected',
        'total_genuine_collaborators': len(collaborators),
        'collaborators': collaborators,
        'jason_virtue_filtered': not any(collab['name'] == 'Jason Virtue' for collab in collaborators),
        'algorithm_improvements': [
            'Integrated Enterprise Meeting Taxonomy classification',
            'Distinguished genuine collaboration from information consumption',
            'Added email list detection and penalty',
            'Enhanced evidence requirements for genuine collaboration',
            'Improved confidence calculation based on collaboration quality'
        ]
    }
    
    filename = f'corrected_collaboration_analysis_{timestamp}.json'
    with open(filename, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"📁 Results saved to: {filename}")

if __name__ == "__main__":
    main()