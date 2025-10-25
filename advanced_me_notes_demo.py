#!/usr/bin/env python3
"""
Complete Me Notes Integration Demo
Shows integration between enhanced Me Notes and Meeting Ranking systems
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta
import json

# Add project paths
sys.path.append(str(Path(__file__).parent))

from enhanced_me_notes_viewer import EnhancedMeNotesAPI
from me_notes_enhanced_ranking import MeNotesEnhancedRanker, create_enhanced_demo_user_profile

def demo_complete_integration():
    """Demonstrate complete integration between Me Notes and Meeting Ranking"""
    
    print("🚀 Complete Me Notes Integration Demo")
    print("=" * 50)
    
    user_email = "cyl@microsoft.com"
    
    # 1. Enhanced Me Notes Analysis
    print(f"\n1. 📊 Enhanced Me Notes Analysis for {user_email}")
    print("-" * 40)
    
    me_notes_api = EnhancedMeNotesAPI(user_email)
    me_notes = me_notes_api.fetch_me_notes(days_back=30)
    
    print(f"✅ Retrieved {len(me_notes)} enhanced Me Notes")
    print(f"🏢 Company Context: {me_notes_api.user_context['company']}")
    
    # Show category breakdown
    categories = {}
    for note in me_notes:
        cat = note.category.value
        categories[cat] = categories.get(cat, 0) + 1
    
    print("\n📋 Category Breakdown:")
    for cat, count in categories.items():
        icons = {"WORK_RELATED": "💼", "EXPERTISE": "🎯", "BEHAVIORAL_PATTERN": "🧭", 
                "INTERESTS": "💡", "FOLLOW_UPS": "📋"}
        print(f"   {icons.get(cat, '📝')} {cat.replace('_', ' ').title()}: {count}")
    
    # 2. Key Insights Extraction
    print(f"\n2. 🎯 Key Insights Extraction")
    print("-" * 30)
    
    work_projects = []
    expertise_areas = []
    collaborators = []
    
    for note in me_notes:
        if note.category.value == "WORK_RELATED":
            if "Priority Calendar" in note.note:
                work_projects.append("Priority Calendar")
            if "Graph" in note.note:
                work_projects.append("Microsoft Graph")
            if "AI" in note.note or "LLM" in note.note:
                work_projects.append("AI/LLM Integration")
        
        elif note.category.value == "EXPERTISE":
            if "calendar" in note.note.lower():
                expertise_areas.append("Calendar Intelligence")
            if "API" in note.note:
                expertise_areas.append("API Integration")
            if "AI" in note.note or "ML" in note.note:
                expertise_areas.append("AI/ML")
        
        elif note.category.value == "FOLLOW_UPS":
            # Extract names (simplified)
            if "Sarah Chen" in note.note:
                collaborators.append("Sarah Chen")
            if "Mike Johnson" in note.note:
                collaborators.append("Mike Johnson")
    
    print(f"💼 Active Projects: {list(set(work_projects))}")
    print(f"🎯 Expertise Areas: {list(set(expertise_areas))}")
    print(f"👥 Recent Collaborators: {list(set(collaborators))}")
    
    # 3. Meeting Scenarios Based on Me Notes
    print(f"\n3. 🗓️ Meeting Scenarios Enhanced by Me Notes")
    print("-" * 45)
    
    # Create realistic meetings based on the Me Notes context
    enhanced_meetings = [
        {
            "id": "meeting_001",
            "subject": "Priority Calendar Architecture Review with Sarah Chen",
            "organizer": "sarah.chen@microsoft.com",
            "attendees": ["cyl@microsoft.com", "sarah.chen@microsoft.com", "mike.johnson@microsoft.com"],
            "start": {"dateTime": (datetime.now() + timedelta(days=1)).isoformat()},
            "responseStatus": "accepted",
            "isOrganizer": False,
            "importance": "high"
        },
        {
            "id": "meeting_002", 
            "subject": "Graph API Integration Planning",
            "organizer": "graph-team@microsoft.com",
            "attendees": ["cyl@microsoft.com", "api-team@microsoft.com"],
            "start": {"dateTime": (datetime.now() + timedelta(days=2)).isoformat()},
            "responseStatus": "tentative",
            "isOrganizer": False,
            "importance": "normal"
        },
        {
            "id": "meeting_003",
            "subject": "AI Productivity Research Sync",
            "organizer": "cyl@microsoft.com", 
            "attendees": ["cyl@microsoft.com", "ai-research@microsoft.com"],
            "start": {"dateTime": (datetime.now() + timedelta(days=3)).isoformat()},
            "responseStatus": "accepted",
            "isOrganizer": True,
            "importance": "high"
        }
    ]
    
    print("📅 Generated Meeting Scenarios:")
    for meeting in enhanced_meetings:
        print(f"   • {meeting['subject']}")
        print(f"     👤 Organizer: {meeting['organizer']}")
        print(f"     📊 Importance: {meeting['importance']}")
        print()
    
    # 4. Me Notes Enhanced Meeting Ranking
    print(f"\n4. 🎯 Me Notes Enhanced Meeting Ranking")
    print("-" * 40)
    
    try:
        # Create enhanced user profile
        user_profile = create_enhanced_demo_user_profile()
        user_profile.email = user_email
        
        # Initialize enhanced ranker
        ranker = MeNotesEnhancedRanker(
            model_name="gemma2:latest",
            user_profile=user_profile
        )
        
        print("🔄 Ranking meetings with Me Notes enhancement...")
        ranking_results = ranker.rank_meetings(enhanced_meetings)
        
        print(f"✅ Ranked {len(ranking_results)} meetings")
        print("\n📊 Enhanced Ranking Results:")
        
        for i, result in enumerate(ranking_results, 1):
            priority_emoji = "🔴" if result.priority_score >= 8 else "🟡" if result.priority_score >= 6 else "🟢"
            print(f"{i}. {priority_emoji} **{result.subject}** ({result.priority_score:.1f}/10)")
            print(f"   🎯 Engagement: {result.engagement_level}")
            print(f"   📝 Signals: {len(result.signals_detected)} detected")
            print(f"   🧠 Reasoning: {result.reasoning[:100]}...")
            print()
        
    except Exception as e:
        print(f"⚠️ Enhanced ranking unavailable: {e}")
        print("💡 This requires Ollama LLM integration")
    
    # 5. Integration Benefits Summary
    print(f"\n5. 🏆 Integration Benefits Summary")
    print("-" * 35)
    
    benefits = [
        "🎯 **Hyper-Personalized Priority Scores**: Meetings aligned with active projects get higher priority",
        "👥 **Relationship-Aware Ranking**: Meetings with known collaborators are prioritized appropriately", 
        "🧠 **Context-Driven Reasoning**: LLM explanations include personal work context and relationships",
        "📊 **Expertise Matching**: Meetings in your areas of expertise receive appropriate weighting",
        "🔄 **Dynamic Adaptation**: System learns from your actual work patterns and interactions",
        "🏢 **Company-Specific Intelligence**: Microsoft context provides realistic team and project awareness"
    ]
    
    for benefit in benefits:
        print(f"   {benefit}")
    
    print(f"\n🎉 Complete integration demo finished!")
    print("💡 This shows the power of combining Me Notes with Meeting Intelligence!")

def demo_cross_user_comparison():
    """Show how different users get different contextual data"""
    
    print("\n🔍 Cross-User Context Comparison")
    print("=" * 40)
    
    users = [
        "cyl@microsoft.com",
        "sarah@google.com", 
        "john@apple.com"
    ]
    
    for user in users:
        print(f"\n👤 User: {user}")
        api = EnhancedMeNotesAPI(user)
        ctx = api.user_context
        
        print(f"   🏢 Company: {ctx['company']}")
        print(f"   👥 Collaborators: {', '.join(ctx['likely_collaborators'][:2])}")
        print(f"   🔧 Teams: {', '.join(ctx['microsoft_teams'][:2])}")
        print(f"   💼 Projects: {', '.join(ctx['common_projects'][:2])}")

def main():
    """Main demo runner"""
    
    print("🧠 Advanced Me Notes Integration Showcase")
    print("=" * 50)
    print()
    print("This demo shows the complete integration between:")
    print("1. Enhanced Me Notes with user-specific context")
    print("2. Meeting Ranking with personal intelligence")
    print("3. Cross-system data flow and benefits")
    print()
    
    try:
        # Run main integration demo
        demo_complete_integration()
        
        # Show cross-user comparison
        demo_cross_user_comparison()
        
        print(f"\n🚀 Advanced Demo Complete!")
        print("✨ This demonstrates the full potential of personalized meeting intelligence!")
        
    except Exception as e:
        print(f"❌ Demo error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()