#!/usr/bin/env python3
"""
Extract 200 Calendar Events
Quick script to extract calendar data using existing authentication
"""

import json
import sys
from datetime import datetime, timedelta, timezone

# Try to use existing Graph API tools
try:
    from tools.microsoft_graph_api import MicrosoftGraphAPI
    
    print("🔐 Initializing Microsoft Graph API...")
    graph_api = MicrosoftGraphAPI()
    
    print("📅 Extracting last 200 calendar events...")
    
    # Get events from last 180 days (6 months)
    start_date = (datetime.now(timezone.utc) - timedelta(days=180)).isoformat()
    end_date = datetime.now(timezone.utc).isoformat()
    
    # Query for calendar events
    query = f"/me/events?$top=200&$orderby=start/dateTime desc&$filter=start/dateTime ge '{start_date}'"
    
    print(f"   Query: {query}")
    events = graph_api.make_request(query)
    
    if events and 'value' in events:
        event_list = events['value']
        print(f"✅ Successfully extracted {len(event_list)} events")
        
        # Save to file
        output_file = 'my_calendar_events_200.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(event_list, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Saved to {output_file}")
        
        # Quick check for Xiaodong Liu
        xiaodong_events = [e for e in event_list if 'Xiaodong' in json.dumps(e)]
        print(f"🔍 Found {len(xiaodong_events)} events with 'Xiaodong'")
        
    else:
        print("❌ Failed to retrieve events")
        sys.exit(1)
        
except ImportError:
    print("❌ Microsoft Graph API tool not found")
    print("💡 Please use automated_calendar_today.py or manual extraction")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
