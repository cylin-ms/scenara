#!/usr/bin/env python3
"""
macOS-Optimized Calendar Automation using AppleScript
Automates Safari to interact with Graph Explorer for calendar access
"""

import os
import sys
import json
import time
import subprocess
import tempfile
import zoneinfo
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Optional


def create_applescript_automation() -> str:
    """Create AppleScript for Safari automation."""
    query = build_calendar_query()
    
    applescript = f'''
    tell application "Safari"
        activate
        
        -- Open Graph Explorer
        set theURL to "https://developer.microsoft.com/en-us/graph/graph-explorer"
        tell window 1
            set current tab to (make new tab with properties {{URL:theURL}})
        end tell
        
        -- Wait for page to load
        delay 5
        
        -- Wait for user to authenticate
        display dialog "Please complete Microsoft authentication in Safari, then click OK to continue." buttons {{"OK"}} default button "OK"
        
        -- Wait a bit more for the page to be ready
        delay 3
        
        -- Execute JavaScript to set query and submit
        set theQuery to "{query}"
        set theScript to "
            // Find query input
            var queryInput = document.querySelector('input[placeholder*=\"query\"], input[aria-label*=\"query\"], textarea[placeholder*=\"query\"]');
            if (!queryInput) {{
                queryInput = document.querySelector('input[type=\"text\"]');
            }}
            
            if (queryInput) {{
                queryInput.value = '" & theQuery & "';
                queryInput.dispatchEvent(new Event('input', {{ bubbles: true }}));
                
                // Find and click run button
                var runButton = document.querySelector('button[title*=\"Run\"], button[aria-label*=\"Run\"]');
                if (!runButton) {{
                    // Try finding by text content
                    var buttons = document.querySelectorAll('button');
                    for (var i = 0; i < buttons.length; i++) {{
                        if (buttons[i].textContent.toLowerCase().includes('run')) {{
                            runButton = buttons[i];
                            break;
                        }}
                    }}
                }}
                
                if (runButton) {{
                    runButton.click();
                }} else {{
                    // Try pressing Enter
                    queryInput.dispatchEvent(new KeyboardEvent('keydown', {{ key: 'Enter', code: 'Enter' }}));
                }}
                
                'Query executed successfully';
            }} else {{
                'Could not find query input field';
            }}
        "
        
        set theResult to do JavaScript theScript in current tab of window 1
        
        -- Wait for results to load
        delay 5
        
        -- Get the JSON response
        set getResponseScript to "
            var responseElement = document.querySelector('.response-body, .json-response, .response-content, pre, code');
            if (!responseElement) {{
                var elements = document.querySelectorAll('*');
                for (var i = 0; i < elements.length; i++) {{
                    var text = elements[i].textContent.trim();
                    if (text.startsWith('{{') && text.length > 100) {{
                        responseElement = elements[i];
                        break;
                    }}
                }}
            }}
            
            if (responseElement) {{
                responseElement.textContent;
            }} else {{
                'No JSON response found';
            }}
        "
        
        set jsonResponse to do JavaScript getResponseScript in current tab of window 1
        
        -- Return the JSON response
        return jsonResponse
    end tell
    '''
    
    return applescript


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


def run_applescript(script: str) -> str:
    """Execute AppleScript and return the result."""
    try:
        # Write script to temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.scpt', delete=False) as f:
            f.write(script)
            script_path = f.name
        
        # Execute the script
        result = subprocess.run(
            ['osascript', script_path],
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )
        
        # Clean up
        os.unlink(script_path)
        
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            print(f"❌ AppleScript error: {{result.stderr}}")
            return None
            
    except subprocess.TimeoutExpired:
        print("❌ AppleScript execution timed out")
        return None
    except Exception as e:
        print(f"❌ Error running AppleScript: {{e}}")
        return None


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
        print(f"❌ Error parsing datetime '{{iso_string}}': {{e}}")
        return None


def format_meeting_time(start_dt: datetime, end_dt: datetime) -> str:
    """Format meeting time range in local timezone."""
    if not start_dt or not end_dt:
        return "❓ Time unavailable"
    
    # Check if same day
    if start_dt.date() == end_dt.date():
        return f"{{start_dt.strftime('%I:%M %p')}} - {{end_dt.strftime('%I:%M %p PDT')}}"
    else:
        return f"{{start_dt.strftime('%m/%d %I:%M %p')}} - {{end_dt.strftime('%m/%d %I:%M %p PDT')}}"


def extract_location(meeting: Dict[str, Any]) -> str:
    """Extract location information from meeting."""
    location = meeting.get('location', {{}})
    
    if isinstance(location, dict):
        display_name = location.get('displayName', '')
        if display_name:
            return f"📍 {{display_name}}"
    
    return ""


def analyze_meeting_conflicts(meetings: List[Dict[str, Any]]) -> None:
    """Analyze meetings for potential conflicts with Flight CI005 at 4:25 PM PDT."""
    flight_time = "4:25 PM PDT"
    print(f"\\n✈️ Flight CI005 Conflict Analysis (Departure: {{flight_time}}):")
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
            print(f"⚠️  CONFLICT: {{meeting.get('subject', 'No subject')}} ({{time_range}})")
    
    if not conflicts_found:
        print("✅ No meeting conflicts with flight departure!")


def display_calendar_results(response_json: Dict[str, Any]) -> None:
    """Display the calendar results in a formatted way."""
    try:
        meetings = response_json.get('value', [])
        
        print("\\n📅 Today's Meetings from Microsoft Graph Explorer")
        print("=" * 55)
        print(f"Found {{len(meetings)}} meeting(s) for today\\n")
        
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
            organizer = meeting.get('organizer', {{}}).get('emailAddress', {{}})
            organizer_name = organizer.get('name', 'Unknown')
            
            # Get location
            location = extract_location(meeting)
            
            # Response status
            response = meeting.get('responseStatus', {{}}).get('response', 'none')
            status_emoji = {{
                'accepted': '✅',
                'tentative': '❓',
                'declined': '❌',
                'none': '⏳'
            }}.get(response, '⏳')
            
            print(f"{{i}}. {{subject}}")
            print(f"   ⏰ {{time_range}}")
            print(f"   👤 Organizer: {{organizer_name}}")
            if location:
                print(f"   {{location}}")
            print(f"   {{status_emoji}} Status: {{response.title()}}")
            print()
        
        # Analyze flight conflicts
        analyze_meeting_conflicts(meetings)
        
    except Exception as e:
        print(f"❌ Error displaying results: {{e}}")


def main():
    """Main automation function for macOS."""
    print("🍎 macOS Calendar Automation via Safari")
    print("=" * 40)
    
    try:
        # Create and run AppleScript
        print("📱 Opening Safari and navigating to Graph Explorer...")
        script = create_applescript_automation()
        
        print("🔐 Please complete authentication when prompted...")
        json_response = run_applescript(script)
        
        if json_response and json_response != "No JSON response found":
            try:
                # Parse the JSON response
                response_json = json.loads(json_response)
                
                # Display results
                display_calendar_results(response_json)
                
                # Save results to file
                output_file = f"calendar_today_{{datetime.now().strftime('%Y%m%d_%H%M%S')}}.json"
                with open(output_file, 'w') as f:
                    json.dump(response_json, f, indent=2)
                print(f"\\n💾 Results saved to: {{output_file}}")
                
            except json.JSONDecodeError as e:
                print(f"❌ Failed to parse JSON response: {{e}}")
                print(f"Raw response: {{json_response[:200]}}...")
        else:
            print("❌ Failed to retrieve calendar data via AppleScript")
            print("💡 Falling back to manual process:")
            print("   1. Go to https://developer.microsoft.com/en-us/graph/graph-explorer")
            print(f"   2. Execute: GET {{build_calendar_query()}}")
            print("   3. Use the parse_graph_explorer_response.py tool")
    
    except KeyboardInterrupt:
        print("\\n⚠️ Operation cancelled by user")
    except Exception as e:
        print(f"❌ Automation failed: {{e}}")
        print("💡 Please try the manual approach or the Selenium version")


if __name__ == "__main__":
    main()