#!/usr/bin/env python3
"""Debug why Yanchao Li is still appearing in hybrid algorithm results"""

import json
from collections import defaultdict

# Load the real data to analyze Yanchao Li specifically
with open('data/real_meetings/50_calendar_events_20241024_145355.json', 'r') as f:
    calendar_data = json.load(f)

print("🔍 DEBUGGING YANCHAO LI IN HYBRID ALGORITHM")
print("=" * 60)

# Track Yanchao Li specifically
yanchao_meetings = []
for event in calendar_data:
    attendees = event['context'].get('attendees', [])
    if 'Yanchao Li' in attendees:
        attendee_count = len(attendees)
        subject = event['context'].get('subject', '')
        start_time = event['context'].get('start_time', '')
        organizer = event['context'].get('organizer', 'Unknown')
        
        # Categorize meeting size
        if attendee_count <= 10:
            size_cat = "🟢 Small"
        elif attendee_count <= 50:
            size_cat = "🟡 Medium" 
        else:
            size_cat = "🔴 Large"
        
        yanchao_meetings.append({
            'subject': subject,
            'attendees': attendee_count,
            'size_cat': size_cat,
            'organizer': organizer,
            'start_time': start_time,
            'time_period': start_time[:7] if start_time else 'unknown'
        })

print(f"👤 YANCHAO LI MEETING ANALYSIS:")
print(f"   📊 Total meetings: {len(yanchao_meetings)}")

# Group by time period
time_periods = defaultdict(list)
for meeting in yanchao_meetings:
    time_periods[meeting['time_period']].append(meeting)

print(f"   📅 Time periods: {len(time_periods)} ({list(time_periods.keys())})")

# Count by size
small_count = sum(1 for m in yanchao_meetings if m['attendees'] <= 10)
medium_count = sum(1 for m in yanchao_meetings if 11 <= m['attendees'] <= 50)
large_count = sum(1 for m in yanchao_meetings if m['attendees'] > 50)

print(f"   🟢 Small (≤10): {small_count}")
print(f"   🟡 Medium (11-50): {medium_count}")
print(f"   🔴 Large (>50): {large_count}")

# Calculate hybrid algorithm score
score = 0
score += small_count * 5      # Small meetings highly weighted
score += medium_count * 2     # Medium meetings moderately weighted  
score += large_count * 0.5    # Large meetings low weight
score += len(time_periods) * 2   # Multiple time periods

print(f"\n🔢 HYBRID ALGORITHM SCORE BREAKDOWN:")
print(f"   Small meetings: {small_count} × 5 = {small_count * 5}")
print(f"   Medium meetings: {medium_count} × 2 = {medium_count * 2}")
print(f"   Large meetings: {large_count} × 0.5 = {large_count * 0.5}")
print(f"   Time periods: {len(time_periods)} × 2 = {len(time_periods) * 2}")
print(f"   Time period bonus: +5 = 5")
print(f"   💯 TOTAL SCORE: {score + 5}")

print(f"\n📋 DETAILED MEETINGS:")
for i, meeting in enumerate(yanchao_meetings, 1):
    organizer_marker = "👤" if meeting['organizer'] == 'Chin-Yew Lin' else "🏢"
    print(f"   {i:2d}. {meeting['size_cat']} {organizer_marker} ({meeting['attendees']:3d}) {meeting['subject'][:50]}...")

print(f"\n❌ THE PROBLEM:")
print(f"   • Yanchao Li gets high score from small meetings (6 × 5 = 30 points)")
print(f"   • Multiple time periods boost (4 × 2 = 8 points)")  
print(f"   • Time period bonus (+5 points)")
print(f"   • Total: 30 + 8 + 5 = 43+ points")
print(f"   • BUT: Average meeting size is {sum(m['attendees'] for m in yanchao_meetings) / len(yanchao_meetings):.1f} people")
print(f"   • This is NOT a genuine collaborator - it's someone in mixed large/small meetings")

print(f"\n✅ SOLUTION:")
print(f"   • Need to check if the 'small meetings' are actually genuine or just large meetings with few attendees")
print(f"   • Should filter out people who appear primarily in event/conference style meetings")
print(f"   • Need better 'system meeting' detection based on meeting subjects")