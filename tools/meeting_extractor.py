#!/usr/bin/env python3
"""
Scenara Meeting Extraction Tool
Retrieves and processes meeting data from multiple sources for meeting intelligence analysis
"""

import argparse
import json
import os
import sys
import zoneinfo
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import List, Dict, Optional, Set, Any
import requests
import msal


class ScenearaMeetingExtractor:
    """
    Comprehensive meeting extraction tool for Scenara project
    Supports multiple data sources and formats for meeting intelligence
    """
    
    def __init__(self, project_root: str = None):
        self.project_root = Path(project_root) if project_root else Path.cwd()
        self.mevals_dir = self.project_root / "MEvals"
        self.output_dir = self.project_root / "meeting_data_extracted"
        self.output_dir.mkdir(exist_ok=True)
        
        # Microsoft Graph configuration (same as MEvals)
        self.tenant_id = "72f988bf-86f1-41af-91ab-2d7cd011db47"
        self.client_id = "9ce97a32-d9ab-4ab2-aadc-f49b39b94e11"
        self.scopes = ["Calendars.Read"]
        
        # Set up local timezone (Pacific Time)
        try:
            self.local_tz = zoneinfo.ZoneInfo("America/Los_Angeles")
        except:
            # Fallback for older Python versions
            self.local_tz = timezone(timedelta(hours=-7))  # PDT
        
    def get_available_sources(self) -> Dict[str, Any]:
        """
        Discover all available meeting data sources
        
        Returns:
            Dictionary mapping source names to their availability and metadata
        """
        sources = {}
        
        # Check for existing JSON files
        json_files = list(self.project_root.glob("my_calendar_events*.json"))
        if json_files:
            sources["local_calendar_json"] = {
                "available": True,
                "files": [str(f) for f in json_files],
                "description": "Local calendar JSON exports from Graph Explorer"
            }
        
        # Check MEvals directory
        if self.mevals_dir.exists():
            sources["mevals_directory"] = {
                "available": True,
                "path": str(self.mevals_dir),
                "description": "MEvals meeting evaluation system with fetch_meetings.py"
            }
        
        # Check for Graph API access
        sources["microsoft_graph_api"] = {
            "available": True,  # Always available, but requires authentication
            "description": "Direct Microsoft Graph Calendar API access",
            "requires_auth": True
        }
        
        # Check meeting prep data
        meeting_prep_dir = self.project_root / "meeting_prep_data"
        if meeting_prep_dir.exists():
            scenario_files = list(meeting_prep_dir.glob("*scenarios*.json"))
            if scenario_files:
                sources["meeting_prep_scenarios"] = {
                    "available": True,
                    "files": [str(f) for f in scenario_files],
                    "description": "Processed meeting preparation scenarios"
                }
        
        return sources
    
    def extract_from_local_json(self, file_path: str = None) -> List[Dict]:
        """
        Extract meetings from local JSON files (Graph Explorer exports)
        
        Args:
            file_path: Specific file path, or auto-detect latest
            
        Returns:
            List of processed meeting objects
        """
        if not file_path:
            # Auto-detect latest calendar file
            json_files = list(self.project_root.glob("my_calendar_events*.json"))
            if not json_files:
                raise FileNotFoundError("No calendar JSON files found")
            file_path = max(json_files, key=lambda f: f.stat().st_mtime)
        
        print(f"📅 Loading calendar data from: {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if 'value' not in data:
            raise ValueError("Invalid JSON format. Expected 'value' field from Graph API")
        
        events = data['value']
        processed_meetings = []
        
        for event in events:
            processed_meeting = self._process_graph_event(event)
            if processed_meeting:
                processed_meetings.append(processed_meeting)
        
        print(f"✅ Processed {len(processed_meetings)} meetings from local JSON")
        return processed_meetings
    
    def extract_from_mevals(self) -> List[Dict]:
        """
        Extract meetings using MEvals fetch_meetings.py script
        
        Returns:
            List of processed meeting objects
        """
        if not self.mevals_dir.exists():
            raise FileNotFoundError(f"MEvals directory not found: {self.mevals_dir}")
        
        fetch_script = self.mevals_dir / "fetch_meetings.py"
        if not fetch_script.exists():
            raise FileNotFoundError(f"MEvals fetch_meetings.py not found: {fetch_script}")
        
        print("🔄 Running MEvals fetch_meetings.py...")
        
        # Change to MEvals directory and run fetch script
        original_cwd = os.getcwd()
        try:
            os.chdir(self.mevals_dir)
            
            # Import and run fetch_meetings
            sys.path.insert(0, str(self.mevals_dir))
            import fetch_meetings
            
            # Run the fetch
            fetch_meetings.main()
            
            # Load the resulting meetings.json
            meetings_file = self.mevals_dir / "meetings.json"
            if meetings_file.exists():
                with open(meetings_file, 'r', encoding='utf-8') as f:
                    meetings_data = json.load(f)
                
                processed_meetings = []
                for event in meetings_data:
                    processed_meeting = self._process_graph_event(event)
                    if processed_meeting:
                        processed_meetings.append(processed_meeting)
                
                print(f"✅ Extracted {len(processed_meetings)} meetings via MEvals")
                return processed_meetings
            else:
                raise FileNotFoundError("MEvals fetch_meetings.py did not create meetings.json")
                
        finally:
            os.chdir(original_cwd)
            if str(self.mevals_dir) in sys.path:
                sys.path.remove(str(self.mevals_dir))
    
    def extract_from_graph_api(self, days_back: int = 30, days_forward: int = 14) -> List[Dict]:
        """
        Extract meetings directly from Microsoft Graph API
        
        Args:
            days_back: Number of days to look back
            days_forward: Number of days to look forward
            
        Returns:
            List of processed meeting objects
        """
        print("🔗 Connecting to Microsoft Graph API...")
        
        # Calculate time range
        now = datetime.now(timezone.utc)
        start_time = now - timedelta(days=days_back)
        end_time = now + timedelta(days=days_forward)
        
        # Build authority and app
        authority = f"https://login.microsoftonline.com/{self.tenant_id}"
        app = msal.PublicClientApplication(self.client_id, authority=authority)
        
        # Try silent authentication first
        accounts = app.get_accounts()
        result = None
        
        if accounts:
            print("🔑 Attempting silent authentication...")
            result = app.acquire_token_silent(self.scopes, account=accounts[0])
        
        if not result or "access_token" not in result:
            print("🔐 Interactive authentication required...")
            result = app.acquire_token_interactive(self.scopes)
        
        if "access_token" not in result:
            raise Exception(f"Authentication failed: {result.get('error_description', 'Unknown error')}")
        
        access_token = result["access_token"]
        
        # Build calendar view URL
        base_url = 'https://graph.microsoft.com/v1.0/me/calendarview'
        params = [
            f"startDateTime={start_time.isoformat()}",
            f"endDateTime={end_time.isoformat()}",
            "$top=100",
            "$orderby=start/dateTime"
        ]
        url = f"{base_url}?{'&'.join(params)}"
        
        # Make API request
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Accept': 'application/json'
        }
        
        print(f"📡 Fetching meetings from {start_time.date()} to {end_time.date()}...")
        
        response = requests.get(url, headers=headers)
        if not response.ok:
            raise Exception(f"Graph API error: {response.status_code} {response.text}")
        
        data = response.json()
        events = data.get('value', [])
        
        # Process events
        processed_meetings = []
        for event in events:
            processed_meeting = self._process_graph_event(event)
            if processed_meeting:
                processed_meetings.append(processed_meeting)
        
        print(f"✅ Extracted {len(processed_meetings)} meetings from Graph API")
        return processed_meetings
    
    def extract_from_meeting_prep_scenarios(self) -> List[Dict]:
        """
        Extract meetings from existing meeting prep scenario files
        
        Returns:
            List of processed meeting scenarios
        """
        meeting_prep_dir = self.project_root / "meeting_prep_data"
        scenario_files = list(meeting_prep_dir.glob("*scenarios*.json"))
        
        if not scenario_files:
            raise FileNotFoundError("No meeting scenario files found in meeting_prep_data")
        
        all_scenarios = []
        
        for file_path in scenario_files:
            print(f"📋 Loading scenarios from: {file_path.name}")
            
            with open(file_path, 'r', encoding='utf-8') as f:
                scenarios = json.load(f)
            
            # Handle different file formats
            if isinstance(scenarios, dict) and 'scenarios' in scenarios:
                scenarios = scenarios['scenarios']
            elif isinstance(scenarios, dict) and 'value' in scenarios:
                scenarios = scenarios['value']
            
            if isinstance(scenarios, list):
                processed_scenarios = []
                for scenario in scenarios:
                    processed_scenario = self._process_scenario_object(scenario)
                    if processed_scenario:
                        processed_scenarios.append(processed_scenario)
                
                all_scenarios.extend(processed_scenarios)
                print(f"   ✅ Loaded {len(processed_scenarios)} scenarios")
        
        print(f"✅ Total {len(all_scenarios)} scenarios extracted")
        return all_scenarios
    
    def _process_graph_event(self, event: Dict) -> Optional[Dict]:
        """
        Process a Microsoft Graph calendar event into standardized format
        
        Args:
            event: Raw Graph API event object
            
        Returns:
            Processed meeting object or None if invalid
        """
        try:
            # Extract attendees
            attendees = []
            if event.get('attendees'):
                for attendee in event['attendees']:
                    if attendee.get('emailAddress'):
                        name = attendee['emailAddress'].get('name', 'Unknown')
                        email = attendee['emailAddress'].get('address', '')
                        attendees.append({
                            'name': name,
                            'email': email,
                            'response': attendee.get('status', {}).get('response', 'none')
                        })
            
            # Calculate duration
            duration_minutes = 60  # Default
            if event.get('start') and event.get('end'):
                start_time = datetime.fromisoformat(event['start']['dateTime'].replace('Z', '+00:00'))
                end_time = datetime.fromisoformat(event['end']['dateTime'].replace('Z', '+00:00'))
                duration_minutes = int((end_time - start_time).total_seconds() / 60)
            
            # Extract meeting details
            subject = event.get('subject', 'Untitled Meeting')
            body_preview = event.get('bodyPreview', '')
            
            # Classify meeting type (basic classification)
            meeting_type = self._classify_meeting_type(subject, body_preview, attendees)
            
            # Convert times to local timezone for display
            start_local = start_time.astimezone(self.local_tz)
            end_local = end_time.astimezone(self.local_tz)
            
            processed_meeting = {
                'id': event.get('id', ''),
                'subject': subject,
                'start_time': event.get('start', {}).get('dateTime', ''),  # Keep original ISO
                'end_time': event.get('end', {}).get('dateTime', ''),      # Keep original ISO
                'start_time_local': start_local.strftime('%H:%M'),         # Add local time
                'end_time_local': end_local.strftime('%H:%M'),             # Add local time
                'timezone_local': start_local.strftime('%Z'),              # Add timezone
                'duration_minutes': duration_minutes,
                'attendees': attendees,
                'attendee_count': len(attendees),
                'body_preview': body_preview,
                'is_online_meeting': event.get('isOnlineMeeting', False),
                'meeting_type': meeting_type,
                'is_organizer': event.get('isOrganizer', False),
                'location': event.get('location', {}).get('displayName', ''),
                'importance': event.get('importance', 'normal'),
                'source': 'microsoft_graph',
                'extracted_at': datetime.now(timezone.utc).isoformat()
            }
            
            return processed_meeting
            
        except Exception as e:
            print(f"⚠️ Error processing event: {e}", file=sys.stderr)
            return None
    
    def _process_scenario_object(self, scenario: Dict) -> Optional[Dict]:
        """
        Process a meeting prep scenario object into standardized format
        
        Args:
            scenario: Raw scenario object
            
        Returns:
            Processed meeting object or None if invalid
        """
        try:
            # Handle different scenario formats
            if 'scenario' in scenario:
                scenario_text = scenario['scenario']
            elif 'meeting_details' in scenario:
                scenario_text = scenario['meeting_details']
            else:
                scenario_text = str(scenario)
            
            # Extract basic info
            subject = scenario.get('title', scenario.get('subject', 'Meeting Scenario'))
            attendees = scenario.get('attendees', [])
            duration = scenario.get('duration_minutes', scenario.get('duration', 60))
            
            # Standardize attendee format
            standardized_attendees = []
            for attendee in attendees:
                if isinstance(attendee, str):
                    standardized_attendees.append({'name': attendee, 'email': '', 'response': 'none'})
                elif isinstance(attendee, dict):
                    standardized_attendees.append({
                        'name': attendee.get('name', attendee.get('email', 'Unknown')),
                        'email': attendee.get('email', ''),
                        'response': attendee.get('response', 'none')
                    })
            
            meeting_type = scenario.get('meeting_type', 'general')
            
            processed_scenario = {
                'id': scenario.get('id', f"scenario_{hash(scenario_text) % 1000000}"),
                'subject': subject,
                'scenario_text': scenario_text,
                'attendees': standardized_attendees,
                'attendee_count': len(standardized_attendees),
                'duration_minutes': duration,
                'meeting_type': meeting_type,
                'source': 'meeting_prep_scenarios',
                'extracted_at': datetime.now(timezone.utc).isoformat()
            }
            
            return processed_scenario
            
        except Exception as e:
            print(f"⚠️ Error processing scenario: {e}", file=sys.stderr)
            return None
    
    def _classify_meeting_type(self, subject: str, body: str, attendees: List[Dict]) -> str:
        """
        Basic meeting type classification
        
        Args:
            subject: Meeting subject
            body: Meeting body/description
            attendees: List of attendees
            
        Returns:
            Meeting type classification
        """
        subject_lower = subject.lower() if subject else ''
        body_lower = body.lower() if body else ''
        combined_text = f"{subject_lower} {body_lower}"
        
        # One-on-one meetings
        if len(attendees) <= 2 and ('1-1' in combined_text or 'one-on-one' in combined_text or '1:1' in combined_text):
            return 'one_on_one'
        
        # Project meetings
        if any(keyword in combined_text for keyword in ['project', 'sprint', 'scrum', 'standup', 'planning']):
            return 'project_management'
        
        # Review meetings
        if any(keyword in combined_text for keyword in ['review', 'feedback', 'retrospective']):
            return 'review'
        
        # Training/Learning
        if any(keyword in combined_text for keyword in ['training', 'workshop', 'demo', 'presentation']):
            return 'training'
        
        # Team meetings
        if any(keyword in combined_text for keyword in ['team', 'all hands', 'sync']):
            return 'team_meeting'
        
        # Client/External
        if any(keyword in combined_text for keyword in ['client', 'customer', 'external']):
            return 'client_meeting'
        
        return 'general'
    
    def save_extracted_meetings(self, meetings: List[Dict], filename: str = None) -> str:
        """
        Save extracted meetings to JSON file
        
        Args:
            meetings: List of processed meetings
            filename: Output filename (optional)
            
        Returns:
            Path to saved file
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"extracted_meetings_{timestamp}.json"
        
        output_path = self.output_dir / filename
        
        # Create metadata
        metadata = {
            'extraction_timestamp': datetime.now(timezone.utc).isoformat(),
            'total_meetings': len(meetings),
            'meeting_types': {},
            'sources': set()
        }
        
        # Analyze meetings
        for meeting in meetings:
            meeting_type = meeting.get('meeting_type', 'unknown')
            metadata['meeting_types'][meeting_type] = metadata['meeting_types'].get(meeting_type, 0) + 1
            metadata['sources'].add(meeting.get('source', 'unknown'))
        
        metadata['sources'] = list(metadata['sources'])
        
        # Save data
        output_data = {
            'metadata': metadata,
            'meetings': meetings
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Saved {len(meetings)} meetings to: {output_path}")
        return str(output_path)
    
    def generate_meeting_summary(self, meetings: List[Dict]) -> Dict:
        """
        Generate summary statistics for extracted meetings
        
        Args:
            meetings: List of processed meetings
            
        Returns:
            Summary statistics dictionary
        """
        if not meetings:
            return {'total_meetings': 0}
        
        # Basic stats
        total_meetings = len(meetings)
        
        # Meeting types
        meeting_types = {}
        sources = {}
        duration_stats = []
        attendee_stats = []
        
        for meeting in meetings:
            # Meeting type distribution
            meeting_type = meeting.get('meeting_type', 'unknown')
            meeting_types[meeting_type] = meeting_types.get(meeting_type, 0) + 1
            
            # Source distribution
            source = meeting.get('source', 'unknown')
            sources[source] = sources.get(source, 0) + 1
            
            # Duration stats
            duration = meeting.get('duration_minutes', 0)
            if duration > 0:
                duration_stats.append(duration)
            
            # Attendee stats
            attendee_count = meeting.get('attendee_count', 0)
            if attendee_count > 0:
                attendee_stats.append(attendee_count)
        
        # Calculate averages
        avg_duration = sum(duration_stats) / len(duration_stats) if duration_stats else 0
        avg_attendees = sum(attendee_stats) / len(attendee_stats) if attendee_stats else 0
        
        summary = {
            'total_meetings': total_meetings,
            'meeting_types': meeting_types,
            'sources': sources,
            'duration_statistics': {
                'average_minutes': round(avg_duration, 1),
                'total_samples': len(duration_stats),
                'range': f"{min(duration_stats) if duration_stats else 0}-{max(duration_stats) if duration_stats else 0} minutes"
            },
            'attendee_statistics': {
                'average_attendees': round(avg_attendees, 1),
                'total_samples': len(attendee_stats),
                'range': f"{min(attendee_stats) if attendee_stats else 0}-{max(attendee_stats) if attendee_stats else 0} attendees"
            }
        }
        
        return summary


def main():
    """Command line interface for Scenara Meeting Extractor"""
    parser = argparse.ArgumentParser(description="Scenara Meeting Extraction Tool")
    parser.add_argument('--source', choices=['local', 'mevals', 'graph', 'scenarios', 'all'], 
                       default='all', help='Meeting data source to extract from')
    parser.add_argument('--output', help='Output filename for extracted meetings')
    parser.add_argument('--days-back', type=int, default=30, 
                       help='Days to look back for Graph API extraction')
    parser.add_argument('--days-forward', type=int, default=14,
                       help='Days to look forward for Graph API extraction')
    parser.add_argument('--list-sources', action='store_true',
                       help='List available meeting data sources')
    parser.add_argument('--summary-only', action='store_true',
                       help='Generate summary without saving full data')
    parser.add_argument('--file-path', help='Specific local JSON file path to extract from')
    
    args = parser.parse_args()
    
    # Initialize extractor
    extractor = ScenearaMeetingExtractor()
    
    # List sources if requested
    if args.list_sources:
        print("🔍 Available Meeting Data Sources:")
        print("=" * 50)
        sources = extractor.get_available_sources()
        
        for source_name, info in sources.items():
            status = "✅ Available" if info['available'] else "❌ Not Available"
            print(f"\n{source_name.replace('_', ' ').title()}: {status}")
            print(f"   Description: {info['description']}")
            
            if 'files' in info:
                print(f"   Files: {len(info['files'])} found")
                for file in info['files'][:3]:  # Show first 3 files
                    print(f"     - {Path(file).name}")
                if len(info['files']) > 3:
                    print(f"     ... and {len(info['files']) - 3} more")
            
            if 'path' in info:
                print(f"   Path: {info['path']}")
            
            if info.get('requires_auth'):
                print(f"   ⚠️  Requires authentication")
        
        return
    
    # Extract meetings
    all_meetings = []
    
    try:
        if args.source == 'local' or args.source == 'all':
            try:
                meetings = extractor.extract_from_local_json(args.file_path)
                all_meetings.extend(meetings)
            except Exception as e:
                print(f"⚠️ Local JSON extraction failed: {e}")
        
        if args.source == 'mevals' or args.source == 'all':
            try:
                meetings = extractor.extract_from_mevals()
                all_meetings.extend(meetings)
            except Exception as e:
                print(f"⚠️ MEvals extraction failed: {e}")
        
        if args.source == 'graph' or args.source == 'all':
            try:
                meetings = extractor.extract_from_graph_api(args.days_back, args.days_forward)
                all_meetings.extend(meetings)
            except Exception as e:
                print(f"⚠️ Graph API extraction failed: {e}")
        
        if args.source == 'scenarios' or args.source == 'all':
            try:
                meetings = extractor.extract_from_meeting_prep_scenarios()
                all_meetings.extend(meetings)
            except Exception as e:
                print(f"⚠️ Scenario extraction failed: {e}")
        
        # Remove duplicates (basic deduplication by ID)
        seen_ids = set()
        unique_meetings = []
        for meeting in all_meetings:
            meeting_id = meeting.get('id', str(hash(str(meeting))))
            if meeting_id not in seen_ids:
                seen_ids.add(meeting_id)
                unique_meetings.append(meeting)
        
        print(f"\n📊 Extraction Complete:")
        print(f"   Total meetings found: {len(all_meetings)}")
        print(f"   Unique meetings: {len(unique_meetings)}")
        
        # Generate summary
        summary = extractor.generate_meeting_summary(unique_meetings)
        
        print(f"\n📈 Meeting Summary:")
        print(f"   Meeting Types: {dict(list(summary['meeting_types'].items())[:5])}")
        print(f"   Sources: {summary['sources']}")
        print(f"   Average Duration: {summary['duration_statistics']['average_minutes']} minutes")
        print(f"   Average Attendees: {summary['attendee_statistics']['average_attendees']}")
        
        # Save unless summary-only
        if not args.summary_only:
            output_path = extractor.save_extracted_meetings(unique_meetings, args.output)
            print(f"\n💾 Full meeting data saved to: {output_path}")
        
    except Exception as e:
        print(f"❌ Extraction failed: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()