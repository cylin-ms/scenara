# GPT-5 Canonical Unit Tasks Analysis Report

**Author**: Chin-Yew Lin  
**Date**: 2025-11-06T23:02:35.360344  
**Analyzer**: GPT-5 with Canonical Unit Tasks Library  
**Library Version**: 1.0

---

## Executive Summary

**Total Prompts Analyzed**: 9  
**Total Canonical Tasks Used**: 57  
**Average Tasks per Prompt**: 6.33  
**Overall Coverage**: 85.96%

**Implementation Effort Distribution**:
- Low: 4 prompts
- Medium: 5 prompts
- High: 0 prompts

---

## Per-Prompt Analysis

### organizer-1

**Prompt**: "Show me my pending invitations and which ones I should prioritize based on my priorities for this week: customer meetings and product strategy."

**Implementation Effort**: Low  
**Coverage**: 100.0%

**Canonical Tasks Required**:

✅ **CAN-01: Calendar Events Retrieval** (Tier 1)
   - Why needed: To retrieve all pending invitations from the user's calendar.
   - How used: Fetch events with status 'pending' or 'tentative' for the current week.

✅ **CAN-04: Natural Language Understanding (Constraint/Intent Extraction)** (Tier 1)
   - Why needed: To extract user priorities from the natural language input.
   - How used: Parse 'customer meetings and product strategy' as key priorities for ranking.

✅ **CAN-02: Meeting Classification/Categorization** (Tier 1)
   - Why needed: To classify meetings by type and relevance to priorities.
   - How used: Determine if each pending invitation is a customer meeting or related to product strategy.

✅ **CAN-11: Priority/Preference Matching** (Tier 2)
   - Why needed: To score and rank meetings based on alignment with user priorities.
   - How used: Compute semantic similarity between meeting details and extracted priorities.

**Execution Sequence**:

1. Step 1: Use CAN-04 to extract user priorities from input text.
2. Step 2: Use CAN-01 to retrieve pending invitations for the current week.
3. Step 3: Apply CAN-02 to classify each meeting by type and relevance.
4. Step 4: Use CAN-11 to compute alignment scores and rank meetings.
5. Step 5: Return a prioritized list of pending invitations to the user.

**Recommendations**:

- Implement a ranking algorithm that combines classification and semantic similarity scores.
- Provide a clear UI or response format to display pending invitations sorted by priority alignment.

---

### organizer-2

**Prompt**: "I have some important meetings this week—flag the ones I need to prep for, and put time on my calendar to prepare."

**Implementation Effort**: Low  
**Coverage**: 100.0%

**Canonical Tasks Required**:

✅ **CAN-01: Calendar Events Retrieval** (Tier 1)
   - Why needed: To retrieve all meetings scheduled for this week so they can be analyzed for importance and preparation needs.
   - How used: Fetch the user's calendar events for the current week.

✅ **CAN-02: Meeting Classification** (Tier 1)
   - Why needed: To determine which meetings are important and require preparation.
   - How used: Classify meetings by importance level based on attendees, subject, and context.

✅ **CAN-03: Calendar Event Creation/Update** (Tier 1)
   - Why needed: To add preparation time blocks to the user's calendar.
   - How used: Create new calendar events for preparation before important meetings.

✅ **CAN-04: Natural Language Understanding** (Tier 1)
   - Why needed: To interpret the user's intent to flag important meetings and schedule prep time.
   - How used: Extract intent and constraints from the prompt such as 'flag important meetings' and 'put time on calendar to prepare'.

✅ **CAN-14: Recommendation Engine** (Tier 2)
   - Why needed: To suggest optimal preparation times based on meeting schedule and availability.
   - How used: Recommend suitable time slots for preparation before each important meeting.

**Execution Sequence**:

1. Step 1: Use CAN-04 to parse user intent and extract constraints.
2. Step 2: Use CAN-01 to retrieve all meetings for the current week.
3. Step 3: Apply CAN-02 to classify meetings by importance.
4. Step 4: Use CAN-14 to recommend preparation time slots.
5. Step 5: Use CAN-03 to create calendar events for preparation.

**Recommendations**:

- Leverage classification models to identify important meetings accurately.
- Use recommendation logic to schedule prep time close to the meeting while avoiding conflicts.

---

### organizer-3

**Prompt**: "I'm spending too much time in meetings. Help me find patterns in my calendar and identify opportunities to reclaim time."

**Implementation Effort**: Medium  
**Coverage**: 83.3%

**Canonical Tasks Required**:

✅ **CAN-01: Calendar Events Retrieval** (Tier 1)
   - Why needed: To analyze meeting patterns, we need access to historical calendar events including details like duration, attendees, and categories.
   - How used: Retrieve all past and upcoming meetings within a relevant time range to identify patterns and time allocation.

✅ **CAN-02: Meeting Classification** (Tier 1)
   - Why needed: To find patterns, meetings must be categorized by type (e.g., 1:1, team sync, customer calls) and importance.
   - How used: Classify each meeting into predefined categories to identify which types consume the most time.

✅ **CAN-10: Time Aggregation/Statistical Analysis** (Tier 2)
   - Why needed: To quantify time spent in different meeting categories and detect patterns.
   - How used: Aggregate total hours by meeting type, compute averages, and identify high-frequency or long-duration meeting types.

✅ **CAN-11: Priority/Preference Matching** (Tier 2)
   - Why needed: To determine which meetings align with user priorities and which can be deprioritized.
   - How used: Compare meeting topics against user-stated priorities to identify low-value meetings for potential removal.

✅ **CAN-14: Recommendation Engine** (Tier 2)
   - Why needed: To provide actionable suggestions for reclaiming time based on analysis.
   - How used: Generate recommendations such as canceling low-value meetings, shortening durations, or consolidating recurring sessions.

⚠️ **CAN-20: Data Visualization/Reporting** (Tier 3)
   - Why needed: To present patterns and insights in an easily understandable visual format.
   - How used: Create charts or summaries showing time distribution across meeting types and trends over time.

**Execution Sequence**:

1. Step 1: Retrieve calendar events (CAN-01)
2. Step 2: Classify meetings by type and importance (CAN-02)
3. Step 3: Aggregate time and compute statistics (CAN-10)
4. Step 4: Match meetings against user priorities (CAN-11)
5. Step 5: Generate actionable recommendations (CAN-14)
6. Step 6: Visualize patterns and insights (CAN-20)

**Recommendations**:

- Implement CAN-20 (Data Visualization) to enhance user understanding of meeting patterns.
- Leverage existing classification and analytics to provide clear, actionable recommendations for time reclamation.

---

### schedule-1

**Prompt**: "Land a weekly 30min 1:1 with Sarah for me, afternoons preferred, avoid Fridays. If her schedule changes, automatically find a new time."

**Implementation Effort**: Medium  
**Coverage**: 66.7%

**Canonical Tasks Required**:

✅ **CAN-04: Natural Language Understanding (Constraint/Intent Extraction)** (Tier 1)
   - Why needed: To extract structured constraints such as recurrence, duration, attendee name, time preferences, and exclusions from the natural language prompt.
   - How used: Parse 'weekly 30min 1:1', 'Sarah', 'afternoons preferred', 'avoid Fridays', and 'automatically find a new time' into structured scheduling constraints.

✅ **CAN-05: Attendee/Contact Resolution** (Tier 1)
   - Why needed: To resolve 'Sarah' to a specific calendar identity (email address) for scheduling.
   - How used: Look up Sarah in the directory and retrieve her email address for the meeting invite.

✅ **CAN-06: Availability Checking (Free/Busy)** (Tier 2)
   - Why needed: To check both the user's and Sarah's availability to find suitable time slots.
   - How used: Retrieve free/busy data for both participants over the desired timeframe to identify open slots.

✅ **CAN-12: Constraint Satisfaction** (Tier 2)
   - Why needed: To find a time slot that satisfies all constraints: weekly recurrence, 30-minute duration, afternoons, avoid Fridays, and both attendees available.
   - How used: Apply constraints to candidate time slots and select the optimal one.

⚠️ **CAN-15: Recurrence Rule Generation** (Tier 3)
   - Why needed: To generate an iCalendar RRULE for a weekly recurring meeting.
   - How used: Convert 'weekly' into RRULE format for the calendar event.

✅ **CAN-03: Calendar Event Creation/Update** (Tier 1)
   - Why needed: To create the recurring 1:1 meeting in the user's calendar.
   - How used: Create a calendar event with the specified recurrence, duration, attendees, and time slot.

✅ **CAN-07: Meeting Invitation/Notification Sending** (Tier 2)
   - Why needed: To send the meeting invitation to Sarah after creating the event.
   - How used: Dispatch the calendar invite to Sarah's email address.

⚠️ **CAN-16: Event Monitoring/Change Detection** (Tier 3)
   - Why needed: To detect if Sarah's schedule changes and trigger rescheduling.
   - How used: Monitor the event or Sarah's calendar for changes that cause conflicts.

⚠️ **CAN-17: Automatic Rescheduling** (Tier 3)
   - Why needed: To automatically find a new time if Sarah's schedule changes.
   - How used: Re-run availability checks and constraint satisfaction to reschedule the meeting.

**Execution Sequence**:

1. Step 1: Extract constraints and intent from user input (CAN-04).
2. Step 2: Resolve attendee 'Sarah' to calendar identity (CAN-05).
3. Step 3: Check availability for user and Sarah (CAN-06).
4. Step 4: Apply constraints to find optimal time slot (CAN-12).
5. Step 5: Generate recurrence rule for weekly meeting (CAN-15).
6. Step 6: Create recurring calendar event (CAN-03).
7. Step 7: Send meeting invitation to Sarah (CAN-07).
8. Step 8: Set up event monitoring for schedule changes (CAN-16).
9. Step 9: Implement automatic rescheduling workflow if conflicts arise (CAN-17).

**Recommendations**:

- Implement recurrence rule generation using dateutil.rrule or similar library.
- Develop webhook-based event monitoring to detect schedule changes.
- Build automatic rescheduling logic that reuses availability and constraint satisfaction modules.

---

### schedule-2

**Prompt**: "Clear my Thursday afternoon—reschedule what you can, and decline the rest."

**Implementation Effort**: Low  
**Coverage**: 100.0%

**Canonical Tasks Required**:

✅ **CAN-04: Natural Language Understanding (Constraint/Intent Extraction)** (Tier 1)
   - Why needed: To interpret the user's natural language request and extract structured constraints such as the time range (Thursday afternoon) and actions (reschedule or decline).
   - How used: Parse 'Thursday afternoon' into a specific date and time range, and identify the intent to reschedule or decline meetings.

✅ **CAN-01: Calendar Events Retrieval** (Tier 1)
   - Why needed: To retrieve all events scheduled during the specified time range (Thursday afternoon) from the user's calendar.
   - How used: Fetch events for Thursday afternoon to determine which meetings need to be rescheduled or declined.

✅ **CAN-06: Availability Checking (Free/Busy)** (Tier 2)
   - Why needed: To find alternative time slots for meetings that need to be rescheduled.
   - How used: Check availability of the user and other attendees to propose new times for rescheduled meetings.

✅ **CAN-12: Constraint Satisfaction** (Tier 2)
   - Why needed: To determine optimal new time slots that satisfy constraints for rescheduling meetings.
   - How used: Apply constraints such as attendee availability and meeting duration to find suitable reschedule options.

✅ **CAN-03: Calendar Event Creation/Update** (Tier 1)
   - Why needed: To update existing events with new times or to decline them if rescheduling is not possible.
   - How used: Modify event start/end times for rescheduled meetings and update RSVP status for declined meetings.

✅ **CAN-13: RSVP Status Update** (Tier 2)
   - Why needed: To formally decline meetings that cannot be rescheduled.
   - How used: Update the RSVP status of events to 'declined' when rescheduling is not feasible.

✅ **CAN-07: Meeting Invitation/Notification Sending** (Tier 2)
   - Why needed: To notify attendees about rescheduled meetings or declined invitations.
   - How used: Send updated invitations for rescheduled meetings and notifications for declined ones.

**Execution Sequence**:

1. Step 1: Use CAN-04 to parse the prompt and extract time range and intent.
2. Step 2: Use CAN-01 to retrieve all events scheduled for Thursday afternoon.
3. Step 3: For each event, attempt rescheduling using CAN-06 and CAN-12 to find alternative slots.
4. Step 4: Apply CAN-03 to update events with new times for successful reschedules.
5. Step 5: Use CAN-13 to decline events that cannot be rescheduled.
6. Step 6: Use CAN-07 to send notifications or updated invitations to attendees.

**Recommendations**:

- Implement robust NLU parsing for temporal expressions like 'Thursday afternoon' to ensure accurate time range extraction.
- Ensure conflict resolution logic prioritizes rescheduling before declining to minimize meeting cancellations.

---

### schedule-3

**Prompt**: "Land a time for Project Alpha with Chris, Sangya, and Kat for 1 hour in the next 2 weeks. Schedule over 1:1s if needed, work around Kat's schedule. In person with a room."

**Implementation Effort**: Medium  
**Coverage**: 75.0%

**Canonical Tasks Required**:

✅ **CAN-04: Natural Language Understanding (Constraint/Intent Extraction)** (Tier 1)
   - Why needed: To extract structured constraints and intent from the natural language prompt.
   - How used: Parse 'Project Alpha', attendees (Chris, Sangya, Kat), duration (1 hour), timeframe (next 2 weeks), constraints (override 1:1s, prioritize Kat's schedule), modality (in-person), and resource requirement (room).

✅ **CAN-05: Attendee/Contact Resolution** (Tier 1)
   - Why needed: To resolve attendee names to actual calendar identities for scheduling.
   - How used: Resolve 'Chris', 'Sangya', and 'Kat' to their corresponding email addresses or user IDs in the directory.

✅ **CAN-06: Availability Checking (Free/Busy)** (Tier 2)
   - Why needed: To check availability of all attendees within the specified timeframe.
   - How used: Retrieve free/busy information for the next 2 weeks for the user and all three attendees.

✅ **CAN-12: Constraint Satisfaction** (Tier 2)
   - Why needed: To find a time slot that satisfies all constraints including attendee availability, override rules, and priority for Kat's schedule.
   - How used: Apply constraints such as 'override 1:1s if needed', 'work around Kat's schedule', and 'within next 2 weeks' to identify optimal time slots.

✅ **CAN-03: Calendar Event Creation/Update** (Tier 1)
   - Why needed: To create the actual meeting event once the time slot is determined.
   - How used: Create a calendar event for 'Project Alpha' with the resolved attendees, chosen time slot, and location details.

✅ **CAN-07: Meeting Invitation/Notification Sending** (Tier 2)
   - Why needed: To send invitations to all attendees after creating the event.
   - How used: Dispatch meeting invitations to Chris, Sangya, and Kat once the event is scheduled.

⚠️ **CAN-19: Resource Booking (Rooms/Equipment)** (Tier 3)
   - Why needed: To book a physical meeting room for the in-person meeting.
   - How used: Search for and reserve an available conference room that fits the meeting time and requirements.

⚠️ **CAN-17: Automatic Rescheduling** (Tier 3)
   - Why needed: To handle the override rule for 1:1s if needed by automatically rescheduling them.
   - How used: If the chosen time conflicts with existing 1:1s, reschedule those meetings automatically.

**Execution Sequence**:

1. Step 1: Extract constraints and intent using CAN-04.
2. Step 2: Resolve attendee identities using CAN-05.
3. Step 3: Check availability for all attendees using CAN-06.
4. Step 4: Apply constraint satisfaction to find optimal time slot using CAN-12.
5. Step 5: Book a physical room using CAN-19.
6. Step 6: Create the calendar event using CAN-03.
7. Step 7: Send meeting invitations using CAN-07.
8. Step 8: If conflicts arise with 1:1s, apply automatic rescheduling using CAN-17.

**Recommendations**:

- Implement CAN-19 (Resource Booking) to support in-person meeting requirements.
- Implement CAN-17 (Automatic Rescheduling) to honor override rules for 1:1 meetings.
- Develop orchestration logic to integrate NLU, availability checking, constraint satisfaction, and event creation seamlessly.

---

### collaborate-1

**Prompt**: "I have a Project Alpha review coming up. Help me set the agenda based on what the team has been working on."

**Implementation Effort**: Medium  
**Coverage**: 83.3%

**Canonical Tasks Required**:

✅ **CAN-04: Natural Language Understanding (Constraint/Intent Extraction)** (Tier 1)
   - Why needed: To interpret the user's intent to create an agenda and extract context such as 'Project Alpha review' and the requirement to base it on team work.
   - How used: Extract intent: create_agenda; extract context: project name = Project Alpha, meeting type = review.

✅ **CAN-05: Attendee/Contact Resolution** (Tier 1)
   - Why needed: To identify which team members are associated with Project Alpha for gathering relevant work updates.
   - How used: Resolve 'the team' to actual team members or group associated with Project Alpha.

✅ **CAN-08: Document/Content Retrieval** (Tier 2)
   - Why needed: To retrieve recent work updates, documents, or progress reports from team repositories or project folders.
   - How used: Fetch documents or summaries from SharePoint, OneDrive, or project management tools related to Project Alpha.

✅ **CAN-09: Document Generation/Formatting** (Tier 2)
   - Why needed: To generate a structured agenda document based on retrieved content and meeting context.
   - How used: Create a formatted agenda with sections for discussion topics, updates, and action items.

✅ **CAN-02: Meeting Classification/Categorization** (Tier 1)
   - Why needed: To classify the meeting as a 'Project Review' for context-aware agenda generation and template selection.
   - How used: Categorize the meeting type to apply appropriate agenda structure and priorities.

⚠️ **CAN-18: Objection/Risk Anticipation** (Tier 3)
   - Why needed: To anticipate potential concerns or risks that might arise during the review and include them in the agenda.
   - How used: Analyze retrieved content to identify risks or blockers and add them as discussion points.

**Execution Sequence**:

1. Step 1: Use CAN-04 to extract intent and context (Project Alpha review).
2. Step 2: Apply CAN-05 to resolve team members associated with Project Alpha.
3. Step 3: Use CAN-08 to retrieve recent work updates and documents.
4. Step 4: Apply CAN-02 to classify the meeting as a project review.
5. Step 5: Optionally use CAN-18 to identify potential risks or objections.
6. Step 6: Use CAN-09 to generate a structured agenda document.

**Recommendations**:

- Leverage existing NLU and document retrieval pipelines to extract context and gather relevant content.
- Implement a lightweight risk anticipation module using LLM reasoning to enhance agenda quality.

---

### collaborate-2

**Prompt**: "I have an executive meeting in 2 hours. Pull together a briefing on the topics we'll be discussing."

**Implementation Effort**: Medium  
**Coverage**: 85.7%

**Canonical Tasks Required**:

✅ **CAN-04: Natural Language Understanding (Constraint/Intent Extraction)** (Tier 1)
   - Why needed: To interpret the user's request, extract the meeting reference, time constraint, and intent to generate a briefing.
   - How used: Parse 'executive meeting in 2 hours' to identify meeting type and time, and extract intent 'create briefing on discussion topics'.

✅ **CAN-01: Calendar Events Retrieval** (Tier 1)
   - Why needed: To find the specific executive meeting scheduled within the next 2 hours.
   - How used: Query the calendar for events matching 'executive meeting' within the next 2-hour window.

✅ **CAN-02: Meeting Classification/Categorization** (Tier 1)
   - Why needed: To confirm that the identified meeting is indeed an executive-level meeting and classify its type for context.
   - How used: Classify the retrieved meeting as 'executive' to ensure correct context for briefing generation.

✅ **CAN-08: Document/Content Retrieval** (Tier 2)
   - Why needed: To gather relevant documents, agendas, or prior notes related to the meeting topics.
   - How used: Retrieve files from SharePoint, OneDrive, or CRM that are linked to the meeting or its topics.

✅ **CAN-09: Document Generation/Formatting** (Tier 2)
   - Why needed: To compile the retrieved information into a structured, professional briefing document.
   - How used: Generate a formatted briefing summarizing discussion topics and key points for the executive meeting.

✅ **CAN-14: Recommendation Engine** (Tier 2)
   - Why needed: To suggest which topics or documents are most relevant for the briefing based on meeting context.
   - How used: Rank and recommend the most critical topics and supporting materials for inclusion in the briefing.

⚠️ **CAN-18: Objection/Risk Anticipation** (Tier 3)
   - Why needed: To anticipate potential concerns or objections that might arise during the executive meeting.
   - How used: Analyze meeting context and related documents to highlight possible risks or sensitive points.

**Execution Sequence**:

1. Step 1: Use CAN-04 to extract meeting intent, type, and time constraint from user input.
2. Step 2: Apply CAN-01 to retrieve the executive meeting scheduled within the next 2 hours.
3. Step 3: Use CAN-02 to confirm meeting classification as executive-level.
4. Step 4: Execute CAN-08 to gather relevant documents and prior meeting materials.
5. Step 5: Apply CAN-14 to recommend the most relevant topics and documents for the briefing.
6. Step 6: Use CAN-09 to generate a structured, formatted briefing document.
7. Step 7: (Optional) Implement CAN-18 to include risk anticipation insights in the briefing.

**Recommendations**:

- Leverage existing NLU, calendar retrieval, and document generation pipelines to fulfill the core request quickly.
- Plan for implementing CAN-18 (risk anticipation) as an enhancement for higher-value executive briefings.

---

### collaborate-3

**Prompt**: "I have a customer meeting tomorrow. Give me a dossier on the attendees and recent interactions."

**Implementation Effort**: Low  
**Coverage**: 100.0%

**Canonical Tasks Required**:

✅ **CAN-01: Calendar Events Retrieval** (Tier 1)
   - Why needed: To identify the specific customer meeting scheduled for tomorrow and retrieve its details.
   - How used: Query the calendar for events on the specified date and extract the meeting details including attendees.

✅ **CAN-05: Attendee/Contact Resolution** (Tier 1)
   - Why needed: To resolve attendee names or email addresses to specific identities for dossier generation.
   - How used: Map meeting attendees to directory profiles for enrichment and dossier creation.

✅ **CAN-08: Document/Content Retrieval** (Tier 2)
   - Why needed: To gather relevant documents or CRM data about attendees and recent interactions.
   - How used: Fetch recent emails, CRM notes, or shared documents related to the attendees.

✅ **CAN-09: Document Generation/Formatting** (Tier 2)
   - Why needed: To compile the retrieved information into a structured, readable dossier.
   - How used: Generate a formatted document summarizing attendee profiles and recent interactions.

✅ **CAN-02: Meeting Classification** (Tier 1)
   - Why needed: To confirm that the meeting is a customer meeting and apply appropriate dossier template.
   - How used: Classify the meeting type based on attendees and context.

**Execution Sequence**:

1. Step 1: Retrieve tomorrow's customer meeting details (CAN-01).
2. Step 2: Classify the meeting as customer-related (CAN-02).
3. Step 3: Resolve attendee identities and enrich profiles (CAN-05).
4. Step 4: Retrieve related documents and recent interactions (CAN-08).
5. Step 5: Generate and format the attendee dossier (CAN-09).

**Recommendations**:

- Integrate CRM and email data sources for richer interaction history.
- Ensure privacy and compliance checks when compiling attendee dossiers.

---

