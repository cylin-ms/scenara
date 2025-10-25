#!/usr/bin/env python3
"""
Revised Enhanced Collaboration Algorithm v4.0
Implementing expert critique recommendations for improved accuracy and scalability
"""

import json
import math
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Dict, List, Any, Tuple

class EnhancedCollaborationAnalyzerV4:
    """
    Version 4.0 of the collaboration algorithm incorporating expert recommendations
    """
    
    def __init__(self):
        self.current_date = datetime.now()
        
        # Improved scoring weights based on critique
        self.weights = {
            'one_on_one': 25,           # Increased from 20 (highest signal)
            'organized_by_me': 18,      # Increased from 15 (active collaboration)
            'attended_their_meetings': 12,  # Increased from 10 (mutual engagement)
            'small_meetings': 6,        # Increased from 5 (focused collaboration)
            'medium_meetings': 2,       # Same (moderate signal)
            'large_meetings': 0.1,      # Same (minimal signal)
            'saved_contact': 15,        # Decreased from 20 (important but not primary)
            'direct_emails': 10,        # Future enhancement
            'chat_messages': 5,         # Future enhancement
            'phone_calls': 15           # Future enhancement
        }
        
        # Temporal decay parameters
        self.temporal_decay_weeks = 26  # 6 months half-life
        self.recency_boost_weeks = 4    # Recent activity boost
        
        # Meeting context classification
        self.high_importance_keywords = [
            'strategy', 'planning', 'review', 'decision', 'critical',
            'urgent', 'executive', 'board', 'leadership', 'vision'
        ]
        
        self.low_importance_keywords = [
            'standup', 'daily', 'routine', 'check-in', 'fyi',
            'announcement', 'broadcast', 'all-hands', 'social'
        ]
    
    def analyze_collaboration_with_improvements(self, calendar_data: List[Dict]) -> List[Dict]:
        """
        Enhanced collaboration analysis with expert recommendations implemented
        """
        print("🚀 Running Enhanced Collaboration Algorithm v4.0...")
        
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
            'total_weighted_score': 0,
            'temporal_score': 0,
            'context_score': 0,
            'recency_score': 0
        })
        
        # Process calendar events with enhanced analysis
        for event in calendar_data:
            attendees = event['context'].get('attendees', [])
            attendee_count = len(attendees)
            organizer = event['context'].get('organizer', 'Unknown')
            is_my_meeting = organizer == 'Chin-Yew Lin'
            start_time = event['context'].get('start_time', '')
            subject = event['context'].get('subject', '').lower()
            
            # Calculate temporal factors
            meeting_date = self._parse_meeting_date(start_time)
            temporal_weight = self._calculate_temporal_weight(meeting_date)
            context_importance = self._classify_meeting_importance(subject)
            
            time_period = start_time[:7] if start_time else 'unknown'
            
            for attendee in attendees:
                if attendee != 'Chin-Yew Lin':
                    data = collaboration_scores[attendee]
                    
                    # Basic tracking
                    data['total_meetings'] += 1
                    data['time_periods'].add(time_period)
                    data['subjects'].append(subject)
                    
                    # Enhanced meeting details tracking
                    meeting_detail = {
                        'date': meeting_date,
                        'size': attendee_count,
                        'subject': subject,
                        'organizer': organizer,
                        'temporal_weight': temporal_weight,
                        'context_importance': context_importance,
                        'weighted_value': 0  # Will be calculated
                    }
                    
                    # Calculate meeting category scores with temporal and context weighting
                    base_score = 0
                    if attendee_count == 2:  # 1:1 meeting
                        data['one_on_one_meetings'] += 1
                        base_score = self.weights['one_on_one']
                    elif attendee_count <= 10:
                        data['small_meetings'] += 1
                        base_score = self.weights['small_meetings']
                    elif attendee_count <= 50:
                        data['medium_meetings'] += 1
                        base_score = self.weights['medium_meetings']
                    else:
                        data['large_meetings'] += 1
                        base_score = self.weights['large_meetings']
                    
                    # Apply temporal and context weighting
                    weighted_score = base_score * temporal_weight * context_importance
                    meeting_detail['weighted_value'] = weighted_score
                    data['meeting_details'].append(meeting_detail)
                    
                    # Organization tracking with enhanced weighting
                    if is_my_meeting:
                        data['organized_by_me'] += 1
                        org_score = self.weights['organized_by_me'] * temporal_weight * context_importance
                        data['total_weighted_score'] += org_score
                    
                    if organizer == attendee:
                        data['i_attended_their_meetings'] += 1
                        attend_score = self.weights['attended_their_meetings'] * temporal_weight * context_importance
                        data['total_weighted_score'] += attend_score
                    
                    # Add meeting score to total
                    data['total_weighted_score'] += weighted_score
        
        # Enhanced filtering and scoring
        genuine_collaborators = []
        
        for person, data in collaboration_scores.items():
            if data['total_meetings'] >= 2:
                
                # Calculate additional scoring factors
                recency_score = self._calculate_recency_score(data['meeting_details'])
                relationship_depth = self._calculate_relationship_depth(data)
                consistency_score = self._calculate_consistency_score(data['time_periods'])
                
                # Enhanced collaboration evidence
                has_strong_evidence = (
                    data['one_on_one_meetings'] > 0 or
                    data['organized_by_me'] > 0 or
                    data['i_attended_their_meetings'] > 0 or
                    data['in_contacts'] or
                    (data['small_meetings'] >= 3 and len(data['time_periods']) > 1)
                )
                
                # System account filtering (enhanced)
                is_system_account = self._is_system_account(person, data['subjects'])
                
                # Final score calculation
                final_score = (
                    data['total_weighted_score'] +
                    recency_score +
                    relationship_depth +
                    consistency_score
                )
                
                # Statistical significance check
                confidence_level = self._calculate_confidence_level(data, final_score)
                
                if (has_strong_evidence and 
                    not is_system_account and 
                    final_score > 15 and 
                    confidence_level > 0.7):
                    
                    collaborator = {
                        'name': person,
                        'final_score': round(final_score, 2),
                        'base_weighted_score': round(data['total_weighted_score'], 2),
                        'recency_score': round(recency_score, 2),
                        'relationship_depth': round(relationship_depth, 2),
                        'consistency_score': round(consistency_score, 2),
                        'confidence_level': round(confidence_level, 3),
                        'one_on_one': data['one_on_one_meetings'],
                        'small_meetings': data['small_meetings'],
                        'medium_meetings': data['medium_meetings'],
                        'large_meetings': data['large_meetings'],
                        'organized_by_me': data['organized_by_me'],
                        'attended_their_meetings': data['i_attended_their_meetings'],
                        'time_periods': len(data['time_periods']),
                        'total_meetings': data['total_meetings'],
                        'evidence_strength': 'strong' if final_score > 50 else 'moderate',
                        'algorithm_version': '4.0'
                    }
                    
                    genuine_collaborators.append(collaborator)
        
        # Sort by final score
        genuine_collaborators.sort(key=lambda x: x['final_score'], reverse=True)
        
        return genuine_collaborators[:8]  # Top 8 collaborators
    
    def _parse_meeting_date(self, start_time: str) -> datetime:
        """Parse meeting date from ISO string"""
        try:
            return datetime.fromisoformat(start_time.replace('Z', '+00:00'))
        except:
            return datetime.now() - timedelta(days=30)  # Default to 30 days ago
    
    def _calculate_temporal_weight(self, meeting_date: datetime) -> float:
        """Calculate temporal weight with decay for older meetings"""
        days_ago = (self.current_date - meeting_date).days
        weeks_ago = days_ago / 7
        
        # Recency boost for very recent meetings
        if weeks_ago <= self.recency_boost_weeks:
            return 1.2  # 20% boost for recent meetings
        
        # Exponential decay for older meetings
        decay_factor = math.exp(-weeks_ago / self.temporal_decay_weeks)
        return max(0.1, decay_factor)  # Minimum weight of 0.1
    
    def _classify_meeting_importance(self, subject: str) -> float:
        """Classify meeting importance based on subject keywords"""
        subject_lower = subject.lower()
        
        # High importance meetings
        if any(keyword in subject_lower for keyword in self.high_importance_keywords):
            return 1.3  # 30% boost
        
        # Low importance meetings
        if any(keyword in subject_lower for keyword in self.low_importance_keywords):
            return 0.7  # 30% reduction
        
        # Default importance
        return 1.0
    
    def _calculate_recency_score(self, meeting_details: List[Dict]) -> float:
        """Calculate score boost for recent collaborative activity"""
        recent_meetings = [
            m for m in meeting_details 
            if (self.current_date - m['date']).days <= 30
        ]
        
        if not recent_meetings:
            return 0
        
        # Higher score for more recent meetings
        recency_boost = len(recent_meetings) * 2
        return min(recency_boost, 10)  # Cap at 10 points
    
    def _calculate_relationship_depth(self, data: Dict) -> float:
        """Calculate relationship depth based on interaction variety"""
        depth_score = 0
        
        # Diversity of interaction types
        if data['one_on_one_meetings'] > 0:
            depth_score += 5
        if data['organized_by_me'] > 0:
            depth_score += 5
        if data['i_attended_their_meetings'] > 0:
            depth_score += 5
        if data['small_meetings'] >= 3:
            depth_score += 3
        
        return depth_score
    
    def _calculate_consistency_score(self, time_periods: set) -> float:
        """Calculate score for consistent collaboration over time"""
        period_count = len(time_periods)
        
        if period_count >= 4:
            return 8  # Long-term consistent collaboration
        elif period_count >= 2:
            return 4  # Multi-period collaboration
        else:
            return 0  # Single period only
    
    def _calculate_confidence_level(self, data: Dict, final_score: float) -> float:
        """Calculate statistical confidence level for the collaboration assessment"""
        
        # Factors that increase confidence
        evidence_count = 0
        if data['one_on_one_meetings'] > 0:
            evidence_count += 2
        if data['organized_by_me'] > 0:
            evidence_count += 2
        if data['i_attended_their_meetings'] > 0:
            evidence_count += 2
        if data['total_meetings'] >= 5:
            evidence_count += 1
        if len(data['time_periods']) >= 3:
            evidence_count += 1
        
        # Base confidence from evidence count
        base_confidence = min(evidence_count / 8, 1.0)
        
        # Score-based confidence adjustment
        score_confidence = min(final_score / 100, 1.0)
        
        # Combined confidence
        return (base_confidence + score_confidence) / 2
    
    def _is_system_account(self, person: str, subjects: List[str]) -> bool:
        """Enhanced system account detection"""
        
        # Name-based detection
        system_indicators = [
            'rob', 'fte', 'extended', 'community', 'team', 'group',
            'holiday', 'event', 'auto', 'system', 'notification',
            'bot', 'service', 'admin'
        ]
        
        if any(indicator in person.lower() for indicator in system_indicators):
            return True
        
        # Behavior-based detection
        holiday_meetings = sum(1 for subj in subjects if 'holiday' in subj)
        if holiday_meetings / len(subjects) > 0.5:  # More than 50% holiday meetings
            return True
        
        return False

def test_enhanced_algorithm():
    """Test the enhanced algorithm with real data"""
    
    print("🧪 TESTING ENHANCED COLLABORATION ALGORITHM V4.0")
    print("=" * 60)
    
    # Load real calendar data
    try:
        with open('meeting_prep_data/real_calendar_scenarios.json', 'r') as f:
            calendar_data = json.load(f)
    except FileNotFoundError:
        print("❌ Calendar data not found")
        return
    
    analyzer = EnhancedCollaborationAnalyzerV4()
    collaborators = analyzer.analyze_collaboration_with_improvements(calendar_data)
    
    print(f"\n✅ ENHANCED ALGORITHM RESULTS:")
    print(f"📊 Found {len(collaborators)} genuine collaborators\n")
    
    for i, collab in enumerate(collaborators, 1):
        print(f"{i:2d}. {collab['name']}")
        print(f"    💯 Final Score: {collab['final_score']}")
        print(f"    🎯 Confidence: {collab['confidence_level']:.1%}")
        print(f"    📊 Components: Base({collab['base_weighted_score']}) + Recency({collab['recency_score']}) + Depth({collab['relationship_depth']}) + Consistency({collab['consistency_score']})")
        print(f"    🤝 Evidence: {collab['one_on_one']} 1:1, {collab['organized_by_me']} organized, {collab['attended_their_meetings']} their meetings")
        print(f"    📅 Span: {collab['time_periods']} periods, {collab['total_meetings']} total meetings")
        print(f"    ⭐ Strength: {collab['evidence_strength']}")
        print()
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"enhanced_algorithm_v4_results_{timestamp}.json"
    
    results = {
        'algorithm_version': '4.0',
        'improvements_implemented': [
            'Temporal decay weighting',
            'Meeting context classification', 
            'Recency scoring',
            'Relationship depth analysis',
            'Consistency scoring',
            'Statistical confidence levels'
        ],
        'collaborators': collaborators,
        'test_timestamp': timestamp
    }
    
    with open(filename, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"📁 Results saved to: {filename}")
    
    return collaborators

if __name__ == "__main__":
    collaborators = test_enhanced_algorithm()
    print("\n🎯 Enhanced Algorithm v4.0 testing complete!")