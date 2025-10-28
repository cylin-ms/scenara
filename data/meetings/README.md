# Meeting Extraction and Classification Workflow

## Overview
This document describes the workflow for extracting daily meetings and running meeting type classification across different platforms (Windows and macOS).

## Quick Start

### Extract Today's Meetings
```bash
python get_todays_meetings.py
```

This will:
- Extract today's meetings from cached calendar data or Microsoft Graph API
- Save to `data/meetings/meetings_YYYY-MM-DD.json`
- Display a summary of meetings found

### Run Meeting Classification
```bash
python classify_todays_meetings.py
```

This will:
- Load today's meetings from `data/meetings/`
- Classify each meeting using the meeting classifier (31+ types)
- Save results with classifications to `data/meetings/meetings_YYYY-MM-DD_classified.json`

## Directory Structure

```
data/
  meetings/
    meetings_2025-10-28.json              # Raw meeting data
    meetings_2025-10-28_classified.json   # With classifications
    README.md                             # This file
```

## File Format

### Raw Meeting Data (`meetings_YYYY-MM-DD.json`)
```json
{
  "metadata": {
    "extraction_date": "2025-10-28T12:12:55",
    "target_date": "2025-10-28",
    "total_meetings": 5,
    "source": "Microsoft Graph API via SilverFlow"
  },
  "meetings": [
    {
      "subject": "Team Sync",
      "start": {"dateTime": "2025-10-28T09:00:00"},
      "end": {"dateTime": "2025-10-28T10:00:00"},
      "attendees": [...],
      "organizer": {...},
      "location": {...},
      "isOnlineMeeting": true
    }
  ]
}
```

### Classified Meeting Data (`meetings_YYYY-MM-DD_classified.json`)
```json
{
  "metadata": {
    "extraction_date": "2025-10-28T12:12:55",
    "classification_date": "2025-10-28T12:15:30",
    "target_date": "2025-10-28",
    "total_meetings": 5,
    "classifier_version": "v8.0",
    "llm_provider": "ollama",
    "llm_model": "gpt-oss:20b"
  },
  "meetings": [
    {
      "subject": "Team Sync",
      "start": {"dateTime": "2025-10-28T09:00:00"},
      "classification": {
        "type": "Team Status Update",
        "confidence": 0.92,
        "reasoning": "Regular team synchronization meeting"
      },
      ...
    }
  ]
}
```

## Platform-Specific Instructions

### Windows
```powershell
# Extract today's meetings
python get_todays_meetings.py

# Classify meetings
python classify_todays_meetings.py

# View results
Get-Content "data/meetings/meetings_$(Get-Date -Format 'yyyy-MM-dd')_classified.json" | ConvertFrom-Json
```

### macOS/Linux
```bash
# Extract today's meetings
python3 get_todays_meetings.py

# Classify meetings
python3 classify_todays_meetings.py

# View results
cat "data/meetings/meetings_$(date +%Y-%m-%d)_classified.json" | jq '.'
```

## Data Sources

### Primary: Microsoft Graph API
- Requires authentication via SilverFlow
- Real-time data extraction
- Includes complete attendee metadata

### Fallback: Cached Calendar Data
- Uses `my_calendar_events_complete_attendees.json`
- Fast, no API calls required
- May not include very recent meetings

## Meeting Classification Types

The classifier can identify 31+ meeting types including:
- Team Status Update
- One-on-One Meeting
- Project Planning Meeting
- Technical Design Review
- Customer Meeting
- Executive Briefing
- Training Session
- Interview
- And many more...

See `tools/meeting_classifier.py` or `COLLABORATOR_DETECTION_ALGORITHM.md` for complete list.

## Workflow for Cross-Platform Development

### 1. Windows Development
```powershell
# Extract and classify
python get_todays_meetings.py
python classify_todays_meetings.py

# Commit changes
git add data/meetings/
git add get_todays_meetings.py classify_todays_meetings.py
git commit -m "Add: Today's meetings extraction and classification"
git push origin master
```

### 2. Switch to macOS Branch
```bash
# On macOS
git checkout macos-dev
git pull origin master  # Merge latest changes

# Run classification with macOS environment
python3 classify_todays_meetings.py

# Compare results
diff data/meetings/meetings_*_classified.json
```

### 3. Validate Results
```bash
# Check classification accuracy
python3 -c "
import json
from pathlib import Path

data = json.load(open('data/meetings/meetings_$(date +%Y-%m-%d)_classified.json'))
meetings = data['meetings']

print(f'Total meetings: {len(meetings)}')
print(f'Classified: {sum(1 for m in meetings if \"classification\" in m)}')
print(f'High confidence (>0.8): {sum(1 for m in meetings if m.get(\"classification\", {}).get(\"confidence\", 0) > 0.8)}')
"
```

## Integration with Collaborator Discovery

The classified meetings can be used to enhance collaborator discovery:

```python
from tools.collaborator_discovery import CollaboratorDiscovery
import json

# Load classified meetings
with open('data/meetings/meetings_2025-10-28_classified.json') as f:
    data = json.load(f)

# Run collaborator discovery with meeting classifications
discovery = CollaboratorDiscovery()
results = discovery.analyze_meetings(
    meetings=data['meetings'],
    include_classifications=True
)
```

## Troubleshooting

### No meetings found
- Check calendar data range: `python -c "import json; print(json.load(open('my_calendar_events_complete_attendees.json'))['metadata']['date_range'])"`
- Run fresh extraction: See SilverFlow integration guide
- Verify date format matches system date

### Classification errors
- Check LLM configuration: `tools/llm_api.py`
- Verify Ollama is running (if using local models)
- Check rate limits (if using OpenAI/Azure APIs)

### Platform differences
- Use `python3` on macOS/Linux, `python` on Windows
- Path separators: Use `Path()` from `pathlib` for cross-platform compatibility
- Line endings: Configure git with `core.autocrlf false`

## Dependencies

Required Python packages:
- `json` (standard library)
- `datetime` (standard library)
- `pathlib` (standard library)
- Custom modules:
  - `tools.meeting_classifier`
  - `tools.llm_api`
  - `SilverFlow.graph_get_meetings` (optional, for live extraction)

## Next Steps

1. Create `classify_todays_meetings.py` script
2. Test on Windows platform
3. Push to GitHub
4. Pull and test on macOS branch
5. Compare classification results across platforms
6. Document any platform-specific differences

## Related Documentation

- `COLLABORATOR_DETECTION_ALGORITHM.md` - Full algorithm documentation
- `SILVERFLOW_INTEGRATION_GUIDE.md` - Calendar extraction guide
- `.cursorrules` - Project context and current state
- `tools/meeting_classifier.py` - Classification implementation

## Created
October 28, 2025

## Author
Scenara Team

## Version
1.0.0
