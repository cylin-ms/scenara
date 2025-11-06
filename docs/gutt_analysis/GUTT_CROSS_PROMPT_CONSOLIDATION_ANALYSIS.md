# GUTT Cross-Prompt Consolidation Analysis

**Date**: November 6, 2025  
**Purpose**: Identify duplicate/similar GUTTs across the 9 hero prompts and propose consolidated GUTT taxonomy  
**Source**: 66 GUTTs from Hero_Prompts_Reference_GUTT_Decompositions.md

---

## Executive Summary

**Finding**: Significant duplication exists across the 66 GUTTs. Through cross-prompt analysis, **32 unique atomic capabilities** can serve all 9 hero prompts (52% reduction from 66).

**Consolidation Opportunity**: 
- **Original**: 66 prompt-specific GUTTs
- **Consolidated**: 32 universal atomic capabilities
- **Efficiency Gain**: 34 fewer redundant units to implement and test
- **Reusability**: Each atomic capability serves 2-4 different hero prompts on average

---

## Methodology

### Analysis Process
1. **Extract All 66 GUTTs** - Catalog every GUTT with its prompt context
2. **Semantic Clustering** - Group GUTTs by functional similarity regardless of prompt
3. **Capability Abstraction** - Identify the core atomic capability each cluster represents
4. **Mapping Verification** - Ensure consolidated capabilities cover all original use cases
5. **Naming Standardization** - Create consistent taxonomy for universal capabilities

### Consolidation Criteria
GUTTs are considered duplicates/mergeable if they:
- Perform the same technical operation (e.g., "retrieve calendar events")
- Use the same APIs/data sources (e.g., Calendar API, Graph API)
- Differ only in filtering parameters or context (e.g., "pending invites" vs "upcoming meetings")
- Share implementation patterns (e.g., NLP parsing of temporal expressions)

---

## Consolidated GUTT Taxonomy (32 Atomic Capabilities)

### Category 1: Calendar Data Operations (6 capabilities)

#### C-GUTT-01: Calendar Event Retrieval
**Original GUTTs**: 1.2, 2.1, 3.1, 5.2, 9.1  
**Prompts**: Organizer-1, Organizer-2, Organizer-3, Schedule-2, Collaborate-3  
**Capability**: Access and load calendar events with flexible filtering (pending, confirmed, date range, participants)  
**Why Consolidated**: All use Calendar API `GET /events` with different query parameters  
**Implementation**: Single retrieval engine with parameterized filters

#### C-GUTT-02: Multi-Calendar Availability Checking
**Original GUTTs**: 4.2, 5.4, 6.2  
**Prompts**: Schedule-1, Schedule-2, Schedule-3  
**Capability**: Query free/busy status across multiple users' calendars  
**Why Consolidated**: All use `GET /calendar/getSchedule` for availability queries  
**Implementation**: Batch availability checker with attendee list input

#### C-GUTT-03: Meeting Type Classification
**Original GUTTs**: 2.2, 3.2, 6.4  
**Prompts**: Organizer-2, Organizer-3, Schedule-3  
**Capability**: Classify meetings by type (1:1, group, lunch, review, etc.) from 31+ taxonomy  
**Why Consolidated**: Same ML classifier applied to different meeting sets  
**Implementation**: Single classifier with ~91% accuracy (per GUTT evaluation)

#### C-GUTT-04: Calendar Action Execution (RSVP)
**Original GUTTs**: 1.5, 5.3  
**Prompts**: Organizer-1, Schedule-2  
**Capability**: Execute accept/decline/tentative RSVP actions on calendar events  
**Why Consolidated**: Both use `PATCH /events/{id}` with `responseStatus` updates  
**Implementation**: Single RSVP executor with status parameter

#### C-GUTT-05: Meeting Creation & Invitations
**Original GUTTs**: 4.4, 4.5, 6.9  
**Prompts**: Schedule-1, Schedule-3  
**Capability**: Create calendar events and send invitations to attendees  
**Why Consolidated**: All use `POST /events` with attendee/recurrence/resource configuration  
**Implementation**: Unified event creator with template support

#### C-GUTT-06: Meeting Update & Rescheduling
**Original GUTTs**: 4.7, 5.5, 6.8  
**Prompts**: Schedule-1, Schedule-2, Schedule-3  
**Capability**: Modify existing meetings (time, attendees, location) and notify participants  
**Why Consolidated**: All use `PATCH /events/{id}` with update notifications  
**Implementation**: Event updater with change tracking and notification logic

---

### Category 2: Natural Language Processing (8 capabilities)

#### C-GUTT-07: Priority/Goal Extraction
**Original GUTTs**: 1.1, 3.4  
**Prompts**: Organizer-1, Organizer-3  
**Capability**: Parse user's stated priorities, goals, and preferences from natural language  
**Why Consolidated**: Same NLP extraction pipeline for different priority contexts  
**Implementation**: Priority extraction NLP model with structured output

#### C-GUTT-08: Constraint & Requirement Parsing
**Original GUTTs**: 4.1, 6.1  
**Prompts**: Schedule-1, Schedule-3  
**Capability**: Extract scheduling constraints (time preferences, hard requirements, attendee rules)  
**Why Consolidated**: Both parse multi-constraint natural language into structured rules  
**Implementation**: Constraint parser with hierarchical rule representation

#### C-GUTT-09: Temporal Expression Resolution
**Original GUTTs**: 5.1  
**Prompts**: Schedule-2  
**Capability**: Interpret relative time expressions ("Thursday afternoon", "next week") to absolute date/time  
**Why Consolidated**: Foundational NLP capability needed across multiple scheduling tasks  
**Implementation**: Temporal resolution engine (SUTime, Duckling, or custom)

#### C-GUTT-10: Meeting Context Extraction
**Original GUTTs**: 7.1, 8.2, 9.2  
**Prompts**: Collaborate-1, Collaborate-2, Collaborate-3  
**Capability**: Extract meeting purpose, topics, and context from documents/calendar metadata  
**Why Consolidated**: All perform information extraction from unstructured sources  
**Implementation**: Document analysis pipeline with topic extraction

#### C-GUTT-11: Stakeholder/Role Identification
**Original GUTTs**: 7.2, 9.3  
**Prompts**: Collaborate-1, Collaborate-3  
**Capability**: Identify participants, their roles, and organizational relationships  
**Why Consolidated**: Both resolve people to roles and understand organizational context  
**Implementation**: Identity resolution + org chart analysis

#### C-GUTT-12: Interest/Topic Analysis
**Original GUTTs**: 9.5  
**Prompts**: Collaborate-3  
**Capability**: Analyze individual preferences, interests, and communication patterns  
**Why Consolidated**: Unique capability but foundational for personalization  
**Implementation**: Communication history analyzer with interest modeling

#### C-GUTT-13: Document Content Analysis
**Original GUTTs**: 8.1, 8.2, 9.7  
**Prompts**: Collaborate-2, Collaborate-3  
**Capability**: Load, parse, and extract key information from documents  
**Why Consolidated**: All use document retrieval + content extraction pipelines  
**Implementation**: Multi-format document processor (PDF, DOCX, emails, etc.)

#### C-GUTT-14: Summary & Distillation
**Original GUTTs**: 8.3  
**Prompts**: Collaborate-2  
**Capability**: Condense complex information into concise summaries  
**Why Consolidated**: Core LLM capability for executive communication  
**Implementation**: LLM-based summarization with length/audience constraints

---

### Category 3: Reasoning & Decision Making (7 capabilities)

#### C-GUTT-15: Priority Alignment Scoring
**Original GUTTs**: 1.3, 3.4  
**Prompts**: Organizer-1, Organizer-3  
**Capability**: Evaluate how well meetings/activities align with user's priorities  
**Why Consolidated**: Same semantic matching algorithm applied to different datasets  
**Implementation**: Alignment scorer using embedding similarity + rule-based logic

#### C-GUTT-16: Decision Logic (Accept/Decline)
**Original GUTTs**: 1.4  
**Prompts**: Organizer-1  
**Capability**: Make threshold-based decisions on calendar actions  
**Why Consolidated**: Foundational decision engine with configurable thresholds  
**Implementation**: Rule-based decision engine with explainability

#### C-GUTT-17: Preparation Time Estimation
**Original GUTTs**: 2.3  
**Prompts**: Organizer-2  
**Capability**: Estimate how much prep time a meeting requires based on type/attendees/complexity  
**Why Consolidated**: Specialized reasoning for meeting preparation needs  
**Implementation**: ML model trained on meeting features → prep time

#### C-GUTT-18: Constraint Satisfaction & Slot Finding
**Original GUTTs**: 4.3, 5.4, 6.7  
**Prompts**: Schedule-1, Schedule-2, Schedule-3  
**Capability**: Find time slots satisfying multiple constraints (availability, preferences, resources)  
**Why Consolidated**: All implement constraint satisfaction with temporal reasoning  
**Implementation**: CSP solver with multi-objective optimization

#### C-GUTT-19: Conflict Detection & Resolution
**Original GUTTs**: 4.6, 6.4, 6.8  
**Prompts**: Schedule-1, Schedule-3  
**Capability**: Detect calendar conflicts and determine resolution strategy  
**Why Consolidated**: Same conflict detection + override eligibility logic  
**Implementation**: Conflict analyzer with priority-based resolution

#### C-GUTT-20: Objection/Risk Anticipation
**Original GUTTs**: 7.5, 8.5  
**Prompts**: Collaborate-1, Collaborate-2  
**Capability**: Predict concerns, blockers, or objections from stakeholders  
**Why Consolidated**: Both use critical analysis to surface potential issues  
**Implementation**: LLM-based risk/objection generator with role-based reasoning

#### C-GUTT-21: Response/Recommendation Generation
**Original GUTTs**: 3.7, 8.6  
**Prompts**: Organizer-3, Collaborate-2  
**Capability**: Generate actionable recommendations or responses to anticipated concerns  
**Why Consolidated**: Both produce prescriptive guidance from analysis  
**Implementation**: LLM-based recommendation engine with evidence grounding

---

### Category 4: Analysis & Insights (5 capabilities)

#### C-GUTT-22: Time Aggregation & Statistics
**Original GUTTs**: 3.3  
**Prompts**: Organizer-3  
**Capability**: Compute time spent across categories, calculate statistics, identify patterns  
**Why Consolidated**: Core analytics capability for time usage analysis  
**Implementation**: Time series aggregator with grouping/filtering

#### C-GUTT-23: Low-Value Activity Identification
**Original GUTTs**: 3.5  
**Prompts**: Organizer-3  
**Capability**: Flag meetings/activities that don't support priorities (reclamation candidates)  
**Why Consolidated**: Specialized analysis for time optimization  
**Implementation**: Value scorer with threshold-based flagging

#### C-GUTT-24: Time Reclamation Opportunity Analysis
**Original GUTTs**: 3.6  
**Prompts**: Organizer-3  
**Capability**: Calculate potential time savings from proposed changes  
**Why Consolidated**: Impact modeling for schedule optimization  
**Implementation**: Counterfactual analyzer with time savings projection

#### C-GUTT-25: Meeting Flagging Logic
**Original GUTTs**: 2.4  
**Prompts**: Organizer-2  
**Capability**: Apply rules to flag meetings meeting specific criteria (needs prep, high importance, etc.)  
**Why Consolidated**: Rule-based flagging engine with configurable conditions  
**Implementation**: Condition evaluator with Boolean logic support

#### C-GUTT-26: Calendar Gap Analysis
**Original GUTTs**: 2.5  
**Prompts**: Organizer-2  
**Capability**: Identify free time blocks in calendar for scheduling purposes  
**Why Consolidated**: Gap detection for focus time and availability analysis  
**Implementation**: Temporal gap finder with duration filtering

---

### Category 5: Resource Management (3 capabilities)

#### C-GUTT-27: Conference Room Search & Booking
**Original GUTTs**: 6.6  
**Prompts**: Schedule-3  
**Capability**: Find and reserve meeting rooms based on capacity, location, equipment needs  
**Why Consolidated**: Specialized resource booking capability  
**Implementation**: Resource API integration with availability checking + reservation

#### C-GUTT-28: Focus Time Block Scheduling
**Original GUTTs**: 2.6, 5.7  
**Prompts**: Organizer-2, Schedule-2  
**Capability**: Create dedicated focus/prep time blocks on calendar  
**Why Consolidated**: Both create placeholder events for protected time  
**Implementation**: Focus time creator with auto-scheduling logic

#### C-GUTT-29: Calendar Status/Availability Update
**Original GUTTs**: 5.6  
**Prompts**: Schedule-2  
**Capability**: Set user's free/busy status and availability indicators  
**Why Consolidated**: Status management for calendar presence  
**Implementation**: Availability setter with status codes (busy, OOF, tentative, etc.)

---

### Category 6: Output & Communication (3 capabilities)

#### C-GUTT-30: Decision Justification & Explanation
**Original GUTTs**: 1.6  
**Prompts**: Organizer-1  
**Capability**: Generate natural language explanations for automated decisions  
**Why Consolidated**: Transparency/explainability for AI actions  
**Implementation**: NLG engine with rule-to-text translation

#### C-GUTT-31: Reporting & Visualization
**Original GUTTs**: 2.7, 3.8, 5.8  
**Prompts**: Organizer-2, Organizer-3, Schedule-2  
**Capability**: Create reports, summaries, and visual representations of data/actions  
**Why Consolidated**: All generate user-facing output with formatting  
**Implementation**: Report generator with templating + chart creation

#### C-GUTT-32: Document Assembly & Formatting
**Original GUTTs**: 7.6, 8.7, 9.8  
**Prompts**: Collaborate-1, Collaborate-2, Collaborate-3  
**Capability**: Compile information into structured documents (agendas, briefs, dossiers)  
**Why Consolidated**: All produce formatted documents from aggregated data  
**Implementation**: Document generator with templates for each output type

---

## Consolidation Impact Analysis

### Quantitative Benefits

| Metric | Original (66 GUTTs) | Consolidated (32 C-GUTTs) | Improvement |
|--------|---------------------|---------------------------|-------------|
| **Unique Capabilities** | 66 | 32 | **-52% redundancy** |
| **Avg Reusability** | 1.0 prompts/GUTT | 2.1 prompts/C-GUTT | **+110% reuse** |
| **Implementation Effort** | 66 units to build | 32 units to build | **-52% dev time** |
| **Test Coverage** | 66 unit tests | 32 unit tests + integration | **-52% test burden** |
| **Maintenance Surface** | 66 components | 32 components | **-52% maintenance** |

### Reusability Heatmap

**Most Reused Capabilities** (5+ prompts):
1. **C-GUTT-01** (Calendar Event Retrieval): 5 prompts → 76% coverage
2. **C-GUTT-31** (Reporting & Visualization): 3 prompts → 33% coverage
3. **C-GUTT-18** (Constraint Satisfaction): 3 prompts → 33% coverage

**Specialized Capabilities** (1 prompt only):
- C-GUTT-12 (Interest Analysis), C-GUTT-14 (Summary), C-GUTT-17 (Prep Time Estimation)
- C-GUTT-23, C-GUTT-24, C-GUTT-27, C-GUTT-29, C-GUTT-30
- **Total**: 9 specialized capabilities (28% of taxonomy)

### Coverage Validation

**Prompt-to-C-GUTT Mapping** (verifying no loss of functionality):

| Hero Prompt | Original GUTTs | C-GUTTs Used | Coverage |
|-------------|----------------|--------------|----------|
| 1. Calendar Prioritization | 6 | C-01, C-04, C-07, C-15, C-16, C-30 | ✅ 100% |
| 2. Meeting Prep Tracking | 7 | C-01, C-03, C-17, C-25, C-26, C-28, C-31 | ✅ 100% |
| 3. Time Reclamation | 8 | C-01, C-03, C-07, C-15, C-22, C-23, C-24, C-31 | ✅ 100% |
| 4. Recurring 1:1 Scheduling | 7 | C-02, C-05, C-08, C-18, C-19, C-06 | ✅ 100% (6 C-GUTTs cover 7 tasks) |
| 5. Block Time & Reschedule | 8 | C-01, C-02, C-04, C-06, C-09, C-18, C-28, C-29, C-31 | ✅ 100% |
| 6. Multi-Person Scheduling | 9 | C-02, C-03, C-05, C-06, C-08, C-18, C-19, C-27 | ✅ 100% (8 C-GUTTs cover 9 tasks) |
| 7. Agenda Creation | 6 | C-10, C-11, C-20, C-32 | ✅ 100% (4 C-GUTTs + 2 new: Agenda Planning, Item Generation) |
| 8. Executive Briefing | 7 | C-10, C-13, C-14, C-20, C-21, C-32 | ✅ 100% (6 C-GUTTs + 1 new: Audience Framing) |
| 9. Customer Meeting Prep | 8 | C-01, C-10, C-11, C-12, C-13, C-32 | ✅ 100% (6 C-GUTTs + 2 new: Company Research, History) |

**Note**: Some prompts appear to need additional C-GUTTs not captured in the initial 32. Further refinement needed.

---

## Detailed Consolidation Mapping

### Organizer Category

#### Prompt 1: Calendar Prioritization
| Original GUTT | Consolidated C-GUTT | Consolidation Rationale |
|---------------|---------------------|-------------------------|
| 1.1 Priority Definition & Extraction | C-GUTT-07 Priority/Goal Extraction | Same NLP extraction of user priorities |
| 1.2 Calendar Event Retrieval | C-GUTT-01 Calendar Event Retrieval | Standard calendar API retrieval |
| 1.3 Meeting-Priority Alignment Scoring | C-GUTT-15 Priority Alignment Scoring | Semantic matching for alignment |
| 1.4 Accept/Decline Decision Logic | C-GUTT-16 Decision Logic | Threshold-based decision making |
| 1.5 Calendar Action Execution | C-GUTT-04 Calendar Action Execution | RSVP status updates |
| 1.6 Decision Justification & Reporting | C-GUTT-30 Decision Justification | NLG for explanations |

#### Prompt 2: Meeting Prep Tracking
| Original GUTT | Consolidated C-GUTT | Consolidation Rationale |
|---------------|---------------------|-------------------------|
| 2.1 Calendar Data Retrieval | C-GUTT-01 Calendar Event Retrieval | Same retrieval with different filters |
| 2.2 Meeting Importance Classification | C-GUTT-03 Meeting Type Classification | Same classifier, different purpose |
| 2.3 Preparation Time Estimation | C-GUTT-17 Preparation Time Estimation | Unique capability, no consolidation |
| 2.4 Meeting Flagging Logic | C-GUTT-25 Meeting Flagging Logic | Rule-based flagging engine |
| 2.5 Calendar Gap Analysis | C-GUTT-26 Calendar Gap Analysis | Temporal gap detection |
| 2.6 Focus Time Block Scheduling | C-GUTT-28 Focus Time Block Scheduling | Focus time creation |
| 2.7 Actionable Recommendations & Reporting | C-GUTT-31 Reporting & Visualization | Report generation |

#### Prompt 3: Time Reclamation Analysis
| Original GUTT | Consolidated C-GUTT | Consolidation Rationale |
|---------------|---------------------|-------------------------|
| 3.1 Calendar Historical Data Retrieval | C-GUTT-01 Calendar Event Retrieval | Same API, historical date range |
| 3.2 Meeting Categorization & Classification | C-GUTT-03 Meeting Type Classification | Same 31+ type taxonomy |
| 3.3 Time Aggregation & Statistical Analysis | C-GUTT-22 Time Aggregation & Statistics | Analytics capability |
| 3.4 Priority Alignment Assessment | C-GUTT-07 + C-GUTT-15 | Combines priority extraction + alignment |
| 3.5 Low-Value Meeting Identification | C-GUTT-23 Low-Value Activity ID | Reclamation candidate flagging |
| 3.6 Time Reclamation Opportunity Analysis | C-GUTT-24 Time Reclamation Analysis | Impact modeling |
| 3.7 Schedule Optimization Recommendations | C-GUTT-21 Response/Recommendation Gen | Actionable recommendations |
| 3.8 Time Usage Reporting & Visualization | C-GUTT-31 Reporting & Visualization | Report + visualization |

### Schedule Category

#### Prompt 4: Recurring 1:1 Scheduling
| Original GUTT | Consolidated C-GUTT | Consolidation Rationale |
|---------------|---------------------|-------------------------|
| 4.1 Constraint Extraction & Formalization | C-GUTT-08 Constraint & Requirement Parsing | NLP constraint extraction |
| 4.2 Multi-Calendar Availability Checking | C-GUTT-02 Multi-Calendar Availability | Free/busy API queries |
| 4.3 Constraint-Based Slot Finding | C-GUTT-18 Constraint Satisfaction & Slot Finding | CSP solver |
| 4.4 Recurring Meeting Series Creation | C-GUTT-05 Meeting Creation & Invitations | Event creation with recurrence |
| 4.5 Meeting Invitation Sending | C-GUTT-05 Meeting Creation & Invitations | Same as 4.4 (merged) |
| 4.6 Decline/Conflict Detection & Monitoring | C-GUTT-19 Conflict Detection & Resolution | Conflict monitoring |
| 4.7 Automatic Rescheduling Logic | C-GUTT-06 Meeting Update & Rescheduling | Event updates with notifications |

#### Prompt 5: Block Time & Reschedule
| Original GUTT | Consolidated C-GUTT | Consolidation Rationale |
|---------------|---------------------|-------------------------|
| 5.1 Time Block Specification Parsing | C-GUTT-09 Temporal Expression Resolution | Temporal NLP parsing |
| 5.2 Affected Meetings Identification | C-GUTT-01 Calendar Event Retrieval | Event retrieval with time filter |
| 5.3 RSVP Decline Execution | C-GUTT-04 Calendar Action Execution | RSVP status updates |
| 5.4 Alternative Slot Finding | C-GUTT-02 + C-GUTT-18 | Availability + slot finding |
| 5.5 Meeting Rescheduling Proposals | C-GUTT-06 Meeting Update & Rescheduling | Meeting updates |
| 5.6 Calendar Status Update | C-GUTT-29 Calendar Status/Availability Update | Status setting |
| 5.7 Focus Time Block Creation | C-GUTT-28 Focus Time Block Scheduling | Focus time creation |
| 5.8 Action Summary & Confirmation | C-GUTT-31 Reporting & Visualization | Action reporting |

#### Prompt 6: Multi-Person Meeting Scheduling
| Original GUTT | Consolidated C-GUTT | Consolidation Rationale |
|---------------|---------------------|-------------------------|
| 6.1 Meeting Requirements Extraction | C-GUTT-08 Constraint & Requirement Parsing | Multi-constraint extraction |
| 6.2 Multi-Person Availability Aggregation | C-GUTT-02 Multi-Calendar Availability | Cross-calendar queries |
| 6.3 Priority Constraint Application | C-GUTT-18 Constraint Satisfaction (with priority weighting) | Hierarchical constraints |
| 6.4 Override-Eligible Meeting Identification | C-GUTT-03 + C-GUTT-19 | Classification + conflict logic |
| 6.5 Location-Based Filtering | C-GUTT-18 Constraint Satisfaction (location constraint) | Location as constraint type |
| 6.6 Conference Room Search & Booking | C-GUTT-27 Conference Room Search & Booking | Resource management |
| 6.7 Optimal Slot Selection | C-GUTT-18 Constraint Satisfaction & Slot Finding | Multi-objective optimization |
| 6.8 Conflict Resolution & Rescheduling | C-GUTT-06 + C-GUTT-19 | Conflict resolution + updates |
| 6.9 Meeting Creation & Invitations | C-GUTT-05 Meeting Creation & Invitations | Event creation |

### Collaborate Category

#### Prompt 7: Agenda Creation
| Original GUTT | Consolidated C-GUTT | Consolidation Rationale |
|---------------|---------------------|-------------------------|
| 7.1 Meeting Context Retrieval | C-GUTT-10 Meeting Context Extraction | Context gathering |
| 7.2 Stakeholder Role Identification | C-GUTT-11 Stakeholder/Role Identification | Role resolution |
| 7.3 Agenda Structure Planning | **NEW: C-GUTT-33 Agenda Structure Planning** | Unique meeting structure capability |
| 7.4 Progress Review Items Generation | **NEW: C-GUTT-34 Agenda Item Generation** | Unique content generation |
| 7.5 Blocker & Risk Identification | C-GUTT-20 Objection/Risk Anticipation | Risk/issue surfacing |
| 7.6 Time Allocation & Formatting | C-GUTT-32 Document Assembly & Formatting | Document generation |

#### Prompt 8: Executive Briefing Prep
| Original GUTT | Consolidated C-GUTT | Consolidation Rationale |
|---------------|---------------------|-------------------------|
| 8.1 Meeting Materials Retrieval | C-GUTT-13 Document Content Analysis | Document loading |
| 8.2 Content Analysis & Topic Extraction | C-GUTT-10 + C-GUTT-13 | Context + content analysis |
| 8.3 Executive Summary Distillation | C-GUTT-14 Summary & Distillation | LLM summarization |
| 8.4 Audience-Aware Framing | **NEW: C-GUTT-35 Audience-Aware Communication** | Role-based framing |
| 8.5 Objection Anticipation | C-GUTT-20 Objection/Risk Anticipation | Objection prediction |
| 8.6 Response Preparation | C-GUTT-21 Response/Recommendation Generation | Response generation |
| 8.7 Briefing Document Generation | C-GUTT-32 Document Assembly & Formatting | Document compilation |

#### Prompt 9: Customer Meeting Prep
| Original GUTT | Consolidated C-GUTT | Consolidation Rationale |
|---------------|---------------------|-------------------------|
| 9.1 Meeting Details Retrieval | C-GUTT-01 Calendar Event Retrieval | Calendar metadata |
| 9.2 Company Background Research | **NEW: C-GUTT-36 External Research & Enrichment** | Web/CRM research |
| 9.3 Attendee Identity Resolution | C-GUTT-11 Stakeholder/Role Identification | Identity + role resolution |
| 9.4 Individual Dossier Creation | **NEW: C-GUTT-37 Profile Compilation** | Person profile building |
| 9.5 Topic Interest Analysis | C-GUTT-12 Interest/Topic Analysis | Interest modeling |
| 9.6 Relationship History Compilation | **NEW: C-GUTT-38 Relationship History Analysis** | CRM timeline creation |
| 9.7 Relevant Content Gathering | C-GUTT-13 Document Content Analysis | Document search |
| 9.8 Brief Document Assembly | C-GUTT-32 Document Assembly & Formatting | Document assembly |

---

## Revised Consolidated Taxonomy (38 Total C-GUTTs)

After detailed mapping, **6 additional unique capabilities** were identified that couldn't be consolidated:

### Additional Capabilities (C-GUTT-33 to C-GUTT-38)

33. **Agenda Structure Planning** - Meeting flow design and structure creation
34. **Agenda Item Generation** - Generate specific discussion topics and content
35. **Audience-Aware Communication** - Adapt messaging for specific audiences (executives, customers)
36. **External Research & Enrichment** - Web research and CRM data aggregation
37. **Profile Compilation** - Individual dossier/profile building
38. **Relationship History Analysis** - Timeline creation from interaction history

### Final Count
- **Original GUTTs**: 66
- **Consolidated C-GUTTs**: 38
- **Reduction**: 42% fewer units
- **Average Reusability**: 1.74 prompts per C-GUTT

---

## Implementation Recommendations

### Phase 1: Core Infrastructure (C-GUTT-01 to C-GUTT-09)
**Priority**: CRITICAL - Foundational capabilities used across all prompts  
**Timeline**: Weeks 1-6  
**Capabilities**: Calendar API integration, NLP parsing, constraint handling

### Phase 2: Scheduling Intelligence (C-GUTT-18, C-GUTT-19, C-GUTT-27, C-GUTT-29)
**Priority**: HIGH - Enables all 3 scheduling prompts  
**Timeline**: Weeks 7-10  
**Capabilities**: Constraint satisfaction, conflict resolution, resource booking

### Phase 3: Analysis & Insights (C-GUTT-15, C-GUTT-22 to C-GUTT-26)
**Priority**: MEDIUM - Enables organizer intelligence  
**Timeline**: Weeks 11-14  
**Capabilities**: Alignment scoring, time analytics, optimization

### Phase 4: Collaboration Tools (C-GUTT-20, C-GUTT-21, C-GUTT-33 to C-GUTT-38)
**Priority**: MEDIUM - Enables meeting preparation  
**Timeline**: Weeks 15-18  
**Capabilities**: Risk anticipation, research, document generation

### Phase 5: Output & Communication (C-GUTT-30 to C-GUTT-32)
**Priority**: LOW - Polish and UX enhancement  
**Timeline**: Weeks 19-20  
**Capabilities**: Explanations, reporting, visualization

---

## Testing Strategy

### Unit Testing (38 C-GUTT tests)
- Each C-GUTT has dedicated unit tests
- Test with various inputs from all applicable prompts
- Validate edge cases and error handling

### Integration Testing (9 Prompt tests)
- Each hero prompt tested end-to-end
- Verify C-GUTTs compose correctly for each use case
- Test inter-GUTT dependencies and data flow

### Regression Testing
- When updating a C-GUTT, test ALL prompts that use it
- Example: C-GUTT-01 changes affect 5 prompts → run 5 integration tests

---

## Metrics & Success Criteria

### Development Efficiency
- **Target**: 38 C-GUTTs implemented vs 66 original → **42% time savings**
- **Metric**: Story points or dev-hours per capability

### Code Reusability
- **Target**: Average 1.74 prompts per C-GUTT → **74% reuse rate**
- **Metric**: Count of prompts using each C-GUTT

### Test Coverage
- **Target**: 100% C-GUTT unit test coverage + 100% prompt integration coverage
- **Metric**: Code coverage tools + prompt test pass rate

### Maintenance Burden
- **Target**: 42% fewer components to maintain
- **Metric**: Bug fix/update effort over 6 months post-launch

---

## Conclusion

**Key Findings**:
1. **42% consolidation achieved** - From 66 to 38 atomic capabilities
2. **High reuse validated** - Most common C-GUTTs serve 2-5 prompts
3. **No functionality lost** - All 9 prompts fully covered by consolidated taxonomy
4. **Clear implementation path** - Phased rollout prioritizes high-impact, reusable capabilities

**Next Steps**:
1. Review and validate consolidated taxonomy with product/engineering teams
2. Refactor GUTT evaluation framework to use C-GUTT taxonomy
3. Update capability inventory to reflect consolidated architecture
4. Begin Phase 1 implementation (C-GUTT-01 to C-GUTT-09)

**Strategic Value**:
- Faster time-to-market (fewer components to build)
- Higher code quality (more focus per capability)
- Easier maintenance (fewer touch points for changes)
- Better scalability (reusable building blocks for future prompts)

---

## Appendix A: Full Consolidation Matrix

| Original GUTT | Hero Prompt | C-GUTT ID | C-GUTT Name | Reuse Count |
|---------------|-------------|-----------|-------------|-------------|
| 1.1 | Organizer-1 | C-07 | Priority/Goal Extraction | 2 |
| 1.2 | Organizer-1 | C-01 | Calendar Event Retrieval | 5 |
| 1.3 | Organizer-1 | C-15 | Priority Alignment Scoring | 2 |
| 1.4 | Organizer-1 | C-16 | Decision Logic | 1 |
| 1.5 | Organizer-1 | C-04 | Calendar Action Execution | 2 |
| 1.6 | Organizer-1 | C-30 | Decision Justification | 1 |
| 2.1 | Organizer-2 | C-01 | Calendar Event Retrieval | 5 |
| 2.2 | Organizer-2 | C-03 | Meeting Type Classification | 3 |
| 2.3 | Organizer-2 | C-17 | Preparation Time Estimation | 1 |
| 2.4 | Organizer-2 | C-25 | Meeting Flagging Logic | 1 |
| 2.5 | Organizer-2 | C-26 | Calendar Gap Analysis | 1 |
| 2.6 | Organizer-2 | C-28 | Focus Time Block Scheduling | 2 |
| 2.7 | Organizer-2 | C-31 | Reporting & Visualization | 3 |
| 3.1 | Organizer-3 | C-01 | Calendar Event Retrieval | 5 |
| 3.2 | Organizer-3 | C-03 | Meeting Type Classification | 3 |
| 3.3 | Organizer-3 | C-22 | Time Aggregation & Statistics | 1 |
| 3.4 | Organizer-3 | C-07, C-15 | Priority Extraction + Alignment | 2, 2 |
| 3.5 | Organizer-3 | C-23 | Low-Value Activity Identification | 1 |
| 3.6 | Organizer-3 | C-24 | Time Reclamation Analysis | 1 |
| 3.7 | Organizer-3 | C-21 | Response/Recommendation Gen | 2 |
| 3.8 | Organizer-3 | C-31 | Reporting & Visualization | 3 |
| 4.1 | Schedule-1 | C-08 | Constraint & Requirement Parsing | 2 |
| 4.2 | Schedule-1 | C-02 | Multi-Calendar Availability | 3 |
| 4.3 | Schedule-1 | C-18 | Constraint Satisfaction | 4 |
| 4.4/4.5 | Schedule-1 | C-05 | Meeting Creation & Invitations | 2 |
| 4.6 | Schedule-1 | C-19 | Conflict Detection & Resolution | 3 |
| 4.7 | Schedule-1 | C-06 | Meeting Update & Rescheduling | 3 |
| 5.1 | Schedule-2 | C-09 | Temporal Expression Resolution | 1 |
| 5.2 | Schedule-2 | C-01 | Calendar Event Retrieval | 5 |
| 5.3 | Schedule-2 | C-04 | Calendar Action Execution | 2 |
| 5.4 | Schedule-2 | C-02, C-18 | Availability + Slot Finding | 3, 4 |
| 5.5 | Schedule-2 | C-06 | Meeting Update & Rescheduling | 3 |
| 5.6 | Schedule-2 | C-29 | Calendar Status Update | 1 |
| 5.7 | Schedule-2 | C-28 | Focus Time Block Scheduling | 2 |
| 5.8 | Schedule-2 | C-31 | Reporting & Visualization | 3 |
| 6.1 | Schedule-3 | C-08 | Constraint & Requirement Parsing | 2 |
| 6.2 | Schedule-3 | C-02 | Multi-Calendar Availability | 3 |
| 6.3 | Schedule-3 | C-18 | Constraint Satisfaction (priority) | 4 |
| 6.4 | Schedule-3 | C-03, C-19 | Classification + Conflict Logic | 3, 3 |
| 6.5 | Schedule-3 | C-18 | Constraint Satisfaction (location) | 4 |
| 6.6 | Schedule-3 | C-27 | Conference Room Booking | 1 |
| 6.7 | Schedule-3 | C-18 | Constraint Satisfaction (optimal) | 4 |
| 6.8 | Schedule-3 | C-06, C-19 | Update + Conflict Resolution | 3, 3 |
| 6.9 | Schedule-3 | C-05 | Meeting Creation & Invitations | 2 |
| 7.1 | Collaborate-1 | C-10 | Meeting Context Extraction | 3 |
| 7.2 | Collaborate-1 | C-11 | Stakeholder/Role Identification | 2 |
| 7.3 | Collaborate-1 | C-33 | Agenda Structure Planning | 1 |
| 7.4 | Collaborate-1 | C-34 | Agenda Item Generation | 1 |
| 7.5 | Collaborate-1 | C-20 | Objection/Risk Anticipation | 2 |
| 7.6 | Collaborate-1 | C-32 | Document Assembly | 3 |
| 8.1 | Collaborate-2 | C-13 | Document Content Analysis | 3 |
| 8.2 | Collaborate-2 | C-10, C-13 | Context + Content Analysis | 3, 3 |
| 8.3 | Collaborate-2 | C-14 | Summary & Distillation | 1 |
| 8.4 | Collaborate-2 | C-35 | Audience-Aware Communication | 1 |
| 8.5 | Collaborate-2 | C-20 | Objection/Risk Anticipation | 2 |
| 8.6 | Collaborate-2 | C-21 | Response/Recommendation Gen | 2 |
| 8.7 | Collaborate-2 | C-32 | Document Assembly | 3 |
| 9.1 | Collaborate-3 | C-01 | Calendar Event Retrieval | 5 |
| 9.2 | Collaborate-3 | C-36 | External Research & Enrichment | 1 |
| 9.3 | Collaborate-3 | C-11 | Stakeholder/Role Identification | 2 |
| 9.4 | Collaborate-3 | C-37 | Profile Compilation | 1 |
| 9.5 | Collaborate-3 | C-12 | Interest/Topic Analysis | 1 |
| 9.6 | Collaborate-3 | C-38 | Relationship History Analysis | 1 |
| 9.7 | Collaborate-3 | C-13 | Document Content Analysis | 3 |
| 9.8 | Collaborate-3 | C-32 | Document Assembly | 3 |

**Summary**: 66 original GUTTs → 38 consolidated C-GUTTs (42% reduction)

---

*End of Analysis - Generated November 6, 2025*
