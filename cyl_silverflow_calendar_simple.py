#!/usr/bin/env python3
"""
CYL's Real Microsoft Calendar Integration - SilverFlow Simple Pattern
Directly using SilverFlow's proven Graph client ID and authentication approach.
No custom app registration needed - leverages existing Microsoft Graph permissions.
"""

import os
import sys
import json
import msal
import requests
from datetime import datetime, timedelta, timezone
from typing import Dict, Any, List, Optional
from urllib.parse import quote


def safe_print(*args, **kwargs):
    """Print text defensively for Windows consoles with legacy code pages."""
    try:
        print(*args, **kwargs)
    except UnicodeEncodeError:
        encoded_args = []
        for arg in args:
            if isinstance(arg, str):
                encoded_args.append(arg.encode('ascii', 'replace').decode('ascii'))
            else:
                encoded_args.append(str(arg))
        print(*encoded_args, **kwargs)


# SilverFlow's proven configuration - using their default/substrate client ID
TENANT_ID = "72f988bf-86f1-41af-91ab-2d7cd011db47"  # Microsoft tenant
GRAPH_CLIENT_ID = "d3590ed6-52b3-4102-aeff-aad2292ab01c"  # SilverFlow's default client (not SPA)
GRAPH_SCOPES = ["https://graph.microsoft.com/Calendars.Read"]  # Use full scope URL


def _login_hint() -> Optional[str]:
    """Generate login hint based on current Windows username."""
    user = os.getenv("USERNAME") or os.getenv("USER")
    return f"{user}@microsoft.com" if user else None


def acquire_graph_token() -> Dict[str, Any]:
    """
    Acquire Microsoft Graph token using SilverFlow's proven pattern.
    Uses Windows Broker (WAM) for seamless authentication.
    """
    safe_print("🔐 Acquiring Microsoft Graph token...")
    
    authority = f"https://login.microsoftonline.com/{TENANT_ID}"
    
    # Try Windows Broker first (like SilverFlow)
    try:
        app = msal.PublicClientApplication(
            GRAPH_CLIENT_ID,
            authority=authority,
            enable_broker_on_windows=True,
        )
        broker_enabled = True
        safe_print("✅ Windows Broker (WAM) authentication enabled")
    except Exception as e:
        safe_print(f"⚠️  Windows Broker unavailable, using fallback: {e}")
        app = msal.PublicClientApplication(
            GRAPH_CLIENT_ID,
            authority=authority,
            enable_broker_on_windows=False,
        )
        broker_enabled = False

    login_hint = _login_hint()
    account = None
    
    # Try to get cached account first (silent auth)
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

    # Try silent token acquisition first
    if account:
        safe_print("🔄 Trying silent token acquisition...")
        result = app.acquire_token_silent(GRAPH_SCOPES, account=account)
        if result and "access_token" in result:
            safe_print("✅ Silent authentication successful!")
            return result

    # Interactive authentication (browser-based)
    safe_print("🌐 Starting interactive authentication (browser)...")
    kwargs = {"scopes": GRAPH_SCOPES}
    if login_hint:
        kwargs["login_hint"] = login_hint
    if broker_enabled:
        kwargs["parent_window_handle"] = msal.application.PublicClientApplication.CONSOLE_WINDOW_HANDLE

    result = app.acquire_token_interactive(**kwargs)
    
    if result and "access_token" in result:
        safe_print("✅ Interactive authentication successful!")
        return result
    else:
        error_msg = result.get("error_description") or result.get("error") or "Unknown authentication error"
        safe_print(f"❌ Authentication failed: {error_msg}")
        raise RuntimeError(f"Authentication failed: {error_msg}")


def build_calendar_url(start_date: datetime, end_date: datetime) -> str:
    """Build Microsoft Graph calendar view URL."""
    start_iso = start_date.astimezone(timezone.utc).isoformat()
    end_iso = end_date.astimezone(timezone.utc).isoformat()
    
    base_url = "https://graph.microsoft.com/v1.0/me/calendarView"
    params = [
        f"startDateTime={quote(start_iso)}",
        f"endDateTime={quote(end_iso)}",
        "$orderby=start/dateTime",
        "$top=50"
    ]
    
    return f"{base_url}?{'&'.join(params)}"


def fetch_calendar_events(access_token: str, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
    """Fetch calendar events from Microsoft Graph."""
    safe_print(f"📅 Fetching calendar events from {start_date.date()} to {end_date.date()}...")
    
    url = build_calendar_url(start_date, end_date)
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json",
        "Prefer": 'outlook.timezone="Pacific Standard Time"'
    }
    
    all_events = []
    page = 0
    
    while url:
        page += 1
        safe_print(f"📄 Fetching page {page}...")
        
        try:
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            events = data.get("value", [])
            all_events.extend(events)
            
            # Check for next page
            url = data.get("@odata.nextLink")
            
            safe_print(f"   Found {len(events)} events on page {page}")
            
        except requests.exceptions.RequestException as e:
            safe_print(f"❌ Error fetching calendar data: {e}")
            break
    
    safe_print(f"✅ Total events retrieved: {len(all_events)}")
    return all_events


def analyze_meetings(events: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Analyze calendar events for insights."""
    safe_print("\n🔍 Analyzing meetings...")
    
    total_meetings = len(events)
    accepted_meetings = 0
    tentative_meetings = 0
    declined_meetings = 0
    no_response_meetings = 0
    
    collaborators = set()
    meeting_subjects = []
    
    for event in events:
        # Response status analysis
        response_status = event.get("responseStatus", {}).get("response", "none").lower()
        if response_status == "accepted":
            accepted_meetings += 1
        elif response_status == "tentativelyaccepted":
            tentative_meetings += 1
        elif response_status == "declined":
            declined_meetings += 1
        else:
            no_response_meetings += 1
        
        # Collect collaborators
        organizer = event.get("organizer", {}).get("emailAddress", {})
        if organizer.get("address"):
            collaborators.add(organizer["address"])
        
        for attendee in event.get("attendees", []):
            email = attendee.get("emailAddress", {}).get("address")
            if email:
                collaborators.add(email)
        
        # Collect subjects
        subject = event.get("subject", "No Subject")
        meeting_subjects.append(subject)
    
    analysis = {
        "total_meetings": total_meetings,
        "accepted_meetings": accepted_meetings,
        "tentative_meetings": tentative_meetings,
        "declined_meetings": declined_meetings,
        "no_response_meetings": no_response_meetings,
        "unique_collaborators": len(collaborators),
        "collaborator_list": sorted(list(collaborators)),
        "meeting_subjects": meeting_subjects[:10]  # First 10 subjects
    }
    
    return analysis


def print_meeting_summary(events: List[Dict[str, Any]], analysis: Dict[str, Any]):
    """Print a formatted summary of calendar events."""
    safe_print("\n" + "="*80)
    safe_print("📅 CYL'S REAL CALENDAR DATA - October 22, 2025")
    safe_print("="*80)
    
    safe_print(f"📊 MEETING STATISTICS:")
    safe_print(f"   • Total meetings: {analysis['total_meetings']}")
    safe_print(f"   • ✅ Accepted: {analysis['accepted_meetings']}")
    safe_print(f"   • ❓ Tentative: {analysis['tentative_meetings']}")
    safe_print(f"   • ❌ Declined: {analysis['declined_meetings']}")
    safe_print(f"   • ⚪ No response: {analysis['no_response_meetings']}")
    safe_print(f"   • 👥 Unique collaborators: {analysis['unique_collaborators']}")
    
    safe_print(f"\n🤝 TOP COLLABORATORS:")
    for i, collaborator in enumerate(analysis['collaborator_list'][:5], 1):
        safe_print(f"   {i}. {collaborator}")
    
    safe_print(f"\n📋 TODAY'S MEETINGS:")
    today_meetings = []
    today = datetime.now(timezone.utc).date()
    
    for event in events:
        start_time = event.get("start", {}).get("dateTime")
        if start_time:
            try:
                event_date = datetime.fromisoformat(start_time.replace('Z', '+00:00')).date()
                if event_date == today:
                    today_meetings.append(event)
            except:
                pass
    
    if today_meetings:
        for i, meeting in enumerate(today_meetings, 1):
            subject = meeting.get("subject", "No Subject")
            start_time = meeting.get("start", {}).get("dateTime", "Unknown time")
            response = meeting.get("responseStatus", {}).get("response", "none")
            
            status_emoji = {
                "accepted": "✅",
                "tentativelyaccepted": "❓", 
                "declined": "❌",
                "none": "⚪"
            }.get(response.lower(), "⚪")
            
            safe_print(f"   {i}. {status_emoji} {subject} ({start_time})")
    else:
        safe_print("   No meetings found for today")
    
    # Flight CI005 conflict analysis
    safe_print(f"\n✈️  FLIGHT CI005 ANALYSIS:")
    safe_print(f"   Flight CI005 departs at 4:25 PM PDT today")
    safe_print(f"   Checking for meeting conflicts...")
    
    conflicts = []
    for meeting in today_meetings:
        start_time = meeting.get("start", {}).get("dateTime")
        end_time = meeting.get("end", {}).get("dateTime")
        if start_time and end_time:
            try:
                start_dt = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
                end_dt = datetime.fromisoformat(end_time.replace('Z', '+00:00'))
                
                # Convert to PDT (UTC-7)
                pdt_offset = timedelta(hours=-7)
                start_pdt = start_dt + pdt_offset
                end_pdt = end_dt + pdt_offset
                
                # Flight departure at 4:25 PM PDT
                flight_time = start_pdt.replace(hour=16, minute=25, second=0, microsecond=0)
                
                # Check if meeting overlaps with travel time (need to leave by 2:25 PM for 4:25 PM flight)
                travel_time = flight_time - timedelta(hours=2)
                
                if end_pdt > travel_time:
                    conflicts.append({
                        "subject": meeting.get("subject", "No Subject"),
                        "end_time": end_pdt.strftime("%I:%M %p PDT"),
                        "response": meeting.get("responseStatus", {}).get("response", "none")
                    })
            except:
                pass
    
    if conflicts:
        safe_print(f"   ⚠️  {len(conflicts)} potential conflicts found:")
        for conflict in conflicts:
            safe_print(f"      • {conflict['subject']} (ends {conflict['end_time']}) - {conflict['response']}")
    else:
        safe_print(f"   ✅ No meeting conflicts with flight departure")


def main():
    """Main execution function."""
    try:
        safe_print("🚀 CYL's Real Microsoft Calendar Integration - SilverFlow Pattern")
        safe_print("="*70)
        
        # Authenticate
        token_result = acquire_graph_token()
        access_token = token_result["access_token"]
        
        # Get user info
        claims = token_result.get("id_token_claims", {})
        user_name = claims.get("name") or claims.get("preferred_username") or "Unknown User"
        safe_print(f"👤 Authenticated as: {user_name}")
        
        # Define date range for October 22, 2025
        target_date = datetime(2025, 10, 22, tzinfo=timezone.utc)
        start_date = target_date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = target_date.replace(hour=23, minute=59, second=59, microsecond=999999)
        
        # Fetch calendar events
        events = fetch_calendar_events(access_token, start_date, end_date)
        
        if not events:
            safe_print("📭 No meetings found for October 22, 2025")
            return
        
        # Analyze meetings
        analysis = analyze_meetings(events)
        
        # Print summary
        print_meeting_summary(events, analysis)
        
        # Save raw data
        output_file = "cyl_real_calendar_oct22_2025.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump({
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "user": user_name,
                "date_range": {
                    "start": start_date.isoformat(),
                    "end": end_date.isoformat()
                },
                "analysis": analysis,
                "events": events
            }, f, indent=2, ensure_ascii=False)
        
        safe_print(f"\n💾 Raw data saved to: {output_file}")
        safe_print("✅ Calendar integration completed successfully!")
        
    except Exception as e:
        safe_print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()