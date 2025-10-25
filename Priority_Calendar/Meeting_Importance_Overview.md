# Meeting Importance Analysis - Quick Reference

## What It Does
Automatically scores calendar events 1-10 for importance to drive smart scheduling decisions like auto-RSVP and meeting prioritization.

## Key Features

### 🎯 Smart Scoring
- **1-4**: Low Importance
- **5-7**: Medium Importance  
- **8-10**: High Importance

### 🔍 High Importance Triggers
- 1-on-1 meetings
- Manager/reporting chain involvement
- User-organized events
- Strategic/planning meetings
- Personal appointments (OOF, medical)
- Last-minute critical meetings

### 📊 What It Analyzes
- **People**: Organizer, attendees, reporting relationships
- **Content**: Subject similarity to past important events
- **Context**: Meeting type, urgency, user role
- **History**: Past acceptance patterns and preferences

### 🚀 Applications
- **Auto-RSVP**: Accept/decline based on importance
- **Smart Scheduling**: Resolve conflicts intelligently
- **Priority Views**: Focus on what matters most
- **Meeting Prep**: Allocate preparation time effectively

## Input Data
- User profile (manager chain, important contacts)
- Event details (subject, body, attendees, timing)
- Historical important meeting patterns
- Organizer-assigned importance labels

## Output
```json
{
  "EventId": "123",
  "ImportanceScore": 8,
  "ReasonUserFacing": "Detailed explanation...",
  "ReasonShort": "Brief summary"
}
```

## Smart Features

### 🧠 Intelligent Overrides
- High importance signals always win
- Last-minute meetings get +3 boost
- Optional status doesn't override strategic importance

### 🌐 Multi-language Support
- Explanations in user's preferred language
- Culturally appropriate phrasing
- Full context preservation

### 🔒 Privacy & Safety
- No bias in scoring decisions
- Sensitive content protection
- Inclusive language usage

This system transforms calendar management from reactive to proactive, helping users focus on their most impactful activities.