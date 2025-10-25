"""
Merge Multiple Calendar Extractions
Combines April-June, July-September, and October calendar data into complete dataset
"""

import json
from datetime import datetime

def load_calendar_file(filepath):
    """Load calendar events from file, handling both formats"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Handle SilverFlow format (dict with 'events' key)
        if isinstance(data, dict) and 'events' in data:
            return data['events']
        # Handle plain array format
        elif isinstance(data, list):
            return data
        else:
            print(f"⚠️  Unknown format in {filepath}")
            return []
    except FileNotFoundError:
        print(f"❌ File not found: {filepath}")
        return []
    except Exception as e:
        print(f"❌ Error loading {filepath}: {e}")
        return []

def main():
    print("=" * 80)
    print("CALENDAR MERGE UTILITY - Complete 7-Month Dataset")
    print("=" * 80)
    print()
    
    # Load all three quarterly extractions
    print("📂 Loading calendar files...")
    
    q2_events = load_calendar_file('calendar_april_june.json')
    print(f"   ✅ April-June 2025 (Q2): {len(q2_events)} events")
    
    q3_events = load_calendar_file('calendar_july_sep.json')
    print(f"   ✅ July-September 2025 (Q3): {len(q3_events)} events")
    
    q4_events = load_calendar_file('calendar_october.json')
    print(f"   ✅ October 2025 (Q4): {len(q4_events)} events")
    
    print()
    
    # Merge all events
    all_events = q2_events + q3_events + q4_events
    total_events = len(all_events)
    
    if total_events == 0:
        print("❌ No events found to merge!")
        return
    
    print(f"🔗 Merging {total_events} total events...")
    
    # Extract date range
    dates = []
    for event in all_events:
        if 'start' in event and 'dateTime' in event['start']:
            try:
                date_str = event['start']['dateTime']
                # Parse ISO 8601 datetime
                date_obj = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                dates.append(date_obj)
            except:
                pass
    
    if dates:
        earliest = min(dates)
        latest = max(dates)
        print(f"   📅 Date Range: {earliest.strftime('%Y-%m-%d')} to {latest.strftime('%Y-%m-%d')}")
        days_span = (latest - earliest).days
        print(f"   ⏱️  Time Span: {days_span} days")
    
    # Save complete dataset
    output_file = 'my_calendar_events_complete.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({'events': all_events}, f, indent=2, ensure_ascii=False)
    
    print()
    print(f"✅ Complete dataset saved to: {output_file}")
    print(f"   📊 Total events: {total_events}")
    print(f"   💾 File size: {len(json.dumps(all_events)) / 1024:.1f} KB")
    print()
    
    # Summary by quarter
    print("📈 Summary by Quarter:")
    print(f"   Q2 (Apr-Jun): {len(q2_events):>3} events ({len(q2_events)/total_events*100:>5.1f}%)")
    print(f"   Q3 (Jul-Sep): {len(q3_events):>3} events ({len(q3_events)/total_events*100:>5.1f}%)")
    print(f"   Q4 (Oct):     {len(q4_events):>3} events ({len(q4_events)/total_events*100:>5.1f}%)")
    print()
    
    print("=" * 80)
    print("✅ MERGE COMPLETE - Ready for dormant detection analysis")
    print("=" * 80)

if __name__ == "__main__":
    main()
