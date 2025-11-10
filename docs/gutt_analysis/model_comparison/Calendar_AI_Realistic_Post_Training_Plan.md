# Calendar.AI Realistic Post-Training Plan

**Document Version**: 1.0  
**Date**: November 10, 2025  
**Author**: Chin-Yew Lin  
**Purpose**: Ground-truth implementation roadmap for post-training based on actual capability discovery

---

## Executive Summary

**Key Reality Check**: The 25 canonical tasks in our V2.0 framework are **conceptual capabilities** - they represent WHAT the system needs to do, not WHAT currently exists. Before executing any post-training plan, we must **discover ground truth**:

1. ✅ **What We Have**: Working implementations (APIs, tools, models)
2. ❓ **What We Don't Have**: Conceptual tasks requiring development
3. 🎯 **Implementation Gap**: Delta between framework requirements and reality

**Strategic Approach**: **Discover → Implement → Train** (not just Train)

---

## 1. The Reality: Conceptual vs Implemented

### 1.1 What We Know (Validated)

✅ **25 Canonical Tasks Framework V2.0**:
- Human-validated task decompositions for 9 hero prompts
- 91.98% F1 score on conceptual task identification
- Execution composition templates (reasoning traces)
- 9 concrete example flows

✅ **Evaluation Infrastructure**:
- GPT-5 integration for task decomposition
- 3-trial stability testing methodology
- Human evaluation workflows
- Gold standard reference documentation (2,900 lines)

### 1.2 What We DON'T Know (Critical Gap)

❓ **Actual Implementation Status**:
- Which canonical tasks have working implementations?
- Which tasks are just API calls vs requiring ML models?
- Which tasks need net-new development?
- What existing code/tools can be reused?

**Example Uncertainty**:
```
CAN-01 (Calendar Events Retrieval):
  - Likely EXISTS: Direct Microsoft Graph API call
  - Implementation: GET /me/calendar/events
  - Status: UNKNOWN - need to verify in codebase

CAN-03 (Meeting Importance Assessment):
  - Likely MISSING: Requires ML model + organizational data
  - Dependencies: User preferences, historical patterns, org hierarchy
  - Status: UNKNOWN - conceptual capability, not simple API

CAN-25 (Event Annotation/Flagging):
  - Likely PARTIAL: Can add flags to events, but conditional logic TBD
  - Implementation: Calendar API supports categories, but rule engine needed
  - Status: UNKNOWN - conceptual framework validated, implementation unclear
```

---

## 2. Phase 0: Ground Truth Discovery (MUST DO FIRST)

**Mission**: Audit existing codebase to map conceptual tasks → actual implementations

### 2.1 Capability Discovery Audit

**Step 1: Scan Existing Codebase**

```bash
# Search for calendar API usage
grep -r "calendar" --include="*.py" .

# Search for Microsoft Graph API calls
grep -r "graph" --include="*.py" .

# Search for LLM integrations
grep -r "llm\|gpt\|claude\|ollama" --include="*.py" .

# Find all tools
ls -la tools/*.py

# Check for classification/ML models
find . -name "*classification*" -o -name "*model*" -o -name "*ml*"
```

**Step 2: Create Implementation Matrix**

| Task ID | Conceptual Capability | Implementation Status | Evidence | Gap |
|---------|----------------------|----------------------|----------|-----|
| CAN-01 | Calendar Events Retrieval | ✅ / ⚠️ / ❌ | File: `xyz.py`, Line X | None / Partial / Complete |
| CAN-02 | Meeting Type Classification | ✅ / ⚠️ / ❌ | Model: `meeting_classifier.py` | ... |
| CAN-03 | Importance Assessment | ✅ / ⚠️ / ❌ | ? | ... |
| ... | ... | ... | ... | ... |

**Status Legend**:
- ✅ **Fully Implemented**: Working code, tested, ready to use
- ⚠️ **Partially Implemented**: Exists but incomplete/untested/needs work
- ❌ **Not Implemented**: Conceptual only, requires net-new development

**Step 3: Document Each Implementation**

For each task, capture:
```python
{
  "task_id": "CAN-01",
  "name": "Calendar Events Retrieval",
  "status": "fully_implemented",  # or "partial" or "not_implemented"
  "implementation": {
    "file": "tools/calendar_api.py",
    "function": "get_calendar_events()",
    "lines": "45-120",
    "dependencies": ["msal", "microsoft.graph"],
    "tested": true,
    "production_ready": true
  },
  "gap_analysis": {
    "missing_features": [],
    "technical_debt": "None",
    "effort_to_complete": "0 days"
  },
  "api_mappings": {
    "microsoft_graph": "GET /me/calendar/events",
    "parameters": ["startDateTime", "endDateTime", "filter"]
  }
}
```

### 2.2 Tools to Build for Discovery

**Tool 1: `audit_canonical_task_implementations.py`**

```python
"""
Audit existing codebase to discover which canonical tasks are implemented.

Usage:
    python tools/audit_canonical_task_implementations.py \
        --framework docs/gutt_analysis/CANONICAL_TASKS_REFERENCE_V2.md \
        --output implementation_audit.json
        
Output:
    - Implementation status for all 25 tasks
    - Gap analysis (what's missing)
    - Dependency tree (what needs to be built first)
    - Effort estimates (days of development)
"""

def audit_task_implementation(task_id, task_spec):
    """
    Search codebase for evidence of implementation.
    """
    evidence = {
        "code_files": search_code_references(task_spec.keywords),
        "api_calls": find_api_calls(task_spec.api_mappings),
        "ml_models": find_model_files(task_spec.name),
        "test_coverage": find_tests(task_id)
    }
    
    status = classify_implementation_status(evidence)
    
    return {
        "task_id": task_id,
        "status": status,  # "full" / "partial" / "none"
        "evidence": evidence,
        "confidence": calculate_confidence(evidence)
    }
```

**Tool 2: `generate_implementation_roadmap.py`**

```python
"""
Generate prioritized implementation roadmap based on:
1. Task frequency (from gold standard)
2. Implementation status (from audit)
3. Dependencies (parent-child relationships)

Output: Phased implementation plan with effort estimates
"""

def generate_roadmap(audit_results, gold_standard):
    """
    Create phased implementation plan.
    """
    # Phase 1: High-frequency + fully implemented (quick wins)
    # Phase 2: High-frequency + partial implementation (complete)
    # Phase 3: High-frequency + not implemented (build)
    # Phase 4: Low-frequency tasks (defer or simplify)
    
    return prioritized_phases
```

---

## 3. Realistic Post-Training Roadmap

### Phase 0: Discovery (Week 1-2) 🔍 **START HERE**

**Objective**: Know the ground truth before making plans

**Actions**:
1. **Audit Codebase**:
   - [ ] Run `audit_canonical_task_implementations.py`
   - [ ] Create implementation matrix (25 tasks × status)
   - [ ] Document evidence for each task (files, functions, APIs)
   - [ ] Estimate implementation effort for gaps

2. **Categorize Tasks**:
   ```
   Category A (Ready): Fully implemented, tested
   Category B (Near-Ready): Partial implementation, needs completion
   Category C (Build Required): Conceptual only, requires development
   Category D (Defer): Low-frequency, can simplify or skip
   ```

3. **Dependency Analysis**:
   - [ ] Map parent-child relationships (e.g., CAN-07 enables CAN-13)
   - [ ] Identify critical path (what must be built first)
   - [ ] Find reusable components (shared code across tasks)

4. **Output Deliverables**:
   - `implementation_audit.json` - Complete status for 25 tasks
   - `implementation_gaps_report.md` - What's missing and why
   - `phased_implementation_roadmap.md` - Build order with effort estimates

**Success Criteria**: 
- 100% of 25 tasks categorized (A/B/C/D)
- Implementation gaps quantified (days of effort)
- Realistic roadmap with dependencies

---

### Phase 1: Implement High-Priority Gaps (Week 3-6)

**Objective**: Build missing capabilities for high-frequency tasks

**Pre-requisite**: Phase 0 complete, gaps identified

**Decision Tree**:
```
For each high-frequency task (>50% usage):
  IF Status = "Full" → SKIP (already done)
  ELSE IF Status = "Partial" → COMPLETE (finish implementation)
  ELSE IF Status = "None" → BUILD (net-new development)
```

**Example Scenarios**:

**Scenario 1: CAN-01 Fully Implemented**
```
Task: Calendar Events Retrieval (100% frequency)
Status: ✅ Fully Implemented
Evidence: tools/calendar_api.py, Line 45-120
Action: SKIP - Already production-ready
Outcome: Use existing implementation in training data
```

**Scenario 2: CAN-03 Partially Implemented**
```
Task: Meeting Importance Assessment (56% frequency)
Status: ⚠️ Partial - Has basic scoring, missing ML model
Evidence: tools/importance_scorer.py, Line 80-150
Gap: No ML model, uses heuristics only
Action: COMPLETE
  1. Collect training data (historical accept/decline decisions)
  2. Train importance classifier
  3. Integrate model into existing scorer
Effort: 5 days
Outcome: Production-ready importance assessment
```

**Scenario 3: CAN-25 Not Implemented**
```
Task: Event Annotation/Flagging (11% frequency)
Status: ❌ Not Implemented - Conceptual only
Evidence: Calendar API supports categories, but no rule engine
Gap: Need conditional logic engine + Calendar API integration
Action: BUILD
  1. Design rule engine (IF condition THEN flag)
  2. Implement Calendar API category/flag updates
  3. Test with Organizer-2 scenario
Effort: 8 days
Outcome: NEW capability for conditional event marking
```

**Priority Order** (Based on Frequency × Gap):
1. CAN-01 (100% freq, Status ?) → Verify/Use
2. CAN-04 (100% freq, Status ?) → Verify/Complete
3. CAN-07 (78% freq, Status ?) → Critical parent task
4. CAN-05 (67% freq, Status ?) → Often missed, critical dependency
5. CAN-03 (56% freq, Status ?) → ML model likely needed
6. CAN-02 (56% freq, Status ?) → Classification model likely exists
7. ... (continue based on actual audit results)

**Milestone**: All high-frequency tasks (>50%) fully implemented

---

### Phase 2: Generate Training Data (Week 7-8)

**Objective**: Create synthetic scenarios ONLY for implemented capabilities

**Pre-requisite**: Phase 1 complete, capabilities working

**Reality-Based Approach**:

```python
# Only generate training data for IMPLEMENTED tasks
implemented_tasks = [
    task for task in canonical_tasks_25 
    if task.implementation_status in ["full", "partial_complete"]
]

# Filter hero prompts to only use implemented capabilities
trainable_prompts = [
    prompt for prompt in hero_prompts_9
    if all(task in implemented_tasks for task in prompt.required_tasks)
]

# Generate synthetic data
synthetic_scenarios = generate_variations(
    templates=trainable_prompts,
    multiplier=10,  # 10x expansion
    validate=True   # Test each scenario with actual implementations
)
```

**Example**:
```
IF CAN-01, CAN-04, CAN-07, CAN-02, CAN-03, CAN-11, CAN-13 all implemented:
  THEN generate 10 variations of Organizer-1
  AND validate each scenario runs end-to-end
ELSE:
  SKIP Organizer-1 until dependencies built
```

**Quality Gate**: Every synthetic scenario must **execute successfully** with actual implementations (not just conceptually valid)

---

### Phase 3: Fine-Tune on Validated Data (Week 9-10)

**Objective**: Train model on REAL execution traces, not conceptual ones

**Training Data Format**:
```json
{
  "scenario_id": "synth_organizer_1_001",
  "prompt": "Keep my Calendar up to date...",
  "expected_tasks": ["CAN-04", "CAN-01", "CAN-07", ...],
  "actual_execution": {
    "can_01_api_call": "GET /me/calendar/events",
    "can_01_response": {...},
    "can_07_extraction": {...},
    "success": true
  },
  "validation": {
    "end_to_end_success": true,
    "f1_score": 0.95,
    "execution_time_ms": 1250
  }
}
```

**Key Difference**: Training data includes **actual API responses** and **execution traces**, not just conceptual task lists.

---

### Phase 4: Iterative Expansion (Week 11+)

**Objective**: Continuously expand as new capabilities are implemented

**Feedback Loop**:
```
1. Discover new capability implemented (e.g., CAN-25 now done)
2. Update implementation_audit.json
3. Generate training data for new capability
4. Fine-tune model with expanded data
5. Validate improvement on test set
6. Deploy to production
7. Repeat
```

---

## 4. Critical Differences from Original Plan

### Original Plan (Overly Optimistic)
```
✅ Step 1-3 Complete → Just generate 100+ scenarios → Fine-tune
```

### Realistic Plan (Grounded in Reality)
```
❓ Audit codebase first → Build missing capabilities → 
Generate ONLY for implemented tasks → Validate execution → Fine-tune
```

### Key Changes

| Aspect | Original Assumption | Reality Check |
|--------|-------------------|---------------|
| **Task Status** | Assumed all 25 tasks ready | ❓ Unknown - need audit |
| **Training Data** | Conceptual scenarios (task lists) | ✅ Execution traces (actual runs) |
| **Validation** | F1 score on task identification | ✅ End-to-end execution success |
| **Timeline** | 2-4 weeks | 10-12 weeks (includes build time) |
| **Deliverable** | 100+ scenarios for fine-tuning | Phased: Audit → Build → Train |

---

## 5. Immediate Action Items (This Week)

### Priority 1: Build Discovery Tool ⚡

**Task**: Create `tools/audit_canonical_task_implementations.py`

**Features**:
- Parse CANONICAL_TASKS_REFERENCE_V2.md for 25 task specs
- Search codebase for implementation evidence
- Classify status: Full / Partial / None
- Generate implementation_audit.json
- Produce gaps report with effort estimates

**Deliverable**: Know ground truth by end of week

### Priority 2: Manual Spot Check (Parallel)

While tool runs, manually verify 5 critical tasks:

1. **CAN-01 (Calendar Retrieval)**: 
   - [ ] Search for `calendar` + `events` in codebase
   - [ ] Find Microsoft Graph API usage
   - [ ] Test: Can we retrieve events right now?

2. **CAN-04 (NLU)**:
   - [ ] Search for LLM integrations (GPT, Claude, Ollama)
   - [ ] Find prompt engineering code
   - [ ] Test: Can we parse user intents right now?

3. **CAN-03 (Importance Assessment)**:
   - [ ] Search for `importance` + `priority` + `scoring`
   - [ ] Look for ML models or heuristic rules
   - [ ] Test: Can we score meetings right now?

4. **CAN-07 (Metadata Extraction)**:
   - [ ] Search for parsing/extraction logic
   - [ ] Find attendee/subject/time parsing
   - [ ] Test: Can we extract metadata right now?

5. **CAN-13 (RSVP Update)**:
   - [ ] Search for calendar write operations
   - [ ] Find accept/decline/tentative logic
   - [ ] Test: Can we update RSVPs right now?

**Decision Point**: 
- IF 4-5 tasks implemented → Phase 1 fast (complete gaps)
- IF 2-3 tasks implemented → Phase 1 moderate (build missing)
- IF 0-1 tasks implemented → Reassess scope (MVP first)

### Priority 3: Document Findings

Create: `CAPABILITY_DISCOVERY_FINDINGS.md`

```markdown
# Capability Discovery Findings

## Summary
- Fully Implemented: X / 25 tasks
- Partially Implemented: Y / 25 tasks
- Not Implemented: Z / 25 tasks

## High-Priority Gaps (Frequency >50%)
1. CAN-XX: Status, Gap, Effort
2. CAN-YY: Status, Gap, Effort

## Quick Wins (Partial → Full)
1. ...

## Build Required (None → Full)
1. ...

## Recommended Roadmap
Phase 1: Complete X quick wins (2 weeks)
Phase 2: Build Y high-priority gaps (4 weeks)
Phase 3: Generate training data (2 weeks)
Phase 4: Fine-tune (2 weeks)
```

---

## 6. Success Metrics (Reality-Based)

### Phase 0 Success
- ✅ 100% of 25 tasks categorized (Full/Partial/None)
- ✅ Implementation gaps quantified (effort in days)
- ✅ Realistic roadmap with dependencies

### Phase 1 Success
- ✅ All high-frequency tasks (>50%) fully implemented
- ✅ End-to-end execution tests passing
- ✅ APIs/models deployed and accessible

### Phase 2 Success
- ✅ X synthetic scenarios generated (X = # of trainable prompts × 10)
- ✅ 100% scenarios execute successfully (not just conceptually valid)
- ✅ Execution traces captured (API calls, responses, timings)

### Phase 3 Success
- ✅ Model fine-tuned on real execution data
- ✅ Performance improvement vs baseline (F1 score, execution success rate)
- ✅ Production deployment ready

---

## 7. Risk Mitigation

### Risk 1: Most Tasks Not Implemented
**Probability**: Medium-High  
**Impact**: High (delays entire roadmap)  
**Mitigation**: 
- Start with MVP subset (5-7 most critical tasks)
- Focus on Category A (calendar API operations) first
- Defer Category C (ML models) to Phase 2

### Risk 2: Partial Implementations Unusable
**Probability**: Medium  
**Impact**: Medium (rework needed)  
**Mitigation**:
- Run actual execution tests during audit
- Don't assume "partial" = "usable"
- Budget time for refactoring/fixing

### Risk 3: Dependency Blocks
**Probability**: High  
**Impact**: Medium (reorder roadmap)  
**Mitigation**:
- Map dependencies early (Phase 0)
- Identify critical path
- Build parent tasks before children

### Risk 4: Conceptual Tasks Can't Be Implemented
**Probability**: Low-Medium  
**Impact**: High (framework needs revision)  
**Mitigation**:
- Some tasks may need to be split or combined
- Framework is validated conceptually, but implementation may differ
- Be flexible - adjust framework based on technical reality

---

## 8. Conclusion

**Key Insight**: We cannot execute a post-training plan without knowing what capabilities actually exist. The 25 canonical tasks are **validated requirements**, but implementation status is **unknown**.

**Strategic Approach**:
1. **Discover First**: Audit codebase, know ground truth
2. **Build Gaps**: Implement missing high-priority capabilities
3. **Train on Reality**: Generate data from ACTUAL executions, not concepts
4. **Iterate**: Expand as new capabilities come online

**Timeline Reality**:
- **Original Plan**: 2-4 weeks (generate scenarios → train)
- **Realistic Plan**: 10-12 weeks (audit → build → generate → train)

**Next Step**: Build `tools/audit_canonical_task_implementations.py` this week to discover ground truth.

---

## Related Documents

- [Calendar_AI_Post_Training_Readiness.md](Calendar_AI_Post_Training_Readiness.md) - Strategic assessment (conceptual)
- [CANONICAL_TASKS_REFERENCE_V2.md](../CANONICAL_TASKS_REFERENCE_V2.md) - 25 task specifications
- [CANONICAL_TASKS_CAPABILITY_INVENTORY_V2.md](../CANONICAL_TASKS_CAPABILITY_INVENTORY_V2.md) - Infrastructure requirements
- [V2_GOLD_STANDARD_REPORT.md](../V2_GOLD_STANDARD_REPORT.md) - Conceptual task decompositions
- [Outlook_Data_Loop_and_Post_Training_Loop.md](Outlook_Data_Loop_and_Post_Training_Loop.md) - Industry reference

---

**Document Status**: ✅ Realistic plan acknowledging implementation unknowns - Discovery phase required

**Version History**:
- v1.0 (2025-11-10): Initial realistic plan grounded in implementation discovery
