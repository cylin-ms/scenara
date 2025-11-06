# Consolidated GUTT Reference - Complete Inventory

**Date**: November 6, 2025  
**Purpose**: Detailed reference for all 39 consolidated atomic capabilities (C-GUTTs)  
**Source**: Cross-prompt consolidation analysis of 66 original GUTTs

---

## How to Use This Reference

Each C-GUTT entry follows this template:
- **C-GUTT-XX: Capability Name**
- **What it does**: Brief description of the capability
- **Used in**: Which hero prompts use this capability
- **Example**: Concrete example showing the capability in action
- **Type**: Category/classification of the capability

---

## Category 1: Calendar Data Operations (7 capabilities)

### C-GUTT-01: Calendar Event Retrieval
- **What it does**: Access and load calendar events with flexible filtering (pending, confirmed, date range, participants)
- **Used in**: Prompts 1 (Calendar Prioritization), 2 (Meeting Prep Tracking), 3 (Time Reclamation), 5 (Block Time & Reschedule), 9 (Customer Meeting Prep)
- **Example**: User asks "show my meetings this week" → retrieves all events from calendar API with date filter 2025-11-06 to 2025-11-12
- **Type**: Calendar API integration capability

### C-GUTT-02: Multi-Calendar Availability Checking
- **What it does**: Query free/busy status across multiple users' calendars
- **Used in**: Prompts 4 (Recurring 1:1 Scheduling), 5 (Block Time & Reschedule), 6 (Multi-Person Scheduling)
- **Example**: Finding time for user + 3 colleagues → checks all 4 calendars simultaneously, returns overlapping free slots
- **Type**: Calendar API integration capability

### C-GUTT-03: Meeting Type Classification
- **What it does**: Classify meetings by type (1:1, group, lunch, review, etc.) from 31+ taxonomy
- **Used in**: Prompts 3 (Time Reclamation), 6 (Multi-Person Scheduling)
- **Example**: Meeting with 2 attendees, 30 min duration, title "Weekly Sync" → classified as "1:1" type
- **Type**: Machine learning classification capability

### C-GUTT-04: Meeting Importance Classification
- **What it does**: Determine meeting importance level (critical, high, medium, low) based on attendees, topics, urgency
- **Used in**: Prompt 2 (Meeting Prep Tracking)
- **Example**: Meeting with VP, "Q4 Strategy Review" title, 2-hour duration → classified as "critical" importance
- **Type**: Machine learning classification capability

### C-GUTT-05: Calendar Action Execution (RSVP)
- **What it does**: Execute accept/decline/tentative RSVP actions on calendar events
- **Used in**: Prompts 1 (Calendar Prioritization), 5 (Block Time & Reschedule)
- **Example**: User declines low-priority meeting → sends RSVP "declined" via Calendar API `PATCH /events/{id}` with responseStatus update
- **Type**: Calendar API write operation capability

### C-GUTT-06: Meeting Creation & Invitations
- **What it does**: Create calendar events and send invitations to attendees
- **Used in**: Prompts 4 (Recurring 1:1 Scheduling), 6 (Multi-Person Scheduling)
- **Example**: Create weekly 1:1 with John, Tuesdays 2pm → creates recurring event with RRULE, sends invitation to John
- **Type**: Calendar API write operation capability

### C-GUTT-07: Meeting Update & Rescheduling
- **What it does**: Modify existing meetings (time, attendees, location) and notify participants
- **Used in**: Prompts 4 (Recurring 1:1), 5 (Block Time & Reschedule), 6 (Multi-Person Scheduling)
- **Example**: Meeting declined → finds new time slot, updates event from 2pm to 4pm, sends notifications to all attendees
- **Type**: Calendar API write operation capability

---

## Category 2: Natural Language Processing (8 capabilities)

### C-GUTT-08: Priority/Goal Extraction
- **What it does**: Parse user's stated priorities, goals, and preferences from natural language
- **Used in**: Prompts 1 (Calendar Prioritization), 3 (Time Reclamation)
- **Example**: User says "I want to focus on customer meetings and product strategy" → extracts and structures these as priorities: ["customer meetings", "product strategy"]
- **Type**: NLP extraction capability

### C-GUTT-09: Constraint & Requirement Parsing
- **What it does**: Extract scheduling constraints (time preferences, hard requirements, attendee rules)
- **Used in**: Prompts 4 (Recurring 1:1 Scheduling), 6 (Multi-Person Scheduling)
- **Example**: "Weekly 30min with Sarah, afternoons preferred, avoid Fridays" → extracts: recurrence=weekly, duration=30min, attendee=Sarah, preferred=afternoons, exclude=Fridays
- **Type**: NLP extraction capability

### C-GUTT-10: Temporal Expression Resolution
- **What it does**: Interpret relative time expressions ("Thursday afternoon", "next week") to absolute date/time
- **Used in**: Prompt 5 (Block Time & Reschedule)
- **Example**: "Clear my Thursday afternoon" on Nov 6, 2025 → resolves to date=2025-11-07, time=13:00-17:00
- **Type**: NLP temporal parsing capability

### C-GUTT-11: Meeting Context Extraction
- **What it does**: Extract meeting purpose, topics, and context from documents/calendar metadata
- **Used in**: Prompts 7 (Agenda Creation), 8 (Executive Briefing), 9 (Customer Meeting Prep)
- **Example**: Calendar event titled "Project Alpha Review" with attached docs → extracts context: project=Alpha, purpose=review, topics=[milestones, blockers, risks]
- **Type**: NLP information extraction capability

### C-GUTT-12: Stakeholder/Role Identification
- **What it does**: Identify participants, their roles, and organizational relationships
- **Used in**: Prompts 7 (Agenda Creation), 9 (Customer Meeting Prep)
- **Example**: Meeting attendees: [Sarah Chen, Mike Jones] → resolves to Sarah=Product Manager, Mike=Marketing Director, relationship=cross-functional
- **Type**: NLP entity resolution capability

### C-GUTT-13: Interest/Topic Analysis
- **What it does**: Analyze individual preferences, interests, and communication patterns
- **Used in**: Prompt 9 (Customer Meeting Prep)
- **Example**: Customer contact history shows frequent emails about "API performance" and "scaling" → identifies interests: [API optimization, infrastructure scaling]
- **Type**: NLP pattern analysis capability

### C-GUTT-14: Document Content Analysis
- **What it does**: Load, parse, and extract key information from documents
- **Used in**: Prompts 8 (Executive Briefing), 9 (Customer Meeting Prep)
- **Example**: Loads 3 PDF files + 5 emails for meeting → extracts key topics, decisions needed, action items from all documents
- **Type**: Document processing capability

### C-GUTT-15: Summary & Distillation
- **What it does**: Condense complex information into concise summaries
- **Used in**: Prompt 8 (Executive Briefing)
- **Example**: 50-page technical report → distills to 3 executive discussion points: 1) Timeline risk, 2) Budget increase needed, 3) Partner dependency
- **Type**: LLM summarization capability

---

## Category 3: Reasoning & Decision Making (7 capabilities)

### C-GUTT-16: Priority Alignment Scoring
- **What it does**: Evaluate how well meetings/activities align with user's priorities
- **Used in**: Prompts 1 (Calendar Prioritization), 3 (Time Reclamation)
- **Example**: Meeting about "Q4 product roadmap" scored against priority "product strategy" → alignment score: 0.95 (high)
- **Type**: Semantic matching capability

### C-GUTT-17: Decision Logic (Accept/Decline)
- **What it does**: Make threshold-based decisions on calendar actions
- **Used in**: Prompt 1 (Calendar Prioritization)
- **Example**: Meeting with alignment score 0.95 exceeds threshold 0.7 → decision: ACCEPT; meeting with score 0.3 → decision: DECLINE
- **Type**: Rule-based decision engine

### C-GUTT-18: Preparation Time Estimation
- **What it does**: Estimate how much prep time a meeting requires based on type/attendees/complexity
- **Used in**: Prompt 2 (Meeting Prep Tracking)
- **Example**: Executive review meeting with 10 slides, VP attendee → estimates 2 hours prep time needed
- **Type**: Machine learning estimation capability

### C-GUTT-19: Constraint Satisfaction & Slot Finding
- **What it does**: Find time slots satisfying multiple constraints (availability, preferences, resources)
- **Used in**: Prompts 4 (Recurring 1:1), 5 (Block Time & Reschedule), 6 (Multi-Person Scheduling)
- **Example**: Find time for 4 people, 1 hour, next 2 weeks, afternoons preferred, needs conference room → returns ranked list of 5 valid slots
- **Type**: Constraint satisfaction solver capability

### C-GUTT-20: Conflict Detection & Resolution
- **What it does**: Detect calendar conflicts and determine resolution strategy
- **Used in**: Prompts 4 (Recurring 1:1), 6 (Multi-Person Scheduling)
- **Example**: Proposed meeting conflicts with existing 1:1 → identifies 1:1 as "override-eligible", proposes rescheduling the 1:1
- **Type**: Conflict analysis capability

### C-GUTT-21: Objection/Risk Anticipation
- **What it does**: Predict concerns, blockers, or objections from stakeholders
- **Used in**: Prompts 7 (Agenda Creation), 8 (Executive Briefing)
- **Example**: Budget increase proposal for executives → anticipates objections: "ROI unclear", "Timeline aggressive", "Why not phase it?"
- **Type**: LLM critical reasoning capability

### C-GUTT-22: Response/Recommendation Generation
- **What it does**: Generate actionable recommendations or responses to anticipated concerns
- **Used in**: Prompts 3 (Time Reclamation), 8 (Executive Briefing)
- **Example**: Time reclamation analysis shows 10 hrs/week in low-value meetings → recommends: "Decline 3 recurring status meetings, delegate 2 reviews"
- **Type**: LLM recommendation capability

---

## Category 4: Analysis & Insights (5 capabilities)

### C-GUTT-23: Time Aggregation & Statistics
- **What it does**: Compute time spent across categories, calculate statistics, identify patterns
- **Used in**: Prompt 3 (Time Reclamation)
- **Example**: Analyzes 30 days of calendar history → computes: 40% in 1:1s (12 hrs/week), 30% in group meetings (9 hrs/week), 20% in reviews (6 hrs/week)
- **Type**: Analytics capability

### C-GUTT-24: Low-Value Activity Identification
- **What it does**: Flag meetings/activities that don't support priorities (reclamation candidates)
- **Used in**: Prompt 3 (Time Reclamation)
- **Example**: User priority is "customer meetings", recurring "Team Happy Hour" has alignment score 0.1 → flagged as low-value, reclamation candidate
- **Type**: Analysis capability

### C-GUTT-25: Time Reclamation Opportunity Analysis
- **What it does**: Calculate potential time savings from proposed changes
- **Used in**: Prompt 3 (Time Reclamation)
- **Example**: Declining 3 weekly status meetings (1hr each) → calculates time savings: 3 hrs/week, 12 hrs/month, 144 hrs/year
- **Type**: Impact modeling capability

### C-GUTT-26: Meeting Flagging Logic
- **What it does**: Apply rules to flag meetings meeting specific criteria (needs prep, high importance, etc.)
- **Used in**: Prompt 2 (Meeting Prep Tracking)
- **Example**: Meeting has importance=critical AND prep_time_estimate>1hr AND lead_time<24hrs → flags as "needs urgent prep"
- **Type**: Rule-based flagging capability

### C-GUTT-27: Calendar Gap Analysis
- **What it does**: Identify free time blocks in calendar for scheduling purposes
- **Used in**: Prompt 2 (Meeting Prep Tracking)
- **Example**: Meeting flagged as needing 2hrs prep, scheduled for Friday 2pm → finds gaps: Thursday 10am-12pm (2hr block available)
- **Type**: Temporal analysis capability

---

## Category 5: Resource Management (3 capabilities)

### C-GUTT-28: Conference Room Search & Booking
- **What it does**: Find and reserve meeting rooms based on capacity, location, equipment needs
- **Used in**: Prompt 6 (Multi-Person Scheduling)
- **Example**: In-person meeting for 5 people, needs projector, Building 41 → searches room resources, finds "Conf Room B41-3A", reserves it
- **Type**: Resource management capability

### C-GUTT-29: Focus Time Block Scheduling
- **What it does**: Create dedicated focus/prep time blocks on calendar
- **Used in**: Prompts 2 (Meeting Prep Tracking), 5 (Block Time & Reschedule)
- **Example**: Meeting needs 2hrs prep → creates calendar event "Focus Time: Prepare for Q4 Review" on Thursday 10am-12pm
- **Type**: Calendar blocking capability

### C-GUTT-30: Calendar Status/Availability Update
- **What it does**: Set user's free/busy status and availability indicators
- **Used in**: Prompt 5 (Block Time & Reschedule)
- **Example**: User blocks Thursday afternoon → sets calendar status to "Busy" for 13:00-17:00, others see as unavailable
- **Type**: Calendar status management capability

---

## Category 6: Output & Communication (3 capabilities)

### C-GUTT-31: Decision Justification & Explanation
- **What it does**: Generate natural language explanations for automated decisions
- **Used in**: Prompt 1 (Calendar Prioritization)
- **Example**: Meeting auto-declined → explains: "Declined 'Weekly Status Sync' - alignment score 0.2 below threshold 0.7. Does not support priority: customer meetings"
- **Type**: Natural language generation capability

### C-GUTT-32: Reporting & Visualization
- **What it does**: Create reports, summaries, and visual representations of data/actions
- **Used in**: Prompts 2 (Meeting Prep), 3 (Time Reclamation), 5 (Block Time & Reschedule)
- **Example**: Time reclamation analysis → generates report with pie chart (time by category), bar chart (top time consumers), summary table with recommendations
- **Type**: Report generation capability

### C-GUTT-33: Document Assembly & Formatting
- **What it does**: Compile information into structured documents (agendas, briefs, dossiers)
- **Used in**: Prompts 7 (Agenda Creation), 8 (Executive Briefing), 9 (Customer Meeting Prep)
- **Example**: Customer meeting prep → assembles brief with sections: Company Overview, Attendee Dossiers, Topics of Interest, Relationship History, Action Items
- **Type**: Document generation capability

---

## Category 7: Specialized Collaboration Capabilities (6 capabilities)

### C-GUTT-34: Agenda Structure Planning
- **What it does**: Meeting flow design and structure creation
- **Used in**: Prompt 7 (Agenda Creation)
- **Example**: Project review meeting → designs structure: 1) Progress Update (15min), 2) Milestone Confirmation (10min), 3) Blockers Discussion (20min), 4) Risk Review (15min)
- **Type**: Meeting planning capability

### C-GUTT-35: Agenda Item Generation
- **What it does**: Generate specific discussion topics and content
- **Used in**: Prompt 7 (Agenda Creation)
- **Example**: Project Alpha progress review → generates items: "Demo new login flow", "Confirm API release date", "Discuss vendor dependency risk"
- **Type**: Content generation capability

### C-GUTT-36: Audience-Aware Communication
- **What it does**: Adapt messaging for specific audiences (executives, customers)
- **Used in**: Prompt 8 (Executive Briefing)
- **Example**: Technical architecture details → reframes for executives: "Migration to new platform enables 10x scaling, reduces costs 30%, delivery Q2 2026"
- **Type**: Communication framing capability

### C-GUTT-37: External Research & Enrichment
- **What it does**: Web research and CRM data aggregation
- **Used in**: Prompt 9 (Customer Meeting Prep)
- **Example**: Customer "Acme Corp" → searches web for recent news, retrieves CRM data for company profile, revenue, industry, recent deals
- **Type**: Information retrieval capability

### C-GUTT-38: Profile Compilation
- **What it does**: Individual dossier/profile building
- **Used in**: Prompt 9 (Customer Meeting Prep)
- **Example**: Meeting attendee "Jane Smith, Acme VP Engineering" → compiles: role, background, LinkedIn profile, past interactions, topics of interest
- **Type**: Profile building capability

### C-GUTT-39: Relationship History Analysis
- **What it does**: Timeline creation from interaction history
- **Used in**: Prompt 9 (Customer Meeting Prep)
- **Example**: Customer relationship with Acme Corp → creates timeline: Initial contact (Jan 2024), Pilot project (Mar 2024), Support ticket (Aug 2024), Renewal discussion (Oct 2024)
- **Type**: Historical analysis capability

---

## Quick Reference: C-GUTT ID to Capability Mapping

| C-GUTT ID | Capability Name | Category | Reuse Count |
|-----------|----------------|----------|-------------|
| C-01 | Calendar Event Retrieval | Calendar Data | 5 prompts |
| C-02 | Multi-Calendar Availability Checking | Calendar Data | 3 prompts |
| C-03 | Meeting Type Classification | Calendar Data | 2 prompts |
| C-04 | Meeting Importance Classification | Calendar Data | 1 prompt |
| C-05 | Calendar Action Execution (RSVP) | Calendar Data | 2 prompts |
| C-06 | Meeting Creation & Invitations | Calendar Data | 2 prompts |
| C-07 | Meeting Update & Rescheduling | Calendar Data | 3 prompts |
| C-08 | Priority/Goal Extraction | NLP | 2 prompts |
| C-09 | Constraint & Requirement Parsing | NLP | 2 prompts |
| C-10 | Temporal Expression Resolution | NLP | 1 prompt |
| C-11 | Meeting Context Extraction | NLP | 3 prompts |
| C-12 | Stakeholder/Role Identification | NLP | 2 prompts |
| C-13 | Interest/Topic Analysis | NLP | 1 prompt |
| C-14 | Document Content Analysis | NLP | 3 prompts |
| C-15 | Summary & Distillation | NLP | 1 prompt |
| C-16 | Priority Alignment Scoring | Reasoning | 2 prompts |
| C-17 | Decision Logic (Accept/Decline) | Reasoning | 1 prompt |
| C-18 | Preparation Time Estimation | Reasoning | 1 prompt |
| C-19 | Constraint Satisfaction & Slot Finding | Reasoning | 4 prompts |
| C-20 | Conflict Detection & Resolution | Reasoning | 3 prompts |
| C-21 | Objection/Risk Anticipation | Reasoning | 2 prompts |
| C-22 | Response/Recommendation Generation | Reasoning | 2 prompts |
| C-23 | Time Aggregation & Statistics | Analysis | 1 prompt |
| C-24 | Low-Value Activity Identification | Analysis | 1 prompt |
| C-25 | Time Reclamation Opportunity Analysis | Analysis | 1 prompt |
| C-26 | Meeting Flagging Logic | Analysis | 1 prompt |
| C-27 | Calendar Gap Analysis | Analysis | 1 prompt |
| C-28 | Conference Room Search & Booking | Resource Mgmt | 1 prompt |
| C-29 | Focus Time Block Scheduling | Resource Mgmt | 2 prompts |
| C-30 | Calendar Status/Availability Update | Resource Mgmt | 1 prompt |
| C-31 | Decision Justification & Explanation | Output | 1 prompt |
| C-32 | Reporting & Visualization | Output | 3 prompts |
| C-33 | Document Assembly & Formatting | Output | 3 prompts |
| C-34 | Agenda Structure Planning | Collaboration | 1 prompt |
| C-35 | Agenda Item Generation | Collaboration | 1 prompt |
| C-36 | Audience-Aware Communication | Collaboration | 1 prompt |
| C-37 | External Research & Enrichment | Collaboration | 1 prompt |
| C-38 | Profile Compilation | Collaboration | 1 prompt |
| C-39 | Relationship History Analysis | Collaboration | 1 prompt |

---

## Most Reused Capabilities (High Implementation Priority)

1. **C-GUTT-01** (Calendar Event Retrieval) - 5 prompts (76% coverage)
2. **C-GUTT-19** (Constraint Satisfaction & Slot Finding) - 4 prompts (44% coverage)
3. **C-GUTT-02** (Multi-Calendar Availability) - 3 prompts (33% coverage)
4. **C-GUTT-07** (Meeting Update & Rescheduling) - 3 prompts (33% coverage)
5. **C-GUTT-11** (Meeting Context Extraction) - 3 prompts (33% coverage)
6. **C-GUTT-14** (Document Content Analysis) - 3 prompts (33% coverage)
7. **C-GUTT-20** (Conflict Detection & Resolution) - 3 prompts (33% coverage)
8. **C-GUTT-32** (Reporting & Visualization) - 3 prompts (33% coverage)
9. **C-GUTT-33** (Document Assembly & Formatting) - 3 prompts (33% coverage)

---

## Implementation Notes

### Technology Stack Recommendations

**Calendar Data Operations (C-01 to C-07)**:
- Microsoft Graph API for calendar access
- OAuth 2.0 authentication
- Batch API support for multi-calendar queries

**NLP Capabilities (C-08 to C-15)**:
- Claude Sonnet 4.5 for summarization, extraction, distillation
- spaCy or NLTK for entity recognition
- SUTime or Duckling for temporal resolution
- Azure AI Document Intelligence for document parsing

**Reasoning & Decision Making (C-16 to C-22)**:
- Sentence transformers for semantic similarity (alignment scoring)
- scikit-learn for ML classifiers (importance, prep time)
- Google OR-Tools for constraint satisfaction
- Claude Sonnet 4.5 for objection anticipation

**Analysis & Insights (C-23 to C-27)**:
- pandas for time aggregation
- NumPy for statistical analysis
- Custom rule engine for flagging logic

**Resource Management (C-28 to C-30)**:
- Microsoft Graph API for room booking
- Calendar API for focus time creation

**Output & Communication (C-31 to C-33)**:
- Claude Sonnet 4.5 for NLG (explanations)
- matplotlib/plotly for visualization
- python-docx for document generation

**Collaboration Capabilities (C-34 to C-39)**:
- Claude Sonnet 4.5 for content generation
- CRM API integration (Salesforce, Dynamics)
- Web scraping (BeautifulSoup, Scrapy)

---

*Reference generated from GUTT Cross-Prompt Consolidation Analysis - November 6, 2025*
