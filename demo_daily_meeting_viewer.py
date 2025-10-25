#!/usr/bin/env python3
"""
Scenara Daily Meeting Viewer - Demo Version
Demonstrates beautiful meeting display using local data
"""

import argparse
import json
import os
import sys
import zoneinfo
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import List, Dict, Optional


def demo_daily_meetings(target_date_str: str, format_type: str = 'md', console_only: bool = False):
    """
    Demo function using existing local meeting data
    """
    print(f"🎯 Scenara Daily Meeting Viewer Demo")
    print(f"📅 Simulating meetings for {target_date_str}")
    print("=" * 60)
    
    # Parse the target date
    try:
        if len(target_date_str) != 8 or not target_date_str.isdigit():
            raise ValueError("Date must be in format YYYYMMDD")
        
        year = int(target_date_str[:4])
        month = int(target_date_str[4:6])
        day = int(target_date_str[6:8])
        target_date = datetime(year, month, day, 0, 0, 0, tzinfo=timezone.utc)
        
    except ValueError as e:
        print(f"❌ Invalid date format: {e}")
        return
    
    # Load sample meeting data from local files
    local_files = list(Path('.').glob("my_calendar_events*.json"))
    if not local_files:
        print("⚠️ No local meeting data found. In a real scenario, this would:")
        print("   1. Authenticate with Microsoft Graph")
        print("   2. Fetch meetings for the specified date")
        print("   3. Format them beautifully")
        
        # Create sample demo meetings
        demo_meetings = create_demo_meetings(target_date)
    else:
        print(f"📊 Using sample data from: {local_files[0].name}")
        with open(local_files[0], 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Take first few meetings as demo
        raw_meetings = data.get('value', [])[:5]  # Limit to 5 for demo
        demo_meetings = process_sample_meetings(raw_meetings, target_date)
    
    # Display results
    display_console_summary(demo_meetings, target_date)
    
    if not console_only:
        # Generate formatted output
        if format_type == 'md':
            content = generate_markdown(demo_meetings, target_date)
            save_output(content, 'md', target_date_str)
        elif format_type == 'html':
            content = generate_html(demo_meetings, target_date)
            save_output(content, 'html', target_date_str)
        elif format_type == 'json':
            content = json.dumps({
                'date': target_date.isoformat(),
                'meetings': demo_meetings,
                'demo_note': 'This is demo data for illustration purposes'
            }, indent=2, ensure_ascii=False)
            save_output(content, 'json', target_date_str)


def create_demo_meetings(target_date: datetime) -> List[Dict]:
    """Create sample meetings for demo purposes"""
    return [
        {
            'id': 'demo-1',
            'subject': 'Scenara Project Review',
            'start_time': '09:00',
            'end_time': '10:00',
            'duration_minutes': 60,
            'location': '',
            'is_online_meeting': True,
            'online_meeting_url': 'https://teams.microsoft.com/meet/demo',
            'attendees': [
                {'name': 'Alice Johnson', 'email': 'alice@company.com', 'response': 'accepted'},
                {'name': 'Bob Smith', 'email': 'bob@company.com', 'response': 'tentative'}
            ],
            'attendee_count': 2,
            'body_preview': 'Weekly review of Scenara meeting intelligence platform progress and next steps.',
            'importance': 'high',
            'is_organizer': True,
            'response_status': 'organizer',
            'web_link': 'https://outlook.office365.com/demo'
        },
        {
            'id': 'demo-2',
            'subject': 'Client Demo Preparation',
            'start_time': '14:00',
            'end_time': '15:30',
            'duration_minutes': 90,
            'location': 'Conference Room A',
            'is_online_meeting': False,
            'online_meeting_url': '',
            'attendees': [
                {'name': 'Carol Wilson', 'email': 'carol@company.com', 'response': 'accepted'},
                {'name': 'David Lee', 'email': 'david@company.com', 'response': 'accepted'},
                {'name': 'Eve Martinez', 'email': 'eve@company.com', 'response': 'accepted'}
            ],
            'attendee_count': 3,
            'body_preview': 'Prepare demonstration materials and agenda for upcoming client presentation.',
            'importance': 'normal',
            'is_organizer': False,
            'response_status': 'accepted',
            'web_link': 'https://outlook.office365.com/demo2'
        },
        {
            'id': 'demo-3',
            'subject': '1:1 with Manager',
            'start_time': '16:00',
            'end_time': '16:30',
            'duration_minutes': 30,
            'location': '',
            'is_online_meeting': True,
            'online_meeting_url': 'https://teams.microsoft.com/meet/demo3',
            'attendees': [
                {'name': 'Manager Name', 'email': 'manager@company.com', 'response': 'accepted'}
            ],
            'attendee_count': 1,
            'body_preview': 'Regular check-in to discuss progress, challenges, and career development.',
            'importance': 'normal',
            'is_organizer': False,
            'response_status': 'accepted',
            'web_link': 'https://outlook.office365.com/demo3'
        }
    ]


def process_sample_meetings(raw_meetings: List[Dict], target_date: datetime) -> List[Dict]:
    """Process sample meetings from local data with proper timezone handling"""
    processed = []
    
    # Set up local timezone (Pacific Time)
    try:
        local_tz = zoneinfo.ZoneInfo("America/Los_Angeles")
    except:
        # Fallback for older Python versions
        local_tz = timezone(timedelta(hours=-7))  # PDT
    
    for i, meeting in enumerate(raw_meetings):
        # Try to extract real meeting times, fallback to simulation
        start_time_str = "09:00"  # default
        end_time_str = "10:00"    # default
        timezone_str = "PDT"
        
        if meeting.get('start') and meeting.get('end'):
            try:
                # Parse actual meeting times if available
                start_dt = datetime.fromisoformat(meeting['start']['dateTime'].replace('Z', '+00:00'))
                end_dt = datetime.fromisoformat(meeting['end']['dateTime'].replace('Z', '+00:00'))
                
                # Convert to local timezone
                start_local = start_dt.astimezone(local_tz)
                end_local = end_dt.astimezone(local_tz)
                
                start_time_str = start_local.strftime('%H:%M')
                end_time_str = end_local.strftime('%H:%M')
                timezone_str = start_local.strftime('%Z')
                duration = int((end_dt - start_dt).total_seconds() / 60)
            except:
                # Fallback to simulation if parsing fails
                start_hour = 9 + (i * 2)  # Space meetings 2 hours apart starting at 9 AM
                start_time_str = f'{start_hour:02d}:00'
                end_time_str = f'{start_hour+1:02d}:00'
                duration = 60
        else:
            # Simulate realistic meeting times for demo
            start_hour = 9 + (i * 2)  # Space meetings 2 hours apart starting at 9 AM
            start_time_str = f'{start_hour:02d}:00'
            end_time_str = f'{start_hour+1:02d}:00'
            duration = 60
        
        # Extract attendees
        attendees = []
        if meeting.get('attendees'):
            for attendee in meeting['attendees'][:3]:  # Limit to 3 for demo
                if attendee.get('emailAddress'):
                    attendees.append({
                        'name': attendee['emailAddress'].get('name', 'Unknown'),
                        'email': attendee['emailAddress'].get('address', ''),
                        'response': attendee.get('status', {}).get('response', 'none')
                    })
        
        processed.append({
            'id': meeting.get('id', f'demo-{i}'),
            'subject': meeting.get('subject', 'Sample Meeting'),
            'start_time': start_time_str,
            'end_time': end_time_str,
            'timezone': timezone_str,
            'duration_minutes': duration,
            'location': meeting.get('location', {}).get('displayName', ''),
            'is_online_meeting': meeting.get('isOnlineMeeting', True),
            'online_meeting_url': meeting.get('onlineMeetingUrl', ''),
            'attendees': attendees,
            'attendee_count': len(attendees),
            'body_preview': meeting.get('bodyPreview', '')[:100] + '...' if meeting.get('bodyPreview') else 'Meeting details not available.',
            'importance': meeting.get('importance', 'normal'),
            'is_organizer': meeting.get('isOrganizer', False),
            'response_status': meeting.get('responseStatus', {}).get('response', 'none'),
            'web_link': meeting.get('webLink', '')
        })
    
    return processed


def display_console_summary(meetings: List[Dict], target_date: datetime):
    """Display beautiful console summary"""
    date_str = target_date.strftime('%B %d, %Y')
    
    print(f"\n📅 Daily Meeting Schedule - {date_str}")
    print("=" * 60)
    
    if not meetings:
        print("🎉 No meetings scheduled!")
        print("   Perfect day for focus work and catching up! ☕")
        return
    
    print(f"📊 Total meetings: {len(meetings)}")
    print()
    
    for i, meeting in enumerate(meetings, 1):
        duration_hrs = meeting['duration_minutes'] // 60
        duration_mins = meeting['duration_minutes'] % 60
        duration_str = f"{duration_hrs}h {duration_mins}m" if duration_hrs > 0 else f"{duration_mins}m"
        
        print(f"{i}. {meeting['subject']}")
        print(f"   ⏰ {meeting['start_time']} - {meeting['end_time']} {meeting.get('timezone', 'PDT')} ({duration_str})")
        
        if meeting['is_online_meeting']:
            print("   🌐 Online Meeting")
        elif meeting['location']:
            print(f"   📍 {meeting['location']}")
        
        if meeting['attendees']:
            print(f"   👥 {meeting['attendee_count']} attendees")
            if len(meeting['attendees']) <= 3:
                attendee_names = [a['name'] for a in meeting['attendees']]
                print(f"      ({', '.join(attendee_names)})")
        
        if meeting['importance'] != 'normal':
            importance_emoji = {'high': '🔴', 'low': '🔵'}.get(meeting['importance'], '⚪')
            print(f"   {importance_emoji} {meeting['importance'].title()} priority")
        
        print()
    
    # Summary
    total_duration = sum(m['duration_minutes'] for m in meetings)
    total_hrs = total_duration // 60
    total_mins = total_duration % 60
    
    print("📈 Summary:")
    print(f"   Total meeting time: {total_hrs}h {total_mins}m")
    print(f"   Online meetings: {sum(1 for m in meetings if m['is_online_meeting'])}")
    print(f"   You're organizing: {sum(1 for m in meetings if m['is_organizer'])}")


def generate_markdown(meetings: List[Dict], target_date: datetime) -> str:
    """Generate markdown format"""
    date_str = target_date.strftime('%B %d, %Y')
    
    md_content = f"""# 📅 Daily Meeting Schedule - {date_str}

Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
Total meetings: **{len(meetings)}**

---

"""
    
    if not meetings:
        md_content += """## 🎉 No meetings scheduled!

Perfect day for focus work! 🎯

"""
        return md_content
    
    for i, meeting in enumerate(meetings, 1):
        duration_hrs = meeting['duration_minutes'] // 60
        duration_mins = meeting['duration_minutes'] % 60
        duration_str = f"{duration_hrs}h {duration_mins}m" if duration_hrs > 0 else f"{duration_mins}m"
        
        md_content += f"""## {i}. {meeting['subject']}

**⏰ Time:** {meeting['start_time']} - {meeting['end_time']} {meeting.get('timezone', 'PDT')} ({duration_str})  
"""
        
        if meeting['is_online_meeting']:
            md_content += f"**📍 Location:** 🌐 Online Meeting  \n"
            if meeting['online_meeting_url']:
                md_content += f"**🔗 Join Link:** [Join Meeting]({meeting['online_meeting_url']})  \n"
        elif meeting['location']:
            md_content += f"**📍 Location:** {meeting['location']}  \n"
        
        if meeting['attendees']:
            md_content += f"**👥 Attendees:** {meeting['attendee_count']} people  \n"
            if len(meeting['attendees']) <= 5:
                attendee_list = []
                for attendee in meeting['attendees']:
                    status_emoji = {
                        'accepted': '✅',
                        'declined': '❌',
                        'tentative': '❓',
                        'none': '⏳'
                    }.get(attendee['response'], '⏳')
                    attendee_list.append(f"{status_emoji} {attendee['name']}")
                md_content += f"  - {', '.join(attendee_list)}  \n"
        
        if meeting['importance'] != 'normal':
            importance_emoji = {'high': '🔴', 'low': '🔵'}.get(meeting['importance'], '⚪')
            md_content += f"**Priority:** {importance_emoji} {meeting['importance'].title()}  \n"
        
        if meeting['body_preview']:
            md_content += f"""
**📝 Description:**
> {meeting['body_preview']}

"""
        
        md_content += "\n---\n\n"
    
    # Summary
    total_duration = sum(m['duration_minutes'] for m in meetings)
    total_hrs = total_duration // 60
    total_mins = total_duration % 60
    
    md_content += f"""## 📊 Daily Summary

- **Total Meetings:** {len(meetings)}
- **Total Meeting Time:** {total_hrs}h {total_mins}m
- **Online Meetings:** {sum(1 for m in meetings if m['is_online_meeting'])}
- **Meetings You're Organizing:** {sum(1 for m in meetings if m['is_organizer'])}

---

*Generated by Scenara Meeting Intelligence* 🚀
"""
    
    return md_content


def generate_html(meetings: List[Dict], target_date: datetime) -> str:
    """Generate HTML format"""
    date_str = target_date.strftime('%B %d, %Y')
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Daily Meetings - {date_str}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            line-height: 1.6;
            color: #333;
            background-color: #f8f9fa;
        }}
        .container {{
            background: white;
            border-radius: 10px;
            padding: 30px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }}
        .meeting {{
            background: #f8f9fa;
            border-left: 4px solid #3498db;
            margin: 20px 0;
            padding: 20px;
            border-radius: 5px;
        }}
        .meeting-title {{
            color: #2c3e50;
            margin-top: 0;
            font-size: 1.3em;
        }}
        .meeting-time {{
            background: #3498db;
            color: white;
            padding: 5px 10px;
            border-radius: 15px;
            display: inline-block;
            font-weight: bold;
            margin-bottom: 10px;
        }}
        .meeting-detail {{
            margin: 8px 0;
        }}
        .online-badge {{
            background: #27ae60;
            color: white;
            padding: 3px 8px;
            border-radius: 10px;
            font-size: 0.8em;
        }}
        .importance-high {{
            border-left-color: #e74c3c;
        }}
        .summary {{
            background: #3498db;
            color: white;
            padding: 20px;
            border-radius: 10px;
            margin-top: 30px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📅 Daily Meeting Schedule - {date_str}</h1>
        <p><strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | <strong>Total meetings:</strong> {len(meetings)}</p>
"""
    
    if not meetings:
        html_content += """
        <div style="text-align: center; padding: 40px;">
            <h2>🎉 No meetings scheduled!</h2>
            <p>Perfect day for focus work!</p>
        </div>
"""
    else:
        for i, meeting in enumerate(meetings, 1):
            duration_hrs = meeting['duration_minutes'] // 60
            duration_mins = meeting['duration_minutes'] % 60
            duration_str = f"{duration_hrs}h {duration_mins}m" if duration_hrs > 0 else f"{duration_mins}m"
            
            importance_class = "importance-high" if meeting['importance'] == 'high' else ""
            
            html_content += f"""
        <div class="meeting {importance_class}">
            <h3 class="meeting-title">{i}. {meeting['subject']}</h3>
            <div class="meeting-time">{meeting['start_time']} - {meeting['end_time']} ({duration_str})</div>
"""
            
            if meeting['is_online_meeting']:
                html_content += f"""
            <div class="meeting-detail">
                📍 <span class="online-badge">Online Meeting</span>
"""
                if meeting['online_meeting_url']:
                    html_content += f"""
                <a href="{meeting['online_meeting_url']}" target="_blank">🔗 Join Meeting</a>
"""
                html_content += "</div>"
            elif meeting['location']:
                html_content += f"""
            <div class="meeting-detail">📍 {meeting['location']}</div>
"""
            
            if meeting['attendees']:
                html_content += f"""
            <div class="meeting-detail">👥 {meeting['attendee_count']} attendees</div>
"""
            
            if meeting['body_preview']:
                html_content += f"""
            <div class="meeting-detail">
                <strong>📝 Description:</strong><br>
                <em>{meeting['body_preview']}</em>
            </div>
"""
            
            html_content += "        </div>"
        
        # Summary
        total_duration = sum(m['duration_minutes'] for m in meetings)
        total_hrs = total_duration // 60
        total_mins = total_duration % 60
        
        html_content += f"""
        <div class="summary">
            <h3>📊 Daily Summary</h3>
            <ul>
                <li><strong>Total Meetings:</strong> {len(meetings)}</li>
                <li><strong>Total Meeting Time:</strong> {total_hrs}h {total_mins}m</li>
                <li><strong>Online Meetings:</strong> {sum(1 for m in meetings if m['is_online_meeting'])}</li>
                <li><strong>Meetings You're Organizing:</strong> {sum(1 for m in meetings if m['is_organizer'])}</li>
            </ul>
        </div>
"""
    
    html_content += """
    </div>
    <div style="text-align: center; margin-top: 20px; color: #7f8c8d;">
        <em>Generated by Scenara Meeting Intelligence 🚀</em>
    </div>
</body>
</html>"""
    
    return html_content


def save_output(content: str, format_type: str, date_str: str):
    """Save output to file"""
    output_dir = Path("meeting_outputs")
    output_dir.mkdir(exist_ok=True)
    
    filename = f"meetings_demo_{date_str}.{format_type}"
    filepath = output_dir / filename
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"💾 Saved {format_type.upper()} output to: {filepath}")
    
    # Show preview for HTML/MD
    if format_type in ['html', 'md']:
        print(f"🌐 Open in browser: file://{filepath.absolute()}")


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="Scenara Daily Meeting Viewer - Demo Version",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python demo_daily_meeting_viewer.py 20251020
  python demo_daily_meeting_viewer.py 20251020 --format html
  python demo_daily_meeting_viewer.py 20251020 --console-only
        """
    )
    
    parser.add_argument('date', help='Date in format YYYYMMDD (e.g., 20251020)')
    parser.add_argument('--format', choices=['md', 'html', 'json'], default='md',
                       help='Output format (default: md)')
    parser.add_argument('--console-only', action='store_true',
                       help='Only display in console, do not save file')
    
    args = parser.parse_args()
    
    demo_daily_meetings(args.date, args.format, args.console_only)


if __name__ == "__main__":
    main()