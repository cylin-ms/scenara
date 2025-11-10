#!/usr/bin/env python3
"""
Schema Alignment Validator

Validates that synthetic training data matches Microsoft Graph API calendar format
from real meeting extraction data (my_calendar_events_complete_attendees.json).

Usage:
    python tools/validate_schema_alignment.py --synthetic data/training/tier1_combined.jsonl
    python tools/validate_schema_alignment.py --real my_calendar_events_complete_attendees.json --synthetic data/training/tier1_combined.jsonl
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Set


# Required Microsoft Graph API fields (from SilverFlow/data/graph_get_meetings.py)
REQUIRED_FIELDS = {
    'id',
    'subject',
    'start',
    'end',
    'organizer',
    'attendees'
}

# Optional standard fields
OPTIONAL_FIELDS = {
    'bodyPreview',
    'showAs',
    'type',
    'responseStatus',
    'seriesMasterId',
    'webLink'
}

# Training-specific fields (added to Graph API schema)
TRAINING_FIELDS = {
    'importance_label',
    'prep_needed',
    'prep_time_minutes',
    'reasoning',
    'persona_id',
    'generation_timestamp'
}


def validate_meeting_schema(meeting: Dict[str, Any], is_synthetic: bool = False) -> List[str]:
    """
    Validate meeting follows Microsoft Graph API schema.
    
    Args:
        meeting: Meeting object to validate
        is_synthetic: Whether this is synthetic training data (has extra fields)
        
    Returns:
        List of validation errors (empty if valid)
    """
    errors = []
    
    # Check required fields
    for field in REQUIRED_FIELDS:
        if field not in meeting:
            errors.append(f"Missing required field: {field}")
    
    # Validate start/end structure
    if 'start' in meeting:
        if not isinstance(meeting['start'], dict):
            errors.append("Field 'start' must be object with 'dateTime' and 'timeZone'")
        elif 'dateTime' not in meeting['start'] or 'timeZone' not in meeting['start']:
            errors.append("Field 'start' missing 'dateTime' or 'timeZone'")
    
    if 'end' in meeting:
        if not isinstance(meeting['end'], dict):
            errors.append("Field 'end' must be object with 'dateTime' and 'timeZone'")
        elif 'dateTime' not in meeting['end'] or 'timeZone' not in meeting['end']:
            errors.append("Field 'end' missing 'dateTime' or 'timeZone'")
    
    # Validate organizer structure
    if 'organizer' in meeting:
        if not isinstance(meeting['organizer'], dict):
            errors.append("Field 'organizer' must be object")
        elif 'emailAddress' not in meeting['organizer']:
            errors.append("Field 'organizer' missing 'emailAddress'")
        else:
            email = meeting['organizer']['emailAddress']
            if 'name' not in email or 'address' not in email:
                errors.append("Organizer emailAddress missing 'name' or 'address'")
    
    # Validate attendees structure
    if 'attendees' in meeting:
        if not isinstance(meeting['attendees'], list):
            errors.append("Field 'attendees' must be array")
        else:
            for i, attendee in enumerate(meeting['attendees']):
                if not isinstance(attendee, dict):
                    errors.append(f"Attendee {i} must be object")
                    continue
                
                if 'type' not in attendee:
                    errors.append(f"Attendee {i} missing 'type' field")
                elif attendee['type'] not in ['required', 'optional', 'resource']:
                    errors.append(f"Attendee {i} has invalid type: {attendee['type']}")
                
                if 'emailAddress' not in attendee:
                    errors.append(f"Attendee {i} missing 'emailAddress'")
                else:
                    email = attendee['emailAddress']
                    if 'name' not in email or 'address' not in email:
                        errors.append(f"Attendee {i} emailAddress missing 'name' or 'address'")
    
    # If synthetic, check training fields
    if is_synthetic:
        for field in TRAINING_FIELDS:
            if field not in meeting:
                errors.append(f"Missing training field: {field}")
        
        # Validate training field types
        if 'importance_label' in meeting:
            if meeting['importance_label'] not in ['critical', 'high', 'medium', 'low']:
                errors.append(f"Invalid importance_label: {meeting['importance_label']}")
        
        if 'prep_needed' in meeting:
            if not isinstance(meeting['prep_needed'], bool):
                errors.append(f"Field 'prep_needed' must be boolean, got {type(meeting['prep_needed'])}")
        
        if 'prep_time_minutes' in meeting:
            if not isinstance(meeting['prep_time_minutes'], (int, float)):
                errors.append(f"Field 'prep_time_minutes' must be number, got {type(meeting['prep_time_minutes'])}")
    
    return errors


def load_real_meetings(json_file: Path) -> List[Dict[str, Any]]:
    """Load real meetings from my_calendar_events_complete_attendees.json"""
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    if 'events' in data:
        return data['events']
    return []


def load_synthetic_meetings(jsonl_file: Path) -> List[Dict[str, Any]]:
    """Load synthetic meetings from JSONL file"""
    meetings = []
    with open(jsonl_file, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                meetings.append(json.loads(line))
    return meetings


def compare_schemas(real_meetings: List[Dict[str, Any]], synthetic_meetings: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Compare schemas between real and synthetic meetings.
    
    Returns:
        Dictionary with comparison results
    """
    # Collect all fields from both datasets
    real_fields = set()
    synthetic_standard_fields = set()  # Exclude training fields
    
    for meeting in real_meetings[:10]:  # Sample first 10
        real_fields.update(meeting.keys())
    
    for meeting in synthetic_meetings[:10]:  # Sample first 10
        synthetic_standard_fields.update(
            k for k in meeting.keys() if k not in TRAINING_FIELDS
        )
    
    # Find differences
    missing_in_synthetic = real_fields - synthetic_standard_fields - OPTIONAL_FIELDS
    extra_in_synthetic = synthetic_standard_fields - real_fields - OPTIONAL_FIELDS
    common_fields = real_fields & synthetic_standard_fields
    
    return {
        'real_fields': sorted(real_fields),
        'synthetic_fields': sorted(synthetic_standard_fields),
        'training_fields': sorted(TRAINING_FIELDS),
        'common_fields': sorted(common_fields),
        'missing_in_synthetic': sorted(missing_in_synthetic),
        'extra_in_synthetic': sorted(extra_in_synthetic),
        'alignment_score': len(common_fields) / len(real_fields) if real_fields else 0
    }


def main():
    parser = argparse.ArgumentParser(
        description="Validate synthetic training data matches Microsoft Graph API schema"
    )
    
    parser.add_argument(
        '--real',
        type=Path,
        default=Path('my_calendar_events_complete_attendees.json'),
        help='Path to real meeting data (default: my_calendar_events_complete_attendees.json)'
    )
    
    parser.add_argument(
        '--synthetic',
        type=Path,
        required=True,
        help='Path to synthetic meeting data (JSONL or JSON)'
    )
    
    parser.add_argument(
        '--sample-size',
        type=int,
        default=10,
        help='Number of meetings to validate (default: 10)'
    )
    
    args = parser.parse_args()
    
    # Load real meetings
    print(f"Loading real meetings from: {args.real}")
    if not args.real.exists():
        print(f"⚠️  Real meeting data not found: {args.real}")
        print("Skipping schema comparison (will only validate synthetic data)")
        real_meetings = []
    else:
        real_meetings = load_real_meetings(args.real)
        print(f"✅ Loaded {len(real_meetings)} real meetings")
    
    # Load synthetic meetings
    print(f"\nLoading synthetic meetings from: {args.synthetic}")
    if not args.synthetic.exists():
        print(f"❌ Synthetic meeting data not found: {args.synthetic}")
        return 1
    
    if args.synthetic.suffix == '.jsonl':
        synthetic_meetings = load_synthetic_meetings(args.synthetic)
    else:
        with open(args.synthetic, 'r', encoding='utf-8') as f:
            synthetic_meetings = json.load(f)
            if isinstance(synthetic_meetings, dict) and 'events' in synthetic_meetings:
                synthetic_meetings = synthetic_meetings['events']
    
    print(f"✅ Loaded {len(synthetic_meetings)} synthetic meetings")
    
    # Validate synthetic meetings
    print(f"\n{'='*60}")
    print(f"Validating {min(args.sample_size, len(synthetic_meetings))} synthetic meetings...")
    print(f"{'='*60}")
    
    validation_errors = []
    for i, meeting in enumerate(synthetic_meetings[:args.sample_size]):
        errors = validate_meeting_schema(meeting, is_synthetic=True)
        if errors:
            validation_errors.append((i, meeting.get('subject', 'Unknown'), errors))
    
    if validation_errors:
        print(f"\n❌ Found {len(validation_errors)} meetings with validation errors:\n")
        for i, subject, errors in validation_errors:
            print(f"Meeting {i}: {subject}")
            for error in errors:
                print(f"  - {error}")
            print()
    else:
        print(f"✅ All {args.sample_size} synthetic meetings are valid!")
    
    # Compare schemas if real data available
    if real_meetings:
        print(f"\n{'='*60}")
        print("Schema Comparison: Real vs Synthetic")
        print(f"{'='*60}")
        
        comparison = compare_schemas(real_meetings, synthetic_meetings)
        
        print(f"\n📊 Alignment Score: {comparison['alignment_score']:.1%}")
        print(f"   (Common fields / Total real fields)")
        
        print(f"\n✅ Common Fields ({len(comparison['common_fields'])}):")
        for field in comparison['common_fields']:
            print(f"   - {field}")
        
        print(f"\n🏷️  Training-Specific Fields ({len(comparison['training_fields'])}):")
        for field in comparison['training_fields']:
            print(f"   - {field}")
        
        if comparison['missing_in_synthetic']:
            print(f"\n⚠️  Missing in Synthetic ({len(comparison['missing_in_synthetic'])}):")
            for field in comparison['missing_in_synthetic']:
                print(f"   - {field}")
        
        if comparison['extra_in_synthetic']:
            print(f"\n🔍 Extra in Synthetic ({len(comparison['extra_in_synthetic'])}):")
            for field in comparison['extra_in_synthetic']:
                print(f"   - {field}")
        
        # Final verdict
        print(f"\n{'='*60}")
        if comparison['alignment_score'] >= 0.9:
            print("✅ EXCELLENT: Synthetic data is 90%+ aligned with real data schema")
        elif comparison['alignment_score'] >= 0.8:
            print("✅ GOOD: Synthetic data is 80%+ aligned with real data schema")
        elif comparison['alignment_score'] >= 0.7:
            print("⚠️  MODERATE: Synthetic data is 70%+ aligned (needs improvement)")
        else:
            print("❌ POOR: Synthetic data alignment is below 70%")
        print(f"{'='*60}")
    
    # Statistics
    print(f"\n{'='*60}")
    print("Training Data Statistics")
    print(f"{'='*60}")
    
    importance_dist = {'critical': 0, 'high': 0, 'medium': 0, 'low': 0}
    prep_needed_count = 0
    total_prep_time = 0
    
    for meeting in synthetic_meetings:
        importance = meeting.get('importance_label', 'low')
        importance_dist[importance] += 1
        
        if meeting.get('prep_needed', False):
            prep_needed_count += 1
            total_prep_time += meeting.get('prep_time_minutes', 0)
    
    print(f"\nTotal Meetings: {len(synthetic_meetings)}")
    print(f"\nImportance Distribution:")
    for level, count in importance_dist.items():
        pct = (count / len(synthetic_meetings) * 100) if synthetic_meetings else 0
        print(f"  {level.capitalize()}: {count} ({pct:.1f}%)")
    
    print(f"\nPrep Needed: {prep_needed_count} ({prep_needed_count/len(synthetic_meetings)*100:.1f}%)")
    if prep_needed_count > 0:
        print(f"Avg Prep Time: {total_prep_time/prep_needed_count:.1f} minutes")
    
    return 0 if not validation_errors else 1


if __name__ == "__main__":
    sys.exit(main())
