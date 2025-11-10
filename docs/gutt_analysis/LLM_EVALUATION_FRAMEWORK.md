# LLM Execution Composition Evaluation Framework

## Overview

This framework evaluates how well different LLMs (GPT-5 and Claude Sonnet 4.5) can compose execution plans by selecting and sequencing tasks from our **24 Canonical Unit Tasks (Framework V2.0)**.

This is **COMPOSITION analysis**, not task discovery. The LLMs are given the validated canonical tasks as candidates and must:
1. SELECT which tasks are needed for a prompt
2. SEQUENCE them in logical order
3. EXPLAIN dependencies and orchestration

## Key Difference from Previous Approach

**Old Approach (GUTT Discovery)**:
- LLMs generated new tasks from scratch
- No constraints on what tasks to identify
- Hard to compare and validate
- Led to inconsistent task definitions

**New Approach (Execution Composition)**:
- LLMs select from 24 validated canonical tasks
- Clear constraints: only use CAN-01 through CAN-23
- Easy to compare against gold standard
- Measures how well LLMs understand task orchestration

## Files

### Core Composition Scripts

1. **`gpt5_execution_composer.py`**
   - Uses GPT-5 (dev-gpt-5-chat-jj) via SilverFlow API
   - Composes execution plans from 24 canonical tasks
   - Outputs JSON with execution_plan, tasks_covered, orchestration

2. **`claude_execution_composer.py`**
   - Uses Claude Sonnet 4.5 (claude-sonnet-4-20250514) via Anthropic API
   - Same task: compose from 24 canonical tasks
   - Parallel implementation for comparison

### Batch Analysis & Evaluation

3. **`run_batch_composition_analysis.py`**
   - Runs BOTH GPT-5 and Claude on all 9 hero prompts
   - Saves results to `docs/gutt_analysis/model_comparison/batch_composition_analysis_*.json`
   - Compares task usage statistics

4. **`compare_against_gold_standard.py`**
   - Evaluates model outputs against gold standard
   - Metrics: Precision, Recall, F1 score per prompt
   - Identifies systematic gaps (commonly missed/extra tasks)
   - Determines winner and per-prompt performance

5. **`run_complete_evaluation.py`**
   - Master orchestration script
   - Runs full workflow: batch analysis → comparison → reporting
   - Interactive, shows progress and summary

## The 24 Canonical Unit Tasks (V2.0)

**Tier 1 (Universal - 6 tasks)**:
- CAN-01: Calendar Events Retrieval (100%)
- CAN-02A: Meeting Type Classification (78%)
- CAN-02B: Meeting Importance Assessment (67%)
- CAN-03: Calendar Event Creation/Update (44%)
- CAN-04: Natural Language Understanding (100%)
- CAN-05: Attendee/Contact Resolution (44%)

**Tier 2 (Common - 11 tasks)**:
- CAN-06: Availability Checking (33%)
- CAN-07: Meeting Metadata Extraction (56%) - **PARENT TASK**
- CAN-08: Document/Content Retrieval (33%)
- CAN-09: Document Generation/Formatting (33%)
- CAN-10: Time Aggregation/Statistical Analysis (11%)
- CAN-11: Priority/Preference Matching (22%)
- CAN-12: Constraint Satisfaction (22%)
- CAN-13: RSVP Status Update/Notification (11%)
- CAN-14: Recommendation Engine (22%)
- CAN-21: Task Duration Estimation (11%)
- CAN-22: Work Attribution Discovery (11%)

**Tier 3 (Specialized - 7 tasks)**:
- CAN-15: Recurrence Rule Generation (11%)
- CAN-16: Event Monitoring/Change Detection (11%)
- CAN-17: Automatic Rescheduling (11%)
- CAN-18: Objection/Risk Anticipation (11%)
- CAN-19: Resource/Logistics Booking (11%)
- CAN-20: Data Visualization/Reporting (11%)
- CAN-23: Conflict Resolution (11%)

**Key Insights**:
- **CAN-07 is a parent task**: Enables CAN-13, CAN-05, CAN-08, CAN-09, CAN-19, CAN-21
- **CAN-02A vs CAN-02B**: Format-based type vs value-based importance
- **CAN-04 is universal**: Every prompt needs NLU
- **Dependencies**: CAN-01 → CAN-06, CAN-07 → child tasks

## 9 Hero Prompts

### Organizer Category
1. **organizer-1**: Prioritize pending invitations based on this week's priorities
2. **organizer-2**: Flag important meetings and schedule prep time
3. **organizer-3**: Show meeting patterns and suggest time reclamation

### Schedule Category
4. **schedule-1**: Land weekly 1:1 with auto-rescheduling
5. **schedule-2**: Bump movable meetings to later in week
6. **schedule-3**: Weekly team sync with priority rules and room booking

### Collaborate Category
7. **collaborate-1**: Prep agenda with team's work updates
8. **collaborate-2**: Pull briefing for 1:1 (tasks, updates, blockers)
9. **collaborate-3**: Create doc of team's quarterly work attribution

## Usage

### Quick Start: Complete Evaluation

```bash
# Run the entire workflow (batch analysis + comparison + reporting)
python tools/run_complete_evaluation.py
```

This will:
1. Run GPT-5 on all 9 prompts
2. Run Claude on all 9 prompts
3. Compare both against gold standard
4. Generate evaluation report with F1 scores, gaps, winner

### Individual Commands

**Run single prompt with GPT-5:**
```bash
python tools/gpt5_execution_composer.py \
  "Show me my pending invitations and which ones I should prioritize" \
  --prompt-id organizer-1 \
  --output gpt5_organizer1.json
```

**Run single prompt with Claude:**
```bash
python tools/claude_execution_composer.py \
  "I have some important meetings—flag prep needs and schedule prep time" \
  --prompt-id organizer-2 \
  --output claude_organizer2.json
```

**Run batch analysis only:**
```bash
python tools/run_batch_composition_analysis.py
```

**Compare specific batch against gold standard:**
```bash
python tools/compare_against_gold_standard.py \
  docs/gutt_analysis/model_comparison/batch_composition_analysis_20251107_123456.json \
  --gold-standard docs/gutt_analysis/gold_standard_analysis.json
```

## Evaluation Metrics

### Task Coverage Metrics

**Precision**: % of selected tasks that are in gold standard
- `Precision = True Positives / (True Positives + False Positives)`
- High precision = few unnecessary tasks

**Recall**: % of gold standard tasks that were selected
- `Recall = True Positives / (True Positives + False Negatives)`
- High recall = few missing tasks

**F1 Score**: Harmonic mean of precision and recall
- `F1 = 2 * (Precision * Recall) / (Precision + Recall)`
- Balanced metric for overall performance

### Interpretation

- **F1 ≥ 0.9**: Excellent - nearly matches gold standard
- **F1 ≥ 0.8**: Good - minor differences
- **F1 ≥ 0.6**: Fair - some gaps but reasonable
- **F1 < 0.6**: Poor - significant gaps

### Gap Analysis

**Missing Tasks** (False Negatives):
- Critical tasks the model failed to include
- Indicates incomplete understanding

**Extra Tasks** (False Positives):
- Unnecessary tasks the model added
- Indicates over-selection or misunderstanding

**Systematic Gaps**:
- Tasks commonly missed by BOTH models
- Indicates ambiguity in prompt or task definition
- Tasks commonly added by BOTH models
- May indicate missing nuance in gold standard

## Output Files

All outputs saved to `docs/gutt_analysis/model_comparison/`:

1. **`batch_composition_analysis_TIMESTAMP.json`**
   - Raw compositions from both GPT-5 and Claude
   - Full execution plans with all steps
   - Task coverage for each prompt

2. **`evaluation_results_TIMESTAMP.json`**
   - Per-prompt scores (precision, recall, F1)
   - Aggregate scores for each model
   - Model comparison (winner, per-prompt breakdown)
   - Systematic gaps identified

## Example Output Structure

```json
{
  "gpt5_evaluation": {
    "aggregate_scores": {
      "average_precision": 0.92,
      "average_recall": 0.88,
      "average_f1": 0.90
    },
    "per_prompt_scores": {
      "organizer-1": {
        "precision": 1.0,
        "recall": 1.0,
        "f1": 1.0,
        "missing_tasks": [],
        "extra_tasks": []
      }
    }
  },
  "model_comparison": {
    "winner": "GPT-5",
    "gpt5_f1": 0.90,
    "claude_f1": 0.87,
    "difference": 0.03
  },
  "systematic_gaps": [
    {
      "type": "commonly_missed_tasks",
      "tasks": ["CAN-07", "CAN-21"],
      "description": "Both models miss parent task and duration estimation"
    }
  ]
}
```

## Key Insights to Track

1. **Parent Task Recognition**: Do models understand CAN-07 enables child tasks?
2. **Type vs Importance Split**: Do models correctly use CAN-02A vs CAN-02B?
3. **Dependency Handling**: Do models sequence CAN-01 before CAN-06?
4. **Universal Task Coverage**: Do models always include CAN-04 (NLU)?
5. **Tier Awareness**: Do models appropriately use Tier 1 vs Tier 3 tasks?

## Gold Standard Reference

The gold standard (`gold_standard_analysis.json`) represents the **validated correct execution compositions** for all 9 prompts, created through:
1. GPT-5 V2 analysis
2. Human evaluation by Chin-Yew Lin
3. Framework refinement (CAN-02 split, CAN-07 redefinition, 3 new tasks)
4. 100% task coverage verification

## Next Steps After Evaluation

1. **Review detailed JSON** to understand specific gaps
2. **Analyze systematic patterns** in missed/extra tasks
3. **Refine prompting strategy** based on weaknesses
4. **Consider model fine-tuning** if gaps are consistent
5. **Update gold standard** if evaluation reveals insights
6. **Iterate on task definitions** if ambiguity found

## Dependencies

- Python 3.8+
- GPT-5 access via SilverFlow LLM API (Microsoft internal)
- Anthropic API key for Claude Sonnet 4.5
- `requests`, `msal` (for GPT-5)
- `anthropic` (for Claude)

## Changelog

**November 7, 2025**:
- Created execution composition framework (replaces GUTT discovery)
- Implemented GPT-5 and Claude composers with 24 canonical tasks
- Built batch analysis and comparison infrastructure
- Defined evaluation metrics (precision, recall, F1)
- Integrated with gold standard analysis (V2.0)

---

*This framework enables systematic comparison of LLM performance on execution composition, moving from subjective evaluation to quantitative metrics.*
