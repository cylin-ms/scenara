# Hero Prompts Canonical Task Analysis - Gold Standard Reference V2.0

**Document Version**: 2.0  
**Date**: November 7, 2025  
**Author**: Chin-Yew Lin  
**Framework**: Calendar.AI Canonical Unit Tasks Framework V2.0 (25 tasks - renumbered CAN-01 through CAN-25)  
**Source**: Human-validated gold standard evaluation  
**Evaluation File**: `v2_gold_standard_20251107_145124.json`

**Related Documents**:
- [GPT5_V2_OPTIMIZATION_SUMMARY.md](model_comparison/GPT5_V2_OPTIMIZATION_SUMMARY.md) - GPT-5 3-trial stability test results
- [v2_gold_standard_v2_20251107.json](v2_gold_standard_v2_20251107.json) - Updated gold standard with V2.0 numbering
- [CANONICAL_TASKS_REFERENCE_V2.md](CANONICAL_TASKS_REFERENCE_V2.md) - Complete 25-task framework specifications
- [GOLD_STANDARD_REPORT_WRITING_GUIDE.md](GOLD_STANDARD_REPORT_WRITING_GUIDE.md) - Report format standards

---

## Document Summary

### Purpose

This document provides the **gold standard canonical task analysis** for the 9 Calendar.AI hero prompts, serving as the authoritative reference for:

1. **LLM Evaluation**: Benchmark model performance in task decomposition (GPT-5, Claude, etc.)
2. **Framework Validation**: Validate the 25 canonical unit tasks V2.0 framework
3. **Training Data**: Ground truth for fine-tuning and prompt optimization
4. **Quality Assurance**: Reference standard for production system validation

### Methodology

This gold standard was created through a rigorous 4-phase process:

#### Phase 1: Framework Development (October-November 2025)
- **Original Framework**: 24 canonical tasks with human evaluation insights
- **Task Evolution**: CAN-02A/CAN-02B renumbered to CAN-02/CAN-03 for clarity
- **NEW Task Addition**: CAN-25 (Event Annotation/Flagging) identified from evaluation needs

#### Phase 2: GPT-5 Baseline Analysis (November 7, 2025)
- **Automated Analysis**: GPT-5 analyzed all 9 hero prompts using optimized V2.0 prompts
- **Performance**: Initial decomposition baseline established
- **Key Findings**:
  - CAN-05 (Attendee Resolution) often missed in automated analysis
  - CAN-18 (Risk Anticipation) scope ambiguity detected
  - CAN-25 (Event Flagging) not yet in framework

#### Phase 3: Human Evaluation (November 7, 2025)
- **Manual Review**: Expert (Chin-Yew Lin) reviewed all GPT-5 outputs
- **Corrections Applied**:
  - Added CAN-25 to Organizer-2 ("flag meetings" requirement)
  - Added missing CAN-05 to Schedule-2 and Collaborate-2
  - Removed CAN-18 from Collaborate-1 (over-interpretation of meeting goals)
  - Added CAN-16 to Organizer-2 ("track" requirement)
- **Validation**: Cross-referenced with original prompt requirements
- **Results**: 5 correct, 3 partial, 1 needs review (out of 9 prompts)

#### Phase 4: Gold Standard Creation (November 7, 2025)
- **Final Documentation**: This comprehensive reference document
- **Execution Composition**: Detailed workflows showing how tasks orchestrate
- **Example Flows**: Concrete scenarios with realistic data
- **Framework Update**: V2.0 framework finalized with 25 tasks

### Gold Standard Statistics

| Metric | Value |
|--------|-------|
| **Total Prompts** | 9 |
| **Total Canonical Tasks** | 25 (CAN-01 through CAN-25) |
| **Tasks Used** | 22 (88% framework coverage) |
| **Average Tasks/Prompt** | 7.2 |
| **Tier 1 (Universal) Coverage** | 100% (all 5 universal tasks used) |
| **Tier 2 (Common) Coverage** | 89% (8 of 9 common tasks used) |
| **Tier 3 (Specialized) Coverage** | 80% (8 of 10 specialized tasks used) |
| **Task Usage Range** | 3-10 tasks per prompt |

**Human Evaluation Results**:
- ✅ **Correct**: 5 prompts (Organizer-1, Organizre-3, Schedule-1, Schedule-3, Collaborate-3)
- ⚠️ **Partial**: 3 prompts (Organizer-2, Schedule-2, Collaborate-2) - missing specific tasks
- ❓ **Needs Review**: 1 prompt (Collaborate-1) - over-interpretation issue

**Key Insights from Evaluation**:
1. **NEW Task Validated**: CAN-25 for event annotation/flagging (Organizer-2: "flag meetings")
2. **CAN-05 Critical**: Attendee resolution often missed but essential (Schedule-2, Collaborate-2)
3. **CAN-18 Scope**: Risk anticipation vs discussion goals (Collaborate-1 over-interpretation)
4. **CAN-16 Usage**: Event monitoring for "track" use case (Organizer-2)

---

## Task Frequency Distribution

| Task ID | Task Name | Frequency | Prompts Using |
|---------|-----------|-----------|---------------|
| CAN-04 | Natural Language Understanding | 100% | 9/9 (ALL) |
| CAN-01 | Calendar Events Retrieval | 100% | 9/9 (ALL) |
| CAN-07 | Meeting Metadata Extraction | 78% | 7/9 |
| CAN-05 | Attendee/Contact Resolution | 67% | 6/9 |
| CAN-02 | Meeting Type Classification | 56% | 5/9 |
| CAN-03 | Meeting Importance Assessment | 56% | 5/9 |
| CAN-09 | Document Generation/Formatting | 56% | 5/9 |
| CAN-12 | Constraint Satisfaction | 44% | 4/9 |
| CAN-06 | Availability Checking | 33% | 3/9 |
| CAN-08 | Document/Content Retrieval | 22% | 2/9 |
| CAN-13 | RSVP Status Update | 22% | 2/9 |
| CAN-11 | Priority/Preference Matching | 22% | 2/9 |
| CAN-14 | Recommendation Engine | 11% | 1/9 |
| CAN-15 | Recurrence Rule Generation | 11% | 1/9 |
| CAN-16 | Event Monitoring/Change Detection | 11% | 1/9 |
| CAN-17 | Automatic Rescheduling | 11% | 1/9 |
| CAN-18 | Objection/Risk Anticipation | 11% | 1/9 |
| CAN-19 | Resource Booking | 11% | 1/9 |
| CAN-20 | Data Visualization/Reporting | 11% | 1/9 |
| CAN-21 | Focus Time/Preparation Time Analysis | 11% | 1/9 |
| CAN-22 | Research/Intelligence Gathering | 11% | 1/9 |
| CAN-23 | Agenda Generation/Structuring | 11% | 1/9 |
| **CAN-25** | **Event Annotation/Flagging (NEW)** | **11%** | **1/9 (Organizer-2)** |

**Unused Tasks**: CAN-24 (Multi-party Coordination/Negotiation) - 0% frequency

---

## Hero Prompt 1: Organizer-1

**Prompt**: "Keep my Calendar up to date by committing to only meetings that are part of my priorities."

**Category**: Organizer  
**Capabilities Required**: Meeting prioritization, RSVP management based on user priorities  
**Evaluation**: ✅ **Correct**

### Canonical Task Decomposition: 7 Tasks

#### Task 1: Natural Language Understanding (CAN-04)
- **Purpose**: Extract user intent (keep calendar updated, commit to priority meetings only) and priorities
- **Input**: User prompt text
- **Output**: Structured constraints: {"intent": "manage_calendar_based_on_priorities", "priorities": ["user's stated priorities"]}
- **Tier**: 1 (Universal)
- **Note**: Universal first step - always needed to parse natural language

#### Task 2: Calendar Events Retrieval (CAN-01)
- **Purpose**: Retrieve pending calendar invitations and existing meetings
- **Input**: Time range (current/upcoming)
- **Output**: List of calendar events with RSVP status
- **Tier**: 1 (Universal)
- **Dependencies**: CAN-04 (NLU extracts time range)

#### Task 3: Meeting Metadata Extraction (CAN-07)
- **Purpose**: Extract RSVP status, attendees, meeting details for pending invitations
- **Input**: Calendar events from CAN-01
- **Output**: Detailed metadata including RSVP status, attendees, subject, organizer
- **Tier**: 2 (Common)
- **Note**: Parent task - enables CAN-13 (RSVP update)

#### Task 4: Meeting Type Classification (CAN-02)
- **Purpose**: Classify meetings by format (1:1, team sync, customer meeting, etc.)
- **Input**: Meeting metadata from CAN-07
- **Output**: Meeting type classification for each event
- **Tier**: 1 (Universal)
- **Note**: Objective, format-based classification

#### Task 5: Meeting Importance Assessment (CAN-03)
- **Purpose**: Assess strategic importance and alignment with user priorities
- **Input**: Meeting metadata + user priorities from CAN-04
- **Output**: Importance scores and priority alignment
- **Tier**: 1 (Universal)
- **Note**: Subjective, value-based assessment - pairs with CAN-02

#### Task 6: Priority/Preference Matching (CAN-11)
- **Purpose**: Match meetings against user's stated priorities
- **Input**: Meetings with classifications + user priorities
- **Output**: Priority-aligned meeting list
- **Tier**: 2 (Common)

#### Task 7: RSVP Status Update (CAN-13)
- **Purpose**: Update RSVP status (accept priority meetings, decline/tentative others)
- **Input**: Prioritized meeting list from CAN-11
- **Output**: RSVP updates sent to calendar system
- **Tier**: 2 (Common)
- **Dependencies**: CAN-07 (metadata extraction provides current RSVP status)

**Evaluation Criteria**:
- RSVP decision accuracy aligned with user priorities
- Meeting type classification precision (% correctly classified)
- Priority matching correctness (alignment score)
- RSVP update execution success rate (% completed without errors)

### Execution Composition

**How Tasks Work Together to Answer the Prompt:**

```
STEP 1: Understand User Intent
CAN-04 (NLU) → Extract user priorities and time constraints
  - Parse: "keep calendar up to date", "commit to only meetings", "part of my priorities"
  - Output: {"intent": "manage_calendar_based_on_priorities", "priorities": [user-stated priorities], "time_window": "ongoing"}

STEP 2: Retrieve Pending Invitations
CAN-01 (Calendar Retrieval) → Load all pending calendar invitations
  - Filter: RSVP status = "pending" OR "tentative"
  - Time range: Current + upcoming meetings
  - Output: Array of calendar events awaiting response

STEP 3: Extract Meeting Details
CAN-07 (Metadata Extraction) → Extract comprehensive meeting information
  - For each invitation: attendees, subject, organizer, agenda, RSVP status, date/time
  - Output: Enriched meeting objects with full metadata

STEP 4-5: Classify Meetings (Parallel Processing)
CAN-02 (Meeting Type) → Classify by format
  - Categories: 1:1, team sync, customer meeting, all-hands, executive review, etc.
  - Objective classification based on attendee count, recurring pattern, subject keywords

CAN-03 (Importance Assessment) → Score strategic value
  - Evaluate: Attendee seniority, business impact, strategic alignment
  - Score: High/Medium/Low importance
  - Subjective assessment based on meeting context

STEP 6: Match Against Priorities
CAN-11 (Priority Matching) → Align meetings with user priorities
  - Compare: Meeting type + importance against user's stated priorities
  - Calculate: Priority alignment scores (0-100%)
  - Rank: Meetings by priority match strength

STEP 7: Execute RSVP Actions
CAN-13 (RSVP Update) → Update calendar responses
  - Accept: High priority matches (>80% alignment)
  - Tentative: Medium priority matches (40-80% alignment)
  - Decline: Low priority matches (<40% alignment)
  - Write: RSVP status to calendar system

OUTPUT: Updated calendar with prioritized commitments
  - Accepted meetings: Those aligned with user priorities
  - Declined meetings: Those not aligned (with justification)
  - Calendar kept current: Only priority-aligned meetings committed
```

**Key Orchestration Patterns**:
- **Sequential Foundation**: CAN-04 → CAN-01 → CAN-07 (linear dependency chain)
- **Parallel Classification**: CAN-02 and CAN-03 can run concurrently on same meeting data
- **Parent-Child Relationship**: CAN-07 (Metadata Extraction) enables CAN-13 (RSVP Update)
- **Decision Point**: CAN-11 (Priority Matching) determines which meetings get accepted/declined
- **Write Operation**: CAN-13 is the only task that modifies calendar state

**Example Flow - Priority-Based RSVP Decision**:

```
User Context:
  - Stated Priorities: ["customer meetings", "product strategy"]
  - Pending Invitation: "Q4 Planning Meeting with Marketing Team"

CAN-04: Extract user intent ✓
  → priorities: ["customer meetings", "product strategy"]
  → intent: manage calendar based on priorities

CAN-01: Retrieved 3 pending invitations ✓
  1. "Q4 Planning Meeting with Marketing Team" (tentative)
  2. "Customer Discovery Call - Contoso" (pending)
  3. "1:1 with Product Manager - Strategy Review" (pending)

CAN-07: Extract metadata for each invitation ✓
  Meeting 1: Attendees: [Marketing Team (8 people)], Subject: "Q4 Planning", Organizer: Marketing VP
  Meeting 2: Attendees: [Contoso VP, Account Manager], Subject: "Discovery Call", Organizer: Sales
  Meeting 3: Attendees: [Product Manager], Subject: "Strategy Review", Organizer: Product Manager

CAN-02: Classify meeting types ✓
  Meeting 1: Type = "Internal Team Meeting" (8+ attendees, internal)
  Meeting 2: Type = "Customer Meeting" (external attendees, customer domain)
  Meeting 3: Type = "1:1 - Product Strategy" (2 people, strategy topic)

CAN-03: Assess importance ✓
  Meeting 1: Importance = "Medium" (planning session, not customer-facing)
  Meeting 2: Importance = "High" (VP-level customer meeting)
  Meeting 3: Importance = "High" (product strategy discussion)

CAN-11: Match against priorities ✓
  Meeting 1: Priority Match = 30% (not customer or product strategy)
  Meeting 2: Priority Match = 95% (customer meeting - direct match!)
  Meeting 3: Priority Match = 90% (product strategy - direct match!)

CAN-13: Execute RSVP updates ✓
  Meeting 1: DECLINE (low priority match)
    → Reason: "Doesn't align with your priorities (customer meetings, product strategy)"
  Meeting 2: ACCEPT (high priority match)
    → Reason: "High priority - customer meeting with VP"
  Meeting 3: ACCEPT (high priority match)
    → Reason: "High priority - product strategy discussion"

OUTPUT to User:
  ✅ Accepted: "Customer Discovery Call - Contoso" (aligns with 'customer meetings')
  ✅ Accepted: "1:1 with Product Manager - Strategy Review" (aligns with 'product strategy')
  ❌ Declined: "Q4 Planning Meeting with Marketing Team" (doesn't align with priorities)
  
Calendar Status: Up to date with only priority-aligned meetings committed ✓
```

---

## Hero Prompt 2: Organizer-2

**Prompt**: "Track all my important meetings and flag any that require focus time to prepare for them."

**Category**: Organizer  
**Capabilities Required**: Meeting tracking, importance assessment, preparation time estimation, event flagging  
**Evaluation**: ⚠️ **Partial** - Missing CAN-25 (Event Annotation/Flagging)

**Human Evaluator Notes**: 
> "Missing 'track important meetings' and 'flag meetings need time for preparation'. Can we attribute 'track' to CAN-16? But we do not have any Canonical task for 'flag'. 'Flag' is an action that we add an annotation to an event on calendar. We need to add new canonical tasks for similar tasks that signal something on calendar if some predefined condition occurs."

### Canonical Task Decomposition: 9 Tasks (Including NEW CAN-25)

#### Task 1: Natural Language Understanding (CAN-04)
- **Purpose**: Extract intent (track important meetings, flag prep-time meetings)
- **Input**: User prompt text
- **Output**: {"intent": "track_and_flag_meetings", "criteria": "important", "flag_condition": "requires_prep_time"}
- **Tier**: 1 (Universal)

#### Task 2: Calendar Events Retrieval (CAN-01)
- **Purpose**: Retrieve upcoming meetings to track
- **Input**: Time range (this week/upcoming)
- **Output**: List of calendar events
- **Tier**: 1 (Universal)

#### Task 3: Meeting Metadata Extraction (CAN-07)
- **Purpose**: Extract meeting details (attendees, subject, complexity indicators)
- **Input**: Calendar events from CAN-01
- **Output**: Meeting metadata including attachments, agenda, attendees
- **Tier**: 2 (Common)

#### Task 4: Meeting Type Classification (CAN-02)
- **Purpose**: Classify meeting formats to assess complexity
- **Input**: Meeting metadata from CAN-07
- **Output**: Meeting type (1:1, team, customer, executive review, etc.)
- **Tier**: 1 (Universal)

#### Task 5: Meeting Importance Assessment (CAN-03)
- **Purpose**: Assess which meetings are "important" based on context
- **Input**: Meeting metadata + classifications
- **Output**: Importance scores identifying important meetings
- **Tier**: 1 (Universal)

#### Task 6: Focus Time/Preparation Time Analysis (CAN-21)
- **Purpose**: Estimate prep time needed based on meeting type, attendees, complexity
- **Input**: Meeting metadata + type classification
- **Output**: Prep time estimates (e.g., "90 min prep for executive review")
- **Tier**: 3 (Specialized)
- **Note**: NEW task usage for prep time estimation

#### Task 7: Priority/Preference Matching (CAN-11)
- **Purpose**: Filter to "important meetings" based on user criteria
- **Input**: Meetings with importance scores
- **Output**: Filtered list of important meetings
- **Tier**: 2 (Common)

#### Task 8: Event Monitoring/Change Detection (CAN-16)
- **Purpose**: Setup tracking/monitoring for important meetings
- **Input**: Important meetings list from CAN-11
- **Output**: Monitoring configuration for changes, updates, cancellations
- **Tier**: 3 (Specialized)
- **Note**: Addresses "track" requirement

#### Task 9: Event Annotation/Flagging (CAN-25) - **NEW IN V2.0**
- **Purpose**: Flag meetings that require prep time with visual indicators
- **Input**: Meetings with prep time estimates from CAN-21
- **Output**: Event annotations/flags added to calendar (e.g., "⚠️ 90 min prep needed")
- **Tier**: 3 (Specialized)
- **Note**: **NEW CANONICAL TASK** - Addresses "flag any that require focus time" requirement

**Evaluation Criteria**:
- Importance classification accuracy (% of truly important meetings identified)
- Prep time estimation reasonableness (realistic time allocations)
- Flagging precision (only flag meetings actually requiring prep)
- Tracking setup completeness (monitoring configured for all important meetings)
- CAN-25 correctness (NEW task appropriately applied for flagging)

### Execution Composition

**How Tasks Work Together to Answer the Prompt:**

```
STEP 1: Understand Tracking and Flagging Requirements
CAN-04 (NLU) → Extract dual intent
  - Parse: "track all my important meetings" = monitoring requirement
  - Parse: "flag any that require focus time to prepare" = conditional annotation
  - Output: {"intent": ["track_meetings", "flag_prep_required"], "criteria": "important", "flag_condition": "requires_focus_time"}

STEP 2: Retrieve Upcoming Meetings
CAN-01 (Calendar Retrieval) → Load calendar for analysis period
  - Time range: Next 2-4 weeks (typical planning horizon)
  - Filter: All scheduled meetings (not just pending)
  - Output: Array of upcoming calendar events

STEP 3: Extract Meeting Context
CAN-07 (Metadata Extraction) → Extract complexity indicators
  - For each meeting: attendees, subject, organizer, agenda, attachments, meeting notes
  - Complexity signals: Agenda length, attachment count, attendee seniority
  - Output: Enriched meeting objects with preparation context

STEP 4-5: Classify and Score Meetings (Parallel Processing)
CAN-02 (Meeting Type) → Classify by format
  - Categories: 1:1, team sync, customer meeting, exec review, board meeting, all-hands
  - High-prep types: Executive reviews, board meetings, customer presentations

CAN-03 (Importance Assessment) → Score strategic value
  - Evaluate: Attendee seniority (VP+, C-level), business impact, customer-facing
  - Output: Importance ratings (Critical, High, Medium, Low)

STEP 6: Estimate Preparation Time
CAN-21 (Preparation Time Analysis) → Calculate prep time needed
  - Input: Meeting type + importance + complexity signals
  - Logic: 
    - Executive review with attachments = 90-120 min prep
    - Customer presentation = 60-90 min prep
    - Board meeting = 2-4 hours prep
    - Regular 1:1 = 0-15 min prep
  - Output: Prep time estimates per meeting

STEP 7: Filter to Important Meetings
CAN-11 (Priority Matching) → Select meetings to track
  - Criteria: Importance = "Critical" OR "High"
  - Output: Filtered list of important meetings requiring tracking

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
  - Meetings requiring prep time visually flagged
  - User can see at-a-glance which meetings need preparation focus time
```

**Key Orchestration Patterns**:
- **Sequential Foundation**: CAN-04 → CAN-01 → CAN-07 (linear dependency)
- **Parallel Classification**: CAN-02 and CAN-03 analyze same metadata concurrently
- **Prep Time Gate**: CAN-21 must complete before CAN-25 (flagging depends on estimates)
- **Parallel Finalization**: CAN-16 (tracking) and CAN-25 (flagging) are independent operations
- **Conditional Logic**: CAN-25 only flags IF prep_time > threshold (conditional execution)
- **NEW Task Pattern**: CAN-25 introduces event annotation capability (V2.0 framework addition)

**Example Flow - Meeting Tracking and Flagging**:

```
User Request: "Track all my important meetings and flag any that require focus time to prepare for them."

CAN-04: Parse requirements ✓
  → track: important meetings
  → flag: meetings requiring focus time for prep
  → criteria: importance + prep time needed

CAN-01: Retrieved 12 upcoming meetings ✓
  1. "Weekly 1:1 with Direct Report" (30 min, Monday)
  2. "Q4 Business Review with CEO" (60 min, Wednesday)
  3. "Customer Presentation - Contoso" (90 min, Thursday)
  4. "Team Standup" (15 min, Daily)
  5. "Board of Directors Meeting" (120 min, Friday)
  ... (7 more meetings)

CAN-07: Extract metadata ✓
  Meeting 2: Attendees: [CEO, CFO, VP Ops], Agenda: 15-page deck attached, Notes: "Prepare revenue projections"
  Meeting 3: Attendees: [Contoso VP, CTO, Account Team], Agenda: "Product demo", Attachments: Demo script, slides
  Meeting 5: Attendees: [Board members (6)], Agenda: "Quarterly board review", Attachments: Board packet (50 pages)

CAN-02: Classify types ✓
  Meeting 1: "1:1 - Management"
  Meeting 2: "Executive Review"  
  Meeting 3: "Customer Presentation"
  Meeting 4: "Team Sync"
  Meeting 5: "Board Meeting"

CAN-03: Assess importance ✓
  Meeting 1: Medium (routine 1:1)
  Meeting 2: CRITICAL (CEO, financial review)
  Meeting 3: HIGH (customer VP, product demo)
  Meeting 4: Low (daily standup)
  Meeting 5: CRITICAL (board governance)

CAN-21: Estimate prep time ✓
  Meeting 1: 15 min (review notes)
  Meeting 2: 120 min (prepare projections, review 15-page deck)
  Meeting 3: 90 min (rehearse demo, review script)
  Meeting 4: 0 min (no prep needed)
  Meeting 5: 240 min (review 50-page packet, prepare responses)

CAN-11: Filter to important meetings ✓
  Important meetings identified: 2 (Q4 Business Review), 3 (Customer Presentation), 5 (Board Meeting)
  → 3 meetings selected for tracking

CAN-16: Setup monitoring ✓
  → Tracking enabled for meetings 2, 3, 5
  → Alerts configured for cancellations, reschedules, attendee changes

CAN-25: Flag meetings needing prep time ✓ (NEW TASK)
  Meeting 2: Prep time 120 min > 30 min threshold → FLAG ⚠️
    → Added annotation: "⚠️ 120 min prep needed - Review deck & prepare projections"
  Meeting 3: Prep time 90 min > 30 min threshold → FLAG ⚠️
    → Added annotation: "⚠️ 90 min prep needed - Rehearse demo & review script"
  Meeting 5: Prep time 240 min > 30 min threshold → FLAG ⚠️
    → Added annotation: "⚠️ 240 min prep needed - Review board packet (50 pages)"

OUTPUT to User:
  ✅ Tracking 3 important meetings (Q4 Business Review, Customer Presentation, Board Meeting)
  ✅ Change monitoring active (will alert on cancellations/reschedules)
  ✅ 3 meetings flagged for prep time:
     ⚠️ Wed - Q4 Business Review: 120 min prep needed
     ⚠️ Thu - Customer Presentation: 90 min prep needed  
     ⚠️ Fri - Board Meeting: 240 min prep needed (schedule focus time!)

**Key Insight**: CAN-25 (Event Annotation/Flagging) is a NEW canonical task created specifically for this use case. The "flag any that require focus time" requirement couldn't be satisfied by existing tasks - it needed a new capability for conditional event annotation based on computed conditions.
```

---

## Hero Prompt 3: Organizre-3

**Prompt**: "Help me understand where I am spending my time and identify ways I can reclaim time to focus more on my top priorities."

**Category**: Organizer  
**Capabilities Required**: Time analysis, pattern identification, recommendation generation, data visualization  
**Evaluation**: ✅ **Correct**

### Canonical Task Decomposition: 9 Tasks

#### Task 1: Natural Language Understanding (CAN-04)
- **Purpose**: Extract intent (time analysis, reclamation recommendations)
- **Input**: User prompt text
- **Output**: {"intent": "analyze_time_and_recommend_reclamation", "priorities": ["top priorities"]}
- **Tier**: 1 (Universal)

#### Task 2: Calendar Events Retrieval (CAN-01)
- **Purpose**: Retrieve historical and upcoming meetings for analysis
- **Input**: Time range (past month/quarter + upcoming)
- **Output**: Complete meeting dataset for analysis
- **Tier**: 1 (Universal)

#### Task 3: Meeting Metadata Extraction (CAN-07)
- **Purpose**: Extract meeting details for categorization
- **Input**: Calendar events from CAN-01
- **Output**: Detailed metadata (attendees, duration, type, recurrence)
- **Tier**: 2 (Common)

#### Task 4: Meeting Type Classification (CAN-02)
- **Purpose**: Classify meetings by format for time breakdown
- **Input**: Meeting metadata from CAN-07
- **Output**: Meeting type classifications (1:1, team, customer, etc.)
- **Tier**: 1 (Universal)

#### Task 5: Meeting Importance Assessment (CAN-03)
- **Purpose**: Assess importance to identify reclamation candidates
- **Input**: Meetings with type classifications
- **Output**: Importance scores (low-priority meetings = reclamation targets)
- **Tier**: 1 (Universal)

#### Task 6: Time Aggregation/Statistical Analysis (CAN-10)
- **Purpose**: Aggregate time spent by meeting type, importance, attendees
- **Input**: Classified meetings with metadata
- **Output**: Time breakdown statistics (e.g., "15 hours/week in team syncs")
- **Tier**: 2 (Common)
- **Note**: Critical for "understand where I am spending my time"

#### Task 7: Priority/Preference Matching (CAN-11)
- **Purpose**: Match meetings against user's top priorities
- **Input**: Meetings + user priorities from CAN-04
- **Output**: Priority alignment analysis
- **Tier**: 2 (Common)

#### Task 8: Recommendation Engine (CAN-14)
- **Purpose**: Generate recommendations for time reclamation
- **Input**: Time analysis + low-priority meetings
- **Output**: Actionable recommendations (decline, delegate, shorten, consolidate)
- **Tier**: 2 (Common)
- **Note**: Addresses "identify ways I can reclaim time"

#### Task 9: Data Visualization/Reporting (CAN-20)
- **Purpose**: Create visual time breakdown (charts, graphs)
- **Input**: Time aggregation statistics from CAN-10
- **Output**: Visual dashboard showing time distribution
- **Tier**: 3 (Specialized)
- **Note**: Helps user "understand" through visualization

**Evaluation Criteria**:
- Time categorization accuracy (% of meetings correctly classified by type)
- Priority alignment scoring correctness (meetings properly matched to priorities)
- Recommendation actionability (% of suggestions user can realistically implement)
- Visualization clarity (dashboard effectively communicates time patterns)
- Reclamation opportunity identification (low-value time correctly identified)

### Execution Composition

**How Tasks Work Together to Answer the Prompt:**

```
STEP 1: Understand Analysis Requirements
CAN-04 (NLU) → Extract dual intent
  - Parse: "understand where I am spending my time" = time analysis requirement
  - Parse: "identify ways I can reclaim time" = optimization/recommendation requirement
  - Parse: "focus more on my top priorities" = priority-based filtering
  - Output: {"intent": ["time_analysis", "reclamation_recommendations"], "priorities": [user's top priorities], "timeframe": "historical_analysis"}

STEP 2: Retrieve Meeting History
CAN-01 (Calendar Retrieval) → Load comprehensive meeting dataset
  - Time range: Past 1-3 months (historical analysis) + upcoming 2 weeks
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
  - Categories: 1:1, team sync, customer meeting, planning, all-hands, admin, other
  - Pattern detection: Recurring vs ad-hoc
  - Output: Type classification for time bucketing

CAN-03 (Importance Assessment) → Score strategic value
  - Criteria: Business impact, attendee seniority, strategic alignment, customer-facing
  - Ratings: High-value (strategic), Medium-value (necessary), Low-value (reclaim candidates)
  - Output: Importance scores for filtering

STEP 6: Aggregate Time Patterns
CAN-10 (Time Aggregation) → Calculate time distribution statistics
  - By type: "30% in 1:1s, 25% in customer meetings, 20% in team syncs, 15% in planning, 10% admin"
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
  - Identify: Low-value recurring meetings (weekly admin reviews, status meetings)
  - Suggest: Decline, delegate, reduce frequency, shorten duration, consolidate
  - Prioritize: Highest-impact reclamation opportunities first
  - Output: Ranked list of actionable recommendations with time savings estimates

CAN-20 (Data Visualization) → Create visual dashboard
  - Pie chart: Time by meeting type
  - Bar chart: Hours per week over time (trending)
  - Heatmap: Meeting density by day/hour
  - Priority breakdown: High vs medium vs low value meetings
  - Output: Interactive visual dashboard

OUTPUT: Comprehensive time analysis and reclamation report
  1. WHERE TIME GOES: Breakdown by type, participant, priority (with visualizations)
  2. PATTERNS DETECTED: Recurring commitments, trending changes
  3. PRIORITY ALIGNMENT: Gap between current spend vs top priorities
  4. RECLAMATION OPPORTUNITIES: Specific recommendations to free up 5-10 hours/week
```

**Key Orchestration Patterns**:
- **Historical Analysis Focus**: All tasks operate on PAST data (1-3 months lookback) plus future scheduled
- **Parallel Classification**: CAN-02, CAN-03, CAN-07 process same events concurrently
- **Aggregation Pipeline**: CAN-10 (time stats) feeds both CAN-14 (recommendations) and CAN-20 (visualization)
- **Recommendation Filtering**: CAN-14 uses CAN-03 (importance) and CAN-11 (priority match) to identify reclamation targets
- **Dual Output**: CAN-14 (actionable text) + CAN-20 (visual dashboard) provide complementary insights
- **Most Complex Prompt**: Uses 9 tasks across all tiers - demonstrates full framework capabilities

**Example Flow - Time Analysis and Reclamation**:

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
  - 1:1s: 50 meetings (30 hours total)
  - Team syncs: 40 meetings (20 hours)
  - Customer meetings: 25 meetings (40 hours)
  - Planning sessions: 15 meetings (30 hours)
  - Admin meetings: 30 meetings (25 hours)
  - Other: 20 meetings (20 hours)

CAN-03: Assess importance ✓
  - High-value: 40 meetings (customer + strategy = 70 hours, 42%)
  - Medium-value: 70 meetings (team syncs + planning = 60 hours, 36%)
  - Low-value: 70 meetings (admin + some 1:1s = 35 hours, 22%)

CAN-10: Aggregate time statistics ✓
  By Type:
  - 1:1s: 30 hours (18%)
  - Customer meetings: 40 hours (24%) ← Aligns with priority!
  - Team syncs: 20 hours (12%)
  - Planning: 30 hours (18%)
  - Admin: 25 hours (15%) ← LOW VALUE!
  - Other: 20 hours (12%)
  
  By Priority Alignment:
  - Aligned with priorities: 70 hours (42%)
  - Necessary but not priorities: 60 hours (36%)
  - NOT aligned (reclaim candidates): 35 hours (22%)

CAN-11: Priority matching analysis ✓
  ✅ Customer meetings (40 hrs) - STRONG alignment with "customer meetings" priority
  ⚠️ Product strategy (only 15 hrs) - WEAK alignment despite being priority!
  ⚠️ Team development (1:1s 30 hrs) - MODERATE alignment
  ❌ Admin meetings (25 hrs) - NO alignment, reclaim target!

CAN-14: Generate reclamation recommendations ✓
  1. **Decline "Weekly Admin Review" (recurring)** → Reclaim 8 hours/month (96 hrs/year)
     - Rationale: Low-value recurring meeting, organizer is peer, can get updates via email
  
  2. **Shorten daily standup from 30→15 min** → Reclaim 5 hours/month (60 hrs/year)
     - Rationale: Team sync often runs over, strict timeboxing can work
  
  3. **Delegate 2 recurring 1:1s** → Reclaim 4 hours/month (48 hrs/year)
     - Rationale: Two team members are senior enough for skip-level reporting
  
  4. **Consolidate monthly planning meetings** → Reclaim 3 hours/month (36 hrs/year)
     - Rationale: Three separate planning meetings could be one combined session
  
  Total potential reclamation: 20 hours/month (240 hours/year!)

CAN-20: Create visual dashboard ✓
  → Pie chart: Time by type (shows 15% in admin = LOW VALUE)
  → Bar chart: Hours/week over 12 weeks (trending up - concerning!)
  → Priority alignment gauge: 42% aligned, 58% not aligned with priorities
  → Heatmap: Heavy meeting load Tue-Thu afternoons

OUTPUT to User:

📊 **WHERE YOU SPEND YOUR TIME** (Past 90 days):
- Customer meetings: 40 hrs (24%) ✅ ALIGNED WITH PRIORITIES
- Planning: 30 hrs (18%)
- 1:1s: 30 hrs (18%)
- Admin: 25 hrs (15%) ❌ LOW VALUE!
- Team syncs: 20 hrs (12%)
- Other: 20 hrs (12%)

📈 **PRIORITY ALIGNMENT ANALYSIS**:
- ✅ Strong: Customer meetings (24% of time, top priority)
- ⚠️ **GAP**: Product strategy (only 9% of time, but listed as top priority!)
- ⚠️ Moderate: Team development (18% in 1:1s)
- ❌ **MISALIGNMENT**: 22% of time in low-value admin/other

💡 **TIME RECLAMATION OPPORTUNITIES** (Ranked by impact):
1. Decline "Weekly Admin Review" → Save 96 hrs/year
2. Shorten daily standup 30→15 min → Save 60 hrs/year
3. Delegate 2 recurring 1:1s to senior leads → Save 48 hrs/year
4. Consolidate monthly planning → Save 36 hrs/year

**Total potential reclamation: 240 hours/year (6 full work weeks!)**

🎯 **RECOMMENDATION**: Use reclaimed time to increase product strategy focus (currently only 15 hrs vs 40 hrs in customer meetings). Gap analysis shows strategy is stated priority but under-represented in calendar.

[Visual Dashboard showing pie charts, trend lines, and priority alignment]
```

---
   ↓
Step 6: CAN-10 (Time Aggregation) - Compute time breakdowns
   ↓
Step 7: CAN-11 (Priority Match) - Analyze alignment with priorities
   ↓
Step 8-9: [PARALLEL] CAN-14 (Recommendations) + CAN-20 (Visualization)
```

**Orchestration Notes**:
- CAN-10 (Time Aggregation) is critical path for both CAN-14 and CAN-20
- CAN-14 and CAN-20 can generate in parallel (independent outputs)
- Final output combines recommendations + visual dashboard

---

## Hero Prompt 4: Schedule-1

**Prompt**: "Starting next week, I want a weekly 30-min 1:1 with {name}. Afternoons preferred, avoid Fridays. Automatically reschedule on declines or conflicts."

**Category**: Schedule  
**Capabilities Required**: Recurring meeting setup, constraint satisfaction, availability checking, automatic rescheduling  
**Evaluation**: ✅ **Correct**

### Canonical Task Decomposition: 9 Tasks

#### Task 1: Natural Language Understanding (CAN-04)
- **Purpose**: Extract scheduling constraints and preferences
- **Input**: User prompt text
- **Output**: {"duration": 30, "recurrence": "weekly", "attendee": "{name}", "preferences": ["afternoon", "avoid_friday"], "automation": "auto_reschedule"}
- **Tier**: 1 (Universal)

#### Task 2: Attendee/Contact Resolution (CAN-05)
- **Purpose**: Resolve "{name}" to directory entry
- **Input**: Attendee name from CAN-04
- **Output**: Full contact details (email, title, calendar access)
- **Tier**: 1 (Universal)
- **Note**: Must happen BEFORE availability checking

#### Task 3: Calendar Events Retrieval (CAN-01)
- **Purpose**: Retrieve existing calendar events to check for conflicts
- **Input**: Time range (next week + recurring future)
- **Output**: Existing meeting schedule
- **Tier**: 1 (Universal)

#### Task 4: Availability Checking (CAN-06)
- **Purpose**: Find available afternoon slots (avoiding Fridays)
- **Input**: Resolved attendee + constraints from CAN-04
- **Output**: List of available time slots matching preferences
- **Tier**: 2 (Common)
- **Dependencies**: CAN-05 (need attendee), CAN-01 (need existing schedule)

#### Task 5: Constraint Satisfaction (CAN-12)
- **Purpose**: Select optimal time slot satisfying all constraints
- **Input**: Available slots + preferences (afternoon, not Friday)
- **Output**: Best time slot (e.g., "Mondays 2pm")
- **Tier**: 2 (Common)

#### Task 6: Recurrence Rule Generation (CAN-15)
- **Purpose**: Generate RRULE for weekly recurrence
- **Input**: Selected time slot + "weekly" recurrence
- **Output**: RRULE pattern (e.g., "FREQ=WEEKLY;BYDAY=MO")
- **Tier**: 3 (Specialized)

#### Task 7: Calendar Event Creation/Update (CAN-03)
- **Purpose**: Create recurring meeting on calendar
- **Input**: Time slot + recurrence rule + attendee
- **Output**: Calendar event created with recurrence
- **Tier**: 1 (Universal)

#### Task 8: Event Monitoring/Change Detection (CAN-16)
- **Purpose**: Setup monitoring for declines and conflicts
- **Input**: Created recurring meeting
- **Output**: Webhook/monitoring configuration
- **Tier**: 3 (Specialized)
- **Note**: Enables automatic rescheduling trigger

#### Task 9: Automatic Rescheduling (CAN-17)
- **Purpose**: Automatically reschedule on declines/conflicts
- **Input**: Monitoring events from CAN-16
- **Output**: Rescheduling workflow triggered on decline/conflict
- **Tier**: 3 (Specialized)
- **Dependencies**: CAN-16 (monitoring must be active)

**Evaluation Criteria**:
- Constraint satisfaction accuracy (afternoon preference, avoid Friday correctly applied)
- Recurrence rule correctness (weekly RRULE properly formatted)
- Automation setup completeness (monitoring + auto-reschedule fully configured)
- Attendee resolution accuracy (correct person identified and scheduled)
- Conflict detection reliability (overlaps detected before scheduling)

### Execution Composition

**How Tasks Work Together to Answer the Prompt:**

```
STEP 1: Understand Scheduling Requirements
CAN-04 (NLU) → Extract scheduling constraints and automation preferences
  - Parse: "Starting next week" = start_date constraint
  - Parse: "weekly 30-min 1:1" = recurrence pattern + duration
  - Parse: "with {name}" = attendee requirement
  - Parse: "Afternoons preferred, avoid Fridays" = soft + hard time constraints
  - Parse: "Automatically reschedule on declines or conflicts" = automation requirement
  - Output: {"duration": 30, "recurrence": "weekly", "attendee": "{name}", "preferences": {"time": "afternoon", "avoid": ["friday"]}, "automation": ["auto_reschedule_on_decline", "auto_reschedule_on_conflict"]}

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
  - Include: User's calendar (for conflicts) + attendee's calendar (for availability)
  - Output: Complete calendar dataset for both parties

STEP 4: Check Attendee Availability
CAN-06 (Availability Checking) → Find afternoon slots avoiding Friday
  - Analyze: User + attendee calendars for free/busy times
  - Filter: Only afternoon slots (e.g., 12pm-5pm)
  - Exclude: All Friday slots (hard constraint)
  - Week-by-week: Check recurring availability pattern
  - Output: List of available afternoon slots ["Mon 2pm", "Tue 3pm", "Wed 2pm", "Thu 4pm"]

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
  - Attributes: Duration 30 min, recurring weekly, location TBD
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
  - On decline: Trigger CAN-06 (find new time) → CAN-12 (select) → CAN-03 (update)
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

**Key Orchestration Patterns**:
- **Sequential Dependency Chain**: CAN-05 → CAN-06 (must resolve attendee before checking their availability)
- **Recurrence Pipeline**: CAN-12 (select time) → CAN-15 (generate RRULE) → CAN-03 (create recurring event)
- **Automation Layer**: CAN-16 (monitoring) → CAN-17 (auto-reschedule) - real-time reactive workflow
- **Constraint Filtering**: CAN-06 applies hard constraints (afternoon, not Friday), CAN-12 applies soft preferences
- **Event-Driven Architecture**: CAN-17 subscribes to CAN-16 events for automatic execution
- **Most Specialized Prompt**: Uses 3 Tier-3 tasks (CAN-15, CAN-16, CAN-17) - demonstrates advanced capabilities

**Example Flow - Recurring 1:1 with Automated Rescheduling**:

```
User Request: "Starting next week, I want a weekly 30-min 1:1 with Sarah Chen. Afternoons preferred, avoid Fridays. Automatically reschedule on declines or conflicts."

CAN-04: Extract scheduling requirements ✓
  → duration: 30 min
  → recurrence: weekly
  → attendee: "Sarah Chen"
  → preferences: afternoon, avoid Friday
  → automation: auto-reschedule enabled

CAN-05: Resolve attendee ✓
  → Found: Sarah Chen (sarah.chen@company.com)
  → Title: Product Manager
  → Calendar access: ✓ Available
  → Timezone: PST (same as user)

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
  Duration: 30 minutes (2:00-2:30 PM)
  Recurrence: Weekly on Mondays
  Attendees: User + Sarah Chen
  Invitation sent: ✓ Awaiting Sarah's response

CAN-16: Setup monitoring ✓
  Webhooks configured:
  - Decline event: If Sarah declines any instance
  - Conflict event: If new meeting overlaps 1:1 time
  - Change event: If Sarah moves/cancels
  Event ID tracked: cal_evt_12345
  Monitoring status: 🟢 Active

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
- **Location**: TBD (Microsoft Teams link auto-generated)

✅ **AUTOMATION CONFIGURED**:
- **Monitoring**: Active for declines and conflicts
- **Auto-Rescheduling**: Enabled
  - If Sarah declines: System will automatically find new afternoon time (not Friday)
  - If conflict detected: System will automatically reschedule
  - Notifications: Both parties notified of any rescheduling

📧 **NEXT STEP**: Awaiting Sarah's acceptance

---

**SCENARIO: Sarah Declines First Instance** (Automation in Action)

3 days later: Sarah declines January 13 meeting

CAN-16: Detect decline event ✓
  → Webhook fired: sarah.chen@company.com declined cal_evt_12345_instance_1

CAN-17: Trigger auto-reschedule ✓
  → Re-run CAN-06: Find afternoon slots week of Jan 13 (not Friday)
  → Available: Tue Jan 14 3pm, Wed Jan 15 2pm
  → Re-run CAN-12: Select Wed Jan 15 2pm (better than Tue)
  → Re-run CAN-03: Update meeting to Wed Jan 15, 2:00 PM
  → Send notification to user and Sarah

Notification to User:
"Your 1:1 with Sarah Chen has been automatically rescheduled from Monday, Jan 13 at 2pm to Wednesday, Jan 15 at 2pm. Future occurrences remain on Mondays at 2pm."

**Key Insight**: CAN-17 (Automatic Rescheduling) creates a "self-healing" calendar - user never has to manually handle declines or conflicts. This is a sophisticated workflow requiring CAN-16 monitoring + full rescheduling pipeline (CAN-06 + CAN-12 + CAN-03) to execute automatically.
```

---

## Hero Prompt 5: Schedule-2

**Prompt**: "Clear my Thursday afternoon. Update my RSVPs and help me reschedule my meetings to another time and show me as {status}."

**Category**: Schedule  
**Capabilities Required**: Meeting rescheduling, RSVP management, availability checking, constraint satisfaction  
**Evaluation**: ⚠️ **Partial** - Missing CAN-05 (Attendee Resolution)

**Human Evaluator Notes**: 
> "The model needs to get metadata, and from there to find attendee for those meetings in the Thursday afternoon."

### Canonical Task Decomposition: 9 Tasks (Including CAN-05)

#### Task 1: Natural Language Understanding (CAN-04)
- **Purpose**: Extract rescheduling requirements
- **Input**: User prompt text
- **Output**: {"time_to_clear": "Thursday afternoon", "actions": ["update_rsvp", "reschedule", "set_status"], "status": "{status}"}
- **Tier**: 1 (Universal)

#### Task 2: Calendar Events Retrieval (CAN-01)
- **Purpose**: Retrieve Thursday afternoon meetings
- **Input**: Time range (Thursday afternoon)
- **Output**: List of meetings to be moved
- **Tier**: 1 (Universal)

#### Task 3: Meeting Metadata Extraction (CAN-07)
- **Purpose**: Extract RSVP status, attendees, meeting details
- **Input**: Thursday afternoon meetings from CAN-01
- **Output**: Detailed metadata for each meeting
- **Tier**: 2 (Common)
- **Note**: Critical for CAN-05 and CAN-13

#### Task 4: Attendee/Contact Resolution (CAN-05) - **MISSING IN ORIGINAL**
- **Purpose**: Resolve attendees for rescheduling coordination
- **Input**: Attendee lists from CAN-07
- **Output**: Full contact details for rescheduling notifications
- **Tier**: 1 (Universal)
- **Note**: **CRITICAL** - Needed to find attendees and check their availability

#### Task 5: RSVP Status Update (CAN-13)
- **Purpose**: Update RSVP status (decline or tentative)
- **Input**: Meetings from CAN-07 + user status preference
- **Output**: RSVP updates sent
- **Tier**: 2 (Common)
- **Dependencies**: CAN-07 (need current RSVP status)

#### Task 6: Availability Checking (CAN-06)
- **Purpose**: Find alternative time slots for rescheduling
- **Input**: Meeting attendees + duration
- **Output**: Available slots for rescheduled meetings
- **Tier**: 2 (Common)
- **Dependencies**: CAN-05 (need attendee calendars)

#### Task 7: Constraint Satisfaction (CAN-12)
- **Purpose**: Select best alternative times for each meeting
- **Input**: Available slots + user preferences
- **Output**: Optimal rescheduling times
- **Tier**: 2 (Common)

#### Task 8: Agenda Generation/Structuring (CAN-23)
- **Purpose**: Generate rescheduling plan/summary
- **Input**: Original meetings + new proposed times
- **Output**: Rescheduling proposal document
- **Tier**: 3 (Specialized)
- **Note**: Human evaluator noted this was included (unusual task usage)

#### Task 9: Calendar Event Creation/Update (CAN-03)
- **Purpose**: Update meeting times in calendar
- **Input**: Rescheduling plan from CAN-23
- **Output**: Calendar events updated to new times
- **Tier**: 1 (Universal)

**Evaluation Criteria**:
- RSVP update correctness (status correctly updated to decline/tentative)
- Attendee resolution completeness (all meeting participants identified)
- Availability detection accuracy (suitable alternative slots found)
- Rescheduling plan quality (proposed times work for all attendees)
- CAN-05 inclusion (CRITICAL - human evaluator identified this as missing dependency)

### Execution Composition

**How Tasks Work Together to Answer the Prompt:**

```
STEP 1: Understand Rescheduling Requirements
CAN-04 (NLU) → Parse multi-action request
  - Parse: "Clear my Thursday afternoon" = time block to free up
  - Parse: "Update my RSVPs" = change response status for affected meetings
  - Parse: "reschedule my meetings to another time" = find alternative slots
  - Parse: "show me as {status}" = set calendar status display
  - Output: {"clear_time": "Thursday afternoon", "actions": ["update_rsvp", "reschedule", "set_status"], "status": "{status}"}

STEP 2: Retrieve Thursday Afternoon Meetings
CAN-01 (Calendar Retrieval) → Load meetings in target time block
  - Time range: Thursday 12:00 PM - 5:00 PM (afternoon definition)
  - Filter: Meetings where user is attendee (not organizer-only)
  - Include: RSVP status, attendees, organizer, duration
  - Output: List of meetings to be cleared (e.g., 4 meetings in Thursday afternoon)

STEP 3: Extract Meeting Metadata
CAN-07 (Metadata Extraction) → Get detailed meeting information
  - For each meeting: Attendee lists, organizer, duration, recurrence, RSVP status
  - Extract: Meeting importance signals (customer meeting? 1:1? team sync?)
  - Extract: Flexibility indicators (recurring? organizer is peer? )
  - Purpose: Provide context for CAN-05 and CAN-13
  - Output: Enriched meeting objects with full metadata

STEP 4: Resolve All Attendees (CRITICAL - MISSING IN ORIGINAL)
CAN-05 (Attendee/Contact Resolution) → Resolve attendees for coordination
  - Input: Attendee lists from CAN-07 (names/emails)
  - Resolve: Full contact details, calendar URLs, timezones
  - Purpose: **ESSENTIAL** for CAN-06 availability checking (need attendee calendars!)
  - Output: Fully resolved attendee objects with calendar access

STEP 5-6: Update RSVPs and Find Alternative Slots (Parallel Processing)
CAN-13 (RSVP Status Update) → Decline or mark tentative
  - For each Thursday meeting: Update user's RSVP to "Declined" or "Tentative" (based on {status})
  - Send: RSVP update notifications to organizers
  - Purpose: Immediately free up Thursday afternoon slot
  - Output: RSVP updates sent for all 4 meetings

CAN-06 (Availability Checking) → Find alternative times for rescheduling
  - Input: Resolved attendees from CAN-05 + meeting durations from CAN-07
  - For each meeting: Check common availability across all attendees
  - Constraints: Avoid Thursday afternoon, find slots within next 1-2 weeks
  - Output: List of alternative time slots for each meeting

STEP 7: Select Best Alternative Times
CAN-12 (Constraint Satisfaction) → Apply preferences to select optimal slots
  - Preferences: Minimize attendee conflicts, respect user's calendar patterns
  - Logic: Earlier in week better, group similar meetings together
  - Validation: Ensure selected times don't conflict with existing commitments
  - Output: Optimal rescheduling plan (Meeting A → Mon 2pm, Meeting B → Tue 10am, etc.)

STEP 8: Generate Rescheduling Proposal
CAN-23 (Agenda/Document Generation) → Create rescheduling plan summary
  - Format: Structured document showing old time → new time for each meeting
  - Include: Rationale for each change (attendee availability, user preferences)
  - Include: Attendees for each meeting (for user review)
  - Purpose: Human evaluator noted this task for transparency/review
  - Output: Rescheduling proposal document

STEP 9: Update Calendar with New Times
CAN-03 (Event Creation/Update) → Execute rescheduling
  - For each meeting: Update meeting time to new slot
  - Send: Meeting update notifications to all attendees
  - Update: User's calendar status to {status} for original Thursday afternoon block
  - Output: Calendar events updated, Thursday afternoon now clear

OUTPUT: Thursday afternoon cleared with meetings rescheduled
  1. RSVP updates sent for all Thursday meetings
  2. Alternative times proposed and scheduled
  3. User's calendar shows {status} for Thursday afternoon
  4. All attendees notified of rescheduling
```

**Key Orchestration Patterns**:
- **Metadata Extraction Enabler**: CAN-07 provides critical input for both CAN-05 and CAN-13
- **MISSING TASK DEPENDENCY**: CAN-05 is ESSENTIAL - cannot check availability (CAN-06) without attendee calendars
- **Parallel RSVP + Availability**: CAN-13 and CAN-06 can run concurrently after CAN-05 completes
- **Human Review Layer**: CAN-23 generates proposal before CAN-03 executes (recommended for user confirmation)
- **Multi-Action Coordination**: Single prompt triggers 3 distinct actions (RSVP update, rescheduling, status setting)
- **Critical Human Evaluator Insight**: Original decomposition missed CAN-05 - human noted "model needs to get metadata, and from there to find attendee for those meetings"

**Example Flow - Clear Thursday Afternoon with Rescheduling**:

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
  - 4:00-5:00 PM: "Team Sprint Planning" (Entire engineering team, 12 people)

CAN-07: Extract metadata ✓
  Meeting 1: Product Roadmap Review
  - Attendees: ["Sarah Chen", "Mike Torres", "3 others"]
  - Organizer: Sarah Chen
  - Duration: 60 min
  - Current RSVP: Accepted
  
  Meeting 2: Customer Check-in: Acme Corp
  - Attendees: ["Jennifer Kim", "Customer Success Team"]
  - Organizer: User (you)
  - Duration: 60 min
  - Current RSVP: N/A (organizer)
  
  Meeting 3: 1:1 with Manager
  - Attendees: ["Alex Johnson"]
  - Organizer: Alex Johnson (manager)
  - Duration: 30 min
  - Current RSVP: Accepted
  
  Meeting 4: Team Sprint Planning
  - Attendees: [12 engineering team members]
  - Organizer: Team lead
  - Duration: 60 min
  - Current RSVP: Accepted

CAN-05: Resolve attendees (CRITICAL - MISSING IN ORIGINAL) ✓
  **Without this step, CAN-06 cannot check attendee availability!**
  
  Resolved contacts:
  - Sarah Chen → sarah.chen@company.com (calendar access ✓)
  - Mike Torres → mike.torres@company.com (calendar access ✓)
  - Jennifer Kim → jennifer.kim@company.com (calendar access ✓)
  - Alex Johnson → alex.johnson@company.com (calendar access ✓)
  - [12 team members] → All resolved with calendar access
  
  Total attendees resolved: 18 unique people across 4 meetings

CAN-13: Update RSVPs (Parallel with CAN-06) ✓
  Meeting 1: RSVP changed to "Declined" ✓
  Meeting 2: As organizer, marked as "Out of Office" ✓
  Meeting 3: RSVP changed to "Declined" ✓
  Meeting 4: RSVP changed to "Declined" ✓
  
  Notifications sent to all organizers

CAN-06: Find alternative time slots (Parallel with CAN-13) ✓
  **Uses resolved attendees from CAN-05 to check availability**
  
  Meeting 1 alternatives:
  - Mon 2-3pm ✅ Sarah, Mike, 3 others all free
  - Tue 10-11am ✅ All free
  - Wed 3-4pm ❌ Mike has conflict
  
  Meeting 2 alternatives:
  - Tue 11am-12pm ✅ Jennifer and team free
  - Wed 2-3pm ✅ All free
  - Fri 10-11am ✅ All free
  
  Meeting 3 alternatives:
  - Mon 10-10:30am ✅ Manager free
  - Tue 9-9:30am ✅ Manager free
  - Fri 4-4:30pm ✅ Manager free
  
  Meeting 4 alternatives:
  - Tue 2-3pm ❌ 3 people have conflicts
  - Wed 10-11am ✅ All 12 team members free!
  - Fri 2-3pm ✅ 11 of 12 free (acceptable)

CAN-12: Select best alternative times ✓
  Meeting 1: **Tuesday 10-11am** (earliest available, all attendees free)
  Meeting 2: **Wednesday 2-3pm** (customer meeting, mid-week better)
  Meeting 3: **Monday 10-10:30am** (start of week, quick sync)
  Meeting 4: **Wednesday 10-11am** (all 12 attendees available!)

CAN-23: Generate rescheduling proposal ✓
  
  **THURSDAY AFTERNOON RESCHEDULING PLAN**
  
  **Original Thursday Schedule** (4 meetings, 3.5 hours blocked):
  
  ❌ 1:00-2:00 PM: Product Roadmap Review
  → **Reschedule to**: Tuesday, 10:00-11:00 AM
  → **Attendees**: Sarah Chen, Mike Torres, 3 others
  → **Reason**: All attendees available, earlier in week
  
  ❌ 2:00-3:00 PM: Customer Check-in: Acme Corp
  → **Reschedule to**: Wednesday, 2:00-3:00 PM
  → **Attendees**: Jennifer Kim, Customer Success Team
  → **Reason**: Customer meeting, mid-week preferred
  
  ❌ 3:00-3:30 PM: 1:1 with Manager
  → **Reschedule to**: Monday, 10:00-10:30 AM
  → **Attendees**: Alex Johnson
  → **Reason**: Start of week check-in
  
  ❌ 4:00-5:00 PM: Team Sprint Planning
  → **Reschedule to**: Wednesday, 10:00-11:00 AM
  → **Attendees**: 12 engineering team members
  → **Reason**: Only slot with all 12 attendees available!
  
  **Result**: Thursday afternoon completely clear, status set to "Out of Office"

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
   - Was: Thursday 1-2 PM
   - Now: **Tuesday 10-11 AM** ✅
   - Attendees: Sarah, Mike, +3 others (all confirmed available)

2. **Customer Check-in: Acme Corp**
   - Was: Thursday 2-3 PM
   - Now: **Wednesday 2-3 PM** ✅
   - Attendees: Jennifer, Customer Success Team (all confirmed)

3. **1:1 with Manager**
   - Was: Thursday 3-3:30 PM
   - Now: **Monday 10-10:30 AM** ✅
   - Attendee: Alex Johnson (confirmed available)

4. **Team Sprint Planning**
   - Was: Thursday 4-5 PM
   - Now: **Wednesday 10-11 AM** ✅
   - Attendees: All 12 engineering team members (confirmed!)

**Status**: Your calendar now shows "Out of Office" for Thursday afternoon
**Notifications**: All attendees have been notified of the rescheduling

**Key Insight**: CAN-05 (Attendee Resolution) is CRITICAL for this workflow - human evaluator correctly identified it was missing in original decomposition. Without CAN-05, the system cannot access attendee calendars to run CAN-06 (availability checking), making rescheduling impossible. This demonstrates the importance of human evaluation to catch missing dependencies.
```

---

## Hero Prompt 6: Schedule-3

**Prompt**: "Land a time to meet about Project Alpha with Chris, Sangya, and Kat for 1 hour in the next 2 weeks. Schedule over 1:1s and lunches if needed and work around Kat's schedule. Make the meeting in person and add a room."

**Category**: Schedule  
**Capabilities Required**: Multi-person scheduling, constraint satisfaction, resource booking, priority-based conflict resolution  
**Evaluation**: ✅ **Correct**

### Canonical Task Decomposition: 10 Tasks

#### Task 1: Natural Language Understanding (CAN-04)
- **Purpose**: Extract complex scheduling constraints
- **Input**: User prompt text
- **Output**: {"attendees": ["Chris", "Sangya", "Kat"], "duration": 60, "timeframe": "next 2 weeks", "priority_constraints": ["work around Kat", "override 1:1s and lunches"], "location": "in_person", "resources": ["room"]}
- **Tier**: 1 (Universal)

#### Task 2: Attendee/Contact Resolution (CAN-05)
- **Purpose**: Resolve Chris, Sangya, Kat to directory entries
- **Input**: Attendee names from CAN-04
- **Output**: Full contact details for all 3 attendees
- **Tier**: 1 (Universal)

#### Task 3: Calendar Events Retrieval (CAN-01)
- **Purpose**: Retrieve calendars for all attendees (next 2 weeks)
- **Input**: Resolved attendees + timeframe
- **Output**: All calendar events for Chris, Sangya, Kat
- **Tier**: 1 (Universal)

#### Task 4: Meeting Metadata Extraction (CAN-07)
- **Purpose**: Extract meeting types from existing events
- **Input**: Calendar events from CAN-01
- **Output**: Meeting details (type, importance, flexibility)
- **Tier**: 2 (Common)

#### Task 5: Meeting Type Classification (CAN-02)
- **Purpose**: Classify existing meetings (identify 1:1s and lunches)
- **Input**: Meeting metadata from CAN-07
- **Output**: Meeting type classifications
- **Tier**: 1 (Universal)
- **Note**: Needed to identify "schedulable over" meetings (1:1s, lunches)

#### Task 6: Meeting Importance Assessment (CAN-03)
- **Purpose**: Assess which meetings can be overridden
- **Input**: Classified meetings from CAN-02
- **Output**: Importance scores (1:1s and lunches = lower priority)
- **Tier**: 1 (Universal)

#### Task 7: Availability Checking (CAN-06)
- **Purpose**: Find common available slots (or overridable slots)
- **Input**: All 3 calendars + "work around Kat" constraint
- **Output**: Available time slots (pure availability + overridable slots)
- **Tier**: 2 (Common)
- **Note**: Must respect Kat's schedule (hard constraint)

#### Task 8: Constraint Satisfaction (CAN-12)
- **Purpose**: Select best time satisfying all constraints
- **Input**: Available slots + priority constraints (Kat > others, Project Alpha > 1:1s/lunches)
- **Output**: Optimal time slot
- **Tier**: 2 (Common)
- **Note**: Complex constraint logic (hard + soft constraints)

#### Task 9: Resource Booking (CAN-19)
- **Purpose**: Book in-person meeting room
- **Input**: Selected time slot + attendee count (3 people)
- **Output**: Room reservation
- **Tier**: 3 (Specialized)

#### Task 10: Calendar Event Creation/Update (CAN-03)
- **Purpose**: Create Project Alpha meeting
- **Input**: Time slot + attendees + room
- **Output**: Calendar event created (may override 1:1s/lunches)
- **Tier**: 1 (Universal)

**Evaluation Criteria**:
- Priority constraint enforcement ("work around Kat" correctly applied as hard constraint)
- Override logic correctness (1:1s and lunches correctly identified as overridable)
- Multi-attendee availability accuracy (common slots correctly identified for 3 people)
- Resource booking success (meeting room reserved for in-person requirement)
- Complex constraint satisfaction (hard + soft constraints balanced appropriately)

### Execution Composition

**How Tasks Work Together to Answer the Prompt:**

```
STEP 1: Understand Complex Scheduling Constraints
CAN-04 (NLU) → Parse multi-layered requirements
  - Parse: "land a time to meet about Project Alpha" = scheduling intent with topic
  - Parse: "with Chris, Sangya, and Kat" = 3 required attendees
  - Parse: "for 1 hour in the next 2 weeks" = duration + timeframe constraints
  - Parse: "Schedule over 1:1s and lunches if needed" = SOFT constraint (override permission)
  - Parse: "work around Kat's schedule" = HARD constraint (Kat has priority)
  - Parse: "Make the meeting in person and add a room" = location + resource requirements
  - Output: {"topic": "Project Alpha", "attendees": ["Chris", "Sangya", "Kat"], "duration": 60, "timeframe": "next 2 weeks", "constraints": {"hard": ["work_around_Kat"], "soft": ["override_1:1s_lunches"]}, "location": "in_person", "resources": ["room"]}

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
  - Extract: Importance signals (customer meeting? team event? admin?)
  - Output: Enriched meeting objects with classification context

STEP 5-6: Classify and Assess Meetings (Parallel Processing)
CAN-02 (Meeting Type Classification) → Categorize existing meetings
  - Identify: 1:1 meetings (2 attendees)
  - Identify: Lunch meetings (keywords: "lunch", duration 30-60 min, time 11am-2pm)
  - Identify: Other meeting types (team sync, customer, planning, etc.)
  - Purpose: Know which meetings can be overridden per soft constraint
  - Output: Type classifications for all 120 events

CAN-03 (Importance Assessment) → Score meeting priority
  - High priority: Customer meetings, board meetings, all-hands (CANNOT override)
  - Medium priority: Team syncs, planning sessions (do not override unless necessary)
  - Low priority: 1:1s and lunches (OVERRIDABLE per prompt)
  - Kat's meetings: Importance scores determine hard constraint enforcement
  - Output: Importance scores for filtering overridable slots

STEP 7: Check Availability with Priority Logic
CAN-06 (Availability Checking) → Find common available slots
  - Phase 1: Pure availability - Find slots where all 3 are free
  - Phase 2: Overridable availability - Find slots where all 3 have only 1:1s or lunches
  - Hard constraint: NEVER override Kat's meetings (work around Kat's schedule)
  - Soft constraint: CAN override Chris's and Sangya's 1:1s/lunches if needed
  - Output: List of available time slots (pure + overridable, sorted by preference)

STEP 8: Select Optimal Time Slot
CAN-12 (Constraint Satisfaction) → Apply complex constraint logic
  - Preference 1: Pure availability (no conflicts for anyone) - BEST OPTION
  - Preference 2: Override Chris's or Sangya's 1:1/lunch - ACCEPTABLE
  - HARD RULE: Never override Kat's meetings (even if 1:1 or lunch)
  - Tiebreaker: Earlier in 2-week window better, mid-week better than Monday/Friday
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
  - Subject: "Project Alpha Discussion"
  - Duration: 60 minutes
  - Note: May override Chris's or Sangya's 1:1/lunch (not Kat's!)
  - Output: Calendar event created, invitations sent

OUTPUT: Project Alpha meeting scheduled with constraints satisfied
  1. Time found within next 2 weeks
  2. All 3 attendees invited
  3. Kat's schedule fully respected (hard constraint)
  4. Chris's or Sangya's 1:1/lunch may be overridden (soft constraint)
  5. In-person meeting room reserved
```

**Key Orchestration Patterns**:
- **Dual-Phase Availability Checking**: CAN-06 runs twice (pure availability + overridable availability)
- **Priority-Based Filtering**: CAN-03 (importance) determines which meetings can be overridden
- **Hard vs Soft Constraints**: CAN-12 enforces Kat priority (hard) while allowing 1:1/lunch override (soft)
- **Parallel Classification**: CAN-02 + CAN-03 process same events concurrently
- **Parallel Finalization**: CAN-19 (room booking) + CAN-03 (event creation) are independent operations
- **Most Complex Scheduling**: Uses 10 tasks with multi-layered constraint logic - demonstrates sophisticated conflict resolution

**Example Flow - Multi-Person Scheduling with Override Logic**:

```
User Request: "Land a time to meet about Project Alpha with Chris, Sangya, and Kat for 1 hour in the next 2 weeks. Schedule over 1:1s and lunches if needed and work around Kat's schedule. Make the meeting in person and add a room."

CAN-04: Extract scheduling requirements ✓
  → topic: "Project Alpha"
  → attendees: ["Chris", "Sangya", "Kat"]
  → duration: 60 minutes
  → timeframe: next 2 weeks
  → hard constraint: "work around Kat"
  → soft constraint: "override 1:1s and lunches if needed"
  → location: "in_person"
  → resources: ["room"]

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
  - Meeting types identified: 1:1s, lunches, team syncs, customer meetings, etc.
  - Attendee counts: Range 2-20 people
  - Durations: Range 15 min - 2 hours
  - Time slots: Throughout business hours

CAN-02: Classify meeting types (Parallel with CAN-03) ✓
  Chris's meetings:
  - 1:1s: 12 meetings (OVERRIDABLE)
  - Lunches: 4 meetings (OVERRIDABLE)
  - Team syncs: 10 meetings
  - Customer meetings: 8 meetings
  - Other: 4 meetings
  
  Sangya's meetings:
  - 1:1s: 15 meetings (OVERRIDABLE)
  - Lunches: 5 meetings (OVERRIDABLE)
  - Team syncs: 12 meetings
  - Planning: 6 meetings
  - Other: 4 meetings
  
  Kat's meetings:
  - 1:1s: 10 meetings (NOT OVERRIDABLE - hard constraint!)
  - Lunches: 3 meetings (NOT OVERRIDABLE - hard constraint!)
  - Team syncs: 12 meetings
  - Customer meetings: 7 meetings
  - Other: 3 meetings

CAN-03: Assess importance (Parallel with CAN-02) ✓
  High priority (CANNOT override):
  - All customer meetings (23 total)
  - All team syncs (34 total)
  - All planning sessions (6 total)
  - ALL of Kat's meetings (35 total - hard constraint!)
  
  Low priority (CAN override per soft constraint):
  - Chris's 1:1s and lunches (16 meetings)
  - Sangya's 1:1s and lunches (20 meetings)
  - Kat's 1:1s and lunches: 13 meetings (BUT CANNOT OVERRIDE due to hard constraint!)

CAN-06: Check availability (dual-phase) ✓
  
  **Phase 1: Pure Availability** (all 3 free, no conflicts)
  Scanning next 2 weeks...
  - Week 1: ❌ No common free slots (all 3 heavily booked)
  - Week 2: ✅ Found 2 slots!
    - Wednesday Week 2, 2:00-3:00 PM ✅ ALL FREE
    - Friday Week 2, 10:00-11:00 AM ✅ ALL FREE
  
  **Phase 2: Overridable Availability** (override Chris's or Sangya's 1:1/lunch)
  Additional slots where Chris or Sangya have 1:1/lunch (but NOT Kat):
  - Tuesday Week 1, 3:00-4:00 PM ✅ Chris has 1:1 (overridable), Sangya free, Kat free
  - Thursday Week 1, 12:00-1:00 PM ✅ Sangya has lunch (overridable), Chris free, Kat free
  - Monday Week 2, 11:00-12:00 PM ✅ Chris has 1:1 (overridable), Sangya free, Kat free
  
  **Rejected Slots** (violate hard constraint):
  - Monday Week 1, 2:00-3:00 PM ❌ Kat has 1:1 (CANNOT OVERRIDE - hard constraint!)
  - Wednesday Week 1, 12:00-1:00 PM ❌ Kat has lunch (CANNOT OVERRIDE - hard constraint!)
  
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
  Available rooms:
  - Conference Room A (capacity 4) ✅ Available
  - Conference Room B (capacity 8) ✅ Available
  - Board Room (capacity 20) ✅ Available (overkill)
  
  Selected: **Conference Room A** (right-sized for 3 people)
  Location: 3rd floor, near Kat's office

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

**Next Step**: All 3 attendees have been invited and will receive calendar notifications.

**Key Insight**: This prompt demonstrates the MOST COMPLEX constraint satisfaction in the framework. CAN-12 must balance:
1. Hard constraint: Never override Kat (priority attendee)
2. Soft constraint: CAN override others' 1:1s/lunches IF needed
3. Pure availability preferred over overrides
4. Multi-person scheduling (3 calendars to coordinate)
5. Resource booking (in-person room requirement)

The system correctly applies priority-based logic: Kat's even low-priority meetings (1:1s, lunches) are treated as high-priority due to "work around Kat's schedule" instruction, while Chris's and Sangya's similar meetings remain overridable.
```

---

## Hero Prompt 7: Collaborate-1

**Prompt**: "Help me set the agenda to review the progress of Project Alpha with the product and marketing team to get confirmation we are on track and discuss any blocking issues or risks."

**Category**: Collaborate  
**Capabilities Required**: Attendee resolution, agenda generation  
**Evaluation**: ❓ **Needs Review** - CAN-18 over-interpretation

**Human Evaluator Notes**: 
> "'to get confirmation we are on track and discuss any blocking issues or risks' in the prompt is to set the goal of the meeting and should be used as input for the agenda generation for CAN-09. The user does not expect the system to find blocking issues and confirm status but the requester want to find out those during the meeting so CAN-18 should not be activated."

### Canonical Task Decomposition: 3 Tasks

#### Task 1: Natural Language Understanding (CAN-04)
- **Purpose**: Extract agenda requirements and meeting goals
- **Input**: User prompt text
- **Output**: {"intent": "generate_agenda", "topic": "Project Alpha progress review", "attendees": ["product team", "marketing team"], "goals": ["confirm on track", "discuss blocking issues/risks"]}
- **Tier**: 1 (Universal)

#### Task 2: Attendee/Contact Resolution (CAN-05)
- **Purpose**: Resolve "product team" and "marketing team" to individual members
- **Input**: Team names from CAN-04
- **Output**: List of product and marketing team members
- **Tier**: 1 (Universal)
- **Note**: Needed to know who will attend (for agenda context)

#### Task 3: Document Generation/Formatting (CAN-09)
- **Purpose**: Generate structured meeting agenda
- **Input**: Meeting goals from CAN-04 ("confirm on track", "discuss blocking issues/risks")
- **Output**: Formatted agenda with topics, time allocations, discussion goals
- **Tier**: 2 (Common)
- **Note**: Goals used as INPUT, not as tasks to execute (CAN-18 should NOT be used)

**Evaluation Criteria**:
- Agenda completeness (covers all stated goals)
- Topic structure clarity (logical flow of discussion)
- Time allocation reasonableness (realistic durations)
- Attendee resolution accuracy (correct team members identified)
- **Critical**: Does NOT include CAN-18 (risk anticipation) - user will discuss risks IN meeting, not have system find them beforehand

### Execution Composition

**How Tasks Work Together to Answer the Prompt:**

```
STEP 1: Parse Agenda Requirements
CAN-04 (NLU) → Extract meeting goals and attendee groups
  - Parse: "set the agenda", "review progress", "get confirmation", "discuss blocking issues/risks"
  - Extract: topic = "Project Alpha progress review"
  - Extract: teams = ["product team", "marketing team"]
  - Extract: goals = ["confirm we are on track", "discuss any blocking issues or risks"]
  - **IMPORTANT**: These are DISCUSSION GOALS for the meeting, not system tasks to execute

STEP 2: Resolve Team Membership
CAN-05 (Attendee Resolution) → Identify individual team members
  - Input: "product team", "marketing team"
  - Lookup: Directory/org chart for team composition
  - Output: 
    - Product team: [PM1, PM2, Designer, Engineer Lead]
    - Marketing team: [Marketing Manager, Content Lead, Campaign Manager]

STEP 3: Generate Meeting Agenda
CAN-09 (Document Generation) → Create structured agenda document
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

OUTPUT: Structured meeting agenda ready for distribution
  - Clear topic breakdown aligned with user's stated goals
  - Realistic time allocations
  - Discussion objectives for each agenda item
  - **NOTE**: Agenda sets up discussion framework; actual risk identification happens DURING meeting
```

**Key Orchestration Patterns**:
- **Simple Sequential**: CAN-04 → CAN-05 → CAN-09 (only 3 tasks, minimal orchestration)
- **No Automation Beyond Agenda**: User wants help SETTING agenda, not executing the meeting goals
- **Critical Distinction**: Meeting goals ≠ System tasks (CAN-18 should NOT run to find risks beforehand)

**Example Flow - Agenda Generation for Project Review**:

```
Input: "Help me set the agenda to review the progress of Project Alpha with the product and marketing team to get confirmation we are on track and discuss any blocking issues or risks."

CAN-04: Parse agenda requirements ✓
  → topic: "Project Alpha progress review"
  → teams: ["product team", "marketing team"]
  → goals: ["confirm on track", "discuss blocking issues/risks"]
  → intent: Generate meeting agenda (NOT find risks or confirm status)

CAN-05: Resolve team membership ✓
  → Product team: [Sarah Chen (PM), Mike Liu (Designer), Alex Kumar (Eng Lead), Jamie Park (PM)]
  → Marketing team: [Dana Williams (Manager), Chris Lee (Content), Taylor Brown (Campaigns)]
  → Total attendees: 7 people

CAN-09: Generate structured agenda ✓
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
  ✅ Structured agenda created for Project Alpha progress review
  ✅ 7 attendees identified (product + marketing teams)
  ✅ Discussion goals embedded in agenda structure
  ✅ Ready to distribute to participants

**Key Insight**: The system did NOT run CAN-18 (Risk Anticipation) because the user wants to DISCUSS risks during the meeting, not have the system find them beforehand. "Discuss any blocking issues or risks" is a MEETING GOAL, not a system task.
```

---

## Hero Prompt 8: Collaborate-2

**Prompt**: "Review the materials for my meeting with senior leadership and suggest the best way to summarize the topics into three main discussion points. Generate any objections or concerns that might come up and give me effective responses."

**Category**: Collaborate  
**Capabilities Required**: Meeting material retrieval, content summarization, objection anticipation, response generation  
**Evaluation**: ⚠️ **Partial** - Missing CAN-05 (Attendee Resolution)

**Human Evaluator Notes**: 
> "The system needs to know who are in the senior leadership to find relevant meetings and meeting related materials. So CAN-05 is a critical task."

### Canonical Task Decomposition: 7 Tasks (Including CAN-05)

#### Task 1: Natural Language Understanding (CAN-04)
- **Purpose**: Extract preparation requirements
- **Input**: User prompt text
- **Output**: {"intent": "prepare_for_meeting", "attendees": "senior leadership", "tasks": ["review materials", "summarize to 3 points", "generate objections", "create responses"]}
- **Tier**: 1 (Universal)

#### Task 2: Attendee/Contact Resolution (CAN-05) - **MISSING IN ORIGINAL**
- **Purpose**: Resolve "senior leadership" to specific executives
- **Input**: "senior leadership" from CAN-04
- **Output**: List of senior leadership members (VPs, C-level)
- **Tier**: 1 (Universal)
- **Note**: **CRITICAL** - Needed to find relevant meetings and materials

#### Task 3: Calendar Events Retrieval (CAN-01)
- **Purpose**: Find the upcoming meeting with senior leadership
- **Input**: Resolved senior leadership attendees from CAN-05
- **Output**: Upcoming meeting event
- **Tier**: 1 (Universal)
- **Dependencies**: CAN-05 (need to know who senior leadership is)

#### Task 4: Meeting Metadata Extraction (CAN-07)
- **Purpose**: Extract meeting details (attendees, agenda, attachments)
- **Input**: Meeting event from CAN-01
- **Output**: Meeting metadata
- **Tier**: 2 (Common)

#### Task 5: Document/Content Retrieval (CAN-08)
- **Purpose**: Retrieve meeting materials (presentations, documents, pre-reads)
- **Input**: Meeting attachments from CAN-07
- **Output**: Meeting materials content
- **Tier**: 2 (Common)
- **Dependencies**: CAN-07 (need attachments list)

#### Task 6: Document Generation/Formatting (CAN-09)
- **Purpose**: Summarize materials into 3 main discussion points
- **Input**: Retrieved materials from CAN-08
- **Output**: Formatted summary with 3 key points
- **Tier**: 2 (Common)

#### Task 7: Objection/Risk Anticipation (CAN-18)
- **Purpose**: Generate potential objections/concerns + effective responses
- **Input**: Discussion points from CAN-09 + senior leadership context
- **Output**: List of objections with prepared responses
- **Tier**: 3 (Specialized)
- **Note**: User explicitly requests this ("Generate any objections or concerns")

**Evaluation Criteria**:
- Attendee resolution accuracy (senior leadership correctly identified from organization)
- Summarization quality (3 discussion points capture key themes from materials)
- Objection anticipation relevance (concerns match senior leadership perspective)
- Response effectiveness (prepared responses address objections convincingly)
- CAN-05 inclusion (CRITICAL - human evaluator identified missing dependency for finding materials)

### Execution Composition

**How Tasks Work Together to Answer the Prompt:**

```
STEP 1: Understand Preparation Requirements
CAN-04 (NLU) → Parse multi-part request
  - Parse: "Review the materials for my meeting with senior leadership" = material retrieval required
  - Parse: "suggest the best way to summarize the topics into three main discussion points" = summarization task
  - Parse: "Generate any objections or concerns that might come up" = objection anticipation
  - Parse: "give me effective responses" = response preparation
  - Output: {"intent": "prepare_for_meeting", "attendees": "senior leadership", "tasks": ["review_materials", "summarize_to_3_points", "generate_objections", "create_responses"]}

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
  - Filter: Likely candidates (multiple C-level attendees, duration 60+ min, formal subject)
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
  - Prioritize: Select 3 most important topics based on:
    - Frequency mentioned across materials
    - Strategic importance signals (revenue, market position, risk)
    - Action-oriented topics (decisions needed, approvals required)
  - Format: Create concise summaries with supporting data points
  - Output: 3 main discussion points with key facts

STEP 7: Generate Objections and Responses
CAN-18 (Objection/Risk Anticipation) → Anticipate senior leadership concerns
  - Input: 3 discussion points from CAN-09 + senior leadership profiles from CAN-05
  - Analyze: For each discussion point, identify potential objections:
    - Financial concerns (CFO perspective)
    - Market risks (CEO perspective)
    - Execution feasibility (COO perspective)
    - Competitive threats (VP Sales perspective)
  - Generate: Prepared responses for each objection with supporting data
  - Output: Objection-response pairs for all 3 discussion points

OUTPUT: Comprehensive meeting preparation package
  1. 3 MAIN DISCUSSION POINTS: Structured summaries from materials
  2. ANTICIPATED OBJECTIONS: Likely concerns from senior leadership
  3. EFFECTIVE RESPONSES: Prepared answers with data/rationale
```

**Key Orchestration Patterns**:
- **CRITICAL MISSING DEPENDENCY**: CAN-05 MUST precede CAN-01 - cannot find "meeting with senior leadership" without knowing who senior leadership is
- **Sequential Document Pipeline**: CAN-07 (get attachments) → CAN-08 (retrieve content) → CAN-09 (summarize)
- **Objection Layer**: CAN-18 runs after CAN-09 (needs discussion points) and uses CAN-05 (needs attendee profiles)
- **Human Evaluator Insight**: Original decomposition missed CAN-05 - evaluator noted "system needs to know who are in the senior leadership to find relevant meetings and meeting related materials"
- **Contrast with Collaborate-1**: Here CAN-18 IS appropriate because user explicitly requested "Generate any objections or concerns" (vs Collaborate-1 where it was over-interpreted)

**Example Flow - Executive Meeting Preparation**:

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
  - Total investment required: $8M over 4 quarters
  - Expected ROI: 30% revenue increase by end of 2025
  
  **Competitive_Market_Analysis.docx** (15 pages):
  - Competitor A launched similar features 2 months ago
  - Market share: We are #3 (18%), Competitor A is #1 (35%)
  - Customer win rate declining: 45% → 38% in past 2 quarters
  - Pricing pressure: Average deal size down 12%

CAN-09: Summarize into 3 main discussion points ✓
  
  Analyzed all materials, identified 3 key themes:
  
  **DISCUSSION POINT 1: Q4 Financial Performance and Revenue Gap**
  - Revenue came in at $45M vs $50M target (-10% miss)
  - Positive: Operating margin improved to 18% (cost management working)
  - Concern: Customer churn increased to 8% (from 6% in Q3)
  - Key Question: What caused revenue miss? Churn? Slower new sales?
  
  **DISCUSSION POINT 2: 2025 Product Roadmap Investment Decision**
  - Proposed investment: $8M across 4 quarters for AI features + mobile redesign + enterprise tier
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
  ✅ **Your Response**: "Fair concern. The miss was driven by 2 large deals slipping from Q4 to Q1 (both confirmed). Churn increase is the real issue - we're implementing a customer success intervention plan targeting at-risk accounts. We project churn to return to 6% by Q2 with this intervention."
  
  ❌ **CEO Objection**: "Churn going from 6% to 8% is a red flag. What's causing it?"
  ✅ **Your Response**: "Exit interviews show 60% of churned customers cited lack of mobile app and AI features - which our 2025 roadmap addresses. This validates our product investment thesis. The other 40% cited pricing, which we're addressing with enterprise tier for price-sensitive segments."
  
  **OBJECTIONS FOR DISCUSSION POINT 2** (Product Roadmap Investment):
  
  ❌ **CFO Objection**: "$8M investment is significant given we just missed revenue target. Can we scale back?"
  ✅ **Your Response**: "We evaluated a phased approach. Minimum viable investment is $5M (AI features only, defer mobile redesign). However, competitive analysis shows Competitor A is gaining share with their mobile app. Delaying mobile risks further customer win rate decline. ROI projections show $8M investment pays back in 10 months."
  
  ❌ **VP Product Objection**: "Enterprise tier launch in Q3 is aggressive. Do we have engineering capacity?"
  ✅ **Your Response**: "Agreed it's tight. We're proposing 2 additional engineering hires in Q1 (already budgeted). Alternative is to push enterprise tier to Q4, but that delays revenue impact by 1 quarter ($3M opportunity cost)."
  
  **OBJECTIONS FOR DISCUSSION POINT 3** (Competitive Position):
  
  ❌ **CEO Objection**: "Win rate declining from 45% to 38% is alarming. Is this a sales execution problem or product gap?"
  ✅ **Your Response**: "Analysis shows 70% of losses are to Competitor A citing their AI features (product gap). 30% are sales execution (pricing/contracting delays). Product roadmap addresses the 70%, and we've streamlined sales approval process to address the 30%. We expect win rate to recover to 42% by Q2."
  
  ❌ **VP Sales Objection**: "Pricing pressure is killing margins. Should we hold the line on price?"
  ✅ **Your Response**: "Short-term yes - we're training sales to sell value, not discount. Medium-term, enterprise tier gives us pricing flexibility (tiered pricing reduces pressure on core product). Financial analysis shows enterprise tier can absorb price-sensitive customers without cannibalizing mid-market deals."

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
- CFO: "How prevent Q1 revenue miss?" → 2 large deals slipped to Q1 (confirmed), churn intervention plan targets 6% by Q2
- CEO: "What's causing churn increase?" → 60% cite lack of mobile/AI (validates roadmap), 40% pricing (enterprise tier addresses)

**Point 2 - Product Investment**:
- CFO: "Can we scale back $8M investment?" → Minimum $5M (AI only), but delaying mobile risks further decline, 10-month payback
- VP Product: "Q3 enterprise tier too aggressive?" → 2 engineering hires needed, alternative Q4 push has $3M opportunity cost

**Point 3 - Competitive Position**:
- CEO: "Is win rate decline sales or product issue?" → 70% product gap (roadmap fixes), 30% sales execution (process streamlined)
- VP Sales: "Hold line on pricing?" → Yes short-term (value selling training), medium-term enterprise tier provides flexibility

**PREPARATION COMPLETE** ✅

**Key Insight**: CAN-05 (Attendee Resolution) is CRITICAL and was missing in original decomposition. Human evaluator correctly identified: "The system needs to know who are in the senior leadership to find relevant meetings and meeting related materials." Without CAN-05, the system cannot search for "meeting with senior leadership" (CAN-01) or tailor objections to specific executive perspectives (CAN-18). This demonstrates human evaluation catching missing dependencies that break the workflow.
```

---

## Hero Prompt 9: Collaborate-3

**Prompt**: "Prepare a brief for my upcoming meeting with customer Beta and include a dossier for each customer attendee and the topics they are most interested in. Include a background on their company."

**Category**: Collaborate  
**Capabilities Required**: Meeting preparation, contact research, company intelligence, document generation  
**Evaluation**: ✅ **Correct**

### Canonical Task Decomposition: 7 Tasks

#### Task 1: Natural Language Understanding (CAN-04)
- **Purpose**: Extract brief preparation requirements
- **Input**: User prompt text
- **Output**: {"intent": "prepare_brief", "customer": "Beta", "components": ["attendee dossiers", "interest topics", "company background"]}
- **Tier**: 1 (Universal)

#### Task 2: Calendar Events Retrieval (CAN-01)
- **Purpose**: Find upcoming meeting with customer Beta
- **Input**: Customer name ("Beta")
- **Output**: Upcoming Beta customer meeting
- **Tier**: 1 (Universal)

#### Task 3: Meeting Metadata Extraction (CAN-07)
- **Purpose**: Extract customer attendees from meeting
- **Input**: Beta meeting from CAN-01
- **Output**: List of customer Beta attendees
- **Tier**: 2 (Common)

#### Task 4: Attendee/Contact Resolution (CAN-05)
- **Purpose**: Resolve customer attendees to full profiles
- **Input**: Customer attendee names from CAN-07
- **Output**: Full profiles (title, role, LinkedIn, background)
- **Tier**: 1 (Universal)

#### Task 5: Document/Content Retrieval (CAN-08)
- **Purpose**: Retrieve past meeting materials, emails with customer Beta
- **Input**: Customer Beta identifier + attendees
- **Output**: Historical interaction content
- **Tier**: 2 (Common)

#### Task 6: Document Generation/Formatting (CAN-09)
- **Purpose**: Generate meeting brief and attendee dossiers
- **Input**: Attendee profiles + historical materials
- **Output**: Formatted brief with dossiers
- **Tier**: 2 (Common)

#### Task 7: Research/Intelligence Gathering (CAN-22)
- **Purpose**: Research customer Beta company background
- **Input**: Company name ("Beta")
- **Output**: Company intelligence (industry, news, financials, recent developments)
- **Tier**: 3 (Specialized)
- **Note**: Addresses "Include a background on their company"

**Evaluation Criteria**:
- Meeting identification accuracy (correct customer Beta meeting found)
- Attendee dossier completeness (all customer attendees profiled with relevant background)
- Interest topic relevance (topics accurately reflect customer priorities from historical data)
- Company background depth (comprehensive intelligence on customer Beta company)
- Document formatting quality (brief is well-structured and executive-ready)

### Execution Composition

**How Tasks Work Together to Answer the Prompt:**

```
STEP 1: Understand Brief Requirements
CAN-04 (NLU) → Parse multi-component preparation request
  - Parse: "Prepare a brief for my upcoming meeting with customer Beta" = meeting prep task
  - Parse: "include a dossier for each customer attendee" = individual profiles required
  - Parse: "the topics they are most interested in" = interest analysis from historical data
  - Parse: "Include a background on their company" = company intelligence research
  - Output: {"intent": "prepare_brief", "customer": "Beta", "components": ["attendee_dossiers", "interest_topics", "company_background"]}

STEP 2: Find Customer Beta Meeting
CAN-01 (Calendar Retrieval) → Locate upcoming meeting
  - Search: Upcoming calendar for meetings with "Beta" in subject, attendees, or meeting notes
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
  - Sources: Public filings, news articles, press releases, industry reports, LinkedIn company page
  - Extract: Industry, size (revenue, employees), recent developments (funding, acquisitions, leadership changes)
  - Financial data: Revenue trends, growth rate, funding status
  - Strategic context: Business priorities, market position, competitive landscape
  - Output: Comprehensive company background report

OUTPUT: Complete meeting brief
  1. CUSTOMER BETA COMPANY BACKGROUND: Industry, financials, recent news, strategic priorities
  2. ATTENDEE DOSSIERS: Profiles for each customer attendee with roles, background, interaction history
  3. INTEREST TOPICS: Key themes each attendee cares about (from historical analysis)
  4. MEETING CONTEXT: Suggested discussion points based on customer interests
```

**Key Orchestration Patterns**:
- **Parallel Research**: CAN-09 (attendee dossiers) + CAN-22 (company research) run independently
- **Historical Analysis**: CAN-08 retrieves past interactions, CAN-09 analyzes for interest patterns
- **Multi-Layer Context**: Individual (dossiers) + company (background) + historical (interests)
- **Profile Enrichment Pipeline**: CAN-07 (extract names) → CAN-05 (resolve to profiles) → CAN-09 (generate dossiers)
- **Most Customer-Facing Prompt**: Demonstrates external research capabilities (CAN-22) and relationship intelligence (CAN-08 + CAN-09 analysis)

**Example Flow - Customer Meeting Brief Preparation**:

```
User Request: "Prepare a brief for my upcoming meeting with customer Beta and include a dossier for each customer attendee and the topics they are most interested in. Include a background on their company."

CAN-04: Extract brief requirements ✓
  → intent: "prepare_brief"
  → customer: "Beta"
  → components: ["attendee_dossiers", "interest_topics", "company_background"]

CAN-01: Find customer Beta meeting ✓
  Search: Upcoming calendar for "Beta"
  Found: "Quarterly Business Review - Beta Corporation"
  - Date: Next Thursday, 10:00-11:30 AM
  - Location: Conference Room A + Video conference
  - Internal attendees: You, VP Sales (Dana), Customer Success Manager (Jordan)
  - External attendees: Sarah Johnson, Michael Lee, Emily Carter (Beta)

CAN-07: Extract customer attendees ✓
  Meeting metadata:
  - Subject: "Quarterly Business Review - Beta Corporation"
  - Duration: 90 minutes
  - Customer attendees identified:
    1. Sarah Johnson (external)
    2. Michael Lee (external)
    3. Emily Carter (external)
  - Internal attendees: You, Dana (VP Sales), Jordan (CSM)

CAN-05: Resolve customer attendees to full profiles ✓
  
  **Sarah Johnson**:
  - Title: VP of Operations, Beta Corporation
  - Role: Decision-maker for operational tools and processes
  - Background: 8 years at Beta, promoted from Director 2 years ago
  - Education: MBA from Stanford, BS Industrial Engineering
  - LinkedIn: linkedin.com/in/sarah-johnson-beta
  - Previous company: McKinsey (consultant for 5 years)
  - Expertise: Process optimization, supply chain management
  
  **Michael Lee**:
  - Title: Director of IT, Beta Corporation
  - Role: Technical evaluation and implementation oversight
  - Background: 3 years at Beta, joined from Amazon
  - Education: MS Computer Science, University of Washington
  - LinkedIn: linkedin.com/in/michael-lee-it
  - Previous company: Amazon (software engineer, 6 years)
  - Expertise: Cloud infrastructure, security, API integrations
  
  **Emily Carter**:
  - Title: Product Manager, Beta Corporation
  - Role: End-user advocate, feature requests
  - Background: 5 years at Beta, former business analyst
  - Education: BA Business Administration, UC Berkeley
  - LinkedIn: linkedin.com/in/emily-carter-pm
  - Previous role: Business Analyst at Beta (promoted 2 years ago)
  - Expertise: Product strategy, user experience, analytics

CAN-08: Retrieve historical interaction materials ✓
  
  Retrieved 15 past meetings + 50 emails with Beta (past 12 months):
  
  **Past Meetings**:
  - Monthly check-ins (10 meetings)
  - Onboarding session (3 months ago)
  - Product training (2 sessions)
  - Quarterly business reviews (2 previous QBRs)
  
  **Email Threads**:
  - Feature requests (15 emails, mostly from Emily)
  - Technical questions (20 emails, mostly from Michael)
  - Process discussions (10 emails, mostly from Sarah)
  - Billing/contract questions (5 emails)
  
  **CRM Notes**:
  - Account health: Green (high satisfaction)
  - Renewal date: 4 months away (important context!)
  - Expansion opportunity: Considering adding 50 more licenses
  - Support tickets: 8 tickets (all resolved, avg resolution time 6 hours)

CAN-09: Generate attendee dossiers with interest topics (Parallel with CAN-22) ✓
  
  **Analyzed historical materials to identify interest topics for each attendee:**
  
  **DOSSIER: Sarah Johnson** (VP of Operations)
  - **Role**: Decision-maker for operational tools, budget owner
  - **Background**: 8 years at Beta, MBA Stanford, ex-McKinsey consultant
  - **Previous Interactions**: 
    - Attended 6 of past 10 monthly check-ins
    - Led conversation in last 2 QBRs
    - Sent 10 emails (mostly strategic questions)
  - **Topics Most Interested In** (from historical analysis):
    1. **ROI and Cost Optimization** (mentioned in 8 of 10 emails)
       - Quote: "How can we reduce time spent on manual data entry?"
       - Context: Sarah is measured on operational efficiency
    2. **Workflow Automation** (discussed in 4 meetings)
       - Quote: "Can we automate the monthly reporting process?"
       - Context: Her team spends 20 hours/month on reports
    3. **Scalability for Growth** (raised in last QBR)
       - Quote: "If we expand to 500 users next year, can system handle it?"
       - Context: Beta is growing 30% YoY, planning headcount expansion
  
  **DOSSIER: Michael Lee** (Director of IT)
  - **Role**: Technical gatekeeper, security/compliance oversight
  - **Background**: 3 years at Beta, ex-Amazon engineer, MS Computer Science
  - **Previous Interactions**:
    - Attended onboarding + 2 training sessions (deep technical engagement)
    - Sent 20 emails (mostly technical questions)
    - Opened 3 support tickets (API integration questions)
  - **Topics Most Interested In** (from historical analysis):
    1. **Security and Compliance** (mentioned in 12 of 20 emails)
       - Quote: "Do you have SOC 2 Type 2 certification?"
       - Context: Beta is in healthcare, subject to HIPAA compliance
    2. **API Integration and Extensibility** (discussed in 3 support tickets)
       - Quote: "Can we integrate with our Salesforce instance via API?"
       - Context: Michael is building internal tools that need API access
    3. **Performance and Uptime** (raised in 2 emails)
       - Quote: "What's your SLA for uptime? Our users need 99.9%"
       - Context: Operational tools are mission-critical for Beta
  
  **DOSSIER: Emily Carter** (Product Manager)
  - **Role**: End-user advocate, feature prioritization influence
  - **Background**: 5 years at Beta, promoted from analyst, BA UC Berkeley
  - **Previous Interactions**:
    - Attended all 10 monthly check-ins (consistent engagement)
    - Sent 15 feature request emails
    - Participated actively in 2 product training sessions
  - **Topics Most Interested In** (from historical analysis):
    1. **Mobile App Enhancements** (mentioned in 8 of 15 emails)
       - Quote: "When will offline mode be available on mobile?"
       - Context: Beta's field team needs offline access
    2. **User Experience Improvements** (discussed in 5 meetings)
       - Quote: "Our team finds the dashboard too cluttered"
       - Context: Emily receives user feedback, advocates for UX
    3. **Analytics and Reporting** (raised in last QBR)
       - Quote: "Can we get custom report templates?"
       - Context: Beta's analysts need specific data views

CAN-22: Research Beta Corporation company background (Parallel with CAN-09) ✓
  
  **BETA CORPORATION - COMPANY BACKGROUND**
  
  **Industry & Business**:
  - Industry: Healthcare Technology (medical device distribution)
  - Founded: 1998 (26 years in business)
  - Headquarters: Seattle, WA
  - Locations: 12 distribution centers across US
  
  **Size & Financials**:
  - Employees: 850 (grown from 600 in 2022)
  - Revenue: $320M annually (est. 2023)
  - Growth rate: 30% YoY (past 3 years)
  - Funding: Privately held, Series C funded ($50M in 2021)
  
  **Recent Developments** (past 6 months):
  - **Expansion**: Opened 2 new distribution centers (Denver, Austin)
  - **Leadership change**: New CEO appointed (Dr. James Park, former Medtronic exec)
  - **Product launch**: New AI-powered inventory prediction system
  - **Partnership**: Announced partnership with major hospital network (Kaiser Permanente)
  
  **Strategic Priorities** (from press releases + earnings calls):
  1. **Geographic expansion**: Targeting 20 distribution centers by 2026
  2. **Digital transformation**: Modernizing legacy systems (our product fits here!)
  3. **Customer experience**: Improving order fulfillment speed (critical metric for them)
  
  **Market Position**:
  - Market share: #4 in medical device distribution (8% market share)
  - Main competitors: McKesson, Cardinal Health, AmerisourceBergen
  - Differentiation: Regional focus + personalized service (vs big national players)
  
  **Relevant News** (past 30 days):
  - Trade publication article: "Beta Corporation invests $15M in technology modernization"
  - LinkedIn post from CEO: "Our vision is to become the most tech-enabled distributor by 2026"
  - Industry report: Beta ranked #1 in customer satisfaction (J.D. Power survey)

OUTPUT to User:

📄 **CUSTOMER MEETING BRIEF - BETA CORPORATION**

**Meeting**: Quarterly Business Review  
**Date**: Next Thursday, 10:00-11:30 AM  
**Customer Attendees**: Sarah Johnson (VP Ops), Michael Lee (Dir IT), Emily Carter (PM)  
**Internal Attendees**: You, Dana (VP Sales), Jordan (CSM)

---

**COMPANY BACKGROUND - BETA CORPORATION**

**Industry**: Healthcare Technology (medical device distribution)  
**Size**: 850 employees, $320M revenue, 30% YoY growth  
**Recent News**: 
- New CEO: Dr. James Park (ex-Medtronic)
- Expansion: Opened Denver + Austin distribution centers
- Partnership: Kaiser Permanente collaboration announced
- Investment: $15M in technology modernization (relevant to us!)

**Strategic Priorities**:
1. Geographic expansion (12 → 20 distribution centers by 2026)
2. Digital transformation (CEO vision: "most tech-enabled distributor by 2026")
3. Customer experience (ranked #1 in customer satisfaction)

**Key Context**: Beta is 4 months from renewal and considering expanding from 200 → 250 licenses.

---

**ATTENDEE DOSSIERS**

**Sarah Johnson** - VP of Operations (Decision-Maker)  
- Background: 8 years at Beta, MBA Stanford, ex-McKinsey  
- **Top Interests**:
  1. ROI & Cost Optimization (asks about efficiency gains in 8 of 10 emails)
  2. Workflow Automation (wants to automate 20 hrs/month manual reporting)
  3. Scalability (planning for 500 users next year, 30% growth)
- **Suggested Talking Points**: Showcase ROI metrics, demo automation features, discuss enterprise scalability

**Michael Lee** - Director of IT (Technical Gatekeeper)  
- Background: 3 years at Beta, ex-Amazon engineer, MS CS  
- **Top Interests**:
  1. Security & Compliance (healthcare = HIPAA, asked about SOC 2 Type 2)
  2. API Integration (building internal tools, needs API access to Salesforce)
  3. Performance & Uptime (requires 99.9% SLA for mission-critical ops)
- **Suggested Talking Points**: Share security certifications, demo API capabilities, review SLA performance

**Emily Carter** - Product Manager (User Advocate)  
- Background: 5 years at Beta, promoted from analyst, BA UC Berkeley  
- **Top Interests**:
  1. Mobile App Enhancements (field team needs offline mode - mentioned 8 times!)
  2. User Experience (feedback: dashboard too cluttered)
  3. Analytics & Reporting (analysts need custom report templates)
- **Suggested Talking Points**: Roadmap for mobile offline mode, preview dashboard redesign, demo custom reporting

---

**MEETING PREP RECOMMENDATIONS**:

1. **For Sarah** (ROI focus): Prepare cost savings analysis showing how automation can reclaim 20 hrs/month
2. **For Michael** (security focus): Bring SOC 2 Type 2 cert, demo API integration with Salesforce
3. **For Emily** (UX focus): Preview mobile offline mode (in roadmap), show dashboard redesign mockups

**Renewal Context**: 4 months to renewal + expansion opportunity (50 additional licenses) - use this QBR to demonstrate value and set up renewal discussion.

**BRIEF COMPLETE** ✅

**Key Insight**: This prompt demonstrates the most comprehensive customer relationship intelligence in the framework. CAN-08 (historical retrieval) + CAN-09 (interest analysis) create personalized dossiers that go beyond static profiles - they analyze PATTERNS in past interactions to predict what each attendee will care about. Combined with CAN-22 (company research), the brief provides both individual-level (dossiers) and company-level (strategic priorities) context, enabling highly tailored meeting preparation.
```

---
- Final brief combines attendee dossiers (CAN-09) + company background (CAN-22)
- CAN-22 usage: External research for company intelligence

---

## Framework V2.0 Validation Summary

### Tasks Confirmed (22/25 used)

**Tier 1 - Universal (6 tasks, all used)**:
- ✅ CAN-01: Calendar Events Retrieval (100% - 9/9 prompts)
- ✅ CAN-02: Meeting Type Classification (56% - 5/9 prompts)
- ✅ CAN-03: Meeting Importance Assessment (56% - 5/9 prompts)
- ✅ CAN-04: Natural Language Understanding (100% - 9/9 prompts)
- ✅ CAN-05: Attendee/Contact Resolution (67% - 6/9 prompts)

**Tier 2 - Common (9 tasks, 8 used)**:
- ✅ CAN-06: Availability Checking (33% - 3/9)
- ✅ CAN-07: Meeting Metadata Extraction (78% - 7/9)
- ✅ CAN-08: Document/Content Retrieval (22% - 2/9)
- ✅ CAN-09: Document Generation (56% - 5/9)
- ✅ CAN-10: Time Aggregation (11% - 1/9)
- ✅ CAN-11: Priority/Preference Matching (22% - 2/9)
- ✅ CAN-12: Constraint Satisfaction (44% - 4/9)
- ✅ CAN-13: RSVP Status Update (22% - 2/9)
- ✅ CAN-14: Recommendation Engine (11% - 1/9)

**Tier 3 - Specialized (10 tasks, 8 used)**:
- ✅ CAN-15: Recurrence Rule Generation (11% - 1/9)
- ✅ CAN-16: Event Monitoring (11% - 1/9)
- ✅ CAN-17: Automatic Rescheduling (11% - 1/9)
- ✅ CAN-18: Objection/Risk Anticipation (11% - 1/9)
- ✅ CAN-19: Resource Booking (11% - 1/9)
- ✅ CAN-20: Data Visualization (11% - 1/9)
- ✅ CAN-21: Preparation Time Analysis (11% - 1/9)
- ✅ CAN-22: Research/Intelligence (11% - 1/9)
- ✅ CAN-23: Agenda Generation (11% - 1/9 - though this is debatable per human eval)
- ✅ **CAN-25: Event Annotation/Flagging (11% - 1/9 - NEW IN V2.0)**

**Not Used**:
- ❌ CAN-24: Multi-party Coordination/Negotiation (0%)

### Human Evaluation Insights

1. **NEW Task Validated**: CAN-25 (Event Annotation/Flagging) confirmed necessary for Organizer-2
2. **CAN-05 Critical**: Often missed by automated analysis but essential (Schedule-2, Collaborate-2)
3. **CAN-18 Scope**: Distinguish between meeting goals vs system tasks (Collaborate-1 lesson)
4. **CAN-16 Usage**: "Track" requirement maps to Event Monitoring (Organizer-2)
5. **CAN-23 Questionable**: Agenda generation vs conflict resolution (Schedule-2 usage debatable)

---

## Implementation Priority (Based on Frequency)

### Phase 1: Core Foundation (100% frequency) - **WEEKS 1-2**
1. CAN-04: Natural Language Understanding (100%)
2. CAN-01: Calendar Events Retrieval (100%)

### Phase 2: High Frequency (50%+ prompts) - **WEEKS 3-5**
3. CAN-07: Meeting Metadata Extraction (78%)
4. CAN-05: Attendee/Contact Resolution (67%)
5. CAN-02: Meeting Type Classification (56%)
6. CAN-03: Meeting Importance Assessment (56%)
7. CAN-09: Document Generation (56%)

### Phase 3: Medium Frequency (25-50% prompts) - **WEEKS 6-8**
8. CAN-12: Constraint Satisfaction (44%)
9. CAN-06: Availability Checking (33%)
10. CAN-11: Priority/Preference Matching (22%)
11. CAN-08: Document/Content Retrieval (22%)
12. CAN-13: RSVP Status Update (22%)

### Phase 4: Specialized Features (11% prompts each) - **WEEKS 9-12**
13-23. All Tier 3 tasks (CAN-14 through CAN-25)

---

## Cross-Prompt Analysis

### Task Usage Matrix

| Task ID | Task Name | Used In Prompts | Total | % |
|---------|-----------|-----------------|-------|---|
| CAN-04 | Natural Language Understanding | O1, O2, O3, S1, S2, S3, C1, C2, C3 | 9/9 | 100% |
| CAN-01 | Calendar Events Retrieval | O1, O2, O3, S1, S2, S3, C1, C2, C3 | 9/9 | 100% |
| CAN-07 | Meeting Metadata Extraction | O1, O2, O3, S2, S3, C2, C3 | 7/9 | 78% |
| CAN-05 | Attendee/Contact Resolution | O1, S1, S2, S3, C1, C2 | 6/9 | 67% |
| CAN-02 | Meeting Type Classification | O1, O3, S2, S3, C2 | 5/9 | 56% |
| CAN-03 | Meeting Importance Assessment | O1, O3, S2, S3, C2 | 5/9 | 56% |
| CAN-09 | Document Generation/Formatting | O3, S2, C1, C2, C3 | 5/9 | 56% |
| CAN-12 | Constraint Satisfaction | S1, S2, S3, O2 | 4/9 | 44% |
| CAN-06 | Availability Checking | S1, S2, S3 | 3/9 | 33% |
| CAN-08 | Document/Content Retrieval | O3, C3 | 2/9 | 22% |
| CAN-11 | Priority/Preference Matching | O1, O3 | 2/9 | 22% |
| CAN-13 | RSVP Status Update | O1, O2 | 2/9 | 22% |
| CAN-10 | Time Aggregation/Statistical Analysis | O3 | 1/9 | 11% |
| CAN-14 | Recommendation Engine | O3 | 1/9 | 11% |
| CAN-15 | Recurrence Rule Generation | S1 | 1/9 | 11% |
| CAN-16 | Event Monitoring/Change Detection | O2 | 1/9 | 11% |
| CAN-17 | Automatic Rescheduling | S1 | 1/9 | 11% |
| CAN-18 | Objection/Risk Anticipation | C2 | 1/9 | 11% |
| CAN-19 | Resource Booking | S3 | 1/9 | 11% |
| CAN-20 | Data Visualization/Reporting | O3 | 1/9 | 11% |
| CAN-21 | Focus Time/Preparation Time Analysis | O2 | 1/9 | 11% |
| CAN-22 | Research/Intelligence Gathering | C3 | 1/9 | 11% |
| CAN-23 | Agenda Generation/Structuring | S2 | 1/9 | 11% |
| **CAN-25** | **Event Annotation/Flagging (NEW)** | **O2** | **1/9** | **11%** |
| CAN-24 | Multi-party Coordination/Negotiation | (none) | 0/9 | 0% |

**Legend**: O1-O3 = Organizer 1-3, S1-S3 = Schedule 1-3, C1-C3 = Collaborate 1-3

**Observations**:
- **Universal Tasks** (100% coverage): CAN-01, CAN-04 (appear in all 9 prompts)
- **High-Frequency Common** (50-99% coverage): CAN-02, CAN-03, CAN-05, CAN-07, CAN-09
- **Medium-Frequency** (25-49%): CAN-06, CAN-12
- **Low-Frequency Specialized** (<25%): CAN-08, CAN-10, CAN-11, CAN-13-CAN-23, CAN-25
- **Unused**: CAN-24 (Multi-party Coordination) - no prompts required this capability

### Performance Metrics

_For detailed performance metrics from GPT-5 V2.0 3-trial stability test, see [GPT5_V2_OPTIMIZATION_SUMMARY.md](model_comparison/GPT5_V2_OPTIMIZATION_SUMMARY.md)._

**Key Results** (from GPT-5 validation testing):
- **Average F1 Score**: 80.07% ± 21.20%
- **Precision**: 87.41% ± 26.00% (EXCELLENT)
- **Recall**: 74.84% ± 17.02% (GOOD)
- **Consistency**: 95.33% (EXCELLENT - very high task selection agreement across trials)
- **CAN-25 Detection**: 100% (3/3 trials in Organizer-2, 0 false positives) ⭐

**Top Performing Prompts**:
1. Organizre-3: 98.04% F1 (time analysis - highest complexity)
2. Collaborate-2: 92.31% F1 (objection generation)
3. Collaborate-3: 92.31% F1 (meeting prep brief)
4. Organizer-2: 87.50% F1 (meeting tracking with CAN-25)

**Prompts Needing Attention**:
1. Collaborate-1: 25.00% F1 (CAN-18 over-interpretation issue)
2. Schedule-2: 66.67% F1 (missing CAN-05, CAN-06, CAN-23)

### Key Findings

#### 1. CAN-25 Successfully Validated ⭐
- **NEW Task Addition**: CAN-25 (Event Annotation/Flagging) added to V2.0 framework
- **Detection Rate**: 100% (3/3 trials in Organizer-2, 0 false positives)
- **Use Case**: "Flag any that require focus time" → Event annotation requirement
- **Conclusion**: Framework gap successfully identified and filled

#### 2. CAN-05 Often Missed but Critical ⚠️
- **Problem**: Automated analysis frequently overlooks attendee resolution
- **Evidence**: Missing from Schedule-2 and Collaborate-2 in initial GPT-5 output
- **Why Critical**: Required for scheduling (availability check) and collaboration (team resolution)
- **Recommendation**: Add explicit attendee resolution triggers to detection prompts

#### 3. Meeting Goals vs System Tasks Distinction 🎯
- **Issue**: CAN-18 (Risk Anticipation) over-applied in Collaborate-1
- **Root Cause**: "Discuss blocking issues" interpreted as system task, not meeting goal
- **Human Insight**: User wants to DISCUSS risks IN meeting, not have system FIND them beforehand
- **Framework Impact**: Need clearer boundaries between meeting agenda items vs system capabilities
- **Recommendation**: Document "goals as input vs tasks as execution" principle

#### 4. Framework Coverage Excellent 📊
- **Coverage**: 88% of framework used across 9 prompts (22 of 25 tasks)
- **Universal Tasks**: 100% coverage (all Tier 1 tasks represented)
- **Specialized Tasks**: 80% coverage (8 of 10 Tier 3 tasks used)
- **Unused Task**: Only CAN-24 (Multi-party Coordination) not exercised
- **Conclusion**: Framework is well-balanced and comprehensive

#### 5. Precision Improvement with V2.0 📈
- **V1.0 Precision**: 74.76%
- **V2.0 Precision**: 87.41% (+12.65% improvement) ⭐
- **Reason**: Better task boundary definitions (CAN-02/03 split, CAN-25 addition)
- **Trade-off**: Higher variance (21.20% vs 0.72%) due to diverse prompt complexity
- **Assessment**: Variance is natural (prompts range from 3-10 tasks), not instability

---

## Conclusions

### Framework Validation Success

The 25 canonical tasks V2.0 framework is validated by:
- **High Coverage**: 88% of framework used across diverse prompts (22 of 25 tasks)
- **Human Expert Validation**: All decompositions reviewed and corrected by domain expert
- **NEW Task Confirmed**: CAN-25 successfully identified and validated through evaluation
- **Clear Tier Structure**: Universal (100%), Common (89%), Specialized (80%) coverage confirms tiered design
- **GPT-5 Validation**: 95.33% consistency across 3 trials proves framework robustness

### Gold Standard Quality

This gold standard is production-ready:
- **100% Human Validation**: All 9 prompts reviewed by expert (Chin-Yew Lin)
- **Documented Edge Cases**: CAN-18 scope, CAN-05 criticality, meeting goals vs tasks
- **Clear Evaluation Status**: 5 correct, 3 partial, 1 needs review (with specific issues documented)
- **Actionable Insights**: 5 key findings with framework improvement recommendations
- **Reproducible**: Detailed execution compositions and example flows enable implementation

### Framework Enhancements in V2.0

1. **Task Renumbering**: CAN-02A/02B → CAN-02/03 for clarity
2. **NEW CAN-25**: Event Annotation/Flagging capability added
3. **Improved Boundaries**: Clearer distinctions between similar tasks
4. **Better Precision**: +12.65% improvement over V1.0 (87.41% vs 74.76%)
5. **Enhanced Documentation**: Execution compositions and example flows for all prompts

### Production Readiness Assessment

**Overall Grade**: **A- (Production-Ready with Minor Improvements)**

✅ **Strengths**:
- Comprehensive 25-task framework with 88% coverage
- Human-validated gold standard for all 9 prompts
- Excellent precision (87.41%) and consistency (95.33%)
- NEW CAN-25 successfully validated
- Clear tier structure and implementation priorities

⚠️ **Areas for Improvement**:
- CAN-05 detection needs strengthening (often missed)
- Meeting goals vs system tasks principle needs explicit documentation
- CAN-24 (Multi-party Coordination) needs test prompts
- Collaborate-1 low performance (25% F1) requires prompt optimization

🎯 **Ready For**:
- LLM evaluation benchmarking (use as ground truth)
- Production implementation (follow 4-phase priority plan)
- Framework validation testing (compare other models against this standard)
- Training data generation (fine-tuning and prompt engineering)

### Future Work

1. **Expand Test Coverage**: Add prompts exercising CAN-24 (Multi-party Coordination)
2. **Strengthen CAN-05 Detection**: Add explicit attendee resolution triggers
3. **Document Design Principles**: Formalize "meeting goals vs system tasks" distinction
4. **Optimize Low Performers**: Address Collaborate-1 (25% F1) and Schedule-2 (66.67% F1)
5. **Multi-Model Validation**: Test Claude, GPT-4, other models against this gold standard
6. **Expand Example Flows**: Add concrete examples for remaining prompts (Organizer-2, 3, Schedule 1-3, Collaborate-2, 3)

---

## Document Metadata

**Version**: 2.0  
**Created**: November 7, 2025  
**Last Updated**: November 7, 2025  
**Author**: Chin-Yew Lin  
**Total Prompts**: 9  
**Total Tasks**: 25 (CAN-01 through CAN-25)  
**Framework**: Calendar.AI Canonical Unit Tasks V2.0  
**Status**: ✅ Gold Standard Reference (Production-Ready)

**Validation**:
- ✅ Human expert review (Chin-Yew Lin - all 9 prompts)
- ✅ Cross-referenced with v2_gold_standard_20251107_145124.json
- ✅ Validated against GPT-5 V2.0 outputs (3 trials, 27 API calls)
- ✅ All 25 canonical tasks framework coverage assessed
- ✅ Consistent task application documented across prompts
- ✅ NEW CAN-25 validated with 100% detection rate

**Usage**:
This document serves as the authoritative reference for:
- **LLM Evaluation**: Benchmark GPT-5, Claude, GPT-4, and other models against human-validated decompositions
- **Training Data**: Ground truth for fine-tuning task decomposition models
- **Framework Validation**: Validate canonical tasks framework completeness and boundaries
- **Production QA**: Reference standard for production system task selection accuracy
- **Implementation Planning**: 4-phase priority roadmap based on task frequency

**Maintenance**:
- Update when canonical tasks framework evolves (new tasks, task splits, boundary clarifications)
- Add new hero prompts as they are created or discovered
- Incorporate learnings from production system performance (real-world validation)
- Align with GPT-5 stability test results and framework optimizations
- Document new edge cases and ambiguities as they emerge

**Related Files**:
- Source: `v2_gold_standard_20251107_145124.json`
- Validation Results: `GPT5_V2_OPTIMIZATION_SUMMARY.md`
- Framework Spec: `CANONICAL_TASKS_REFERENCE_V2.md`
- Writing Guide: `GOLD_STANDARD_REPORT_WRITING_GUIDE.md`

---

*End of Document*
