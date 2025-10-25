#!/usr/bin/env python3
"""
Meeting Intelligence Pipeline: Extract → Rank → Display
Integrates Meeting Extraction Tool with Meeting Ranking Tool using Ollama LLM
"""

import sys
from pathlib import Path
from datetime import datetime
import json

# Add project root to path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

from meeting_ranking_tool import OllamaMeetingRanker, create_demo_user_profile
from daily_meeting_viewer import ScenaraDailyMeetingViewer

class MeetingIntelligencePipeline:
    """
    Complete meeting intelligence pipeline that:
    1. Extracts meetings from Graph API/local data
    2. Ranks meetings using Priority Calendar framework
    3. Displays intelligent calendar views
    4. Provides automated recommendations
    """
    
    def __init__(self, user_profile=None, ollama_model="gemma2:latest"):
        """Initialize the meeting intelligence pipeline"""
        self.user_profile = user_profile or create_demo_user_profile()
        
        # Initialize components
        self.extractor = ScenaraDailyMeetingViewer()
        self.ranker = OllamaMeetingRanker(
            model_name=ollama_model,
            user_profile=self.user_profile
        )
        
        print("🚀 Meeting Intelligence Pipeline Initialized")
        print(f"👤 User: {self.user_profile.email}")
        print(f"🤖 LLM Model: {ollama_model}")
    
    def process_daily_meetings(self, date_str: str, use_graph_api: bool = False):
        """
        Complete pipeline: Extract → Rank → Display meetings for a specific date
        
        Args:
            date_str: Date in YYYYMMDD format (e.g., "20251021")
            use_graph_api: Whether to use real Graph API or demo data
        """
        print(f"\n📅 Processing meetings for {date_str}")
        print("=" * 50)
        
        # Step 1: Extract meetings
        if use_graph_api:
            print("📡 Extracting meetings from Microsoft Graph API...")
            try:
                meetings = self.extractor.get_meetings_for_date(date_str)
                print(f"✅ Extracted {len(meetings)} meetings from Graph API")
            except Exception as e:
                print(f"❌ Graph API failed: {e}")
                print("🔄 Falling back to demo data...")
                meetings = self._get_demo_meetings_for_date(date_str)
        else:
            print("🧪 Using demo meeting data...")
            meetings = self._get_demo_meetings_for_date(date_str)
        
        if not meetings:
            print("📭 No meetings found for this date")
            return None
        
        # Step 2: Rank meetings using Priority Calendar
        print(f"\n🎯 Ranking {len(meetings)} meetings using Priority Calendar framework...")
        ranked_meetings = self.ranker.rank_meetings(meetings)
        
        # Step 3: Display intelligent calendar views
        print("\n📊 Generating intelligent calendar views...")
        
        # Console view (immediate feedback)
        console_view = self.ranker.display_ranked_meetings(ranked_meetings, "console")
        print(console_view)
        
        # Save comprehensive reports
        saved_files = self.ranker.save_ranking_results(
            ranked_meetings, 
            output_dir="daily_intelligence",
            date_suffix=date_str
        )
        
        print(f"\n💾 Saved intelligence reports:")
        for format_type, filepath in saved_files.items():
            print(f"📄 {format_type.upper()}: {filepath}")
        
        # Step 4: Generate automated recommendations
        recommendations = self._generate_pipeline_recommendations(ranked_meetings)
        
        print("\n🤖 Automated Recommendations:")
        for rec in recommendations:
            print(f"   {rec}")
        
        return {
            "date": date_str,
            "total_meetings": len(meetings),
            "ranked_meetings": ranked_meetings,
            "saved_files": saved_files,
            "recommendations": recommendations
        }
    
    def _get_demo_meetings_for_date(self, date_str: str):
        """Get demo meetings for testing"""
        from meeting_ranking_tool import create_demo_meetings
        
        # Create demo meetings with date-specific IDs
        demo_meetings = create_demo_meetings()
        
        # Update meeting IDs to include date
        for i, meeting in enumerate(demo_meetings):
            meeting['id'] = f"{date_str}_meeting_{i+1}"
            # Update start time to match the requested date
            meeting['start']['dateTime'] = f"2025-{date_str[4:6]}-{date_str[6:8]}T{9+i*2:02d}:00:00Z"
        
        print(f"✅ Generated {len(demo_meetings)} demo meetings for {date_str}")
        return demo_meetings
    
    def _generate_pipeline_recommendations(self, ranked_meetings):
        """Generate pipeline-level recommendations"""
        recommendations = []
        
        # Critical meeting protection
        critical_meetings = [m for m in ranked_meetings if m.priority_score >= 8]
        if critical_meetings:
            recommendations.append(f"🔴 {len(critical_meetings)} critical meetings need focus protection")
        
        # Preparation time planning
        intensive_prep = [m for m in ranked_meetings if m.preparation_level == "Intensive"]
        if intensive_prep:
            total_prep_time = len(intensive_prep) * 2  # 2 hours per intensive meeting
            recommendations.append(f"📚 Block {total_prep_time} hours for meeting preparation")
        
        # Meeting fatigue detection
        if len(ranked_meetings) > self.user_profile.meeting_fatigue_threshold:
            recommendations.append(f"⚠️ Meeting fatigue risk: {len(ranked_meetings)} meetings exceed threshold of {self.user_profile.meeting_fatigue_threshold}")
        
        # Auto-decision suggestions
        auto_accept = [m for m in ranked_meetings if m.recommendations.get('action') == 'auto_accept']
        consider_decline = [m for m in ranked_meetings if m.recommendations.get('action') == 'consider_decline']
        
        if auto_accept:
            recommendations.append(f"✅ Auto-accept {len(auto_accept)} critical meetings")
        if consider_decline:
            recommendations.append(f"❓ Consider declining {len(consider_decline)} optional meetings")
        
        # Energy optimization
        drive_meetings = [m for m in ranked_meetings if m.engagement_level == "Drive"]
        if len(drive_meetings) > 2:
            recommendations.append(f"⚡ High cognitive load: {len(drive_meetings)} meetings require active leadership")
        
        return recommendations
    
    def compare_dates(self, date1: str, date2: str):
        """Compare meeting intelligence between two dates"""
        print(f"\n📊 Comparing meeting intelligence: {date1} vs {date2}")
        print("=" * 60)
        
        # Process both dates
        results1 = self.process_daily_meetings(date1)
        results2 = self.process_daily_meetings(date2)
        
        if not results1 or not results2:
            print("❌ Cannot compare - missing data for one or both dates")
            return
        
        # Generate comparison
        comparison = {
            "date1": {
                "date": date1,
                "total_meetings": results1["total_meetings"],
                "critical_count": len([m for m in results1["ranked_meetings"] if m.priority_score >= 8])
            },
            "date2": {
                "date": date2, 
                "total_meetings": results2["total_meetings"],
                "critical_count": len([m for m in results2["ranked_meetings"] if m.priority_score >= 8])
            }
        }
        
        print(f"\n📈 Comparison Results:")
        print(f"   {date1}: {comparison['date1']['total_meetings']} meetings ({comparison['date1']['critical_count']} critical)")
        print(f"   {date2}: {comparison['date2']['total_meetings']} meetings ({comparison['date2']['critical_count']} critical)")
        
        # Workload analysis
        if comparison['date1']['total_meetings'] > comparison['date2']['total_meetings']:
            print(f"   📊 {date1} has higher meeting load (+{comparison['date1']['total_meetings'] - comparison['date2']['total_meetings']} meetings)")
        elif comparison['date2']['total_meetings'] > comparison['date1']['total_meetings']:
            print(f"   📊 {date2} has higher meeting load (+{comparison['date2']['total_meetings'] - comparison['date1']['total_meetings']} meetings)")
        else:
            print(f"   📊 Equal meeting load on both dates")
        
        return comparison
    
    def generate_weekly_intelligence_report(self, start_date: str):
        """Generate weekly meeting intelligence report"""
        print(f"\n📅 Generating Weekly Meeting Intelligence Report")
        print(f"Starting from: {start_date}")
        print("=" * 60)
        
        # Process 7 days starting from start_date
        weekly_results = []
        
        for i in range(7):
            # Calculate date (simplified - assumes same month)
            day = int(start_date[6:8]) + i
            if day > 31:  # Simple month rollover
                day = day - 31
                month = int(start_date[4:6]) + 1
                if month > 12:
                    month = 1
            else:
                month = int(start_date[4:6])
            
            date_str = f"{start_date[:4]}{month:02d}{day:02d}"
            
            print(f"\n📅 Processing {date_str}...")
            result = self.process_daily_meetings(date_str)
            if result:
                weekly_results.append(result)
        
        # Generate weekly summary
        total_meetings = sum(r["total_meetings"] for r in weekly_results)
        total_critical = sum(len([m for m in r["ranked_meetings"] if m.priority_score >= 8]) for r in weekly_results)
        
        print(f"\n📊 Weekly Summary:")
        print(f"   Total Meetings: {total_meetings}")
        print(f"   Critical Meetings: {total_critical}")
        print(f"   Average per Day: {total_meetings/len(weekly_results):.1f}")
        print(f"   Meeting Intensity: {total_critical/total_meetings*100:.1f}% critical")
        
        return weekly_results


def demo_pipeline():
    """Demonstration of the complete meeting intelligence pipeline"""
    print("🎯 Meeting Intelligence Pipeline Demo")
    print("=" * 50)
    
    # Initialize pipeline
    user_profile = create_demo_user_profile()
    pipeline = MeetingIntelligencePipeline(user_profile=user_profile)
    
    # Demo 1: Process today's meetings
    today = datetime.now().strftime("%Y%m%d")
    print(f"\n🔹 Demo 1: Today's Meeting Intelligence ({today})")
    result_today = pipeline.process_daily_meetings(today)
    
    # Demo 2: Process tomorrow's meetings  
    tomorrow = "20251022"  # Fixed date for demo
    print(f"\n🔹 Demo 2: Tomorrow's Meeting Intelligence ({tomorrow})")
    result_tomorrow = pipeline.process_daily_meetings(tomorrow)
    
    # Demo 3: Compare two dates
    print(f"\n🔹 Demo 3: Date Comparison")
    pipeline.compare_dates(today, tomorrow)
    
    # Demo 4: Weekly report (simplified)
    print(f"\n🔹 Demo 4: Weekly Intelligence Summary")
    weekly_results = pipeline.generate_weekly_intelligence_report("20251021")
    
    print(f"\n✅ Pipeline demo complete!")
    print(f"\n🔗 Integration Points:")
    print(f"   📡 Meeting Extraction: Graph API + local data")
    print(f"   🤖 LLM Ranking: Ollama with Priority Calendar framework")
    print(f"   📊 Multi-format Output: MD, JSON, HTML, Console")
    print(f"   🎯 Smart Recommendations: Auto-accept, prep time, conflicts")
    
    return {
        "today": result_today,
        "tomorrow": result_tomorrow,
        "weekly": weekly_results
    }


if __name__ == "__main__":
    print("🚀 Meeting Intelligence Pipeline: Extract → Rank → Display")
    print("Powered by Ollama LLM + Priority Calendar Framework")
    print("=" * 70)
    
    try:
        # Run complete demonstration
        demo_results = demo_pipeline()
        
        print(f"\n🎉 Meeting Intelligence Pipeline Demo Successful!")
        print(f"\n📋 Generated Outputs:")
        print(f"   📄 Daily intelligence reports in multiple formats")
        print(f"   🎯 Priority rankings with LLM reasoning")
        print(f"   🤖 Automated recommendations and insights")
        print(f"   📊 Comparative analysis and weekly summaries")
        
    except Exception as e:
        print(f"\n❌ Pipeline demo failed: {e}")
        import traceback
        traceback.print_exc()