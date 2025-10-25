#!/usr/bin/env python3
"""
Find Today's Meetings Tool
Extract and display today's meetings from existing calendar data
"""

import json
import os
from datetime import datetime, timezone, timedelta
from typing import List, Dict, Any
from pathlib import Path

def parse_datetime(date_str: str) -> datetime:
    """Parse Microsoft Graph datetime format"""
    if date_str.endswith('Z'):
        return datetime.fromisoformat(date_str[:-1]).replace(tzinfo=timezone.utc)
    return datetime.fromisoformat(date_str)

def is_today(event_datetime: str, target_date: datetime) -> bool:
    """Check if event is on target date"""
    try:
        event_dt = parse_datetime(event_datetime)
        # Convert to local time for comparison
        local_event = event_dt.astimezone()
        local_target = target_date.astimezone()
        
        return (local_event.year == local_target.year and 
                local_event.month == local_target.month and 
                local_event.day == local_target.day)
    except Exception:
        return False

def format_meeting_time(start_str: str, end_str: str) -> str:
    """Format meeting time for display"""
    try:
        start_dt = parse_datetime(start_str).astimezone()
        end_dt = parse_datetime(end_str).astimezone()
        
        start_time = start_dt.strftime("%H:%M")
        end_time = end_dt.strftime("%H:%M")
        return f"{start_time}-{end_time}"
    except Exception:
        return "Time TBD"

def extract_attendees(attendees: List[Dict]) -> str:
    """Extract attendee names"""
    if not attendees:
        return "No attendees"
    
    names = []
    for attendee in attendees[:3]:  # Show first 3
        if attendee.get('emailAddress', {}).get('name'):
            names.append(attendee['emailAddress']['name'])
    
    if len(attendees) > 3:
        names.append(f"+ {len(attendees) - 3} more")
    
    return ", ".join(names) if names else "No attendees"

def find_todays_meetings():
    """Find and display today's meetings"""
    print("📅 Finding Today's Meetings")
    print("=" * 40)
    
    # Get today's date
    today = datetime.now()
    print(f"🗓️  Target Date: {today.strftime('%A, %B %d, %Y')}")
    
    # Find calendar data file
    calendar_files = [
        "my_calendar_events_50.json",
        "my_calendar_events.json"
    ]
    
    calendar_data = None
    used_file = None
    
    for file_name in calendar_files:
        if Path(file_name).exists():
            with open(file_name, 'r') as f:
                calendar_data = json.load(f)
            used_file = file_name
            break
    
    if not calendar_data:
        print("❌ No calendar data found!")
        print("💡 Run one of these to fetch calendar data:")
        print("   - python automated_calendar_today.py")
        print("   - python cyl_silverflow_calendar_today.py")
        return
    
    print(f"📂 Using calendar data from: {used_file}")
    
    # Extract events
    events = calendar_data.get('value', [])
    print(f"🔍 Scanning {len(events)} total calendar events...")
    
    # Filter today's meetings
    todays_meetings = []
    
    for event in events:
        # Check if event has start time
        start_info = event.get('start')
        if not start_info:
            continue
            
        start_datetime = start_info.get('dateTime')
        if not start_datetime:
            continue
        
        # Check if it's today
        if is_today(start_datetime, today):
            # Skip cancelled meetings
            if event.get('isCancelled', False):
                continue
                
            todays_meetings.append(event)
    
    # Sort by start time
    todays_meetings.sort(key=lambda x: x.get('start', {}).get('dateTime', ''))
    
    print(f"\n🎯 Found {len(todays_meetings)} meetings for today:")
    print("-" * 50)
    
    if not todays_meetings:
        print("✨ No meetings scheduled for today! Enjoy your free time.")
        return
    
    # Display meetings
    for i, meeting in enumerate(todays_meetings, 1):
        start_info = meeting.get('start', {})
        end_info = meeting.get('end', {})
        
        # Basic info
        subject = meeting.get('subject') or "Untitled Meeting"
        time_range = format_meeting_time(
            start_info.get('dateTime', ''),
            end_info.get('dateTime', '')
        )
        
        # Meeting type indicators
        indicators = []
        if meeting.get('isOrganizer', False):
            indicators.append("👤 Organizer")
        if meeting.get('responseStatus', {}).get('response') == 'accepted':
            indicators.append("✅ Accepted")
        elif meeting.get('responseStatus', {}).get('response') == 'tentative':
            indicators.append("❓ Tentative")
        
        # Location
        location = meeting.get('location', {})
        location_str = ""
        if location.get('displayName'):
            location_str = f" 📍 {location['displayName']}"
        
        print(f"\n{i}. ⏰ {time_range} - {subject}")
        
        if indicators:
            print(f"   {' | '.join(indicators)}")
        
        if location_str:
            print(f"   {location_str}")
        
        # Attendees (abbreviated)
        attendees = meeting.get('attendees', [])
        if attendees:
            attendee_summary = extract_attendees(attendees)
            print(f"   👥 {attendee_summary}")
        
        # Meeting link
        web_link = meeting.get('webLink')
        if web_link:
            print(f"   🔗 Join: {web_link[:50]}...")
    
    # Summary
    print(f"\n📊 SUMMARY:")
    print(f"   📅 Date: {today.strftime('%A, %B %d, %Y')}")
    print(f"   🕐 Total Meetings: {len(todays_meetings)}")
    
    if todays_meetings:
        first_meeting = todays_meetings[0]
        last_meeting = todays_meetings[-1]
        
        first_time = format_meeting_time(
            first_meeting.get('start', {}).get('dateTime', ''),
            first_meeting.get('start', {}).get('dateTime', '')
        ).split('-')[0]
        
        last_time = format_meeting_time(
            last_meeting.get('end', {}).get('dateTime', ''),
            last_meeting.get('end', {}).get('dateTime', '')
        ).split('-')[1]
        
        print(f"   ⏰ Time Range: {first_time} - {last_time}")
    
    # Generate quick JSON for other tools
    meeting_summary = {
        "date": today.strftime('%Y-%m-%d'),
        "total_meetings": len(todays_meetings),
        "meetings": [
            {
                "time": format_meeting_time(
                    m.get('start', {}).get('dateTime', ''),
                    m.get('end', {}).get('dateTime', '')
                ),
                "subject": m.get('subject') or "Untitled Meeting",
                "is_organizer": m.get('isOrganizer', False),
                "location": m.get('location', {}).get('displayName'),
                "attendee_count": len(m.get('attendees', []))
            }
            for m in todays_meetings
        ]
    }
    
    # Save summary
    summary_file = f"todays_meetings_{today.strftime('%Y%m%d')}.json"
    with open(summary_file, 'w') as f:
        json.dump(meeting_summary, f, indent=2)
    
    print(f"   💾 Summary saved to: {summary_file}")

if __name__ == "__main__":
    find_todays_meetings()