# Single Model Validation Interface - Quick Reference

## Overview

The revised validation interface evaluates **one LLM's classifications at a time** instead of comparing two models side-by-side. This provides a cleaner, more focused validation experience.

## Key Changes

### Before (Dual Model)
- ✗ Validated GPT-5 vs Copilot simultaneously
- ✗ Complex interface with side-by-side comparisons
- ✗ Single validation file for both models
- ✗ Confusing when models need to be evaluated separately

### After (Single Model)
- ✓ Validate one model at a time
- ✓ Clean, focused interface
- ✓ Separate validation files per model
- ✓ Easy to compare different models' results later

## Usage

### Starting the Validation App

```bash
# Basic usage (uses today's date)
python start_validation_single.py gpt5

# Specify a date
python start_validation_single.py gpt5 2025-10-29
python start_validation_single.py copilot 2025-10-29
```

### Available Models

| Model | Command | File |
|-------|---------|------|
| GPT-5 | `gpt5` | `meeting_classification_gpt5.json` |
| GitHub Copilot | `copilot` | `meeting_classification_github_copilot.json` |
| GPT-4o | `gpt4o` | `meeting_classification_gpt4o.json` |
| Claude | `claude` | `meeting_classification_claude.json` |

### Direct App Launch

```bash
# Launch validation app directly (advanced usage)
python validation_app_single.py <model> [date]

# Examples
python validation_app_single.py gpt5 2025-10-29
python validation_app_single.py copilot 2025-10-29
```

## Interface Features

### Clean Single-Model View
- **Model Badge**: Shows which model you're validating
- **AI Classification Card**: Displays the model's classification with:
  - Specific meeting type
  - Primary category
  - Confidence score
  - Reasoning (if available)

### Validation Controls
1. **Correctness**: Mark as ✓ Correct or ✗ Incorrect
2. **Correct Type** (if incorrect): Select from full taxonomy
3. **Notes**: Add observations or comments
4. **Difficulty**: Rate as 😊 Easy, 🤔 Medium, or 😰 Hard

### Statistics Dashboard
- Total Meetings
- Validated Count
- Model Accuracy
- Progress Percentage

## File Organization

### Validation Results
Each model gets its own validation file:
```
experiments/2025-10-29/
  ├── human_validation_gpt5.json
  ├── human_validation_copilot.json
  ├── human_validation_gpt4o.json
  └── human_validation_claude.json
```

### Validation File Structure
```json
{
  "validation_date": "2025-10-29T20:45:00",
  "validator": "Human Expert",
  "model": "gpt5",
  "model_display_name": "GPT-5",
  "total_meetings": 8,
  "validated_count": 5,
  "validations": {
    "meeting-id-1": {
      "timestamp": "2025-10-29T20:46:15",
      "is_correct": true,
      "correct_type": null,
      "correct_category": null,
      "notes": "Clear progress review meeting",
      "difficulty": "easy"
    },
    "meeting-id-2": {
      "timestamp": "2025-10-29T20:47:30",
      "is_correct": false,
      "correct_type": "Team Status Update Meetings",
      "correct_category": "Internal Recurring Meetings (Cadence)",
      "notes": "Misclassified as Planning but clearly a status sync",
      "difficulty": "medium"
    }
  }
}
```

## Workflow

### 1. Extract Today's Meetings
```bash
python SilverFlow/data/graph_get_meetings.py
python process_todays_meetings.py
```

### 2. Run Classification
```bash
# Run one or more models
python classify_with_gpt5.py
python classify_with_copilot_auto.py
```

### 3. Validate Each Model
```bash
# Validate GPT-5
python start_validation_single.py gpt5

# Stop server (Ctrl+C), then validate Copilot
python start_validation_single.py copilot
```

### 4. Compare Results
```bash
# Analyze accuracy for each model
python analyze_validation_accuracy.py --model gpt5
python analyze_validation_accuracy.py --model copilot

# Or compare all models
python compare_model_validations.py 2025-10-29
```

## Benefits

### Focused Validation
- No cognitive load from comparing two models
- Clearer assessment of each model individually
- Better for recording detailed notes

### Flexible Comparison
- Validate models on different days
- Easy to add new models to comparison
- Can re-validate a single model without affecting others

### Better Analysis
- Separate accuracy metrics per model
- Track which models handle specific meeting types better
- Identify systematic errors per model

## API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/` | GET | Main validation interface |
| `/api/validate` | POST | Save validation for a meeting |
| `/api/stats` | GET | Get validation statistics |
| `/api/export` | GET | Download validation results |
| `/api/report` | GET | Generate detailed analysis report |

## Export Format

Download validation results as JSON:
- Click "📊 Export Results" button, or
- Visit `http://localhost:5000/api/export`
- Saves as: `validation_{model}_{date}.json`

## Tips

### Validation Best Practices
1. **Read meeting details carefully** - Don't just validate based on title
2. **Check reasoning** - Model's explanation can reveal errors
3. **Note patterns** - Document systematic errors in notes field
4. **Use difficulty ratings** - Helps identify ambiguous meetings
5. **Save frequently** - Validates are saved individually

### Handling Edge Cases
- **Missing classification**: If model hasn't classified yet, classification card shows "Not yet classified"
- **Low confidence**: Yellow or red confidence badges indicate uncertainty
- **Ambiguous meetings**: Mark as "hard" and add detailed notes

### Multi-Model Workflow
For best results validating multiple models:
1. Validate all meetings for Model A
2. Take a break (avoid fatigue bias)
3. Validate all meetings for Model B
4. Compare results using analysis scripts

## Troubleshooting

### "Classification file not found"
```bash
# Run classification first
python classify_with_gpt5.py  # or whichever model
```

### "Meetings file not found"
```bash
# Extract meetings first
python process_todays_meetings.py 2025-10-29
```

### Port 5000 already in use
```bash
# Kill existing Flask process
Get-Process python | Stop-Process -Force  # PowerShell
# OR
pkill python  # Linux/Mac
```

### Validation not saving
- Check browser console for errors
- Verify you've marked the classification as correct/incorrect
- If marked incorrect, ensure you selected correct type
- Check write permissions on experiments directory

## Migration from Dual-Model Interface

### Old Files (Still Available)
- `validation_app.py` - Dual-model validation
- `start_validation_app.py` - Dual-model launcher
- `templates/validation.html` - Dual-model template

### New Files
- `validation_app_single.py` - Single-model validation
- `start_validation_single.py` - Single-model launcher
- `templates/validation_single.html` - Single-model template

### Converting Old Validations
If you have dual-model validations and want to split them:
```bash
python split_dual_validations.py experiments/2025-10-28/human_validation_results.json
# Creates: human_validation_gpt5.json, human_validation_copilot.json
```

## Next Steps

After validation:
1. **Analyze accuracy**: `python analyze_validation_accuracy.py --model gpt5`
2. **Compare models**: `python compare_model_validations.py 2025-10-29`
3. **Update prompts**: If errors found, refine classification prompts
4. **Continue validation**: Build up to 50+ validated meetings
5. **Track trends**: Monitor if accuracy improves over time

---

**Created**: October 29, 2025  
**Purpose**: Single-model validation for cleaner, more focused classification assessment
