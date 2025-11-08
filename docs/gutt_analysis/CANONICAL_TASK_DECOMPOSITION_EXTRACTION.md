# Canonical Task Decomposition - All Hero Prompts
## Extracted from Gold Standard Reference V2.1

**Date**: November 8, 2025  
**Source**: `CANONICAL_TASKS_GOLD_STANDARD_REFERENCE_V2.md`  
**Framework**: Calendar.AI V2.0 (25 Canonical Tasks)

---

## Hero Prompt 1: Organizer-1

## Hero Prompt 1: Organizer-1

**Full Prompt**: "Keep my Calendar up to date by committing to only meetings that are part of my priorities. My priorities are customer meetings and product strategy. Show me as 'Busy' for high priority meetings and keep all declined meetings on my calendar."

**Task Count**: 7 tasks

**Canonical Tasks**:
1. **CAN-04**: Natural Language Understanding (Tier 1 - Universal)
   - *Purpose*: Parse user prompts to extract intent, constraints, time ranges, priorities, and actionable requirements
2. **CAN-01**: Calendar Events Retrieval (Tier 1 - Universal)
   - *Purpose*: Retrieve calendar event data from calendar systems via API, with optional filters for time range, attendees, or status
3. **CAN-07**: Meeting Metadata Extraction (Tier 2 - Common)
   - *Purpose*: Extract detailed metadata from calendar events including RSVP status, attendees, agenda, attachments, and meeting links
4. **CAN-02**: Meeting Type Classification (Tier 1 - Universal)
   - *Purpose*: Classify calendar events by meeting format/type based on structural attributes (attendee count, subject keywords, organizer)
5. **CAN-03**: Meeting Importance Assessment (Tier 1 - Universal)
   - *Purpose*: Assess the business importance, urgency, or priority level of meetings based on context, attendees, and user goals
6. **CAN-11**: Priority/Preference Matching (Tier 2 - Common)
   - *Purpose*: Match meetings and time slots against user priorities, preferences, and constraints
7. **CAN-13**: RSVP Status Update (Tier 2 - Common)
   - *Purpose*: Update meeting RSVP status (accept, decline, tentative) in calendar system

---

## Hero Prompt 2: Organizer-2

**Full Prompt**: "Track all my important meetings and flag any that require focus time to prepare for them."

**Task Count**: 9 tasks (including NEW CAN-25)

**Canonical Tasks**:
1. **CAN-04**: Natural Language Understanding (Tier 1 - Universal)
   - *Purpose*: Parse user prompts to extract intent, constraints, time ranges, priorities, and actionable requirements
2. **CAN-01**: Calendar Events Retrieval (Tier 1 - Universal)
   - *Purpose*: Retrieve calendar event data from calendar systems via API, with optional filters for time range, attendees, or status
3. **CAN-07**: Meeting Metadata Extraction (Tier 2 - Common)
   - *Purpose*: Extract detailed metadata from calendar events including RSVP status, attendees, agenda, attachments, and meeting links
4. **CAN-02**: Meeting Type Classification (Tier 1 - Universal)
   - *Purpose*: Classify calendar events by meeting format/type based on structural attributes (attendee count, subject keywords, organizer)
5. **CAN-03**: Meeting Importance Assessment (Tier 1 - Universal)
   - *Purpose*: Assess the business importance, urgency, or priority level of meetings based on context, attendees, and user goals
6. **CAN-21**: Focus Time/Preparation Time Analysis (Tier 3 - Specialized)
   - *Purpose*: Estimate preparation time needed for meetings and identify when focus time blocks should be scheduled
7. **CAN-11**: Priority/Preference Matching (Tier 2 - Common)
   - *Purpose*: Match meetings and time slots against user priorities, preferences, and constraints
8. **CAN-16**: Event Monitoring/Change Detection (Tier 3 - Specialized)
   - *Purpose*: Monitor calendar events for changes (updates, cancellations, new invitations) and trigger notifications or actions
9. **CAN-25**: Event Annotation/Flagging (Tier 3 - Specialized) **[NEW TASK in V2.0]**
   - *Purpose*: Add annotations, flags, or visual indicators to calendar events when predefined conditions are met (e.g., prep time needed, VIP attendee, budget approval required)

---

## Hero Prompt 3: Organizre-3

**Full Prompt**: "Help me understand where I am spending my time and identify ways I can reclaim time for my top priorities."

**Task Count**: 9 tasks

**Canonical Tasks**:
1. **CAN-04**: Natural Language Understanding (Tier 1 - Universal)
   - *Purpose*: Parse user prompts to extract intent, constraints, time ranges, priorities, and actionable requirements
2. **CAN-01**: Calendar Events Retrieval (Tier 1 - Universal)
   - *Purpose*: Retrieve calendar event data from calendar systems via API, with optional filters for time range, attendees, or status
3. **CAN-07**: Meeting Metadata Extraction (Tier 2 - Common)
   - *Purpose*: Extract detailed metadata from calendar events including RSVP status, attendees, agenda, attachments, and meeting links
4. **CAN-02**: Meeting Type Classification (Tier 1 - Universal)
   - *Purpose*: Classify calendar events by meeting format/type based on structural attributes (attendee count, subject keywords, organizer)
5. **CAN-03**: Meeting Importance Assessment (Tier 1 - Universal)
   - *Purpose*: Assess the business importance, urgency, or priority level of meetings based on context, attendees, and user goals
6. **CAN-10**: Time Aggregation/Statistical Analysis (Tier 2 - Common)
   - *Purpose*: Aggregate and analyze time spent across meetings, categories, people, and projects with statistical summaries
7. **CAN-11**: Priority/Preference Matching (Tier 2 - Common)
   - *Purpose*: Match meetings and time slots against user priorities, preferences, and constraints
8. **CAN-14**: Recommendation Engine (Tier 2 - Common)
   - *Purpose*: Generate intelligent recommendations for meetings, time slots, actions, or optimizations based on analysis
9. **CAN-20**: Data Visualization/Reporting (Tier 3 - Specialized)
   - *Purpose*: Create visual representations of meeting data, time analysis, and calendar insights

---

## Hero Prompt 4: Schedule-1

## Hero Prompt 4: Schedule-1

**Full Prompt**: "Starting next week, I want a weekly 30-min 1:1 with {name}. Afternoons preferred, avoid Fridays. Automatically reschedule if {name} declines or conflicts arise."

**Task Count**: 9 tasks

**Canonical Tasks**:
1. **CAN-04**: Natural Language Understanding (Tier 1 - Universal)
   - *Purpose*: Parse user prompts to extract intent, constraints, time ranges, priorities, and actionable requirements
2. **CAN-05**: Attendee/Contact Resolution (Tier 1 - Universal)
   - *Purpose*: Resolve names, email addresses, and contact details to full user profiles with organizational context
3. **CAN-01**: Calendar Events Retrieval (Tier 1 - Universal)
   - *Purpose*: Retrieve calendar event data from calendar systems via API, with optional filters for time range, attendees, or status
4. **CAN-06**: Availability Checking (Tier 2 - Common)
   - *Purpose*: Check free/busy status across calendars to find available time slots for scheduling
5. **CAN-12**: Constraint Satisfaction (Tier 2 - Common)
   - *Purpose*: Find time slots or solutions that satisfy multiple constraints (time, attendees, resources, preferences)
6. **CAN-15**: Recurrence Rule Generation (Tier 3 - Specialized)
   - *Purpose*: Generate recurrence rules (RRULE) for recurring meetings with complex patterns
7. **CAN-03**: Meeting Importance Assessment (Tier 1 - Universal)
   - *Purpose*: Assess the business importance, urgency, or priority level of meetings based on context, attendees, and user goals
8. **CAN-16**: Event Monitoring/Change Detection (Tier 3 - Specialized)
   - *Purpose*: Monitor calendar events for changes (updates, cancellations, new invitations) and trigger notifications or actions
9. **CAN-17**: Automatic Rescheduling (Tier 3 - Specialized)
   - *Purpose*: Automatically reschedule meetings when conflicts or declines occur, finding alternative time slots

---

## Hero Prompt 5: Schedule-2

**Prompt**: "Clear my Thursday afternoon. Update my RSVPs and help me reschedule my meetings to another time and show me as {status}."

**Task Count**: 9 Tasks (Including CAN-05)

**Gold Standard Revision (Nov 8, 2025)**: CAN-23 → CAN-17 (accepting automatic rescheduling task)

### Tasks:
1. **CAN-04** - Natural Language Understanding (Tier 1: Universal)
   - *Purpose*: Parse user prompts to extract intent, constraints, time ranges, priorities, and actionable requirements
2. **CAN-01** - Calendar Events Retrieval (Tier 1: Universal)
   - *Purpose*: Retrieve calendar event data from calendar systems via API, with optional filters for time range, attendees, or status
3. **CAN-07** - Meeting Metadata Extraction (Tier 2: Common)
   - *Purpose*: Extract detailed metadata from calendar events including RSVP status, attendees, agenda, attachments, and meeting links
4. **CAN-05** - Attendee/Contact Resolution (Tier 1: Universal) ⚠️ **MISSING IN ORIGINAL**
   - *Purpose*: Resolve names, email addresses, and contact details to full user profiles with organizational context
5. **CAN-13** - RSVP Status Update (Tier 2: Common)
   - *Purpose*: Update meeting RSVP status (accept, decline, tentative) in calendar system
6. **CAN-06** - Availability Checking (Tier 2: Common)
   - *Purpose*: Check free/busy status across calendars to find available time slots for scheduling
7. **CAN-12** - Constraint Satisfaction (Tier 2: Common)
   - *Purpose*: Find time slots or solutions that satisfy multiple constraints (time, attendees, resources, preferences)
8. **CAN-17** - Automatic Rescheduling (Tier 3: Specialized) ✅ **REVISED**
   - *Purpose*: Automatically reschedule meetings when conflicts or declines occur, finding alternative time slots
9. **CAN-03** - Meeting Importance Assessment (Tier 1: Universal)
   - *Purpose*: Assess the business importance, urgency, or priority level of meetings based on context, attendees, and user goals


**Note**: Human evaluator identified CAN-05 as critical missing task. CAN-17 accepted as appropriate for "help me reschedule" automation request.

---

## Hero Prompt 6: Schedule-3

**Prompt**: "Land a time to meet about Project Alpha with Chris, Sangya, and Kat for 1 hour in the next 2 weeks. Schedule over 1:1s and lunches if needed and work around Kat's schedule. Make the meeting in person and add a room."

**Task Count**: 10 Tasks (Highest complexity)

### Tasks:
1. **CAN-04** - Natural Language Understanding (Tier 1: Universal)
   - *Purpose*: Parse user prompts to extract intent, constraints, time ranges, priorities, and actionable requirements
2. **CAN-05** - Attendee/Contact Resolution (Tier 1: Universal)
   - *Purpose*: Resolve names, email addresses, and contact details to full user profiles with organizational context
3. **CAN-01** - Calendar Events Retrieval (Tier 1: Universal)
   - *Purpose*: Retrieve calendar event data from calendar systems via API, with optional filters for time range, attendees, or status
4. **CAN-07** - Meeting Metadata Extraction (Tier 2: Common)
   - *Purpose*: Extract detailed metadata from calendar events including RSVP status, attendees, agenda, attachments, and meeting links
5. **CAN-02** - Meeting Type Classification (Tier 1: Universal)
   - *Purpose*: Classify calendar events by meeting format/type based on structural attributes (attendee count, subject keywords, organizer)
6. **CAN-03** - Meeting Importance Assessment (Tier 1: Universal)
   - *Purpose*: Assess the business importance, urgency, or priority level of meetings based on context, attendees, and user goals
7. **CAN-06** - Availability Checking (Tier 2: Common)
   - *Purpose*: Check free/busy status across calendars to find available time slots for scheduling
8. **CAN-12** - Constraint Satisfaction (Tier 2: Common)
   - *Purpose*: Find time slots or solutions that satisfy multiple constraints (time, attendees, resources, preferences)
9. **CAN-19** - Resource Booking (Tier 3: Specialized)
   - *Purpose*: Book meeting rooms, equipment, and other physical or virtual resources
10. **CAN-03** - Calendar Event Creation/Update (Tier 1: Universal)
   - *Purpose*: Assess the business importance, urgency, or priority level of meetings based on context, attendees, and user goals

**Note**: Most complex prompt with hard constraints (Kat's schedule) and soft constraints (override 1:1s/lunches).

---

## Hero Prompt 7: Collaborate-1

**Prompt**: "Help me set the agenda to review the progress of Project Alpha with the product and marketing team to get confirmation we are on track and discuss any blocking issues or risks."

**Task Count**: 3 Tasks (Lowest complexity)

**Gold Standard Revision (Nov 8, 2025)**: CAN-09 → CAN-23 (accepting specialized agenda generation)

### Tasks:
1. **CAN-04** - Natural Language Understanding (Tier 1: Universal)
   - *Purpose*: Parse user prompts to extract intent, constraints, time ranges, priorities, and actionable requirements
2. **CAN-05** - Attendee/Contact Resolution (Tier 1: Universal) ⚠️ **MISSING IN ORIGINAL**
   - *Purpose*: Resolve names, email addresses, and contact details to full user profiles with organizational context
3. **CAN-23** - Agenda Generation/Structuring (Tier 3: Specialized) ✅ **REVISED**
   - *Purpose*: Generate structured meeting agendas with topics, time allocations, and discussion goals

**Note**: CAN-23 accepted as appropriate when prompt explicitly says "set the agenda". Meeting goals ("confirm on track", "discuss risks") are INPUT for agenda, not system tasks to execute. CAN-18 should NOT be used (user will discuss risks IN meeting).

---

## Hero Prompt 8: Collaborate-2

**Prompt**: "Review the materials for my meeting with senior leadership and suggest the best way to summarize the topics into three main discussion points. Generate any objections or concerns that might come up and give me effective responses."

**Task Count**: 7 Tasks (Including CAN-05)

### Tasks:
1. **CAN-04** - Natural Language Understanding (Tier 1: Universal)
   - *Purpose*: Parse user prompts to extract intent, constraints, time ranges, priorities, and actionable requirements
2. **CAN-05** - Attendee/Contact Resolution (Tier 1: Universal) ⚠️ **MISSING IN ORIGINAL**
   - *Purpose*: Resolve names, email addresses, and contact details to full user profiles with organizational context
3. **CAN-01** - Calendar Events Retrieval (Tier 1: Universal)
   - *Purpose*: Retrieve calendar event data from calendar systems via API, with optional filters for time range, attendees, or status
4. **CAN-07** - Meeting Metadata Extraction (Tier 2: Common)
   - *Purpose*: Extract detailed metadata from calendar events including RSVP status, attendees, agenda, attachments, and meeting links
5. **CAN-08** - Document/Content Retrieval (Tier 2: Common)
   - *Purpose*: Retrieve meeting-related documents, emails, chat messages, and content from various sources
6. **CAN-09** - Document Generation/Formatting (Tier 2: Common)
   - *Purpose*: Generate formatted documents like agendas, briefs, dossiers, summaries, and meeting materials
7. **CAN-18** - Objection/Risk Anticipation (Tier 3: Specialized)
   - *Purpose*: Anticipate potential objections, concerns, or risks that might arise in meetings and prepare responses

**Note**: CAN-05 critical for resolving "senior leadership" to specific executives. CAN-18 appropriate here because user explicitly requests "Generate any objections or concerns".

---

## Hero Prompt 9: Collaborate-3

**Prompt**: "Prepare a brief for my upcoming meeting with customer Beta and include a dossier for each customer attendee and the topics they are most interested in. Include a background on their company."

**Task Count**: 7 Tasks

### Tasks:
1. **CAN-04** - Natural Language Understanding (Tier 1: Universal)
   - *Purpose*: Parse user prompts to extract intent, constraints, time ranges, priorities, and actionable requirements
2. **CAN-01** - Calendar Events Retrieval (Tier 1: Universal)
   - *Purpose*: Retrieve calendar event data from calendar systems via API, with optional filters for time range, attendees, or status
3. **CAN-07** - Meeting Metadata Extraction (Tier 2: Common)
   - *Purpose*: Extract detailed metadata from calendar events including RSVP status, attendees, agenda, attachments, and meeting links
4. **CAN-05** - Attendee/Contact Resolution (Tier 1: Universal)
   - *Purpose*: Resolve names, email addresses, and contact details to full user profiles with organizational context
5. **CAN-08** - Document/Content Retrieval (Tier 2: Common)
   - *Purpose*: Retrieve meeting-related documents, emails, chat messages, and content from various sources
6. **CAN-09** - Document Generation/Formatting (Tier 2: Common)
   - *Purpose*: Generate formatted documents like agendas, briefs, dossiers, summaries, and meeting materials
7. **CAN-22** - Research/Intelligence Gathering (Tier 3: Specialized)
   - *Purpose*: Research and gather intelligence about meeting participants, companies, topics, and context from external sources

**Note**: CAN-22 is essential for gathering company background on customer Beta. Rich customer intelligence enables personalized meeting preparation.

---

## Summary Statistics

### Task Count Distribution
| Prompt | Task Count | Complexity |
|--------|------------|------------|
| Schedule-3 | 10 tasks | Highest |
| Organizer-2 | 9 tasks | High |
| Organizre-3 | 9 tasks | High |
| Schedule-1 | 9 tasks | High |
| Schedule-2 | 9 tasks | High |
| Collaborate-2 | 7 tasks | Medium |
| Collaborate-3 | 7 tasks | Medium |
| Organizer-1 | 7 tasks | Medium |
| Collaborate-1 | 3 tasks | Lowest |

**Average**: 7.2 tasks per prompt

### Most Frequently Used Tasks

| Rank | Task ID | Task Name | Frequency |
|------|---------|-----------|-----------|
| 1 | CAN-04 | Natural Language Understanding | 9/9 (100%) |
| 1 | CAN-01 | Calendar Events Retrieval | 9/9 (100%) |
| 3 | CAN-07 | Meeting Metadata Extraction | 7/9 (78%) |
| 4 | CAN-05 | Attendee/Contact Resolution | 6/9 (67%) |
| 4 | CAN-03 | Meeting Importance Assessment | 6/9 (67%) |
| 6 | CAN-02 | Meeting Type Classification | 5/9 (56%) |
| 6 | CAN-09 | Document Generation/Formatting | 5/9 (56%) |
| 8 | CAN-12 | Constraint Satisfaction | 4/9 (44%) |
| 8 | CAN-06 | Availability Checking | 4/9 (44%) |
| 8 | CAN-13 | RSVP Status Update | 4/9 (44%) |

### Task Tier Distribution

**Tier 1 (Universal)**: CAN-01, CAN-02, CAN-03, CAN-04, CAN-05
- Used extensively across all prompts
- Average: 4.8 Tier 1 tasks per prompt

**Tier 2 (Common)**: CAN-06, CAN-07, CAN-08, CAN-09, CAN-10, CAN-11, CAN-12, CAN-13, CAN-14
- Used selectively based on prompt requirements
- Average: 2.1 Tier 2 tasks per prompt

**Tier 3 (Specialized)**: CAN-15, CAN-16, CAN-17, CAN-18, CAN-19, CAN-20, CAN-21, CAN-22, CAN-23, CAN-24, CAN-25
- Used for specific capabilities
- Average: 1.3 Tier 3 tasks per prompt

### Critical Patterns Identified

1. **CAN-05 Systematic Under-use**: 
   - Missing in original evaluations: Schedule-2, Collaborate-1, Collaborate-2
   - Critical for attendee resolution in coordination scenarios
   - Human evaluator identified as essential dependency

2. **NEW Task Validated (CAN-25)**:
   - Event Annotation/Flagging
   - First use: Organizer-2 ("flag meetings requiring prep time")
   - Fills gap for visual indicators on calendar

3. **Gold Standard Revisions (Nov 8, 2025)**:
   - **Collaborate-1**: CAN-09 → CAN-23 (specialized agenda generation)
   - **Schedule-2**: CAN-23 → CAN-17 (automatic rescheduling)
   - **Principle**: Accept specialized tasks when prompt explicitly mentions specialization

4. **Task Substitution Patterns**:
   - CAN-09 vs CAN-23: General document vs specialized agenda
   - CAN-17 vs CAN-23: Auto-reschedule vs conflict resolution
   - CAN-06 vs CAN-21: Availability check vs prep time analysis

### Complexity Drivers

**High Complexity Prompts (9-10 tasks)**:
- Multi-attendee coordination (Schedule-3: 3 people)
- Complex constraints (Schedule-3: hard + soft constraints)
- Multiple actions (Schedule-2: RSVP + reschedule + status)
- Time analysis (Organizre-3: historical + recommendations)
- Automation setup (Schedule-1: monitoring + auto-reschedule)

**Low Complexity Prompts (3-7 tasks)**:
- Simple agenda generation (Collaborate-1: 3 tasks)
- Single action focus (Organizer-1: priority-based RSVP)
- Document preparation (Collaborate-2, Collaborate-3)

---

## Usage Notes

This extraction provides a quick reference for:
1. **Task Selection**: Which tasks are needed for similar prompts
2. **Dependency Patterns**: Which tasks depend on others (e.g., CAN-06 needs CAN-05)
3. **Coverage Analysis**: Framework coverage across different scenarios
4. **Complexity Assessment**: Task count as proxy for prompt complexity
5. **Gold Standard Reference**: Authoritative task decompositions for evaluation

**Version**: 2.1 (includes November 8, 2025 gold standard revisions)  
**Framework Coverage**: 22 of 25 tasks used (88%)  
**Unused Tasks**: CAN-24, plus 2 others from specialized tier

---

**Document Status**: COMPLETE  
**Extracted**: November 8, 2025  
**Source File**: `docs/gutt_analysis/CANONICAL_TASKS_GOLD_STANDARD_REFERENCE_V2.md`
