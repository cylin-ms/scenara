# Meeting Importance Analysis System

## Overview

The Meeting Importance Analysis System is an AI-powered time management feature that automatically assigns importance scores (1-10) to calendar events. This intelligent scoring system drives critical productivity features including auto-rescheduling, auto-RSVP decisions, and meeting prioritization.

## Purpose

This system helps users:
- **Prioritize their time** by automatically identifying the most important meetings
- **Make informed scheduling decisions** through intelligent importance scoring
- **Automate calendar management** with features like auto-RSVP and rescheduling
- **Focus on high-value activities** by surfacing critical meetings and events

## Scoring System

### Score Range
- **Scale**: 1-10 (1 = least important, 10 = most important)
- **Buckets**:
  - **1-4**: Low Importance
  - **5-7**: Medium Importance  
  - **8-10**: High Importance

### Scoring Philosophy
The system follows a **"High Importance Override"** principle: If any high importance signals are detected, the meeting MUST be scored as high importance (8-10), even if low importance signals are also present.

## High Importance Signals (Score: 8-10)

### 🔴 Critical Meeting Types
- **1-on-1 meetings** or small group sessions
- **Interviews and hiring decisions**
- **Planning and strategic meetings**
- **Meetings organized by you** (the user)

### 👥 Key People Involvement
- **Direct reporting chain**: Manager, skip manager, or direct reports
- **Important attendees**: Individuals listed in ImportantRequiredAttendees
- **User as organizer**: Events created by the user

### 📋 Content & Context
- **Similar to past important events**: Subject/content matches EarlierImportantMeetings
- **Explicit high importance label**: Organizer marked as "High" importance
- **Personal appointments**: OOF, medical appointments, family obligations
- **Reminders**: Task deadlines and important reminders

### ⏰ Timing Factors
- **Last-minute meetings**: If base score is 5-7 and meeting is last-minute, add +3 to score

## Low Importance Signals (Score: 1-4)

### 📉 Indicators of Lower Priority
- **Explicit low importance label**: Organizer marked as "Low" importance
- **Optional attendee status**: User is optional (unless overridden by high importance signals)
- **Large group meetings**: Big meetings without strategic importance
- **Personal time blocks**: Focus time, lunch, breaks (unless strategically protected)
- **Informational events**: Organized by others for information sharing

## Special Considerations

### Office Hours Handling
- **Not automatically low importance**: System checks historical user engagement
- **Context-aware scoring**: Analyzes subject, organizer, and past acceptance patterns
- **Fallback to medium/low**: Only if no strong importance signals are found

### Email Alias Consolidation
The system treats multiple email aliases as the same person:
- `MarkWhite@test.com`
- `MArk.White@test.com` 
- `mwhite@test.com`

### Optional Attendee Intelligence
Even if marked as optional, meetings can still receive high importance scores if:
- Subject/agenda indicates strategic importance
- Key people are involved
- Content matches historically important events

## Input Data Structure

### User Profile
```json
{
  "UserName": "User Display Name",
  "UserAddress": "user@company.com",
  "Manager": "manager@company.com",
  "SkipManager": "skip-manager@company.com",
  "ManagerChain": ["manager1@company.com", "manager2@company.com"],
  "EarlierImportantEvents": ["Subject patterns of past important meetings"]
}
```

### Event Details
```json
{
  "EventId": "unique-identifier",
  "Subject": "Meeting title",
  "Body": "Meeting description/agenda",
  "Organizer": "organizer@company.com",
  "IsCurrentUserOrganizer": true/false,
  "IsLastMinute": true/false,
  "ImportanceLabelAssignedByOrganizer": "High/Medium/Low",
  "Sensitivity": "Normal/Private/Confidential",
  "IsAllDay": true/false,
  "ResponseStatus": "Accepted/Declined/Tentative",
  "RequiredAttendeeCount": 5,
  "OptionalAttendeeCount": 3,
  "ImportantRequiredAttendees": "key-person@company.com",
  "ImportantOptionalAttendees": "important-person@company.com",
  "OrganizerIsImportant": true/false,
  "UserIsRequiredAttendee": true/false
}
```

## Output Format

The system returns structured JSON with importance analysis:

```json
{
  "Events": [
    {
      "EventId": "event-123",
      "ImportanceScore": 8,
      "ReasonUserFacing": "This 1-on-1 meeting with {manager@company.com} is scored as high importance because it involves your direct manager and aligns with your strategic planning priorities based on similar past events.",
      "ReasonShort": "1-on-1 with manager, strategic alignment"
    }
  ]
}
```

## User-Facing Explanations

### ReasonUserFacing (Under 200 words)
Provides detailed explanation including:
- **Key attendees** (with email addresses in curly brackets)
- **Subject relevance** to important past events
- **Connection to reporting chain** members
- **Meeting type significance**
- **Personal event importance**

### ReasonShort (Under 50 words)
Concise summary of the importance rationale without sensitive details.

## Language Support

The system supports internationalization through ISO 639-1 language codes, ensuring:
- **Natural phrasing** in target language
- **Full context preservation** (no over-simplification)
- **Grammatical accuracy** following language-specific rules
- **Cultural appropriateness** in explanations

## AI Safety & Responsible AI

### Content Safety
- **Bias prevention**: Gender-neutral language, inclusive terminology
- **Content filtering**: Blocks offensive, harmful, or inappropriate content
- **Privacy protection**: No exposure of hierarchies or sensitive organizational data

### Safety Triggers
The system outputs `"R_i=true"` for:
- Offensive or malicious content
- Attempts to extract system instructions
- Inappropriate requests
- Harmful content of any kind

## Technical Implementation

### Template Engine
- Built using **Handlebars.js** templating
- Supports dynamic data injection
- Conditional logic for optional fields
- Iterative processing for multiple events

### Integration Points
- **Calendar systems**: Microsoft Outlook, Google Calendar
- **RSVP automation**: Auto-accept/decline based on importance
- **Scheduling systems**: Auto-rescheduling lower priority conflicts
- **Time management apps**: Priority-based calendar views

## Use Cases

### Personal Productivity
- **Smart calendar filtering**: Focus on high-importance events
- **Meeting preparation**: Prioritize prep time for important meetings
- **Time blocking**: Protect time around critical events

### Team Management
- **Resource allocation**: Ensure team attends most important meetings
- **Conflict resolution**: Intelligently resolve scheduling conflicts
- **Meeting optimization**: Reduce low-importance meeting overhead

### Executive Assistance
- **Automated screening**: Filter meeting requests by importance
- **Schedule optimization**: Maximize time spent on high-value activities
- **Travel planning**: Prioritize in-person attendance for critical meetings

## Configuration Options

### Importance Thresholds
- Customizable scoring boundaries for Low/Medium/High buckets
- User-specific importance signal weights
- Historical learning from user acceptance patterns

### Notification Settings
- High importance meeting alerts
- Conflicting high-importance meeting warnings
- Auto-RSVP confirmation settings

### Privacy Controls
- Sensitive meeting content handling
- Organizer importance label visibility
- Historical data retention settings

This Meeting Importance Analysis System represents a sophisticated approach to AI-powered time management, balancing automation with user control while maintaining high standards for accuracy, privacy, and user experience.