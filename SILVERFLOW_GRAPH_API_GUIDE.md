# SilverFlow Graph API Meeting Extraction Guide

## Overview

This guide documents how to properly use `SilverFlow/data/graph_get_meetings.py` for Microsoft Graph API calendar extraction, based on lessons learned from debugging the meeting extraction workflow.

## Quick Reference

### Location
- **Script**: `SilverFlow/data/graph_get_meetings.py`
- **Output**: `SilverFlow/data/out/graph_meetings.json` + `graph_meetings.md`

### Authentication
- **Method**: MSAL with Windows Broker (WAM) on Windows
- **Type**: Interactive authentication with Microsoft SSO
- **Platform**: 
  - Windows: Windows Broker enabled (automatic)
  - macOS/Linux: Device code flow or interactive browser (may require different auth)

## Command Line Usage

### Basic Formats

```bash
# Navigate to correct directory first
cd SilverFlow/data

# Option 1: Days forward (today only)
python graph_get_meetings.py 0 --select "subject,start,end,attendees" --max-events 50

# Option 2: Days back and forward (7 days each direction)
python graph_get_meetings.py -7 7 --max-events 200

# Option 3: ISO datetime (MOST RELIABLE for exact dates)
python graph_get_meetings.py "2025-10-28T00:00:00" "2025-10-29T00:00:00" --select "subject,start,end,attendees,organizer,bodyPreview,isOnlineMeeting" --max-events 100
```

### Key Parameters

- **`range`**: Either `<daysForward>`, `<daysBack> <daysForward>`, or `"<startISO>" "<endISO>"`
- **`--select`**: Fields to retrieve (comma-separated, no spaces)
  - Common: `subject,start,end,location,attendees,organizer,bodyPreview,isOnlineMeeting,onlineMeetingUrl`
- **`--max-events`**: Maximum meetings to fetch (default: 5000)
- **`--top`**: Page size for pagination (default: 50)
- **`--filter`**: OData filter expression (default: excludes cancelled and OOF)
- **`--tz`**: IANA timezone preference (defaults to user's timezone)

## Python Subprocess Integration

### ✅ CORRECT Method (Relative Path with CWD)

```python
import subprocess
import json
from pathlib import Path

# Use relative path when setting working directory
result = subprocess.run(
    [
        sys.executable,
        "graph_get_meetings.py",  # Relative to cwd
        "2025-10-28T00:00:00",
        "2025-10-29T00:00:00",
        "--select", "subject,start,end,location,attendees,organizer,bodyPreview,isOnlineMeeting",
        "--max-events", "100"
    ],
    cwd="SilverFlow/data",  # Set working directory
    capture_output=True,
    text=True
)

# Check for errors
if result.returncode != 0:
    print(f"Error: {result.stderr}")
else:
    print(result.stdout)

# Parse output file
output_file = Path("SilverFlow/data/out/graph_meetings.json")
with open(output_file, 'r', encoding='utf-8') as f:
    data = json.load(f)
    
print(f"Found {data['totalEvents']} meetings")
```

### ❌ WRONG Method (Causes Path Doubling)

```python
# DO NOT USE - Causes nested path error
silverflow_script = Path("SilverFlow/data/graph_get_meetings.py")
result = subprocess.run(
    [sys.executable, str(silverflow_script), "0"],  # Absolute path
    cwd=str(silverflow_script.parent),  # Sets cwd, making path relative
    ...
)
# Error: "Can't open 'SilverFlow/data/SilverFlow/data/graph_get_meetings.py'"
# Reason: Path becomes relative to cwd and doubles!
```

### Alternative Method (Absolute Path, No CWD)

```python
# Also works - use absolute path without setting cwd
script_path = Path("SilverFlow/data/graph_get_meetings.py").resolve()
result = subprocess.run(
    [
        sys.executable,
        str(script_path),
        "2025-10-28T00:00:00",
        "2025-10-29T00:00:00",
        "--select", "subject,start,end,attendees",
        "--max-events", "100"
    ],
    capture_output=True,
    text=True
)
```

## Date Range Best Practices

### ISO Datetime Format (Recommended)

**Why**: Most reliable for exact date boundaries

```bash
# Extract exactly October 28, 2025 (midnight to midnight)
python graph_get_meetings.py "2025-10-28T00:00:00" "2025-10-29T00:00:00"
```

**Advantages**:
- ✅ Exact date boundaries (no timezone ambiguity)
- ✅ Works consistently across platforms
- ✅ Easy to calculate programmatically
- ✅ No confusion about "today" at different times

### Days Forward/Backward

**Why**: Convenient for relative time ranges

```bash
# Today only
python graph_get_meetings.py 0

# This week (7 days back to 7 days forward)
python graph_get_meetings.py -7 7
```

**Caveats**:
- ⚠️ "Today" depends on current time and timezone
- ⚠️ May include late-night meetings from adjacent days
- ⚠️ UTC conversion can cause unexpected date boundaries

## Output Format

### JSON Structure

```json
{
  "generatedAt": "2025-10-28T04:38:46Z",
  "totalEvents": 8,
  "events": [
    {
      "subject": "Meeting Prep STCA Sync",
      "start": {
        "dateTime": "2025-10-28T11:35:00.0000000",
        "timeZone": "Asia/Shanghai"
      },
      "end": {
        "dateTime": "2025-10-28T13:00:00.0000000",
        "timeZone": "Asia/Shanghai"
      },
      "location": {
        "displayName": "Microsoft Teams Meeting"
      },
      "attendees": [
        {
          "type": "required",
          "emailAddress": {
            "name": "Mark Grimaldi",
            "address": "Mark.Grimaldi@microsoft.com"
          },
          "status": {
            "response": "organizer"
          }
        }
      ],
      "organizer": {
        "emailAddress": {
          "name": "Mark Grimaldi",
          "address": "Mark.Grimaldi@microsoft.com"
        }
      },
      "bodyPreview": "Meeting description...",
      "isOnlineMeeting": true,
      "onlineMeetingUrl": "https://teams.microsoft.com/..."
    }
  ]
}
```

### Markdown Output

Human-readable format with meeting list, times, organizers, and attendee counts.

## Common Issues and Solutions

### Issue 1: "Can't open file" with nested path

**Symptom**: `Can't open 'SilverFlow/data/SilverFlow/data/graph_get_meetings.py'`

**Cause**: Using absolute path with `cwd` parameter causes path doubling

**Solution**: Use relative path when setting `cwd`:
```python
# Correct
subprocess.run([sys.executable, "graph_get_meetings.py"], cwd="SilverFlow/data")
```

### Issue 2: No meetings found for today

**Symptom**: Returns 0 meetings when you know you have meetings

**Causes**:
1. Cached calendar data is outdated
2. Timezone confusion (UTC vs local time)
3. Late-night meetings counted as next day

**Solutions**:
1. Use ISO datetime with explicit date boundaries
2. Check script output for actual date range queried
3. Increase date range to include adjacent days
4. Verify user's actual meeting count (they may have forgotten some!)

### Issue 3: Authentication failure on macOS

**Symptom**: MSAL authentication fails (no Windows Broker)

**Solution**: Script should fall back to device code flow or browser-based auth

**Workaround**: Run script manually in terminal to complete interactive auth

## Real-World Example: October 28, 2025

### User Report
- "I should have 5 meetings today"
- macOS branch reported 0 meetings

### Investigation
1. Cached data ended October 24 (4 days old)
2. Fallback to cache showed 0 meetings
3. Fresh Graph API extraction needed

### Solution
```bash
cd SilverFlow/data
python graph_get_meetings.py "2025-10-28T00:00:00" "2025-10-29T00:00:00" \
  --select "subject,start,end,location,attendees,organizer,bodyPreview,isOnlineMeeting" \
  --max-events 100
```

### Result
- **Found 8 meetings** (not 5!)
- User forgot 3 evening meetings (11:00pm - 12:00am)
- Complete attendee lists (4-29 people per meeting)
- Full metadata for classification pipeline

## Integration with get_todays_meetings.py

The `get_todays_meetings.py` script now properly calls SilverFlow Graph API:

```python
# Calculate today's date range in ISO format
today = datetime.now().date()
start_time = datetime.combine(today, datetime.min.time())
end_time = start_time + timedelta(days=1)

# Call SilverFlow script with subprocess
result = subprocess.run(
    [
        sys.executable,
        "graph_get_meetings.py",
        start_time.strftime("%Y-%m-%dT%H:%M:%S"),
        end_time.strftime("%Y-%m-%dT%H:%M:%S"),
        "--select", "subject,start,end,location,attendees,organizer,bodyPreview,isOnlineMeeting",
        "--max-events", "50"
    ],
    cwd="SilverFlow/data",
    capture_output=True,
    text=True
)

# Parse output and filter for today
output_file = Path("SilverFlow/data/out/graph_meetings.json")
# ... process and save to data/meetings/meetings_YYYY-MM-DD.json
```

## Cross-Platform Notes

### Windows
- ✅ MSAL with Windows Broker (seamless SSO)
- ✅ Uses `python` command
- ✅ PowerShell or CMD works

### macOS
- ⚠️ No Windows Broker (different auth flow)
- ✅ Uses `python3` command
- ✅ Bash or Zsh terminal
- 🔧 May require interactive browser authentication

### Linux
- ⚠️ No Windows Broker (different auth flow)
- ✅ Uses `python3` command
- ✅ May require device code flow for headless servers

## Field Selection Guide

### Essential Fields
- `subject` - Meeting title
- `start` - Start time with timezone
- `end` - End time with timezone
- `attendees` - Complete attendee list (critical for filtering)

### Recommended Fields
- `organizer` - Meeting organizer
- `bodyPreview` - Meeting description
- `location` - Physical or virtual location
- `isOnlineMeeting` - Teams/online flag
- `onlineMeetingUrl` - Teams link

### Advanced Fields
- `type` - Meeting type
- `responseStatus` - User's response
- `showAs` - Calendar status (busy/free/etc)
- `seriesMasterId` - Recurring meeting identifier
- `webLink` - Outlook web link

## Performance Tips

1. **Use `--max-events`** to limit results for faster queries
2. **Narrow date ranges** with ISO datetime for specific days
3. **Select only needed fields** to reduce JSON size
4. **Cache results** if querying the same range multiple times
5. **Pagination** is automatic (don't worry about it)

## Security Notes

- ✅ Uses Microsoft MSAL library (official)
- ✅ Windows Broker provides secure SSO
- ✅ No credentials stored in code
- ✅ Token caching follows Microsoft best practices
- ⚠️ Requires user consent for Calendar.Read scope

## Next Steps

1. Test on macOS to verify cross-platform authentication
2. Implement classification pipeline for extracted meetings
3. Compare results between Windows and macOS
4. Document platform-specific authentication differences
5. Consider implementing device code flow for non-Windows platforms

## Resources

- **Script Location**: `SilverFlow/data/graph_get_meetings.py`
- **Documentation**: This file
- **GitHub**: https://github.com/cylin-ms/scenara
- **Microsoft Graph**: https://docs.microsoft.com/en-us/graph/api/calendar-list-events
