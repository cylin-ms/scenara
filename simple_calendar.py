#!/usr/bin/env python3
"""
Dead Simple Calendar Check
Just opens Graph Explorer with instructions - no complexity
"""

import webbrowser
import sys
import json
import zoneinfo
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List


def parse_iso_datetime(iso_string: str) -> datetime:
    """Parse ISO datetime string and convert to local timezone."""
    try:
        dt = datetime.fromisoformat(iso_string.replace('Z', '+00:00'))
        try:
            local_tz = zoneinfo.ZoneInfo("America/Los_Angeles")
        except:
            local_tz = timezone(timedelta(hours=-7))
        return dt.astimezone(local_tz)
    except Exception:
        return None


def format_meeting_time(start_dt: datetime, end_dt: datetime) -> str:
    """Format meeting time range in local timezone."""
    if not start_dt or not end_dt:
        return "❓ Time unavailable"
    
    if start_dt.date() == end_dt.date():
        return f"{start_dt.strftime('%I:%M %p')} - {end_dt.strftime('%I:%M %p PDT')}"
    else:
        return f"{start_dt.strftime('%m/%d %I:%M %p')} - {end_dt.strftime('%m/%d %I:%M %p PDT')}"


def analyze_flight_conflicts(meetings: List[Dict[str, Any]]) -> None:
    """Check for conflicts with 4:25 PM flight departure."""
    print(f"\n✈️ Flight CI005 Conflict Analysis (Departure: 4:25 PM PDT):")
    print("=" * 50)
    
    conflicts = []
    for meeting in meetings:
        start_dt = parse_iso_datetime(meeting['start']['dateTime'])
        end_dt = parse_iso_datetime(meeting['end']['dateTime'])
        
        if not start_dt or not end_dt:
            continue
        
        # Check 3:00-5:00 PM window for flight conflicts
        flight_dt = start_dt.replace(hour=16, minute=25, second=0, microsecond=0)
        conflict_start = flight_dt - timedelta(hours=1, minutes=25)
        conflict_end = flight_dt + timedelta(minutes=35)
        
        if start_dt <= conflict_end and end_dt >= conflict_start:
            conflicts.append((meeting, start_dt, end_dt))
    
    if conflicts:
        for meeting, start_dt, end_dt in conflicts:
            time_range = format_meeting_time(start_dt, end_dt)
            print(f"⚠️  CONFLICT: {meeting.get('subject', 'No subject')} ({time_range})")
    else:
        print("✅ No meeting conflicts with flight departure!")


def parse_and_display_calendar(json_text: str) -> None:
    """Parse and display calendar JSON response."""
    try:
        response_json = json.loads(json_text)
        
        if 'error' in response_json:
            print(f"❌ Graph API Error: {response_json['error'].get('message', 'Unknown error')}")
            return
        
        meetings = response_json.get('value', [])
        
        print(f"\n📅 Today's Calendar ({len(meetings)} meeting{'s' if len(meetings) != 1 else ''})")
        print("=" * 40)
        
        if not meetings:
            print("🎉 No meetings scheduled for today!")
            return
        
        for i, meeting in enumerate(meetings, 1):
            subject = meeting.get('subject', 'No Subject')
            start_dt = parse_iso_datetime(meeting['start']['dateTime'])
            end_dt = parse_iso_datetime(meeting['end']['dateTime'])
            time_range = format_meeting_time(start_dt, end_dt)
            
            organizer = meeting.get('organizer', {}).get('emailAddress', {}).get('name', 'Unknown')
            
            location = meeting.get('location', {})
            location_str = f" 📍 {location.get('displayName', '')}" if location.get('displayName') else ""
            
            response = meeting.get('responseStatus', {}).get('response', 'none')
            status = {'accepted': '✅', 'tentative': '❓', 'declined': '❌', 'none': '⏳'}.get(response, '⏳')
            
            print(f"{i}. {subject}")
            print(f"   ⏰ {time_range}")
            print(f"   👤 {organizer}{location_str} {status}")
            print()
        
        analyze_flight_conflicts(meetings)
        
        # Save to file
        output_file = f"calendar_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_file, 'w') as f:
            json.dump(response_json, f, indent=2)
        print(f"\n💾 Calendar data saved to: {output_file}")
        
    except json.JSONDecodeError as e:
        print(f"❌ Failed to parse JSON: {e}")
        print("💡 Please ensure you copied the complete JSON response from Graph Explorer")
    except Exception as e:
        print(f"❌ Error processing calendar data: {e}")


def main():
    """Ultra-simple calendar access."""
    print("📅 Today's Calendar Check")
    print("=" * 25)
    
    # Today's dates for the query
    today = datetime.now(timezone.utc).date()
    start_iso = f"{today}T00:00:00.000Z"
    end_iso = f"{today}T23:59:59.999Z"
    
    # Graph API query path (without the base URL for Graph Explorer)
    query_path = f"/me/calendarView?startDateTime={start_iso}&endDateTime={end_iso}&$orderby=start/dateTime"
    
    # Pre-fill Graph Explorer with the query
    from urllib.parse import quote
    graph_explorer_url = f"https://developer.microsoft.com/en-us/graph/graph-explorer?request={quote(query_path)}&method=GET&version=v1.0"
    
    print("🌐 Opening Microsoft Graph Explorer with pre-filled query...")
    webbrowser.open(graph_explorer_url)
    
    print("\n✅ The query should be pre-filled:")
    print("=" * 50)
    print(f"GET {query_path}")
    print("=" * 50)
    
    print("\n📝 Steps:")
    print("1. Sign in when prompted")
    print("2. The query should already be filled in")
    print("3. Click 'Run query'")
    print("4. Copy the JSON response and paste it back here!")
    
    # Save query to clipboard as backup
    try:
        import subprocess
        subprocess.run(['pbcopy'], input=query_path.encode(), timeout=1)
        print("\n📋 Query also copied to clipboard as backup!")
    except:
        pass
    
    # Wait for user to paste JSON response
    print("\n⏳ After running the query, paste the JSON response here:")
    print("(Press Enter twice when done, or Ctrl+C to cancel)")
    
    try:
        # Collect JSON response
        json_lines = []
        while True:
            try:
                line = input()
                if line.strip() == "" and json_lines:
                    break
                json_lines.append(line)
            except EOFError:
                break
        
        if json_lines:
            json_text = '\n'.join(json_lines)
            parse_and_display_calendar(json_text)
        else:
            print("❌ No JSON response received")
            
    except KeyboardInterrupt:
        print("\n👋 Cancelled")


if __name__ == "__main__":
    main()