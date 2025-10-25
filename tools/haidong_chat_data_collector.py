#!/usr/bin/env python3
"""
Manual Teams Chat Data Collection for Haidong Zhang

This tool helps manually collect Teams chat data between Chin-Yew Lin and 
Haidong Zhang to provide complete collaboration analysis.

Based on user feedback: "have you consider chat history between me and haidong 
and group chats where haidong also a member of?"
"""

import json
from datetime import datetime
from typing import Dict, List

class ManualTeamsChatCollector:
    def __init__(self):
        self.chat_data = {}
        
    def collect_haidong_chat_data(self):
        """Collect Teams chat data between Chin-Yew Lin and Haidong Zhang"""
        
        print("💬 MANUAL TEAMS CHAT DATA COLLECTION: HAIDONG ZHANG")
        print("=" * 60)
        print("Please provide Teams chat activity data between you and Haidong Zhang")
        print("(Check your Teams chat history for accurate numbers)")
        print()
        
        # Direct Messages (1:1 Chat)
        print("📱 DIRECT MESSAGES (1:1 Chat)")
        print("-" * 30)
        daily_dms = self._get_numeric_input(
            "Average daily direct messages with Haidong (last 30 days): ", 
            default=0, max_val=50
        )
        
        file_shares_dm = self._get_numeric_input(
            "Files shared in DMs (last 30 days): ", 
            default=0, max_val=20
        )
        
        # Group Chats
        print("\n👥 GROUP CHATS")
        print("-" * 15)
        shared_group_chats = self._get_numeric_input(
            "Number of group chats you both participate in: ", 
            default=0, max_val=10
        )
        
        if shared_group_chats > 0:
            weekly_group_messages = self._get_numeric_input(
                "Your messages per week in shared group chats: ", 
                default=0, max_val=100
            )
            
            haidong_mentions = self._get_numeric_input(
                "@mentions of Haidong in group chats (last 30 days): ", 
                default=0, max_val=20
            )
            
            mentions_by_haidong = self._get_numeric_input(
                "@mentions by Haidong of you (last 30 days): ", 
                default=0, max_val=20
            )
        else:
            weekly_group_messages = 0
            haidong_mentions = 0
            mentions_by_haidong = 0
        
        # Voice/Video Calls in Teams
        print("\n📞 TEAMS CALLS (Not on Calendar)")
        print("-" * 35)
        ad_hoc_calls = self._get_numeric_input(
            "Ad-hoc Teams calls with Haidong (last 30 days): ", 
            default=0, max_val=15
        )
        
        # Chat Engagement Quality
        print("\n💪 CHAT ENGAGEMENT QUALITY")
        print("-" * 30)
        print("Rate the typical engagement level in your chats:")
        print("1. Quick operational messages only")
        print("2. Mix of operational and project discussion") 
        print("3. Deep project discussions and brainstorming")
        print("4. Strategic planning and decision making")
        
        engagement_level = self._get_numeric_input(
            "Select engagement level (1-4): ", 
            min_val=1, max_val=4, default=2
        )
        
        # Communication Frequency Pattern
        print("\n🕐 COMMUNICATION FREQUENCY")
        print("-" * 28)
        print("How often do you typically communicate with Haidong via Teams?")
        print("1. Multiple times per day")
        print("2. Daily")
        print("3. Few times per week")
        print("4. Weekly")
        print("5. Bi-weekly or less")
        
        frequency_pattern = self._get_numeric_input(
            "Select frequency (1-5): ", 
            min_val=1, max_val=5, default=2
        )
        
        # Calculate chat collaboration score
        chat_score = self._calculate_haidong_chat_score(
            daily_dms, file_shares_dm, weekly_group_messages, 
            haidong_mentions, mentions_by_haidong, ad_hoc_calls,
            engagement_level, frequency_pattern
        )
        
        # Store data
        haidong_data = {
            'name': 'Haidong Zhang',
            'daily_dms': daily_dms,
            'file_shares_dm': file_shares_dm,
            'shared_group_chats': shared_group_chats,
            'weekly_group_messages': weekly_group_messages,
            'haidong_mentions': haidong_mentions,
            'mentions_by_haidong': mentions_by_haidong,
            'ad_hoc_calls': ad_hoc_calls,
            'engagement_level': engagement_level,
            'frequency_pattern': frequency_pattern,
            'chat_collaboration_score': chat_score,
            'collection_date': datetime.now().isoformat()
        }
        
        return haidong_data
    
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
    
    def _calculate_haidong_chat_score(self, daily_dms: int, file_shares: int, 
                                    weekly_group: int, mentions_to: int, 
                                    mentions_from: int, calls: int,
                                    engagement: int, frequency: int) -> float:
        """Calculate comprehensive chat collaboration score for Haidong"""
        
        # Base messaging score
        base_score = daily_dms * 30 * 3  # Daily DMs heavily weighted
        base_score += weekly_group * 4 * 1.5  # Weekly group participation
        
        # Interaction quality bonuses
        base_score += file_shares * 10      # File sharing shows collaboration
        base_score += mentions_to * 5       # @mentions indicate engagement
        base_score += mentions_from * 5     # Bidirectional engagement
        base_score += calls * 15            # Ad-hoc calls show urgency/importance
        
        # Engagement quality multiplier
        engagement_multiplier = {1: 0.8, 2: 1.0, 3: 1.3, 4: 1.6}
        base_score *= engagement_multiplier.get(engagement, 1.0)
        
        # Frequency pattern multiplier  
        frequency_multiplier = {1: 1.5, 2: 1.3, 3: 1.1, 4: 1.0, 5: 0.8}
        base_score *= frequency_multiplier.get(frequency, 1.0)
        
        return base_score
    
    def update_collaboration_rankings(self, haidong_chat_data: Dict):
        """Update collaboration rankings with Haidong's chat data"""
        
        print(f"\n📊 UPDATED COLLABORATION ANALYSIS WITH HAIDONG CHAT DATA")
        print("=" * 60)
        
        # Previous scores
        previous_scores = {
            "Haidong Zhang": {
                "calendar_score": 345.4,
                "document_score": 185.0 * 2,  # Document collaboration weighted 2x
                "chat_score": 0  # Was missing!
            },
            "Xiaodong Liu": {
                "calendar_score": 0,
                "document_score": 0, 
                "chat_score": 611.5  # High chat activity
            },
            "Caroline Mao": {
                "calendar_score": 133.4,
                "document_score": 15.0 * 2,
                "chat_score": 0
            }
        }
        
        # Update Haidong's chat score
        previous_scores["Haidong Zhang"]["chat_score"] = haidong_chat_data["chat_collaboration_score"]
        
        # Calculate final scores
        final_rankings = []
        for person, scores in previous_scores.items():
            total_score = scores["calendar_score"] + scores["document_score"] + scores["chat_score"]
            final_rankings.append({
                "name": person,
                "total_score": total_score,
                "calendar_score": scores["calendar_score"],
                "document_score": scores["document_score"], 
                "chat_score": scores["chat_score"]
            })
        
        # Sort by total score
        final_rankings.sort(key=lambda x: x["total_score"], reverse=True)
        
        print("🏆 FINAL COLLABORATION RANKINGS (Complete Data):")
        print("-" * 55)
        
        for i, person in enumerate(final_rankings, 1):
            name = person["name"]
            total = person["total_score"]
            calendar = person["calendar_score"] 
            documents = person["document_score"]
            chat = person["chat_score"]
            
            print(f"{i}. {name}")
            print(f"   🎯 Total Score: {total:.1f}")
            print(f"   📅 Calendar: {calendar:.1f}")
            print(f"   📄 Documents: {documents:.1f}")
            print(f"   💬 Chat: {chat:.1f}")
            
            # Identify primary collaboration mode
            max_component = max(calendar, documents, chat)
            if max_component == chat:
                print(f"   🎯 Primary Mode: Teams Chat")
            elif max_component == documents:
                print(f"   🎯 Primary Mode: Document Co-Authoring")
            else:
                print(f"   🎯 Primary Mode: Calendar Meetings")
            print()
        
        # Show Haidong's detailed chat breakdown
        if haidong_chat_data["chat_collaboration_score"] > 0:
            print("📱 HAIDONG ZHANG CHAT BREAKDOWN:")
            print("-" * 35)
            print(f"   Daily DMs: {haidong_chat_data['daily_dms']}")
            print(f"   File shares: {haidong_chat_data['file_shares_dm']}")
            print(f"   Group chats: {haidong_chat_data['shared_group_chats']}")
            print(f"   Weekly group messages: {haidong_chat_data['weekly_group_messages']}")
            print(f"   @mentions (to Haidong): {haidong_chat_data['haidong_mentions']}")
            print(f"   @mentions (from Haidong): {haidong_chat_data['mentions_by_haidong']}")
            print(f"   Ad-hoc calls: {haidong_chat_data['ad_hoc_calls']}")
            print(f"   Engagement level: {haidong_chat_data['engagement_level']}/4")
            print(f"   Frequency pattern: {haidong_chat_data['frequency_pattern']}/5")
        
        return final_rankings
    
    def save_haidong_data(self, haidong_data: Dict, filename: str = None):
        """Save Haidong's chat data to JSON"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"haidong_zhang_chat_data_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(haidong_data, f, indent=2)
        
        print(f"💾 Haidong's chat data saved to: {filename}")
        return filename

def main():
    """Main execution for Haidong Zhang chat data collection"""
    print("🚀 TEAMS CHAT DATA COLLECTION: HAIDONG ZHANG")
    print("=" * 55)
    print("Addressing: 'have you consider chat history between me and haidong")
    print("and group chats where haidong also a member of?'")
    print()
    print("This tool collects comprehensive Teams chat data to provide")
    print("accurate collaboration analysis for Haidong Zhang.")
    print()
    
    collector = ManualTeamsChatCollector()
    
    # Collect Haidong's chat data
    haidong_data = collector.collect_haidong_chat_data()
    
    print(f"\n✅ HAIDONG ZHANG CHAT DATA COLLECTED!")
    print(f"💬 Chat Collaboration Score: {haidong_data['chat_collaboration_score']:.1f}")
    
    # Update collaboration rankings
    final_rankings = collector.update_collaboration_rankings(haidong_data)
    
    # Save data
    filename = collector.save_haidong_data(haidong_data)
    
    print(f"\n🎯 KEY INSIGHT:")
    if final_rankings[0]["name"] == "Haidong Zhang":
        print("   ✅ Haidong Zhang confirmed as #1 collaborator!")
        print("   📊 Complete data shows true collaboration intensity")
    else:
        print(f"   🔄 Top collaborator: {final_rankings[0]['name']}")
        print("   📊 Chat data provides more complete picture")
    
    print(f"\n💡 NEXT STEPS:")
    print("   1. Verify chat numbers by checking Teams history")
    print("   2. Add this data to enhanced_collaborator_discovery_v5.py")
    print("   3. Request Microsoft Graph Chat.Read permissions for automation")

if __name__ == "__main__":
    main()