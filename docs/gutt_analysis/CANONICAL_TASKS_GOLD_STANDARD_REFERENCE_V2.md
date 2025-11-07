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

### Execution Composition

**Pattern**: Sequential with parallel classification + specialized flagging

```
Step 1: CAN-04 (NLU) - Parse tracking and flagging requirements
   ↓
Step 2: CAN-01 (Retrieval) - Get upcoming meetings
   ↓
Step 3: CAN-07 (Metadata) - Extract meeting details
   ↓
Step 4-5: [PARALLEL] CAN-02 (Type) + CAN-03 (Importance)
   ↓
Step 6: CAN-21 (Prep Time) - Estimate preparation time needed
   ↓
Step 7: CAN-11 (Priority Match) - Filter to important meetings
   ↓
Step 8-9: [PARALLEL] CAN-16 (Monitoring) + CAN-25 (Flagging)
```

**Orchestration Notes**:
- CAN-21 critical for CAN-25 (prep time estimates drive flagging logic)
- CAN-16 and CAN-25 can run in parallel (independent operations)
- CAN-25 (NEW) implements conditional event annotation

**V2.0 Framework Impact**: This prompt drove the creation of CAN-25 (Event Annotation/Flagging)

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

### Execution Composition

**Pattern**: Sequential with parallel classification + final reporting

```
Step 1: CAN-04 (NLU) - Parse time analysis and reclamation intent
   ↓
Step 2: CAN-01 (Retrieval) - Get historical + upcoming meetings
   ↓
Step 3: CAN-07 (Metadata) - Extract meeting details
   ↓
Step 4-5: [PARALLEL] CAN-02 (Type) + CAN-03 (Importance)
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

### Execution Composition

**Pattern**: Sequential with constraint resolution + automation setup

```
Step 1: CAN-04 (NLU) - Parse scheduling requirements
   ↓
Step 2: CAN-05 (Attendee Resolution) - Resolve "{name}"
   ↓
Step 3: CAN-01 (Retrieval) - Get existing calendar
   ↓
Step 4: CAN-06 (Availability) - Find afternoon slots (not Friday)
   ↓
Step 5: CAN-12 (Constraints) - Select best time slot
   ↓
Step 6: CAN-15 (Recurrence) - Generate weekly RRULE
   ↓
Step 7: CAN-03 (Event Creation) - Create recurring meeting
   ↓
Step 8: CAN-16 (Monitoring) - Setup change detection
   ↓
Step 9: CAN-17 (Auto-reschedule) - Enable automatic rescheduling
```

**Orchestration Notes**:
- CAN-05 must complete before CAN-06 (need attendee calendar)
- CAN-16 → CAN-17 dependency (monitoring enables auto-reschedule)
- Steps 8-9 are automation setup (one-time configuration)

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

### Execution Composition

**Pattern**: Sequential with metadata extraction enabling parallelization

```
Step 1: CAN-04 (NLU) - Parse rescheduling requirements
   ↓
Step 2: CAN-01 (Retrieval) - Get Thursday afternoon meetings
   ↓
Step 3: CAN-07 (Metadata) - Extract attendees and RSVP status
   ↓
Step 4: CAN-05 (Attendee Resolution) - Resolve attendees for coordination
   ↓
Step 5-6: [PARALLEL] CAN-13 (RSVP Update) + CAN-06 (Availability Check)
   ↓
Step 7: CAN-12 (Constraints) - Select best alternative times
   ↓
Step 8: CAN-23 (Agenda/Plan) - Generate rescheduling proposal
   ↓
Step 9: CAN-03 (Event Update) - Update calendar with new times
```

**Orchestration Notes**:
- CAN-05 critical dependency for CAN-06 (need attendee calendars)
- CAN-13 and CAN-06 can run in parallel after CAN-05
- User confirmation recommended before CAN-03 (final updates)

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

### Execution Composition

**Pattern**: Sequential with parallel analysis + final booking

```
Step 1: CAN-04 (NLU) - Parse complex constraints
   ↓
Step 2: CAN-05 (Attendee Resolution) - Resolve Chris, Sangya, Kat
   ↓
Step 3: CAN-01 (Retrieval) - Get all 3 calendars
   ↓
Step 4: CAN-07 (Metadata) - Extract meeting details
   ↓
Step 5-6: [PARALLEL] CAN-02 (Type Classification) + CAN-03 (Importance)
   ↓
Step 7: CAN-06 (Availability) - Find slots (work around Kat)
   ↓
Step 8: CAN-12 (Constraints) - Select best time (complex logic)
   ↓
Step 9-10: [PARALLEL] CAN-19 (Room Booking) + CAN-03 (Event Creation)
```

**Orchestration Notes**:
- "Work around Kat" = hard constraint (must respect Kat's schedule)
- "Schedule over 1:1s/lunches" = soft constraint (override if needed)
- CAN-19 and CAN-03 can run in parallel (independent operations)
- Conflict resolution: Project Alpha > 1:1s/lunches

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

### Execution Composition

**Pattern**: Sequential with document processing

```
Step 1: CAN-04 (NLU) - Parse preparation requirements
   ↓
Step 2: CAN-05 (Attendee Resolution) - Identify senior leadership
   ↓
Step 3: CAN-01 (Retrieval) - Find upcoming senior leadership meeting
   ↓
Step 4: CAN-07 (Metadata) - Extract meeting details and attachments
   ↓
Step 5: CAN-08 (Document Retrieval) - Get meeting materials
   ↓
Step 6: CAN-09 (Summarization) - Create 3 main discussion points
   ↓
Step 7: CAN-18 (Objections) - Generate objections + responses
```

**Orchestration Notes**:
- CAN-05 critical dependency for CAN-01 (must know who senior leadership is)
- CAN-07 → CAN-08 dependency (need attachments list)
- CAN-18 explicitly requested by user (vs Collaborate-1 where it was over-interpretation)

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

### Execution Composition

**Pattern**: Sequential with parallel research + generation

```
Step 1: CAN-04 (NLU) - Parse brief requirements
   ↓
Step 2: CAN-01 (Retrieval) - Find customer Beta meeting
   ↓
Step 3: CAN-07 (Metadata) - Extract customer attendees
   ↓
Step 4: CAN-05 (Attendee Resolution) - Resolve to full profiles
   ↓
Step 5: CAN-08 (Document Retrieval) - Get historical materials
   ↓
Step 6-7: [PARALLEL] CAN-09 (Brief Generation) + CAN-22 (Company Research)
```

**Orchestration Notes**:
- CAN-09 and CAN-22 can run in parallel (independent research)
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
