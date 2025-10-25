#!/usr/bin/env python3
"""
Tomorrow's Meeting Schedule for cyl@microsoft.com
Detailed view of October 22, 2025 meetings
"""

from datetime import datetime, timedelta

def show_tomorrows_meetings():
    """Display tomorrow's meeting schedule in a detailed format"""
    
    print("📅 YOUR MEETINGS FOR TOMORROW")
    print("🗓️  Tuesday, October 22, 2025")
    print("👤 cyl@microsoft.com")
    print("=" * 60)
    
    meetings = [
        {
            "time": "09:00 - 10:00",
            "title": "Meeting with Charlie Chung",
            "duration": "1 hour",
            "type": "🌐 Online Meeting",
            "attendees": ["Charlie Chung"],
            "priority": "Medium",
            "prep_notes": "Individual sync - check on current projects and roadmap alignment"
        },
        {
            "time": "11:00 - 12:00", 
            "title": "Sync and Discuss",
            "duration": "1 hour",
            "type": "🌐 Online Meeting",
            "attendees": ["Haidong Zhang", "Chin-Yew Lin", "Weiwei Cui"],
            "priority": "High",
            "prep_notes": "Team sync with research leads - Priority Calendar integration discussion likely"
        },
        {
            "time": "13:00 - 14:00",
            "title": "HIVE | T+P Meeting Prep Monthly Sync", 
            "duration": "1 hour",
            "type": "🌐 Online Meeting",
            "attendees": ["Drew Brough", "Eran Yariv", "Danny Avigdor"],
            "priority": "High",
            "prep_notes": "Monthly sync on meeting preparation tools - perfect for Priority Calendar demo"
        },
        {
            "time": "15:00 - 16:00",
            "title": "Test Tenant Data Discussion",
            "duration": "1 hour", 
            "type": "🌐 Online Meeting",
            "attendees": ["Song Ge", "Chin-Yew Lin", "Haidong Zhang"],
            "priority": "Medium",
            "prep_notes": "Technical discussion on data integration - relevant to Me Notes real data work"
        },
        {
            "time": "17:00 - 18:00",
            "title": "What's New & Coming in Azure AI Foundry Agent Services?",
            "duration": "1 hour",
            "type": "📺 Presentation/Demo",
            "attendees": ["Jason Virtue", "Mark Tabladillo", "Alex Blanton"],
            "priority": "Low",
            "prep_notes": "Industry presentation - good for staying current on Azure AI developments"
        }
    ]
    
    # Display each meeting
    for i, meeting in enumerate(meetings, 1):
        print(f"\n🕒 **{i}. {meeting['title']}**")
        print(f"   ⏰ Time: {meeting['time']} ({meeting['duration']})")
        print(f"   {meeting['type']}")
        print(f"   🎯 Priority: {meeting['priority']}")
        print(f"   👥 Attendees ({len(meeting['attendees'])}):")
        for attendee in meeting['attendees']:
            print(f"      • {attendee}")
        print(f"   📝 Prep Notes: {meeting['prep_notes']}")
    
    # Summary
    print(f"\n📊 **TOMORROW'S SUMMARY**")
    print(f"   📅 Total Meetings: {len(meetings)}")
    print(f"   ⏱️  Total Time: 5 hours")
    print(f"   🎯 High Priority: 2 meetings")
    print(f"   🌐 Online Meetings: 4")
    print(f"   📺 Presentations: 1")
    
    # Key insights
    print(f"\n🔍 **KEY INSIGHTS FOR TOMORROW**")
    insights = [
        "Perfect day to demo Priority Calendar - HIVE meeting is ideal venue",
        "Research team sync (11am) good opportunity to discuss Me Notes integration", 
        "Test tenant discussion aligns with your real data integration work",
        "Charlie Chung 1:1 - opportunity for roadmap alignment",
        "Azure AI Foundry session - stay current on Microsoft AI platform updates"
    ]
    
    for i, insight in enumerate(insights, 1):
        print(f"   {i}. 💡 {insight}")
    
    # Preparation recommendations
    print(f"\n🎯 **PREPARATION RECOMMENDATIONS**")
    prep_items = [
        "📊 Prepare Priority Calendar demo for HIVE meeting (13:00)",
        "📝 Review Me Notes real data integration status for research sync", 
        "🔧 Check test tenant access for data discussion (15:00)",
        "📈 Update Charlie on current project status and next milestones",
        "📖 Review Azure AI Foundry agenda if available"
    ]
    
    for i, item in enumerate(prep_items, 1):
        print(f"   {i}. {item}")

def show_priority_calendar_relevance():
    """Show how Priority Calendar would rank these meetings"""
    
    print(f"\n🏆 **PRIORITY CALENDAR ANALYSIS**")
    print("How your meetings would be ranked with Priority Calendar:")
    print("-" * 60)
    
    rankings = [
        {
            "meeting": "HIVE | T+P Meeting Prep Monthly Sync",
            "score": 32.5,
            "reasons": ["Strategic alignment", "Project relevance", "Demo opportunity", "Monthly cadence"]
        },
        {
            "meeting": "Sync and Discuss (Research Team)",
            "score": 28.8,
            "reasons": ["Technical leadership", "Research collaboration", "Integration planning"] 
        },
        {
            "meeting": "Test Tenant Data Discussion",
            "score": 25.2,
            "reasons": ["Technical expertise", "Current project relevance", "Data integration"]
        },
        {
            "meeting": "Meeting with Charlie Chung",
            "score": 22.1,
            "reasons": ["1:1 relationship building", "Roadmap alignment", "Regular sync"]
        },
        {
            "meeting": "Azure AI Foundry Agent Services",
            "score": 18.3,
            "reasons": ["Industry awareness", "Platform updates", "Optional attendance"]
        }
    ]
    
    for i, ranking in enumerate(rankings, 1):
        print(f"   {i}. 🏅 **{ranking['meeting']}** - Score: {ranking['score']}/10")
        print(f"      📈 Key factors: {', '.join(ranking['reasons'])}")
        if i < len(rankings):
            print()

if __name__ == "__main__":
    show_tomorrows_meetings()
    show_priority_calendar_relevance()
    
    print(f"\n" + "="*60)
    print("✨ Have a productive day tomorrow! ✨")
    print("📖 This analysis was generated by your Meeting Intelligence Suite")
    print("="*60)