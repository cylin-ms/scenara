#!/usr/bin/env python3
"""
Daily Meeting Digest - Quick overview of today's important meetings and prep needs
"""

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from track_important_meetings import MeetingImportanceTracker


def print_daily_digest(target_date: str = None):
    """Print daily digest of meetings and prep requirements."""
    
    if not target_date:
        target_date = datetime.now().strftime('%Y-%m-%d')
    
    date_obj = datetime.fromisoformat(target_date)
    
    print("=" * 80)
    print(f"📅 DAILY MEETING DIGEST - {date_obj.strftime('%A, %B %d, %Y')}")
    print("=" * 80)
    
    # Initialize tracker
    tracker = MeetingImportanceTracker()
    if not tracker.load_calendar_data():
        return
    
    # Get meetings for target date
    day_meetings = []
    for meeting in tracker.meetings:
        start_str = meeting.get('start', {}).get('dateTime', '')
        if not start_str:
            continue
        
        start_dt = datetime.fromisoformat(start_str.replace('Z', '+00:00').split('.')[0])
        if start_dt.date() == date_obj.date():
            # Calculate importance
            importance_score, reasons = tracker.calculate_importance_score(meeting)
            prep_time = tracker.estimate_prep_time(meeting, importance_score)
            
            day_meetings.append({
                'start': start_dt,
                'end': datetime.fromisoformat(meeting.get('end', {}).get('dateTime', '').replace('Z', '+00:00').split('.')[0]),
                'subject': meeting.get('subject'),
                'importance_score': importance_score,
                'prep_time': prep_time,
                'attendee_count': len([a for a in meeting.get('attendees', []) if a.get('type') != 'resource']),
                'is_online': meeting.get('isOnlineMeeting', False),
                'reasons': reasons
            })
    
    # Sort by start time
    day_meetings.sort(key=lambda x: x['start'])
    
    if not day_meetings:
        print(f"\n✅ No meetings scheduled for {date_obj.strftime('%B %d')}")
        print("\n💡 Great day for deep work! 🎉")
        return
    
    # Summary
    important_count = len([m for m in day_meetings if m['importance_score'] >= 30])
    prep_count = len([m for m in day_meetings if m['prep_time'] > 0])
    total_prep = sum(m['prep_time'] for m in day_meetings)
    total_meeting_time = sum((m['end'] - m['start']).total_seconds() / 60 for m in day_meetings)
    
    print(f"\n📊 Summary:")
    print(f"   • Total Meetings: {len(day_meetings)}")
    print(f"   • Important Meetings: {important_count}")
    print(f"   • Requiring Prep: {prep_count}")
    print(f"   • Total Meeting Time: {total_meeting_time/60:.1f} hours")
    print(f"   • Total Prep Time: {total_prep} minutes")
    
    # Prep needed today/yesterday
    if prep_count > 0:
        yesterday = date_obj - timedelta(days=1)
        print(f"\n⏰ PREP ALERT:")
        print(f"   You should have blocked {total_prep} minutes yesterday ({yesterday.strftime('%B %d')})")
        print(f"   for meeting preparation. If not done, prep early today!")
    
    # Meeting schedule
    print(f"\n{'=' * 80}")
    print("📅 TODAY'S SCHEDULE")
    print("=" * 80)
    
    for i, meeting in enumerate(day_meetings, 1):
        duration = (meeting['end'] - meeting['start']).total_seconds() / 60
        
        # Header
        print(f"\n{i}. {meeting['start'].strftime('%H:%M')}-{meeting['end'].strftime('%H:%M')} ({int(duration)}min) | {meeting['subject']}")
        
        # Details
        details = []
        details.append(f"👥 {meeting['attendee_count']} attendees")
        if meeting['is_online']:
            details.append("🌐 Online")
        if meeting['importance_score'] >= 30:
            details.append(f"🔴 Important (Score: {meeting['importance_score']})")
        if meeting['prep_time'] > 0:
            details.append(f"⏰ {meeting['prep_time']}min prep needed")
        
        print(f"   {' | '.join(details)}")
        
        # Why important
        if meeting['reasons']:
            print(f"   💡 {', '.join(meeting['reasons'][:2])}")
    
    # Recommendations
    print(f"\n{'=' * 80}")
    print("💡 RECOMMENDATIONS")
    print("=" * 80)
    
    # Find longest gap for deep work
    if len(day_meetings) > 1:
        gaps = []
        for i in range(len(day_meetings) - 1):
            gap_start = day_meetings[i]['end']
            gap_end = day_meetings[i + 1]['start']
            gap_duration = (gap_end - gap_start).total_seconds() / 60
            if gap_duration >= 30:
                gaps.append({
                    'start': gap_start,
                    'end': gap_end,
                    'duration': gap_duration
                })
        
        if gaps:
            longest_gap = max(gaps, key=lambda x: x['duration'])
            print(f"\n🎯 Best time for focused work:")
            print(f"   {longest_gap['start'].strftime('%H:%M')}-{longest_gap['end'].strftime('%H:%M')} ({int(longest_gap['duration'])} minutes)")
    
    # Prep reminder
    if prep_count > 0:
        meetings_needing_prep = [m for m in day_meetings if m['prep_time'] > 0]
        first_important = meetings_needing_prep[0]
        
        print(f"\n⚠️  Preparation Reminder:")
        print(f"   First important meeting: {first_important['start'].strftime('%H:%M')} - {first_important['subject']}")
        print(f"   Suggested prep: {first_important['prep_time']} minutes before the meeting")
        
        # Find time to prep
        if day_meetings[0]['start'] > date_obj.replace(hour=8, minute=0):
            morning_gap = (day_meetings[0]['start'] - date_obj.replace(hour=8, minute=0)).total_seconds() / 60
            if morning_gap >= total_prep:
                print(f"   ✅ You have {int(morning_gap)} minutes before first meeting - use for prep!")
    
    # Meeting density warning
    if len(day_meetings) >= 5:
        print(f"\n⚠️  High Meeting Density Alert:")
        print(f"   You have {len(day_meetings)} meetings today!")
        print(f"   Recommendation: Block lunch time and end-of-day for recovery")
    
    # Tomorrow's prep preview
    tomorrow = date_obj + timedelta(days=1)
    tomorrow_meetings = []
    for meeting in tracker.meetings:
        start_str = meeting.get('start', {}).get('dateTime', '')
        if not start_str:
            continue
        start_dt = datetime.fromisoformat(start_str.replace('Z', '+00:00').split('.')[0])
        if start_dt.date() == tomorrow.date():
            importance_score, _ = tracker.calculate_importance_score(meeting)
            prep_time = tracker.estimate_prep_time(meeting, importance_score)
            if prep_time > 0:
                tomorrow_meetings.append({
                    'subject': meeting.get('subject'),
                    'prep_time': prep_time
                })
    
    if tomorrow_meetings:
        total_tomorrow_prep = sum(m['prep_time'] for m in tomorrow_meetings)
        print(f"\n📅 Tomorrow's Prep Preview ({tomorrow.strftime('%B %d')}):")
        print(f"   {len(tomorrow_meetings)} meeting(s) requiring {total_tomorrow_prep} minutes prep")
        print(f"   💡 Block time today to prepare!")
    
    print(f"\n{'=' * 80}")


def main():
    """Main execution."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Daily meeting digest')
    parser.add_argument('--date', help='Target date (YYYY-MM-DD), default: today')
    
    args = parser.parse_args()
    
    print_daily_digest(args.date)


if __name__ == '__main__':
    main()
