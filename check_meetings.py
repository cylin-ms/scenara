"""Check all extracted meetings"""
import json

data = json.load(open('SilverFlow/data/out/graph_meetings.json', 'r', encoding='utf-8'))
events = data['events']

print(f'Total events extracted: {len(events)}')
print(f'Time range: {data["startUtc"]} to {data["endUtc"]}')
print(f'Timezone: {data["timeZone"]}')
print('\nAll events:')

for i, e in enumerate(events, 1):
    start = e['start']['dateTime']
    subject = e['subject']
    attendees = len(e.get('attendees', []))
    print(f'{i}. {subject}')
    print(f'   Start: {start}')
    print(f'   Attendees: {attendees}')
    print()

print(f'\nEvents starting with 2025-10-29: {sum(1 for e in events if e["start"]["dateTime"].startswith("2025-10-29"))}')
print(f'Events starting with 2025-10-30: {sum(1 for e in events if e["start"]["dateTime"].startswith("2025-10-30"))}')
