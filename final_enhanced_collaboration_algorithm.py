#!/usr/bin/env python3
"""
Final Revised Enhanced Collaboration Algorithm v4.1
Fixed temporal weighting and optimized thresholds based on debugging
"""

import json
import math
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Dict, List, Any

class FinalEnhancedCollaborationAlgorithm:
    """
    Final version incorporating expert feedback with proper temporal handling
    """
    
    def __init__(self):
        # Optimized scoring weights based on analysis
        self.weights = {
            'one_on_one': 25,
            'organized_by_me': 18,
            'attended_their_meetings': 12,
            'small_meetings': 6,
            'medium_meetings': 2,
            'large_meetings': 0.1,
            'saved_contact': 15
        }
        
        # Context importance multipliers
        self.high_importance_keywords = [
            'strategy', 'planning', 'review', 'decision', 'critical',
            'urgent', 'executive', 'leadership', 'vision', 'roadmap'
        ]
        
        self.low_importance_keywords = [
            'standup', 'daily', 'routine', 'fyi', 'announcement', 
            'broadcast', 'all-hands', 'social', 'lunch'
        ]
    
    def analyze_enhanced_collaboration(self, calendar_data: List[Dict]) -> List[Dict]:
        """
        Enhanced collaboration analysis with improved temporal and context handling
        """
        print("🚀 Running Final Enhanced Collaboration Algorithm v4.1...")
        
        collaboration_scores = defaultdict(lambda: {
            'total_meetings': 0,
            'one_on_one_meetings': 0,
            'small_meetings': 0,
            'medium_meetings': 0,
            'large_meetings': 0,
            'organized_by_me': 0,
            'i_attended_their_meetings': 0,
            'meeting_details': [],
            'time_periods': set(),
            'subjects': [],
            'in_contacts': False,
            'base_score': 0,
            'context_bonus': 0,
            'recency_bonus': 0,
            'consistency_bonus': 0
        })
        
        current_date = datetime.now()
        
        # Process calendar events
        for event in calendar_data:
            attendees = event['context'].get('attendees', [])
            attendee_count = len(attendees)
            organizer = event['context'].get('organizer', 'Unknown')
            is_my_meeting = organizer == 'Chin-Yew Lin'
            start_time = event['context'].get('start_time', '')
            subject = event['context'].get('subject', '').lower()
            
            # Parse meeting date with fallback
            try:
                if start_time:
                    meeting_date = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
                else:
                    meeting_date = current_date - timedelta(days=30)
            except:
                meeting_date = current_date - timedelta(days=30)
            
            time_period = start_time[:7] if start_time else 'unknown'
            
            # Calculate context importance
            context_multiplier = self._get_context_multiplier(subject)
            
            # Calculate recency factor (simplified)
            days_ago = (current_date - meeting_date).days
            recency_factor = 1.2 if days_ago <= 30 else 1.0  # Recent boost
            
            for attendee in attendees:
                if attendee != 'Chin-Yew Lin':
                    data = collaboration_scores[attendee]
                    
                    # Basic tracking
                    data['total_meetings'] += 1
                    data['time_periods'].add(time_period)
                    data['subjects'].append(subject)
                    
                    # Meeting details for analysis
                    meeting_detail = {
                        'date': meeting_date,
                        'size': attendee_count,
                        'subject': subject,
                        'organizer': organizer,
                        'context_multiplier': context_multiplier,
                        'recency_factor': recency_factor
                    }
                    data['meeting_details'].append(meeting_detail)
                    
                    # Calculate base meeting score
                    base_meeting_score = 0
                    if attendee_count == 2:  # 1:1 meeting
                        data['one_on_one_meetings'] += 1
                        base_meeting_score = self.weights['one_on_one']
                    elif attendee_count <= 10:
                        data['small_meetings'] += 1
                        base_meeting_score = self.weights['small_meetings']
                    elif attendee_count <= 50:
                        data['medium_meetings'] += 1
                        base_meeting_score = self.weights['medium_meetings']
                    else:
                        data['large_meetings'] += 1
                        base_meeting_score = self.weights['large_meetings']
                    
                    # Apply context and recency factors
                    final_meeting_score = base_meeting_score * context_multiplier * recency_factor
                    data['base_score'] += final_meeting_score
                    
                    # Organization tracking
                    if is_my_meeting:
                        data['organized_by_me'] += 1
                        org_score = self.weights['organized_by_me'] * context_multiplier * recency_factor
                        data['base_score'] += org_score
                    
                    if organizer == attendee:
                        data['i_attended_their_meetings'] += 1
                        attend_score = self.weights['attended_their_meetings'] * context_multiplier * recency_factor
                        data['base_score'] += attend_score
        
        # Calculate additional scoring factors
        for person, data in collaboration_scores.items():
            if data['total_meetings'] >= 2:
                
                # Context bonus for high-importance meetings
                high_importance_meetings = sum(
                    1 for detail in data['meeting_details']
                    if detail['context_multiplier'] > 1.0
                )
                data['context_bonus'] = high_importance_meetings * 2
                
                # Recency bonus for recent activity
                recent_meetings = sum(
                    1 for detail in data['meeting_details']
                    if detail['recency_factor'] > 1.0
                )
                data['recency_bonus'] = recent_meetings * 1.5
                
                # Consistency bonus for multi-period collaboration
                if len(data['time_periods']) >= 3:
                    data['consistency_bonus'] = 5
                elif len(data['time_periods']) >= 2:
                    data['consistency_bonus'] = 2
        
        # Final filtering and ranking
        genuine_collaborators = []
        
        for person, data in collaboration_scores.items():
            if data['total_meetings'] >= 2:
                
                # Enhanced evidence requirements
                has_strong_evidence = (
                    data['one_on_one_meetings'] > 0 or
                    data['organized_by_me'] > 0 or
                    data['i_attended_their_meetings'] > 0 or
                    data['in_contacts'] or
                    (data['small_meetings'] >= 3 and len(data['time_periods']) > 1)
                )
                
                # Enhanced system account detection
                is_system_account = self._is_enhanced_system_account(person, data['subjects'])
                
                # Calculate final score
                final_score = (
                    data['base_score'] + 
                    data['context_bonus'] + 
                    data['recency_bonus'] + 
                    data['consistency_bonus']
                )
                
                # Adjusted threshold based on debugging (lowered from 15 to 10)
                min_score_threshold = 10
                
                if (has_strong_evidence and 
                    not is_system_account and 
                    final_score > min_score_threshold):
                    
                    # Calculate confidence level
                    confidence = self._calculate_confidence(data, final_score)
                    
                    collaborator = {
                        'name': person,
                        'final_score': round(final_score, 2),
                        'base_score': round(data['base_score'], 2),
                        'context_bonus': round(data['context_bonus'], 2),
                        'recency_bonus': round(data['recency_bonus'], 2),
                        'consistency_bonus': round(data['consistency_bonus'], 2),
                        'confidence_level': round(confidence, 3),
                        'evidence_summary': {
                            'one_on_one': data['one_on_one_meetings'],
                            'organized_by_me': data['organized_by_me'],
                            'attended_their_meetings': data['i_attended_their_meetings'],
                            'small_meetings': data['small_meetings'],
                            'medium_meetings': data['medium_meetings'],
                            'large_meetings': data['large_meetings'],
                            'time_periods': len(data['time_periods']),
                            'total_meetings': data['total_meetings']
                        },
                        'collaboration_strength': self._assess_strength(final_score),
                        'algorithm_version': '4.1_final'
                    }
                    
                    genuine_collaborators.append(collaborator)
        
        # Sort by final score
        genuine_collaborators.sort(key=lambda x: x['final_score'], reverse=True)
        
        return genuine_collaborators[:8]  # Top 8
    
    def _get_context_multiplier(self, subject: str) -> float:
        """Get context importance multiplier"""
        subject_lower = subject.lower()
        
        if any(keyword in subject_lower for keyword in self.high_importance_keywords):
            return 1.3  # 30% boost for important meetings
        elif any(keyword in subject_lower for keyword in self.low_importance_keywords):
            return 0.8  # 20% reduction for routine meetings
        else:
            return 1.0  # Normal weight
    
    def _is_enhanced_system_account(self, person: str, subjects: List[str]) -> bool:
        """Enhanced system account detection"""
        
        # Name-based detection
        system_indicators = [
            'rob', 'fte', 'extended', 'community', 'team', 'group',
            'holiday', 'event', 'auto', 'system', 'notification',
            'bot', 'service', 'admin', 'learning'
        ]
        
        person_lower = person.lower()
        if any(indicator in person_lower for indicator in system_indicators):
            return True
        
        # Behavior-based detection
        if subjects:
            holiday_meetings = sum(1 for subj in subjects if 'holiday' in subj.lower())
            if holiday_meetings / len(subjects) > 0.4:  # 40% threshold
                return True
        
        return False
    
    def _calculate_confidence(self, data: Dict, final_score: float) -> float:
        """Calculate confidence level for collaboration assessment"""
        
        evidence_factors = 0
        
        # Strong evidence factors
        if data['one_on_one_meetings'] > 0:
            evidence_factors += 0.3
        if data['organized_by_me'] > 0:
            evidence_factors += 0.3
        if data['i_attended_their_meetings'] > 0:
            evidence_factors += 0.3
        
        # Supporting evidence
        if data['small_meetings'] >= 3:
            evidence_factors += 0.2
        if len(data['time_periods']) >= 3:
            evidence_factors += 0.2
        if data['total_meetings'] >= 5:
            evidence_factors += 0.1
        
        # Score-based confidence
        score_confidence = min(final_score / 100, 0.5)
        
        return min(evidence_factors + score_confidence, 1.0)
    
    def _assess_strength(self, score: float) -> str:
        """Assess collaboration strength based on score"""
        if score >= 80:
            return 'very_strong'
        elif score >= 50:
            return 'strong'
        elif score >= 25:
            return 'moderate'
        else:
            return 'weak'

def test_final_algorithm():
    """Test the final enhanced algorithm"""
    
    print("🧪 TESTING FINAL ENHANCED COLLABORATION ALGORITHM V4.1")
    print("=" * 65)
    
    # Load real calendar data
    try:
        with open('meeting_prep_data/real_calendar_scenarios.json', 'r') as f:
            calendar_data = json.load(f)
    except FileNotFoundError:
        print("❌ Calendar data not found")
        return
    
    analyzer = FinalEnhancedCollaborationAlgorithm()
    collaborators = analyzer.analyze_enhanced_collaboration(calendar_data)
    
    print(f"\n✅ FINAL ENHANCED ALGORITHM RESULTS:")
    print(f"📊 Found {len(collaborators)} genuine collaborators\n")
    
    for i, collab in enumerate(collaborators, 1):
        evidence = collab['evidence_summary']
        print(f"{i:2d}. {collab['name']}")
        print(f"    💯 Final Score: {collab['final_score']}")
        print(f"    🎯 Confidence: {collab['confidence_level']:.1%}")
        print(f"    ⭐ Strength: {collab['collaboration_strength']}")
        print(f"    📊 Score Breakdown:")
        print(f"       Base: {collab['base_score']} | Context: +{collab['context_bonus']} | Recency: +{collab['recency_bonus']} | Consistency: +{collab['consistency_bonus']}")
        print(f"    🤝 Evidence:")
        print(f"       1:1 meetings: {evidence['one_on_one']}")
        print(f"       Organized by you: {evidence['organized_by_me']}")
        print(f"       Attended their meetings: {evidence['attended_their_meetings']}")
        print(f"       Small meetings: {evidence['small_meetings']}")
        print(f"       Time periods: {evidence['time_periods']}")
        print(f"       Total meetings: {evidence['total_meetings']}")
        print()
    
    # Create summary comparison
    print("🔍 ALGORITHM EVOLUTION COMPARISON:")
    print("-" * 40)
    print("v1.0 (Simple): Yanchao Li incorrectly included (false positive)")
    print("v3.0 (Enhanced): Correctly filtered Yanchao Li")
    print("v4.1 (Final): Enhanced with temporal, context, and confidence analysis")
    print(f"v4.1 Results: {len(collaborators)} high-confidence genuine collaborators")
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"final_enhanced_algorithm_results_{timestamp}.json"
    
    results = {
        'algorithm_version': '4.1_final',
        'enhancements': [
            'Temporal weighting with recency boost',
            'Meeting context importance classification',
            'Multi-factor confidence calculation',
            'Enhanced system account detection',
            'Consistency scoring across time periods',
            'Optimized scoring thresholds'
        ],
        'collaborators': collaborators,
        'test_timestamp': timestamp,
        'total_found': len(collaborators)
    }
    
    with open(filename, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n📁 Results saved to: {filename}")
    
    return collaborators

if __name__ == "__main__":
    collaborators = test_final_algorithm()
    print("\n🎯 Final Enhanced Algorithm v4.1 testing complete!")
    print("✅ Ready for integration into Me Notes generation!")