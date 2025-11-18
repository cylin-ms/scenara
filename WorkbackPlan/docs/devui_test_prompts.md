# BizChat DevUI Test Prompts for Workback Planning

**Generated**: 2025-11-18T13:45:22.164999
**Purpose**: Test prompts based on real meetings from past 6 months

---

## Test Prompt 1: Board Review Meeting

**Complexity**: high
**Lead Time**: 60 days
**Description**: High-stakes quarterly board meeting requiring executive preparation

**Status**: ❌ No matching meeting found (use synthetic example)

### BizChat Prompt

```
# No Board Review Meeting found in your calendar

Create a synthetic example for testing.
```

### Expected Tool Calls

Based on this prompt, ContextFlow should capture:
- `graph_calendar_get_events` - Retrieve meeting details
- `graph_get_people` - Get attendee information
- `bizchat_context` - Gather contextual information
- `bizchat_recommendations` - Get related content
- Potentially other tools based on meeting type

---

## Test Prompt 2: Quarterly Business Review (QBR)

**Complexity**: high
**Lead Time**: 45 days
**Description**: Strategic performance review with executives and stakeholders

### Real Meeting Example

```
Subject: STCA Monthly Extended PLT + Managers 
Date: 2025-08-01T10:35:00.0000000
Attendees (180): Yingqin Gu, Yi Shao, Yingfang Wang, Xinyu Liu, Vincent Fan, ... and 175 more
Description: Moving out for a week due to conflict.
Starting this month, monthly PLT meeting and Quarterly Manager Q&A are combined. Agenda will be sent via email prior to each meeting.

_______________________...
```

### BizChat Prompt

```
I have an upcoming quarterly business review (qbr) titled "STCA Monthly Extended PLT + Managers " scheduled for the scheduled date. 

This is a high-complexity meeting that typically requires 45 days of preparation time.

Can you help me create a detailed workback plan that includes:
1. All key milestones leading up to the meeting
2. Specific tasks with owners and deadlines
3. Dependencies between tasks
4. Critical path activities
5. Risk mitigation strategies

Please consider:
- The meeting requires coordination across multiple teams
- There are likely dependencies on deliverables and approvals
- We need to ensure adequate time for review cycles
- Executive-level stakeholders will be involved

Generate a comprehensive workback plan that ensures successful meeting preparation.
```

### Expected Tool Calls

Based on this prompt, ContextFlow should capture:
- `graph_calendar_get_events` - Retrieve meeting details
- `graph_get_people` - Get attendee information
- `bizchat_context` - Gather contextual information
- `bizchat_recommendations` - Get related content
- Potentially other tools based on meeting type

---

## Test Prompt 3: Product Launch

**Complexity**: high
**Lead Time**: 90 days
**Description**: Cross-functional product launch requiring coordinated activities

### Real Meeting Example

```
Subject: How-to Navigate M365 Pulse: A 101 Beginner’s Guide
Date: 2025-05-15T07:05:00.0000000
Attendees (374): Mahima Srinivasan, ENGAGE_M365Core, M365 Core All, M365 Core, Rob Seth, ... and 369 more
Description: ________________________________
From: Mahima Srinivasan <mahima.srinivasan@microsoft.com>
Sent: 08 May 2025 17:33
To: M365 Core All <M365CoreFTE@microsoft.com>; M365 Core <perryc_org_fte@microsoft...
```

### BizChat Prompt

```
I have an upcoming product launch titled "How-to Navigate M365 Pulse: A 101 Beginner’s Guide" scheduled for the scheduled date. 

This is a high-complexity meeting that typically requires 90 days of preparation time.

Can you help me create a detailed workback plan that includes:
1. All key milestones leading up to the meeting
2. Specific tasks with owners and deadlines
3. Dependencies between tasks
4. Critical path activities
5. Risk mitigation strategies

Please consider:
- The meeting requires coordination across multiple teams
- There are likely dependencies on deliverables and approvals
- We need to ensure adequate time for review cycles
- Executive-level stakeholders will be involved

Generate a comprehensive workback plan that ensures successful meeting preparation.
```

### Expected Tool Calls

Based on this prompt, ContextFlow should capture:
- `graph_calendar_get_events` - Retrieve meeting details
- `graph_get_people` - Get attendee information
- `bizchat_context` - Gather contextual information
- `bizchat_recommendations` - Get related content
- Potentially other tools based on meeting type

---

## Test Prompt 4: M&A Due Diligence

**Complexity**: high
**Lead Time**: 120 days
**Description**: Complex due diligence process for mergers and acquisitions

**Status**: ❌ No matching meeting found (use synthetic example)

### BizChat Prompt

```
# No M&A Due Diligence found in your calendar

Create a synthetic example for testing.
```

### Expected Tool Calls

Based on this prompt, ContextFlow should capture:
- `graph_calendar_get_events` - Retrieve meeting details
- `graph_get_people` - Get attendee information
- `bizchat_context` - Gather contextual information
- `bizchat_recommendations` - Get related content
- Potentially other tools based on meeting type

---

## Test Prompt 5: Team Offsite Planning

**Complexity**: medium
**Lead Time**: 30 days
**Description**: Strategic team planning session requiring logistics and agenda

**Status**: ❌ No matching meeting found (use synthetic example)

### BizChat Prompt

```
# No Team Offsite Planning found in your calendar

Create a synthetic example for testing.
```

### Expected Tool Calls

Based on this prompt, ContextFlow should capture:
- `graph_calendar_get_events` - Retrieve meeting details
- `graph_get_people` - Get attendee information
- `bizchat_context` - Gather contextual information
- `bizchat_recommendations` - Get related content
- Potentially other tools based on meeting type

---

## Test Prompt 6: Conference/Event Preparation

**Complexity**: medium
**Lead Time**: 45 days
**Description**: External conference requiring materials and speaker preparation

### Real Meeting Example

```
Subject: E+D: FY26 Kickoff
Date: 2025-07-18T01:05:00.0000000
Attendees (404): Experiences + Devices Exec Mgmt, BIC Org FTE - All, Caroline Gaffney, Experiences + Devices All FTE, E+D Exec Office, ... and 399 more
Description: E+D FY26 Kickoff

Join us live at aka.ms/ExDevent


Please join Rajesh and E+D leaders for our live FY26 Kickoff event. Rajesh will share updates on our E+D mission, strategy, priorities, culture...
```

### BizChat Prompt

```
I have an upcoming conference/event preparation titled "E+D: FY26 Kickoff" scheduled for the scheduled date. 

This is a medium-complexity meeting that typically requires 45 days of preparation time.

Can you help me create a detailed workback plan that includes:
1. All key milestones leading up to the meeting
2. Specific tasks with owners and deadlines
3. Dependencies between tasks
4. Critical path activities
5. Risk mitigation strategies

Please consider:
- The meeting requires coordination across multiple teams
- There are likely dependencies on deliverables and approvals
- We need to ensure adequate time for review cycles
- Executive-level stakeholders will be involved

Generate a comprehensive workback plan that ensures successful meeting preparation.
```

### Expected Tool Calls

Based on this prompt, ContextFlow should capture:
- `graph_calendar_get_events` - Retrieve meeting details
- `graph_get_people` - Get attendee information
- `bizchat_context` - Gather contextual information
- `bizchat_recommendations` - Get related content
- Potentially other tools based on meeting type

---

## Test Prompt 7: Executive Presentation

**Complexity**: medium
**Lead Time**: 21 days
**Description**: High-visibility presentation to executive leadership

### Real Meeting Example

```
Subject: LIVE! FY26 Employee Town Hall in September
Date: 2025-09-12T00:30:00.0000000
Attendees (364): Employee News & Events, Microsoft- Global Employees Extended (FTE), All FTEs in Canada, Harley Santana, Lauren Ciha, ... and 359 more
Description: Updated date and time
FY26 Employee Town Hall in September
Join us for the next Employee Town Hall, an opportunity for you to hear directly from Satya and the senior leadership team about what is to...
```

### BizChat Prompt

```
I have an upcoming executive presentation titled "LIVE! FY26 Employee Town Hall in September" scheduled for the scheduled date. 

This is a medium-complexity meeting that typically requires 21 days of preparation time.

Can you help me create a detailed workback plan that includes:
1. All key milestones leading up to the meeting
2. Specific tasks with owners and deadlines
3. Dependencies between tasks
4. Critical path activities
5. Risk mitigation strategies

Please consider:
- The meeting requires coordination across multiple teams
- There are likely dependencies on deliverables and approvals
- We need to ensure adequate time for review cycles
- Executive-level stakeholders will be involved

Generate a comprehensive workback plan that ensures successful meeting preparation.
```

### Expected Tool Calls

Based on this prompt, ContextFlow should capture:
- `graph_calendar_get_events` - Retrieve meeting details
- `graph_get_people` - Get attendee information
- `bizchat_context` - Gather contextual information
- `bizchat_recommendations` - Get related content
- Potentially other tools based on meeting type

---

## Test Prompt 8: Project Kickoff

**Complexity**: medium
**Lead Time**: 14 days
**Description**: Project initialization requiring team alignment and planning

### Real Meeting Example

```
Subject: E+D: FY26 Kickoff
Date: 2025-07-18T01:05:00.0000000
Attendees (404): Experiences + Devices Exec Mgmt, BIC Org FTE - All, Caroline Gaffney, Experiences + Devices All FTE, E+D Exec Office, ... and 399 more
Description: E+D FY26 Kickoff

Join us live at aka.ms/ExDevent


Please join Rajesh and E+D leaders for our live FY26 Kickoff event. Rajesh will share updates on our E+D mission, strategy, priorities, culture...
```

### BizChat Prompt

```
I have an upcoming project kickoff titled "E+D: FY26 Kickoff" scheduled for the scheduled date. 

This is a medium-complexity meeting that typically requires 14 days of preparation time.

Can you help me create a detailed workback plan that includes:
1. All key milestones leading up to the meeting
2. Specific tasks with owners and deadlines
3. Dependencies between tasks
4. Critical path activities
5. Risk mitigation strategies

Please consider:
- The meeting requires coordination across multiple teams
- There are likely dependencies on deliverables and approvals
- We need to ensure adequate time for review cycles
- Executive-level stakeholders will be involved

Generate a comprehensive workback plan that ensures successful meeting preparation.
```

### Expected Tool Calls

Based on this prompt, ContextFlow should capture:
- `graph_calendar_get_events` - Retrieve meeting details
- `graph_get_people` - Get attendee information
- `bizchat_context` - Gather contextual information
- `bizchat_recommendations` - Get related content
- Potentially other tools based on meeting type

---

## Test Prompt 9: Budget Planning

**Complexity**: medium
**Lead Time**: 30 days
**Description**: Annual or quarterly budget planning process

### Real Meeting Example

```
Subject: E+D: FY26 Kickoff
Date: 2025-07-18T01:05:00.0000000
Attendees (404): Experiences + Devices Exec Mgmt, BIC Org FTE - All, Caroline Gaffney, Experiences + Devices All FTE, E+D Exec Office, ... and 399 more
Description: E+D FY26 Kickoff

Join us live at aka.ms/ExDevent


Please join Rajesh and E+D leaders for our live FY26 Kickoff event. Rajesh will share updates on our E+D mission, strategy, priorities, culture...
```

### BizChat Prompt

```
I have an upcoming budget planning titled "E+D: FY26 Kickoff" scheduled for the scheduled date. 

This is a medium-complexity meeting that typically requires 30 days of preparation time.

Can you help me create a detailed workback plan that includes:
1. All key milestones leading up to the meeting
2. Specific tasks with owners and deadlines
3. Dependencies between tasks
4. Critical path activities
5. Risk mitigation strategies

Please consider:
- The meeting requires coordination across multiple teams
- There are likely dependencies on deliverables and approvals
- We need to ensure adequate time for review cycles
- Executive-level stakeholders will be involved

Generate a comprehensive workback plan that ensures successful meeting preparation.
```

### Expected Tool Calls

Based on this prompt, ContextFlow should capture:
- `graph_calendar_get_events` - Retrieve meeting details
- `graph_get_people` - Get attendee information
- `bizchat_context` - Gather contextual information
- `bizchat_recommendations` - Get related content
- Potentially other tools based on meeting type

---

## Test Prompt 10: Hiring Committee

**Complexity**: low
**Lead Time**: 7 days
**Description**: Interview process requiring coordination and preparation

### Real Meeting Example

```
Subject: Virtual Interview for Senior Applied Scientist(LLM) (1864549)
Date: 2025-10-24T15:00:00.0000000
Attendees (4): Microsoft Recruit, Chin-Yew Lin, Maggie Wang (HR), Coco Li (RANDSTAD NORTH AMERICA INC)
Description: Hi Interview Team,



Please confirm your availability to interview Ting-An Chen for the position of Senior Applied Scientist(LLM) (1864549) on October 24th, 2025.


We value you, your insights...
```

### BizChat Prompt

```
I have an upcoming hiring committee titled "Virtual Interview for Senior Applied Scientist(LLM) (1864549)" scheduled for the scheduled date. 

This is a low-complexity meeting that typically requires 7 days of preparation time.

Can you help me create a detailed workback plan that includes:
1. All key milestones leading up to the meeting
2. Specific tasks with owners and deadlines
3. Dependencies between tasks
4. Critical path activities
5. Risk mitigation strategies

Please consider:
- The meeting requires coordination across multiple teams
- There are likely dependencies on deliverables and approvals
- We need to ensure adequate time for review cycles
- Executive-level stakeholders will be involved

Generate a comprehensive workback plan that ensures successful meeting preparation.
```

### Expected Tool Calls

Based on this prompt, ContextFlow should capture:
- `graph_calendar_get_events` - Retrieve meeting details
- `graph_get_people` - Get attendee information
- `bizchat_context` - Gather contextual information
- `bizchat_recommendations` - Get related content
- Potentially other tools based on meeting type

---

