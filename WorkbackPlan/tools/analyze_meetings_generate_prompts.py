#!/usr/bin/env python3
"""
Analyze User's Meetings and Generate DevUI Test Prompts
Extract meetings matching workback planning proposal types and create test prompts

Author: Chin-Yew Lin
Date: November 18, 2025
"""

import json
import re
from datetime import datetime, timedelta
from typing import List, Dict, Any
from collections import defaultdict

# Meeting types from workback planning proposal
WBP_MEETING_TYPES = {
    "Board Review Meeting": {
        "keywords": ["board", "board review", "board meeting", "directors"],
        "description": "High-stakes quarterly board meeting requiring executive preparation",
        "complexity": "high",
        "lead_time_days": 60
    },
    "Quarterly Business Review (QBR)": {
        "keywords": ["qbr", "quarterly", "business review", "q1", "q2", "q3", "q4"],
        "description": "Strategic performance review with executives and stakeholders",
        "complexity": "high",
        "lead_time_days": 45
    },
    "Product Launch": {
        "keywords": ["launch", "product launch", "release", "ship", "ga"],
        "description": "Cross-functional product launch requiring coordinated activities",
        "complexity": "high",
        "lead_time_days": 90
    },
    "M&A Due Diligence": {
        "keywords": ["acquisition", "merger", "due diligence", "m&a", "diligence"],
        "description": "Complex due diligence process for mergers and acquisitions",
        "complexity": "high",
        "lead_time_days": 120
    },
    "Team Offsite Planning": {
        "keywords": ["offsite", "team offsite", "planning offsite", "retreat"],
        "description": "Strategic team planning session requiring logistics and agenda",
        "complexity": "medium",
        "lead_time_days": 30
    },
    "Conference/Event Preparation": {
        "keywords": ["conference", "summit", "event", "convention", "symposium"],
        "description": "External conference requiring materials and speaker preparation",
        "complexity": "medium",
        "lead_time_days": 45
    },
    "Executive Presentation": {
        "keywords": ["executive", "ceo", "cto", "vp", "leadership", "senior"],
        "description": "High-visibility presentation to executive leadership",
        "complexity": "medium",
        "lead_time_days": 21
    },
    "Project Kickoff": {
        "keywords": ["kickoff", "kick-off", "project start", "initiation"],
        "description": "Project initialization requiring team alignment and planning",
        "complexity": "medium",
        "lead_time_days": 14
    },
    "Budget Planning": {
        "keywords": ["budget", "planning", "fy", "fiscal", "financial planning"],
        "description": "Annual or quarterly budget planning process",
        "complexity": "medium",
        "lead_time_days": 30
    },
    "Hiring Committee": {
        "keywords": ["hiring", "interview", "candidate", "recruitment"],
        "description": "Interview process requiring coordination and preparation",
        "complexity": "low",
        "lead_time_days": 7
    }
}


class MeetingAnalyzer:
    def __init__(self, calendar_file: str):
        self.calendar_file = calendar_file
        self.meetings = []
        self.matched_meetings = defaultdict(list)
        self.load_meetings()
    
    def load_meetings(self):
        """Load meetings from calendar JSON"""
        print(f"📂 Loading meetings from: {self.calendar_file}")
        
        with open(self.calendar_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Handle different JSON structures
        if 'events' in data:
            self.meetings = data['events']
        elif isinstance(data, list):
            self.meetings = data
        else:
            raise ValueError("Unexpected JSON structure")
        
        print(f"✅ Loaded {len(self.meetings)} meetings")
    
    def match_meeting_type(self, meeting: Dict) -> List[str]:
        """Match meeting to workback planning types"""
        subject = (meeting.get('subject') or '').lower()
        body = (meeting.get('bodyPreview') or '').lower()
        text = f"{subject} {body}"
        
        matches = []
        for meeting_type, info in WBP_MEETING_TYPES.items():
            for keyword in info['keywords']:
                if keyword in text:
                    matches.append(meeting_type)
                    break
        
        return matches
    
    def is_within_6_months(self, meeting: Dict) -> bool:
        """Check if meeting is within the data range (April-October 2025)"""
        # All meetings in the file are from the past 6 months based on metadata
        # Just verify the meeting has a valid start date
        try:
            start_str = meeting.get('start', {}).get('dateTime', '')
            if not start_str:
                return False
            
            # Handle Graph API format: 2025-04-01T14:35:00.0000000
            # Graph API returns 7 digits after decimal, Python datetime expects max 6
            if '.' in start_str:
                # Split at decimal point
                base, fraction = start_str.split('.')
                # Keep only first 6 digits of fractional seconds
                fraction = fraction[:6]
                start_str = f"{base}.{fraction}"
            
            meeting_date = datetime.fromisoformat(start_str)
            # Data is from April-October 2025, all within range
            return True
        except Exception as e:
            #print(f"Debug: Failed to parse date: {meeting.get('subject')} - {e}")
            return False
    
    def analyze_meetings(self):
        """Analyze meetings and categorize by workback planning types"""
        print("\n🔍 Analyzing meetings for workback planning types...")
        
        recent_meetings = [m for m in self.meetings if self.is_within_6_months(m)]
        print(f"📅 Found {len(recent_meetings)} meetings in past 6 months")
        
        for meeting in recent_meetings:
            matches = self.match_meeting_type(meeting)
            for match in matches:
                self.matched_meetings[match].append(meeting)
        
        print(f"\n📊 Meeting Type Matches:")
        for meeting_type in WBP_MEETING_TYPES.keys():
            count = len(self.matched_meetings[meeting_type])
            icon = "✅" if count > 0 else "❌"
            print(f"   {icon} {meeting_type}: {count} meetings")
    
    def get_best_example(self, meeting_type: str) -> Dict:
        """Get best example meeting for a type"""
        meetings = self.matched_meetings[meeting_type]
        if not meetings:
            return None
        
        # Prefer meetings with more attendees (higher complexity)
        def score_meeting(m):
            attendees = len(m.get('attendees', []))
            has_body = 1 if m.get('bodyPreview') else 0
            return attendees * 10 + has_body
        
        meetings.sort(key=score_meeting, reverse=True)
        return meetings[0]
    
    def format_meeting_summary(self, meeting: Dict) -> str:
        """Format meeting as readable summary"""
        if not meeting:
            return "No matching meeting found"
        
        subject = meeting.get('subject', 'Untitled')
        start = meeting.get('start', {}).get('dateTime', 'Unknown')
        attendees = meeting.get('attendees', [])
        body = meeting.get('bodyPreview', '')
        
        # Format date
        try:
            dt = datetime.fromisoformat(start.replace('Z', '+00:00'))
            formatted_date = dt.strftime("%B %d, %Y at %I:%M %p")
        except:
            formatted_date = start
        
        # Get attendee names
        attendee_names = []
        for att in attendees[:5]:  # First 5
            email = att.get('emailAddress', {})
            name = email.get('name') or email.get('address', '')
            if name:
                attendee_names.append(name)
        
        if len(attendees) > 5:
            attendee_names.append(f"... and {len(attendees) - 5} more")
        
        summary = f"""Subject: {subject}
Date: {formatted_date}
Attendees ({len(attendees)}): {', '.join(attendee_names)}
Description: {body[:200]}{'...' if len(body) > 200 else ''}"""
        
        return summary
    
    def generate_devui_prompt(self, meeting_type: str, meeting: Dict) -> str:
        """Generate BizChat prompt for DevUI testing"""
        if not meeting:
            return f"# No {meeting_type} found in your calendar\n\nCreate a synthetic example for testing."
        
        info = WBP_MEETING_TYPES[meeting_type]
        subject = meeting.get('subject', 'the meeting')
        start = meeting.get('start', {}).get('dateTime', '')
        
        # Format date for prompt
        try:
            dt = datetime.fromisoformat(start.replace('Z', '+00:00'))
            date_str = dt.strftime("%B %d, %Y")
        except:
            date_str = "the scheduled date"
        
        prompt = f"""I have an upcoming {meeting_type.lower()} titled "{subject}" scheduled for {date_str}. 

This is a {info['complexity']}-complexity meeting that typically requires {info['lead_time_days']} days of preparation time.

Can you help me create a detailed workback plan that includes:
1. All key milestones leading up to the meeting
2. Specific tasks with owners and deadlines
3. Dependencies between tasks
4. Critical path activities
5. Risk mitigation strategies

Please consider:
- The meeting requires coordination across multiple teams
- There are likely dependencies on deliverables and approvals
- We need to ensure adequate time for review cycles
- Executive-level stakeholders will be involved

Generate a comprehensive workback plan that ensures successful meeting preparation."""
        
        return prompt
    
    def generate_test_prompts_file(self, output_file: str):
        """Generate complete test prompts file"""
        print(f"\n📝 Generating test prompts file: {output_file}")
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("# BizChat DevUI Test Prompts for Workback Planning\n\n")
            f.write(f"**Generated**: {datetime.now().isoformat()}\n")
            f.write(f"**Purpose**: Test prompts based on real meetings from past 6 months\n\n")
            f.write("---\n\n")
            
            for idx, (meeting_type, info) in enumerate(WBP_MEETING_TYPES.items(), 1):
                meeting = self.get_best_example(meeting_type)
                
                f.write(f"## Test Prompt {idx}: {meeting_type}\n\n")
                f.write(f"**Complexity**: {info['complexity']}\n")
                f.write(f"**Lead Time**: {info['lead_time_days']} days\n")
                f.write(f"**Description**: {info['description']}\n\n")
                
                if meeting:
                    f.write("### Real Meeting Example\n\n")
                    f.write("```\n")
                    f.write(self.format_meeting_summary(meeting))
                    f.write("\n```\n\n")
                else:
                    f.write("**Status**: ❌ No matching meeting found (use synthetic example)\n\n")
                
                f.write("### BizChat Prompt\n\n")
                f.write("```\n")
                f.write(self.generate_devui_prompt(meeting_type, meeting))
                f.write("\n```\n\n")
                
                f.write("### Expected Tool Calls\n\n")
                f.write("Based on this prompt, ContextFlow should capture:\n")
                f.write("- `graph_calendar_get_events` - Retrieve meeting details\n")
                f.write("- `graph_get_people` - Get attendee information\n")
                f.write("- `bizchat_context` - Gather contextual information\n")
                f.write("- `bizchat_recommendations` - Get related content\n")
                f.write("- Potentially other tools based on meeting type\n\n")
                
                f.write("---\n\n")
        
        print(f"✅ Test prompts file created: {output_file}")
    
    def generate_summary_report(self, output_file: str):
        """Generate analysis summary report"""
        print(f"\n📊 Generating summary report: {output_file}")
        
        report = {
            "analysis_date": datetime.now().isoformat(),
            "total_meetings": len(self.meetings),
            "meetings_last_6_months": sum(1 for m in self.meetings if self.is_within_6_months(m)),
            "meeting_type_coverage": {},
            "matched_meetings_by_type": {}
        }
        
        for meeting_type, info in WBP_MEETING_TYPES.items():
            count = len(self.matched_meetings[meeting_type])
            report["meeting_type_coverage"][meeting_type] = {
                "count": count,
                "has_example": count > 0,
                "complexity": info["complexity"],
                "lead_time_days": info["lead_time_days"]
            }
            
            if count > 0:
                best = self.get_best_example(meeting_type)
                report["matched_meetings_by_type"][meeting_type] = {
                    "subject": best.get("subject"),
                    "date": best.get("start", {}).get("dateTime"),
                    "attendee_count": len(best.get("attendees", []))
                }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)
        
        print(f"✅ Summary report created: {output_file}")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Analyze meetings and generate DevUI test prompts"
    )
    parser.add_argument(
        "--calendar",
        default="/Users/cyl/projects/scenara/my_calendar_events_complete_attendees.json",
        help="Calendar JSON file"
    )
    parser.add_argument(
        "--output",
        default="/Users/cyl/projects/scenara/WorkbackPlan/docs/devui_test_prompts.md",
        help="Output test prompts file"
    )
    parser.add_argument(
        "--report",
        default="/Users/cyl/projects/scenara/WorkbackPlan/docs/meeting_analysis_report.json",
        help="Output analysis report"
    )
    
    args = parser.parse_args()
    
    print("🎯 Meeting Analysis & DevUI Test Prompt Generation")
    print("=" * 70)
    
    analyzer = MeetingAnalyzer(args.calendar)
    analyzer.analyze_meetings()
    analyzer.generate_test_prompts_file(args.output)
    analyzer.generate_summary_report(args.report)
    
    print("\n✨ Analysis complete!")
    print(f"\n📝 Files created:")
    print(f"   1. Test Prompts: {args.output}")
    print(f"   2. Analysis Report: {args.report}")
    print(f"\n🎯 Next steps:")
    print(f"   1. Review test prompts")
    print(f"   2. Run each prompt in ContextFlow + BizChat")
    print(f"   3. Export sessions from ContextFlow")
    print(f"   4. Run: python tools/integrate_contextflow_tools.py")


if __name__ == "__main__":
    main()
