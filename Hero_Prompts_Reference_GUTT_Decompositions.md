# Hero Prompts Reference GUTT Decompositions - Ground Truth

**Source**: Calendar.AI Hero Prompts Evaluation Framework  
**Purpose**: Reference decompositions for benchmarking LLM GUTT analysis capabilities  
**Date**: November 6, 2025  
**Update**: Includes C-GUTT consolidation analysis (66 → 39 atomic capabilities)

**Related Documents**:
- [CONSOLIDATED_GUTT_REFERENCE.md](docs/gutt_analysis/CONSOLIDATED_GUTT_REFERENCE.md) - Complete C-GUTT specifications
- [GUTT_CROSS_PROMPT_CONSOLIDATION_ANALYSIS.md](docs/gutt_analysis/GUTT_CROSS_PROMPT_CONSOLIDATION_ANALYSIS.md) - Consolidation methodology
- [CAPABILITY_INVENTORY_ANALYSIS.md](docs/gutt_analysis/CAPABILITY_INVENTORY_ANALYSIS.md) - Infrastructure implementation view

---

## Hero Prompt 1: Calendar Prioritization (Organizer-1)

**Prompt**: "Keep my Calendar up to date by committing to only meetings that are part of my priorities."

**Capabilities Tested**: C1 (Calendar Access), C2 (Event Analysis), C5 (Action Control), C7 (Priority Reasoning)

### Reference GUTT Decomposition: **6 Unit Tasks**

#### GUTT 1: Priority Definition & Extraction
- **Capability**: Identify and structure user's priorities from context
- **Skills**: Natural language understanding, priority extraction, rule formalization
- **User Goal**: System understands what matters to the user

#### GUTT 2: Calendar Event Retrieval
- **Capability**: Access and load pending calendar invitations and scheduled meetings
- **Skills**: Calendar API integration, event filtering (pending/confirmed), data parsing
- **User Goal**: Get all meetings that need decision-making

#### GUTT 3: Meeting-Priority Alignment Scoring
- **Capability**: Evaluate how well each meeting aligns with stated priorities
- **Skills**: Semantic matching, relevance scoring, priority ranking, feature extraction
- **User Goal**: Know which meetings support goals and which don't

#### GUTT 4: Accept/Decline Decision Logic
- **Capability**: Determine which meetings to accept vs decline based on priority alignment
- **Skills**: Threshold-based decision making, conflict resolution, calendar optimization
- **User Goal**: Automated keep/decline recommendations

#### GUTT 5: Calendar Action Execution
- **Capability**: Execute accept/decline actions on calendar system
- **Skills**: Calendar API write operations, RSVP updates, confirmation handling
- **User Goal**: Calendar automatically reflects priority decisions

#### GUTT 6: Decision Justification & Reporting
- **Capability**: Explain why each meeting was accepted or declined
- **Skills**: Natural language generation, rule-based explanation, transparency reporting
- **User Goal**: Understand the reasoning behind each decision

**Evaluation**: Decision accuracy vs gold set, justification quality linking to priority rules

---

## Hero Prompt 2: Meeting Prep Tracking (Organizer-2)

**Prompt**: "Track all my important meetings and flag any that require focus time to prepare for them."

**Capabilities Tested**: C1, C2, C3, C7, C10

### Reference GUTT Decomposition: **7 Unit Tasks** ✅ COMPLETED

*(See Reference_GUTT_Decomposition_Ground_Truth.md for full details)*

1. Calendar Data Retrieval
2. Meeting Importance Classification
3. Preparation Time Estimation
4. Meeting Flagging Logic
5. Calendar Gap Analysis
6. Focus Time Block Scheduling
7. Actionable Recommendations & Reporting

**Evaluation**: Flag precision/recall for "needs prep" label, lead-time coverage

---

## Hero Prompt 3: Time Reclamation Analysis (Organizer-3)

**Prompt**: "Help me understand where I am spending my time and identify ways I can reclaim time to focus more on my top priorities."

**Capabilities Tested**: C7 (Priority Reasoning), C8 (Pattern Recognition), C10 (Analytics)

### Reference GUTT Decomposition: **8 Unit Tasks**

#### GUTT 1: Calendar Historical Data Retrieval
- **Capability**: Load past calendar events for specified time period
- **Skills**: Calendar API integration, date range filtering, historical data access
- **User Goal**: Get comprehensive time usage data

#### GUTT 2: Meeting Categorization & Classification
- **Capability**: Classify meetings by type, purpose, importance, participants
- **Skills**: Meeting type taxonomy (31+ types), automatic classification, labeling
- **User Goal**: Understand what kinds of meetings fill the calendar

#### GUTT 3: Time Aggregation & Statistical Analysis
- **Capability**: Compute time spent per category, participant, project, etc.
- **Skills**: Time calculation, statistical aggregation, grouping, trend analysis
- **User Goal**: Quantify where time is actually going

#### GUTT 4: Priority Alignment Assessment
- **Capability**: Evaluate which time usage aligns with stated priorities
- **Skills**: Priority mapping, alignment scoring, gap identification
- **User Goal**: See misalignment between goals and actual time usage

#### GUTT 5: Low-Value Meeting Identification
- **Capability**: Flag meetings that consume time without supporting priorities
- **Skills**: Value scoring, reclamation candidate detection, opportunity identification
- **User Goal**: Know which meetings to eliminate or delegate

#### GUTT 6: Time Reclamation Opportunity Analysis
- **Capability**: Calculate potential time savings from proposed changes
- **Skills**: Impact modeling, time savings projection, feasibility assessment
- **User Goal**: Understand how much time could be reclaimed

#### GUTT 7: Schedule Optimization Recommendations
- **Capability**: Suggest specific changes (decline, delegate, shorten, consolidate)
- **Skills**: Recommendation generation, actionable guidance, change proposals
- **User Goal**: Know exactly what to do to reclaim time

#### GUTT 8: Time Usage Reporting & Visualization
- **Capability**: Present insights with charts, summaries, comparisons
- **Skills**: Data visualization, report generation, insight communication
- **User Goal**: Easily understand patterns and take action

**Evaluation**: Pattern accuracy, swap feasibility, time savings realization

---

## Hero Prompt 4: Recurring 1:1 Scheduling (Schedule-1)

**Prompt**: "Starting next week, I want a weekly 30-min 1:1 with {name}. Afternoons preferred, avoid Fridays. Automatically reschedule on declines or conflicts."

**Capabilities Tested**: C3 (Scheduling), C4 (Constraints), C5 (Actions)

### Reference GUTT Decomposition: **7 Unit Tasks**

#### GUTT 1: Constraint Extraction & Formalization
- **Capability**: Parse scheduling requirements into structured constraints
- **Skills**: NLP for constraint extraction, rule formalization, preference modeling
- **User Goal**: System understands all scheduling rules

#### GUTT 2: Multi-Calendar Availability Checking
- **Capability**: Check free/busy status for user and attendee
- **Skills**: Calendar API for multiple users, free/busy queries, availability matrix
- **User Goal**: Find times when both parties are free

#### GUTT 3: Constraint-Based Slot Finding
- **Capability**: Identify time slots matching all constraints (weekly, afternoons, not Fridays, 30min)
- **Skills**: Constraint satisfaction, temporal reasoning, slot ranking
- **User Goal**: Get valid time options that meet preferences

#### GUTT 4: Recurring Meeting Series Creation
- **Capability**: Create recurring calendar event with proper series configuration
- **Skills**: Recurrence rule generation (iCalendar RRULE), series management
- **User Goal**: One-time setup creates ongoing weekly meetings

#### GUTT 5: Meeting Invitation Sending
- **Capability**: Send calendar invitation to attendee
- **Skills**: Calendar invitation API, email notification, RSVP request
- **User Goal**: Attendee receives and can accept/decline

#### GUTT 6: Decline/Conflict Detection & Monitoring
- **Capability**: Monitor for attendee declines or new calendar conflicts
- **Skills**: Event change detection, RSVP tracking, conflict identification
- **User Goal**: System knows when rescheduling is needed

#### GUTT 7: Automatic Rescheduling Logic
- **Capability**: When declined/conflicted, find new slot and send updated invitation
- **Skills**: Trigger-based automation, slot re-finding, invitation updates
- **User Goal**: Seamless rescheduling without manual intervention

**Evaluation**: Valid vs invalid proposals under hard constraints, automation reliability

---

## Hero Prompt 5: Block Time & Reschedule (Schedule-2)

**Prompt**: "Clear my Thursday afternoon. Update my RSVPs and help me reschedule my meetings to another time and show me as {status}."

**Capabilities Tested**: C3 (Scheduling), C4 (Constraints), C5 (Actions)

### Reference GUTT Decomposition: **8 Unit Tasks**

#### GUTT 1: Time Block Specification Parsing
- **Capability**: Interpret "Thursday afternoon" into specific date/time range
- **Skills**: Temporal expression resolution, date/time parsing, context awareness
- **User Goal**: System knows exactly which time block to clear

#### GUTT 2: Affected Meetings Identification
- **Capability**: Find all meetings within the target time block
- **Skills**: Calendar querying, temporal overlap detection, meeting filtering
- **User Goal**: Know which meetings need rescheduling

#### GUTT 3: RSVP Decline Execution
- **Capability**: Decline all meetings in the blocked time
- **Skills**: Calendar API updates, RSVP status changes, batch operations
- **User Goal**: Notify organizers user won't attend

#### GUTT 4: Alternative Slot Finding
- **Capability**: For each meeting, identify alternative time slots
- **Skills**: Availability checking, attendee coordination, slot ranking
- **User Goal**: Find times when same attendees can meet

#### GUTT 5: Meeting Rescheduling Proposals
- **Capability**: Send reschedule requests with proposed new times
- **Skills**: Meeting update API, attendee communication, proposal generation
- **User Goal**: Meetings moved to new times

#### GUTT 6: Calendar Status Update
- **Capability**: Set user's status/availability for the blocked time
- **Skills**: Free/busy status setting, calendar property updates
- **User Goal**: Others see user as unavailable during blocked time

#### GUTT 7: Focus Time Block Creation
- **Capability**: Create placeholder event for the blocked time
- **Skills**: Calendar event creation, focus time labeling
- **User Goal**: Visual representation of blocked time on calendar

#### GUTT 8: Action Summary & Confirmation
- **Capability**: Report what was done (declined X, rescheduled Y, blocked Z hours)
- **Skills**: Action tracking, status reporting, confirmation generation
- **User Goal**: Understand complete outcome of the request

**Evaluation**: Task completion rate across sequential steps, coordination success

---

## Hero Prompt 6: Multi-Person Meeting Scheduling (Schedule-3)

**Prompt**: "Land a time to meet about Project Alpha with Chris, Sangya, and Kat for 1 hour in the next 2 weeks. Schedule over 1:1s and lunches if needed and work around Kat's schedule. Make the meeting in person and add a room."

**Capabilities Tested**: C3, C4, C5, C6 (Resource booking)

### Reference GUTT Decomposition: **9 Unit Tasks**

#### GUTT 1: Meeting Requirements Extraction
- **Capability**: Parse all requirements (attendees, duration, date range, constraints, modality, resources)
- **Skills**: Multi-constraint NLP extraction, requirement structuring
- **User Goal**: System understands all meeting parameters

#### GUTT 2: Multi-Person Availability Aggregation
- **Capability**: Check calendars for Chris, Sangya, Kat and merge availability
- **Skills**: Cross-calendar API access, availability intersection, constraint prioritization
- **User Goal**: Find times when all required attendees are available

#### GUTT 3: Priority Constraint Application (Kat's schedule)
- **Capability**: Ensure primary consideration of Kat's availability
- **Skills**: Hierarchical constraint handling, priority weighting
- **User Goal**: Kat's conflicts are hard constraints, others can be overridden

#### GUTT 4: Override-Eligible Meeting Identification
- **Capability**: Identify 1:1s and lunches that can be rescheduled if needed
- **Skills**: Meeting type classification, override eligibility rules, conflict detection
- **User Goal**: System knows which existing meetings are movable

#### GUTT 5: Location-Based Filtering
- **Capability**: Filter for in-person meeting capability (office presence, not remote)
- **Skills**: Location awareness, modality constraints, participant location checking
- **User Goal**: Meeting scheduled when in-person attendance is possible

#### GUTT 6: Conference Room Search & Booking
- **Capability**: Find available room for in-person meeting and reserve it
- **Skills**: Room resource API, availability checking, capacity matching, room booking
- **User Goal**: Meeting has physical space reserved

#### GUTT 7: Optimal Slot Selection
- **Capability**: Rank and select best time considering all constraints
- **Skills**: Multi-objective optimization, slot scoring, feasibility validation
- **User Goal**: Best possible time is chosen

#### GUTT 8: Conflict Resolution & Rescheduling
- **Capability**: If needed, reschedule override-eligible conflicts
- **Skills**: Cascading rescheduling, conflict resolution, meeting moves
- **User Goal**: Conflicts automatically resolved

#### GUTT 9: Meeting Creation & Invitations
- **Capability**: Create meeting with all attendees, room, and details
- **Skills**: Calendar event creation, multi-person invitations, resource inclusion
- **User Goal**: Meeting appears on all calendars with room reserved

**Evaluation**: % feasible vs infeasible schedules, constraint satisfaction accuracy

---

## Hero Prompt 7: Agenda Creation (Collaborate-1)

**Prompt**: "Help me set the agenda to review the progress of Project Alpha with the product and marketing team to get confirmation we are on track and discuss any blocking issues or risks."

**Capabilities Tested**: Contextual reasoning, meeting structure planning

### Reference GUTT Decomposition: **6 Unit Tasks**

#### GUTT 1: Meeting Context Retrieval
- **Capability**: Gather information about Project Alpha from available sources
- **Skills**: Document retrieval, context extraction, project status queries
- **User Goal**: Agenda based on actual project state

#### GUTT 2: Stakeholder Role Identification
- **Capability**: Understand product team vs marketing team roles and concerns
- **Skills**: Role-based reasoning, stakeholder analysis, perspective modeling
- **User Goal**: Agenda addresses each group's needs

#### GUTT 3: Agenda Structure Planning
- **Capability**: Create logical flow for review meeting (progress → confirmation → blockers → risks)
- **Skills**: Meeting structure best practices, agenda templating, flow optimization
- **User Goal**: Meeting has clear structure and progression

#### GUTT 4: Progress Review Items Generation
- **Capability**: List specific accomplishments, milestones, metrics to review
- **Skills**: Achievement extraction, milestone identification, metrics selection
- **User Goal**: Concrete progress discussion points

#### GUTT 5: Blocker & Risk Identification
- **Capability**: Surface known issues, dependencies, and potential risks for discussion
- **Skills**: Issue tracking, risk analysis, dependency mapping
- **User Goal**: Problems addressed proactively

#### GUTT 6: Time Allocation & Formatting
- **Capability**: Assign time to each agenda item and format for distribution
- **Skills**: Time budgeting, agenda formatting, document generation
- **User Goal**: Professional, well-structured agenda document

**Evaluation**: Agenda completeness, stakeholder coverage, action alignment

---

## Hero Prompt 8: Executive Briefing Prep (Collaborate-2)

**Prompt**: "Review the materials for my meeting with senior leadership and suggest the best way to summarize the topics into three main discussion points. Generate any objections or concerns that might come up and give me effective responses."

**Capabilities Tested**: Critical summarization, role-based reasoning

### Reference GUTT Decomposition: **7 Unit Tasks**

#### GUTT 1: Meeting Materials Retrieval
- **Capability**: Access and load all relevant documents for the meeting
- **Skills**: Document access, file reading, content extraction
- **User Goal**: System has all materials to analyze

#### GUTT 2: Content Analysis & Topic Extraction
- **Capability**: Identify main themes and topics across materials
- **Skills**: Document analysis, theme extraction, topic clustering
- **User Goal**: Understand what the materials cover

#### GUTT 3: Executive Summary Distillation
- **Capability**: Condense complex topics into 3 concise discussion points
- **Skills**: Summarization, priority ranking, executive communication
- **User Goal**: Clear, high-level discussion framework

#### GUTT 4: Audience-Aware Framing
- **Capability**: Frame discussion points appropriate for senior leadership
- **Skills**: Role-based communication, executive context, tone adjustment
- **User Goal**: Points resonate with executive concerns

#### GUTT 5: Objection Anticipation
- **Capability**: Predict concerns or pushback from senior leaders
- **Skills**: Critical thinking, risk identification, executive perspective modeling
- **User Goal**: Prepared for tough questions

#### GUTT 6: Response Preparation
- **Capability**: Generate effective responses to anticipated objections
- **Skills**: Argumentation, evidence marshaling, persuasive communication
- **User Goal**: Confident, well-reasoned responses ready

#### GUTT 7: Briefing Document Generation
- **Capability**: Format summary, objections, and responses into prep document
- **Skills**: Document formatting, professional presentation, structure
- **User Goal**: Comprehensive prep materials ready to review

**Evaluation**: Summary quality, objection realism, response effectiveness

---

## Hero Prompt 9: Customer Meeting Prep (Collaborate-3)

**Prompt**: "Prepare a brief for my upcoming meeting with customer Beta and include a dossier for each customer attendee and the topics they are most interested in. Include a background on their company."

**Capabilities Tested**: Information aggregation, personalization, CRM integration

### Reference GUTT Decomposition: **8 Unit Tasks**

#### GUTT 1: Meeting Details Retrieval
- **Capability**: Get meeting information (attendees, time, purpose)
- **Skills**: Calendar API, meeting metadata extraction
- **User Goal**: Know who's attending and meeting context

#### GUTT 2: Company Background Research
- **Capability**: Gather information about customer Beta company
- **Skills**: CRM data access, web research, company profile compilation
- **User Goal**: Understand customer's business and context

#### GUTT 3: Attendee Identity Resolution
- **Capability**: Identify each customer attendee and their roles
- **Skills**: Contact resolution, role identification, org chart analysis
- **User Goal**: Know who you're meeting with

#### GUTT 4: Individual Dossier Creation
- **Capability**: For each attendee, compile background, role, history
- **Skills**: CRM querying, interaction history, profile building
- **User Goal**: Personalized context for each attendee

#### GUTT 5: Topic Interest Analysis
- **Capability**: Identify topics each attendee cares about based on history
- **Skills**: Communication analysis, interest extraction, preference modeling
- **User Goal**: Discuss what matters to each person

#### GUTT 6: Relationship History Compilation
- **Capability**: Summarize past interactions, deals, issues with customer
- **Skills**: CRM data aggregation, timeline creation, context building
- **User Goal**: Aware of relationship history and context

#### GUTT 7: Relevant Content Gathering
- **Capability**: Find related materials (proposals, presentations, tickets)
- **Skills**: Document search, relevance matching, content curation
- **User Goal**: Have supporting materials ready

#### GUTT 8: Brief Document Assembly
- **Capability**: Compile all information into structured prep brief
- **Skills**: Document generation, formatting, professional presentation
- **User Goal**: Complete brief ready for meeting prep

**Evaluation**: Information accuracy, personalization quality, completeness

---

## Summary Statistics

| Hero Prompt | Category | GUTT Count | Complexity | Data Sources |
|-------------|----------|------------|------------|--------------|
| 1. Calendar Prioritization | Organizer | 6 | Medium | Calendar, User Preferences |
| 2. Meeting Prep Tracking | Organizer | 7 | Medium | Calendar, Meeting Metadata |
| 3. Time Reclamation | Organizer | 8 | High | Historical Calendar, Analytics |
| 4. Recurring 1:1 Scheduling | Schedule | 7 | Medium | Multi-Calendar, Constraints |
| 5. Block Time & Reschedule | Schedule | 8 | High | Calendar, Sequential Actions |
| 6. Multi-Person Scheduling | Schedule | 9 | Very High | Multi-Calendar, Resources |
| 7. Agenda Creation | Collaborate | 6 | Medium | Project Data, Context |
| 8. Executive Briefing | Collaborate | 7 | High | Documents, Analysis |
| 9. Customer Meeting Prep | Collaborate | 8 | High | CRM, Research, Documents |

**Total**: 9 Hero Prompts, **66 GUTTs**, Average: 7.3 GUTTs per prompt

**Consolidation Update (November 6, 2025)**:
- **Original GUTTs**: 66 prompt-specific unit tasks
- **Consolidated C-GUTTs**: 39 atomic capabilities (41% reduction)
- **Average Reusability**: 1.69 prompts per C-GUTT
- **Most Reused**: C-GUTT-01 (Calendar Event Retrieval) serves 5 prompts (76% coverage)

See [CONSOLIDATED_GUTT_REFERENCE.md](docs/gutt_analysis/CONSOLIDATED_GUTT_REFERENCE.md) for complete C-GUTT specifications and [GUTT_CROSS_PROMPT_CONSOLIDATION_ANALYSIS.md](docs/gutt_analysis/GUTT_CROSS_PROMPT_CONSOLIDATION_ANALYSIS.md) for consolidation methodology.

---

## C-GUTT Mapping Summary

**Implementation Focus**: Build the 39 atomic C-GUTTs rather than 66 discrete capabilities to achieve better code reuse and architectural clarity.

### High-Reuse C-GUTTs (Priority Implementation)

| C-GUTT | Capability Name | Prompts | Coverage | Priority |
|--------|----------------|---------|----------|----------|
| **C-01** | Calendar Event Retrieval | 5/9 | 76% | CRITICAL |
| **C-19** | Constraint Satisfaction & Slot Finding | 4/9 | 44% | HIGH |
| **C-02** | Multi-Calendar Availability Checking | 3/9 | 33% | HIGH |
| **C-07** | Meeting Update & Rescheduling | 3/9 | 33% | HIGH |
| **C-11** | Meeting Context Extraction | 3/9 | 33% | HIGH |
| **C-14** | Document Content Analysis | 3/9 | 33% | HIGH |
| **C-20** | Conflict Detection & Resolution | 3/9 | 33% | HIGH |
| **C-32** | Reporting & Visualization | 3/9 | 33% | MEDIUM |
| **C-33** | Document Assembly & Formatting | 3/9 | 33% | MEDIUM |

### C-GUTT Categories

1. **Calendar Data Operations** (7 C-GUTTs): C-01 to C-07
2. **Natural Language Processing** (8 C-GUTTs): C-08 to C-15
3. **Reasoning & Decision Making** (7 C-GUTTs): C-16 to C-22
4. **Analysis & Insights** (5 C-GUTTs): C-23 to C-27
5. **Resource Management** (3 C-GUTTs): C-28 to C-30
6. **Output & Communication** (3 C-GUTTs): C-31 to C-33
7. **Specialized Collaboration** (6 C-GUTTs): C-34 to C-39

**Implementation Strategy**:
- Build high-reuse C-GUTTs first (C-01, C-19, C-02, C-07, C-11, C-14, C-20)
- Top 9 C-GUTTs enable 67% of all hero prompt functionality
- 39 atomic capabilities provide 100% coverage with better architecture than 66 discrete tasks

---

## Usage

This document serves as the **ground truth reference** for evaluating LLM GUTT decomposition capabilities.

Use with `tools/gutt_decomposition_evaluator.py` to:
1. Compare LLM decompositions against these references
2. Calculate precision, recall, F1 scores
3. Assess granularity (over/under-decomposition)
4. Identify missing or extra GUTTs

**Next Steps**: Run Ollama analysis on all 9 prompts and compare results.
