"""
Extract today's meetings from Microsoft Graph API and save to data/meetings directory.
"""

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

try:
    from SilverFlow.graph_get_meetings import get_meetings
    
    # Get today's date
    today = datetime.now().date()
    today_str = today.strftime("%Y-%m-%d")
    
    print(f"📅 Extracting meetings for {today_str}...")
    
    # Calculate date range for today only
    start_date = today.isoformat()
    end_date = (today + timedelta(days=1)).isoformat()
    
    # Get meetings using SilverFlow
    print(f"Fetching meetings from {start_date} to {end_date}...")
    meetings = get_meetings(
        start_date=start_date,
        end_date=end_date,
        select_fields=["subject", "start", "end", "location", "attendees", "organizer", "bodyPreview", "isOnlineMeeting", "onlineMeetingUrl"]
    )
    
    print(f"✅ Found {len(meetings)} meetings for today")
    
    # Create output structure
    output = {
        "metadata": {
            "extraction_date": datetime.now().isoformat(),
            "target_date": today_str,
            "total_meetings": len(meetings),
            "source": "Microsoft Graph API via SilverFlow"
        },
        "meetings": meetings
    }
    
    # Save to data/meetings directory
    output_dir = Path("data/meetings")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_file = output_dir / f"meetings_{today_str}.json"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Saved to: {output_file}")
    
    # Print summary
    print("\n📊 Meeting Summary:")
    for i, meeting in enumerate(meetings, 1):
        start_time = meeting.get('start', {}).get('dateTime', 'N/A')
        subject = meeting.get('subject', 'No subject')
        print(f"  {i}. {start_time} - {subject}")
    
except ImportError as e:
    print(f"❌ Error: Could not import SilverFlow module")
    print(f"   {e}")
    print("\nTrying alternative method using calendar data file...")
    
    # Alternative: Load from existing calendar file
    calendar_file = Path("my_calendar_events_complete_attendees.json")
    if calendar_file.exists():
        with open(calendar_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        events = data.get('events', [])
        today = datetime.now().date()
        today_str = today.strftime("%Y-%m-%d")
        
        # Filter today's meetings
        todays_meetings = []
        for event in events:
            start_dt = event.get('start', {}).get('dateTime', '')
            if start_dt and start_dt.startswith(today_str):
                todays_meetings.append(event)
        
        print(f"✅ Found {len(todays_meetings)} meetings for {today_str}")
        
        # Create output structure
        output = {
            "metadata": {
                "extraction_date": datetime.now().isoformat(),
                "target_date": today_str,
                "total_meetings": len(todays_meetings),
                "source": "Local calendar cache"
            },
            "meetings": todays_meetings
        }
        
        # Save to data/meetings directory
        output_dir = Path("data/meetings")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        output_file = output_dir / f"meetings_{today_str}.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Saved to: {output_file}")
        
        # Print summary
        if todays_meetings:
            print("\n📊 Meeting Summary:")
            for i, meeting in enumerate(todays_meetings, 1):
                start_time = meeting.get('start', {}).get('dateTime', 'N/A')
                subject = meeting.get('subject', 'No subject')
                print(f"  {i}. {start_time} - {subject}")
        else:
            print("\nℹ️  No meetings found for today")
    else:
        print(f"❌ Calendar file not found: {calendar_file}")
        print("Please run calendar extraction first")
        sys.exit(1)

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
