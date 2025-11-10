# GPT-5 Composition Analysis Evaluation UX

## Overview

Interactive web-based evaluation interface for reviewing GPT-5's canonical task decomposition and execution plan analysis across all 9 hero prompts.

## Features

### 1. **Task Decomposition Evaluation**
- ✅ **Check/Uncheck Correctness**: All tasks default to "correct" - simply uncheck any that are incorrect
- ➕ **Add Missing Tasks**: Select from the 20 canonical tasks to add any that GPT-5 missed
- 📊 **Visual Feedback**: Color-coded tier badges (Tier 1/2/3)

### 2. **Execution Plan Rating**
- ✅ **Correct**: Execution plan is accurate and complete
- ~ **Partially Correct**: Has some issues but generally right
- ✗ **Incorrect**: Execution plan needs major corrections
- 📝 **Notes**: Add detailed feedback about what needs improvement

### 3. **Progress Tracking**
- 📈 **Visual Progress Bar**: See how many prompts you've evaluated
- 💾 **Auto-Save**: Progress saved automatically to browser localStorage
- 🔄 **Resume Anytime**: Close and reopen - your progress is preserved

### 4. **Results Export**
- 💾 **Download JSON**: Export complete evaluation results
- 📁 **Server Save**: Results automatically saved to `docs/gutt_analysis/evaluation_results_*.json`

## How to Use

### Start the Server

```bash
python tools/evaluate_composition_analysis.py
```

The browser will open automatically at `http://localhost:8080/`

### Evaluation Workflow

1. **Select a Prompt**: Click any prompt button (organizer-1, organizer-2, etc.)

2. **Review Task Decomposition**:
   - Check that all identified tasks are correct
   - Uncheck any incorrect tasks
   - Add any missing tasks from the dropdown

3. **Review Execution Plan**:
   - Read through each step's input → processing → output
   - Rate the overall execution plan (Correct/Partial/Incorrect)
   - Add notes about specific issues

4. **Save & Continue**: Click "Save & Continue" to mark as evaluated and move to next

5. **Complete All 9 Prompts**: Work through all prompts at your own pace

6. **View Summary**: After completing all prompts, see overall statistics

7. **Download Results**: Export the complete evaluation data

### Stop the Server

Press `Ctrl+C` in the terminal when done.

## Data Structure

### Evaluation Results JSON

```json
{
  "metadata": {
    "timestamp": "2025-11-06T23:45:00",
    "total_prompts": 9,
    "evaluator": "Chin-Yew Lin",
    "source_file": "gpt5_composition_analysis_20251106_232748.json"
  },
  "evaluations": {
    "organizer-1": {
      "prompt_id": "organizer-1",
      "prompt_text": "Show me my pending invitations...",
      "tasks": {
        "CAN-01": true,   // correct
        "CAN-04": true,   // correct
        "CAN-02": false   // incorrect
      },
      "added_tasks": ["CAN-11"],  // tasks added
      "execution_plan_rating": "correct|partial|incorrect",
      "notes": "Step 3 should use semantic similarity..."
    }
  }
}
```

## Output Files

Results are saved to:
- **Browser**: `localStorage` (automatic backup)
- **Server**: `docs/gutt_analysis/evaluation_results_YYYYMMDD_HHMMSS.json`

## Tips

- ✅ **Default is Correct**: Only uncheck tasks that are wrong - saves time
- 📝 **Be Specific in Notes**: Explain what's wrong and how to improve
- 💾 **Save Often**: Click "Save & Continue" after each prompt
- 🔄 **Resume Later**: Your progress is saved - you can close and continue later
- 📊 **Review Summary**: Check overall accuracy stats at the end

## Use Cases

1. **Quality Assurance**: Validate GPT-5's decomposition accuracy
2. **Training Data**: Generate ground truth for model improvement
3. **Gap Analysis**: Identify which tasks GPT-5 struggles with
4. **Implementation Planning**: Prioritize based on accuracy patterns

## Technical Details

- **Port**: 8080 (default)
- **Technology**: Pure HTML/CSS/JavaScript (no frameworks)
- **Storage**: Browser localStorage + server-side JSON files
- **Auto-save**: Every change triggers localStorage save
- **Browser Compatibility**: All modern browsers (Chrome, Edge, Firefox, Safari)

## Example Evaluation Session

```
1. Start server: python tools/evaluate_composition_analysis.py
2. Browser opens automatically
3. Click "organizer-1" prompt
4. Review 4 execution steps
5. All tasks look correct ✓
6. Execution plan is correct ✓
7. Add note: "Good sequential flow"
8. Click "Save & Continue"
9. Repeat for remaining 8 prompts
10. View summary: 95% task accuracy, 7/9 correct plans
11. Download results JSON
12. Ctrl+C to stop server
```

## Next Steps After Evaluation

1. **Analyze Results**: Use evaluation data to compute accuracy metrics
2. **Identify Patterns**: Which task types are most accurate/problematic?
3. **Refine Prompts**: Improve GPT-5 prompts based on common errors
4. **Implementation Priority**: Focus on high-accuracy decompositions first
5. **Model Fine-tuning**: Use evaluations as training data

---

**Created**: November 6, 2025  
**Author**: GitHub Copilot  
**Purpose**: Quality assurance for GPT-5 canonical task analysis
