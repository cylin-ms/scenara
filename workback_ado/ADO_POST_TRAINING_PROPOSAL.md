# Azure DevOps as Training Data for Workback Planning Post-Training

**Author**: Chin-Yew Lin  
**Date**: November 11, 2025  
**Purpose**: Proposal to use Azure DevOps work items as gold-standard training data for workback planning

---

## Executive Summary

**Proposal**: Use Azure DevOps (ADO) work item data as the primary training data source for workback planning post-training, replacing synthetic scenarios and LLM-as-Judge evaluation.

**Why ADO Solves the Post-Training Challenge**:

| Challenge (from V2 Analysis) | How ADO Solves It |
|------------------------------|-------------------|
| **No ground truth** | ✅ Real execution outcomes (on-time, delayed, blocked) |
| **Circular reasoning** | ✅ No LLM-judging-LLM - outcomes from actual execution |
| **Synthetic data mismatch** | ✅ Real project contexts with actual constraints |
| **Proxy metrics ≠ effectiveness** | ✅ Direct outcome measurement (shipped vs delayed) |
| **Verification = Generation complexity** | ✅ Historical data provides verification through execution |

**Bottom Line**: ADO provides what Stratos-Exp lacks - **real-world validation through actual project execution**.

---

## Part 1: The Post-Training Data Problem (Recap)

### What We Need for Effective Post-Training

From the V2 analysis, effective post-training requires:

1. **Real contexts** - Not synthetic scenarios
2. **Expert knowledge** - Domain-specific patterns
3. **Outcome validation** - Did the plan actually work?
4. **Causal reasoning data** - What caused success/failure?

### What Stratos-Exp Provides (Insufficient)

❌ **Synthetic scenarios** - Made-up meeting contexts  
❌ **LLM-generated plans** - No execution validation  
❌ **LLM-as-Judge scores** - Circular reasoning  
❌ **No outcomes** - Can't learn what actually works  

### What ADO Provides (Ideal)

✅ **Real project contexts** - Actual work from real teams  
✅ **Executed plans** - Tasks that were actually completed  
✅ **Outcome labels** - Success, delayed, blocked, cancelled  
✅ **Causal data** - Dependencies, blockers, resolutions  

---

## Part 2: ADO Data Advantages

### Advantage 1: Real Execution Outcomes

**What ADO Tracks**:
```json
{
  "work_item_id": 12345,
  "title": "Implement OAuth authentication",
  "state": "Closed",
  
  "planned": {
    "estimate_hours": 13,
    "target_date": "2025-09-15"
  },
  
  "actual": {
    "completed_hours": 18,
    "closed_date": "2025-09-18"
  },
  
  "outcome_label": {
    "effort_outcome": "over_budget_38%",
    "schedule_outcome": "3_days_late",
    "overall": "completed_with_delays"
  },
  
  "blockers": [
    {
      "date": "2025-09-10",
      "reason": "Waiting for OAuth credentials from InfoSec",
      "duration_days": 2
    }
  ]
}
```

**Training Signal**: Model learns that OAuth tasks often have credential provisioning delays (add 2-day buffer).

### Advantage 2: Explicit Dependency Chains

**ADO Work Item Links**:
- `System.LinkTypes.Dependency-Forward` - Predecessor relationship
- `System.LinkTypes.Dependency-Reverse` - Successor relationship
- `System.LinkTypes.Hierarchy-Forward` - Parent/child

**Example**:
```
Epic: Q1 Mobile App Launch
├── Feature: User Authentication
│   ├── Task: Design login UI [Completed: 5 days]
│   ├── Task: Implement auth API [Completed: 8 days, 3 days late]
│   │   └── BLOCKER: OAuth credentials (2 days)
│   └── Task: Integrate frontend [DEPENDS ON: auth API]
│       └── Completed: 3 days (started after API done)
```

**Training Signal**: Model learns correct dependency ordering and realistic task durations.

### Advantage 3: Complexity Stratification

**Automatic Q2/Q1 Classification**:

```python
def classify_ado_complexity(work_item):
    """Map ADO work item to Q2 (Low) or Q1 (High) complexity"""
    
    score = 0
    
    # Story points: 1-3=Low, 5-8=Medium, 13+=High
    if work_item.story_points >= 13:
        score += 3
    elif work_item.story_points >= 8:
        score += 2
    
    # Team count: 1=Low, 2-3=Medium, 4+=High
    score += min(len(work_item.teams) - 1, 3)
    
    # Dependencies: <5=Low, 5-15=Medium, >15=High
    links = len(work_item.predecessor_links)
    if links >= 15:
        score += 3
    elif links >= 5:
        score += 1
    
    # Duration: 1-2 sprints=Low, 3-4=Medium, 5+=High
    if work_item.sprint_count >= 4:
        score += 3
    elif work_item.sprint_count >= 2:
        score += 1
    
    # Classify
    if score <= 3:
        return "Q2_Low_Complexity"
    elif score <= 6:
        return "Q3_Medium"
    else:
        return "Q1_High_Complexity"
```

**Benefit**: Start training with Q2 work items (single team, clear dependencies, 1-2 sprints).

### Advantage 4: Value Assessment

**ADO Value Signals**:

```python
def assess_ado_value(work_item):
    """Determine High/Medium/Low value"""
    
    value_score = 0
    
    # Priority: P0/P1 = critical
    if work_item.priority in ["P0", "1"]:
        value_score += 3
    elif work_item.priority in ["P1", "2"]:
        value_score += 2
    
    # Business value field (if set)
    if work_item.business_value >= 50:
        value_score += 2
    
    # Customer commitment tags
    if any(tag in work_item.tags for tag in 
           ["customer-committed", "roadmap", "OKR"]):
        value_score += 2
    
    # Hard deadline
    if work_item.target_date and work_item.external_commitment:
        value_score += 2
    
    return "High" if value_score >= 6 else \
           "Medium" if value_score >= 3 else "Low"
```

**Benefit**: Focus training on high-value projects (customer commitments, hard deadlines).

### Advantage 5: Rich Context

**What ADO Captures** (beyond basic fields):

- **Descriptions**: Natural language context of what needs to be done
- **Acceptance Criteria**: Definition of done
- **Discussions**: Team conversations about blockers, decisions
- **History**: All state changes with timestamps
- **Attachments**: Design docs, specs, diagrams
- **Related Work**: Context from linked items

**Training Value**: Model learns not just structure, but domain patterns (e.g., "OAuth tasks need credentials", "UI design needs user testing").

---

## Part 3: Training Data Synthesis from ADO

### Step 1: Extract Completed Projects

**Target Projects**:
- Completed in last 6-12 months (recent patterns)
- 50+ work items with dependencies
- >80% have estimates and actuals logged
- Clear outcome (shipped, delayed, or cancelled)

**Example Extraction**:
```python
# WIQL Query for completed projects
query = """
SELECT [System.Id], [System.Title], [System.State],
       [System.WorkItemType], [Microsoft.VSTS.Scheduling.StoryPoints],
       [Microsoft.VSTS.Scheduling.OriginalEstimate],
       [Microsoft.VSTS.Scheduling.CompletedWork],
       [System.CreatedDate], [Microsoft.VSTS.Common.ClosedDate]
FROM WorkItems
WHERE [System.TeamProject] = 'YourProject'
  AND [System.State] = 'Closed'
  AND [System.WorkItemType] IN ('Epic', 'Feature', 'User Story', 'Task')
  AND [Microsoft.VSTS.Common.ClosedDate] >= '2025-01-01'
  AND [Microsoft.VSTS.Scheduling.CompletedWork] IS NOT NULL
ORDER BY [System.Id]
"""
```

### Step 2: Build Training Examples

**Training Example Structure**:

```json
{
  "training_id": "ado_12345",
  "source": "azure_devops",
  
  "context": {
    "goal": "Q1 Mobile App Launch",
    "description": "Launch mobile app with user auth and profile features",
    "deadline": "2025-03-31",
    "priority": "P0",
    "business_value": 100,
    "teams": ["iOS Team", "Backend Team", "Design Team"],
    "stakeholders": ["alice@example.com", "bob@example.com"]
  },
  
  "plan": {
    "tasks": [
      {
        "id": "task_1",
        "title": "Design login UI",
        "estimated_hours": 40,
        "actual_hours": 40,
        "assigned_to": "design_team",
        "dependencies": [],
        "outcome": "completed_on_time"
      },
      {
        "id": "task_2",
        "title": "Implement OAuth API",
        "estimated_hours": 80,
        "actual_hours": 120,
        "assigned_to": "backend_team",
        "dependencies": [],
        "outcome": "completed_late",
        "blockers": [
          {
            "reason": "Waiting for OAuth credentials",
            "duration_days": 2
          }
        ]
      },
      {
        "id": "task_3",
        "title": "Integrate frontend with API",
        "estimated_hours": 60,
        "actual_hours": 65,
        "assigned_to": "ios_team",
        "dependencies": ["task_2"],
        "outcome": "completed_on_time"
      }
    ]
  },
  
  "outcome": {
    "overall": "completed_with_delays",
    "shipped_date": "2025-04-05",
    "delay_days": 5,
    "effort_variance": 1.15,
    "success_metrics": {
      "goal_achieved": true,
      "timeline_met": false,
      "budget_met": false
    }
  },
  
  "lessons_learned": {
    "what_went_wrong": [
      "OAuth credentials took 2 extra days to provision",
      "Backend complexity underestimated by 50%"
    ],
    "what_to_improve": [
      "Request OAuth credentials in advance (Day -5)",
      "Add 40% buffer for auth-related backend tasks",
      "Ensure frontend team has parallel work during API development"
    ]
  },
  
  "metadata": {
    "complexity": "Q2_Low",
    "value": "High",
    "work_item_count": 15,
    "team_count": 3,
    "duration_weeks": 9
  }
}
```

### Step 3: Expert Correction

**Challenge**: ADO shows what happened, not necessarily what SHOULD have happened.

**Solution**: Expert PM reviews and creates "ideal plan"

```json
{
  "training_id": "ado_12345",
  
  "plans": {
    "actual_ado": {
      "tasks": [...],  // What actually happened (from ADO)
      "outcome": "completed_with_delays"
    },
    
    "expert_corrected": {
      "tasks": [
        {
          "id": "task_0",
          "title": "Request OAuth credentials from InfoSec",
          "estimated_hours": 2,
          "start_day": -5,  // 5 days BEFORE project kickoff
          "dependencies": [],
          "note": "Should have been done in advance"
        },
        {
          "id": "task_1",
          "title": "Design login UI",
          "estimated_hours": 40,
          "dependencies": [],
          "parallelizable": true
        },
        {
          "id": "task_2",
          "title": "Implement OAuth API",
          "estimated_hours": 120,  // Expert corrects estimate to realistic 120
          "dependencies": ["task_0"],  // Now depends on credentials
          "note": "Auth tasks typically need 1.5x estimate"
        },
        {
          "id": "task_3",
          "title": "Integrate frontend with API",
          "estimated_hours": 60,
          "dependencies": ["task_2"]
        }
      ],
      "estimated_outcome": "completed_on_time"
    }
  },
  
  "expert_feedback": {
    "key_improvements": [
      "Added upfront task for credential provisioning",
      "Increased OAuth estimate from 80 to 120 hours (1.5x factor)",
      "Made dependencies explicit (API depends on credentials)"
    ],
    "general_lessons": [
      "Always include infrastructure/setup tasks as Day 0 items",
      "Auth/security tasks need 1.5x buffer due to typical blockers",
      "Identify critical path early (API was bottleneck)"
    ]
  }
}
```

**Training Approach**: Train model to generate "expert_corrected" plans, not "actual_ado" plans.

---

## Part 4: Complexity-Value Prioritization (Q2 First)

### Phase 1 Pilot: 50 Q2 Work Items

**Selection Criteria**:
- **Complexity**: Q2 (Low) - Single team, <5 dependencies, 1-2 sprints
- **Value**: High - Customer committed, P0/P1 priority
- **Outcome**: Mix of successes and failures (learn from both)
- **Data Quality**: >90% completeness (estimates, actuals, links)

**Example Q2 Work Items**:
```python
q2_candidates = [
    {
        "id": 12340,
        "title": "Add password reset feature",
        "story_points": 5,
        "teams": 1,
        "dependencies": 2,
        "sprints": 1,
        "priority": "P1",
        "outcome": "completed_on_time",
        "complexity": "Q2_Low",
        "value": "High"
    },
    {
        "id": 12450,
        "title": "Implement email notifications",
        "story_points": 8,
        "teams": 1,
        "dependencies": 3,
        "sprints": 2,
        "priority": "P0",
        "outcome": "completed_late_2days",
        "complexity": "Q2_Low",
        "value": "High"
    }
    # ... 48 more Q2 examples
]
```

**Why Start with Q2**:
- ✅ Easier for experts to review (10-15 min each vs 30+ min for Q1)
- ✅ Model can learn successfully (within LLM capability)
- ✅ Quick validation cycles (weeks not months)
- ✅ Build user trust with early wins

### Phase 2 Scale: 200-500 Mixed

**Complexity Mix**:
- 60% Q2 (Low complexity, high value)
- 20% Q3 (Low complexity, medium value)
- 15% Q1 (High complexity, high value)
- 5% Edge cases

**Rationale**: Master Q2 first, then graduate to Q1.

---

## Part 5: Training Strategies

### Strategy 1: Supervised Learning (Expert Plans)

**Objective**: Generate plans like expert-corrected versions

```python
# Training setup
Input: Project context (from ADO description + metadata)
Target: Expert-corrected plan
Loss: Cross-entropy

# Example
train_example = {
    "input": {
        "goal": "Add OAuth authentication",
        "deadline": "4 weeks",
        "teams": ["backend"],
        "complexity": "medium"
    },
    "target": expert_corrected_plan,  # With upfront credential task
    "weight": 1.0
}
```

**Expected Result**: Model learns to include upfront tasks (credentials, approvals).

### Strategy 2: Preference Learning (Actual vs Optimal)

**Objective**: Learn that expert plans are better than actual plans with issues

```python
# DPO (Direct Preference Optimization)
Input: Project context
Plan A: Actual plan (had delays) - WORSE
Plan B: Expert-corrected plan (would be on-time) - BETTER
Label: B > A

# Training signal: Prefer plans that include buffers and upfront tasks
```

**Expected Result**: Model learns to prefer better planning patterns.

### Strategy 3: Outcome Prediction

**Objective**: Predict if plan will succeed before execution

```python
# Classification task
Input: Project context + Proposed plan
Target: Outcome label (success / partial_success / delayed / failed)
Loss: Cross-entropy

# Use case: "This plan likely to be delayed because no buffer for OAuth"
```

**Expected Result**: Model learns risk assessment capabilities.

### Strategy 4: Effort Estimation

**Objective**: Predict realistic effort from historical data

```python
# Regression task
Input: Task description + Context
Target: Actual hours (from completed_work field)
Loss: MAE or MSE

# Example: "OAuth implementation" → Model predicts 120 hours (not 80)
```

**Expected Result**: Model learns realistic estimation patterns.

### Strategy 5: Critical Path Identification

**Objective**: Identify tasks likely to cause delays

```python
# Binary classification per task
Input: Dependency graph + Task estimates
Target: Which tasks caused delays (from ADO history)
Loss: Binary cross-entropy

# Use case: Model flags OAuth task as "high risk - likely blocker"
```

**Expected Result**: Model learns to identify risky dependencies.

---

## Part 6: Integration with Scenara Ecosystem

### Combined Data Sources

**Power of Integration**:

```json
{
  "training_example": {
    "ado_context": {
      "work_item_id": 12345,
      "project": "Q1 Mobile Launch",
      "stakeholders": ["alice@example.com", "bob@example.com"]
    },
    
    "scenara_context": {
      "meeting": {
        "subject": "Q1 Mobile App Planning",
        "date": "2025-01-15",
        "attendees": ["alice@example.com", "bob@example.com", "carol@example.com"]
      },
      "collaborators": {
        "alice@example.com": {
          "role": "Product Manager",
          "interaction_frequency": "high"
        },
        "bob@example.com": {
          "role": "Engineering Lead",
          "interaction_frequency": "medium"
        }
      }
    },
    
    "plan": {...},
    "outcome": {...}
  }
}
```

**Benefit**: Richer context = better plans

### Execution Feedback Loop

**Workflow**:
```
Week 1: Meeting → Scenara generates plan
Week 1: User approves → Scenara creates ADO work items via API
Week 2-8: Team executes in ADO
Week 9: Scenara extracts outcomes from ADO
Week 10: Expert reviews discrepancies
Week 11: Add to training data
Week 12: Retrain model
```

**Continuous Improvement**: Model gets better as it learns from real executions.

---

## Part 7: Competitive Advantage

### What Competitors Can't Do

**General LLMs (GPT-4, Claude, Gemini)**:
- ❌ No access to enterprise ADO data
- ❌ Trained only on internet text (blog posts about project management)
- ❌ No real execution outcomes
- ❌ Can't learn organization-specific patterns

**PM Tools (Monday, Asana, Jira)**:
- ⚠️ Have execution data but weak AI
- ⚠️ Don't integrate with meeting intelligence
- ⚠️ Generic recommendations

**Scenara with ADO**:
- ✅ Real execution data + outcomes
- ✅ Meeting context + calendar + org data
- ✅ Organization-specific learning
- ✅ Continuous feedback loop

### Defensible Moat

**Data Moat**: 
- Proprietary training data from customer ADO instances
- General LLMs can't access this data
- 12-18 month lead time for competitors

**Network Effects**:
- More customers → More training data → Better models → More customers

**Switching Costs**:
- After model learns customer's patterns, hard to switch to generic AI

**Market Positioning**:
> "Scenara learns from YOUR actual project outcomes. Unlike generic AI trained on internet text, we improve continuously by learning what actually works in YOUR organization."

---

## Part 8: Implementation Roadmap

### Month 1: Pilot (50 Q2 Examples)

**Week 1: Setup**
- [ ] Setup ADO API access (PAT token)
- [ ] Identify 2-3 completed projects
- [ ] Validate data quality

**Week 2: Extract**
- [ ] Extract 50 Q2 work items
- [ ] Build dependency graphs
- [ ] Generate outcome labels

**Week 3-4: Expert Review**
- [ ] Send to PM experts for correction
- [ ] Collect expert-corrected plans
- [ ] Document lessons learned

**Deliverable**: 50 (context, expert_plan, outcome) training examples

**Cost**: $2,500-5,000 (expert time)

### Month 2-3: Scale (200-500 Examples)

**Week 5-6: Expand Extraction**
- [ ] Extract from 5-10 additional projects
- [ ] Mix: 60% Q2, 20% Q3, 15% Q1, 5% edge cases
- [ ] Quality validation

**Week 7-10: Expert Review**
- [ ] All Q1 items (high complexity) - 100% review
- [ ] 50% of Q2 items - spot check
- [ ] 30% of Q3 items - sample

**Week 11-12: Training Data Prep**
- [ ] Format for model training
- [ ] Train/validation/test splits
- [ ] Augment with Scenara meeting context

**Deliverable**: 200-500 training examples

**Cost**: $10,000-25,000

### Month 4-6: Model Training & Validation

**Week 13-16: First Training Iteration**
- [ ] Fine-tune on ADO data
- [ ] Validate on held-out test set
- [ ] Compare vs Stratos-Exp baseline

**Week 17-20: Integration**
- [ ] End-to-end testing: Meeting → Plan → ADO items
- [ ] API integration validation
- [ ] User acceptance testing

**Week 21-24: Production Rollout**
- [ ] Deploy to pilot users
- [ ] Monitor metrics
- [ ] Setup continuous learning pipeline

**Deliverable**: Production-ready model

---

## Part 9: Success Metrics

### Short-term (3 months)

**Plan Quality**:
- **Target**: 65% of plans rated "would use as-is" or "minor edits"
- **Baseline**: Stratos-Exp ~40%
- **Improvement**: +25 percentage points

**Estimate Accuracy**:
- **Target**: Within 30% of actuals for 70% of tasks
- **Baseline**: ±50% error
- **Improvement**: -20 percentage points

**Dependency Identification**:
- **Target**: 75% of critical dependencies identified
- **Baseline**: ~50%
- **Improvement**: +25 percentage points

### Medium-term (6 months)

**Execution Alignment**:
- **Target**: 60% of generated plans lead to on-time execution
- **Measure**: Plans created in ADO → Track outcomes

**Learning Velocity**:
- **Target**: 5% improvement per month as data grows
- **Measure**: Validation accuracy over time

**User Satisfaction**:
- **Target**: 4.0/5.0 average rating
- **Measure**: User ratings after plan generation

### Long-term (12 months)

**Business Impact**:
- **Target**: 20% reduction in project delays
- **Compare**: Teams with Scenara vs without

**Adoption**:
- **Target**: 70% of generated plans executed (not discarded)
- **Measure**: ADO creation rate

---

## Part 10: Risk Mitigation

### Risk 1: Data Privacy

**Concern**: Customer ADO data is sensitive

**Mitigation**:
- On-premise deployment option
- Federated learning (aggregate without raw data)
- Data anonymization (remove PII)
- Customer control over data sharing

### Risk 2: Data Quality Varies

**Concern**: Not all ADO instances have clean data

**Mitigation**:
- Quality scoring (only use >80% complete)
- Minimum bar for training data
- Expert curation for critical examples

### Risk 3: Patterns Don't Generalize

**Concern**: Company A's data doesn't help Company B

**Mitigation**:
- Base model (multi-org)
- Fine-tuning (company-specific)
- 80% shared knowledge, 20% custom

---

## Conclusion

**The Case for ADO**:

Azure DevOps provides the **gold standard training data** that Stratos-Exp lacks:
1. ✅ **Real execution outcomes** (not synthetic scenarios)
2. ✅ **Validated dependencies** (not LLM-generated guesses)
3. ✅ **Complexity stratification** (automatic Q2/Q1 classification)
4. ✅ **Continuous learning** (feedback loop from execution)
5. ✅ **Defensible moat** (proprietary enterprise data)

**Strategic Recommendation**:

**Start Now**: Pilot with 50 Q2 work items from completed projects  
**Scale Smart**: 60% Q2, 20% Q3, 15% Q1, 5% edge cases  
**Build Moat**: Create defensible advantage through proprietary training data  

**Expected ROI**:
- Development: ~$50,000 (3 months)
- Customer value: $100K-$1M per customer per year (20% delay reduction)
- Competitive lead: 12-18 months

This is the **right strategic move** for Scenara workback planning.

---

**Author**: Chin-Yew Lin  
**Date**: November 11, 2025  
**Next Action**: Approve pilot, select 2-3 target ADO projects
