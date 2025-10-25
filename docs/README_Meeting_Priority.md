# Meeting Priority & Categorization System

## Overview

The Meeting Priority & Categorization System is an AI-powered scheduling intelligence feature that automatically categorizes calendar events into four distinct priority levels. This system helps users understand their meeting obligations and optimize their time allocation by providing clear guidance on which meetings require active participation, preparation, or can be deprioritized.

## Purpose

This system empowers users to:
- **Optimize time allocation** by clearly understanding meeting priorities
- **Reduce cognitive load** through automatic meeting categorization
- **Improve meeting preparation** by identifying which events require advance work
- **Enable selective attendance** by highlighting optional vs. critical meetings
- **Streamline calendar management** with intelligent priority-based views

## Meeting Categories

### 🔴 **Important**
**Definition**: Meetings that are critical for the user to attend and usually require preparation.

**Characteristics**:
- User is the organizer or organized by manager
- Involves key stakeholders and decision-making
- Typically accepted with high engagement expected
- Requires advance preparation and active participation
- Strategic or high-impact business discussions

**Examples**: 1-on-1s with manager, project planning, client presentations, team planning sessions

### 🟡 **Participant**
**Definition**: Meetings the user is expected to attend but do not require extensive preparation.

**Characteristics**:
- User is required but not driving the agenda
- Regular team meetings or status updates
- Typically accepted with passive participation expected
- Standard business operations meetings
- Information sharing or coordination sessions

**Examples**: Team standups, department meetings, training sessions, project status updates

### 🟢 **Flex** 
**Definition**: Optional meetings the user may attend if time permits.

**Characteristics**:
- User attendance is optional or beneficial but not critical
- Often have not responded or marked as tentative
- Learning opportunities or informational sessions
- Can be skipped if higher priorities arise
- Networking or community events

**Examples**: Optional training, company-wide announcements, social events, optional project reviews

### 🔵 **Follow**
**Definition**: Meetings the user does not need to attend but should follow up on.

**Characteristics**:
- Often include "Follow" in the subject line
- User may be tentatively accepted for awareness
- Information can be obtained through meeting notes or recordings
- Decisions or outcomes may impact user's work
- Monitoring for relevance without active participation

**Examples**: Project reviews in adjacent teams, executive briefings, stakeholder updates

## Categorization Logic

### Strong Priority Signals

#### **High Priority Indicators**:
- **IsOrganizer**: User is organizing the meeting
- **IsOrganizedByManager**: Manager is organizing the meeting
- **IsRequired**: User is marked as required attendee
- **UserFeedback**: Historical user feedback indicating importance
- **Manager Chain Involvement**: Manager, skip manager, or direct reports attending

#### **Medium Priority Indicators**:
- **Accepted Status**: User has accepted the meeting
- **Team Member Presence**: Colleagues or team members attending
- **Project Alignment**: Meeting tagged with user's active projects
- **Work Hours**: Meeting during user's preferred work hours

#### **Low Priority Indicators**:
- **Optional Status**: User marked as optional attendee
- **No Response**: User hasn't responded to invite
- **Large Groups**: High participant count diluting individual importance
- **Outside Hours**: Meeting outside preferred work schedule

### Decision Framework

```
if (IsOrganizer || IsOrganizedByManager || UserFeedback == "Important") {
    category = "Important"
    confidence = "High"
} else if (IsRequired && ResponseStatus == "Accepted") {
    category = "Participant" 
    confidence = "Medium"
} else if (ResponseStatus == "None" || "Optional") {
    category = "Flex"
    confidence = "Medium"
} else if (Subject.contains("Follow") || ResponseStatus == "Tentative") {
    category = "Follow"
    confidence = "Low"
}
```

## User Profile Integration

### Preference Categories

#### **WorkHourPreferences**
- **Preferred meeting times** and time zones
- **Focus time blocks** for deep work
- **Meeting-free periods** for preparation
- **Overtime tolerance** for critical meetings

#### **SchedulingPreferences** 
- **Meeting duration preferences** (30min vs 1hr)
- **Back-to-back meeting tolerance**
- **Advance notice requirements**
- **Recurring meeting patterns**

#### **PrioritizationPreferences**
- **Historical categorization patterns** from user feedback
- **Project importance rankings**
- **Stakeholder priority mappings**
- **Meeting type preferences** (1-on-1 vs group)

### Profile-Driven Intelligence

The system learns from user behavior:
- **Pattern Recognition**: If user consistently marks "Calendar.AI" meetings as Important, apply that pattern
- **Stakeholder Weighting**: Learn which organizers/attendees trigger higher importance
- **Subject Line Patterns**: Identify keywords that correlate with user's priority decisions
- **Response History**: Track acceptance patterns to infer meeting value

## Input Data Structure

### Meeting Metadata
```json
{
  "EventId": "unique-identifier",
  "Subject": "Meeting title",
  "IsOrganizer": true/false,
  "ResponseStatus": "Accepted/Declined/Tentative/None",
  "IsOrganizedByManager": true/false,
  "IsUserRequired": true/false,
  "ShowAs": "Busy/Free/Tentative/OutOfOffice",
  "ParticipantCount": 8,
  "Project": "project-identifier",
  "StartTime": "2025-10-20T14:00:00Z",
  "AttendanceDuration": "60 minutes",
  "EventType": "Meeting/Event/Appointment",
  "AttendeesFromManagerChain": 2,
  "AttendeesFromTeamMembers": 3,
  "AttendeesFromDirectReports": 1,
  "RemainingAttendeesCount": 2,
  "UserFeedback": "Important/Participant/Flex/Follow"
}
```

### User Profile
```json
{
  "PreferenceCategories": [
    {
      "Category": "PrioritizationPreferences",
      "Preferences": [
        {
          "Description": "Mark Calendar.AI meetings as Important",
          "Weight": 0.8,
          "Source": "User",
          "FeedbackStatus": "Confirmed"
        }
      ]
    }
  ]
}
```

## Output Format

```json
{
  "MeetingsWithCategory": [
    {
      "EventId": "event-123",
      "Category": "Important",
      "Confidence": "High",
      "Reasoning": "User is the organizer and meeting involves direct reports for strategic planning.",
      "Subject": "Q4 Team Planning Session"
    }
  ]
}
```

## Confidence Levels

### **High Confidence**
- Clear signals from multiple strong indicators
- Consistent with user's historical patterns
- Unambiguous categorization criteria met

### **Medium Confidence** 
- Some strong signals present but not conclusive
- Moderate alignment with user preferences
- Default choice when uncertain between Participant/Flex

### **Low Confidence**
- Weak or conflicting signals
- Limited historical data for comparison
- Edge cases requiring user validation

## AI Decision Rules

### Core Principles
1. **Strong Signal Priority**: Organizer status, manager involvement, explicit feedback override other factors
2. **User Feedback Authority**: Historical user categorization takes precedence
3. **Conservative Defaults**: When uncertain between Participant/Flex, choose Participant
4. **Profile Learning**: User-sourced preferences weighted higher than system-inferred patterns

### Edge Case Handling
- **Conflicting Signals**: Prioritize user feedback > organizer status > manager involvement
- **Missing Data**: Use participant count and response status as fallbacks
- **New Meeting Types**: Default to Participant until user feedback establishes pattern
- **Schedule Conflicts**: Consider timing preferences in confidence scoring

## Integration Applications

### Calendar Management
- **Priority-based views**: Filter calendar by importance level
- **Time blocking**: Protect time around Important meetings
- **Conflict resolution**: Auto-reschedule lower priority meetings

### Productivity Tools
- **Meeting preparation**: Allocate prep time for Important meetings
- **Agenda management**: Prioritize agenda items by meeting category
- **Follow-up tracking**: Set reminders for Follow category meetings

### Team Coordination
- **Delegation assistance**: Identify meetings that can be delegated
- **Coverage planning**: Arrange coverage for Important meetings during OOO
- **Meeting optimization**: Reduce unnecessary meeting attendance

## Use Cases

### Personal Productivity
- **Time optimization**: Focus on high-impact meetings
- **Preparation planning**: Allocate preparation time effectively
- **Energy management**: Balance Important vs. Participant meetings

### Executive Assistance
- **Calendar curation**: Filter meeting requests by priority
- **Scheduling optimization**: Protect time for critical activities
- **Meeting analytics**: Track time allocation across priority levels

### Team Management
- **Meeting effectiveness**: Ensure right people at right meetings
- **Resource allocation**: Distribute team time optimally
- **Decision tracking**: Monitor outcomes from Important meetings

## Performance Metrics

### Accuracy Measures
- **User feedback alignment**: Percentage of auto-categories matching user intent
- **Category stability**: Consistency of categorization for similar meetings
- **Confidence calibration**: Relationship between confidence scores and accuracy

### Business Impact
- **Time savings**: Reduction in time spent on low-priority meetings
- **Preparation efficiency**: Better allocation of meeting prep time
- **Decision velocity**: Faster prioritization decisions

### User Satisfaction
- **Category usefulness**: User ratings of categorization accuracy
- **Workflow integration**: Adoption of priority-based calendar views
- **Behavioral change**: Shift in meeting attendance patterns

This Meeting Priority & Categorization System transforms calendar management from reactive scheduling to proactive priority optimization, enabling users to make informed decisions about their time allocation and meeting engagement.