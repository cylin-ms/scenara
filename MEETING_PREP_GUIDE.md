# Meeting Importance Tracker & Focus Time Scheduler

Track important meetings and automatically schedule focus time for preparation.

## 🎯 Overview

This toolkit helps you:
1. **Identify important meetings** based on multiple criteria (executives, customers, large meetings, etc.)
2. **Flag meetings requiring preparation** with estimated prep time
3. **Schedule focus time blocks** automatically in your calendar
4. **Get daily digests** of upcoming meetings and prep needs

## 📋 Tools Available

### 1. `track_important_meetings.py`
Analyzes your calendar to identify important meetings and estimate preparation time.

**Usage:**
```bash
# Analyze meetings for a date range
python3 track_important_meetings.py --from-date 2025-10-01 --to-date 2025-10-31

# Save report to file
python3 track_important_meetings.py --output important_meetings_report.txt

# Output as JSON for programmatic use
python3 track_important_meetings.py --json --output analysis.json
```

**Features:**
- Importance scoring based on:
  - Executive attendees (C-level, VPs)
  - External attendees (customers, partners)
  - Large meetings (10+ people)
  - Meeting type (reviews, approvals, presentations)
  - Decision-making meetings
- Preparation time estimation (15-180 minutes per meeting)
- Categorized reports with actionable insights

### 2. `schedule_focus_time.py`
Automatically finds time slots and schedules focus blocks for meeting preparation.

**Usage:**
```bash
# Schedule focus time for next 2 weeks
python3 schedule_focus_time.py

# Export to iCalendar format (import to Outlook/Google Calendar)
python3 schedule_focus_time.py --export-ical meeting_prep.ics

# Export to JSON
python3 schedule_focus_time.py --json focus_blocks.json

# Specific date range
python3 schedule_focus_time.py --from-date 2025-11-01 --to-date 2025-11-15
```

**Features:**
- Finds available time slots in your calendar
- Schedules prep time the day before meetings
- Exports to .ics format for calendar import
- Groups multiple meeting preps into single blocks

### 3. `daily_meeting_digest.py`
Quick daily overview of meetings and preparation needs.

**Usage:**
```bash
# Today's digest
python3 daily_meeting_digest.py

# Specific date
python3 daily_meeting_digest.py --date 2025-11-06
```

**Shows:**
- Meeting count and total time
- Important meetings highlighted
- Prep time requirements
- Best time slots for focused work
- Tomorrow's prep preview

## 🔍 How It Works

### Importance Scoring

Meetings are scored based on weighted criteria:

| Criterion | Weight | Example |
|-----------|--------|---------|
| Executive Attendee | 25 | VP, CVP, C-level |
| External Attendee | 20 | Customer, partner |
| Large Meeting | 15 | 10+ attendees |
| Presentation | 20 | Demo, showcase |
| Decision Making | 25 | Review, approval, planning |
| Cross-team | 15 | Multiple organizations |
| Direct Manager | 15 | Your manager present |

**Score Ranges:**
- 80+: Very important (requires significant prep)
- 50-79: Important (moderate prep)
- 30-49: Somewhat important (light prep)
- <30: Standard meeting

### Preparation Time Estimation

Based on meeting type and importance:

| Meeting Type | Prep Time |
|--------------|-----------|
| Executive Briefing | 120 min |
| Customer Meeting | 90 min |
| Product Demo | 90 min |
| Technical Design Review | 60 min |
| Project Planning | 45 min |
| Performance Review | 45 min |
| All Hands | 30 min |
| Interview | 30 min |

## 📊 Sample Output

### Important Meetings Report
```
================================================================================
🔴 HIGH IMPORTANCE MEETINGS
================================================================================

1. Executive Strategy Session
   📅 2025-11-10 14:00
   🎯 Importance Score: 85
   👥 Attendees: 12
   ⏰ Prep Time Needed: 90 minutes
   💡 Why Important:
      • Executive attendee(s): 2
      • Large meeting: 12 attendees
      • Keyword 'strategy' in subject

2. Customer Demo: AI Features
   📅 2025-11-12 10:00
   🎯 Importance Score: 75
   👥 Attendees: 8
   ⏰ Prep Time Needed: 90 minutes
   💡 Why Important:
      • External attendee(s): 4
      • Presentation/demo meeting
```

### Focus Time Schedule
```
================================================================================
🎯 SCHEDULED FOCUS TIME BLOCKS
================================================================================

1. Wednesday, November 09, 2025
   ⏰ 08:00 - 09:30 (90 minutes)
   📝 Prepare for 1 meeting(s) on November 10
   📋 Meetings to prepare:
      • 14:00 Executive Strategy Session (90min)

2. Monday, November 11, 2025
   ⏰ 14:00 - 15:30 (90 minutes)
   📝 Prepare for 1 meeting(s) on November 12
   📋 Meetings to prepare:
      • 10:00 Customer Demo: AI Features (90min)
```

### Daily Digest
```
================================================================================
📅 DAILY MEETING DIGEST - Wednesday, November 06, 2025
================================================================================

📊 Summary:
   • Total Meetings: 5
   • Important Meetings: 2
   • Requiring Prep: 2
   • Total Meeting Time: 3.5 hours
   • Total Prep Time: 90 minutes

⏰ PREP ALERT:
   You should have blocked 90 minutes yesterday (November 05)
   for meeting preparation. If not done, prep early today!

================================================================================
📅 TODAY'S SCHEDULE
================================================================================

1. 09:00-09:30 (30min) | Team Standup
   👥 8 attendees | 🌐 Online

2. 10:00-11:00 (60min) | Customer Requirements Review
   👥 6 attendees | 🔴 Important (Score: 55) | ⏰ 60min prep needed
   💡 External attendee(s): 3, Keyword 'review' in subject

3. 14:00-15:00 (60min) | Technical Design Review
   👥 10 attendees | 🔴 Important (Score: 45) | ⏰ 30min prep needed
   💡 Large meeting: 10 attendees, Keyword 'review' in subject

================================================================================
💡 RECOMMENDATIONS
================================================================================

🎯 Best time for focused work:
   11:00-14:00 (180 minutes)

⚠️  Preparation Reminder:
   First important meeting: 10:00 - Customer Requirements Review
   Suggested prep: 60 minutes before the meeting
   ✅ You have 60 minutes before first meeting - use for prep!
```

## 🎨 Customization

### Modify Importance Weights

Edit `track_important_meetings.py`:

```python
IMPORTANCE_WEIGHTS = {
    'executive_attendee': 25,      # Increase for more exec focus
    'external_attendee': 20,       # Increase for customer focus
    'large_meeting': 15,
    'presentation': 20,
    'decision_making': 25,
    # Add custom criteria...
}
```

### Adjust Prep Time Estimates

```python
PREP_REQUIRED_TYPES = {
    'Executive Briefing': 120,     # Modify time in minutes
    'Customer Meeting': 90,
    'Your Custom Type': 45,        # Add new types
}
```

### Customize Keywords

```python
HIGH_IMPORTANCE_KEYWORDS = {
    'executive': ['exec', 'vp', 'cvp', 'your-exec-title'],
    'external': ['customer', 'client', 'your-partner-name'],
    'decision': ['review', 'approval', 'your-decision-keyword'],
}
```

## 📥 Calendar Integration

### Import Focus Time to Outlook
1. Run: `python3 schedule_focus_time.py --export-ical prep_time.ics`
2. Open Outlook → File → Open & Export → Import/Export
3. Select "Import an iCalendar (.ics) or vCalendar file"
4. Choose `prep_time.ics`
5. Click "Import"

### Import to Google Calendar
1. Generate .ics file as above
2. Open Google Calendar
3. Click "+" next to "Other calendars"
4. Select "Import"
5. Choose `prep_time.ics`
6. Select target calendar
7. Click "Import"

## 🔄 Automation

### Daily Digest Email (macOS/Linux)
Add to crontab to run every morning at 7 AM:

```bash
0 7 * * * cd /path/to/scenara && python3 daily_meeting_digest.py | mail -s "Daily Meeting Digest" your@email.com
```

### Weekly Focus Time Updates
Generate weekly focus blocks every Monday:

```bash
0 8 * * 1 cd /path/to/scenara && python3 schedule_focus_time.py --export-ical ~/Desktop/weekly_prep.ics
```

## 📊 Data Requirements

### Input Data Format
Uses `my_calendar_events_complete_attendees.json` with structure:
```json
{
  "metadata": {
    "total_events": 267,
    "date_range": {"start": "2025-04-01", "end": "2025-10-24"}
  },
  "events": [
    {
      "subject": "Meeting Title",
      "start": {"dateTime": "2025-11-06T09:00:00"},
      "end": {"dateTime": "2025-11-06T10:00:00"},
      "attendees": [...],
      "organizer": {...},
      "isOnlineMeeting": true
    }
  ]
}
```

### Updating Calendar Data
To get fresh data:
1. On Windows DevBox: Run `SilverFlow/data/graph_get_meetings.py`
2. Copy updated JSON to macOS
3. Re-run analysis tools

## 🛠️ Troubleshooting

### No meetings found
- Check date range in calendar data file
- Verify JSON file exists: `my_calendar_events_complete_attendees.json`
- Run with `--from-date` and `--to-date` matching your data range

### Importance scores seem wrong
- Review and customize `IMPORTANCE_WEIGHTS`
- Add domain-specific keywords to `HIGH_IMPORTANCE_KEYWORDS`
- Check attendee email addresses (external detection uses @microsoft.com)

### Focus time blocks overlap meetings
- Scheduler finds gaps but may need manual adjustment
- Review generated .ics before importing
- Manually adjust times in calendar after import

## 💡 Pro Tips

1. **Run daily digest every morning** to start your day prepared
2. **Import focus blocks weekly** to stay ahead of prep needs
3. **Customize keywords** for your organization's terminology
4. **Adjust prep times** based on your actual experience
5. **Block travel time** separately from meeting prep
6. **Use JSON output** to integrate with other tools

## 📁 Files Generated

| File | Description |
|------|-------------|
| `important_meetings_report.txt` | Text report of analysis |
| `meeting_prep_focus_time.ics` | iCalendar file for import |
| `meeting_prep_focus_blocks.json` | JSON with focus blocks |
| `analysis.json` | Full analysis results |

## 🔗 Related Tools

- `track_important_meetings.py` - Main analysis engine
- `schedule_focus_time.py` - Focus time scheduler
- `daily_meeting_digest.py` - Daily summary
- `classify_todays_meetings.py` - Meeting type classification
- `tools/collaborator_discovery.py` - Relationship analysis

## 📝 Version

**Version:** 1.0.0  
**Created:** November 6, 2025  
**Part of:** Scenara 2.0 Meeting Intelligence System

## 🤝 Integration with Scenara

These tools are part of the larger Scenara 2.0 ecosystem:
- Meeting classification feeds into importance scoring
- Collaborator rankings inform executive/important person detection
- Focus time recommendations integrate with Priority Calendar
- Daily logs capture preparation effectiveness

---

**Next Steps:**
1. Run `python3 track_important_meetings.py` to see your important meetings
2. Run `python3 schedule_focus_time.py --export-ical prep.ics` to create focus blocks
3. Import `prep.ics` to your calendar
4. Start your day with `python3 daily_meeting_digest.py`

🎯 **Focus on what matters. Prepare for success.**
