#!/usr/bin/env python3
"""
Comprehensive Automated Collaboration Discovery System v7.0

This system automatically computes collaboration scores using multiple data sources
and sophisticated temporal analysis, considering:

- Duration and time periods (year-long, month-long, weekly patterns)
- Communication frequency patterns and consistency
- RSVP response speed and meeting engagement
- Cross-modal collaboration analysis (calendar + chat + documents + email)
- Temporal collaboration intensity mapping
- Behavioral collaboration indicators

Addresses the need for automated, comprehensive collaboration analysis rather
than manual, static scoring approaches.
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Set
from collections import defaultdict, Counter
import math
import statistics

class AutomatedCollaborationAnalysis:
    def __init__(self, data_sources: Dict[str, str]):
        """
        Initialize with multiple data source paths
        
        data_sources = {
            'calendar': 'path/to/calendar_data.json',
            'chat': 'path/to/chat_data.json', 
            'documents': 'path/to/document_data.json',
            'email': 'path/to/email_data.json'
        }
        """
        self.data_sources = data_sources
        self.collaboration_metrics = {}
        self.temporal_patterns = {}
        self.behavioral_indicators = {}
        
    def compute_temporal_collaboration_patterns(self, person: str, events: List[Dict]) -> Dict:
        """
        Analyze temporal patterns of collaboration over time
        """
        if not events:
            return {}
            
        # Parse timestamps and sort chronologically
        timestamped_events = []
        for event in events:
            try:
                if 'timestamp' in event:
                    ts = datetime.fromisoformat(event['timestamp'].replace('Z', '+00:00'))
                elif 'start_time' in event:
                    ts = datetime.fromisoformat(event['start_time'].replace('Z', '+00:00'))
                else:
                    continue
                timestamped_events.append((ts, event))
            except:
                continue
                
        timestamped_events.sort(key=lambda x: x[0])
        
        if len(timestamped_events) < 2:
            return {'pattern': 'insufficient_data'}
            
        # Analyze time spans
        first_event = timestamped_events[0][0]
        last_event = timestamped_events[-1][0]
        total_duration = (last_event - first_event).days
        
        # Compute collaboration frequency patterns
        daily_events = defaultdict(int)
        weekly_events = defaultdict(int)
        monthly_events = defaultdict(int)
        
        for ts, event in timestamped_events:
            daily_events[ts.strftime('%Y-%m-%d')] += 1
            weekly_events[ts.strftime('%Y-W%U')] += 1
            monthly_events[ts.strftime('%Y-%m')] += 1
            
        # Calculate consistency metrics
        weekly_counts = list(weekly_events.values())
        monthly_counts = list(monthly_events.values())
        
        consistency_score = 0
        if len(weekly_counts) > 1:
            weekly_std = statistics.stdev(weekly_counts)
            weekly_mean = statistics.mean(weekly_counts)
            consistency_score = max(0, 100 - (weekly_std / weekly_mean * 100))
            
        # Determine collaboration pattern
        pattern_type = "sporadic"
        if total_duration >= 365:  # Year-long
            if len(monthly_events) >= 10:
                pattern_type = "year_long_sustained"
        elif total_duration >= 30:  # Month-long
            if len(weekly_events) >= 3:
                pattern_type = "month_long_regular" 
        elif total_duration >= 7:  # Week-long
            if len(daily_events) >= 3:
                pattern_type = "week_intensive"
                
        # Calculate interaction frequency
        events_per_week = len(timestamped_events) / max(1, total_duration / 7)
        frequency_intensity = min(100, events_per_week * 10)  # Scale to 0-100
        
        return {
            'pattern_type': pattern_type,
            'total_duration_days': total_duration,
            'total_events': len(timestamped_events),
            'events_per_week': round(events_per_week, 2),
            'consistency_score': round(consistency_score, 2),
            'frequency_intensity': round(frequency_intensity, 2),
            'active_weeks': len(weekly_events),
            'active_months': len(monthly_events),
            'first_interaction': first_event.isoformat(),
            'last_interaction': last_event.isoformat()
        }
        
    def compute_rsvp_response_patterns(self, person: str, calendar_events: List[Dict]) -> Dict:
        """
        Analyze RSVP response speed and meeting engagement patterns
        """
        rsvp_data = {
            'response_times': [],
            'response_rates': {},
            'meeting_attendance': 0,
            'organized_meetings': 0,
            'quick_responders': 0  # Responses within 1 hour
        }
        
        for event in calendar_events:
            context = event.get('context', {})
            attendees = context.get('attendees', [])
            organizer = context.get('organizer', '')
            
            if person not in attendees:
                continue
                
            # Meeting organization analysis
            if organizer == person:
                rsvp_data['organized_meetings'] += 1
            elif organizer == "Chin-Yew Lin":  # User organized, person responded
                rsvp_data['meeting_attendance'] += 1
                
                # Simulate RSVP response time analysis
                # In real implementation, this would come from calendar API
                event_created = context.get('created_time')
                rsvp_time = context.get('rsvp_time')
                
                if event_created and rsvp_time:
                    try:
                        created = datetime.fromisoformat(event_created.replace('Z', '+00:00'))
                        responded = datetime.fromisoformat(rsvp_time.replace('Z', '+00:00'))
                        response_delay = (responded - created).total_seconds() / 3600  # Hours
                        
                        rsvp_data['response_times'].append(response_delay)
                        if response_delay <= 1:
                            rsvp_data['quick_responders'] += 1
                    except:
                        pass
        
        # Calculate RSVP metrics
        if rsvp_data['response_times']:
            avg_response_time = statistics.mean(rsvp_data['response_times'])
            response_speed_score = max(0, 100 - avg_response_time * 2)  # Faster = higher score
        else:
            avg_response_time = 0
            response_speed_score = 50  # Default middle score
            
        attendance_rate = rsvp_data['meeting_attendance'] / max(1, len(calendar_events)) * 100
        organization_ratio = rsvp_data['organized_meetings'] / max(1, len(calendar_events)) * 100
        
        return {
            'avg_response_time_hours': round(avg_response_time, 2),
            'response_speed_score': round(response_speed_score, 2),
            'attendance_rate': round(attendance_rate, 2),
            'organization_ratio': round(organization_ratio, 2),
            'quick_response_rate': round(rsvp_data['quick_responders'] / max(1, len(rsvp_data['response_times'])) * 100, 2),
            'total_organized': rsvp_data['organized_meetings'],
            'total_attended': rsvp_data['meeting_attendance']
        }
        
    def compute_communication_frequency_analysis(self, person: str, all_data: Dict) -> Dict:
        """
        Analyze communication frequency across all channels
        """
        frequency_analysis = {
            'calendar': {'events': 0, 'frequency_score': 0},
            'chat': {'messages': 0, 'frequency_score': 0},
            'email': {'messages': 0, 'frequency_score': 0},
            'documents': {'collaborations': 0, 'frequency_score': 0}
        }
        
        # Calendar frequency
        calendar_events = all_data.get('calendar', [])
        person_events = [e for e in calendar_events if person in e.get('context', {}).get('attendees', [])]
        
        if person_events:
            temporal_patterns = self.compute_temporal_collaboration_patterns(person, person_events)
            frequency_analysis['calendar']['events'] = len(person_events)
            frequency_analysis['calendar']['frequency_score'] = temporal_patterns.get('frequency_intensity', 0)
            
        # Chat frequency (simulated - would come from Teams API)
        chat_data = all_data.get('chat', {})
        if person in chat_data:
            person_chat = chat_data[person]
            daily_messages = person_chat.get('daily_messages', 0)
            chat_frequency_score = min(100, daily_messages * 5)  # Scale daily messages
            
            frequency_analysis['chat']['messages'] = daily_messages * 30  # Monthly estimate
            frequency_analysis['chat']['frequency_score'] = chat_frequency_score
            
        # Email frequency (simulated - would come from Mail API)  
        email_data = all_data.get('email', {})
        if person in email_data:
            person_email = email_data[person]
            weekly_emails = person_email.get('weekly_emails', 0)
            email_frequency_score = min(100, weekly_emails * 8)  # Scale weekly emails
            
            frequency_analysis['email']['messages'] = weekly_emails * 4  # Monthly estimate
            frequency_analysis['email']['frequency_score'] = email_frequency_score
            
        # Document collaboration frequency
        doc_data = all_data.get('documents', {})
        if person in doc_data:
            person_docs = doc_data[person]
            doc_collaborations = person_docs.get('joint_documents', 0)
            doc_frequency_score = min(100, doc_collaborations * 15)  # Scale document count
            
            frequency_analysis['documents']['collaborations'] = doc_collaborations
            frequency_analysis['documents']['frequency_score'] = doc_frequency_score
            
        return frequency_analysis
        
    def compute_comprehensive_collaboration_score(self, person: str, all_data: Dict) -> Dict:
        """
        Compute comprehensive collaboration score considering all factors
        """
        print(f"🔍 COMPREHENSIVE ANALYSIS: {person}")
        print("-" * 50)
        
        # Get all person-related events
        calendar_events = all_data.get('calendar', [])
        person_events = [e for e in calendar_events if person in e.get('context', {}).get('attendees', [])]
        
        # 1. Temporal Analysis
        temporal_patterns = self.compute_temporal_collaboration_patterns(person, person_events)
        temporal_score = (
            temporal_patterns.get('frequency_intensity', 0) * 0.3 +
            temporal_patterns.get('consistency_score', 0) * 0.2 +
            min(100, temporal_patterns.get('total_duration_days', 0) / 3.65) * 0.5  # Duration bonus
        )
        
        # 2. RSVP and Engagement Analysis
        rsvp_patterns = self.compute_rsvp_response_patterns(person, person_events)
        engagement_score = (
            rsvp_patterns.get('response_speed_score', 0) * 0.4 +
            rsvp_patterns.get('attendance_rate', 0) * 0.3 +
            rsvp_patterns.get('organization_ratio', 0) * 0.3
        )
        
        # 3. Multi-Channel Frequency Analysis
        frequency_analysis = self.compute_communication_frequency_analysis(person, all_data)
        frequency_score = (
            frequency_analysis['calendar']['frequency_score'] * 0.25 +
            frequency_analysis['chat']['frequency_score'] * 0.35 +
            frequency_analysis['email']['frequency_score'] * 0.2 +
            frequency_analysis['documents']['frequency_score'] * 0.2
        )
        
        # 4. Collaboration Depth Analysis
        depth_indicators = {
            'one_on_one_meetings': len([e for e in person_events if len(e.get('context', {}).get('attendees', [])) == 2]),
            'organized_meetings': len([e for e in person_events if e.get('context', {}).get('organizer') == person]),
            'working_sessions': len([e for e in person_events if any(keyword in e.get('context', {}).get('subject', '').lower() 
                                   for keyword in ['sync', 'discuss', 'review', 'planning', 'working'])]),
        }
        
        depth_score = (
            depth_indicators['one_on_one_meetings'] * 30 +
            depth_indicators['organized_meetings'] * 25 +
            depth_indicators['working_sessions'] * 15
        )
        
        # 5. Final Comprehensive Score
        final_score = (
            temporal_score * 0.25 +      # Consistency and duration
            engagement_score * 0.2 +     # Responsiveness and engagement  
            frequency_score * 0.35 +     # Communication frequency
            min(depth_score, 200) * 0.2  # Collaboration depth (capped)
        )
        
        return {
            'person': person,
            'final_score': round(final_score, 2),
            'breakdown': {
                'temporal_score': round(temporal_score, 2),
                'engagement_score': round(engagement_score, 2), 
                'frequency_score': round(frequency_score, 2),
                'depth_score': round(min(depth_score, 200), 2)
            },
            'temporal_patterns': temporal_patterns,
            'rsvp_patterns': rsvp_patterns,
            'frequency_analysis': frequency_analysis,
            'depth_indicators': depth_indicators,
            'data_completeness': self._assess_data_completeness(person, all_data)
        }
        
    def _assess_data_completeness(self, person: str, all_data: Dict) -> Dict:
        """Assess how complete our data is for this person"""
        completeness = {
            'calendar': len([e for e in all_data.get('calendar', []) if person in e.get('context', {}).get('attendees', [])]) > 0,
            'chat': person in all_data.get('chat', {}),
            'email': person in all_data.get('email', {}), 
            'documents': person in all_data.get('documents', {}),
            'completeness_percentage': 0
        }
        
        completeness['completeness_percentage'] = sum(completeness.values()) / 4 * 100
        return completeness
        
    def run_automated_analysis(self, target_people: List[str]) -> Dict:
        """
        Run automated comprehensive collaboration analysis
        """
        print("🚀 AUTOMATED COLLABORATION DISCOVERY v7.0")
        print("=" * 60)
        print("Comprehensive temporal, behavioral, and cross-modal analysis")
        print()
        
        # Load all available data sources
        all_data = {}
        
        # Load calendar data
        if 'calendar' in self.data_sources and os.path.exists(self.data_sources['calendar']):
            with open(self.data_sources['calendar'], 'r') as f:
                all_data['calendar'] = json.load(f)
                print(f"✅ Calendar data loaded: {len(all_data['calendar'])} events")
        else:
            all_data['calendar'] = []
            print("❌ No calendar data available")
            
        # Simulate other data sources (in real implementation, load from APIs)
        all_data['chat'] = {
            'Haidong Zhang': {
                'daily_messages': 8,
                'group_chats': 5,
                'mentions_per_week': 12,
                'file_shares_per_month': 15
            },
            'Xiaodong Liu': {
                'daily_messages': 5,
                'group_chats': 2, 
                'mentions_per_week': 3,
                'file_shares_per_month': 2
            }
        }
        
        all_data['email'] = {
            'Haidong Zhang': {
                'weekly_emails': 6,
                'response_rate': 95,
                'avg_response_time_hours': 2.5
            }
        }
        
        all_data['documents'] = {
            'Haidong Zhang': {
                'joint_documents': 4,
                'edit_sessions': 25,
                'shared_workspaces': 3
            }
        }
        
        print(f"✅ Simulated chat data for {len(all_data['chat'])} people")
        print(f"✅ Simulated email data for {len(all_data['email'])} people") 
        print(f"✅ Simulated document data for {len(all_data['documents'])} people")
        print()
        
        # Analyze each person comprehensively
        results = []
        for person in target_people:
            analysis = self.compute_comprehensive_collaboration_score(person, all_data)
            results.append(analysis)
            
            print(f"📊 ANALYSIS SUMMARY:")
            print(f"   🎯 Final Score: {analysis['final_score']:.1f}")
            print(f"   ⏱️  Temporal: {analysis['breakdown']['temporal_score']:.1f}")
            print(f"   📱 Engagement: {analysis['breakdown']['engagement_score']:.1f}")
            print(f"   🔄 Frequency: {analysis['breakdown']['frequency_score']:.1f}")
            print(f"   🤝 Depth: {analysis['breakdown']['depth_score']:.1f}")
            
            # Show key patterns
            if analysis['temporal_patterns'].get('pattern_type'):
                print(f"   📈 Pattern: {analysis['temporal_patterns']['pattern_type']}")
                print(f"   ⏰ Duration: {analysis['temporal_patterns']['total_duration_days']} days")
                print(f"   🔁 Frequency: {analysis['temporal_patterns']['events_per_week']:.1f} events/week")
                
            if analysis['rsvp_patterns'].get('response_speed_score'):
                print(f"   ⚡ RSVP Speed: {analysis['rsvp_patterns']['avg_response_time_hours']:.1f}h avg")
                print(f"   ✅ Quick Response Rate: {analysis['rsvp_patterns']['quick_response_rate']:.1f}%")
                
            print(f"   📊 Data Completeness: {analysis['data_completeness']['completeness_percentage']:.0f}%")
            print()
        
        # Sort by final score  
        results.sort(key=lambda x: x['final_score'], reverse=True)
        
        print("🏆 FINAL AUTOMATED RANKINGS:")
        print("-" * 60)
        for i, result in enumerate(results, 1):
            print(f"{i}. {result['person']} - {result['final_score']:.1f} points")
            pattern = result['temporal_patterns'].get('pattern_type', 'unknown')
            completeness = result['data_completeness']['completeness_percentage']
            print(f"   📈 {pattern} | 📊 {completeness:.0f}% data complete")
        
        return {
            'algorithm_version': '7.0_automated_comprehensive',
            'timestamp': datetime.now().isoformat(),
            'analysis_results': results,
            'methodology': 'temporal + behavioral + cross-modal + engagement',
            'data_sources_used': list(all_data.keys())
        }

def main():
    """Run comprehensive automated collaboration analysis"""
    
    # Configure data sources
    data_sources = {
        'calendar': 'meeting_prep_data/real_calendar_scenarios.json',
        'chat': 'teams_chat_data.json',  # Would come from Teams API
        'email': 'email_data.json',      # Would come from Mail API  
        'documents': 'document_data.json' # Would come from Files API
    }
    
    # Initialize analysis system
    analyzer = AutomatedCollaborationAnalysis(data_sources)
    
    # Target people for analysis
    target_people = ['Haidong Zhang', 'Xiaodong Liu', 'Caroline Mao']
    
    # Run comprehensive analysis
    results = analyzer.run_automated_analysis(target_people)
    
    # Save detailed results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"automated_collaboration_analysis_{timestamp}.json"
    
    with open(filename, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"✅ Detailed results saved to: {filename}")
    
    print(f"\n💡 KEY INSIGHTS:")
    print("   • Temporal patterns reveal sustained vs sporadic collaboration")
    print("   • RSVP speed indicates engagement and prioritization")
    print("   • Cross-modal frequency shows collaboration intensity")
    print("   • Behavioral indicators reveal collaboration depth")
    
    print(f"\n🔮 REQUIRED FOR COMPLETE AUTOMATION:")
    print("   • Microsoft Graph API: Chat.Read, Mail.Read, Files.Read")
    print("   • Real-time data ingestion and processing")
    print("   • Temporal pattern recognition algorithms")
    print("   • Behavioral analytics and scoring models")

if __name__ == "__main__":
    main()