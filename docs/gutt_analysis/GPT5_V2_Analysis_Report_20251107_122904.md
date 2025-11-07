# GPT-5 V2 Hero Prompts Analysis Report

**Date**: November 07, 2025  
**Model**: dev-gpt-5-chat-jj  
**Framework**: 24 Canonical Tasks v2.0  
**Prompts Analyzed**: 8

---

## Executive Summary

**Analysis Results**:
- **Total Prompts**: 8
- **Successful**: 8
- **Failed**: 0
- **Success Rate**: 100.0%

**Framework**: 24 Canonical Tasks (23 unique + CAN-02A/CAN-02B split)
- **Tier 1 (Universal)**: 5 tasks - Core foundational capabilities
- **Tier 2 (Common)**: 9 tasks - Frequently used capabilities
- **Tier 3 (Specialized)**: 10 tasks - Advanced/specialized capabilities

---

## Prompt-by-Prompt Analysis

### Organizer-2

**Prompt**: "“Track all my important meetings and flag any that require focus time to prepare for them.”"

**Canonical Tasks**: 7 tasks identified

**Task IDs**: CAN-04, CAN-01, CAN-07, CAN-02A, CAN-02B, CAN-21, CAN-11

**Execution Plan**: 7 steps

**Steps**:
1. **CAN-04**: Natural Language Understanding
   - Parse the user prompt to extract intent: track important meetings and flag those requiring focus time for preparation. Identify constraints such as importance criteria and preparation needs.
2. **CAN-01**: Calendar Events Retrieval
   - Retrieve all upcoming calendar events within a relevant timeframe (e.g., next 2-4 weeks) to analyze importance and preparation requirements.
3. **CAN-07**: Meeting Metadata Extraction
   - Extract metadata from each event such as attendees, RSVP status, agenda, attachments, and notes to help assess importance and preparation needs.
4. **CAN-02A**: Meeting Type Classification
   - Classify meetings by type (e.g., 1:1, team sync, client call) to help determine which meetings are likely to be important and require preparation.
5. **CAN-02B**: Meeting Importance Assessment
   - Assess the strategic importance and urgency of each meeting using metadata, attendees, and context to identify which meetings are 'important'.
6. **CAN-21**: Task Duration Estimation
   - Estimate preparation time required for each important meeting based on complexity, number of attendees, and presence of attachments or agenda.
7. **CAN-11**: Priority/Preference Matching
   - Match identified important meetings and their preparation needs against user preferences and priorities to finalize which should be flagged.

---

### Organizre-3

**Prompt**: "“Help me understand where I am spending my time .and identify ways I can reclaim time to focus more on my top priorities.”"

**Canonical Tasks**: 8 tasks identified

**Task IDs**: CAN-04, CAN-01, CAN-07, CAN-02A, CAN-02B, CAN-10, CAN-20, CAN-14

**Execution Plan**: 8 steps

**Steps**:
1. **CAN-04**: Natural Language Understanding
   - Parse the user prompt to extract intent: analyze time allocation and suggest ways to reclaim time for top priorities. Identify constraints such as focus on priorities and optimization goals.
2. **CAN-01**: Calendar Events Retrieval
   - Retrieve all calendar events for a relevant timeframe (e.g., past few weeks or month) to analyze time distribution.
3. **CAN-07**: Meeting Metadata Extraction
   - Extract metadata from retrieved events such as attendees, RSVP status, duration, and meeting notes to support classification and importance assessment.
4. **CAN-02A**: Meeting Type Classification
   - Classify meetings by format (1:1, team sync, customer call, etc.) to understand structural patterns in time allocation.
5. **CAN-02B**: Meeting Importance Assessment
   - Assess the strategic importance and urgency of each meeting to determine which are aligned with top priorities and which are candidates for reduction or elimination.
6. **CAN-10**: Time Aggregation/Statistical Analysis
   - Aggregate time spent across different meeting types and importance levels to quantify where time is being allocated.
7. **CAN-20**: Data Visualization/Reporting
   - Generate visualizations (charts, graphs) to show patterns of time usage and highlight areas for optimization.
8. **CAN-14**: Recommendation Engine
   - Generate personalized recommendations on how to reclaim time, such as reducing low-importance meetings or consolidating similar sessions.

---

### Schedule-1

**Prompt**: "“Starting next week, I want a weekly 30-min 1:1 with {name}. Afternoons preferred, avoid Fridays. Automatically reschedule on declines or conflicts.”"

**Canonical Tasks**: 8 tasks identified

**Task IDs**: CAN-04, CAN-05, CAN-01, CAN-06, CAN-12, CAN-15, CAN-03, CAN-17

**Execution Plan**: 8 steps

**Steps**:
1. **CAN-04**: Natural Language Understanding
   - Parse user prompt to extract intent (schedule recurring 1:1), constraints (weekly, 30-min, afternoons, avoid Fridays, start next week), attendee ({name}), and auto-reschedule requirement.
2. **CAN-05**: Attendee/Contact Resolution
   - Resolve {name} to a specific contact in the directory, handle any ambiguity.
3. **CAN-01**: Calendar Events Retrieval
   - Retrieve both user's and attendee's calendar events for the relevant timeframe (starting next week onward) to check availability and conflicts.
4. **CAN-06**: Availability Checking
   - Check free/busy status for both parties, considering constraints (afternoons, avoid Fridays) to find suitable slots.
5. **CAN-12**: Constraint Satisfaction
   - Apply optimization to select the best slot that satisfies all constraints (weekly recurrence, 30-min duration, afternoons, avoid Fridays).
6. **CAN-15**: Recurrence Rule Generation
   - Generate RRULE for weekly recurring meeting starting next week.
7. **CAN-03**: Calendar Event Creation/Update
   - Create the recurring 1:1 meeting event with resolved attendee, selected slot, and recurrence rule.
8. **CAN-17**: Automatic Rescheduling
   - Set up workflow to automatically reschedule the meeting if declines or conflicts occur in the future.

---

### Schedule-2

**Prompt**: "“Clear my Thursday afternoon. Update my RSVPs and help me reschedule my meetings to another time and show me as {status}.”"

**Canonical Tasks**: 8 tasks identified

**Task IDs**: CAN-04, CAN-01, CAN-07, CAN-13, CAN-06, CAN-12, CAN-23, CAN-03

**Execution Plan**: 8 steps

**Steps**:
1. **CAN-04**: Natural Language Understanding
   - Parse the user prompt to extract intent: clear Thursday afternoon, update RSVPs, reschedule meetings, and set status. Identify constraints such as timeframe (Thursday afternoon) and desired status.
2. **CAN-01**: Calendar Events Retrieval
   - Retrieve all calendar events scheduled for Thursday afternoon to identify which meetings need to be cleared or rescheduled.
3. **CAN-07**: Meeting Metadata Extraction
   - Extract metadata for the retrieved events, including RSVP status, attendees, and logistics, to support RSVP updates and rescheduling.
4. **CAN-13**: RSVP Status Update/Notification
   - Update RSVP statuses for meetings being cleared or rescheduled as per user intent.
5. **CAN-06**: Availability Checking
   - Check availability for the user and attendees to find alternative time slots for rescheduling the cleared meetings.
6. **CAN-12**: Constraint Satisfaction
   - Apply scheduling constraints to identify optimal new times for the meetings, considering user availability and preferences.
7. **CAN-23**: Conflict Resolution
   - Handle any conflicts or unsatisfiable constraints during rescheduling by applying trade-offs or escalation logic.
8. **CAN-03**: Calendar Event Creation/Update
   - Update the calendar by removing or moving meetings from Thursday afternoon to the newly selected time slots and set the user's status as requested.

---

### Schedule-3

**Prompt**: "“Land a time to meet about Project Alpha with Chris, Sangya, and Kat for 1 hour in the next 2 weeks. Schedule over 1:1s and lunches if needed and work around Kat’s schedule. Make the meeting in person and add a room.”"

**Canonical Tasks**: 10 tasks identified

**Task IDs**: CAN-04, CAN-05, CAN-01, CAN-07, CAN-02A, CAN-02B, CAN-06, CAN-12, CAN-19, CAN-03

**Execution Plan**: 10 steps

**Steps**:
1. **CAN-04**: Natural Language Understanding
   - Parse the user prompt to extract intent (schedule a meeting), constraints (1 hour, next 2 weeks, in-person, add room), attendees (Chris, Sangya, Kat), priorities (schedule over 1:1s and lunches, work around Kat’s schedule).
2. **CAN-05**: Attendee/Contact Resolution
   - Resolve attendee names (Chris, Sangya, Kat) to their calendar identities and ensure correct email addresses or directory entries.
3. **CAN-01**: Calendar Events Retrieval
   - Retrieve the user's calendar events and attendees’ calendars for the next 2 weeks to check availability and conflicts.
4. **CAN-07**: Meeting Metadata Extraction
   - Extract metadata from retrieved events such as meeting types, attendees, and whether they are 1:1s or lunches to prioritize scheduling over them if needed.
5. **CAN-02A**: Meeting Type Classification
   - Classify existing meetings (e.g., 1:1s, lunches, team meetings) to identify which can be deprioritized or overridden.
6. **CAN-02B**: Meeting Importance Assessment
   - Assess the importance of existing meetings to determine which can be rescheduled or deprioritized in favor of the new meeting.
7. **CAN-06**: Availability Checking
   - Check free/busy status for all attendees across the next 2 weeks and identify potential time slots for the new meeting.
8. **CAN-12**: Constraint Satisfaction
   - Apply constraints (1-hour duration, in-person, add room, prioritize over 1:1s and lunches, work around Kat’s schedule) to select the optimal time slot.
9. **CAN-19**: Resource/Logistics Booking
   - Book an appropriate meeting room for the in-person meeting.
10. **CAN-03**: Calendar Event Creation/Update
   - Create the new calendar event for Project Alpha with the selected time slot, attendees, and booked room.

---

### Collaborate-1

**Prompt**: "“Help me set the agenda to review the progress of Project Alpha with the product and marketing team to get confirmation we are on track and discuss any blocking issues or risks.”"

**Canonical Tasks**: 7 tasks identified

**Task IDs**: CAN-04, CAN-05, CAN-01, CAN-07, CAN-09, CAN-18, CAN-03

**Execution Plan**: 7 steps

**Steps**:
1. **CAN-04**: Natural Language Understanding
   - Parse the user prompt to extract intent (create agenda), meeting context (Project Alpha), participants (product and marketing team), objectives (review progress, confirm on track, discuss blockers/risks).
2. **CAN-05**: Attendee/Contact Resolution
   - Resolve 'product team' and 'marketing team' into actual attendee lists by querying directory or team definitions.
3. **CAN-01**: Calendar Events Retrieval
   - Retrieve any existing scheduled meetings related to Project Alpha with these teams to determine if agenda applies to an existing meeting or a new one.
4. **CAN-07**: Meeting Metadata Extraction
   - Extract metadata from the identified meeting(s): attendees, RSVP status, notes, attachments, and any existing agenda items.
5. **CAN-09**: Document Generation/Formatting
   - Generate a structured agenda document including sections: progress review, confirmation of being on track, discussion of blocking issues and risks.
6. **CAN-18**: Objection/Risk Anticipation
   - Analyze previous meetings and project notes to anticipate potential objections, risks, or blockers to include in the agenda discussion points.
7. **CAN-03**: Calendar Event Creation/Update
   - Attach the generated agenda to the identified meeting or create a new meeting if none exists, ensuring attendees and objectives are included.

---

### Collaborate-2

**Prompt**: "“Review the materials for my meeting with senior leadership and suggest the best way to summarize the topics into three main discussion points. Generate any objections or concerns that might come up and give me effective responses.”"

**Canonical Tasks**: 6 tasks identified

**Task IDs**: CAN-04, CAN-01, CAN-07, CAN-08, CAN-09, CAN-18

**Execution Plan**: 6 steps

**Steps**:
1. **CAN-04**: Natural Language Understanding
   - Parse the user prompt to extract intent: identify the target meeting (senior leadership), required actions (review materials, summarize into three points, anticipate objections, generate responses).
2. **CAN-01**: Calendar Events Retrieval
   - Retrieve upcoming calendar events to locate the meeting with senior leadership.
3. **CAN-07**: Meeting Metadata Extraction
   - Extract metadata for the identified meeting: attendees, attachments, notes, and any linked documents.
4. **CAN-08**: Document/Content Retrieval
   - Retrieve all attachments and pre-read materials associated with the senior leadership meeting.
5. **CAN-09**: Document Generation/Formatting
   - Analyze retrieved materials and generate a concise summary with three main discussion points.
6. **CAN-18**: Objection/Risk Anticipation
   - Analyze meeting context and materials to anticipate potential objections or concerns from senior leadership and generate effective responses.

---

### Collaborate-3

**Prompt**: "“Prepare a brief for my upcoming meeting with customer Beta and include a dossier for each customer attendee and the topics they are most interested in. Include a background on their company.”"

**Canonical Tasks**: 6 tasks identified

**Task IDs**: CAN-04, CAN-01, CAN-07, CAN-05, CAN-08, CAN-09

**Execution Plan**: 6 steps

**Steps**:
1. **CAN-04**: Natural Language Understanding
   - Parse the user prompt to extract intent (prepare meeting brief), identify target meeting (with customer Beta), and required outputs (dossier for each attendee, topics of interest, company background).
2. **CAN-01**: Calendar Events Retrieval
   - Retrieve upcoming calendar events to locate the meeting with customer Beta.
3. **CAN-07**: Meeting Metadata Extraction
   - Extract metadata for the identified meeting, including attendees, RSVP status, and any attached documents.
4. **CAN-05**: Attendee/Contact Resolution
   - Resolve attendee names to directory entries and enrich with contact details for dossier creation.
5. **CAN-08**: Document/Content Retrieval
   - Retrieve any pre-reads or shared documents attached to the meeting that may inform the brief.
6. **CAN-09**: Document Generation/Formatting
   - Generate a structured meeting brief including: meeting overview, attendee dossiers, topics of interest, and company background.

---

