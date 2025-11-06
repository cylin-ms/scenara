"""
Track Important Meetings and Flag Preparation Requirements

Analyzes calendar data to:
1. Identify important meetings based on multiple criteria
2. Flag meetings requiring focus time for preparation
3. Calculate recommended prep time for each meeting
4. Generate daily/weekly reports with actionable insights
"""

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict
from typing import List, Dict, Any, Tuple

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))


class MeetingImportanceTracker:
    """Track and analyze meeting importance with prep time recommendations."""
    
    # Meeting importance criteria weights
    IMPORTANCE_WEIGHTS = {
        'executive_attendee': 25,      # C-level or VP attendees
        'external_attendee': 20,       # Customers, partners
        'large_meeting': 15,           # 10+ attendees
        'presentation': 20,            # Requires presenting
        'decision_making': 25,         # Review, approval, planning
        'cross_team': 15,              # Multiple organizations
        'recurring_key': 10,           # Important recurring series
        'direct_manager': 15,          # Your manager attending
        'skip_level': 20,              # Manager's manager
    }
    
    # Keywords indicating high-importance meetings
    HIGH_IMPORTANCE_KEYWORDS = {
        'executive': ['exec', 'vp', 'cvp', 'svp', 'cxo', 'ceo', 'cto', 'cfo'],
        'external': ['customer', 'client', 'partner', 'vendor', 'external'],
        'decision': ['review', 'approval', 'decision', 'planning', 'strategy', 'roadmap'],
        'presentation': ['present', 'demo', 'showcase', 'pitch', 'briefing'],
        'critical': ['urgent', 'critical', 'escalation', 'incident', 'issue'],
    }
    
    # Meeting types requiring preparation
    PREP_REQUIRED_TYPES = {
        'Executive Briefing': 120,      # 2 hours prep
        'Customer Meeting': 90,         # 1.5 hours prep
        'Technical Design Review': 60,  # 1 hour prep
        'Project Planning Meeting': 45, # 45 min prep
        'Product Demo': 90,             # 1.5 hours prep
        'Strategy Session': 60,         # 1 hour prep
        'Performance Review': 45,       # 45 min prep
        'All Hands Meeting': 30,        # 30 min prep
        'Board Meeting': 180,           # 3 hours prep
        'Interview': 30,                # 30 min prep
    }
    
    def __init__(self, calendar_file: str = "my_calendar_events_complete_attendees.json"):
        """Initialize tracker with calendar data."""
        self.calendar_file = Path(calendar_file)
        self.meetings = []
        self.important_meetings = []
        self.prep_required = []
        
    def load_calendar_data(self) -> bool:
        """Load calendar events from JSON file."""
        try:
            with open(self.calendar_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.meetings = data.get('events', [])
                print(f"✅ Loaded {len(self.meetings)} meetings from calendar")
                return True
        except Exception as e:
            print(f"❌ Error loading calendar: {e}")
            return False
    
    def calculate_importance_score(self, meeting: Dict[str, Any]) -> Tuple[int, List[str]]:
        """
        Calculate importance score for a meeting.
        
        Returns:
            Tuple of (score, reasons) where reasons explain why it's important
        """
        score = 0
        reasons = []
        
        subject = meeting.get('subject', '').lower()
        attendees = meeting.get('attendees', [])
        
        # Check for executive attendees
        exec_count = sum(1 for a in attendees 
                        if any(kw in a.get('emailAddress', {}).get('name', '').lower() 
                              for kw in self.HIGH_IMPORTANCE_KEYWORDS['executive']))
        if exec_count > 0:
            score += self.IMPORTANCE_WEIGHTS['executive_attendee'] * exec_count
            reasons.append(f"Executive attendee(s): {exec_count}")
        
        # Check for external attendees (non-microsoft.com)
        external_count = sum(1 for a in attendees 
                           if '@microsoft.com' not in a.get('emailAddress', {}).get('address', '').lower())
        if external_count > 0:
            score += self.IMPORTANCE_WEIGHTS['external_attendee']
            reasons.append(f"External attendee(s): {external_count}")
        
        # Large meeting
        attendee_count = len([a for a in attendees if a.get('type') != 'resource'])
        if attendee_count >= 10:
            score += self.IMPORTANCE_WEIGHTS['large_meeting']
            reasons.append(f"Large meeting: {attendee_count} attendees")
        
        # Check subject for keywords
        for category, keywords in self.HIGH_IMPORTANCE_KEYWORDS.items():
            for keyword in keywords:
                if keyword in subject:
                    weight_key = category if category in self.IMPORTANCE_WEIGHTS else 'decision_making'
                    score += self.IMPORTANCE_WEIGHTS.get(weight_key, 10)
                    reasons.append(f"Keyword '{keyword}' in subject")
                    break
        
        # Presentation indicators
        presentation_keywords = ['present', 'demo', 'showcase', 'pitch', 'share out']
        if any(kw in subject for kw in presentation_keywords):
            score += self.IMPORTANCE_WEIGHTS['presentation']
            reasons.append("Presentation/demo meeting")
        
        return score, reasons
    
    def estimate_prep_time(self, meeting: Dict[str, Any], importance_score: int) -> int:
        """
        Estimate preparation time needed in minutes.
        
        Args:
            meeting: Meeting data
            importance_score: Calculated importance score
            
        Returns:
            Preparation time in minutes
        """
        subject = meeting.get('subject', '').lower()
        
        # Check for known meeting types requiring prep
        for meeting_type, prep_time in self.PREP_REQUIRED_TYPES.items():
            if meeting_type.lower() in subject:
                return prep_time
        
        # Check keywords
        if any(kw in subject for kw in ['review', 'approval', 'decision']):
            return 45
        if any(kw in subject for kw in ['present', 'demo', 'showcase']):
            return 60
        if any(kw in subject for kw in ['strategy', 'planning', 'roadmap']):
            return 60
        
        # Base on importance score
        if importance_score >= 80:
            return 90  # 1.5 hours for very important meetings
        elif importance_score >= 50:
            return 60  # 1 hour
        elif importance_score >= 30:
            return 30  # 30 minutes
        
        return 0  # No prep needed
    
    def analyze_meetings(self, from_date: str = None, to_date: str = None) -> Dict[str, Any]:
        """
        Analyze meetings for importance and prep requirements.
        
        Args:
            from_date: Start date (YYYY-MM-DD), defaults to today
            to_date: End date (YYYY-MM-DD), defaults to 2 weeks from now
            
        Returns:
            Analysis results dictionary
        """
        if not from_date:
            from_date = datetime.now().strftime('%Y-%m-%d')
        if not to_date:
            to_date = (datetime.now() + timedelta(days=14)).strftime('%Y-%m-%d')
        
        print(f"\n📊 Analyzing meetings from {from_date} to {to_date}...")
        
        from_dt = datetime.fromisoformat(from_date)
        to_dt = datetime.fromisoformat(to_date)
        
        important_meetings = []
        prep_required_meetings = []
        
        for meeting in self.meetings:
            # Parse meeting start time
            start_str = meeting.get('start', {}).get('dateTime', '')
            if not start_str:
                continue
            
            # Handle timezone info
            start_dt = datetime.fromisoformat(start_str.replace('Z', '+00:00').split('.')[0])
            
            # Filter by date range
            if not (from_dt <= start_dt <= to_dt):
                continue
            
            # Calculate importance
            importance_score, reasons = self.calculate_importance_score(meeting)
            prep_time = self.estimate_prep_time(meeting, importance_score)
            
            # Create enhanced meeting record
            enhanced_meeting = {
                'subject': meeting.get('subject'),
                'start': start_str,
                'end': meeting.get('end', {}).get('dateTime'),
                'importance_score': importance_score,
                'importance_reasons': reasons,
                'prep_time_minutes': prep_time,
                'attendee_count': len([a for a in meeting.get('attendees', []) 
                                      if a.get('type') != 'resource']),
                'organizer': meeting.get('organizer', {}).get('emailAddress', {}).get('name'),
                'is_online': meeting.get('isOnlineMeeting', False),
                'original_data': meeting
            }
            
            # Flag important meetings (score >= 30)
            if importance_score >= 30:
                important_meetings.append(enhanced_meeting)
            
            # Flag meetings requiring prep
            if prep_time > 0:
                prep_required_meetings.append(enhanced_meeting)
        
        # Sort by importance score (descending)
        important_meetings.sort(key=lambda x: x['importance_score'], reverse=True)
        prep_required_meetings.sort(key=lambda x: x['prep_time_minutes'], reverse=True)
        
        self.important_meetings = important_meetings
        self.prep_required = prep_required_meetings
        
        return {
            'analysis_period': {
                'from': from_date,
                'to': to_date
            },
            'summary': {
                'total_meetings_analyzed': len([m for m in self.meetings 
                                               if from_dt <= datetime.fromisoformat(
                                                   m.get('start', {}).get('dateTime', '').replace('Z', '+00:00').split('.')[0]
                                               ) <= to_dt]),
                'important_meetings': len(important_meetings),
                'prep_required': len(prep_required_meetings),
                'total_prep_time_hours': sum(m['prep_time_minutes'] for m in prep_required_meetings) / 60
            },
            'important_meetings': important_meetings,
            'prep_required': prep_required_meetings
        }
    
    def generate_report(self, analysis: Dict[str, Any], output_file: str = None) -> str:
        """Generate formatted report of important meetings and prep requirements."""
        
        lines = []
        lines.append("=" * 80)
        lines.append("📅 IMPORTANT MEETINGS TRACKER")
        lines.append("=" * 80)
        lines.append(f"\n📊 Analysis Period: {analysis['analysis_period']['from']} to {analysis['analysis_period']['to']}")
        lines.append(f"\n📈 Summary:")
        lines.append(f"   • Total Meetings Analyzed: {analysis['summary']['total_meetings_analyzed']}")
        lines.append(f"   • Important Meetings: {analysis['summary']['important_meetings']}")
        lines.append(f"   • Meetings Requiring Prep: {analysis['summary']['prep_required']}")
        lines.append(f"   • Total Prep Time Needed: {analysis['summary']['total_prep_time_hours']:.1f} hours")
        
        # Important Meetings Section
        if analysis['important_meetings']:
            lines.append(f"\n{'=' * 80}")
            lines.append("🔴 HIGH IMPORTANCE MEETINGS")
            lines.append("=" * 80)
            
            for i, meeting in enumerate(analysis['important_meetings'][:20], 1):
                start_dt = datetime.fromisoformat(meeting['start'].replace('Z', '+00:00').split('.')[0])
                lines.append(f"\n{i}. {meeting['subject']}")
                lines.append(f"   📅 {start_dt.strftime('%Y-%m-%d %H:%M')}")
                lines.append(f"   🎯 Importance Score: {meeting['importance_score']}")
                lines.append(f"   👥 Attendees: {meeting['attendee_count']}")
                if meeting['prep_time_minutes'] > 0:
                    lines.append(f"   ⏰ Prep Time Needed: {meeting['prep_time_minutes']} minutes")
                if meeting['importance_reasons']:
                    lines.append(f"   💡 Why Important:")
                    for reason in meeting['importance_reasons']:
                        lines.append(f"      • {reason}")
        
        # Prep Required Section
        if analysis['prep_required']:
            lines.append(f"\n{'=' * 80}")
            lines.append("⏰ MEETINGS REQUIRING PREPARATION")
            lines.append("=" * 80)
            
            # Group by day
            by_day = defaultdict(list)
            for meeting in analysis['prep_required']:
                start_dt = datetime.fromisoformat(meeting['start'].replace('Z', '+00:00').split('.')[0])
                day_key = start_dt.strftime('%Y-%m-%d')
                by_day[day_key].append(meeting)
            
            for day in sorted(by_day.keys()):
                day_dt = datetime.fromisoformat(day)
                lines.append(f"\n📆 {day_dt.strftime('%A, %B %d, %Y')}")
                lines.append("-" * 80)
                
                daily_prep = sum(m['prep_time_minutes'] for m in by_day[day])
                lines.append(f"   Total prep time needed: {daily_prep} minutes ({daily_prep/60:.1f} hours)\n")
                
                for meeting in sorted(by_day[day], key=lambda x: x['start']):
                    start_dt = datetime.fromisoformat(meeting['start'].replace('Z', '+00:00').split('.')[0])
                    lines.append(f"   • {start_dt.strftime('%H:%M')} - {meeting['subject']}")
                    lines.append(f"     ⏰ Prep: {meeting['prep_time_minutes']} min | 🎯 Score: {meeting['importance_score']} | 👥 {meeting['attendee_count']} attendees")
                    if meeting['importance_reasons']:
                        lines.append(f"     💡 {', '.join(meeting['importance_reasons'][:2])}")
                    lines.append("")
        
        # Recommendations
        lines.append(f"\n{'=' * 80}")
        lines.append("💡 RECOMMENDATIONS")
        lines.append("=" * 80)
        
        total_prep = analysis['summary']['total_prep_time_hours']
        if total_prep > 10:
            lines.append("\n⚠️  HIGH PREP TIME ALERT:")
            lines.append(f"   You need {total_prep:.1f} hours of prep time in the next 2 weeks.")
            lines.append(f"   Suggestion: Block at least 1-2 hours daily for meeting preparation.")
        elif total_prep > 5:
            lines.append(f"\n✅ Moderate prep time: {total_prep:.1f} hours needed.")
            lines.append(f"   Suggestion: Block 30-60 minutes daily for preparation.")
        else:
            lines.append(f"\n✅ Low prep burden: {total_prep:.1f} hours needed.")
        
        # Focus time recommendations
        if analysis['prep_required']:
            lines.append("\n📅 FOCUS TIME RECOMMENDATIONS:")
            lines.append("   Schedule these focus blocks to prepare:")
            
            by_day_sorted = sorted(by_day.items())
            for day, meetings in by_day_sorted[:7]:  # Next 7 days
                day_dt = datetime.fromisoformat(day)
                daily_prep = sum(m['prep_time_minutes'] for m in meetings)
                if daily_prep >= 30:
                    # Suggest focus time day before
                    prep_day = (day_dt - timedelta(days=1)).strftime('%Y-%m-%d')
                    lines.append(f"   • {prep_day}: Block {daily_prep} minutes for {day_dt.strftime('%B %d')} meetings")
        
        report = "\n".join(lines)
        
        # Save to file if requested
        if output_file:
            output_path = Path(output_file)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"\n💾 Report saved to: {output_path}")
        
        return report


def main():
    """Main execution function."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Track important meetings and flag prep requirements')
    parser.add_argument('--from-date', help='Start date (YYYY-MM-DD), default: today')
    parser.add_argument('--to-date', help='End date (YYYY-MM-DD), default: 2 weeks from today')
    parser.add_argument('--calendar-file', default='my_calendar_events_complete_attendees.json',
                       help='Calendar data JSON file')
    parser.add_argument('--output', help='Save report to file')
    parser.add_argument('--json', action='store_true', help='Output results as JSON')
    
    args = parser.parse_args()
    
    # Initialize tracker
    tracker = MeetingImportanceTracker(args.calendar_file)
    
    # Load calendar data
    if not tracker.load_calendar_data():
        return 1
    
    # Analyze meetings
    analysis = tracker.analyze_meetings(args.from_date, args.to_date)
    
    # Generate output
    if args.json:
        output_file = args.output or f"important_meetings_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(analysis, f, indent=2, default=str)
        print(f"✅ JSON output saved to: {output_file}")
    else:
        report = tracker.generate_report(analysis, args.output)
        print(report)
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
