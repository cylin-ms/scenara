"""
Schedule Focus Time for Meeting Preparation

Analyzes important meetings and automatically suggests or creates
focus time blocks in your calendar for preparation.
"""

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Any

sys.path.insert(0, str(Path(__file__).parent))
from track_important_meetings import MeetingImportanceTracker


class FocusTimeScheduler:
    """Schedule focus time blocks for meeting preparation."""
    
    def __init__(self, tracker: MeetingImportanceTracker):
        """Initialize with meeting importance tracker."""
        self.tracker = tracker
        self.focus_blocks = []
    
    def find_available_slots(self, date: str, duration_minutes: int) -> List[Dict[str, Any]]:
        """
        Find available time slots on a given date.
        
        Args:
            date: Date string (YYYY-MM-DD)
            duration_minutes: Required duration in minutes
            
        Returns:
            List of available time slots
        """
        target_date = datetime.fromisoformat(date)
        
        # Get all meetings on that day
        day_meetings = []
        for meeting in self.tracker.meetings:
            start_str = meeting.get('start', {}).get('dateTime', '')
            if not start_str:
                continue
            
            start_dt = datetime.fromisoformat(start_str.replace('Z', '+00:00').split('.')[0])
            if start_dt.date() == target_date.date():
                end_str = meeting.get('end', {}).get('dateTime', '')
                end_dt = datetime.fromisoformat(end_str.replace('Z', '+00:00').split('.')[0])
                day_meetings.append({
                    'start': start_dt,
                    'end': end_dt,
                    'subject': meeting.get('subject')
                })
        
        # Sort by start time
        day_meetings.sort(key=lambda x: x['start'])
        
        # Find gaps between meetings
        available_slots = []
        
        # Define work hours (8 AM - 6 PM)
        work_start = target_date.replace(hour=8, minute=0, second=0, microsecond=0)
        work_end = target_date.replace(hour=18, minute=0, second=0, microsecond=0)
        
        if not day_meetings:
            # Entire day available
            available_slots.append({
                'start': work_start,
                'end': work_end,
                'duration_minutes': (work_end - work_start).total_seconds() / 60
            })
        else:
            # Check before first meeting
            if day_meetings[0]['start'] > work_start:
                gap_duration = (day_meetings[0]['start'] - work_start).total_seconds() / 60
                if gap_duration >= duration_minutes:
                    available_slots.append({
                        'start': work_start,
                        'end': day_meetings[0]['start'],
                        'duration_minutes': gap_duration
                    })
            
            # Check gaps between meetings
            for i in range(len(day_meetings) - 1):
                gap_start = day_meetings[i]['end']
                gap_end = day_meetings[i + 1]['start']
                gap_duration = (gap_end - gap_start).total_seconds() / 60
                
                if gap_duration >= duration_minutes:
                    available_slots.append({
                        'start': gap_start,
                        'end': gap_end,
                        'duration_minutes': gap_duration
                    })
            
            # Check after last meeting
            if day_meetings[-1]['end'] < work_end:
                gap_duration = (work_end - day_meetings[-1]['end']).total_seconds() / 60
                if gap_duration >= duration_minutes:
                    available_slots.append({
                        'start': day_meetings[-1]['end'],
                        'end': work_end,
                        'duration_minutes': gap_duration
                    })
        
        return available_slots
    
    def schedule_focus_blocks(self, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Schedule focus time blocks for meetings requiring preparation.
        
        Args:
            analysis: Analysis results from MeetingImportanceTracker
            
        Returns:
            List of scheduled focus time blocks
        """
        focus_blocks = []
        
        # Group prep meetings by day
        from collections import defaultdict
        by_day = defaultdict(list)
        
        for meeting in analysis['prep_required']:
            start_dt = datetime.fromisoformat(meeting['start'].replace('Z', '+00:00').split('.')[0])
            day_key = start_dt.strftime('%Y-%m-%d')
            by_day[day_key].append(meeting)
        
        # For each day with meetings needing prep
        for meeting_day, meetings in sorted(by_day.items()):
            meeting_date = datetime.fromisoformat(meeting_day)
            
            # Calculate total prep needed
            total_prep = sum(m['prep_time_minutes'] for m in meetings)
            
            # Try to schedule focus time the day before
            prep_date = meeting_date - timedelta(days=1)
            prep_date_str = prep_date.strftime('%Y-%m-%d')
            
            # Find available slots
            available = self.find_available_slots(prep_date_str, total_prep)
            
            if available:
                # Use first available slot
                slot = available[0]
                focus_start = slot['start']
                focus_end = focus_start + timedelta(minutes=total_prep)
                
                # Create focus block
                focus_block = {
                    'date': prep_date_str,
                    'start': focus_start.isoformat(),
                    'end': focus_end.isoformat(),
                    'duration_minutes': total_prep,
                    'purpose': f"Prepare for {len(meetings)} meeting(s) on {meeting_date.strftime('%B %d')}",
                    'meetings_to_prep': [
                        {
                            'subject': m['subject'],
                            'start': m['start'],
                            'prep_time': m['prep_time_minutes']
                        }
                        for m in meetings
                    ]
                }
                
                focus_blocks.append(focus_block)
                
                print(f"✅ Scheduled {total_prep}min focus time on {prep_date_str} at {focus_start.strftime('%H:%M')}")
            else:
                print(f"⚠️  No available slot found on {prep_date_str} for {total_prep}min prep")
                
                # Try same day, early morning
                same_day_slots = self.find_available_slots(meeting_day, total_prep)
                if same_day_slots:
                    slot = same_day_slots[0]
                    focus_start = slot['start']
                    focus_end = focus_start + timedelta(minutes=total_prep)
                    
                    focus_block = {
                        'date': meeting_day,
                        'start': focus_start.isoformat(),
                        'end': focus_end.isoformat(),
                        'duration_minutes': total_prep,
                        'purpose': f"Prepare for {len(meetings)} meeting(s) today",
                        'meetings_to_prep': [
                            {
                                'subject': m['subject'],
                                'start': m['start'],
                                'prep_time': m['prep_time_minutes']
                            }
                            for m in meetings
                        ],
                        'note': 'Same-day prep (no slot available day before)'
                    }
                    
                    focus_blocks.append(focus_block)
                    print(f"✅ Scheduled {total_prep}min focus time on {meeting_day} at {focus_start.strftime('%H:%M')} (same day)")
        
        self.focus_blocks = focus_blocks
        return focus_blocks
    
    def generate_calendar_entries(self, output_file: str = None) -> str:
        """Generate calendar entries in iCalendar format."""
        
        ical_lines = [
            "BEGIN:VCALENDAR",
            "VERSION:2.0",
            "PRODID:-//Scenara//Meeting Prep Focus Time//EN",
            "CALSCALE:GREGORIAN",
            "METHOD:PUBLISH",
            "X-WR-CALNAME:Meeting Preparation Focus Time",
            "X-WR-TIMEZONE:UTC"
        ]
        
        for block in self.focus_blocks:
            start_dt = datetime.fromisoformat(block['start'])
            end_dt = datetime.fromisoformat(block['end'])
            
            # Format for iCal (YYYYMMDDTHHMMSSZ)
            dtstart = start_dt.strftime('%Y%m%dT%H%M%S')
            dtend = end_dt.strftime('%Y%m%dT%H%M%S')
            
            # Create description with meeting list
            description = f"{block['purpose']}\\n\\n"
            for meeting in block['meetings_to_prep']:
                description += f"- {meeting['subject']} ({meeting['prep_time']}min prep)\\n"
            
            ical_lines.extend([
                "BEGIN:VEVENT",
                f"DTSTART:{dtstart}",
                f"DTEND:{dtend}",
                f"SUMMARY:🎯 Focus Time: Meeting Prep ({block['duration_minutes']}min)",
                f"DESCRIPTION:{description}",
                "STATUS:CONFIRMED",
                "TRANSP:OPAQUE",
                "CATEGORIES:Focus Time,Meeting Prep",
                "END:VEVENT"
            ])
        
        ical_lines.append("END:VCALENDAR")
        
        ical_content = "\n".join(ical_lines)
        
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(ical_content)
            print(f"\n📅 Calendar file saved: {output_file}")
            print(f"   Import this file into Outlook/Google Calendar to add focus blocks")
        
        return ical_content
    
    def print_summary(self):
        """Print summary of scheduled focus blocks."""
        
        if not self.focus_blocks:
            print("\n⚠️  No focus time blocks scheduled")
            return
        
        print(f"\n{'=' * 80}")
        print("🎯 SCHEDULED FOCUS TIME BLOCKS")
        print("=" * 80)
        
        total_time = sum(b['duration_minutes'] for b in self.focus_blocks)
        print(f"\nTotal Focus Time: {total_time} minutes ({total_time/60:.1f} hours)")
        print(f"Number of Blocks: {len(self.focus_blocks)}\n")
        
        for i, block in enumerate(self.focus_blocks, 1):
            start_dt = datetime.fromisoformat(block['start'])
            end_dt = datetime.fromisoformat(block['end'])
            
            print(f"{i}. {start_dt.strftime('%A, %B %d, %Y')}")
            print(f"   ⏰ {start_dt.strftime('%H:%M')} - {end_dt.strftime('%H:%M')} ({block['duration_minutes']} minutes)")
            print(f"   📝 {block['purpose']}")
            
            if 'note' in block:
                print(f"   ℹ️  {block['note']}")
            
            print(f"   📋 Meetings to prepare:")
            for meeting in block['meetings_to_prep']:
                meeting_time = datetime.fromisoformat(meeting['start'].replace('Z', '+00:00').split('.')[0])
                print(f"      • {meeting_time.strftime('%H:%M')} {meeting['subject']} ({meeting['prep_time']}min)")
            print()


def main():
    """Main execution."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Schedule focus time for meeting preparation')
    parser.add_argument('--from-date', help='Start date (YYYY-MM-DD), default: today')
    parser.add_argument('--to-date', help='End date (YYYY-MM-DD), default: 2 weeks from today')
    parser.add_argument('--calendar-file', default='my_calendar_events_complete_attendees.json',
                       help='Calendar data JSON file')
    parser.add_argument('--export-ical', help='Export focus blocks to iCalendar file')
    parser.add_argument('--json', help='Export focus blocks to JSON file')
    
    args = parser.parse_args()
    
    print("🎯 Focus Time Scheduler for Meeting Preparation\n")
    
    # Initialize tracker
    tracker = MeetingImportanceTracker(args.calendar_file)
    
    if not tracker.load_calendar_data():
        return 1
    
    # Analyze meetings
    print("\n📊 Analyzing meetings for preparation requirements...")
    analysis = tracker.analyze_meetings(args.from_date, args.to_date)
    
    print(f"   • Found {analysis['summary']['prep_required']} meetings requiring prep")
    print(f"   • Total prep time needed: {analysis['summary']['total_prep_time_hours']:.1f} hours\n")
    
    # Schedule focus blocks
    scheduler = FocusTimeScheduler(tracker)
    focus_blocks = scheduler.schedule_focus_blocks(analysis)
    
    # Print summary
    scheduler.print_summary()
    
    # Export if requested
    if args.export_ical:
        scheduler.generate_calendar_entries(args.export_ical)
    
    if args.json:
        with open(args.json, 'w', encoding='utf-8') as f:
            json.dump(focus_blocks, f, indent=2, default=str)
        print(f"✅ JSON export saved: {args.json}")
    
    print("\n💡 Next Steps:")
    print("   1. Review the scheduled focus time blocks above")
    print("   2. Import the .ics file to your calendar (if generated)")
    print("   3. Block these times in your calendar to ensure uninterrupted prep")
    print("   4. Use the prep time to review materials, prepare presentations, etc.")
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
