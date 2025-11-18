# Workback Plan Test Scenario Generator

Automated generation of realistic test scenarios and workback plans for quality evaluation using gpt-oss:120b.

## Overview

This tool generates **33 test scenarios** (3 per meeting type × 11 meeting types) with realistic "movie set" contexts, then creates **99 workback plans** (3 quality levels per scenario) for comprehensive evaluation testing.

**Total Output**:
- 33 realistic scenarios with company/team context
- 99 workback plans (33 scenarios × 3 quality levels)
- Quality levels: Low, Medium, High

## Meeting Types Covered

1. **Weekly Newsletter** (T-7) - Low complexity
2. **Sprint Planning** (T-14) - Medium complexity
3. **Monthly Business Review** (T-30) - High complexity
4. **Feature Launch** (T-30) - High complexity
5. **Squad Mission Planning** (T-42 to T-56) - Medium-High complexity
6. **Quarterly Business Review** (T-60) - Very High complexity
7. **Annual Kickoff** (T-60) - High complexity
8. **Major Product Launch** (T-90) - Very High complexity
9. **Strategic Offsite** (T-90) - Very High complexity
10. **Board Meeting** (T-90) - Very High complexity
11. **M&A Integration** (T-90+) - Extreme complexity

## Quick Start

### Generate All Scenarios and Plans (Full Suite)

```bash
# Generate 33 scenarios + 99 workback plans (takes ~2-3 hours)
python src/workback_planning/generate_test_scenarios.py
```

This will create:
- `data/workback_scenarios/master_index.json` - Complete index of all scenarios
- `data/workback_scenarios/{type}_scenario_{num}.json` - Individual scenario files
- `data/workback_scenarios/{type}_scenario_{num}_{quality}.json` - Workback plans

### Generate Scenarios Only (Faster)

```bash
# Generate scenarios without workback plans (takes ~30 minutes)
python src/workback_planning/generate_test_scenarios.py --scenario-only
```

### Generate for Specific Meeting Type

```bash
# Generate only Sprint Planning scenarios
python src/workback_planning/generate_test_scenarios.py --meeting-type 2_sprint_planning

# Generate only Squad Mission scenarios
python src/workback_planning/generate_test_scenarios.py --meeting-type 5_squad_mission
```

### Custom Number of Scenarios

```bash
# Generate 5 scenarios per meeting type (instead of default 3)
python src/workback_planning/generate_test_scenarios.py --scenarios 5
```

## Usage Examples

### Example 1: Quick Test with Simple Meeting Type

```bash
# Generate newsletter scenarios only (fastest, ~5 minutes)
python src/workback_planning/generate_test_scenarios.py \
    --meeting-type 1_weekly_newsletter \
    --scenarios 2
```

### Example 2: Generate Scenarios for Evaluation Framework Testing

```bash
# Generate scenarios for 4 key meeting types (Newsletter, MBR, QBR, Launch)
for type in 1_weekly_newsletter 3_monthly_business_review 6_quarterly_business_review 8_major_product_launch; do
    python src/workback_planning/generate_test_scenarios.py --meeting-type $type
done
```

### Example 3: Just Generate Scenarios, Create Plans Later

```bash
# Step 1: Generate all scenarios (30 minutes)
python src/workback_planning/generate_test_scenarios.py --scenario-only

# Step 2: Manually review scenarios, then generate plans
# (modify script to load existing scenarios)
```

## Output Structure

```
data/workback_scenarios/
├── master_index.json                              # Complete index
├── 1_weekly_newsletter_scenario_1.json           # Scenario 1
├── 1_weekly_newsletter_scenario_1_low.json       # Low quality plan
├── 1_weekly_newsletter_scenario_1_medium.json    # Medium quality plan
├── 1_weekly_newsletter_scenario_1_high.json      # High quality plan
├── 1_weekly_newsletter_scenario_2.json           # Scenario 2
├── 1_weekly_newsletter_scenario_2_low.json
├── 1_weekly_newsletter_scenario_2_medium.json
├── 1_weekly_newsletter_scenario_2_high.json
├── 1_weekly_newsletter_scenario_3.json           # Scenario 3
├── 1_weekly_newsletter_scenario_3_low.json
├── 1_weekly_newsletter_scenario_3_medium.json
├── 1_weekly_newsletter_scenario_3_high.json
├── 1_weekly_newsletter_all_scenarios.json        # All newsletter scenarios
├── 2_sprint_planning_scenario_1.json             # Sprint planning starts
... (continues for all 11 meeting types)
└── 11_ma_integration_scenario_3_high.json        # Last plan
```

## Scenario Structure

Each scenario JSON contains:

```json
{
  "scenario_name": "Q4 Product Marketing Newsletter",
  "company_context": "TechCorp Inc., B2B SaaS, Product Marketing team of 12",
  "meeting_event_details": "Newsletter sent every Friday at 9 AM PST",
  "stakeholders": [
    "Sarah Chen (Content Creator, Senior Marketing Manager)",
    "Mike Johnson (Reviewer, Director of Product Marketing)",
    "Lisa Wong (Approver, VP Marketing)",
    "James Park (Marketing Ops, Newsletter Distribution)"
  ],
  "deliverables": [
    "Newsletter content (500-750 words)",
    "Hero image and graphics",
    "Distribution list (1,500 subscribers)"
  ],
  "success_criteria": [
    "Open rate > 35%",
    "Click-through rate > 8%",
    "Published on time every Friday at 9 AM"
  ],
  "constraints": [
    "Must include executive quote",
    "Legal review required for customer stories",
    "Approval needed by Thursday 5 PM"
  ],
  "workback_prompt": "Create a workback plan for TechCorp's weekly Product Marketing newsletter sent every Friday at 9 AM PST...",
  "meeting_type": "Weekly Team Newsletter",
  "meeting_type_key": "1_weekly_newsletter",
  "scenario_number": 1,
  "horizon": "T-7",
  "complexity": "Low"
}
```

## Workback Plan Quality Levels

### Low Quality Characteristics
- Missing key tasks or phases
- Vague task descriptions ("work on content", "handle stuff")
- Few or no dependencies defined
- Missing stakeholder assignments
- No milestones or poorly defined milestones
- Unrealistic timelines
- No risk consideration
- Minimal deliverables identified

**Expected ACRUE Score**: 50-65%

### Medium Quality Characteristics
- Most major tasks present but some gaps
- Reasonable task descriptions
- Some dependencies defined
- Most tasks have owners
- Milestones present but may lack detail
- Generally realistic timelines
- Some consideration of risks
- Key deliverables identified

**Expected ACRUE Score**: 70-80%

### High Quality Characteristics
- Comprehensive task coverage
- Clear, actionable task descriptions
- Well-defined dependencies
- All tasks assigned to specific owners
- Clear milestones with completion criteria
- Realistic timelines with buffers
- Proactive risk management
- Complete deliverable list

**Expected ACRUE Score**: 85-95%

## Using Generated Data for Evaluation

### Step 1: Generate Test Suite

```bash
python src/workback_planning/generate_test_scenarios.py
```

### Step 2: Run ACRUE Evaluation

```python
from src.workback_planning.evaluator.assertion_evaluator import WorkbackPlanAssertionEvaluator
import json

# Load generated plans
with open('data/workback_scenarios/1_weekly_newsletter_scenario_1_high.json') as f:
    plan_data = json.load(f)

# Evaluate with ACRUE framework
evaluator = WorkbackPlanAssertionEvaluator(judge_llm="gpt-4")
evaluation = evaluator.evaluate_all(
    plan_data['plan'],
    plan_data['workback_prompt']
)

# Generate report
report = evaluator.generate_report(evaluation)
print(report)
```

### Step 3: Compare Quality Levels

```python
# Evaluate all 3 quality levels for a scenario
for quality in ['low', 'medium', 'high']:
    with open(f'data/workback_scenarios/1_weekly_newsletter_scenario_1_{quality}.json') as f:
        plan_data = json.load(f)
    
    evaluation = evaluator.evaluate_all(plan_data['plan'], plan_data['workback_prompt'])
    print(f"{quality.upper()}: {evaluation['overall_score']}/100")
```

Expected output:
```
LOW: 58.5/100 (Poor tier)
MEDIUM: 76.0/100 (Acceptable tier)
HIGH: 89.5/100 (Good tier)
```

### Step 4: Model Comparison

```python
# Generate plans with different models for comparison
models = ["gpt-oss:20b", "gpt-oss:120b", "gpt-4o", "claude-opus-3"]

for model in models:
    generator = ScenarioGenerator(model=model)
    # Generate plans and evaluate
```

## Performance Estimates

**Full generation (33 scenarios × 3 plans = 99 plans)**:
- Time: ~2-3 hours with gpt-oss:120b
- LLM calls: ~132 (33 scenarios + 99 plans)

**Scenarios only (33 scenarios)**:
- Time: ~30 minutes
- LLM calls: 33

**Single meeting type (3 scenarios × 3 plans = 9 plans)**:
- Time: ~15-20 minutes
- LLM calls: 12

## Troubleshooting

### Issue: JSON parsing errors

**Solution**: The LLM might return malformed JSON. Check logs and retry:
```bash
# Add verbose logging
python src/workback_planning/generate_test_scenarios.py --meeting-type 1_weekly_newsletter 2>&1 | tee generation.log
```

### Issue: Ollama connection errors

**Solution**: Ensure Ollama is running:
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Start Ollama if needed
ollama serve

# Verify gpt-oss:120b is available
ollama list | grep gpt-oss
```

### Issue: Plans are too similar across quality levels

**Solution**: The quality level instructions might be too subtle. Review generated plans and adjust `quality_instructions` in `generate_workback_plan()` method.

### Issue: Out of memory

**Solution**: Generate one meeting type at a time:
```bash
for type in {1..11}; do
    python src/workback_planning/generate_test_scenarios.py --meeting-type ${type}_*
done
```

## Advanced Usage

### Custom Quality Level Instructions

Edit `generate_test_scenarios.py` to modify quality characteristics:

```python
quality_instructions = {
    "low": """Your custom low quality instructions...""",
    "medium": """Your custom medium quality instructions...""",
    "high": """Your custom high quality instructions..."""
}
```

### Using Different LLM Models

```bash
# Use GPT-4 instead of gpt-oss:120b
python src/workback_planning/generate_test_scenarios.py --model gpt-4

# Use Claude
python src/workback_planning/generate_test_scenarios.py --model claude-opus-3
```

### Batch Processing

```bash
# Generate scenarios in parallel (requires GNU parallel)
parallel -j 4 python src/workback_planning/generate_test_scenarios.py --meeting-type {} ::: \
    1_weekly_newsletter \
    2_sprint_planning \
    3_monthly_business_review \
    4_feature_launch
```

## Next Steps

1. **Generate full test suite**: Run full generation to create 99 workback plans
2. **Implement ACRUE evaluator**: Build `WorkbackPlanAssertionEvaluator` class
3. **Evaluate all plans**: Run ACRUE evaluation on all 99 plans
4. **Analyze results**: Compare low/medium/high quality scores
5. **Model comparison**: Generate plans with multiple LLMs and compare
6. **Iterate on prompts**: Refine quality instructions based on evaluation results

## Related Documentation

- [Workback Plan Meeting Types V1.0](../../docs/workback_planning/WORKBACK_PLAN_MEETING_TYPES_V1.md)
- [Workback Plan Evaluation Framework V1.0](../../docs/workback_planning/WORKBACK_PLAN_EVALUATION_FRAMEWORK_V1.md)
- [Workback Plan Canonical Tasks V1.0](../../docs/workback_planning/WORKBACK_PLAN_CANONICAL_TASKS_V1.md)

---

**Created**: November 17, 2025  
**Model**: gpt-oss:120b (default)  
**Output**: 33 scenarios, 99 workback plans  
**Evaluation Framework**: ACRUE (50 assertions)
