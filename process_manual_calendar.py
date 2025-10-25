#!/usr/bin/env python3
"""
Process manually downloaded calendar data from Microsoft Graph Explorer
"""

import json
import os
from datetime import datetime

def process_manual_calendar_data():
    """Process calendar data from Graph Explorer"""
    # Check for the new 50 events file first, then fall back to the original
    input_files = ["my_calendar_events_50.json", "my_calendar_events.json"]
    input_file = None
    
    for file in input_files:
        if os.path.exists(file):
            input_file = file
            break
    
    if not input_file:
        print(f"❌ No calendar events file found!")
        print("Please follow the manual extraction steps:")
        print("1. Go to: https://developer.microsoft.com/graph/graph-explorer")
        print("2. Query: https://graph.microsoft.com/v1.0/me/events?$top=50")
        print("3. Save response as: my_calendar_events_50.json")
        return
    
    print(f"📂 Using calendar data from: {input_file}")
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if 'value' not in data:
            print("❌ Invalid JSON format. Expected 'value' field from Graph API response.")
            return
        
        events = data['value']
        print(f"📅 Found {len(events)} calendar events")
        
        # Format for Meeting PromptCoT
        scenarios = []
        for i, event in enumerate(events):
            # Extract attendees
            attendees = []
            if event.get('attendees'):
                for attendee in event['attendees']:
                    if attendee.get('emailAddress'):
                        attendees.append(attendee['emailAddress'].get('name', 'Unknown'))
            
            # Calculate duration
            duration_minutes = 60
            if event.get('start') and event.get('end'):
                try:
                    start_time = datetime.fromisoformat(event['start']['dateTime'].replace('Z', '+00:00'))
                    end_time = datetime.fromisoformat(event['end']['dateTime'].replace('Z', '+00:00'))
                    duration_minutes = int((end_time - start_time).total_seconds() / 60)
                except:
                    pass
            
            # Classify meeting type
            subject = event.get('subject', '') or ''
            subject_lower = subject.lower() if subject else ''
            
            if any(word in subject_lower for word in ['design', 'architecture', 'technical', 'engineering', 'code', 'api']):
                meeting_type = 'Technical Design Review'
            elif any(word in subject_lower for word in ['strategy', 'roadmap', 'planning', 'product', 'feature']):
                meeting_type = 'Product Strategy Session'
            elif any(word in subject_lower for word in ['retro', 'retrospective', 'sprint', 'standup', 'scrum']):
                meeting_type = 'Team Retrospective'
            elif any(word in subject_lower for word in ['1:1', 'one-on-one', 'review', 'performance', 'feedback']):
                meeting_type = 'Performance Review'
            elif any(word in subject_lower for word in ['sync', 'standup', 'status', 'update', 'checkpoint']):
                meeting_type = 'Project Status Update'
            elif any(word in subject_lower for word in ['budget', 'financial', 'cost', 'investment']):
                meeting_type = 'Budget Planning Meeting'
            elif any(word in subject_lower for word in ['customer', 'client', 'user', 'discovery', 'interview']):
                meeting_type = 'Customer Discovery Call'
            elif any(word in subject_lower for word in ['training', 'workshop', 'learning', 'onboarding']):
                meeting_type = 'Training Session'
            elif any(word in subject_lower for word in ['vendor', 'supplier', 'procurement', 'evaluation']):
                meeting_type = 'Vendor Evaluation'
            else:
                meeting_type = 'General Business Meeting'
            
            # Generate scenario
            scenario = {
                'id': f"real_calendar_{i+1:03d}",
                'source': 'microsoft_calendar_manual',
                'context': {
                    'subject': event.get('subject', 'No Subject') or 'No Subject',
                    'description': event.get('bodyPreview', '') or '',
                    'attendees': attendees,
                    'attendee_count': len(attendees),
                    'duration_minutes': duration_minutes,
                    'start_time': event.get('start', {}).get('dateTime', '') if event.get('start') else '',
                    'end_time': event.get('end', {}).get('dateTime', '') if event.get('end') else '',
                    'is_online_meeting': event.get('isOnlineMeeting', False),
                    'importance': event.get('importance', 'normal') or 'normal',
                    'organizer': event.get('organizer', {}).get('emailAddress', {}).get('name', 'Unknown') if event.get('organizer') else 'Unknown',
                    'location': event.get('location', {}).get('displayName', '') if event.get('location') else '',
                },
                'meeting_type': meeting_type,
                'preparation_requirements': [
                    "Review agenda and objectives",
                    "Prepare meeting materials" if duration_minutes > 60 else "Review key points",
                    "Coordinate with attendees" if len(attendees) > 5 else "Check attendee availability"
                ],
                'complexity': 'critical' if len(attendees) > 10 or duration_minutes > 180 else 'high' if len(attendees) > 8 or duration_minutes > 120 else 'medium' if len(attendees) > 3 or duration_minutes > 60 else 'low',
                'quality_score': min(8.5 + (len(attendees) * 0.1) + (1.0 if duration_minutes > 60 else 0) + (0.5 if event.get('isOnlineMeeting') else 0), 10.0),
                'extracted_date': datetime.now().isoformat()
            }
            
            scenarios.append(scenario)
        
        # Save formatted data
        os.makedirs("meeting_prep_data", exist_ok=True)
        output_file = "meeting_prep_data/real_calendar_scenarios.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(scenarios, f, indent=2, ensure_ascii=False)
        
        # Print summary
        avg_quality = sum(s['quality_score'] for s in scenarios) / len(scenarios)
        meeting_types = {}
        for s in scenarios:
            mt = s['meeting_type']
            meeting_types[mt] = meeting_types.get(mt, 0) + 1
        
        print(f"✅ Processed {len(scenarios)} real meeting scenarios")
        print(f"💾 Saved to: {output_file}")
        print(f"📊 Average quality score: {avg_quality:.2f}/10.0")
        print(f"🏢 Meeting types found: {len(meeting_types)}")
        
        for mt, count in meeting_types.items():
            print(f"  - {mt}: {count}")
        
        print("\n🎯 SUCCESS! Your real calendar data is ready.")
        print("Next steps:")
        print("1. Run: python update_training_data.py")
        print("2. Launch: streamlit run meeting_data_explorer.py")
        print("3. Access: http://localhost:8501")
        
    except Exception as e:
        print(f"❌ Error processing calendar data: {e}")

if __name__ == "__main__":
    process_manual_calendar_data()
