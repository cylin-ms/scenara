# Quick Start Guide for macOS

## Running Meeting Classification on macOS Branch

### 1. Switch to macOS Branch
```bash
cd /path/to/scenara
git checkout macos-dev  # or create if doesn't exist: git checkout -b macos-dev
git pull origin master  # Pull latest changes from master
```

### 2. Verify Environment
```bash
# Check Python version
python3 --version  # Should be 3.8+

# Check required packages
python3 -c "import json, datetime, pathlib; print('✅ Standard libraries OK')"

# Check Scenara modules
python3 -c "from tools.meeting_classifier import classify_meeting; print('✅ Meeting classifier OK')"
```

### 3. Extract Today's Meetings
```bash
# Run extraction
python3 get_todays_meetings.py

# Output will be in: data/meetings/meetings_YYYY-MM-DD.json
```

### 4. Classify Meetings
```bash
# Run classification
python3 classify_todays_meetings.py

# This will create: data/meetings/meetings_YYYY-MM-DD_classified.json
```

### 5. View Results
```bash
# View with pretty formatting (requires jq)
cat data/meetings/meetings_$(date +%Y-%m-%d)_classified.json | jq '.'

# Or view metadata only
cat data/meetings/meetings_$(date +%Y-%m-%d)_classified.json | jq '.metadata'

# Or simple view
cat data/meetings/meetings_$(date +%Y-%m-%d)_classified.json
```

### 6. Compare with Windows Results

If you ran classification on both Windows and macOS:

```bash
# Copy Windows results to compare
# (assuming you have them from Windows)

# Compare classification results
python3 -c "
import json
from pathlib import Path

# Load both files
win_data = json.load(open('meetings_2025-10-28_classified_windows.json'))
mac_data = json.load(open('meetings_2025-10-28_classified_macos.json'))

# Compare
print('Windows classified:', win_data['metadata']['total_classified'])
print('macOS classified:', mac_data['metadata']['total_classified'])

# Compare meeting types
win_types = [m.get('classification', {}).get('type') for m in win_data['meetings']]
mac_types = [m.get('classification', {}).get('type') for m in mac_data['meetings']]

differences = sum(1 for w, m in zip(win_types, mac_types) if w != m)
print(f'Classification differences: {differences}/{len(win_types)}')
"
```

### 7. Commit macOS Results

```bash
# Add classification results
git add data/meetings/meetings_*_classified.json

# Commit
git commit -m "Add: macOS meeting classification results for $(date +%Y-%m-%d)"

# Push to macOS branch
git push origin macos-dev
```

## Troubleshooting

### ImportError: No module named 'tools.meeting_classifier'
```bash
# Check if you're in the right directory
pwd  # Should be in scenara root

# Verify tools directory exists
ls -la tools/meeting_classifier*.py
```

### No meetings found
```bash
# Check calendar data range
python3 -c "
import json
data = json.load(open('my_calendar_events_complete_attendees.json', encoding='utf-8'))
print('Date range:', data['metadata']['date_range'])
print('Total events:', data['metadata']['total_events'])
"

# If data is outdated, extract fresh data using SilverFlow
cd SilverFlow
python3 graph_get_meetings.py --select attendees
```

### LLM/Classifier Issues
```bash
# Check which classifier is being used
python3 -c "
try:
    from tools.meeting_classifier_gpt4o import classify_meeting
    print('Using: GPT-4o classifier')
except ImportError:
    from tools.meeting_classifier import classify_meeting
    print('Using: Keyword-based classifier')
"

# If using Ollama, check it's running
curl http://localhost:11434/api/tags
```

## Platform-Specific Notes

### Line Endings
macOS uses LF, Windows uses CRLF. Git should handle this automatically, but verify:
```bash
git config core.autocrlf
# Should be 'input' on macOS, 'false' on Windows
```

### Python Command
- macOS: Use `python3`
- Windows: Use `python`

### Path Separators
Both scripts use `pathlib.Path()` which handles platform differences automatically.

## Expected Output

### get_todays_meetings.py
```
📅 Extracting meetings for 2025-10-28...
Trying alternative method using calendar data file...
✅ Found 0 meetings for 2025-10-28
💾 Saved to: data/meetings/meetings_2025-10-28.json
```

### classify_todays_meetings.py
```
🎯 Meeting Classification Tool

📅 Date: 2025-10-28
📋 Meetings found: 5

🔍 Classifying 5 meetings...
   Using classifier: GPT-4o

  [1/5] Team Sync
       Time: 2025-10-28T09:00:00
       Type: Team Status Update (confidence: 0.92)

  [2/5] 1:1 with Manager
       Time: 2025-10-28T14:00:00
       Type: One-on-One Meeting (confidence: 0.95)

📊 Classification Summary:
   Total meetings: 5
   Successfully classified: 5
   High confidence (>0.8): 5

   Meeting types:
     - Team Status Update: 2
     - One-on-One Meeting: 2
     - Project Planning Meeting: 1

✅ Classification complete!
📄 Results saved to: data/meetings/meetings_2025-10-28_classified.json
```

## Next Steps

1. Run classification on macOS
2. Compare results with Windows classification
3. Document any platform-specific differences
4. Update `.cursorrules` with findings
5. Merge macOS improvements back to master

## Related Files

- `data/meetings/README.md` - Complete workflow documentation
- `COLLABORATOR_DETECTION_ALGORITHM.md` - Algorithm details
- `.cursorrules` - Project context
- `tools/meeting_classifier*.py` - Classifier implementations

---
Created: October 28, 2025
Platform: macOS
