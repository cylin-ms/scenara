#!/usr/bin/env python3
"""
Identify Top 7 Meeting Types from Calendar Data

Analyzes calendar meetings from the past 6 months and classifies them into the top 7
high-complexity meeting types for post-training synthetic data generation.

Top 7 Meeting Types:
1. Quarterly Business Review (QBR)
2. Board of Directors Meeting
3. Executive Sales Presentation
4. Product Launch Go/No-Go Decision
5. Annual SOX 404 Compliance Review
6. Quarterly Earnings Call
7. M&A Deal Approval (Board)

Usage:
    python tools/identify_top7_meetings.py
    python tools/identify_top7_meetings.py --input my_calendar_events_complete_attendees.json
    python tools/identify_top7_meetings.py --output data/top7_meetings.json
    python tools/identify_top7_meetings.py --dry-run  # Preview without LLM calls
"""

import argparse
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from tools.llm_api import LLMAPIClient
except ImportError:
    print("ERROR: Could not import LLMAPIClient")
    sys.exit(1)


# Top 7 Meeting Type Definitions
TOP_7_MEETING_TYPES = {
    "quarterly_business_review": {
        "name": "Quarterly Business Review (QBR)",
        "keywords": ["qbr", "quarterly business review", "quarterly review", "q1", "q2", "q3", "q4", "business review"],
        "indicators": ["performance", "metrics", "kpi", "revenue", "targets", "strategic", "division"],
        "typical_attendees": 15,  # 15+ attendees
        "typical_duration": 120,  # 2+ hours
    },
    "board_of_directors": {
        "name": "Board of Directors Meeting",
        "keywords": ["board meeting", "board of directors", "board session", "directors meeting"],
        "indicators": ["governance", "fiduciary", "board", "directors", "vote", "resolution"],
        "typical_attendees": 8,  # 8+ attendees
        "typical_duration": 120,  # 2+ hours
    },
    "executive_sales_presentation": {
        "name": "Executive Sales Presentation",
        "keywords": ["sales presentation", "customer presentation", "executive brief", "customer exec"],
        "indicators": ["cio", "cfo", "ceo", "c-level", "executive", "customer", "prospect", "roi", "proposal"],
        "typical_attendees": 4,  # 4+ attendees
        "typical_duration": 60,  # 1+ hours
    },
    "product_launch": {
        "name": "Product Launch Go/No-Go Decision",
        "keywords": ["product launch", "launch decision", "go/no-go", "go-no-go", "launch readiness"],
        "indicators": ["launch", "readiness", "gtm", "go-to-market", "release", "shipping"],
        "typical_attendees": 10,  # 10+ attendees
        "typical_duration": 90,  # 1.5+ hours
    },
    "compliance_review": {
        "name": "Annual SOX 404 Compliance Review",
        "keywords": ["sox", "compliance review", "audit", "sox 404", "internal controls"],
        "indicators": ["compliance", "audit", "controls", "sox", "regulatory", "governance"],
        "typical_attendees": 6,  # 6+ attendees
        "typical_duration": 120,  # 2+ hours
    },
    "earnings_call": {
        "name": "Quarterly Earnings Call",
        "keywords": ["earnings call", "earnings", "investor relations", "ir call", "earnings announcement"],
        "indicators": ["earnings", "investor", "analysts", "guidance", "financial results", "eps"],
        "typical_attendees": 50,  # Large audience
        "typical_duration": 60,  # 1+ hours
    },
    "ma_deal_approval": {
        "name": "M&A Deal Approval (Board)",
        "keywords": ["m&a", "merger", "acquisition", "deal approval", "transaction"],
        "indicators": ["acquisition", "merger", "due diligence", "valuation", "deal", "transaction"],
        "typical_attendees": 12,  # 12+ attendees
        "typical_duration": 180,  # 3+ hours
    }
}


def load_calendar_data(input_file: Path) -> Dict[str, Any]:
    """Load calendar events from JSON file."""
    print(f"\n📅 Loading calendar data from: {input_file}")
    
    if not input_file.exists():
        print(f"❌ Error: File not found: {input_file}")
        sys.exit(1)
    
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    meetings = data.get('meetings', data.get('value', []))
    print(f"✅ Loaded {len(meetings)} meetings")
    
    return {'meetings': meetings, 'metadata': data.get('metadata', {})}


def filter_recent_meetings(meetings: List[Dict], months: int = 6) -> List[Dict]:
    """Filter meetings from the past N months."""
    cutoff_date = datetime.now() - timedelta(days=months * 30)
    
    recent_meetings = []
    for meeting in meetings:
        start_time_str = meeting.get('start', {}).get('dateTime')
        if not start_time_str:
            continue
        
        try:
            # Parse ISO 8601 datetime
            start_time = datetime.fromisoformat(start_time_str.replace('Z', '+00:00'))
            if start_time.replace(tzinfo=None) >= cutoff_date:
                recent_meetings.append(meeting)
        except Exception as e:
            # Skip meetings with invalid dates
            continue
    
    print(f"📊 Filtered to {len(recent_meetings)} meetings from past {months} months")
    return recent_meetings


def calculate_meeting_duration(meeting: Dict) -> int:
    """Calculate meeting duration in minutes."""
    try:
        start_str = meeting.get('start', {}).get('dateTime')
        end_str = meeting.get('end', {}).get('dateTime')
        
        if not start_str or not end_str:
            return 0
        
        start = datetime.fromisoformat(start_str.replace('Z', '+00:00'))
        end = datetime.fromisoformat(end_str.replace('Z', '+00:00'))
        
        duration = (end - start).total_seconds() / 60
        return int(duration)
    except Exception:
        return 0


def get_attendee_count(meeting: Dict) -> int:
    """Get number of attendees (excluding resources)."""
    attendees = meeting.get('attendees', [])
    # Filter out conference rooms (type="resource")
    real_attendees = [a for a in attendees if a.get('type') != 'resource']
    return len(real_attendees)


def keyword_match(meeting: Dict, scenario: Dict) -> float:
    """
    Calculate keyword match score (0.0 to 1.0).
    
    Returns higher score if meeting subject/body contains scenario keywords.
    """
    subject = meeting.get('subject', '').lower()
    body = meeting.get('bodyPreview', '').lower()
    text = f"{subject} {body}"
    
    keywords = scenario['keywords']
    indicators = scenario['indicators']
    
    # Count keyword matches
    keyword_matches = sum(1 for kw in keywords if kw in text)
    indicator_matches = sum(1 for ind in indicators if ind in text)
    
    # Calculate score
    keyword_score = min(keyword_matches / len(keywords), 1.0)
    indicator_score = min(indicator_matches / (len(indicators) * 0.5), 1.0)  # Need 50% of indicators
    
    # Weighted average
    score = (keyword_score * 0.7) + (indicator_score * 0.3)
    
    return score


def heuristic_match(meeting: Dict, scenario: Dict) -> float:
    """
    Calculate heuristic match score (0.0 to 1.0).
    
    Checks attendee count and duration against typical values.
    """
    duration = calculate_meeting_duration(meeting)
    attendee_count = get_attendee_count(meeting)
    
    # Duration score (within 50% of typical)
    typical_duration = scenario['typical_duration']
    duration_diff = abs(duration - typical_duration) / typical_duration
    duration_score = max(0, 1.0 - duration_diff)
    
    # Attendee score (within 50% of typical)
    typical_attendees = scenario['typical_attendees']
    attendee_diff = abs(attendee_count - typical_attendees) / typical_attendees
    attendee_score = max(0, 1.0 - attendee_diff)
    
    # Weighted average
    score = (duration_score * 0.4) + (attendee_score * 0.6)
    
    return score


def pre_screen_meetings(meetings: List[Dict]) -> List[Dict]:
    """
    Pre-screen meetings using keyword and heuristic matching.
    
    Returns meetings that have ANY potential match (score > 0.3) with ANY scenario.
    """
    candidates = []
    
    print(f"\n🔍 Pre-screening {len(meetings)} meetings...")
    
    for meeting in meetings:
        subject = meeting.get('subject', 'No Subject')
        max_score = 0.0
        best_match = None
        
        for scenario_key, scenario in TOP_7_MEETING_TYPES.items():
            keyword_score = keyword_match(meeting, scenario)
            heuristic_score = heuristic_match(meeting, scenario)
            
            # Combined score
            combined_score = (keyword_score * 0.6) + (heuristic_score * 0.4)
            
            if combined_score > max_score:
                max_score = combined_score
                best_match = scenario_key
        
        # Keep meetings with score > 0.3
        if max_score > 0.3:
            meeting['_prescreening'] = {
                'score': max_score,
                'best_match': best_match,
                'scenario_name': TOP_7_MEETING_TYPES[best_match]['name']
            }
            candidates.append(meeting)
    
    print(f"✅ Pre-screened to {len(candidates)} candidates")
    return candidates


def classify_with_llm(meeting: Dict, llm_client: LLMAPIClient) -> Optional[Dict]:
    """
    Use LLM to classify meeting into one of the top 7 types.
    
    Returns classification result or None if no match.
    """
    subject = meeting.get('subject', 'No Subject')
    body = meeting.get('bodyPreview', '')
    duration = calculate_meeting_duration(meeting)
    attendee_count = get_attendee_count(meeting)
    
    # Get first few attendees for context
    attendees = meeting.get('attendees', [])
    attendee_names = [a.get('emailAddress', {}).get('name', 'Unknown') for a in attendees[:5]]
    
    prompt = f"""Analyze this meeting and determine if it matches one of these 7 high-complexity meeting types:

1. Quarterly Business Review (QBR) - Board-level strategic performance review
2. Board of Directors Meeting - Governance and fiduciary oversight
3. Executive Sales Presentation - C-level customer presentation
4. Product Launch Go/No-Go Decision - Critical launch readiness decision
5. Annual SOX 404 Compliance Review - Regulatory compliance audit
6. Quarterly Earnings Call - Public investor relations event
7. M&A Deal Approval (Board) - Major acquisition/merger decision

Meeting Details:
- Subject: {subject}
- Duration: {duration} minutes
- Attendees: {attendee_count} people
- Sample attendees: {', '.join(attendee_names[:3])}
- Description: {body[:200]}

Return JSON with:
{{
    "matches": true/false,
    "meeting_type": "one of the 7 types or null",
    "confidence": 0.0-1.0,
    "reasoning": "brief explanation"
}}

If this meeting does NOT match any of the 7 high-complexity types, return {{"matches": false}}.
"""

    try:
        response = llm_client.query_llm(prompt, provider="ollama", model="gpt-oss:20b")
        
        # Parse JSON response
        response_clean = response.strip()
        if response_clean.startswith("```json"):
            response_clean = response_clean.split("```json")[1].split("```")[0].strip()
        elif response_clean.startswith("```"):
            response_clean = response_clean.split("```")[1].split("```")[0].strip()
        
        result = json.loads(response_clean)
        return result
    
    except Exception as e:
        print(f"⚠️  LLM classification error for '{subject}': {e}")
        return None


def batch_classify_meetings(candidates: List[Dict], llm_client: LLMAPIClient, dry_run: bool = False) -> List[Dict]:
    """
    Classify candidate meetings using LLM.
    
    Returns list of meetings that match one of the top 7 types.
    """
    print(f"\n🤖 Classifying {len(candidates)} candidates with Ollama LLM...")
    
    if dry_run:
        print("   (DRY RUN: Skipping LLM calls)")
        return []
    
    matched_meetings = []
    
    for i, meeting in enumerate(candidates, 1):
        subject = meeting.get('subject', 'No Subject')
        print(f"   [{i}/{len(candidates)}] {subject[:60]}...")
        
        classification = classify_with_llm(meeting, llm_client)
        
        if classification and classification.get('matches'):
            meeting['_llm_classification'] = classification
            matched_meetings.append(meeting)
            print(f"      ✅ MATCH: {classification.get('meeting_type')} (confidence: {classification.get('confidence'):.2f})")
        else:
            print(f"      ⚠️  No match")
    
    print(f"\n✅ Found {len(matched_meetings)} meetings matching top 7 types")
    return matched_meetings


def generate_statistics(matched_meetings: List[Dict]) -> Dict:
    """Generate statistics for matched meetings."""
    stats = {
        'total_matches': len(matched_meetings),
        'by_type': {},
        'by_confidence': {
            'high': 0,  # > 0.8
            'medium': 0,  # 0.5-0.8
            'low': 0  # < 0.5
        },
        'average_duration': 0,
        'average_attendees': 0
    }
    
    if not matched_meetings:
        return stats
    
    # Count by type
    for meeting in matched_meetings:
        meeting_type = meeting.get('_llm_classification', {}).get('meeting_type', 'Unknown')
        stats['by_type'][meeting_type] = stats['by_type'].get(meeting_type, 0) + 1
        
        confidence = meeting.get('_llm_classification', {}).get('confidence', 0)
        if confidence > 0.8:
            stats['by_confidence']['high'] += 1
        elif confidence > 0.5:
            stats['by_confidence']['medium'] += 1
        else:
            stats['by_confidence']['low'] += 1
    
    # Calculate averages
    durations = [calculate_meeting_duration(m) for m in matched_meetings]
    attendees = [get_attendee_count(m) for m in matched_meetings]
    
    stats['average_duration'] = sum(durations) / len(durations) if durations else 0
    stats['average_attendees'] = sum(attendees) / len(attendees) if attendees else 0
    
    return stats


def save_results(matched_meetings: List[Dict], stats: Dict, output_file: Path):
    """Save matched meetings and statistics to JSON file."""
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    output_data = {
        'metadata': {
            'generated_at': datetime.now().isoformat(),
            'total_matches': len(matched_meetings),
            'statistics': stats
        },
        'meetings': matched_meetings
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2)
    
    print(f"\n💾 Results saved to: {output_file}")


def print_summary(stats: Dict):
    """Print summary statistics."""
    print(f"\n{'='*80}")
    print(f"SUMMARY STATISTICS")
    print(f"{'='*80}")
    print(f"Total matches: {stats['total_matches']}")
    
    print(f"\n📊 By Meeting Type:")
    for meeting_type, count in sorted(stats['by_type'].items(), key=lambda x: x[1], reverse=True):
        print(f"   {meeting_type}: {count}")
    
    print(f"\n🎯 By Confidence:")
    print(f"   High (>0.8): {stats['by_confidence']['high']}")
    print(f"   Medium (0.5-0.8): {stats['by_confidence']['medium']}")
    print(f"   Low (<0.5): {stats['by_confidence']['low']}")
    
    print(f"\n📈 Averages:")
    print(f"   Duration: {stats['average_duration']:.0f} minutes")
    print(f"   Attendees: {stats['average_attendees']:.0f} people")
    print(f"{'='*80}\n")


def main():
    parser = argparse.ArgumentParser(
        description='Identify top 7 meeting types from calendar data'
    )
    parser.add_argument(
        '--input',
        type=Path,
        default=Path('my_calendar_events_complete_attendees.json'),
        help='Input calendar JSON file'
    )
    parser.add_argument(
        '--output',
        type=Path,
        default=Path('data/top7_meetings.json'),
        help='Output JSON file'
    )
    parser.add_argument(
        '--months',
        type=int,
        default=6,
        help='Number of months to look back (default: 6)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview candidates without LLM classification'
    )
    
    args = parser.parse_args()
    
    print(f"\n{'='*80}")
    print(f"TOP 7 MEETING TYPE IDENTIFICATION")
    print(f"{'='*80}")
    
    # Load calendar data
    calendar_data = load_calendar_data(args.input)
    meetings = calendar_data['meetings']
    
    # Filter recent meetings
    recent_meetings = filter_recent_meetings(meetings, args.months)
    
    if not recent_meetings:
        print("❌ No recent meetings found")
        return
    
    # Pre-screen meetings
    candidates = pre_screen_meetings(recent_meetings)
    
    if not candidates:
        print("❌ No candidates found matching top 7 types")
        return
    
    # Initialize LLM client
    if not args.dry_run:
        llm_client = LLMAPIClient()
    else:
        llm_client = None
    
    # Classify with LLM
    matched_meetings = batch_classify_meetings(candidates, llm_client, args.dry_run)
    
    if not matched_meetings and not args.dry_run:
        print("❌ No meetings matched the top 7 types")
        return
    
    # Generate statistics
    stats = generate_statistics(matched_meetings)
    
    # Print summary
    if not args.dry_run:
        print_summary(stats)
    
    # Save results
    if not args.dry_run:
        save_results(matched_meetings, stats, args.output)
        print(f"✅ Complete! Found {len(matched_meetings)} meetings matching top 7 types")
    else:
        print(f"\n✅ DRY RUN complete. Found {len(candidates)} candidates for LLM classification")
        print(f"   Run without --dry-run to perform actual classification")


if __name__ == '__main__':
    main()
