# Enterprise Meeting Intelligence - Canonical Tasks Capability Inventory V2.0

**Date**: November 7, 2025 (Canonical Unit Tasks Framework V2.0)  
**Author**: Chin-Yew Lin  
**Source**: Human-validated gold standard analysis of 9 Calendar.AI v2 Hero Prompts  
**Framework**: 25 Canonical Unit Tasks (renumbered CAN-01 through CAN-25)  
**Purpose**: Define atomic capabilities required for production implementation

**Related Documents**:
- [CANONICAL_TASKS_GOLD_STANDARD_REFERENCE_V2.md](./CANONICAL_TASKS_GOLD_STANDARD_REFERENCE_V2.md) - Complete gold standard with all 9 v2 hero prompt analyses
- [GPT5_V2_OPTIMIZATION_SUMMARY.md](./model_comparison/GPT5_V2_OPTIMIZATION_SUMMARY.md) - 3-trial stability test and optimization results
- [CANONICAL_TASKS_REFERENCE_V2.md](./CANONICAL_TASKS_REFERENCE_V2.md) - Complete specifications for all 25 canonical tasks

---

## Journey to V2.0 Framework

This document represents the culmination of a rigorous **4-phase methodology** to establish a validated, production-ready framework for Calendar.AI capabilities:

### Phase 1: Original Framework Development (October-November 2025)
**Objective**: Establish foundational canonical tasks framework

- **Initial Analysis**: 24 canonical tasks identified through expert decomposition of hero prompts
- **Consolidation**: Reduced 66 GUTTs → 39 C-GUTTs → 24 canonical tasks (41% reduction)
- **Framework V1.0**: 24 tasks with CAN-02A/CAN-02B split for type vs importance
- **Key Achievement**: Atomic task definition, clear parent-child relationships, tier classification

**Limitations Identified**:
- Missing specialized capabilities (e.g., event flagging/annotation)
- CAN-02A/CAN-02B numbering created gap (confusing sequential ordering)
- No validation against LLM capabilities at scale
- Unclear which tasks require special prompt engineering

### Phase 2: GPT-5 Baseline Analysis (November 7, 2025)
**Objective**: Validate v2 prompts with automated LLM analysis

- **New Prompts**: 9 hero prompts v2 (functionally identical to v1, minor typo fixes)
- **Automated Analysis**: GPT-5 analyzed all 9 v2 prompts using optimized system prompts
- **Performance Baseline**: Initial decomposition established
- **Critical Gaps Discovered**:
  - **CAN-05 (Attendee Resolution)**: Frequently missed despite being critical dependency
  - **CAN-18 (Risk Anticipation)**: Over-interpretation issues (meeting goals vs risks)
  - **Missing Task**: Event flagging/annotation capability not yet in framework
  - **CAN-16 (Event Monitoring)**: "Track" use case not clearly mapped

**Key Insight**: Framework needed one more task (CAN-25) for conditional event annotation, and sequential renumbering for clarity.

### Phase 3: 3-Trial Stability Test (November 7, 2025)
**Objective**: Validate framework stability and LLM consistency

**Test Design**:
- **27 API Calls**: 3 independent trials × 9 v2 hero prompts (100% success rate)
- **Statistical Rigor**: Multiple runs to measure variance and consistency
- **Optimized Prompts**: Used enhanced system prompts from Phase 2 learnings

**Results**:
- **Average Performance**: F1 78.40% ± 0.72% (EXCELLENT < 1% variance)
- **Consistency**: 93.6% task selection agreement across trials
- **Framework Stability**: < 1% variance proves reliable task decomposition
- **Frequency Distribution**: Stable across all 3 trials

**Statistical Validation**: Framework demonstrates production-grade reliability with minimal variance.

### Phase 4: Human Evaluation & Gold Standard Creation (November 7, 2025)
**Objective**: Create authoritative V2.0 reference through expert review

**Human Evaluation Process**:
- **Expert Review**: Human evaluator (Chin-Yew Lin) reviewed all GPT-5 Trial 1 outputs
- **Systematic Corrections Applied**:
  - ✅ **Added CAN-25**: New task for event annotation/flagging (Organizer-2: "flag meetings")
  - ✅ **Added Missing CAN-05**: Attendee resolution critical for Schedule-2, Collaborate-2
  - ✅ **Removed CAN-18**: From Collaborate-1 (over-interpretation of "meeting goals")
  - ✅ **Added CAN-16**: Event monitoring for "track" requirement (Organizer-2)
  - ✅ **Ensured CAN-04**: 100% coverage (NLU required for all prompts)
- **Framework Renumbering**: CAN-02A/CAN-02B → CAN-02/CAN-03, new CAN-25 added
- **Validation Results**: 5 correct, 3 partial, 1 needs review (out of 9 prompts)

**V2.0 Framework Finalized**:
- **Total Tasks**: 25 (CAN-01 through CAN-25, sequential numbering)
- **NEW Task**: CAN-25 (Event Annotation/Flagging) - validated through human evaluation
- **Tasks Used**: 22/25 (88% framework coverage across all v2 prompts)
- **Average**: 7.2 tasks per prompt (range: 3-10)
- **Tier Distribution**: 
  - Tier 1 (Universal): 6 tasks (100% coverage)
  - Tier 2 (Common): 9 tasks (89% coverage)
  - Tier 3 (Specialized): 10 tasks (80% coverage)

**Gold Standard Statistics**:
- **Coverage**: 100% Tier 1, 89% Tier 2, 80% Tier 3
- **Frequency Leaders**: CAN-04 (100%), CAN-01 (100%), CAN-07 (78%)
- **Critical Dependencies**: CAN-05 often missed but essential
- **Validation**: Human-corrected, LLM-validated, statistically rigorous

---

## Document Purpose

This document presents the **infrastructure-centric view** of capabilities needed to implement the **25 Canonical Unit Tasks** that serve all 9 Calendar.AI v2 hero prompts.

**What are Canonical Unit Tasks V2.0?**
- **Atomic capabilities**: Each task is a single, well-defined functional unit
- **Framework-validated**: Validated through 4-phase human-in-the-loop + LLM methodology
- **Production-ready**: Gold standard reference with statistical validation (93.6% consistency, F1 78.40% ± 0.72%)
- **Implementation focus**: These 25 tasks are what must be built - proven coverage of all v2 hero prompts
- **Sequential numbering**: Clean 1-25 ordering (no gaps, CAN-02A/CAN-02B now CAN-02/CAN-03)

**Two Complementary Views**:
1. **This Document - Infrastructure View**: Groups 25 canonical tasks by technical implementation layer (Calendar API, NLP, ML, etc.)
2. **[CANONICAL_TASKS_GOLD_STANDARD_REFERENCE_V2.md](./CANONICAL_TASKS_GOLD_STANDARD_REFERENCE_V2.md) - Functional View**: Each task with v2 hero prompt examples and detailed decompositions

**Key Changes in V2.0**:
- ✅ **25 Tasks Total**: Added CAN-25 (Event Annotation/Flagging)
- ✅ **Renumbered**: CAN-02A/CAN-02B → CAN-02/CAN-03 (sequential 1-25)
- ✅ **Human-Validated**: All 9 v2 prompts reviewed by expert
- ✅ **Statistical Rigor**: 3-trial stability test, < 1% variance
- ✅ **Updated Tiers**: Redistributed based on actual v2 usage patterns

---

## Executive Summary

The **25 Canonical Unit Tasks Framework V2.0** provides complete coverage for all 9 Calendar.AI v2 hero prompts, organized into **10 foundational capability clusters** and **52+ specific technical capabilities** for implementation.

**Framework Characteristics**:
- **Total Tasks**: 25 (CAN-01 through CAN-25, sequential numbering)
- **Tasks Used**: 22/25 (88% utilization across all v2 prompts)
- **Average Tasks/Prompt**: 7.2 (range: 3-10)
- **Framework Stability**: 93.6% LLM consistency across 3 trials, F1 78.40% ± 0.72%
- **NEW in V2.0**: CAN-25 (Event Annotation/Flagging) for conditional event marking

**Key Insights**:
- **2 Universal Tasks** (100% frequency): CAN-04 (NLU), CAN-01 (Calendar Retrieval)
- **High-Frequency Tasks** (78%): CAN-07 (Metadata Extraction) - critical parent task
- **6 Core Infrastructure Capabilities** enable 90% of framework (Calendar API, NLP, ML, Data Access, Orchestration, Constraint Solving)
- **3 Intelligence Capabilities** differentiate basic vs advanced features (Semantic Analysis, Pattern Recognition, Risk Anticipation)
- **Critical Dependencies**: 
  - CAN-05 (Attendee Resolution) - often missed but essential for Schedule-2, Collaborate-2
  - CAN-07 (Metadata Extraction) - parent task, enables multiple children
- **Most Common Tasks**: CAN-02 (Type, 56%), CAN-03 (Importance, 56%), CAN-09 (Document Gen, 56%)

**Tier Distribution**:
- **Tier 1 (Universal)**: 6 tasks - Required for 50%+ prompts (CAN-01 through CAN-06)
- **Tier 2 (Common)**: 9 tasks - Needed for 25-50% prompts (CAN-06 through CAN-14)
- **Tier 3 (Specialized)**: 10 tasks - Advanced/optional capabilities (CAN-15 through CAN-25)

**V2.0 Improvements**:
- **Clearer Numbering**: Sequential 1-25 (no gaps from CAN-02A/CAN-02B split)
- **Complete Coverage**: CAN-25 fills event annotation gap
- **Human-Validated**: Expert corrections ensure accuracy
- **Statistical Confidence**: < 1% variance across 3 independent trials

---

## Capability Taxonomy

### Tier 1: Foundation Infrastructure (Required for MVP)

#### 1. **Calendar Data Access & Management**
*Implements: CAN-01, CAN-13, CAN-17*

**Core Capabilities**:
- **C1.1 Calendar Events Retrieval** → **CAN-01**: Query user's calendar events (past, present, future)
  - **Description**: Load calendar events for specified time periods with comprehensive filtering
  - **Capabilities**:
    - Date range filtering (historical, current, future planning horizons)
    - Event metadata extraction (title, time, attendees, location, status, recurrence)
    - Status filtering (pending invitations, tentative, confirmed, declined)
    - Historical data access for pattern analysis
    - Multi-calendar aggregation (user's multiple calendars)
  - **Frequency**: 100% (9/9 v2 prompts) - CRITICAL FOUNDATION
  - **Used By**: All v2 hero prompts require calendar data retrieval
  - **Technical Requirements**:
    - Microsoft Graph Calendar API integration (`GET /me/calendar/events`)
    - OAuth 2.0 / MSAL authentication with proper scopes (`Calendars.Read`, `Calendars.ReadWrite`)
    - Pagination for large event datasets (>100 events)
    - Efficient caching and sync strategies (delta queries)
    - Real-time event change subscriptions (webhooks for live updates)

- **C1.2 RSVP Status Update** → **CAN-13**: Update meeting response status (accept/decline/tentative)
  - **Description**: Modify user's RSVP status for meeting invitations
  - **Capabilities**:
    - Accept meeting invitations
    - Decline meeting invitations (with optional message)
    - Set tentative status (maybe attending)
    - Batch RSVP updates (multiple invitations at once)
    - Add response comments/notes
  - **Frequency**: 44% (4/9 v2 prompts) - organizer-1, schedule-1, schedule-2, collaborate-2
  - **Dependencies**: Requires CAN-07 (Metadata Extraction) to identify invitations
  - **Technical Requirements**:
    - Calendar API write permissions (`Calendars.ReadWrite`)
    - Event response API (`POST /events/{id}/accept`, `/decline`, `/tentativelyAccept`)
    - Response message formatting
    - Error handling for already-responded events
    - Notification suppression controls

- **C1.3 Automatic Rescheduling** → **CAN-17**: Orchestrated workflow for automatic meeting rescheduling
  - **Description**: Detect conflicts/declines and automatically reschedule affected meetings
  - **Capabilities**:
    - Trigger detection (decline notifications, new conflict events)
    - Affected meeting identification
    - Re-run constraint satisfaction logic (CAN-12)
    - New slot finding (CAN-06, CAN-12)
    - Update calendar and notify attendees
  - **Frequency**: 11% (1/9 v2 prompts) - schedule-1
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
- **C2.1 Natural Language Understanding (NLU)** → **CAN-04**: Parse user's natural language query into structured intent
  - **Description**: Convert free-form text prompts into actionable parameters and intent classification
  - **Capabilities**:
    - Intent classification (schedule, find, analyze, summarize, optimize, etc.)
    - Entity extraction (people names, dates, meeting types, priorities, constraints)
    - Temporal expression parsing ("next week", "Thursday afternoon", "Q4")
    - Constraint extraction (time preferences, attendee requirements, location needs)
    - Ambiguity resolution (clarifying questions when needed)
    - Multi-turn conversation context tracking
  - **Frequency**: 100% (9/9 v2 prompts) - CRITICAL FOUNDATION
  - **Used By**: Every v2 hero prompt requires NLU to understand user request
  - **Technical Requirements**:
    - LLM integration (GPT-4, Claude, local models)
    - Named Entity Recognition (NER) for people, dates, locations
    - Intent classification model (fine-tuned on Calendar.AI domain)
    - Temporal expression parser (datetime normalization)
    - Coreference resolution for pronouns/references
    - Conversation state management

- **C2.2 Meeting Importance Assessment** → **CAN-03**: Evaluate business importance/priority of meetings
  - **Description**: Assess strategic value, urgency, and priority level based on context
  - **Capabilities**:
    - Attendee seniority scoring (VP+, director-level, senior leadership)
    - Business impact evaluation (customer-facing, revenue-driving, strategic planning)
    - Strategic alignment assessment (company OKRs, team goals, project milestones)
    - Urgency calculation (deadline proximity, blocker status)
    - Importance scoring (High/Medium/Low with confidence)
    - User preference learning (what matters to this specific user)
  - **Frequency**: 56% (5/9 v2 prompts) - organizer-1, organizer-2, organizre-3, schedule-3, collaborate-2
  - **Dependencies**: Often requires CAN-05 (Attendee Resolution) to identify seniority
  - **Note**: Subjective assessment - differs from CAN-02 (objective type classification)
  - **Technical Requirements**:
    - Organizational hierarchy data (reporting structure, job titles)
    - Business context data (active projects, OKRs, priorities)
    - ML importance scoring model (trained on historical user decisions)
    - User preference storage (accepted vs declined patterns)
    - Confidence scoring for recommendations

**Priority**: CRITICAL - Foundation for intelligent behavior

---

#### 3. **Meeting Classification & Analysis**
*Implements: CAN-02, CAN-07*

**Core Capabilities**:
- **C3.1 Meeting Type Classification** → **CAN-02**: Classify meetings by format/structure
  - **Description**: Categorize meetings into objective types based on structural attributes
  - **Capabilities**:
    - Format classification (1:1, team sync, all-hands, customer meeting, executive review)
    - Domain classification (internal, external customer, vendor, partner)
    - Pattern recognition (recurring vs one-time, scheduled vs ad-hoc)
    - Subject keyword analysis (project names, meeting type indicators)
    - Attendee count-based classification (2-person vs team vs all-hands)
    - 31+ meeting type taxonomy support
  - **Frequency**: 56% (5/9 v2 prompts) - organizer-1, organizer-2, organizre-3, schedule-3, collaborate-1
  - **Note**: Objective classification based on structure - differs from CAN-03 (subjective importance)
  - **Technical Requirements**:
    - ML classification model (multi-class, 31+ types)
    - Training data: labeled historical meetings
    - Keyword dictionaries (meeting type indicators)
    - Attendee domain parsing (email domains)
    - Feature engineering (count, duration, recurrence, keywords)
    - Confidence thresholds and fallback logic

- **C3.2 Meeting Metadata Extraction** → **CAN-07**: Extract comprehensive meeting details
  - **Description**: Parse and structure detailed meeting information from calendar events
  - **Capabilities**:
    - Attendee list extraction (required, optional, organizer)
    - Subject/title parsing
    - Date/time extraction (start, end, duration, timezone)
    - Location parsing (physical room, Teams link, Zoom URL)
    - RSVP status tracking (per attendee)
    - Recurrence pattern extraction (daily, weekly, custom RRULE)
    - Agenda/body content parsing
    - Attachment/document references
  - **Frequency**: 78% (7/9 v2 prompts) - High-frequency parent task
  - **Used By**: organizer-1, organizer-2, organizre-3, schedule-2, collaborate-1, collaborate-2, collaborate-3
  - **Parent Task**: Enables CAN-05, CAN-08, CAN-09, CAN-13, CAN-19, CAN-21
  - **Technical Requirements**:
    - Calendar event object parsing (Microsoft Graph, Google Calendar schemas)
    - Email address parsing and validation
    - URL extraction (meeting links)
    - Recurrence rule parsing (RFC 5545 RRULE)
    - HTML content parsing (agenda in event body)
    - Attachment metadata extraction

**Priority**: CRITICAL - Core classification and data extraction

---

#### 4. **Contact & People Data**
*Implements: CAN-05*

**Core Capabilities**:
- **C4.1 Attendee/Contact Resolution** → **CAN-05**: Resolve people identities and organizational context
  - **Description**: Match email addresses to full contact profiles with organizational data
  - **Capabilities**:
    - Email-to-contact resolution (user profile lookup)
    - Job title and role extraction
    - Reporting hierarchy resolution (manager, skip-level, org chart)
    - Seniority level determination (individual contributor, manager, director, VP, C-level)
    - Team/department affiliation
    - External contact classification (customer, partner, vendor)
    - Contact photo and presence data (optional)
  - **Frequency**: 67% (6/9 v2 prompts)
  - **Used By**: organizer-1, organizre-3, schedule-2, schedule-3, collaborate-1, collaborate-2
  - **Critical Dependency**: Often missed by LLMs but ESSENTIAL for importance assessment, senior leadership identification
  - **Human Evaluator Insight**: "Model needs to get metadata, and from there find attendee for those meetings" (Schedule-2)
  - **Technical Requirements**:
    - Microsoft Graph People API (`GET /me/people`, `/users/{id}`)
    - Azure AD user profile access
    - Organizational hierarchy data (manager chains)
    - External contact enrichment (CRM integration)
    - Contact caching for performance
    - Privacy controls for sensitive data

**Priority**: CRITICAL - Required for importance assessment and senior leadership queries

---

#### 5. **Time & Availability Management**
*Implements: CAN-06, CAN-10*

**Core Capabilities**:
- **C5.1 Availability Checking (Free/Busy)** → **CAN-06**: Check calendar availability for scheduling
  - **Description**: Query free/busy time slots across single or multiple calendars
  - **Capabilities**:
    - Single-user availability lookup
    - Multi-user availability aggregation (find common free slots)
    - Time zone handling (cross-timezone scheduling)
    - Working hours awareness (respect user preferences)
    - Buffer time consideration (travel, prep time)
    - Recurring event detection (avoid recurring conflicts)
  - **Frequency**: 33% (3/9 v2 prompts) - schedule-1, schedule-2, schedule-3
  - **Dependencies**: Requires CAN-01 (Calendar Retrieval)
  - **Technical Requirements**:
    - Calendar API free/busy query (`POST /me/calendar/getSchedule`)
    - Multi-user availability aggregation
    - Time zone conversion library
    - Working hours configuration storage
    - Conflict detection algorithms
    - Duration-aware slot finding

- **C5.2 Time Aggregation/Statistical Analysis** → **CAN-10**: Analyze time spent patterns
  - **Description**: Calculate time statistics and spending patterns across meetings
  - **Capabilities**:
    - Total hours calculation (by time period)
    - Meeting type breakdown (hours per meeting type)
    - Attendee-based aggregation (time with specific people)
    - Trend analysis (week-over-week, month-over-month)
    - Percentage calculations (% of time in customer meetings)
    - Historical pattern recognition
  - **Frequency**: 11% (1/9 v2 prompts) - organizre-3
  - **Dependencies**: Requires CAN-01 (Calendar Retrieval), CAN-02 (Type Classification)
  - **Technical Requirements**:
    - Time series data processing
    - Aggregation queries (SQL/NoSQL)
    - Statistical computation (mean, median, percentiles)
    - Trend detection algorithms
    - Data visualization preparation
    - Performance optimization for large datasets

**Priority**: HIGH - Core scheduling and analytics capabilities

---

### Tier 2: Common Capabilities (Needed for Most Use Cases)

#### 6. **Document & Content Management**
*Implements: CAN-08, CAN-09*

**Core Capabilities**:
- **C6.1 Document/Content Retrieval** → **CAN-08**: Retrieve meeting-related documents and content
  - **Description**: Access and fetch content associated with calendar events
  - **Capabilities**:
    - Meeting attachments retrieval (files attached to invites)
    - OneDrive/SharePoint document lookup (linked in event body)
    - Teams chat history for recurring meetings
    - Email thread retrieval (related to meeting)
    - Previous meeting notes/minutes
    - Agenda documents and slides
  - **Frequency**: 33% (3/9 v2 prompts) - collaborate-1, collaborate-2, collaborate-3
  - **Dependencies**: Child of CAN-07 (Metadata Extraction)
  - **Technical Requirements**:
    - Microsoft Graph Files API (`/me/drive/items/{id}`)
    - SharePoint REST API for document libraries
    - Teams Chat API for conversation history
    - Email API for related messages
    - Permission checking (user access validation)
    - Document parsing (PDF, Word, PowerPoint)

- **C6.2 Document Generation/Formatting** → **CAN-09**: Create formatted output documents
  - **Description**: Generate meeting summaries, reports, agendas, and other documents
  - **Capabilities**:
    - Meeting summary generation (key points, decisions, action items)
    - Agenda formatting (structured outline)
    - Report generation (analytics, time spent reports)
    - Email composition (meeting requests, updates)
    - Markdown/HTML formatting
    - Export to multiple formats (PDF, Word, email body)
  - **Frequency**: 56% (5/9 v2 prompts) - organizer-1, schedule-2, collaborate-1, collaborate-2, collaborate-3
  - **Dependencies**: Child of CAN-07 (Metadata Extraction)
  - **Technical Requirements**:
    - LLM text generation (GPT-4 for summaries)
    - Template rendering engine (Jinja2, Handlebars)
    - Document format libraries (python-docx, pypdf)
    - HTML/Markdown rendering
    - Email formatting (MIME)
    - Style/branding application

**Priority**: HIGH - Content creation and retrieval for collaboration

---

#### 7. **Scheduling & Constraint Resolution**
*Implements: CAN-11, CAN-12, CAN-14*

**Core Capabilities**:
- **C7.1 Priority/Preference Matching** → **CAN-11**: Align meetings with user priorities
  - **Description**: Compare and rank meetings against user's stated priorities/preferences
  - **Capabilities**:
    - Priority list parsing (user's top priorities)
    - Meeting-to-priority matching (keyword alignment, topic relevance)
    - Scoring and ranking (priority match percentage)
    - Preference-based filtering (only show matches above threshold)
    - Justification generation (explain why meeting matches priority)
    - Multi-criteria decision support
  - **Frequency**: 44% (4/9 v2 prompts) - organizer-1, schedule-2, collaborate-1, collaborate-3
  - **Dependencies**: Requires CAN-02 (Type), CAN-03 (Importance)
  - **Technical Requirements**:
    - Semantic similarity scoring (embeddings, cosine similarity)
    - Keyword matching and NLP
    - Multi-attribute scoring algorithms
    - User preference storage and learning
    - Explainability module (why this score)
    - Threshold configuration

- **C7.2 Constraint Satisfaction** → **CAN-12**: Find time slots that satisfy all constraints
  - **Description**: Solve scheduling constraints to find valid meeting times
  - **Capabilities**:
    - Multi-constraint solving (time, attendees, duration, recurrence)
    - Optimal slot selection (minimize conflicts, respect preferences)
    - Recurring meeting scheduling (weekly, biweekly, monthly patterns)
    - Buffer time insertion (before/after meetings)
    - Location constraint handling (room capacity, availability)
    - Conflict resolution strategies
  - **Frequency**: 44% (4/9 v2 prompts) - schedule-1, schedule-2, schedule-3, collaborate-3
  - **Dependencies**: Requires CAN-06 (Availability)
  - **Technical Requirements**:
    - Constraint satisfaction solver (OR-Tools, Z3, custom algorithms)
    - Multi-user calendar aggregation
    - Scoring function for slot quality
    - Optimization algorithms (genetic, simulated annealing)
    - Constraint prioritization (hard vs soft constraints)
    - Fallback strategies when no solution exists

- **C7.3 Recommendation Engine** → **CAN-14**: Suggest optimal meeting times and configurations
  - **Description**: Generate intelligent recommendations for scheduling decisions
  - **Capabilities**:
    - Best time slot suggestions (considering all factors)
    - Alternative options ranking (if first choice unavailable)
    - Meeting consolidation recommendations (combine similar meetings)
    - Attendee subset suggestions (optional vs required)
    - Duration optimization (right-size meetings)
    - Frequency recommendations (how often to meet)
  - **Frequency**: 44% (4/9 v2 prompts) - schedule-1, schedule-2, schedule-3, collaborate-3
  - **Dependencies**: Requires CAN-12 (Constraint Satisfaction)
  - **Technical Requirements**:
    - Ranking algorithms (multi-criteria decision making)
    - Historical pattern learning (what worked before)
    - User feedback loop (improve over time)
    - Alternative generation strategies
    - Explanation generation (why this recommendation)
    - A/B testing framework for optimization

**Priority**: HIGH - Intelligent scheduling and optimization

---

#### 8. **Advanced Meeting Intelligence**
*Implements: CAN-16, CAN-21, CAN-22, CAN-25*

**Core Capabilities**:
- **C8.1 Event Monitoring/Change Detection** → **CAN-16**: Track meeting changes over time
  - **Description**: Monitor calendar events for changes and notify users
  - **Capabilities**:
    - Change detection (reschedule, cancellation, attendee changes)
    - Notification triggering (alert user to important changes)
    - Historical tracking (audit trail of event modifications)
    - Pattern recognition (frequently rescheduled meetings)
    - Anomaly detection (unusual meeting patterns)
    - Watch list management (which events to monitor)
  - **Frequency**: 11% (1/9 v2 prompts) - organizer-2
  - **Use Case**: "Track all my important meetings" - monitoring requirement
  - **Technical Requirements**:
    - Calendar change notifications (webhooks/polling)
    - Event diff computation (what changed)
    - Notification system integration
    - Event storage for historical comparison
    - Change pattern analysis
    - User notification preferences

- **C8.2 Focus Time/Preparation Time Analysis** → **CAN-21**: Identify prep time needs
  - **Description**: Analyze meetings requiring preparation and estimate needed focus time
  - **Capabilities**:
    - Prep time estimation (based on meeting type, importance, attendees)
    - Focus time block suggestions (when to prepare)
    - Material review time calculation (document reading time)
    - Meeting complexity scoring (simple vs requires deep prep)
    - Buffer time recommendations (pre-meeting focus blocks)
    - Auto-block focus time in calendar
  - **Frequency**: 11% (1/9 v2 prompts) - organizer-2
  - **Use Case**: "Flag meetings that require focus time to prepare"
  - **Dependencies**: Child of CAN-07 (Metadata Extraction)
  - **Technical Requirements**:
    - Complexity scoring model (ML-based)
    - Historical prep time data (user patterns)
    - Document size/complexity analysis
    - Calendar gap analysis (find focus time slots)
    - Auto-scheduling of prep blocks
    - Integration with task management systems

- **C8.3 Research/Intelligence Gathering** → **CAN-22**: Gather background information
  - **Description**: Collect relevant context and background for meetings
  - **Capabilities**:
    - Attendee background research (LinkedIn, org profiles)
    - Company/account research (CRM data, news, financials)
    - Previous meeting history (past interactions)
    - Related project context (ongoing work, decisions)
    - Topic research (industry trends, technical background)
    - Competitive intelligence (if customer/partner meeting)
  - **Frequency**: 33% (3/9 v2 prompts) - collaborate-1, collaborate-2, collaborate-3
  - **Dependencies**: Requires CAN-05 (Attendee Resolution), CAN-08 (Document Retrieval)
  - **Technical Requirements**:
    - Web search integration (Bing, Google)
    - CRM API integration (Salesforce, Dynamics)
    - LinkedIn/social media APIs
    - Internal knowledge base search
    - Document summarization (LLM)
    - Privacy controls (what data to surface)

- **C8.4 Event Annotation/Flagging** → **CAN-25**: Mark events with conditional flags/labels (NEW in V2.0)
  - **Description**: Apply conditional flags, labels, or annotations to calendar events
  - **Capabilities**:
    - Conditional event flagging (importance, prep needed, conflicts, etc.)
    - Custom label application (categories, tags, priorities)
    - Visual indicators (color coding, icons)
    - Filter-based auto-tagging (rules-based annotation)
    - Batch flagging operations (flag all matching events)
    - Flag persistence and synchronization
  - **Frequency**: 11% (1/9 v2 prompts) - organizer-2
  - **Use Case**: "Flag any that require focus time to prepare" - conditional marking
  - **NEW Task Rationale**: Identified through human evaluation - "flag meetings" is distinct from monitoring/tracking
  - **Technical Requirements**:
    - Calendar event tagging/categories API
    - Conditional logic engine (rule evaluation)
    - Visual annotation system (colors, icons)
    - Bulk update operations
    - Tag/flag management UI
    - Synchronization with calendar system

**Priority**: MEDIUM - Advanced intelligence for power users

---

### Tier 3: Specialized Capabilities (Optional/Advanced Features)

#### 9. **Workflow Automation & Orchestration**
*Implements: CAN-15, CAN-17, CAN-23, CAN-24*

**Core Capabilities**:
- **C9.1 Recurrence Rule Generation** → **CAN-15**: Create recurring meeting patterns
  - **Description**: Generate iCalendar RRULE specifications for recurring events
  - **Capabilities**:
    - Natural language recurrence parsing ("every other Tuesday")
    - RRULE generation (RFC 5545 compliance)
    - Custom recurrence patterns (complex schedules)
    - Exception handling (skip holidays, specific dates)
    - Recurrence modification (change future instances)
    - Until/count termination handling
  - **Frequency**: 11% (1/9 v2 prompts) - schedule-1
  - **Technical Requirements**:
    - RRULE library (python-dateutil, rrule.js)
    - Natural language parsing for recurrence
    - Holiday calendar integration
    - Exception date handling
    - Validation of RRULE syntax
    - Preview generation (show next N occurrences)

- **C9.2 Automatic Rescheduling** → **CAN-17**: Orchestrated automatic meeting rescheduling
  - **Description**: Detect conflicts and automatically reschedule meetings
  - **Capabilities**:
    - Conflict detection (overlapping events, declines)
    - Affected meeting identification
    - Alternative slot finding (CAN-06 + CAN-12)
    - Automatic calendar update
    - Attendee notification
    - Rollback on failure
  - **Frequency**: 11% (1/9 v2 prompts) - schedule-1
  - **Note**: Complex orchestrated workflow combining multiple tasks
  - **Dependencies**: CAN-06 (Availability), CAN-12 (Constraints), CAN-13 (RSVP)
  - **Technical Requirements**:
    - Event-driven triggers (decline notifications)
    - Workflow orchestration (state machine)
    - Retry/rollback logic
    - Multi-step transaction handling
    - Notification templates
    - Audit logging

- **C9.3 Conflict Resolution/Auto-Rescheduling** → **CAN-23**: Resolve calendar conflicts automatically
  - **Description**: Handle meeting conflicts with intelligent resolution strategies
  - **Capabilities**:
    - Conflict detection (double-bookings, overlaps)
    - Priority-based resolution (keep higher priority)
    - Alternative time finding
    - Automatic "bump" logic (reschedule lower priority)
    - Multi-conflict resolution (cascade handling)
    - User confirmation workflow
  - **Frequency**: 11% (1/9 v2 prompts) - schedule-1
  - **Dependencies**: Requires CAN-03 (Importance), CAN-12 (Constraints)
  - **Technical Requirements**:
    - Conflict detection algorithms
    - Priority scoring system
    - Decision trees for resolution
    - Multi-step orchestration
    - User approval workflows
    - Fallback strategies

- **C9.4 Multi-party Coordination/Negotiation** → **CAN-24**: Coordinate across multiple participants
  - **Description**: Find consensus time across multiple busy calendars
  - **Capabilities**:
    - Multi-calendar aggregation (all attendees)
    - Polling/voting for preferred times
    - Iterative negotiation (suggest, gather feedback, adjust)
    - Priority attendee weighting (required vs optional)
    - Compromise detection (best available slot)
    - Automated follow-up (nudge non-responders)
  - **Frequency**: 11% (1/9 v2 prompts) - schedule-3
  - **Dependencies**: Requires CAN-06 (Availability), CAN-12 (Constraints)
  - **Technical Requirements**:
    - Multi-user availability API
    - Voting/polling system
    - Consensus algorithms
    - Email/notification workflows
    - Response tracking
    - Timeout/deadline handling

**Priority**: MEDIUM - Advanced automation for complex scenarios

---

#### 10. **Presentation & Insights**
*Implements: CAN-18, CAN-20, CAN-23*

**Core Capabilities**:
- **C10.1 Objection/Risk Anticipation** → **CAN-18**: Predict potential issues or concerns
  - **Description**: Anticipate objections, risks, or challenges for upcoming meetings
  - **Capabilities**:
    - Risk pattern recognition (historical conflicts)
    - Stakeholder concern prediction (based on past behavior)
    - Topic sensitivity analysis (controversial subjects)
    - Decision blocker identification (missing approvals, data)
    - Preparation gap detection (insufficient background)
    - Mitigation strategy suggestions
  - **Frequency**: 22% (2/9 v2 prompts) - collaborate-1, collaborate-3
  - **Note**: Scope clarification needed - distinguish from meeting goals/objectives
  - **Human Evaluator Warning**: Collaborate-1 over-interpretation - removed CAN-18 from that prompt
  - **Technical Requirements**:
    - Historical meeting analysis
    - Sentiment analysis on past discussions
    - Stakeholder modeling (positions, concerns)
    - Topic risk scoring
    - LLM-based prediction
    - Mitigation recommendation engine

- **C10.2 Data Visualization/Reporting** → **CAN-20**: Visual representation of calendar data
  - **Description**: Create visual reports and dashboards for meeting analytics
  - **Capabilities**:
    - Time spent charts (pie, bar, timeline)
    - Meeting type distribution graphs
    - Trend visualization (time series)
    - Heatmaps (busiest times/days)
    - Attendee network graphs (collaboration patterns)
    - Executive dashboards (KPIs, summaries)
  - **Frequency**: 11% (1/9 v2 prompts) - organizre-3
  - **Dependencies**: Requires CAN-10 (Time Aggregation)
  - **Technical Requirements**:
    - Charting library (D3.js, Chart.js, matplotlib)
    - Dashboard framework (Grafana, custom)
    - Data transformation pipelines
    - Export formats (PNG, PDF, interactive HTML)
    - Color schemes and branding
    - Responsive design for mobile

- **C10.3 Agenda Generation/Structuring** → **CAN-23**: Create structured meeting agendas
  - **Description**: Generate well-structured agendas for upcoming meetings
  - **Capabilities**:
    - Topic extraction (from previous meetings, documents)
    - Agenda item prioritization (most important first)
    - Time allocation per topic (realistic estimates)
    - Structured formatting (numbered sections, subsections)
    - Decision points identification (what needs to be decided)
    - Action item sections (follow-up tracking)
  - **Frequency**: 22% (2/9 v2 prompts) - collaborate-1, collaborate-3
  - **Dependencies**: Requires CAN-08 (Document Retrieval), CAN-22 (Research)
  - **Technical Requirements**:
    - Topic extraction NLP
    - LLM-based structuring (GPT-4)
    - Template library (meeting type-specific)
    - Time estimation models
    - Formatting engine (Markdown, Word)
    - Integration with meeting tools (Teams, Zoom)

**Priority**: LOW - Nice-to-have features for enhanced user experience

---

## Implementation Roadmap

### Phase 1: MVP Foundation (Weeks 1-4)
**Goal**: Enable basic meeting management and intelligence

**Tier 1 Tasks** (6 tasks):
1. ✅ **CAN-01** (Calendar Retrieval) - Week 1
2. ✅ **CAN-04** (NLU) - Week 1-2
3. ✅ **CAN-02** (Type Classification) - Week 2
4. ✅ **CAN-03** (Importance Assessment) - Week 2
5. ✅ **CAN-05** (Attendee Resolution) - Week 3
6. ✅ **CAN-07** (Metadata Extraction) - Week 3

**Critical Infrastructure**:
- Microsoft Graph API integration
- LLM API setup (GPT-4/Claude)
- Authentication (MSAL + OAuth 2.0)
- Database schema (events, users, contacts)
- Basic NLU pipeline

**Deliverable**: Can retrieve, classify, and assess importance of meetings

---

### Phase 2: Scheduling & Optimization (Weeks 5-8)
**Goal**: Enable intelligent scheduling and constraint resolution

**Tier 2 Tasks** (9 tasks):
1. ✅ **CAN-06** (Availability) - Week 5
2. ✅ **CAN-11** (Priority Matching) - Week 5
3. ✅ **CAN-12** (Constraint Satisfaction) - Week 6
4. ✅ **CAN-13** (RSVP Update) - Week 6
5. ✅ **CAN-14** (Recommendation Engine) - Week 7
6. ✅ **CAN-09** (Document Generation) - Week 7
7. ✅ **CAN-08** (Document Retrieval) - Week 8
8. ✅ **CAN-10** (Time Aggregation) - Week 8
9. ✅ **CAN-21** (Focus Time Analysis) - Week 8

**Infrastructure Additions**:
- Constraint solver integration (OR-Tools)
- Recommendation scoring algorithms
- Document template library
- Time series analytics

**Deliverable**: Can schedule meetings, optimize calendar, generate summaries

---

### Phase 3: Advanced Intelligence (Weeks 9-12)
**Goal**: Enable specialized capabilities and workflow automation

**Tier 3 Tasks** (10 tasks):
1. ✅ **CAN-16** (Event Monitoring) - Week 9
2. ✅ **CAN-22** (Research/Intelligence) - Week 9
3. ✅ **CAN-25** (Event Flagging) - Week 9 (NEW)
4. ✅ **CAN-15** (Recurrence Rules) - Week 10
5. ✅ **CAN-17** (Auto-Rescheduling) - Week 10
6. ✅ **CAN-23** (Conflict Resolution) - Week 11
7. ✅ **CAN-24** (Multi-party Coordination) - Week 11
8. ✅ **CAN-18** (Risk Anticipation) - Week 12
9. ✅ **CAN-20** (Visualization) - Week 12
10. ✅ **CAN-23** (Agenda Generation) - Week 12 (Note: Renumbered from previous framework)

**Infrastructure Additions**:
- Workflow orchestration engine
- Event-driven architecture (webhooks)
- Visualization library
- External data integration (CRM, LinkedIn)

**Deliverable**: Full-featured Calendar.AI platform with all 25 capabilities

---

## Capability Dependencies

### Critical Dependency Chains

1. **Calendar Foundation Chain**:
   - CAN-04 (NLU) → **Required by ALL**
   - CAN-01 (Calendar Retrieval) → **Required by ALL**
   - CAN-07 (Metadata Extraction) → **Parent of 6 tasks**

2. **Scheduling Chain**:
   - CAN-01 → CAN-06 (Availability) → CAN-12 (Constraints) → CAN-14 (Recommendations)

3. **RSVP Chain**:
   - CAN-07 (Metadata) → CAN-13 (RSVP Update)

4. **Importance Assessment Chain**:
   - CAN-05 (Attendee Resolution) → CAN-03 (Importance) → CAN-11 (Priority Matching)

5. **Document Chain**:
   - CAN-07 (Metadata) → CAN-08 (Document Retrieval) → CAN-09 (Document Generation)

6. **Advanced Intelligence Chain**:
   - CAN-08 (Documents) + CAN-05 (Attendees) → CAN-22 (Research) → CAN-23 (Agenda Generation)

7. **Monitoring & Flagging Chain** (NEW):
   - CAN-16 (Event Monitoring) + CAN-21 (Focus Time) → CAN-25 (Event Flagging)

### Parent-Child Relationships

**CAN-07 (Metadata Extraction)** is the critical parent task:
- Child: CAN-05 (Attendee Resolution)
- Child: CAN-08 (Document Retrieval)
- Child: CAN-09 (Document Generation)
- Child: CAN-13 (RSVP Update)
- Child: CAN-19 (Resource Booking)
- Child: CAN-21 (Focus Time Analysis)

**Human Evaluator Insights**:
- **CAN-05 Critical**: "Model needs to get metadata, and from there to find attendee for those meetings" (Schedule-2)
- **CAN-05 for Senior Leadership**: "System needs to know who are in the senior leadership to find relevant meetings and meeting related materials" (Collaborate-2)
- **CAN-05 MUST Precede CAN-01**: Cannot find "meeting with senior leadership" without knowing who senior leadership is

---

## V2.0 Gold Standard Validation

### Statistical Performance

**3-Trial Stability Test**:
- **F1 Score**: 78.40% ± 0.72% (EXCELLENT < 1% variance)
- **Consistency**: 93.6% task selection agreement across trials
- **API Calls**: 27/27 successful (100% success rate)

**Framework Coverage**:
- **Total Tasks**: 25 (CAN-01 through CAN-25)
- **Tasks Used**: 22/25 (88% framework coverage)
- **Average Tasks/Prompt**: 7.2 (range: 3-10)

**Tier Performance**:
- **Tier 1**: 100% coverage (all 6 universal tasks used)
- **Tier 2**: 89% coverage (8/9 common tasks used)
- **Tier 3**: 80% coverage (8/10 specialized tasks used)

### Human Evaluation Results

**9 V2 Prompts Evaluated**:
- ✅ **Correct**: 5 prompts (Organizer-1, Organizre-3, Schedule-1, Schedule-3, Collaborate-3)
- ⚠️ **Partial**: 3 prompts (Organizer-2, Schedule-2, Collaborate-2) - missing specific tasks
- ❓ **Needs Review**: 1 prompt (Collaborate-1) - over-interpretation issue

**Key Corrections Applied**:
1. **Added CAN-25**: Event Annotation/Flagging (Organizer-2: "flag meetings")
2. **Added CAN-05**: Attendee Resolution (Schedule-2, Collaborate-2) - critical dependency
3. **Removed CAN-18**: From Collaborate-1 (over-interpretation of "meeting goals")
4. **Added CAN-16**: Event Monitoring (Organizer-2: "track meetings")

**Framework Evolution**:
- **Renumbering**: CAN-02A/CAN-02B → CAN-02/CAN-03 (cleaner sequential ordering)
- **New Task**: CAN-25 validated through human evaluation
- **Validated Dependencies**: CAN-05 confirmed as critical for senior leadership queries

---

## Success Metrics

### Implementation Success Criteria

**MVP (Phase 1)**:
- ✅ All 6 Tier 1 tasks implemented
- ✅ Can process all 9 v2 hero prompts (basic level)
- ✅ F1 > 70% on hero prompt decomposition
- ✅ < 2s response time for NLU + retrieval

**Production (Phase 2)**:
- ✅ All 15 Tier 1+2 tasks implemented
- ✅ Can handle 8/9 hero prompts (advanced level)
- ✅ F1 > 75% on hero prompt decomposition
- ✅ < 5s end-to-end for scheduling recommendations

**Enterprise (Phase 3)**:
- ✅ All 25 tasks implemented
- ✅ Can handle all 9 hero prompts (full feature set)
- ✅ F1 > 78% matching gold standard
- ✅ < 10s for complex workflows (multi-party coordination)

### Quality Metrics

**Accuracy**:
- Task decomposition F1 > 78% (gold standard)
- Meeting type classification > 85% accuracy
- Importance assessment agreement > 80% with users
- Availability finding correctness > 95%

**Performance**:
- Calendar retrieval < 500ms (100 events)
- NLU processing < 1s per query
- Constraint solving < 3s (5-person meeting)
- End-to-end scheduling < 10s

**Reliability**:
- API success rate > 99.5%
- LLM availability > 99.9% (with fallbacks)
- Data consistency 100% (no lost events)
- Webhook delivery > 98%

---

## Appendix: V2.0 Framework Summary

### Complete Task List (25 Tasks)

**Tier 1 - Universal** (6 tasks, 50%+ frequency):
1. CAN-01: Calendar Events Retrieval (100%)
2. CAN-02: Meeting Type Classification (56%)
3. CAN-03: Meeting Importance Assessment (56%)
4. CAN-04: Natural Language Understanding (100%)
5. CAN-05: Attendee/Contact Resolution (67%)
6. CAN-06: Availability Checking (33%) - *Note: Borderline Tier 1/2*

**Tier 2 - Common** (9 tasks, 25-50% frequency):
7. CAN-07: Meeting Metadata Extraction (78%)
8. CAN-08: Document/Content Retrieval (33%)
9. CAN-09: Document Generation/Formatting (56%)
10. CAN-10: Time Aggregation/Statistical Analysis (11%) - *Note: Borderline Tier 2/3*
11. CAN-11: Priority/Preference Matching (44%)
12. CAN-12: Constraint Satisfaction (44%)
13. CAN-13: RSVP Status Update (44%)
14. CAN-14: Recommendation Engine (44%)
15. CAN-21: Focus Time/Preparation Time Analysis (11%) - *Moved to Tier 2 from Tier 3*

**Tier 3 - Specialized** (10 tasks, <25% frequency):
16. CAN-15: Recurrence Rule Generation (11%)
17. CAN-16: Event Monitoring/Change Detection (11%)
18. CAN-17: Automatic Rescheduling (11%)
19. CAN-18: Objection/Risk Anticipation (22%)
20. CAN-19: Resource Booking (Rooms/Equipment) (0%) - *Not used in v2 prompts*
21. CAN-20: Data Visualization/Reporting (11%)
22. CAN-22: Research/Intelligence Gathering (33%)
23. CAN-23: Agenda Generation/Structuring (22%)
24. CAN-24: Multi-party Coordination/Negotiation (11%)
25. CAN-25: Event Annotation/Flagging (11%) - **NEW in V2.0**

### Key Changes from V1.0 to V2.0

1. **Task Count**: 24 → 25 tasks
2. **New Task**: CAN-25 (Event Annotation/Flagging)
3. **Renumbered**: CAN-02A/CAN-02B → CAN-02/CAN-03 (sequential 1-25)
4. **Human Validated**: All 9 v2 prompts reviewed by expert
5. **Statistical Validation**: 3-trial stability test (F1 78.40% ± 0.72%)
6. **Updated Tiers**: Based on actual v2 usage patterns

### Framework Validation Highlights

- **93.6% Consistency**: Across 3 independent LLM trials
- **< 1% Variance**: Excellent framework stability
- **88% Coverage**: 22/25 tasks used across all v2 prompts
- **100% Success Rate**: 27/27 GPT-5 API calls successful
- **Human-Corrected**: Expert review ensured accuracy

---

**Document End**

*This infrastructure capability inventory provides the technical foundation for implementing all 25 canonical tasks in the Calendar.AI V2.0 framework. For functional/prompt-based analysis, see [CANONICAL_TASKS_GOLD_STANDARD_REFERENCE_V2.md](./CANONICAL_TASKS_GOLD_STANDARD_REFERENCE_V2.md).*
