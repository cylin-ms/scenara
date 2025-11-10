# Canonical Tasks Gap Analysis: V1 vs V2

**Author**: Chin-Yew Lin  
**Date**: November 7, 2025  
**Analysis Source**: Evaluation Results from evaluation_results_20251107_005227.json

## Executive Summary

**Critical Finding**: 4 out of 20 canonical tasks (20%) were **never used** in any of the 9 execution composition plans, despite being identified as necessary in the V1 task identification analysis.

**Paradox**: Both V1 (Task Identification) and V2 (Execution Composition) analyzed the **same 9 hero prompts** using GPT-5. Yet V1 identified these tasks as necessary, while V2 did not include them in any execution plan.

## The Missing Tasks

| Task ID | Task Name | Tier | V1 Usage | V2 Usage | Gap |
|---------|-----------|------|----------|----------|-----|
| CAN-07 | Meeting Metadata Extraction | 2 | 3 prompts | 0 prompts | **-3** |
| CAN-17 | Automatic Rescheduling | 3 | 2 prompts | 0 prompts | **-2** |
| CAN-18 | Objection/Risk Anticipation | 3 | 2 prompts | 0 prompts | **-2** |
| CAN-20 | Data Visualization/Reporting | 3 | 1 prompt | 0 prompts | **-1** |

**Total Gap**: 8 task instances lost between V1 and V2

## V1 Analysis: Where Were These Tasks Identified?

### CAN-07: Meeting Metadata Extraction (Tier 2)
**V1 identified in 3 prompts:**

1. **schedule-1**: "Land a weekly 30min 1:1 with Sarah for me..."
   - **Why needed**: "To send meeting invitation to Sarah"
   - **How used**: "Create and send calendar invitation with meeting details"
   - **Execution sequence**: "Step 7: Send meeting invitation to Sarah (CAN-07)"

2. **schedule-2**: "Bump all my meetings that can move to later in the week..."
   - **Why needed**: "To send notifications or updated invitations to attendees"
   - **How used**: "Notify attendees of rescheduled meetings"
   - **Execution sequence**: "Step 6: Use CAN-07 to send notifications or updated invitations"

3. **schedule-3**: "I have a weekly team-sync on Tuesdays at 2pm..."
   - **Why needed**: "To send meeting invitations and updates to attendees"
   - **How used**: "Create invitation, notify attendees of changes"
   - **Execution sequence**: "Step 7: Send meeting invitations using CAN-07"

**V2 Analysis**: Did NOT include CAN-07 in any execution plan

**Why the gap?**
- V2 may have considered sending invitations as **implicit** in CAN-03 (Calendar Event Creation/Update)
- CAN-07 definition focuses on *extracting* metadata, not *sending* invitations
- Possible mismatch between task name and V1's usage

### CAN-17: Automatic Rescheduling (Tier 3)
**V1 identified in 2 prompts:**

1. **schedule-1**: "If her schedule changes, automatically find a new time"
   - **Why needed**: "To automatically reschedule the 1:1 when Sarah's availability changes"
   - **How used**: "Monitor Sarah's calendar, detect conflicts, find alternative times"
   - **Execution sequence**: "Step 9: Implement automatic rescheduling workflow if conflicts arise (CAN-17)"

2. **schedule-3**: "I have a weekly team-sync on Tuesdays at 2pm. My 1:1s with my manager take priority..."
   - **Why needed**: "To automatically reschedule team meeting when it conflicts with manager 1:1s"
   - **How used**: "Detect conflicts, apply priority rules, reschedule automatically"
   - **Execution sequence**: "Step 8: If conflicts arise with 1:1s, apply automatic rescheduling using CAN-17"

**V2 Analysis**: Did NOT include CAN-17 in any execution plan

**Why the gap?**
- V1 interpreted "automatically find a new time" as needing CAN-17
- V2 may have treated this as a **manual workflow** using CAN-16 (Event Monitoring) + CAN-03 (Event Update)
- **V2 schedule-1 included CAN-16** (Event Monitoring/Change Detection) - possibly as a substitute
- Automatic rescheduling is **complex**: requires monitoring, conflict detection, rule application, and rescheduling - may be beyond single task scope

### CAN-18: Objection/Risk Anticipation (Tier 3)
**V1 identified in 2 prompts:**

1. **collaborate-1**: "Prep an agenda for my next meeting with the Project Alpha team..."
   - **Why needed**: "To identify potential risks or objections from team members"
   - **How used**: "Analyze collaboration patterns, flag potential blockers or concerns"
   - **Execution sequence**: "Step 5: Optionally use CAN-18 to identify potential risks or objections"
   - **Note**: Marked as "Optional"

2. **collaborate-2**: "Before my 1:1 with Jordan, pull together a briefing..."
   - **Why needed**: "To anticipate objections or challenges in Jordan's projects"
   - **How used**: "Identify risks, blockers, or concerns to address proactively"
   - **Execution sequence**: "Step 7: (Optional) Implement CAN-18 to include risk anticipation insights"
   - **Note**: Marked as "Optional" and "enhancement for higher-value executive briefings"

**V2 Analysis**: Did NOT include CAN-18 in any execution plan

**Why the gap?**
- V1 **marked both instances as "Optional"** - not core requirements
- CAN-18 is **advanced AI capability** (risk prediction, objection forecasting)
- V2 likely focused on **core executable tasks** and excluded speculative/optional features
- This may be a **future enhancement** rather than MVP requirement

### CAN-20: Data Visualization/Reporting (Tier 3)
**V1 identified in 1 prompt:**

1. **organizer-3**: "Show me patterns in the kinds of meetings that fill up my week..."
   - **Why needed**: "To present patterns and insights in an easily understandable visual format"
   - **How used**: "Create charts or summaries showing time distribution across meeting types and trends over time"
   - **Execution sequence**: "Step 6: Visualize patterns and insights (CAN-20)"
   - **Implementation status**: "needs_implementation"

**V2 Analysis**: Did NOT include CAN-20 in execution plan for organizer-3

**Why the gap?**
- V1 marked as "needs_implementation" (Tier 3, not currently available)
- V2 organizer-3 execution plan **stops at Step 5** (Recommendation Engine)
- **Visualization is output format**, not computational step
- V2 may have assumed visualization happens in **UI layer**, not in execution logic
- The prompt says "Show me patterns" - could be interpreted as text output vs. visual charts

## Root Cause Analysis

### Hypothesis 1: Different Analysis Focus
- **V1 Prompt**: "What canonical tasks are needed?" → Identified all possibly relevant tasks
- **V2 Prompt**: "How do tasks compose into computational workflow?" → Only included executable steps
- **Result**: V2 excluded non-executable tasks (optional, UI-layer, future enhancements)

### Hypothesis 2: Task Definition Ambiguity
- **CAN-07**: Name says "Metadata *Extraction*" but V1 used it for "Invitation *Sending*"
- **CAN-17**: "Automatic Rescheduling" is complex workflow, not single atomic task
- **CAN-18**: "Risk Anticipation" is speculative AI capability, not deterministic computation
- **CAN-20**: "Visualization" is presentation layer, not business logic

### Hypothesis 3: GPT-5 Interpretation Variance
- **V1**: GPT-5 was generous in identifying "needed" tasks, including optional and future capabilities
- **V2**: GPT-5 was conservative in building execution plans, focusing on core MVP functionality
- **Result**: Natural variance in AI interpretation between two different prompts

## Evaluation Findings vs V1/V2 Gap

### What the Evaluator (Chin-Yew Lin) Found:

1. **CAN-02 Conflation** (Mentioned 4 times)
   - "Meeting Classification lumps two types: meeting type and meeting priority"
   - **Implication**: Need to split CAN-02 into CAN-02A (Type) and CAN-02B (Importance)

2. **CAN-11 vs CAN-02 Overlap**
   - "If CAN-02 identifies important vs. unimportant, why do we need CAN-11?"
   - **Implication**: Redundancy between classification and preference matching

3. **Missing CAN-04 in organizer-3**
   - "Isn't NLP CAN-04 needed for all prompts?"
   - **Implication**: CAN-04 should be universal, not selectively applied

4. **CAN-06 depends on CAN-01**
   - "Does CAN-06 (Availability Checking) depend on CAN-01 (Calendar Retrieval)?"
   - **Implication**: Need explicit dependency documentation

5. **Missing Capabilities**
   - **Task Duration Estimation** (organizer-2): "Capability to estimate prep time"
   - **Who Works On What** (collaborate-1): "Discover who works on what"
   - **Conflict Resolution** (schedule-1): "Do we have conflict resolution module?"

6. **Document Generation Scope** (collaborate-1)
   - "Does CAN-09 include all document types: PPT, spreadsheet, code, etc.?"
   - **Implication**: May need specialized sub-tasks

## Comparison: V1 vs V2 Task Coverage

| Tier | Total Tasks | V1 Used | V2 Used | Gap |
|------|-------------|---------|---------|-----|
| 1 (Universal) | 5 | 5 (100%) | 5 (100%) | 0 |
| 2 (Common) | 9 | 9 (100%) | 8 (89%) | -1 (CAN-07) |
| 3 (Specialized) | 6 | 6 (100%) | 3 (50%) | -3 (CAN-17, CAN-18, CAN-20) |
| **Total** | **20** | **20 (100%)** | **16 (80%)** | **-4** |

**Key Insight**: The gap is primarily in **Tier 3 (Specialized)** tasks, which are:
- More advanced capabilities
- Often marked "needs_implementation"
- May be optional/future enhancements
- Less clearly defined as atomic computational steps

## Recommendations

### 1. Reconcile CAN-07 (Meeting Metadata Extraction)
**Issue**: Name suggests extraction, but V1 used it for sending invitations

**Options**:
- **A**: Rename to "Meeting Invitation Management" (broader scope)
- **B**: Keep as "Metadata Extraction" and remove sending functionality
- **C**: Merge sending functionality into CAN-03 (Calendar Event Creation/Update)

**Recommendation**: **Option C** - Sending invitations is part of creating/updating events. CAN-07 should focus on extracting metadata from existing meetings (attendees, topics, decisions, action items).

### 2. Clarify CAN-17 (Automatic Rescheduling)
**Issue**: Is this a single task or a complex workflow?

**Analysis**:
- Requires: CAN-16 (monitoring) + CAN-06 (availability) + CAN-12 (constraints) + CAN-03 (update)
- **CAN-17 is a composite capability**, not atomic task

**Recommendation**: 
- Keep CAN-17 as **Tier 3 orchestrated capability** (not atomic task)
- Document dependencies: CAN-16 → CAN-06 → CAN-12 → CAN-03
- Mark as "requires orchestration across multiple tasks"

### 3. Clarify CAN-18 (Objection/Risk Anticipation)
**Issue**: Advanced AI capability, marked optional in V1

**Analysis**:
- Speculative intelligence (predicting future objections)
- Not deterministic computation
- V1 marked as "Optional" and "enhancement"

**Recommendation**: 
- Keep as **Tier 3 future enhancement**
- Mark as "AI-powered speculative analysis"
- Not required for MVP execution plans
- Consider for Phase 3 implementation

### 4. Clarify CAN-20 (Data Visualization/Reporting)
**Issue**: Is visualization part of execution logic or UI layer?

**Analysis**:
- organizer-3: "Show me patterns" could be text vs. visual
- V2 execution plan focused on **data generation**, not presentation
- Visualization typically handled by UI framework, not business logic

**Recommendation**:
- Keep CAN-20 as **Tier 3 UI-layer capability**
- Execution plans should output **structured data** (JSON, statistics)
- Visualization happens in **presentation layer** (separate from core logic)
- Add note: "Execution plans generate data; visualization is UI responsibility"

### 5. Split CAN-02 (Meeting Classification)
**Critical Issue**: Conflates meeting type and meeting importance

**Evidence**: Evaluator mentioned 4 times across multiple prompts

**Recommendation**:
- **CAN-02A**: Meeting Type Classification
  - Format-based: 1:1, team meeting, customer meeting, all-hands, etc.
  - Deterministic based on attendee count, subject keywords
- **CAN-02B**: Meeting Importance/Priority Assessment
  - Value-based: important vs. unimportant, high priority vs. low priority
  - Context-dependent: aligns with user goals and priorities

### 6. Clarify CAN-11 vs CAN-02 Boundary
**Issue**: Overlap between classification and preference matching

**Recommendation**:
- **CAN-02A/B**: Classify meetings by objective attributes (type, importance)
- **CAN-11**: Match meetings to **user-specific preferences** (priorities, goals, working style)
- Example: CAN-02B might flag a meeting as "important" (objective), while CAN-11 scores it against "customer meetings and product strategy" (subjective user priorities)

### 7. Make CAN-04 (NLU) Universal
**Issue**: Missing from organizer-3, but evaluator says it should be universal

**Recommendation**:
- Add CAN-04 to **all** natural language prompts
- It's the **entry point** for all execution plans
- Without NLU, system can't parse user intent and constraints

### 8. Document Task Dependencies
**Issue**: CAN-06 relationship to CAN-01 unclear

**Recommendation**: Create dependency graph showing:
- **CAN-06** (Availability Checking) **depends on** CAN-01 (Calendar Retrieval)
- **CAN-11** (Preference Matching) **depends on** CAN-04 (NLU - to extract preferences)
- **CAN-17** (Auto Rescheduling) **depends on** CAN-16 + CAN-06 + CAN-12 + CAN-03

### 9. Add Missing Capabilities
**New capabilities identified by evaluator:**

**CAN-21: Task Duration Estimation** (Tier 2)
- Estimate time required for meeting preparation
- Learn from historical data: "How long does this person typically need?"
- Needed for: organizer-2

**CAN-22: Work Attribution Discovery** (Tier 2)
- Discover who works on what from documents and collaboration patterns
- Beyond just "who has access" - infer active contribution
- Needed for: collaborate-1

**CAN-23: Conflict Resolution** (Tier 3)
- Handle cases where constraints cannot be satisfied
- Negotiate trade-offs, suggest alternatives
- Needed for: schedule-1 ("Do we assume we can always find a time?")

## Revised Canonical Task Library

### Tasks to Modify:
1. **CAN-02** → Split into **CAN-02A** (Type) and **CAN-02B** (Importance)
2. **CAN-07** → Refocus on metadata extraction, remove invitation sending
3. **CAN-17** → Mark as orchestrated capability, document dependencies
4. **CAN-18** → Mark as optional/future enhancement
5. **CAN-20** → Mark as UI-layer capability

### Tasks to Add:
6. **CAN-21**: Task Duration Estimation (Tier 2)
7. **CAN-22**: Work Attribution Discovery (Tier 2)
8. **CAN-23**: Conflict Resolution (Tier 3)

### Tasks to Enhance:
9. **CAN-04**: Mark as universal (required for all NL prompts)
10. **CAN-09**: Clarify scope (all document types or specialized?)

## Next Steps

1. **Update CANONICAL_UNIT_TASKS_REFERENCE.md** with revisions
2. **Re-run V2 analysis** with corrected task definitions
3. **Create task dependency graph** showing relationships
4. **Add missing CAN-04** to organizer-3 execution plan
5. **Add missing CAN-01** to schedule-1 execution plan
6. **Build V3 analysis** incorporating evaluation feedback
7. **Implement Phase 1 prompts** with corrected task framework

## Conclusion

The gap between V1 and V2 analysis reveals important insights:

1. **Tier 3 tasks** are less well-defined and often represent **composite capabilities** rather than atomic tasks
2. **Task naming** matters - CAN-07 name doesn't match V1 usage
3. **Optional vs. Required** distinction is important - CAN-18 was optional in V1, excluded in V2
4. **UI vs. Logic separation** - CAN-20 visualization is presentation layer, not execution logic
5. **Evaluator feedback** identified critical issues (CAN-02 conflation, CAN-11 overlap) that require framework revision

The 20 canonical tasks remain valid, but need:
- **Clearer definitions** (especially Tier 3)
- **Explicit dependencies** (CAN-06 ← CAN-01)
- **Scope boundaries** (CAN-02 vs CAN-11)
- **Layer assignment** (business logic vs UI)
- **Additional capabilities** (CAN-21, CAN-22, CAN-23)

---

**Analysis Date**: November 7, 2025  
**Analyst**: GitHub Copilot with Human Evaluation by Chin-Yew Lin  
**Status**: Pending framework revision and V3 analysis
