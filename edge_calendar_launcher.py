#!/usr/bin/env python3
"""
Simple Edge Launcher for Microsoft Graph Calendar Access
Opens Microsoft Edge and provides step-by-step instructions
"""

import os
import sys
import json
import subprocess
import webbrowser
import time
import zoneinfo
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List


def build_calendar_query() -> str:
    """Build the Graph API calendar query for today."""
    # Today's date range in UTC
    today = datetime.now(timezone.utc).date()
    start_datetime = datetime.combine(today, datetime.min.time()).replace(tzinfo=timezone.utc)
    end_datetime = datetime.combine(today, datetime.max.time()).replace(tzinfo=timezone.utc)
    
    start_iso = start_datetime.isoformat().replace('+00:00', 'Z')
    end_iso = end_datetime.isoformat().replace('+00:00', 'Z')
    
    query = f"/me/calendarView?startDateTime={start_iso}&endDateTime={end_iso}&$orderby=start/dateTime"
    return query


def open_edge_to_graph_explorer():
    """Open Microsoft Edge to Graph Explorer."""
    graph_explorer_url = "https://developer.microsoft.com/en-us/graph/graph-explorer"
    
    try:
        # Try to open specifically in Edge on macOS
        subprocess.run([
            'open', '-a', 'Microsoft Edge', graph_explorer_url
        ], check=True)
        print("✅ Opened Microsoft Edge")
        return True
    except subprocess.CalledProcessError:
        try:
            # Fallback to default browser
            webbrowser.open(graph_explorer_url)
            print("✅ Opened in default browser")
            return True
        except Exception as e:
            print(f"❌ Failed to open browser: {e}")
            return False


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


def display_calendar_results(response_json: Dict[str, Any]) -> None:
    """Display the calendar results in a formatted way."""
    try:
        meetings = response_json.get('value', [])
        
        print("\n📅 Today's Meetings from Microsoft Graph Explorer")
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
        
    except Exception as e:
        print(f"❌ Error displaying results: {e}")


def main():
    """Main function for Edge-based automation."""
    print("🌐 Microsoft Edge Graph Explorer Calendar Access")
    print("=" * 50)
    
    # Build the query
    query = build_calendar_query()
    
    # Open Edge to Graph Explorer
    print("📱 Opening Microsoft Edge to Graph Explorer...")
    if not open_edge_to_graph_explorer():
        print("❌ Failed to open browser. Please manually go to:")
        print("   https://developer.microsoft.com/en-us/graph/graph-explorer")
        return
    
    print("\n🔐 Step-by-step instructions:")
    print("=" * 30)
    print("1. ✅ Microsoft Edge is now opening Graph Explorer")
    print("2. 🔑 Sign in with your Microsoft account when prompted")
    print("3. 📝 In the query box, paste this query:")
    print(f"   GET {query}")
    print("4. ▶️  Click the 'Run query' button")
    print("5. 📋 When you see the JSON response, copy ALL of it")
    print("6. ⬇️  Come back here and paste it")
    
    # Wait for user to complete the process
    print("\n⏳ Waiting for you to complete the steps above...")
    print("   Once you have the JSON response, paste it below and press Enter twice:")
    print("   (Or press Ctrl+C to cancel)")
    
    try:
        # Collect multiline input
        json_lines = []
        print("\n📥 Paste the JSON response here:")
        while True:
            try:
                line = input()
                if line.strip() == "" and json_lines:
                    # Empty line after some content - user is done
                    break
                json_lines.append(line)
            except EOFError:
                # Ctrl+D pressed
                break
        
        if not json_lines:
            print("❌ No input received")
            return
        
        json_text = '\n'.join(json_lines)
        
        # Parse and display results
        try:
            response_json = json.loads(json_text)
            
            # Display results
            display_calendar_results(response_json)
            
            # Save results to file
            output_file = f"calendar_today_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(output_file, 'w') as f:
                json.dump(response_json, f, indent=2)
            print(f"\n💾 Results saved to: {output_file}")
            
        except json.JSONDecodeError as e:
            print(f"❌ Failed to parse JSON: {e}")
            print("💡 Please ensure you copied the complete JSON response")
            
    except KeyboardInterrupt:
        print("\n⚠️ Operation cancelled")
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()