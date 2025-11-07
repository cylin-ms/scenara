# Appendix – Gold-Standard Multi-step Reasoning Plan for Hero Prompts V2.0

**Document Version**: 2.0 (Simplified Format)  
**Date**: November 7, 2025  
**Author**: Chin-Yew Lin  
**Framework**: Calendar.AI Canonical Unit Tasks Framework V2.0 (25 tasks)  

---

## 1) Organizer-1: "Keep my Calendar up to date by committing to only meetings that are part of my priorities."

| Steps | Atomic Agent Capabilities |
| ------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1. Understand User Intent | • **Natural Language Understanding**: Extract user priorities and time constraints from the prompt |
| 2. Retrieve Pending Invitations | • **Calendar Events Retrieval**: Retrieve all pending calendar invitations for the current week |
| 3. Extract Meeting Metadata | • **Meeting Metadata Extraction**: Extract detailed metadata from pending invitations (attendees, agenda, organizer) |
| 4. Classify & Analyze Meetings | • **Meeting Type Classification**: Classify each pending invitation by meeting type<br>• **Meeting Importance Assessment**: Assess strategic importance of each meeting relative to user priorities |
| 5. Match Against Priorities | • **Priority/Preference Matching**: Compare meetings against user's stated priorities and calculate alignment scores |
| 6. Execute RSVP Actions | • **RSVP Status Update**: Update RSVP status based on prioritization decisions (accept/decline/tentative) |

---

## 2) Organizer-2: "Track all my important meetings and flag any that require focus time to prepare for them."

| Steps | Atomic Agent Capabilities |
| ------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1. Understand User Intent | • **Natural Language Understanding**: Extract user intent to identify "important meetings" and "prep time" requirements |
| 2. Retrieve Calendar | • **Calendar Events Retrieval**: Retrieve all upcoming meetings within planning horizon |
| 3. Identify Important Meetings | • **Meeting Type Classification**: Classify meetings by type to identify high-stakes formats<br>• **Meeting Importance Assessment**: Identify which meetings qualify as "important" based on criteria<br>• **Meeting Metadata Extraction**: Extract meeting details to assess prep requirements |
| 4. Assess Preparation Needs | • **Document/Content Retrieval**: Retrieve related documents, agendas, previous meeting notes<br>• **Focus Time/Preparation Time Analysis**: Estimate how much prep time is needed for each important meeting |
| 5. Filter Important Meetings | • **Priority/Preference Matching**: Filter to "important meetings" based on user criteria |
| 6. Setup Meeting Tracking | • **Event Monitoring/Change Detection**: Setup tracking/monitoring for important meetings |
| 7. Flag Prep-Required Meetings | • **Event Annotation/Flagging**: Flag meetings that require focus time with visual indicators |

---

## 3) Organizre-3: "Help me understand where I am spending my time and identify ways I can reclaim time to focus more on my top priorities."

| Steps | Atomic Agent Capabilities |
| ---------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1. Understand User Intent | • **Natural Language Understanding**: Extract user intent for time analysis and reclamation focus |
| 2. Retrieve Historical Data | • **Calendar Events Retrieval**: Load historical calendar events for time analysis period |
| 3. Classify & Enrich Historical Meetings | • **Meeting Type Classification**: Classify past meetings by type for categorization<br>• **Meeting Importance Assessment**: Assess which past meetings aligned with top priorities<br>• **Meeting Metadata Extraction**: Extract meeting details for analysis |
| 4. Aggregate & Analyze | • **Time Aggregation/Statistical Analysis**: Aggregate time spent per category, participant, project |
| 5. Match Against Priorities | • **Priority/Preference Matching**: Analyze alignment with user's top priorities and identify gaps |
| 6. Generate Reclamation Recommendations | • **Recommendation Engine**: Identify low-value meetings and reclamation opportunities |
| 7. Visualize Patterns | • **Data Visualization/Reporting**: Create visual representations of time distribution |

---

## 4) Schedule-1: "Starting next week, I want a weekly 30-min 1:1 with {name}. Afternoons preferred, avoid Fridays. Automatically reschedule on declines or conflicts."

| Steps | Atomic Agent Capabilities |
| -------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1. Parse Scheduling Requirements | • **Natural Language Understanding**: Extract scheduling requirements (recurring, participants, durations, timeframe, preferences) |
| 2. Resolve Participant Identity | • **Attendee/Contact Resolution**: Resolve {name} to full contact profile with calendar access |
| 3. Check Availability | • **Availability Checking**: Check user's and {name}'s availability for afternoons, excluding Fridays |
| 4. Analyze Constraints | • **Constraint Satisfaction**: Find time slots that satisfy all constraints (30 min, weekly, afternoon, not Friday) |
| 5. Generate Recurrence Pattern | • **Recurrence Rule Generation**: Create iCalendar RRULE for weekly recurrence pattern |
| 6. Create Recurring Meeting | • **Calendar Event Creation**: Create recurring calendar event with all specified details |
| 7. Setup Change Monitoring | • **Event Monitoring/Change Detection**: Setup monitoring for declines and conflicts |
| 8. Configure Auto-Reschedule | • **Automatic Rescheduling**: Configure orchestrated workflow to automatically reschedule on declines/conflicts |

---

## 5) Schedule-2: "Clear my Thursday afternoon. Update my RSVPs and help me reschedule my meetings to another time and show me as {status}."

| Steps | Atomic Agent Capabilities |
| --------------------------------- | -------------------------------------------------------------------------------------------------------- |
| 1. Understand Rescheduling Requirements | • **Natural Language Understanding**: Extract multi-action request (clear time block, update RSVPs, reschedule, set status) |
| 2. Retrieve Thursday Meetings | • **Calendar Events Retrieval**: Retrieve all meetings in Thursday afternoon time block |
| 3. Extract Meeting Metadata | • **Meeting Metadata Extraction**: Extract meeting details (attendees, organizer, duration, RSVP status) |
| 4. Resolve All Attendees | • **Attendee/Contact Resolution**: Resolve attendees for coordination and availability checking |
| 5. Update RSVPs | • **RSVP Status Update**: Update RSVP status to decline or tentative for Thursday meetings |
| 6. Find Alternative Time Slots | • **Availability Checking**: Check availability across all attendees to find alternative meeting times |
| 7. Select Optimal Alternatives | • **Constraint Satisfaction**: Apply preferences to select best alternative time slots |
| 8. Generate Rescheduling Plan | • **Agenda Generation/Structuring**: Create rescheduling proposal showing old time → new time |
| 9. Update Calendar | • **Calendar Event Update**: Execute rescheduling and set calendar status to {status} for Thursday afternoon |

---

## 6) Schedule-3: "Land a time to meet about Project Alpha with Chris, Sangya, and Kat for 1 hour in the next 2 weeks. Schedule over 1:1s and lunches if needed and work around Kat's schedule. Make the meeting in person and add a room."

| Steps | Atomic Agent Capabilities |
| -------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1. Parse Complex Requirements | • **Natural Language Understanding**: Extract multi-constraint scheduling request (participants, duration, timeframe, conflict resolution, location, resources) |
| 2. Resolve Participant Identities | • **Attendee/Contact Resolution**: Resolve all participant names to full contact profiles with calendar access |
| 3. Check Multi-Party Availability | • **Availability Checking**: Check availability for all 4 participants within next 2 weeks |
| 4. Identify Conflict Types | • **Meeting Type Classification**: Classify existing meetings to identify reschedulable types (1:1s, lunches) |
| 5. Solve Complex Constraints | • **Constraint Satisfaction**: Find time slots satisfying all constraints (Kat's schedule, 1 hour, 2 weeks, in-person) |
| 6. Handle Scheduling Conflicts | • **Conflict Resolution**: Resolve conflicts by identifying which 1:1s/lunches can be rescheduled |
| 7. Find Meeting Room | • **Resource Booking**: Book conference room for in-person meeting with required capacity |
| 8. Generate Meeting Proposal | • **Recommendation Engine**: Propose optimal solution with alternatives if primary option unavailable |
| 9. Create Calendar Event | • **Calendar Event Creation**: Create meeting with all details (attendees, time, location, room) |
| 10. Coordinate Multi-Party | • **Multi-party Coordination/Negotiation**: Handle scheduling negotiations if no perfect slot exists |

---

## 7) Collaborate-1: "Help me set the agenda to review the progress of Project Alpha with the product and marketing team to get confirmation we are on track and discuss any blocking issues or risks."

| Steps | Atomic Agent Capabilities |
| -------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1. Understand Agenda Requirements | • **Natural Language Understanding**: Extract agenda structure requirements and discussion topics |
| 2. Find Project Alpha Meetings | • **Calendar Events Retrieval**: Find existing/upcoming Project Alpha meetings with product and marketing teams |
| 3. Retrieve Meeting Materials | • **Document/Content Retrieval**: Retrieve related documents (previous notes, action items, project plans, blockers) |
| 4. Gather Background Intelligence | • **Research/Intelligence Gathering**: Gather project context, current status, milestones, known blockers |
| 5. Identify Priority Topics | • **Priority/Preference Matching**: Identify most important agenda topics based on user's stated goals |
| 6. Structure Agenda | • **Agenda Generation/Structuring**: Create structured meeting agenda with sections for progress, confirmation, blocking issues |
| 7. Generate Formatted Agenda | • **Document Generation/Formatting**: Generate formatted agenda document for distribution |

---

## 8) Collaborate-2: "Review the materials for my meeting with senior leadership and suggest the best way to summarize the topics into three main discussion points. Generate any objections or concerns that might come up and give me effective responses."

| Steps | Atomic Agent Capabilities |
| -------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1. Understand Preparation Requirements | • **Natural Language Understanding**: Extract multi-part preparation request (review, summarize, anticipate objections, prepare responses) |
| 2. Identify Senior Leadership | • **Attendee/Contact Resolution**: Identify who qualifies as "senior leadership" to find the correct meeting |
| 3. Find Senior Leadership Meeting | • **Calendar Events Retrieval**: Find the specific meeting with senior leadership |
| 4. Extract Meeting Metadata | • **Meeting Metadata Extraction**: Extract meeting context (attendees, agenda, organizer, purpose) |
| 5. Retrieve All Materials | • **Document/Content Retrieval**: Retrieve all meeting materials (attachments, presentations, reports, previous notes) |
| 6. Gather Intelligence | • **Research/Intelligence Gathering**: Gather background on attendees, topics, company priorities, strategic initiatives |
| 7. Synthesize to Three Points | • **Document Generation/Formatting**: Summarize materials into 3 main discussion points with executive-level clarity |
| 8. Anticipate Objections | • **Objection/Risk Anticipation**: Predict potential concerns or pushback from senior leadership |
| 9. Generate Effective Responses | • **Document Generation/Formatting**: Create response strategies with data/evidence for each anticipated objection |
| 10. Assess Meeting Importance | • **Meeting Importance Assessment**: Confirm high-stakes nature and identify critical success factors |

---

## 9) Collaborate-3: "Prepare a brief for my upcoming meeting with customer Beta and include a dossier for each customer attendee and the topics they are most interested in. Include a background on their company."

| Steps | Atomic Agent Capabilities |
| -------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1. Understand Brief Requirements | • **Natural Language Understanding**: Extract preparation requirements (brief, individual dossiers, topic interests, company background) |
| 2. Find Customer Beta Meeting | • **Calendar Events Retrieval**: Find the specific meeting with customer Beta |
| 3. Extract Meeting Details | • **Meeting Metadata Extraction**: Extract meeting context (attendees, agenda, organizer, purpose, location) |
| 4. Resolve Customer Attendees | • **Attendee/Contact Resolution**: Resolve customer attendee identities to full profiles |
| 5. Retrieve Meeting Materials | • **Document/Content Retrieval**: Retrieve all related content (previous notes, emails, presentations, contracts) |
| 6. Research Customer Company | • **Research/Intelligence Gathering**: Gather comprehensive background (company info, attendee profiles, topics of interest, relationship history) |
| 7. Create Individual Dossiers | • **Document Generation/Formatting**: Generate attendee dossiers with profiles, topics of interest, decision authority |
| 8. Generate Company Background | • **Document Generation/Formatting**: Create company background section (overview, industry, news, relationship history) |
| 9. Compile Meeting Brief | • **Document Generation/Formatting**: Assemble comprehensive brief (overview, company background, dossiers, talking points) |

---

**Document End**
