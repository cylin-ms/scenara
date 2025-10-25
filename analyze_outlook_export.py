#!/usr/bin/env python3
"""
CYL's Calendar Analysis from Outlook Export
Analyzes exported calendar data from Outlook (.ics or .csv format)
"""

import os
import sys
import json
import csv
import re
from datetime import datetime, timezone, timedelta
from typing import List, Dict, Any
import argparse


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


def parse_outlook_csv(file_path: str, target_date: str) -> List[Dict[str, Any]]:
    """Parse Outlook CSV export for meetings on target date."""
    safe_print(f"📊 Parsing Outlook CSV export: {file_path}")
    
    events = []
    target_date_obj = datetime.strptime(target_date, "%Y-%m-%d").date()
    
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            # Try to detect delimiter
            sample = f.read(1024)
            f.seek(0)
            
            if '\t' in sample:
                delimiter = '\t'
            elif ',' in sample:
                delimiter = ','
            else:
                delimiter = ','
            
            reader = csv.DictReader(f, delimiter=delimiter)
            
            for row in reader:
                # Try different column name variations
                subject = (row.get('Subject') or row.get('subject') or 
                          row.get('Title') or row.get('title') or 
                          row.get('Summary') or row.get('summary', 'No Subject'))
                
                start_time = (row.get('Start Date') or row.get('Start Time') or 
                             row.get('start') or row.get('Start') or 
                             row.get('Date') or row.get('date'))
                
                # Parse date
                if start_time:
                    try:
                        # Try various date formats
                        for fmt in ['%Y-%m-%d %H:%M:%S', '%m/%d/%Y %H:%M:%S', 
                                   '%Y-%m-%d', '%m/%d/%Y', '%d/%m/%Y']:
                            try:
                                event_date = datetime.strptime(start_time.strip(), fmt).date()
                                break
                            except ValueError:
                                continue
                        else:
                            continue  # Skip if no format matches
                        
                        if event_date == target_date_obj:
                            response_status = (row.get('Response') or row.get('response') or 
                                             row.get('My Response') or row.get('Status') or 
                                             row.get('ResponseStatus') or 'none')
                            
                            organizer = (row.get('Organizer') or row.get('organizer') or 
                                       row.get('From') or row.get('from') or '')
                            
                            events.append({
                                'subject': subject,
                                'start': start_time,
                                'responseStatus': {'response': response_status.lower()},
                                'organizer': {'emailAddress': {'address': organizer}},
                                'attendees': []  # Not usually in CSV exports
                            })
                    except Exception as e:
                        safe_print(f"⚠️  Error parsing row: {e}")
                        continue
    
    except Exception as e:
        safe_print(f"❌ Error reading CSV file: {e}")
        return []
    
    safe_print(f"✅ Found {len(events)} events for {target_date}")
    return events


def parse_outlook_ics(file_path: str, target_date: str) -> List[Dict[str, Any]]:
    """Parse Outlook ICS export for meetings on target date."""
    safe_print(f"📅 Parsing Outlook ICS export: {file_path}")
    
    events = []
    target_date_obj = datetime.strptime(target_date, "%Y-%m-%d").date()
    
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # Simple ICS parser
        event_blocks = content.split('BEGIN:VEVENT')[1:]
        
        for block in event_blocks:
            if 'END:VEVENT' not in block:
                continue
                
            event_content = block.split('END:VEVENT')[0]
            event_data = {}
            
            # Extract fields
            lines = event_content.split('\n')
            for line in lines:
                line = line.strip()
                if ':' in line:
                    key, value = line.split(':', 1)
                    if key == 'SUMMARY':
                        event_data['subject'] = value
                    elif key.startswith('DTSTART'):
                        try:
                            # Parse ICS datetime format
                            dt_str = value.replace('T', ' ').replace('Z', '')
                            if len(dt_str) == 15:  # YYYYMMDDTHHMMSSZ
                                dt_str = f"{dt_str[:4]}-{dt_str[4:6]}-{dt_str[6:8]} {dt_str[9:11]}:{dt_str[11:13]}:{dt_str[13:15]}"
                            event_dt = datetime.fromisoformat(dt_str).date()
                            
                            if event_dt == target_date_obj:
                                event_data['start'] = value
                                event_data['match_date'] = True
                        except:
                            continue
                    elif key == 'ORGANIZER':
                        # Extract email from ORGANIZER:MAILTO:email@domain.com
                        email_match = re.search(r'MAILTO:([^;]+)', value)
                        if email_match:
                            event_data['organizer'] = email_match.group(1)
            
            if event_data.get('match_date') and event_data.get('subject'):
                events.append({
                    'subject': event_data['subject'],
                    'start': event_data.get('start', ''),
                    'responseStatus': {'response': 'none'},  # ICS usually doesn't include response
                    'organizer': {'emailAddress': {'address': event_data.get('organizer', '')}},
                    'attendees': []
                })
    
    except Exception as e:
        safe_print(f"❌ Error reading ICS file: {e}")
        return []
    
    safe_print(f"✅ Found {len(events)} events for {target_date}")
    return events


def analyze_exported_calendar(events: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Analyze exported calendar events."""
    safe_print("\n🔍 Analyzing exported calendar data...")
    
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
        if response_status in ["accepted", "accept"]:
            accepted_meetings += 1
        elif response_status in ["tentativelyaccepted", "tentative", "maybe"]:
            tentative_meetings += 1
        elif response_status in ["declined", "decline", "no"]:
            declined_meetings += 1
        else:
            no_response_meetings += 1
        
        # Collect collaborators
        organizer_email = event.get("organizer", {}).get("emailAddress", {}).get("address", "")
        if organizer_email:
            collaborators.add(organizer_email)
        
        # Collect subjects
        subject = event.get("subject", "No Subject")
        meeting_subjects.append(subject)
    
    return {
        "total_meetings": total_meetings,
        "accepted_meetings": accepted_meetings,
        "tentative_meetings": tentative_meetings,
        "declined_meetings": declined_meetings,
        "no_response_meetings": no_response_meetings,
        "unique_collaborators": len(collaborators),
        "collaborator_list": sorted(list(collaborators)),
        "meeting_subjects": meeting_subjects
    }


def print_analysis_summary(events: List[Dict[str, Any]], analysis: Dict[str, Any], target_date: str):
    """Print formatted analysis summary."""
    safe_print("\n" + "="*80)
    safe_print(f"📅 CYL'S CALENDAR ANALYSIS - {target_date}")
    safe_print("="*80)
    
    safe_print(f"📊 MEETING STATISTICS:")
    safe_print(f"   • Total meetings: {analysis['total_meetings']}")
    safe_print(f"   • ✅ Accepted: {analysis['accepted_meetings']}")
    safe_print(f"   • ❓ Tentative: {analysis['tentative_meetings']}")
    safe_print(f"   • ❌ Declined: {analysis['declined_meetings']}")
    safe_print(f"   • ⚪ No response/Unknown: {analysis['no_response_meetings']}")
    safe_print(f"   • 👥 Unique collaborators: {analysis['unique_collaborators']}")
    
    safe_print(f"\n📋 MEETINGS LIST:")
    for i, event in enumerate(events, 1):
        subject = event.get('subject', 'No Subject')
        response = event.get('responseStatus', {}).get('response', 'none')
        start_time = event.get('start', 'Unknown time')
        
        status_emoji = {
            "accepted": "✅", "accept": "✅",
            "tentativelyaccepted": "❓", "tentative": "❓", "maybe": "❓",
            "declined": "❌", "decline": "❌", "no": "❌",
        }.get(response.lower(), "⚪")
        
        safe_print(f"   {i}. {status_emoji} {subject}")
        safe_print(f"      Time: {start_time}")
        safe_print(f"      Response: {response}")
        safe_print()
    
    # Flight conflict analysis
    safe_print(f"✈️  FLIGHT CI005 ANALYSIS:")
    safe_print(f"   Flight CI005 departs at 4:25 PM PDT")
    safe_print(f"   Need to leave by 2:25 PM for travel to airport")
    safe_print(f"   Review meeting end times to check for conflicts")
    
    # Verification
    safe_print(f"\n🔍 VERIFICATION:")
    safe_print(f"   Expected: 1 accepted + 7 tentative meetings")
    safe_print(f"   Found: {analysis['accepted_meetings']} accepted + {analysis['tentative_meetings']} tentative meetings")
    
    if analysis['accepted_meetings'] == 1 and analysis['tentative_meetings'] == 7:
        safe_print("   ✅ Perfect match with your calendar check!")
    else:
        safe_print("   ❓ Different from expected - may be due to export format limitations")


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(description="Analyze exported Outlook calendar data")
    parser.add_argument("file", help="Path to exported calendar file (.csv or .ics)")
    parser.add_argument("--date", default="2025-10-22", help="Target date (YYYY-MM-DD)")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.file):
        safe_print(f"❌ File not found: {args.file}")
        sys.exit(1)
    
    safe_print("🚀 CYL's Calendar Analysis from Outlook Export")
    safe_print("=" * 50)
    
    # Determine file type and parse
    file_ext = os.path.splitext(args.file)[1].lower()
    
    if file_ext == '.csv':
        events = parse_outlook_csv(args.file, args.date)
    elif file_ext == '.ics':
        events = parse_outlook_ics(args.file, args.date)
    else:
        safe_print(f"❌ Unsupported file type: {file_ext}")
        safe_print("💡 Supported formats: .csv, .ics")
        sys.exit(1)
    
    if not events:
        safe_print(f"📭 No meetings found for {args.date}")
        safe_print("💡 Tips:")
        safe_print("   • Check the date format in your export")
        safe_print("   • Ensure the export includes the target date")
        safe_print("   • Try exporting in a different format")
        return
    
    # Analyze events
    analysis = analyze_exported_calendar(events)
    
    # Print summary
    print_analysis_summary(events, analysis, args.date)
    
    # Save results
    output_file = f"cyl_calendar_analysis_{args.date.replace('-', '')}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "source_file": args.file,
            "target_date": args.date,
            "analysis": analysis,
            "events": events
        }, f, indent=2, ensure_ascii=False)
    
    safe_print(f"\n💾 Analysis saved to: {output_file}")
    safe_print("✅ Calendar analysis completed!")


if __name__ == "__main__":
    main()