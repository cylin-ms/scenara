# Meeting Classification Validation Web App

A beautiful, interactive web application for validating AI meeting classifications.

## Features

✨ **Interactive UI**
- View all meetings with full details
- See both GPT-5 and GitHub Copilot classifications side-by-side
- Rate each classification (correct/incorrect)
- Select correct type from full taxonomy dropdown
- Add notes and difficulty ratings
- Real-time accuracy statistics

📊 **Analytics**
- Live accuracy tracking for both models
- Progress visualization
- Export validation results as JSON
- Detailed validation report

🎨 **User Experience**
- Beautiful gradient design
- Responsive layout
- Smooth animations
- Easy navigation
- Auto-scroll to next meeting

## Quick Start

### 1. Install Dependencies

```powershell
pip install flask
```

### 2. Run the App

```powershell
python validation_app.py
```

### 3. Open Your Browser

Navigate to: **http://localhost:5000**

## How to Use

### Validate a Meeting

1. **Review Meeting Details**
   - Subject, time, duration, attendees
   - Meeting description preview

2. **Review AI Classifications**
   - GPT-5 classification (left panel)
   - GitHub Copilot classification (right panel)
   - Confidence scores for each

3. **Rate Classifications**
   - Click ✓ Correct or ✗ Incorrect for each model
   - If incorrect, select correct category and type from dropdowns

4. **Add Context** (Optional)
   - Add notes about your reasoning
   - Rate difficulty (Easy/Medium/Hard)

5. **Save**
   - Click "Save Validation"
   - Progress updates automatically
   - Scroll to next meeting

### View Statistics

Real-time stats appear at the top:
- **Total Meetings**: Number of meetings to validate
- **Validated**: Number you've completed
- **GPT-5 Accuracy**: Percentage of correct GPT-5 classifications
- **Copilot Accuracy**: Percentage of correct Copilot classifications

### Export Results

Click the **"📊 Export Results"** button (bottom-right) to download:
- `validation_results.json` - Complete validation data
- Includes all ratings, notes, and corrections
- Can be used for further analysis

## Data Files

### Input
- `data/meetings/meetings_2025-10-28.json` - Today's meetings
- `experiments/2025-10-28/meeting_classification_gpt5.json` - GPT-5 results
- `experiments/2025-10-28/meeting_classification_github_copilot.json` - Copilot results

### Output
- `experiments/2025-10-28/human_validation_results.json` - Your validations
  - Meeting-by-meeting validation data
  - Correct/incorrect flags for each model
  - Correct classifications (if AI was wrong)
  - Notes and difficulty ratings
  - Timestamps

## API Endpoints

The app provides several API endpoints:

### `GET /`
Main validation interface

### `POST /api/validate`
Save validation for a meeting

**Request Body:**
```json
{
  "meeting_id": "AAkBOQAICN4U68W0gAA...",
  "gpt5_correct": true,
  "copilot_correct": false,
  "correct_type": "Planning Sessions",
  "correct_category": "Strategic Planning & Decision Meetings",
  "notes": "This is clearly a planning meeting based on...",
  "difficulty": "medium"
}
```

### `GET /api/stats`
Get validation statistics

**Response:**
```json
{
  "total": 8,
  "validated": 5,
  "gpt5_accuracy": 80.0,
  "copilot_accuracy": 60.0,
  "progress": 62.5
}
```

### `GET /api/export`
Download validation results JSON file

### `GET /api/report`
Get detailed validation report

**Response:**
```json
{
  "summary": {
    "total_meetings": 8,
    "validated_meetings": 8,
    "gpt5_accuracy": 87.5,
    "copilot_accuracy": 75.0
  },
  "gpt5_errors": [...],
  "copilot_errors": [...]
}
```

## Meeting Taxonomy

The app includes the complete 31+ meeting type taxonomy:

### 1. Internal Recurring Meetings (Cadence)
- Team Status Update Meetings
- Progress Review Meetings
- One-on-One Meetings
- Action Review Meetings
- Governance & Strategy Cadence

### 2. Strategic Planning & Decision Meetings
- Planning Sessions
- Decision-Making Meetings
- Problem-Solving / Incident Resolution Meetings
- Brainstorming / Innovation Meetings
- Workshops & Design Sessions

### 3. External & Client-Facing Meetings
- Sales & Client Meetings
- Vendor/Supplier Meetings
- Partnership/Business Development Meetings
- Interviews and Recruiting Meetings
- Client Training or Onboarding

### 4. Informational & Broadcast Meetings
- All-Hands / Town Hall Meetings
- Informational Briefings
- Training & Education Sessions
- Webinars and Broadcasts

### 5. Team-Building & Culture Meetings
- Team-Building Activities
- Recognition & Social Events
- Communities of Practice & Networking Meets

## Tips for Validation

### High Confidence Cases
If both models agree and have high confidence (>95%), they're likely correct. Quick validation!

### Disagreement Cases
When models disagree, these are the most interesting:
- Meeting 1: "[Async Task]" - Informational vs Status Update
- Meeting 3: "Meeting Prep STCA Sync" - Status vs Planning

Pay special attention to these edge cases.

### Common Patterns
- **"Meeting Prep"** → Usually Planning Sessions
- **"Sync"** → Could be Status Update or Planning (context matters)
- **"Office Hours"** → Usually Informational Briefings
- **"Weekly Review"** → Progress Review Meetings
- **"1:1" / "1-on-1"** → One-on-One Meetings

### Ambiguous Meetings
If a meeting genuinely fits multiple types:
- Choose the PRIMARY purpose (>50% of meeting)
- Add notes explaining the ambiguity
- Rate as "Hard" difficulty

## Expected Time

- **5-10 minutes** for all 8 meetings
- **~1 minute per meeting** average
- Quick validation for clear cases
- More time for ambiguous cases

## Next Steps After Validation

Once you complete all 8 meetings:

1. **Review Statistics**
   - Check GPT-5 vs Copilot accuracy
   - Identify which model performed better
   - Compare to 87.5% cross-model agreement

2. **Export Results**
   - Download validation JSON
   - Use for further analysis
   - Reference for prompt refinement

3. **Analyze Errors**
   - Review error patterns
   - Identify taxonomy gaps
   - Suggest prompt improvements

4. **Update Prompt** (if needed)
   - Add rules for common errors
   - Clarify ambiguous type definitions
   - Re-run experiments

## Technical Details

- **Framework**: Flask (Python web framework)
- **Frontend**: Pure HTML/CSS/JavaScript (no dependencies)
- **Storage**: JSON files (no database needed)
- **Port**: 5000 (configurable)
- **Hot Reload**: Enabled in debug mode

## Troubleshooting

### Port Already in Use
```powershell
# Kill process on port 5000
Get-Process -Id (Get-NetTCPConnection -LocalPort 5000).OwningProcess | Stop-Process
```

### Flask Not Found
```powershell
pip install flask
```

### Can't Access from Other Devices
The app runs on `0.0.0.0:5000` so it's accessible from other devices on your network.
Find your IP and navigate to `http://YOUR_IP:5000`

## Development

To modify the app:

1. **Backend Logic**: Edit `validation_app.py`
2. **Frontend UI**: Edit `templates/validation.html`
3. **Styling**: Modify `<style>` section in template
4. **API**: Add endpoints in `validation_app.py`

Changes to templates reload automatically in debug mode.

## Author

**Scenara 2.0 Project**  
Date: October 28, 2025  
Version: 1.0

## License

Internal use for Scenara 2.0 meeting classification validation.
