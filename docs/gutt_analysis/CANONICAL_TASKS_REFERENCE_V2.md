# Canonical Tasks Reference Library v2.0

**Author**: Chin-Yew Lin  
**Date**: November 7, 2025  
**Version**: 2.0  
**Source**: Human-validated gold standard from v2 hero prompts evaluation  
**Framework**: 25 Canonical Tasks (renumbered 1-25)  
**Validation**: Human evaluation of 9 v2 hero prompts (November 7, 2025)

---

## Executive Summary

**25 Canonical Tasks** identified as the complete set of atomic capabilities required for Calendar.AI platform.
- **Task IDs**: CAN-01 through CAN-25
- **New in v2.0**: CAN-25 (Event Annotation/Flagging) - added based on human evaluation feedback

**Key Changes from v1.0**:
- ✅ **Renumbered**: All tasks renumbered sequentially 1-25 (no gaps)
- ✅ **New Task Added**: CAN-25 for conditional event annotation/flagging
- ✅ **Validated**: Based on human evaluation of v2 hero prompts gold standard
- ✅ **Updated Tiers**: Redistributed based on actual usage patterns

**Implementation Strategy**:
- **Tier 1** (6 tasks): Universal capabilities (50%+ prompts) → **Build first** ⭐⭐⭐⭐⭐
- **Tier 2** (9 tasks): Common capabilities (25-50% prompts) → **Build next** ⭐⭐⭐
- **Tier 3** (10 tasks): Specialized capabilities (<25% prompts) → **Build on-demand** ⭐

---

## What is a Canonical Task?

A **Canonical Task** is an atomic, reusable capability that:

1. ✅ **Atomic**: Indivisible at API/tool level - cannot be meaningfully split further
2. ✅ **API-sized**: Maps to a single API call or tool invocation
3. ✅ **Reusable**: Common capability across multiple scenarios/prompts
4. ✅ **Clear I/O**: Well-defined input/output boundaries
5. ✅ **Validated**: Confirmed through human evaluation of real use cases

**Example**:
- ✅ **Valid**: "Calendar Events Retrieval" → Single API call `GET /me/calendar/events`
- ❌ **Invalid**: "Setup meeting and send invites and book room" → 3 separate API calls

---

## Quick Reference: All 25 Canonical Tasks

| ID | Task Name | Tier | Priority |
|----|-----------|------|----------|
| [CAN-01](#can-01-calendar-events-retrieval) | Calendar Events Retrieval | 1 | ⭐⭐⭐⭐⭐ |
| [CAN-02](#can-02-meeting-type-classification) | Meeting Type Classification | 1 | ⭐⭐⭐⭐⭐ |
| [CAN-03](#can-03-meeting-importance-assessment) | Meeting Importance Assessment | 1 | ⭐⭐⭐⭐⭐ |
| [CAN-04](#can-04-natural-language-understanding) | Natural Language Understanding | 1 | ⭐⭐⭐⭐⭐ |
| [CAN-05](#can-05-attendeecontact-resolution) | Attendee/Contact Resolution | 1 | ⭐⭐⭐⭐⭐ |
| [CAN-06](#can-06-availability-checking) | Availability Checking (Free/Busy) | 2 | ⭐⭐⭐⭐ |
| [CAN-07](#can-07-meeting-metadata-extraction) | Meeting Metadata Extraction | 2 | ⭐⭐⭐⭐ |
| [CAN-08](#can-08-documentcontent-retrieval) | Document/Content Retrieval | 2 | ⭐⭐⭐ |
| [CAN-09](#can-09-document-generation) | Document Generation/Formatting | 2 | ⭐⭐⭐ |
| [CAN-10](#can-10-time-aggregation-analysis) | Time Aggregation/Statistical Analysis | 2 | ⭐⭐⭐ |
| [CAN-11](#can-11-prioritypreference-matching) | Priority/Preference Matching | 2 | ⭐⭐⭐ |
| [CAN-12](#can-12-constraint-satisfaction) | Constraint Satisfaction | 2 | ⭐⭐⭐ |
| [CAN-13](#can-13-rsvp-status-update) | RSVP Status Update | 2 | ⭐⭐⭐ |
| [CAN-14](#can-14-recommendation-engine) | Recommendation Engine | 2 | ⭐⭐⭐ |
| [CAN-15](#can-15-recurrence-rule-generation) | Recurrence Rule Generation | 3 | ⭐⭐ |
| [CAN-16](#can-16-event-monitoringchange-detection) | Event Monitoring/Change Detection | 3 | ⭐⭐ |
| [CAN-17](#can-17-automatic-rescheduling) | Automatic Rescheduling | 3 | ⭐⭐ |
| [CAN-18](#can-18-objectionrisk-anticipation) | Objection/Risk Anticipation | 3 | ⭐⭐ |
| [CAN-19](#can-19-resource-booking) | Resource Booking (Rooms/Equipment) | 3 | ⭐⭐ |
| [CAN-20](#can-20-data-visualizationreporting) | Data Visualization/Reporting | 3 | ⭐⭐ |
| [CAN-21](#can-21-focus-time-analysis) | Focus Time/Preparation Time Analysis | 3 | ⭐⭐ |
| [CAN-22](#can-22-research-intelligence-gathering) | Research/Intelligence Gathering | 3 | ⭐⭐ |
| [CAN-23](#can-23-agenda-generation) | Agenda Generation/Structuring | 3 | ⭐⭐ |
| [CAN-24](#can-24-multi-party-coordination) | Multi-party Coordination/Negotiation | 3 | ⭐ |
| [CAN-25](#can-25-event-annotationflagging) | Event Annotation/Flagging | 3 | ⭐⭐ |

---

## Tier 1: Universal Capabilities (6 tasks)

### CAN-01: Calendar Events Retrieval

**Description**: Retrieve calendar event data from calendar systems via API, with optional filters for time range, attendees, or status.

**Frequency**: 9/9 prompts (100%) - **MOST UNIVERSAL CAPABILITY**

**API/Tool**: 
- Microsoft Graph: `GET /me/calendar/events`
- Google Calendar: `GET /calendar/v3/users/me/events`

**Used In**: ALL 9 v2 hero prompts
- Organizer-1: Retrieve pending invitations
- Organizer-2: Get upcoming meetings for tracking
- Organizre-3: Get historical events for time analysis
- Schedule-1: Check calendar for recurring meeting setup
- Schedule-2: Find Thursday afternoon meetings
- Schedule-3: Get multi-person calendars
- Collaborate-1: Find Project Alpha meetings
- Collaborate-2: Find senior leadership meeting
- Collaborate-3: Find customer Beta meeting

**Input Schema**:
```json
{
  "time_range": {
    "start": "ISO8601 datetime",
    "end": "ISO8601 datetime"
  },
  "filters": {
    "status": ["accepted", "tentative", "declined"],
    "categories": ["array of strings"],
    "attendees": ["email addresses"]
  }
}
```

**Output Schema**:
```json
{
  "events": [
    {
      "id": "string",
      "subject": "string",
      "start": {"dateTime": "ISO8601", "timeZone": "string"},
      "end": {"dateTime": "ISO8601", "timeZone": "string"},
      "attendees": ["array"],
      "responseStatus": "string"
    }
  ]
}
```

**Implementation Priority**: ⭐⭐⭐⭐⭐ **CRITICAL** - Build in Week 1

---

### CAN-02: Meeting Type Classification

**Description**: Classify calendar events by meeting format/type based on structural attributes (attendee count, subject keywords, organizer).

**Note**: Previously CAN-02A in v1.0, renumbered to CAN-02 in v2.0

**Frequency**: 7/9 prompts (78%)

**Type**: Format-based classification (objective)

**API/Tool**: 
- ML Classification Model
- Azure AI Language (Text classification)
- LLM (Few-shot classification)

**Used In**: 7 v2 prompts
- Organizer-1, Organizer-2, Organizre-3, Schedule-3, Collaborate-1, Collaborate-2, Collaborate-3

**Meeting Type Taxonomy** (31+ types):
1. **1:1**: 2 attendees
2. **Team Sync**: 3-10 attendees, recurring
3. **Customer Meeting**: External domain attendees
4. **All-Hands**: 50+ attendees
5. **Executive Review**: VP+ attendees
6. **Project Review**: Project-specific
7. **Interview**: HR involved
8. **Lunch/Social**: Meal time
9. **Training/Workshop**
10. **Stand-up**: Daily, 15min
... and 21+ more

**Input Schema**:
```json
{
  "event": {
    "subject": "string",
    "attendees": ["array"],
    "organizer": "string",
    "isRecurring": "boolean",
    "duration": "minutes"
  }
}
```

**Output Schema**:
```json
{
  "meeting_type": "string",
  "confidence": 0.0-1.0,
  "attributes": {
    "format": "1:1|team|all-hands|...",
    "domain": "internal|customer|vendor"
  }
}
```

**Implementation Priority**: ⭐⭐⭐⭐⭐ **CRITICAL** - Build in Week 2

---

### CAN-03: Meeting Importance Assessment

**Description**: Assess the business importance, urgency, or priority level of meetings based on context, attendees, and user goals.

**Note**: Previously CAN-02B in v1.0, renumbered to CAN-03 in v2.0

**Frequency**: 7/9 prompts (78%)

**Type**: Value-based assessment (context-dependent)

**API/Tool**: 
- ML Scoring Model
- LLM reasoning (GPT-5, Claude)
- Rule-based scoring

**Used In**: 7 v2 prompts
- Organizer-1, Organizer-2, Organizre-3, Schedule-3, Collaborate-1, Collaborate-2, Collaborate-3

**Importance Factors**:
1. **Attendee Seniority**: VP/C-level = High importance
2. **External Stakeholders**: Customer/Partner = High importance
3. **User Priorities**: Alignment with stated goals
4. **Business Impact**: Revenue, strategy, compliance
5. **Urgency**: Deadline proximity, blocking issues
6. **Meeting Rarity**: One-time vs recurring

**Input Schema**:
```json
{
  "event": "calendar event object",
  "user_priorities": ["customer meetings", "product strategy"],
  "context": {
    "attendee_roles": ["VP", "IC", "Customer"],
    "business_domain": "string",
    "urgency_signals": ["deadline", "blocker"]
  }
}
```

**Output Schema**:
```json
{
  "importance_score": 0.0-1.0,
  "importance_level": "critical|high|medium|low",
  "rationale": "string explaining the assessment",
  "priority_alignment": ["which user priorities this aligns with"]
}
```

**Implementation Priority**: ⭐⭐⭐⭐⭐ **CRITICAL** - Build in Week 2

---

### CAN-04: Natural Language Understanding

**Description**: Parse user prompts to extract intent, constraints, time ranges, priorities, and actionable requirements.

**Frequency**: 9/9 prompts (100%) - **UNIVERSAL FIRST STEP**

**API/Tool**: 
- Azure AI Language (Intent recognition, Entity extraction)
- OpenAI GPT-4/GPT-5 (Structured output)
- Claude (Structured extraction)

**Used In**: ALL 9 v2 hero prompts (always Step 1)

**Extraction Targets**:
1. **Intent**: What user wants to do (track, schedule, analyze, prepare)
2. **Constraints**: Time ranges, preferences, requirements
3. **Entities**: People names, meeting types, priorities
4. **Time Expressions**: "this week", "next Thursday", "next 2 weeks"
5. **Preferences**: "afternoons preferred", "avoid Fridays"
6. **Actions**: "flag", "reschedule", "show me as busy"

**Input Schema**:
```json
{
  "user_query": "natural language prompt string"
}
```

**Output Schema**:
```json
{
  "intent": "track|schedule|analyze|prepare|flag|reschedule",
  "constraints": {
    "time_range": {"start": "datetime", "end": "datetime"},
    "time_preferences": ["afternoons", "avoid Fridays"],
    "attendees": ["name1", "name2"],
    "priorities": ["customer meetings", "product strategy"]
  },
  "entities": {
    "people": ["Chris", "Sangya", "Kat"],
    "projects": ["Project Alpha"],
    "companies": ["customer Beta"]
  },
  "actions": ["flag_prep_time", "auto_reschedule", "update_rsvp"]
}
```

**Implementation Priority**: ⭐⭐⭐⭐⭐ **CRITICAL** - Build in Week 1

---

### CAN-05: Attendee/Contact Resolution

**Description**: Resolve names, email addresses, and contact details to full user profiles with organizational context.

**Frequency**: 6/9 prompts (67%)

**API/Tool**: 
- Microsoft Graph: `GET /users/{user-id}`
- Microsoft Graph: `GET /me/people`
- Azure AD: User directory search

**Used In**: 6 v2 prompts
- Schedule-1: Resolve "{name}" for 1:1 setup
- Schedule-2: Resolve attendees for rescheduling
- Schedule-3: Resolve Chris, Sangya, Kat
- Collaborate-1: Resolve product and marketing team members
- Collaborate-2: Resolve senior leadership attendees
- Collaborate-3: Resolve customer Beta attendees

**Human Evaluation Insight**: 
> "The system needs to know who are in the senior leadership to find relevant meetings and meeting related materials. So CAN-05 is a critical task." - Collaborate-2 evaluation

**Resolution Types**:
1. **Name → Email**: "Chris" → "chris@contoso.com"
2. **Email → Full Profile**: Title, department, manager, photo
3. **Role → People**: "senior leadership" → [List of VPs/C-level]
4. **Team → Members**: "product team" → [Product team members]
5. **Company → Contacts**: "customer Beta" → [Beta company contacts]

**Input Schema**:
```json
{
  "query": {
    "type": "name|email|role|team|company",
    "value": "string",
    "context": "optional organizational context"
  }
}
```

**Output Schema**:
```json
{
  "resolved_people": [
    {
      "id": "user-id",
      "displayName": "string",
      "email": "string",
      "jobTitle": "string",
      "department": "string",
      "officeLocation": "string",
      "manager": "user object"
    }
  ]
}
```

**Implementation Priority**: ⭐⭐⭐⭐⭐ **CRITICAL** - Build in Week 2

---

## Tier 2: Common Capabilities (9 tasks)

### CAN-06: Availability Checking

**Description**: Check free/busy status across calendars to find available time slots for scheduling.

**Frequency**: 4/9 prompts (44%)

**API/Tool**: 
- Microsoft Graph: `POST /me/calendar/getSchedule`
- Google Calendar: Free/busy query

**Used In**: 4 v2 prompts
- Schedule-1: Check availability for weekly 1:1
- Schedule-2: Find alternative time slots
- Schedule-3: Multi-person availability check
- (Collaborate prompts don't typically need this)

**Input Schema**:
```json
{
  "attendees": ["email1@domain.com", "email2@domain.com"],
  "time_range": {
    "start": "ISO8601 datetime",
    "end": "ISO8601 datetime"
  },
  "duration": "minutes"
}
```

**Output Schema**:
```json
{
  "available_slots": [
    {
      "start": "ISO8601 datetime",
      "end": "ISO8601 datetime",
      "attendee_status": {
        "email1@domain.com": "free",
        "email2@domain.com": "free"
      }
    }
  ],
  "busy_slots": ["array of busy time blocks"]
}
```

**Implementation Priority**: ⭐⭐⭐⭐ **HIGH** - Build in Week 3

---

### CAN-07: Meeting Metadata Extraction

**Description**: Extract detailed metadata from calendar events including RSVP status, attendees, agenda, attachments, and meeting links.

**Frequency**: 7/9 prompts (78%)

**API/Tool**: 
- Microsoft Graph: Event properties
- Parse email invitations
- Extract from meeting descriptions

**Used In**: 7 v2 prompts
- Organizer-1, Organizer-2, Organizre-3, Schedule-2, Schedule-3, Collaborate-2, Collaborate-3

**Note**: This is a **PARENT TASK** - enables CAN-05 (attendee analysis) and CAN-13 (RSVP update)

**Metadata Extracted**:
1. **RSVP Status**: accepted, tentative, declined, pending
2. **Attendees**: Required, optional, resources
3. **Agenda/Description**: Meeting purpose and topics
4. **Attachments**: Documents, presentations
5. **Meeting Links**: Teams/Zoom URLs
6. **Organizer**: Who created the meeting
7. **Categories/Tags**: User-defined labels
8. **Importance**: High/Normal/Low flag

**Input Schema**:
```json
{
  "event_id": "string"
}
```

**Output Schema**:
```json
{
  "metadata": {
    "responseStatus": "accepted|tentative|declined|pending",
    "attendees": {
      "required": ["array"],
      "optional": ["array"],
      "resources": ["rooms", "equipment"]
    },
    "body": {
      "content": "HTML or plain text",
      "agenda_items": ["extracted topics"]
    },
    "attachments": ["array of file references"],
    "onlineMeeting": {"joinUrl": "string", "provider": "Teams|Zoom"},
    "organizer": "user object",
    "categories": ["tags"],
    "importance": "high|normal|low"
  }
}
```

**Implementation Priority**: ⭐⭐⭐⭐ **HIGH** - Build in Week 3

---

### CAN-08: Document/Content Retrieval

**Description**: Retrieve meeting-related documents, emails, chat messages, and content from various sources.

**Frequency**: 4/9 prompts (44%)

**API/Tool**: 
- Microsoft Graph: SharePoint, OneDrive
- Microsoft Graph: Outlook messages
- Microsoft Graph: Teams chat
- CRM systems, project management tools

**Used In**: 4 v2 prompts
- Collaborate-1: Retrieve Project Alpha documents
- Collaborate-2: Retrieve senior leadership meeting materials
- Collaborate-3: Retrieve customer Beta company background
- (Organization/Schedule prompts typically don't need this)

**Content Sources**:
1. **SharePoint**: Project documents, presentations
2. **OneDrive**: Personal files shared in meetings
3. **Outlook**: Email threads related to meeting
4. **Teams**: Chat messages about the topic
5. **CRM**: Customer records, interaction history
6. **Project Tools**: Jira, Azure DevOps, GitHub

**Input Schema**:
```json
{
  "search_query": {
    "keywords": ["Project Alpha", "customer Beta"],
    "attendees": ["filter by who has access"],
    "date_range": "recent|all",
    "sources": ["sharepoint", "email", "teams", "crm"]
  }
}
```

**Output Schema**:
```json
{
  "documents": [
    {
      "id": "string",
      "title": "string",
      "url": "string",
      "source": "sharepoint|onedrive|teams|crm",
      "modified": "datetime",
      "modifiedBy": "user",
      "relevance_score": 0.0-1.0
    }
  ]
}
```

**Implementation Priority**: ⭐⭐⭐ **MEDIUM** - Build in Week 4

---

### CAN-09: Document Generation/Formatting

**Description**: Generate formatted documents like agendas, briefs, dossiers, summaries, and meeting materials.

**Frequency**: 5/9 prompts (56%)

**API/Tool**: 
- LLM (GPT-5, Claude) for content generation
- Templates (Word, Markdown, HTML)
- Microsoft Graph: Create/update documents

**Used In**: 5 v2 prompts
- Collaborate-1: Generate agenda for Project Alpha review
- Collaborate-2: Summarize topics into 3 discussion points, generate response scripts
- Collaborate-3: Prepare brief, create attendee dossiers
- (Organizer/Schedule prompts typically output structured data, not documents)

**Document Types**:
1. **Agenda**: Structured meeting outline with time allocations
2. **Brief**: Meeting preparation document with context
3. **Dossier**: Person profile with background and interests
4. **Summary**: Condensed version of longer content
5. **Response Script**: Prepared answers to anticipated questions
6. **Talking Points**: Bullet-point discussion guides

**Input Schema**:
```json
{
  "document_type": "agenda|brief|dossier|summary|script",
  "content_sources": ["documents", "emails", "context"],
  "requirements": {
    "length": "short|medium|long",
    "format": "markdown|html|docx|pdf",
    "structure": "bullet|narrative|mixed"
  },
  "context": {
    "meeting": "event object",
    "attendees": ["array"],
    "goal": "string describing meeting purpose"
  }
}
```

**Output Schema**:
```json
{
  "document": {
    "title": "string",
    "content": "formatted text",
    "format": "markdown|html|docx",
    "sections": [
      {
        "heading": "string",
        "content": "string",
        "order": "integer"
      }
    ]
  }
}
```

**Implementation Priority**: ⭐⭐⭐ **MEDIUM** - Build in Week 4

---

### CAN-10: Time Aggregation/Statistical Analysis

**Description**: Aggregate and analyze time spent across meetings, categories, people, and projects with statistical summaries.

**Frequency**: 2/9 prompts (22%)

**API/Tool**: 
- pandas, NumPy for data analysis
- SQL for aggregation queries
- Visualization libraries

**Used In**: 2 v2 prompts
- Organizre-3: "Understand where I am spending my time" - time breakdown analysis
- (Potentially other prompts for analytics features)

**Analysis Types**:
1. **Time by Category**: Hours per meeting type (1:1, team, customer)
2. **Time by Person**: Hours with each person/team
3. **Time by Project**: Hours per project or initiative
4. **Trend Analysis**: Week-over-week, month-over-month changes
5. **Utilization**: % of time in meetings vs focused work
6. **Peak Times**: When most meetings occur

**Input Schema**:
```json
{
  "events": ["array of calendar events"],
  "aggregation": {
    "group_by": ["type", "attendees", "project", "time_period"],
    "metrics": ["total_hours", "meeting_count", "average_duration"],
    "time_range": "week|month|quarter|year"
  }
}
```

**Output Schema**:
```json
{
  "summary": {
    "total_hours": 40.5,
    "meeting_count": 25,
    "average_duration_minutes": 45
  },
  "breakdown": [
    {
      "category": "Customer Meetings",
      "hours": 12.5,
      "count": 5,
      "percentage": 30.9
    }
  ],
  "trends": {
    "week_over_week_change": "+15%",
    "month_over_month_change": "-5%"
  }
}
```

**Implementation Priority**: ⭐⭐⭐ **MEDIUM** - Build in Week 5

---

### CAN-11: Priority/Preference Matching

**Description**: Match meetings and time slots against user priorities, preferences, and constraints.

**Frequency**: 5/9 prompts (56%)

**API/Tool**: 
- Semantic similarity (embeddings)
- Rule-based matching
- LLM reasoning

**Used In**: 5 v2 prompts
- Organizer-1: Match to "customer meetings" and "product strategy" priorities
- Organizer-2: Match to "important meetings" criteria
- Organizre-3: Match to "top priorities" for time reclamation
- (Schedule and Collaborate prompts use constraints more than priority matching)

**Matching Types**:
1. **Keyword Matching**: "customer" in priorities → customer meetings
2. **Semantic Matching**: "product strategy" → roadmap meetings, vision discussions
3. **Attendee Matching**: Priority people → meetings with those people
4. **Time Preference**: "afternoons preferred" → PM time slots
5. **Constraint Matching**: "avoid Fridays" → exclude Friday slots

**Input Schema**:
```json
{
  "items": ["meetings or time slots"],
  "priorities": ["customer meetings", "product strategy"],
  "preferences": {
    "time_of_day": "morning|afternoon|evening",
    "days_to_avoid": ["Friday"],
    "preferred_duration": "minutes",
    "preferred_attendees": ["names"]
  }
}
```

**Output Schema**:
```json
{
  "matches": [
    {
      "item": "meeting or time slot",
      "match_score": 0.0-1.0,
      "matched_priorities": ["which priorities matched"],
      "matched_preferences": ["which preferences matched"],
      "rationale": "explanation of match"
    }
  ],
  "sorted_by_score": true
}
```

**Implementation Priority**: ⭐⭐⭐ **MEDIUM** - Build in Week 3

---

### CAN-12: Constraint Satisfaction

**Description**: Find time slots or solutions that satisfy multiple constraints (time, attendees, resources, preferences).

**Frequency**: 4/9 prompts (44%)

**API/Tool**: 
- Constraint Programming (OR-Tools, Python-constraint)
- Rule-based solver
- Heuristic search

**Used In**: 4 v2 prompts
- Schedule-1: Weekly 30-min, afternoons, avoid Fridays
- Schedule-2: Clear Thursday afternoon + reschedule constraints
- Schedule-3: 1 hour, next 2 weeks, 3 people, work around Kat, in-person + room
- (Organization/Collaborate prompts have fewer hard constraints)

**Constraint Types**:
1. **Time Constraints**: Specific days, time ranges, durations
2. **Attendee Constraints**: Required people, work around someone's schedule
3. **Resource Constraints**: Room availability, equipment
4. **Preference Constraints**: Soft preferences (afternoons preferred)
5. **Conflict Constraints**: Don't overlap with existing meetings
6. **Business Rules**: Meeting policies, working hours

**Input Schema**:
```json
{
  "constraints": {
    "required": [
      {"type": "duration", "value": 60, "unit": "minutes"},
      {"type": "attendees", "value": ["email1", "email2", "email3"]},
      {"type": "timeframe", "start": "datetime", "end": "datetime"}
    ],
    "preferred": [
      {"type": "time_of_day", "value": "afternoon", "weight": 0.8},
      {"type": "avoid_day", "value": "Friday", "weight": 0.6}
    ],
    "rules": [
      {"type": "work_around", "person": "kat@contoso.com"},
      {"type": "in_person", "location": "Seattle office"}
    ]
  }
}
```

**Output Schema**:
```json
{
  "solutions": [
    {
      "time_slot": {"start": "datetime", "end": "datetime"},
      "satisfies_required": ["all required constraints"],
      "satisfies_preferred": ["percentage of preferred constraints"],
      "constraint_violations": [],
      "score": 0.0-1.0
    }
  ]
}
```

**Implementation Priority**: ⭐⭐⭐ **MEDIUM** - Build in Week 4

---

### CAN-13: RSVP Status Update

**Description**: Update meeting RSVP status (accept, decline, tentative) in calendar system.

**Frequency**: 3/9 prompts (33%)

**API/Tool**: 
- Microsoft Graph: `POST /me/events/{id}/accept`
- Microsoft Graph: `POST /me/events/{id}/decline`
- Microsoft Graph: `POST /me/events/{id}/tentativelyAccept`

**Used In**: 3 v2 prompts
- Organizer-1: Accept priority meetings, decline/tentative others
- Schedule-2: Update RSVPs when clearing Thursday afternoon
- (Other prompts don't explicitly update RSVP status)

**Note**: This is a **WRITE operation** (vs CAN-07 which is READ operation for metadata)

**Dependencies**: Requires CAN-07 (Metadata Extraction) to know current RSVP status

**Actions**:
1. **Accept**: Confirm attendance
2. **Decline**: Reject invitation
3. **Tentative**: Provisional acceptance
4. **Propose New Time**: Suggest alternative (advanced)

**Input Schema**:
```json
{
  "event_id": "string",
  "action": "accept|decline|tentative|propose_new_time",
  "comment": "optional message to organizer",
  "proposed_time": "optional if action=propose_new_time"
}
```

**Output Schema**:
```json
{
  "success": true,
  "updated_status": "accepted|declined|tentativelyAccepted",
  "notification_sent": true
}
```

**Implementation Priority**: ⭐⭐⭐ **MEDIUM** - Build in Week 5

---

### CAN-14: Recommendation Engine

**Description**: Generate intelligent recommendations for meetings, time slots, actions, or optimizations based on analysis.

**Frequency**: 3/9 prompts (33%)

**API/Tool**: 
- LLM reasoning (GPT-5, Claude)
- Rule-based recommendations
- ML recommendation models

**Used In**: 3 v2 prompts
- Organizer-1: Recommend which invitations to prioritize
- Organizre-3: Recommend ways to reclaim time
- (Other prompts execute actions rather than recommend)

**Recommendation Types**:
1. **Prioritization**: Which meetings to accept/prioritize
2. **Time Optimization**: Which meetings to decline/reschedule to save time
3. **Scheduling**: Best time slots for new meetings
4. **Preparation**: Which meetings need prep time
5. **Delegation**: Which meetings could be delegated
6. **Consolidation**: Which meetings could be combined

**Input Schema**:
```json
{
  "context": {
    "events": ["array of meetings"],
    "priorities": ["user priorities"],
    "constraints": "time, resources, goals"
  },
  "recommendation_type": "prioritize|optimize|schedule|prepare",
  "max_recommendations": 5
}
```

**Output Schema**:
```json
{
  "recommendations": [
    {
      "item": "meeting or action",
      "recommendation": "accept|decline|reschedule|prepare|delegate",
      "confidence": 0.0-1.0,
      "rationale": "explanation",
      "impact": "high|medium|low",
      "effort": "high|medium|low"
    }
  ],
  "summary": "overall recommendation strategy"
}
```

**Implementation Priority**: ⭐⭐⭐ **MEDIUM** - Build in Week 5

---

## Tier 3: Specialized Capabilities (10 tasks)

### CAN-15: Recurrence Rule Generation

**Description**: Generate recurrence rules (RRULE) for recurring meetings with complex patterns.

**Frequency**: 2/9 prompts (22%)

**API/Tool**: 
- iCalendar RRULE specification
- Recurrence pattern parser
- Microsoft Graph recurrence pattern

**Used In**: 2 v2 prompts
- Schedule-1: "weekly 30-min 1:1" → Generate weekly recurrence
- (Other prompts are for one-time meetings or don't specify recurrence)

**Recurrence Patterns**:
1. **Simple**: Daily, Weekly, Monthly, Yearly
2. **Complex**: Every other Tuesday, First Monday of month, Weekdays only
3. **With End Date**: Until specific date
4. **With Count**: Repeat N times
5. **With Exceptions**: Skip specific dates

**Input Schema**:
```json
{
  "pattern": {
    "type": "daily|weekly|monthly|yearly",
    "interval": 1,
    "daysOfWeek": ["monday", "tuesday"],
    "dayOfMonth": 15,
    "month": 6
  },
  "range": {
    "type": "endDate|numbered|noEnd",
    "startDate": "ISO8601 date",
    "endDate": "ISO8601 date",
    "numberOfOccurrences": 10
  },
  "exceptions": ["ISO8601 dates to skip"]
}
```

**Output Schema**:
```json
{
  "rrule": "FREQ=WEEKLY;BYDAY=MO,WE,FR;UNTIL=20251231",
  "human_readable": "Every Monday, Wednesday, and Friday until Dec 31, 2025",
  "occurrences_preview": ["next 5 occurrence dates"]
}
```

**Implementation Priority**: ⭐⭐ **LOW** - Build in Week 6+

---

### CAN-16: Event Monitoring/Change Detection

**Description**: Monitor calendar events for changes (updates, cancellations, new invitations) and trigger notifications or actions.

**Frequency**: 2/9 prompts (22%)

**API/Tool**: 
- Microsoft Graph Webhooks/Subscriptions
- Delta queries for change tracking
- Event polling

**Used In**: 2 v2 prompts
- Organizer-2: "Track all my important meetings" - continuous monitoring
- Schedule-1: "Automatically reschedule on declines or conflicts" - detect changes
- (Added to Organizer-2 based on human evaluation)

**Human Evaluation Insight**: 
> "Missing 'track important meetings'. Can we attribute 'track' to CAN-16?" - Organizer-2 evaluation

**Monitoring Types**:
1. **New Invitations**: Detect new meeting requests
2. **Updates**: Time change, location change, attendee changes
3. **Cancellations**: Meeting cancelled by organizer
4. **RSVP Changes**: Attendees accept/decline
5. **Conflicts**: New meeting conflicts with existing

**Input Schema**:
```json
{
  "subscription": {
    "event_types": ["created", "updated", "deleted"],
    "filters": {
      "importance": "high",
      "attendees": ["specific people"],
      "categories": ["tags"]
    },
    "notification_url": "webhook endpoint"
  }
}
```

**Output Schema**:
```json
{
  "change_events": [
    {
      "event_id": "string",
      "change_type": "created|updated|deleted",
      "timestamp": "ISO8601",
      "changes": {
        "field": "before → after values"
      },
      "trigger_action": "flag|notify|reschedule"
    }
  ]
}
```

**Implementation Priority**: ⭐⭐ **LOW** - Build in Week 7+

---

### CAN-17: Automatic Rescheduling

**Description**: Automatically reschedule meetings when conflicts or declines occur, finding alternative time slots.

**Frequency**: 1/9 prompts (11%)

**API/Tool**: 
- Microsoft Graph: Update event
- Orchestrates CAN-06 (availability), CAN-12 (constraints)

**Used In**: 1 v2 prompt
- Schedule-1: "Automatically reschedule on declines or conflicts"

**Rescheduling Triggers**:
1. **Decline Received**: Attendee declines meeting
2. **Conflict Detected**: New meeting conflicts with existing
3. **Organizer Change**: Organizer changes time
4. **User Request**: Manual reschedule request

**Rescheduling Strategy**:
1. **Find Alternative Slots**: Use CAN-06 for availability
2. **Apply Constraints**: Use CAN-12 for preferences
3. **Update Event**: Modify calendar event
4. **Notify Attendees**: Send update notifications

**Input Schema**:
```json
{
  "event_id": "string to reschedule",
  "trigger": "decline|conflict|request",
  "constraints": "same as CAN-12",
  "notify_attendees": true
}
```

**Output Schema**:
```json
{
  "rescheduled": true,
  "old_time": "ISO8601 datetime",
  "new_time": "ISO8601 datetime",
  "notifications_sent": true,
  "alternative_slots_considered": 5
}
```

**Implementation Priority**: ⭐⭐ **LOW** - Build in Week 8+

---

### CAN-18: Objection/Risk Anticipation

**Description**: Anticipate potential objections, concerns, or risks that might arise in meetings and prepare responses.

**Frequency**: 1/9 prompts (11%)

**API/Tool**: 
- LLM reasoning (GPT-5, Claude)
- Historical meeting analysis
- Sentiment analysis

**Used In**: 1 v2 prompt
- Collaborate-2: "Generate any objections or concerns that might come up and give me effective responses"

**Human Evaluation Insight**: 
> "The user does not expect the system to find blocking issues and confirm status but the requester want to find out those during the meeting so CAN-18 should not be activated." - Collaborate-1 evaluation (GPT-5 over-interpreted)

**Anticipation Types**:
1. **Technical Objections**: Feasibility, timeline, resources
2. **Business Objections**: Cost, ROI, priority
3. **Political Objections**: Stakeholder concerns, turf wars
4. **Risk Identification**: What could go wrong
5. **Competitive Concerns**: Market, competitors

**Input Schema**:
```json
{
  "meeting_context": {
    "topic": "string",
    "attendees": ["array with roles"],
    "goal": "what you're proposing or presenting"
  },
  "background": {
    "previous_discussions": ["context"],
    "stakeholder_concerns": ["known issues"]
  }
}
```

**Output Schema**:
```json
{
  "objections": [
    {
      "objection": "Likely concern or question",
      "source": "who might raise it",
      "severity": "high|medium|low",
      "response": "Effective counter-argument or mitigation",
      "supporting_data": ["evidence to use in response"]
    }
  ]
}
```

**Implementation Priority**: ⭐⭐ **LOW** - Build in Week 8+

---

### CAN-19: Resource Booking

**Description**: Book meeting rooms, equipment, and other physical or virtual resources.

**Frequency**: 1/9 prompts (11%)

**API/Tool**: 
- Microsoft Graph: `POST /places`
- Room finder APIs
- Equipment reservation systems

**Used In**: 1 v2 prompt
- Schedule-3: "Make the meeting in person and add a room"

**Resource Types**:
1. **Meeting Rooms**: Conference rooms, huddle spaces
2. **Equipment**: Projectors, whiteboards, video conferencing
3. **Virtual Resources**: Zoom rooms, Teams channels
4. **Parking**: For in-person meetings
5. **Catering**: For large meetings

**Booking Constraints**:
1. **Capacity**: Room must fit N attendees
2. **Location**: Proximity to attendees
3. **Amenities**: AV equipment, whiteboards
4. **Time**: Available during meeting time
5. **Building**: Specific office building

**Input Schema**:
```json
{
  "meeting": {
    "start": "ISO8601 datetime",
    "end": "ISO8601 datetime",
    "attendee_count": 4
  },
  "requirements": {
    "location": "Seattle office",
    "capacity_minimum": 4,
    "amenities": ["projector", "whiteboard"],
    "building": "Building 92"
  }
}
```

**Output Schema**:
```json
{
  "resources": [
    {
      "id": "room-id",
      "name": "Conference Room A",
      "building": "Building 92",
      "floor": 3,
      "capacity": 8,
      "amenities": ["projector", "whiteboard", "video conference"],
      "available": true,
      "booked": true
    }
  ]
}
```

**Implementation Priority**: ⭐⭐ **LOW** - Build in Week 7+

---

### CAN-20: Data Visualization/Reporting

**Description**: Create visual representations of meeting data, time analysis, and calendar insights.

**Frequency**: 1/9 prompts (11%)

**API/Tool**: 
- Chart.js, D3.js for visualization
- Matplotlib, Plotly for Python
- Power BI embedding

**Used In**: 1 v2 prompt
- Organizre-3: "Help me understand where I am spending my time" - visual time breakdown

**Visualization Types**:
1. **Time Breakdown**: Pie chart of time by category
2. **Trend Lines**: Meeting count over time
3. **Heat Maps**: When meetings typically occur
4. **Gantt Charts**: Meeting timeline view
5. **Network Graphs**: Collaboration patterns
6. **Comparison Charts**: Week-over-week, month-over-month

**Input Schema**:
```json
{
  "data": "output from CAN-10 (time aggregation)",
  "visualization_type": "pie|bar|line|heatmap|gantt|network",
  "title": "string",
  "dimensions": {"width": 800, "height": 600}
}
```

**Output Schema**:
```json
{
  "visualization": {
    "type": "chart type",
    "data": "chart.js config or image URL",
    "format": "svg|png|interactive_html",
    "insights": ["Notable patterns highlighted"]
  }
}
```

**Implementation Priority**: ⭐⭐ **LOW** - Build in Week 9+

---

### CAN-21: Focus Time/Preparation Time Analysis

**Description**: Estimate preparation time needed for meetings and identify when focus time blocks should be scheduled.

**Frequency**: 1/9 prompts (11%)

**API/Tool**: 
- ML model for time estimation
- Rule-based estimation
- Historical preparation time analysis

**Used In**: 1 v2 prompt
- Organizer-2: "Flag any that require focus time to prepare for them"

**Preparation Time Factors**:
1. **Meeting Type**: Executive reviews need more prep than 1:1s
2. **Attendee Seniority**: C-level meetings need thorough prep
3. **Meeting Topic**: Complex topics need research time
4. **Your Role**: Presenter vs attendee changes prep needs
5. **Materials**: Document review, presentation creation

**Estimation Logic**:
- **1:1 with peer**: 5-15 min prep
- **Team meeting**: 15-30 min prep
- **Customer meeting**: 30-60 min prep
- **Executive review**: 1-2 hours prep
- **Board meeting**: 4+ hours prep

**Input Schema**:
```json
{
  "meeting": {
    "type": "executive_review|customer|team|1:1",
    "attendees": ["array with roles"],
    "your_role": "presenter|attendee|organizer",
    "topic_complexity": "high|medium|low"
  }
}
```

**Output Schema**:
```json
{
  "preparation_needed": true,
  "estimated_prep_time_minutes": 60,
  "suggested_prep_window": {
    "start": "1 day before meeting",
    "end": "2 hours before meeting"
  },
  "prep_tasks": [
    "Review Q3 financials",
    "Prepare 5-slide deck",
    "Research competitor announcements"
  ],
  "focus_time_block": {
    "duration_minutes": 90,
    "suggested_time": "Morning of meeting day"
  }
}
```

**Implementation Priority**: ⭐⭐ **LOW** - Build in Week 7+

---

### CAN-22: Research/Intelligence Gathering

**Description**: Research and gather intelligence about meeting participants, companies, topics, and context from external sources.

**Frequency**: 1/9 prompts (11%)

**API/Tool**: 
- Web search APIs (Bing, Google)
- LinkedIn API
- CRM data
- News aggregators
- Company databases

**Used In**: 1 v2 prompt
- Collaborate-3: "Include a background on their company" - research customer Beta

**Research Types**:
1. **People Intelligence**: LinkedIn profiles, job history, publications
2. **Company Intelligence**: Company background, news, financials
3. **Topic Intelligence**: Industry trends, recent developments
4. **Competitive Intelligence**: Competitor activities
5. **Historical Context**: Previous interactions, meeting history

**Input Schema**:
```json
{
  "research_target": {
    "type": "person|company|topic",
    "name": "string",
    "context": "why researching"
  },
  "depth": "quick|moderate|deep",
  "sources": ["linkedin", "crm", "news", "web"]
}
```

**Output Schema**:
```json
{
  "intelligence": {
    "summary": "Executive summary paragraph",
    "key_facts": [
      "Fact 1 with source",
      "Fact 2 with source"
    ],
    "recent_news": ["News items from last 30 days"],
    "talking_points": ["Relevant discussion topics"],
    "sources": ["URLs and references"]
  }
}
```

**Implementation Priority**: ⭐⭐ **LOW** - Build in Week 9+

---

### CAN-23: Agenda Generation/Structuring

**Description**: Generate structured meeting agendas with topics, time allocations, and discussion goals.

**Frequency**: 1/9 prompts (11%)

**API/Tool**: 
- LLM (GPT-5, Claude) for agenda generation
- Templates for standard agenda formats
- CAN-09 for document formatting

**Used In**: 1 v2 prompt
- Collaborate-1: "Help me set the agenda to review the progress of Project Alpha"

**Human Evaluation Insight**: 
> "The goal 'to get confirmation we are on track and discuss any blocking issues or risks' should be used as input for the agenda generation for CAN-09." - Collaborate-1 evaluation

**Agenda Components**:
1. **Meeting Objectives**: What should be accomplished
2. **Topic List**: Items to discuss
3. **Time Allocations**: Minutes per topic
4. **Discussion Leaders**: Who leads each topic
5. **Decision Points**: What needs to be decided
6. **Action Items**: Expected outcomes

**Input Schema**:
```json
{
  "meeting": {
    "subject": "string",
    "duration_minutes": 60,
    "attendees": ["array"],
    "goal": "what you want to achieve"
  },
  "topics": ["suggested discussion topics"],
  "template": "standard|executive|customer|project_review"
}
```

**Output Schema**:
```json
{
  "agenda": {
    "meeting_objective": "Clear statement of meeting purpose",
    "items": [
      {
        "order": 1,
        "topic": "Project Alpha Status Update",
        "duration_minutes": 15,
        "leader": "Product Manager",
        "description": "Review Q4 milestones and progress",
        "expected_outcome": "Confirmation of on-track status"
      }
    ],
    "total_duration": 60,
    "decision_points": ["Go/no-go on feature X"],
    "parking_lot": "For topics that don't fit in time"
  }
}
```

**Implementation Priority**: ⭐⭐ **LOW** - Build in Week 8+

---

### CAN-24: Multi-party Coordination/Negotiation

**Description**: Coordinate and negotiate time slots across multiple parties with complex constraints and competing preferences.

**Frequency**: 1/9 prompts (11%)

**API/Tool**: 
- Orchestrates CAN-05, CAN-06, CAN-12
- Multi-party scheduling algorithms
- Preference aggregation

**Used In**: 1 v2 prompt (implicitly)
- Schedule-3: Coordinate 3 people (Chris, Sangya, Kat) with "work around Kat's schedule"

**Note**: This is more of an **orchestration pattern** than a single API call, but included as canonical task for completeness.

**Coordination Complexity**:
1. **Simple**: 2 people, flexible time
2. **Moderate**: 3-5 people, some constraints
3. **Complex**: 6+ people, multiple constraints
4. **Very Complex**: VIPs, competing priorities, global timezones

**Negotiation Strategies**:
1. **Priority-based**: VIP schedules take precedence
2. **Democratic**: Find time that works for majority
3. **Constraint-relaxation**: Gradually relax preferences to find solution
4. **Alternative formats**: Offer multiple time options for voting

**Input Schema**:
```json
{
  "participants": [
    {
      "email": "string",
      "priority": "required|important|optional",
      "constraints": "their specific constraints",
      "flexibility": "high|medium|low"
    }
  ],
  "meeting_requirements": "from CAN-12",
  "coordination_strategy": "priority|democratic|relaxation"
}
```

**Output Schema**:
```json
{
  "proposed_times": [
    {
      "slot": "datetime",
      "attendee_status": {
        "person1": "available",
        "person2": "preferred",
        "person3": "conflict_but_can_move"
      },
      "quality_score": 0.0-1.0
    }
  ],
  "negotiations_needed": ["person X has conflict, may need to reschedule their 1:1"]
}
```

**Implementation Priority**: ⭐ **VERY LOW** - Build in Week 10+

---

### CAN-25: Event Annotation/Flagging (NEW in v2.0)

**Description**: Add annotations, flags, or visual indicators to calendar events when predefined conditions are met (e.g., prep time needed, VIP attendee, budget approval required).

**Frequency**: 1/9 prompts (11%)

**API/Tool**: 
- Microsoft Graph: Update event categories/tags
- Custom calendar properties
- Visual indicators in calendar UI

**Used In**: 1 v2 prompt
- Organizer-2: "Flag any that require focus time to prepare for them"

**Human Evaluation Rationale**: 
> "We do not have any Canonical task for 'flag'. 'Flag' is an action that we add an annotation to an event on calendar. We need to add new canonical tasks for similar tasks that signal something on calendar if some predefined condition occurs." - Organizer-2 evaluation

**Annotation Types**:
1. **Prep Time Needed**: Flag meetings requiring preparation
2. **VIP Attendee**: Highlight meetings with executives/customers
3. **Budget Approval**: Financial decision meetings
4. **Deadline Sensitive**: Time-critical meetings
5. **Follow-up Required**: Needs action items after meeting
6. **Travel Required**: In-person meetings requiring travel

**Flagging Conditions**:
- **Prep Time**: Executive review OR customer meeting OR presentation role
- **VIP**: C-level OR customer executive in attendees
- **Budget**: Keywords "budget", "approval", "spend" in subject
- **Deadline**: Meeting within 3 days of project milestone
- **Follow-up**: Recurring meeting OR project review
- **Travel**: Location != user's office

**Input Schema**:
```json
{
  "event_id": "string",
  "annotation": {
    "type": "prep_time|vip|budget|deadline|followup|travel",
    "flag_label": "string to display",
    "flag_color": "red|orange|yellow|blue|green",
    "condition_met": "why this was flagged",
    "action_required": "what user should do"
  }
}
```

**Output Schema**:
```json
{
  "event_updated": true,
  "visual_indicator": {
    "category": "Needs Prep",
    "color": "orange",
    "icon": "⚠️",
    "tooltip": "90 min prep recommended: Executive review with VP"
  },
  "notification_sent": true
}
```

**Example Use Cases**:
1. **Organizer-2**: Flag meetings needing prep time (orange flag)
2. **VIP Alerts**: Flag customer executive meetings (red flag)
3. **Budget Tracking**: Flag financial approval meetings (yellow flag)
4. **Travel Planning**: Flag in-person meetings requiring travel (blue flag)

**Implementation Priority**: ⭐⭐ **LOW** - Build in Week 8+

---

## Task Dependencies & Orchestration

### Parent-Child Relationships

**CAN-07 (Meeting Metadata Extraction) is PARENT to**:
- CAN-05 (Attendee Resolution) - needs attendee list
- CAN-13 (RSVP Update) - needs current RSVP status

**CAN-04 (NLU) is PARENT to**:
- ALL tasks - must understand intent first

**CAN-01 (Calendar Retrieval) is PARENT to**:
- Most analysis tasks - need event data

### Orchestration Patterns

**Sequential**: CAN-04 → CAN-01 → CAN-07 → CAN-05
**Parallel**: CAN-02, CAN-03, CAN-05 (can analyze same meeting concurrently)
**Conditional**: CAN-25 only if CAN-21 estimates prep time > threshold

---

## v2.0 Changes Log

### Added
- **CAN-25**: Event Annotation/Flagging (new task based on Organizer-2 evaluation feedback)

### Renumbered
- All tasks renumbered sequentially 1-25 (no CAN-02A/CAN-02B split in numbering)
- Old CAN-02A → CAN-02 (Meeting Type Classification)
- Old CAN-02B → CAN-03 (Meeting Importance Assessment)
- Old CAN-03 → CAN-04 (shifted Calendar Event Creation, but actually moved to different position)
- All subsequent tasks shifted by +1 or +2 depending on position

### Reorganized
- Clearer tier boundaries based on actual v2 usage patterns
- Updated frequency counts from v2 gold standard human evaluation
- Added human evaluation insights as notes

---

## Implementation Roadmap

### Phase 1: Foundation (Weeks 1-2)
- CAN-01: Calendar Events Retrieval
- CAN-04: Natural Language Understanding
- CAN-02: Meeting Type Classification
- CAN-03: Meeting Importance Assessment
- CAN-05: Attendee/Contact Resolution

### Phase 2: Core Features (Weeks 3-5)
- CAN-06: Availability Checking
- CAN-07: Meeting Metadata Extraction
- CAN-11: Priority/Preference Matching
- CAN-12: Constraint Satisfaction
- CAN-13: RSVP Status Update
- CAN-14: Recommendation Engine

### Phase 3: Advanced Features (Weeks 6-9)
- CAN-08: Document/Content Retrieval
- CAN-09: Document Generation
- CAN-10: Time Aggregation/Analysis
- CAN-15: Recurrence Rule Generation
- CAN-16: Event Monitoring
- CAN-17: Automatic Rescheduling
- CAN-21: Focus Time Analysis
- CAN-23: Agenda Generation
- CAN-25: Event Annotation/Flagging

### Phase 4: Specialized Features (Weeks 10+)
- CAN-18: Objection/Risk Anticipation
- CAN-19: Resource Booking
- CAN-20: Data Visualization
- CAN-22: Research/Intelligence Gathering
- CAN-24: Multi-party Coordination

---

**Document End**
