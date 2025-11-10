#!/usr/bin/env python3
"""
Calendar Visualization Tool for Training Data

Visualizes generated 4-week calendars in multiple formats:
1. Weekly grid view (like Outlook/Google Calendar)
2. Daily timeline view with meeting details
3. Statistics dashboard
4. HTML export for sharing

Usage:
    # View Tier 1 Sales Manager calendar
    python post_training/tools/visualize_calendar.py \
        --calendar post_training/data/training/calendars/tier1_sales_manager_pipeline_calendar_4weeks.jsonl
    
    # Compare all three tiers
    python post_training/tools/visualize_calendar.py \
        --calendar post_training/data/training/calendars/tier1_sales_manager_pipeline_calendar_4weeks.jsonl \
        --calendar post_training/data/training/calendars/tier2_senior_ic_architect_calendar_4weeks.jsonl \
        --calendar post_training/data/training/calendars/tier3_specialist_legal_calendar_4weeks.jsonl \
        --compare
    
    # Export to HTML
    python post_training/tools/visualize_calendar.py \
        --calendar post_training/data/training/calendars/tier1_sales_manager_pipeline_calendar_4weeks.jsonl \
        --output calendar_view.html
"""

import argparse
import json
import sys
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# Terminal colors for rich output
class Colors:
    CRITICAL = '\033[91m'  # Red
    HIGH = '\033[93m'      # Yellow
    MEDIUM = '\033[92m'    # Green
    LOW = '\033[94m'       # Blue
    PREP = '\033[95m'      # Magenta
    RESET = '\033[0m'      # Reset
    BOLD = '\033[1m'
    DIM = '\033[2m'


def load_calendar(calendar_path: Path) -> List[Dict[str, Any]]:
    """Load calendar from JSONL file."""
    meetings = []
    with open(calendar_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                meetings.append(json.loads(line))
    return meetings


def parse_datetime(dt_str: str) -> datetime:
    """Parse ISO datetime string."""
    # Handle format: "2025-11-17T10:00:00.0000000"
    if '.' in dt_str:
        dt_str = dt_str.split('.')[0]
    return datetime.fromisoformat(dt_str)


def format_time(dt: datetime) -> str:
    """Format time as HH:MM AM/PM."""
    return dt.strftime("%I:%M %p").lstrip('0')


def get_importance_color(importance: str) -> str:
    """Get terminal color for importance level."""
    colors = {
        'critical': Colors.CRITICAL,
        'high': Colors.HIGH,
        'medium': Colors.MEDIUM,
        'low': Colors.LOW
    }
    return colors.get(importance.lower(), Colors.RESET)


def get_importance_emoji(importance: str) -> str:
    """Get emoji for importance level."""
    emojis = {
        'critical': '🔴',
        'high': '🟡',
        'medium': '🟢',
        'low': '🔵'
    }
    return emojis.get(importance.lower(), '⚪')


def print_weekly_grid(meetings: List[Dict[str, Any]], persona_name: str):
    """Print calendar in weekly grid view."""
    # Group meetings by week
    weeks = defaultdict(lambda: defaultdict(list))
    
    for meeting in meetings:
        start_dt = parse_datetime(meeting['start']['dateTime'])
        week_num = start_dt.isocalendar()[1]
        day_name = start_dt.strftime('%A')
        weeks[week_num][day_name].append(meeting)
    
    print(f"\n{Colors.BOLD}{'='*100}{Colors.RESET}")
    print(f"{Colors.BOLD}📅 Calendar View: {persona_name}{Colors.RESET}")
    print(f"{Colors.BOLD}{'='*100}{Colors.RESET}\n")
    
    # Print each week
    for week_num in sorted(weeks.keys()):
        week_meetings = weeks[week_num]
        
        # Get week date range
        first_meeting = min(
            [m for day_meetings in week_meetings.values() for m in day_meetings],
            key=lambda m: parse_datetime(m['start']['dateTime'])
        )
        start_dt = parse_datetime(first_meeting['start']['dateTime'])
        week_start = start_dt - timedelta(days=start_dt.weekday())
        week_end = week_start + timedelta(days=6)
        
        print(f"{Colors.BOLD}Week {week_num}: {week_start.strftime('%b %d')} - {week_end.strftime('%b %d, %Y')}{Colors.RESET}")
        print(f"{Colors.DIM}{'─'*100}{Colors.RESET}")
        
        # Print each day
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        for day in days:
            day_meetings = sorted(
                week_meetings.get(day, []),
                key=lambda m: parse_datetime(m['start']['dateTime'])
            )
            
            if not day_meetings:
                continue
            
            # Day header
            first_meeting_dt = parse_datetime(day_meetings[0]['start']['dateTime'])
            day_date = first_meeting_dt.strftime('%b %d')
            print(f"\n  {Colors.BOLD}{day}, {day_date}{Colors.RESET} ({len(day_meetings)} meetings)")
            
            # Print meetings
            for meeting in day_meetings:
                start_dt = parse_datetime(meeting['start']['dateTime'])
                end_dt = parse_datetime(meeting['end']['dateTime'])
                duration = int((end_dt - start_dt).total_seconds() / 60)
                
                importance = meeting.get('importance_label', 'medium')
                prep_needed = meeting.get('prep_needed', False)
                prep_time = meeting.get('prep_time_minutes', 0)
                
                color = get_importance_color(importance)
                emoji = get_importance_emoji(importance)
                prep_emoji = '📝' if prep_needed else '  '
                
                subject = meeting['subject'][:60] + '...' if len(meeting['subject']) > 60 else meeting['subject']
                
                print(f"    {format_time(start_dt):>8} - {format_time(end_dt):<8} "
                      f"{emoji} {color}{subject}{Colors.RESET} "
                      f"{Colors.DIM}({duration}min){Colors.RESET} {prep_emoji}")
                
                if prep_needed and prep_time > 0:
                    print(f"                              {Colors.DIM}└─ Prep: {prep_time} min{Colors.RESET}")
        
        print()


def print_daily_timeline(meetings: List[Dict[str, Any]], persona_name: str, target_date: Optional[datetime] = None):
    """Print detailed timeline for a specific day."""
    if target_date is None:
        # Use first meeting's date
        target_date = parse_datetime(meetings[0]['start']['dateTime'])
    
    # Filter meetings for target date
    day_meetings = [
        m for m in meetings
        if parse_datetime(m['start']['dateTime']).date() == target_date.date()
    ]
    
    if not day_meetings:
        print(f"No meetings found for {target_date.strftime('%B %d, %Y')}")
        return
    
    day_meetings = sorted(day_meetings, key=lambda m: parse_datetime(m['start']['dateTime']))
    
    print(f"\n{Colors.BOLD}{'='*100}{Colors.RESET}")
    print(f"{Colors.BOLD}📋 Daily Timeline: {persona_name} - {target_date.strftime('%A, %B %d, %Y')}{Colors.RESET}")
    print(f"{Colors.BOLD}{'='*100}{Colors.RESET}\n")
    
    for i, meeting in enumerate(day_meetings, 1):
        start_dt = parse_datetime(meeting['start']['dateTime'])
        end_dt = parse_datetime(meeting['end']['dateTime'])
        duration = int((end_dt - start_dt).total_seconds() / 60)
        
        importance = meeting.get('importance_label', 'medium')
        prep_needed = meeting.get('prep_needed', False)
        prep_time = meeting.get('prep_time_minutes', 0)
        reasoning = meeting.get('reasoning', '')
        
        color = get_importance_color(importance)
        emoji = get_importance_emoji(importance)
        
        # Meeting header
        print(f"{Colors.BOLD}Meeting {i}/{len(day_meetings)}{Colors.RESET}")
        print(f"{Colors.DIM}{'─'*100}{Colors.RESET}")
        print(f"  {emoji} {Colors.BOLD}{meeting['subject']}{Colors.RESET}")
        print(f"  ⏰ {format_time(start_dt)} - {format_time(end_dt)} ({duration} minutes)")
        print(f"  {color}▸ Importance: {importance.upper()}{Colors.RESET}")
        
        if prep_needed:
            print(f"  📝 Prep Required: {prep_time} minutes")
        
        # Attendees
        attendees = meeting.get('attendees', [])
        if attendees:
            required = [a for a in attendees if a.get('type') == 'required']
            optional = [a for a in attendees if a.get('type') == 'optional']
            resources = [a for a in attendees if a.get('type') == 'resource']
            
            print(f"  👥 Attendees: {len(required)} required", end='')
            if optional:
                print(f", {len(optional)} optional", end='')
            if resources:
                print(f", {len(resources)} resources", end='')
            print()
        
        # Meeting description
        body = meeting.get('bodyPreview', '')
        if body:
            # Wrap text at 90 chars
            wrapped_lines = []
            current_line = ""
            for word in body.split():
                if len(current_line) + len(word) + 1 <= 90:
                    current_line += word + " "
                else:
                    wrapped_lines.append(current_line.strip())
                    current_line = word + " "
            if current_line:
                wrapped_lines.append(current_line.strip())
            
            print(f"  {Colors.DIM}Description:{Colors.RESET}")
            for line in wrapped_lines:
                print(f"    {line}")
        
        # Reasoning
        if reasoning:
            print(f"  {Colors.DIM}Reasoning: {reasoning}{Colors.RESET}")
        
        print()


def print_statistics(meetings: List[Dict[str, Any]], persona_name: str):
    """Print calendar statistics."""
    total = len(meetings)
    
    # Importance distribution
    importance_dist = defaultdict(int)
    for meeting in meetings:
        importance_dist[meeting.get('importance_label', 'unknown')] += 1
    
    # Prep time analysis
    prep_meetings = [m for m in meetings if m.get('prep_needed', False)]
    total_prep_time = sum(m.get('prep_time_minutes', 0) for m in prep_meetings)
    
    # Meeting types
    recurring = sum(1 for m in meetings if m.get('type') == 'occurrence')
    ad_hoc = total - recurring
    
    # Duration analysis
    durations = []
    for meeting in meetings:
        start_dt = parse_datetime(meeting['start']['dateTime'])
        end_dt = parse_datetime(meeting['end']['dateTime'])
        duration = int((end_dt - start_dt).total_seconds() / 60)
        durations.append(duration)
    
    avg_duration = sum(durations) / len(durations) if durations else 0
    
    # Weekly distribution
    weeks = defaultdict(int)
    for meeting in meetings:
        start_dt = parse_datetime(meeting['start']['dateTime'])
        week_num = start_dt.isocalendar()[1]
        weeks[week_num] += 1
    
    print(f"\n{Colors.BOLD}{'='*100}{Colors.RESET}")
    print(f"{Colors.BOLD}📊 Calendar Statistics: {persona_name}{Colors.RESET}")
    print(f"{Colors.BOLD}{'='*100}{Colors.RESET}\n")
    
    print(f"{Colors.BOLD}Overall:{Colors.RESET}")
    print(f"  Total Meetings: {total}")
    print(f"  Weeks: {len(weeks)}")
    print(f"  Avg Meetings/Week: {total / len(weeks):.1f}")
    print(f"  Avg Meeting Duration: {avg_duration:.0f} minutes")
    
    print(f"\n{Colors.BOLD}Importance Distribution:{Colors.RESET}")
    for importance in ['critical', 'high', 'medium', 'low']:
        count = importance_dist.get(importance, 0)
        pct = (count / total * 100) if total > 0 else 0
        emoji = get_importance_emoji(importance)
        color = get_importance_color(importance)
        bar = '█' * int(pct / 2)
        print(f"  {emoji} {color}{importance.capitalize():8}{Colors.RESET}: {count:3} ({pct:5.1f}%) {bar}")
    
    print(f"\n{Colors.BOLD}Meeting Types:{Colors.RESET}")
    print(f"  🔄 Recurring: {recurring} ({recurring/total*100:.1f}%)")
    print(f"  📌 Ad-hoc:    {ad_hoc} ({ad_hoc/total*100:.1f}%)")
    
    print(f"\n{Colors.BOLD}Prep Time Analysis:{Colors.RESET}")
    print(f"  Meetings Requiring Prep: {len(prep_meetings)} ({len(prep_meetings)/total*100:.1f}%)")
    print(f"  Total Prep Time: {total_prep_time} minutes ({total_prep_time/60:.1f} hours)")
    print(f"  Avg Prep Time/Week: {total_prep_time/len(weeks)/60:.1f} hours")
    if prep_meetings:
        print(f"  Avg Prep Time/Meeting: {total_prep_time/len(prep_meetings):.0f} minutes")
    
    print(f"\n{Colors.BOLD}Weekly Distribution:{Colors.RESET}")
    for week_num in sorted(weeks.keys()):
        count = weeks[week_num]
        bar = '█' * int(count / 3)
        print(f"  Week {week_num}: {count:2} meetings {bar}")
    
    print()


def export_html(meetings: List[Dict[str, Any]], persona_name: str, output_path: Path):
    """Export calendar to HTML for sharing."""
    # Group meetings by week and day
    weeks = defaultdict(lambda: defaultdict(list))
    for meeting in meetings:
        start_dt = parse_datetime(meeting['start']['dateTime'])
        week_num = start_dt.isocalendar()[1]
        day_name = start_dt.strftime('%A')
        weeks[week_num][day_name].append(meeting)
    
    html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Calendar View - {persona_name}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
        }}
        .header h1 {{
            margin: 0;
            font-size: 32px;
        }}
        .week {{
            background: white;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 30px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .week-header {{
            font-size: 24px;
            font-weight: bold;
            color: #333;
            margin-bottom: 20px;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
        }}
        .day {{
            margin-bottom: 25px;
        }}
        .day-header {{
            font-size: 18px;
            font-weight: bold;
            color: #555;
            margin-bottom: 10px;
            padding: 10px;
            background-color: #f8f9fa;
            border-left: 4px solid #667eea;
        }}
        .meeting {{
            margin-left: 20px;
            margin-bottom: 15px;
            padding: 15px;
            border-left: 4px solid;
            background-color: #fafafa;
            border-radius: 5px;
        }}
        .meeting.critical {{ border-left-color: #dc3545; background-color: #fff5f5; }}
        .meeting.high {{ border-left-color: #ffc107; background-color: #fffef5; }}
        .meeting.medium {{ border-left-color: #28a745; background-color: #f5fff5; }}
        .meeting.low {{ border-left-color: #17a2b8; background-color: #f5fcff; }}
        .meeting-time {{
            font-weight: bold;
            color: #666;
            font-size: 14px;
        }}
        .meeting-subject {{
            font-size: 16px;
            font-weight: bold;
            color: #333;
            margin: 5px 0;
        }}
        .meeting-description {{
            color: #666;
            font-size: 14px;
            margin: 5px 0;
        }}
        .meeting-meta {{
            display: flex;
            gap: 20px;
            margin-top: 10px;
            font-size: 13px;
            color: #888;
        }}
        .badge {{
            display: inline-block;
            padding: 3px 8px;
            border-radius: 12px;
            font-size: 11px;
            font-weight: bold;
        }}
        .badge.critical {{ background-color: #dc3545; color: white; }}
        .badge.high {{ background-color: #ffc107; color: #333; }}
        .badge.medium {{ background-color: #28a745; color: white; }}
        .badge.low {{ background-color: #17a2b8; color: white; }}
        .prep-indicator {{
            background-color: #9c27b0;
            color: white;
            padding: 3px 8px;
            border-radius: 12px;
            font-size: 11px;
            font-weight: bold;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>📅 Calendar View: {persona_name}</h1>
        <p>Generated training data calendar visualization</p>
    </div>
"""
    
    # Generate weeks
    for week_num in sorted(weeks.keys()):
        week_meetings = weeks[week_num]
        
        # Get week date range
        first_meeting = min(
            [m for day_meetings in week_meetings.values() for m in day_meetings],
            key=lambda m: parse_datetime(m['start']['dateTime'])
        )
        start_dt = parse_datetime(first_meeting['start']['dateTime'])
        week_start = start_dt - timedelta(days=start_dt.weekday())
        week_end = week_start + timedelta(days=6)
        
        html += f"""
    <div class="week">
        <div class="week-header">Week {week_num}: {week_start.strftime('%b %d')} - {week_end.strftime('%b %d, %Y')}</div>
"""
        
        # Generate days
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        for day in days:
            day_meetings = sorted(
                week_meetings.get(day, []),
                key=lambda m: parse_datetime(m['start']['dateTime'])
            )
            
            if not day_meetings:
                continue
            
            first_meeting_dt = parse_datetime(day_meetings[0]['start']['dateTime'])
            day_date = first_meeting_dt.strftime('%b %d')
            
            html += f"""
        <div class="day">
            <div class="day-header">{day}, {day_date} ({len(day_meetings)} meetings)</div>
"""
            
            for meeting in day_meetings:
                start_dt = parse_datetime(meeting['start']['dateTime'])
                end_dt = parse_datetime(meeting['end']['dateTime'])
                duration = int((end_dt - start_dt).total_seconds() / 60)
                
                importance = meeting.get('importance_label', 'medium')
                prep_needed = meeting.get('prep_needed', False)
                prep_time = meeting.get('prep_time_minutes', 0)
                
                prep_badge = f'<span class="prep-indicator">📝 Prep: {prep_time}min</span>' if prep_needed else ''
                
                html += f"""
            <div class="meeting {importance}">
                <div class="meeting-time">{format_time(start_dt)} - {format_time(end_dt)} ({duration} min)</div>
                <div class="meeting-subject">{meeting['subject']}</div>
                <div class="meeting-description">{meeting.get('bodyPreview', '')[:150]}...</div>
                <div class="meeting-meta">
                    <span class="badge {importance}">{importance.upper()}</span>
                    {prep_badge}
                    <span>{len(meeting.get('attendees', []))} attendees</span>
                </div>
            </div>
"""
            
            html += """
        </div>
"""
        
        html += """
    </div>
"""
    
    html += """
</body>
</html>
"""
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✅ HTML calendar exported to: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Visualize calendar training data"
    )
    
    parser.add_argument(
        '--calendar',
        type=Path,
        action='append',
        required=True,
        help='Path to calendar JSONL file (can specify multiple for comparison)'
    )
    
    parser.add_argument(
        '--view',
        choices=['week', 'day', 'stats', 'all'],
        default='all',
        help='View mode: week (grid), day (timeline), stats (statistics), all (default)'
    )
    
    parser.add_argument(
        '--date',
        type=str,
        help='Target date for day view (YYYY-MM-DD)'
    )
    
    parser.add_argument(
        '--output',
        type=Path,
        help='Export to HTML file'
    )
    
    parser.add_argument(
        '--compare',
        action='store_true',
        help='Compare multiple calendars side-by-side'
    )
    
    args = parser.parse_args()
    
    # Load calendars
    calendars = []
    for cal_path in args.calendar:
        meetings = load_calendar(cal_path)
        persona_id = meetings[0].get('persona_id', 'unknown')
        
        # Extract persona name from first meeting
        persona_name = persona_id.replace('_', ' ').title()
        calendars.append({
            'path': cal_path,
            'meetings': meetings,
            'persona_name': persona_name,
            'persona_id': persona_id
        })
    
    # Parse target date if provided
    target_date = None
    if args.date:
        target_date = datetime.strptime(args.date, '%Y-%m-%d')
    
    # Display calendars
    for calendar in calendars:
        if args.view in ['week', 'all']:
            print_weekly_grid(calendar['meetings'], calendar['persona_name'])
        
        if args.view in ['day', 'all']:
            print_daily_timeline(calendar['meetings'], calendar['persona_name'], target_date)
        
        if args.view in ['stats', 'all']:
            print_statistics(calendar['meetings'], calendar['persona_name'])
        
        # Export to HTML if requested
        if args.output:
            if len(calendars) == 1:
                export_html(calendar['meetings'], calendar['persona_name'], args.output)
            else:
                # Multi-calendar export
                output_name = args.output.stem
                output_ext = args.output.suffix
                output_path = args.output.parent / f"{output_name}_{calendar['persona_id']}{output_ext}"
                export_html(calendar['meetings'], calendar['persona_name'], output_path)
    
    # Comparison view
    if args.compare and len(calendars) > 1:
        print(f"\n{Colors.BOLD}{'='*100}{Colors.RESET}")
        print(f"{Colors.BOLD}🔄 Calendar Comparison{Colors.RESET}")
        print(f"{Colors.BOLD}{'='*100}{Colors.RESET}\n")
        
        for calendar in calendars:
            total = len(calendar['meetings'])
            importance_dist = defaultdict(int)
            for m in calendar['meetings']:
                importance_dist[m.get('importance_label', 'unknown')] += 1
            
            prep_count = sum(1 for m in calendar['meetings'] if m.get('prep_needed', False))
            
            print(f"{Colors.BOLD}{calendar['persona_name']}{Colors.RESET}")
            print(f"  Total: {total} meetings")
            print(f"  Critical: {importance_dist['critical']} ({importance_dist['critical']/total*100:.1f}%)")
            print(f"  Prep Needed: {prep_count} ({prep_count/total*100:.1f}%)")
            print()


if __name__ == "__main__":
    main()
