#!/usr/bin/env python3
"""
Enhanced Collaborator Discovery v5.0 - Chat Integration Ready

This version of the collaborator discovery algorithm acknowledges the limitation
of calendar-only data and provides mechanisms to integrate Teams chat data
either through API access or manual input.
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Tuple

class EnhancedCollaboratorDiscoveryV5:
    def __init__(self, calendar_data_path: str):
        self.calendar_data_path = calendar_data_path
        self.manual_chat_data_path = "manual_chat_collaboration_data.json"
        
        # Load calendar data
        with open(calendar_data_path, 'r') as f:
            self.calendar_data = json.load(f)
            
        # Try to load manual chat data if available
        self.chat_data = self.load_manual_chat_data()
        
    def load_manual_chat_data(self) -> Dict:
        """Load manual chat collaboration data if available"""
        if os.path.exists(self.manual_chat_data_path):
            try:
                with open(self.manual_chat_data_path, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️  Warning: Could not load chat data: {e}")
                return {}
        return {}
    
    def save_manual_chat_data(self, chat_data: Dict):
        """Save manual chat collaboration data"""
        with open(self.manual_chat_data_path, 'w') as f:
            json.dump(chat_data, f, indent=2)
        print(f"💾 Chat data saved to: {self.manual_chat_data_path}")
    
    def add_manual_chat_collaborator(self, name: str, daily_chats: int, 
                                   weekly_group_chats: int, relationship_strength: int):
        """Add manual chat collaboration data for a specific person"""
        if 'chat_collaborators' not in self.chat_data:
            self.chat_data['chat_collaborators'] = {}
            
        chat_score = (daily_chats * 30 * 3) + (weekly_group_chats * 1)
        strength_multiplier = {1: 1.5, 2: 1.2, 3: 1.0, 4: 0.7}
        final_score = chat_score * strength_multiplier.get(relationship_strength, 1.0)
        
        self.chat_data['chat_collaborators'][name] = {
            'daily_chats': daily_chats,
            'weekly_group_chats': weekly_group_chats,
            'relationship_strength': relationship_strength,
            'chat_score': final_score,
            'added_date': datetime.now().isoformat()
        }
        
        self.save_manual_chat_data(self.chat_data)
        print(f"✅ Added chat data for {name} (Chat Score: {final_score:.1f})")
    
    def discover_collaborators_enhanced(self, user_name: str = "Chin-Yew Lin") -> Dict:
        """
        Enhanced collaborator discovery that combines calendar and chat data
        """
        print(f"🔍 Enhanced Collaborator Discovery v5.0 - Chat Integration Ready")
        print(f"👤 Analyzing collaborations for: {user_name}")
        print(f"📊 Data Sources:")
        print(f"   ✅ Calendar meetings: {len(self.calendar_data)} events")
        
        if self.chat_data.get('chat_collaborators'):
            chat_count = len(self.chat_data['chat_collaborators'])
            print(f"   ✅ Manual chat data: {chat_count} collaborators")
        else:
            print(f"   ❌ No chat data available")
            print(f"   💡 Use add_manual_chat_collaborator() to add chat relationships")
        
        print("-" * 70)
        
        # Analyze calendar data (existing algorithm)
        calendar_collaborators = self.analyze_calendar_collaborations(user_name)
        
        # Combine with chat data
        combined_collaborators = self.combine_calendar_and_chat_data(calendar_collaborators)
        
        # Rank and score
        final_results = self.rank_combined_collaborators(combined_collaborators)
        
        return final_results
    
    def analyze_calendar_collaborations(self, user_name: str) -> Dict:
        """Analyze calendar collaborations using existing algorithm v4.2"""
        collaborators = {}
        
        for event in self.calendar_data:
            context = event.get('context', {})
            attendees = context.get('attendees', [])
            organizer = context.get('organizer', '')
            subject = context.get('subject', '')
            
            if user_name not in attendees:
                continue
                
            for attendee in attendees:
                if attendee == user_name or not attendee:
                    continue
                    
                # Initialize collaborator data
                if attendee not in collaborators:
                    collaborators[attendee] = {
                        'calendar_meetings': 0,
                        'one_on_one': 0,
                        'organized_by_user': 0,
                        'organized_by_them': 0,
                        'small_meetings': 0,
                        'working_sessions': 0,
                        'calendar_score': 0
                    }
                
                data = collaborators[attendee]
                data['calendar_meetings'] += 1
                
                # Meeting size analysis
                attendee_count = len(attendees)
                if attendee_count == 2:
                    data['one_on_one'] += 1
                elif attendee_count <= 10:
                    data['small_meetings'] += 1
                
                # Organization analysis
                if organizer == user_name:
                    data['organized_by_user'] += 1
                elif organizer == attendee:
                    data['organized_by_them'] += 1
                
                # Working session detection
                working_keywords = ['planning', 'design', 'workshop', 'brainstorm', 
                                  'decision', 'review', 'working', 'sync', 'alignment']
                if any(keyword in subject.lower() for keyword in working_keywords):
                    data['working_sessions'] += 1
        
        # Calculate calendar scores
        for attendee, data in collaborators.items():
            data['calendar_score'] = (
                data['one_on_one'] * 30 +
                data['organized_by_user'] * 25 +
                data['organized_by_them'] * 15 +
                data['working_sessions'] * 20 +
                data['small_meetings'] * 8
            )
        
        return collaborators
    
    def combine_calendar_and_chat_data(self, calendar_collaborators: Dict) -> Dict:
        """Combine calendar collaborations with chat data"""
        combined = calendar_collaborators.copy()
        
        # Add chat data for people not in calendar
        if self.chat_data.get('chat_collaborators'):
            for name, chat_info in self.chat_data['chat_collaborators'].items():
                if name not in combined:
                    combined[name] = {
                        'calendar_meetings': 0,
                        'one_on_one': 0,
                        'organized_by_user': 0,
                        'organized_by_them': 0,
                        'small_meetings': 0,
                        'working_sessions': 0,
                        'calendar_score': 0
                    }
                
                # Add chat data
                combined[name].update({
                    'daily_chats': chat_info['daily_chats'],
                    'weekly_group_chats': chat_info['weekly_group_chats'],
                    'chat_score': chat_info['chat_score'],
                    'relationship_strength': chat_info['relationship_strength'],
                    'data_source': 'calendar+chat' if combined[name]['calendar_meetings'] > 0 else 'chat_only'
                })
        
        # Mark calendar-only collaborators
        for name, data in combined.items():
            if 'data_source' not in data:
                data['data_source'] = 'calendar_only'
                data['daily_chats'] = 0
                data['weekly_group_chats'] = 0
                data['chat_score'] = 0
                data['relationship_strength'] = 0
        
        return combined
    
    def rank_combined_collaborators(self, collaborators: Dict) -> Dict:
        """Rank collaborators using combined calendar + chat scores"""
        ranked_list = []
        
        for name, data in collaborators.items():
            # Calculate combined score
            calendar_score = data['calendar_score']
            chat_score = data.get('chat_score', 0)
            
            # Chat data heavily weighted since it represents daily interaction
            combined_score = calendar_score + (chat_score * 1.5)
            
            # Calculate collaboration indicators
            genuine_meetings = (
                data['one_on_one'] + 
                data['organized_by_user'] + 
                data['working_sessions']
            )
            
            has_genuine_collaboration = (
                genuine_meetings > 0 or 
                data.get('daily_chats', 0) > 0
            )
            
            if data['calendar_meetings'] >= 2 or data.get('daily_chats', 0) > 0:
                if has_genuine_collaboration:
                    importance_score = combined_score * 0.6 + (genuine_meetings * 10)
                    
                    ranked_list.append({
                        'name': name,
                        'importance_score': importance_score,
                        'combined_score': combined_score,
                        'calendar_score': calendar_score,
                        'chat_score': chat_score,
                        'data_source': data['data_source'],
                        'genuine_meetings': genuine_meetings,
                        'calendar_meetings': data['calendar_meetings'],
                        'daily_chats': data.get('daily_chats', 0),
                        'one_on_one': data['one_on_one'],
                        'organized_by_user': data['organized_by_user'],
                        'working_sessions': data['working_sessions']
                    })
        
        # Sort by importance score
        ranked_list.sort(key=lambda x: x['importance_score'], reverse=True)
        
        return {
            'algorithm_version': '5.0_chat_integration_ready',
            'timestamp': datetime.now().isoformat(),
            'total_collaborators': len(ranked_list),
            'chat_enhanced_count': len([c for c in ranked_list if c['chat_score'] > 0]),
            'calendar_only_count': len([c for c in ranked_list if c['data_source'] == 'calendar_only']),
            'chat_only_count': len([c for c in ranked_list if c['data_source'] == 'chat_only']),
            'collaborators': ranked_list
        }
    
    def display_results(self, results: Dict):
        """Display enhanced results with chat integration status"""
        print(f"\n🤝 ENHANCED COLLABORATOR DISCOVERY RESULTS v5.0")
        print("=" * 60)
        print(f"📅 Analysis Date: {results['timestamp'][:10]}")
        print(f"🔢 Total Collaborators: {results['total_collaborators']}")
        print(f"💬 Chat-Enhanced: {results['chat_enhanced_count']}")
        print(f"📅 Calendar-Only: {results['calendar_only_count']}")
        print(f"💬 Chat-Only: {results['chat_only_count']}")
        
        print(f"\n🏆 TOP COLLABORATORS:")
        print("-" * 60)
        
        for i, collab in enumerate(results['collaborators'][:10], 1):
            source_icon = {
                'calendar+chat': '💬📅',
                'calendar_only': '📅',
                'chat_only': '💬'
            }
            
            print(f"{i}. {collab['name']} {source_icon[collab['data_source']]}")
            print(f"   🎯 Importance: {collab['importance_score']:.1f}")
            
            if collab['data_source'] != 'chat_only':
                print(f"   📅 Calendar: {collab['calendar_meetings']} meetings, "
                      f"{collab['one_on_one']} 1:1s")
            
            if collab['data_source'] != 'calendar_only':
                print(f"   💬 Chat: {collab['daily_chats']} daily messages")
            
            print()
        
        # Data source explanation
        print("📊 DATA SOURCE LEGEND:")
        print("   💬📅 = Calendar + Chat data")
        print("   📅 = Calendar data only")
        print("   💬 = Chat data only (manual)")
        
        if results['calendar_only_count'] > 0:
            print(f"\n⚠️  WARNING: {results['calendar_only_count']} collaborators have")
            print("   calendar data only. Consider adding chat data for:")
            calendar_only = [c['name'] for c in results['collaborators'] 
                           if c['data_source'] == 'calendar_only'][:5]
            for name in calendar_only:
                print(f"   • {name}")

# Quick setup functions
def quick_add_xiaodong_liu(discovery_tool):
    """Quick function to add Xiaodong Liu chat data"""
    print("🚀 Quick Setup: Adding Xiaodong Liu chat collaboration data")
    discovery_tool.add_manual_chat_collaborator(
        name="Xiaodong Liu",
        daily_chats=5,  # Assuming frequent daily chats
        weekly_group_chats=3,  # Some group chat participation  
        relationship_strength=1  # Essential collaboration
    )

def main():
    """Main execution with enhanced chat integration"""
    print("🚀 ENHANCED COLLABORATOR DISCOVERY v5.0 - CHAT INTEGRATION READY")
    print("=" * 70)
    
    # Initialize discovery tool
    calendar_path = "meeting_prep_data/real_calendar_scenarios.json"
    discovery = EnhancedCollaboratorDiscoveryV5(calendar_path)
    
    # Check if we want to add Xiaodong Liu quickly
    add_xiaodong = input("Add Xiaodong Liu chat data? (y/n): ").lower() == 'y'
    if add_xiaodong:
        quick_add_xiaodong_liu(discovery)
    
    # Run enhanced discovery
    results = discovery.discover_collaborators_enhanced()
    
    # Display results
    discovery.display_results(results)
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"enhanced_collaborator_discovery_v5_{timestamp}.json"
    
    with open(filename, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n✅ Results saved to: {filename}")
    
    # Instructions for adding more chat data
    print(f"\n💡 TO ADD MORE CHAT COLLABORATORS:")
    print("   discovery.add_manual_chat_collaborator(")
    print("       name='Person Name',")
    print("       daily_chats=3,  # Average daily messages")
    print("       weekly_group_chats=5,  # Group chat interactions")
    print("       relationship_strength=1  # 1=Essential, 2=Regular, 3=Occasional")
    print("   )")

if __name__ == "__main__":
    main()