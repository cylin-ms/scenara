"""Process today's meetings from SilverFlow output"""
import json
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo

# Load SilverFlow data
with open('SilverFlow/data/out/graph_meetings.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Get user's timezone from the data
user_timezone = data.get('timeZone', 'Asia/Shanghai')
print(f"User timezone: {user_timezone}")

# Extract events from SilverFlow format
all_meetings = data.get('events', [])

# Filter for October 29 meetings using proper timezone conversion
# Convert all times to user's local timezone and filter by calendar date
target_date = datetime(2025, 10, 29).date()
oct29_meetings = []

for meeting in all_meetings:
    start_time_str = meeting.get('start', {}).get('dateTime', '')
    if not start_time_str:
        continue
    
    # Parse the datetime string (format: 2025-10-29T08:00:00.0000000)
    # Remove the fractional seconds part for parsing
    clean_time_str = start_time_str.split('.')[0]
    
    # Parse as naive datetime (already in local timezone from Graph API)
    meeting_dt = datetime.fromisoformat(clean_time_str)
    
    # Add timezone info (Graph API returns times in the user's local timezone)
    meeting_dt_local = meeting_dt.replace(tzinfo=ZoneInfo(user_timezone))
    
    # Check if this meeting's date matches our target date in the user's timezone
    if meeting_dt_local.date() == target_date:
        oct29_meetings.append(meeting)

print(f'Found {len(oct29_meetings)} meetings for October 29, 2025')

# Save to standard location
output_dir = Path('data/meetings')
output_dir.mkdir(parents=True, exist_ok=True)
output_file = output_dir / 'meetings_2025-10-29.json'

output_data = {
    'extraction_date': datetime.now().isoformat(),
    'date': '2025-10-29',
    'total_meetings': len(oct29_meetings),
    'meetings': oct29_meetings
}

with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(output_data, f, indent=2, ensure_ascii=False)

print(f'\nSaved to: {output_file}')
print('\nMeetings for October 29, 2025:')
for i, m in enumerate(oct29_meetings, 1):
    subject = m.get('subject', 'No subject')
    start = m['start']['dateTime'][:16]
    attendees = len(m.get('attendees', []))
    print(f'  {i}. {subject} ({start}) - {attendees} attendees')
