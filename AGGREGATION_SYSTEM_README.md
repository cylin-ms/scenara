# Aggregated Validation System - README

## Overview

The aggregated validation system collects human validation results across multiple days, builds training/evaluation datasets, and tracks accuracy trends over time.

## Quick Start

```powershell
# Run aggregation (scans all experiment dates)
python aggregate_validation_results.py
```

## What It Does

### 1. **Finds All Validation Files**
- Scans `experiments/` directory for all date folders (e.g., `2025-10-28`)
- Loads `human_validation_results.json` from each date
- Processes all validated meetings

### 2. **Aggregates Metrics**
- Overall accuracy (GPT-5 and Copilot)
- Accuracy by difficulty level (easy/medium/hard)
- Error patterns and frequencies
- Trends over time (as you validate more days)

### 3. **Builds Datasets**
- **Training Set** (80%): For prompt refinement and model fine-tuning
- **Evaluation Set** (20%): For measuring accuracy
- **Error Catalog**: All misclassifications with patterns

### 4. **Saves Results**
All files saved to `experiments/aggregated_validation/`:
- `training_dataset.json` - Training examples
- `evaluation_dataset.json` - Test examples
- `accuracy_trends.json` - Metrics over time
- `error_catalog.json` - All errors cataloged

## Output Files

### Training Dataset (`training_dataset.json`)

```json
{
  "metadata": {
    "created": "2025-10-28T17:07:15.987125",
    "total_examples": 6,
    "purpose": "Training data for meeting classification",
    "split": "training (80%)"
  },
  "examples": [
    {
      "id": "...",
      "date": "2025-10-28",
      "features": {
        "subject": "Meeting Prep STCA Sync",
        "body_preview": "...",
        "attendee_count": 10,
        "duration_minutes": 85.0,
        "keywords": ["meeting prep", "sync"]
      },
      "ground_truth": {
        "specific_type": "Team Status Update Meetings",
        "primary_category": "Internal Recurring Meetings (Cadence)",
        "difficulty": "easy",
        "notes": ""
      },
      "validation_metadata": {
        "timestamp": "2025-10-28T16:50:06.652793",
        "gpt5_correct": true,
        "copilot_correct": false
      }
    }
  ]
}
```

### Error Catalog (`error_catalog.json`)

```json
{
  "metadata": {
    "created": "2025-10-28T17:07:15.997162",
    "total_errors": 2,
    "unique_patterns": 2
  },
  "error_patterns": {
    "Informational Briefings → Team Status Update Meetings": 1,
    "Planning Session → Team Status Update Meetings": 1
  },
  "errors": [
    {
      "id": "...",
      "date": "2025-10-28",
      "model": "gpt5",
      "meeting_subject": "Update Copilot Agility BPR [Async Task]",
      "keywords": ["[async task]"],
      "ai_classification": {
        "specific_type": "Informational Briefings",
        "primary_category": "Informational & Broadcast Meetings",
        "confidence": 0.78
      },
      "correct_classification": {
        "specific_type": "Team Status Update Meetings",
        "primary_category": "Internal Recurring Meetings (Cadence)"
      },
      "error_pattern": "Informational Briefings → Team Status Update Meetings",
      "difficulty": "easy",
      "notes": ""
    }
  ]
}
```

### Accuracy Trends (`accuracy_trends.json`)

```json
{
  "metadata": {
    "created": "2025-10-28T17:07:15.992650",
    "dates_analyzed": ["2025-10-28"]
  },
  "overall": {
    "total_meetings": 8,
    "gpt5_accuracy": 75.0,
    "copilot_accuracy": 75.0
  },
  "by_date": {
    "2025-10-28": {
      "date": "2025-10-28",
      "total_meetings": 8,
      "gpt5_correct": 6,
      "copilot_correct": 6,
      "gpt5_accuracy": 75.0,
      "copilot_accuracy": 75.0,
      "both_correct": 5,
      "both_wrong": 1
    }
  },
  "by_difficulty": {
    "easy": {
      "total": 7,
      "gpt5_correct": 5,
      "copilot_correct": 5
    },
    "medium": {
      "total": 1,
      "gpt5_correct": 1,
      "copilot_correct": 1
    }
  }
}
```

## Usage Workflow

### Daily Validation
1. Extract today's meetings: `python extract_todays_meetings.py`
2. Run classifications: `python classify_with_gpt5.py` (or Copilot)
3. Validate via web app: `.\START_VALIDATION.ps1`
4. Complete 8 meetings (~8 minutes)

### Periodic Aggregation
```powershell
# After validating multiple days
python aggregate_validation_results.py
```

**Output**:
- Current overall accuracy
- Accuracy trends (improvement over time)
- Updated training/evaluation datasets
- Error pattern analysis

### Using the Datasets

#### For Prompt Refinement
```python
import json

# Load error catalog
with open('experiments/aggregated_validation/error_catalog.json') as f:
    errors = json.load(f)

# Find top error patterns
patterns = errors['error_patterns']
print("Top errors to fix:")
for pattern, count in sorted(patterns.items(), key=lambda x: x[1], reverse=True):
    print(f"  {pattern}: {count} times")
```

#### For Model Fine-tuning
```python
# Load training dataset
with open('experiments/aggregated_validation/training_dataset.json') as f:
    training = json.load(f)

# Each example has:
# - features: meeting metadata (subject, keywords, duration)
# - ground_truth: human-validated classification
# Use for fine-tuning classification models
```

## Dataset Growth

As you continue daily validations:

| Stage | Meetings | Status | Use Case |
|-------|----------|--------|----------|
| **Initial** | 8-20 | Small | Error pattern discovery |
| **Growing** | 20-50 | Medium | Prompt refinement, trend analysis |
| **Substantial** | 50+ | Large | Model fine-tuning, production deployment |

**Current**: 8 meetings (Initial stage)

## Key Metrics Tracked

### Overall Accuracy
- GPT-5 accuracy across all validated meetings
- Copilot accuracy across all validated meetings
- Comparison to production threshold (80%)

### By Difficulty
- Easy meetings (human-rated)
- Medium meetings
- Hard meetings
- Identifies if models struggle with certain difficulty levels

### By Date
- Track improvement after prompt refinements
- Compare accuracy before/after changes
- Identify regression if accuracy drops

### Error Patterns
- Most common misclassification patterns
- Frequency of each pattern
- Helps prioritize prompt improvements

## Example Output

```
================================================================================
  AGGREGATED VALIDATION ANALYSIS - MULTI-DAY DATASET BUILDER
================================================================================

Found 3 validation file(s):
   - 2025-10-28: experiments\2025-10-28\human_validation_results.json
   - 2025-10-29: experiments\2025-10-29\human_validation_results.json
   - 2025-10-30: experiments\2025-10-30\human_validation_results.json

Processing 2025-10-28...
  + 2025-10-28: 8 meetings
    GPT-5: 75.0% | Copilot: 75.0%

Processing 2025-10-29...
  + 2025-10-29: 12 meetings
    GPT-5: 83.3% | Copilot: 75.0%

Processing 2025-10-30...
  + 2025-10-30: 10 meetings
    GPT-5: 90.0% | Copilot: 80.0%

OVERALL STATISTICS
--------------------------------------------------------------------------------
Total Meetings Validated: 30
Validation Dates: 2025-10-28, 2025-10-29, 2025-10-30

GPT-5 Overall Accuracy:      82.7% (25/30)
Copilot Overall Accuracy:    76.7% (23/30)

TOP ERROR PATTERNS
--------------------------------------------------------------------------------
1. Planning Sessions → Team Status Update Meetings (5 occurrences)
2. Informational Briefings → Team Status Update Meetings (2 occurrences)

DATASET SPLIT
--------------------------------------------------------------------------------
Total Examples:      30
Training Set:        24 (80%)
Evaluation Set:      6 (20%)
Error Examples:      12
```

## Next Steps

### Continue Validating
- Goal: 50+ validated meetings
- Daily validation takes ~8-10 minutes
- Builds reliable training dataset

### Analyze Trends
```powershell
# After multiple days
python aggregate_validation_results.py
```

Review:
- Is accuracy improving?
- Are error patterns changing?
- Which model performs better overall?

### Refine Prompts
Based on error catalog:
1. Identify top error patterns
2. Update `prompts/meeting_classification_prompt.md`
3. Re-run experiments
4. Validate improvements

### Production Deployment
Once accuracy > 80%:
1. Choose best-performing model
2. Deploy classification system
3. Continue monitoring accuracy
4. Periodic re-validation

## Files in System

```
aggregate_validation_results.py     # Main aggregation script
experiments/
  └── aggregated_validation/
      ├── training_dataset.json      # 80% of validated meetings
      ├── evaluation_dataset.json    # 20% of validated meetings
      ├── accuracy_trends.json       # Metrics over time
      └── error_catalog.json         # All errors cataloged
  └── 2025-10-28/
      ├── human_validation_results.json
      ├── meeting_classification_gpt5.json
      └── meeting_classification_github_copilot.json
  └── 2025-10-29/
      └── human_validation_results.json
  └── ...
```

## Tips

1. **Validate consistently**: Daily validation builds dataset faster
2. **Review error patterns**: Focus prompt improvements on top errors
3. **Track trends**: Monitor if accuracy improves after changes
4. **Split dataset properly**: Keep evaluation set separate for unbiased metrics
5. **Document changes**: Note when you update prompts to correlate with accuracy changes

## Current Status

- **Total Meetings**: 8
- **GPT-5 Accuracy**: 75.0%
- **Copilot Accuracy**: 75.0%
- **Dataset Size**: Small (need 50+ for production)
- **Training Examples**: 6
- **Evaluation Examples**: 2
- **Top Error**: "Meeting Prep" + "Sync" → misclassified as Planning

**Recommendation**: Continue daily validation to reach 50+ meetings for robust statistics.
