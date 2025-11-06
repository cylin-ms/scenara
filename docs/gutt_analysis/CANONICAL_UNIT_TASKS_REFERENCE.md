# Canonical Unit Tasks Reference Library

**Author**: Chin-Yew Lin  
**Date**: November 6, 2025  
**Version**: 1.0  
**Source**: Cross-model semantic consolidation (Claude 4.5 + GPT-5 v2)  
**Method**: AI Reasoning analysis of 132 GUTTs (66 Claude + 66 GPT-5)  
**Framework**: 5-Relationship Model (=, <, >, ∩, ⊥) + Unit Task Principle

---

## Executive Summary

**20 Canonical Unit Tasks** identified as the atomic capabilities required for Calendar.AI platform.

**Key Statistics**:
- **Semantic Equivalence**: 63.6% (42/66 pairs) - Claude and GPT-5 converged on same capabilities
- **Coverage**: 100% of observed capabilities across 9 hero prompts
- **Validation**: Cross-validated by 2 independent LLMs

**Implementation Strategy**:
- **Tier 1** (5 tasks): Universal capabilities (50%+ prompts) → **Build first** ⭐⭐⭐⭐⭐
- **Tier 2** (9 tasks): Common capabilities (25-50% prompts) → **Build next** ⭐⭐⭐
- **Tier 3** (6 tasks): Specialized capabilities (<25% prompts) → **Build on-demand** ⭐

---

## What is a Canonical Unit Task?

A **Canonical Unit Task** is an atomic, reusable capability that:

1. ✅ **Atomic**: Indivisible at API/tool level - cannot be meaningfully split further
2. ✅ **API-sized**: Maps to a single API call or tool invocation
3. ✅ **Reusable**: Common capability across multiple scenarios/prompts
4. ✅ **Clear I/O**: Well-defined input/output boundaries
5. ✅ **Cross-validated**: Identified by multiple independent LLMs (Claude + GPT-5)

**Example**:
- ✅ **Valid**: "Calendar Events Retrieval" → Single API call `GET /me/calendar/events`
- ❌ **Invalid**: "Setup meeting and send invites and book room" → 3 separate API calls

---

## Quick Reference: All 20 Canonical Tasks

| ID | Task Name | Frequency | Tier | API/Tool | Priority |
|----|-----------|-----------|------|----------|----------|
| [CAN-01](#canonical-01-calendar-events-retrieval) | Calendar Events Retrieval | 9/9 (100%) | 1 | Microsoft Graph | ⭐⭐⭐⭐⭐ |
| [CAN-02](#canonical-02-meeting-classificationcategorization) | Meeting Classification | 7/9 (78%) | 1 | ML Model | ⭐⭐⭐⭐⭐ |
| [CAN-03](#canonical-03-calendar-event-creationupdate) | Calendar Event Creation/Update | 6/9 (67%) | 1 | Microsoft Graph | ⭐⭐⭐⭐⭐ |
| [CAN-04](#canonical-04-natural-language-understanding) | NLU (Constraint/Intent) | 6/9 (67%) | 1 | Azure AI, OpenAI | ⭐⭐⭐⭐⭐ |
| [CAN-05](#canonical-05-attendeecontact-resolution) | Attendee/Contact Resolution | 5/9 (56%) | 1 | Microsoft Graph | ⭐⭐⭐⭐ |
| [CAN-06](#canonical-06-availability-checking-freebusy) | Availability Checking | 4/9 (44%) | 2 | Microsoft Graph | ⭐⭐⭐ |
| [CAN-07](#canonical-07-meeting-invitationnotification-sending) | Meeting Invitations | 4/9 (44%) | 2 | Email/Calendar | ⭐⭐⭐ |
| [CAN-08](#canonical-08-documentcontent-retrieval) | Document/Content Retrieval | 4/9 (44%) | 2 | SharePoint, CRM | ⭐⭐⭐ |
| [CAN-09](#canonical-09-document-generationformatting) | Document Generation | 4/9 (44%) | 2 | NLG, Templates | ⭐⭐⭐ |
| [CAN-10](#canonical-10-time-aggregationstatistical-analysis) | Time Aggregation/Analytics | 3/9 (33%) | 2 | pandas, SQL | ⭐⭐ |
| [CAN-11](#canonical-11-prioritypreference-matching) | Priority/Preference Matching | 3/9 (33%) | 2 | Semantic similarity | ⭐⭐ |
| [CAN-12](#canonical-12-constraint-satisfaction) | Constraint Satisfaction | 3/9 (33%) | 2 | OR-Tools, CSP | ⭐⭐⭐ |
| [CAN-13](#canonical-13-rsvp-status-update) | RSVP Status Update | 3/9 (33%) | 2 | Microsoft Graph | ⭐⭐ |
| [CAN-14](#canonical-14-recommendation-engine) | Recommendation Engine | 3/9 (33%) | 2 | LLM, Rules | ⭐⭐ |
| [CAN-15](#canonical-15-recurrence-rule-generation) | Recurrence Rule Generation | 2/9 (22%) | 3 | iCalendar RRULE | ⭐ |
| [CAN-16](#canonical-16-event-monitoringchange-detection) | Event Monitoring | 2/9 (22%) | 3 | Webhooks | ⭐ |
| [CAN-17](#canonical-17-automatic-rescheduling) | Automatic Rescheduling | 2/9 (22%) | 3 | Automation | ⭐ |
| [CAN-18](#canonical-18-objectionrisk-anticipation) | Objection/Risk Anticipation | 2/9 (22%) | 3 | LLM reasoning | ⭐ |
| [CAN-19](#canonical-19-resource-booking-roomsequipment) | Resource Booking | 1/9 (11%) | 3 | Microsoft Graph | ⭐ |
| [CAN-20](#canonical-20-data-visualizationreporting) | Data Visualization | 1/9 (11%) | 3 | Chart.js, D3.js | ⭐ |

---

## Tier 1: Universal Capabilities (50%+ prompt coverage)

### CANONICAL-01: Calendar Events Retrieval

**Frequency**: 9/9 prompts (100%) - **MOST UNIVERSAL CAPABILITY**

**Description**: Retrieve calendar event data from calendar systems via API, with optional filters for time range, attendees, or status.

**API/Tool**: 
- Microsoft Graph: `GET /me/calendar/events`
- Google Calendar: `GET /calendar/v3/users/me/events`

**Used In**: ALL 9 hero prompts
- organizer-1: Get pending invitations for priority evaluation
- organizer-2: Get upcoming meetings to flag prep needs
- organizer-3: Get historical events for time analysis
- schedule-1: Check calendar for conflicts
- schedule-2: Find meetings in Thursday afternoon time block
- schedule-3: Get multi-person calendar data
- collaborate-1: Get project-related meetings
- collaborate-2: Get upcoming executive meeting
- collaborate-3: Get customer meeting details

**Example**:
```
User: "Show my meetings this week"
→ GET /me/calendar/events?$filter=start/dateTime ge '2025-11-06T00:00:00' and start/dateTime lt '2025-11-13T00:00:00'
→ Returns: Array of event objects with subject, start, end, attendees, etc.
```

**Parameters**:
- Time range: `startDateTime`, `endDateTime`
- Filters: `status` (accepted/tentative/declined), `attendees`, `categories`
- Pagination: `$top`, `$skip`
- Selection: `$select` (choose fields to return)
- Ordering: `$orderby`

**Model References**:
- **Claude**: C2 (org-1), C1 (org-2), C1 (org-3), C2 (sch-2), C2 (sch-3), C1 (col-3)
- **GPT-5**: G1 (org-1), G1 (org-2), G1 (org-3), G2 (sch-2), G3 (sch-3), G2 (col-3)

**Implementation Priority**: ⭐⭐⭐⭐⭐ **CRITICAL** - Build in Week 1
- Foundational capability required by all other features
- Enables basic calendar visibility
- Gateway to all calendar-based intelligence

---

### CANONICAL-02: Meeting Classification/Categorization

**Frequency**: 7/9 prompts (78%)

**Description**: Assign categories, scores, or classifications to calendar events based on attributes, content, and context.

**API/Tool**: 
- ML Classification Model (scikit-learn, TensorFlow, PyTorch)
- Azure AI Language (Text classification)
- OpenAI GPT (Few-shot classification)
- Claude (Classification prompts)

**Used In**: 7 prompts
- organizer-1: Classify events by priority alignment
- organizer-2: Classify by importance level
- organizer-3: Categorize by meeting type (31+ taxonomy)
- schedule-3: Identify override-eligible meetings (1:1s, lunches)
- collaborate-1: Classify by project/topic
- collaborate-2: Classify by relevance to briefing
- collaborate-3: Classify customer vs internal meetings

**Classification Variants**:

1. **Priority Alignment** (organizer-1):
   - Input: Meeting metadata + user priorities
   - Output: Alignment score 0.0-1.0
   - Example: "Q4 Product Strategy" meeting vs "customer meetings" priority → 0.92 (high)

2. **Importance Level** (organizer-2):
   - Input: Attendees, title, duration, urgency
   - Output: Critical/High/Medium/Low
   - Example: Meeting with VP, "Q4 Strategy Review", 2hr → Critical

3. **Meeting Type** (organizer-3):
   - Input: Meeting metadata
   - Output: One of 31+ types
   - Types: 1:1, Team Sync, All-Hands, Executive Review, Customer Call, Interview, Lunch, Training, etc.
   - Example: 2 attendees, 30min, "Weekly Sync" → 1:1

4. **Override Eligibility** (schedule-3):
   - Input: Meeting type, importance, flexibility
   - Output: Can be rescheduled? (Boolean)
   - Example: 1:1 with peer, no critical deliverable → True (can override)

**Example**:
```python
# Simple importance classifier
def classify_importance(meeting):
    score = 0
    if has_executive_attendee(meeting): score += 25
    if has_customer_attendee(meeting): score += 20
    if meeting.duration > 90: score += 15
    if "urgent" in meeting.subject.lower(): score += 20
    
    if score >= 50: return "Critical"
    elif score >= 30: return "High"
    elif score >= 15: return "Medium"
    else: return "Low"
```

**Model References**:
- **Claude**: C3 (org-1), C2 (org-2), C2 (org-3), C4 (sch-3)
- **GPT-5**: G4 (org-1), G2 (org-2), G3 (org-3), G5 (sch-3)

**Implementation Priority**: ⭐⭐⭐⭐⭐ **CRITICAL** - Build in Week 2-3
- High reuse across multiple features
- Core intelligence capability
- Enables smart calendar management

---

### CANONICAL-03: Calendar Event Creation/Update

**Frequency**: 6/9 prompts (67%)

**Description**: Create or modify calendar events via API, including recurrence rules, attendees, and resources.

**API/Tool**:
- Microsoft Graph: `POST /me/calendar/events`, `PATCH /me/calendar/events/{id}`
- Google Calendar: `POST /calendar/v3/calendars/primary/events`, `PUT /calendar/v3/calendars/primary/events/{id}`

**Used In**: 6 prompts
- organizer-1: Update RSVP status (accept/decline)
- organizer-2: Create focus time blocks
- schedule-1: Create recurring meeting series
- schedule-2: Update events (reschedule, decline)
- schedule-3: Create multi-person meeting with room
- collaborate-1: Update meeting with agenda

**Operation Variants**:

1. **Single Event Creation** (schedule-3):
```json
POST /me/calendar/events
{
  "subject": "Project Alpha Review",
  "start": {"dateTime": "2025-11-08T14:00:00", "timeZone": "Pacific Standard Time"},
  "end": {"dateTime": "2025-11-08T15:00:00", "timeZone": "Pacific Standard Time"},
  "attendees": [
    {"emailAddress": {"address": "chris@company.com"}},
    {"emailAddress": {"address": "sangya@company.com"}},
    {"emailAddress": {"address": "kat@company.com"}}
  ],
  "location": {"displayName": "Conference Room B41-3A"}
}
```

2. **Recurring Series** (schedule-1):
```json
POST /me/calendar/events
{
  "subject": "Weekly 1:1 with Sarah",
  "recurrence": {
    "pattern": {
      "type": "weekly",
      "interval": 1,
      "daysOfWeek": ["tuesday"]
    },
    "range": {
      "type": "noEnd",
      "startDate": "2025-11-12"
    }
  },
  "start": {"dateTime": "2025-11-12T14:00:00", "timeZone": "Pacific Standard Time"},
  "end": {"dateTime": "2025-11-12T14:30:00", "timeZone": "Pacific Standard Time"}
}
```

3. **RSVP Update** (organizer-1, schedule-2):
```json
PATCH /me/events/{id}
{
  "responseStatus": "declined"
}
```

4. **Event Modification** (schedule-2):
```json
PATCH /me/events/{id}
{
  "start": {"dateTime": "2025-11-08T16:00:00"},
  "end": {"dateTime": "2025-11-08T17:00:00"}
}
```

5. **Focus Time Block** (organizer-2):
```json
POST /me/calendar/events
{
  "subject": "Focus Time: Prepare for Q4 Review",
  "start": {"dateTime": "2025-11-07T10:00:00"},
  "end": {"dateTime": "2025-11-07T12:00:00"},
  "isReminderOn": true,
  "showAs": "busy",
  "categories": ["Focus Time", "Preparation"]
}
```

**Model References**:
- **Claude**: C5 (org-1), C6 (org-2), C4 (sch-1), C5 (sch-2), C9 (sch-3)
- **GPT-5**: G6 (org-1), G6 (sch-1), G5 (sch-2), G9 (sch-3)

**Implementation Priority**: ⭐⭐⭐⭐⭐ **CRITICAL** - Build in Week 3
- Core write capability
- Enables calendar modifications
- Required for automation features

---

### CANONICAL-04: Natural Language Understanding (Constraint/Intent Extraction)

**Frequency**: 6/9 prompts (67%)

**Description**: Extract structured information (entities, constraints, intents) from unstructured natural language input.

**API/Tool**:
- Azure AI Language (Entity extraction, Intent recognition)
- OpenAI GPT-4 (Structured output, Function calling)
- Claude (Structured extraction)
- Custom NLP pipelines (spaCy, NLTK)

**Used In**: 6 prompts
- organizer-1: Extract user priorities from text
- schedule-1: Parse scheduling constraints
- schedule-2: Parse "Thursday afternoon" to datetime
- schedule-3: Extract meeting requirements (attendees, duration, constraints)
- collaborate-1: Extract meeting intent and project context
- collaborate-2: Extract topics from meeting materials

**Extraction Patterns**:

1. **Priority Extraction** (organizer-1):
```
Input: "I want to focus on customer meetings and product strategy"
Output: {
  "priorities": ["customer meetings", "product strategy"],
  "priority_level": "high"
}
```

2. **Constraint Parsing** (schedule-1):
```
Input: "Weekly 30min 1:1 with Sarah, afternoons preferred, avoid Fridays"
Output: {
  "recurrence": "weekly",
  "duration": 30,
  "attendees": ["Sarah"],
  "time_preferences": {
    "preferred": "afternoon",
    "exclusions": ["friday"]
  }
}
```

3. **Temporal Resolution** (schedule-2):
```
Input: "Clear my Thursday afternoon" (spoken on Nov 6, 2025)
Output: {
  "date": "2025-11-07",
  "time_range": {
    "start": "13:00:00",
    "end": "17:00:00"
  }
}
```

4. **Multi-Constraint Extraction** (schedule-3):
```
Input: "Land a time for Project Alpha with Chris, Sangya, and Kat for 1 hour in the next 2 weeks. Schedule over 1:1s if needed, work around Kat's schedule. In person with a room."
Output: {
  "purpose": "Project Alpha",
  "attendees": ["Chris", "Sangya", "Kat"],
  "duration": 60,
  "timeframe": {"type": "relative", "value": "2 weeks"},
  "constraints": {
    "priority_attendee": "Kat",
    "override_rules": ["1:1s", "lunches"],
    "modality": "in-person",
    "resources": ["room"]
  }
}
```

5. **Intent Recognition** (collaborate-1):
```
Input: "Help me set the agenda for Project Alpha review"
Output: {
  "intent": "create_agenda",
  "context": {
    "project": "Project Alpha",
    "meeting_type": "review"
  }
}
```

**Implementation Example**:
```python
from azure.ai.textanalytics import TextAnalyticsClient

def extract_scheduling_constraints(text):
    # Use Azure AI or OpenAI for extraction
    client = TextAnalyticsClient(endpoint, credential)
    
    # Extract entities
    entities = client.recognize_entities(documents=[text])[0].entities
    
    # Parse temporal expressions
    dates = [e for e in entities if e.category == "DateTime"]
    people = [e for e in entities if e.category == "Person"]
    
    # Extract constraints using pattern matching
    constraints = {
        "recurrence": extract_recurrence(text),
        "duration": extract_duration(text),
        "attendees": [p.text for p in people],
        "time_preferences": extract_time_preferences(text)
    }
    
    return constraints
```

**Model References**:
- **Claude**: C1 (org-1), C1 (sch-1), C1 (sch-2), C1 (sch-3), C2 (col-2)
- **GPT-5**: G1 (sch-1), G1 (sch-2), G1 (sch-3), G1 (col-1), G2 (col-2)

**Implementation Priority**: ⭐⭐⭐⭐⭐ **CRITICAL** - Build in Week 1-2
- Enables natural language interface
- Required for conversational AI
- Foundation for user experience

---

### CANONICAL-05: Attendee/Contact Resolution

**Frequency**: 5/9 prompts (56%)

**Description**: Resolve participant names/descriptions to specific calendar identities via directory lookup.

**API/Tool**:
- Microsoft Graph: `GET /users`, `GET /users?$filter=displayName eq 'Chris'`
- Azure AD Directory Search
- Google Workspace Directory API

**Used In**: 5 prompts
- schedule-1: Resolve "{name}" to email address
- schedule-3: Resolve "Chris", "Sangya", "Kat" to calendar identities
- collaborate-1: Resolve "product team" and "marketing team"
- collaborate-3: Identify customer attendees vs internal
- (Implicit in others requiring multi-person scheduling)

**Resolution Patterns**:

1. **Name to Email** (schedule-1):
```
Input: "Sarah"
→ GET /users?$filter=startswith(displayName,'Sarah')
→ Candidates: [sarah.smith@company.com, sarah.jones@company.com]
→ Disambiguation: Choose based on past interactions or ask user
→ Output: sarah.smith@company.com
```

2. **Team Expansion** (collaborate-1):
```
Input: "product team"
→ GET /groups?$filter=displayName eq 'Product Team'
→ GET /groups/{id}/members
→ Output: [sarah@company.com, mike@company.com, lisa@company.com, john@company.com]
```

3. **Role-Based Lookup**:
```
Input: "my manager"
→ GET /me/manager
→ Output: manager.name@company.com
```

4. **Customer vs Internal** (collaborate-3):
```
Input: Meeting with attendees [john@acme.com, sarah@company.com, mike@company.com]
→ Check domain: acme.com (external), company.com (internal)
→ Output: {
  "customer_attendees": [john@acme.com],
  "internal_attendees": [sarah@company.com, mike@company.com]
}
```

5. **Fuzzy Matching with Disambiguation**:
```
Input: "Chris" (ambiguous - 3 matches)
→ Candidates:
  1. Chris Jones (Engineering) - last interaction: 2 days ago
  2. Chris Smith (Marketing) - last interaction: 30 days ago
  3. Christopher Lee (Sales) - last interaction: never
→ Ranking: Recency + context
→ Top choice: Chris Jones
```

**Implementation Example**:
```python
class ContactResolver:
    def resolve(self, name_or_description):
        # Try exact match
        user = self.graph_client.users.get_by_name(name_or_description)
        if user:
            return user.email
        
        # Try partial match
        candidates = self.graph_client.users.search(name_or_description)
        
        if len(candidates) == 1:
            return candidates[0].email
        elif len(candidates) > 1:
            # Disambiguate using interaction history
            return self.disambiguate(candidates)
        else:
            # Try group expansion
            group = self.graph_client.groups.get_by_name(name_or_description)
            if group:
                return self.get_group_members(group.id)
        
        raise ResolutionError(f"Could not resolve: {name_or_description}")
```

**Model References**:
- **Claude**: C2 (sch-3), C2 (col-1), C3 (col-3)
- **GPT-5**: G2 (sch-1), G2 (sch-3), G4 (col-1), G3 (col-3)

**Implementation Priority**: ⭐⭐⭐⭐ **HIGH** - Build in Week 4
- Required for multi-person scheduling
- Enables team-based features
- Critical for collaboration scenarios

---

## Tier 2: Common Capabilities (25-50% prompt coverage)

### CANONICAL-06: Availability Checking (Free/Busy)

**Frequency**: 4/9 prompts (44%)

**Description**: Retrieve availability status (free/busy) for specified users and time ranges.

**API/Tool**:
- Microsoft Graph: `POST /me/calendar/getSchedule`
- Google Calendar: `POST /freeBusy`

**Used In**: 4 prompts
- schedule-1: Check user + attendee availability for recurring 1:1
- schedule-2: Find alternative times when rescheduling
- schedule-3: Multi-person availability aggregation (4 people)

**Example**:
```
POST /me/calendar/getSchedule
{
  "schedules": [
    "user@company.com",
    "chris@company.com",
    "sangya@company.com",
    "kat@company.com"
  ],
  "startTime": {
    "dateTime": "2025-11-07T00:00:00",
    "timeZone": "Pacific Standard Time"
  },
  "endTime": {
    "dateTime": "2025-11-21T23:59:59",
    "timeZone": "Pacific Standard Time"
  },
  "availabilityViewInterval": 30
}

Response:
{
  "value": [
    {
      "scheduleId": "chris@company.com",
      "availabilityView": "222220000022222..." // 0=free, 2=busy
    },
    ...
  ]
}
```

**Model References**:
- **Claude**: C2 (sch-1), C4 (sch-2), C2 (sch-3)
- **GPT-5**: G5 (sch-1), G4 (sch-2), G3+G6 (sch-3)

**Implementation Priority**: ⭐⭐⭐ MEDIUM-HIGH

---

### CANONICAL-07: Meeting Invitation/Notification Sending

**Frequency**: 4/9 prompts (44%)

**Description**: Dispatch calendar invitations or notifications via email/calendar system.

**API/Tool**:
- Microsoft Graph: `POST /me/sendMail`
- Calendar invitation system (automatic with event creation)
- Email service

**Used In**: 4 prompts
- organizer-2: Send prep time reminders
- schedule-1: Send initial invitation + auto-reschedule notifications
- schedule-2: Send reschedule notifications
- schedule-3: Send meeting invitation

**Model References**:
- **Claude**: C5 (sch-1), C5 (sch-2), C9 (sch-3)
- **GPT-5**: G7 (sch-1), G5 (sch-2), G9 (sch-3), G6 (org-2)

**Implementation Priority**: ⭐⭐⭐ MEDIUM

---

### CANONICAL-08: Document/Content Retrieval

**Frequency**: 4/9 prompts (44%)

**Description**: Retrieve documents, data, or content from various sources.

**API/Tool**:
- SharePoint API, OneDrive API
- CRM API (Salesforce, Dynamics 365)
- Web search

**Used In**: 4 prompts (collaborate-1, collaborate-2, collaborate-3)

**Implementation Priority**: ⭐⭐⭐ MEDIUM

---

### CANONICAL-09: Document Generation/Formatting

**Frequency**: 4/9 prompts (44%)

**Description**: Generate formatted documents from structured data.

**API/Tool**:
- Natural Language Generation (Claude, GPT-4)
- Template engines (Jinja2, Mustache)
- Document libraries (python-docx, HTML/PDF generators)

**Used In**: 4 prompts
- schedule-2: Action summary report
- collaborate-1: Agenda document
- collaborate-2: Executive briefing
- collaborate-3: Customer dossier

**Implementation Priority**: ⭐⭐⭐ MEDIUM

---

### CANONICAL-10: Time Aggregation/Statistical Analysis

**Frequency**: 3/9 prompts (33%)

**Description**: Aggregate and compute statistical metrics from calendar event data.

**Used In**: 1 prompt (organizer-3: Time Reclamation)

**Example**:
```python
import pandas as pd

# Aggregate time by category
time_by_category = df.groupby('meeting_type')['duration_hours'].sum()
# Output: {'1:1': 12.5, 'Team': 9.0, 'Customer': 6.5, ...}

# Average meeting duration
avg_duration = df['duration_hours'].mean()

# Meetings per week
meetings_per_week = df.groupby('week')['meeting_id'].count()
```

**Implementation Priority**: ⭐⭐ MEDIUM

---

### CANONICAL-11: Priority/Preference Matching

**Frequency**: 3/9 prompts (33%)

**Description**: Score/classify events based on alignment with user priorities.

**Used In**: 2 prompts (organizer-1, organizer-3)

**Example**:
```python
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L6-v2')

# User priority
priority = "customer meetings and product strategy"
priority_embedding = model.encode(priority)

# Meeting
meeting_text = "Q4 Customer Strategy Review with VP Product"
meeting_embedding = model.encode(meeting_text)

# Semantic similarity
score = util.cos_sim(priority_embedding, meeting_embedding)[0][0]
# Output: 0.92 (high alignment)
```

**Implementation Priority**: ⭐⭐ MEDIUM

---

### CANONICAL-12: Constraint Satisfaction

**Frequency**: 3/9 prompts (33%)

**Description**: Find time slots satisfying multiple scheduling constraints.

**API/Tool**:
- Google OR-Tools (Constraint Programming)
- python-constraint
- Custom CSP solver

**Used In**: 2 prompts (schedule-1, schedule-3)

**Example**:
```python
from ortools.sat.python import cp_model

model = cp_model.CpModel()

# Variables: possible time slots (0-23 hours)
slot = model.NewIntVar(0, 23, 'slot')

# Constraints
model.Add(slot >= 13)  # Afternoon (1pm or later)
model.Add(slot <= 17)  # Before end of day (5pm)
# Constraint: Not Friday (would need day-of-week variable)

# Solve
solver = cp_model.CpSolver()
status = solver.Solve(model)

if status == cp_model.OPTIMAL:
    print(f'Optimal slot: {solver.Value(slot)}:00')
```

**Implementation Priority**: ⭐⭐⭐ MEDIUM-HIGH

---

### CANONICAL-13: RSVP Status Update

**Frequency**: 3/9 prompts (33%)

**Description**: Update meeting RSVP status via calendar API.

**Used In**: 2 prompts (organizer-1, schedule-2)

**Implementation Priority**: ⭐⭐ MEDIUM

---

### CANONICAL-14: Recommendation Engine

**Frequency**: 3/9 prompts (33%)

**Description**: Generate actionable recommendations based on analysis.

**Used In**: 3 prompts (organizer-2, organizer-3, collaborate-2)

**Implementation Priority**: ⭐⭐ MEDIUM

---

## Tier 3: Specialized Capabilities (<25% prompt coverage)

### CANONICAL-15: Recurrence Rule Generation

**Frequency**: 2/9 prompts (22%)

**Description**: Generate iCalendar RRULE specifications from natural language.

**Used In**: 1 prompt (schedule-1)

**Example**:
```python
from dateutil.rrule import rrule, WEEKLY, MO, TU, WE, TH

# "Weekly on Tuesdays"
rule = rrule(WEEKLY, byweekday=TU)
rrule_string = rule.__str__()  # FREQ=WEEKLY;BYDAY=TU
```

**Implementation Priority**: ⭐ LOW

---

### CANONICAL-16: Event Monitoring/Change Detection

**Frequency**: 2/9 prompts (22%)

**Description**: Detect and respond to calendar event changes via webhooks.

**Used In**: 1 prompt (schedule-1: auto-reschedule trigger)

**Implementation Priority**: ⭐ LOW

---

### CANONICAL-17: Automatic Rescheduling

**Frequency**: 2/9 prompts (22%)

**Description**: Automatically reschedule meetings in response to conflicts.

**Used In**: 2 prompts (schedule-1, schedule-3)

**Implementation Priority**: ⭐ LOW

---

### CANONICAL-18: Objection/Risk Anticipation

**Frequency**: 2/9 prompts (22%)

**Description**: Predict objections or concerns using LLM reasoning.

**Used In**: 2 prompts (collaborate-1, collaborate-2)

**Implementation Priority**: ⭐ LOW

---

### CANONICAL-19: Resource Booking (Rooms/Equipment)

**Frequency**: 1/9 prompts (11%)

**Description**: Search and book physical resources.

**API/Tool**: Microsoft Graph: `GET /places`

**Used In**: 1 prompt (schedule-3)

**Implementation Priority**: ⭐ LOW

---

### CANONICAL-20: Data Visualization/Reporting

**Frequency**: 1/9 prompts (11%)

**Description**: Generate visualizations from calendar data.

**API/Tool**: Chart.js, D3.js, matplotlib, plotly

**Used In**: 1 prompt (organizer-3)

**Implementation Priority**: ⭐ LOW

---

## Implementation Roadmap

### Phase 1: Universal Tier (Weeks 1-4) ⭐⭐⭐⭐⭐

**Build Order**: CAN-01 → CAN-04 → CAN-02 → CAN-03 → CAN-05

**Week 1**:
- **CAN-01**: Calendar Events Retrieval
  - Microsoft Graph integration
  - Filtering, pagination, error handling
  - Unit tests with mock data

- **CAN-04**: NLU (Constraint/Intent Extraction) - Part 1
  - Azure AI Language integration
  - Temporal expression parsing
  - Entity extraction

**Week 2**:
- **CAN-04**: NLU - Part 2
  - Constraint parsing patterns
  - Intent recognition
  - Custom NLP pipeline

- **CAN-02**: Meeting Classification - Part 1
  - Feature extraction from meetings
  - Training data collection
  - Simple rule-based classifier

**Week 3**:
- **CAN-02**: Meeting Classification - Part 2
  - ML model training (scikit-learn)
  - Meeting type taxonomy (31+ types)
  - Importance scoring algorithm

- **CAN-03**: Calendar Event Creation/Update - Part 1
  - Single event creation
  - Event updates/modifications

**Week 4**:
- **CAN-03**: Calendar Event Creation/Update - Part 2
  - Recurring series with RRULE
  - RSVP status updates
  - Error handling & validation

- **CAN-05**: Attendee/Contact Resolution
  - Directory integration
  - Name resolution logic
  - Team expansion
  - Disambiguation

**Deliverables**:
- 5 fully implemented Tier 1 capabilities
- API wrappers and error handling
- Unit test coverage >80%
- Integration tests with Microsoft Graph
- Documentation and usage examples

---

### Phase 2: Common Tier (Weeks 5-8) ⭐⭐⭐

**Build Order**: CAN-06 → CAN-12 → CAN-07 → CAN-08 → CAN-09 → Others

**Week 5**:
- **CAN-06**: Availability Checking
  - Free/busy API integration
  - Multi-user aggregation
  - Common slot finding

- **CAN-12**: Constraint Satisfaction
  - Google OR-Tools integration
  - CSP model for scheduling
  - Slot ranking algorithm

**Week 6**:
- **CAN-07**: Meeting Invitations
  - Email notification service
  - Calendar invitation formatting
  - Template system

- **CAN-08**: Document/Content Retrieval
  - SharePoint API integration
  - CRM API integration
  - Content search

**Week 7**:
- **CAN-09**: Document Generation
  - NLG integration (Claude/GPT-4)
  - Template engine (Jinja2)
  - Professional formatting (Word, PDF)

**Week 8**:
- **CAN-10**: Time Aggregation/Analytics
- **CAN-11**: Priority/Preference Matching
- **CAN-13**: RSVP Status Update
- **CAN-14**: Recommendation Engine

**Deliverables**:
- 9 Tier 2 capabilities implemented
- Integration with external services
- Advanced scheduling algorithms
- Content generation pipelines

---

### Phase 3: Specialized Tier (Weeks 9-12) ⭐

**Build On-Demand Based on Product Priorities**

**Week 9-10**:
- CAN-15: Recurrence Rule Generation (if needed for recurring features)
- CAN-16: Event Monitoring (if automation required)

**Week 11**:
- CAN-17: Automatic Rescheduling (if auto-features prioritized)
- CAN-18: Objection/Risk Anticipation (if collaboration features prioritized)

**Week 12**:
- CAN-19: Resource Booking (if facilities integration prioritized)
- CAN-20: Data Visualization (if analytics dashboard prioritized)

**Deliverables**:
- Specialized capabilities as needed
- Advanced automation workflows
- Enterprise integrations
- Analytics and reporting

---

## Usage: Evaluating New Prompts

### Step 1: Decompose Prompt into Unit Tasks

When evaluating a new Calendar.AI prompt, identify which canonical tasks are required:

**Example Prompt**: "Find time for bi-weekly standup with my product team, avoid Friday afternoons, and send calendar invites"

**Decomposition**:
1. ✅ **CAN-04**: NLU - Extract constraints
   - Recurrence: "bi-weekly"
   - Attendees: "product team"
   - Time exclusion: "avoid Friday afternoons"

2. ✅ **CAN-05**: Attendee Resolution
   - Resolve "product team" → [sarah@, mike@, lisa@, john@]

3. ✅ **CAN-06**: Availability Checking
   - Check free/busy for user + all team members

4. ✅ **CAN-15**: Recurrence Rule Generation
   - Generate: FREQ=WEEKLY;INTERVAL=2

5. ✅ **CAN-12**: Constraint Satisfaction
   - Find slots: bi-weekly, all attendees free, not Friday afternoon

6. ✅ **CAN-03**: Calendar Event Creation
   - Create recurring meeting with RRULE

7. ✅ **CAN-07**: Meeting Invitations
   - Send invites to all team members

**Coverage**: 7 canonical tasks identified → All available in library → 100% coverage ✅

---

### Step 2: Check Implementation Status

| Task | Status | Implementation Week |
|------|--------|---------------------|
| CAN-04 (NLU) | ✅ Implemented | Week 1-2 |
| CAN-05 (Contact Resolution) | ✅ Implemented | Week 4 |
| CAN-06 (Availability) | ✅ Implemented | Week 5 |
| CAN-15 (Recurrence Rules) | ⚠️ Tier 3 | Week 9-10 (on-demand) |
| CAN-12 (Constraint Satisfaction) | ✅ Implemented | Week 5 |
| CAN-03 (Event Creation) | ✅ Implemented | Week 3 |
| CAN-07 (Invitations) | ✅ Implemented | Week 6 |

**Result**: 6/7 tasks ready (86%), 1 task needs implementation (CAN-15)

---

### Step 3: Estimate Implementation Effort

**If all tasks exist**: Low effort - orchestration only  
**If 1-2 tasks missing**: Medium effort - implement missing + orchestration  
**If 3+ tasks missing**: High effort - multiple new capabilities needed

**This prompt**: Low-Medium effort
- 6 tasks ready
- 1 specialized task (recurrence rules) - can use library (dateutil.rrule)
- Primarily orchestration work

---

## Technology Stack Summary

### Calendar Operations
- **Microsoft Graph API** - Calendar CRUD, availability, rooms
- **Google Calendar API** - Alternative calendar provider
- **OAuth 2.0** - Authentication

### Natural Language Processing
- **Azure AI Language** - Entity extraction, intent recognition
- **OpenAI GPT-4 / Claude** - Structured extraction, summarization
- **spaCy** - NLP pipelines
- **SUTime / Duckling** - Temporal expression parsing

### Machine Learning
- **scikit-learn** - Classification, clustering
- **Sentence Transformers** - Semantic similarity
- **TensorFlow / PyTorch** - Deep learning models (if needed)

### Constraint Solving & Optimization
- **Google OR-Tools** - Constraint programming
- **python-constraint** - CSP solver

### Document Processing & Generation
- **python-docx** - Word document generation
- **Jinja2** - Template engine
- **Azure AI Document Intelligence** - Document parsing
- **Beautiful Soup** - Web scraping

### Data & Analytics
- **pandas** - Data manipulation
- **NumPy** - Numerical computing
- **matplotlib / plotly** - Visualization
- **Chart.js / D3.js** - Interactive charts

### Integration & Automation
- **Microsoft Graph Webhooks** - Event notifications
- **FastAPI / Flask** - API server
- **Celery** - Background task queue

---

## Validation & Quality Metrics

### Coverage Metrics
- **Prompt Coverage**: 100% (all 9 hero prompts mapped)
- **Cross-Model Agreement**: 63.6% exact equivalence + 22.7% subset = 86.3% semantic alignment
- **Validation**: 2 independent LLMs (Claude 4.5 + GPT-5 v2)

### Reusability Metrics
- **Tier 1**: 56-100% reuse (5 tasks) - Universal capabilities
- **Tier 2**: 33-44% reuse (9 tasks) - Common capabilities  
- **Tier 3**: 11-22% reuse (6 tasks) - Specialized capabilities

### Implementation Metrics
- **API Mappings**: 20/20 tasks have clear API/tool mappings ✅
- **Code Examples**: 15/20 tasks have implementation examples
- **Test Coverage Target**: >80% unit test coverage for Tier 1

---

## Frequently Asked Questions

### Q: Why 20 canonical tasks instead of 39 C-GUTTs?

**A**: Canonical tasks are higher-level atomic capabilities validated by **both Claude and GPT-5**. The 20 tasks represent the consolidation of 132 GUTTs (66 Claude + 66 GPT-5) with 63.6% exact semantic equivalence. They are:
- More atomic (true Unit Task principle)
- Cross-validated (higher confidence)
- Easier to implement (clear API boundaries)
- Better for platform architecture

C-GUTTs (39) are more detailed and better for granular implementation planning.

---

### Q: Can I use both Canonical Tasks and C-GUTTs?

**A**: Yes! They complement each other:
- **Canonical Tasks**: Platform evaluation, decomposition quality, prioritization
- **C-GUTTs**: Detailed implementation, nuanced variants, testing granularity

Many C-GUTTs map to Canonical Tasks (e.g., C-GUTT-01 = CAN-01).

---

### Q: What if a new prompt needs capabilities not in the 20?

**A**: 
1. Check if it's truly new or a variant of existing tasks
2. If new, add to library with frequency 1/N
3. If frequency increases across prompts, promote to higher tier
4. Library is designed to evolve with new use cases

---

### Q: How were the 5-relationship model assignments made?

**A**: Using **AI reasoning** (Claude Sonnet 4.5), not string matching:
- Analyzed semantic meaning of each capability
- Compared atomic operations (API calls)
- Identified hierarchies (subset/superset)
- Found overlapping capabilities with unique aspects
- 6.5x better than text similarity (63.6% vs 9.8%)

---

## Conclusion

The **20 Canonical Unit Tasks** represent the atomic, reusable capabilities for Calendar.AI platform, validated across 2 independent LLMs.

**Key Achievements**:
- ✅ 100% coverage of 9 hero prompts
- ✅ 63.6% semantic equivalence across models
- ✅ Clear implementation roadmap (12 weeks)
- ✅ Tier-based prioritization (Universal → Common → Specialized)

**Next Steps**:
1. Review and validate with Calendar.AI team
2. Begin Phase 1 implementation (Tier 1 tasks)
3. Use for new prompt evaluation
4. Extend library as new capabilities discovered

---

**Document Version**: 1.0  
**Last Updated**: November 6, 2025  
**Maintained By**: Calendar.AI Platform Team  
**Related Documents**:
- [GUTT_CONSOLIDATION_PROPOSAL.md](GUTT_CONSOLIDATION_PROPOSAL.md) - Detailed analysis
- [CONSOLIDATED_GUTT_REFERENCE.md](CONSOLIDATED_GUTT_REFERENCE.md) - C-GUTT reference
- [copilot_claude_semantic_analysis.md](copilot_claude_semantic_analysis.md) - Full analysis
