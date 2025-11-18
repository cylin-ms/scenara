**Author**: Chin-Yew Lin  
**Created**: November 17, 2025  
**Based on**: Copilot Researcher Domain-Expertise Integration Pipeline

---

# Workback Planning Domain-Expertise Integration Proposal

## Executive Summary

This proposal adapts the **Copilot Researcher Domain-Expertise Integration Pipeline** methodology for our **Workback Planning (WBP)** system. By applying their proven framework for post-training data generation and domain specialization, we can systematically enhance WBP quality from the current **GUTT v4.0 ACRUE baseline** (70-80% accuracy on 31 meeting types) to **enterprise-grade precision** (95%+ accuracy with domain-specific expertise).

**Key Insight**: The Researcher team's success comes from combining (1) expert-curated datasets with detailed rubrics, (2) rigorous ACRUE evaluation frameworks (Accuracy, Completeness, Relevance, Usefulness, Exceptional), and (3) iterative fine-tuning with real user feedback. We already have 80% of their infrastructure—we need to adapt their vertical selection and expert data collection methodology.

---

## 1. Vertical Selection Framework

### Our Adaptation: Meeting-Type Based Vertical Selection

Following Researcher's **4-criteria persona scoring** (Complexity, Business Impact, Standardization, Data Availability), we score each of our **31 meeting types** to prioritize which verticals to optimize first.

#### Scoring Rubric (1-4 scale per criterion)

| Criterion | Definition for WBP | Measurement Signals |
|-----------|-------------------|---------------------|
| **Complexity of Workflow Data** | How scattered and heterogeneous the meeting context, stakeholder relationships, task dependencies, and timeline constraints are | Number of attendees, cross-functional dependencies, parallel workstreams, artifact types, timeline horizon (T-7 to T-90+) |
| **Business Impact** | Expected measurable value to S500 customers (risk reduction, timeline accuracy, stakeholder alignment, decision quality) | Stakeholder seniority (exec/board/team), decision criticality (M&A/QBR/product launch), external exposure, cost of schedule slippage |
| **Standardization of Output** | How well workback plans can be expressed in repeatable structures (phases, tasks, deliverables, participants, dependencies) | Template availability (CXA examples), industry best practices, regulatory requirements, existing frameworks (agile/waterfall) |
| **Domain Data Availability** | Access to sufficient, representative meeting contexts, workback plan examples, and expert-validated templates | Public examples (CXA templates), internal Microsoft data, industry frameworks, customer case studies |

### Initial Vertical Prioritization

Based on our **33 scenarios across 99 workback plans**, we score the top candidates:

| Meeting Type | Complexity | Business Impact | Standardization | Data Availability | **Total** | Priority |
|--------------|-----------|-----------------|-----------------|-------------------|-----------|----------|
| **M&A Integration Planning (T-90+)** | 4 | 4 | 3 | 3 | **3.5** | **P0** |
| **Quarterly Business Review (T-60)** | 4 | 4 | 4 | 4 | **4.0** | **P0** |
| **Major Product Launch (T-90)** | 4 | 4 | 3 | 3 | **3.5** | **P0** |
| **Board Meeting Prep (T-90)** | 3 | 4 | 4 | 3 | **3.5** | **P0** |
| **Strategic Offsite (T-90)** | 3 | 4 | 3 | 3 | **3.25** | **P1** |
| **Squad Mission Planning (T-42 to T-56)** | 3 | 3 | 4 | 4 | **3.5** | **P1** |
| **Sprint Planning (T-14)** | 2 | 2 | 4 | 4 | **3.0** | **P2** |
| **Newsletter Launch (T-7)** | 1 | 1 | 3 | 4 | **2.25** | **P3** |

**Recommendation**: Focus Phase 1 on **Corporate Finance & Strategy** verticals (M&A, QBR, Product Launch, Board Prep) scoring ≥3.5, similar to Researcher's Finance/Legal focus.

---

## 2. Expert Data Collection

### Our Adaptation: Enterprise Planning Professional Dataset

Following Mercor's deliverable structure, we collect datasets for each meeting type vertical:

#### 2.1 Prompts (Meeting Scenarios)
- **Target**: 30 distinct meeting scenarios per vertical (e.g., 30 M&A integrations, 30 QBRs)
- **Complexity**: Professional-grade scenarios with realistic constraints:
  * **M&A Example**: "Plan Day 1 readiness for acquiring NeuroGenix (1200 employees, $850M revenue, Basel HQ) by Apex BioPharma ($12B revenue, 18K employees). Legal close: Dec 15, 2025. Integration kickoff: Dec 20. Capture $120M cost synergies Year 2, $200M revenue synergies Year 3. Cultural integration: US data-driven hierarchical vs European collaborative research-first."
  * **QBR Example**: "Plan Q4 2025 board review for TechCorp covering FY performance, strategic initiatives, competitive landscape, financial projections, and risk assessment. CEO presents to 7 board members including audit committee chair and external advisors."

#### 2.2 Evidence Documents (Meeting Context)
- **Target**: 3-10 documents per scenario
- **Document Types**:
  * Previous meeting notes/minutes
  * Strategic plans and roadmaps
  * Stakeholder org charts and Me Notes profiles
  * Financial reports and metrics
  * Project charters and requirements
  * Industry benchmarks and best practices
  * Regulatory/compliance requirements
- **Synthetic Enterprise Data**: Leverage our **user profile generator** (42 enterprise personas) to create realistic:
  * Email threads leading to the meeting
  * Teams chat conversations with task assignments
  * Calendar patterns showing stakeholder availability
  * Document collaboration history

#### 2.3 Evaluation Rubrics (Per-Scenario Quality Criteria)

This is the **centerpiece**. Each scenario gets a detailed rubric with 15-50 criteria, extending our **GUTT v4.0 ACRUE** framework:

##### Content Criteria (ACRUE - from GUTT v4.0)
- **Accuracy**: Correct task sequencing, realistic timelines, appropriate dependencies
  * *Example*: "T-90 M&A plan includes Day 1 readiness tasks at T-0, not T-30" (Critical)
  * *Example*: "Critical path identified correctly with no circular dependencies" (Major)
  
- **Completeness**: All necessary phases, tasks, deliverables, and stakeholders covered
  * *Example*: "M&A plan includes all 6 workstreams: HR, IT, Finance, Product, Sales, Legal" (Critical)
  * *Example*: "Each task has assigned owner from appropriate department" (Major)
  
- **Relevance**: Tasks appropriate for meeting type, timeline, and industry context
  * *Example*: "T-7 newsletter plan doesn't include board approval tasks" (Major)
  * *Example*: "Tech product launch includes beta testing, not manufacturing setup" (Minor)
  
- **Usefulness**: Actionable with clear next steps, dependencies, and decision points
  * *Example*: "Each milestone has clear go/no-go criteria" (Major)
  * *Example*: "Risk mitigation tasks identified with contingency plans" (Minor)
  
- **Exceptional**: Outstanding quality that exceeds baseline expectations
  * *Example*: "Includes proactive risk mitigation for top 3 failure modes" (Major)
  * *Example*: "Timeline optimization reduces critical path by 15% vs standard approach" (Minor)

##### Presentation Criteria (P - Style & Format)
- **Structure**: Proper phase breakdown, clear task grouping, logical flow
  * *Example*: "Plan organized into phases: Planning → Execution → Review → Follow-up" (Major)
  * *Example*: "Tasks grouped by workstream with clear ownership" (Minor)
  
- **Formatting**: Professional appearance, consistent naming, proper metadata
  * *Example*: "Task IDs follow pattern: workstream-phase-sequence (e.g., HR-01-003)" (Minor)
  * *Example*: "Deliverables clearly marked with @ notation" (Minor)
  
- **Tone**: Appropriate for stakeholder seniority and meeting criticality
  * *Example*: "Board-level plan uses formal language, no casual abbreviations" (Major)
  * *Example*: "Sprint planning uses agile terminology (story points, velocity)" (Minor)
  
- **Length**: Appropriate task count for timeline horizon and complexity
  * *Example*: "T-7 plan contains 15-25 tasks, not 100 tasks" (Major)
  * *Example*: "T-90+ M&A plan contains 70-100+ tasks across workstreams" (Critical)

##### Domain-Specific Criteria (Industry Best Practices)
- **Compliance**: Regulatory requirements for industry (finance, healthcare, legal)
  * *Example*: "M&A plan includes SOX compliance tasks for public company" (Critical)
  * *Example*: "Healthcare product launch includes FDA approval milestones" (Critical)
  
- **Framework Adherence**: Follows industry methodologies (agile, waterfall, MMM)
  * *Example*: "Squad mission uses Microsoft MMM framework (Mission, Metrics, Methods)" (Major)
  * *Example*: "Sprint planning follows Scrum framework with proper ceremonies" (Major)

#### JSON Rubric Format Example

```json
{
  "scenario_id": "ma-integration-001",
  "meeting_type": "M&A Integration Planning",
  "timeline_horizon": "T-90+",
  "rubric_version": "1.0",
  "criteria": [
    {
      "id": "accuracy-001",
      "category": "Accuracy",
      "description": "Plan includes Day 1 readiness tasks (payroll, ERP, security, communications) scheduled for T-0",
      "weight": "Critical",
      "binary_check": true,
      "dependencies": []
    },
    {
      "id": "completeness-001",
      "category": "Completeness",
      "description": "All 6 integration workstreams covered: HR, IT, Finance, Product Development, Sales & Marketing, Legal & Compliance",
      "weight": "Critical",
      "binary_check": false,
      "scoring": "partial_credit",
      "max_score": 6,
      "dependencies": []
    },
    {
      "id": "usefulness-005",
      "category": "Usefulness",
      "description": "Critical path identified with timeline dependencies marked",
      "weight": "Major",
      "binary_check": true,
      "dependencies": ["completeness-001"]
    },
    {
      "id": "presentation-003",
      "category": "Presentation",
      "description": "Tasks grouped by workstream with clear phase structure (Planning → Day 1 → 30/60/90 Day Milestones)",
      "weight": "Minor",
      "binary_check": true,
      "dependencies": []
    }
  ],
  "expected_task_count": {"min": 70, "max": 120, "optimal": 90},
  "expected_duration_days": {"min": 90, "max": 180, "optimal": 120}
}
```

#### 2.4 Golden Outputs (Expert-Validated Plans)

For each scenario, **T+P (Time and Places) PMs** produce the **ideal workback plan**:
- Complete phase breakdown
- All tasks with dependencies, owners, deliverables
- Realistic timeline with critical path
- Stakeholder assignments with role clarity
- Risk mitigation and contingency plans

**Our Domain Experts**: **T+P (Time and Places) PMs** are the gold standard for workback planning expertise. They:
- Manage Microsoft's calendar, scheduling, and meeting intelligence systems
- Plan complex meeting workflows from T-7 newsletters to T-90+ M&A integrations
- Master all 31 meeting types with deep understanding of executive and operational planning
- Understand enterprise scheduling dynamics, stakeholder coordination, and meeting preparation
- Know Microsoft's internal processes for QBRs, board meetings, product launches, strategic offsites
- Have battle-tested templates and best practices from managing thousands of critical meetings

**Sources for Golden Plans**:
1. **T+P PM Templates** (primary): Meeting preparation workflows, executive scheduling, QBR planning
2. **CXA Templates** (existing): slide05, slide07 workback examples for executive meetings
3. **Microsoft Internal**: IPG Patents Group, Finance org, real project plans
4. **Industry Best Practices**: PMI templates, agile frameworks, consulting firm deliverables

---

## 3. Pipeline Integration & Evaluation

### 3.1 Grounding Data Strategy (Two Approaches)

Following Researcher's dual approach:

#### Approach A: Direct Context Provision (Simplified RAG)
- **Method**: Disable search tools, provide supplied documents directly as context
- **Pros**: Simpler to implement, isolates reasoning quality from retrieval quality
- **Cons**: Doesn't test end-to-end Workback Plan agent capabilities
- **Use Case**: Initial baseline evaluation, SFT data generation

#### Approach B: Synthetic Tenant with Realistic Data Trail
- **Method**: Build communication trail in synthetic Microsoft 365 tenant:
  * Meeting invites with proper attendees and agenda
  * Email threads with task assignments and updates
  * Teams chats with informal discussions
  * SharePoint documents with versioning history
  * Calendar patterns showing availability constraints
- **Pros**: Tests full Workback Plan agent pipeline, realistic enterprise complexity
- **Cons**: Higher implementation complexity, requires synthetic data generation
- **Use Case**: Final evaluation, production readiness testing

**Our Recommendation**: Start with **Approach A** for rapid prototyping, transition to **Approach B** for production validation.

### 3.2 Automated Scoring Using Rubrics

Implement `score_workback_plan(output, rubric_set)` function:

```python
def score_workback_plan(
    plan: WorkbackPlan,
    rubric: Dict[str, Any],
    llm_client: LLMAPIClient
) -> Dict[str, Any]:
    """
    Score workback plan against rubric criteria.
    
    Args:
        plan: Generated workback plan (WorkbackPlan model)
        rubric: Evaluation rubric with criteria list
        llm_client: LLM for evaluating nuanced criteria
    
    Returns:
        scores: Per-criterion scores + overall ACRUE score
    """
    scores = {
        "criteria_scores": [],
        "category_scores": {},
        "overall_score": 0.0,
        "critical_failures": [],
        "major_issues": [],
        "minor_issues": []
    }
    
    for criterion in rubric["criteria"]:
        if criterion["binary_check"]:
            # Binary evaluation via LLM
            score = evaluate_binary_criterion(plan, criterion, llm_client)
        else:
            # Graded evaluation with partial credit
            score = evaluate_graded_criterion(plan, criterion, llm_client)
        
        scores["criteria_scores"].append({
            "id": criterion["id"],
            "score": score,
            "weight": criterion["weight"]
        })
        
        # Track failures by severity
        if score < 1.0:
            if criterion["weight"] == "Critical":
                scores["critical_failures"].append(criterion)
            elif criterion["weight"] == "Major":
                scores["major_issues"].append(criterion)
            else:
                scores["minor_issues"].append(criterion)
    
    # Calculate weighted overall score
    scores["overall_score"] = calculate_weighted_score(
        scores["criteria_scores"]
    )
    
    # Calculate ACRUE category scores (+ Presentation for style)
    scores["category_scores"] = {
        "Accuracy": avg([s for s in scores["criteria_scores"] if s["category"] == "Accuracy"]),
        "Completeness": avg([s for s in scores["criteria_scores"] if s["category"] == "Completeness"]),
        "Relevance": avg([s for s in scores["criteria_scores"] if s["category"] == "Relevance"]),
        "Usefulness": avg([s for s in scores["criteria_scores"] if s["category"] == "Usefulness"]),
        "Exceptional": avg([s for s in scores["criteria_scores"] if s["category"] == "Exceptional"]),
        "Presentation": avg([s for s in scores["criteria_scores"] if s["category"] == "Presentation"])
    }
    
    return scores
```

### 3.3 Evaluation Sets & Validation Strategy

Following Researcher's holdout approach:

- **Training Set**: 25 scenarios per vertical (30 total - 5 holdout)
- **Validation Set**: 5 scenarios per vertical (held out for testing)
- **Horizontal Set**: Original 33 scenarios across 31 meeting types (ensure no regression)

**Success Criteria**:
- **Vertical Improvement**: ≥15% improvement on vertical rubric scores vs baseline
- **Horizontal Stability**: <5% regression on horizontal ACRUE scores
- **User Satisfaction**: ≥4.0/5.0 rating from early adopters

---

## 4. Fine-Tuning Strategy

### 4.1 Training Approach (PFT + RFT)

Following industry best practices from Microsoft, OpenAI, Anthropic, and Meta:

1. **Supervised Fine-Tuning (SFT)** - Bootstrap with expert plans
   - Start with 25 expert-validated (prompt, context, golden_plan) triplets per vertical
   - Learn domain-specific patterns, terminology, and structure
   - Baseline model: o3-DR or gpt-oss:120b (our current production model)

2. **Preference Fine-Tuning (PFT)** - DPO-style alignment
   - Use pairwise preference data: (prompt, context, better_plan, worse_plan)
   - Direct Preference Optimization (DPO) instead of classical RLHF
   - Optimizes for: clarity, actionability, accuracy, structured reasoning
   - Avoids RLHF issues: overly cautious outputs, generic "management speak", hedging behavior
   - **Why PFT?** Project planning requires decisive recommendations and concrete milestones, not safe/verbose outputs

3. **Reinforcement Fine-Tuning (RFT)** - Light RL for tool workflows
   - Used only for procedural correctness in tool-use sequences
   - Not for planning text quality (that's handled by PFT)
   - Example: "If model correctly identifies critical path at step 3, reward +1"
   - Trains workflow correctness: dependency analysis, timeline validation, stakeholder mapping

4. **Counterfactual Augmentation**
   - Generate plan pairs with intentional quality differences
   - Train model to recognize superior planning patterns
   - Examples: complete vs incomplete stakeholder analysis, realistic vs optimistic timelines

### 4.2 How Assertions & LLMCheckList Support PFT + RFT Training

Our existing **ACRUE assertion framework** (50+ assertions in `WORKBACK_PLAN_EVALUATION_FRAMEWORK_V1.md`) plays different but complementary roles in PFT and RFT:

#### 4.2.1 Assertions in PFT (Preference Fine-Tuning)

**Role**: Generate high-quality preference pairs for DPO training

**Data Generation Process**:
```python
# 1. Generate two candidate plans for same scenario
plan_A = model.generate(scenario_context)
plan_B = model.generate(scenario_context, temperature=1.2)

# 2. Evaluate both with LLM-as-Judge using ACRUE assertions
score_A = llm_judge.evaluate_assertions(plan_A, assertion_checklist)
score_B = llm_judge.evaluate_assertions(plan_B, assertion_checklist)

# 3. Create preference pair based on assertion pass rates
if score_A > score_B + margin:
    preference_pair = (scenario, better=plan_A, worse=plan_B)
elif score_B > score_A + margin:
    preference_pair = (scenario, better=plan_B, worse=plan_A)
else:
    skip  # Too similar, not useful for learning
```

**Assertion Categories for PFT Preference Data**:
- **Accuracy assertions** → Prefer plans with correct dependencies, realistic timelines
- **Completeness assertions** → Prefer plans with all necessary milestones/tasks
- **Relevance assertions** → Prefer plans aligned with meeting type and goals
- **Usefulness assertions** → Prefer plans that are actionable and executable
- **Exceptional assertions** → Prefer plans with proactive risk mitigation, contingencies

**PFT Training Data Requirements** (per vertical):
- 50 preference pairs minimum
- Each pair needs clear quality difference (score gap ≥15%)
- Balanced across ACRUE categories (not all "completeness" issues)
- Mix of subtle differences (1-2 assertion failures) and obvious differences (5+ failures)

**Example Preference Pair**:
```json
{
  "scenario": "QBR meeting Dec 15, 2025 with CEO/CFO",
  "better_plan": {
    "acrue_score": 0.88,
    "passed_assertions": ["A1", "A2", "C1", "C2", "C3", "R1", "U1"],
    "strengths": "Complete milestone chain, realistic timelines, identified backup presenter"
  },
  "worse_plan": {
    "acrue_score": 0.62,
    "failed_assertions": ["C2", "C3", "U2"],
    "weaknesses": "Missing data collection milestone, no tech readiness check, unrealistic 3-day deck finalization"
  }
}
```

#### 4.2.2 Assertions in RFT (Reinforcement Fine-Tuning)

**Role**: Provide procedural correctness rewards for tool workflow training

**RFT Focus Areas** (not planning quality):
1. **Dependency Analysis Correctness**
   - Reward: +1 if model correctly identifies M2 depends on M1
   - Assertion check: A5 (dependency relationships are logically sound)
   
2. **Timeline Validation**
   - Reward: +1 if model catches impossible timelines (M2 before M1)
   - Assertion check: A2 (all dates/deadlines are feasible)
   
3. **Stakeholder Mapping**
   - Reward: +1 if model assigns tasks to attendees (not external people)
   - Assertion check: A4 (task owners match meeting attendees)

4. **Constraint Satisfaction**
   - Reward: +1 if plan respects holiday blackout dates
   - Assertion check: A3 (working days vs calendar days calculated correctly)

**RFT Training Data Requirements** (per vertical):
- 100-200 tool workflow scenarios
- Binary reward signals (correct=+1, incorrect=0)
- Focus on common procedural errors, not subjective quality
- Examples: circular dependencies, missing critical path, timezone errors

**Key Distinction**:
- **PFT uses assertions** to rank plan quality (holistic evaluation)
- **RFT uses assertions** to verify workflow steps (procedural correctness)

#### 4.2.3 LLMCheckList: Automated Preference Pair Generation

**Purpose**: Scale up preference pair creation using LLM-as-Judge

**Workflow**:
```python
# 1. Generate N candidate plans per scenario (N=3-5)
candidates = [model.generate(scenario) for _ in range(5)]

# 2. LLM Judge evaluates each with ACRUE assertions
scores = [llm_judge.evaluate(plan, assertions) for plan in candidates]

# 3. Select best and worst for preference pairs
best_plan = candidates[argmax(scores)]
worst_plan = candidates[argmin(scores)]

# 4. Validate quality gap is significant
if (max(scores) - min(scores)) >= 0.15:  # 15% threshold
    save_preference_pair(best_plan, worst_plan)
```

**Advantages of LLMCheckList Approach**:
- **Scalable**: Generate 1000s of preference pairs without human labeling
- **Consistent**: Same rubric applied to all evaluations
- **Explainable**: Each preference has specific assertion failures documented
- **Refinable**: Can adjust assertion weights based on what matters most

**Quality Control**:
- Human spot-check 10-20% of preference pairs
- Reject pairs where LLM Judge is uncertain (low confidence)
- Monitor for bias in assertion types (e.g., overweighting completeness)

### 4.3 Training Recipe

```python
# Phase 1: SFT (Weeks 1-2)
sft_config = {
    "base_model": "gpt-oss:120b",
    "training_data": "25_expert_plans_per_vertical",
    "epochs": 3,
    "learning_rate": 5e-5,
    "batch_size": 4,
    "validation_split": 0.2
}

# Phase 2: PFT - Direct Preference Optimization (Weeks 3-4)
pft_config = {
    "method": "DPO",  # Direct Preference Optimization
    "preference_pairs": "50_pairs_per_vertical",  # (better_plan, worse_plan)
    "beta": 0.1,  # DPO regularization strength
    "learning_rate": 1e-6,
    "epochs": 2
}

# Phase 3: RFT - Light RL for tool workflows (Weeks 5-6)
rft_config = {
    "base_model": "best_pft_model",  # Start from PFT checkpoint
    "reward_function": "procedural_correctness",  # Tool workflow accuracy only
    "method": "light_RL",  # Not full RLHF
    "focus": ["dependency_analysis", "timeline_validation", "stakeholder_mapping"],
    "training_iterations": 500  # Much lighter than classical RLHF
}

# Phase 4: Counterfactual Learning (Week 7)
counterfactual_config = {
    "base_model": "best_rft_model",
    "preference_pairs": "100_quality_comparison_scenarios",
    "contrastive_learning": True,
    "margin_loss": 0.3
}
```

### 4.3 Preventing Catastrophic Forgetting

Key mitigation strategies:

1. **Regular Validation on Horizontal Sets**
   - Test on all 31 meeting types after each training epoch
   - Monitor ACRUE scores for regression
   - Stop training if horizontal accuracy drops >5%

2. **Model Head Fine-Tuning** (if full fine-tuning causes forgetting)
   - Freeze transformer layers, only train final projection heads
   - Adds vertical-specific parameters without disrupting base model
   - Deploy as LoRA adapters for efficient serving

3. **Regularization Techniques**
   - Elastic Weight Consolidation (EWC) to preserve important weights
   - Knowledge Distillation from base model
   - Multi-task learning with horizontal + vertical objectives

---

## 5. Early Adopter Feedback Loop

### 5.1 Target User Groups

Following Researcher's S500 + MSIT approach:

#### External S500 Customers
- **Finance**: BlackRock, Goldman Sachs, JPMorgan (M&A, QBR expertise)
- **Technology**: Microsoft Azure customers (product launch, strategic planning)
- **Healthcare**: Eli Lilly, Johnson & Johnson (regulatory compliance, board meetings)
- **Consulting**: McKinsey, BCG, Deloitte (strategic offsite, transformation planning)

#### Internal Microsoft Teams
- **Finance Data & Experiences Group** (CFO org): QBR planning, financial reporting
- **IPG Patents Group** (CELA org): Patent filing workflows, regulatory planning
- **Azure Product Teams**: Major feature launch planning, go-to-market workback
- **GXP Squad Teams**: Mission planning, quarterly objectives

### 5.2 Feedback Collection Framework

**Structured Feedback Form**:
```json
{
  "scenario_id": "ma-integration-001",
  "reviewer": {
    "name": "Jane Smith",
    "role": "M&A Integration Director",
    "company": "Fortune 500 Finance",
    "experience_years": 15
  },
  "ratings": {
    "overall_quality": 4.5,
    "accuracy": 5.0,
    "completeness": 4.0,
    "relevance": 5.0,
    "usefulness": 4.0,
    "exceptional": 4.5,
    "presentation": 5.0
  },
  "qualitative_feedback": {
    "strengths": [
      "Excellent Day 1 readiness checklist",
      "Realistic timeline with proper dependency sequencing",
      "Clear workstream ownership and accountability"
    ],
    "weaknesses": [
      "Missing cultural integration tasks beyond Day 100",
      "Could add more detail on IT security cut-over risks",
      "Synergy targets not broken down by workstream"
    ],
    "suggested_improvements": [
      "Add quarterly culture integration checkpoints through Year 2",
      "Include backup plans for critical IT migrations",
      "Provide workstream-level synergy tracking dashboards"
    ]
  },
  "would_use_in_production": true,
  "improvement_vs_baseline": "+30% vs manual planning time"
}
```

### 5.3 Iteration Protocol

**4-Week Feedback Cycles**:

- **Week 1**: Deploy fine-tuned model to 5 early adopters (1 per vertical)
- **Week 2**: Collect structured feedback + usage analytics
- **Week 3**: Analyze feedback, update rubrics, retrain if needed
- **Week 4**: Deploy updated model, measure improvement delta

**Go/No-Go Criteria** (End of 12-Week Pilot):
- ✅ **GO**: ≥4.0/5.0 average rating, ≥15% improvement vs baseline, <5% horizontal regression
- ❌ **NO-GO**: <3.5/5.0 rating, <10% improvement, or >10% horizontal regression

---

## 6. Data Requirements & Costs

### 6.1 Expert Data Collection (Per Vertical)

Following Mercor's pricing model ($1,500 per prompt):

| Deliverable | Quantity | Cost per Unit | Total Cost |
|-------------|----------|---------------|------------|
| Complex meeting scenarios | 30 | $1,500 | $45,000 |
| Evidence documents (5 avg per scenario) | 150 | $100 | $15,000 |
| Detailed evaluation rubrics (30 criteria avg) | 30 | $500 | $15,000 |
| Golden output workback plans | 30 | $2,000 | $60,000 |
| **Total per vertical** | - | - | **$135,000** |

**4-Vertical Pilot Cost** (M&A, QBR, Product Launch, Board Prep):
- **Total**: $540,000 for 120 expert-validated scenarios
- **Alternative**: Leverage internal Microsoft experts (Finance org, IPG) for 50% cost savings

### 6.2 Fine-Tuning Compute Costs

Assuming Azure OpenAI or local fine-tuning costs:

| Phase | Compute Hours | Cost per Hour | Total Cost |
|-------|--------------|---------------|------------|
| SFT (3 epochs × 100 examples) | 20 | $10 | $200 |
| PFT/DPO (2 epochs × 50 preference pairs) | 25 | $12 | $300 |
| RFT (500 iterations, light RL) | 15 | $12 | $180 |
| Counterfactual Learning | 10 | $10 | $100 |
| **Total per vertical** | **70** | - | **$780** |

**4-Vertical Pilot**: $3,120 in compute costs (13% savings vs classical RLHF)

### 6.3 Total Pilot Budget

| Category | Cost |
|----------|------|
| Expert data collection (4 verticals) | $540,000 |
| Fine-tuning compute (4 verticals, PFT+RFT) | $3,120 |
| Evaluation infrastructure | $20,000 |
| Early adopter incentives | $10,000 |
| **Total 12-Week Pilot** | **$573,120** |

**Cost Reduction Strategies**:
1. Use internal Microsoft experts (IPG, Finance org) → Save $270,000
2. Start with 2 verticals (M&A + QBR) → Save $270,000
3. Leverage existing CXA templates → Save $60,000 (golden plans)

**Lean Pilot Option**: **$243,120** (2 verticals, internal experts, CXA templates)
- Expert data collection (2 verticals): $270,000 × 50% = $135,000
- Fine-tuning compute (2 verticals, PFT+RFT): $1,560
- Evaluation infrastructure: $20,000
- Early adopter incentives: $10,000
- **Note**: 13% compute savings vs classical RLHF ($1,800 → $1,560)

---

## 7. Key Risks & Mitigation

### 7.1 Data Quality Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| **Unrealistic scenarios** | Model learns incorrect patterns | Validate scenarios with 3+ domain experts before collection |
| **Incomplete rubrics** | Evaluation misses critical quality dimensions | Start with CXA templates, expand iteratively with expert review |
| **Overfitting to rubrics** | Model games metrics without real improvement | Qualitative review by users, measure production task completion |

### 7.2 Fine-Tuning Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| **Minimal model gain** | gpt-oss:120b already proficient, FT doesn't help | Baseline evaluation first, set minimum 15% improvement threshold |
| **Catastrophic forgetting** | Vertical optimization hurts horizontal performance | Regular validation on 31 meeting types, EWC regularization |
| **Overfitting to training set** | Doesn't generalize to new scenarios | Hold out 20% for validation, test on customer scenarios |

### 7.3 User Adoption Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| **Wrong early adopters** | Feedback doesn't reflect target users | Select users who validated task importance, commit to weekly check-ins |
| **Lukewarm feedback** | Improvements not valuable enough | Focus on high-pain scenarios (M&A, board prep), measure time savings |
| **Disengaged users** | Low-quality feedback, no iteration signal | Incentivize participation, provide usage analytics, iterate bi-weekly |

---

## 8. Success Metrics & KPIs

### 8.1 Technical Quality Metrics

| Metric | Baseline | Target | Measurement Method |
|--------|----------|--------|-------------------|
| **Vertical ACRUE Score** | 70-80% | ≥85% | Rubric-based automated evaluation |
| **Horizontal ACRUE Score** | 70-80% | ≥70% (no regression) | Original 31-type GUTT v4.0 eval |
| **Critical Failure Rate** | 10-15% | <5% | % scenarios with any critical rubric failure |
| **Task Completeness** | 75% | ≥90% | % plans with all required tasks for meeting type |
| **Timeline Accuracy** | 70% | ≥90% | % plans with realistic T-minus timelines |

### 8.2 User Experience Metrics

| Metric | Target | Measurement Method |
|--------|--------|-------------------|
| **Overall Satisfaction** | ≥4.0/5.0 | Post-usage survey (5-point Likert) |
| **Would Use in Production** | ≥70% | Binary question in feedback form |
| **Time Savings vs Manual** | ≥30% | Self-reported time comparison |
| **Adoption Rate** | ≥50% | % early adopters using regularly after 4 weeks |
| **Recommendation (NPS)** | ≥40 | Net Promoter Score calculation |

### 8.3 Business Impact Metrics

| Metric | Target | Measurement Method |
|--------|--------|-------------------|
| **Meeting Preparation Time** | -40% | Time tracking before/after |
| **Schedule Slip Reduction** | -25% | Track projects using WBP vs baseline |
| **Stakeholder Alignment** | +30% | Post-meeting surveys on clarity/agreement |
| **Decision Quality** | +20% | Retrospective assessment of outcomes |

---

## 9. Implementation Roadmap

### Phase 1: Foundation (Weeks 1-4)

**Goals**: Infrastructure setup, baseline evaluation, pilot scoping

- ✅ **Week 1**: Vertical selection scoring (complete 31 meeting types)
  * Score all meeting types on 4 criteria
  * Select top 4 verticals for pilot (M&A, QBR, Product Launch, Board Prep)
  * Secure budget approval ($243K-$574K range)

- ✅ **Week 2**: Baseline evaluation on existing data
  * Run gpt-oss:120b on CXA templates and 33 scenarios
  * Measure current ACRUE scores per meeting type
  * Identify gap areas (likely: completeness, exceptional quality, presentation)

- 🔄 **Week 3**: Expert data collection planning
  * Engage internal experts (Finance org, IPG Patents)
  * Define scenario templates and rubric structures
  * Set up data collection infrastructure

- ⏸️ **Week 4**: Early adopter recruitment
  * Identify 5-10 S500 customers + MSIT teams
  * Present pilot objectives and success criteria
  * Sign participation agreements

### Phase 2: Data Collection (Weeks 5-8)

**Goals**: Expert-curated datasets for 2-4 verticals

- **Week 5-6**: Scenario & document collection
  * Collect 30 scenarios per vertical (2-4 verticals = 60-120 total)
  * Gather 3-10 evidence documents per scenario
  * Validate scenario realism with 3+ domain experts

- **Week 7**: Rubric development
  * Create detailed rubrics (15-50 criteria per scenario)
  * Map to ACRUE categories + domain-specific criteria
  * Validate rubrics with early adopters

- **Week 8**: Golden output generation
  * Domain experts create ideal workback plans
  * Review for consistency and quality
  * Package in standardized JSON format

### Phase 3: Model Development (Weeks 9-12)

**Goals**: Fine-tuned models for priority verticals

- **Week 9-10**: Supervised Fine-Tuning (SFT) - Bootstrap with expert plans
  * Train on 25 expert plans per vertical
  * Validate on 5 holdout scenarios
  * Monitor horizontal set for regression

- **Week 11-12**: Preference Fine-Tuning (PFT/DPO) and light Reinforcement Fine-Tuning (RFT)
  * Create pairwise preference data (better vs worse plans)
  * Train DPO model (2 epochs on 50 preference pairs per vertical)
  * Apply light RFT for tool workflow correctness (500 iterations)
  * Evaluate improvement vs SFT baseline
  * Measure PFT impact on planning quality (decisiveness, clarity, actionability)
  * Validate RFT tool workflow accuracy (dependency analysis, timeline validation)

- **Week 12**: Counterfactual learning & validation
  * Generate negative examples with intentional errors
  * Train contrastive objective
  * Final evaluation on validation + horizontal sets

### Phase 4: Early Adopter Testing (Weeks 13-16)

**Goals**: Real-world validation, feedback collection, iteration

- **Week 13**: Deploy to 5 early adopters
  * 1 customer per vertical (M&A, QBR, Product Launch, Board Prep)
  * Provide training and support materials
  * Set up usage tracking and analytics

- **Week 14**: Collect structured feedback
  * Post-usage surveys with ratings + qualitative comments
  * In-depth interviews with power users
  * Analyze usage patterns and failure modes

- **Week 15**: Iterate based on feedback
  * Update rubrics to cover missed criteria
  * Retrain models with new edge cases
  * Deploy updated version (v2)

- **Week 16**: Final evaluation & go/no-go decision
  * Measure against success criteria (≥4.0 rating, ≥15% improvement)
  * Document lessons learned
  * Decide on scale-up vs pivot vs stop

### Phase 5: Scale (Weeks 17+)

**Goals**: Production deployment, additional verticals, continuous improvement

- **Weeks 17-20**: Production infrastructure
  * Deploy fine-tuned models to production Ollama servers
  * Implement A/B testing framework
  * Set up monitoring and alerting

- **Weeks 21-24**: Expand to additional verticals
  * Add 2-3 more meeting types (Strategic Offsite, Squad Mission, etc.)
  * Leverage learnings from Phase 1-4
  * Repeat data collection → training → validation cycle

- **Ongoing**: Continuous improvement loop
  * Monthly feedback collection from production users
  * Quarterly model retraining with new data
  * Annual vertical selection review and prioritization

---

## 10. Lessons from Researcher Team

### What We're Adopting

✅ **4-Criteria Vertical Selection Framework**
- Proven method for prioritizing high-value use cases
- Avoids "boil the ocean" approach
- Focuses resources on measurable business impact

✅ **Detailed Per-Scenario Rubrics**
- Moves beyond generic ACRUE to domain-specific quality
- Enables precise automated evaluation
- Provides clear training signal for fine-tuning

✅ **Modern SFT + PFT + RFT Approach**
- SFT bootstraps domain knowledge from expert examples
- PFT (DPO) optimizes planning quality via preference learning
- RFT ensures tool/workflow correctness with light RL
- Avoids classical RLHF issues (overly cautious, verbose outputs)

✅ **Early Adopter Validation Loop**
- Real users catch nuances automated evals miss
- Prevents overfitting to test sets
- Generates authentic user feedback for iteration

✅ **Holdout Validation Sets**
- 20% holdout prevents overfitting
- Horizontal set ensures no catastrophic forgetting
- Go/no-go criteria based on real metrics

### What We're Adapting

🔄 **Meeting-Type Verticals Instead of Role-Based**
- Researcher focuses on Finance/Legal personas
- We focus on meeting types (M&A, QBR, Product Launch)
- Maps better to our 31-type taxonomy and customer workflows

🔄 **User Profile Generator for Synthetic Data**
- Researcher uses real enterprise data + synthetic corpora
- We generate realistic stakeholder profiles (42 personas, 10 categories)
- Creates synthetic Microsoft 365 tenant with realistic communication trails

🔄 **GUTT v4.0 ACRUE as Foundation**
- Researcher builds ACRUE from scratch
- We already have validated ACRUE framework (70-80% baseline)
- Extend with domain-specific criteria rather than replace

🔄 **Ollama + gpt-oss:120b for Fine-Tuning**
- Researcher uses o3-DR (proprietary OpenAI model)
- We use open-source gpt-oss:120b on remote Ollama (192.168.2.204:11434)
- Maintains control over training infrastructure and costs

### What We're Learning From

⚠️ **Minimal Model Gain Risk**
- Researcher acknowledges o3-DR may already be proficient
- Mitigation: Baseline evaluation first, set high improvement bar (≥15%)
- Our advantage: gpt-oss:120b baseline is lower, more room for improvement

⚠️ **Pipeline Integration Throughput**
- Researcher struggled with backlog when Mercor delivered faster than training pipeline
- Mitigation: Build converters upfront, dry-run with sample data, measure iteration time
- Our plan: Start with 2 verticals (M&A, QBR), expand after validating throughput

⚠️ **Rubric Granularity Trade-off**
- Too generic → high scores even for mediocre output (LLM Asserts)
- Too specific → impossibly low scores, no training signal
- Sweet spot: 15-50 criteria per scenario, mix of binary + graded scoring

---

## 11. Open Questions & Next Steps

### Open Questions for Discussion

1. **Budget Allocation**: Lean pilot ($243K) vs full pilot ($574K)?
   * Lean: 2 verticals, internal experts, CXA templates
   * Full: 4 verticals, external Mercor-style vendor, custom golden plans

2. **Vertical Selection**: Start with which 2 verticals?
   * Option A: M&A + QBR (highest business impact)
   * Option B: M&A + Squad Mission (highest + Microsoft-specific)
   * Option C: QBR + Product Launch (highest data availability)

3. **Fine-Tuning Approach**: Modern SFT + PFT + RFT (recommended)
   * SFT: Bootstrap with expert knowledge (Weeks 1-2)
   * PFT (DPO): Learn planning preferences without RLHF instability (Weeks 3-4)
   * RFT: Light RL for tool workflow correctness only (Weeks 5-6)
   * Rationale: Avoids classical RLHF issues (overly cautious, verbose outputs)

4. **Early Adopter Mix**: Heavy S500 customers or heavy MSIT teams?
   * S500: More realistic, better product-market fit signal
   * MSIT: Easier access, faster feedback, lower risk

### Immediate Next Steps (This Week)

- [ ] Review proposal with team, align on approach
- [ ] Select 2 priority verticals for lean pilot
- [ ] Identify internal expert resources (Finance org, IPG)
- [ ] Baseline evaluation: run gpt-oss:120b on CXA templates
- [ ] Draft initial rubric templates for selected verticals
- [ ] Reach out to early adopter candidates (2-3 customers, 2-3 MSIT teams)

### 30-Day Milestones

- [ ] Complete vertical selection scoring (all 31 meeting types)
- [ ] Secure budget approval for lean pilot ($243K)
- [ ] Collect 10 scenarios for first vertical (M&A or QBR)
- [ ] Create detailed rubrics for 10 scenarios
- [ ] Generate 5 golden output plans with domain experts
- [ ] Run baseline evaluation + gap analysis
- [ ] Confirm 2 S500 + 2 MSIT early adopters

---

## 12. Conclusion

The Copilot Researcher Domain-Expertise Integration Pipeline provides a **proven, systematic framework** for enhancing AI systems with domain-specific knowledge. By adapting their methodology to Workback Planning, we can:

1. **Prioritize high-value verticals** using objective 4-criteria scoring (Complexity, Business Impact, Standardization, Data Availability)

2. **Collect expert-curated datasets** with realistic scenarios, evidence documents, detailed rubrics (15-50 criteria), and golden outputs

3. **Fine-tune systematically** using modern SFT + PFT + RFT approach, with pairwise preference learning and light RL for tool workflows

4. **Validate with real users** through structured early adopter feedback loops, preventing overfitting and ensuring production readiness

5. **Measure rigorously** against technical quality (ACRUE scores), user experience (satisfaction, adoption), and business impact (time savings, decision quality)

**Key Success Factors**:
- Start lean (2 verticals, $243K) and expand based on results
- Leverage internal Microsoft expertise (Finance, IPG) to reduce costs
- Build on existing GUTT v4.0 ACRUE foundation (70-80% baseline)
- Use our user profile generator to create realistic synthetic data
- Deploy on Ollama + gpt-oss:120b for infrastructure control

**Expected Outcomes** (12-Week Pilot):
- ✅ 15%+ improvement in vertical ACRUE scores (Accuracy, Completeness, Relevance, Usefulness, Exceptional: 70-80% → 85%+)
- ✅ <5% regression in horizontal scores (maintain 70-80%)
- ✅ 4.0+/5.0 user satisfaction rating
- ✅ 30%+ time savings vs manual workback planning
- ✅ Clear go/no-go decision for scale-up to 10+ verticals

By following the Researcher team's blueprint—adjusted for our meeting intelligence domain—we can systematically elevate Workback Planning from a general-purpose tool to a domain-expert system that S500 customers trust for their most critical strategic planning needs.

---

**Appendices** (To Be Developed):

- **Appendix A**: Detailed vertical selection scoring matrix (all 31 meeting types)
- **Appendix B**: Sample rubric templates for M&A, QBR, Product Launch, Board Prep
- **Appendix C**: Expert data collection playbook (scenarios, documents, golden plans)
- **Appendix D**: Fine-tuning technical specifications (SFT, PFT/DPO, RFT, counterfactual learning)
- **Appendix E**: Early adopter engagement guide (recruitment, training, feedback collection)
- **Appendix F**: Evaluation dashboard mockups (ACRUEP scores, user metrics, business impact)

---

**Document Status**: DRAFT for Team Review  
**Next Review**: November 18, 2025  
**Owner**: Chin-Yew Lin  
**Contributors**: TBD (Team Discussion)
