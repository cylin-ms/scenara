# GPT-5 Execution Composition Evaluation Report

**Date**: November 7, 2025  
**Framework Version**: 2.0 (24 Canonical Unit Tasks)  
**Model**: GPT-5 (via SilverFlow API)  
**Evaluation Type**: Execution Composition (SELECT from 24 tasks)  
**Test Set**: 9 Hero Prompts (3 Organizer, 3 Schedule, 3 Collaborate)

---

## Executive Summary

GPT-5 achieved an **F1 score of 79.74%** when composing execution plans from the 24 canonical unit tasks. The model demonstrated strong understanding of universal tasks (CAN-01, CAN-04) but showed inconsistent recognition of the CAN-07 parent task and struggled with specialized tasks (CAN-18, CAN-20, CAN-23).

### Key Findings

- ✅ **Perfect Universal Task Coverage**: CAN-01 (Retrieval) and CAN-04 (NLU) appeared in all 9 prompts
- ⚠️ **CAN-07 Confusion**: Missed in 2 prompts where needed, unnecessarily added in 3 prompts
- ❌ **Specialized Task Gaps**: Never selected CAN-18 (Objection/Risk), CAN-20 (Visualization), CAN-23 (Conflict Resolution)
- ✅ **New Task Integration**: Successfully used CAN-21 (Duration) and CAN-22 (Work Attribution)
- 📊 **Overall Coverage**: 21/24 tasks used (87.5%), 3 Tier 3 tasks unused

---

## Performance Metrics

### Aggregate Scores

| Metric | Score | Interpretation |
|--------|-------|----------------|
| **Precision** | 81.18% | GPT-5 rarely adds unnecessary tasks |
| **Recall** | 79.85% | Misses ~20% of gold standard tasks |
| **F1 Score** | 79.74% | **FAIR** overall performance |
| **Success Rate** | 9/9 (100%) | All prompts processed without errors |

### Performance Distribution

| Grade | F1 Range | Count | Prompts |
|-------|----------|-------|---------|
| **Excellent** | ≥ 90% | 0 | - |
| **Good** | 80-89% | 7 | organizer-1, organizer-2, schedule-1, schedule-2, schedule-3, collaborate-1, collaborate-2 |
| **Fair** | 60-79% | 1 | organizer-3 |
| **Poor** | < 60% | 1 | collaborate-3 |

---

## Per-Prompt Analysis

### 🏆 Best Performance: schedule-1 (F1: 88.89%)

**Prompt**: "Schedule a weekly 1:1 with my manager, auto-reschedule if conflicts arise"

**GPT-5**: `CAN-01, CAN-03, CAN-04, CAN-05, CAN-06, CAN-15, CAN-16, CAN-17` (8 tasks)  
**Gold**: `CAN-01, CAN-03, CAN-04, CAN-05, CAN-06, CAN-12, CAN-15, CAN-16, CAN-17, CAN-23` (10 tasks)

**Analysis**:
- ✅ Perfect precision (100%) - no unnecessary tasks
- ⚠️ Missed CAN-12 (Constraint Satisfaction) and CAN-23 (Conflict Resolution)
- ✅ Correctly identified CAN-17 (Automated Rescheduling) - key differentiator
- Strong understanding of scheduling automation workflow

---

### ⚠️ Fair Performance: organizer-3 (F1: 71.43%)

**Prompt**: "Show me my meeting patterns and reclaim time from low-value meetings"

**GPT-5**: `CAN-01, CAN-02A, CAN-02B, CAN-04, CAN-07, CAN-10, CAN-14` (7 tasks)  
**Gold**: `CAN-01, CAN-02A, CAN-04, CAN-10, CAN-11, CAN-14, CAN-20` (7 tasks)

**Analysis**:
- ❌ Missed CAN-20 (Visualization/Dashboards) - critical for "show me patterns"
- ❌ Missed CAN-11 (Priority/Ranking) - needed for "low-value" assessment
- ➕ Added CAN-07 (Metadata Extraction) unnecessarily - already covered by CAN-01
- ➕ Added CAN-02B (Importance) unnecessarily - CAN-02A sufficient
- Struggled with analytical/reporting requirements

---

### ❌ Worst Performance: collaborate-3 (F1: 54.55%)

**Prompt**: "Generate a team quarterly work summary from meetings"

**GPT-5**: `CAN-01, CAN-04, CAN-07, CAN-09, CAN-22` (5 tasks)  
**Gold**: `CAN-01, CAN-02A, CAN-04, CAN-05, CAN-08, CAN-09` (6 tasks)

**Analysis**:
- ❌ Missed CAN-02A (Meeting Type) - needed to filter relevant meetings
- ❌ Missed CAN-05 (Attendee Extraction) - needed for team composition
- ❌ Missed CAN-08 (Document Analysis) - critical for "work summary"
- ➕ Added CAN-07 (Metadata) unnecessarily - already covered
- ✅ Correctly identified CAN-22 (Work Attribution) - new task, well understood
- Confused content extraction (CAN-08) with generation (CAN-09)

---

## Systematic Patterns

### ⚠️ CAN-07 Confusion (Most Critical Issue)

**CAN-07**: Meeting Metadata Extraction (Parent Task)

**Problem**: GPT-5 shows inconsistent understanding of CAN-07's role:

| Scenario | GPT-5 Behavior | Correct Behavior |
|----------|----------------|------------------|
| **Missed** (2 times) | schedule-2, schedule-3 | Should include when RSVP/logistics needed |
| **Correctly Included** (4 times) | organizer-2, collaborate-1, collaborate-2, collaborate-3 | ✅ Appropriate |
| **Unnecessarily Added** (3 times) | organizer-1, organizer-3, collaborate-3 | CAN-01 (Retrieval) already covers basic metadata |

**Root Cause**: Model doesn't distinguish when **basic metadata** (via CAN-01) suffices vs. when **deep metadata extraction** (CAN-07) is needed for child tasks like CAN-13 (RSVP), CAN-19 (Resource Booking).

**Recommendation**: Improve system prompt to clarify:
- CAN-01 retrieves meeting objects
- CAN-07 extracts structured metadata **when enabling child tasks**

---

### ❌ Specialized Task Avoidance

**Never Selected**:
- **CAN-18** (Objection/Risk Detection) - Missed in collaborate-1
- **CAN-20** (Visualization/Dashboards) - Missed in organizer-3
- **CAN-23** (Conflict Resolution) - Missed in schedule-1

**Hypothesis**: GPT-5 treats these as "optional enhancements" rather than core requirements.

**Evidence**:
- collaborate-1 prompt: "Prep agenda for 1:1" → Should anticipate objections (CAN-18)
- organizer-3 prompt: "Show me patterns" → Requires visualization (CAN-20)
- schedule-1 prompt: "Auto-reschedule if conflicts" → Needs resolution strategy (CAN-23)

**Recommendation**: Add explicit prompt keywords triggering specialized tasks:
- "anticipate", "risks" → CAN-18
- "show", "visualize", "dashboard" → CAN-20
- "resolve conflicts", "prioritize" → CAN-23

---

### ✅ Strong Foundational Understanding

**Universal Tasks (100% Coverage)**:
- **CAN-01** (Calendar Data Retrieval): All 9 prompts ✅
- **CAN-04** (Natural Language Understanding): All 9 prompts ✅

**Tier 1 Tasks (High Accuracy)**:
- **CAN-03** (Meeting Creation): 5/5 prompts requiring scheduling ✅
- **CAN-02A/B** (Type/Importance): Good separation, minor confusion
- **CAN-05** (Attendee Extraction): 5/6 prompts requiring people data ✅
- **CAN-06** (Time/Duration Parsing): Consistent usage ✅

**New Tasks (Successfully Integrated)**:
- **CAN-21** (Duration Estimation): organizer-2 ✅
- **CAN-22** (Work Attribution): collaborate-3 ✅

---

## Task-Specific Insights

### CAN-02A vs CAN-02B Confusion

**Expected**: CAN-02A (Type) and CAN-02B (Importance) are independent
**Observed**: GPT-5 sometimes treats them as mutually exclusive

| Prompt | GPT-5 Selection | Correct? |
|--------|-----------------|----------|
| organizer-1 | Both CAN-02A + CAN-02B | ❌ Unnecessary (only type needed) |
| organizer-2 | Only CAN-02B | ✅ Correct (prioritization focus) |
| organizer-3 | Both CAN-02A + CAN-02B | ⚠️ CAN-02B unnecessary |

**Recommendation**: Clarify that:
- CAN-02A = **What** type of meeting (1:1, team, customer)
- CAN-02B = **How** important (strategic, urgent, reschedulable)
- Both can be needed, but CAN-02A more common

---

### CAN-12 (Constraint Satisfaction) Under-Selection

**Frequency**: Used in 2/9 prompts (schedule-2, schedule-3)  
**Expected**: Should appear in all scheduling prompts (5/9)

**Missed Opportunities**:
- schedule-1: "auto-reschedule if conflicts" → CAN-12 needed to find valid slots
- organizer-2: "schedule prep time before meetings" → CAN-12 needed to satisfy constraints

**Current System Prompt**:
> "CAN-12: Advanced scheduling algorithms (CSP/optimization)"

**Improved Wording**:
> "CAN-12: Constraint Satisfaction - finding valid time slots while respecting constraints (availability, preferences, conflicts)"

---

## Comparison to Gold Standard

### Task Coverage Comparison

| Category | Gold Standard | GPT-5 | Gap |
|----------|---------------|-------|-----|
| **Total Unique Tasks** | 24/24 (100%) | 21/24 (87.5%) | -3 tasks |
| **Tier 1 (Universal)** | 6/6 (100%) | 6/6 (100%) | ✅ Perfect |
| **Tier 2 (Common)** | 11/11 (100%) | 10/11 (91%) | -CAN-18 |
| **Tier 3 (Specialized)** | 7/7 (100%) | 5/7 (71%) | -CAN-20, -CAN-23 |

### Task Usage Frequency

| Task | Gold | GPT-5 | Delta | Notes |
|------|------|-------|-------|-------|
| CAN-01 | 9/9 | 9/9 | ✅ | Universal retrieval |
| CAN-04 | 9/9 | 9/9 | ✅ | Universal NLU |
| CAN-07 | 5/9 | 6/9 | ⚠️ +1 | Over-included |
| CAN-18 | 1/9 | 0/9 | ❌ -1 | Never selected |
| CAN-20 | 1/9 | 0/9 | ❌ -1 | Never selected |
| CAN-23 | 1/9 | 0/9 | ❌ -1 | Never selected |

---

## Strengths

1. ✅ **Perfect Universal Task Recognition**: CAN-01 and CAN-04 in all prompts
2. ✅ **High Precision**: 81.18% - rarely adds unnecessary tasks
3. ✅ **Robust API Reliability**: 9/9 prompts processed successfully
4. ✅ **Quick Response Time**: 8-10 seconds per prompt
5. ✅ **New Task Integration**: CAN-21 and CAN-22 correctly used on first attempt
6. ✅ **Strong Scheduling Logic**: CAN-15, CAN-16, CAN-17 correctly identified in automation contexts
7. ✅ **Good Tier 1 Coverage**: All 6 universal tasks used appropriately

---

## Weaknesses

1. ❌ **CAN-07 Role Confusion**: Unclear when metadata extraction is foundational vs. optional
2. ❌ **Specialized Task Avoidance**: Never selected CAN-18, CAN-20, CAN-23
3. ❌ **CAN-12 Under-Selection**: Missed constraint satisfaction in 3 scheduling prompts
4. ⚠️ **CAN-02A/B Separation**: Occasional confusion between type and importance
5. ⚠️ **Document Analysis Gap**: Missed CAN-08 in collaborate-3 (work summary)
6. ⚠️ **Tier 3 Bias**: Treats specialized tasks as optional enhancements

---

## Recommendations

### 1. Improve CAN-07 Guidance (Critical)

**Current System Prompt**:
```
CAN-07: Meeting Metadata Extraction
  Description: Extract structured metadata from meeting invitations
  Parent Task For: CAN-13 (RSVP), CAN-05 (Attendees), CAN-08 (Documents)...
```

**Recommended System Prompt**:
```
CAN-07: Meeting Metadata Extraction (PARENT TASK)
  When to Use:
    ✅ YES: When child tasks require detailed metadata (RSVP status, attachments, logistics)
    ✅ YES: Prompts mentioning "attendees", "attachments", "RSVP", "resources"
    ❌ NO: Basic meeting retrieval (CAN-01 sufficient)
  
  Child Tasks Enabled: CAN-13, CAN-05, CAN-08, CAN-09, CAN-19, CAN-21
  Dependencies: Requires CAN-01 first
```

### 2. Add Keyword Triggers for Specialized Tasks

**CAN-18 (Objection/Risk Detection)**:
- Keywords: "anticipate", "risks", "objections", "concerns", "blockers"
- Example: collaborate-1 "prep agenda" → should trigger CAN-18

**CAN-20 (Visualization/Dashboards)**:
- Keywords: "show", "visualize", "dashboard", "patterns", "trends", "summary view"
- Example: organizer-3 "show patterns" → should trigger CAN-20

**CAN-23 (Conflict Resolution)**:
- Keywords: "resolve conflicts", "prioritize", "auto-reschedule", "conflict strategy"
- Example: schedule-1 "auto-reschedule if conflicts" → should trigger CAN-23

### 3. Clarify CAN-12 (Constraint Satisfaction)

**Current**: Perceived as "advanced" optimization  
**Recommended**: Position as standard scheduling requirement

**Updated Description**:
```
CAN-12: Constraint Satisfaction
  Required For: Finding valid meeting times while respecting:
    - Attendee availability
    - User preferences (time of day, buffer time)
    - Existing calendar conflicts
    - Room/resource availability
  
  Use When: Any scheduling task (not just optimization)
```

### 4. Improve CAN-02A/B Differentiation

**Add Examples**:
```
CAN-02A (Meeting Type): "What kind of meeting?"
  Examples: 1:1, team sync, customer call, standup, retrospective

CAN-02B (Meeting Importance): "How important is this meeting?"
  Examples: strategic, urgent, routine, reschedulable, optional
  
Independent Attributes: A meeting can be "team sync" (CAN-02A) AND "urgent" (CAN-02B)
```

### 5. Provide Execution Pattern Examples

**Add to system prompt**:
```
Common Execution Patterns:
1. Simple Scheduling: CAN-04 → CAN-01 → CAN-06 → CAN-12 → CAN-03
2. Smart Organizer: CAN-04 → CAN-01 → CAN-02B → CAN-07 → CAN-14
3. Collaboration Prep: CAN-04 → CAN-01 → CAN-07 → CAN-08 → CAN-09
4. Pattern Analysis: CAN-04 → CAN-01 → CAN-10 → CAN-20

Parent-Child Dependencies:
- CAN-01 enables: CAN-07
- CAN-07 enables: CAN-13, CAN-05, CAN-08, CAN-19, CAN-21
```

---

## Next Steps

### Immediate Actions

1. ✅ **GPT-5 Evaluation Complete**: 79.74% F1 score documented
2. 🔄 **Run Claude Sonnet 4.5 Analysis**: Use backend AI reasoning per .cursorrules
3. 📊 **Compare Models**: Identify which model better handles specialized tasks
4. 📝 **Update Framework**: Based on systematic gaps identified

### Framework Improvements

1. **CAN-07 Clarification**: Add "when to use" guidance and parent task examples
2. **Specialized Task Triggers**: Document keyword patterns for CAN-18, CAN-20, CAN-23
3. **CAN-12 Repositioning**: From "advanced" to "standard scheduling"
4. **Execution Patterns**: Add common task sequences to reference doc

### Model Fine-Tuning Opportunities

1. **Training Data**: Create 50+ examples with correct CAN-07 usage
2. **Specialized Task Examples**: Generate prompts requiring CAN-18, CAN-20, CAN-23
3. **Constraint Satisfaction Examples**: Scheduling scenarios requiring CAN-12
4. **Few-Shot Learning**: Add 3-5 example compositions to system prompt

---

## Conclusion

GPT-5 demonstrates **strong foundational understanding** (81% precision, 100% universal task coverage) but struggles with **parent task dependencies** (CAN-07 confusion) and **specialized task recognition** (CAN-18, CAN-20, CAN-23 avoidance). The 79.74% F1 score is **FAIR** and indicates the model is production-ready for Tier 1-2 tasks but requires prompt engineering improvements for comprehensive coverage.

**Grade: B-** (FAIR)  
**Readiness**: Production-ready with limitations  
**Primary Blocker**: CAN-07 parent task confusion  
**Quick Win**: Add keyword triggers for specialized tasks

---

**Report Generated**: November 7, 2025  
**Evaluation Script**: `tools/compare_gpt5_to_gold.py`  
**Data Files**:
- GPT-5 Compositions: `docs/gutt_analysis/model_comparison/gpt5_compositions_20251107_014703.json`
- Gold Standard: `docs/gutt_analysis/gold_standard_analysis.json`
