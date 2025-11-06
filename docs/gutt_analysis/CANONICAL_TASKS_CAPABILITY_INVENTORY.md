# Enterprise Meeting Intelligence - Canonical Tasks Capability Inventory

**Date**: November 7, 2025 (Canonical Unit Tasks Framework v2.0)  
**Author**: Chin-Yew Lin  
**Source**: Gold standard analysis of 9 Calendar.AI Hero Prompts  
**Framework**: 24 Canonical Unit Tasks (validated through 4-phase methodology)  
**Purpose**: Define atomic capabilities required for production implementation

**Related Documents**:
- [CANONICAL_TASKS_GOLD_STANDARD_REFERENCE.md](./CANONICAL_TASKS_GOLD_STANDARD_REFERENCE.md) - Complete gold standard with all 9 hero prompt analyses
- [GPT5_OPTIMIZATION_SUMMARY.md](./model_comparison/GPT5_OPTIMIZATION_SUMMARY.md) - 3-trial stability test and optimization results
- [CANONICAL_UNIT_TASKS_REFERENCE.md](./CANONICAL_UNIT_TASKS_REFERENCE.md) - Complete specifications for all 24 canonical tasks

---

## Journey to Canonical Tasks Framework

This document represents the culmination of a rigorous **4-phase methodology** to establish a validated, production-ready framework for Calendar.AI capabilities:

### Phase 1: Original GUTT Analysis (October-November 2025)
**Objective**: Understand Calendar.AI requirements through hero prompts

- **Manual Decomposition**: Expert analysis of 9 hero prompts into 66 capability requirements
- **Cross-Prompt Consolidation**: Identified common patterns, reduced to 39 atomic C-GUTTs (Consolidated Generative Unit Test Tasks)
- **Framework Evolution**: Refined boundaries between capabilities, established parent-child relationships
- **Key Achievement**: 41% reduction (66→39 tasks) through consolidation, average 1.69 prompts per task

**Limitations Identified**:
- Manual analysis prone to inconsistency
- No validation against LLM capabilities
- Unclear which tasks are truly "atomic"
- Missing specialized capabilities (e.g., conflict resolution, risk anticipation)

### Phase 2: GPT-5 Baseline Analysis (November 6, 2025)
**Objective**: Validate framework with automated LLM analysis

- **Automated Analysis**: GPT-5 analyzed all 9 hero prompts using initial system prompts
- **Performance Baseline**: F1 79.74% (single run, no variance data)
- **Critical Gaps Discovered**:
  - CAN-07 (Metadata Extraction): Only 55.6% detection rate (5/9 prompts)
  - CAN-23 (Conflict Resolution): 0% detection rate (0/9 prompts)
  - CAN-22 (Work Attribution): 11% detection rate (1/9 prompts)
  - CAN-18 (Risk Anticipation): 0% detection rate
  - CAN-20 (Visualization): Poor detection

**Key Insight**: Initial prompts lacked explicit guidance for parent tasks, specialized capabilities, and task differentiation (e.g., CAN-02A vs CAN-02B, CAN-07 vs CAN-13).

### Phase 3: Prompt Optimization & 3-Trial Stability Test (November 7, 2025)
**Objective**: Optimize LLM prompts and validate with statistical rigor

**6 Critical Prompt Enhancements**:
1. **CAN-07 Parent Task Guidance**: Explicit keywords ("pending invitations", "RSVP", "attendees", "documents"), child task list (CAN-13, CAN-05, CAN-08, CAN-09, CAN-19, CAN-21)
2. **CAN-02A vs CAN-02B Differentiation**: OBJECTIVE type classification vs SUBJECTIVE importance assessment
3. **CAN-13 vs CAN-07 Read/Write Distinction**: WRITE operations (send/update) vs READ operations (extract)
4. **Specialized Task Keywords**: CAN-18 ("anticipate", "risks"), CAN-20 ("visualize", "show"), CAN-23 ("auto-reschedule", "bump")
5. **DO/DON'T Guidelines**: 9 explicit rules for task selection
6. **Dependency Chains**: Clear ordering requirements (CAN-01→CAN-06, CAN-07→children, CAN-12→CAN-23)

**3-Trial Stability Test Results**:
- **27 API Calls**: 3 independent trials × 9 hero prompts (100% success rate)
- **Average Performance**: F1 78.40% ± 0.72% (EXCELLENT < 1% variance)
- **Consistency**: 93.6% task selection agreement across trials
- **Major Improvements**:
  - CAN-07: 55.6% → **100%** (+44.4%)
  - CAN-23: 0% → **66.7%** (+66.7%)
  - CAN-22: 11% → **100%** in collaborate prompts (+89%)
  - CAN-18: 0% → **33.3%** (+33.3%)
  - CAN-20: 11% → **66.7%** (+55.7%)

**Statistical Validation**: < 1% F1 variance proves framework stability and LLM prompt quality.

### Phase 4: Human Correction & Gold Standard Creation (November 7, 2025)
**Objective**: Create authoritative reference through expert review

- **Expert Review**: Human expert (Chin-Yew Lin) reviewed all GPT-5 optimized outputs
- **Systematic Corrections**:
  - Ensured all 24 canonical tasks represented across 9 prompts
  - Added missing CAN-04 (NLU) to prompts where omitted (100% coverage required)
  - Consistently split CAN-02 into CAN-02A (Type) and CAN-02B (Importance)
  - Added CAN-07 (Metadata Extraction) wherever "pending invitations" appeared
  - Added orchestrated workflows: CAN-17 (Auto-Rescheduling), CAN-23 (Conflict Resolution)
  - Added optional enhancements: CAN-18 (Risk Anticipation), CAN-20 (Visualization)
- **Cross-Validation**: Compared with original GUTT decompositions to ensure completeness
- **Final Framework**: 24 canonical unit tasks (23 unique + CAN-02A/CAN-02B split)

**Gold Standard Statistics**:
- **Coverage**: 100% Tier 1 (Universal), 95% Tier 2 (Common), 71% Tier 3 (Specialized)
- **Average**: 7.8 tasks per prompt (range: 7-11)
- **Frequency Leaders**: CAN-04, CAN-01, CAN-07 at 100% (9/9 prompts)
- **Validation**: Human-corrected, LLM-validated, scientifically rigorous

---

## Document Purpose

This document presents the **infrastructure-centric view** of capabilities needed to implement the **24 Canonical Unit Tasks** that serve all 9 Calendar.AI hero prompts.

**What are Canonical Unit Tasks?**
- **Atomic capabilities**: Each task is a single, well-defined functional unit
- **Framework-validated**: Validated through 4-phase human-in-the-loop + LLM methodology
- **Production-ready**: Gold standard reference with statistical validation (93.6% consistency)
- **Implementation focus**: These 24 tasks are what must be built - proven coverage of all hero prompts

**Two Complementary Views**:
1. **This Document - Infrastructure View**: Groups canonical tasks by technical implementation layer (Calendar API, NLP, ML, etc.)
2. **[CANONICAL_TASKS_GOLD_STANDARD_REFERENCE.md](./CANONICAL_TASKS_GOLD_STANDARD_REFERENCE.md) - Functional View**: Each task with hero prompt examples and detailed decompositions

---

## Executive Summary

The **24 Canonical Unit Tasks Framework** provides complete coverage for all 9 Calendar.AI hero prompts, organized into **10 foundational capability clusters** and **52 specific technical capabilities** for implementation.

**Framework Characteristics**:
- **Total Tasks**: 24 (23 unique + CAN-02A/CAN-02B split)
- **Tasks Used**: 23/24 (96% utilization across all prompts)
- **Average Tasks/Prompt**: 7.8 (range: 7-11)
- **Framework Stability**: 93.6% LLM consistency across 3 trials, F1 78.40% ± 0.72%

**Key Insights**:
- **3 Universal Tasks** (100% frequency): CAN-04 (NLU), CAN-01 (Calendar Retrieval), CAN-07 (Metadata Extraction)
- **6 Core Infrastructure Capabilities** enable 90% of framework (Calendar API, NLP, ML, Data Access, Orchestration, Constraint Solving)
- **3 Intelligence Capabilities** differentiate basic vs advanced features (Semantic Analysis, Pattern Recognition, Risk Anticipation)
- **Critical Dependencies**: CAN-07 is parent task for 6 children (CAN-13, CAN-05, CAN-08, CAN-09, CAN-19, CAN-21)
- **Most Common Tasks**: CAN-02A (89%), CAN-02B (78%), CAN-14 (67%), CAN-09 (56%)

**Tier Distribution**:
- **Tier 1 (Universal)**: 6 tasks - Required for nearly all prompts (CAN-01, CAN-02A, CAN-02B, CAN-03, CAN-04, CAN-05)
- **Tier 2 (Common)**: 11 tasks - Needed for majority of use cases (CAN-06 through CAN-14, CAN-21, CAN-22)
- **Tier 3 (Specialized)**: 7 tasks - Advanced/optional capabilities (CAN-15 through CAN-20, CAN-23)

---

## Capability Taxonomy

### Tier 1: Foundation Infrastructure (Required for MVP)

#### 1. **Calendar Data Access & Management**
*Implements: CAN-01, CAN-11, CAN-17*

**Core Capabilities**:
- **C1.1 Calendar Events Retrieval** → **CAN-01**: Query user's calendar events (past, present, future)
  - **Description**: Load calendar events for specified time periods with comprehensive filtering
  - **Capabilities**:
    - Date range filtering (historical, current, future planning horizons)
    - Event metadata extraction (title, time, attendees, location, status, recurrence)
    - Status filtering (pending invitations, tentative, confirmed, declined)
    - Historical data access for pattern analysis
    - Multi-calendar aggregation (user's multiple calendars)
  - **Frequency**: 100% (9/9 prompts) - CRITICAL FOUNDATION
  - **Used By**: All hero prompts require calendar data retrieval
  - **Technical Requirements**:
    - Microsoft Graph Calendar API integration
    - OAuth 2.0 / MSAL authentication with proper scopes
    - Pagination for large event datasets (>100 events)
    - Efficient caching and sync strategies (delta queries)
    - Real-time event change subscriptions (webhooks for live updates)

- **C1.2 Time Block Scheduling** → **CAN-11**: Create calendar events and time blocks
  - **Description**: Schedule new calendar events, focus time blocks, and buffer periods
  - **Capabilities**:
    - Single event creation with full metadata (title, time, attendees, location)
    - Recurring event creation (iCalendar RRULE generation)
    - Meeting invitation sending with RSVP tracking
    - Buffer time block insertion (prep time, travel time, breaks)
    - Focus time scheduling (protected work blocks)
    - Conflict detection before creation
  - **Frequency**: 22% (2/9 prompts) - organizer-2, schedule-2
  - **Dependencies**: Requires CAN-01 (Calendar Retrieval) to check availability
  - **Technical Requirements**:
    - Calendar API write permissions
    - Recurrence rule generation (RFC 5545 compliance)
    - Invitation formatting and delivery
    - Transaction management (atomic creation)
    - Error handling and rollback

- **C1.3 Automatic Rescheduling** → **CAN-17**: Orchestrated workflow for automatic meeting rescheduling
  - **Description**: Detect conflicts/declines and automatically reschedule affected meetings
  - **Capabilities**:
    - Trigger detection (decline notifications, new conflict events)
    - Affected meeting identification
    - Re-run constraint satisfaction logic (CAN-12)
    - New slot finding (CAN-06, CAN-12)
    - Update calendar and notify attendees
  - **Frequency**: 11% (1/9 prompts) - schedule-1
  - **Dependencies**: Requires CAN-12 (Constraint Satisfaction), CAN-06 (Availability), CAN-13 (RSVP Update)
  - **Note**: Complex orchestrated workflow, not a single API call
  - **Technical Requirements**:
    - Event-driven architecture (webhook handlers)
    - Workflow orchestration engine
    - Retry logic and failure handling
    - Notification system (inform affected parties)
    - Audit trail for transparency

**Priority**: CRITICAL - Foundation for 100% of functionality

---

#### 2. **Natural Language Understanding & Intent Extraction**
*Implements: CAN-04, CAN-03*

**Core Capabilities**:
- **C2.1 Natural Language Understanding** → **CAN-04**: Parse user prompts into structured intents and constraints
  - **Description**: Universal first step - extract user intent, constraints, and parameters from natural language
  - **Capabilities**:
    - Temporal expression parsing ("next week", "Thursday afternoon", "in 2 weeks")
    - Entity extraction (people names, meeting types, priorities, locations)
    - Intent classification (schedule, analyze, prioritize, prepare, collaborate)
    - Multi-constraint extraction (duration, participants, preferences, timeframe)
    - Implicit requirement detection (e.g., "buffer time" implies rest periods needed)
  - **Frequency**: 100% (9/9 prompts) - UNIVERSAL FIRST STEP
  - **Used By**: All prompts start with NLU to understand user request
  - **Technical Requirements**:
    - LLM integration (GPT-4, Claude, or equivalent)
    - Prompt engineering framework for consistent parsing
    - Date/time normalization libraries (handle relative dates)
    - Entity recognition (named entity extraction)
    - Output schema validation (structured JSON output)

- **C2.2 Scheduling Constraint Analysis** → **CAN-03**: Formalize and validate scheduling constraints
  - **Description**: Analyze constraints from user prompt and calendar context
  - **Capabilities**:
    - Hard vs soft constraint classification
    - Constraint feasibility assessment (can all constraints be satisfied?)
    - Priority ordering of constraints (which to relax if over-constrained)
    - Temporal constraint modeling (before/after relationships, gaps)
    - Resource constraint analysis (room capacity, equipment needs)
    - Conflict identification (mutually exclusive constraints)
  - **Frequency**: 44% (4/9 prompts) - organizer-3, schedule-1, schedule-3, collaborate-3
  - **Dependencies**: Requires CAN-04 (NLU) for initial constraint extraction
  - **Technical Requirements**:
    - Constraint modeling language/framework
    - Constraint validation logic
    - Feasibility checking algorithms
    - Constraint relaxation strategies
    - Priority weighting system

**Priority**: CRITICAL - Universal requirements for all use cases

---

#### 3. **Meeting Classification & Analysis**
*Implements: CAN-02A, CAN-02B, CAN-05*

**Core Capabilities**:
- **C3.1 Meeting Type Classification** → **CAN-02A**: Categorize meetings by format/structure (OBJECTIVE)
  - **Description**: Classify meetings into 31+ structural types based on format characteristics
  - **Meeting Types**: 1:1, team sync, all-hands, customer meeting, board meeting, workshop, standup, planning, review, demo, training, social, interview, lunch, coffee chat, focus time, etc.
  - **Classification Features**:
    - Attendee count (1:1, small group, large group)
    - Duration patterns (15 min standup, 30 min 1:1, 60 min team sync)
    - Title keywords and patterns
    - Recurrence patterns (daily standup, weekly 1:1, monthly review)
    - Organizer role (manager for 1:1s, exec for all-hands)
  - **Frequency**: 89% (8/9 prompts) - Missing only in collaborate-2
  - **Note**: OBJECTIVE classification based on observable meeting properties, NOT importance/value
  - **Technical Requirements**:
    - Multi-class classification model (GPT-5, Claude, or fine-tuned model)
    - Feature engineering (meeting attributes → ML features)
    - Confidence scoring for predictions
    - Multi-label support (meeting can be multiple types)
    - Training data collection and annotation

- **C3.2 Meeting Importance Assessment** → **CAN-02B**: Assess strategic value and priority (SUBJECTIVE)
  - **Description**: Determine meeting priority level based on strategic value, urgency, and user context
  - **Importance Levels**: Critical, high, important, medium, routine, low
  - **Assessment Factors**:
    - Executive/stakeholder attendance (VP+, C-suite, key customers)
    - Strategic topics (product strategy, budget, hiring, customer escalation)
    - Temporal urgency (deadline proximity, time-sensitive decisions)
    - User role in meeting (presenter vs attendee, decision maker vs observer)
    - Alignment with user's stated priorities
    - Preparation requirements (high-stakes presentations)
  - **Frequency**: 78% (7/9 prompts) - organizer-1, organizer-2, organizer-3, schedule-1, collaborate-1, collaborate-2, collaborate-3
  - **Note**: SUBJECTIVE assessment based on value/priority, distinct from format-based type (CAN-02A)
  - **Dependencies**: Often used alongside CAN-02A for comprehensive meeting understanding
  - **Technical Requirements**:
    - Context-aware importance scoring model
    - User preference learning (personalized importance)
    - Urgency detection (deadline proximity, keywords)
    - Stakeholder significance ranking
    - Dynamic importance (changes based on context)

- **C3.3 Meeting Attendees Analysis** → **CAN-05**: Analyze attendee composition and relationships
  - **Description**: Identify participants, their roles, relationships, and organizational context
  - **Capabilities**:
    - Attendee categorization (internal, external, customer, executive, team member)
    - Role identification (organizer, required, optional, presenter)
    - Organizational hierarchy (manager, direct report, peer, cross-team)
    - Relationship strength (frequent collaborator, rare interaction)
    - Attendee count and distribution analysis
  - **Frequency**: 56% (5/9 prompts) - organizer-1, schedule-1, collaborate-1, collaborate-2, collaborate-3
  - **Dependencies**: Requires CAN-07 (Metadata Extraction) to get attendee lists
  - **Technical Requirements**:
    - Microsoft Graph People API integration
    - Organizational chart access
    - Contact classification (internal vs external domain matching)
    - Relationship graph analysis
    - Privacy-compliant data access

**Priority**: CRITICAL - Core intelligence for meeting understanding

---

#### 4. **Meeting Metadata Extraction**
*Implements: CAN-07 (PARENT TASK)*

**Core Capabilities**:
- **C4.1 Meeting Metadata Extraction** → **CAN-07**: Extract comprehensive meeting details from calendar events
  - **Description**: PARENT/FOUNDATIONAL task that extracts meeting metadata enabling 6 child tasks
  - **Extracted Metadata**:
    - **RSVP Status**: Pending, accepted, tentative, declined (enables CAN-13)
    - **Attendees**: Required, optional, organizer lists (enables CAN-05)
    - **Attachments**: Documents, agendas, prep materials (enables CAN-08)
    - **Meeting Notes**: Previous meeting notes, action items (enables CAN-09)
    - **Logistics**: Location, room, conference link, dial-in (enables CAN-19)
    - **Duration**: Scheduled time, actual time, time zones (enables CAN-21)
    - **Recurrence**: Recurrence pattern, series information
    - **Custom Properties**: Tags, categories, importance flags
  - **Frequency**: 100% (9/9 prompts) - UNIVERSAL PARENT TASK
  - **Used By**: All prompts require metadata extraction
  - **Child Tasks Enabled**: CAN-13 (RSVP Update), CAN-05 (Attendees), CAN-08 (Documents), CAN-09 (Content Generation), CAN-19 (Resources), CAN-21 (Duration Estimation)
  - **Keyword Triggers**: "pending invitations", "RSVP", "attendees", "documents", "prep materials", "meeting details"
  - **Note**: READ operation (extract/retrieve) vs CAN-13 WRITE operation (update RSVP)
  - **Technical Requirements**:
    - Calendar API extended properties access
    - Attachment retrieval and parsing
    - Note/description field parsing
    - Recurrence rule interpretation
    - Structured metadata output (JSON schema)

**Priority**: CRITICAL - Parent task enabling 6 downstream capabilities

---

### Tier 2: Common Capabilities (Majority of Use Cases)

#### 5. **Availability & Constraint Satisfaction**
*Implements: CAN-06, CAN-12, CAN-23*

**Core Capabilities**:
- **C5.1 Availability Checking** → **CAN-06**: Check free/busy status for users and resources
  - **Description**: Find available time slots by checking calendar availability
  - **Capabilities**:
    - Free/busy queries for single or multiple users
    - Time slot identification (available windows)
    - Multi-calendar aggregation (user's calendars + delegates)
    - Resource availability (conference rooms, equipment)
    - Timezone-aware availability calculation
    - Working hours respect (default 9-5 unless customized)
  - **Frequency**: 44% (4/9 prompts) - organizer-2, schedule-1, schedule-2, schedule-3
  - **Dependencies**: Requires CAN-01 (Calendar Retrieval) to load schedules
  - **Technical Requirements**:
    - Graph API free/busy queries (findMeetingTimes endpoint)
    - Intersection algorithms (find common availability)
    - Timezone conversion libraries
    - Working hours configuration access
    - Efficient availability caching

- **C5.2 Constraint Satisfaction** → **CAN-12**: Find time slots satisfying all constraints
  - **Description**: Optimize scheduling to satisfy hard/soft constraints from CAN-03
  - **Capabilities**:
    - Multi-objective optimization (minimize conflicts, maximize preferences)
    - Hard constraint enforcement (must satisfy: duration, attendees, date range)
    - Soft constraint weighting (prefer: time of day, avoid Fridays)
    - Slot ranking algorithms (score each candidate slot)
    - Infeasibility detection (no solution exists)
    - Constraint relaxation strategies (which constraints to drop if over-constrained)
  - **Frequency**: 33% (3/9 prompts) - schedule-1, schedule-2, schedule-3
  - **Dependencies**: Requires CAN-03 (Constraint Analysis), CAN-06 (Availability)
  - **Technical Requirements**:
    - Constraint satisfaction solver (OR-Tools, custom algorithms)
    - Multi-objective optimization framework
    - Heuristic search (when exhaustive search infeasible)
    - Constraint priority weighting system
    - Solution quality metrics

- **C5.3 Conflict Resolution** → **CAN-23**: Handle scheduling conflicts and auto-reschedule
  - **Description**: Detect conflicts and resolve through intelligent rescheduling strategies
  - **Capabilities**:
    - Conflict detection (overlapping meetings, double-bookings)
    - Override eligibility rules (which meetings can be bumped)
    - Cascading rescheduling (move conflicting meeting to new slot)
    - Multi-party coordination (inform affected attendees)
    - Undo/rollback capabilities (restore if resolution fails)
    - Priority-based conflict resolution (keep higher priority meeting)
  - **Frequency**: 22% (2/9 prompts) - schedule-1, schedule-2
  - **Keyword Triggers**: "auto-reschedule", "bump", "prioritize conflicts", "resolve"
  - **Dependencies**: Requires CAN-12 (Constraint Satisfaction) to find alternative slots
  - **Technical Requirements**:
    - Conflict detection algorithms
    - Priority comparison logic
    - Graph algorithms (dependency tracking)
    - Concurrency control (prevent race conditions)
    - Notification system (communicate changes)

**Priority**: HIGH - Critical for scheduling intelligence

---

#### 6. **Content Generation & Documentation**
*Implements: CAN-08, CAN-09, CAN-10, CAN-13, CAN-14*

**Core Capabilities**:
- **C6.1 Meeting Documentation Retrieval** → **CAN-08**: Retrieve related documents, agendas, notes
  - **Description**: Access meeting-related documents and content from various sources
  - **Content Sources**:
    - Calendar event attachments
    - OneDrive/SharePoint linked documents
    - Teams meeting notes and recordings
    - Email attachments and threads
    - Previous meeting notes from recurring series
  - **Frequency**: 44% (4/9 prompts) - organizer-2, collaborate-2, collaborate-3, and implied in organizer-3
  - **Dependencies**: Requires CAN-07 (Metadata Extraction) to identify document references
  - **Technical Requirements**:
    - Microsoft Graph Files API (OneDrive, SharePoint)
    - Teams API for meeting artifacts
    - Email API for attachment retrieval
    - Document format support (PDF, DOCX, PPTX parsing)
    - Search capabilities (find related documents)

- **C6.2 Content Generation** → **CAN-09**: Generate meeting agendas, summaries, prep materials
  - **Description**: Create structured content for meetings using templates and AI
  - **Generated Content**:
    - Meeting agendas (structured, role-based)
    - Prep documents (context, talking points, decisions needed)
    - Briefing materials (executive summaries, dossiers)
    - Follow-up summaries (action items, decisions, next steps)
    - Email drafts (meeting requests, follow-ups)
  - **Frequency**: 56% (5/9 prompts) - organizer-2, organizer-3, collaborate-1, collaborate-2, collaborate-3
  - **Dependencies**: Requires CAN-07 (Metadata Extraction) for meeting context
  - **Technical Requirements**:
    - LLM integration for content generation
    - Template library (agenda templates, brief formats)
    - Context assembly (combine multiple data sources)
    - Output formatting (markdown, HTML, DOCX)
    - Version control (track document updates)

- **C6.3 Meeting Summarization** → **CAN-10**: Aggregate and summarize meeting data
  - **Description**: Create summaries from meeting content, notes, and context
  - **Summarization Types**:
    - Time aggregations (total hours per category, participant, project)
    - Discussion summaries (key topics, decisions, action items)
    - Collaboration summaries (who met with whom, frequency)
    - Context summaries (background for upcoming meetings)
    - Executive summaries (compress many docs → 3 talking points)
  - **Frequency**: 33% (3/9 prompts) - organizer-3, collaborate-1, collaborate-3
  - **Technical Requirements**:
    - Multi-document summarization (LLM-based)
    - Statistical aggregation engine
    - Topic extraction and clustering
    - Temporal analysis (time-based grouping)
    - Audience-aware framing (executive vs detailed)

- **C6.4 RSVP Status Update** → **CAN-13**: Send meeting responses and update attendance status
  - **Description**: Execute accept/decline/tentative actions on calendar invitations
  - **Capabilities**:
    - RSVP response sending (accept, decline, tentative)
    - Response message customization (optional note)
    - Bulk RSVP operations (batch accept/decline)
    - Delegation support (respond on behalf of)
    - Notification handling (inform organizer)
  - **Frequency**: 44% (4/9 prompts) - organizer-1, schedule-1, schedule-2, schedule-3
  - **Note**: WRITE operation (send/update) vs CAN-07 READ operation (extract RSVP status)
  - **Keyword Mapping**: "Respond to invitations" = CAN-13, "Pending invitations" = CAN-07
  - **Dependencies**: Requires CAN-07 (Metadata Extraction) to get current RSVP status
  - **Technical Requirements**:
    - Calendar API write operations
    - Response message formatting
    - Batch operation support
    - Error handling (failed sends)
    - Audit logging

- **C6.5 Meeting Insights & Recommendations** → **CAN-14**: Generate actionable insights and suggestions
  - **Description**: Provide strategic recommendations based on analysis
  - **Insight Types**:
    - Prioritization recommendations ("Accept customer meetings, decline 1:1s this week")
    - Time reclamation opportunities ("Decline recurring X to save 3 hours/week")
    - Schedule optimization ("Consolidate meetings to create focus blocks")
    - Preparation guidance ("Flag 3 high-stakes meetings needing prep")
    - Collaboration insights ("Top 5 collaborators account for 60% of time")
    - Risk alerts ("No prep time before board meeting")
  - **Frequency**: 67% (6/9 prompts) - organizer-1, organizer-2, organizer-3, schedule-2, collaborate-1, collaborate-3
  - **Technical Requirements**:
    - Decision rule engine
    - Recommendation scoring algorithms
    - Impact simulation (quantify benefits)
    - A/B testing framework (measure quality)
    - User feedback collection

**Priority**: HIGH - Differentiates intelligent assistant from simple calendar tool

---

#### 7. **Data Integration & Contextual Intelligence**
*Implements: CAN-21, CAN-22*

**Core Capabilities**:
- **C7.1 Task Duration Estimation** → **CAN-21**: Estimate time required for tasks and preparation
  - **Description**: Predict how much time is needed for meeting preparation or task completion
  - **Estimation Factors**:
    - Meeting type (board meeting needs 2 hours prep, standup needs 5 minutes)
    - Meeting importance (critical meetings need more prep)
    - Documentation volume (10 docs to review vs 1 doc)
    - User role (presenter needs more prep than attendee)
    - Historical patterns (user's past prep time for similar meetings)
  - **Frequency**: 22% (2/9 prompts) - organizer-2, schedule-3 (implied for travel time)
  - **Dependencies**: Requires CAN-07 (Metadata Extraction) for meeting context
  - **Technical Requirements**:
    - Duration prediction model (regression or LLM-based)
    - Historical pattern analysis
    - Meeting complexity scoring
    - User role detection
    - Calibration with actual outcomes

- **C7.2 Work Attribution Discovery** → **CAN-22**: Identify collaboration relationships and work patterns
  - **Description**: Discover who works with whom and on what, for collaboration insights
  - **Discovery Capabilities**:
    - Collaboration graph construction (who meets with whom)
    - Project/topic attribution (identify shared work areas)
    - Frequent collaborator identification (top N people)
    - Team boundary detection (implicit team membership)
    - Work pattern analysis (collaboration frequency, timing)
  - **Frequency**: 33% (3/9 prompts) - collaborate-1, collaborate-2, collaborate-3
  - **Note**: 100% detection in collaborate prompts (all 3/3) - specialized for collaboration analysis
  - **Dependencies**: Requires CAN-05 (Attendees Analysis) for co-occurrence data
  - **Technical Requirements**:
    - Graph analysis algorithms (community detection)
    - Co-occurrence matrix construction
    - Relationship strength scoring
    - Topic modeling (identify shared projects)
    - Visualization generation (collaboration network)

**Priority**: MEDIUM-HIGH - Enables advanced collaboration and productivity features

---

### Tier 3: Specialized Capabilities (Advanced/Optional)

#### 8. **Advanced Coordination & Resource Management**
*Implements: CAN-15, CAN-16, CAN-19*

**Core Capabilities**:
- **C8.1 Time Zone Management** → **CAN-15**: Handle multi-timezone scheduling and conversions
  - **Description**: Convert and optimize meeting times across participant time zones
  - **Capabilities**:
    - Time zone conversion (meeting times for all participants)
    - Optimal meeting window identification (minimize inconvenient times)
    - Timezone-aware availability checking
    - Daylight saving time handling
    - Participant location tracking
  - **Frequency**: 11% (1/9 prompts) - schedule-3
  - **Keyword Trigger**: "across all time zones", "global team", "time zone"
  - **Technical Requirements**:
    - Timezone database (IANA timezone data)
    - Conversion libraries (moment-timezone, pytz)
    - DST transition handling
    - Location-to-timezone mapping
    - Fairness algorithms (rotate meeting times)

- **C8.2 Recurring Patterns Detection** → **CAN-16**: Identify meeting patterns and series information
  - **Description**: Detect recurring meeting patterns for analysis and optimization
  - **Pattern Types**:
    - Explicit recurrence (iCalendar RRULE series)
    - Implicit patterns (weekly 1:1s without formal recurrence)
    - Back-to-back meeting sequences
    - Time block patterns (morning meetings, afternoon focus time)
    - Seasonal patterns (quarterly reviews, annual planning)
  - **Frequency**: 11% (1/9 prompts) - schedule-2
  - **Keyword Trigger**: "back-to-back meetings", "recurring", "patterns"
  - **Technical Requirements**:
    - Recurrence rule parsing (RFC 5545)
    - Time series pattern detection
    - Sequence identification algorithms
    - Statistical pattern recognition
    - Anomaly detection (unusual patterns)

- **C8.3 Meeting Resources Management** → **CAN-19**: Manage conference rooms, equipment, and resources
  - **Description**: Book and manage meeting resources (rooms, equipment, catering)
  - **Resource Types**:
    - Conference rooms (capacity, location, equipment)
    - Equipment (projectors, whiteboards, video conferencing)
    - Catering and supplies
    - Parking and access
  - **Frequency**: 11% (1/9 prompts) - schedule-3 (implied for travel time/location)
  - **Dependencies**: Requires CAN-07 (Metadata Extraction) for resource metadata
  - **Technical Requirements**:
    - Microsoft Graph Places API
    - Room/resource calendar integration
    - Capacity and equipment metadata
    - Location data (building, floor, room)
    - Booking and release operations

**Priority**: MEDIUM - Nice-to-have for enterprise coordination

---

#### 9. **Advanced Analytics & Intelligence**
*Implements: CAN-18, CAN-20*

**Core Capabilities**:
- **C9.1 Objection/Risk Anticipation** → **CAN-18**: Anticipate objections and prepare mitigation strategies
  - **Description**: Critical thinking about proposals to identify potential objections and risks
  - **Capabilities**:
    - Stakeholder perspective modeling (what concerns will VP have?)
    - Risk identification from context (project delays, budget constraints)
    - Objection anticipation (pushback on proposals)
    - Mitigation strategy generation (counter-arguments, evidence)
    - Persuasive communication preparation
  - **Frequency**: 11% (1/9 prompts) - collaborate-3 (executive prep)
  - **Keyword Triggers**: "anticipate", "risks", "objections", "blockers", "prepare for pushback"
  - **Technical Requirements**:
    - Reasoning-capable LLM (GPT-4, Claude Sonnet)
    - Chain-of-thought prompting
    - Stakeholder analysis framework
    - Risk assessment models
    - Argumentation strategy generation

- **C9.2 Data Visualization** → **CAN-20**: Create visual representations of data and patterns
  - **Description**: Generate charts, graphs, and visual dashboards from meeting data
  - **Visualization Types**:
    - Time distribution charts (pie chart: 30% in 1:1s, 20% in customer meetings)
    - Collaboration networks (graph: who works with whom)
    - Timeline views (meeting history, upcoming schedule)
    - Pattern dashboards (meeting density heatmaps)
    - Trend analysis (meeting volume over time)
  - **Frequency**: 22% (2/9 prompts) - organizer-3, collaborate-1
  - **Keyword Triggers**: "show", "visualize", "dashboard", "patterns", "trends", "display"
  - **Technical Requirements**:
    - Charting libraries (Chart.js, D3.js, Plotly)
    - Graph visualization (network diagrams)
    - Data aggregation for visualization
    - Interactive dashboard frameworks
    - Export formats (PNG, SVG, PDF)

**Priority**: MEDIUM - High-value features for advanced users

---

## Implementation Roadmap

### Phase 1: MVP Foundation (Months 1-3)
**Objective**: Build core infrastructure for basic scheduling and intelligence

**Capabilities to Build**:
1. **Calendar Data Access** (C1.1): CAN-01 Calendar Retrieval - CRITICAL
2. **Natural Language Understanding** (C2.1, C2.2): CAN-04 NLU, CAN-03 Constraints - CRITICAL
3. **Meeting Classification** (C3.1, C3.2, C3.3): CAN-02A Type, CAN-02B Importance, CAN-05 Attendees - CRITICAL
4. **Metadata Extraction** (C4.1): CAN-07 - CRITICAL PARENT TASK
5. **Basic Content Generation** (C6.2, C6.4): CAN-09 Content, CAN-13 RSVP - HIGH
6. **Simple Recommendations** (C6.5): CAN-14 Insights - HIGH

**Prompts Supported**: organizer-1 (priority invitations), partial organizer-2 (meeting prep)

**Success Criteria**: 
- Handle 3/9 hero prompts end-to-end
- F1 > 75% on gold standard evaluation
- < 2 second response time for basic queries

---

### Phase 2: Scheduling Intelligence (Months 4-6)
**Objective**: Add advanced scheduling, constraint satisfaction, and time management

**Capabilities to Build**:
7. **Availability & Constraints** (C5.1, C5.2): CAN-06 Availability, CAN-12 Constraint Satisfaction - HIGH
8. **Time Block Scheduling** (C1.2): CAN-11 - HIGH
9. **Documentation Access** (C6.1): CAN-08 Documents - MEDIUM-HIGH
10. **Summarization** (C6.3): CAN-10 - MEDIUM-HIGH
11. **Duration Estimation** (C7.1): CAN-21 - MEDIUM

**Prompts Supported**: organizer-2 (complete), organizer-3, schedule-1, schedule-2

**Success Criteria**:
- Handle 7/9 hero prompts end-to-end
- Multi-meeting scheduling success rate > 90%
- Constraint satisfaction accuracy > 85%

---

### Phase 3: Collaboration & Advanced Features (Months 7-9)
**Objective**: Enable collaboration insights, risk analysis, and specialized capabilities

**Capabilities to Build**:
12. **Work Attribution** (C7.2): CAN-22 - MEDIUM-HIGH
13. **Conflict Resolution** (C5.3): CAN-23 - MEDIUM
14. **Visualization** (C9.2): CAN-20 - MEDIUM
15. **Risk Anticipation** (C9.1): CAN-18 - MEDIUM
16. **Advanced Coordination** (C8.1, C8.2, C8.3): CAN-15 Timezone, CAN-16 Patterns, CAN-19 Resources - MEDIUM

**Prompts Supported**: All 9/9 hero prompts including collaborate-1, collaborate-2, collaborate-3, schedule-3

**Success Criteria**:
- Complete framework coverage (all 24 canonical tasks)
- Handle all 9 hero prompts at production quality
- F1 > 85% on gold standard evaluation

---

### Phase 4: Orchestration & Automation (Months 10-12)
**Objective**: Add complex workflows and automation

**Capabilities to Build**:
17. **Automatic Rescheduling** (C1.3): CAN-17 - COMPLEX WORKFLOW
18. **Event-Driven Automation** (C4.1-C4.4): Action execution framework
19. **Workflow Orchestration**: Multi-step task coordination
20. **Real-time Monitoring**: Webhooks, change subscriptions

**Prompts Enhanced**: All prompts gain automation capabilities

**Success Criteria**:
- Automatic rescheduling success rate > 80%
- < 5 second end-to-end latency for complex workflows
- Zero data loss/corruption in automated operations

---

## Task Frequency & Priority Matrix

### Universal Tasks (100% Frequency)
| Task ID | Task Name | Frequency | Priority | Implementation Phase |
|---------|-----------|-----------|----------|---------------------|
| CAN-04 | Natural Language Understanding | 9/9 (100%) | CRITICAL | Phase 1 (Month 1) |
| CAN-01 | Calendar Events Retrieval | 9/9 (100%) | CRITICAL | Phase 1 (Month 1) |
| CAN-07 | Meeting Metadata Extraction | 9/9 (100%) | CRITICAL | Phase 1 (Month 1) |

### High-Frequency Common Tasks (50%+ Usage)
| Task ID | Task Name | Frequency | Priority | Implementation Phase |
|---------|-----------|-----------|----------|---------------------|
| CAN-02A | Meeting Type Classification | 8/9 (89%) | CRITICAL | Phase 1 (Month 2) |
| CAN-02B | Meeting Importance Assessment | 7/9 (78%) | CRITICAL | Phase 1 (Month 2) |
| CAN-14 | Meeting Insights & Recommendations | 6/9 (67%) | HIGH | Phase 1 (Month 3) |
| CAN-09 | Content Generation | 5/9 (56%) | HIGH | Phase 1 (Month 3) |
| CAN-05 | Meeting Attendees Analysis | 5/9 (56%) | HIGH | Phase 1 (Month 2) |

### Medium-Frequency Common Tasks (30-50% Usage)
| Task ID | Task Name | Frequency | Priority | Implementation Phase |
|---------|-----------|-----------|----------|---------------------|
| CAN-03 | Scheduling Constraint Analysis | 4/9 (44%) | HIGH | Phase 2 (Month 4) |
| CAN-06 | Availability Checking | 4/9 (44%) | HIGH | Phase 2 (Month 4) |
| CAN-08 | Meeting Documentation Retrieval | 4/9 (44%) | MEDIUM-HIGH | Phase 2 (Month 5) |
| CAN-13 | RSVP Status Update | 4/9 (44%) | HIGH | Phase 1 (Month 3) |
| CAN-10 | Meeting Summarization | 3/9 (33%) | MEDIUM-HIGH | Phase 2 (Month 5) |
| CAN-12 | Constraint Satisfaction | 3/9 (33%) | HIGH | Phase 2 (Month 4) |
| CAN-22 | Work Attribution Discovery | 3/9 (33%) | MEDIUM-HIGH | Phase 3 (Month 7) |

### Low-Frequency Common/Specialized Tasks (<30% Usage)
| Task ID | Task Name | Frequency | Priority | Implementation Phase |
|---------|-----------|-----------|----------|---------------------|
| CAN-11 | Time Block Scheduling | 2/9 (22%) | HIGH | Phase 2 (Month 5) |
| CAN-20 | Data Visualization | 2/9 (22%) | MEDIUM | Phase 3 (Month 8) |
| CAN-21 | Task Duration Estimation | 2/9 (22%) | MEDIUM | Phase 2 (Month 6) |
| CAN-23 | Conflict Resolution | 2/9 (22%) | MEDIUM | Phase 3 (Month 7) |
| CAN-15 | Time Zone Management | 1/9 (11%) | MEDIUM | Phase 3 (Month 9) |
| CAN-16 | Recurring Patterns Detection | 1/9 (11%) | MEDIUM | Phase 3 (Month 9) |
| CAN-17 | Automatic Rescheduling | 1/9 (11%) | MEDIUM | Phase 4 (Month 10) |
| CAN-18 | Objection/Risk Anticipation | 1/9 (11%) | MEDIUM | Phase 3 (Month 8) |
| CAN-19 | Meeting Resources Management | 1/9 (11%) | MEDIUM | Phase 3 (Month 9) |

### Unused Tasks (0% in Current Prompts)
| Task ID | Task Name | Frequency | Status | Notes |
|---------|-----------|-----------|--------|-------|
| CAN-24 | (Not defined) | 0/9 (0%) | RESERVED | Framework allows 24 tasks, 23 currently defined |

---

## Dependency Graph

### Parent-Child Relationships

**CAN-07 (Meeting Metadata Extraction)** → Enables 6 child tasks:
- CAN-13 (RSVP Status Update) - needs RSVP status from metadata
- CAN-05 (Meeting Attendees Analysis) - needs attendee lists from metadata
- CAN-08 (Meeting Documentation Retrieval) - needs attachment references from metadata
- CAN-09 (Content Generation) - needs meeting context from metadata
- CAN-19 (Meeting Resources Management) - needs resource/location info from metadata
- CAN-21 (Task Duration Estimation) - needs meeting details from metadata

### Sequential Dependencies

**CAN-04 (NLU)** → **CAN-03 (Constraints)** → **CAN-12 (Constraint Satisfaction)**
- Natural language → Structured constraints → Optimization

**CAN-01 (Calendar Retrieval)** → **CAN-06 (Availability Checking)**
- Need calendar data before checking availability

**CAN-12 (Constraint Satisfaction)** → **CAN-23 (Conflict Resolution)**
- Handle unsatisfiable constraints through conflict resolution

**CAN-07 (Metadata Extraction)** → **CAN-05 (Attendees)** → **CAN-22 (Work Attribution)**
- Metadata → Attendee lists → Collaboration patterns

---

## Technical Architecture Recommendations

### 1. **API Layer**
- **Calendar API**: Microsoft Graph Calendar (primary)
- **People API**: Microsoft Graph People, Azure AD
- **Files API**: Microsoft Graph Files, OneDrive, SharePoint
- **Communication API**: Microsoft Graph Mail, Teams Messages
- **Authentication**: OAuth 2.0, MSAL library

### 2. **Intelligence Layer**
- **LLM Integration**: GPT-4 Turbo or Claude Sonnet 4.5 for NLU, content generation, reasoning
- **Embedding Models**: text-embedding-ada-002 for semantic similarity
- **Classification Models**: Fine-tuned GPT-5 or custom models for meeting type/importance
- **Prompt Engineering**: Version-controlled prompt templates with validation

### 3. **Data Layer**
- **Caching**: Redis for calendar data, API responses
- **Search**: Azure Cognitive Search or Elasticsearch for document retrieval
- **Graph Database**: Neo4j for collaboration relationships (CAN-22)
- **Vector Store**: Pinecone or FAISS for semantic search
- **Time Series**: InfluxDB for pattern analysis

### 4. **Orchestration Layer**
- **Workflow Engine**: Azure Durable Functions or custom orchestrator
- **Event Processing**: Azure Event Grid for webhooks
- **Queue**: Azure Service Bus for async operations
- **Scheduling**: Temporal or custom scheduler for recurring tasks

### 5. **Monitoring & Observability**
- **Logging**: Application Insights for telemetry
- **Metrics**: Task success rates, latency, accuracy
- **Alerting**: Anomaly detection, error thresholds
- **A/B Testing**: Experimentation framework for recommendations

---

## Success Metrics

### Framework Validation
- **Gold Standard Alignment**: F1 > 85% on all 9 hero prompts
- **LLM Consistency**: < 2% variance across multiple trials
- **Task Coverage**: All 24 canonical tasks exercised in production

### Performance Metrics
- **Latency**: 
  - Simple queries (organizer-1): < 2 seconds
  - Complex workflows (schedule-1): < 10 seconds
  - Batch operations: < 30 seconds
- **Accuracy**:
  - Meeting classification: > 90% accuracy
  - Constraint satisfaction: > 85% success rate
  - Recommendation acceptance: > 70% user adoption

### User Experience
- **Task Completion**: > 95% success rate for supported prompts
- **User Satisfaction**: NPS > 50
- **Error Rate**: < 1% critical errors
- **Automation Value**: Average 5+ hours reclaimed per user per week

---

## Appendix: Gold Standard Validation

This framework has been validated through:

1. **Human Expert Review**: Chin-Yew Lin manually corrected GPT-5 outputs
2. **LLM Validation**: GPT-5 analyzed all 9 prompts with 93.6% consistency across 3 trials
3. **Statistical Rigor**: F1 78.40% ± 0.72% (< 1% variance, EXCELLENT stability)
4. **Coverage**: All 24 canonical tasks represented, 100% Tier 1 coverage
5. **Cross-Reference**: Validated against original GUTT decompositions (66→39→24 tasks)

See [CANONICAL_TASKS_GOLD_STANDARD_REFERENCE.md](./CANONICAL_TASKS_GOLD_STANDARD_REFERENCE.md) for complete gold standard documentation.

---

## Document Metadata

**Version**: 1.0  
**Created**: November 7, 2025  
**Author**: Chin-Yew Lin  
**Framework**: Calendar.AI Canonical Unit Tasks v2.0  
**Total Tasks**: 24 (23 unique + CAN-02A/CAN-02B split)  
**Validation Status**: ✅ Gold Standard (Human-Corrected, LLM-Validated)

**Maintenance**:
- Update when new hero prompts added
- Refine when canonical tasks framework evolves
- Adjust priorities based on production learnings
- Incorporate user feedback and usage analytics

---

*End of Document*
