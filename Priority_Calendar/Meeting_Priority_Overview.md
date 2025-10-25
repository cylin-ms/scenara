# Meeting Priority System - Quick Reference

## What It Does
Automatically categorizes calendar meetings into 4 priority levels to help users optimize their time and understand meeting obligations.

## 4 Priority Categories

### 🔴 **Important** - Critical Attendance Required
- **Must attend** with preparation needed
- **User is organizer** or organized by manager
- **Key stakeholders** and decision-making involved
- **Examples**: 1-on-1s, strategic planning, client presentations

### 🟡 **Participant** - Expected Attendance  
- **Should attend** but minimal preparation
- **Required attendee** for routine business
- **Information sharing** and coordination
- **Examples**: Team standups, status meetings, training

### 🟢 **Flex** - Optional Attendance
- **May attend** if time permits
- **Optional or beneficial** but not critical
- **Learning opportunities** or networking
- **Examples**: Optional training, company events, social meetings

### 🔵 **Follow** - Monitor Only
- **Don't need to attend** but should follow up
- **Track outcomes** through notes/recordings
- **Often marked tentative** for awareness
- **Examples**: Adjacent team reviews, executive briefings

## Key Decision Factors

### 🎯 Strong Priority Signals
- **IsOrganizer**: You're running the meeting → Important
- **IsOrganizedByManager**: Manager organized → Important  
- **UserFeedback**: Historical user categorization → Follow pattern
- **IsRequired**: Marked as required → Participant
- **Manager Chain**: Manager/reports attending → Higher priority

### 📊 Supporting Signals
- **Response Status**: Accepted vs No Response
- **Participant Count**: Small groups = higher importance
- **Project Alignment**: Related to your active projects
- **Work Hours**: During vs outside preferred times
- **Team Members**: Colleagues attending

## Smart Features

### 🧠 Profile Learning
- **Pattern Recognition**: Learns from your categorization history
- **Stakeholder Intelligence**: Remembers which organizers you prioritize
- **Subject Keywords**: Identifies importance triggers in meeting titles
- **Time Preferences**: Considers your work hour preferences

### 🔄 Adaptive Categorization
- **User Feedback Loop**: Improves accuracy based on corrections
- **Context Awareness**: Considers meeting timing and duration
- **Conservative Defaults**: When uncertain, defaults to "Participant"
- **Multi-signal Integration**: Combines multiple indicators for accuracy

## Output Format
```json
{
  "EventId": "meeting-123",
  "Category": "Important",
  "Confidence": "High", 
  "Reasoning": "You are the organizer with direct reports attending",
  "Subject": "Team Planning Session"
}
```

## Confidence Levels
- **High**: Clear signals, consistent with patterns
- **Medium**: Some indicators, moderate certainty  
- **Low**: Weak signals, needs user validation

## Use Cases

### 📅 Calendar Management
- **Priority Views**: Filter by importance level
- **Time Blocking**: Protect prep time for Important meetings
- **Conflict Resolution**: Auto-reschedule lower priority items

### ⚡ Productivity
- **Meeting Prep**: Allocate preparation time intelligently
- **Energy Management**: Balance high vs low engagement meetings
- **Focus Protection**: Minimize disruption to deep work

### 👥 Team Coordination  
- **Delegation**: Identify meetings others can attend
- **Coverage Planning**: Ensure Important meetings are covered
- **Meeting Optimization**: Reduce unnecessary attendance

## Integration Benefits
- **Smart Scheduling**: Automatically prioritize meeting requests
- **Preparation Alerts**: Notify before Important meetings need prep
- **Analytics**: Track time allocation across priority levels
- **Decision Support**: Guide accept/decline decisions

This system transforms reactive calendar management into proactive priority optimization, helping you focus on what matters most.