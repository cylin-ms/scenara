#!/usr/bin/env python3
"""
SilverFlow-Pattern Calendar Integration for Today's Meetings
Based on proven SilverFlow graph_get_meetings.py pattern, adapted for macOS
"""

import os
import sys
import json
import pathlib
import zoneinfo
from datetime import datetime, timedelta, timezone
from urllib.parse import quote
from typing import Dict, Any, List, Optional, Tuple
import requests
import msal


def safe_print(*args, **kwargs):
    """Print text defensively for Windows consoles with legacy code pages."""
    try:
        print(*args, **kwargs)
    except UnicodeEncodeError:
        # Fallback for legacy console encodings
        args_str = ' '.join(str(arg) for arg in args)
        args_safe = args_str.encode('utf-8', errors='replace').decode('utf-8')
        print(args_safe, **kwargs)


# SilverFlow's proven configuration
TENANT_ID = "72f988bf-86f1-41af-91ab-2d7cd011db47"  # Microsoft tenant
CLIENT_ID = "9ce97a32-d9ab-4ab2-aadc-f49b39b94e11"  # SilverFlow's working client
GRAPH_SCOPES = ["https://graph.microsoft.com/Calendars.Read"]  # Use full URI format
DEFAULT_FILTER = "(isCancelled eq false) and (showAs ne 'oof') and (showAs ne 'workingElsewhere')"
DEFAULT_SELECT = "id,subject,start,end,type,organizer,bodyPreview,webLink,seriesMasterId,responseStatus,showAs,attendees,location"


def _login_hint() -> Optional[str]:
    """Generate login hint for Microsoft employees."""
    user = os.getenv("USERNAME") or os.getenv("USER") or None
    return f"{user}@microsoft.com" if user else None


def acquire_token_interactive() -> Dict[str, Any]:
    """
    Acquire token using interactive authentication for macOS.
    Adapted from SilverFlow pattern but without Windows Broker.
    """
    authority = f"https://login.microsoftonline.com/{TENANT_ID}"
    
    # MSAL configuration for macOS (no Windows Broker)
    app = msal.PublicClientApplication(
        CLIENT_ID,
        authority=authority,
        # Note: enable_broker_on_windows removed for macOS compatibility
    )

    login_hint = _login_hint()
    account = None
    
    try:
        if login_hint:
            accounts = app.get_accounts(username=login_hint)
            if accounts:
                account = accounts[0]
        if not account:
            accounts = app.get_accounts()
            if accounts:
                account = accounts[0]
    except Exception:
        pass

    # Try silent authentication first
    if account:
        result = app.acquire_token_silent(GRAPH_SCOPES, account=account)
        if result and "access_token" in result:
            return result

    # Interactive authentication for macOS
    safe_print("🔐 Starting interactive authentication...")
    safe_print("A browser window will open for Microsoft login.")
    
    result = app.acquire_token_interactive(
        GRAPH_SCOPES,
        login_hint=login_hint,
        # Note: parent_window_handle removed for macOS compatibility
    )
    return result


def build_calendar_view_url(start: datetime, end: datetime) -> str:
    """Build the Microsoft Graph calendarView URL."""
    base_url = "https://graph.microsoft.com/v1.0"
    
    start_iso = start.astimezone(timezone.utc).isoformat()
    end_iso = end.astimezone(timezone.utc).isoformat()
    
    params = [
        f"startDateTime={quote(start_iso)}",
        f"endDateTime={quote(end_iso)}",
        f"$orderby=start/dateTime",
        f"$top=50",
        f"$select={quote(DEFAULT_SELECT)}",
        f"$filter={quote(DEFAULT_FILTER)}",
    ]
    
    return f"{base_url}/me/calendarView?{'&'.join(params)}"


def fetch_todays_meetings(access_token: str) -> Tuple[List[Dict[str, Any]], Optional[str]]:
    """Fetch today's meetings using SilverFlow's proven pattern."""
    # Today's date range (local timezone aware)
    try:
        local_tz = zoneinfo.ZoneInfo("America/Los_Angeles")
    except:
        local_tz = timezone(timedelta(hours=-7))  # PDT fallback
    
    now = datetime.now(local_tz)
    start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_day = now.replace(hour=23, minute=59, second=59, microsecond=999999)
    
    url = build_calendar_view_url(start_of_day, end_of_day)
    
    # SilverFlow's proven headers pattern
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Accept': 'application/json',
        'Prefer': 'IdType="ImmutableId", outlook.timezone="America/Los_Angeles"'
    }
    
    meetings = []
    page = 0
    
    while url:
        page += 1
        try:
            resp = requests.get(url, headers=headers, timeout=60)
        except Exception as ex:
            return meetings, f"Network error calling Graph: {ex}"
        
        if not resp.ok:
            return meetings, f"HTTP {resp.status_code} on page {page}: {resp.text[:400]}"
        
        try:
            data = resp.json()
        except Exception as ex:
            return meetings, f"Failed to parse JSON on page {page}: {ex}"
        
        page_meetings = (data or {}).get('value') or []
        if page_meetings:
            meetings.extend(page_meetings)
        
        # Handle pagination
        next_link = (data or {}).get('@odata.nextLink')
        if next_link and len(meetings) < 1000:  # Safety limit
            url = next_link
        else:
            url = None
    
    return meetings, None


def format_meeting_for_display(meeting: Dict[str, Any], local_tz) -> Dict[str, Any]:
    """Format meeting data with proper timezone conversion."""
    try:
        start_dt = datetime.fromisoformat(meeting['start']['dateTime'].replace('Z', '+00:00'))
        end_dt = datetime.fromisoformat(meeting['end']['dateTime'].replace('Z', '+00:00'))
        
        # Convert to local timezone
        start_local = start_dt.astimezone(local_tz)
        end_local = end_dt.astimezone(local_tz)
        
        duration_minutes = int((end_dt - start_dt).total_seconds() / 60)
        
        # Extract attendees
        attendees = []
        if meeting.get('attendees'):
            for attendee in meeting['attendees']:
                if attendee.get('emailAddress'):
                    attendees.append({
                        'name': attendee['emailAddress'].get('name', 'Unknown'),
                        'email': attendee['emailAddress'].get('address', ''),
                        'response': attendee.get('status', {}).get('response', 'none')
                    })
        
        return {
            'id': meeting.get('id', ''),
            'subject': meeting.get('subject', 'Untitled Meeting'),
            'start_time': start_local.strftime('%H:%M'),
            'end_time': end_local.strftime('%H:%M'),
            'timezone': start_local.strftime('%Z'),
            'duration_minutes': duration_minutes,
            'location': meeting.get('location', {}).get('displayName', ''),
            'is_online_meeting': meeting.get('onlineMeetingUrl') is not None,
            'online_meeting_url': meeting.get('onlineMeetingUrl', ''),
            'attendees': attendees,
            'attendee_count': len(attendees),
            'body_preview': meeting.get('bodyPreview', ''),
            'importance': meeting.get('importance', 'normal'),
            'is_organizer': meeting.get('isOrganizer', False),
            'response_status': meeting.get('responseStatus', {}).get('response', 'none'),
            'raw_meeting': meeting  # Keep original for reference
        }
    except Exception as ex:
        safe_print(f"Warning: Error formatting meeting {meeting.get('subject', 'Unknown')}: {ex}")
        return None


def display_meetings(meetings: List[Dict[str, Any]]):
    """Display meetings in a beautiful console format."""
    if not meetings:
        safe_print("📅 No meetings found for today!")
        return
    
    safe_print(f"\n📅 Your Real Meetings Today - {datetime.now().strftime('%B %d, %Y')}")
    safe_print("=" * 60)
    safe_print(f"📊 Total meetings: {len(meetings)}")
    safe_print()
    
    # Group by status
    accepted = [m for m in meetings if m['response_status'] == 'accepted']
    tentative = [m for m in meetings if m['response_status'] == 'tentativelyAccepted']
    others = [m for m in meetings if m['response_status'] not in ['accepted', 'tentativelyAccepted']]
    
    safe_print(f"✅ **Accepted:** {len(accepted)} meetings")
    safe_print(f"❓ **Tentative:** {len(tentative)} meetings")
    safe_print(f"📋 **Other:** {len(others)} meetings")
    safe_print()
    
    # Display all meetings sorted by time
    all_meetings = sorted(meetings, key=lambda m: m['start_time'])
    
    for i, meeting in enumerate(all_meetings, 1):
        status_emoji = "✅" if meeting['response_status'] == 'accepted' else "❓" if meeting['response_status'] == 'tentativelyAccepted' else "📋"
        duration_str = f"{meeting['duration_minutes']//60}h {meeting['duration_minutes']%60}m" if meeting['duration_minutes'] >= 60 else f"{meeting['duration_minutes']}m"
        
        safe_print(f"{i}. {status_emoji} **{meeting['subject']}**")
        safe_print(f"   ⏰ {meeting['start_time']} - {meeting['end_time']} {meeting['timezone']} ({duration_str})")
        
        if meeting['is_online_meeting']:
            safe_print(f"   🌐 Online Meeting")
        elif meeting['location']:
            safe_print(f"   📍 {meeting['location']}")
        
        if meeting['attendees']:
            safe_print(f"   👥 {meeting['attendee_count']} attendees")
            # Show first few attendees
            for attendee in meeting['attendees'][:3]:
                safe_print(f"      ({attendee['name']})")
            if len(meeting['attendees']) > 3:
                safe_print(f"      ... and {len(meeting['attendees']) - 3} more")
        
        safe_print()


def main():
    """Main function following SilverFlow pattern."""
    safe_print("🎯 SilverFlow-Pattern Real Calendar Access")
    safe_print("Fetching your actual Microsoft 365 meetings for today...")
    safe_print()
    
    # Acquire token using SilverFlow's proven Windows Broker pattern
    result = acquire_token_interactive()
    if not result or "access_token" not in result:
        err = (result or {}).get("error_description") or (result or {}).get("error") or "Unknown error"
        safe_print(f"❌ Authentication failed: {err}")
        return 1
    
    access_token = result["access_token"]
    safe_print("✅ Authentication successful!")
    
    # Fetch today's meetings
    safe_print("📡 Fetching today's meetings from Microsoft Graph...")
    raw_meetings, error = fetch_todays_meetings(access_token)
    
    if error:
        safe_print(f"⚠️ Warning: {error}")
    
    if not raw_meetings:
        safe_print("📅 No meetings found for today.")
        return 0
    
    # Set up timezone for formatting
    try:
        local_tz = zoneinfo.ZoneInfo("America/Los_Angeles")
    except:
        local_tz = timezone(timedelta(hours=-7))  # PDT fallback
    
    # Format meetings for display
    formatted_meetings = []
    for meeting in raw_meetings:
        formatted = format_meeting_for_display(meeting, local_tz)
        if formatted:
            formatted_meetings.append(formatted)
    
    # Display results
    display_meetings(formatted_meetings)
    
    # Save raw data for further analysis
    output_dir = pathlib.Path("meeting_outputs")
    output_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = output_dir / f"silverflow_real_meetings_{timestamp}.json"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'meeting_count': len(formatted_meetings),
            'meetings': formatted_meetings,
            'raw_meetings': raw_meetings
        }, f, indent=2, ensure_ascii=False)
    
    safe_print(f"💾 Data saved to: {output_file}")
    safe_print(f"\n🎯 Ready for Flight CI005 analysis at 4:25 PM PDT!")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())