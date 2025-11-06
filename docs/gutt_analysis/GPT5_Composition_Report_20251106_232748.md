# GPT-5 Execution Composition Analysis Report

**Generated**: 20251106_232748
**Model**: dev-gpt-5-chat-jj
**Analysis Type**: Execution Composition & Data Flow

---

## Executive Summary

- **Total Prompts Analyzed**: 9
- **Successful Analyses**: 9
- **Total Execution Steps**: 50
- **Average Steps per Prompt**: 5.6

### Composition Patterns

- **sequential**: 2 prompts
- **sequential with conditional branching**: 1 prompts
- **hybrid (sequential core flow with parallel RRULE generation and asynchronous monitoring)**: 1 prompts
- **hybrid (sequential core flow with parallel sub-tasks and conditional branching)**: 1 prompts
- **hybrid (parallel for data retrieval, sequential for constraint solving and event creation)**: 1 prompts
- **hybrid (mostly sequential with partial parallelism)**: 1 prompts
- **hybrid (sequential core with parallel sub-tasks in content retrieval)**: 1 prompts
- **hybrid (sequential with parallel sub-tasks)**: 1 prompts

---

## Detailed Execution Plans

### 1. organizer-1

**Prompt**: Show me my pending invitations and which ones I should prioritize based on my priorities for this week: customer meetings and product strategy.

**Composition Pattern**: sequential

**Execution Steps**: 4

#### Step 1: CAN-04 - Natural Language Understanding (Constraint/Intent Extraction) (Tier 1)

**Input**:
- Type: `user_prompt`
- Description: Raw user input text specifying the request and priorities
- Schema: `{"text": "Show me my pending invitations and which ones I should prioritize based on my priorities for this week: customer meetings and product strategy."}`

**Processing**: Use NLU to extract structured intents and constraints: identify action (show pending invitations), extract user priorities (customer meetings, product strategy), and time frame (this week).

**Output**:
- Description: Structured representation of user intent and constraints
- Schema: `{"intent": "show_pending_invitations", "priorities": ["customer meetings", "product strategy"], "timeframe": "this week"}`

**Flows To**: step_2

#### Step 2: CAN-01 - Calendar Events Retrieval (Tier 1)

**Input**:
- Type: `previous_step_output + external_data`
- Description: Structured constraints from step 1 and calendar API
- Schema: `{"time_range": "start/end of current week", "filter": "status eq 'pending' or responseStatus eq 'notResponded'"}`

**Processing**: Call Microsoft Graph API to retrieve all calendar events within the specified time range that have pending invitations (user has not responded).

**Output**:
- Description: List of pending invitation events with metadata
- Schema: `[{"id": "string", "subject": "string", "start": "datetime", "end": "datetime", "attendees": ["email"], "organizer": "email", "responseStatus": "notResponded"}]`

**Flows To**: step_3

#### Step 3: CAN-02 - Meeting Classification (Tier 1)

**Input**:
- Type: `previous_step_output + previous_step_output`
- Description: Pending invitations from step 2 and user priorities from step 1
- Schema: `{"events": [{"id": "string", "subject": "string", "attendees": ["string"], "bodyPreview": "string"}], "priorities": ["customer meetings", "product strategy"]}`

**Processing**: Classify each event by relevance to user priorities using semantic similarity and rule-based classification. Compute a priority score for each event (0.0-1.0) and assign a category (High, Medium, Low).

**Output**:
- Description: List of pending invitations with priority scores and categories
- Schema: `[{"id": "string", "subject": "string", "priority_score": "float", "priority_category": "High|Medium|Low"}]`

**Flows To**: step_4

#### Step 4: CAN-11 - Priority/Preference Matching (Tier 2)

**Input**:
- Type: `previous_step_output`
- Description: Classified events with scores from step 3
- Schema: `[{"id": "string", "subject": "string", "priority_score": "float"}]`

**Processing**: Rank events by priority score and filter top recommendations. Apply threshold logic (e.g., score > 0.7 = High priority).

**Output**:
- Description: Ranked list of pending invitations with priority recommendations
- Schema: `{"ranked_events": [{"id": "string", "subject": "string", "priority_score": "float", "priority_category": "High|Medium|Low"}]}`

**Flows To**: [Final Output]

**Data Flow Summary**:

User input is parsed by NLU (step 1) to extract priorities and timeframe → Calendar API retrieves pending invitations (step 2) → Events are classified against priorities (step 3) → Ranked by priority score for final recommendation (step 4).

**Orchestration Logic**:

- Sequential execution: steps 1 → 2 → 3 → 4
- Error handling: If NLU fails, fallback to default timeframe (current week) and no priority filtering
- If calendar retrieval fails, return error message to user
- If classification fails, return unranked pending invitations
- Retry strategy: API calls retried up to 3 times with exponential backoff

**Final Output**:
- Type: `UI_display`
- Description: User sees a ranked list of pending invitations with priority recommendations
- Schema: `{"pending_invitations": [{"subject": "string", "start": "datetime", "priority_category": "High|Medium|Low", "priority_score": "float"}]}`

---

### 2. organizer-2

**Prompt**: I have some important meetings this week—flag the ones I need to prep for, and put time on my calendar to prepare.

**Composition Pattern**: sequential with conditional branching

**Execution Steps**: 5

#### Step 1: CAN-04 - Natural Language Understanding (Constraint/Intent Extraction) (Tier 1)

**Input**:
- Type: `user_prompt`
- Description: Raw user input text specifying intent and constraints
- Schema: `{"text": "I have some important meetings this week\u2014flag the ones I need to prep for, and put time on my calendar to prepare."}`

**Processing**: Extract user intent (flag important meetings, schedule prep time) and temporal constraints (this week). Identify actions: classify meetings by importance, allocate prep time.

**Output**:
- Description: Structured representation of user intent and constraints
- Schema: `{"intent": "flag_and_schedule_prep", "timeframe": {"start": "2025-11-06T00:00:00", "end": "2025-11-13T00:00:00"}, "actions": ["identify_important_meetings", "schedule_prep_time"]}`

**Flows To**: step_2

#### Step 2: CAN-01 - Calendar Events Retrieval (Tier 1)

**Input**:
- Type: `previous_step_output + external_data`
- Description: Timeframe from NLU and calendar API
- Schema: `{"timeframe": {"start": "2025-11-06T00:00:00", "end": "2025-11-13T00:00:00"}}`

**Processing**: Query calendar API for all events within the specified timeframe. Retrieve metadata: subject, start, end, attendees, location.

**Output**:
- Description: List of calendar events for the week
- Schema: `[{"id": "event123", "subject": "Q4 Strategy Review", "start": "2025-11-08T14:00:00", "end": "2025-11-08T15:00:00", "attendees": ["vp@company.com"], "location": "Conf Room A"}]`

**Flows To**: step_3

#### Step 3: CAN-02 - Meeting Classification (Tier 1)

**Input**:
- Type: `previous_step_output`
- Description: List of events retrieved from calendar
- Schema: `[{"id": "event123", "subject": "Q4 Strategy Review", "attendees": ["vp@company.com"], "duration": 60}]`

**Processing**: Apply classification model to determine importance level for each meeting (Critical, High, Medium, Low) based on attendees, subject, duration, and context.

**Output**:
- Description: Events annotated with importance classification
- Schema: `[{"id": "event123", "subject": "Q4 Strategy Review", "importance": "Critical"}]`

**Flows To**: step_4

#### Step 4: CAN-14 - Recommendation Engine (Tier 2)

**Input**:
- Type: `previous_step_output`
- Description: Classified events with importance levels
- Schema: `[{"id": "event123", "subject": "Q4 Strategy Review", "importance": "Critical"}]`

**Processing**: Select meetings flagged as Critical or High importance. Generate recommendations for prep time allocation (e.g., 30-60 minutes before meeting).

**Output**:
- Description: List of meetings requiring prep and recommended prep slots
- Schema: `[{"event_id": "event123", "prep_duration": 60, "preferred_prep_time": "before_meeting"}]`

**Flows To**: step_5

#### Step 5: CAN-03 - Calendar Event Creation/Update (Tier 1)

**Input**:
- Type: `previous_step_output`
- Description: Recommended prep slots for important meetings
- Schema: `[{"event_id": "event123", "prep_duration": 60, "preferred_prep_time": "before_meeting"}]`

**Processing**: Create new calendar events for prep time. Schedule them before the corresponding important meetings, ensuring no conflicts.

**Output**:
- Description: Confirmation of prep events created in calendar
- Schema: `[{"prep_event_id": "prep456", "linked_meeting_id": "event123", "start": "2025-11-08T13:00:00", "end": "2025-11-08T14:00:00"}]`

**Flows To**: [Final Output]

**Data Flow Summary**:

User intent and timeframe extracted → Calendar events retrieved → Events classified by importance → Important meetings identified → Prep time recommendations generated → Prep events created in calendar.

**Orchestration Logic**:

- Sequential execution: NLU → Retrieval → Classification → Recommendation → Event Creation
- Conditional branching: If no important meetings found, skip prep scheduling
- Error handling: If calendar API fails, retry up to 3 times with exponential backoff
- Fallback: If prep slot conflicts cannot be resolved, notify user for manual adjustment

**Final Output**:
- Type: `UI_display + calendar_update`
- Description: User sees flagged important meetings and new prep time blocks added to calendar
- Schema: `{"flagged_meetings": [{"id": "event123", "subject": "Q4 Strategy Review", "importance": "Critical"}], "prep_events": [{"id": "prep456", "linked_meeting_id": "event123", "start": "2025-11-08T13:00:00", "end": "2025-11-08T14:00:00"}]}`

---

### 3. organizer-3

**Prompt**: I'm spending too much time in meetings. Help me find patterns in my calendar and identify opportunities to reclaim time.

**Composition Pattern**: sequential

**Execution Steps**: 5

#### Step 1: CAN-01 - Calendar Events Retrieval (Tier 1)

**Input**:
- Type: `user_prompt`
- Description: User request triggers retrieval of historical calendar data for analysis
- Schema: `{"time_range": {"start": "ISO8601 datetime", "end": "ISO8601 datetime"}, "filters": {"status": "accepted", "include_fields": ["subject", "start", "end", "attendees", "categories"]}}`

**Processing**: Call Microsoft Graph API to fetch all calendar events within the last 4-8 weeks (configurable). Apply filters to include only accepted meetings and relevant fields.

**Output**:
- Description: Array of raw calendar event objects
- Schema: `[{"id": "string", "subject": "string", "start": "datetime", "end": "datetime", "attendees": ["string"], "categories": ["string"]}]`

**Flows To**: step_2

#### Step 2: CAN-02 - Meeting Classification (Tier 1)

**Input**:
- Type: `previous_step_output`
- Description: Raw calendar events from step 1
- Schema: `[{"id": "string", "subject": "string", "start": "datetime", "end": "datetime", "attendees": ["string"]}]`

**Processing**: Apply ML or rule-based classification to categorize each meeting by type (e.g., 1:1, team sync, customer call) and importance level (Critical/High/Medium/Low).

**Output**:
- Description: Calendar events enriched with classification metadata
- Schema: `[{"id": "string", "subject": "string", "start": "datetime", "end": "datetime", "meeting_type": "string", "importance": "string"}]`

**Flows To**: step_3

#### Step 3: CAN-10 - Time Aggregation/Statistical Analysis (Tier 2)

**Input**:
- Type: `previous_step_output`
- Description: Classified calendar events from step 2
- Schema: `[{"id": "string", "meeting_type": "string", "importance": "string", "duration_minutes": "integer"}]`

**Processing**: Aggregate total time spent by meeting type, importance, and week. Compute metrics such as total meeting hours, average duration, and distribution across categories.

**Output**:
- Description: Aggregated statistics and patterns
- Schema: `{"total_meeting_hours": "float", "avg_meeting_duration": "float", "time_by_type": {"1:1": "float", "Team Sync": "float", "Customer Call": "float"}, "time_by_importance": {"Critical": "float", "High": "float", "Medium": "float", "Low": "float"}}`

**Flows To**: step_4

#### Step 4: CAN-11 - Priority/Preference Matching (Tier 2)

**Input**:
- Type: `previous_step_output + user_prompt`
- Description: Aggregated stats and user intent to reclaim time
- Schema: `{"aggregated_stats": {"time_by_type": "object", "time_by_importance": "object"}, "user_intent": "reduce meeting load"}`

**Processing**: Identify low-value or low-priority meeting categories consuming significant time. Rank opportunities for time reclamation based on importance and alignment with user goals.

**Output**:
- Description: Ranked list of meeting types or patterns to reduce
- Schema: `[{"pattern": "string", "time_spent_hours": "float", "recommendation": "string"}]`

**Flows To**: step_5

#### Step 5: CAN-14 - Recommendation Engine (Tier 2)

**Input**:
- Type: `previous_step_output`
- Description: Ranked opportunities for time reclamation
- Schema: `[{"pattern": "string", "time_spent_hours": "float", "recommendation": "string"}]`

**Processing**: Generate actionable recommendations such as 'Convert weekly 1:1s to bi-weekly', 'Decline low-priority recurring meetings', or 'Block focus time'. Format for user-friendly display.

**Output**:
- Description: Final recommendations with supporting data
- Schema: `{"summary": "string", "recommendations": [{"action": "string", "impact": "string", "supporting_data": "string"}]}`

**Flows To**: [Final Output]

**Data Flow Summary**:

User prompt triggers calendar retrieval (step 1), events are classified (step 2), aggregated for patterns (step 3), matched against user intent (step 4), and converted into actionable recommendations (step 5). Each step enriches data for the next, forming a sequential pipeline.

**Orchestration Logic**:

- Sequential execution: steps 1 → 2 → 3 → 4 → 5
- Error handling: If calendar retrieval fails, abort with user-friendly error
- Fallback: If classification model unavailable, use rule-based fallback
- Conditional: If insufficient data (<10 meetings), return advisory message instead of full analysis
- Parallelization: None required; all steps depend on previous outputs

**Final Output**:
- Type: `UI_display`
- Description: User receives a dashboard or summary report showing meeting patterns and actionable recommendations to reclaim time
- Schema: `{"summary": "string", "charts": {"time_by_type": "bar_chart", "time_by_importance": "pie_chart"}, "recommendations": [{"action": "string", "impact": "string", "supporting_data": "string"}]}`

---

### 4. schedule-1

**Prompt**: Land a weekly 30min 1:1 with Sarah for me, afternoons preferred, avoid Fridays. If her schedule changes, automatically find a new time.

**Composition Pattern**: hybrid (sequential core flow with parallel RRULE generation and asynchronous monitoring)

**Execution Steps**: 7

#### Step 1: CAN-04 - Natural Language Understanding (Constraint/Intent Extraction) (Tier 1)

**Input**:
- Type: `user_prompt`
- Description: Raw natural language scheduling request from user
- Schema: `"{ \"text\": \"Land a weekly 30min 1:1 with Sarah for me, afternoons preferred, avoid Fridays. If her schedule changes, automatically find a new time.\" }"`

**Processing**: Parse the user prompt to extract structured constraints: recurrence pattern, duration, attendee name, time preferences, exclusions, and automation intent.

**Output**:
- Description: Structured scheduling constraints extracted from natural language
- Schema: `"{ \"recurrence\": \"weekly\", \"duration_minutes\": 30, \"attendees\": [\"Sarah\"], \"time_preferences\": {\"preferred\": \"afternoon\", \"exclude_days\": [\"Friday\"]}, \"automation\": {\"auto_reschedule\": true} }"`

**Flows To**: step_2, step_5

#### Step 2: CAN-05 - Attendee/Contact Resolution (Tier 1)

**Input**:
- Type: `previous_step_output`
- Description: Attendee names extracted from NLU step
- Schema: `"{ \"attendees\": [\"Sarah\"] }"`

**Processing**: Resolve attendee name(s) to unique calendar identities using directory lookup and disambiguation logic.

**Output**:
- Description: Resolved attendee identities with email addresses
- Schema: `"{ \"attendees\": [{\"name\": \"Sarah Smith\", \"email\": \"sarah.smith@company.com\"}] }"`

**Flows To**: step_3

#### Step 3: CAN-06 - Availability Checking (Free/Busy) (Tier 2)

**Input**:
- Type: `previous_step_output + external_data`
- Description: Resolved attendee emails and user identity; time window for scheduling
- Schema: `"{ \"schedules\": [\"me@company.com\", \"sarah.smith@company.com\"], \"time_window\": {\"start\": \"2025-11-06T00:00:00\", \"end\": \"2025-12-06T23:59:59\"} }"`

**Processing**: Call calendar API to retrieve free/busy information for both user and Sarah over the next month, with 30-minute granularity.

**Output**:
- Description: Availability blocks for each participant
- Schema: `"{ \"availability\": {\"me@company.com\": [...], \"sarah.smith@company.com\": [...] } }"`

**Flows To**: step_4

#### Step 4: CAN-12 - Constraint Satisfaction (Tier 2)

**Input**:
- Type: `previous_step_output + step_1 constraints`
- Description: Availability data combined with user constraints (recurrence, duration, time preferences, exclusions)
- Schema: `"{ \"availability\": {...}, \"constraints\": {\"recurrence\": \"weekly\", \"duration\": 30, \"preferred_time\": \"afternoon\", \"exclude_days\": [\"Friday\"]} }"`

**Processing**: Run constraint solver to identify optimal recurring time slots that satisfy all constraints and both participants' availability.

**Output**:
- Description: Optimal time slot(s) for recurring meeting
- Schema: `"{ \"selected_slot\": {\"day\": \"Tuesday\", \"start\": \"14:00\", \"end\": \"14:30\"}, \"recurrence\": \"weekly\" }"`

**Flows To**: step_6

#### Step 5: CAN-15 - Recurrence Rule Generation (Tier 3)

**Input**:
- Type: `step_1 constraints`
- Description: Recurrence pattern extracted from NLU
- Schema: `"{ \"recurrence\": \"weekly\" }"`

**Processing**: Generate iCalendar RRULE string for weekly recurrence.

**Output**:
- Description: RRULE string for recurring event
- Schema: `"{ \"rrule\": \"FREQ=WEEKLY;BYDAY=TU\" }"`

**Flows To**: step_6

#### Step 6: CAN-03 - Calendar Event Creation/Update (Tier 1)

**Input**:
- Type: `previous_step_outputs`
- Description: Selected time slot, recurrence rule, attendee identities
- Schema: `"{ \"subject\": \"1:1 with Sarah\", \"start\": \"2025-11-11T14:00:00\", \"end\": \"2025-11-11T14:30:00\", \"attendees\": [\"sarah.smith@company.com\"], \"rrule\": \"FREQ=WEEKLY;BYDAY=TU\" }"`

**Processing**: Create recurring calendar event via Microsoft Graph API with specified attendees, time, and recurrence rule.

**Output**:
- Description: Confirmation of event creation with event ID
- Schema: `"{ \"event_id\": \"AAMkAGVmMDEz...\", \"status\": \"created\" }"`

**Flows To**: step_7

#### Step 7: CAN-16 - Event Monitoring/Change Detection (Tier 3)

**Input**:
- Type: `previous_step_output`
- Description: Created event ID and automation flag
- Schema: `"{ \"event_id\": \"AAMkAGVmMDEz...\", \"auto_reschedule\": true }"`

**Processing**: Subscribe to calendar webhook notifications for changes in Sarah's schedule or this event; trigger rescheduling workflow if conflicts arise.

**Output**:
- Description: Webhook subscription confirmation
- Schema: `"{ \"subscription_id\": \"sub_12345\", \"status\": \"active\" }"`

**Flows To**: [Final Output]

**Data Flow Summary**:

User prompt → NLU extracts constraints → Attendee resolution → Availability check → Constraint solver finds optimal slot → Recurrence rule generated → Event created → Monitoring set up for auto-reschedule.

**Orchestration Logic**:

- Sequential execution for steps 1-6; step 5 (RRULE generation) can run in parallel with step 3-4.
- Conditional: If attendee resolution fails, prompt user for clarification.
- Error handling: Retry API calls for availability and event creation on transient errors.
- Fallback: If no slot found, return alternative suggestions or ask user to relax constraints.
- Asynchronous: Event monitoring runs as background subscription after event creation.

**Final Output**:
- Type: `calendar_update`
- Description: Recurring 1:1 meeting scheduled in user's calendar with auto-reschedule enabled
- Schema: `"{ \"status\": \"success\", \"event_details\": {\"subject\": \"1:1 with Sarah\", \"start\": \"2025-11-11T14:00:00\", \"recurrence\": \"weekly\", \"attendees\": [\"sarah.smith@company.com\"]}, \"auto_reschedule\": true }"`

---

### 5. schedule-2

**Prompt**: Clear my Thursday afternoon—reschedule what you can, and decline the rest.

**Composition Pattern**: hybrid (sequential core flow with parallel sub-tasks and conditional branching)

**Execution Steps**: 6

#### Step 1: CAN-04 - Natural Language Understanding (Constraint/Intent Extraction) (Tier 1)

**Input**:
- Type: `user_prompt`
- Description: Raw user input text specifying intent and constraints
- Schema: `"{ \"text\": \"Clear my Thursday afternoon\u2014reschedule what you can, and decline the rest.\" }"`

**Processing**: Parse natural language to extract structured constraints: target time window (Thursday afternoon), actions (reschedule vs decline), and intent (clear schedule). Resolve relative date to absolute date using current context.

**Output**:
- Description: Structured representation of constraints and intent
- Schema: `"{ \"intent\": \"clear_time_block\", \"time_range\": { \"date\": \"2025-11-07\", \"start\": \"13:00\", \"end\": \"17:00\" }, \"actions\": { \"primary\": \"reschedule\", \"fallback\": \"decline\" } }"`

**Flows To**: step_2

#### Step 2: CAN-01 - Calendar Events Retrieval (Tier 1)

**Input**:
- Type: `previous_step_output + external_data`
- Description: Time range from step 1 and user calendar data
- Schema: `"{ \"time_range\": { \"start\": \"2025-11-07T13:00:00\", \"end\": \"2025-11-07T17:00:00\" } }"`

**Processing**: Query calendar API to retrieve all events overlapping the specified time range. Include event details: id, subject, start, end, attendees, flexibility indicators.

**Output**:
- Description: List of events scheduled during Thursday afternoon
- Schema: `"[ { \"id\": \"evt123\", \"subject\": \"Team Sync\", \"start\": \"2025-11-07T14:00:00\", \"end\": \"2025-11-07T15:00:00\", \"attendees\": [\"a@company.com\"], \"isFlexible\": true }, ... ]"`

**Flows To**: step_3

#### Step 3: CAN-02 - Meeting Classification (Tier 1)

**Input**:
- Type: `previous_step_output`
- Description: List of events retrieved from calendar
- Schema: `"[ { \"id\": \"evt123\", \"subject\": \"Team Sync\", \"attendees\": [...], \"duration\": 60 } ]"`

**Processing**: Classify each event by importance and flexibility to determine rescheduling eligibility. Use rules or ML model to assign categories: {critical, high, medium, low} and reschedulable flag.

**Output**:
- Description: Events annotated with classification and rescheduling eligibility
- Schema: `"[ { \"id\": \"evt123\", \"importance\": \"medium\", \"reschedulable\": true }, { \"id\": \"evt456\", \"importance\": \"high\", \"reschedulable\": false } ]"`

**Flows To**: step_4

#### Step 4: CAN-06 - Availability Checking (Free/Busy) (Tier 2)

**Input**:
- Type: `previous_step_output + external_data`
- Description: Events marked as reschedulable and attendee lists
- Schema: `"{ \"reschedulable_events\": [ { \"id\": \"evt123\", \"attendees\": [\"a@company.com\"] } ], \"time_window\": \"next 7 days\" }"`

**Processing**: For each reschedulable event, check availability of all attendees in the next 7 days to find alternative slots. Use free/busy API to get availability grids.

**Output**:
- Description: Candidate alternative time slots for each reschedulable event
- Schema: `"{ \"evt123\": [ { \"start\": \"2025-11-10T10:00:00\", \"end\": \"2025-11-10T11:00:00\" }, ... ] }"`

**Flows To**: step_5

#### Step 5: CAN-03 - Calendar Event Creation/Update (Tier 1)

**Input**:
- Type: `previous_step_output`
- Description: Alternative slots for reschedulable events and original event IDs
- Schema: `"{ \"evt123\": { \"new_time\": { \"start\": \"2025-11-10T10:00:00\", \"end\": \"2025-11-10T11:00:00\" } } }"`

**Processing**: Update calendar events with new time slots for reschedulable meetings. For non-reschedulable events, mark for decline.

**Output**:
- Description: Update confirmation for rescheduled events and list of events to decline
- Schema: `"{ \"rescheduled\": [\"evt123\"], \"to_decline\": [\"evt456\"] }"`

**Flows To**: step_6

#### Step 6: CAN-13 - RSVP Status Update (Tier 2)

**Input**:
- Type: `previous_step_output`
- Description: List of events to decline
- Schema: `"{ \"to_decline\": [\"evt456\", \"evt789\"] }"`

**Processing**: Send RSVP decline updates for events that cannot be rescheduled.

**Output**:
- Description: Confirmation of declined events
- Schema: `"{ \"declined\": [\"evt456\", \"evt789\"] }"`

**Flows To**: [Final Output]

**Data Flow Summary**:

User input → NLU extracts constraints → Calendar events retrieved → Events classified for rescheduling → Availability checked for alternatives → Events updated or declined → RSVP updates sent.

**Orchestration Logic**:

- Sequential execution with conditional branching: only reschedulable events proceed to availability checking.
- Error handling: If availability API fails, fallback to declining event.
- Retry strategy: Retry calendar API calls up to 3 times on transient errors.
- Parallelization: Availability checks for multiple events can run in parallel.

**Final Output**:
- Type: `UI_display|calendar_update`
- Description: User sees summary of cleared time block, rescheduled events, and declined events. Calendar is updated accordingly.
- Schema: `"{ \"summary\": { \"cleared_time\": \"2025-11-07T13:00-17:00\", \"rescheduled\": [ { \"subject\": \"Team Sync\", \"new_time\": \"2025-11-10T10:00\" } ], \"declined\": [\"Project Update\"] } }"`

---

### 6. schedule-3

**Prompt**: Land a time for Project Alpha with Chris, Sangya, and Kat for 1 hour in the next 2 weeks. Schedule over 1:1s if needed, work around Kat's schedule. In person with a room.

**Composition Pattern**: hybrid (parallel for data retrieval, sequential for constraint solving and event creation)

**Execution Steps**: 7

#### Step 1: CAN-04 - Natural Language Understanding (Constraint/Intent Extraction) (Tier 1)

**Input**:
- Type: `user_prompt`
- Description: Raw user input text containing scheduling intent and constraints
- Schema: `"{ \"text\": \"Land a time for Project Alpha with Chris, Sangya, and Kat for 1 hour in the next 2 weeks. Schedule over 1:1s if needed, work around Kat's schedule. In person with a room.\" }"`

**Processing**: Extract structured constraints: purpose, attendees, duration, timeframe, override rules, priority attendee, modality, resource requirements.

**Output**:
- Description: Structured representation of scheduling constraints
- Schema: `"{ \"purpose\": \"Project Alpha\", \"attendees\": [\"Chris\", \"Sangya\", \"Kat\"], \"duration\": 60, \"timeframe\": {\"type\": \"relative\", \"value\": \"2 weeks\"}, \"constraints\": {\"override_rules\": [\"1:1s\"], \"priority_attendee\": \"Kat\", \"modality\": \"in-person\", \"resources\": [\"room\"]} }"`

**Flows To**: step_2

#### Step 2: CAN-05 - Attendee/Contact Resolution (Tier 1)

**Input**:
- Type: `previous_step_output`
- Description: Attendee names extracted from NLU step
- Schema: `"{ \"attendees\": [\"Chris\", \"Sangya\", \"Kat\"] }"`

**Processing**: Resolve each name to a unique calendar identity (email) using directory lookup and disambiguation.

**Output**:
- Description: Resolved attendee identities with email addresses
- Schema: `"{ \"attendees\": [\"chris@company.com\", \"sangya@company.com\", \"kat@company.com\"] }"`

**Flows To**: step_3

#### Step 3: CAN-01 - Calendar Events Retrieval (Tier 1)

**Input**:
- Type: `external_data`
- Description: Timeframe and attendee identities for availability analysis
- Schema: `"{ \"startDateTime\": \"2025-11-07T00:00:00\", \"endDateTime\": \"2025-11-21T23:59:59\", \"attendees\": [\"me@company.com\", \"chris@company.com\", \"sangya@company.com\", \"kat@company.com\"] }"`

**Processing**: Retrieve all events for user and attendees within the next 2 weeks to build availability map and identify 1:1 meetings for override.

**Output**:
- Description: Raw calendar events for all participants
- Schema: `"{ \"events\": [ {\"id\": \"evt1\", \"subject\": \"1:1 with Chris\", \"start\": \"2025-11-10T14:00:00\", \"end\": \"2025-11-10T14:30:00\", \"attendees\": [\"me@company.com\", \"chris@company.com\"]}, ... ] }"`

**Flows To**: step_4

#### Step 4: CAN-06 - Availability Checking (Free/Busy) (Tier 2)

**Input**:
- Type: `previous_step_output`
- Description: Calendar events for all attendees
- Schema: `"{ \"events\": [ ... ], \"attendees\": [\"me@company.com\", \"chris@company.com\", \"sangya@company.com\", \"kat@company.com\"] }"`

**Processing**: Compute free/busy slots for all attendees within the timeframe, considering override rules for 1:1 meetings.

**Output**:
- Description: Aggregated availability matrix for all attendees
- Schema: `"{ \"availability\": [ {\"time\": \"2025-11-10T14:00:00\", \"status\": {\"me\": \"busy\", \"chris\": \"busy\", \"sangya\": \"free\", \"kat\": \"free\"}}, ... ] }"`

**Flows To**: step_5

#### Step 5: CAN-12 - Constraint Satisfaction (Tier 2)

**Input**:
- Type: `previous_step_output`
- Description: Availability matrix and scheduling constraints
- Schema: `"{ \"availability\": [...], \"constraints\": {\"duration\": 60, \"priority_attendee\": \"kat@company.com\", \"override_rules\": [\"1:1s\"]} }"`

**Processing**: Apply constraint solver to find optimal time slot satisfying duration, attendee availability, priority attendee preference, and override rules.

**Output**:
- Description: Selected optimal time slot for the meeting
- Schema: `"{ \"start\": \"2025-11-12T15:00:00\", \"end\": \"2025-11-12T16:00:00\" }"`

**Flows To**: step_6

#### Step 6: CAN-19 - Resource Booking (Rooms/Equipment) (Tier 3)

**Input**:
- Type: `previous_step_output`
- Description: Selected time slot and resource requirement
- Schema: `"{ \"start\": \"2025-11-12T15:00:00\", \"end\": \"2025-11-12T16:00:00\", \"resources\": [\"room\"] }"`

**Processing**: Query available rooms for the selected time slot and book one.

**Output**:
- Description: Booked room details
- Schema: `"{ \"room\": {\"name\": \"Conference Room B41-3A\", \"id\": \"room123\"} }"`

**Flows To**: step_7

#### Step 7: CAN-03 - Calendar Event Creation/Update (Tier 1)

**Input**:
- Type: `previous_step_output`
- Description: Final meeting details including attendees, time slot, and room
- Schema: `"{ \"subject\": \"Project Alpha Meeting\", \"start\": \"2025-11-12T15:00:00\", \"end\": \"2025-11-12T16:00:00\", \"attendees\": [\"chris@company.com\", \"sangya@company.com\", \"kat@company.com\"], \"location\": \"Conference Room B41-3A\" }"`

**Processing**: Create the calendar event in the user's calendar and send invitations to attendees.

**Output**:
- Description: Confirmation of event creation with event ID
- Schema: `"{ \"event_id\": \"evt123\", \"status\": \"created\" }"`

**Flows To**: [Final Output]

**Data Flow Summary**:

User prompt → NLU extracts constraints → Attendee resolution → Calendar events retrieval → Availability computation → Constraint solver selects slot → Room booking → Event creation and invitations.

**Orchestration Logic**:

- Sequential execution with dependency chaining
- Error handling: If attendee resolution fails, prompt user for clarification
- Fallback: If no slot found, relax override rules and retry
- Parallelization: Calendar retrieval for multiple attendees can run in parallel
- Conditional: Room booking only if modality = in-person

**Final Output**:
- Type: `calendar_update`
- Description: User receives confirmation of scheduled meeting with details
- Schema: `"{ \"meeting\": { \"subject\": \"Project Alpha Meeting\", \"start\": \"2025-11-12T15:00:00\", \"end\": \"2025-11-12T16:00:00\", \"attendees\": [\"chris@company.com\", \"sangya@company.com\", \"kat@company.com\"], \"location\": \"Conference Room B41-3A\", \"status\": \"confirmed\" } }"`

---

### 7. collaborate-1

**Prompt**: I have a Project Alpha review coming up. Help me set the agenda based on what the team has been working on.

**Composition Pattern**: hybrid (mostly sequential with partial parallelism)

**Execution Steps**: 5

#### Step 1: CAN-04 - Natural Language Understanding (Constraint/Intent Extraction) (Tier 1)

**Input**:
- Type: `user_prompt`
- Description: Raw user input text describing the intent and context
- Schema: `{"text": "string"}`

**Processing**: Use NLU to extract structured intent and context from the user prompt. Identify the meeting purpose (Project Alpha review), intent (create agenda), and relevant entities (project name).

**Output**:
- Description: Structured representation of user intent and context
- Schema: `{"intent": "create_agenda", "context": {"project": "Project Alpha", "meeting_type": "review"}}`

**Flows To**: step_2

#### Step 2: CAN-05 - Attendee/Contact Resolution (Tier 1)

**Input**:
- Type: `previous_step_output + external_data`
- Description: Project context from step 1 and directory data to resolve team members
- Schema: `{"project": "Project Alpha", "directory": "organization directory API"}`

**Processing**: Resolve the 'team' associated with Project Alpha by querying directory or project metadata. Expand group references into individual team members with emails.

**Output**:
- Description: List of resolved team members for Project Alpha
- Schema: `{"team_members": [{"name": "string", "email": "string"}]}`

**Flows To**: step_3

#### Step 3: CAN-01 - Calendar Events Retrieval (Tier 1)

**Input**:
- Type: `previous_step_output + external_data`
- Description: Team member list and project context to retrieve relevant past meetings
- Schema: `{"team_members": ["email"], "project": "Project Alpha"}`

**Processing**: Query calendar API for recent meetings involving these team members and filter by project-related keywords (e.g., 'Project Alpha') to gather context on what the team has been working on.

**Output**:
- Description: List of recent project-related meetings with metadata
- Schema: `{"meetings": [{"id": "string", "subject": "string", "start": "datetime", "end": "datetime", "attendees": ["string"], "notes": "string"}]}`

**Flows To**: step_4

#### Step 4: CAN-08 - Document/Content Retrieval (Tier 2)

**Input**:
- Type: `previous_step_output + external_data`
- Description: Meeting list and project context to retrieve related documents or work items
- Schema: `{"meetings": [{"id": "string", "subject": "string"}], "project": "Project Alpha"}`

**Processing**: Fetch relevant documents, notes, or work items from SharePoint, OneDrive, or project management tools associated with Project Alpha to understand recent progress.

**Output**:
- Description: Collection of documents and summaries related to the project
- Schema: `{"documents": [{"title": "string", "summary": "string", "link": "string"}]}`

**Flows To**: step_5

#### Step 5: CAN-09 - Document Generation/Formatting (Tier 2)

**Input**:
- Type: `previous_step_output`
- Description: Aggregated meeting data and documents to generate an agenda
- Schema: `{"meetings": [{"subject": "string", "notes": "string"}], "documents": [{"summary": "string"}]}`

**Processing**: Synthesize meeting notes and document summaries into a structured agenda. Use NLG and templates to produce a professional agenda document with sections like 'Recent Progress', 'Discussion Points', and 'Next Steps'.

**Output**:
- Description: Formatted agenda document for the upcoming review meeting
- Schema: `{"agenda": {"title": "Project Alpha Review Agenda", "sections": [{"heading": "string", "items": ["string"]}]}}`

**Flows To**: [Final Output]

**Data Flow Summary**:

User prompt → NLU extracts intent and context → Resolve team members → Retrieve recent project meetings → Fetch related documents → Generate structured agenda document.

**Orchestration Logic**:

- Sequential execution: Steps 1 → 2 → 3 → 4 → 5
- Error handling: If team resolution fails, prompt user for clarification
- Fallback: If no documents found, generate agenda from meeting notes only
- Parallelization: Steps 3 and 4 can partially overlap after team resolution

**Final Output**:
- Type: `UI_display`
- Description: A structured agenda displayed to the user, optionally downloadable as a document
- Schema: `{"agenda": {"title": "string", "sections": [{"heading": "string", "items": ["string"]}]}, "download_link": "string"}`

---

### 8. collaborate-2

**Prompt**: I have an executive meeting in 2 hours. Pull together a briefing on the topics we'll be discussing.

**Composition Pattern**: hybrid (sequential core with parallel sub-tasks in content retrieval)

**Execution Steps**: 5

#### Step 1: CAN-04 - Natural Language Understanding (Constraint/Intent Extraction) (Tier 1)

**Input**:
- Type: `user_prompt`
- Description: Raw user input text specifying urgency and intent
- Schema: `{"text": "I have an executive meeting in 2 hours. Pull together a briefing on the topics we'll be discussing."}`

**Processing**: Extract structured intent and constraints: identify meeting type (executive), time reference (in 2 hours), and intent (prepare briefing).

**Output**:
- Description: Structured representation of user intent and constraints
- Schema: `{"intent": "prepare_briefing", "meeting_type": "executive", "timeframe": {"relative": "2 hours", "absolute_start": "2025-11-06T14:00:00Z"}}`

**Flows To**: step_2

#### Step 2: CAN-01 - Calendar Events Retrieval (Tier 1)

**Input**:
- Type: `previous_step_output`
- Description: Meeting type and timeframe from NLU output
- Schema: `{"meeting_type": "executive", "absolute_start": "2025-11-06T14:00:00Z"}`

**Processing**: Query calendar API for events starting within the next 2 hours, filter for executive meeting type using metadata or title keywords.

**Output**:
- Description: Event object for the upcoming executive meeting
- Schema: `{"event_id": "string", "subject": "Executive Strategy Review", "start": "2025-11-06T14:00:00Z", "end": "2025-11-06T15:00:00Z", "attendees": ["vp@company.com", "ceo@company.com"], "bodyPreview": "Agenda: Q4 strategy, budget allocation"}`

**Flows To**: step_3

#### Step 3: CAN-02 - Meeting Classification (Tier 1)

**Input**:
- Type: `previous_step_output`
- Description: Event details retrieved from calendar
- Schema: `{"subject": "Executive Strategy Review", "bodyPreview": "Agenda: Q4 strategy, budget allocation"}`

**Processing**: Classify meeting context and extract key topics from subject and agenda text to guide briefing content.

**Output**:
- Description: Structured classification and topic list
- Schema: `{"meeting_category": "Executive Review", "topics": ["Q4 strategy", "budget allocation"]}`

**Flows To**: step_4

#### Step 4: CAN-08 - Document/Content Retrieval (Tier 2)

**Input**:
- Type: `previous_step_output`
- Description: Topics identified from meeting classification
- Schema: `{"topics": ["Q4 strategy", "budget allocation"]}`

**Processing**: Search enterprise content sources (SharePoint, CRM) for relevant documents, reports, and data related to identified topics.

**Output**:
- Description: Collection of relevant documents and key excerpts
- Schema: `{"documents": [{"title": "Q4 Strategy Plan", "link": "https://sharepoint.company.com/q4-strategy", "summary": "Key objectives and KPIs for Q4"}, {"title": "Budget Allocation Report", "link": "https://sharepoint.company.com/budget-allocation", "summary": "Breakdown of departmental budgets"}]}`

**Flows To**: step_5

#### Step 5: CAN-09 - Document Generation/Formatting (Tier 2)

**Input**:
- Type: `previous_step_output`
- Description: Relevant documents and summaries for briefing
- Schema: `{"documents": [{"title": "Q4 Strategy Plan", "summary": "Key objectives and KPIs for Q4"}, {"title": "Budget Allocation Report", "summary": "Breakdown of departmental budgets"}]}`

**Processing**: Generate a concise executive briefing document summarizing key topics, linking to source documents, and highlighting critical points.

**Output**:
- Description: Formatted briefing document ready for user consumption
- Schema: `{"briefing_title": "Executive Meeting Briefing", "sections": [{"topic": "Q4 Strategy", "summary": "Key objectives and KPIs for Q4", "source_link": "https://sharepoint.company.com/q4-strategy"}, {"topic": "Budget Allocation", "summary": "Breakdown of departmental budgets", "source_link": "https://sharepoint.company.com/budget-allocation"}]}`

**Flows To**: [Final Output]

**Data Flow Summary**:

User prompt → NLU extracts intent and timeframe → Calendar retrieval finds the meeting → Classification identifies topics → Content retrieval gathers supporting documents → Document generation compiles an executive briefing.

**Orchestration Logic**:

- Sequential execution: Steps 1-5 must occur in order.
- Conditional branching: If no meeting found in Step 2, return error or ask user for clarification.
- Error handling: Retry calendar API calls on transient errors; fallback to approximate time search if exact match fails.
- Parallelization: Document retrieval (Step 4) can fetch multiple sources in parallel.
- Timeout handling: If content retrieval exceeds time limit, generate briefing with available data.

**Final Output**:
- Type: `UI_display`
- Description: An executive briefing document summarizing key topics and linking to supporting materials.
- Schema: `{"briefing_title": "Executive Meeting Briefing", "sections": [{"topic": "string", "summary": "string", "source_link": "URL"}], "generated_at": "timestamp"}`

---

### 9. collaborate-3

**Prompt**: I have a customer meeting tomorrow. Give me a dossier on the attendees and recent interactions.

**Composition Pattern**: hybrid (sequential with parallel sub-tasks)

**Execution Steps**: 6

#### Step 1: CAN-04 - Natural Language Understanding (Constraint/Intent Extraction) (Tier 1)

**Input**:
- Type: `user_prompt`
- Description: Raw user input text specifying meeting context and request
- Schema: `{"text": "I have a customer meeting tomorrow. Give me a dossier on the attendees and recent interactions."}`

**Processing**: Extract intent ('generate_dossier'), meeting type ('customer meeting'), and temporal constraint ('tomorrow').

**Output**:
- Description: Structured representation of user intent and constraints
- Schema: `{"intent": "generate_dossier", "meeting_type": "customer", "timeframe": {"date": "2025-11-07"}}`

**Flows To**: step_2

#### Step 2: CAN-01 - Calendar Events Retrieval (Tier 1)

**Input**:
- Type: `previous_step_output`
- Description: Structured constraints from NLU step
- Schema: `{"meeting_type": "customer", "timeframe": {"date": "2025-11-07"}}`

**Processing**: Query calendar API for events matching date and likely customer meeting indicators (attendees with external domains, subject keywords).

**Output**:
- Description: List of candidate events for the specified date
- Schema: `[{"id": "event123", "subject": "Customer Strategy Review", "start": "2025-11-07T14:00:00", "end": "2025-11-07T15:00:00", "attendees": [{"email": "john@acme.com", "name": "John Doe"}, {"email": "sarah@company.com", "name": "Sarah Smith"}]}]`

**Flows To**: step_3

#### Step 3: CAN-02 - Meeting Classification (Tier 1)

**Input**:
- Type: `previous_step_output`
- Description: Candidate events retrieved from calendar
- Schema: `[{"id": "event123", "subject": "Customer Strategy Review", "attendees": [{"email": "john@acme.com"}, {"email": "sarah@company.com"}]}]`

**Processing**: Classify the retrieved event(s) to confirm they are customer meetings by checking attendee domains and subject keywords.

**Output**:
- Description: Filtered and confirmed customer meeting event(s)
- Schema: `[{"id": "event123", "classification": "customer_meeting", "attendees": [{"email": "john@acme.com"}, {"email": "sarah@company.com"}]}]`

**Flows To**: step_4

#### Step 4: CAN-05 - Attendee/Contact Resolution (Tier 1)

**Input**:
- Type: `previous_step_output`
- Description: Confirmed meeting attendees
- Schema: `[{"email": "john@acme.com"}, {"email": "sarah@company.com"}]`

**Processing**: Resolve attendee identities to full profiles using directory and CRM lookups, including roles, company, and relationship context.

**Output**:
- Description: Enriched attendee profiles
- Schema: `[{"email": "john@acme.com", "name": "John Doe", "company": "Acme Corp", "role": "VP of Sales", "internal_external": "external"}, {"email": "sarah@company.com", "name": "Sarah Smith", "company": "Company Inc", "role": "Account Manager", "internal_external": "internal"}]`

**Flows To**: step_5

#### Step 5: CAN-08 - Document/Content Retrieval (Tier 2)

**Input**:
- Type: `previous_step_output`
- Description: Enriched attendee profiles
- Schema: `[{"email": "john@acme.com", "company": "Acme Corp"}]`

**Processing**: Retrieve recent interactions (emails, meetings, CRM notes) related to these attendees from connected systems (Outlook, CRM, SharePoint).

**Output**:
- Description: Collection of recent interactions for each attendee
- Schema: `{"john@acme.com": [{"type": "email", "date": "2025-11-01", "summary": "Follow-up on Q4 proposal"}, {"type": "meeting", "date": "2025-10-28", "summary": "Quarterly business review"}], "sarah@company.com": [{"type": "internal_note", "date": "2025-11-02", "summary": "Prep for customer strategy review"}]}`

**Flows To**: step_6

#### Step 6: CAN-09 - Document Generation/Formatting (Tier 2)

**Input**:
- Type: `previous_step_output`
- Description: Enriched attendee profiles and recent interactions
- Schema: `{"attendees": [{"name": "John Doe", "company": "Acme Corp", "role": "VP of Sales", "recent_interactions": [{"type": "email", "summary": "Follow-up on Q4 proposal"}]}]}`

**Processing**: Generate a well-formatted dossier document summarizing attendee details and recent interactions, using a predefined template.

**Output**:
- Description: Final dossier document (structured JSON or formatted text)
- Schema: `{"title": "Customer Meeting Dossier", "date": "2025-11-07", "attendees": [{"name": "John Doe", "company": "Acme Corp", "role": "VP of Sales", "recent_interactions": ["2025-11-01: Follow-up on Q4 proposal", "2025-10-28: Quarterly business review"]}]}`

**Flows To**: [Final Output]

**Data Flow Summary**:

User prompt → NLU extracts intent and date → Calendar retrieval finds candidate events → Classification confirms customer meeting → Attendee resolution enriches profiles → Content retrieval gathers recent interactions → Document generation compiles dossier.

**Orchestration Logic**:

- Sequential execution: Steps 1-6 must occur in order
- Conditional branching: If no events found in Step 2, return 'No customer meeting found' message
- Error handling: Retry API calls for calendar and directory lookups up to 3 times on transient errors
- Fallback: If content retrieval fails, generate dossier with attendee info only
- Parallelization: Within Step 5, retrieve interactions for multiple attendees in parallel

**Final Output**:
- Type: `UI_display`
- Description: A structured dossier summarizing attendees and recent interactions for the identified customer meeting
- Schema: `{"title": "Customer Meeting Dossier", "meeting_date": "2025-11-07", "attendees": [{"name": "John Doe", "company": "Acme Corp", "role": "VP of Sales", "recent_interactions": ["2025-11-01: Follow-up on Q4 proposal", "2025-10-28: Quarterly business review"]}, {"name": "Sarah Smith", "company": "Company Inc", "role": "Account Manager", "recent_interactions": ["2025-11-02: Prep for customer strategy review"]}]}`

---
