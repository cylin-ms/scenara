# GPT-5 V2 Hero Prompts Analysis Report

**Date**: November 07, 2025  
**Model**: dev-gpt-5-chat-jj  
**Framework**: 24 Canonical Tasks v2.0  
**Prompts Analyzed**: 9

---

## Executive Summary

**Analysis Results**:
- **Total Prompts**: 9
- **Successful**: 9
- **Failed**: 0
- **Success Rate**: 100.0%

**Framework**: 24 Canonical Tasks (23 unique + CAN-02A/CAN-02B split)
- **Tier 1 (Universal)**: 5 tasks - Core foundational capabilities
- **Tier 2 (Common)**: 9 tasks - Frequently used capabilities
- **Tier 3 (Specialized)**: 10 tasks - Advanced/specialized capabilities

---

## Prompt-by-Prompt Analysis

### Organizer-1

**Prompt**: "“Keep my Calendar up to date by committing to only meetings that are part of my priorities.”"

**Canonical Tasks**: 7 tasks identified

**Task IDs**: CAN-04, CAN-01, CAN-07, CAN-02A, CAN-02B, CAN-11, CAN-13

**Execution Plan**: 7 steps

**Steps**:
1. **CAN-04**: Natural Language Understanding
   - Parse the user prompt to extract intent to keep calendar updated, accept only priority meetings, and identify constraints related to priorities and RSVP actions.
2. **CAN-01**: Calendar Events Retrieval
   - Retrieve all current calendar events and pending invitations for the relevant timeframe to evaluate which meetings align with priorities.
3. **CAN-07**: Meeting Metadata Extraction
   - Extract metadata from retrieved events including RSVP status, attendees, and invitation details to identify which meetings require a response.
4. **CAN-02A**: Meeting Type Classification
   - Classify each meeting by type (e.g., 1:1, team sync, customer) to help determine alignment with user priorities.
5. **CAN-02B**: Meeting Importance Assessment
   - Assess the strategic importance and urgency of each meeting to determine if it aligns with the user's stated priorities.
6. **CAN-11**: Priority/Preference Matching
   - Match meetings against the user's stated priorities to identify which invitations should be accepted or declined.
7. **CAN-13**: RSVP Status Update/Notification
   - Update RSVP status for pending invitations based on priority matching results, accepting priority meetings and declining others.

---

### Organizer-2

**Prompt**: "“Track all my important meetings and flag any that require focus time to prepare for them.”"

**Canonical Tasks**: 7 tasks identified

**Task IDs**: CAN-04, CAN-01, CAN-07, CAN-02A, CAN-02B, CAN-21, CAN-11

**Execution Plan**: 7 steps

**Steps**:
1. **CAN-04**: Natural Language Understanding
   - Parse the user prompt to extract intent: track important meetings and flag those requiring focus time for preparation. Identify constraints such as 'important meetings' and 'requires prep time'.
2. **CAN-01**: Calendar Events Retrieval
   - Retrieve all upcoming calendar events within a relevant timeframe (e.g., next few weeks) to analyze which are important and need preparation.
3. **CAN-07**: Meeting Metadata Extraction
   - Extract metadata from each event such as attendees, agenda, attachments, and notes to help assess importance and preparation needs.
4. **CAN-02A**: Meeting Type Classification
   - Classify each meeting by type (e.g., 1:1, team sync, client meeting) to help determine which meetings are likely to be important.
5. **CAN-02B**: Meeting Importance Assessment
   - Assess the strategic importance and urgency of each meeting based on metadata, attendees, and context.
6. **CAN-21**: Task Duration Estimation
   - Estimate preparation time required for each meeting based on complexity, number of attendees, and presence of attachments or agenda.
7. **CAN-11**: Priority/Preference Matching
   - Match identified important meetings and prep requirements against user preferences to finalize which meetings to flag.

---

### Organizre-3

**Prompt**: "“Help me understand where I am spending my time .and identify ways I can reclaim time to focus more on my top priorities.”"

**Canonical Tasks**: 9 tasks identified

**Task IDs**: CAN-04, CAN-01, CAN-07, CAN-02A, CAN-02B, CAN-10, CAN-11, CAN-14, CAN-20

**Execution Plan**: 9 steps

**Steps**:
1. **CAN-04**: Natural Language Understanding
   - Parse the user prompt to extract intent (analyze time usage and reclaim time), constraints (focus on top priorities), and entities (time allocation, priorities).
2. **CAN-01**: Calendar Events Retrieval
   - Retrieve all calendar events for a relevant timeframe (e.g., past 2-4 weeks) to analyze time allocation.
3. **CAN-07**: Meeting Metadata Extraction
   - Extract metadata from retrieved events such as attendees, duration, RSVP status, and notes to support classification and analysis.
4. **CAN-02A**: Meeting Type Classification
   - Classify meetings by type (1:1, team sync, customer, etc.) to understand structural patterns in time usage.
5. **CAN-02B**: Meeting Importance Assessment
   - Assess the strategic importance and urgency of each meeting to identify low-value time sinks.
6. **CAN-10**: Time Aggregation/Statistical Analysis
   - Aggregate time spent across meeting types and importance levels to reveal patterns and quantify time allocation.
7. **CAN-11**: Priority/Preference Matching
   - Match current calendar usage against the user's stated top priorities to identify misalignments.
8. **CAN-14**: Recommendation Engine
   - Generate personalized recommendations for reclaiming time, such as reducing low-value meetings or delegating.
9. **CAN-20**: Data Visualization/Reporting
   - Create visual dashboards and charts to illustrate time distribution and highlight areas for improvement.

---

### Schedule-1

**Prompt**: "“Starting next week, I want a weekly 30-min 1:1 with {name}. Afternoons preferred, avoid Fridays. Automatically reschedule on declines or conflicts.”"

**Canonical Tasks**: 9 tasks identified

**Task IDs**: CAN-04, CAN-05, CAN-01, CAN-06, CAN-12, CAN-15, CAN-03, CAN-16, CAN-17

**Execution Plan**: 9 steps

**Steps**:
1. **CAN-04**: Natural Language Understanding
   - Parse the user prompt to extract intent (schedule recurring 1:1), constraints (weekly, 30-min, afternoons, avoid Fridays, starting next week), attendee name, and requirement for automatic rescheduling.
2. **CAN-05**: Attendee/Contact Resolution
   - Resolve the provided attendee name to a directory entry or email address to ensure accurate scheduling.
3. **CAN-01**: Calendar Events Retrieval
   - Retrieve both user's and attendee's calendar events for the relevant timeframe (starting next week onward) to check availability and avoid conflicts.
4. **CAN-06**: Availability Checking
   - Check free/busy status for both parties to identify common available slots in afternoons, excluding Fridays.
5. **CAN-12**: Constraint Satisfaction
   - Apply constraints (weekly recurrence, 30-min duration, afternoons, avoid Fridays) to select the optimal slot from available options.
6. **CAN-15**: Recurrence Rule Generation
   - Generate an RRULE for a weekly recurring meeting starting next week.
7. **CAN-03**: Calendar Event Creation/Update
   - Create the recurring 1:1 meeting event with the selected slot, attendee, and recurrence rule.
8. **CAN-16**: Event Monitoring/Change Detection
   - Monitor the scheduled event for changes such as declines or conflicts.
9. **CAN-17**: Automatic Rescheduling
   - Automatically reschedule the meeting if a decline or conflict is detected, reapplying constraints and preferences.

---

### Schedule-2

**Prompt**: "“Clear my Thursday afternoon. Update my RSVPs and help me reschedule my meetings to another time and show me as {status}.”"

**Canonical Tasks**: 8 tasks identified

**Task IDs**: CAN-04, CAN-01, CAN-07, CAN-13, CAN-06, CAN-12, CAN-23, CAN-03

**Execution Plan**: 8 steps

**Steps**:
1. **CAN-04**: Natural Language Understanding
   - Parse the user prompt to extract intent: clear Thursday afternoon, update RSVPs, reschedule meetings, and set status. Identify constraints such as timeframe (Thursday afternoon) and desired status.
2. **CAN-01**: Calendar Events Retrieval
   - Retrieve all calendar events scheduled for Thursday afternoon to identify which meetings need to be cleared and rescheduled.
3. **CAN-07**: Meeting Metadata Extraction
   - Extract metadata from retrieved events, including RSVP status, attendees, and logistics, to enable RSVP updates and rescheduling.
4. **CAN-13**: RSVP Status Update/Notification
   - Update RSVP statuses for affected meetings as per user intent (accept/decline or tentative) and notify attendees if necessary.
5. **CAN-06**: Availability Checking
   - Check availability for the user and attendees to find alternative time slots for rescheduling the cleared meetings.
6. **CAN-12**: Constraint Satisfaction
   - Apply scheduling constraints to determine optimal new times for the meetings, considering user availability and preferences.
7. **CAN-23**: Conflict Resolution
   - Handle any unsatisfiable constraints or conflicts during rescheduling by performing trade-off analysis and escalation if needed.
8. **CAN-03**: Calendar Event Creation/Update
   - Update the calendar by removing or moving original meetings and creating new events at the rescheduled times. Also update the user's status for Thursday afternoon as requested.

---

### Schedule-3

**Prompt**: "“Land a time to meet about Project Alpha with Chris, Sangya, and Kat for 1 hour in the next 2 weeks. Schedule over 1:1s and lunches if needed and work around Kat’s schedule. Make the meeting in person and add a room.”"

**Canonical Tasks**: 10 tasks identified

**Task IDs**: CAN-04, CAN-05, CAN-01, CAN-07, CAN-02A, CAN-02B, CAN-06, CAN-12, CAN-19, CAN-03

**Execution Plan**: 10 steps

**Steps**:
1. **CAN-04**: Natural Language Understanding
   - Parse the user prompt to extract intent (schedule a meeting), constraints (1 hour, next 2 weeks, attendees: Chris, Sangya, Kat, prioritize over 1:1s and lunches, in-person, add room, work around Kat's schedule).
2. **CAN-05**: Attendee/Contact Resolution
   - Resolve attendee names (Chris, Sangya, Kat) to directory entries and ensure correct email addresses for scheduling.
3. **CAN-01**: Calendar Events Retrieval
   - Retrieve calendar events for the next 2 weeks for the user and attendees to check availability and identify 1:1s and lunches.
4. **CAN-07**: Meeting Metadata Extraction
   - Extract metadata from retrieved events such as meeting type, RSVP status, and notes to identify which events are 1:1s or lunches.
5. **CAN-02A**: Meeting Type Classification
   - Classify existing meetings (from metadata) into types like 1:1, lunch, team sync to prioritize which can be overridden.
6. **CAN-02B**: Meeting Importance Assessment
   - Assess importance of existing meetings to determine which can be deprioritized (e.g., 1:1s and lunches) to schedule the new meeting.
7. **CAN-06**: Availability Checking
   - Check free/busy status across all attendees for the next 2 weeks, considering constraints and Kat's schedule.
8. **CAN-12**: Constraint Satisfaction
   - Apply constraints (1 hour duration, in-person, prioritize over 1:1s and lunches, work around Kat's schedule) to select the optimal time slot.
9. **CAN-19**: Resource/Logistics Booking
   - Book a physical meeting room for the in-person meeting as requested.
10. **CAN-03**: Calendar Event Creation/Update
   - Create the new meeting event with title 'Project Alpha', add attendees, set duration to 1 hour, include room details, and finalize scheduling.

---

### Collaborate-1

**Prompt**: "“Help me set the agenda to review the progress of Project Alpha with the product and marketing team to get confirmation we are on track and discuss any blocking issues or risks.”"

**Canonical Tasks**: 4 tasks identified

**Task IDs**: CAN-04, CAN-05, CAN-18, CAN-09

**Execution Plan**: 4 steps

**Steps**:
1. **CAN-04**: Natural Language Understanding
   - Parse the user prompt to extract intent (create agenda), meeting context (Project Alpha), participants (product and marketing team), objectives (review progress, confirm on track, discuss blockers and risks).
2. **CAN-05**: Attendee/Contact Resolution
   - Resolve 'product team' and 'marketing team' to actual attendee email addresses or directory entries.
3. **CAN-18**: Objection/Risk Anticipation
   - Analyze historical meetings and project data to anticipate potential risks or blockers related to Project Alpha for inclusion in the agenda.
4. **CAN-09**: Document Generation/Formatting
   - Generate a structured meeting agenda including sections for progress review, confirmation of being on track, and discussion of blockers/risks.

---

### Collaborate-2

**Prompt**: "“Review the materials for my meeting with senior leadership and suggest the best way to summarize the topics into three main discussion points. Generate any objections or concerns that might come up and give me effective responses.”"

**Canonical Tasks**: 6 tasks identified

**Task IDs**: CAN-04, CAN-01, CAN-07, CAN-08, CAN-09, CAN-18

**Execution Plan**: 6 steps

**Steps**:
1. **CAN-04**: Natural Language Understanding
   - Parse the user prompt to extract intent: identify meeting reference (senior leadership), need to review materials, summarize into three discussion points, and anticipate objections with responses.
2. **CAN-01**: Calendar Events Retrieval
   - Retrieve upcoming calendar events to locate the meeting with senior leadership and its associated details.
3. **CAN-07**: Meeting Metadata Extraction
   - Extract metadata for the identified senior leadership meeting, including attendees, attachments, notes, and any linked documents.
4. **CAN-08**: Document/Content Retrieval
   - Retrieve all attachments, pre-reads, and shared documents associated with the senior leadership meeting.
5. **CAN-09**: Document Generation/Formatting
   - Analyze retrieved documents and generate a concise summary with three main discussion points for the meeting.
6. **CAN-18**: Objection/Risk Anticipation
   - Analyze meeting context and historical patterns to anticipate potential objections or concerns from senior leadership and generate effective responses.

---

### Collaborate-3

**Prompt**: "“Prepare a brief for my upcoming meeting with customer Beta and include a dossier for each customer attendee and the topics they are most interested in. Include a background on their company.”"

**Canonical Tasks**: 7 tasks identified

**Task IDs**: CAN-04, CAN-01, CAN-07, CAN-05, CAN-08, CAN-09, CAN-22

**Execution Plan**: 7 steps

**Steps**:
1. **CAN-04**: Natural Language Understanding
   - Parse the user prompt to extract intent (prepare meeting brief), identify target meeting (with customer Beta), and required outputs (dossier for each attendee, topics of interest, company background).
2. **CAN-01**: Calendar Events Retrieval
   - Retrieve upcoming calendar events to locate the meeting with customer Beta.
3. **CAN-07**: Meeting Metadata Extraction
   - Extract metadata for the identified meeting, including attendee list, RSVP status, and any attached documents or notes.
4. **CAN-05**: Attendee/Contact Resolution
   - Resolve each attendee to their full contact profile, including roles and organizational details, to prepare dossiers.
5. **CAN-08**: Document/Content Retrieval
   - Retrieve any pre-reads, shared documents, or historical meeting notes relevant to the customer Beta meeting.
6. **CAN-09**: Document Generation/Formatting
   - Generate a structured meeting brief including: meeting overview, attendee dossiers (with topics of interest), and company background for Beta.
7. **CAN-22**: Work Attribution Discovery
   - Analyze historical collaboration patterns and documents to infer topics each attendee is most interested in.

---

