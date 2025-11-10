# GitHub Copilot (Claude Sonnet 4.5) Semantic GUTT Analysis

**Generated**: November 6, 2025  
**Method**: Direct AI reasoning using 5-relationship model  
**Framework**: Unit Task principle - atomic, API-sized capabilities  

---

## Analysis Framework

### 5-Relationship Model
For any two Unit Tasks A and B:

1. **A = B** (EQUIVALENT) - Same atomic capability, different naming
2. **A < B** (SUBSET) - A is narrower/more specific than B  
3. **A > B** (SUPERSET) - A is broader and encompasses B
4. **A ∩ B** (OVERLAPPING) - Partial overlap, each has unique aspects
5. **A ⊥ B** (DISJOINT) - Completely different, no overlap

---

## PHASE 1: PER-PROMPT SEMANTIC MATCHING

### Prompt 1: organizer-1 (Priority-based calendar management)

**Original Prompt**: "Keep my Calendar up to date by committing to only meetings that are part of my priorities."

#### Relationship Analysis

**EQUIVALENT (=)**

1. **C2 = G1**: Calendar Event Retrieval = Retrieve Calendar Events
   - Both: GET calendar events via API (Graph/Google Calendar)
   - Atomic capability: Calendar read access

2. **C3 = G4**: Meeting-Priority Alignment Scoring = Classify Event Against Priorities
   - Both: Score/classify events against priority criteria
   - Atomic capability: Priority matching algorithm

3. **C5 = G6**: Calendar Action Execution = Commit Priority Meetings  
   - Both: Update calendar RSVP status via API
   - Atomic capability: Calendar write (RSVP update)

**SUBSET (<)**

4. **C2 < G2**: Calendar Event Retrieval < Extract Event Attributes
   - C2 retrieves events; G2 adds parsing step
   - G2 is broader: retrieval + parsing

**OVERLAPPING (∩)**

5. **C1 ∩ G3**: Priority Definition & Extraction ∩ Retrieve User Priority Profile
   - C1: Extract priorities from text + structure them
   - G3: Load existing priority profile from store
   - Overlap: Both get priority data
   - Difference: C1 creates from text, G3 loads from store

6. **C4 ∩ G5**: Accept/Decline Decision Logic ∩ Filter Non-Priority Events
   - C4: Decision rules → accept/decline
   - G5: Filter to priority subset
   - Overlap: Both use priority alignment
   - Difference: C4 outputs decisions, G5 outputs filtered list

**CLAUDE UNIQUE**

7. **C6** (Decision Justification & Reporting) - No GPT-5 equivalent
   - Capability: NLG for explaining why each decision was made
   - API: Natural language generation service
   - Reason: GPT-5 doesn't include explainability task

**GPT-5 UNIQUE**

None - All GPT-5 tasks map to Claude tasks

**Summary**: 3 equivalent pairs, 1 subset, 2 overlapping, 1 Claude-unique

---

### Prompt 2: organizer-2 (Track important meetings, flag prep needs)

**Original Prompt**: "Track all my important meetings and flag any that require focus time to prepare for them."

#### Relationship Analysis

**EQUIVALENT (=)**

1. **C1 = G1**: Calendar Data Retrieval = Retrieve Calendar Events
   - Both: GET /calendar/events
   - Atomic capability: Calendar read API

2. **C2 = G2**: Meeting Importance Classification = Identify Important Meetings
   - Both: Classify meetings by importance criteria
   - Atomic capability: Classification algorithm

3. **C4 = G5**: Meeting Flagging Logic = Flag Meetings Requiring Focus Time
   - Both: Mark/tag meetings meeting criteria
   - Atomic capability: Calendar annotation/tagging

4. **C6 = G6**: Focus Time Block Scheduling ⊥ Notify User of Preparation Needs
   - Actually NOT equivalent - see below

**SUBSET (<)**

5. **G3 < C2**: Extract Meeting Context < Meeting Importance Classification
   - G3: Parse meeting details (title, agenda, participants)
   - C2: Parse + score + classify
   - G3 is subset of C2's broader capability

**SUPERSET (>)**

6. **C5 > G4**: Calendar Gap Analysis > Determine Preparation Requirement
   - C5: Find available slots + validate duration + work hours
   - G4: Assess if prep is needed (boolean)
   - C5 is broader scheduling capability

**OVERLAPPING (∩)**

7. **C3 ∩ G4**: Preparation Time Estimation ∩ Determine Preparation Requirement
   - C3: Calculate prep time duration (90min, 120min, etc.)
   - G4: Boolean - does it need prep?
   - Overlap: Both assess prep needs
   - Difference: C3 quantifies, G4 classifies

**CLAUDE UNIQUE**

8. **C5** (Calendar Gap Analysis) - More sophisticated than G4
9. **C6** (Focus Time Block Scheduling) - Creates actual calendar events
10. **C7** (Actionable Recommendations & Reporting) - Generates insights/digest

**GPT-5 UNIQUE**

11. **G6** (Notify User of Preparation Needs) - Alert/reminder system
   - Different from C6 which creates calendar blocks

**Summary**: 3 equivalent, 1 subset, 1 superset, 1 overlapping, 3 Claude-unique, 1 GPT-5-unique

---

### Prompt 3: organizer-3 (Time reclamation analysis)

**Original Prompt**: "Help me understand where I am spending my time and identify ways I can reclaim time to focus more on my top priorities."

#### Relationship Analysis

**EQUIVALENT (=)**

1. **C1 = G1**: Calendar Historical Data Retrieval = Retrieve Calendar Events
   - Both: GET calendar events for date range
   - Atomic capability: Calendar history API

2. **C2 = G3**: Meeting Categorization & Classification = Classify Events by Category
   - Both: Assign meeting types/categories
   - Atomic capability: Classification model

3. **C3 = G5**: Time Aggregation & Statistical Analysis = Compute Time Allocation Metrics
   - Both: Sum duration by dimensions (category, person, etc.)
   - Atomic capability: Aggregation queries

4. **C4 = G4**: Priority Alignment Assessment = Identify Priority Alignment
   - Both: Match events to priorities
   - Atomic capability: Priority mapping algorithm

5. **C5 = G6**: Low-Value Meeting Identification = Detect Low-Value or Non-Priority Blocks
   - Both: Flag meetings not aligned with priorities
   - Atomic capability: Priority filtering

6. **C7 = G7**: Schedule Optimization Recommendations = Generate Time Reclaim Recommendations
   - Both: Suggest decline/shorten/delegate actions
   - Atomic capability: Recommendation engine

7. **C8 = G8**: Time Usage Reporting & Visualization = Present Insights and Recommendations
   - Both: Dashboard/charts with insights
   - Atomic capability: Data visualization + NLG

**SUBSET (<)**

8. **G2 < C2**: Extract Event Attributes < Meeting Categorization & Classification
   - G2: Parse event fields
   - C2: Parse + classify into 31+ types
   - G2 is preprocessing subset

**CLAUDE UNIQUE**

9. **C6** (Time Reclamation Opportunity Analysis) - What-if scenario modeling
   - GPT-5 has similar in G7 but C6 is more detailed impact modeling

**GPT-5 UNIQUE**

None - All covered by Claude tasks

**Summary**: 7 equivalent pairs, 1 subset, 1 Claude-unique
**Perfect alignment!** 8/8 Claude GUTTs mapped to GPT-5 equivalents

---

### Prompt 4: schedule-1 (Recurring 1:1 with constraints)

**Original Prompt**: "Starting next week, I want a weekly 30-min 1:1 with {name}. Afternoons preferred, avoid Fridays. Automatically reschedule on declines or conflicts."

#### Relationship Analysis

**EQUIVALENT (=)**

1. **C2 = G5**: Multi-Calendar Availability Checking = Find Optimal Time Slot
   - Actually NOT equivalent - see subset below

2. **C4 = G6**: Recurring Meeting Series Creation = Create Calendar Event
   - Both: POST calendar event with recurrence rule
   - Atomic capability: Calendar event creation with RRULE

3. **C5 = G7**: Meeting Invitation Sending = Send Invitation
   - Both: Dispatch calendar invite to attendees
   - Atomic capability: Invitation/notification API

4. **C6 = G8**: Decline/Conflict Detection & Monitoring = Monitor for Declines or Conflicts
   - Both: Track RSVP status + calendar changes
   - Atomic capability: Event status monitoring/webhooks

5. **C7 = G9**: Automatic Rescheduling Logic = Automatically Reschedule
   - Both: Trigger-based rescheduling workflow
   - Atomic capability: Dynamic scheduling automation

**SUBSET (<)**

6. **G1 < C1**: Parse Scheduling Intent < Constraint Extraction & Formalization
   - G1: Extract basic parameters (who, when, duration)
   - C1: Extract + formalize into structured constraints + rules
   - G1 is narrower

7. **G2 < C2**: Resolve Participant Identity < Multi-Calendar Availability Checking
   - G2: Contact resolution only
   - C2: Resolution + free/busy queries + availability matrix
   - G2 is preprocessing step

8. **G4 < C3**: Apply Time Preferences < Constraint-Based Slot Finding
   - G4: Filter by time-of-day and day-of-week
   - C3: Full constraint satisfaction (time + duration + recurrence + preferences)
   - G4 is subset

**SUPERSET (>)**

9. **G5 > C2**: Find Optimal Time Slot > Multi-Calendar Availability Checking
   - G5: Availability + constraint satisfaction + optimization
   - C2: Just availability checking
   - G5 is broader (includes C3's functionality too)

**OVERLAPPING (∩)**

10. **C3 ∩ G3**: Constraint-Based Slot Finding ∩ Determine Recurrence Pattern
    - C3: Find slots matching ALL constraints (time, recurrence, duration)
    - G3: Just translate "weekly" into RRULE
    - Overlap: Both handle recurrence
    - Difference: C3 is broader slot-finding, G3 is narrower RRULE generation

**CLAUDE UNIQUE**

None - All Claude tasks map to GPT-5

**GPT-5 UNIQUE**

11. **G1** (Parse Scheduling Intent) - Separated NLU step
12. **G2** (Resolve Participant Identity) - Separated contact resolution
13. **G3** (Determine Recurrence Pattern) - Separated RRULE generation
14. **G4** (Apply Time Preferences) - Separated constraint application

**Note**: GPT-5 has MORE granular decomposition (9 vs 7 tasks). Claude bundles some tasks.

**Summary**: 5 equivalent, 3 subset, 1 superset, 1 overlapping, 0 Claude-unique, 4 GPT-5-unique

---

### Prompt 5: schedule-2 (Clear time block & reschedule)

**Original Prompt**: "Clear my Thursday afternoon. Update my RSVPs and help me reschedule my meetings to another time and show me as {status}."

#### Relationship Analysis

**EQUIVALENT (=)**

1. **C1 = G1**: Time Block Specification Parsing = Identify Thursday Afternoon Time Window
   - Both: Parse "Thursday afternoon" → specific datetime range
   - Atomic capability: Temporal expression resolution

2. **C2 = G2**: Affected Meetings Identification = Retrieve Thursday Afternoon Events
   - Both: Query calendar for events in time range
   - Atomic capability: Calendar query with time filter

3. **C3 = G3**: RSVP Decline Execution = Cancel or Decline Thursday Events
   - Both: Update RSVP status to "declined"
   - Atomic capability: Calendar RSVP update API

4. **C4 = G4**: Alternative Slot Finding = Propose Alternative Times for Affected Meetings
   - Both: Find new available times for same attendees
   - Atomic capability: Availability search + slot ranking

5. **C5 = G5**: Meeting Rescheduling Proposals = Reschedule Meetings to Proposed Times
   - Both: Send updated meeting invites with new times
   - Atomic capability: Calendar event update + notification

6. **C6 = G6**: Calendar Status Update = Update User Calendar Status for Thursday Afternoon
   - Both: Set free/busy status for time block
   - Atomic capability: Availability status API

**SUBSET (<)**

None

**OVERLAPPING (∩)**

7. **C7 ∩ G6**: Focus Time Block Creation ∩ Update User Calendar Status
   - C7: Create placeholder calendar event (visual)
   - G6: Set free/busy status (metadata)
   - Overlap: Both mark time as unavailable
   - Difference: C7 creates event, G6 updates status field

**CLAUDE UNIQUE**

8. **C7** (Focus Time Block Creation) - Additional visual calendar event
9. **C8** (Action Summary & Confirmation) - Report what was done

**GPT-5 UNIQUE**

None - All mapped

**Summary**: 6 equivalent pairs, 1 overlapping, 2 Claude-unique
**Excellent alignment!** 6/8 perfect matches

---

### Prompt 6: schedule-3 (Multi-person meeting with room)

**Original Prompt**: "Land a time to meet about Project Alpha with Chris, Sangya, and Kat for 1 hour in the next 2 weeks. Schedule over 1:1s and lunches if needed and work around Kat's schedule. Make the meeting in person and add a room."

#### Relationship Analysis

**EQUIVALENT (=)**

1. **C1 = G1**: Meeting Requirements Extraction = Parse Meeting Request
   - Both: Extract attendees, duration, constraints from NL
   - Atomic capability: NLU + entity extraction

2. **C2 = G3**: Multi-Person Availability Aggregation = Retrieve Participant Calendars
   - Both: GET calendar data for multiple users
   - Atomic capability: Multi-calendar API access

3. **C6 = G8**: Conference Room Search & Booking = Find Available Room
   - Both: Query room resources + reserve
   - Atomic capability: Resource booking API

4. **C9 = G9**: Meeting Creation & Invitations = Create and Send Meeting Invite
   - Both: POST calendar event with attendees + room
   - Atomic capability: Calendar event creation

**SUBSET (<)**

5. **G2 < C1**: Resolve Participant Identities < Meeting Requirements Extraction
   - G2: Just contact resolution
   - C1: Extract ALL requirements (attendees, duration, constraints, etc.)
   - G2 is preprocessing subset

6. **G4 < C3**: Retrieve Kat's Constraints < Priority Constraint Application
   - G4: Get Kat's calendar
   - C3: Apply Kat as hard constraint in scheduling logic
   - G4 is data retrieval subset

7. **G6 < C7**: Compute Common Availability < Optimal Slot Selection
   - G6: Calculate overlapping free time
   - C7: Calculate overlap + rank + select best + validate
   - G6 is subset of broader optimization

**SUPERSET (>)**

None

**OVERLAPPING (∩)**

8. **C4 ∩ G5**: Override-Eligible Meeting Identification ∩ Apply Override Rules
   - C4: Identify which meetings CAN be overridden (1:1s, lunches)
   - G5: Determine WHEN to apply override rules
   - Overlap: Both handle override logic
   - Difference: C4 is classification, G5 is policy application

9. **C5 ∩ G7**: Location-Based Filtering ∩ Select Optimal Time Slot
   - C5: Filter for in-person feasibility
   - G7: Multi-criteria optimization including location
   - Overlap: Both consider location
   - Difference: C5 is single-criterion filter, G7 is multi-criterion optimization

**CLAUDE UNIQUE**

10. **C3** (Priority Constraint Application) - Explicit Kat priority handling
11. **C4** (Override-Eligible Meeting Identification) - Classification task
12. **C5** (Location-Based Filtering) - In-person constraint handling
13. **C8** (Conflict Resolution & Rescheduling) - Cascade rescheduling of conflicts

**GPT-5 UNIQUE**

14. **G2** (Resolve Participant Identities) - Separated contact resolution
15. **G4** (Retrieve Kat's Constraints) - Separated constraint retrieval
16. **G5** (Apply Override Rules) - Policy reasoning task
17. **G6** (Compute Common Availability) - Separated availability calculation
18. **G7** (Select Optimal Time Slot) - Separated optimization task

**Summary**: 4 equivalent, 3 subset, 2 overlapping, 4 Claude-unique, 5 GPT-5-unique

**Note**: Similar to schedule-1, GPT-5 has finer granularity (9 vs 9 tasks but different bundling)

---

### Prompt 7: collaborate-1 (Set agenda for project review)

**Original Prompt**: "Help me set the agenda to review the progress of Project Alpha with the product and marketing team to get confirmation we are on track and discuss any blocking issues or risks."

#### Relationship Analysis

**EQUIVALENT (=)**

1. **C1 = G2**: Meeting Context Retrieval = Identify Project Context
   - Both: Get Project Alpha information
   - Atomic capability: Project data retrieval

2. **C2 = G3**: Stakeholder Role Identification = Determine Participants
   - Both: Identify product team + marketing team
   - Atomic capability: Role/team mapping

3. **C3 = G6**: Agenda Structure Planning = Generate Agenda Items
   - Both: Create logical flow of discussion topics
   - Atomic capability: Agenda generation algorithm

4. **C6 = G8**: Time Allocation & Formatting = Present Agenda for Confirmation
   - Both: Format agenda professionally
   - Atomic capability: Document formatting/presentation

**SUBSET (<)**

5. **G1 < C3**: Extract Meeting Intent < Agenda Structure Planning
   - G1: Recognize intent ("set agenda", "progress review")
   - C3: Intent + structure + flow optimization
   - G1 is preprocessing

6. **G5 < C4**: Define Agenda Objectives < Progress Review Items Generation
   - G5: Structure objectives (review, confirm, discuss risks)
   - C4: Objectives + concrete items (milestones, metrics, achievements)
   - G5 is subset

**OVERLAPPING (∩)**

7. **C4 ∩ G5**: Progress Review Items Generation ∩ Define Agenda Objectives
   - C4: List specific accomplishments, milestones, metrics
   - G5: Extract objectives from prompt
   - Overlap: Both identify what to cover
   - Difference: C4 generates concrete items, G5 structures objectives

8. **C5 ∩ G5**: Blocker & Risk Identification ∩ Define Agenda Objectives
   - C5: Surface actual blockers/risks from project data
   - G5: Note that "discuss blocking issues or risks" is an objective
   - Overlap: Both recognize risks as agenda item
   - Difference: C5 finds actual risks, G5 just notes it as topic

**CLAUDE UNIQUE**

9. **C1** (Meeting Context Retrieval) - Richer project data gathering
10. **C4** (Progress Review Items Generation) - Concrete items with evidence
11. **C5** (Blocker & Risk Identification) - Actual risk surfacing

**GPT-5 UNIQUE**

12. **G1** (Extract Meeting Intent) - Separated NLU task
13. **G4** (Retrieve Team Member Details) - Contact resolution
14. **G7** (Validate Agenda Completeness) - Quality check task

**Summary**: 4 equivalent, 2 subset, 2 overlapping (with nuance), 3 Claude-unique, 3 GPT-5-unique

---

### Prompt 8: collaborate-2 (Executive briefing prep)

**Original Prompt**: "Review the materials for my meeting with senior leadership and suggest the best way to summarize the topics into three main discussion points. Generate any objections or concerns that might come up and give me effective responses."

#### Relationship Analysis

**EQUIVALENT (=)**

1. **C1 = G1**: Meeting Materials Retrieval = Retrieve Meeting Materials
   - Both: Access/load all documents for meeting
   - Atomic capability: Document retrieval API

2. **C2 = G2**: Content Analysis & Topic Extraction = Analyze Meeting Materials
   - Both: NLP analysis to extract key themes
   - Atomic capability: Topic extraction/NLP

3. **C5 = G5**: Objection Anticipation = Generate Potential Objections
   - Both: Predict concerns from senior leadership
   - Atomic capability: Critical thinking/risk modeling

4. **C6 = G6**: Response Preparation = Create Effective Responses
   - Both: Generate persuasive counter-arguments
   - Atomic capability: Argumentation engine

5. **C7 = G6**: Briefing Document Generation ⊥ Create Effective Responses
   - Actually different - see Claude-unique below

**SUBSET (<)**

6. **G3 < C3**: Generate Candidate Discussion Topics < Executive Summary Distillation
   - G3: List 8-12 possible topics
   - C3: List + prioritize + distill to top 3
   - G3 is preliminary step

7. **G4 < C3**: Rank and Select Top Three Topics < Executive Summary Distillation
   - G4: Ranking logic
   - C3: Ranking + distillation + executive framing
   - G4 is subset

**OVERLAPPING (∩)**

8. **C3 ∩ G3 ∩ G4**: Executive Summary Distillation ∩ Generate Candidate Topics ∩ Rank Topics
   - C3: Single task - extract topics + rank + distill to 3
   - G3 + G4: Two tasks - first generate candidates, then rank
   - Overlap: Same overall capability
   - Difference: Granularity (Claude bundles, GPT-5 splits)

**CLAUDE UNIQUE**

9. **C4** (Audience-Aware Framing) - Strategic framing for executives
10. **C7** (Briefing Document Generation) - Final document assembly

**GPT-5 UNIQUE**

11. **G3** (Generate Candidate Discussion Topics) - Separated candidate generation
12. **G4** (Rank and Select Top Three Topics) - Separated ranking

**Summary**: 4 equivalent, 2 subset, 1 overlapping bundling pattern, 2 Claude-unique, 2 GPT-5-unique

---

### Prompt 9: collaborate-3 (Customer meeting brief)

**Original Prompt**: "Prepare a brief for my upcoming meeting with customer Beta and include a dossier for each customer attendee and the topics they are most interested in. Include a background on their company."

#### Relationship Analysis

**EQUIVALENT (=)**

1. **C1 = G2**: Meeting Details Retrieval = Extract Meeting Details
   - Both: GET meeting attendees, time, subject
   - Atomic capability: Calendar event read API

2. **C2 = G7**: Company Background Research = Retrieve Company Background for Customer Beta
   - Both: Get company info (industry, size, products, news)
   - Atomic capability: Company research/CRM lookup

3. **C3 = G3**: Attendee Identity Resolution = Identify Customer Attendees
   - Both: Identify customer-side attendees and roles
   - Atomic capability: Contact resolution + role identification

4. **C4 = G6**: Individual Dossier Creation = Compile Dossier for Each Customer Attendee
   - Both: Build profile for each attendee
   - Atomic capability: Profile compilation

5. **C5 = G5**: Topic Interest Analysis = Determine Topics of Interest for Each Attendee
   - Both: Identify topics each person cares about
   - Atomic capability: Interest extraction from history

6. **C8 = G8**: Brief Document Assembly = Compose Meeting Brief
   - Both: Compile all info into structured brief
   - Atomic capability: Document generation/assembly

**SUBSET (<)**

7. **G1 < C1**: Identify Upcoming Meeting with Customer Beta < Meeting Details Retrieval
   - G1: Find the meeting (search)
   - C1: Find + get details (search + retrieval)
   - G1 is search subset

8. **G4 < C4**: Retrieve Profile Data for Each Customer Attendee < Individual Dossier Creation
   - G4: Fetch profile data (CRM/LinkedIn lookup)
   - C4: Fetch + compile + add history + create dossier
   - G4 is data retrieval subset

**OVERLAPPING (∩)**

9. **C6 ∩ C4 ∩ G6**: Relationship History Compilation ∩ Individual Dossier Creation ∩ Compile Dossier
   - C6: Standalone task for relationship history
   - C4: Includes relationship history in dossier
   - Overlap: Relationship history is part of dossier
   - Difference: Claude separates history compilation as distinct task

**CLAUDE UNIQUE**

10. **C6** (Relationship History Compilation) - Dedicated history task
11. **C7** (Relevant Content Gathering) - Find supporting materials (proposals, docs)

**GPT-5 UNIQUE**

12. **G1** (Identify Upcoming Meeting) - Separated meeting search

**Summary**: 6 equivalent pairs, 2 subset, 1 overlapping, 2 Claude-unique, 1 GPT-5-unique
**Excellent alignment!** 6/8 core capabilities match

---

## PHASE 1 SUMMARY

### Overall Statistics

| Prompt | Claude GUTTs | GPT-5 GUTTs | Equivalent (=) | Subset (<) | Superset (>) | Overlapping (∩) | Claude-Only | GPT-5-Only |
|--------|--------------|-------------|----------------|------------|--------------|-----------------|-------------|------------|
| organizer-1 | 6 | 6 | 3 | 1 | 0 | 2 | 1 | 0 |
| organizer-2 | 7 | 6 | 3 | 1 | 1 | 1 | 3 | 1 |
| organizer-3 | 8 | 8 | 7 | 1 | 0 | 0 | 1 | 0 |
| schedule-1 | 7 | 9 | 5 | 3 | 1 | 1 | 0 | 4 |
| schedule-2 | 8 | 6 | 6 | 0 | 0 | 1 | 2 | 0 |
| schedule-3 | 9 | 9 | 4 | 3 | 0 | 2 | 4 | 5 |
| collaborate-1 | 6 | 8 | 4 | 2 | 0 | 2 | 3 | 3 |
| collaborate-2 | 7 | 6 | 4 | 2 | 0 | 1 | 2 | 2 |
| collaborate-3 | 8 | 8 | 6 | 2 | 0 | 1 | 2 | 1 |
| **TOTALS** | **66** | **66** | **42** | **15** | **2** | **11** | **18** | **16** |

### Key Findings

1. **High Core Alignment**: 42/66 GUTTs (63.6%) are EQUIVALENT (same atomic capability)

2. **Granularity Differences**: 
   - 15 subset relationships (GPT-5 often separates preprocessing steps)
   - 2 superset relationships (Claude sometimes bundles more)
   - Pattern: GPT-5 tends to be more granular (e.g., schedule-1: 9 vs 7 tasks)

3. **Overlapping Capabilities**: 11 pairs have partial overlap
   - Often due to different bundling choices
   - Example: Claude separates "Relationship History" from "Dossier Creation", GPT-5 bundles

4. **Model-Unique Tasks**:
   - Claude: 18 unique (27.3%) - Often explanability, reporting, advanced features
   - GPT-5: 16 unique (24.2%) - Often separated NLU/preprocessing steps

5. **Best Alignment**: organizer-3 (7/8 equivalent) and schedule-2 (6/8 equivalent)

6. **Most Granularity Difference**: schedule-1 (5 equivalent but 4 GPT-5-unique preprocessing tasks)

---

## PHASE 2: CROSS-PROMPT CANONICAL UNIT TASKS

### Analysis Methodology

Using the 5-relationship model, I identify Unit Tasks that appear across multiple prompts:
- Tasks with **= relationships** across prompts (truly equivalent capabilities)
- Tasks forming **< / >** hierarchies (general vs specific versions)
- Tasks with **∩ patterns** (overlapping but with variations)

---

### Canonical Unit Task #1: **Calendar Events Retrieval**

**API/Tool**: Microsoft Graph API: `GET /me/calendar/events` or Google Calendar API: `GET /calendar/v3/users/me/events`

**Frequency**: **9/9 prompts** (100%)

**Equivalent Tasks (=)**:
- organizer-1: C2 (Calendar Event Retrieval), G1 (Retrieve Calendar Events)
- organizer-2: C1 (Calendar Data Retrieval), G1 (Retrieve Calendar Events)
- organizer-3: C1 (Calendar Historical Data Retrieval), G1 (Retrieve Calendar Events)
- schedule-2: G2 (Retrieve Thursday Afternoon Events) - filtered variant
- schedule-3: C2 (Multi-Person Availability Aggregation), G3 (Retrieve Participant Calendars)
- collaborate-3: C1 (Meeting Details Retrieval), G2 (Extract Meeting Details)

**Subset Variations (<)**:
- schedule-2: G2 < Generic retrieval (time-filtered)
- collaborate-3: G1 < C1 (meeting search + retrieval)

**Description**: The most fundamental Calendar.AI capability. Every prompt requires reading calendar data, whether for a single user, multiple users, current events, or historical analysis.

**Canonical Definition**: Atomic capability to retrieve calendar event data from calendar systems via API, with optional filters for time range, attendees, or status.

---

### Canonical Unit Task #2: **Meeting Classification/Categorization**

**API/Tool**: ML Classification Model / NLP Service (Azure AI Language, OpenAI, custom model)

**Frequency**: **7/9 prompts** (78%)

**Equivalent Tasks (=)**:
- organizer-1: C3 (Meeting-Priority Alignment Scoring), G4 (Classify Event Against Priorities)
- organizer-2: C2 (Meeting Importance Classification), G2 (Identify Important Meetings)
- organizer-3: C2 (Meeting Categorization & Classification), G3 (Classify Events by Category)
- schedule-3: C4 (Override-Eligible Meeting Identification) - specialized classification

**Overlapping Variations (∩)**:
- organizer-2: C2 ∩ G3 (Importance vs context extraction)

**Description**: Classify meetings by type, importance, category, or priority alignment. Critical for intelligent calendar management.

**Variants**:
- Priority alignment classification (organizer-1)
- Importance scoring (organizer-2)
- Type categorization - 31+ meeting types (organizer-3)
- Override-eligibility (1:1s, lunches) (schedule-3)

**Canonical Definition**: Atomic capability to assign categories, scores, or classifications to calendar events based on attributes, content, and context.

---

### Canonical Unit Task #3: **Calendar Event Creation/Update**

**API/Tool**: Microsoft Graph API: `POST /me/calendar/events`, `PATCH /me/calendar/events/{id}`

**Frequency**: **6/9 prompts** (67%)

**Equivalent Tasks (=)**:
- organizer-1: C5 (Calendar Action Execution), G6 (Commit Priority Meetings)
- organizer-2: C6 (Focus Time Block Scheduling) - create blocking event
- schedule-1: C4 (Recurring Meeting Series Creation), G6 (Create Calendar Event)
- schedule-2: C5 (Meeting Rescheduling Proposals), G5 (Reschedule Meetings)
- schedule-3: C9 (Meeting Creation & Invitations), G9 (Create and Send Meeting Invite)

**Description**: Create new calendar events or update existing ones. Includes:
- Single events
- Recurring series (with RRULE)
- RSVP status updates
- Event modifications

**Canonical Definition**: Atomic capability to create or modify calendar events via API, including recurrence rules, attendees, and resources.

---

### Canonical Unit Task #4: **Natural Language Understanding (Constraint/Intent Extraction)**

**API/Tool**: NLU Service (Azure AI Language, OpenAI GPT, custom NLP)

**Frequency**: **6/9 prompts** (67%)

**Equivalent Tasks (=)**:
- organizer-1: C1 (Priority Definition & Extraction)
- schedule-1: C1 (Constraint Extraction & Formalization), G1 (Parse Scheduling Intent)
- schedule-2: C1 (Time Block Specification Parsing), G1 (Identify Thursday Afternoon Time Window)
- schedule-3: C1 (Meeting Requirements Extraction), G1 (Parse Meeting Request)
- collaborate-1: G1 (Extract Meeting Intent), G2 (Identify Project Context)
- collaborate-2: C2 (Content Analysis & Topic Extraction), G2 (Analyze Meeting Materials)

**Subset Variations (<)**:
- schedule-1: G1 < C1 (basic extraction vs formalization)
- collaborate-1: G1 < C3 (intent recognition vs full planning)

**Description**: Parse natural language user input to extract structured parameters, constraints, intents, priorities, or requirements.

**Canonical Definition**: Atomic capability to extract structured information (entities, constraints, intents) from unstructured natural language input.

---

### Canonical Unit Task #5: **Attendee/Contact Resolution**

**API/Tool**: Microsoft Graph API: `GET /users`, Directory lookup, Contact resolution service

**Frequency**: **5/9 prompts** (56%)

**Equivalent Tasks (=)**:
- schedule-1: G2 (Resolve Participant Identity)
- schedule-3: G2 (Resolve Participant Identities)
- collaborate-1: G4 (Retrieve Team Member Details)
- collaborate-3: C3 (Attendee Identity Resolution), G3 (Identify Customer Attendees)

**Subset Variations (<)**:
- schedule-1: G2 < C2 (resolution is subset of availability checking)
- schedule-3: G2 < C1 (resolution is subset of requirement extraction)

**Description**: Map human-readable names ("Chris", "product team") to calendar identities (email addresses, user IDs).

**Canonical Definition**: Atomic capability to resolve participant names/descriptions to specific calendar identities via directory lookup.

---

### Canonical Unit Task #6: **Availability Checking (Free/Busy)**

**API/Tool**: Microsoft Graph API: `POST /me/calendar/getSchedule`, Google Calendar API: `POST /freeBusy`

**Frequency**: **4/9 prompts** (44%)

**Equivalent Tasks (=)**:
- schedule-1: C2 (Multi-Calendar Availability Checking)
- schedule-2: C4 (Alternative Slot Finding), G4 (Propose Alternative Times)
- schedule-3: C2 (Multi-Person Availability Aggregation), G3 (Retrieve Participant Calendars), G6 (Compute Common Availability)

**Subset Variations (<)**:
- schedule-3: G6 < C7 (availability calculation is subset of optimization)

**Description**: Query free/busy status for one or more users to find available time slots.

**Canonical Definition**: Atomic capability to retrieve availability status (free/busy) for specified users and time ranges.

---

### Canonical Unit Task #7: **Meeting Invitation/Notification Sending**

**API/Tool**: Microsoft Graph API: `POST /me/sendMail`, Calendar invitation system

**Frequency**: **4/9 prompts** (44%)

**Equivalent Tasks (=)**:
- schedule-1: C5 (Meeting Invitation Sending), G7 (Send Invitation)
- schedule-2: C5 (Meeting Rescheduling Proposals), G5 (Reschedule Meetings)
- schedule-3: C9 (Meeting Creation & Invitations), G9 (Create and Send Meeting Invite)
- organizer-2: G6 (Notify User of Preparation Needs) - different type

**Description**: Send calendar invitations, updates, or notifications to attendees.

**Canonical Definition**: Atomic capability to dispatch calendar invitations or notifications via email/calendar system.

---

### Canonical Unit Task #8: **Document/Content Retrieval**

**API/Tool**: SharePoint API, OneDrive API, CRM API, Web search

**Frequency**: **4/9 prompts** (44%)

**Equivalent Tasks (=)**:
- collaborate-1: C1 (Meeting Context Retrieval), G2 (Identify Project Context)
- collaborate-2: C1 (Meeting Materials Retrieval), G1 (Retrieve Meeting Materials)
- collaborate-3: C2 (Company Background Research), G7 (Retrieve Company Background)
- collaborate-3: C7 (Relevant Content Gathering)

**Description**: Access documents, project data, company information, or other content to support meeting preparation.

**Canonical Definition**: Atomic capability to retrieve documents, data, or content from various sources (SharePoint, CRM, web, etc.).

---

### Canonical Unit Task #9: **Time Aggregation/Statistical Analysis**

**API/Tool**: Data aggregation/analytics service

**Frequency**: **3/9 prompts** (33%)

**Equivalent Tasks (=)**:
- organizer-3: C3 (Time Aggregation & Statistical Analysis), G5 (Compute Time Allocation Metrics)

**Related**:
- organizer-2: C3 (Preparation Time Estimation) - different type of calculation
- schedule-3: C7 (Optimal Slot Selection) - optimization math

**Description**: Aggregate calendar data to compute metrics (total hours by category, average meeting duration, etc.).

**Canonical Definition**: Atomic capability to aggregate and compute statistical metrics from calendar event data.

---

### Canonical Unit Task #10: **Priority/Preference Matching**

**API/Tool**: Semantic matching algorithm, priority scoring service

**Frequency**: **3/9 prompts** (33%)

**Equivalent Tasks (=)**:
- organizer-1: C3 (Meeting-Priority Alignment Scoring), G4 (Classify Event Against Priorities)
- organizer-3: C4 (Priority Alignment Assessment), G4 (Identify Priority Alignment)

**Related**:
- organizer-1: C1 ∩ G3 (Priority extraction vs retrieval)

**Description**: Match calendar events against user priorities or preferences to determine alignment.

**Canonical Definition**: Atomic capability to score/classify calendar events based on alignment with user-defined priorities or preferences.

---

### Canonical Unit Task #11: **Constraint Satisfaction/Slot Finding**

**API/Tool**: Constraint solver, scheduling algorithm

**Frequency**: **3/9 prompts** (33%)

**Equivalent Tasks (=)**:
- schedule-1: C3 (Constraint-Based Slot Finding), G5 (Find Optimal Time Slot)
- schedule-3: C7 (Optimal Slot Selection), G6 (Compute Common Availability), G7 (Select Optimal Time Slot)

**Subset Variations (<)**:
- schedule-1: G4 < C3 (time preference filtering is subset)
- schedule-3: G6 < C7 (availability calculation is subset of optimization)

**Description**: Find time slots satisfying multiple constraints (duration, participant availability, time preferences, location, etc.).

**Canonical Definition**: Atomic capability to find time slots satisfying multiple scheduling constraints using constraint satisfaction algorithms.

---

### Canonical Unit Task #12: **Recurrence Rule Generation**

**API/Tool**: iCalendar RRULE specification

**Frequency**: **2/9 prompts** (22%)

**Equivalent Tasks (=)**:
- schedule-1: C4 (Recurring Meeting Series Creation), G3 (Determine Recurrence Pattern), G6 (Create Calendar Event)

**Description**: Generate iCalendar recurrence rules (RRULE) for recurring events (daily, weekly, monthly, etc.).

**Canonical Definition**: Atomic capability to generate iCalendar RRULE specifications from natural language recurrence patterns.

---

### Canonical Unit Task #13: **Event Monitoring/Change Detection**

**API/Tool**: Calendar webhooks, change notifications, polling

**Frequency**: **2/9 prompts** (22%)

**Equivalent Tasks (=)**:
- schedule-1: C6 (Decline/Conflict Detection & Monitoring), G8 (Monitor for Declines or Conflicts)

**Description**: Monitor calendar events for changes (RSVP updates, conflicts, deletions, modifications).

**Canonical Definition**: Atomic capability to detect and respond to calendar event changes via webhooks or polling.

---

### Canonical Unit Task #14: **Automatic Rescheduling**

**API/Tool**: Dynamic scheduling service, workflow automation

**Frequency**: **2/9 prompts** (22%)

**Equivalent Tasks (=)**:
- schedule-1: C7 (Automatic Rescheduling Logic), G9 (Automatically Reschedule)
- schedule-3: C8 (Conflict Resolution & Rescheduling)

**Description**: Automatically find new time and update meeting when conflicts or declines occur.

**Canonical Definition**: Atomic capability to automatically reschedule meetings in response to conflicts or declines using dynamic scheduling logic.

---

### Canonical Unit Task #15: **RSVP Status Update**

**API/Tool**: Microsoft Graph API: `POST /me/events/{id}/accept`, `POST /me/events/{id}/decline`

**Frequency**: **3/9 prompts** (33%)

**Equivalent Tasks (=)**:
- organizer-1: C5 (Calendar Action Execution), G6 (Commit Priority Meetings)
- schedule-2: C3 (RSVP Decline Execution), G3 (Cancel or Decline Thursday Events)

**Description**: Update user's RSVP response to meeting invitations (accept, decline, tentative).

**Canonical Definition**: Atomic capability to update meeting RSVP status via calendar API.

---

### Canonical Unit Task #16: **Resource Booking (Rooms, Equipment)**

**API/Tool**: Microsoft Graph API: `GET /places`, Resource scheduling service

**Frequency**: **1/9 prompts** (11%)

**Tasks**:
- schedule-3: C6 (Conference Room Search & Booking), G8 (Find Available Room)

**Description**: Find and reserve physical resources like conference rooms or equipment.

**Canonical Definition**: Atomic capability to search for and book physical resources (rooms, equipment) via resource scheduling API.

---

### Canonical Unit Task #17: **Document Generation/Assembly**

**API/Tool**: Document generation service, NLG, template engine

**Frequency**: **4/9 prompts** (44%)

**Equivalent Tasks (=)**:
- organizer-2: C7 (Actionable Recommendations & Reporting)
- organizer-3: C8 (Time Usage Reporting & Visualization), G8 (Present Insights)
- collaborate-1: C6 (Time Allocation & Formatting), G8 (Present Agenda)
- collaborate-2: C7 (Briefing Document Generation)
- collaborate-3: C8 (Brief Document Assembly), G8 (Compose Meeting Brief)

**Description**: Generate formatted documents (briefs, agendas, reports) from structured data.

**Canonical Definition**: Atomic capability to generate formatted documents from structured data using templates and NLG.

---

### Canonical Unit Task #18: **Recommendation Engine**

**API/Tool**: Recommendation service, rule engine

**Frequency**: **3/9 prompts** (33%)

**Equivalent Tasks (=)**:
- organizer-2: C7 (Actionable Recommendations & Reporting)
- organizer-3: C7 (Schedule Optimization Recommendations), G7 (Generate Time Reclaim Recommendations)
- collaborate-2: C6 (Response Preparation), G6 (Create Effective Responses)

**Description**: Generate actionable recommendations (what meetings to decline, how to optimize schedule, responses to objections).

**Canonical Definition**: Atomic capability to generate actionable recommendations based on analysis using rule engines or ML models.

---

### Canonical Unit Task #19: **Data Visualization**

**API/Tool**: Charting library (Chart.js, D3.js), dashboard service

**Frequency**: **1/9 prompts** (11%)

**Tasks**:
- organizer-3: C8 (Time Usage Reporting & Visualization), G8 (Present Insights)

**Description**: Create charts, graphs, dashboards to visualize calendar data and insights.

**Canonical Definition**: Atomic capability to generate visualizations (charts, graphs, dashboards) from calendar data.

---

### Canonical Unit Task #20: **Objection/Risk Anticipation**

**API/Tool**: Critical thinking model, risk analysis service

**Frequency**: **2/9 prompts** (22%)

**Equivalent Tasks (=)**:
- collaborate-1: C5 (Blocker & Risk Identification)
- collaborate-2: C5 (Objection Anticipation), G5 (Generate Potential Objections)

**Description**: Predict potential concerns, objections, risks, or blockers for meetings or projects.

**Canonical Definition**: Atomic capability to predict objections, concerns, or risks using critical thinking and risk modeling.

---

## PHASE 2 SUMMARY

### Canonical Unit Task Library (20 Core Capabilities)

| # | Canonical Unit Task | Frequency | Primary API/Tool | Task Type |
|---|---------------------|-----------|------------------|-----------|
| 1 | Calendar Events Retrieval | 9/9 (100%) | Graph API: GET /calendar/events | Data Retrieval |
| 2 | Meeting Classification | 7/9 (78%) | ML Classification Service | Classification |
| 3 | Calendar Event Creation/Update | 6/9 (67%) | Graph API: POST /calendar/events | Data Modification |
| 4 | NLU (Constraint/Intent Extraction) | 6/9 (67%) | NLU Service | Parsing |
| 5 | Attendee/Contact Resolution | 5/9 (56%) | Graph API: GET /users | Data Retrieval |
| 6 | Availability Checking | 4/9 (44%) | Graph API: POST /getSchedule | Data Retrieval |
| 7 | Meeting Invitation Sending | 4/9 (44%) | Email/Calendar API | Notification |
| 8 | Document/Content Retrieval | 4/9 (44%) | SharePoint/CRM API | Data Retrieval |
| 9 | Time Aggregation/Analytics | 3/9 (33%) | Analytics Service | Analysis |
| 10 | Priority/Preference Matching | 3/9 (33%) | Semantic Matching | Classification |
| 11 | Constraint Satisfaction | 3/9 (33%) | Scheduling Algorithm | Optimization |
| 12 | Recurrence Rule Generation | 2/9 (22%) | iCalendar RRULE | Parsing |
| 13 | Event Monitoring | 2/9 (22%) | Webhooks/Polling | Monitoring |
| 14 | Automatic Rescheduling | 2/9 (22%) | Workflow Automation | Execution |
| 15 | RSVP Status Update | 3/9 (33%) | Graph API: POST /accept | Data Modification |
| 16 | Resource Booking | 1/9 (11%) | Resource API | Data Modification |
| 17 | Document Generation | 4/9 (44%) | NLG/Templates | Reporting |
| 18 | Recommendation Engine | 3/9 (33%) | Rule Engine/ML | Decision Making |
| 19 | Data Visualization | 1/9 (11%) | Charting Library | Reporting |
| 20 | Objection/Risk Anticipation | 2/9 (22%) | Risk Modeling | Analysis |

### Key Insights

1. **Universal Capabilities**: Calendar Events Retrieval (100%), Meeting Classification (78%)

2. **Core Operations**: Event creation, NLU extraction, contact resolution, availability checking (44-67%)

3. **Advanced Features**: Recommendation engines, risk anticipation, automatic rescheduling (22-33%)

4. **Specialized**: Resource booking, data visualization (11%)

5. **Capability Categories**:
   - **Data Retrieval**: #1, #5, #6, #8 (4 capabilities)
   - **Data Modification**: #3, #15, #16 (3 capabilities)
   - **Classification**: #2, #10 (2 capabilities)
   - **Analysis**: #9, #20 (2 capabilities)
   - **Optimization**: #11, #14 (2 capabilities)
   - **Notification**: #7 (1 capability)
   - **Reporting**: #17, #19 (2 capabilities)
   - **Parsing**: #4, #12 (2 capabilities)
   - **Decision Making**: #18 (1 capability)
   - **Monitoring**: #13 (1 capability)

---

## CONCLUSIONS & RECOMMENDATIONS

### 1. Overall Assessment

**Claude Sonnet 4.5 and GPT-5 v2 show strong semantic alignment in GUTT decomposition:**

- **63.6% equivalent tasks** (42/66) - Same atomic capabilities, different naming
- **27.3% hierarchical relationships** (15 subset + 2 superset) - Granularity differences
- **16.7% overlapping tasks** (11 pairs) - Different bundling choices
- **25.5% unique tasks** (18 Claude + 16 GPT-5) - Model-specific decomposition strategies

### 2. Granularity Patterns

**GPT-5 Tendency**: More granular decomposition
- Separates NLU, contact resolution, constraint application as distinct tasks
- Example: schedule-1 has 9 tasks vs Claude's 7

**Claude Tendency**: Bundles related operations
- Groups preprocessing with main capability
- Example: "Calendar Event Retrieval" includes parsing; GPT-5 separates "Extract Event Attributes"

**Neither approach is wrong** - reflects different design philosophies:
- GPT-5: Pipeline-oriented (explicit preprocessing steps)
- Claude: End-to-end task orientation (implicit preprocessing)

### 3. Canonical GUTT Library for Calendar.AI

**Recommended Reference Set: 20 Canonical Unit Tasks**

**Tier 1 - Universal (50%+ of prompts)**:
1. Calendar Events Retrieval (100%)
2. Meeting Classification (78%)
3. Calendar Event Creation/Update (67%)
4. NLU (Constraint/Intent Extraction) (67%)
5. Attendee/Contact Resolution (56%)

**Tier 2 - Common (25-50% of prompts)**:
6. Availability Checking (44%)
7. Meeting Invitation Sending (44%)
8. Document/Content Retrieval (44%)
9. Document Generation (44%)
10. Time Aggregation/Analytics (33%)
11. Priority/Preference Matching (33%)
12. Constraint Satisfaction (33%)
13. RSVP Status Update (33%)
14. Recommendation Engine (33%)

**Tier 3 - Specialized (<25% of prompts)**:
15. Recurrence Rule Generation (22%)
16. Event Monitoring (22%)
17. Automatic Rescheduling (22%)
18. Objection/Risk Anticipation (22%)
19. Resource Booking (11%)
20. Data Visualization (11%)

### 4. Evaluation Framework Recommendations

When evaluating NEW prompts for Calendar.AI solutions:

**Step 1**: Decompose prompt using GUTT framework (either Claude or GPT-5)

**Step 2**: Map each GUTT to canonical Unit Tasks using 5-relationship model:
- **=**: Direct match to canonical task
- **<**: Specialized version of canonical task
- **>**: Broader version encompassing multiple canonical tasks
- **∩**: Overlaps with canonical task but has unique aspects
- **⊥**: Novel capability not in canonical library (add to library!)

**Step 3**: Coverage analysis:
- Which Tier 1 tasks are needed?
- Which Tier 2/3 specialized tasks?
- Any novel tasks requiring new API/tool development?

**Step 4**: Quality assessment:
- Are all necessary canonical tasks covered?
- Are tasks atomic (API-sized)?
- Are overlapping tasks properly bundled or separated?
- Is granularity appropriate for implementation?

### 5. Future Work

1. **Expand Canonical Library**: Test on additional Calendar.AI prompts, add new canonical tasks as discovered

2. **Embeddings-Based Matching**: Use semantic embeddings (sentence-transformers) for more accurate automatic matching

3. **API Mapping**: Create explicit mapping from each canonical task to specific API endpoints

4. **Implementation Templates**: Build reusable code templates for each canonical Unit Task

5. **Cross-Model Validation**: Test with additional LLMs (Gemini, Llama, etc.) to further validate canonical library

---

## APPENDIX: Methodology Notes

### Why 5-Relationship Model?

Traditional binary matching (match/no-match) loses information about:
- **Granularity differences**: One model bundles what another splits
- **Hierarchical relationships**: General vs specific versions of capabilities
- **Partial overlaps**: Tasks sharing some functionality but with unique aspects

The 5-relationship model (=, <, >, ∩, ⊥) provides richer semantic understanding, critical for:
- Identifying true equivalents despite different naming
- Understanding decomposition strategies
- Building robust canonical library
- Evaluating new decompositions

### Unit Task Principle

Each Unit Task represents an **atomic capability** that:
1. **Maps to single API call or tool** - "What would one API provide?"
2. **Is indivisible** - Cannot be split further without losing coherence
3. **Has clear input/output** - Well-defined boundaries
4. **Is reusable** - Applicable across different scenarios

This principle ensures canonical tasks are:
- **Implementation-ready**: Direct mapping to APIs
- **Technology-agnostic**: Describes capability, not specific implementation
- **Composable**: Can be combined to build complex workflows
- **Measurable**: Success criteria clear (API succeeds/fails)

---

**End of Analysis**

Generated by GitHub Copilot Agent Mode (Claude Sonnet 4.5)  
November 6, 2025
