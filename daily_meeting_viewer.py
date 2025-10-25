#!/usr/bin/env python3
"""
Scenara Daily Meeting Viewer
Retrieves and displays meetings for a specific date in beautiful formatted output
"""

import argparse
import json
import os
import sys
import zoneinfo
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import List, Dict, Optional
import requests
import msal


class ScenaraDailyMeetingViewer:
    """
    Beautiful meeting viewer for specific dates
    Supports multiple output formats: markdown, html, json, console
    """
    
    def __init__(self):
        # Microsoft Graph configuration (same as MEvals)
        self.tenant_id = "72f988bf-86f1-41af-91ab-2d7cd011db47"
        self.client_id = "9ce97a32-d9ab-4ab2-aadc-f49b39b94e11"
        self.scopes = ["Calendars.Read"]
        
        # Set local timezone (Pacific Time)
        try:
            self.local_tz = zoneinfo.ZoneInfo("America/Los_Angeles")
        except:
            # Fallback for older Python versions
            from datetime import timezone, timedelta
            # PDT is UTC-7, PST is UTC-8
            self.local_tz = timezone(timedelta(hours=-7))  # PDT
        
        self.output_dir = Path("meeting_outputs")
        self.output_dir.mkdir(exist_ok=True)
    
    def parse_date(self, date_str: str) -> datetime:
        """
        Parse date string in format YYYYMMDD to datetime
        
        Args:
            date_str: Date in format "20251020"
            
        Returns:
            datetime object for the specified date
        """
        try:
            if len(date_str) != 8 or not date_str.isdigit():
                raise ValueError("Date must be in format YYYYMMDD (e.g., 20251020)")
            
            year = int(date_str[:4])
            month = int(date_str[4:6])
            day = int(date_str[6:8])
            
            # Create datetime for start of day in UTC
            target_date = datetime(year, month, day, 0, 0, 0, tzinfo=timezone.utc)
            return target_date
            
        except ValueError as e:
            raise ValueError(f"Invalid date format '{date_str}': {e}")
    
    def authenticate(self) -> str:
        """
        Authenticate with Microsoft Graph and return access token
        
        Returns:
            Access token string
        """
        print("🔐 Authenticating with Microsoft Graph...")
        
        authority = f"https://login.microsoftonline.com/{self.tenant_id}"
        app = msal.PublicClientApplication(self.client_id, authority=authority)
        
        # Try silent authentication first
        accounts = app.get_accounts()
        result = None
        
        if accounts:
            print("🔑 Attempting silent authentication...")
            result = app.acquire_token_silent(self.scopes, account=accounts[0])
        
        if not result or "access_token" not in result:
            print("🔐 Interactive authentication required...")
            print("   A browser window will open for Microsoft login")
            result = app.acquire_token_interactive(self.scopes)
        
        if "access_token" not in result:
            raise Exception(f"Authentication failed: {result.get('error_description', 'Unknown error')}")
        
        print("✅ Authentication successful!")
        return result["access_token"]
    
    def fetch_meetings_for_date(self, target_date: datetime) -> List[Dict]:
        """
        Fetch meetings for a specific date from Microsoft Graph
        
        Args:
            target_date: Date to fetch meetings for
            
        Returns:
            List of meeting objects
        """
        access_token = self.authenticate()
        
        # Calculate start and end of day
        start_time = target_date
        end_time = start_time + timedelta(days=1)
        
        # Build Graph API URL
        base_url = 'https://graph.microsoft.com/v1.0/me/calendarview'
        params = [
            f"startDateTime={start_time.isoformat()}",
            f"endDateTime={end_time.isoformat()}",
            "$top=100",
            "$orderby=start/dateTime"
        ]
        url = f"{base_url}?{'&'.join(params)}"
        
        # Make API request
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Accept': 'application/json'
        }
        
        print(f"📡 Fetching meetings for {target_date.strftime('%B %d, %Y')}...")
        
        response = requests.get(url, headers=headers)
        if not response.ok:
            raise Exception(f"Graph API error: {response.status_code} {response.text}")
        
        data = response.json()
        meetings = data.get('value', [])
        
        print(f"✅ Found {len(meetings)} meetings")
        return meetings
    
    def process_meeting(self, meeting: Dict) -> Dict:
        """
        Process raw meeting data into display format
        
        Args:
            meeting: Raw meeting object from Graph API
            
        Returns:
            Processed meeting object
        """
        # Extract times and convert to local timezone
        start_dt = datetime.fromisoformat(meeting['start']['dateTime'].replace('Z', '+00:00'))
        end_dt = datetime.fromisoformat(meeting['end']['dateTime'].replace('Z', '+00:00'))
        
        # Convert to local timezone
        start_local = start_dt.astimezone(self.local_tz)
        end_local = end_dt.astimezone(self.local_tz)
        
        duration_minutes = int((end_dt - start_dt).total_seconds() / 60)
        
        # Extract attendees
        attendees = []
        if meeting.get('attendees'):
            for attendee in meeting['attendees']:
                if attendee.get('emailAddress'):
                    name = attendee['emailAddress'].get('name', 'Unknown')
                    email = attendee['emailAddress'].get('address', '')
                    response_status = attendee.get('status', {}).get('response', 'none')
                    attendees.append({
                        'name': name,
                        'email': email,
                        'response': response_status
                    })
        
        # Format body preview
        body_preview = meeting.get('bodyPreview', '').strip()
        if len(body_preview) > 200:
            body_preview = body_preview[:200] + "..."
        
        return {
            'id': meeting.get('id', ''),
            'subject': meeting.get('subject', 'Untitled Meeting'),
            'start_time': start_local.strftime('%H:%M'),
            'end_time': end_local.strftime('%H:%M'),
            'timezone': start_local.strftime('%Z'),  # Add timezone info
            'duration_minutes': duration_minutes,
            'location': meeting.get('location', {}).get('displayName', ''),
            'is_online_meeting': meeting.get('isOnlineMeeting', False),
            'online_meeting_url': meeting.get('onlineMeetingUrl', ''),
            'attendees': attendees,
            'attendee_count': len(attendees),
            'body_preview': body_preview,
            'importance': meeting.get('importance', 'normal'),
            'is_organizer': meeting.get('isOrganizer', False),
            'response_status': meeting.get('responseStatus', {}).get('response', 'none'),
            'web_link': meeting.get('webLink', '')
        }
    
    def generate_markdown(self, meetings: List[Dict], target_date: datetime) -> str:
        """
        Generate markdown format output
        
        Args:
            meetings: List of processed meetings
            target_date: Target date
            
        Returns:
            Markdown formatted string
        """
        date_str = target_date.strftime('%B %d, %Y')
        date_iso = target_date.strftime('%Y-%m-%d')
        
        md_content = f"""# 📅 Daily Meeting Schedule - {date_str}

Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
Total meetings: **{len(meetings)}**

---

"""
        
        if not meetings:
            md_content += """## 🎉 No meetings scheduled!

Looks like you have a free day! Perfect time for:
- 🎯 Focus work and deep thinking
- 📚 Learning and skill development  
- 🔄 Catching up on tasks
- ☕ Taking well-deserved breaks

"""
            return md_content
        
        # Group meetings by time
        for i, meeting in enumerate(meetings, 1):
            duration_hrs = meeting['duration_minutes'] // 60
            duration_mins = meeting['duration_minutes'] % 60
            duration_str = f"{duration_hrs}h {duration_mins}m" if duration_hrs > 0 else f"{duration_mins}m"
            
            # Meeting header
            md_content += f"""## {i}. {meeting['subject']}

**⏰ Time:** {meeting['start_time']} - {meeting['end_time']} {meeting.get('timezone', 'PDT')} ({duration_str})  
"""
            
            # Location/Online meeting
            if meeting['is_online_meeting']:
                md_content += f"**📍 Location:** 🌐 Online Meeting  \n"
                if meeting['online_meeting_url']:
                    md_content += f"**🔗 Join Link:** [Join Meeting]({meeting['online_meeting_url']})  \n"
            elif meeting['location']:
                md_content += f"**📍 Location:** {meeting['location']}  \n"
            
            # Attendees
            if meeting['attendees']:
                md_content += f"**👥 Attendees:** {meeting['attendee_count']} people  \n"
                if len(meeting['attendees']) <= 5:  # Show individual attendees for small meetings
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
            
            # Importance
            if meeting['importance'] != 'normal':
                importance_emoji = {'high': '🔴', 'low': '🔵'}.get(meeting['importance'], '⚪')
                md_content += f"**Priority:** {importance_emoji} {meeting['importance'].title()}  \n"
            
            # Your response
            if meeting['response_status'] != 'none':
                response_emoji = {
                    'accepted': '✅ Accepted',
                    'declined': '❌ Declined',
                    'tentative': '❓ Tentative',
                    'organizer': '👑 Organizer'
                }.get(meeting['response_status'], meeting['response_status'])
                md_content += f"**Your Status:** {response_emoji}  \n"
            
            # Description preview
            if meeting['body_preview']:
                md_content += f"""
**📝 Description:**
> {meeting['body_preview']}

"""
            
            # Outlook link
            if meeting['web_link']:
                md_content += f"**🔗 Open in Outlook:** [View Meeting]({meeting['web_link']})  \n"
            
            md_content += "\n---\n\n"
        
        # Footer with summary
        total_duration = sum(m['duration_minutes'] for m in meetings)
        total_hrs = total_duration // 60
        total_mins = total_duration % 60
        
        md_content += f"""## 📊 Daily Summary

- **Total Meetings:** {len(meetings)}
- **Total Meeting Time:** {total_hrs}h {total_mins}m
- **Online Meetings:** {sum(1 for m in meetings if m['is_online_meeting'])}
- **In-Person Meetings:** {sum(1 for m in meetings if not m['is_online_meeting'] and m['location'])}
- **Meetings You're Organizing:** {sum(1 for m in meetings if m['is_organizer'])}

---

*Generated by Scenara Meeting Intelligence* 🚀
"""
        
        return md_content
    
    def generate_html(self, meetings: List[Dict], target_date: datetime) -> str:
        """
        Generate HTML format output
        
        Args:
            meetings: List of processed meetings
            target_date: Target date
            
        Returns:
            HTML formatted string
        """
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
        .attendees {{
            background: #ecf0f1;
            padding: 10px;
            border-radius: 5px;
            margin: 10px 0;
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
        .no-meetings {{
            text-align: center;
            padding: 40px;
            color: #7f8c8d;
        }}
        .emoji {{
            font-size: 1.2em;
        }}
        a {{
            color: #3498db;
            text-decoration: none;
        }}
        a:hover {{
            text-decoration: underline;
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
        <div class="no-meetings">
            <h2>🎉 No meetings scheduled!</h2>
            <p>Looks like you have a free day! Perfect time for:</p>
            <ul style="text-align: left; display: inline-block;">
                <li>🎯 Focus work and deep thinking</li>
                <li>📚 Learning and skill development</li>
                <li>🔄 Catching up on tasks</li>
                <li>☕ Taking well-deserved breaks</li>
            </ul>
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
            <div class="meeting-time">{meeting['start_time']} - {meeting['end_time']} {meeting.get('timezone', 'PDT')} ({duration_str})</div>
"""
                
                # Location
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
                
                # Attendees
                if meeting['attendees']:
                    html_content += f"""
            <div class="meeting-detail">👥 {meeting['attendee_count']} attendees</div>
"""
                    if len(meeting['attendees']) <= 5:
                        html_content += '<div class="attendees">'
                        for attendee in meeting['attendees']:
                            status_emoji = {
                                'accepted': '✅',
                                'declined': '❌',
                                'tentative': '❓',
                                'none': '⏳'
                            }.get(attendee['response'], '⏳')
                            html_content += f'<span style="margin-right: 15px;">{status_emoji} {attendee["name"]}</span>'
                        html_content += '</div>'
                
                # Description
                if meeting['body_preview']:
                    html_content += f"""
            <div class="meeting-detail">
                <strong>📝 Description:</strong><br>
                <em>{meeting['body_preview']}</em>
            </div>
"""
                
                # Links
                if meeting['web_link']:
                    html_content += f"""
            <div class="meeting-detail">
                <a href="{meeting['web_link']}" target="_blank">🔗 Open in Outlook</a>
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
                <li><strong>In-Person Meetings:</strong> {sum(1 for m in meetings if not m['is_online_meeting'] and m['location'])}</li>
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
    
    def save_output(self, content: str, format_type: str, target_date: datetime) -> str:
        """
        Save formatted content to file
        
        Args:
            content: Formatted content string
            format_type: Output format (md, html, json)
            target_date: Target date
            
        Returns:
            Path to saved file
        """
        date_str = target_date.strftime('%Y%m%d')
        extension = format_type
        filename = f"meetings_{date_str}.{extension}"
        filepath = self.output_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"💾 Saved {format_type.upper()} output to: {filepath}")
        return str(filepath)
    
    def display_console_summary(self, meetings: List[Dict], target_date: datetime):
        """
        Display a beautiful console summary
        
        Args:
            meetings: List of processed meetings
            target_date: Target date
        """
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


def main():
    """Command line interface"""
    parser = argparse.ArgumentParser(
        description="Scenara Daily Meeting Viewer - Beautiful meeting schedules for any date",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python daily_meeting_viewer.py 20251020
  python daily_meeting_viewer.py 20251020 --format html
  python daily_meeting_viewer.py 20251020 --format md --output my_meetings.md
  python daily_meeting_viewer.py 20251020 --console-only
  
Date format: YYYYMMDD (e.g., 20251020 for October 20, 2025)
        """
    )
    
    parser.add_argument('date', help='Date in format YYYYMMDD (e.g., 20251020)')
    parser.add_argument('--format', choices=['md', 'html', 'json'], default='md',
                       help='Output format (default: md)')
    parser.add_argument('--output', help='Custom output filename')
    parser.add_argument('--console-only', action='store_true',
                       help='Only display in console, do not save file')
    parser.add_argument('--open', action='store_true',
                       help='Open the generated file after creation (HTML/MD)')
    
    args = parser.parse_args()
    
    try:
        # Initialize viewer
        viewer = ScenaraDailyMeetingViewer()
        
        # Parse date
        target_date = viewer.parse_date(args.date)
        print(f"🎯 Retrieving meetings for {target_date.strftime('%B %d, %Y')}")
        
        # Fetch meetings
        raw_meetings = viewer.fetch_meetings_for_date(target_date)
        
        # Process meetings
        processed_meetings = []
        for meeting in raw_meetings:
            processed = viewer.process_meeting(meeting)
            processed_meetings.append(processed)
        
        # Always show console summary
        viewer.display_console_summary(processed_meetings, target_date)
        
        # Generate and save formatted output (unless console-only)
        if not args.console_only:
            if args.format == 'md':
                content = viewer.generate_markdown(processed_meetings, target_date)
            elif args.format == 'html':
                content = viewer.generate_html(processed_meetings, target_date)
            elif args.format == 'json':
                content = json.dumps({
                    'date': target_date.isoformat(),
                    'meetings': processed_meetings,
                    'summary': {
                        'total_meetings': len(processed_meetings),
                        'total_duration_minutes': sum(m['duration_minutes'] for m in processed_meetings),
                        'online_meetings': sum(1 for m in processed_meetings if m['is_online_meeting']),
                        'organizer_meetings': sum(1 for m in processed_meetings if m['is_organizer'])
                    }
                }, indent=2, ensure_ascii=False)
            
            # Save file
            if args.output:
                filepath = args.output
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"💾 Saved to custom file: {filepath}")
            else:
                filepath = viewer.save_output(content, args.format, target_date)
            
            # Open file if requested
            if args.open and not args.output:
                import webbrowser
                import os
                full_path = os.path.abspath(filepath)
                webbrowser.open(f'file://{full_path}')
                print(f"🌐 Opened in default application")
        
        print(f"\n✅ Meeting retrieval complete!")
        
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()