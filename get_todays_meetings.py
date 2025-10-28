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
    # Try using SilverFlow graph_get_meetings.py script
    import subprocess
    import os
    
    today = datetime.now().date()
    today_str = today.strftime("%Y-%m-%d")
    
    print(f"📅 Extracting meetings for {today_str}...")
    
    # Use SilverFlow script directly
    silverflow_script = Path("SilverFlow/data/graph_get_meetings.py")
    
    if silverflow_script.exists():
        print("🔄 Using SilverFlow Graph API extraction...")
        
        # Run SilverFlow script to get today's meetings
        result = subprocess.run(
            [
                sys.executable,
                "graph_get_meetings.py",
                "0",  # 0 days forward (today only)
                "--select", "subject,start,end,location,attendees,organizer,bodyPreview,isOnlineMeeting,onlineMeetingUrl",
                "--max-events", "50"
            ],
            cwd="SilverFlow/data",
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            # Read the generated JSON file
            json_output = silverflow_script.parent / "out" / "graph_meetings.json"
            
            if json_output.exists():
                with open(json_output, 'r', encoding='utf-8') as f:
                    silverflow_data = json.load(f)
                
                meetings = silverflow_data.get('events', [])
                
                # Filter for today's meetings only
                todays_meetings = []
                for meeting in meetings:
                    start_dt = meeting.get('start', {}).get('dateTime', '')
                    if start_dt and start_dt.startswith(today_str):
                        todays_meetings.append(meeting)
                
                print(f"✅ Found {len(todays_meetings)} meetings for today")
                
                # Create output structure
                output = {
                    "metadata": {
                        "extraction_date": datetime.now().isoformat(),
                        "target_date": today_str,
                        "total_meetings": len(todays_meetings),
                        "source": "Microsoft Graph API via SilverFlow",
                        "extraction_method": "graph_get_meetings.py"
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
                        attendees = meeting.get('attendees', [])
                        print(f"  {i}. {start_time} - {subject}")
                        print(f"      Attendees: {len(attendees)} people")
                else:
                    print("\nℹ️  No meetings found for today")
                
                sys.exit(0)
            else:
                print(f"⚠️  SilverFlow output file not found: {json_output}")
                print("Falling back to cached data...")
        else:
            print(f"⚠️  SilverFlow extraction failed: {result.stderr}")
            print("Falling back to cached data...")
    else:
        print(f"⚠️  SilverFlow script not found: {silverflow_script}")
        print("Falling back to cached data...")

except Exception as e:
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
