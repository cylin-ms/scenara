#!/usr/bin/env python3
"""
Simple Calendar Data Extractor
Uses Microsoft Graph Explorer technique for easy authentication
"""

import json
import webbrowser
import time
import os
from datetime import datetime, timedelta

def get_manual_auth_instructions():
    """Provide manual authentication instructions"""
    print("🔐 Microsoft Calendar Data Extraction")
    print("=" * 50)
    print()
    print("Since automated authentication is having issues, let's use a manual approach:")
    print()
    print("📋 STEP 1: Get Your Calendar Data Manually")
    print("-" * 40)
    print("1. Open Microsoft Graph Explorer: https://developer.microsoft.com/graph/graph-explorer")
    print("2. Sign in with your Microsoft account")
    print("3. In the query box, paste this URL:")
    print("   https://graph.microsoft.com/v1.0/me/events?$top=100&$orderby=start/dateTime desc")
    print("4. Click 'Run Query'")
    print("5. Copy the JSON response")
    print()
    print("📋 STEP 2: Save Your Data")
    print("-" * 25)
    print("6. Create a file called 'my_calendar_events.json' in this directory")
    print("7. Paste the JSON response into that file")
    print("8. Run: python3 process_manual_calendar.py")
    print()
    print("🌐 Opening Graph Explorer now...")
    
    try:
        webbrowser.open("https://developer.microsoft.com/graph/graph-explorer")
        time.sleep(2)
        print("✅ Graph Explorer should be opening in your browser")
    except:
        print("⚠️ Please manually open: https://developer.microsoft.com/graph/graph-explorer")
    
    print()
    print("📝 Query to use in Graph Explorer:")
    print("https://graph.microsoft.com/v1.0/me/events?$top=100&$orderby=start/dateTime desc&$filter=start/dateTime ge '2024-07-01T00:00:00Z'")
    print()
    print("💡 TIP: This query gets your last 100 calendar events since July 2024")

def create_processor_script():
    """Create a script to process manually downloaded calendar data"""
    processor_code = '''#!/usr/bin/env python3
"""
Process manually downloaded calendar data from Microsoft Graph Explorer
"""

import json
import os
from datetime import datetime

def process_manual_calendar_data():
    """Process calendar data from Graph Explorer"""
    input_file = "my_calendar_events.json"
    
    if not os.path.exists(input_file):
        print(f"❌ File {input_file} not found!")
        print("Please follow the manual extraction steps:")
        print("1. Go to: https://developer.microsoft.com/graph/graph-explorer")
        print("2. Query: https://graph.microsoft.com/v1.0/me/events?$top=100")
        print("3. Save response as: my_calendar_events.json")
        return
    
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
            subject = event.get('subject', '').lower()
            if any(word in subject for word in ['design', 'architecture', 'technical']):
                meeting_type = 'Technical Design Review'
            elif any(word in subject for word in ['strategy', 'roadmap', 'planning']):
                meeting_type = 'Product Strategy Session'
            elif any(word in subject for word in ['retro', 'retrospective', 'sprint']):
                meeting_type = 'Team Retrospective'
            elif any(word in subject for word in ['1:1', 'one-on-one', 'review']):
                meeting_type = 'Performance Review'
            elif any(word in subject for word in ['sync', 'standup', 'status']):
                meeting_type = 'Project Status Update'
            else:
                meeting_type = 'General Business Meeting'
            
            # Generate scenario
            scenario = {
                'id': f"real_calendar_{i+1:03d}",
                'source': 'microsoft_calendar_manual',
                'context': {
                    'subject': event.get('subject', 'No Subject'),
                    'description': event.get('bodyPreview', ''),
                    'attendees': attendees,
                    'attendee_count': len(attendees),
                    'duration_minutes': duration_minutes,
                    'start_time': event.get('start', {}).get('dateTime', ''),
                    'is_online_meeting': event.get('isOnlineMeeting', False),
                    'importance': event.get('importance', 'normal'),
                },
                'meeting_type': meeting_type,
                'preparation_requirements': [
                    "Review agenda and objectives",
                    "Prepare meeting materials" if duration_minutes > 60 else "Review key points",
                    "Coordinate with attendees" if len(attendees) > 5 else "Check attendee availability"
                ],
                'complexity': 'high' if len(attendees) > 8 or duration_minutes > 120 else 'medium' if len(attendees) > 3 else 'low',
                'quality_score': min(8.0 + (len(attendees) * 0.1) + (1.0 if duration_minutes > 60 else 0), 10.0),
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
        
        print("\\n🎯 SUCCESS! Your real calendar data is ready.")
        print("Next steps:")
        print("1. Run: python update_training_data.py")
        print("2. Launch: streamlit run meeting_data_explorer.py")
        print("3. Access: http://localhost:8501")
        
    except Exception as e:
        print(f"❌ Error processing calendar data: {e}")

if __name__ == "__main__":
    process_manual_calendar_data()
'''
    
    with open("process_manual_calendar.py", "w", encoding="utf-8") as f:
        f.write(processor_code)
    
    print("📝 Created process_manual_calendar.py")

def main():
    get_manual_auth_instructions()
    create_processor_script()
    
    print()
    print("🎯 SUMMARY:")
    print("1. ✅ Graph Explorer is opening in your browser")
    print("2. ✅ Query URL is provided above")
    print("3. ✅ Processor script created: process_manual_calendar.py")
    print()
    print("Once you have your calendar data:")
    print("👉 python3 process_manual_calendar.py")

if __name__ == "__main__":
    main()