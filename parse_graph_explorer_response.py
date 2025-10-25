#!/usr/bin/env python3
"""
Parse Microsoft Graph Explorer JSON Response for Today's Meetings
Designed to work with Graph Explorer output for macOS users
"""

import json
import sys
import zoneinfo
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List


def parse_iso_datetime(iso_string: str) -> datetime:
    """Parse ISO datetime string and convert to local timezone."""
    try:
        # Parse the ISO string
        dt = datetime.fromisoformat(iso_string.replace('Z', '+00:00'))
        
        # Convert to local timezone (PDT)
        try:
            local_tz = zoneinfo.ZoneInfo("America/Los_Angeles")
        except:
            # Fallback for PDT (UTC-7)
            local_tz = timezone(timedelta(hours=-7))
        
        return dt.astimezone(local_tz)
    except Exception as e:
        print(f"❌ Error parsing datetime '{iso_string}': {e}")
        return None


def format_meeting_time(start_dt: datetime, end_dt: datetime) -> str:
    """Format meeting time range in local timezone."""
    if not start_dt or not end_dt:
        return "❓ Time unavailable"
    
    # Check if same day
    if start_dt.date() == end_dt.date():
        return f"{start_dt.strftime('%I:%M %p')} - {end_dt.strftime('%I:%M %p PDT')}"
    else:
        return f"{start_dt.strftime('%m/%d %I:%M %p')} - {end_dt.strftime('%m/%d %I:%M %p PDT')}"


def extract_location(meeting: Dict[str, Any]) -> str:
    """Extract location information from meeting."""
    location = meeting.get('location', {})
    
    if isinstance(location, dict):
        display_name = location.get('displayName', '')
        if display_name:
            return f"📍 {display_name}"
    
    return ""


def analyze_meeting_conflicts(meetings: List[Dict[str, Any]]) -> None:
    """Analyze meetings for potential conflicts with Flight CI005 at 4:25 PM PDT."""
    flight_time = "4:25 PM PDT"
    print(f"\n✈️ Flight CI005 Conflict Analysis (Departure: {flight_time}):")
    print("=" * 50)
    
    conflicts_found = False
    
    for meeting in meetings:
        start_dt = parse_iso_datetime(meeting['start']['dateTime'])
        end_dt = parse_iso_datetime(meeting['end']['dateTime'])
        
        if not start_dt or not end_dt:
            continue
        
        # Flight departure time (4:25 PM PDT)
        flight_dt = start_dt.replace(hour=16, minute=25, second=0, microsecond=0)
        
        # Check for conflicts (meeting overlaps with 3:00-5:00 PM window)
        conflict_start = flight_dt - timedelta(hours=1, minutes=25)  # 3:00 PM
        conflict_end = flight_dt + timedelta(minutes=35)  # 5:00 PM
        
        if (start_dt <= conflict_end and end_dt >= conflict_start):
            conflicts_found = True
            time_range = format_meeting_time(start_dt, end_dt)
            print(f"⚠️  CONFLICT: {meeting.get('subject', 'No subject')} ({time_range})")
    
    if not conflicts_found:
        print("✅ No meeting conflicts with flight departure!")


def parse_graph_response(json_text: str) -> None:
    """Parse and display Graph Explorer calendar response."""
    try:
        data = json.loads(json_text)
        meetings = data.get('value', [])
        
        print("📅 Today's Meetings from Microsoft Graph Explorer")
        print("=" * 55)
        print(f"Found {len(meetings)} meeting(s) for today\n")
        
        if not meetings:
            print("🎉 No meetings scheduled for today!")
            return
        
        # Display meetings
        for i, meeting in enumerate(meetings, 1):
            subject = meeting.get('subject', 'No Subject')
            
            # Parse times
            start_dt = parse_iso_datetime(meeting['start']['dateTime'])
            end_dt = parse_iso_datetime(meeting['end']['dateTime'])
            time_range = format_meeting_time(start_dt, end_dt)
            
            # Get organizer
            organizer = meeting.get('organizer', {}).get('emailAddress', {})
            organizer_name = organizer.get('name', 'Unknown')
            
            # Get location
            location = extract_location(meeting)
            
            # Response status
            response = meeting.get('responseStatus', {}).get('response', 'none')
            status_emoji = {
                'accepted': '✅',
                'tentative': '❓',
                'declined': '❌',
                'none': '⏳'
            }.get(response, '⏳')
            
            print(f"{i}. {subject}")
            print(f"   ⏰ {time_range}")
            print(f"   👤 Organizer: {organizer_name}")
            if location:
                print(f"   {location}")
            print(f"   {status_emoji} Status: {response.title()}")
            print()
        
        # Analyze flight conflicts
        analyze_meeting_conflicts(meetings)
        
    except json.JSONDecodeError as e:
        print(f"❌ Error parsing JSON: {e}")
        print("Please ensure you copied the complete JSON response from Graph Explorer.")
    except Exception as e:
        print(f"❌ Error processing data: {e}")


def main():
    """Main function to handle command line input or file input."""
    print("📋 Microsoft Graph Explorer Response Parser")
    print("=" * 45)
    
    if len(sys.argv) > 1:
        # Read from file
        try:
            with open(sys.argv[1], 'r') as f:
                json_text = f.read()
            parse_graph_response(json_text)
        except FileNotFoundError:
            print(f"❌ File not found: {sys.argv[1]}")
        except Exception as e:
            print(f"❌ Error reading file: {e}")
    else:
        # Interactive input
        print("\nPaste the JSON response from Graph Explorer below.")
        print("Query: GET /me/calendarView?startDateTime=2025-10-22T00:00:00.000Z&endDateTime=2025-10-22T23:59:59.999Z&$orderby=start/dateTime")
        print("(Press Ctrl+D when finished, or Ctrl+C to cancel)\n")
        
        try:
            json_text = sys.stdin.read()
            if json_text.strip():
                parse_graph_response(json_text)
            else:
                print("No input provided.")
        except KeyboardInterrupt:
            print("\n\nOperation cancelled.")
        except Exception as e:
            print(f"❌ Error reading input: {e}")


if __name__ == "__main__":
    main()