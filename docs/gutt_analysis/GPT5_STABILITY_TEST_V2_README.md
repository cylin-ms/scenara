# GPT-5 Stability Test V2.0 - 25 Canonical Tasks Framework

**Version**: 2.0  
**Date**: November 7, 2025  
**Framework**: 25 Canonical Tasks (CAN-01 through CAN-25)  
**New in V2.0**: CAN-25 (Event Annotation/Flagging)

---

## Overview

This document describes the **3-trial stability test methodology** for validating GPT-5's execution composition analysis using the updated **25 Canonical Tasks Framework V2.0**.

### Purpose

1. **Validate V2.0 Framework**: Test new CAN-25 (Event Annotation/Flagging) detection
2. **Measure Stability**: Ensure consistent task selection across multiple runs
3. **Compute Average Performance**: Get statistically robust baseline metrics
4. **Compare V1.0 vs V2.0**: Understand impact of renumbering and new task addition
5. **Identify Non-determinism**: Find prompts with high variance

---

## Methodology

### 3-Trial Consistency Testing

**Execution Strategy**:
- **3 Independent Trials**: Run EXACT same 9 hero prompts 3 times
- **27 Total API Calls**: 9 prompts × 3 trials = 27 GPT-5 queries
- **Optimized V2.0 Prompts**: Enhanced system prompts with CAN-25 guidance
- **Fair Testing**: Identical inputs across all trials for reproducibility

### What We Analyze

1. **Per-Prompt Stability**:
   - **Always Selected Tasks**: Tasks appearing in ALL 3 trials (100% consistency)
   - **Sometimes Selected Tasks**: Tasks appearing in 1-2 trials (variance)
   - **Consistency Percentage**: (Always / Total Unique) × 100%
   - **Task Count Variance**: Standard deviation of task counts

2. **CAN-25 Detection** (NEW in V2.0):
   - Which prompts use CAN-25 (Event Annotation/Flagging)?
   - Consistency: How many trials detected CAN-25?
   - Expected prompts: Organizer-2 ("flag any that require focus time")

3. **Aggregate Statistics**:
   - Average task count across all prompts
   - Average variance across all prompts
   - Overall consistency percentage
   - CAN-25 detection rate

---

## Running the Stability Test

### Prerequisites

```bash
# Ensure Python environment is set up
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# Install dependencies
pip install requests msal
```

### Step 1: Run 3-Trial Stability Test

```bash
# Run from project root
python tools/run_gpt5_stability_test_v2.py
```

**What it does**:
1. Initializes GPT-5 Execution Composer V2.0
2. Runs 3 trials of all 9 hero prompts (27 API calls)
3. Saves trial results to `docs/gutt_analysis/model_comparison/gpt5_stability_v2/`
4. Generates stability analysis with CAN-25 detection statistics

**Expected Duration**: ~5-10 minutes (depends on API response time)

**Output Files**:
```
docs/gutt_analysis/model_comparison/gpt5_stability_v2/
├── gpt5_v2_trial1_TIMESTAMP.json          # Trial 1 results
├── gpt5_v2_trial2_TIMESTAMP.json          # Trial 2 results
├── gpt5_v2_trial3_TIMESTAMP.json          # Trial 3 results
└── gpt5_v2_stability_analysis_TIMESTAMP.json  # Stability metrics
```

### Step 2: Compute Average Performance

```bash
# Compute average across 3 trials
python tools/compute_gpt5_average_v2.py
```

**What it does**:
1. Loads all 3 trial results
2. Computes average task usage across trials
3. Calculates precision, recall, F1 scores
4. Generates comparison to gold standard

**Output**:
```
docs/gutt_analysis/model_comparison/gpt5_stability_v2/
└── gpt5_v2_average_performance.json       # Average metrics
```

---

## Key Differences: V2.0 vs V1.0

### Framework Changes

| Aspect | V1.0 (24 tasks) | V2.0 (25 tasks) |
|--------|-----------------|-----------------|
| **Total Tasks** | 24 | 25 |
| **Task IDs** | CAN-01 to CAN-23 (CAN-02A/CAN-02B split) | CAN-01 to CAN-25 (sequential) |
| **New Task** | - | CAN-25: Event Annotation/Flagging |
| **Renumbering** | CAN-02A, CAN-02B | CAN-02, CAN-03 |
| **Flagging Support** | No dedicated task | CAN-25 for event flags/annotations |

### Prompt Optimization V2.0

**New Instructions Added**:

1. **CAN-25 Guidance**:
   ```
   5. **CAN-25: Event Annotation/Flagging (NEW in V2.0)**:
      - Add flags/annotations to calendar events when conditions are met
      - Use when prompt asks to: "flag meetings", "mark important", "highlight"
      - Example: "Flag any that require focus time" → Use CAN-25
   ```

2. **Enhanced Keywords**:
   - CAN-25: "flag", "annotate", "mark", "highlight", "signal", "indicator"
   - CAN-21: "prep time", "focus time", "preparation"
   - CAN-23: "agenda", "structure", "topics"

3. **Explicit DO/DON'T**:
   ```
   ✅ **DO**: Use CAN-25 when prompt asks to flag/mark/annotate meetings
   ❌ **DON'T**: Forget CAN-25 for flagging/annotation requests (new in V2.0)
   ```

---

## Expected Results

### Target Metrics (Based on V1.0 Baseline)

| Metric | V1.0 Baseline | V2.0 Target |
|--------|---------------|-------------|
| **F1 Score** | 78.40% ± 0.72% | ≥78% (maintain) |
| **Precision** | 74.76% ± 0.25% | ≥74% |
| **Recall** | 84.25% ± 1.79% | ≥84% |
| **Consistency** | 93.6% | ≥93% |
| **CAN-25 Detection** | N/A | ≥50% for Organizer-2 |

### CAN-25 Expected Usage

**Prompts likely to use CAN-25**:
1. ✅ **Organizer-2**: "flag any that require focus time to prepare for them"
2. ❓ **Organizer-1**: "prioritize based on my priorities" (possible)
3. ❓ **Schedule-2**: "clear my schedule for Thursday afternoon" (possible)

**Success Criteria**:
- CAN-25 detected in **at least 1 prompt** (Organizer-2)
- **≥2/3 trials** consistent detection for Organizer-2
- **No false positives** in prompts without flagging keywords

---

## Stability Analysis Metrics

### Per-Prompt Metrics

For each of the 9 hero prompts:

```json
{
  "prompt_id": "Organizer-2",
  "always_selected": ["CAN-04", "CAN-01", "CAN-07", "CAN-25"],
  "sometimes_selected": ["CAN-02", "CAN-03"],
  "total_unique_tasks": 6,
  "consistency_percentage": 66.67,
  "average_task_count": 5.67,
  "task_count_variance": 0.2222,
  "task_count_std_dev": 0.47,
  "can25_usage": {
    "detected": true,
    "trials_with_can25": 3,
    "consistency": "3/3"
  }
}
```

**Interpretation**:
- **Always selected**: Core tasks needed 100% of time
- **Sometimes selected**: Tasks with variance (needs investigation)
- **Consistency %**: Higher = more stable (>90% excellent)
- **Variance**: Lower = more stable (<1.0 excellent)
- **CAN-25 usage**: New metric for V2.0 validation

### Aggregate Metrics

```json
{
  "framework_version": "2.0",
  "total_canonical_tasks": 25,
  "aggregate": {
    "average_task_count": 7.2,
    "average_variance": 0.45,
    "overall_consistency_percentage": 91.5,
    "can25_detection": {
      "total_prompts_with_can25": 2,
      "percentage": 22.2,
      "prompts_using_can25": [
        {"prompt_id": "Organizer-2", "consistency": "3/3"},
        {"prompt_id": "Organizer-1", "consistency": "1/3"}
      ]
    }
  }
}
```

---

## Statistical Confidence

### Sample Size

- **3 trials** × **9 prompts** = **27 observations**
- **95% Confidence Interval**: F1 = μ ± 1.96 × (σ / √n)

For V1.0 baseline (F1 = 78.40%, σ = 0.72%):
- **95% CI**: [77.0%, 79.8%]
- **Margin of Error**: ±1.4%

### Stability Threshold

**EXCELLENT**: Variance < 1% → Highly reproducible  
**GOOD**: Variance 1-2% → Acceptable for production  
**FAIR**: Variance 2-5% → Needs prompt refinement  
**POOR**: Variance > 5% → Unstable, requires investigation

---

## Troubleshooting

### High Variance Prompts

If a prompt shows variance > 2%:

1. **Check Prompt Ambiguity**: Does the prompt have multiple valid interpretations?
2. **Review Task Dependencies**: Are dependencies clearly stated?
3. **Analyze Varying Tasks**: Which tasks are inconsistent? Why?
4. **Refine Prompt Instructions**: Add explicit guidance for edge cases

**Example from V1.0**:
- **organizer-1**: 68.48% ± 6.00% → High variance
- **Root Cause**: "Prioritize invitations" - unclear if CAN-02A or CAN-02B or both
- **Fix**: Enhanced prompt with "Use BOTH CAN-02 and CAN-03 for prioritization"

### CAN-25 Not Detected

If CAN-25 missing in Organizer-2:

1. **Check Keyword Matching**: Does "flag" trigger CAN-25?
2. **Review System Prompt**: Is CAN-25 guidance clear?
3. **Analyze GPT-5 Response**: What reasoning did GPT-5 provide?
4. **Compare to Gold Standard**: Is CAN-25 actually needed?

---

## Files and Tools

### Created Files

1. **`tools/gpt5_execution_composer_v2.py`** (800+ lines)
   - V2.0 composer with 25 canonical tasks
   - Optimized system prompts with CAN-25 guidance
   - Enhanced keyword matching for specialized tasks

2. **`tools/run_gpt5_stability_test_v2.py`** (400+ lines)
   - 3-trial batch runner for V2.0
   - CAN-25 detection statistics
   - Stability analysis with V2.0 metrics

3. **`tools/compute_gpt5_average_v2.py`** (300+ lines)
   - Average performance calculator
   - Comparison to V2.0 gold standard
   - Precision/recall/F1 metrics

4. **`docs/gutt_analysis/CANONICAL_TASKS_REFERENCE_V2.md`** (1,500+ lines)
   - Complete 25 tasks reference library
   - CAN-25 specification and examples
   - Renumbered task IDs (1-25)

### Usage

```bash
# Full stability test workflow
python tools/run_gpt5_stability_test_v2.py         # Run 3 trials
python tools/compute_gpt5_average_v2.py            # Compute averages
python tools/compare_v1_v2_stability.py            # Compare V1 vs V2

# Single-prompt testing
python tools/gpt5_execution_composer_v2.py "Help me track all my important meetings this week and flag any that require focus time to prepare for them." --prompt-id Organizer-2

# View results
cat docs/gutt_analysis/model_comparison/gpt5_stability_v2/gpt5_v2_stability_analysis_*.json
```

---

## Next Steps

After completing V2.0 stability test:

1. ✅ **Validate CAN-25 Detection**: Confirm Organizer-2 uses CAN-25 consistently
2. ✅ **Compare V1 vs V2**: Analyze impact of framework changes
3. ✅ **Update Gold Standard**: Incorporate V2.0 human evaluation results
4. ✅ **Generate Comparison Report**: Document V1→V2 improvements
5. ❓ **Create V2 Evaluation UX**: Build web tool for human validation of V2 results

---

## References

- **V1.0 Stability Test**: `.cursorrules` (Lines 913-1010)
- **V1.0 Baseline**: 78.40% F1 ± 0.72% (November 7, 2025)
- **Gold Standard V2**: `v2_gold_standard_20251107_145124.json`
- **Framework V2.0**: `CANONICAL_TASKS_REFERENCE_V2.md`

---

**Document Version**: 1.0  
**Last Updated**: November 7, 2025  
**Author**: GitHub Copilot (guided by Chin-Yew Lin)
