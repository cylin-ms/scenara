#!/usr/bin/env python3
"""
Workback Plan Meeting Schema Aligner

Aligns meeting objects in workback plan examples with Microsoft Graph API schema
from SilverFlow extraction tool (my_calendar_events_complete_attendees.json).

This ensures consistency between:
1. Real meeting data extracted via SilverFlow
2. Workback plan meeting contexts (example scenarios)
3. Meeting intelligence pipeline inputs

The aligned meeting objects can be used as input to the workback planning generator
(src/workback_planning/) which uses a two-stage LLM pipeline to generate complete
workback plans with milestones, tasks, and dependencies.

Usage:
    python tools/align_workback_meeting_schema.py --validate workback_ado/*.md
    python tools/align_workback_meeting_schema.py --convert workback_ado/WORKBACK_PLAN_01_QBR.md
"""

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


# Microsoft Graph API Schema (from SilverFlow extraction)
GRAPH_API_REQUIRED_FIELDS = {
    'id',            # Unique meeting identifier
    'subject',       # Meeting title/subject
    'start',         # Start time (object with dateTime and timeZone)
    'end',           # End time (object with dateTime and timeZone)
    'organizer',     # Organizer (object with emailAddress)
    'attendees'      # List of attendees (array of objects)
}

GRAPH_API_OPTIONAL_FIELDS = {
    'bodyPreview',      # Meeting description/body preview
    'showAs',           # busy, free, tentative, oof, workingElsewhere, unknown
    'type',             # singleInstance, occurrence, exception, seriesMaster
    'responseStatus',   # User's response (object with response and time)
    'seriesMasterId',   # ID of the series master (for recurring meetings)
    'webLink',          # Outlook web link
    '@odata.etag'       # ETag for concurrency control
}

# Workback-specific fields (additional context for planning)
WORKBACK_SPECIFIC_FIELDS = {
    'meeting_type',             # QBR, Board Meeting, Sales Presentation, etc.
    'complexity',               # low, medium, high
    'workback_plan',            # Reference to the workback plan
    'prep_requirements',        # Preparation requirements
    'critical_success_factors', # CSFs for the meeting
    'risk_factors'             # Potential risks
}


def create_graph_api_meeting_object(
    meeting_id: str,
    subject: str,
    start_datetime: str,
    end_datetime: str,
    timezone: str,
    organizer_name: str,
    organizer_email: str,
    attendees: List[Dict[str, Any]],
    body_preview: Optional[str] = None,
    show_as: str = "busy",
    meeting_type: str = "singleInstance"
) -> Dict[str, Any]:
    """
    Create a Microsoft Graph API-compliant meeting object.
    
    Args:
        meeting_id: Unique meeting identifier (e.g., "WB-QBR-001")
        subject: Meeting title
        start_datetime: ISO 8601 datetime string (e.g., "2025-12-15T14:00:00.0000000")
        end_datetime: ISO 8601 datetime string
        timezone: IANA timezone (e.g., "America/Los_Angeles", "Asia/Shanghai")
        organizer_name: Full name of organizer
        organizer_email: Email address of organizer
        attendees: List of attendee objects (see create_attendee)
        body_preview: Optional meeting description
        show_as: busy, free, tentative, oof, workingElsewhere, unknown
        meeting_type: singleInstance, occurrence, exception, seriesMaster
        
    Returns:
        Graph API-compliant meeting object
    """
    meeting = {
        "id": meeting_id,
        "subject": subject,
        "bodyPreview": body_preview or "",
        "showAs": show_as,
        "type": meeting_type,
        "start": {
            "dateTime": start_datetime,
            "timeZone": timezone
        },
        "end": {
            "dateTime": end_datetime,
            "timeZone": timezone
        },
        "organizer": {
            "emailAddress": {
                "name": organizer_name,
                "address": organizer_email
            }
        },
        "attendees": attendees,
        "responseStatus": {
            "response": "organizer",
            "time": datetime.utcnow().isoformat() + "Z"
        }
    }
    
    return meeting


def create_attendee(
    name: str,
    email: str,
    attendee_type: str = "required",
    response: str = "none"
) -> Dict[str, Any]:
    """
    Create a Graph API-compliant attendee object.
    
    Args:
        name: Full name of attendee
        email: Email address
        attendee_type: required, optional, resource
        response: none, organizer, tentativelyAccepted, accepted, declined, notResponded
        
    Returns:
        Graph API-compliant attendee object
    """
    if attendee_type not in ['required', 'optional', 'resource']:
        raise ValueError(f"Invalid attendee_type: {attendee_type}. Must be 'required', 'optional', or 'resource'")
    
    return {
        "type": attendee_type,
        "status": {
            "response": response,
            "time": "0001-01-01T00:00:00Z"
        },
        "emailAddress": {
            "name": name,
            "address": email
        }
    }


def parse_workback_meeting_context(markdown_text: str) -> Optional[Dict[str, Any]]:
    """
    Parse meeting context from workback plan markdown.
    
    Extracts meeting details from the "Meeting Context" section.
    
    Returns:
        Parsed meeting context or None if not found
    """
    # Extract Meeting Context section
    context_pattern = r'### Meeting Context\s+(.*?)(?=\n###|\n---|\Z)'
    context_match = re.search(context_pattern, markdown_text, re.DOTALL)
    
    if not context_match:
        return None
    
    context_text = context_match.group(1)
    
    # Parse fields
    meeting_type = re.search(r'\*\*Meeting Type\*\*:\s*(.+)', context_text)
    target_date = re.search(r'\*\*Target Date\*\*:\s*(.+)', context_text)
    organizer = re.search(r'\*\*Organizer\*\*:\s*(.+)', context_text)
    attendees = re.search(r'\*\*Attendees\*\*:\s*(.+)', context_text)
    objective = re.search(r'\*\*Objective\*\*:\s*(.+)', context_text)
    
    return {
        'meeting_type': meeting_type.group(1) if meeting_type else None,
        'target_date': target_date.group(1) if target_date else None,
        'organizer': organizer.group(1) if organizer else None,
        'attendees': attendees.group(1) if attendees else None,
        'objective': objective.group(1) if objective else None
    }


def convert_workback_to_graph_api(
    meeting_context: Dict[str, Any],
    meeting_id_prefix: str = "WB"
) -> Dict[str, Any]:
    """
    Convert workback meeting context to Graph API format.
    
    Args:
        meeting_context: Parsed meeting context from workback plan
        meeting_id_prefix: Prefix for meeting ID (default: "WB" for workback)
        
    Returns:
        Graph API-compliant meeting object
    """
    # Parse target date (e.g., "December 15, 2025, 2:00 PM - 4:00 PM PT")
    # This is a simplified parser - enhance as needed
    target_date_str = meeting_context.get('target_date', '')
    
    # Default values for demonstration
    meeting_id = f"{meeting_id_prefix}-{meeting_context.get('meeting_type', 'MEETING').replace(' ', '-').upper()}-001"
    subject = f"{meeting_context.get('meeting_type', 'Meeting')}"
    
    # Parse organizer (e.g., "SVP of Operations" or "Sarah Chen, SVP Operations")
    organizer_str = meeting_context.get('organizer', 'Unknown Organizer')
    organizer_name = organizer_str.split(',')[0] if ',' in organizer_str else organizer_str
    organizer_email = f"{organizer_name.lower().replace(' ', '.')}@example.com"
    
    # Parse attendees (e.g., "CEO, CFO, Division heads (8), Key stakeholders (12)")
    attendees_list = []
    attendees_str = meeting_context.get('attendees', '')
    
    # This is a simplified parser - you may want to enhance it
    if 'CEO' in attendees_str:
        attendees_list.append(create_attendee("Chief Executive Officer", "ceo@example.com", "required"))
    if 'CFO' in attendees_str:
        attendees_list.append(create_attendee("Chief Financial Officer", "cfo@example.com", "required"))
    
    # Default times (you'll want to parse these properly)
    start_datetime = "2025-12-15T14:00:00.0000000"
    end_datetime = "2025-12-15T16:00:00.0000000"
    timezone = "America/Los_Angeles"
    
    # Create Graph API meeting object
    meeting = create_graph_api_meeting_object(
        meeting_id=meeting_id,
        subject=subject,
        start_datetime=start_datetime,
        end_datetime=end_datetime,
        timezone=timezone,
        organizer_name=organizer_name,
        organizer_email=organizer_email,
        attendees=attendees_list,
        body_preview=meeting_context.get('objective', ''),
        show_as="busy",
        meeting_type="singleInstance"
    )
    
    # Add workback-specific metadata (not part of Graph API schema)
    meeting['_workback_metadata'] = {
        'meeting_type': meeting_context.get('meeting_type'),
        'complexity': 'high',  # You may want to infer this
        'original_context': meeting_context
    }
    
    return meeting


def validate_graph_api_schema(meeting: Dict[str, Any]) -> List[str]:
    """
    Validate meeting object against Graph API schema.
    
    Returns:
        List of validation errors (empty if valid)
    """
    errors = []
    
    # Check required fields
    for field in GRAPH_API_REQUIRED_FIELDS:
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
    
    return errors


def process_workback_plan_file(file_path: Path, validate_only: bool = False) -> Dict[str, Any]:
    """
    Process a workback plan markdown file.
    
    Args:
        file_path: Path to workback plan markdown file
        validate_only: If True, only validate; if False, convert to Graph API format
        
    Returns:
        Dictionary with results
    """
    print(f"\n{'='*80}")
    print(f"Processing: {file_path.name}")
    print(f"{'='*80}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Parse meeting context
    meeting_context = parse_workback_meeting_context(content)
    
    if not meeting_context:
        print("❌ No meeting context found")
        return {'success': False, 'error': 'No meeting context found'}
    
    print(f"\n📋 Meeting Context:")
    print(f"   Type: {meeting_context.get('meeting_type')}")
    print(f"   Date: {meeting_context.get('target_date')}")
    print(f"   Organizer: {meeting_context.get('organizer')}")
    print(f"   Attendees: {meeting_context.get('attendees')}")
    
    if validate_only:
        print("\n✅ Validation mode: Meeting context parsed successfully")
        return {'success': True, 'meeting_context': meeting_context}
    
    # Convert to Graph API format
    meeting = convert_workback_to_graph_api(meeting_context)
    
    # Validate the converted meeting
    errors = validate_graph_api_schema(meeting)
    
    if errors:
        print(f"\n❌ Validation errors ({len(errors)}):")
        for error in errors:
            print(f"   - {error}")
        return {'success': False, 'meeting': meeting, 'errors': errors}
    
    print(f"\n✅ Converted to Graph API format successfully")
    print(f"\n📄 Meeting Object:")
    print(json.dumps(meeting, indent=2))
    
    # Save converted meeting
    output_file = file_path.parent / f"{file_path.stem}_meeting.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(meeting, f, indent=2)
    
    print(f"\n💾 Saved to: {output_file}")
    
    return {'success': True, 'meeting': meeting, 'output_file': str(output_file)}


def main():
    parser = argparse.ArgumentParser(
        description='Align workback plan meeting objects with Microsoft Graph API schema'
    )
    parser.add_argument(
        'files',
        nargs='+',
        type=Path,
        help='Workback plan markdown files to process'
    )
    parser.add_argument(
        '--validate',
        action='store_true',
        help='Only validate meeting context (do not convert)'
    )
    parser.add_argument(
        '--output-dir',
        type=Path,
        help='Output directory for converted meeting objects'
    )
    
    args = parser.parse_args()
    
    print(f"\n🔧 Workback Plan Meeting Schema Aligner")
    print(f"{'='*80}")
    print(f"Mode: {'Validate Only' if args.validate else 'Convert to Graph API'}")
    print(f"Files: {len(args.files)}")
    
    results = []
    for file_path in args.files:
        if not file_path.exists():
            print(f"\n❌ File not found: {file_path}")
            continue
        
        result = process_workback_plan_file(file_path, validate_only=args.validate)
        results.append(result)
    
    # Summary
    print(f"\n{'='*80}")
    print(f"SUMMARY")
    print(f"{'='*80}")
    
    successful = sum(1 for r in results if r.get('success'))
    failed = len(results) - successful
    
    print(f"Total files processed: {len(results)}")
    print(f"✅ Successful: {successful}")
    print(f"❌ Failed: {failed}")
    
    if failed == 0:
        print(f"\n🎉 All files processed successfully!")
        return 0
    else:
        print(f"\n⚠️  Some files had errors. Review output above.")
        return 1


if __name__ == '__main__':
    sys.exit(main())
