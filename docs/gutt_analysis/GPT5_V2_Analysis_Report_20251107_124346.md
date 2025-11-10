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
   - Parse the user prompt to extract intent: track important meetings and flag those requiring preparation time. Identify constraints such as 'important meetings' and 'focus time requirement'.
2. **CAN-01**: Calendar Events Retrieval
   - Retrieve all upcoming calendar events within a relevant timeframe (e.g., next few weeks) to analyze importance and preparation needs.
3. **CAN-07**: Meeting Metadata Extraction
   - Extract metadata from each event such as attendees, agenda, attachments, and notes to help assess preparation requirements.
4. **CAN-02A**: Meeting Type Classification
   - Classify each meeting by type (e.g., 1:1, team sync, client meeting) to support importance assessment and preparation needs.
5. **CAN-02B**: Meeting Importance Assessment
   - Assess the strategic importance and urgency of each meeting to identify which ones are 'important' as per user intent.
6. **CAN-21**: Task Duration Estimation
   - Estimate preparation time required for each meeting based on complexity, agenda, and attachments to flag those needing focus time.
7. **CAN-11**: Priority/Preference Matching
   - Match identified important meetings and prep requirements against user priorities to finalize which meetings to track and flag.

---

### Organizre-3

**Prompt**: "“Help me understand where I am spending my time .and identify ways I can reclaim time to focus more on my top priorities.”"

**Canonical Tasks**: 9 tasks identified

**Task IDs**: CAN-04, CAN-01, CAN-07, CAN-02A, CAN-02B, CAN-10, CAN-11, CAN-14, CAN-20

**Execution Plan**: 9 steps

**Steps**:
1. **CAN-04**: Natural Language Understanding
   - Parse the user prompt to extract intent (analyze time usage, reclaim time, focus on top priorities) and constraints (timeframe, priorities).
2. **CAN-01**: Calendar Events Retrieval
   - Retrieve all calendar events for the relevant timeframe (e.g., past weeks/month) to analyze time allocation.
3. **CAN-07**: Meeting Metadata Extraction
   - Extract metadata from retrieved events such as attendees, duration, RSVP status, and notes to support deeper analysis.
4. **CAN-02A**: Meeting Type Classification
   - Classify meetings by type (1:1, team sync, customer, etc.) to understand where time is being spent by category.
5. **CAN-02B**: Meeting Importance Assessment
   - Assess the strategic importance and urgency of each meeting to identify low-value meetings that can be reduced or eliminated.
6. **CAN-10**: Time Aggregation/Statistical Analysis
   - Aggregate time spent across different meeting types and importance levels to identify patterns and time sinks.
7. **CAN-11**: Priority/Preference Matching
   - Match current meeting patterns against the user's stated top priorities to highlight misalignments.
8. **CAN-14**: Recommendation Engine
   - Generate personalized recommendations for reclaiming time, such as reducing low-value meetings or delegating.
9. **CAN-20**: Data Visualization/Reporting
   - Create visual dashboards and charts to show time allocation patterns and suggested changes for better focus.

---

### Schedule-1

**Prompt**: "“Starting next week, I want a weekly 30-min 1:1 with {name}. Afternoons preferred, avoid Fridays. Automatically reschedule on declines or conflicts.”"

**Canonical Tasks**: 9 tasks identified

**Task IDs**: CAN-04, CAN-05, CAN-01, CAN-06, CAN-12, CAN-15, CAN-03, CAN-16, CAN-17

**Execution Plan**: 9 steps

**Steps**:
1. **CAN-04**: Natural Language Understanding
   - Parse the user prompt to extract intent (schedule recurring 1:1), constraints (weekly, 30-min, afternoons, avoid Fridays, starting next week), attendee ({name}), and special instructions (auto-reschedule on declines/conflicts).
2. **CAN-05**: Attendee/Contact Resolution
   - Resolve the provided attendee name ({name}) to a directory entry or email address to ensure accurate invitation.
3. **CAN-01**: Calendar Events Retrieval
   - Retrieve the user's calendar events and the attendee's calendar (if accessible) for the upcoming weeks to check availability and avoid conflicts.
4. **CAN-06**: Availability Checking
   - Check free/busy status for both the user and the attendee to find common available afternoon slots, excluding Fridays.
5. **CAN-12**: Constraint Satisfaction
   - Apply constraints (weekly recurrence, 30-min duration, afternoons, avoid Fridays) to select the optimal slot from available options.
6. **CAN-15**: Recurrence Rule Generation
   - Generate an RRULE for a weekly recurring meeting starting next week.
7. **CAN-03**: Calendar Event Creation/Update
   - Create the recurring 1:1 meeting event with the selected slot, attendee, and recurrence rule.
8. **CAN-16**: Event Monitoring/Change Detection
   - Monitor the scheduled event for changes such as declines or conflicts.
9. **CAN-17**: Automatic Rescheduling
   - Automatically reschedule the meeting when declines or conflicts occur, maintaining original constraints.

---

### Schedule-2

**Prompt**: "“Clear my Thursday afternoon. Update my RSVPs and help me reschedule my meetings to another time and show me as {status}.”"

**Canonical Tasks**: 8 tasks identified

**Task IDs**: CAN-04, CAN-01, CAN-07, CAN-13, CAN-06, CAN-12, CAN-23, CAN-03

**Execution Plan**: 8 steps

**Steps**:
1. **CAN-04**: Natural Language Understanding
   - Parse the user prompt to extract intent: clear Thursday afternoon, update RSVPs, reschedule meetings, and set status. Identify constraints such as day (Thursday), time (afternoon), and desired status.
2. **CAN-01**: Calendar Events Retrieval
   - Retrieve all calendar events scheduled for Thursday afternoon to identify which meetings need to be cleared or rescheduled.
3. **CAN-07**: Meeting Metadata Extraction
   - Extract metadata for the retrieved events, including RSVP status, attendees, and logistics, to determine which RSVPs need updating and what details are required for rescheduling.
4. **CAN-13**: RSVP Status Update/Notification
   - Update RSVP statuses for the affected meetings as per user intent (e.g., decline or tentative) and notify attendees if required.
5. **CAN-06**: Availability Checking
   - Check the user's calendar and possibly attendees' calendars to find alternative time slots for rescheduling the cleared meetings.
6. **CAN-12**: Constraint Satisfaction
   - Apply scheduling constraints (attendee availability, user preferences, time windows) to determine optimal new times for the meetings.
7. **CAN-23**: Conflict Resolution
   - Handle any unsatisfiable constraints or conflicts during rescheduling by prioritizing meetings or suggesting trade-offs.
8. **CAN-03**: Calendar Event Creation/Update
   - Update the calendar by removing or moving the original Thursday afternoon meetings to their new time slots and apply the user's desired status (e.g., Out of Office, Busy) for Thursday afternoon.

---

### Schedule-3

**Prompt**: "“Land a time to meet about Project Alpha with Chris, Sangya, and Kat for 1 hour in the next 2 weeks. Schedule over 1:1s and lunches if needed and work around Kat’s schedule. Make the meeting in person and add a room.”"

**Canonical Tasks**: 10 tasks identified

**Task IDs**: CAN-04, CAN-05, CAN-01, CAN-07, CAN-02A, CAN-02B, CAN-06, CAN-12, CAN-19, CAN-03

**Execution Plan**: 10 steps

**Steps**:
1. **CAN-04**: Natural Language Understanding
   - Parse the user prompt to extract intent (schedule a meeting), constraints (1 hour, next 2 weeks, in-person, add room), participants (Chris, Sangya, Kat), priorities (schedule over 1:1s and lunches, work around Kat’s schedule).
2. **CAN-05**: Attendee/Contact Resolution
   - Resolve names Chris, Sangya, and Kat to their directory entries and ensure correct email addresses for scheduling.
3. **CAN-01**: Calendar Events Retrieval
   - Retrieve calendar events for the user and attendees within the next 2 weeks to check availability and identify 1:1s and lunches.
4. **CAN-07**: Meeting Metadata Extraction
   - Extract metadata from retrieved events such as meeting titles, types, and any RSVP or location details to identify which events are 1:1s or lunches.
5. **CAN-02A**: Meeting Type Classification
   - Classify existing meetings (e.g., 1:1s, lunches, team syncs) to determine which can be deprioritized or overridden.
6. **CAN-02B**: Meeting Importance Assessment
   - Assess importance of existing meetings to decide which can be rescheduled or deprioritized in favor of the new Project Alpha meeting.
7. **CAN-06**: Availability Checking
   - Check free/busy status for all attendees over the next 2 weeks, considering Kat’s schedule as a hard constraint.
8. **CAN-12**: Constraint Satisfaction
   - Apply constraints (1-hour duration, in-person, room required, prioritize over 1:1s and lunches, Kat’s schedule) to find optimal time slots.
9. **CAN-19**: Resource/Logistics Booking
   - Book an in-person meeting room for the selected time slot.
10. **CAN-03**: Calendar Event Creation/Update
   - Create the new Project Alpha meeting event with confirmed time, attendees, and room details.

---

### Collaborate-1

**Prompt**: "“Help me set the agenda to review the progress of Project Alpha with the product and marketing team to get confirmation we are on track and discuss any blocking issues or risks.”"

**Canonical Tasks**: 7 tasks identified

**Task IDs**: CAN-04, CAN-05, CAN-01, CAN-07, CAN-08, CAN-18, CAN-09

**Execution Plan**: 7 steps

**Steps**:
1. **CAN-04**: Natural Language Understanding
   - Parse the user prompt to extract intent (create agenda), meeting context (Project Alpha), participants (product and marketing team), objectives (review progress, confirm on track, discuss blockers/risks).
2. **CAN-05**: Attendee/Contact Resolution
   - Resolve 'product team' and 'marketing team' into actual attendee lists by querying directory or team structures.
3. **CAN-01**: Calendar Events Retrieval
   - Retrieve existing calendar events related to Project Alpha or involving the product and marketing teams to check for context or conflicts.
4. **CAN-07**: Meeting Metadata Extraction
   - Extract metadata from relevant events such as attendees, notes, and any attached documents for Project Alpha meetings.
5. **CAN-08**: Document/Content Retrieval
   - Retrieve any pre-reads, progress reports, or attachments from previous Project Alpha meetings to incorporate into the agenda.
6. **CAN-18**: Objection/Risk Anticipation
   - Analyze previous meeting notes and context to anticipate potential blockers or risks for Project Alpha.
7. **CAN-09**: Document Generation/Formatting
   - Generate a structured agenda document including sections for progress review, confirmation of status, and discussion of blockers/risks.

---

### Collaborate-2

**Prompt**: "“Review the materials for my meeting with senior leadership and suggest the best way to summarize the topics into three main discussion points. Generate any objections or concerns that might come up and give me effective responses.”"

**Canonical Tasks**: 6 tasks identified

**Task IDs**: CAN-04, CAN-01, CAN-07, CAN-08, CAN-09, CAN-18

**Execution Plan**: 7 steps

**Steps**:
1. **CAN-04**: Natural Language Understanding
   - Parse the user prompt to extract intent: identify the target meeting (senior leadership), required actions (review materials, summarize into three points, anticipate objections, generate responses). Extract entities like meeting name, attendees, and deliverable requirements.
2. **CAN-01**: Calendar Events Retrieval
   - Retrieve upcoming calendar events to locate the meeting with senior leadership, including its scheduled time and details.
3. **CAN-07**: Meeting Metadata Extraction
   - Extract metadata for the identified senior leadership meeting, including attendees, RSVP status, attachments, notes, and any linked documents.
4. **CAN-08**: Document/Content Retrieval
   - Retrieve all attachments, pre-reads, and shared documents associated with the senior leadership meeting for review.
5. **CAN-09**: Document Generation/Formatting
   - Generate a concise summary of the meeting materials, distilling them into three main discussion points as requested by the user.
6. **CAN-18**: Objection/Risk Anticipation
   - Analyze the meeting context and materials to anticipate potential objections, concerns, or risks that senior leadership might raise.
7. **CAN-09**: Document Generation/Formatting
   - Generate effective responses or counterpoints to each anticipated objection, formatted for easy reference during the meeting.

---

### Collaborate-3

**Prompt**: "“Prepare a brief for my upcoming meeting with customer Beta and include a dossier for each customer attendee and the topics they are most interested in. Include a background on their company.”"

**Canonical Tasks**: 6 tasks identified

**Task IDs**: CAN-04, CAN-01, CAN-07, CAN-05, CAN-08, CAN-09

**Execution Plan**: 6 steps

**Steps**:
1. **CAN-04**: Natural Language Understanding
   - Parse the user prompt to extract intent (prepare meeting brief), identify target meeting (with customer Beta), and required components (dossier for each attendee, topics of interest, company background).
2. **CAN-01**: Calendar Events Retrieval
   - Retrieve upcoming calendar events to locate the meeting with customer Beta.
3. **CAN-07**: Meeting Metadata Extraction
   - Extract metadata for the identified meeting: attendees, RSVP status, any attached documents, and notes.
4. **CAN-05**: Attendee/Contact Resolution
   - Resolve each attendee's identity to directory entries or CRM records to gather additional context.
5. **CAN-08**: Document/Content Retrieval
   - Retrieve any pre-reads, shared documents, or historical meeting notes related to the customer or attendees.
6. **CAN-09**: Document Generation/Formatting
   - Generate the meeting brief including: agenda summary, attendee dossiers (with topics of interest), and company background.

---

