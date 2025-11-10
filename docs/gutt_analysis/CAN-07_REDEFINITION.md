# CAN-07 Redefinition: Meeting Metadata Extraction (Parent Task)

**Author**: Chin-Yew Lin  
**Date**: November 7, 2025  
**Issue**: CAN-07 was incorrectly named "Meeting Invitation Sending" but should be foundational metadata extraction

---

## The Problem

**Original V1 Usage** (Incorrect):
- schedule-1: "Send meeting invitation to Sarah"
- schedule-2: "Send notifications to attendees"
- schedule-3: "Send meeting invitations"

**Why This Was Wrong**:
- Sending invitations is part of **CAN-03 (Calendar Event Creation/Update)**
- Creating an event in calendar systems **automatically sends invitations**
- CAN-07 was redundantly defined

---

## The Correct Definition

### CAN-07: Meeting Metadata Extraction

**Tier**: 2 (Common)  
**Type**: **Parent/Foundational Task**  
**Purpose**: Extract structured metadata from calendar events to enable downstream capabilities

### What It Extracts:

1. **RSVP Status Information**
   - Who accepted/declined/tentative/no-response
   - Response timestamps
   - Response comments
   - Enables: CAN-13 (RSVP Status Update)

2. **Attendee Information**
   - Required vs. optional attendees
   - Organizer details
   - Distribution lists expansion
   - Enables: CAN-05 (Attendee/Contact Resolution)

3. **Meeting Attachments & Pre-reads**
   - Document attachments
   - Links in meeting description
   - Pre-read materials
   - Enables: CAN-08 (Document/Content Retrieval)

4. **Meeting Context & History**
   - Meeting series history
   - Previous meeting notes
   - Recurring pattern metadata
   - Enables: Pattern analysis, preparation recommendations

5. **Meeting Logistics**
   - Location (physical/virtual)
   - Conference bridge details
   - Room/resource bookings
   - Enables: CAN-19 (Resource Booking)

6. **Meeting Content**
   - Agenda items (if structured)
   - Subject/title
   - Description/body
   - Enables: CAN-09 (Document Generation)

---

## Dependency Relationships

### CAN-07 Enables (Child Tasks):

```
CAN-07 (Meeting Metadata Extraction)
  ├─> CAN-13 (RSVP Status Update)
  │     └─ Needs: Attendee RSVP status from metadata
  │
  ├─> CAN-05 (Attendee/Contact Resolution)
  │     └─ Needs: Attendee list and details from metadata
  │
  ├─> CAN-08 (Document/Content Retrieval)
  │     └─ Needs: Attachment links and pre-read references
  │
  ├─> CAN-19 (Resource Booking)
  │     └─ Needs: Room/resource information from metadata
  │
  └─> CAN-09 (Document Generation)
        └─ Needs: Meeting context, agenda, previous notes
```

### CAN-07 Depends On:

```
CAN-01 (Calendar Events Retrieval)
  └─> CAN-07 (Meeting Metadata Extraction)
        └─ Needs: Calendar events to extract metadata from
```

---

## When CAN-07 Should Be Used

### Use Case 1: **Checking Who Responded to Meeting**
```
Prompt: "Who hasn't responded to my Project Alpha kickoff meeting?"

Flow:
1. CAN-01: Retrieve "Project Alpha kickoff" event
2. CAN-07: Extract RSVP status for all attendees
3. Filter: Find attendees with "no-response" status
4. Return: List of non-responders
```

### Use Case 2: **Finding Meetings with Pre-reads**
```
Prompt: "Show me meetings this week that have pre-read materials"

Flow:
1. CAN-01: Retrieve all meetings this week
2. CAN-07: Extract attachment/link metadata from each event
3. Filter: Events with attachments or links
4. Return: Meetings with pre-read materials
```

### Use Case 3: **Prepare for Meeting with Context**
```
Prompt: "Help me prep for my 1:1 with Jordan"

Flow:
1. CAN-01: Find next 1:1 with Jordan
2. CAN-07: Extract metadata:
   - Previous meeting notes (from series history)
   - Agenda items (from description)
   - Attachments (documents to review)
3. CAN-08: Retrieve the actual documents
4. CAN-09: Generate briefing with context
```

### Use Case 4: **Analyze Meeting Attendance Patterns**
```
Prompt: "Which team meetings have low attendance?"

Flow:
1. CAN-01: Retrieve team meetings (last month)
2. CAN-07: Extract RSVP status for each meeting
3. CAN-10: Compute attendance statistics
4. Return: Meetings with <50% acceptance rate
```

---

## Where CAN-07 Should Appear in Gold Standard

### organizer-2: "Flag meetings I need to prep for, put time on calendar"
**Add CAN-07 after CAN-02B**:
```
Step 3: CAN-02B - Assess which meetings are important
Step 4: CAN-07 - Extract metadata (attachments, agenda, previous notes)
Step 5: CAN-21 - Estimate prep time based on metadata
Step 6: CAN-14 - Recommend prep blocks
Step 7: CAN-03 - Create prep time on calendar
```

**Why**: Need to know if meeting has pre-reads (attachments) to estimate prep time

---

### schedule-2: "Bump all my meetings that can move"
**Add CAN-07 after CAN-02B**:
```
Step 3: CAN-02B - Classify which meetings are reschedulable
Step 4: CAN-07 - Extract attendee/organizer info to determine flexibility
Step 5: CAN-06 - Find new time slots
Step 6: CAN-03 - Reschedule meetings
Step 7: CAN-13 - Update RSVP status / notify attendees
```

**Why**: Need attendee info to know who to notify about reschedule

---

### collaborate-1: "Prep an agenda for my next meeting with Project Alpha team"
**Add CAN-07 after CAN-01**:
```
Step 2: CAN-01 - Find next Project Alpha meeting
Step 3: CAN-07 - Extract existing agenda, previous notes, attendees
Step 4: CAN-05 - Resolve team members
Step 5: CAN-08 - Retrieve documents (using attachment refs from CAN-07)
Step 6: CAN-22 - Discover who works on what
Step 7: CAN-18 - Anticipate risks (optional)
Step 8: CAN-09 - Generate updated agenda
```

**Why**: Need to extract existing agenda and previous meeting notes to build upon

---

### collaborate-2: "Pull together a briefing for my 1:1 with Jordan"
**Add CAN-07 after CAN-02A**:
```
Step 3: CAN-02A - Classify as 1:1 meeting
Step 4: CAN-07 - Extract previous 1:1 notes, agenda, action items
Step 5: CAN-08 - Retrieve Jordan's recent work
Step 6: CAN-09 - Generate briefing (incorporating previous context)
```

**Why**: Need previous 1:1 notes and action items to provide continuity

---

## API Implementation

### Microsoft Graph API

```python
# Extract meeting metadata
event = graph_client.users(user_id).events(event_id).get()

metadata = {
    "rsvp_status": {
        attendee.email: {
            "status": attendee.response.response_type,
            "time": attendee.response.time,
            "comment": attendee.response.comment
        }
        for attendee in event.attendees
    },
    "attachments": [
        {
            "name": att.name,
            "content_type": att.content_type,
            "size": att.size,
            "url": att.web_url if hasattr(att, 'web_url') else None
        }
        for att in event.attachments
    ],
    "organizer": {
        "name": event.organizer.email_address.name,
        "email": event.organizer.email_address.address
    },
    "attendees": {
        "required": [a for a in event.attendees if a.type == "required"],
        "optional": [a for a in event.attendees if a.type == "optional"]
    },
    "location": {
        "display_name": event.location.display_name,
        "type": event.location.location_type,
        "room": event.location.unique_id if hasattr(event.location, 'unique_id') else None
    },
    "online_meeting": {
        "join_url": event.online_meeting.join_url if event.online_meeting else None,
        "conference_id": event.online_meeting.conference_id if event.online_meeting else None
    },
    "series_info": {
        "is_recurring": event.recurrence is not None,
        "series_master_id": event.series_master_id,
        "occurrence_number": event.occurrence_number if hasattr(event, 'occurrence_number') else None
    },
    "body_preview": event.body_preview,
    "body_content": event.body.content,
    "categories": event.categories,
    "importance": event.importance,
    "sensitivity": event.sensitivity
}
```

### Google Calendar API

```python
event = service.events().get(calendarId='primary', eventId=event_id).execute()

metadata = {
    "rsvp_status": {
        att['email']: {
            "status": att.get('responseStatus'),
            "comment": att.get('comment'),
            "optional": att.get('optional', False)
        }
        for att in event.get('attendees', [])
    },
    "attachments": event.get('attachments', []),
    "organizer": event.get('organizer'),
    "conference_data": event.get('conferenceData'),
    "location": event.get('location'),
    "description": event.get('description'),
    "recurring_event_id": event.get('recurringEventId'),
    "extended_properties": event.get('extendedProperties', {})
}
```

---

## Summary: CAN-07 Correction

| Aspect | ❌ Old (Incorrect) | ✅ New (Correct) |
|--------|-------------------|------------------|
| **Name** | Meeting Invitation Sending | Meeting Metadata Extraction |
| **Type** | Redundant (duplicate of CAN-03) | Parent/Foundational Task |
| **Purpose** | Send invitations | Extract structured data from events |
| **Tier** | 2 | 2 |
| **Enables** | Nothing (redundant) | CAN-13, CAN-05, CAN-08, CAN-19, CAN-09 |
| **Depends On** | - | CAN-01 (Calendar Retrieval) |
| **Usage** | 0/9 prompts (correctly) | Should be 5-6/9 prompts |
| **Examples** | Send invitation (wrong) | Extract RSVP status, attachments, attendees |

---

## Action Items

1. ✅ **Update CANONICAL_UNIT_TASKS_REFERENCE.md**
   - Change CAN-07 name and description
   - Add dependency diagram
   - Add API implementation examples

2. ✅ **Update Gold Standard Analysis**
   - Add CAN-07 to 5 prompts: organizer-2, schedule-2, collaborate-1, collaborate-2, (optional: organizer-3)
   - Document dependency relationships

3. ✅ **Update Gap Analysis**
   - Correct explanation of why CAN-07 wasn't used
   - Show it as foundational task, not unused task

4. ✅ **Update Evaluation Summary**
   - Add CAN-07 to recommended corrections
   - Show proper usage patterns

---

**This redefinition transforms CAN-07 from a redundant task to a critical foundational capability that enables multiple downstream tasks.**
