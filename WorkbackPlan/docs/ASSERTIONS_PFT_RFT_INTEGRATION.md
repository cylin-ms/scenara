# How ACRUE Assertions Support PFT + RFT Training

**Date**: November 18, 2025  
**Author**: Chin-Yew Lin  
**Purpose**: Explain how our assertion framework integrates with modern PFT+RFT training approach

---

## Executive Summary

Our **ACRUE assertion framework** (50+ assertions) serves **different but complementary roles** in PFT and RFT training:

| Training Phase | Assertion Role | Data Generated | Purpose |
|----------------|----------------|----------------|---------|
| **PFT (DPO)** | Quality ranking | Preference pairs (better vs worse plans) | Learn planning preferences via holistic quality comparison |
| **RFT (Light RL)** | Procedural correctness | Binary rewards (+1/0) for workflow steps | Verify tool execution accuracy, not subjective quality |
| **SFT** | Validation | Filter out low-quality expert plans (<70% pass rate) | Bootstrap with only high-quality examples |

---

## 1. PFT: Assertions Generate Preference Pairs

### 1.1 The Challenge with PFT Training Data

**Problem**: DPO requires preference pairs (better_plan, worse_plan), but human labeling doesn't scale:
- Cost: $50-100 per comparison (2 experts × 15 min each)
- Time: 1000 pairs = 250 hours of expert time
- Consistency: Different experts may disagree on "better"

**Solution**: Use LLM-as-Judge with ACRUE assertions to automate preference pair generation

### 1.2 Assertion-Based Preference Pair Generation

```python
def generate_preference_pair(scenario):
    # 1. Generate multiple candidate plans
    plan_A = model.generate(scenario, temperature=0.8)
    plan_B = model.generate(scenario, temperature=1.2)
    plan_C = model.generate(scenario, temperature=1.5)
    
    # 2. Evaluate each with ACRUE assertions (LLM-as-Judge)
    score_A = evaluate_assertions(plan_A, acrue_checklist_50)
    score_B = evaluate_assertions(plan_B, acrue_checklist_50)
    score_C = evaluate_assertions(plan_C, acrue_checklist_50)
    
    # 3. Select best and worst (need 15%+ score gap)
    if max(scores) - min(scores) >= 0.15:
        better_plan = candidates[argmax(scores)]
        worse_plan = candidates[argmin(scores)]
        
        # 4. Document specific assertion failures for explainability
        return {
            "scenario": scenario,
            "better": {
                "plan": better_plan,
                "acrue_score": 0.88,
                "passed": ["A1", "A2", "C1-C5", "R1-R3", "U1"],
                "failed": ["E1", "E2"]
            },
            "worse": {
                "plan": worse_plan,
                "acrue_score": 0.62,
                "passed": ["A1", "R1", "U1"],
                "failed": ["A2", "C2", "C3", "C4", "R2", "U2"]
            },
            "key_differences": [
                "Better plan has complete milestone chain (C2)",
                "Better plan identifies backup presenter (U2)",
                "Worse plan has unrealistic 3-day finalization (A2)"
            ]
        }
```

### 1.3 PFT Training Data Requirements

**Per Vertical (e.g., QBR, M&A, Board Prep)**:
- **50 preference pairs minimum**
- **Quality gap**: ≥15% score difference (e.g., 88% vs 62%)
- **Diversity**: Balanced across ACRUE categories
  * 10 pairs testing Accuracy (dependencies, timelines)
  * 15 pairs testing Completeness (missing milestones, tasks)
  * 10 pairs testing Relevance (goal alignment, context fit)
  * 10 pairs testing Usefulness (actionability, executability)
  * 5 pairs testing Exceptional (risk mitigation, contingencies)

**Quality Control**:
- Human spot-check 10-20% of pairs
- Reject pairs where LLM Judge uncertainty is high
- Monitor for bias (e.g., always preferring longer plans)

### 1.4 Example Preference Pair for PFT

**Scenario**: QBR on Dec 15, 2025 with CEO, CFO, 20 stakeholders

**Better Plan** (ACRUE: 0.88, 44/50 assertions passed):
```yaml
Strengths:
- Complete milestone chain: Data collection (T-21) → Draft (T-14) → Review (T-7) → Lock (T-3)
- Identified backup presenter (COO) in case SVP unavailable
- Tech readiness check scheduled T-1
- All task owners are meeting attendees
- Realistic timeline: 3 weeks for data collection, 2 weeks for deck creation

Failed assertions:
- E1: No proactive risk mitigation documented
- E2: No contingency plan for late financial data
```

**Worse Plan** (ACRUE: 0.62, 31/50 assertions passed):
```yaml
Weaknesses:
- Missing data collection milestone entirely (C2 fail)
- Deck finalization in only 3 days (A2 fail - unrealistic)
- No tech readiness check (C3 fail)
- Task owner "John Smith" not in attendee list (A4 fail)
- No backup presenter identified (U2 fail)

Passed assertions:
- Goal correctly extracted (A1)
- Relevant to QBR meeting type (R1)
- Basic structure present (U1)
```

**PFT learns**: "Plans with complete milestone chains, realistic timelines, and backup presenters are better than plans missing key milestones and with unrealistic deadlines."

---

## 2. RFT: Assertions Verify Workflow Correctness

### 2.1 The Challenge with RFT Training

**Problem**: RFT needs procedural correctness signals, not subjective quality scores

**Examples of Workflow Correctness**:
- ✅ M2 depends on M1 (correct dependency chain)
- ❌ M1 depends on M2 (circular dependency)
- ✅ Task assigned to meeting attendee
- ❌ Task assigned to external person not in meeting
- ✅ 14 working days = 20 calendar days (accounting for weekends)
- ❌ 14 calendar days = 10 working days (incorrect math)

### 2.2 Assertion-Based RFT Rewards

**RFT Focus** (not holistic quality, just procedural correctness):

```python
def calculate_rft_reward(plan, scenario):
    reward = 0.0
    
    # Reward 1: Dependency chain correctness (A5 assertion)
    if check_no_circular_dependencies(plan.milestones):
        reward += 1.0
    if check_dependencies_exist(plan.milestones):
        reward += 1.0
    
    # Reward 2: Timeline validation (A2, A3 assertions)
    if check_working_days_correct(plan.milestones):
        reward += 1.0
    if check_no_impossible_timelines(plan.milestones):
        reward += 1.0
    
    # Reward 3: Stakeholder mapping (A4 assertion)
    if check_task_owners_in_attendees(plan.tasks, scenario.attendees):
        reward += 1.0
    
    # Reward 4: Constraint satisfaction (A3 assertion)
    if check_respects_holiday_blackouts(plan.milestones, scenario.holidays):
        reward += 1.0
    
    return reward  # Range: 0.0 to 6.0
```

### 2.3 RFT Training Data Requirements

**Per Vertical**:
- **100-200 workflow scenarios**
- **Binary rewards** (correct=+1, incorrect=0)
- **Focus on common errors**:
  * Circular dependencies (M1 → M2 → M3 → M1)
  * Missing critical path milestones
  * Timezone calculation errors
  * Task ownership misassignments
  * Holiday/weekend miscalculations

**Key Distinction from PFT**:
| Aspect | PFT (Preference Learning) | RFT (Workflow Correctness) |
|--------|---------------------------|----------------------------|
| **Input** | 2 complete plans | Single plan + expected workflow |
| **Output** | Preference ranking | Binary correctness signal |
| **Focus** | Holistic quality | Procedural accuracy |
| **Assertions** | All 50 ACRUE assertions | Subset: A2-A5 (accuracy only) |
| **Example** | "Plan A better than Plan B because more complete" | "Dependency chain correct: +1 reward" |

### 2.4 Example RFT Scenario

**Scenario**: Board meeting on Jan 15, 2026 (T=0)

**Correct Workflow** (Reward: +6):
```yaml
✅ M1 (T-60): Data collection complete
✅ M2 (T-30): First draft complete [depends on M1]
✅ M3 (T-14): CEO review [depends on M2]
✅ M4 (T-7): Final lock [depends on M3]
✅ All task owners in attendee list
✅ Working days calculated correctly (60 calendar days = ~42 working days)
```

**Incorrect Workflow** (Reward: +2):
```yaml
❌ M1 (T-30): Data collection [should start T-60, too late]
✅ M2 (T-20): First draft [depends on M1] ✓
❌ M3 (T-25): CEO review [BEFORE M2, impossible!]
❌ M4 (T-7): Final lock [circular dependency: M4→M1]
✅ Task owners correct ✓
❌ Working days wrong (30 calendar days ≠ 42 working days)
```

**RFT learns**: "Dependencies must flow forward in time, working days must account for weekends, task owners must be meeting attendees."

---

## 3. SFT: Assertions Filter Expert Plans

### 3.1 Quality Gate for Expert Data

**Challenge**: Not all "expert plans" are actually high quality

**Solution**: Use assertions to validate expert-provided plans before SFT training

```python
def validate_expert_plan(plan):
    score = evaluate_assertions(plan, acrue_checklist_50)
    
    if score >= 0.85:  # 85% threshold
        return "ACCEPT", "High-quality expert plan"
    elif score >= 0.70:
        return "REVIEW", "Borderline plan, needs human check"
    else:
        return "REJECT", f"Low quality: {score:.0%} pass rate"
```

### 3.2 SFT Training Data Requirements

**Per Vertical**:
- **25 expert plans** (after filtering)
- **Quality threshold**: ≥85% ACRUE pass rate (≥42/50 assertions)
- **Diversity**: Cover different complexity levels
  * 5 simple scenarios (small meetings, short timelines)
  * 15 medium scenarios (typical QBRs, product launches)
  * 5 complex scenarios (M&A, Board prep with many stakeholders)

**Rejection Criteria**:
- Missing critical milestones (C2, C3 failures)
- Unrealistic timelines (A2 failures)
- Irrelevant to meeting type (R1, R2 failures)

---

## 4. Complete Training Data Requirements

### 4.1 Per Vertical (e.g., QBR)

| Phase | Data Type | Quantity | Quality Requirement | Purpose |
|-------|-----------|----------|---------------------|---------|
| **SFT** | Expert plans | 25 | ≥85% ACRUE (42+/50) | Bootstrap domain knowledge |
| **PFT** | Preference pairs | 50 | 15% score gap | Learn planning preferences |
| **RFT** | Workflow scenarios | 100-200 | Binary correctness | Verify tool workflows |
| **Validation** | Holdout set | 5 | ≥90% ACRUE (45+/50) | Measure improvement |
| **Horizontal** | Other meeting types | 10-15 | ≥80% ACRUE (40+/50) | Prevent forgetting |

### 4.2 Total Dataset (4 Verticals)

| Phase | Total Scenarios | Total Assertions Evaluated | Est. LLM Judge Calls |
|-------|----------------|---------------------------|---------------------|
| **SFT filtering** | 100 plans | 5,000 (100×50) | 5,000 |
| **PFT generation** | 200 pairs (600 candidates) | 30,000 (600×50) | 30,000 |
| **RFT training** | 400-800 scenarios | 2,400-4,800 (400×6) | 4,000 |
| **Validation** | 80 plans | 4,000 (80×50) | 4,000 |
| **Total** | ~1,000 scenarios | ~41,000 assertion checks | ~43,000 LLM calls |

**Cost Estimate** (GPT-4 as judge):
- 43,000 calls × $0.02 per call ≈ **$860** for assertion evaluation
- Much cheaper than human labeling ($50-100 per comparison)

---

## 5. Implementation Workflow

### 5.1 Step-by-Step Process

```python
# Week 1-2: Collect and validate expert plans (SFT)
expert_plans = collect_expert_plans(vertical="QBR", count=30)
filtered_plans = [p for p in expert_plans 
                  if evaluate_assertions(p) >= 0.85]
assert len(filtered_plans) >= 25, "Need more expert plans"

# Week 3-4: Generate preference pairs (PFT)
preference_pairs = []
for scenario in scenarios:
    candidates = [model.generate(scenario, temp=t) 
                  for t in [0.8, 1.0, 1.2, 1.5, 1.8]]
    scores = [evaluate_assertions(c) for c in candidates]
    if max(scores) - min(scores) >= 0.15:
        best = candidates[argmax(scores)]
        worst = candidates[argmin(scores)]
        preference_pairs.append((scenario, best, worst))

assert len(preference_pairs) >= 50, "Need more preference pairs"

# Week 5-6: Create workflow scenarios (RFT)
workflow_scenarios = []
for scenario in scenarios:
    # Generate correct and incorrect variants
    correct_plan = create_correct_workflow(scenario)
    incorrect_plans = introduce_workflow_errors(correct_plan)
    workflow_scenarios.extend([
        (scenario, correct_plan, reward=6),
        *[(scenario, p, reward=calculate_reward(p)) 
          for p in incorrect_plans]
    ])

assert len(workflow_scenarios) >= 100, "Need more RFT scenarios"

# Week 7-8: Train models
sft_model = train_sft(filtered_plans)
pft_model = train_dpo(sft_model, preference_pairs)
rft_model = train_light_rl(pft_model, workflow_scenarios)
```

### 5.2 Quality Assurance

**Human Validation Loop**:
1. Sample 10% of preference pairs for human review
2. Check agreement rate between LLM Judge and human experts
3. If agreement <80%, refine assertion definitions
4. Retrain LLM Judge or adjust assertion weights

**Monitoring Metrics**:
- Preference pair quality gap (target: 15-25%)
- RFT reward distribution (avoid all +6 or all 0)
- Validation set ACRUE scores (target: 90%+ after training)
- Horizontal set regression (alert if drop >5%)

---

## 6. Key Takeaways

### 6.1 Assertions Serve Multiple Purposes

✅ **PFT**: Generate preference pairs at scale via automated quality ranking  
✅ **RFT**: Verify procedural correctness with binary rewards  
✅ **SFT**: Filter out low-quality expert plans before training  
✅ **Evaluation**: Continuous validation during and after training  

### 6.2 Why This Approach Works

1. **Scalable**: Automate preference pair generation (1000s vs manual labeling)
2. **Consistent**: Same rubric applied to all evaluations
3. **Explainable**: Each preference has documented assertion failures
4. **Refinable**: Can adjust assertion weights based on what matters most
5. **Cost-effective**: $860 for assertion evaluation vs $50K+ for human labeling

### 6.3 Integration with Proposal

This assertion-based approach is **fully compatible** with the training strategy in Section 4 of the proposal:

- **SFT (Weeks 1-2)**: Use assertions to filter expert plans (≥85% pass rate)
- **PFT (Weeks 3-4)**: Use assertions to generate 50 preference pairs per vertical
- **RFT (Weeks 5-6)**: Use assertions to create 100-200 workflow scenarios
- **Evaluation (Weeks 7-12)**: Use assertions to validate improvements

**Total training data needed per vertical**: 25 expert plans + 50 preference pairs + 150 workflow scenarios = **~225 scenarios**

**Total cost per vertical**: $860 assertion evaluation + $780 compute = **$1,640**

**Total cost (4 verticals)**: $1,640 × 4 = **$6,560** (vs $3,120 compute-only estimate, now includes assertion evaluation)

---

## 7. Next Steps

1. **Validate LLM-as-Judge reliability** with human agreement study (Week 1)
2. **Generate first preference pairs** for QBR vertical (Week 2-3)
3. **Create RFT workflow scenarios** with common errors (Week 4)
4. **Run SFT → PFT → RFT pipeline** on 1 vertical (Weeks 5-6)
5. **Measure ACRUE improvement** before/after training (Week 7)
6. **Scale to remaining verticals** if results validate approach (Weeks 8-12)

