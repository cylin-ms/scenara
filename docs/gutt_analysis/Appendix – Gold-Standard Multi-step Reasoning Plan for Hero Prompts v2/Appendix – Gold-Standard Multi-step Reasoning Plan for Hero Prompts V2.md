# Appendix – Gold-Standard Multi-step Reasoning Plan for Hero Prompts V2.0

**Document Version**: 2.0  
**Date**: November 7, 2025  
**Author**: Chin-Yew Lin  
**Framework**: Calendar.AI Canonical Unit Tasks Framework V2.0 (25 tasks - CAN-01 through CAN-25)  
**Source**: Human-validated gold standard evaluation  

**Related Documents**:
- [CANONICAL_TASKS_GOLD_STANDARD_REFERENCE_V2.md](../CANONICAL_TASKS_GOLD_STANDARD_REFERENCE_V2.md) - Complete gold standard with detailed decompositions
- [CANONICAL_TASKS_REFERENCE_V2.md](../CANONICAL_TASKS_REFERENCE_V2.md) - Complete specifications for all 25 canonical tasks
- [CANONICAL_TASKS_CAPABILITY_INVENTORY_V2.md](../CANONICAL_TASKS_CAPABILITY_INVENTORY_V2.md) - Infrastructure-centric capability inventory

---

## Overview

This appendix provides **concise multi-step reasoning plans** for all 9 Calendar.AI v2 hero prompts, showing how canonical tasks orchestrate to answer each prompt. Each plan maps user intent to atomic agent capabilities in a clear step-by-step format.

**Key Features**:
- ✅ **V2.0 Framework**: Uses 25 canonical tasks (CAN-01 through CAN-25)
- ✅ **Human-Validated**: Based on expert evaluation of v2 prompts
- ✅ **NEW Task**: Includes CAN-25 (Event Annotation/Flagging)
- ✅ **Critical Dependencies**: Highlights essential tasks like CAN-05 (Attendee Resolution)

**Changes from V1.0**:
- **Renumbered Tasks**: CAN-02A/CAN-02B → CAN-02/CAN-03 (sequential 1-25)
- **NEW Task Added**: CAN-25 for event flagging/annotation (Organizer-2)
- **Missing Tasks Identified**: CAN-05 added to Schedule-2, Collaborate-2 (human evaluation)
- **Scope Clarifications**: CAN-18 removed from Collaborate-1 (over-interpretation)

---

## 1) Organizer-1 Prompt: "Keep my Calendar up to date by committing to only meetings that are part of my priorities."

**Evaluation**: ✅ **Correct**  
**Total Tasks**: 7

| Steps | Atomic Agent Capabilities (V2.0 Framework) |
| ------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1. Understand User Intent | · **CAN-04** (Natural Language Understanding): Extract user priorities and time constraints from the prompt<br>· Parse: "keep calendar up to date", "commit to only meetings", "part of my priorities"<br>· Output: Intent = manage calendar based on priorities |
| 2. Retrieve Pending Invitations | · **CAN-01** (Calendar Events Retrieval): Retrieve all pending calendar invitations<br>· Filter: RSVP status = "pending" OR "tentative"<br>· Time range: Current + upcoming meetings |
| 3. Extract Meeting Metadata | · **CAN-07** (Meeting Metadata Extraction): Extract detailed metadata from pending invitations<br>· For each invitation: attendees, subject, organizer, agenda, RSVP status, date/time |
| 4. Classify & Analyze Meetings | · **CAN-02** (Meeting Type Classification): Classify each pending invitation by meeting type (1:1, team sync, customer, etc.)<br>· **CAN-03** (Meeting Importance Assessment): Assess strategic importance of each meeting relative to user priorities<br>· Note: CAN-02 and CAN-03 can run in parallel |
| 5. Match Against Priorities | · **CAN-11** (Priority/Preference Matching): Compare meetings against user's stated priorities<br>· Calculate priority alignment scores (0-100%)<br>· Rank meetings by priority match strength |
| 6. Execute RSVP Actions | · **CAN-13** (RSVP Status Update): Update RSVP status based on prioritization decisions<br>· Accept: High priority matches (>80% alignment)<br>· Tentative: Medium priority matches (40-80%)<br>· Decline: Low priority matches (<40%) |

**Key Orchestration**: CAN-04 → CAN-01 → CAN-07 → [CAN-02 + CAN-03 parallel] → CAN-11 → CAN-13

**Critical Dependencies**:
- CAN-07 (Metadata Extraction) enables CAN-13 (RSVP Update)
- CAN-11 (Priority Matching) determines RSVP decisions

---

## 2) Organizer-2 Prompt: "Track all my important meetings and flag any that require focus time to prepare for them."

**Evaluation**: ⚠️ **Partial** - Missing CAN-25 in original GPT-5 analysis (added by human evaluator)  
**Total Tasks**: 9 (includes NEW CAN-25)

| Steps | Atomic Agent Capabilities (V2.0 Framework) |
| ------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1. Understand User Intent | · **CAN-04** (Natural Language Understanding): Extract dual intent (track + flag)<br>· Parse: "track all my important meetings" = monitoring requirement<br>· Parse: "flag any that require focus time" = conditional annotation |
| 2. Retrieve Upcoming Meetings | · **CAN-01** (Calendar Events Retrieval): Retrieve all upcoming meetings within planning horizon<br>· Time range: Next 2-4 weeks (typical planning window) |
| 3. Extract Meeting Context | · **CAN-07** (Meeting Metadata Extraction): Extract meeting details to assess complexity<br>· For each meeting: attendees, subject, agenda, attachments, organizer<br>· Complexity signals: Agenda length, attachment count, attendee seniority |
| 4. Classify & Assess Meetings | · **CAN-02** (Meeting Type Classification): Classify meetings by format (1:1, exec review, customer, etc.)<br>· **CAN-03** (Meeting Importance Assessment): Identify which meetings qualify as "important"<br>· High-prep types: Executive reviews, board meetings, customer presentations |
| 5. Estimate Preparation Time | · **CAN-21** (Focus Time/Preparation Time Analysis): Estimate prep time needed for each meeting<br>· Based on: Meeting type, attendees, complexity, agenda length<br>· Output: Prep time estimates (e.g., "90 min prep for executive review") |
| 6. Filter Important Meetings | · **CAN-11** (Priority/Preference Matching): Filter to "important meetings" based on criteria<br>· Apply importance threshold to identify tracking targets |
| 7. Setup Meeting Tracking | · **CAN-16** (Event Monitoring/Change Detection): Setup tracking/monitoring for important meetings<br>· Configure: Change notifications, update alerts, cancellation monitoring<br>· Addresses "track" requirement |
| 8. Flag Prep-Required Meetings | · **CAN-25** (Event Annotation/Flagging): Flag meetings requiring focus time with visual indicators<br>· **NEW in V2.0**: Conditional event flagging capability<br>· Apply flags/annotations (e.g., "⚠️ 90 min prep needed")<br>· Addresses "flag any that require focus time" requirement |

**Key Orchestration**: CAN-04 → CAN-01 → CAN-07 → [CAN-02 + CAN-03] → CAN-21 → CAN-11 → [CAN-16 + CAN-25]

**Human Evaluator Notes**:
> "Missing 'track important meetings' and 'flag meetings need time for preparation'. Can we attribute 'track' to CAN-16? But we do not have any Canonical task for 'flag'. 'Flag' is an action that we add an annotation to an event on calendar. We need to add new canonical tasks for similar tasks that signal something on calendar if some predefined condition occurs."

**V2.0 Framework Evolution**: CAN-25 (Event Annotation/Flagging) was added based on this human evaluation insight.

---

## 3) Organizre-3 Prompt: "Help me understand where I am spending my time and identify ways I can reclaim time to focus more on my top priorities."

**Evaluation**: ✅ **Correct**  
**Total Tasks**: 9

| Steps | Atomic Agent Capabilities (V2.0 Framework) |
| ---------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1. Understand User Intent | · **CAN-04** (Natural Language Understanding): Extract user intent for time analysis and reclamation focus<br>· Parse: "where I am spending my time" = historical analysis<br>· Parse: "identify ways to reclaim time" = optimization recommendations |
| 2. Retrieve Historical Calendar Data | · **CAN-01** (Calendar Events Retrieval): Load historical calendar events for analysis<br>· Time range: Past 1-3 months (historical lookback)<br>· Include: All completed and upcoming meetings |
| 3. Extract Meeting Metadata | · **CAN-07** (Meeting Metadata Extraction): Extract meeting details for analysis<br>· For each meeting: attendees, subject, duration, recurrence, organizer |
| 4. Classify & Assess Meetings | · **CAN-02** (Meeting Type Classification): Classify past meetings by type for categorization<br>· **CAN-03** (Meeting Importance Assessment): Assess which past meetings aligned with top priorities<br>· Categories: 1:1s, team syncs, customer meetings, planning, admin, etc. |
| 5. Aggregate Time Statistics | · **CAN-10** (Time Aggregation/Statistical Analysis): Compute time spent per category<br>· Aggregate by: Meeting type, participant, project, priority alignment<br>· Calculate: Total hours, percentages, trends over time |
| 6. Match Against Priorities | · **CAN-11** (Priority/Preference Matching): Analyze alignment with user's top priorities<br>· Identify: High-value vs low-value meetings<br>· Calculate: Gap between current spend vs desired priorities |
| 7. Generate Reclamation Recommendations | · **CAN-14** (Recommendation Engine): Generate specific time reclamation opportunities<br>· Identify: Low-value recurring meetings to decline<br>· Suggest: Meeting consolidation, delegation, shortening opportunities |
| 8. Create Visual Representations | · **CAN-20** (Data Visualization/Reporting): Create visual time distribution reports<br>· Charts: Pie chart (time by type), bar chart (hours per week), heatmap (meeting density)<br>· Dashboard: Priority alignment gauge, trend lines |

**Key Orchestration**: CAN-04 → CAN-01 → CAN-07 → [CAN-02 + CAN-03] → CAN-10 → CAN-11 → [CAN-14 + CAN-20 parallel]

**Critical Insights**:
- Historical analysis focus (1-3 months lookback)
- CAN-10 (Time Aggregation) feeds both CAN-14 and CAN-20
- Most complex prompt: Uses 9 tasks across all tiers

---

## 4) Schedule-1 Prompt: "Starting next week, I want a weekly 30-min 1:1 with {name}. Afternoons preferred, avoid Fridays. Automatically reschedule on declines or conflicts."

**Evaluation**: ✅ **Correct**  
**Total Tasks**: 9

| Steps | Atomic Agent Capabilities (V2.0 Framework) |
| -------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1. Parse Scheduling Requirements | · **CAN-04** (Natural Language Understanding): Extract scheduling requirements<br>· Parse: Duration (30 min), participant ({name}), recurrence (weekly), start time (next week)<br>· Parse constraints: "Afternoons preferred", "avoid Fridays", "automatically reschedule" |
| 2. Resolve Participant Identity | · **CAN-05** (Attendee/Contact Resolution): Resolve {name} to full contact profile<br>· Lookup: Email address, calendar access, timezone<br>· Output: Participant identity for availability checking |
| 3. Check Availability | · **CAN-06** (Availability Checking): Check user's and {name}'s availability<br>· Find: Common free slots for next week and ongoing<br>· Apply: "Afternoons preferred", "avoid Fridays" constraints |
| 4. Analyze Constraints | · **CAN-12** (Constraint Satisfaction): Find time slots satisfying all constraints<br>· Constraints: 30 min duration, weekly recurrence, afternoon slot, not Friday<br>· Select: Optimal recurring time slot (e.g., "Tuesday 2:00 PM weekly") |
| 5. Generate Recurrence Pattern | · **CAN-15** (Recurrence Rule Generation): Create iCalendar RRULE for weekly pattern<br>· RRULE: "FREQ=WEEKLY;BYDAY=TU;BYHOUR=14" (example: Tuesday 2 PM weekly)<br>· Validate: No end date (ongoing) or specify count/until |
| 6. Create Recurring Meeting | · **CAN-13** (Calendar Event Creation): Create recurring calendar event<br>· Title: "1:1 with {name}"<br>· Duration: 30 min<br>· Recurrence: Per CAN-15 RRULE<br>· Attendees: User + {name} |
| 7. Setup Automatic Rescheduling | · **CAN-16** (Event Monitoring/Change Detection): Setup monitoring for declines/conflicts<br>· Monitor: Decline notifications, new conflict events<br>· Trigger: Automatic rescheduling workflow when detected |
| 8. Configure Auto-Reschedule Workflow | · **CAN-17** (Automatic Rescheduling): Setup orchestrated workflow for auto-rescheduling<br>· Workflow: Detect decline → Find alternative slot (CAN-06 + CAN-12) → Update calendar → Notify<br>· Dependencies: CAN-06 (Availability), CAN-12 (Constraints), CAN-13 (Update) |

**Key Orchestration**: CAN-04 → CAN-05 → CAN-06 → CAN-12 → CAN-15 → CAN-13 → CAN-16 → CAN-17

**Critical Dependencies**:
- CAN-05 required to resolve participant before checking availability
- CAN-17 (Auto-Rescheduling) orchestrates multiple tasks (CAN-06, CAN-12, CAN-13)
- Complex workflow automation with event-driven triggers

---

## 5) Schedule-2 Prompt: "Clear my Thursday afternoon. Update my RSVPs and help me reschedule my meetings to another time and show me as {status}."

**Evaluation**: ⚠️ **Partial** - Missing CAN-05 in original GPT-5 analysis (added by human evaluator)  
**Total Tasks**: 9

| Steps | Atomic Agent Capabilities (V2.0 Framework) |
| --------------------------------- | -------------------------------------------------------------------------------------------------------- |
| 1. Understand Rescheduling Requirements | · **CAN-04** (Natural Language Understanding): Parse multi-action request<br>· Parse: "Clear my Thursday afternoon" = time block to free up<br>· Parse: "Update my RSVPs" = change response status<br>· Parse: "reschedule my meetings" = find alternative slots<br>· Parse: "show me as {status}" = calendar status display |
| 2. Retrieve Thursday Meetings | · **CAN-01** (Calendar Events Retrieval): Load meetings in target time block<br>· Time range: Thursday 12:00 PM - 5:00 PM (afternoon)<br>· Filter: Meetings where user is attendee |
| 3. Extract Meeting Metadata | · **CAN-07** (Meeting Metadata Extraction): Get detailed meeting information<br>· For each meeting: Attendee lists, organizer, duration, recurrence, RSVP status<br>· Extract: Context for rescheduling decisions |
| 4. Resolve All Attendees | · **CAN-05** (Attendee/Contact Resolution): Resolve attendees for coordination<br>· **CRITICAL - MISSING IN ORIGINAL**: Cannot check availability without this!<br>· Resolve: Full contact details, calendar URLs, timezones<br>· Human evaluator note: "Model needs to get metadata, and from there to find attendee for those meetings" |
| 5. Update RSVPs | · **CAN-13** (RSVP Status Update): Decline or mark tentative for Thursday meetings<br>· For each meeting: Update user's RSVP to "Declined" or "Tentative" based on {status}<br>· Send: RSVP update notifications to organizers |
| 6. Find Alternative Time Slots | · **CAN-06** (Availability Checking): Find alternative times for rescheduling<br>· Input: Resolved attendees from CAN-05 + meeting durations from CAN-07<br>· Check: Common availability across all attendees<br>· Constraints: Avoid Thursday afternoon, find slots within next 1-2 weeks |
| 7. Select Optimal Alternatives | · **CAN-12** (Constraint Satisfaction): Apply preferences to select best slots<br>· Preferences: Minimize conflicts, respect calendar patterns<br>· Validation: Ensure selected times don't conflict with existing commitments |
| 8. Generate Rescheduling Plan | · **CAN-23** (Agenda Generation/Structuring): Create rescheduling proposal document<br>· Format: Structured plan showing old time → new time for each meeting<br>· Include: Rationale for each change, attendees for review |
| 9. Update Calendar | · **CAN-13** (Calendar Event Update): Execute rescheduling<br>· For each meeting: Update meeting time to new slot<br>· Send: Meeting update notifications to all attendees<br>· Update: User's calendar status to {status} for Thursday afternoon |

**Key Orchestration**: CAN-04 → CAN-01 → CAN-07 → **CAN-05** → [CAN-13 + CAN-06 parallel] → CAN-12 → CAN-23 → CAN-13

**Human Evaluator Insight**:
> "Critical Human Evaluator Insight: Original decomposition missed CAN-05 - human noted 'model needs to get metadata, and from there to find attendee for those meetings'. CAN-05 is ESSENTIAL for CAN-06 availability checking - cannot access attendee calendars without it."

**Critical Dependencies**:
- **CAN-05 MUST precede CAN-06**: Cannot check availability without attendee calendars
- CAN-07 (Metadata) enables both CAN-05 and CAN-13
- CAN-23 generates proposal for human review before execution

---

## 6) Schedule-3 Prompt: "Land a time to meet about Project Alpha with Chris, Sangya, and Kat for 1 hour in the next 2 weeks. Schedule over 1:1s and lunches if needed and work around Kat's schedule. Make the meeting in person and add a room."

**Evaluation**: ✅ **Correct**  
**Total Tasks**: 10

| Steps | Atomic Agent Capabilities (V2.0 Framework) |
| ----- | ------------------------- |
| 1. Parse Complex Requirements | · **CAN-04** (Natural Language Understanding): Extract multi-constraint scheduling request<br>· Parse: Participants (Chris, Sangya, Kat), duration (1 hour), timeframe (next 2 weeks)<br>· Parse: Conflict resolution ("schedule over 1:1s and lunches"), priority ("work around Kat's schedule")<br>· Parse: Location requirement ("in person"), resource need ("add a room") |
| 2. Resolve Participant Identities | · **CAN-05** (Attendee/Contact Resolution): Resolve all participant names to contacts<br>· Resolve: "Chris" → chris.smith@company.com<br>· Resolve: "Sangya" → sangya.jones@company.com<br>· Resolve: "Kat" → kat.wilson@company.com<br>· Extract: Calendar access, timezones, office locations |
| 3. Check Multi-Party Availability | · **CAN-06** (Availability Checking): Check availability for all 4 participants<br>· Time range: Next 2 weeks<br>· Duration: 1 hour blocks<br>· Priority: Kat's availability (hard constraint) |
| 4. Identify Conflict Types | · **CAN-02** (Meeting Type Classification): Classify existing meetings to identify reschedulable types<br>· Identify: 1:1s (reschedulable), lunches (reschedulable), customer meetings (keep), team syncs (keep)<br>· Purpose: Determine which conflicts can be "scheduled over" |
| 5. Solve Complex Constraints | · **CAN-12** (Constraint Satisfaction): Find time slots satisfying all constraints<br>· Hard constraints: Kat's schedule, 1 hour duration, next 2 weeks, in-person (same location)<br>· Soft constraints: Minimize rescheduling, prefer afternoons, avoid Fridays |
| 6. Handle Scheduling Conflicts | · **CAN-23** (Conflict Resolution): Resolve conflicts by rescheduling lower-priority meetings<br>· Logic: Can schedule over 1:1s and lunches (per prompt)<br>· Identify: Which 1:1s/lunches need to be moved for best slot |
| 7. Find Meeting Room | · **CAN-19** (Resource Booking): Book conference room for in-person meeting<br>· Requirements: Room capacity for 4 people, same building/floor, video conferencing capability<br>· Check: Room availability for selected time slot |
| 8. Generate Meeting Proposal | · **CAN-14** (Recommendation Engine): Propose optimal solution with alternatives<br>· Best option: Specific date/time + room + which conflicts to reschedule<br>· Alternatives: 2-3 backup options if primary declined |
| 9. Create Calendar Event | · **CAN-13** (Calendar Event Creation): Create meeting with all details<br>· Title: "Project Alpha Discussion"<br>· Attendees: User, Chris, Sangya, Kat<br>· Duration: 1 hour<br>· Location: Booked room (from CAN-19) |
| 10. Coordinate Multi-Party | · **CAN-24** (Multi-party Coordination/Negotiation): Handle scheduling negotiations if needed<br>· If no perfect slot: Run polling/voting for preferred times<br>· If conflicts persist: Iterative negotiation to find compromise |

**Key Orchestration**: CAN-04 → CAN-05 → CAN-06 → CAN-02 → CAN-12 → CAN-23 → CAN-19 → CAN-14 → CAN-13 → CAN-24

**Critical Insights**:
- Most complex scheduling prompt (10 tasks)
- Priority attendee (Kat) as hard constraint
- Conflict resolution strategy: schedule over specific meeting types
- Resource booking (room) integrated with scheduling

---

## 7) Collaborate-1 Prompt: "Help me set the agenda to review the progress of Project Alpha with the product and marketing team to get confirmation we are on track and discuss any blocking issues or risks."

**Evaluation**: ❓ **Needs Review** - CAN-18 removed (over-interpretation of "risks")  
**Total Tasks**: 7

| Steps | Atomic Agent Capabilities (V2.0 Framework) |
| ----- | ------------------------- |
| 1. Understand Agenda Requirements | · **CAN-04** (Natural Language Understanding): Extract agenda structure requirements<br>· Parse: Meeting purpose ("review progress of Project Alpha")<br>· Parse: Discussion topics ("get confirmation on track", "discuss blocking issues")<br>· Parse: Attendees ("product and marketing team") |
| 2. Find Project Alpha Meetings | · **CAN-01** (Calendar Events Retrieval): Find existing/upcoming Project Alpha meetings<br>· Search: Subject contains "Project Alpha"<br>· Filter: Meetings with product and marketing teams<br>· Identify: Specific meeting to prepare agenda for |
| 3. Retrieve Meeting Materials | · **CAN-08** (Document/Content Retrieval): Retrieve related documents and content<br>· Retrieve: Previous Project Alpha meeting notes, action items<br>· Retrieve: Project plans, status reports, blockers documentation<br>· Retrieve: Teams chat history, emails about Project Alpha |
| 4. Gather Background Intelligence | · **CAN-22** (Research/Intelligence Gathering): Gather project context and background<br>· Research: Current project status, recent updates, key milestones<br>· Research: Known blockers, risks, dependencies<br>· Research: Stakeholder concerns, recent decisions |
| 5. Identify Priority Discussion Topics | · **CAN-11** (Priority/Preference Matching): Identify most important agenda topics<br>· Match: User's stated goals ("confirmation on track", "blocking issues")<br>· Prioritize: Topics by urgency and importance |
| 6. Structure Agenda | · **CAN-23** (Agenda Generation/Structuring): Create structured meeting agenda<br>· Section 1: Progress review (status updates)<br>· Section 2: Confirmation checkpoint ("Are we on track?")<br>· Section 3: Blocking issues discussion<br>· Section 4: Action items and next steps |
| 7. Generate Formatted Agenda | · **CAN-09** (Document Generation/Formatting): Generate formatted agenda document<br>· Format: Numbered sections, time allocations, discussion prompts<br>· Include: Background materials, previous action items, decision points<br>· Output: Professional agenda document for distribution |

**Key Orchestration**: CAN-04 → CAN-01 → CAN-08 → CAN-22 → CAN-11 → CAN-23 → CAN-09

**Human Evaluator Notes**:
> "CAN-18 (Risk Anticipation) removed from decomposition. Original analysis over-interpreted 'discuss any blocking issues or risks' as requiring risk prediction. The prompt asks to DISCUSS risks (agenda topic), not ANTICIPATE/PREDICT future risks. CAN-18 is about predicting objections/concerns, not listing discussion topics."

**Scope Clarification**:
- "Discuss risks" = agenda topic (CAN-23)
- "Anticipate risks" = risk prediction (CAN-18) - NOT required here

---

## 8) Collaborate-2 Prompt: "Review the materials for my meeting with senior leadership and suggest the best way to summarize the topics into three main discussion points. Generate any objections or concerns that might come up and give me effective responses."

**Evaluation**: ⚠️ **Partial** - Missing CAN-05 in original GPT-5 analysis (added by human evaluator)  
**Total Tasks**: 10

| Steps | Atomic Agent Capabilities (V2.0 Framework) |
| ----- | ------------------------- |
| 1. Understand Preparation Requirements | · **CAN-04** (Natural Language Understanding): Extract multi-part preparation request<br>· Parse: "Review materials" = document analysis<br>· Parse: "Summarize into three main points" = content synthesis<br>· Parse: "Generate objections/concerns" = risk anticipation<br>· Parse: "Effective responses" = response preparation |
| 2. Find Senior Leadership Meeting | · **CAN-01** (Calendar Events Retrieval): Find the specific meeting<br>· Search: Upcoming meetings with "senior leadership"<br>· Filter: User's calendar for next 1-2 weeks<br>· Identify: Target meeting for preparation |
| 3. Resolve Senior Leadership | · **CAN-05** (Attendee/Contact Resolution): Identify who qualifies as "senior leadership"<br>· **CRITICAL - MISSING IN ORIGINAL**: Must know WHO senior leadership is!<br>· Resolve: Attendee list to profiles, identify VP+, C-level executives<br>· Human evaluator note: "System needs to know who are in the senior leadership to find relevant meetings and meeting related materials" |
| 4. Extract Meeting Metadata | · **CAN-07** (Meeting Metadata Extraction): Extract meeting context<br>· Extract: Attendees, agenda, organizer, meeting purpose<br>· Extract: Attached documents, previous meeting notes |
| 5. Retrieve All Meeting Materials | · **CAN-08** (Document/Content Retrieval): Retrieve all related content<br>· Retrieve: Meeting attachments (presentations, reports)<br>· Retrieve: Previous senior leadership meeting notes<br>· Retrieve: Email threads, status updates, background documents |
| 6. Gather Intelligence | · **CAN-22** (Research/Intelligence Gathering): Gather background on attendees and topics<br>· Research: Senior leadership profiles, recent focus areas<br>· Research: Company priorities, strategic initiatives<br>· Research: Recent executive communications, concerns |
| 7. Synthesize to Three Points | · **CAN-09** (Document Generation/Formatting): Summarize materials into 3 main discussion points<br>· Analyze: All retrieved materials for key themes<br>· Synthesize: Consolidate into 3 clear, concise discussion points<br>· Format: Executive-level summary (brief, impactful) |
| 8. Anticipate Objections | · **CAN-18** (Objection/Risk Anticipation): Predict potential concerns or pushback<br>· Based on: Senior leadership perspectives, past behavior, strategic priorities<br>· Identify: Likely objections, questions, challenges for each discussion point<br>· Output: List of anticipated objections/concerns |
| 9. Generate Effective Responses | · **CAN-09** (Document Generation): Create response strategies<br>· For each objection: Draft clear, compelling response<br>· Include: Data/evidence, alternative approaches, mitigation strategies<br>· Format: Q&A style preparation document |
| 10. Assess Meeting Importance | · **CAN-03** (Meeting Importance Assessment): Confirm high-stakes nature<br>· Assess: Senior leadership = high importance<br>· Identify: Critical success factors for this meeting |

**Key Orchestration**: CAN-04 → CAN-01 → **CAN-05** → CAN-07 → CAN-08 → CAN-22 → CAN-09 → CAN-18 → CAN-09 → CAN-03

**Human Evaluator Insight**:
> "CRITICAL MISSING DEPENDENCY: CAN-05 MUST precede CAN-01 - cannot find 'meeting with senior leadership' without knowing who senior leadership is. System needs to know who are in the senior leadership to find relevant meetings and meeting related materials."

**Critical Dependencies**:
- **CAN-05 required BEFORE CAN-01**: Must identify senior leadership to find the meeting
- CAN-18 (Risk Anticipation) appropriately used here (vs removed from Collaborate-1)
- Two uses of CAN-09: Topic summary + response generation

---

## 9) Collaborate-3 Prompt: "Prepare a brief for my upcoming meeting with customer Beta and include a dossier for each customer attendee and the topics they are most interested in. Include a background on their company."

**Evaluation**: ✅ **Correct**  
**Total Tasks**: 9

| Steps | Atomic Agent Capabilities (V2.0 Framework) |
| ----- | ------------------------- |
| 1. Understand Brief Requirements | · **CAN-04** (Natural Language Understanding): Extract preparation requirements<br>· Parse: "Prepare a brief" = comprehensive meeting preparation<br>· Parse: "Customer Beta" = specific customer account<br>· Parse: "Dossier for each attendee" = individual profiles<br>· Parse: "Topics they are interested in" = preference research<br>· Parse: "Background on their company" = company research |
| 2. Find Customer Beta Meeting | · **CAN-01** (Calendar Events Retrieval): Find the specific meeting<br>· Search: Upcoming meetings with "Beta" or customer domain<br>· Filter: Customer meetings (external attendees)<br>· Identify: Target meeting for preparation |
| 3. Extract Meeting Details | · **CAN-07** (Meeting Metadata Extraction): Extract meeting context<br>· Extract: Attendees, agenda, organizer, meeting purpose, location<br>· Extract: Attached documents, previous meeting history |
| 4. Resolve Customer Attendees | · **CAN-05** (Attendee/Contact Resolution): Resolve customer attendee identities<br>· Resolve: Each customer attendee to full profile<br>· Extract: Names, titles, roles, contact information<br>· Identify: External domain (customer Beta) vs internal attendees |
| 5. Retrieve Meeting Materials | · **CAN-08** (Document/Content Retrieval): Retrieve all related content<br>· Retrieve: Previous meeting notes with customer Beta<br>· Retrieve: Email threads, presentations, proposals<br>· Retrieve: Customer contracts, SOWs, support tickets |
| 6. Research Customer Company | · **CAN-22** (Research/Intelligence Gathering): Gather comprehensive background<br>· Company research: Customer Beta's business, industry, recent news, financials<br>· Attendee research: LinkedIn profiles, recent publications, interests<br>· Topic research: Customer's stated priorities, pain points, strategic initiatives<br>· Relationship history: Past interactions, purchases, support issues |
| 7. Create Individual Dossiers | · **CAN-09** (Document Generation/Formatting): Generate attendee dossiers<br>· For each customer attendee: Profile (name, title, role, background)<br>· Include: Topics of interest, recent activities, decision-making authority<br>· Format: Professional dossier template |
| 8. Generate Company Background | · **CAN-09** (Document Generation/Formatting): Create company background section<br>· Include: Company overview, industry, size, key facts<br>· Include: Recent news, strategic direction, competitive landscape<br>· Include: Relationship history with your company |
| 9. Compile Meeting Brief | · **CAN-09** (Document Generation/Formatting): Assemble comprehensive brief<br>· Section 1: Meeting overview (date, attendees, purpose)<br>· Section 2: Company background (from step 8)<br>· Section 3: Attendee dossiers (from step 7)<br>· Section 4: Suggested talking points, potential opportunities<br>· Format: Executive briefing document |

**Key Orchestration**: CAN-04 → CAN-01 → CAN-07 → CAN-05 → CAN-08 → CAN-22 → [CAN-09 x3: dossiers, background, brief]

**Critical Insights**:
- Heavy emphasis on CAN-22 (Research/Intelligence) for customer preparation
- CAN-09 used three times for different document generation tasks
- CAN-05 critical for resolving customer attendee identities
- Customer-facing preparation requires comprehensive background gathering

---

## V2.0 Framework Summary

### Task Frequency Across All 9 Prompts

| Task ID | Task Name | Frequency | Prompts |
|---------|-----------|-----------|---------|
| **CAN-04** | Natural Language Understanding | 100% | 9/9 (ALL) |
| **CAN-01** | Calendar Events Retrieval | 100% | 9/9 (ALL) |
| **CAN-07** | Meeting Metadata Extraction | 78% | 7/9 |
| **CAN-05** | Attendee/Contact Resolution | 67% | 6/9 |
| **CAN-02** | Meeting Type Classification | 56% | 5/9 |
| **CAN-03** | Meeting Importance Assessment | 56% | 5/9 |
| **CAN-09** | Document Generation/Formatting | 56% | 5/9 |
| **CAN-12** | Constraint Satisfaction | 44% | 4/9 |
| **CAN-13** | RSVP Status Update / Event Creation | 44% | 4/9 |
| **CAN-11** | Priority/Preference Matching | 44% | 4/9 |
| **CAN-14** | Recommendation Engine | 44% | 4/9 |
| **CAN-06** | Availability Checking | 33% | 3/9 |
| **CAN-08** | Document/Content Retrieval | 33% | 3/9 |
| **CAN-22** | Research/Intelligence Gathering | 33% | 3/9 |
| **CAN-18** | Objection/Risk Anticipation | 22% | 2/9 |
| **CAN-20** | Data Visualization/Reporting | 11% | 1/9 |
| **CAN-23** | Agenda Generation/Conflict Resolution | 22% | 2/9 |
| **CAN-10** | Time Aggregation/Analysis | 11% | 1/9 |
| **CAN-15** | Recurrence Rule Generation | 11% | 1/9 |
| **CAN-16** | Event Monitoring/Change Detection | 11% | 1/9 |
| **CAN-17** | Automatic Rescheduling | 11% | 1/9 |
| **CAN-21** | Focus Time/Preparation Analysis | 11% | 1/9 |
| **CAN-24** | Multi-party Coordination | 11% | 1/9 |
| **CAN-25** | Event Annotation/Flagging (NEW) | 11% | 1/9 |
| **CAN-19** | Resource Booking | 11% | 1/9 |

### Key V2.0 Insights

**Universal Foundation** (100% frequency):
- **CAN-04** (NLU): Every prompt requires natural language understanding
- **CAN-01** (Calendar Retrieval): Every prompt requires calendar data access

**Critical Parent Task**:
- **CAN-07** (Metadata Extraction): Appears in 78% of prompts, enables multiple child tasks

**Often-Missed Critical Task**:
- **CAN-05** (Attendee Resolution): 67% frequency, CRITICAL dependency but frequently missed by LLMs
  - Required for: Schedule-2 (find attendees), Collaborate-2 (identify senior leadership)
  - Human evaluator identified this as missing in original GPT-5 analysis

**NEW in V2.0**:
- **CAN-25** (Event Annotation/Flagging): Added based on human evaluation of Organizer-2
  - Addresses "flag meetings" requirement (conditional event marking)

**Scope Clarifications**:
- **CAN-18** (Risk Anticipation): Appropriate for Collaborate-2 (predict objections), NOT for Collaborate-1 (discuss risks as agenda topic)

### Implementation Priority

**Phase 1 - MVP** (Weeks 1-4):
- ✅ CAN-04, CAN-01 (100% frequency - CRITICAL)
- ✅ CAN-07 (78% frequency - parent task)
- ✅ CAN-05 (67% frequency - often missed but critical)
- ✅ CAN-02, CAN-03 (56% frequency - core classification)

**Phase 2 - Common** (Weeks 5-8):
- ✅ CAN-09, CAN-12, CAN-13, CAN-11, CAN-14 (44-56% frequency)
- ✅ CAN-06, CAN-08, CAN-22 (33% frequency)

**Phase 3 - Specialized** (Weeks 9-12):
- ✅ All remaining tasks including NEW CAN-25

---

**Document End**

*This appendix provides concise multi-step reasoning plans for all 9 v2 hero prompts. For detailed execution composition and example flows, see [CANONICAL_TASKS_GOLD_STANDARD_REFERENCE_V2.md](../CANONICAL_TASKS_GOLD_STANDARD_REFERENCE_V2.md).*
