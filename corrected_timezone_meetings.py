#!/usr/bin/env python3
"""
CORRECTED Tomorrow's Meeting Schedule for cyl@microsoft.com
Tuesday, October 22, 2025 - PACIFIC TIME (PDT, UTC-7)
"""

from datetime import datetime, timezone, timedelta
import pytz

def show_corrected_meetings():
    """Display tomorrow's meetings in correct Pacific Time"""
    
    print("📅 YOUR MEETINGS FOR TOMORROW (CORRECTED)")
    print("🗓️  Tuesday, October 22, 2025")
    print("🌏 Time Zone: Pacific Daylight Time (PDT, UTC-7)")
    print("👤 cyl@microsoft.com")
    print("=" * 60)
    
    # UTC times from the data, converted to Pacific Time
    meetings_utc = [
        {"utc_start": 9, "utc_end": 10, "title": "Meeting with Charlie Chung", "attendees": ["Charlie Chung"]},
        {"utc_start": 11, "utc_end": 12, "title": "Sync and Discuss", "attendees": ["Haidong Zhang", "Chin-Yew Lin", "Weiwei Cui"]},
        {"utc_start": 13, "utc_end": 14, "title": "HIVE | T+P Meeting Prep Monthly Sync", "attendees": ["Drew Brough", "Eran Yariv", "Danny Avigdor"]},
        {"utc_start": 15, "utc_end": 16, "title": "Test Tenant Data Discussion", "attendees": ["Song Ge", "Chin-Yew Lin", "Haidong Zhang"]},
        {"utc_start": 17, "utc_end": 18, "title": "What's New & Coming in Azure AI Foundry Agent Services?", "attendees": ["Jason Virtue", "Mark Tabladillo", "Alex Blanton"]}
    ]
    
    pacific_offset = -7  # PDT is UTC-7
    
    print("🚨 **TIMEZONE CORRECTION APPLIED**")
    print("   Previous times were shown in UTC")
    print("   Corrected to Pacific Daylight Time (PDT)")
    print()
    
    for i, meeting in enumerate(meetings_utc, 1):
        # Convert UTC to Pacific Time
        pacific_start = meeting["utc_start"] + pacific_offset
        pacific_end = meeting["utc_end"] + pacific_offset
        
        # Handle day rollover
        day_note = ""
        if pacific_start < 0:
            pacific_start += 24
            pacific_end += 24
            day_note = " (Monday night)"
        
        # Format times
        start_time = f"{pacific_start:02d}:00"
        end_time = f"{pacific_end:02d}:00"
        
        print(f"🕒 **{i}. {meeting['title']}**{day_note}")
        print(f"   ⏰ Pacific Time: {start_time} - {end_time}")
        print(f"   🌐 UTC Time: {meeting['utc_start']:02d}:00 - {meeting['utc_end']:02d}:00")
        print(f"   👥 Attendees ({len(meeting['attendees'])}):")
        for attendee in meeting['attendees']:
            print(f"      • {attendee}")
        print()
    
    print("⚠️  **IMPORTANT MEETING TIME ANALYSIS**")
    print("=" * 60)
    
    # Analyze the corrected times
    corrected_analysis = [
        "02:00-03:00 PDT: Very early morning meeting (unusual for Pacific timezone)",
        "04:00-05:00 PDT: Early morning meeting (before typical work hours)",
        "06:00-07:00 PDT: Early morning meeting (still before typical work hours)", 
        "08:00-09:00 PDT: Normal morning meeting time",
        "10:00-11:00 PDT: Normal morning meeting time"
    ]
    
    for analysis in corrected_analysis:
        print(f"   📊 {analysis}")
    
    print()
    print("🤔 **TIMEZONE HYPOTHESIS**")
    print("These meeting times suggest either:")
    print("   1. 🌏 Meetings scheduled for attendees in other timezones (Asia/Europe)")
    print("   2. 📅 The calendar data may already be in Pacific Time (not UTC)")
    print("   3. 🔄 The original UTC assumption was incorrect")

def check_calendar_data_timezone():
    """Check the original calendar data to understand timezone"""
    
    print("\n🔍 **CALENDAR DATA ANALYSIS**")
    print("=" * 60)
    
    try:
        import json
        from pathlib import Path
        
        calendar_file = Path("my_calendar_events_50.json")
        if calendar_file.exists():
            with open(calendar_file) as f:
                data = json.load(f)
            
            print(f"📄 Found calendar file: {calendar_file}")
            
            # Look for timezone indicators in the data
            sample_events = data[:3] if isinstance(data, list) else []
            
            print("\n📋 **Sample Event Analysis:**")
            for i, event in enumerate(sample_events, 1):
                print(f"\n   Event {i}: {event.get('subject', 'No subject')}")
                
                # Check for timezone information
                start_time = event.get('start', {})
                end_time = event.get('end', {})
                
                if isinstance(start_time, dict):
                    start_dt = start_time.get('dateTime', 'N/A')
                    start_tz = start_time.get('timeZone', 'N/A')
                    print(f"   Start: {start_dt} ({start_tz})")
                
                if isinstance(end_time, dict):
                    end_dt = end_time.get('dateTime', 'N/A') 
                    end_tz = end_time.get('timeZone', 'N/A')
                    print(f"   End: {end_dt} ({end_tz})")
                
                # Look for any timezone fields
                tz_fields = [k for k in event.keys() if 'time' in k.lower() or 'zone' in k.lower()]
                if tz_fields:
                    print(f"   Timezone fields: {tz_fields}")
        else:
            print(f"❌ Calendar file not found: {calendar_file}")
            
    except Exception as e:
        print(f"⚠️ Error analyzing calendar data: {e}")

def provide_timezone_recommendations():
    """Provide recommendations for proper timezone handling"""
    
    print("\n🎯 **TIMEZONE HANDLING RECOMMENDATIONS**")
    print("=" * 60)
    
    recommendations = [
        "🔧 Update Microsoft Graph integration to respect user timezone",
        "📍 Detect user location from Microsoft 365 profile",
        "⚙️ Add timezone parameter to meeting viewer tools",
        "🌏 Display meetings in both local time and UTC for clarity",
        "✅ Validate timezone handling with real Microsoft Graph API data"
    ]
    
    for i, rec in enumerate(recommendations, 1):
        print(f"   {i}. {rec}")
    
    print("\n💡 **IMMEDIATE ACTIONS**")
    print("   1. 🔍 Verify your actual meeting times in Outlook/Teams")
    print("   2. 🕒 Confirm which timezone your calendar shows") 
    print("   3. 🔧 I'll update the tools to handle Pacific Time correctly")
    print("   4. 📊 When we get real Microsoft Graph data, timezone will be properly handled")

if __name__ == "__main__":
    show_corrected_meetings()
    check_calendar_data_timezone()
    provide_timezone_recommendations()
    
    print("\n" + "="*60)
    print("🚨 TIMEZONE CORRECTION APPLIED")
    print("📧 Please verify these times against your actual Outlook calendar")
    print("🔧 Future versions will handle timezone automatically")
    print("="*60)