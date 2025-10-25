#!/usr/bin/env python3
"""
Direct Microsoft Graph Calendar Access
Clean, simple solution using Microsoft Graph REST API
"""

import os
import sys
import json
import subprocess
import zoneinfo
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Optional


def get_calendar_data_direct() -> Optional[Dict[str, Any]]:
    """Get calendar data directly using Microsoft Graph CLI."""
    # Build today's query
    today = datetime.now(timezone.utc).date()
    start_datetime = datetime.combine(today, datetime.min.time()).replace(tzinfo=timezone.utc)
    end_datetime = datetime.combine(today, datetime.max.time()).replace(tzinfo=timezone.utc)
    
    start_iso = start_datetime.isoformat().replace('+00:00', 'Z')
    end_iso = end_datetime.isoformat().replace('+00:00', 'Z')
    
    # Try Microsoft Graph CLI first
    try:
        print("🔍 Checking for Microsoft Graph CLI...")
        result = subprocess.run(['az', '--version'], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print("✅ Azure CLI found, attempting direct Graph API call...")
            
            graph_cmd = [
                'az', 'rest',
                '--method', 'GET',
                '--url', f"https://graph.microsoft.com/v1.0/me/calendarView?startDateTime={start_iso}&endDateTime={end_iso}&$orderby=start/dateTime"
            ]
            
            result = subprocess.run(graph_cmd, capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                return json.loads(result.stdout)
            else:
                print(f"❌ Graph API call failed: {result.stderr}")
                
    except (subprocess.TimeoutExpired, FileNotFoundError, json.JSONDecodeError):
        pass
    
    # Try Microsoft Graph PowerShell if available
    try:
        print("🔍 Checking for Microsoft Graph PowerShell...")
        pwsh_cmd = [
            'pwsh', '-Command',
            f'Get-MgUserCalendarView -UserId "me" -StartDateTime "{start_iso}" -EndDateTime "{end_iso}" | ConvertTo-Json -Depth 10'
        ]
        
        result = subprocess.run(pwsh_cmd, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            return json.loads(result.stdout)
            
    except (subprocess.TimeoutExpired, FileNotFoundError, json.JSONDecodeError):
        pass
    
    return None


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
        
        # Check 3:00-5:00 PM window
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


def display_meetings(response_json: Dict[str, Any]) -> None:
    """Display meetings in a clean format."""
    meetings = response_json.get('value', [])
    
    print(f"\n📅 Today's Calendar ({len(meetings)} meeting{'s' if len(meetings) != 1 else ''})")
    print("=" * 40)
    
    if not meetings:
        print("🎉 No meetings scheduled!")
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


def install_graph_cli():
    """Provide instructions for installing Graph CLI tools."""
    print("\n💡 To enable direct calendar access, install one of these:")
    print("   Option 1 - Azure CLI:")
    print("     brew install azure-cli")
    print("     az login")
    print()
    print("   Option 2 - Microsoft Graph PowerShell:")
    print("     brew install powershell")
    print("     pwsh -Command 'Install-Module Microsoft.Graph -Scope CurrentUser'")
    print("     pwsh -Command 'Connect-MgGraph -Scopes \"Calendars.Read\"'")


def quick_browser_method():
    """Fallback to quick browser method."""
    import webbrowser
    
    today = datetime.now(timezone.utc).date()
    start_datetime = datetime.combine(today, datetime.min.time()).replace(tzinfo=timezone.utc)
    end_datetime = datetime.combine(today, datetime.max.time()).replace(tzinfo=timezone.utc)
    
    start_iso = start_datetime.isoformat().replace('+00:00', 'Z')
    end_iso = end_datetime.isoformat().replace('+00:00', 'Z')
    
    query = f"/me/calendarView?startDateTime={start_iso}&endDateTime={end_iso}&$orderby=start/dateTime"
    url = f"https://developer.microsoft.com/en-us/graph/graph-explorer?request={query}&method=GET&version=v1.0"
    
    print(f"\n🌐 Opening Graph Explorer with pre-filled query...")
    webbrowser.open(url)
    
    print("📋 Copy the JSON result and paste it here:")
    try:
        json_input = []
        while True:
            line = input()
            if not line.strip() and json_input:
                break
            json_input.append(line)
        
        if json_input:
            json_text = '\n'.join(json_input)
            response_json = json.loads(json_text)
            display_meetings(response_json)
        
    except (KeyboardInterrupt, EOFError):
        print("\n👋 Cancelled")
    except json.JSONDecodeError:
        print("❌ Invalid JSON")


def main():
    """Main function."""
    print("📅 Quick Calendar Check")
    print("=" * 25)
    
    # Try direct methods first
    response_json = get_calendar_data_direct()
    
    if response_json:
        display_meetings(response_json)
        
        # Save to file
        output_file = f"calendar_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_file, 'w') as f:
            json.dump(response_json, f, indent=2)
        print(f"💾 Saved to {output_file}")
        
    else:
        print("❌ Direct access failed")
        install_graph_cli()
        
        # Quick browser fallback
        try:
            choice = input("\n🌐 Open Graph Explorer? (y/n): ").lower()
            if choice.startswith('y'):
                quick_browser_method()
        except (KeyboardInterrupt, EOFError):
            print("\n👋 Goodbye!")


if __name__ == "__main__":
    main()