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

## CANONICAL UNIT TASKS (Claude 4.5 + GPT-5 v2 Consolidation)

**Date**: November 6, 2025  
**Method**: AI Reasoning - Semantic analysis of 132 GUTTs (66 Claude + 66 GPT-5)  
**Framework**: 5-Relationship Model (=, <, >, ∩, ⊥) + Unit Task Principle

**Summary**: 20 atomic capabilities identified through cross-model consolidation

---

### Tier 1: Universal Capabilities (50%+ prompt coverage)

#### CANONICAL-01: Calendar Events Retrieval ⭐⭐⭐⭐⭐
- **Frequency**: 9/9 prompts (100% - MOST UNIVERSAL)
- **What it does**: Retrieve calendar event data from calendar systems via API, with optional filters for time range, attendees, or status
- **API/Tool**: `GET /me/calendar/events` (Microsoft Graph), `GET /calendar/v3/users/me/events` (Google Calendar)
- **Used in**: ALL 9 hero prompts
- **Example**: User requests "show meetings this week" → API call with startDateTime=2025-11-06, endDateTime=2025-11-12 → returns array of event objects
- **Claude Tasks**: C2 (org-1), C1 (org-2), C1 (org-3), C2 (sch-2), C2 (sch-3), C1 (col-3)
- **GPT-5 Tasks**: G1 (org-1), G1 (org-2), G1 (org-3), G2 (sch-2), G3 (sch-3), G2 (col-3)
- **Type**: Calendar API read operation
- **Implementation Priority**: ⭐⭐⭐⭐⭐ CRITICAL - Build first

#### CANONICAL-02: Meeting Classification/Categorization ⭐⭐⭐⭐⭐
- **Frequency**: 7/9 prompts (78%)
- **What it does**: Assign categories, scores, or classifications to calendar events based on attributes, content, and context
- **API/Tool**: ML Classification Model, Azure AI Language, OpenAI GPT, Custom classifier
- **Used in**: Prompts 1, 2, 3, 6 (organizer-1, organizer-2, organizer-3, schedule-3)
- **Example**: Meeting with title "1:1 with Sarah", 30min duration, 2 attendees → classified as type="1:1", importance="medium", override_eligible=true
- **Variants**:
  - Priority alignment classification (organizer-1): Score 0-1 how well meeting aligns with user priorities
  - Importance scoring (organizer-2): Critical/High/Medium/Low based on attendees, urgency
  - Type categorization (organizer-3): 31+ meeting types (1:1, team sync, executive review, etc.)
  - Override-eligibility (schedule-3): Identify 1:1s and lunches that can be rescheduled
- **Claude Tasks**: C3 (org-1), C2 (org-2), C2 (org-3), C4 (sch-3)
- **GPT-5 Tasks**: G4 (org-1), G2 (org-2), G3 (org-3), G5 (sch-3)
- **Type**: Machine Learning classification
- **Implementation Priority**: ⭐⭐⭐⭐⭐ CRITICAL - High reuse

#### CANONICAL-03: Calendar Event Creation/Update ⭐⭐⭐⭐⭐
- **Frequency**: 6/9 prompts (67%)
- **What it does**: Create or modify calendar events via API, including recurrence rules, attendees, and resources
- **API/Tool**: `POST /me/calendar/events`, `PATCH /me/calendar/events/{id}` (Microsoft Graph)
- **Used in**: Prompts 1, 2, 4, 5, 6 (organizer-1, organizer-2, schedule-1, schedule-2, schedule-3)
- **Example**: Create weekly recurring 1:1 → POST with subject="Weekly 1:1 with Sarah", recurrence={pattern:"weekly",daysOfWeek:["tuesday"]}, attendees=[{emailAddress:"sarah@company.com"}]
- **Variants**:
  - Single event creation (schedule-3)
  - Recurring series with iCalendar RRULE (schedule-1)
  - RSVP status updates: accept/decline/tentative (organizer-1, schedule-2)
  - Event time/attendee modifications (schedule-2, schedule-3)
  - Focus time block creation (organizer-2)
- **Claude Tasks**: C5 (org-1), C6 (org-2), C4 (sch-1), C5 (sch-2), C9 (sch-3)
- **GPT-5 Tasks**: G6 (org-1), G6 (sch-1), G5 (sch-2), G9 (sch-3)
- **Type**: Calendar API write operation
- **Implementation Priority**: ⭐⭐⭐⭐⭐ CRITICAL - Core write capability

#### CANONICAL-04: Natural Language Understanding (Constraint/Intent Extraction) ⭐⭐⭐⭐⭐
- **Frequency**: 6/9 prompts (67%)
- **What it does**: Extract structured information (entities, constraints, intents) from unstructured natural language input
- **API/Tool**: Azure AI Language, OpenAI GPT, Claude, Custom NLP pipeline
- **Used in**: Prompts 1, 4, 5, 6, 7, 8 (organizer-1, schedule-1/2/3, collaborate-1/2)
- **Example**: "Weekly 30min 1:1 with Sarah, afternoons preferred, avoid Fridays" → {recurrence:"weekly", duration:30, attendee:"Sarah", time_preference:"afternoon", exclusion:"Friday"}
- **Variants**:
  - Priority extraction (organizer-1): "Focus on customer meetings and product strategy" → priorities=["customer meetings", "product strategy"]
  - Constraint parsing (schedule-1/2/3): Time preferences, hard requirements, attendee rules
  - Temporal resolution (schedule-2): "Thursday afternoon" → 2025-11-07 13:00-17:00
  - Topic extraction (collaborate-2): Extract themes from meeting materials
  - Intent recognition (collaborate-1): "set the agenda" → intent="create_agenda"
- **Claude Tasks**: C1 (org-1), C1 (sch-1), C1 (sch-2), C1 (sch-3), C2 (col-2)
- **GPT-5 Tasks**: G1 (sch-1), G1 (sch-2), G1 (sch-3), G1 (col-1), G2 (col-2)
- **Type**: Natural Language Processing
- **Implementation Priority**: ⭐⭐⭐⭐⭐ CRITICAL - Enables natural language interface

#### CANONICAL-05: Attendee/Contact Resolution ⭐⭐⭐⭐
- **Frequency**: 5/9 prompts (56%)
- **What it does**: Resolve participant names/descriptions to specific calendar identities via directory lookup
- **API/Tool**: `GET /users` (Microsoft Graph), Azure AD Directory, Contact resolver
- **Used in**: Prompts 4, 6, 7, 9 (schedule-1, schedule-3, collaborate-1, collaborate-3)
- **Example**: "Schedule with Chris and the product team" → resolves to chris.jones@company.com + [sarah.smith@company.com, mike.wang@company.com, lisa.chen@company.com]
- **Variants**:
  - Name to email resolution: "Chris" → chris.jones@company.com
  - Team expansion: "product team" → [list of team member emails]
  - Role-based lookup: "my manager" → manager.name@company.com
  - Customer attendee identification: Filter external vs internal attendees
- **Claude Tasks**: C2 (sch-3), C2 (col-1), C3 (col-3)
- **GPT-5 Tasks**: G2 (sch-1), G2 (sch-3), G4 (col-1), G3 (col-3)
- **Type**: Directory/Contact resolution
- **Implementation Priority**: ⭐⭐⭐⭐ HIGH - Required for multi-person scheduling

---

### Tier 2: Common Capabilities (25-50% prompt coverage)

#### CANONICAL-06: Availability Checking (Free/Busy) ⭐⭐⭐
- **Frequency**: 4/9 prompts (44%)
- **What it does**: Retrieve availability status (free/busy) for specified users and time ranges
- **API/Tool**: `POST /me/calendar/getSchedule` (Microsoft Graph), `POST /freeBusy` (Google Calendar)
- **Used in**: Prompts 4, 5, 6 (schedule-1, schedule-2, schedule-3)
- **Example**: Check availability for [user, chris, sarah, mike] from 2025-11-07 to 2025-11-21 → returns free/busy schedules for all 4 users
- **Variants**:
  - Single user availability (schedule-1)
  - Multi-user availability aggregation (schedule-3)
  - Common availability calculation: Find overlapping free slots
  - Alternative slot finding (schedule-2): When rescheduling needed
- **Claude Tasks**: C2 (sch-1), C4 (sch-2), C2 (sch-3)
- **GPT-5 Tasks**: G5 (sch-1), G4 (sch-2), G3+G6 (sch-3)
- **Type**: Calendar API availability query
- **Implementation Priority**: ⭐⭐⭐ MEDIUM-HIGH - Core scheduling capability

#### CANONICAL-07: Meeting Invitation/Notification Sending ⭐⭐⭐
- **Frequency**: 4/9 prompts (44%)
- **What it does**: Dispatch calendar invitations or notifications via email/calendar system
- **API/Tool**: `POST /me/sendMail` (Microsoft Graph), Calendar invitation system, Email service
- **Used in**: Prompts 2, 4, 5, 6 (organizer-2, schedule-1, schedule-2, schedule-3)
- **Example**: Send invitation for new meeting → Calendar system sends email to attendees with .ics attachment, RSVP buttons
- **Variants**:
  - Initial invitation (schedule-1, schedule-3)
  - Reschedule notification (schedule-2)
  - Prep time reminder (organizer-2)
  - Update notification (schedule-1 auto-reschedule)
- **Claude Tasks**: C5 (sch-1), C5 (sch-2), C9 (sch-3)
- **GPT-5 Tasks**: G7 (sch-1), G5 (sch-2), G9 (sch-3), G6 (org-2)
- **Type**: Email/Calendar notification
- **Implementation Priority**: ⭐⭐⭐ MEDIUM - Required for collaboration

#### CANONICAL-08: Document/Content Retrieval ⭐⭐⭐
- **Frequency**: 4/9 prompts (44%)
- **What it does**: Retrieve documents, data, or content from various sources (SharePoint, CRM, web, etc.)
- **API/Tool**: SharePoint API, OneDrive API, CRM API (Salesforce/Dynamics), Web search
- **Used in**: Prompts 7, 8, 9 (collaborate-1, collaborate-2, collaborate-3)
- **Example**: Customer meeting prep → Retrieve: CRM records for "Acme Corp", recent proposals from SharePoint, company news from web search
- **Variants**:
  - Project context retrieval: Get Project Alpha docs, status reports (collaborate-1)
  - Meeting materials: Load presentations, reports for executive briefing (collaborate-2)
  - Company background: CRM data + web research (collaborate-3)
  - Supporting content: Related documents, case studies (collaborate-3)
- **Claude Tasks**: C1 (col-1), C1 (col-2), C2+C7 (col-3)
- **GPT-5 Tasks**: G2 (col-1), G1 (col-2), G7 (col-3)
- **Type**: Document/Data retrieval
- **Implementation Priority**: ⭐⭐⭐ MEDIUM - Enables context-aware features

#### CANONICAL-09: Document Generation/Formatting ⭐⭐⭐
- **Frequency**: 4/9 prompts (44%)
- **What it does**: Generate formatted documents from structured data using templates and NLG
- **API/Tool**: Natural Language Generation service, Template engine, python-docx, HTML/PDF generators
- **Used in**: Prompts 5, 7, 8, 9 (schedule-2, collaborate-1, collaborate-2, collaborate-3)
- **Example**: Customer meeting brief → Generates Word document with sections: Company Overview, Attendee Dossiers (with photos), Topics of Interest, Relationship History
- **Variants**:
  - Agenda generation (collaborate-1): Structured meeting flow with time allocations
  - Executive briefing (collaborate-2): 3 discussion points + objections + responses
  - Customer dossier (collaborate-3): Comprehensive prep brief
  - Action summary (schedule-2): Report of actions taken (declined, rescheduled, blocked)
- **Claude Tasks**: C6 (col-1), C7 (col-2), C8 (col-3), C8 (sch-2)
- **GPT-5 Tasks**: G8 (col-1), G6 (col-2), G8 (col-3)
- **Type**: Document generation, Natural Language Generation
- **Implementation Priority**: ⭐⭐⭐ MEDIUM - Professional output quality

#### CANONICAL-10: Time Aggregation/Statistical Analysis ⭐⭐
- **Frequency**: 3/9 prompts (33%)
- **What it does**: Aggregate and compute statistical metrics from calendar event data
- **API/Tool**: Data aggregation service, pandas, NumPy, SQL analytics
- **Used in**: Prompt 3 (organizer-3: Time Reclamation)
- **Example**: Analyze 30 days calendar history → Computes: 40% time in 1:1s (12 hrs/wk), 30% in group meetings (9 hrs/wk), 20% in customer calls (6 hrs/wk)
- **Variants**:
  - Time spent by category (1:1, team, executive, customer)
  - Time spent by person (which colleagues consume most time)
  - Time spent by project/topic
  - Average meeting duration, meeting count per day/week
  - Trend analysis (increasing/decreasing over time)
- **Claude Tasks**: C3 (org-3)
- **GPT-5 Tasks**: G5 (org-3)
- **Type**: Analytics, Statistical computation
- **Implementation Priority**: ⭐⭐ MEDIUM - Insights generation

#### CANONICAL-11: Priority/Preference Matching ⭐⭐
- **Frequency**: 3/9 prompts (33%)
- **What it does**: Score/classify calendar events based on alignment with user-defined priorities or preferences
- **API/Tool**: Semantic similarity service (Sentence Transformers), Priority scoring algorithm
- **Used in**: Prompts 1, 3 (organizer-1, organizer-3)
- **Example**: User priority="customer meetings", Meeting about "Q4 Customer Strategy Review" → Semantic similarity score=0.92 (high alignment)
- **Variants**:
  - Priority alignment scoring (organizer-1): Score each meeting 0-1 against priorities
  - Gap identification (organizer-3): Find misalignment between time usage and priorities
  - Preference matching: Match meetings to user preferences (time of day, meeting size, etc.)
- **Claude Tasks**: C3 (org-1), C4 (org-3)
- **GPT-5 Tasks**: G4 (org-1), G4 (org-3)
- **Type**: Semantic matching, Relevance scoring
- **Implementation Priority**: ⭐⭐ MEDIUM - Intelligent prioritization

#### CANONICAL-12: Constraint Satisfaction ⭐⭐⭐
- **Frequency**: 3/9 prompts (33%)
- **What it does**: Find time slots satisfying multiple scheduling constraints using CSP algorithms
- **API/Tool**: Constraint solver (Google OR-Tools, python-constraint), Custom scheduling algorithm
- **Used in**: Prompts 4, 6 (schedule-1, schedule-3)
- **Example**: Constraints: weekly recurring, 30min, afternoons, not Friday, both attendees free → Solver finds: "Tuesdays 2:00-2:30pm" satisfies all
- **Variants**:
  - Simple constraint satisfaction (schedule-1): Time preferences + availability
  - Multi-constraint optimization (schedule-3): Attendee priority (Kat's schedule), override rules, location (in-person), resource (room)
  - Hard vs soft constraints: Must-have vs nice-to-have
  - Slot ranking: Order solutions by preference match
- **Claude Tasks**: C3 (sch-1), C7 (sch-3)
- **GPT-5 Tasks**: G4+G5 (sch-1), G6+G7 (sch-3)
- **Type**: Constraint Satisfaction Problem solver
- **Implementation Priority**: ⭐⭐⭐ MEDIUM-HIGH - Complex scheduling scenarios

#### CANONICAL-13: RSVP Status Update ⭐⭐
- **Frequency**: 3/9 prompts (33%)
- **What it does**: Update meeting RSVP status via calendar API
- **API/Tool**: `POST /me/events/{id}/accept`, `POST /me/events/{id}/decline`, `POST /me/events/{id}/tentativelyAccept`
- **Used in**: Prompts 1, 5 (organizer-1, schedule-2)
- **Example**: Decline low-priority meeting → PATCH /events/{id} with responseStatus="declined", sends notification to organizer
- **Variants**:
  - Accept meeting (organizer-1: priority-aligned)
  - Decline meeting (organizer-1: low priority; schedule-2: blocked time)
  - Tentative response
  - Bulk RSVP updates (schedule-2: decline all in time block)
- **Claude Tasks**: C3 (sch-2), C5 (org-1)
- **GPT-5 Tasks**: G3 (sch-2), G6 (org-1)
- **Type**: Calendar API write operation
- **Implementation Priority**: ⭐⭐ MEDIUM - Standard calendar operation

#### CANONICAL-14: Recommendation Engine ⭐⭐
- **Frequency**: 3/9 prompts (33%)
- **What it does**: Generate actionable recommendations based on analysis using rules or ML
- **API/Tool**: Rule engine, LLM (Claude/GPT), Recommendation algorithm
- **Used in**: Prompts 2, 3, 8 (organizer-2, organizer-3, collaborate-2)
- **Example**: Time analysis shows 10hrs/week in low-priority meetings → Recommends: "Decline 'Weekly Team Happy Hour' (saves 1hr/wk), Shorten 'Status Sync' from 60min to 30min (saves 2hrs/month)"
- **Variants**:
  - Time reclamation recommendations (organizer-3): Decline, delegate, shorten, consolidate
  - Preparation recommendations (organizer-2): When to schedule focus time
  - Response recommendations (collaborate-2): Effective responses to anticipated objections
- **Claude Tasks**: C7 (org-2), C7 (org-3), C6 (col-2)
- **GPT-5 Tasks**: G7 (org-3), G6 (col-2)
- **Type**: Recommendation system
- **Implementation Priority**: ⭐⭐ MEDIUM - Value-add insights

---

### Tier 3: Specialized Capabilities (<25% prompt coverage)

#### CANONICAL-15: Recurrence Rule Generation ⭐
- **Frequency**: 2/9 prompts (22%)
- **What it does**: Generate iCalendar RRULE specifications from natural language recurrence patterns
- **API/Tool**: iCalendar RRULE specification, python-dateutil.rrule, Custom RRULE generator
- **Used in**: Prompts 4 (schedule-1)
- **Example**: "Weekly starting next Monday" → RRULE:FREQ=WEEKLY;BYDAY=MO;DTSTART=20251110
- **Variants**:
  - Weekly recurring (schedule-1): Every Tuesday at 2pm
  - Bi-weekly: Every other Friday
  - Monthly: First Monday of each month
  - Custom patterns: Every weekday except Friday
- **Claude Tasks**: C4 (sch-1)
- **GPT-5 Tasks**: G3 (sch-1)
- **Type**: Temporal pattern generation
- **Implementation Priority**: ⭐ LOW - Specialized use case

#### CANONICAL-16: Event Monitoring/Change Detection ⭐
- **Frequency**: 2/9 prompts (22%)
- **What it does**: Detect and respond to calendar event changes via webhooks or polling
- **API/Tool**: Microsoft Graph Webhooks, Change Notifications API, Polling service
- **Used in**: Prompts 4 (schedule-1)
- **Example**: Subscribe to meeting RSVP changes → Webhook fires when attendee declines → Trigger auto-reschedule workflow
- **Variants**:
  - RSVP change detection (schedule-1): Attendee accepts/declines/tentative
  - Conflict detection: New meeting conflicts with existing
  - Event update tracking: Time/location/attendee changes
  - Cancellation monitoring
- **Claude Tasks**: C6 (sch-1)
- **GPT-5 Tasks**: G8 (sch-1)
- **Type**: Event monitoring, Webhooks
- **Implementation Priority**: ⭐ LOW - Advanced automation

#### CANONICAL-17: Automatic Rescheduling ⭐
- **Frequency**: 2/9 prompts (22%)
- **What it does**: Automatically reschedule meetings in response to conflicts or declines
- **API/Tool**: Workflow automation, Dynamic scheduling service, Orchestration engine
- **Used in**: Prompts 4, 6 (schedule-1, schedule-3)
- **Example**: Attendee declines Tuesday 2pm meeting → System finds new slot (Thursday 3pm), updates event, sends notification automatically
- **Variants**:
  - Decline-triggered rescheduling (schedule-1): When attendee declines, find new time
  - Conflict-driven rescheduling (schedule-3): Override lower-priority meetings
  - Cascading rescheduling: When moving one meeting affects others
- **Claude Tasks**: C7 (sch-1), C8 (sch-3)
- **GPT-5 Tasks**: G9 (sch-1)
- **Type**: Workflow automation
- **Implementation Priority**: ⭐ LOW - Advanced automation

#### CANONICAL-18: Objection/Risk Anticipation ⭐
- **Frequency**: 2/9 prompts (22%)
- **What it does**: Predict objections, concerns, or risks using critical thinking and risk modeling
- **API/Tool**: LLM (Claude/GPT-4), Risk analysis model, Critical thinking engine
- **Used in**: Prompts 7, 8 (collaborate-1, collaborate-2)
- **Example**: Executive briefing on budget increase → Anticipates objections: "ROI unclear" (provide cost-benefit analysis), "Timeline aggressive" (show risk mitigation), "Why not MVP?" (explain scope rationale)
- **Variants**:
  - Executive objections (collaborate-2): Budget, timeline, scope concerns
  - Project blockers (collaborate-1): Dependencies, resource constraints, technical risks
  - Stakeholder concerns: Different perspectives (product vs marketing vs engineering)
- **Claude Tasks**: C5 (col-1), C5 (col-2)
- **GPT-5 Tasks**: G5 (col-2)
- **Type**: LLM reasoning, Risk analysis
- **Implementation Priority**: ⭐ LOW - Advanced collaboration feature

#### CANONICAL-19: Resource Booking (Rooms/Equipment) ⭐
- **Frequency**: 1/9 prompts (11%)
- **What it does**: Search for and book physical resources (rooms, equipment) via resource scheduling API
- **API/Tool**: `GET /places` (Microsoft Graph), Room booking API, Equipment reservation system
- **Used in**: Prompt 6 (schedule-3)
- **Example**: Need conference room for 5 people, in-person, with projector → Searches rooms, finds "Conf Room B41-3A" (capacity 8, has projector), reserves it
- **Variants**:
  - Room search by capacity: Find rooms fitting attendee count
  - Equipment requirements: Projector, whiteboard, video conferencing
  - Location filtering: Specific building or floor
  - Availability checking: Room free during time slot
- **Claude Tasks**: C6 (sch-3)
- **GPT-5 Tasks**: G8 (sch-3)
- **Type**: Resource management
- **Implementation Priority**: ⭐ LOW - Facilities integration

#### CANONICAL-20: Data Visualization/Reporting ⭐
- **Frequency**: 1/9 prompts (11%)
- **What it does**: Generate visualizations (charts, graphs, dashboards) from calendar data
- **API/Tool**: Chart.js, D3.js, matplotlib, plotly, Power BI, Tableau
- **Used in**: Prompt 3 (organizer-3: Time Reclamation)
- **Example**: Time usage analysis → Generates: Pie chart (time by category), Bar chart (top 10 time consumers), Line chart (trend over weeks), Dashboard with key metrics
- **Variants**:
  - Time distribution visualization: How time is allocated
  - Trend analysis: Meeting load over time
  - Comparison views: Current vs target allocation
  - Interactive dashboards: Drill-down capabilities
- **Claude Tasks**: C8 (org-3)
- **GPT-5 Tasks**: G8 (org-3)
- **Type**: Data visualization
- **Implementation Priority**: ⭐ LOW - Reporting/analytics feature

---

## Canonical Tasks: Quick Reference Table

| ID | Canonical Task | Frequency | Tier | APIs/Tools | Priority |
|----|---------------|-----------|------|------------|----------|
| **CAN-01** | **Calendar Events Retrieval** | **9/9 (100%)** | 1 | Microsoft Graph, Google Calendar | ⭐⭐⭐⭐⭐ |
| **CAN-02** | **Meeting Classification** | **7/9 (78%)** | 1 | ML Model, Azure AI, OpenAI | ⭐⭐⭐⭐⭐ |
| **CAN-03** | **Calendar Event Creation/Update** | **6/9 (67%)** | 1 | Microsoft Graph POST/PATCH | ⭐⭐⭐⭐⭐ |
| **CAN-04** | **NLU (Constraint/Intent Extraction)** | **6/9 (67%)** | 1 | Azure AI, OpenAI, Claude | ⭐⭐⭐⭐⭐ |
| **CAN-05** | **Attendee/Contact Resolution** | **5/9 (56%)** | 1 | Microsoft Graph /users | ⭐⭐⭐⭐ |
| **CAN-06** | **Availability Checking** | **4/9 (44%)** | 2 | Microsoft Graph /getSchedule | ⭐⭐⭐ |
| **CAN-07** | **Meeting Invitations** | **4/9 (44%)** | 2 | Email/Calendar system | ⭐⭐⭐ |
| **CAN-08** | **Document/Content Retrieval** | **4/9 (44%)** | 2 | SharePoint, OneDrive, CRM | ⭐⭐⭐ |
| **CAN-09** | **Document Generation** | **4/9 (44%)** | 2 | NLG, Template engine | ⭐⭐⭐ |
| **CAN-10** | **Time Aggregation/Analytics** | **3/9 (33%)** | 2 | pandas, NumPy, SQL | ⭐⭐ |
| **CAN-11** | **Priority/Preference Matching** | **3/9 (33%)** | 2 | Semantic similarity | ⭐⭐ |
| **CAN-12** | **Constraint Satisfaction** | **3/9 (33%)** | 2 | OR-Tools, CSP solver | ⭐⭐⭐ |
| **CAN-13** | **RSVP Status Update** | **3/9 (33%)** | 2 | Microsoft Graph accept/decline | ⭐⭐ |
| **CAN-14** | **Recommendation Engine** | **3/9 (33%)** | 2 | LLM, Rule engine | ⭐⭐ |
| **CAN-15** | **Recurrence Rule Generation** | **2/9 (22%)** | 3 | iCalendar RRULE | ⭐ |
| **CAN-16** | **Event Monitoring** | **2/9 (22%)** | 3 | Webhooks, Polling | ⭐ |
| **CAN-17** | **Automatic Rescheduling** | **2/9 (22%)** | 3 | Workflow automation | ⭐ |
| **CAN-18** | **Objection/Risk Anticipation** | **2/9 (22%)** | 3 | LLM reasoning | ⭐ |
| **CAN-19** | **Resource Booking** | **1/9 (11%)** | 3 | Microsoft Graph /places | ⭐ |
| **CAN-20** | **Data Visualization** | **1/9 (11%)** | 3 | Chart.js, D3.js, plotly | ⭐ |

---

## Implementation Roadmap

### Phase 1: Universal Tier (Weeks 1-4)
**Build Order**: CAN-01 → CAN-04 → CAN-02 → CAN-03 → CAN-05

1. **CAN-01: Calendar Events Retrieval** (Week 1)
   - Foundational capability - required by all other features
   - Implement Microsoft Graph integration
   - Add filtering, pagination, error handling

2. **CAN-04: NLU (Constraint/Intent Extraction)** (Week 1-2)
   - Critical for natural language interface
   - Integrate Azure AI Language or OpenAI
   - Build prompt templates for common patterns

3. **CAN-02: Meeting Classification** (Week 2-3)
   - High-reuse capability across multiple features
   - Train/fine-tune classification model
   - Implement 31+ meeting type taxonomy

4. **CAN-03: Calendar Event Creation/Update** (Week 3)
   - Core write capability
   - Implement CRUD operations
   - Add recurrence rule support

5. **CAN-05: Attendee/Contact Resolution** (Week 4)
   - Required for multi-person scenarios
   - Directory integration
   - Disambiguation logic

### Phase 2: Common Tier (Weeks 5-8)
**Build Order**: CAN-06 → CAN-12 → CAN-07 → CAN-08 → CAN-09 → Others

Focus on scheduling capabilities (CAN-06, CAN-12) first, then collaboration features (CAN-08, CAN-09).

### Phase 3: Specialized Tier (Weeks 9-12)
**Build Order**: Based on product priorities and use case demand

Implement on-demand as specific features require them.

---

## Comparison: C-GUTT (39) vs Canonical Tasks (20)

| Aspect | C-GUTT (39 tasks) | Canonical Tasks (20 tasks) |
|--------|-------------------|----------------------------|
| **Source** | Claude 4.5 only (66 GUTTs) | Claude 4.5 + GPT-5 v2 (132 GUTTs) |
| **Method** | Within-model consolidation | Cross-model semantic consolidation |
| **Validation** | Single model perspective | Dual model validation (higher confidence) |
| **Granularity** | Mid-level (39 tasks) | Higher-level (20 tasks) - more atomic |
| **Coverage** | 9 prompts (Calendar.AI hero set) | 9 prompts (same dataset) |
| **Organization** | 7 categories | 3 tiers by frequency |
| **Use Case** | Implementation reference | Platform evaluation + architecture |

### When to Use Each

**Use C-GUTT (39 tasks)**:
- ✅ Detailed implementation planning
- ✅ Understanding capability variants and nuances
- ✅ Technology stack selection
- ✅ Granular tracking and testing

**Use Canonical Tasks (20 tasks)**:
- ✅ New prompt evaluation and decomposition
- ✅ Platform-wide capability planning
- ✅ Implementation prioritization (Tier 1 → 2 → 3)
- ✅ Cross-validation of LLM decomposition quality
- ✅ Architectural design decisions

### Mapping Between Systems

Many C-GUTTs map to Canonical Tasks with 1:1 or N:1 relationships:

- **CANONICAL-01** (Calendar Events Retrieval) = C-GUTT-01
- **CANONICAL-02** (Meeting Classification) = C-GUTT-03 + C-GUTT-04
- **CANONICAL-03** (Calendar Event Creation/Update) = C-GUTT-05 + C-GUTT-06 + C-GUTT-07
- **CANONICAL-04** (NLU) = C-GUTT-08 + C-GUTT-09 + C-GUTT-10
- And so on...

---

*Reference generated from GUTT Cross-Prompt Consolidation Analysis - November 6, 2025*  
*Canonical Tasks generated from Claude 4.5 + GPT-5 v2 AI Reasoning Consolidation - November 6, 2025*

