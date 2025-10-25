#!/usr/bin/env python3
"""
Scenara Meeting Intelligence Demo
Demonstrates integration of meeting extraction with LLM analysis
"""

from tools.meeting_extractor import ScenearaMeetingExtractor
from tools.llm_api import LLMAPIClient

def demo_meeting_intelligence():
    """Demonstrate Scenara's meeting intelligence capabilities"""
    print("🎯 Scenara Meeting Intelligence Demo")
    print("=" * 50)
    
    # Initialize tools
    extractor = ScenearaMeetingExtractor()
    llm_client = LLMAPIClient()
    
    print("\n📊 Step 1: Extract Meeting Data")
    print("-" * 30)
    
    # Extract meetings from local source (fastest for demo)
    try:
        meetings = extractor.extract_from_local_json()
        print(f"✅ Extracted {len(meetings)} meetings from local calendar")
    except Exception as e:
        print(f"⚠️ Local extraction failed, trying scenarios: {e}")
        try:
            meetings = extractor.extract_from_meeting_prep_scenarios()
            meetings = meetings[:10]  # Limit for demo
            print(f"✅ Extracted {len(meetings)} meeting scenarios")
        except Exception as e2:
            print(f"❌ All extractions failed: {e2}")
            return
    
    print(f"\n📈 Step 2: Analyze Meeting Patterns")
    print("-" * 35)
    
    # Generate summary
    summary = extractor.generate_meeting_summary(meetings)
    print(f"📅 Total Meetings: {summary['total_meetings']}")
    print(f"🏷️ Meeting Types: {dict(list(summary['meeting_types'].items())[:3])}")
    print(f"⏱️ Average Duration: {summary['duration_statistics']['average_minutes']} minutes")
    print(f"👥 Average Attendees: {summary['attendee_statistics']['average_attendees']}")
    
    print(f"\n🤖 Step 3: LLM Analysis of Key Meetings")
    print("-" * 40)
    
    # Analyze most interesting meetings with LLM
    interesting_meetings = []
    
    # Find meetings with specific characteristics
    for meeting in meetings[:5]:  # Analyze first 5 meetings
        if (meeting.get('attendee_count', 0) >= 3 or 
            meeting.get('duration_minutes', 0) >= 60 or
            meeting.get('meeting_type') in ['project_management', 'review', 'client_meeting']):
            interesting_meetings.append(meeting)
    
    for i, meeting in enumerate(interesting_meetings[:3], 1):  # Analyze top 3
        print(f"\n🔍 Meeting {i}: {meeting.get('subject', 'Untitled')[:50]}...")
        
        # Create analysis prompt
        prompt = f"""
        Analyze this meeting for preparation insights:
        
        Subject: {meeting.get('subject', 'N/A')}
        Type: {meeting.get('meeting_type', 'general')}
        Duration: {meeting.get('duration_minutes', 0)} minutes
        Attendees: {meeting.get('attendee_count', 0)} people
        
        Provide:
        1. Key preparation points (2-3 items)
        2. Potential discussion topics
        3. Success metrics
        
        Keep response concise (under 150 words).
        """
        
        try:
            analysis = llm_client.query_llm(prompt, provider="ollama")
            print(f"💡 AI Analysis:")
            print(f"   {analysis[:200]}...")
            if len(analysis) > 200:
                print("   [Analysis truncated for demo]")
        except Exception as e:
            print(f"⚠️ LLM analysis failed: {e}")
            print("💡 Demo Analysis:")
            print(f"   • Prepare agenda for {meeting.get('duration_minutes', 0)}-minute {meeting.get('meeting_type', 'general')} meeting")
            print(f"   • Review attendee backgrounds ({meeting.get('attendee_count', 0)} participants)")
            print(f"   • Set clear objectives and success criteria")
    
    print(f"\n🔧 Step 4: Integration Capabilities")
    print("-" * 35)
    
    print("✅ Available Integrations:")
    print("   📊 Meeting data extraction (Microsoft Graph, MEvals, local JSON)")
    print("   🤖 LLM analysis and preparation (Ollama gpt-oss:20b)")
    print("   🌐 Web research for meeting topics")
    print("   📸 Screenshot documentation workflow")
    print("   📋 Task management and lessons learned tracking")
    
    print(f"\n🎉 Scenara Meeting Intelligence Demo Complete!")
    print("=" * 50)
    print("💡 Next Steps:")
    print("   1. Run: python tools/meeting_extractor.py --source all")
    print("   2. Integrate with daily workflow automation")
    print("   3. Set up recurring meeting preparation pipeline")
    print("   4. Customize LLM prompts for specific meeting types")

if __name__ == "__main__":
    demo_meeting_intelligence()