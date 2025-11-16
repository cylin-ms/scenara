#!/usr/bin/env python3
"""
Identify Top 7 Meeting Types from Real Calendar Data

Scans my_calendar_events_complete_attendees.json (267 events, April-October 2025)
to find real meetings matching the 7 top meeting type scenarios.

Top 7 Meeting Types:
1. Quarterly Business Review (QBR)
2. Board of Directors Meeting
3. Executive Sales Presentation
4. Product Launch Go/No-Go Decision
5. Annual SOX 404 Compliance Review
6. Quarterly Earnings Call
7. M&A Deal Approval (Board)
"""

import json
import re
from datetime import datetime
from collections import defaultdict
from typing import Dict, List, Any

# Define patterns for each of the 7 top meeting types
MEETING_TYPE_PATTERNS = {
    "quarterly_business_review": {
        "name": "Quarterly Business Review (QBR)",
        "keywords": [
            r'\bqbr\b',
            r'\bquarterly\s+business\s+review\b',
            r'\bquarterly\s+review\b',
            r'\bq[1-4]\s+review\b',
            r'\bquarter\s+review\b',
            r'\bbusiness\s+review\b.*\bquarter',
        ],
        "attendee_min": 8,  # Typically large cross-functional meetings
        "duration_min": 60,  # At least 1 hour
    },
    
    "board_of_directors": {
        "name": "Board of Directors Meeting",
        "keywords": [
            r'\bboard\s+meeting\b',
            r'\bboard\s+of\s+directors\b',
            r'\bboard\s+review\b',
            r'\bexecutive\s+board\b',
            r'\bgoverning\s+board\b',
            r'\badvisory\s+board\b',
        ],
        "attendee_min": 5,  # Board meetings typically have senior leaders
        "duration_min": 90,
    },
    
    "executive_sales_presentation": {
        "name": "Executive Sales Presentation",
        "keywords": [
            r'\bexecutive\s+briefing\b',
            r'\bexecutive\s+presentation\b',
            r'\bc-level\s+presentation\b',
            r'\bcustomer\s+executive\s+review\b',
            r'\bexecutive\s+demo\b',
            r'\bsales\s+presentation\b.*\bexecutive',
            r'\bexecutive\s+overview\b',
        ],
        "attendee_min": 3,  # Smaller executive meetings
        "duration_min": 45,
    },
    
    "product_launch": {
        "name": "Product Launch Go/No-Go Decision",
        "keywords": [
            r'\bproduct\s+launch\b',
            r'\bgo\s*/\s*no-?go\b',
            r'\blaunch\s+decision\b',
            r'\blaunch\s+readiness\b',
            r'\brelease\s+decision\b',
            r'\bga\s+decision\b',
            r'\bship\s+decision\b',
        ],
        "attendee_min": 6,  # Cross-functional launch teams
        "duration_min": 60,
    },
    
    "compliance_review": {
        "name": "Annual SOX 404 Compliance Review",
        "keywords": [
            r'\bsox\b',
            r'\bsox\s+404\b',
            r'\bcompliance\s+review\b',
            r'\baudit\s+review\b',
            r'\binternal\s+controls\b',
            r'\bexternal\s+audit\b',
            r'\bfinancial\s+audit\b',
        ],
        "attendee_min": 4,  # Compliance + Finance + IT + Auditors
        "duration_min": 90,
    },
    
    "earnings_call": {
        "name": "Quarterly Earnings Call",
        "keywords": [
            r'\bearnings\s+call\b',
            r'\bearnings\s+release\b',
            r'\bquarterly\s+earnings\b',
            r'\binvestor\s+relations\b',
            r'\banalyst\s+call\b',
            r'\bfinancial\s+results\b.*\bcall',
        ],
        "attendee_min": 3,  # CEO, CFO, IR team (large external audience)
        "duration_min": 60,
    },
    
    "ma_deal_approval": {
        "name": "M&A Deal Approval (Board)",
        "keywords": [
            r'\bm&a\b',
            r'\bmerger\b',
            r'\bacquisition\b',
            r'\bdeal\s+approval\b',
            r'\btransaction\s+review\b',
            r'\bdue\s+diligence\b',
            r'\binvestment\s+decision\b',
        ],
        "attendee_min": 6,  # Board, executives, advisors
        "duration_min": 120,  # Typically long meetings
    },
}


def load_calendar_data(filepath: str = "my_calendar_events_complete_attendees.json") -> Dict:
    """Load calendar data from JSON file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def match_meeting_type(event: Dict[str, Any]) -> List[str]:
    """
    Match an event against the 7 top meeting type patterns.
    Returns list of matching types (can match multiple).
    """
    subject = event.get('subject', '').lower()
    body_preview = event.get('bodyPreview', '').lower()
    combined_text = f"{subject} {body_preview}"
    
    # Get attendee count and duration
    attendees = event.get('attendees', [])
    attendee_count = len(attendees)
    
    start_str = event.get('start', {}).get('dateTime', '')
    end_str = event.get('end', {}).get('dateTime', '')
    duration_minutes = 0
    
    if start_str and end_str:
        try:
            start_dt = datetime.fromisoformat(start_str.replace('Z', '+00:00'))
            end_dt = datetime.fromisoformat(end_str.replace('Z', '+00:00'))
            duration_minutes = int((end_dt - start_dt).total_seconds() / 60)
        except:
            pass
    
    # Check each meeting type pattern
    matches = []
    
    for meeting_key, pattern in MEETING_TYPE_PATTERNS.items():
        # Check keyword match
        keyword_match = False
        for keyword_regex in pattern['keywords']:
            if re.search(keyword_regex, combined_text, re.IGNORECASE):
                keyword_match = True
                break
        
        if not keyword_match:
            continue
        
        # Check attendee count threshold
        if attendee_count < pattern['attendee_min']:
            continue
        
        # Check duration threshold
        if duration_minutes < pattern['duration_min']:
            continue
        
        matches.append(meeting_key)
    
    return matches


def analyze_calendar_for_top7(calendar_data: Dict) -> Dict:
    """
    Analyze calendar data to identify meetings matching the top 7 types.
    Returns structured results with statistics and matched events.
    """
    events = calendar_data.get('events', [])
    metadata = calendar_data.get('metadata', {})
    
    print(f"\n{'='*80}")
    print(f"IDENTIFYING TOP 7 MEETING TYPES FROM REAL CALENDAR DATA")
    print(f"{'='*80}")
    print(f"Dataset: {metadata.get('total_events', len(events))} events")
    print(f"Date Range: {metadata.get('date_range', {}).get('start')} to {metadata.get('date_range', {}).get('end')}")
    print(f"{'='*80}\n")
    
    # Track matches by type
    matches_by_type = defaultdict(list)
    events_with_matches = []
    
    # Scan all events
    for event in events:
        matched_types = match_meeting_type(event)
        
        if matched_types:
            event_with_matches = {
                'event': event,
                'matched_types': matched_types
            }
            events_with_matches.append(event_with_matches)
            
            for meeting_type in matched_types:
                matches_by_type[meeting_type].append(event)
    
    # Print summary statistics
    print(f"📊 SUMMARY STATISTICS")
    print(f"{'─'*80}")
    print(f"Total events scanned: {len(events)}")
    print(f"Events with matches: {len(events_with_matches)}")
    print(f"Match rate: {len(events_with_matches)/len(events)*100:.1f}%\n")
    
    # Print matches by type
    print(f"📋 MATCHES BY TYPE")
    print(f"{'─'*80}")
    
    for meeting_key in MEETING_TYPE_PATTERNS.keys():
        pattern = MEETING_TYPE_PATTERNS[meeting_key]
        count = len(matches_by_type[meeting_key])
        print(f"{pattern['name']}: {count} matches")
    
    print(f"\n{'='*80}\n")
    
    # Print detailed matches
    for meeting_key, matched_events in matches_by_type.items():
        if not matched_events:
            continue
        
        pattern = MEETING_TYPE_PATTERNS[meeting_key]
        print(f"\n{'='*80}")
        print(f"📌 {pattern['name']} ({len(matched_events)} matches)")
        print(f"{'='*80}\n")
        
        for i, event in enumerate(matched_events, 1):
            subject = event.get('subject', 'No Subject')
            start = event.get('start', {}).get('dateTime', 'Unknown')
            attendee_count = len(event.get('attendees', []))
            
            # Calculate duration
            start_str = event.get('start', {}).get('dateTime', '')
            end_str = event.get('end', {}).get('dateTime', '')
            duration_minutes = 0
            if start_str and end_str:
                try:
                    start_dt = datetime.fromisoformat(start_str.replace('Z', '+00:00'))
                    end_dt = datetime.fromisoformat(end_str.replace('Z', '+00:00'))
                    duration_minutes = int((end_dt - start_dt).total_seconds() / 60)
                except:
                    pass
            
            print(f"{i}. {subject}")
            print(f"   📅 Date: {start[:10]}")
            print(f"   ⏱️  Duration: {duration_minutes} minutes")
            print(f"   👥 Attendees: {attendee_count}")
            
            # Show key attendees (first 3)
            attendees = event.get('attendees', [])
            if attendees:
                key_attendees = [a.get('emailAddress', {}).get('name', 'Unknown') for a in attendees[:3]]
                print(f"   🎯 Key Attendees: {', '.join(key_attendees)}")
                if len(attendees) > 3:
                    print(f"      ... and {len(attendees) - 3} more")
            print()
    
    # Return structured results
    return {
        'total_events': len(events),
        'matched_events': len(events_with_matches),
        'matches_by_type': {
            meeting_key: {
                'name': MEETING_TYPE_PATTERNS[meeting_key]['name'],
                'count': len(matched_events),
                'events': matched_events
            }
            for meeting_key, matched_events in matches_by_type.items()
        },
        'metadata': metadata
    }


def export_matches(results: Dict, output_file: str = "top7_meeting_matches.json"):
    """Export matched meetings to JSON file"""
    
    # Prepare export data (without full event objects to keep file size manageable)
    export_data = {
        'generated': datetime.now().isoformat(),
        'source_dataset': 'my_calendar_events_complete_attendees.json',
        'summary': {
            'total_events': results['total_events'],
            'matched_events': results['matched_events'],
            'match_rate': f"{results['matched_events']/results['total_events']*100:.1f}%"
        },
        'matches_by_type': {}
    }
    
    for meeting_key, match_data in results['matches_by_type'].items():
        export_data['matches_by_type'][meeting_key] = {
            'name': match_data['name'],
            'count': match_data['count'],
            'events': [
                {
                    'subject': event.get('subject'),
                    'start': event.get('start', {}).get('dateTime'),
                    'end': event.get('end', {}).get('dateTime'),
                    'attendee_count': len(event.get('attendees', [])),
                    'organizer': event.get('organizer', {}).get('emailAddress', {}).get('name'),
                    'id': event.get('id')
                }
                for event in match_data['events']
            ]
        }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(export_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Exported matches to: {output_file}")


def main():
    """Main execution"""
    # Load calendar data
    calendar_data = load_calendar_data()
    
    # Analyze for top 7 meeting types
    results = analyze_calendar_for_top7(calendar_data)
    
    # Export results
    export_matches(results)
    
    print(f"\n{'='*80}")
    print(f"✅ ANALYSIS COMPLETE")
    print(f"{'='*80}")
    print(f"Next steps:")
    print(f"1. Review matched meetings in top7_meeting_matches.json")
    print(f"2. Validate matches against scenario definitions")
    print(f"3. Use matched meetings as seed data for synthetic generation")
    print(f"4. Create training/evaluation datasets")
    print(f"{'='*80}\n")


if __name__ == "__main__":
    main()
