#!/usr/bin/env python3
"""
Manual Teams Chat Collaboration Discovery

This tool helps manually identify close collaborators who primarily 
communicate through Teams chat rather than calendar meetings.

Since we can't access Teams chat data automatically due to Microsoft Graph
API limitations, this tool provides a framework for manual data collection.
"""

import json
from datetime import datetime
from typing import Dict, List, Tuple

class ManualChatCollaboratorDiscovery:
    def __init__(self):
        self.chat_data = {}
        
    def collect_manual_chat_data(self):
        """
        Interactive data collection for Teams chat patterns
        """
        print("🔍 MANUAL TEAMS CHAT COLLABORATION DISCOVERY")
        print("=" * 55)
        print("\nSince we can't access Teams chat data automatically,")
        print("please provide the following information manually:\n")
        
        collaborators = []
        
        while True:
            print(f"\n👤 Collaborator #{len(collaborators) + 1}")
            print("-" * 25)
            
            name = input("Name (or 'done' to finish): ").strip()
            if name.lower() == 'done':
                break
                
            # Chat frequency
            print("\n📊 Chat Activity (last 30 days):")
            daily_chats = self._get_numeric_input("Direct messages per day (average): ", default=0)
            group_chats = self._get_numeric_input("Group chat interactions per week: ", default=0)
            
            # Meeting patterns
            print("\n📅 Meeting Patterns:")
            calendar_meetings = self._get_numeric_input("Calendar meetings together (last 30 days): ", default=0)
            ad_hoc_calls = self._get_numeric_input("Ad-hoc Teams calls (not on calendar): ", default=0)
            
            # Collaboration type
            print("\n🤝 Collaboration Type:")
            print("1. Daily operational collaboration")
            print("2. Project-based collaboration") 
            print("3. Mentoring/support relationship")
            print("4. Cross-team coordination")
            print("5. Informal/social interaction")
            
            collab_type = self._get_numeric_input("Select type (1-5): ", min_val=1, max_val=5, default=1)
            
            # Relationship strength
            print("\n💪 Relationship Strength:")
            print("1. Essential daily collaboration")
            print("2. Regular weekly collaboration")
            print("3. Occasional project collaboration")
            print("4. Infrequent interaction")
            
            strength = self._get_numeric_input("Select strength (1-4): ", min_val=1, max_val=4, default=2)
            
            collaborator = {
                'name': name,
                'daily_chats': daily_chats,
                'weekly_group_chats': group_chats,
                'calendar_meetings': calendar_meetings,
                'ad_hoc_calls': ad_hoc_calls,
                'collaboration_type': collab_type,
                'relationship_strength': strength,
                'chat_score': self._calculate_chat_score(daily_chats, group_chats, strength),
                'total_score': self._calculate_total_score(
                    daily_chats, group_chats, calendar_meetings, ad_hoc_calls, strength
                )
            }
            
            collaborators.append(collaborator)
            print(f"✅ Added {name} (Chat Score: {collaborator['chat_score']:.1f})")
        
        return self._analyze_and_rank(collaborators)
    
    def _get_numeric_input(self, prompt: str, min_val: int = 0, max_val: int = None, default: int = 0) -> int:
        """Get numeric input with validation"""
        while True:
            try:
                response = input(prompt).strip()
                if not response:
                    return default
                value = int(response)
                if value < min_val:
                    print(f"❌ Value must be >= {min_val}")
                    continue
                if max_val and value > max_val:
                    print(f"❌ Value must be <= {max_val}")
                    continue
                return value
            except ValueError:
                print("❌ Please enter a valid number")
    
    def _calculate_chat_score(self, daily_chats: int, group_chats: int, strength: int) -> float:
        """Calculate collaboration score based on chat activity"""
        base_score = (daily_chats * 30) * 3  # Daily DMs heavily weighted
        base_score += group_chats * 1         # Group chats moderately weighted
        
        # Strength multiplier
        strength_multiplier = {1: 1.5, 2: 1.2, 3: 1.0, 4: 0.7}
        
        return base_score * strength_multiplier.get(strength, 1.0)
    
    def _calculate_total_score(self, daily_chats: int, group_chats: int, 
                              calendar_meetings: int, ad_hoc_calls: int, strength: int) -> float:
        """Calculate total collaboration score including meetings"""
        chat_score = self._calculate_chat_score(daily_chats, group_chats, strength)
        meeting_score = calendar_meetings * 15  # Calendar meetings
        call_score = ad_hoc_calls * 20         # Ad-hoc calls highly weighted
        
        return chat_score + meeting_score + call_score
    
    def _analyze_and_rank(self, collaborators: List[Dict]) -> Dict:
        """Analyze and rank collaborators"""
        # Sort by total score
        ranked = sorted(collaborators, key=lambda x: x['total_score'], reverse=True)
        
        analysis = {
            'timestamp': datetime.now().isoformat(),
            'total_collaborators': len(ranked),
            'chat_heavy_collaborators': len([c for c in ranked if c['chat_score'] > c['total_score'] * 0.7]),
            'meeting_heavy_collaborators': len([c for c in ranked if c['chat_score'] < c['total_score'] * 0.3]),
            'ranked_collaborators': ranked
        }
        
        return analysis
    
    def display_results(self, analysis: Dict):
        """Display analysis results"""
        print("\n🏆 MANUAL CHAT COLLABORATION ANALYSIS RESULTS")
        print("=" * 55)
        
        print(f"📊 Total Collaborators Analyzed: {analysis['total_collaborators']}")
        print(f"💬 Chat-Heavy Collaborators: {analysis['chat_heavy_collaborators']}")
        print(f"📅 Meeting-Heavy Collaborators: {analysis['meeting_heavy_collaborators']}")
        
        print(f"\n🏆 TOP COLLABORATORS (Including Chat Activity):")
        print("-" * 55)
        
        for i, collab in enumerate(analysis['ranked_collaborators'][:10], 1):
            strength_labels = {1: "Essential", 2: "Regular", 3: "Occasional", 4: "Infrequent"}
            type_labels = {
                1: "Daily Ops", 2: "Project", 3: "Mentoring", 
                4: "Cross-team", 5: "Informal"
            }
            
            print(f"{i}. {collab['name']}")
            print(f"   🎯 Total Score: {collab['total_score']:.1f}")
            print(f"   💬 Chat Score: {collab['chat_score']:.1f}")
            print(f"   📊 Daily Chats: {collab['daily_chats']}")
            print(f"   📅 Calendar Meetings: {collab['calendar_meetings']}")
            print(f"   🤝 Type: {type_labels[collab['collaboration_type']]}")
            print(f"   💪 Strength: {strength_labels[collab['relationship_strength']]}")
            print()
        
        return analysis
    
    def save_results(self, analysis: Dict, filename: str = None):
        """Save results to JSON file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"manual_chat_collaboration_analysis_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(analysis, f, indent=2)
        
        print(f"💾 Results saved to: {filename}")
        return filename

def main():
    """Main execution function"""
    print("🚀 STARTING MANUAL TEAMS CHAT COLLABORATION DISCOVERY")
    print("=" * 60)
    print("\nThis tool helps identify close collaborators who primarily")
    print("communicate through Teams chat rather than calendar meetings.\n")
    
    discovery = ManualChatCollaboratorDiscovery()
    
    # Collect manual data
    analysis = discovery.collect_manual_chat_data()
    
    if analysis['total_collaborators'] > 0:
        # Display results
        discovery.display_results(analysis)
        
        # Save results
        filename = discovery.save_results(analysis)
        
        print(f"\n✅ ANALYSIS COMPLETE!")
        print(f"📁 Results saved to: {filename}")
        print(f"\n💡 Use this data to enhance the collaboration algorithm")
        print(f"   by manually adding chat collaboration scores!")
    else:
        print("\n❌ No collaborators data collected.")

if __name__ == "__main__":
    main()