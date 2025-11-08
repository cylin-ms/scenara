# Calendar.AI Hero Prompts - Gold Standard Reference Report V2.0

**Document Version**: 2.1  
**Date**: November 8, 2025  
**Author**: Chin-Yew Lin  
**Framework**: Calendar.AI Canonical Unit Tasks Framework V2.0 (25 tasks - CAN-01 through CAN-25)  
**Source**: Human-validated gold standard evaluation with revisions  
**Evaluation Files**: 
- `v2_gold_standard_20251107_145124.json` (original GPT-5 analysis)
- `v2_gold_standard_v2_20251107.json` (revised with gold standard updates)

**Gold Standard Revisions (November 8, 2025)**:
1. **Collaborate-1**: CAN-09 (Document Generation) → CAN-23 (Agenda Generation/Structuring)
   - Rationale: Prompt explicitly mentions "set the agenda" - specialized task more appropriate
2. **Schedule-2**: CAN-23 (Conflict Resolution) → CAN-17 (Automatic Rescheduling)
   - Rationale: Prompt explicitly requests "help me reschedule" - automation task more appropriate

**Related Documents**:
- [CANONICAL_TASKS_GOLD_STANDARD_REFERENCE_V2.md](CANONICAL_TASKS_GOLD_STANDARD_REFERENCE_V2.md) - Comprehensive gold standard reference with execution compositions
- [CANONICAL_TASK_DECOMPOSITION_EXTRACTION.md](CANONICAL_TASK_DECOMPOSITION_EXTRACTION.md) - Quick reference extraction with task purposes
- [CANONICAL_TASKS_REFERENCE_V2.md](CANONICAL_TASKS_REFERENCE_V2.md) - Complete 25-task framework specifications
- [GPT5_V2_OPTIMIZATION_SUMMARY.md](model_comparison/GPT5_V2_OPTIMIZATION_SUMMARY.md) - GPT-5 3-trial stability test results
- [GOLD_STANDARD_REPORT_WRITING_GUIDE.md](GOLD_STANDARD_REPORT_WRITING_GUIDE.md) - Report format standards

**Supporting Documents Used to Create This Report**:
- **Primary Data Source**: `v2_gold_standard_v2_20251107.json` - Human-validated gold standard task decompositions
- **Original Prompts**: `9_hero_prompts_v2.txt` - Original v2 hero prompt definitions
- **Framework Specification**: `CANONICAL_TASKS_REFERENCE_V2.md` - Complete task definitions, schemas, and tiers
- **Gold Standard Reference**: `CANONICAL_TASKS_GOLD_STANDARD_REFERENCE_V2.md` - Source of truth with all task decompositions (v2.1, 2,840 lines)
- **Writing Guide**: `GOLD_STANDARD_REPORT_WRITING_GUIDE.md` - Template and formatting standards for this report
- **Baseline Results**: `v2_gold_standard_20251107_145124.json` - Original GPT-5 automated analysis results
- **Evaluation Data**: GPT-5 3-trial stability test results (November 7, 2025) with F1 scores and variance analysis

**Document Creation Process**:
1. Used `v2_gold_standard_v2_20251107.json` for authoritative task lists and evaluations
2. Referenced `9_hero_prompts_v2.txt` for exact prompt text
3. Cross-validated all task decompositions against `CANONICAL_TASKS_GOLD_STANDARD_REFERENCE_V2.md`
4. Followed structure and format from `GOLD_STANDARD_REPORT_WRITING_GUIDE.md`
5. Added execution compositions and examples based on framework specifications
6. Incorporated human evaluator notes from Chin-Yew Lin's manual review

---

## Executive Summary

### Purpose

This document provides the **gold standard canonical task analysis** for the 9 Calendar.AI hero prompts, serving as the authoritative reference for:

1. **LLM Evaluation**: Benchmark model performance in task decomposition (GPT-5, Claude, etc.)
2. **Framework Validation**: Validate the 25 canonical unit tasks V2.0 framework
3. **Training Data**: Ground truth for fine-tuning and prompt optimization
4. **Quality Assurance**: Reference standard for production system validation

### Methodology

This gold standard was created through a rigorous 4-phase process:

#### Phase 1: Framework Development (October-November 2025)
- **Original Framework**: 24 canonical tasks developed from initial meeting intelligence analysis
- **Task Evolution**: CAN-02A/CAN-02B consolidated and renumbered to CAN-02/CAN-03 for clarity
  - CAN-02A (Meeting Type Classification) → CAN-02
  - CAN-02B (Meeting Importance Assessment) → CAN-03
- **NEW Task Addition**: CAN-25 (Event Annotation/Flagging) identified from evaluation needs
- **Framework Finalized**: 25 canonical tasks organized into 3 tiers (Universal, Common, Specialized)

#### Phase 2: GPT-5 Baseline Analysis (November 7, 2025)
- **Automated Analysis**: GPT-5 analyzed all 9 hero prompts using optimized V2.0 decomposition prompts
- **Performance**: Initial baseline established with systematic evaluation
- **Key Findings**:
  - CAN-05 (Attendee Resolution) frequently missed in automated analysis (3 prompts affected)
  - CAN-18 (Risk Anticipation) scope ambiguity detected (over-interpretation in Collaborate-1)
  - CAN-25 (Event Flagging) not yet in framework but needed for Organizer-2
  - CAN-16 (Event Monitoring) missing from Organizer-2 despite "track" requirement

#### Phase 3: Prompt Optimization & Validation (November 7, 2025)
- **Optimization**: Enhanced GPT-5 prompts with critical concepts:
  1. **Explicit task definitions** with clear boundaries
  2. **Tier-based organization** (Universal → Common → Specialized)
  3. **Dependency relationships** between tasks
  4. **Context-specific guidance** for specialized tasks
  5. **Over-interpretation warnings** for scope clarity

- **3-Trial Stability Test**: 3 API calls per prompt (3 trials × 9 prompts = 27 evaluations)
  - **Average Performance**: F1 91.98% ± 16.38% (EXCELLENT - ceiling effect with 7/9 at 100%)
  - **CAN-05 Detection**: Improved through explicit dependency documentation
  - **CAN-25 Validation**: NEW task added based on evaluation findings
  - **Consistency**: High task selection agreement across trials (7/9 prompts at 100% F1)

#### Phase 4: Human Correction & Gold Standard Creation (November 7-8, 2025)
- **Manual Review**: Human expert (Chin-Yew Lin) reviewed all GPT-5 outputs against prompt requirements
- **Corrections Applied**:
  - **Added CAN-25** to Organizer-2 ("flag meetings" requirement)
  - **Added missing CAN-05** to Schedule-2, Collaborate-1, and Collaborate-2 (critical for attendee resolution)
  - **Removed CAN-18** from Collaborate-1 (over-interpretation: meeting goals are INPUT, not system tasks)
  - **Added CAN-16** to Organizer-2 ("track" requirement for continuous monitoring)
- **Gold Standard Revisions** (November 8, 2025):
  - **Collaborate-1**: Accepted CAN-23 (Agenda Generation) as specialized task when prompt explicitly says "set the agenda"
  - **Schedule-2**: Accepted CAN-17 (Automatic Rescheduling) as automation task when prompt explicitly says "help me reschedule"
  - **Specialization Principle Established**: Accept specialized tasks (Tier 3) when prompts explicitly mention the specialization
- **Validation**: Cross-referenced with original prompt requirements and execution workflows
- **Final Output**: This comprehensive gold standard reference report

### Gold Standard Statistics

#### Overall Metrics

| Metric | Value |
|--------|-------|
| **Total Prompts** | 9 hero prompts |
| **Total Canonical Tasks** | 25 (CAN-01 through CAN-25) |
| **Tasks Used** | 22 unique tasks (88% framework coverage) |
| **Average Tasks/Prompt** | 7.2 tasks |
| **Task Range** | 3-10 tasks per prompt |
| **Tier 1 (Universal) Coverage** | 100% (all 5 universal tasks used) |
| **Tier 2 (Common) Coverage** | 89% (8 of 9 common tasks used) |
| **Tier 3 (Specialized) Coverage** | 80% (8 of 10 specialized tasks used) |
| **Unused Tasks** | 3 tasks (CAN-24, and 2 others with 0% usage) |

#### Human Evaluation Results (Updated November 8, 2025)

| Rating | Count | Prompts | F1 Score Range |
|--------|-------|---------|----------------|
| ✅ **Correct** | 5 prompts | Organizer-1, Organizer-2, Organizre-3, Schedule-1, Schedule-3, Collaborate-2, Collaborate-3 | 100% |
| ⚠️ **Partial** | 2 prompts | Schedule-2 (missing CAN-06), Collaborate-1 (missing CAN-05) | 50-88.89% |

**Performance Metrics**:
- **Mean F1**: 93.21% ± 14.97% (EXCELLENT)
- **Median F1**: 100% (7 of 9 prompts)
- **Best F1**: 100% (7 prompts)
- **Weakest F1**: 50% (Collaborate-1 - lowest complexity with only 3 tasks)
- **Distribution**: 7 at 100%, 1 at 88.89%, 1 at 50%

**Note on Statistical Interpretation**: The large standard deviation (±16.38%) reflects a **ceiling effect** where 7 of 9 prompts achieved perfect 100% F1 scores. This is mathematically correct for bounded metrics (0-100%) and indicates **excellent overall performance** with most prompts at maximum accuracy.

#### Key Insights from Evaluation

1. **NEW Task Validated**: CAN-25 (Event Annotation/Flagging) for "flag meetings" requirement (Organizer-2)
2. **CAN-05 Critical But Often Missed**: Attendee resolution essential but frequently overlooked in automated analysis (Schedule-2, Collaborate-1, Collaborate-2)
3. **Specialization Principle Established**: Accept specialized tasks (CAN-23, CAN-17) when prompts explicitly mention the specialization
4. **CAN-16 Usage Clarified**: Event monitoring appropriate for "track" use case (Organizer-2)
5. **CAN-18 Scope Boundaries**: Risk anticipation should NOT be used when meeting goals are INPUT for other tasks (Collaborate-1)
6. **Framework Coverage Validated**: 88% of canonical tasks used across 9 prompts demonstrates comprehensive framework design

---

## Task Frequency Distribution

| Task ID | Task Name | Frequency | Prompts Using | Tier |
|---------|-----------|-----------|---------------|------|
| **CAN-04** | Natural Language Understanding | 100% | 9/9 (ALL) | Universal |
| **CAN-01** | Calendar Events Retrieval | 100% | 9/9 (ALL) | Universal |
| **CAN-07** | Meeting Metadata Extraction | 78% | 7/9 | Common |
| **CAN-05** | Attendee/Contact Resolution | 67% | 6/9 | Universal |
| **CAN-03** | Meeting Importance Assessment | 67% | 6/9 | Universal |
| **CAN-02** | Meeting Type Classification | 56% | 5/9 | Universal |
| **CAN-09** | Document Generation/Formatting | 56% | 5/9 | Common |
| **CAN-08** | Document/Content Retrieval | 44% | 4/9 | Common |
| **CAN-12** | Constraint Satisfaction | 44% | 4/9 | Common |
| **CAN-06** | Availability Checking | 44% | 4/9 | Common |
| **CAN-11** | Priority/Preference Matching | 56% | 5/9 | Common |
| **CAN-13** | RSVP Status Update | 33% | 3/9 | Common |
| **CAN-14** | Recommendation Engine | 33% | 3/9 | Common |
| **CAN-10** | Time Aggregation/Statistical Analysis | 22% | 2/9 | Common |
| **CAN-16** | Event Monitoring/Change Detection | 22% | 2/9 | Specialized |
| **CAN-15** | Recurrence Rule Generation | 22% | 2/9 | Specialized |
| **CAN-17** | Automatic Rescheduling | 11% | 1/9 | Specialized |
| **CAN-18** | Objection/Risk Anticipation | 11% | 1/9 | Specialized |
| **CAN-19** | Resource Booking | 11% | 1/9 | Specialized |
| **CAN-20** | Data Visualization/Reporting | 11% | 1/9 | Specialized |
| **CAN-21** | Focus Time/Preparation Time Analysis | 11% | 1/9 | Specialized |
| **CAN-22** | Research/Intelligence Gathering | 11% | 1/9 | Specialized |
| **CAN-23** | Agenda Generation/Structuring | 11% | 1/9 | Specialized |
| **CAN-25** | Event Annotation/Flagging (NEW) | 11% | 1/9 | Specialized |
| **CAN-24** | Multi-party Coordination/Negotiation | 0% | 0/9 | Specialized |

**Observations**:
- **Universal Tasks** (100% coverage in tier): CAN-04, CAN-01 appear in ALL prompts; CAN-05, CAN-03, CAN-02 in 56-67%
- **Common Tasks** (50-99% usage): CAN-07 (78%), CAN-09, CAN-11 (56%) show high reuse across prompt types
- **Specialized Tasks** (<50% usage): All 10 specialized tasks used, but each appears in only 1-2 prompts (appropriate specialization)
- **Unused Tasks**: Only CAN-24 (Multi-party Coordination) at 0% - may be orchestration pattern rather than discrete task

---

## Part 2: Per-Prompt Detailed Analysis

---

### Hero Prompt 1: Organizer-1

**Prompt**: "Keep my Calendar up to date by committing to only meetings that are part of my priorities."

**Category**: Organizer  
**Capabilities Required**: Meeting prioritization, RSVP management based on user priorities  
**Gold Standard F1**: 100%  
**Evaluation**: ✅ **Correct**

#### Canonical Task Decomposition: 7 Tasks

**Task 1: Natural Language Understanding (CAN-04)**
- **Purpose**: Extract user intent (keep calendar updated, commit based on priorities) and understand constraint
- **Input**: User prompt text
- **Output**: Structured constraints: {"intent": "manage_calendar_based_on_priorities", "constraint": "only_priority_meetings"}
- **Tier**: Universal (Tier 1)

**Task 2: Calendar Events Retrieval (CAN-01)**
- **Purpose**: Retrieve pending calendar invitations and existing meetings for RSVP management
- **Input**: Time range (current/upcoming), filter for pending RSVPs
- **Output**: List of calendar events with RSVP status (pending, tentative, accepted)
- **Tier**: Universal (Tier 1)
- **Dependencies**: CAN-04 (NLU extracts time range)

**Task 3: Meeting Metadata Extraction (CAN-07)**
- **Purpose**: Extract RSVP status, attendees, meeting details for pending invitations to enable prioritization
- **Input**: Calendar events from CAN-01
- **Output**: Detailed metadata including RSVP status, attendees, subject, organizer, date/time
- **Tier**: Common (Tier 2)
- **Note**: PARENT task - enables CAN-13 (RSVP Update)

**Task 4: Meeting Type Classification (CAN-02)**
- **Purpose**: Classify meetings by format (1:1, team sync, customer meeting, etc.) for priority matching
- **Input**: Meeting metadata from CAN-07
- **Output**: Meeting type classification for each event (31+ types supported)
- **Tier**: Universal (Tier 1)
- **Note**: Objective, format-based classification

**Task 5: Meeting Importance Assessment (CAN-03)**
- **Purpose**: Assess strategic importance and alignment with user priorities
- **Input**: Meeting metadata + user priorities (must be defined separately)
- **Output**: Importance scores and priority alignment ratings
- **Tier**: Universal (Tier 1)
- **Note**: Subjective, value-based assessment - pairs with CAN-02

**Task 6: Priority/Preference Matching (CAN-11)**
- **Purpose**: Match meetings against user's priorities (system must know user's priorities)
- **Input**: Classified meetings + user priorities
- **Output**: Priority-aligned meeting list with match scores
- **Tier**: Common (Tier 2)

**Task 7: RSVP Status Update (CAN-13)**
- **Purpose**: Update RSVP status (accept priority meetings, decline/tentative others)
- **Input**: Prioritized meeting list from CAN-11
- **Output**: RSVP updates sent to calendar system (accept/decline/tentative)
- **Tier**: Common (Tier 2)
- **Dependencies**: CAN-07 (metadata extraction provides current RSVP status)

#### Evaluation Criteria
- RSVP decision accuracy aligned with user priorities (>90% correct)
- Meeting type classification precision (% correctly classified)
- Priority matching correctness (alignment score accuracy)
- RSVP update execution success rate (% completed without errors)

#### Execution Composition

**How Tasks Work Together to Answer the Prompt:**

```
STEP 1: Understand User Intent
CAN-04 (NLU) → Extract intent and constraint
  - Parse: "keep calendar up to date", "committing to only meetings", "part of my priorities"
  - Extract: intent = "manage_calendar_based_on_priorities"
  - Extract: constraint = "only_priority_meetings"
  - Note: User's specific priorities must be known from user profile/settings
  - Output: Structured intent with constraint parameters

STEP 2: Retrieve Pending Invitations
CAN-01 (Calendar Retrieval) → Load all pending calendar invitations
  - Filter: RSVP status = "pending" OR "tentative"
  - Time range: Current + upcoming meetings (next 4 weeks)
  - Output: Array of calendar events awaiting response (e.g., 15 pending invitations)

STEP 3: Extract Meeting Details
CAN-07 (Metadata Extraction) → Extract comprehensive meeting information
  - For each invitation: attendees, subject, organizer, agenda, RSVP status, date/time
  - Parse: Meeting descriptions for context clues
  - Output: Enriched meeting objects with full metadata

STEP 4-5: Classify Meetings (Parallel Processing)
CAN-02 (Meeting Type) → Classify by format
  - Categories: 1:1, team sync, customer meeting, all-hands, executive review
  - Logic: Attendee count, recurring pattern, subject keywords
  - Output: Objective classification based on structure

CAN-03 (Importance Assessment) → Score strategic value
  - Evaluate: Attendee seniority, business impact, strategic alignment
  - Score: High/Medium/Low importance based on context
  - Output: Subjective assessment based on meeting context

STEP 6: Match Against User's Priorities
CAN-11 (Priority Matching) → Align meetings with user's known priorities
  - Input: User's priorities from profile/settings (e.g., ["customer meetings", "product strategy"])
  - Compare: Meeting type + importance against user's priorities
  - Calculate: Priority alignment scores (0-100%)
  - Rank: Meetings by priority match strength
  - Output: Sorted list with alignment justification

STEP 7: Execute RSVP Actions
CAN-13 (RSVP Update) → Update calendar responses based on priority alignment
  - Accept: High priority matches (>80% alignment)
  - Tentative: Medium priority matches (40-80% alignment)
  - Decline: Low priority matches (<40% alignment)
  - Output: Updated RSVP status sent to calendar system

OUTPUT: Updated calendar with prioritized commitments
  - Accepted meetings: Those aligned with user's priorities
  - Declined/Tentative meetings: Those not aligned (with justification)
  - Calendar status: Current with only priority-aligned commitments
```

#### Key Orchestration Patterns
- **Sequential Foundation**: CAN-04 → CAN-01 → CAN-07 (linear dependency chain)
- **Parallel Classification**: CAN-02 and CAN-03 can run concurrently on same meeting data
- **Parent-Child Relationship**: CAN-07 (Metadata Extraction) enables CAN-13 (RSVP Update)
- **Decision Point**: CAN-11 (Priority Matching) determines which meetings get accepted/declined/tentative
- **Write Operation**: CAN-13 is the only task that modifies calendar state

#### Example Flow - Priority-Based RSVP Management

```
Input: "Keep my Calendar up to date by committing to only meetings that are part of my priorities."

Context: User profile has priorities = ["customer meetings", "product strategy"]

CAN-04: Extract intent and constraint ✓
  → intent: manage_calendar_based_on_priorities
  → constraint: only_priority_meetings
  → Note: System retrieves user's priorities from profile

CAN-01: Retrieved 5 pending invitations ✓
  1. "Q4 Planning Meeting with Marketing Team" (tentative)
  2. "Customer Discovery Call - Contoso" (pending)
  3. "1:1 with Product Manager - Strategy Review" (pending)
  4. "Engineering Team Standup" (pending)
  5. "Product Roadmap Review with PM Team" (pending)

CAN-07: Extract metadata for each invitation ✓
  Meeting 1: Attendees: [Marketing Team (8)], Subject: "Q4 Planning", Organizer: Marketing VP
  Meeting 2: Attendees: [Contoso VP, Account Mgr], Subject: "Discovery Call", Type: Customer
  Meeting 3: Attendees: [Product Manager], Subject: "Strategy Review", Type: 1:1
  Meeting 4: Attendees: [Engineering Team (12)], Subject: "Standup", Type: Daily recurring
  Meeting 5: Attendees: [PM Team (6)], Subject: "Roadmap Review", Type: Product strategy

CAN-02: Classify meeting types ✓
  Meeting 1: "Internal Team Meeting" (8+ attendees, internal)
  Meeting 2: "Customer Meeting" (external domain, customer context)
  Meeting 3: "1:1 - Product Strategy" (2 people, strategy keyword)
  Meeting 4: "Team Sync" (daily standup pattern)
  Meeting 5: "Product Planning" (PM team, roadmap keyword)

CAN-03: Assess importance ✓
  Meeting 1: Medium (planning session, not customer-facing)
  Meeting 2: HIGH (VP-level customer meeting)
  Meeting 3: HIGH (product strategy discussion)
  Meeting 4: Low (routine daily standup)
  Meeting 5: HIGH (product roadmap - strategic planning)

CAN-11: Match against user's priorities (from profile) ✓
  User priorities: ["customer meetings", "product strategy"]
  Meeting 1: Priority Match = 25% (not customer or product strategy)
  Meeting 2: Priority Match = 95% (CUSTOMER MEETING - direct match!)
  Meeting 3: Priority Match = 90% (PRODUCT STRATEGY - direct match!)
  Meeting 4: Priority Match = 10% (routine operations, not strategic)
  Meeting 5: Priority Match = 85% (PRODUCT STRATEGY - roadmap planning)

CAN-13: Execute RSVP updates ✓
  Meeting 1: DECLINE (low priority match 25%)
    → Action: Decline
    → Reason: "Doesn't align with priorities"
  
  Meeting 2: ACCEPT (high priority match 95%)
    → Action: Accept
    → Reason: "HIGH PRIORITY - Customer meeting with VP"
  
  Meeting 3: ACCEPT (high priority match 90%)
    → Action: Accept
    → Reason: "HIGH PRIORITY - Product strategy discussion"
  
  Meeting 4: DECLINE (low priority match 10%)
    → Action: Decline
    → Reason: "Routine operational meeting, not aligned with priorities"
  
  Meeting 5: ACCEPT (high priority match 85%)
    → Action: Accept
    → Reason: "HIGH PRIORITY - Product roadmap strategy"

OUTPUT to User:
  ✅ ACCEPTED (3 meetings aligned with priorities):
     • Customer Discovery Call - Contoso (customer meetings priority)
     • 1:1 with Product Manager - Strategy Review (product strategy priority)
     • Product Roadmap Review with PM Team (product strategy priority)
  
  ❌ DECLINED (2 meetings not aligned):
     • Q4 Planning Meeting with Marketing Team
     • Engineering Team Standup
  
Calendar Status: ✅ Up to date with only priority-aligned meetings committed
```

---

### Hero Prompt 2: Organizer-2

**Prompt**: "Track all my important meetings and flag any that require focus time to prepare for them."

**Category**: Organizer  
**Capabilities Required**: Meeting tracking, importance assessment, preparation time estimation, event flagging  
**Gold Standard F1**: 100%  
**Evaluation**: ✅ **Correct** (with CAN-25 added)

**Human Evaluator Notes**: 
> "Missing 'track important meetings' and 'flag meetings need time for preparation'. Can we attribute 'track' to CAN-16? But we do not have any Canonical task for 'flag'. 'Flag' is an action that we add an annotation to an event on calendar. We need to add new canonical tasks for similar tasks that signal something on calendar if some predefined condition occurs."

#### Canonical Task Decomposition: 9 Tasks (Including NEW CAN-25)

**Task 1: Natural Language Understanding (CAN-04)**
- **Purpose**: Extract dual intent (track important meetings, flag prep-time meetings)
- **Input**: User prompt text
- **Output**: {"intent": ["track_and_flag_meetings"], "criteria": "important", "flag_condition": "requires_prep_time"}
- **Tier**: Universal (Tier 1)

**Task 2: Calendar Events Retrieval (CAN-01)**
- **Purpose**: Retrieve upcoming meetings to track and analyze
- **Input**: Time range (this week/upcoming 2-4 weeks)
- **Output**: List of calendar events for tracking analysis
- **Tier**: Universal (Tier 1)

**Task 3: Meeting Metadata Extraction (CAN-07)**
- **Purpose**: Extract meeting details (attendees, subject, complexity indicators) for prep time estimation
- **Input**: Calendar events from CAN-01
- **Output**: Meeting metadata including attachments, agenda, attendees, organizer
- **Tier**: Common (Tier 2)

**Task 4: Meeting Type Classification (CAN-02)**
- **Purpose**: Classify meeting formats to assess complexity and prep requirements
- **Input**: Meeting metadata from CAN-07
- **Output**: Meeting type (1:1, team, customer, executive review, board meeting, etc.)
- **Tier**: Universal (Tier 1)

**Task 5: Meeting Importance Assessment (CAN-03)**
- **Purpose**: Assess which meetings are "important" based on attendee seniority, business impact
- **Input**: Meeting metadata + classifications
- **Output**: Importance scores identifying important meetings (Critical/High/Medium/Low)
- **Tier**: Universal (Tier 1)

**Task 6: Focus Time/Preparation Time Analysis (CAN-21)**
- **Purpose**: Estimate prep time needed based on meeting type, attendees, complexity
- **Input**: Meeting metadata + type classification + complexity signals
- **Output**: Prep time estimates (e.g., "90 min prep for executive review", "240 min for board meeting")
- **Tier**: Specialized (Tier 3)

**Task 7: Priority/Preference Matching (CAN-11)**
- **Purpose**: Filter to "important meetings" based on user criteria
- **Input**: Meetings with importance scores
- **Output**: Filtered list of important meetings requiring tracking
- **Tier**: Common (Tier 2)

**Task 8: Event Monitoring/Change Detection (CAN-16)**
- **Purpose**: Setup tracking/monitoring for important meetings (addresses "track" requirement)
- **Input**: Important meetings list from CAN-11
- **Output**: Monitoring configuration for changes, updates, cancellations
- **Tier**: Specialized (Tier 3)
- **Note**: Addresses "track" requirement with continuous monitoring

**Task 9: Event Annotation/Flagging (CAN-25) - NEW IN V2.0**
- **Purpose**: Flag meetings that require prep time with visual indicators (addresses "flag" requirement)
- **Input**: Meetings with prep time estimates from CAN-21
- **Output**: Event annotations/flags added to calendar (e.g., "⚠️ 90 min prep needed")
- **Tier**: Specialized (Tier 3)
- **Note**: **NEW CANONICAL TASK** created for this use case - conditional event annotation based on computed conditions

#### Evaluation Criteria
- Importance classification accuracy (% of truly important meetings identified)
- Prep time estimation reasonableness (realistic time allocations)
- Flagging precision (only flag meetings actually requiring prep >30min)
- Tracking setup completeness (monitoring configured for all important meetings)
- CAN-25 correctness (NEW task appropriately applied for conditional flagging)

#### Execution Composition

**How Tasks Work Together to Answer the Prompt:**

```
STEP 1: Understand Tracking and Flagging Requirements
CAN-04 (NLU) → Extract dual intent
  - Parse: "track all my important meetings" = monitoring requirement
  - Parse: "flag any that require focus time to prepare" = conditional annotation
  - Output: {"intent": ["track_meetings", "flag_prep_required"], "criteria": "important"}

STEP 2: Retrieve Upcoming Meetings
CAN-01 (Calendar Retrieval) → Load calendar for analysis period
  - Time range: Next 2-4 weeks (typical planning horizon)
  - Filter: All scheduled meetings (not just pending)
  - Output: Array of upcoming calendar events (e.g., 25 meetings)

STEP 3: Extract Meeting Context
CAN-07 (Metadata Extraction) → Extract complexity indicators
  - For each meeting: attendees, subject, organizer, agenda, attachments, notes
  - Complexity signals: Agenda length, attachment count, attendee seniority
  - Output: Enriched meeting objects with preparation context

STEP 4-5: Classify and Score Meetings (Parallel Processing)
CAN-02 (Meeting Type) → Classify by format
  - Categories: 1:1, team sync, customer, exec review, board meeting
  - High-prep types: Executive reviews, board meetings, customer presentations

CAN-03 (Importance Assessment) → Score strategic value
  - Evaluate: Attendee seniority (VP+, C-level), business impact, customer-facing
  - Output: Importance ratings (Critical, High, Medium, Low)

STEP 6: Estimate Preparation Time
CAN-21 (Preparation Time Analysis) → Calculate prep time needed
  - Logic: Executive review + attachments = 90-120 min
  - Logic: Customer presentation = 60-90 min
  - Logic: Board meeting = 2-4 hours
  - Logic: Regular 1:1 = 0-15 min
  - Output: Prep time estimates per meeting

STEP 7: Filter to Important Meetings
CAN-11 (Priority Matching) → Select meetings to track
  - Criteria: Importance = "Critical" OR "High"
  - Output: Filtered list of important meetings

STEP 8-9: Setup Tracking and Flagging (Parallel Operations)
CAN-16 (Event Monitoring) → Configure change tracking
  - Monitor: Cancellations, reschedules, attendee changes
  - Alert: User when important meeting changes occur
  - Output: Monitoring rules active for important meetings

CAN-25 (Event Annotation/Flagging) → Flag meetings needing prep (NEW TASK)
  - Condition: IF prep_time > 30 minutes THEN add flag
  - Flag format: "⚠️ [X] min prep needed before meeting"
  - Visibility: Add to calendar event as annotation/category
  - Output: Visual flags added to calendar for prep-required meetings

OUTPUT: Comprehensive meeting tracking and flagging system
  - Important meetings tracked with change monitoring active
  - Meetings requiring prep time visually flagged with time estimates
  - User can see at-a-glance which meetings need preparation focus time
```

#### Key Orchestration Patterns
- **Sequential Foundation**: CAN-04 → CAN-01 → CAN-07 (linear dependency)
- **Parallel Classification**: CAN-02 and CAN-03 analyze same metadata concurrently
- **Prep Time Gate**: CAN-21 must complete before CAN-25 (flagging depends on estimates)
- **Parallel Finalization**: CAN-16 (tracking) and CAN-25 (flagging) are independent operations
- **Conditional Logic**: CAN-25 only flags IF prep_time > threshold (conditional execution)
- **NEW Task Pattern**: CAN-25 introduces event annotation capability (V2.0 framework addition)

#### Example Flow - Meeting Tracking and Flagging

```
User Request: "Track all my important meetings and flag any that require focus time to prepare for them."

CAN-04: Parse requirements ✓
  → track: important meetings
  → flag: meetings requiring focus time for prep

CAN-01: Retrieved 12 upcoming meetings ✓
  1. "Weekly 1:1 with Direct Report" (30 min)
  2. "Q4 Business Review with CEO" (60 min)
  3. "Customer Presentation - Contoso" (90 min)
  4. "Team Standup" (15 min, Daily)
  5. "Board of Directors Meeting" (120 min)
  ... (7 more meetings)

CAN-07: Extract metadata ✓
  Meeting 2: Attendees: [CEO, CFO, VP Ops], Agenda: 15-page deck, Notes: "Prepare revenue projections"
  Meeting 3: Attendees: [Contoso VP, CTO], Agenda: "Product demo", Attachments: Demo script
  Meeting 5: Attendees: [Board (6)], Agenda: "Q4 board review", Attachments: 50-page packet

CAN-02: Classify types ✓
  Meeting 1: "1:1 - Management"
  Meeting 2: "Executive Review"
  Meeting 3: "Customer Presentation"
  Meeting 4: "Team Sync"
  Meeting 5: "Board Meeting"

CAN-03: Assess importance ✓
  Meeting 1: Medium
  Meeting 2: CRITICAL (CEO financial review)
  Meeting 3: HIGH (customer VP)
  Meeting 4: Low
  Meeting 5: CRITICAL (board governance)

CAN-21: Estimate prep time ✓
  Meeting 1: 15 min
  Meeting 2: 120 min (prepare projections, review 15-page deck)
  Meeting 3: 90 min (rehearse demo, review script)
  Meeting 4: 0 min
  Meeting 5: 240 min (review 50-page board packet)

CAN-11: Filter to important ✓
  → Important meetings: #2 (Q4 Business Review), #3 (Customer Presentation), #5 (Board Meeting)

CAN-16: Setup monitoring ✓
  → Tracking enabled for meetings 2, 3, 5
  → Alerts: cancellations, reschedules, attendee changes

CAN-25: Flag meetings needing prep ✓ (NEW TASK)
  Meeting 2: 120 min > 30 min → FLAG ⚠️
    → "⚠️ 120 min prep needed - Review deck & prepare projections"
  Meeting 3: 90 min > 30 min → FLAG ⚠️
    → "⚠️ 90 min prep needed - Rehearse demo & review script"
  Meeting 5: 240 min > 30 min → FLAG ⚠️
    → "⚠️ 240 min prep needed - Review 50-page board packet"

OUTPUT to User:
  ✅ Tracking 3 important meetings
  ✅ Change monitoring active
  ✅ 3 meetings flagged for prep time:
     ⚠️ Wed - Q4 Business Review: 120 min prep
     ⚠️ Thu - Customer Presentation: 90 min prep
     ⚠️ Fri - Board Meeting: 240 min prep (schedule focus time!)

**Key Insight**: CAN-25 is a NEW canonical task created for this use case - the "flag" requirement couldn't be satisfied by existing tasks.
```

---

### Hero Prompt 3: Organizre-3

**Prompt**: "Help me understand where I am spending my time and identify ways I can reclaim time to focus more on my top priorities."

**Category**: Organizer  
**Capabilities Required**: Time analysis, pattern identification, recommendation generation, data visualization  
**Gold Standard F1**: 100%  
**Evaluation**: ✅ **Correct**

#### Canonical Task Decomposition: 9 Tasks

**Task 1: Natural Language Understanding (CAN-04)**
- **Purpose**: Extract dual intent (time analysis + reclamation recommendations)
- **Input**: User prompt text
- **Output**: {"intent": ["analyze_time_spend", "recommend_reclamation"], "priorities": [user's top priorities]}
- **Tier**: Universal (Tier 1)

**Task 2: Calendar Events Retrieval (CAN-01)**
- **Purpose**: Retrieve historical and upcoming meetings for comprehensive time analysis
- **Input**: Time range (past 1-3 months + upcoming 2 weeks)
- **Output**: Complete meeting dataset for analysis (e.g., 180 meetings over 90 days)
- **Tier**: Universal (Tier 1)

**Task 3: Meeting Metadata Extraction (CAN-07)**
- **Purpose**: Extract meeting details for categorization and analysis
- **Input**: Calendar events from CAN-01
- **Output**: Detailed metadata (attendees, duration, type, recurrence pattern)
- **Tier**: Common (Tier 2)

**Task 4: Meeting Type Classification (CAN-02)**
- **Purpose**: Classify meetings by format for time breakdown analysis
- **Input**: Meeting metadata from CAN-07
- **Output**: Meeting type classifications (1:1, team, customer, planning, admin, etc.)
- **Tier**: Universal (Tier 1)

**Task 5: Meeting Importance Assessment (CAN-03)**
- **Purpose**: Assess importance to identify low-value reclamation candidates
- **Input**: Meetings with type classifications
- **Output**: Importance scores (High/Medium/Low-value meetings)
- **Tier**: Universal (Tier 1)

**Task 6: Time Aggregation/Statistical Analysis (CAN-10)**
- **Purpose**: Aggregate time spent by meeting type, importance, attendees with trends
- **Input**: Classified meetings with metadata
- **Output**: Time breakdown statistics (e.g., "30% in 1:1s, 25% in customer meetings, 15% in admin")
- **Tier**: Common (Tier 2)
- **Note**: Critical for "understand where I am spending my time"

**Task 7: Priority/Preference Matching (CAN-11)**
- **Purpose**: Match meetings against user's top priorities for gap analysis
- **Input**: Meetings + user priorities from CAN-04
- **Output**: Priority alignment analysis (where time SHOULD go vs ACTUALLY goes)
- **Tier**: Common (Tier 2)

**Task 8: Recommendation Engine (CAN-14)**
- **Purpose**: Generate actionable recommendations for time reclamation
- **Input**: Time analysis + low-priority/low-value meetings
- **Output**: Ranked recommendations (decline, delegate, shorten, consolidate) with time savings
- **Tier**: Common (Tier 2)
- **Note**: Addresses "identify ways I can reclaim time"

**Task 9: Data Visualization/Reporting (CAN-20)**
- **Purpose**: Create visual time breakdown (charts, graphs, dashboard)
- **Input**: Time aggregation statistics from CAN-10
- **Output**: Visual dashboard showing time distribution (pie charts, trend lines, heatmaps)
- **Tier**: Specialized (Tier 3)
- **Note**: Helps user "understand" through visualization

#### Evaluation Criteria
- Time categorization accuracy (% of meetings correctly classified by type)
- Priority alignment scoring correctness (meetings properly matched to priorities)
- Recommendation actionability (% of suggestions user can realistically implement)
- Visualization clarity (dashboard effectively communicates time patterns)
- Reclamation opportunity identification (low-value time correctly identified)

#### Execution Composition

**How Tasks Work Together to Answer the Prompt:**

```
STEP 1: Understand Analysis Requirements
CAN-04 (NLU) → Extract dual intent
  - Parse: "understand where I am spending my time" = historical time analysis
  - Parse: "identify ways I can reclaim time" = optimization/recommendation generation
  - Parse: "focus more on my top priorities" = priority-based gap analysis
  - Output: {"intent": ["time_analysis", "reclamation_recommendations"], "timeframe": "historical"}

STEP 2: Retrieve Meeting History
CAN-01 (Calendar Retrieval) → Load comprehensive meeting dataset
  - Time range: Past 1-3 months (historical) + upcoming 2 weeks
  - Include: All completed and scheduled meetings
  - Filter: Exclude canceled meetings
  - Output: Complete meeting history (e.g., 180 meetings over 90 days)

STEP 3: Extract Meeting Details
CAN-07 (Metadata Extraction) → Extract classification signals
  - For each meeting: attendees, duration, subject, organizer, recurrence pattern
  - Additional: Meeting notes, attachments, historical attendance
  - Output: Enriched meeting objects with full context

STEP 4-5: Classify and Score Meetings (Parallel Processing)
CAN-02 (Meeting Type) → Categorize by format
  - Categories: 1:1, team sync, customer, planning, all-hands, admin, other
  - Pattern detection: Recurring vs ad-hoc
  - Output: Type classification for time bucketing

CAN-03 (Importance Assessment) → Score strategic value
  - Criteria: Business impact, attendee seniority, strategic alignment
  - Ratings: High-value (strategic), Medium-value (necessary), Low-value (reclaim targets)
  - Output: Importance scores for filtering

STEP 6: Aggregate Time Patterns
CAN-10 (Time Aggregation) → Calculate time distribution statistics
  - By type: "30% in 1:1s, 25% in customer meetings, 20% in team syncs"
  - By participant: "8 hours/month with Manager, 6 hours with Product Team"
  - By importance: "40% high-value, 35% medium-value, 25% low-value"
  - Trends: Time spend increasing/decreasing over time
  - Output: Comprehensive time breakdown with multiple dimensions

STEP 7: Match Against Priorities
CAN-11 (Priority Matching) → Analyze priority alignment
  - Compare: Current time allocation vs user's stated top priorities
  - Gap analysis: Where time SHOULD go vs where it ACTUALLY goes
  - Output: Priority alignment scores and misalignment identification

STEP 8-9: Generate Insights and Visualizations (Parallel Processing)
CAN-14 (Recommendation Engine) → Generate reclamation opportunities
  - Identify: Low-value recurring meetings (admin reviews, status meetings)
  - Suggest: Decline, delegate, reduce frequency, shorten, consolidate
  - Prioritize: Highest-impact recommendations first
  - Output: Ranked actionable recommendations with time savings estimates

CAN-20 (Data Visualization) → Create visual dashboard
  - Pie chart: Time by meeting type
  - Bar chart: Hours per week over time (trending)
  - Heatmap: Meeting density by day/hour
  - Priority breakdown: High vs medium vs low value
  - Output: Interactive visual dashboard

OUTPUT: Comprehensive time analysis and reclamation report
  1. WHERE TIME GOES: Breakdown by type, participant, priority (with visualizations)
  2. PATTERNS DETECTED: Recurring commitments, trending changes
  3. PRIORITY ALIGNMENT: Gap between current spend vs top priorities
  4. RECLAMATION OPPORTUNITIES: Specific recommendations to free up time
```

#### Key Orchestration Patterns
- **Historical Analysis Focus**: All tasks operate on PAST data (1-3 months lookback) plus future scheduled
- **Parallel Classification**: CAN-02, CAN-03 process same events concurrently
- **Aggregation Pipeline**: CAN-10 (time stats) feeds both CAN-14 (recommendations) and CAN-20 (visualization)
- **Recommendation Filtering**: CAN-14 uses CAN-03 (importance) and CAN-11 (priority match) to identify targets
- **Dual Output**: CAN-14 (actionable text) + CAN-20 (visual dashboard) provide complementary insights
- **Most Complex Organizer**: Uses 9 tasks across all tiers - demonstrates full framework capabilities

#### Example Flow - Time Analysis and Reclamation

```
User Request: "Help me understand where I am spending my time and identify ways I can reclaim time to focus more on my top priorities."

User Priorities: ["customer meetings", "product strategy", "team development"]

CAN-04: Extract intent ✓
  → analyze time spend + generate reclamation recommendations
  → priorities: ["customer meetings", "product strategy", "team development"]

CAN-01: Retrieved 180 meetings (past 90 days) ✓
  - Completed: 165 meetings
  - Upcoming: 15 meetings
  - Total hours: 165 hours (11 hours/week average)

CAN-07: Extract metadata for all 180 meetings ✓
  - Attendee counts: Range 2-50 people
  - Durations: Range 15 min - 2 hours
  - Recurrence: 60 recurring, 120 ad-hoc

CAN-02: Classify meeting types ✓
  - 1:1s: 50 meetings (30 hours total, 18%)
  - Team syncs: 40 meetings (20 hours, 12%)
  - Customer meetings: 25 meetings (40 hours, 24%)
  - Planning sessions: 15 meetings (30 hours, 18%)
  - Admin meetings: 30 meetings (25 hours, 15%)
  - Other: 20 meetings (20 hours, 12%)

CAN-03: Assess importance ✓
  - High-value: 40 meetings (70 hours, 42%)
  - Medium-value: 70 meetings (60 hours, 36%)
  - Low-value: 70 meetings (35 hours, 22%) ← Reclaim targets!

CAN-10: Aggregate time statistics ✓
  By Type:
  - Customer meetings: 40 hrs (24%) ✅ Aligns with priority!
  - Planning: 30 hrs (18%)
  - 1:1s: 30 hrs (18%)
  - Admin: 25 hrs (15%) ❌ LOW VALUE!
  - Team syncs: 20 hrs (12%)
  - Other: 20 hrs (12%)
  
  By Priority Alignment:
  - Aligned with priorities: 70 hrs (42%)
  - Necessary but not priorities: 60 hrs (36%)
  - NOT aligned (reclaim candidates): 35 hrs (22%)

CAN-11: Priority matching analysis ✓
  ✅ Customer meetings (40 hrs) - STRONG alignment
  ⚠️ Product strategy (only 15 hrs) - WEAK alignment despite being priority!
  ⚠️ Team development (30 hrs in 1:1s) - MODERATE alignment
  ❌ Admin meetings (25 hrs) - NO alignment, reclaim target!

CAN-14: Generate reclamation recommendations ✓
  1. **Decline "Weekly Admin Review" (recurring)** → Reclaim 8 hrs/month (96 hrs/year)
     Rationale: Low-value, can get updates via email
  
  2. **Shorten daily standup from 30→15 min** → Reclaim 5 hrs/month (60 hrs/year)
     Rationale: Team sync often runs over, strict timeboxing
  
  3. **Delegate 2 recurring 1:1s** → Reclaim 4 hrs/month (48 hrs/year)
     Rationale: Senior team members ready for skip-level
  
  4. **Consolidate monthly planning** → Reclaim 3 hrs/month (36 hrs/year)
     Rationale: Three separate meetings could be one
  
  Total potential reclamation: 20 hrs/month (240 hrs/year!)

CAN-20: Create visual dashboard ✓
  → Pie chart: Shows 15% in admin (LOW VALUE)
  → Bar chart: Hours/week trending up over 12 weeks
  → Priority gauge: 42% aligned, 58% misaligned
  → Heatmap: Heavy load Tue-Thu afternoons

OUTPUT to User:

📊 **WHERE YOU SPEND YOUR TIME** (Past 90 days, 165 hours total):
- Customer meetings: 40 hrs (24%) ✅ ALIGNED
- Planning: 30 hrs (18%)
- 1:1s: 30 hrs (18%)
- Admin: 25 hrs (15%) ❌ LOW VALUE
- Team syncs: 20 hrs (12%)
- Other: 20 hrs (12%)

📈 **PRIORITY ALIGNMENT**:
- ✅ Strong: Customer meetings (24%, top priority)
- ⚠️ **GAP**: Product strategy (9% of time, but top priority!)
- ⚠️ Moderate: Team development (18% in 1:1s)
- ❌ **MISALIGNMENT**: 22% in low-value admin/other

💡 **TIME RECLAMATION** (Ranked by impact):
1. Decline "Weekly Admin Review" → 96 hrs/year
2. Shorten daily standup → 60 hrs/year
3. Delegate 2 recurring 1:1s → 48 hrs/year
4. Consolidate monthly planning → 36 hrs/year

**TOTAL: 240 hours/year (6 full work weeks!)**

🎯 **RECOMMENDATION**: Use reclaimed time for product strategy (currently only 15 hrs vs 40 hrs in customer meetings). Gap analysis shows strategy is stated priority but under-represented.

[Visual Dashboard: pie charts, trend lines, priority alignment gauges]
```

---

### Hero Prompt 4: Schedule-1

**Prompt**: "Starting next week, I want a weekly 30-min 1:1 with {name}. Afternoons preferred, avoid Fridays. Automatically reschedule on declines or conflicts."

**Category**: Schedule  
**Capabilities Required**: Recurring meeting setup, constraint satisfaction, availability checking, automatic rescheduling  
**Gold Standard F1**: 100%  
**Evaluation**: ✅ **Correct**

#### Canonical Task Decomposition: 9 Tasks

**Task 1: Natural Language Understanding (CAN-04)**
- **Purpose**: Extract scheduling constraints and preferences
- **Input**: User prompt text
- **Output**: {"duration": 30, "recurrence": "weekly", "attendee": "{name}", "preferences": ["afternoon", "avoid_friday"], "automation": "auto_reschedule"}
- **Tier**: Universal (Tier 1)

**Task 2: Attendee/Contact Resolution (CAN-05)**
- **Purpose**: Resolve "{name}" to directory entry
- **Input**: Attendee name from CAN-04
- **Output**: Full contact details (email, title, calendar access)
- **Tier**: Universal (Tier 1)
- **Note**: Must happen BEFORE availability checking

**Task 3: Calendar Events Retrieval (CAN-01)**
- **Purpose**: Retrieve existing calendar events to check for conflicts
- **Input**: Time range (next week + recurring future)
- **Output**: Existing meeting schedule
- **Tier**: Universal (Tier 1)

**Task 4: Availability Checking (CAN-06)**
- **Purpose**: Find available afternoon slots (avoiding Fridays)
- **Input**: Resolved attendee + constraints from CAN-04
- **Output**: List of available time slots matching preferences
- **Tier**: Common (Tier 2)
- **Dependencies**: CAN-05 (need attendee), CAN-01 (need existing schedule)

**Task 5: Constraint Satisfaction (CAN-12)**
- **Purpose**: Select optimal time slot satisfying all constraints
- **Input**: Available slots + preferences (afternoon, not Friday)
- **Output**: Best time slot (e.g., "Mondays 2pm")
- **Tier**: Common (Tier 2)

**Task 6: Recurrence Rule Generation (CAN-15)**
- **Purpose**: Generate RRULE for weekly recurrence
- **Input**: Selected time slot + "weekly" recurrence
- **Output**: RRULE pattern (e.g., "FREQ=WEEKLY;BYDAY=MO")
- **Tier**: Specialized (Tier 3)

**Task 7: Calendar Event Creation/Update (CAN-03)**
- **Purpose**: Create recurring meeting on calendar
- **Input**: Time slot + recurrence rule + attendee
- **Output**: Calendar event created with recurrence
- **Tier**: Universal (Tier 1)

**Task 8: Event Monitoring/Change Detection (CAN-16)**
- **Purpose**: Setup monitoring for declines and conflicts
- **Input**: Created recurring meeting
- **Output**: Webhook/monitoring configuration
- **Tier**: Specialized (Tier 3)
- **Note**: Enables automatic rescheduling trigger

**Task 9: Automatic Rescheduling (CAN-17)**
- **Purpose**: Automatically reschedule on declines/conflicts
- **Input**: Monitoring events from CAN-16
- **Output**: Rescheduling workflow triggered on decline/conflict
- **Tier**: Specialized (Tier 3)
- **Dependencies**: CAN-16 (monitoring must be active)

#### Evaluation Criteria
- Constraint satisfaction accuracy (afternoon preference, avoid Friday correctly applied)
- Recurrence rule correctness (weekly RRULE properly formatted)
- Automation setup completeness (monitoring + auto-reschedule fully configured)
- Attendee resolution accuracy (correct person identified and scheduled)
- Conflict detection reliability (overlaps detected before scheduling)

#### Execution Composition

**How Tasks Work Together to Answer the Prompt:**

```
STEP 1: Understand Scheduling Requirements
CAN-04 (NLU) → Extract scheduling constraints and automation preferences
  - Parse: "Starting next week" = start_date constraint
  - Parse: "weekly 30-min 1:1" = recurrence pattern + duration
  - Parse: "with {name}" = attendee requirement
  - Parse: "Afternoons preferred, avoid Fridays" = soft + hard time constraints
  - Parse: "Automatically reschedule" = automation requirement
  - Output: Comprehensive scheduling parameters

STEP 2: Resolve Attendee Identity
CAN-05 (Attendee Resolution) → Look up "{name}" in directory
  - Search: Organization directory, contact list, recent collaborators
  - Match: Resolve to full contact details (email, calendar URL, timezone)
  - Validate: Confirm calendar access available
  - Output: Full attendee object with calendar permissions

STEP 3: Retrieve Existing Calendar State
CAN-01 (Calendar Retrieval) → Load current calendar events
  - Time range: "Next week" + recurring future (52 weeks for recurrence)
  - Purpose: Detect conflicts before scheduling
  - Include: User's calendar + attendee's calendar
  - Output: Complete calendar dataset for both parties

STEP 4: Check Attendee Availability
CAN-06 (Availability Checking) → Find afternoon slots avoiding Friday
  - Analyze: User + attendee calendars for free/busy times
  - Filter: Only afternoon slots (e.g., 12pm-5pm)
  - Exclude: All Friday slots (hard constraint)
  - Week-by-week: Check recurring availability pattern
  - Output: Available afternoon slots ["Mon 2pm", "Tue 3pm", "Wed 2pm", "Thu 4pm"]

STEP 5: Select Optimal Time Slot
CAN-12 (Constraint Satisfaction) → Apply preferences to select best time
  - Hard constraints: Must be afternoon, must not be Friday
  - Soft preferences: Earlier in week better (more prep time)
  - Recurring feasibility: Select slot available most weeks (minimize conflicts)
  - Output: Optimal time selection (e.g., "Mondays 2:00 PM")

STEP 6: Generate Recurrence Rule
CAN-15 (Recurrence Rule Generation) → Create weekly RRULE pattern
  - Frequency: WEEKLY
  - Day: BYDAY=MO (if Monday selected)
  - Start: DTSTART = next Monday at 2pm
  - No end date: Ongoing recurrence
  - Output: RRULE string "FREQ=WEEKLY;BYDAY=MO;DTSTART=20250113T140000Z"

STEP 7: Create Recurring Meeting
CAN-03 (Event Creation) → Schedule meeting on both calendars
  - Create: Calendar event with recurrence pattern
  - Invite: Send meeting invitation to attendee
  - Subject: "1:1 with {name}" (auto-generated)
  - Attributes: Duration 30 min, recurring weekly
  - Output: Calendar event ID (for monitoring)

STEP 8: Setup Change Monitoring
CAN-16 (Event Monitoring) → Configure webhooks for meeting changes
  - Monitor: Decline responses from attendee
  - Monitor: Schedule conflicts (new meetings overlapping)
  - Monitor: Calendar changes (attendee moves/cancels)
  - Trigger: Webhook fires on any of these events
  - Output: Monitoring service active, event ID registered

STEP 9: Enable Automatic Rescheduling
CAN-17 (Auto-Reschedule) → Configure rescheduling workflow
  - On decline: Trigger CAN-06 → CAN-12 → CAN-03 (find/select/update)
  - On conflict: Same rescheduling workflow
  - Notification: Send rescheduling confirmation to both parties
  - Retry logic: If no slots available, notify user for manual intervention
  - Output: Automation workflow active, linked to CAN-16 webhooks

OUTPUT: Fully automated recurring meeting system
  1. Weekly 1:1 scheduled (Mondays 2pm, starting next week)
  2. Attendee invited and confirmed
  3. Monitoring active for declines/conflicts
  4. Automatic rescheduling enabled (hands-free maintenance)
```

#### Key Orchestration Patterns
- **Sequential Dependency Chain**: CAN-05 → CAN-06 (must resolve attendee before checking their availability)
- **Recurrence Pipeline**: CAN-12 (select time) → CAN-15 (generate RRULE) → CAN-03 (create recurring event)
- **Automation Layer**: CAN-16 (monitoring) → CAN-17 (auto-reschedule) - real-time reactive workflow
- **Constraint Filtering**: CAN-06 applies hard constraints (afternoon, not Friday), CAN-12 applies soft preferences
- **Event-Driven Architecture**: CAN-17 subscribes to CAN-16 events for automatic execution
- **Most Specialized Prompt**: Uses 3 Tier-3 tasks (CAN-15, CAN-16, CAN-17) - demonstrates advanced capabilities

#### Example Flow - Recurring 1:1 with Automated Rescheduling

```
User Request: "Starting next week, I want a weekly 30-min 1:1 with Sarah Chen. Afternoons preferred, avoid Fridays. Automatically reschedule on declines or conflicts."

CAN-04: Extract scheduling requirements ✓
  → duration: 30 min, recurrence: weekly, attendee: "Sarah Chen"
  → preferences: afternoon, avoid Friday
  → automation: auto-reschedule enabled

CAN-05: Resolve attendee ✓
  → Found: Sarah Chen (sarah.chen@company.com)
  → Title: Product Manager, Calendar access: ✓ Available, Timezone: PST

CAN-01: Retrieve calendars ✓
  User calendar: 42 meetings next 4 weeks
  Sarah's calendar: 38 meetings next 4 weeks
  Overlap conflicts: 12 shared time blocks

CAN-06: Check afternoon availability (avoiding Friday) ✓
  Week 1 options:
  - Mon 2-3pm ✅ Both free
  - Mon 3-4pm ✅ Both free
  - Tue 2-3pm ❌ User has meeting
  - Wed 3-4pm ✅ Both free
  - Thu 4-5pm ❌ Sarah has meeting
  - Fri 2-5pm 🚫 EXCLUDED (hard constraint)

CAN-12: Select optimal time ✓
  Candidates: Mon 2pm, Mon 3pm, Wed 3pm
  Selected: **Monday 2:00 PM** (earliest in week, consistent slot)
  Rationale: Monday provides most prep time for weekly sync

CAN-15: Generate recurrence rule ✓
  RRULE: FREQ=WEEKLY;BYDAY=MO;DTSTART=20250113T140000Z
  First occurrence: January 13, 2025 at 2:00 PM PST
  Recurring: Every Monday indefinitely

CAN-03: Create recurring meeting ✓
  Event created: "1:1 with Sarah Chen"
  Duration: 30 minutes (2:00-2:30 PM), Recurrence: Weekly on Mondays
  Attendees: User + Sarah Chen, Invitation sent: ✓

CAN-16: Setup monitoring ✓
  Webhooks configured:
  - Decline event: If Sarah declines any instance
  - Conflict event: If new meeting overlaps 1:1 time
  - Change event: If Sarah moves/cancels
  Event ID tracked: cal_evt_12345, Monitoring status: 🟢 Active

CAN-17: Enable auto-rescheduling ✓
  Rescheduling workflow:
  1. Webhook triggers on decline/conflict
  2. Auto-run CAN-06 to find alternative afternoon slots (not Friday)
  3. Auto-run CAN-12 to select best alternative
  4. Auto-run CAN-03 to update meeting time
  5. Send notification: "Your 1:1 with Sarah has been automatically rescheduled to..."
  Fallback: If no slots available, notify user for manual handling
  Automation status: 🟢 Active

OUTPUT to User:

✅ **RECURRING 1:1 SCHEDULED**:
- **Meeting**: 1:1 with Sarah Chen
- **Schedule**: Every Monday, 2:00-2:30 PM PST
- **First occurrence**: January 13, 2025

✅ **AUTOMATION CONFIGURED**:
- **Monitoring**: Active for declines and conflicts
- **Auto-Rescheduling**: Enabled
  - If Sarah declines: System will automatically find new afternoon time (not Friday)
  - If conflict detected: System will automatically reschedule
  - Notifications: Both parties notified of any rescheduling

---

SCENARIO: Sarah Declines First Instance (Automation in Action)

3 days later: Sarah declines January 13 meeting

CAN-16: Detect decline event ✓
  → Webhook fired: sarah.chen@company.com declined cal_evt_12345_instance_1

CAN-17: Trigger auto-reschedule ✓
  → Re-run CAN-06: Find afternoon slots week of Jan 13 (not Friday)
  → Available: Tue Jan 14 3pm, Wed Jan 15 2pm
  → Re-run CAN-12: Select Wed Jan 15 2pm (better than Tue)
  → Re-run CAN-03: Update meeting to Wed Jan 15, 2:00 PM
  → Send notification to user and Sarah

Notification: "Your 1:1 with Sarah Chen has been automatically rescheduled from Monday, Jan 13 at 2pm to Wednesday, Jan 15 at 2pm. Future occurrences remain on Mondays at 2pm."

**Key Insight**: CAN-17 (Automatic Rescheduling) creates a "self-healing" calendar - user never has to manually handle declines or conflicts. This is a sophisticated workflow requiring CAN-16 monitoring + full rescheduling pipeline (CAN-06 + CAN-12 + CAN-03) to execute automatically.
```

---

### Hero Prompt 5: Schedule-2

**Prompt**: "Clear my Thursday afternoon. Update my RSVPs and help me reschedule my meetings to another time and show me as {status}."

**Category**: Schedule  
**Capabilities Required**: Meeting rescheduling, RSVP management, availability checking, constraint satisfaction  
**Gold Standard F1**: 88.89%  
**Evaluation**: ⚠️ **Partial** - Missing CAN-06 (Availability Checking)

**Gold Standard Revision (November 8, 2025)**: 
> Changed CAN-23 (Conflict Resolution) to CAN-17 (Automatic Rescheduling). When prompt explicitly requests "help me reschedule", the automatic rescheduling task (CAN-17) is more appropriate than conflict resolution (CAN-23). CAN-17 actively performs the rescheduling automation, while CAN-23 would only detect conflicts.
> 
> **CAN-05 Removal (November 8, 2025)**: Removed CAN-05 (Attendee Resolution) from Schedule-2. Since meetings are already booked on the calendar, attendee information is available directly from CAN-07 (Meeting Metadata Extraction). CAN-05 is only needed when resolving names to calendar identities (e.g., "{name}" in Schedule-1), not when extracting attendees from existing meetings.

#### Canonical Task Decomposition: 8 Tasks (Removed CAN-05)

**Task 1: Natural Language Understanding (CAN-04)**
- **Purpose**: Extract rescheduling requirements
- **Input**: User prompt text
- **Output**: {"time_to_clear": "Thursday afternoon", "actions": ["update_rsvp", "reschedule", "set_status"], "status": "{status}"}
- **Tier**: Universal (Tier 1)

**Task 2: Calendar Events Retrieval (CAN-01)**
- **Purpose**: Retrieve Thursday afternoon meetings
- **Input**: Time range (Thursday afternoon)
- **Output**: List of meetings to be moved
- **Tier**: Universal (Tier 1)

**Task 3: Meeting Metadata Extraction (CAN-07)**
- **Purpose**: Extract RSVP status, attendees, meeting details
- **Input**: Thursday afternoon meetings from CAN-01
- **Output**: Detailed metadata including attendee information for rescheduling
- **Tier**: Common (Tier 2)
- **Note**: Provides all attendee information needed for CAN-06 (availability checking) and CAN-13 (RSVP updates)

**Task 4: RSVP Status Update (CAN-13)**
- **Purpose**: Update RSVP status (decline or tentative)
- **Input**: Meetings from CAN-07 + user status preference
- **Output**: RSVP updates sent
- **Tier**: Common (Tier 2)
- **Dependencies**: CAN-07 (need current RSVP status)

**Task 5: Availability Checking (CAN-06) - **MISSING IN ORIGINAL****
- **Purpose**: Find alternative time slots for rescheduling
- **Input**: Meeting attendees from CAN-07 + duration
- **Output**: Available slots for rescheduled meetings
- **Tier**: Common (Tier 2)
- **Dependencies**: CAN-07 (attendee information comes from metadata extraction)

**Task 6: Constraint Satisfaction (CAN-12)**
- **Purpose**: Select best alternative times for each meeting
- **Input**: Available slots + user preferences
- **Output**: Optimal rescheduling times
- **Tier**: Common (Tier 2)

**Task 7: Automatic Rescheduling (CAN-17) - **REVISED FROM CAN-23****
- **Purpose**: Automatically propose and execute rescheduling
- **Input**: Original meetings + new proposed times from CAN-12
- **Output**: Rescheduling proposal with automated time suggestions
- **Tier**: Specialized (Tier 3)
- **Note**: User explicitly requested "help me reschedule" - CAN-17 performs the automation action

**Task 8: Calendar Event Creation/Update (CAN-03)**
- **Purpose**: Update meeting times in calendar
- **Input**: Rescheduling plan from CAN-17
- **Output**: Calendar events updated to new times
- **Tier**: Universal (Tier 1)

#### Evaluation Criteria
- RSVP update correctness (status correctly updated to decline/tentative)
- Availability detection accuracy (suitable alternative slots found)
- Rescheduling plan quality (proposed times work for all attendees)
- CAN-06 inclusion (CRITICAL - human evaluator identified availability checking as missing)

#### Execution Composition

**How Tasks Work Together to Answer the Prompt:**

```
STEP 1: Understand Rescheduling Requirements
CAN-04 (NLU) → Parse multi-action request
  - Parse: "Clear my Thursday afternoon" = time block to free up
  - Parse: "Update my RSVPs" = change response status
  - Parse: "reschedule my meetings to another time" = find alternative slots
  - Parse: "show me as {status}" = set calendar status display
  - Output: Comprehensive rescheduling parameters

STEP 2: Retrieve Thursday Afternoon Meetings
CAN-01 (Calendar Retrieval) → Load meetings in target time block
  - Time range: Thursday 12:00 PM - 5:00 PM (afternoon definition)
  - Filter: Meetings where user is attendee
  - Include: RSVP status, attendees, organizer, duration
  - Output: List of meetings to be cleared (e.g., 4 meetings)

STEP 3: Extract Meeting Metadata
CAN-07 (Metadata Extraction) → Get detailed meeting information
  - For each meeting: Attendee lists, organizer, duration, recurrence, RSVP status
  - Extract: Meeting importance signals (customer meeting? 1:1?)
  - Extract: Flexibility indicators (recurring? organizer is peer?)
  - Extract: Attendee information (names, emails) for availability checking
  - Purpose: Provide context for CAN-13 (RSVP) and CAN-06 (availability)
  - Output: Enriched meeting objects with full metadata including attendee details

STEP 4-5: Update RSVPs and Find Alternative Slots (Parallel Processing)
CAN-13 (RSVP Status Update) → Decline or mark tentative
  - For each Thursday meeting: Update user's RSVP to "Declined" or "Tentative"
  - Send: RSVP update notifications to organizers
  - Purpose: Immediately free up Thursday afternoon slot
  - Output: RSVP updates sent for all meetings

CAN-06 (Availability Checking) → Find alternative times for rescheduling
  - Input: Attendee information from CAN-07 + meeting durations
  - For each meeting: Check common availability across all attendees
  - Constraints: Avoid Thursday afternoon, find slots within next 1-2 weeks
  - Output: List of alternative time slots for each meeting

STEP 6: Select Best Alternative Times
CAN-12 (Constraint Satisfaction) → Apply preferences
  - Preferences: Minimize attendee conflicts, respect calendar patterns
  - Logic: Earlier in week better, group similar meetings together
  - Validation: Ensure selected times don't conflict
  - Output: Optimal rescheduling plan

STEP 7: Generate Rescheduling Proposal with Automation
CAN-17 (Automatic Rescheduling) → Create rescheduling plan
  - Format: Structured proposal showing old time → new time
  - Include: Rationale for each change (attendee availability)
  - Include: Automated time suggestions based on CAN-12 constraints
  - Purpose: Provide automation action requested by "help me reschedule"
  - Output: Rescheduling proposal with automated suggestions

STEP 8: Update Calendar with New Times
CAN-03 (Event Creation/Update) → Execute rescheduling
  - For each meeting: Update meeting time to new slot
  - Send: Meeting update notifications to all attendees
  - Update: User's calendar status to {status} for Thursday afternoon
  - Output: Calendar events updated, Thursday afternoon now clear

OUTPUT: Thursday afternoon cleared with meetings rescheduled
  1. RSVP updates sent for all Thursday meetings
  2. Alternative times proposed and scheduled
  3. User's calendar shows {status} for Thursday afternoon
  4. All attendees notified of rescheduling
```

#### Key Orchestration Patterns
- **Metadata Extraction Enabler**: CAN-07 provides critical input for both CAN-13 (RSVP) and CAN-06 (availability) - attendee information comes from existing meeting metadata
- **No Attendee Resolution Needed**: Since meetings are already booked, CAN-07 extracts attendee details directly from calendar events (unlike Schedule-1 where "{name}" must be resolved)
- **Parallel RSVP + Availability**: CAN-13 and CAN-06 can run concurrently after CAN-07 completes
- **Automation Layer**: CAN-17 provides automated rescheduling action requested by user
- **Multi-Action Coordination**: Single prompt triggers 3 distinct actions (RSVP update, rescheduling, status setting)
- **Critical Missing Task**: Original decomposition missed CAN-06 (Availability Checking) - human evaluator noted this was needed to find alternative times
- **Gold Standard Revision**: CAN-23 → CAN-17 to reflect explicit automation request in prompt

#### Example Flow - Clear Thursday Afternoon with Rescheduling

```
User Request: "Clear my Thursday afternoon. Update my RSVPs and help me reschedule my meetings to another time and show me as Out of Office."

CAN-04: Extract rescheduling requirements ✓
  → clear_time: "Thursday afternoon"
  → actions: ["update_rsvp", "reschedule", "set_status"]
  → status: "Out of Office"

CAN-01: Retrieve Thursday afternoon meetings ✓
  Found 4 meetings:
  - 1:00-2:00 PM: "Product Roadmap Review" (Sarah, Mike, 3 others)
  - 2:00-3:00 PM: "Customer Check-in: Acme Corp" (Jennifer, Customer team)
  - 3:00-3:30 PM: "1:1 with Manager" (Manager only)
  - 4:00-5:00 PM: "Team Sprint Planning" (12 engineering team members)

CAN-07: Extract metadata ✓
  Meeting 1: Product Roadmap Review
  - Attendees: ["Sarah Chen", "Mike Torres", "+3 others"]
  - Organizer: Sarah Chen, Duration: 60 min, Current RSVP: Accepted
  
  Meeting 2: Customer Check-in: Acme Corp
  - Attendees: ["Jennifer Kim", "Customer VP", "Account Manager"]
  - Organizer: You, Duration: 60 min, Current RSVP: Accepted
  
  Meeting 3: 1:1 with Manager
  - Attendees: ["Manager"]
  - Organizer: Manager, Duration: 30 min, Current RSVP: Accepted
  
  Meeting 4: Team Sprint Planning
  - Attendees: [12 engineering team members listed with emails]
  - Organizer: Engineering Lead, Duration: 60 min, Current RSVP: Accepted

CAN-13: Update RSVPs (Parallel with CAN-06) ✓
  Meeting 1: RSVP changed to "Declined" ✓
  Meeting 2: As organizer, marked as "Out of Office" ✓
  Meeting 3: RSVP changed to "Declined" ✓
  Meeting 4: RSVP changed to "Declined" ✓
  
  Notifications sent to all organizers

CAN-06: Find alternative time slots (Parallel with CAN-13) ✓
  **Uses attendee information from CAN-07 to check availability**
  
  Meeting 1 alternatives:
  - Mon 2-3pm ✅ Sarah, Mike, 3 others all free
  - Tue 10-11am ✅ All free
  
  Meeting 2 alternatives:
  - Tue 11am-12pm ✅ Jennifer and team free
  - Wed 2-3pm ✅ All free
  
  Meeting 3 alternatives:
  - Mon 10-10:30am ✅ Manager free
  - Tue 9-9:30am ✅ Manager free
  
  Meeting 4 alternatives:
  - Wed 10-11am ✅ All 12 team members free!
  - Fri 2-3pm ✅ 11 of 12 free

CAN-12: Select best alternative times ✓
  Meeting 1: **Tuesday 10-11am** (earliest available)
  Meeting 2: **Wednesday 2-3pm** (customer meeting, mid-week)
  Meeting 3: **Monday 10-10:30am** (start of week sync)
  Meeting 4: **Wednesday 10-11am** (all 12 attendees available!)

CAN-17: Generate rescheduling proposal ✓
  
  **THURSDAY AFTERNOON RESCHEDULING PLAN**
  
  ❌ 1:00-2:00 PM: Product Roadmap Review
  → **Reschedule to**: Tuesday, 10:00-11:00 AM
  → **Reason**: All attendees available, earlier in week
  
  ❌ 2:00-3:00 PM: Customer Check-in: Acme Corp
  → **Reschedule to**: Wednesday, 2:00-3:00 PM
  → **Reason**: Customer meeting, mid-week preferred
  
  ❌ 3:00-3:30 PM: 1:1 with Manager
  → **Reschedule to**: Monday, 10:00-10:30 AM
  → **Reason**: Start of week check-in
  
  ❌ 4:00-5:00 PM: Team Sprint Planning
  → **Reschedule to**: Wednesday, 10:00-11:00 AM
  → **Reason**: Only slot with all 12 attendees available!

CAN-03: Update calendar with new times ✓
  Meeting 1: Updated to Tue 10am ✓ (Notifications sent to 5 attendees)
  Meeting 2: Updated to Wed 2pm ✓ (Notifications sent to Customer team)
  Meeting 3: Updated to Mon 10am ✓ (Notification sent to manager)
  Meeting 4: Updated to Wed 10am ✓ (Notifications sent to 12 team members)
  
  Thursday afternoon: Marked as "Out of Office" ✓

OUTPUT to User:

✅ **THURSDAY AFTERNOON CLEARED**

**Meetings Rescheduled** (4 meetings moved):

1. **Product Roadmap Review**
   - Was: Thursday 1-2 PM → Now: **Tuesday 10-11 AM** ✅

2. **Customer Check-in: Acme Corp**
   - Was: Thursday 2-3 PM → Now: **Wednesday 2-3 PM** ✅

3. **1:1 with Manager**
   - Was: Thursday 3-3:30 PM → Now: **Monday 10-10:30 AM** ✅

4. **Team Sprint Planning**
   - Was: Thursday 4-5 PM → Now: **Wednesday 10-11 AM** ✅

**Status**: Your calendar now shows "Out of Office" for Thursday afternoon
**Notifications**: All attendees notified of rescheduling

**Key Insight**: Schedule-2 demonstrates that CAN-05 (Attendee Resolution) is NOT needed when working with existing calendar meetings. Since meetings are already booked, CAN-07 (Meeting Metadata Extraction) provides complete attendee information directly from the calendar events. CAN-05 is only required when resolving names to identities (like "{name}" in Schedule-1 or "senior leadership" in Collaborate-2).
```

---

### Hero Prompt 6: Schedule-3

**Prompt**: "Land a time to meet about Project Alpha with Chris, Sangya, and Kat for 1 hour in the next 2 weeks. Schedule over 1:1s and lunches if needed and work around Kat's schedule. Make the meeting in person and add a room."

**Category**: Schedule  
**Capabilities Required**: Multi-person scheduling, constraint satisfaction, resource booking, priority-based conflict resolution  
**Gold Standard F1**: 100%  
**Evaluation**: ✅ **Correct**

#### Canonical Task Decomposition: 10 Tasks

**Task 1: Natural Language Understanding (CAN-04)**
- **Purpose**: Extract complex scheduling constraints
- **Input**: User prompt text
- **Output**: {"attendees": ["Chris", "Sangya", "Kat"], "duration": 60, "timeframe": "next 2 weeks", "priority_constraints": ["work around Kat", "override 1:1s and lunches"], "location": "in_person", "resources": ["room"]}
- **Tier**: Universal (Tier 1)

**Task 2: Attendee/Contact Resolution (CAN-05)**
- **Purpose**: Resolve Chris, Sangya, Kat to directory entries
- **Input**: Attendee names from CAN-04
- **Output**: Full contact details for all 3 attendees
- **Tier**: Universal (Tier 1)

**Task 3: Calendar Events Retrieval (CAN-01)**
- **Purpose**: Retrieve calendars for all attendees (next 2 weeks)
- **Input**: Resolved attendees + timeframe
- **Output**: All calendar events for Chris, Sangya, Kat
- **Tier**: Universal (Tier 1)

**Task 4: Meeting Metadata Extraction (CAN-07)**
- **Purpose**: Extract meeting types from existing events
- **Input**: Calendar events from CAN-01
- **Output**: Meeting details (type, importance, flexibility)
- **Tier**: Common (Tier 2)

**Task 5: Meeting Type Classification (CAN-02)**
- **Purpose**: Classify existing meetings (identify 1:1s and lunches)
- **Input**: Meeting metadata from CAN-07
- **Output**: Meeting type classifications
- **Tier**: Universal (Tier 1)
- **Note**: Needed to identify "schedulable over" meetings (1:1s, lunches)

**Task 6: Meeting Importance Assessment (CAN-03)**
- **Purpose**: Assess which meetings can be overridden
- **Input**: Classified meetings from CAN-02
- **Output**: Importance scores (1:1s and lunches = lower priority)
- **Tier**: Universal (Tier 1)

**Task 7: Availability Checking (CAN-06)**
- **Purpose**: Find common available slots (or overridable slots)
- **Input**: All 3 calendars + "work around Kat" constraint
- **Output**: Available time slots (pure availability + overridable slots)
- **Tier**: Common (Tier 2)
- **Note**: Must respect Kat's schedule (hard constraint)

**Task 8: Constraint Satisfaction (CAN-12)**
- **Purpose**: Select best time satisfying all constraints
- **Input**: Available slots + priority constraints
- **Output**: Optimal time slot
- **Tier**: Common (Tier 2)
- **Note**: Complex constraint logic (hard + soft constraints)

**Task 9: Resource Booking (CAN-19)**
- **Purpose**: Book in-person meeting room
- **Input**: Selected time slot + attendee count (3 people)
- **Output**: Room reservation
- **Tier**: Specialized (Tier 3)

**Task 10: Calendar Event Creation/Update (CAN-03)**
- **Purpose**: Create Project Alpha meeting
- **Input**: Time slot + attendees + room
- **Output**: Calendar event created (may override 1:1s/lunches)
- **Tier**: Universal (Tier 1)

#### Evaluation Criteria
- Priority constraint enforcement ("work around Kat" correctly applied as hard constraint)
- Override logic correctness (1:1s and lunches correctly identified as overridable)
- Multi-attendee availability accuracy (common slots correctly identified for 3 people)
- Resource booking success (meeting room reserved for in-person requirement)
- Complex constraint satisfaction (hard + soft constraints balanced appropriately)

#### Execution Composition

**How Tasks Work Together to Answer the Prompt:**

```
STEP 1: Understand Complex Scheduling Constraints
CAN-04 (NLU) → Parse multi-layered requirements
  - Parse: "land a time to meet about Project Alpha" = scheduling intent
  - Parse: "with Chris, Sangya, and Kat" = 3 required attendees
  - Parse: "for 1 hour in the next 2 weeks" = duration + timeframe
  - Parse: "Schedule over 1:1s and lunches if needed" = SOFT constraint (override permission)
  - Parse: "work around Kat's schedule" = HARD constraint (Kat has priority)
  - Parse: "Make the meeting in person and add a room" = location + resource requirements
  - Output: Comprehensive constraint specification

STEP 2: Resolve All Attendees
CAN-05 (Attendee/Contact Resolution) → Look up Chris, Sangya, and Kat
  - Search: Organization directory for all 3 names
  - Resolve: Full contact details (emails, calendar URLs, timezones, office locations)
  - Validate: Confirm calendar access for all 3 attendees
  - Output: 3 fully resolved attendee objects with calendar permissions

STEP 3: Retrieve All 3 Calendars
CAN-01 (Calendar Retrieval) → Load calendar events for next 2 weeks
  - For Chris: Retrieve all events (next 14 days)
  - For Sangya: Retrieve all events (next 14 days)
  - For Kat: Retrieve all events (next 14 days) - PRIORITY SCHEDULE
  - Include: Event types, attendees, importance, flexibility indicators
  - Output: Complete calendar dataset for 3 people (e.g., 120 total events)

STEP 4: Extract Meeting Metadata
CAN-07 (Metadata Extraction) → Get detailed meeting information
  - For each event: Extract attendees, duration, organizer, meeting type signals
  - Purpose: Identify which meetings are 1:1s or lunches (potentially overridable)
  - Extract: Importance signals (customer meeting? team event?)
  - Output: Enriched meeting objects with classification context

STEP 5-6: Classify and Assess Meetings (Parallel Processing)
CAN-02 (Meeting Type Classification) → Categorize existing meetings
  - Identify: 1:1 meetings (2 attendees)
  - Identify: Lunch meetings (keywords: "lunch", duration 30-60 min, time 11am-2pm)
  - Identify: Other meeting types (team sync, customer, planning, etc.)
  - Purpose: Know which meetings can be overridden per soft constraint
  - Output: Type classifications for all 120 events

CAN-03 (Importance Assessment) → Score meeting priority
  - High priority: Customer meetings, board meetings (CANNOT override)
  - Medium priority: Team syncs, planning sessions
  - Low priority: 1:1s and lunches (OVERRIDABLE per prompt)
  - Kat's meetings: Importance scores determine hard constraint enforcement
  - Output: Importance scores for filtering overridable slots

STEP 7: Check Availability with Priority Logic
CAN-06 (Availability Checking) → Find common available slots
  - Phase 1: Pure availability - Find slots where all 3 are free
  - Phase 2: Overridable availability - Find slots where all 3 have only 1:1s or lunches
  - Hard constraint: NEVER override Kat's meetings
  - Soft constraint: CAN override Chris's and Sangya's 1:1s/lunches if needed
  - Output: List of available time slots (pure + overridable, sorted)

STEP 8: Select Optimal Time Slot
CAN-12 (Constraint Satisfaction) → Apply complex constraint logic
  - Preference 1: Pure availability (no conflicts) - BEST OPTION
  - Preference 2: Override Chris's or Sangya's 1:1/lunch - ACCEPTABLE
  - HARD RULE: Never override Kat's meetings (even if 1:1 or lunch)
  - Tiebreaker: Earlier in 2-week window better, mid-week better
  - Output: Optimal time slot selected (e.g., "Wednesday 2pm")

STEP 9-10: Book Resources and Create Meeting (Parallel Processing)
CAN-19 (Resource Booking) → Reserve meeting room
  - Requirements: In-person meeting room for 3 people + 1 hour
  - Check: Room availability at selected time slot
  - Preferences: Conference room near attendees' offices
  - Output: Room reservation (e.g., "Conference Room B, 3rd floor")

CAN-03 (Event Creation/Update) → Schedule Project Alpha meeting
  - Create: Calendar event for selected time
  - Invite: Chris, Sangya, Kat
  - Location: Reserved conference room
  - Subject: "Project Alpha Discussion", Duration: 60 minutes
  - Note: May override Chris's or Sangya's 1:1/lunch (not Kat's!)
  - Output: Calendar event created, invitations sent

OUTPUT: Project Alpha meeting scheduled with constraints satisfied
  1. Time found within next 2 weeks
  2. All 3 attendees invited
  3. Kat's schedule fully respected (hard constraint)
  4. Chris's or Sangya's 1:1/lunch may be overridden (soft constraint)
  5. In-person meeting room reserved
```

#### Key Orchestration Patterns
- **Dual-Phase Availability Checking**: CAN-06 runs twice (pure availability + overridable availability)
- **Priority-Based Filtering**: CAN-03 (importance) determines which meetings can be overridden
- **Hard vs Soft Constraints**: CAN-12 enforces Kat priority (hard) while allowing 1:1/lunch override (soft)
- **Parallel Classification**: CAN-02 + CAN-03 process same events concurrently
- **Parallel Finalization**: CAN-19 (room booking) + CAN-03 (event creation) are independent operations
- **Most Complex Scheduling**: Uses 10 tasks with multi-layered constraint logic - demonstrates sophisticated conflict resolution

#### Example Flow - Multi-Person Scheduling with Override Logic

```
User Request: "Land a time to meet about Project Alpha with Chris, Sangya, and Kat for 1 hour in the next 2 weeks. Schedule over 1:1s and lunches if needed and work around Kat's schedule. Make the meeting in person and add a room."

CAN-04: Extract scheduling requirements ✓
  → topic: "Project Alpha", attendees: ["Chris", "Sangya", "Kat"]
  → duration: 60 minutes, timeframe: next 2 weeks
  → hard constraint: "work around Kat", soft constraint: "override 1:1s and lunches if needed"
  → location: "in_person", resources: ["room"]

CAN-05: Resolve attendees ✓
  - Chris Martinez → chris.martinez@company.com (calendar access ✓)
  - Sangya Patel → sangya.patel@company.com (calendar access ✓)
  - Kat Williams → kat.williams@company.com (calendar access ✓, PRIORITY)

CAN-01: Retrieve calendars (next 2 weeks) ✓
  Chris's calendar: 38 meetings
  Sangya's calendar: 42 meetings
  Kat's calendar: 35 meetings (PRIORITY - work around this!)
  Total events: 115 meetings

CAN-07: Extract metadata ✓
  - Meeting types identified: 1:1s, lunches, team syncs, customer meetings
  - Attendee counts: Range 2-20 people, Durations: Range 15 min - 2 hours

CAN-02: Classify meeting types (Parallel with CAN-03) ✓
  Chris's meetings: 12 1:1s (OVERRIDABLE), 4 lunches (OVERRIDABLE), 22 other
  Sangya's meetings: 15 1:1s (OVERRIDABLE), 5 lunches (OVERRIDABLE), 22 other
  Kat's meetings: 10 1:1s (NOT OVERRIDABLE), 3 lunches (NOT OVERRIDABLE), 22 other

CAN-03: Assess importance (Parallel with CAN-02) ✓
  High priority (CANNOT override):
  - All customer meetings (23 total)
  - All team syncs (34 total)
  - ALL of Kat's meetings (35 total - hard constraint!)
  
  Low priority (CAN override per soft constraint):
  - Chris's 1:1s and lunches (16 meetings)
  - Sangya's 1:1s and lunches (20 meetings)
  - Kat's 1:1s and lunches: CANNOT OVERRIDE due to hard constraint!

CAN-06: Check availability (dual-phase) ✓
  
  **Phase 1: Pure Availability**
  - Week 1: ❌ No common free slots
  - Week 2: ✅ Found 2 slots!
    - Wednesday Week 2, 2:00-3:00 PM ✅ ALL FREE
    - Friday Week 2, 10:00-11:00 AM ✅ ALL FREE
  
  **Phase 2: Overridable Availability**
  - Tuesday Week 1, 3:00-4:00 PM ✅ Chris has 1:1 (overridable), Sangya free, Kat free
  - Thursday Week 1, 12:00-1:00 PM ✅ Sangya has lunch (overridable), Chris free, Kat free
  - Monday Week 2, 11:00-12:00 PM ✅ Chris has 1:1 (overridable), Sangya free, Kat free
  
  **Rejected Slots** (violate hard constraint):
  - Monday Week 1, 2:00-3:00 PM ❌ Kat has 1:1 (CANNOT OVERRIDE)
  - Wednesday Week 1, 12:00-1:00 PM ❌ Kat has lunch (CANNOT OVERRIDE)
  
  Total available slots: 5 (2 pure + 3 overridable)

CAN-12: Select optimal time slot ✓
  Candidates:
  1. Wednesday Week 2, 2:00-3:00 PM (pure availability, mid-week) ⭐ BEST
  2. Friday Week 2, 10:00-11:00 AM (pure availability, but Friday less ideal)
  3. Tuesday Week 1, 3:00-4:00 PM (override Chris's 1:1)
  4. Thursday Week 1, 12:00-1:00 PM (override Sangya's lunch)
  5. Monday Week 2, 11:00-12:00 PM (override Chris's 1:1)
  
  Selected: **Wednesday Week 2, 2:00-3:00 PM**
  Rationale: Pure availability (no overrides needed!), mid-week, afternoon slot

CAN-19: Book meeting room (Parallel with CAN-03) ✓
  Requirements: 3 people, 60 minutes, in-person
  Time: Wednesday Week 2, 2:00-3:00 PM
  Available rooms: Conference Room A (capacity 4) ✅, Conference Room B (capacity 8) ✅
  Selected: **Conference Room A** (right-sized for 3 people), Location: 3rd floor

CAN-03: Create calendar event ✓
  Event created: "Project Alpha Discussion"
  Time: Wednesday, January 22, 2025, 2:00-3:00 PM
  Duration: 60 minutes
  Attendees: Chris Martinez, Sangya Patel, Kat Williams
  Location: Conference Room A (3rd floor)
  Status: Invitations sent to all 3 attendees

OUTPUT to User:

✅ **PROJECT ALPHA MEETING SCHEDULED**

**Meeting Details**:
- **Time**: Wednesday, January 22, 2025, 2:00-3:00 PM
- **Duration**: 1 hour
- **Attendees**: Chris Martinez, Sangya Patel, Kat Williams
- **Location**: Conference Room A (3rd floor) - In-person

**Scheduling Notes**:
- ✅ **Kat's schedule fully respected** (hard constraint satisfied)
- ✅ **No overrides needed** (found pure availability slot!)
- ✅ Selected Wednesday mid-week (optimal for all)
- ✅ Meeting room reserved

**Alternative Considered**:
If Wednesday 2pm wasn't available, system would have overridden Chris's or Sangya's 1:1/lunch per your instructions, but NEVER Kat's meetings.

**Key Insight**: This prompt demonstrates the MOST COMPLEX constraint satisfaction in the framework. CAN-12 must balance: (1) Hard constraint: Never override Kat (priority attendee), (2) Soft constraint: CAN override others' 1:1s/lunches IF needed, (3) Pure availability preferred over overrides, (4) Multi-person scheduling (3 calendars to coordinate), (5) Resource booking (in-person room requirement). The system correctly applies priority-based logic: Kat's even low-priority meetings (1:1s, lunches) are treated as high-priority due to "work around Kat's schedule" instruction.
```

---

### Hero Prompt 7: Collaborate-1

**Prompt**: "Help me set the agenda to review the progress of Project Alpha with the product and marketing team to get confirmation we are on track and discuss any blocking issues or risks."

**Category**: Collaborate  
**Capabilities Required**: Attendee resolution, agenda generation  
**Gold Standard F1**: 50%  
**Evaluation**: ⚠️ **Partial** - Missing CAN-05, over-applied CAN-18

**Gold Standard Revision (November 8, 2025)**: 
> Changed CAN-09 (Document Generation) to CAN-23 (Agenda Generation/Structuring). When prompt explicitly mentions "set the agenda", the specialized agenda generation task (CAN-23) is more appropriate than general document generation (CAN-09). The meeting goals ("get confirmation", "discuss risks") should be used as INPUT for CAN-23, not as system tasks to execute.

**Human Evaluator Notes**: 
> "'to get confirmation we are on track and discuss any blocking issues or risks' in the prompt is to set the goal of the meeting and should be used as input for the agenda generation for CAN-23 (was CAN-09). The user does not expect the system to find blocking issues and confirm status but the requester want to find out those during the meeting so CAN-18 should not be activated."

#### Canonical Task Decomposition: 3 Tasks

**Task 1: Natural Language Understanding (CAN-04)**
- **Purpose**: Extract agenda requirements and meeting goals
- **Input**: User prompt text
- **Output**: {"intent": "generate_agenda", "topic": "Project Alpha progress review", "attendees": ["product team", "marketing team"], "goals": ["confirm on track", "discuss blocking issues/risks"]}
- **Tier**: Universal (Tier 1)

**Task 2: Attendee/Contact Resolution (CAN-05) - **MISSING IN ORIGINAL****
- **Purpose**: Resolve "product team" and "marketing team" to individual members
- **Input**: Team names from CAN-04
- **Output**: List of product and marketing team members
- **Tier**: Universal (Tier 1)
- **Note**: Needed to know who will attend (for agenda context)

**Task 3: Agenda Generation/Structuring (CAN-23) - **REVISED FROM CAN-09****
- **Purpose**: Generate specialized meeting agenda structure
- **Input**: Meeting goals from CAN-04 ("confirm on track", "discuss blocking issues/risks")
- **Output**: Structured agenda with topics, time allocations, discussion goals
- **Tier**: Specialized (Tier 3)
- **Note**: User explicitly requested "set the agenda" - CAN-23 is specialized for agenda creation. Goals used as INPUT, not as tasks to execute (CAN-18 should NOT be used)

#### Evaluation Criteria
- Agenda completeness (covers all stated goals)
- Topic structure clarity (logical flow of discussion)
- Time allocation reasonableness (realistic durations)
- Attendee resolution accuracy (correct team members identified)
- **Critical**: Does NOT include CAN-18 (risk anticipation) - user will discuss risks IN meeting, not have system find them beforehand

#### Execution Composition

**How Tasks Work Together to Answer the Prompt:**

```
STEP 1: Parse Agenda Requirements
CAN-04 (NLU) → Extract meeting goals and attendee groups
  - Parse: "set the agenda" = agenda generation intent
  - Parse: "review progress", "get confirmation", "discuss blocking issues/risks" = MEETING GOALS
  - Extract: topic = "Project Alpha progress review"
  - Extract: teams = ["product team", "marketing team"]
  - Extract: goals = ["confirm we are on track", "discuss any blocking issues or risks"]
  - **IMPORTANT**: These are DISCUSSION GOALS for the meeting, not system tasks to execute

STEP 2: Resolve Team Membership (MISSING IN ORIGINAL)
CAN-05 (Attendee Resolution) → Identify individual team members
  - Input: "product team", "marketing team"
  - Lookup: Directory/org chart for team composition
  - Output: 
    - Product team: [PM1, PM2, Designer, Engineer Lead]
    - Marketing team: [Marketing Manager, Content Lead, Campaign Manager]

STEP 3: Generate Meeting Agenda
CAN-23 (Agenda Generation/Structuring) → Create specialized agenda structure
  - Meeting title: "Project Alpha Progress Review"
  - Attendees: 7 people (product + marketing teams)
  - Duration: 60 minutes (estimated)
  - Agenda structure:
    1. Introductions & Context (5 min)
    2. Project Alpha Status Overview (15 min)
       - Goal: "Get confirmation we are on track"
    3. Blocking Issues Discussion (20 min)
       - Goal: "Discuss any blocking issues or risks"
    4. Next Steps & Action Items (15 min)
    5. Q&A (5 min)

OUTPUT: Specialized meeting agenda ready for distribution
  - Clear topic breakdown aligned with user's stated goals
  - Realistic time allocations
  - Discussion objectives for each agenda item
  - **NOTE**: Agenda sets up discussion framework; actual risk identification happens DURING meeting
```

#### Key Orchestration Patterns
- **Simple Sequential**: CAN-04 → CAN-05 → CAN-23 (only 3 tasks, minimal orchestration)
- **No Automation Beyond Agenda**: User wants help SETTING agenda, not executing the meeting goals
- **Critical Distinction**: Meeting goals ≠ System tasks (CAN-18 should NOT run to find risks beforehand)
- **Gold Standard Revision**: CAN-09 → CAN-23 reflects specialized agenda generation requirement
- **Simplest Collaborate Prompt**: Only 3 tasks - demonstrates minimum collaboration preparation

#### Example Flow - Agenda Generation for Project Review

```
User Request: "Help me set the agenda to review the progress of Project Alpha with the product and marketing team to get confirmation we are on track and discuss any blocking issues or risks."

CAN-04: Parse agenda requirements ✓
  → topic: "Project Alpha progress review"
  → teams: ["product team", "marketing team"]
  → goals: ["confirm on track", "discuss blocking issues/risks"]
  → intent: Generate meeting agenda (NOT find risks or confirm status)

CAN-05: Resolve team membership (MISSING IN ORIGINAL) ✓
  → Product team: [Sarah Chen (PM), Mike Liu (Designer), Alex Kumar (Eng Lead), Jamie Park (PM)]
  → Marketing team: [Dana Williams (Manager), Chris Lee (Content), Taylor Brown (Campaigns)]
  → Total attendees: 7 people

CAN-23: Generate structured agenda (REVISED FROM CAN-09) ✓
  → Meeting Title: "Project Alpha Progress Review"
  → Proposed Duration: 60 minutes
  → Agenda:
    
    **PROJECT ALPHA PROGRESS REVIEW**
    Date: [TBD]
    Duration: 60 minutes
    Attendees: Product Team (Sarah, Mike, Alex, Jamie) + Marketing Team (Dana, Chris, Taylor)
    
    AGENDA:
    1. Welcome & Objectives (5 min)
       - Review meeting goals
    
    2. Project Alpha Status Update (15 min)
       - Current progress overview
       - Milestones achieved
       - **GOAL**: Get confirmation we are on track
    
    3. Blocking Issues & Risks Discussion (20 min)
       - Open discussion of any blockers
       - Risk identification and mitigation
       - **GOAL**: Surface and discuss any blocking issues or risks
    
    4. Action Items & Next Steps (15 min)
       - Assign owners for identified issues
       - Set follow-up timeline
    
    5. Q&A / Wrap-up (5 min)

OUTPUT to User:

✅ **STRUCTURED AGENDA CREATED**

**PROJECT ALPHA PROGRESS REVIEW**
- **Attendees**: 7 people (Product + Marketing teams)
- **Duration**: 60 minutes
- **Agenda**: 5 sections with time allocations
- **Discussion Goals**: Embedded in agenda structure

**Key Sections**:
1. Status Update (15 min) - Confirm we're on track
2. Blocking Issues Discussion (20 min) - Surface and discuss risks
3. Action Items (15 min) - Assign ownership and next steps

**Ready to distribute to participants** ✅

**Key Insight**: The system did NOT run CAN-18 (Risk Anticipation) because the user wants to DISCUSS risks during the meeting, not have the system FIND them beforehand. "Discuss any blocking issues or risks" is a MEETING GOAL, not a system task. This demonstrates a critical principle: meeting agenda items are INPUTS to the agenda structure (CAN-23), not tasks for the system to execute. The Gold Standard Revision from CAN-09 to CAN-23 also reflects that specialized agenda generation is more appropriate than general document generation when "set the agenda" is explicitly requested.
```

---

### Hero Prompt 8: Collaborate-2

**Prompt**: "Review the materials for my meeting with senior leadership and suggest the best way to summarize the topics into three main discussion points. Generate any objections or concerns that might come up and give me effective responses."

**Category**: Collaborate  
**Capabilities Required**: Meeting material retrieval, content summarization, objection anticipation, response generation  
**Gold Standard F1**: 77.78%  
**Evaluation**: ⚠️ **Partial** - Missing CAN-05 (Attendee Resolution)

**Human Evaluator Notes**: 
> "The system needs to know who are in the senior leadership to find relevant meetings and meeting related materials. So CAN-05 is a critical task."

#### Canonical Task Decomposition: 7 Tasks (Including CAN-05)

**Task 1: Natural Language Understanding (CAN-04)**
- **Purpose**: Extract preparation requirements
- **Input**: User prompt text
- **Output**: {"intent": "prepare_for_meeting", "attendees": "senior leadership", "tasks": ["review materials", "summarize to 3 points", "generate objections", "create responses"]}
- **Tier**: Universal (Tier 1)

**Task 2: Attendee/Contact Resolution (CAN-05) - **MISSING IN ORIGINAL****
- **Purpose**: Resolve "senior leadership" to specific executives
- **Input**: "senior leadership" from CAN-04
- **Output**: List of senior leadership members (VPs, C-level)
- **Tier**: Universal (Tier 1)
- **Note**: **CRITICAL** - Needed to find relevant meetings and materials

**Task 3: Calendar Events Retrieval (CAN-01)**
- **Purpose**: Find the upcoming meeting with senior leadership
- **Input**: Resolved senior leadership attendees from CAN-05
- **Output**: Upcoming meeting event
- **Tier**: Universal (Tier 1)
- **Dependencies**: CAN-05 (need to know who senior leadership is)

**Task 4: Meeting Metadata Extraction (CAN-07)**
- **Purpose**: Extract meeting details (attendees, agenda, attachments)
- **Input**: Meeting event from CAN-01
- **Output**: Meeting metadata
- **Tier**: Common (Tier 2)

**Task 5: Document/Content Retrieval (CAN-08)**
- **Purpose**: Retrieve meeting materials (presentations, documents, pre-reads)
- **Input**: Meeting attachments from CAN-07
- **Output**: Meeting materials content
- **Tier**: Common (Tier 2)
- **Dependencies**: CAN-07 (need attachments list)

**Task 6: Document Generation/Formatting (CAN-09)**
- **Purpose**: Summarize materials into 3 main discussion points
- **Input**: Retrieved materials from CAN-08
- **Output**: Formatted summary with 3 key points
- **Tier**: Common (Tier 2)

**Task 7: Objection/Risk Anticipation (CAN-18)**
- **Purpose**: Generate potential objections/concerns + effective responses
- **Input**: Discussion points from CAN-09 + senior leadership context
- **Output**: List of objections with prepared responses
- **Tier**: Specialized (Tier 3)
- **Note**: User explicitly requests this ("Generate any objections or concerns")

#### Evaluation Criteria
- Attendee resolution accuracy (senior leadership correctly identified from organization)
- Summarization quality (3 discussion points capture key themes from materials)
- Objection anticipation relevance (concerns match senior leadership perspective)
- Response effectiveness (prepared responses address objections convincingly)
- CAN-05 inclusion (CRITICAL - human evaluator identified missing dependency for finding materials)

#### Execution Composition

**How Tasks Work Together to Answer the Prompt:**

```
STEP 1: Understand Preparation Requirements
CAN-04 (NLU) → Parse multi-part request
  - Parse: "Review the materials for my meeting with senior leadership" = material retrieval required
  - Parse: "suggest the best way to summarize the topics into three main discussion points" = summarization task
  - Parse: "Generate any objections or concerns that might come up" = objection anticipation
  - Parse: "give me effective responses" = response preparation
  - Output: Comprehensive preparation parameters

STEP 2: Resolve Senior Leadership Attendees (CRITICAL - MISSING IN ORIGINAL)
CAN-05 (Attendee/Contact Resolution) → Identify who is "senior leadership"
  - Search: Organization directory for senior leadership (VPs, C-level executives)
  - Resolve: Full contact details, titles, reporting structure
  - Purpose: **ESSENTIAL** - Cannot find "meeting with senior leadership" without knowing who they are!
  - Output: Senior leadership list (e.g., CEO, CFO, COO, VP Product, VP Sales)

STEP 3: Find the Senior Leadership Meeting
CAN-01 (Calendar Retrieval) → Locate upcoming meeting
  - Input: Resolved senior leadership attendees from CAN-05
  - Search: Upcoming calendar for meetings with ANY senior leadership member
  - Filter: Likely candidates (multiple C-level attendees, duration 60+ min)
  - Output: Identified meeting (e.g., "Executive Business Review" with CEO, CFO, VP Product)

STEP 4: Extract Meeting Details
CAN-07 (Metadata Extraction) → Get meeting metadata
  - Extract: Attendee list, meeting agenda, scheduled time, location
  - Extract: Attachments (presentations, pre-read documents, data reports)
  - Extract: Meeting organizer, purpose, previous meeting series
  - Output: Meeting metadata including list of attached materials

STEP 5: Retrieve Meeting Materials
CAN-08 (Document Retrieval) → Load all attached materials
  - Input: Attachment list from CAN-07
  - Retrieve: Q3 Financial Report.pdf, Product Roadmap Update.pptx, Market Analysis.docx
  - Parse: Extract text content from documents for analysis
  - Output: Full content of all meeting materials (e.g., 50 pages of documents)

STEP 6: Summarize into 3 Main Discussion Points
CAN-09 (Document Generation) → Synthesize materials into key themes
  - Analyze: Identify recurring themes across all materials
  - Prioritize: Select 3 most important topics based on frequency, strategic importance, action-oriented
  - Format: Create concise summaries with supporting data points
  - Output: 3 main discussion points with key facts

STEP 7: Generate Objections and Responses
CAN-18 (Objection/Risk Anticipation) → Anticipate senior leadership concerns
  - Input: 3 discussion points from CAN-09 + senior leadership profiles from CAN-05
  - Analyze: For each discussion point, identify potential objections
    - Financial concerns (CFO perspective)
    - Market risks (CEO perspective)
    - Execution feasibility (COO perspective)
  - Generate: Prepared responses for each objection with supporting data
  - Output: Objection-response pairs for all 3 discussion points

OUTPUT: Comprehensive meeting preparation package
  1. 3 MAIN DISCUSSION POINTS: Structured summaries from materials
  2. ANTICIPATED OBJECTIONS: Likely concerns from senior leadership
  3. EFFECTIVE RESPONSES: Prepared answers with data/rationale
```

#### Key Orchestration Patterns
- **CRITICAL MISSING DEPENDENCY**: CAN-05 MUST precede CAN-01 - cannot find "meeting with senior leadership" without knowing who senior leadership is
- **Sequential Document Pipeline**: CAN-07 (get attachments) → CAN-08 (retrieve content) → CAN-09 (summarize)
- **Objection Layer**: CAN-18 runs after CAN-09 (needs discussion points) and uses CAN-05 (needs attendee profiles)
- **Human Evaluator Insight**: Original decomposition missed CAN-05 - evaluator noted "system needs to know who are in the senior leadership"
- **Contrast with Collaborate-1**: Here CAN-18 IS appropriate because user explicitly requested "Generate any objections or concerns"

#### Example Flow - Executive Meeting Preparation

```
User Request: "Review the materials for my meeting with senior leadership and suggest the best way to summarize the topics into three main discussion points. Generate any objections or concerns that might come up and give me effective responses."

CAN-04: Extract preparation requirements ✓
  → intent: "prepare_for_meeting"
  → attendees: "senior leadership"
  → tasks: ["review_materials", "summarize_to_3_points", "generate_objections", "create_responses"]

CAN-05: Resolve "senior leadership" (CRITICAL - MISSING IN ORIGINAL) ✓
  **Without this step, system cannot find the meeting!**
  
  Organization directory search: "senior leadership"
  Identified:
  - Jennifer Park (CEO)
  - Michael Chen (CFO)
  - Sarah Williams (COO)
  - Alex Kumar (VP Product)
  - Dana Rodriguez (VP Sales)
  
  Output: 5 senior leadership members resolved

CAN-01: Find upcoming senior leadership meeting ✓
  **Uses resolved attendees from CAN-05 to search calendar**
  
  Search: Upcoming meetings with Jennifer Park (CEO) OR Michael Chen (CFO) OR ...
  Found: "Q4 Executive Business Review"
  - Date: Next Tuesday, 2:00-3:30 PM
  - Attendees: Jennifer Park (CEO), Michael Chen (CFO), Alex Kumar (VP Product)
  - Organizer: You
  - Duration: 90 minutes

CAN-07: Extract meeting metadata ✓
  Meeting details:
  - Subject: "Q4 Executive Business Review"
  - Attendees: CEO, CFO, VP Product (3 executives)
  - Attachments: 3 documents
    1. Q4_Financial_Performance.pdf
    2. Product_Roadmap_2025.pptx
    3. Competitive_Market_Analysis.docx

CAN-08: Retrieve meeting materials ✓
  Retrieved 3 documents (50 pages total):
  
  **Q4_Financial_Performance.pdf** (15 pages):
  - Revenue: $45M (target $50M, -10% miss)
  - Operating margin: 18% (improved from 15% in Q3)
  - Customer churn: 8% (up from 6% in Q3 - concerning!)
  - Cash position: $22M (healthy)
  
  **Product_Roadmap_2025.pptx** (20 slides):
  - Launch new AI features in Q1 2025
  - Mobile app redesign in Q2
  - Enterprise tier launch in Q3
  - Total investment: $8M over 4 quarters
  - Expected ROI: 30% revenue increase by end of 2025
  
  **Competitive_Market_Analysis.docx** (15 pages):
  - Competitor A launched similar features 2 months ago
  - Market share: We are #3 (18%), Competitor A is #1 (35%)
  - Customer win rate declining: 45% → 38%
  - Pricing pressure: Average deal size down 12%

CAN-09: Summarize into 3 main discussion points ✓
  
  **DISCUSSION POINT 1: Q4 Financial Performance and Revenue Gap**
  - Revenue came in at $45M vs $50M target (-10% miss)
  - Positive: Operating margin improved to 18%
  - Concern: Customer churn increased to 8% (from 6%)
  - Key Question: What caused revenue miss?
  
  **DISCUSSION POINT 2: 2025 Product Roadmap Investment Decision**
  - Proposed investment: $8M across 4 quarters
  - Expected return: 30% revenue increase by end of 2025
  - Strategic importance: Competitor A already launched similar features
  - Key Decision: Approve $8M investment or scale back?
  
  **DISCUSSION POINT 3: Competitive Position and Market Share**
  - Market share: #3 position at 18% (behind Competitor A at 35%)
  - Customer win rate declining: 45% → 38%
  - Pricing pressure: Average deal size down 12%
  - Key Question: How do we regain competitive momentum?

CAN-18: Generate objections and effective responses ✓
  **Uses senior leadership profiles from CAN-05 to anticipate perspective-specific objections**
  
  **OBJECTIONS FOR DISCUSSION POINT 1** (Q4 Financial Performance):
  
  ❌ **CFO Objection**: "Revenue miss of 10% is concerning. How do we know Q1 won't have the same problem?"
  ✅ **Your Response**: "Fair concern. The miss was driven by 2 large deals slipping from Q4 to Q1 (both confirmed). Churn increase is the real issue - we're implementing a customer success intervention plan targeting at-risk accounts. We project churn to return to 6% by Q2."
  
  ❌ **CEO Objection**: "Churn going from 6% to 8% is a red flag. What's causing it?"
  ✅ **Your Response**: "Exit interviews show 60% of churned customers cited lack of mobile app and AI features - which our 2025 roadmap addresses. This validates our product investment thesis. The other 40% cited pricing, which we're addressing with enterprise tier."
  
  **OBJECTIONS FOR DISCUSSION POINT 2** (Product Roadmap Investment):
  
  ❌ **CFO Objection**: "$8M investment is significant given we just missed revenue target. Can we scale back?"
  ✅ **Your Response**: "We evaluated a phased approach. Minimum viable investment is $5M (AI features only). However, competitive analysis shows Competitor A is gaining share with their mobile app. Delaying mobile risks further customer win rate decline. ROI projections show $8M investment pays back in 10 months."
  
  ❌ **VP Product Objection**: "Enterprise tier launch in Q3 is aggressive. Do we have engineering capacity?"
  ✅ **Your Response**: "Agreed it's tight. We're proposing 2 additional engineering hires in Q1 (already budgeted). Alternative is to push enterprise tier to Q4, but that delays revenue impact by 1 quarter ($3M opportunity cost)."
  
  **OBJECTIONS FOR DISCUSSION POINT 3** (Competitive Position):
  
  ❌ **CEO Objection**: "Win rate declining from 45% to 38% is alarming. Is this a sales execution problem or product gap?"
  ✅ **Your Response**: "Analysis shows 70% of losses are to Competitor A citing their AI features (product gap). 30% are sales execution (pricing/contracting delays). Product roadmap addresses the 70%, and we've streamlined sales approval process to address the 30%. We expect win rate to recover to 42% by Q2."

OUTPUT to User:

📋 **EXECUTIVE MEETING PREPARATION BRIEF**

**Meeting**: Q4 Executive Business Review  
**Attendees**: Jennifer Park (CEO), Michael Chen (CFO), Alex Kumar (VP Product)  
**Date**: Next Tuesday, 2:00-3:30 PM

---

**THREE MAIN DISCUSSION POINTS**:

1. **Q4 Financial Performance and Revenue Gap**
   - Revenue: $45M vs $50M target (-10% miss)
   - Margin: 18% (improved from 15%)
   - Churn: 8% (up from 6% - key concern)

2. **2025 Product Roadmap Investment Decision**
   - Investment: $8M for AI + Mobile + Enterprise tier
   - Expected ROI: 30% revenue increase
   - Competitive urgency: Competitor A already launched

3. **Competitive Position and Market Share**
   - Market share: #3 at 18% (vs Competitor A at 35%)
   - Win rate: 45% → 38% (declining)
   - Pricing pressure: Average deal size down 12%

---

**ANTICIPATED OBJECTIONS & EFFECTIVE RESPONSES**:

**Point 1 - Financial Performance**:
- CFO: "How prevent Q1 revenue miss?" → 2 large deals slipped to Q1 (confirmed), churn intervention plan
- CEO: "What's causing churn increase?" → 60% cite lack of mobile/AI (validates roadmap), 40% pricing (enterprise tier addresses)

**Point 2 - Product Investment**:
- CFO: "Can we scale back $8M investment?" → Minimum $5M (AI only), but delaying mobile risks further decline, 10-month payback
- VP Product: "Q3 enterprise tier too aggressive?" → 2 engineering hires needed, alternative Q4 push has $3M opportunity cost

**Point 3 - Competitive Position**:
- CEO: "Is win rate decline sales or product issue?" → 70% product gap (roadmap fixes), 30% sales execution (process streamlined)

**PREPARATION COMPLETE** ✅

**Key Insight**: CAN-05 (Attendee Resolution) is CRITICAL and was missing in original decomposition. Human evaluator correctly identified: "The system needs to know who are in the senior leadership to find relevant meetings and meeting related materials." Without CAN-05, the system cannot search for "meeting with senior leadership" (CAN-01) or tailor objections to specific executive perspectives (CAN-18).
```

---

### Hero Prompt 9: Collaborate-3

**Prompt**: "Prepare a brief for my upcoming meeting with customer Beta and include a dossier for each customer attendee and the topics they are most interested in. Include a background on their company."

**Category**: Collaborate  
**Capabilities Required**: Meeting preparation, contact research, company intelligence, document generation  
**Gold Standard F1**: 100%  
**Evaluation**: ✅ **Correct**

#### Canonical Task Decomposition: 7 Tasks

**Task 1: Natural Language Understanding (CAN-04)**
- **Purpose**: Extract brief preparation requirements
- **Input**: User prompt text
- **Output**: {"intent": "prepare_brief", "customer": "Beta", "components": ["attendee dossiers", "interest topics", "company background"]}
- **Tier**: Universal (Tier 1)

**Task 2: Calendar Events Retrieval (CAN-01)**
- **Purpose**: Find upcoming meeting with customer Beta
- **Input**: Customer name ("Beta")
- **Output**: Upcoming Beta customer meeting
- **Tier**: Universal (Tier 1)

**Task 3: Meeting Metadata Extraction (CAN-07)**
- **Purpose**: Extract customer attendees from meeting
- **Input**: Beta meeting from CAN-01
- **Output**: List of customer Beta attendees
- **Tier**: Common (Tier 2)

**Task 4: Attendee/Contact Resolution (CAN-05)**
- **Purpose**: Resolve customer attendees to full profiles
- **Input**: Customer attendee names from CAN-07
- **Output**: Full profiles (title, role, LinkedIn, background)
- **Tier**: Universal (Tier 1)

**Task 5: Document/Content Retrieval (CAN-08)**
- **Purpose**: Retrieve past meeting materials, emails with customer Beta
- **Input**: Customer Beta identifier + attendees
- **Output**: Historical interaction content
- **Tier**: Common (Tier 2)

**Task 6: Document Generation/Formatting (CAN-09)**
- **Purpose**: Generate meeting brief and attendee dossiers
- **Input**: Attendee profiles + historical materials
- **Output**: Formatted brief with dossiers
- **Tier**: Common (Tier 2)

**Task 7: Research/Intelligence Gathering (CAN-22)**
- **Purpose**: Research customer Beta company background
- **Input**: Company name ("Beta")
- **Output**: Company intelligence (industry, news, financials, recent developments)
- **Tier**: Specialized (Tier 3)
- **Note**: Addresses "Include a background on their company"

#### Evaluation Criteria
- Meeting identification accuracy (correct customer Beta meeting found)
- Attendee dossier completeness (all customer attendees profiled with relevant background)
- Interest topic relevance (topics accurately reflect customer priorities from historical data)
- Company background depth (comprehensive intelligence on customer Beta company)
- Document formatting quality (brief is well-structured and executive-ready)

#### Execution Composition

**How Tasks Work Together to Answer the Prompt:**

```
STEP 1: Understand Brief Requirements
CAN-04 (NLU) → Parse multi-component preparation request
  - Parse: "Prepare a brief for my upcoming meeting with customer Beta" = meeting prep task
  - Parse: "include a dossier for each customer attendee" = individual profiles required
  - Parse: "the topics they are most interested in" = interest analysis from historical data
  - Parse: "Include a background on their company" = company intelligence research
  - Output: Comprehensive brief requirements

STEP 2: Find Customer Beta Meeting
CAN-01 (Calendar Retrieval) → Locate upcoming meeting
  - Search: Upcoming calendar for meetings with "Beta" in subject, attendees, or notes
  - Filter: Customer-facing meetings (external attendees)
  - Identify: "Quarterly Business Review - Beta Corporation"
  - Output: Meeting event (e.g., next Thursday 10:00-11:30 AM)

STEP 3: Extract Customer Attendees
CAN-07 (Metadata Extraction) → Get meeting participant details
  - Extract: All attendees from meeting
  - Separate: Internal attendees vs external customer Beta attendees
  - Customer attendees identified: ["Sarah Johnson", "Michael Lee", "Emily Carter"]
  - Output: List of 3 customer Beta attendee names

STEP 4: Resolve Attendees to Full Profiles
CAN-05 (Attendee/Contact Resolution) → Build comprehensive profiles
  - For each customer attendee: Search CRM, LinkedIn, contact database
  - Retrieve: Title, role, seniority, background, LinkedIn profile, previous interactions
  - Enrich: Years at company, previous roles, education, expertise areas
  - Output: Full profiles for all 3 customer attendees

STEP 5: Retrieve Historical Interaction Materials
CAN-08 (Document Retrieval) → Load past meeting data
  - Search: Previous meetings with customer Beta (past 6-12 months)
  - Retrieve: Meeting notes, email threads, shared documents, presentations
  - Search: CRM notes, support tickets, product usage data
  - Purpose: Identify topics customer Beta has discussed (for interest analysis)
  - Output: Historical content corpus (e.g., 15 past meetings, 50 emails)

STEP 6-7: Generate Dossiers and Research Company (Parallel Processing)
CAN-09 (Document Generation) → Create attendee dossiers and brief structure
  - For each attendee: Synthesize profile + historical interactions into dossier
  - Analyze: Historical materials to identify topics each attendee discussed frequently
  - Interest topics: Recurring themes in their questions, requests, concerns
  - Format: Executive-ready dossier with key facts, interest areas, interaction history
  - Output: 3 attendee dossiers with interest topic analysis

CAN-22 (Research/Intelligence) → Gather company background
  - Research: Customer Beta company profile
  - Sources: Public filings, news articles, press releases, industry reports
  - Extract: Industry, size (revenue, employees), recent developments
  - Financial data: Revenue trends, growth rate, funding status
  - Strategic context: Business priorities, market position, competitive landscape
  - Output: Comprehensive company background report

OUTPUT: Complete meeting brief
  1. CUSTOMER BETA COMPANY BACKGROUND: Industry, financials, recent news
  2. ATTENDEE DOSSIERS: Profiles for each customer attendee with interaction history
  3. INTEREST TOPICS: Key themes each attendee cares about
  4. MEETING CONTEXT: Suggested discussion points based on customer interests
```

#### Key Orchestration Patterns
- **Parallel Research**: CAN-09 (attendee dossiers) + CAN-22 (company research) run independently
- **Historical Analysis**: CAN-08 retrieves past interactions, CAN-09 analyzes for interest patterns
- **Multi-Layer Context**: Individual (dossiers) + company (background) + historical (interests)
- **Profile Enrichment Pipeline**: CAN-07 (extract names) → CAN-05 (resolve to profiles) → CAN-09 (generate dossiers)
- **Most Customer-Facing Prompt**: Demonstrates external research capabilities (CAN-22) and relationship intelligence

#### Example Flow - Customer Meeting Brief Preparation

```
User Request: "Prepare a brief for my upcoming meeting with customer Beta and include a dossier for each customer attendee and the topics they are most interested in. Include a background on their company."

CAN-04: Extract brief requirements ✓
  → intent: "prepare_brief", customer: "Beta"
  → components: ["attendee_dossiers", "interest_topics", "company_background"]

CAN-01: Find customer Beta meeting ✓
  Found: "Quarterly Business Review - Beta Corporation"
  - Date: Next Thursday, 10:00-11:30 AM
  - Location: Conference Room A + Video
  - Internal: You, VP Sales (Dana), CSM (Jordan)
  - External: Sarah Johnson, Michael Lee, Emily Carter (Beta)

CAN-07: Extract customer attendees ✓
  Customer attendees identified:
  1. Sarah Johnson (external)
  2. Michael Lee (external)
  3. Emily Carter (external)

CAN-05: Resolve customer attendees to full profiles ✓
  
  **Sarah Johnson**:
  - Title: VP of Operations, Beta Corporation
  - Background: 8 years at Beta, promoted from Director 2 years ago
  - Education: MBA Stanford, BS Industrial Engineering
  - Previous: McKinsey (consultant 5 years)
  - Expertise: Process optimization, supply chain
  
  **Michael Lee**:
  - Title: Director of IT, Beta Corporation
  - Background: 3 years at Beta, joined from Amazon
  - Education: MS Computer Science, UW
  - Previous: Amazon (software engineer, 6 years)
  - Expertise: Cloud infrastructure, security, APIs
  
  **Emily Carter**:
  - Title: Product Manager, Beta Corporation
  - Background: 5 years at Beta, former business analyst
  - Education: BA Business Administration, UC Berkeley
  - Previous: Business Analyst at Beta (promoted 2 years ago)
  - Expertise: Product strategy, user experience, analytics

CAN-08: Retrieve historical interaction materials ✓
  Retrieved 15 past meetings + 50 emails (past 12 months):
  - Monthly check-ins (10 meetings)
  - Onboarding session (3 months ago)
  - Product training (2 sessions)
  - Quarterly business reviews (2 previous QBRs)
  - Feature requests (15 emails from Emily)
  - Technical questions (20 emails from Michael)
  - Process discussions (10 emails from Sarah)

CAN-09: Generate attendee dossiers with interest topics (Parallel with CAN-22) ✓
  
  **DOSSIER: Sarah Johnson** (VP of Operations)
  - **Topics Most Interested In**:
    1. ROI & Cost Optimization (mentioned in 8 of 10 emails)
    2. Workflow Automation (discussed in 4 meetings)
    3. Scalability for Growth (raised in last QBR)
  
  **DOSSIER: Michael Lee** (Director of IT)
  - **Topics Most Interested In**:
    1. Security & Compliance (mentioned in 12 of 20 emails)
    2. API Integration (discussed in 3 support tickets)
    3. Performance & Uptime (raised in 2 emails)
  
  **DOSSIER: Emily Carter** (Product Manager)
  - **Topics Most Interested In**:
    1. Mobile App Enhancements (mentioned in 8 of 15 emails)
    2. User Experience Improvements (discussed in 5 meetings)
    3. Analytics & Reporting (raised in last QBR)

CAN-22: Research Beta Corporation company background (Parallel with CAN-09) ✓
  
  **BETA CORPORATION - COMPANY BACKGROUND**
  - Industry: Healthcare Technology (medical device distribution)
  - Founded: 1998 (26 years)
  - Employees: 850 (grown from 600 in 2022)
  - Revenue: $320M annually (30% YoY growth)
  - Recent: New CEO (Dr. James Park, ex-Medtronic), 2 new distribution centers
  - Strategic: Geographic expansion (20 centers by 2026), digital transformation

OUTPUT to User:

📄 **CUSTOMER MEETING BRIEF - BETA CORPORATION**

**Meeting**: Quarterly Business Review  
**Date**: Next Thursday, 10:00-11:30 AM  
**Customer Attendees**: Sarah Johnson (VP Ops), Michael Lee (Dir IT), Emily Carter (PM)

---

**COMPANY BACKGROUND - BETA CORPORATION**

**Industry**: Healthcare Technology (medical device distribution)  
**Size**: 850 employees, $320M revenue, 30% YoY growth  
**Recent News**: 
- New CEO: Dr. James Park (ex-Medtronic)
- Expansion: Opened Denver + Austin distribution centers
- Investment: $15M in technology modernization

**Strategic Priorities**:
1. Geographic expansion (12 → 20 distribution centers by 2026)
2. Digital transformation (CEO vision: "most tech-enabled distributor by 2026")
3. Customer experience (ranked #1 in customer satisfaction)

---

**ATTENDEE DOSSIERS**

**Sarah Johnson** - VP of Operations (Decision-Maker)  
- **Top Interests**:
  1. ROI & Cost Optimization
  2. Workflow Automation (wants to automate 20 hrs/month reporting)
  3. Scalability (planning for 500 users next year)

**Michael Lee** - Director of IT (Technical Gatekeeper)  
- **Top Interests**:
  1. Security & Compliance (healthcare = HIPAA, asked about SOC 2 Type 2)
  2. API Integration (building internal tools, needs Salesforce access)
  3. Performance & Uptime (requires 99.9% SLA)

**Emily Carter** - Product Manager (User Advocate)  
- **Top Interests**:
  1. Mobile App Enhancements (field team needs offline mode)
  2. User Experience (feedback: dashboard too cluttered)
  3. Analytics & Reporting (analysts need custom templates)

---

**MEETING PREP RECOMMENDATIONS**:
1. **For Sarah**: Prepare cost savings analysis (automation reclaims 20 hrs/month)
2. **For Michael**: Bring SOC 2 Type 2 cert, demo API integration
3. **For Emily**: Preview mobile offline mode roadmap, show dashboard redesign

**BRIEF COMPLETE** ✅

**Key Insight**: This prompt demonstrates the most comprehensive customer relationship intelligence in the framework. CAN-08 (historical retrieval) + CAN-09 (interest analysis) create personalized dossiers that analyze PATTERNS in past interactions to predict what each attendee will care about. Combined with CAN-22 (company research), the brief provides both individual-level (dossiers) and company-level (strategic priorities) context.
```

---

## Part 3: Cross-Prompt Analysis

### Task Usage Summary

The following table shows which canonical tasks are used across all 9 hero prompts:

| Task ID | Task Name | Prompts Using | Total | % Coverage |
|---------|-----------|---------------|-------|------------|
| CAN-04 | Natural Language Understanding | O1, O2, O3, S1, S2, S3, C1, C2, C3 | 9/9 | 100% |
| CAN-01 | Calendar Events Retrieval | O1, O2, O3, S1, S2, S3, C1, C2, C3 | 9/9 | 100% |
| CAN-07 | Meeting Metadata Extraction | O1, O2, O3, S2, S3, C2, C3 | 7/9 | 78% |
| CAN-05 | Attendee/Contact Resolution | O1, S1, S2, S3, C1, C2 | 6/9 | 67% |
| CAN-02 | Meeting Type Classification | O1, O3, S3, C2 | 4/9 | 44% |
| CAN-03 | Meeting Importance Assessment | O1, O3, S3, C2 | 4/9 | 44% |
| CAN-09 | Document Generation/Formatting | C1, C2, C3 | 3/9 | 33% |
| CAN-12 | Constraint Satisfaction | S1, S2, S3 | 3/9 | 33% |
| CAN-06 | Availability Checking | S1, S2, S3 | 3/9 | 33% |
| CAN-11 | Priority/Preference Matching | O1, O3 | 2/9 | 22% |
| CAN-13 | RSVP Status Update | O1, S2 | 2/9 | 22% |
| CAN-08 | Document/Content Retrieval | C2, C3 | 2/9 | 22% |
| CAN-10 | Time Aggregation/Statistical Analysis | O3 | 1/9 | 11% |
| CAN-14 | Recommendation Engine | O3 | 1/9 | 11% |
| CAN-15 | Recurrence Rule Generation | S1 | 1/9 | 11% |
| CAN-16 | Event Monitoring/Change Detection | O2 | 1/9 | 11% |
| CAN-17 | Automatic Rescheduling | S1, S2 | 2/9 | 22% |
| CAN-18 | Objection/Risk Anticipation | C2 | 1/9 | 11% |
| CAN-19 | Resource Booking | S3 | 1/9 | 11% |
| CAN-20 | Data Visualization/Reporting | O3 | 1/9 | 11% |
| CAN-21 | Focus Time/Preparation Time Analysis | O2 | 1/9 | 11% |
| CAN-22 | Research/Intelligence Gathering | C3 | 1/9 | 11% |
| CAN-23 | Agenda Generation/Structuring | C1 | 1/9 | 11% |
| **CAN-25** | **Event Annotation/Flagging (NEW)** | **O2** | **1/9** | **11%** |
| CAN-24 | Multi-party Coordination/Negotiation | (none) | 0/9 | 0% |

**Legend**: O1-O3 = Organizer 1-3, S1-S3 = Schedule 1-3, C1-C3 = Collaborate 1-3

### Performance Metrics by Prompt

| Prompt | Category | Tasks | Gold Standard F1 | Evaluation | Key Issues |
|--------|----------|-------|------------------|------------|------------|
| Organizre-3 | Organizer | 9 | 100% | ✅ Correct | None - highest complexity, perfect score |
| Organizer-1 | Organizer | 7 | 100% | ✅ Correct | None - RSVP automation working |
| Organizer-2 | Organizer | 9 | 100% | ✅ Correct | NEW CAN-25 validated |
| Schedule-1 | Schedule | 9 | 100% | ✅ Correct | Automation layer (CAN-16, CAN-17) |
| Schedule-3 | Schedule | 10 | 100% | ✅ Correct | Most complex (10 tasks) |
| Collaborate-3 | Collaborate | 7 | 100% | ✅ Correct | Customer intelligence (CAN-22) |
| Schedule-2 | Schedule | 8 | 88.89% | ⚠️ Partial | Missing CAN-06; Revised CAN-17; CAN-05 removed (not needed) |
| Collaborate-2 | Collaborate | 7 | 77.78% | ⚠️ Partial | Missing CAN-05 (critical) |
| Collaborate-1 | Collaborate | 3 | 50% | ⚠️ Partial | Missing CAN-05, over-applied CAN-18; Revised CAN-23 |

**Overall Statistics**:
- **Mean F1**: 93.21% ± 14.97%
- **Median F1**: 100%
- **Prompts at 100% F1**: 6 of 9 (67%)
- **Prompts needing improvement**: 3 of 9 (33%)

### Task Frequency Distribution by Tier

**Tier 1 - Universal Tasks** (6 tasks):
- CAN-01 (Calendar Retrieval): 100% coverage ⭐
- CAN-04 (NLU): 100% coverage ⭐
- CAN-05 (Attendee Resolution): 67% coverage
- CAN-02 (Meeting Type): 44% coverage
- CAN-03 (Meeting Importance): 44% coverage

**Tier 2 - Common Tasks** (9 tasks, 8 used):
- CAN-07 (Metadata Extraction): 78% coverage
- CAN-12 (Constraint Satisfaction): 33% coverage
- CAN-06 (Availability Checking): 33% coverage
- CAN-09 (Document Generation): 33% coverage
- CAN-11 (Priority Matching): 22% coverage
- CAN-13 (RSVP Update): 22% coverage
- CAN-08 (Document Retrieval): 22% coverage
- CAN-10 (Time Aggregation): 11% coverage
- CAN-14 (Recommendation Engine): 11% coverage

**Tier 3 - Specialized Tasks** (10 tasks, 8 used):
- CAN-17 (Automatic Rescheduling): 22% coverage (used in 2 prompts) ⭐
- CAN-15 (Recurrence Rule): 11% coverage
- CAN-16 (Event Monitoring): 11% coverage
- CAN-18 (Objection Anticipation): 11% coverage
- CAN-19 (Resource Booking): 11% coverage
- CAN-20 (Data Visualization): 11% coverage
- CAN-21 (Prep Time Analysis): 11% coverage
- CAN-22 (Research/Intelligence): 11% coverage
- CAN-23 (Agenda Generation): 11% coverage
- **CAN-25 (Event Annotation/Flagging - NEW)**: 11% coverage ⭐
- CAN-24 (Multi-party Coordination): 0% coverage (not used)

**Framework Coverage**: 22 of 25 tasks used (88%)

### Key Findings

#### Finding 1: CAN-25 Successfully Validated ⭐

**NEW Task Addition**: CAN-25 (Event Annotation/Flagging) successfully added to V2.0 framework through human evaluation.

**Evidence**:
- Organizer-2 prompt: "Track all my important meetings and **flag any that require focus time**"
- Human evaluator identified "flag" requirement as distinct from "track" (CAN-16)
- CAN-25 defined as: Visual annotation/flagging of calendar events with indicators
- Tier 3 (Specialized) task due to specific use case

**Validation**:
- Detection rate: 100% across evaluation
- No false positives in other prompts
- Clear boundary from CAN-16 (monitoring) - CAN-16 tracks changes, CAN-25 adds visual markers

**Impact**: Framework now complete for meeting flagging/highlighting use cases (visual indicators for prep time, importance, deadlines).

#### Finding 2: CAN-05 Critical but Often Missed ⚠️

**Problem**: Attendee/Contact Resolution (CAN-05) frequently missing in automated analysis despite being critical.

**Evidence**:
- Schedule-2: Missing CAN-05 → cannot check attendee availability (CAN-06 fails)
- Collaborate-2: Missing CAN-05 → cannot find "senior leadership" meeting (CAN-01 fails)
- Collaborate-1: Missing CAN-05 → cannot resolve "product team" and "marketing team"

**Human Evaluator Quotes**:
- Schedule-2: "The model needs to get metadata, and from there to **find attendee** for those meetings"
- Collaborate-2: "The system needs to know **who are in the senior leadership** to find relevant meetings"

**Root Cause**: Generic terms ("senior leadership", "product team", "{name}") not triggering attendee resolution detection.

**Recommendation**: Add explicit CAN-05 triggers for:
- Team references (e.g., "product team", "marketing team")
- Role references (e.g., "senior leadership", "C-level")
- Name placeholders (e.g., "{name}", "with [person]")

#### Finding 3: Meeting Goals vs System Tasks Distinction 🎯

**Issue**: CAN-18 (Risk/Objection Anticipation) over-applied when meeting goals mentioned in prompt.

**Example - Collaborate-1**:
- Prompt: "...to get confirmation we are on track and **discuss any blocking issues or risks**"
- Automated analysis: Included CAN-18 (Risk Anticipation)
- Human evaluator: "User does not expect the system to **find blocking issues** but the requester want to **find out those during the meeting**"

**Principle Established**: 
- **Meeting goals** (what to discuss IN meeting) ≠ **System tasks** (what system should execute)
- "Discuss risks" = agenda item (INPUT to CAN-23)
- "Anticipate objections" = system task (CAN-18 executes)

**Contrast - Collaborate-2** (CAN-18 correctly applied):
- Prompt: "**Generate any objections** or concerns that might come up"
- Here "generate" explicitly requests system execution → CAN-18 appropriate

**Recommendation**: Document this principle in framework guidelines with examples.

#### Finding 4: Framework Coverage Excellent 📊

**Coverage Statistics**:
- **Overall**: 22 of 25 tasks used (88%)
- **Tier 1 (Universal)**: 6 of 6 used (100%) ⭐
- **Tier 2 (Common)**: 8 of 9 used (89%)
- **Tier 3 (Specialized)**: 8 of 10 used (80%)
- **Unused**: Only CAN-24 (Multi-party Coordination)

**Tier Validation**:
- Universal tasks (Tier 1) appear in 44-100% of prompts ✅
- Common tasks (Tier 2) appear in 11-78% of prompts ✅
- Specialized tasks (Tier 3) appear in 11-22% of prompts ✅

**Conclusion**: Tier structure well-balanced - universal tasks have high coverage, specialized tasks used selectively.

**CAN-24 Status**: Multi-party Coordination not used in 9 hero prompts - here's why:

**Why Schedule-3 Doesn't Need CAN-24**:

Schedule-3 ("Land a time with Chris, Sangya, and Kat...") is the most complex multi-person scheduling prompt (10 tasks), but uses **deterministic constraint satisfaction** instead of negotiation:

```
Deterministic Solution Path (Schedule-3):
CAN-06 (Availability Checking) → Finds common free slots for all 3 people
CAN-12 (Constraint Satisfaction) → Applies constraints (work around Kat, override 1:1s/lunches)
Result: Wednesday 2pm selected → MEETING SCHEDULED ✅

No negotiation needed because a valid solution was found!
```

**CAN-24 is a fallback mechanism** for when normal scheduling FAILS:

```
Negotiation Required Path (CAN-24 needed):
CAN-06 → No common free slots found! ❌
CAN-24 (Multi-party Coordination) → Negotiation loop:
  1. Generate 3-5 alternative time options
  2. Send poll to all participants: "Which time works best?"
  3. Collect votes, find majority preference
  4. If still conflicts: Propose compromises (shorten meeting, change format, rotate times)
  5. Re-run CAN-12 with relaxed constraints
  6. Repeat until solution found or escalate to manual
```

**When CAN-24 Would Be Used**:

1. **No Perfect Slot**: "Schedule with 5 executives next week" → no common availability → poll for best compromise
2. **Competing Priorities**: "Schedule CEO, CFO, VP Sales - all have tight schedules" → negotiate who can reschedule existing meetings
3. **Global Timezones**: "Schedule team in Seattle, London, Tokyo, Sydney" → no time works for all → propose rotating meeting times or async alternative
4. **VIP Conflicts**: "Land time with Board members" → multiple VIPs with inflexible schedules → iterative proposal/counter-proposal

**Key Distinction**:
- **CAN-06 + CAN-12**: Deterministic (finds solution from available options)
- **CAN-24**: Interactive negotiation (creates solution through participant collaboration)

**Framework Design**: CAN-24 is more of an **orchestration pattern** (meta-task) that loops CAN-05, CAN-06, CAN-12 with participant input, rather than a single API call. It's a fallback for when first-pass scheduling fails.

**Recommendation**: Add test prompts where deterministic scheduling fails to validate CAN-24 design:
- "Schedule 8 executives for Q1 planning - many have conflicts"
- "Land time with global team across 4 timezones - need everyone present"
- "Schedule board meeting - work around all 6 board members' schedules"

#### Finding 5: Gold Standard Revisions Improved Accuracy 📈

**Revision 1: Collaborate-1**
- **Original**: CAN-09 (Document Generation)
- **Revised**: CAN-23 (Agenda Generation/Structuring)
- **Rationale**: "Set the agenda" explicitly requests specialized agenda generation, not generic document creation
- **Impact**: More precise task boundaries, reduces ambiguity

**Revision 2: Schedule-2**
- **Original**: CAN-23 (Conflict Resolution)
- **Revised**: CAN-17 (Automatic Rescheduling)
- **Rationale**: "Help me reschedule" requests automation action, not just conflict detection
- **Impact**: Distinguishes between detection (CAN-23) and automation (CAN-17)

**Pattern**: Human evaluation refines task boundaries when similar tasks could apply - selects most specific/appropriate task based on prompt intent.

**Framework Benefit**: These revisions establish precedents for future similar prompts.

---

## Part 4: Conclusions

### Optimization Success

The V2.0 gold standard demonstrates successful framework optimization:

**Objectives Achieved**:
1. ✅ **NEW Task Validated**: CAN-25 (Event Annotation/Flagging) successfully identified and incorporated
2. ✅ **Task Boundaries Refined**: CAN-02/03 split validated, CAN-09/23 distinction clarified
3. ✅ **High Accuracy**: 91.98% mean F1 across 9 diverse prompts (6 at 100%)
4. ✅ **Framework Coverage**: 88% of 25 tasks used, excellent tier distribution
5. ✅ **Human Validation**: All 9 prompts reviewed by domain expert with actionable insights

**Performance Comparison**:
- V1.0 (24 tasks): Average precision 74.76%, lower task specificity
- V2.0 (25 tasks): Average precision 87.41% (+12.65%), clearer boundaries ⭐

**Key Improvements**:
- CAN-25 addition addresses flagging/annotation gap
- CAN-05 criticality documented (missing in 3 prompts)
- Meeting goals vs system tasks principle established
- Gold standard revisions (CAN-09→23, CAN-23→17) set precedents

### Framework Validation

The 25 canonical tasks V2.0 framework is validated for production use:

**Evidence of Completeness**:
1. **High Coverage**: 88% of framework exercised across diverse use cases
2. **Balanced Tiers**: Universal (100%), Common (89%), Specialized (80%) coverage
3. **NEW Capability**: CAN-25 identified through evaluation, no other gaps found
4. **Edge Cases Documented**: CAN-05 criticality, CAN-18 scope, meeting goals vs tasks

**Evidence of Accuracy**:
1. **Expert Validation**: 100% human review by framework creator (Chin-Yew Lin)
2. **High Agreement**: 91.98% F1 mean, 6 of 9 at 100%
3. **Clear Boundaries**: Task distinctions validated (CAN-16 vs CAN-25, CAN-09 vs CAN-23)
4. **Reproducible**: Detailed execution compositions enable consistent decomposition

**Framework Strengths**:
- Clear tier structure (Universal → Common → Specialized)
- Well-defined task boundaries with documented edge cases
- Comprehensive coverage of meeting intelligence capabilities
- Validated against real-world prompts (9 hero prompts)

**Areas for Improvement**:
- CAN-05 detection needs strengthening (add explicit triggers)
- CAN-24 needs test prompts to validate (currently unused)
- Meeting goals vs system tasks principle needs explicit documentation

### Production Readiness

**Overall Grade**: **A- (Production-Ready with Minor Improvements)**

✅ **Ready For**:
1. **LLM Evaluation**: Use as ground truth for benchmarking GPT-5, Claude, GPT-4, other models
2. **Production Implementation**: Follow 4-phase priority plan (Universal → Common → Specialized)
3. **Training Data Generation**: Fine-tuning datasets for task decomposition models
4. **Quality Assurance**: Reference standard for production system accuracy validation

⚠️ **Improvements Needed**:
1. **Strengthen CAN-05 Detection**: Add explicit triggers for team/role references
2. **Document Design Principles**: Formalize "meeting goals vs system tasks" with examples
3. **Expand Test Coverage**: Add prompts exercising CAN-24 (Multi-party Coordination)
4. **Optimize Low Performers**: Address Collaborate-1 (50% F1) through prompt engineering

**Implementation Priority** (Based on Task Frequency):

**Phase 1: Core Foundation** (100% frequency) - WEEKS 1-2
- CAN-04: Natural Language Understanding (100%)
- CAN-01: Calendar Events Retrieval (100%)

**Phase 2: High Frequency** (50%+ prompts) - WEEKS 3-5
- CAN-07: Meeting Metadata Extraction (78%)
- CAN-05: Attendee/Contact Resolution (67%) ⚠️ Include explicit detection
- CAN-02: Meeting Type Classification (44%)
- CAN-03: Meeting Importance Assessment (44%)

**Phase 3: Medium Frequency** (25-50% prompts) - WEEKS 6-8
- CAN-12: Constraint Satisfaction (33%)
- CAN-06: Availability Checking (33%)
- CAN-09: Document Generation (33%)
- CAN-11: Priority Matching (22%)
- CAN-13: RSVP Update (22%)
- CAN-17: Automatic Rescheduling (22%) ⭐ Used in automation layer
- CAN-08: Document Retrieval (22%)

**Phase 4: Specialized Features** (11% prompts each) - WEEKS 9-12
- CAN-10, CAN-14, CAN-15, CAN-16, CAN-18, CAN-19, CAN-20, CAN-21, CAN-22, CAN-23, **CAN-25** ⭐

### Future Work

1. **Expand Test Coverage for CAN-24 (Multi-party Coordination)**: 
   - **Why**: CAN-24 not exercised because all 9 hero prompts had deterministic solutions (CAN-06 + CAN-12 found valid slots)
   - **What's Needed**: Add prompts where normal scheduling FAILS and requires negotiation:
     * "Schedule 8 executives for Q1 planning next week - many have conflicts" (no common availability)
     * "Land time with global team across Seattle, London, Tokyo, Sydney - need everyone present" (timezone conflicts)
     * "Schedule board meeting - work around all 6 board members' schedules" (multiple VIP constraints)
   - **Expected Behavior**: CAN-24 should trigger poll/voting mechanism, propose compromises, iterate until solution found
   - **Validates**: CAN-24 as fallback mechanism when deterministic scheduling fails

2. **Create Adversarial Test Cases**:
   - Ambiguous prompts that could trigger multiple tasks
   - Edge cases with conflicting constraints
   - Cross-category prompts (Organizer + Schedule + Collaborate hybrid)

3. **Strengthen CAN-05 Detection**:
   - Document explicit triggers: team references, role references, name placeholders
   - Add CAN-05 detection rules to LLM evaluation prompts
   - Validate improved detection with Schedule-2, Collaborate-1, Collaborate-2

4. **Document Design Principles**:
   - Formalize "meeting goals vs system tasks" with examples
   - Create decision tree for CAN-09 vs CAN-23 (document vs agenda generation)
   - Document CAN-16 vs CAN-25 distinction (monitoring vs annotation)

4. **Optimize Low Performers**:
   - Collaborate-1 (50% F1): Clarify CAN-18 scope, add CAN-05 detection
   - Schedule-2 (88.89% F1): Improve CAN-06 detection; CAN-05 correctly removed

5. **Multi-Model Validation**:
   - Benchmark Claude 3.5 Sonnet against gold standard
   - Benchmark GPT-4 Turbo against gold standard
   - Benchmark Gemini Pro against gold standard
   - Compare model performance, identify systematic differences

6. **Real-World Validation**:
   - Deploy framework in production system
   - Collect user feedback on task decomposition accuracy
   - Identify production edge cases not covered by hero prompts
   - Iterate framework based on production learnings

---

## Part 5: Document Metadata

**Document Information**:
- **Title**: V2 Gold Standard Reference - 9 Hero Prompts with Human Validation
- **Version**: 2.1
- **Created**: November 7, 2025
- **Last Updated**: November 8, 2025
- **Author**: Chin-Yew Lin
- **Framework**: Calendar.AI Canonical Unit Tasks V2.0 (25 tasks)

**Scope**:
- **Total Prompts**: 9 (3 Organizer, 3 Schedule, 3 Collaborate)
- **Total Tasks**: 25 (CAN-01 through CAN-25)
- **Tasks Used**: 22 (88% framework coverage)
- **Evaluation Status**: 6 correct, 3 partial
- **Gold Standard Revisions**: 2 (Collaborate-1 CAN-09→23, Schedule-2 CAN-23→17)
- **NEW Tasks**: 1 (CAN-25: Event Annotation/Flagging)

**Validation**:
- ✅ 100% human expert review (Chin-Yew Lin)
- ✅ All 9 prompts validated against GPT-5 outputs
- ✅ Task boundaries refined through human evaluation
- ✅ Execution compositions documented for all prompts
- ✅ Example flows with concrete data provided
- ✅ NEW CAN-25 validated with 100% detection rate

**Related Documents**:
1. `v2_gold_standard_v2_20251107.json` - Source data (revised with both gold standard changes)
2. `CANONICAL_TASKS_GOLD_STANDARD_REFERENCE_V2.md` - Detailed reference (2,840 lines, version 2.1)
3. `GOLD_STANDARD_REPORT_WRITING_GUIDE.md` - Report format specification (829 lines)
4. `GPT5_V2_OPTIMIZATION_SUMMARY.md` - GPT-5 validation results (3-trial stability test)
5. `FRAMEWORK_V2.0_SPECIFICATION.md` - Complete framework specification

**Usage**:

This document serves as the authoritative reference for:

1. **LLM Evaluation**: 
   - Benchmark GPT-5, Claude, GPT-4, and other models
   - Ground truth for task decomposition accuracy
   - Compare model outputs against human-validated decompositions

2. **Training Data**:
   - Fine-tuning datasets for task decomposition models
   - Prompt engineering examples
   - Task selection patterns and orchestration strategies

3. **Framework Validation**:
   - Validate canonical tasks framework completeness
   - Identify task boundary ambiguities
   - Test framework coverage across use cases

4. **Production QA**:
   - Reference standard for production system accuracy
   - Regression testing baseline
   - Quality assurance validation

5. **Implementation Planning**:
   - 4-phase priority roadmap based on task frequency
   - Task dependency identification
   - Orchestration pattern templates

**Maintenance Protocol**:

Update this document when:
- Canonical tasks framework evolves (new tasks, task splits, renumbering)
- New hero prompts are created or discovered
- Production system reveals edge cases or ambiguities
- Gold standard revisions are made through human evaluation
- Framework validation results change (new model evaluations)

**Quality Checklist**:
- ✅ All 9 prompts have complete task decomposition (Purpose, Input, Output, Tier, Dependencies, Notes)
- ✅ All 9 prompts have execution compositions (step-by-step workflows)
- ✅ All 9 prompts have key orchestration patterns documented
- ✅ All 9 prompts have example flows with concrete data
- ✅ All evaluation statuses documented (correct/partial + F1 scores)
- ✅ Human evaluator notes included for partial prompts
- ✅ Gold standard revisions documented with rationale
- ✅ NEW CAN-25 validated and documented
- ✅ Cross-prompt analysis completed (task usage matrix)
- ✅ Key findings documented with evidence
- ✅ Implementation priority roadmap provided
- ✅ Future work recommendations actionable

**Status**: ✅ **Gold Standard Reference (Production-Ready)**

---

*End of Document*
