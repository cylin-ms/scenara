#!/usr/bin/env python3
"""
Real Microsoft Graph Calendar Integration - SilverFlow Pattern
Improved authentication and calendar access following SilverFlow's proven patterns.
"""

import os
import sys
import json
import msal
import requests
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Optional, Tuple
from pathlib import Path

# Configuration - Using CYL's actual Azure app registration
GRAPH_CLIENT_ID = "82ec4101-520f-443d-a61e-593dca1f0c95"  # CYL's Me Notes Intelligence app
MICROSOFT_TENANT_ID = "72f988bf-86f1-41af-91ab-2d7cd011db47"  # Microsoft tenant
GRAPH_SCOPES = ["Calendars.Read", "User.Read"]  # SilverFlow's exact scope pattern
GRAPH_BASE_URL = "https://graph.microsoft.com/v1.0"

# Default calendar query settings
DEFAULT_FILTER = "(isCancelled eq false) and (showAs ne 'oof') and (showAs ne 'workingElsewhere')"
DEFAULT_SELECT = "id,subject,start,end,type,organizer,bodyPreview,webLink,seriesMasterId,responseStatus,showAs,attendees,location"

def safe_print(*args, **kwargs):
    """Print text defensively for console compatibility."""
    try:
        print(*args, **kwargs)
    except UnicodeEncodeError:
        safe_args = []
        for arg in args:
            if isinstance(arg, str):
                safe_args.append(arg.encode('ascii', 'replace').decode('ascii'))
            else:
                safe_args.append(str(arg))
        print(*safe_args, **kwargs)

def _login_hint() -> Optional[str]:
    """Generate login hint for MSAL authentication - SilverFlow pattern."""
    user = os.getenv("USERNAME") or os.getenv("USER") or ""
    return f"{user}@microsoft.com" if user else None

def acquire_token_interactive(scopes: List[str]) -> Dict[str, Any]:
    """
    Acquire Microsoft Graph token using MSAL with Windows Broker support.
    Based on SilverFlow's proven authentication pattern.
    """
    authority = f"https://login.microsoftonline.com/{MICROSOFT_TENANT_ID}"
    
    # Try to enable Windows Broker (WAM) for seamless auth
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

    # First, try to find cached accounts (silent authentication)
    try:
        if login_hint:
            accounts = app.get_accounts(username=login_hint)
            if accounts:
                account = accounts[0]
                safe_print(f"📋 Found cached account: {account.get('username', 'Unknown')}")
        
        if not account:
            accounts = app.get_accounts()
            if accounts:
                account = accounts[0]
                safe_print(f"📋 Using cached account: {account.get('username', 'Unknown')}")
    except Exception as e:
        safe_print(f"⚠️  Could not access cached accounts: {e}")
        account = None

    # Try silent authentication first
    if account:
        safe_print("🔐 Attempting silent authentication...")
        result = app.acquire_token_silent(scopes, account=account)
        if result and "access_token" in result:
            safe_print("✅ Silent authentication successful!")
            return result

    # Fall back to interactive authentication
    safe_print("🔐 Starting interactive authentication...")
    kwargs = {"scopes": scopes}
    
    if login_hint:
        kwargs["login_hint"] = login_hint
        
    if broker_enabled:
        kwargs["parent_window_handle"] = msal.application.PublicClientApplication.CONSOLE_WINDOW_HANDLE

    result = app.acquire_token_interactive(**kwargs)
    
    if "access_token" not in result:
        error_msg = result.get("error_description") or result.get("error") or "Unknown authentication error"
        raise RuntimeError(f"Authentication failed: {error_msg}")
    
    # Extract user info for confirmation
    claims = result.get("id_token_claims", {})
    user_display = claims.get("name") or claims.get("preferred_username") or "Unknown User"
    safe_print(f"✅ Authentication successful for: {user_display}")
    
    return result

def build_calendar_view_url(start_time: datetime, end_time: datetime, 
                           select: str = DEFAULT_SELECT, 
                           filter_clause: str = DEFAULT_FILTER,
                           top: int = 50) -> str:
    """Build Microsoft Graph calendar view URL with proper formatting."""
    from urllib.parse import quote
    
    start_iso = start_time.isoformat()
    end_iso = end_time.isoformat()
    
    params = [
        f"startDateTime={quote(start_iso)}",
        f"endDateTime={quote(end_iso)}",
        f"$top={top}",
        f"$select={quote(select)}",
        f"$filter={quote(filter_clause)}"
    ]
    
    url = f"{GRAPH_BASE_URL}/me/calendarview?" + "&".join(params)
    return url

def fetch_calendar_events(access_token: str, start_time: datetime, end_time: datetime,
                         max_events: int = 100) -> Tuple[List[Dict[str, Any]], Optional[str]]:
    """
    Fetch calendar events from Microsoft Graph with pagination support.
    Returns (events_list, error_message).
    """
    url = build_calendar_view_url(start_time, end_time)
    
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Accept': 'application/json',
        'Prefer': 'IdType="ImmutableId", outlook.timezone="UTC"'
    }
    
    events = []
    page_count = 0
    
    while url and len(events) < max_events:
        page_count += 1
        safe_print(f"📄 Fetching calendar page {page_count}...")
        
        try:
            response = requests.get(url, headers=headers, timeout=60)
        except Exception as e:
            return events, f"Network error: {e}"
        
        if not response.ok:
            error_detail = response.text[:500] if response.text else "No details"
            return events, f"HTTP {response.status_code}: {error_detail}"
        
        try:
            data = response.json()
        except json.JSONDecodeError as e:
            return events, f"Invalid JSON response: {e}"
        
        page_events = data.get("value", [])
        events.extend(page_events)
        
        safe_print(f"📅 Retrieved {len(page_events)} events from page {page_count}")
        
        # Check for next page
        url = data.get("@odata.nextLink")
        
        if len(events) >= max_events:
            events = events[:max_events]
            break
    
    return events, None

def analyze_meeting_conflicts(events: List[Dict[str, Any]], 
                             flight_departure: datetime = None) -> Dict[str, Any]:
    """Analyze calendar events for conflicts and patterns."""
    
    analysis = {
        "total_meetings": len(events),
        "accepted_meetings": 0,
        "tentative_meetings": 0,
        "declined_meetings": 0,
        "organizer_meetings": 0,
        "attendee_meetings": 0,
        "conflicts": [],
        "flight_conflicts": []
    }
    
    # Flight CI005 departure: 4:25 PM PDT (21:25 UTC) on October 22, 2025
    if flight_departure is None:
        flight_departure = datetime(2025, 10, 22, 21, 25, 0, tzinfo=timezone.utc)
    
    # Buffer times around flight
    conflict_start = flight_departure - timedelta(hours=2)  # 2 hours before
    conflict_end = flight_departure + timedelta(hours=1)    # 1 hour after
    
    for event in events:
        # Extract response status
        response_status = event.get("responseStatus", {}).get("response", "none").lower()
        
        if response_status == "accepted":
            analysis["accepted_meetings"] += 1
        elif response_status == "tentativelyaccepted":
            analysis["tentative_meetings"] += 1
        elif response_status == "declined":
            analysis["declined_meetings"] += 1
        
        # Check if user is organizer
        organizer = event.get("organizer", {})
        if organizer and organizer.get("emailAddress", {}).get("address", "").endswith("@microsoft.com"):
            analysis["organizer_meetings"] += 1
        else:
            analysis["attendee_meetings"] += 1
        
        # Check for flight conflicts
        try:
            start_str = event.get("start", {}).get("dateTime", "")
            end_str = event.get("end", {}).get("dateTime", "")
            
            if start_str and end_str:
                meeting_start = datetime.fromisoformat(start_str.replace('Z', '+00:00'))
                meeting_end = datetime.fromisoformat(end_str.replace('Z', '+00:00'))
                
                # Check if meeting overlaps with flight buffer period
                if (meeting_start < conflict_end and meeting_end > conflict_start):
                    conflict_info = {
                        "subject": event.get("subject", "No Subject"),
                        "start": meeting_start.isoformat(),
                        "end": meeting_end.isoformat(),
                        "response_status": response_status,
                        "organizer": organizer.get("emailAddress", {}).get("name", "Unknown")
                    }
                    analysis["flight_conflicts"].append(conflict_info)
        except Exception as e:
            safe_print(f"⚠️  Error parsing meeting times: {e}")
    
    return analysis

def main():
    """Main function to test real calendar integration."""
    safe_print("🚀 CYL's Real Microsoft Calendar Integration - SilverFlow Pattern")
    safe_print("=" * 70)
    
    try:
        # Authenticate
        safe_print("🔐 Starting Microsoft Graph authentication...")
        token_result = acquire_token_interactive(GRAPH_SCOPES)
        access_token = token_result["access_token"]
        
        # Define time range - October 22, 2025 (tomorrow)
        target_date = datetime(2025, 10, 22, 0, 0, 0, tzinfo=timezone.utc)
        start_time = target_date
        end_time = target_date + timedelta(days=1)
        
        safe_print(f"📅 Fetching meetings for {start_time.strftime('%Y-%m-%d')}")
        
        # Fetch calendar events
        events, error = fetch_calendar_events(access_token, start_time, end_time)
        
        if error:
            safe_print(f"❌ Error fetching calendar: {error}")
            return 1
        
        safe_print(f"✅ Successfully retrieved {len(events)} calendar events")
        
        # Analyze events
        analysis = analyze_meeting_conflicts(events)
        
        safe_print("\n📊 CALENDAR ANALYSIS")
        safe_print("-" * 30)
        safe_print(f"Total meetings: {analysis['total_meetings']}")
        safe_print(f"✅ Accepted: {analysis['accepted_meetings']}")
        safe_print(f"❓ Tentative: {analysis['tentative_meetings']}")
        safe_print(f"❌ Declined: {analysis['declined_meetings']}")
        safe_print(f"🎯 As organizer: {analysis['organizer_meetings']}")
        safe_print(f"👥 As attendee: {analysis['attendee_meetings']}")
        
        # Flight conflict analysis
        if analysis['flight_conflicts']:
            safe_print(f"\n✈️  FLIGHT CI005 CONFLICTS ({len(analysis['flight_conflicts'])} found)")
            safe_print("-" * 40)
            for i, conflict in enumerate(analysis['flight_conflicts'], 1):
                start_time_local = datetime.fromisoformat(conflict['start'])
                safe_print(f"{i}. {conflict['subject']}")
                safe_print(f"   Time: {start_time_local.strftime('%H:%M')} UTC")
                safe_print(f"   Status: {conflict['response_status']}")
                safe_print(f"   Organizer: {conflict['organizer']}")
                safe_print()
        else:
            safe_print("\n✅ No conflicts with Flight CI005 (4:25 PM PDT departure)")
        
        # Save results
        output_dir = Path("calendar_analysis")
        output_dir.mkdir(exist_ok=True)
        
        results = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "user_email": "cyl@microsoft.com",
            "date_analyzed": target_date.isoformat(),
            "flight_info": {
                "flight": "CI005",
                "departure_time": "2025-10-22T21:25:00Z",
                "departure_time_pdt": "2025-10-22T14:25:00-07:00"
            },
            "analysis": analysis,
            "events": events
        }
        
        output_file = output_dir / f"calendar_analysis_{target_date.strftime('%Y%m%d')}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        safe_print(f"💾 Results saved to: {output_file}")
        
        return 0
        
    except Exception as e:
        safe_print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())