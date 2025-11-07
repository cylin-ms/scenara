# Hero Prompts Canonical Task Analysis - Gold Standard Reference V2.0

**Document Version**: 2.0  
**Date**: November 7, 2025  
**Author**: Chin-Yew Lin  
**Framework**: Calendar.AI Canonical Unit Tasks Framework V2.0 (25 tasks - renumbered CAN-01 through CAN-25)  
**Source**: Human-validated gold standard evaluation  
**Evaluation File**: `v2_gold_standard_20251107_145124.json`

---

## Document Summary

**Purpose**: This document serves as the gold standard reference for how the 25 canonical unit tasks compose to fulfill real Calendar.AI user prompts. Each decomposition has been human-validated and represents the ground truth for:
- LLM evaluation and comparison (GPT-5, Claude, etc.)
- Framework validation and refinement
- Training data for prompt engineering
- Implementation priority planning

**Methodology**: 4-phase validation process
1. **Framework Development** (Nov 7, 2025): Consolidated to 25 canonical tasks with human evaluation insights
2. **GPT-5 Baseline** (Nov 7, 2025): Initial decomposition using optimized prompts
3. **Human Evaluation** (Nov 7, 2025): Expert review with corrections and notes
4. **Gold Standard Creation** (Nov 7, 2025): Final validated decompositions with execution composition

**Statistics**:
- **Total Prompts**: 9 (3 Organizer, 3 Schedule, 3 Collaborate)
- **Total Canonical Tasks**: 25 (CAN-01 through CAN-25)
- **Tasks Used Across Prompts**: 22 unique tasks (88% coverage)
- **Average Tasks per Prompt**: 7.2 tasks
- **Task Usage Range**: 3-10 tasks per prompt

**Human Evaluation Results**:
- ✅ **Correct**: 5 prompts (Organizer-1, Organizre-3, Schedule-1, Schedule-3, Collaborate-3)
- ⚠️ **Partial**: 3 prompts (Organizer-2, Schedule-2, Collaborate-2) - missing specific tasks
- ❓ **Needs Review**: 1 prompt (Collaborate-1) - over-interpretation issue

**Key Insights from Evaluation**:
1. **NEW Task Needed**: CAN-25 for event annotation/flagging (Organizer-2: "flag meetings")
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

### Execution Composition

**Pattern**: Sequential with early classification parallelization

```
Step 1: CAN-04 (NLU) - Parse user priorities and intent
   ↓
Step 2: CAN-01 (Retrieval) - Get pending invitations
   ↓
Step 3: CAN-07 (Metadata) - Extract RSVP status and details
   ↓
Step 4-5: [PARALLEL] CAN-02 (Type Classification) + CAN-03 (Importance Assessment)
   ↓
Step 6: CAN-11 (Priority Matching) - Align with user priorities
   ↓
Step 7: CAN-13 (RSVP Update) - Accept/decline based on priority alignment
```

**Orchestration Notes**:
- Steps 4-5 can run in parallel (both operate on metadata)
- Error handling: Graceful degradation if classification fails
- User confirmation recommended before RSVP updates

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

### Execution Composition

**Pattern**: Simple sequential (3 steps only)

```
Step 1: CAN-04 (NLU) - Extract agenda requirements and goals
   ↓
Step 2: CAN-05 (Attendee Resolution) - Resolve product and marketing teams
   ↓
Step 3: CAN-09 (Agenda Generation) - Create structured agenda
```

**Orchestration Notes**:
- **CAN-18 NOT INCLUDED**: "Discuss blocking issues/risks" is a meeting GOAL, not a system task
- User wants to DISCUSS risks in the meeting, not have system ANTICIPATE them beforehand
- Simplest prompt (only 3 tasks) - agenda generation focused

**Key Learning**: Distinguish between meeting goals (input to CAN-09) vs system tasks (CAN-18)

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

**Document Status**: ✅ COMPLETE - Human-validated gold standard for 9 v2 hero prompts  
**Next Steps**: Use for LLM evaluation, framework validation, implementation planning  
**Version**: 2.0 (25 Canonical Tasks - including new CAN-25)
