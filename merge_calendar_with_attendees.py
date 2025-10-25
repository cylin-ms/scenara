#!/usr/bin/env python3
"""
Merge Calendar Data with Attendees (April-October 2025)
Created: 2025-10-26

This script merges three quarterly calendar extractions into a complete dataset:
- April-June 2025: 92 events
- July-September 2025: 125 events  
- October 2025: 50 events
Total: 267 events with attendees field

All extractions include attendees field via SilverFlow --select parameter.
"""

import json
from datetime import datetime

def main():
    print("=" * 80)
    print("MERGE CALENDAR DATA WITH ATTENDEES")
    print("=" * 80)
    
    # Load all three quarterly extractions
    print("\n1. LOADING QUARTERLY EXTRACTIONS...")
    
    with open('calendar_april_june_attendees.json', 'r', encoding='utf-8') as f:
        q2_data = json.load(f)
        q2_events = q2_data.get('events', [])
        print(f"   ✅ April-June 2025: {len(q2_events)} events")
    
    with open('calendar_july_sep_attendees.json', 'r', encoding='utf-8') as f:
        q3_data = json.load(f)
        q3_events = q3_data.get('events', [])
        print(f"   ✅ July-September 2025: {len(q3_events)} events")
    
    with open('calendar_october_with_attendees.json', 'r', encoding='utf-8') as f:
        q4_data = json.load(f)
        q4_events = q4_data.get('events', [])
        print(f"   ✅ October 2025: {len(q4_events)} events")
    
    # Merge all events
    print("\n2. MERGING EVENTS...")
    all_events = q2_events + q3_events + q4_events
    print(f"   ✅ Total events: {len(all_events)}")
    
    # Verify attendees field present
    print("\n3. VERIFYING ATTENDEES FIELD...")
    events_with_attendees = sum(1 for e in all_events if 'attendees' in e)
    print(f"   ✅ Events with attendees: {events_with_attendees}/{len(all_events)}")
    
    if events_with_attendees < len(all_events):
        print(f"   ⚠️  WARNING: {len(all_events) - events_with_attendees} events missing attendees field!")
    
    # Get date range
    print("\n4. DATE RANGE ANALYSIS...")
    dates = []
    for event in all_events:
        if 'start' in event and 'dateTime' in event['start']:
            date_str = event['start']['dateTime'][:10]
            dates.append(date_str)
    
    if dates:
        print(f"   ✅ First meeting: {min(dates)}")
        print(f"   ✅ Last meeting: {max(dates)}")
    
    # Sample attendees verification
    print("\n5. SAMPLE ATTENDEES VERIFICATION...")
    sample_count = 0
    for event in all_events:
        if 'attendees' in event and len(event.get('attendees', [])) > 0:
            subject = event.get('subject', 'N/A')
            attendee_count = len(event['attendees'])
            print(f"   ✅ '{subject}': {attendee_count} attendees")
            sample_count += 1
            if sample_count >= 3:
                break
    
    # Save merged dataset
    print("\n6. SAVING COMPLETE DATASET...")
    merged_data = {
        'metadata': {
            'total_events': len(all_events),
            'date_range': {
                'start': min(dates) if dates else 'N/A',
                'end': max(dates) if dates else 'N/A'
            },
            'sources': {
                'april_june': len(q2_events),
                'july_september': len(q3_events),
                'october': len(q4_events)
            },
            'attendees_included': True,
            'extraction_method': 'SilverFlow graph_get_meetings.py with --select attendees',
            'created': datetime.now().isoformat()
        },
        'events': all_events
    }
    
    output_file = 'my_calendar_events_complete_attendees.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(merged_data, f, indent=2, ensure_ascii=False)
    
    print(f"   ✅ Saved to: {output_file}")
    print(f"   ✅ File size: {len(json.dumps(merged_data, ensure_ascii=False)) / 1024:.1f} KB")
    
    # Summary
    print("\n" + "=" * 80)
    print("✅ MERGE COMPLETE!")
    print("=" * 80)
    print(f"Total Events: {len(all_events)}")
    print(f"Date Range: {min(dates) if dates else 'N/A'} to {max(dates) if dates else 'N/A'}")
    print(f"Attendees Field: {'✅ Present' if events_with_attendees == len(all_events) else '⚠️ Partial'}")
    print(f"Output File: {output_file}")
    print("=" * 80)

if __name__ == '__main__':
    main()
