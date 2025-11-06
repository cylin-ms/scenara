# Enterprise Meeting Intelligence - Capability Inventory Analysis

**Date**: November 6, 2025 (Updated to C-GUTT Taxonomy)  
**Source**: Consolidated analysis of 9 Calendar.AI Hero Prompts  
**Method**: Cross-prompt consolidation of 66 original tasks → 39 atomic C-GUTTs  
**Purpose**: Define atomic capabilities required for production implementation

**Related Documents**:
- [Consolidated GUTT Reference](./CONSOLIDATED_GUTT_REFERENCE.md) - Complete inventory of 39 atomic C-GUTTs with examples
- [GUTT Cross-Prompt Consolidation Analysis](./GUTT_CROSS_PROMPT_CONSOLIDATION_ANALYSIS.md) - Detailed consolidation methodology (66→39, 41% reduction)

---

## Document Purpose

This document presents the **infrastructure-centric view** of capabilities needed to implement the 39 atomic C-GUTTs (Consolidated Generative Unit Test Tasks) that serve all 9 Calendar.AI hero prompts.

**What are C-GUTTs?**
- **Atomic capabilities**: Each C-GUTT is a single, well-defined functional unit
- **Cross-prompt reuse**: Average 1.69 prompts per C-GUTT (vs 1.0 for original decomposition)
- **Implementation focus**: These 39 C-GUTTs are what must be built - no redundant capabilities

**Two Complementary Views**:
1. **This Document - Infrastructure View**: Groups C-GUTTs by technical implementation layer (Calendar API, NLP, ML, etc.)
2. **[CONSOLIDATED_GUTT_REFERENCE.md](./CONSOLIDATED_GUTT_REFERENCE.md) - Functional View**: Each C-GUTT with examples and usage patterns

---

## Executive Summary

Consolidated 66 original unit tasks across 9 hero prompts into **39 atomic C-GUTTs**, organized into **12 foundational capability clusters** and **47 specific technical capabilities** for implementation.

**Consolidation Results**:
- **Original decomposition**: 66 prompt-specific tasks
- **Consolidated C-GUTTs**: 39 atomic capabilities (41% reduction)
- **Implementation efficiency**: Build once, reuse across 1-5 prompts per C-GUTT
- **Most critical**: C-GUTT-01 (Calendar Event Retrieval) serves 5 prompts (76% coverage)

**Key Insights**:
- **4 Core Infrastructure Capabilities** (Calendar API, NLP, Data Access, Action Execution) enable 85% of C-GUTTs
- **3 Intelligence Capabilities** (ML Classification, Semantic Analysis, Pattern Recognition) differentiate basic vs advanced features
- **5 Specialized Capabilities** for advanced use cases (Multi-calendar coordination, Resource booking, CRM integration)
- **Critical Dependencies**: Calendar API (C-GUTT-01 used by 5 prompts), NLP (8 C-GUTTs), Constraint Satisfaction (C-GUTT-19 used by 4 prompts)
- **Most Reused C-GUTTs**: C-GUTT-01 (76%), C-GUTT-19 (44%), C-GUTT-02/07/11/14/20/32/33 (33% each)

---

## Capability Taxonomy

### Tier 1: Foundation Infrastructure (Required for MVP)

#### 1. **Calendar Data Access & Management**
*Implements: C-GUTT-01, C-GUTT-02, C-GUTT-05, C-GUTT-06, C-GUTT-07, C-GUTT-30*

**Core Capabilities**:
- **C1.1 Single Calendar Read** → **C-GUTT-01**: Query user's calendar events (past, present, future)
  - Date range filtering
  - Event metadata extraction (title, time, attendees, location, status)
  - Pending invitation vs confirmed event filtering
  - Historical data access (time series analysis)
  - **Used by 5 prompts**: Organizer-1, Organizer-2, Organizer-3, Schedule-2, Collaborate-3

- **C1.2 Multi-Calendar Read** → **C-GUTT-02**: Access calendars for multiple users
  - Cross-user free/busy queries
  - Availability aggregation across attendees
  - Permissions and access control handling
  - **Used by 3 prompts**: Schedule-1, Schedule-2, Schedule-3

- **C1.3 Calendar Write Operations** → **C-GUTT-05, C-GUTT-06, C-GUTT-07**: Modify calendar state
  - RSVP updates (accept/decline) → C-GUTT-05
  - Event creation (single and recurring) → C-GUTT-06
  - Event updates and rescheduling → C-GUTT-07
  - Event deletion
  - Recurrence rule generation (iCalendar RRULE)
  - **Used by 6 prompts**: Organizer-1, Schedule-1, Schedule-2, Schedule-3

- **C1.4 Calendar Status Management** → **C-GUTT-30**: Control user availability representation
  - Free/busy status updates
  - Out-of-office settings
  - Working hours configuration
  - **Used by 1 prompt**: Schedule-2

**Technical Requirements**:
- Microsoft Graph Calendar API integration
- OAuth 2.0 / MSAL authentication
- Pagination for large datasets
- Real-time event change subscriptions (webhooks)
- Efficient caching and sync strategies

**Priority**: CRITICAL - Blocks 91% of functionality

---

#### 2. **Natural Language Understanding & Generation**
*Implements: C-GUTT-08, C-GUTT-09, C-GUTT-10, C-GUTT-11, C-GUTT-12, C-GUTT-13, C-GUTT-14, C-GUTT-15*

**Core Capabilities**:
- **C2.1 Constraint Extraction** → **C-GUTT-09**: Parse user requests into structured requirements
  - Temporal expressions ("next week", "Thursday afternoon", "in the next 2 weeks")
  - Preferences ("afternoons preferred", "avoid Fridays")
  - Hard vs soft constraints identification
  - Multi-constraint parsing
  - **Used by 2 prompts**: Schedule-1, Schedule-3

- **C2.2 Priority & Goal Understanding** → **C-GUTT-08**: Extract user priorities and goals
  - Priority statement parsing
  - Goal formalization
  - Implicit preference detection
  - **Used by 2 prompts**: Organizer-1, Organizer-3

- **C2.3 Semantic Content Analysis** → **C-GUTT-11**: Understand meaning of text (meeting titles, descriptions, documents)
  - Topic extraction
  - Theme identification
  - Intent classification
  - **Used by 3 prompts**: Collaborate-1, Collaborate-2, Collaborate-3

- **C2.4 Natural Language Generation** → **C-GUTT-31, C-GUTT-32, C-GUTT-33**: Create human-readable outputs
  - Decision justifications and explanations → C-GUTT-31
  - Meeting agendas and summaries → C-GUTT-33
  - Reports and recommendations → C-GUTT-32
  - Professional communication tone
  - **Used by 5 prompts**: Organizer-1, Organizer-2, Organizer-3, Schedule-2, all Collaborate prompts

**Technical Requirements**:
- LLM integration (GPT-4, Claude Sonnet 4.5, or equivalent)
- Prompt engineering framework
- Context window management (meeting data + instructions)
- Output parsing and validation
- Date/time normalization libraries

**Priority**: CRITICAL - Blocks 79% of functionality

---

#### 3. **Data Access & Integration Layer**
*Enables: 45/66 GUTTs (68%)*

**Core Capabilities**:
- **C3.1 Document Access & Retrieval**: Read documents from various sources
  - OneDrive/SharePoint integration
  - Teams files access
  - Email attachments
  - Document format support (PDF, DOCX, PPTX, etc.)
  - **GUTTs Enabled**: 7.1, 8.1, 9.7

- **C3.2 CRM Data Access**: Customer relationship data
  - Contact information and roles
  - Company profiles
  - Interaction history
  - Relationship timelines
  - **GUTTs Enabled**: 9.2, 9.3, 9.4, 9.6

- **C3.3 Organizational Data**: Internal org structure and people info
  - Microsoft Graph People API
  - Organizational hierarchy (manager chains, reports)
  - Job titles and roles
  - Skills and expertise data
  - **GUTTs Enabled**: 7.2, 8.4, 9.3

- **C3.4 Communication History**: Teams chat, email, collaboration patterns
  - Teams chat messages
  - Email threads
  - Document sharing activity
  - Collaboration frequency metrics
  - **GUTTs Enabled**: 9.4, 9.5, 9.6

**Technical Requirements**:
- Microsoft Graph API (People, Teams, OneDrive, SharePoint)
- CRM integration (Dynamics 365, Salesforce, or custom)
- Search APIs (Microsoft Search, Substrate)
- Document parsing libraries
- Data caching and indexing

**Priority**: HIGH - Enables advanced collaboration features

---

#### 4. **Action Execution & Orchestration**
*Enables: 38/66 GUTTs (58%)*

**Core Capabilities**:
- **C4.1 Sequential Task Execution**: Chain multiple operations
  - Workflow orchestration
  - Error handling and rollback
  - Transaction management
  - Progress tracking
  - **GUTTs Enabled**: 5.3→5.4→5.5→5.6→5.7, 6.7→6.8→6.9

- **C4.2 Batch Operations**: Execute multiple similar actions efficiently
  - Bulk RSVP updates
  - Mass meeting creation
  - Parallel API calls
  - **GUTTs Enabled**: 5.3 (decline multiple meetings)

- **C4.3 Event-Driven Automation**: React to calendar changes
  - Decline/conflict detection triggers
  - Automatic rescheduling on conflicts
  - Real-time monitoring
  - **GUTTs Enabled**: 4.6, 4.7

- **C4.4 Confirmation & Reporting**: Track and report action outcomes
  - Action logging
  - Success/failure tracking
  - Summary generation
  - **GUTTs Enabled**: 1.6, 5.8, 9.8

**Technical Requirements**:
- Workflow engine (custom or Azure Logic Apps)
- Webhook handling infrastructure
- Retry logic and idempotency
- Audit logging
- Notification system

**Priority**: HIGH - Differentiator for automation features

---

### Tier 2: Intelligence & Analysis (Advanced Features)

#### 5. **Machine Learning Classification**
*Enables: 35/66 GUTTs (53%)*

**Important**: Meeting Type and Meeting Importance are **distinct capabilities** (C-GUTT-03 vs C-GUTT-04):
- **Type** = structural category (1:1, group, lunch, standup) - format-based
- **Importance** = priority level (critical, high, medium, low) - value-based
- A 1:1 can be low or high importance; a group meeting can be critical or routine

**Core Capabilities**:
- **C5.1 Meeting Type Classification** (→ C-GUTT-03): Categorize meetings into 31+ types
  - 1:1s, team meetings, all-hands, workshops, etc.
  - Based on: attendee count, duration patterns, title keywords, recurrence
  - Confidence scoring
  - Multi-label classification support
  - **GUTTs Enabled**: 3.2, 6.4 (identify override-eligible meetings)

- **C5.2 Meeting Importance Classification** (→ C-GUTT-04): Determine meeting priority level
  - Context-based importance (exec attendance, strategic topics, urgency signals)
  - User-specific importance (role in meeting, relationship to goals)
  - Temporal urgency (deadline proximity, preparation requirements)
  - **Distinct from Type**: Focus on value/priority, not format
  - **GUTTs Enabled**: 2.2 (flag important meetings needing prep)

- **C5.3 Preparation Time Estimation** (→ C-GUTT-18): Predict prep time needed
  - Meeting type → prep time mapping
  - Complexity assessment (attendees, materials, decision weight)
  - User role consideration (presenter vs attendee)
  - **GUTTs Enabled**: 2.3

**Technical Requirements**:
- Meeting classification model (GPT-5, Claude, or fine-tuned)
- Feature engineering (meeting attributes → ML features)
- Training data collection and annotation
- Model versioning and A/B testing
- Performance monitoring (accuracy, latency)

**Priority**: MEDIUM-HIGH - Enables intelligent automation

---

#### 6. **Semantic Analysis & Reasoning**
*Enables: 38/66 GUTTs (58%)*

**Core Capabilities**:
- **C6.1 Priority-Meeting Alignment**: Match meetings to stated priorities
  - Semantic similarity scoring
  - Relevance assessment
  - Multi-factor alignment (topic, people, outcomes)
  - **GUTTs Enabled**: 1.3, 3.4

- **C6.2 Topic Interest Modeling**: Understand what topics people care about
  - Historical topic extraction from communications
  - Interest profile building
  - Personalization based on role and history
  - **GUTTs Enabled**: 9.5

- **C6.3 Objection/Risk Anticipation**: Predict concerns and issues
  - Critical thinking on proposals
  - Stakeholder perspective modeling
  - Risk identification from context
  - **GUTTs Enabled**: 8.5

- **C6.4 Response Generation**: Create effective answers to objections
  - Argumentation strategies
  - Evidence marshaling from context
  - Persuasive communication
  - **GUTTs Enabled**: 8.6

**Technical Requirements**:
- Semantic embedding models (text-embedding-ada-002, sentence-transformers)
- Vector similarity search (FAISS, Pinecone)
- Reasoning-capable LLM (GPT-4, Claude Sonnet)
- Prompt engineering for chain-of-thought reasoning
- Context management (multi-document reasoning)

**Priority**: MEDIUM - Differentiates good from great UX

---

#### 7. **Pattern Recognition & Analytics**
*Enables: 25/66 GUTTs (38%)*

**Core Capabilities**:
- **C7.1 Time Usage Analysis**: Understand how time is spent
  - Meeting aggregation by category, participant, project
  - Trend detection over time periods
  - Statistical summaries
  - **GUTTs Enabled**: 3.3

- **C7.2 Low-Value Meeting Detection**: Flag time-wasting meetings
  - Value scoring algorithms
  - Reclamation opportunity identification
  - Pattern-based detection (recurring low-value)
  - **GUTTs Enabled**: 3.5

- **C7.3 Scheduling Pattern Optimization**: Find better ways to schedule
  - Conflict pattern analysis
  - Fragmentation detection (many small gaps)
  - Consolidation opportunities
  - **GUTTs Enabled**: 3.6, 3.7

**Technical Requirements**:
- Time series analysis libraries
- Statistical aggregation engine
- Visualization generation (charts, graphs)
- Anomaly detection algorithms
- Recommendation engine

**Priority**: MEDIUM - Enables analytics and insights features

---

### Tier 3: Advanced Coordination (Enterprise Scale)

#### 8. **Multi-Party Scheduling & Coordination**
*Enables: 20/66 GUTTs (30%)*

**Core Capabilities**:
- **C8.1 Availability Aggregation**: Combine free/busy across multiple calendars
  - Intersection algorithms (find common free times)
  - Hierarchical constraint handling (prioritize certain attendees)
  - Timezone normalization
  - **GUTTs Enabled**: 6.2, 6.3

- **C8.2 Constraint Satisfaction Optimization**: Find best time given complex rules
  - Multi-objective optimization (minimize conflicts, maximize preferences)
  - Hard vs soft constraint weighting
  - Slot ranking algorithms
  - **GUTTs Enabled**: 4.3, 6.7

- **C8.3 Conflict Resolution**: Handle scheduling conflicts automatically
  - Override eligibility rules (what meetings can be moved)
  - Cascading rescheduling (moving one meeting affects others)
  - Undo/rollback capabilities
  - **GUTTs Enabled**: 6.4, 6.8

- **C8.4 Automatic Rescheduling**: Move meetings when conflicts arise
  - Trigger detection (decline, new conflict)
  - Re-run scheduling logic
  - Communication to attendees
  - **GUTTs Enabled**: 4.7, 5.4, 5.5

**Technical Requirements**:
- Constraint satisfaction solver (OR-Tools, custom algorithms)
- Graph algorithms (dependency tracking)
- Concurrency control (prevent race conditions)
- Notification system (inform affected parties)
- Undo/audit trail

**Priority**: MEDIUM - Needed for advanced scheduling features

---

#### 9. **Resource Management**
*Enables: 12/66 GUTTs (18%)*

**Core Capabilities**:
- **C9.1 Conference Room Discovery**: Find available rooms
  - Room resource calendars
  - Capacity matching
  - Location/building filtering
  - Equipment requirements (video, whiteboard)
  - **GUTTs Enabled**: 6.6

- **C9.2 Room Booking**: Reserve rooms for meetings
  - Resource reservation API
  - Booking confirmation
  - Release on cancellation
  - **GUTTs Enabled**: 6.6

- **C9.3 Location Intelligence**: Understand physical context
  - In-person vs remote meeting capability
  - Participant location tracking
  - Travel time considerations
  - **GUTTs Enabled**: 6.5

**Technical Requirements**:
- Microsoft Graph Places API
- Room/resource calendars integration
- Location data (office locations, remote status)
- Capacity and equipment metadata

**Priority**: LOW-MEDIUM - Nice-to-have for in-person meetings

---

#### 10. **Decision Support & Recommendations**
*Enables: 22/66 GUTTs (33%)*

**Core Capabilities**:
- **C10.1 Accept/Decline Logic**: Recommend meeting responses
  - Priority alignment assessment
  - Schedule impact evaluation
  - Threshold-based rules
  - **GUTTs Enabled**: 1.4

- **C10.2 Time Reclamation Recommendations**: Suggest specific changes
  - Meeting elimination candidates
  - Delegation suggestions
  - Consolidation opportunities
  - Shortening proposals (60min → 30min)
  - **GUTTs Enabled**: 3.7

- **C10.3 Preparation Guidance**: Advise on meeting prep
  - Flagging high-prep meetings
  - Focus time blocking suggestions
  - Lead time adequacy checking
  - **GUTTs Enabled**: 2.4, 2.6

- **C10.4 Actionable Insights**: Provide clear next steps
  - Specific, actionable recommendations
  - Prioritized action lists
  - Impact quantification (e.g., "reclaim 5 hours/week")
  - **GUTTs Enabled**: 2.7, 3.6, 3.8

**Technical Requirements**:
- Decision rule engine
- Recommendation scoring
- Impact simulation
- A/B testing framework (measure recommendation quality)
- User feedback collection

**Priority**: MEDIUM-HIGH - Key to user value delivery

---

#### 11. **Context Synthesis & Briefing**
*Enables: 18/66 GUTTs (27%)*

**Core Capabilities**:
- **C11.1 Multi-Source Information Aggregation**: Combine data from many sources
  - Calendar + documents + CRM + communications
  - Deduplication and conflict resolution
  - Temporal ordering and recency weighting
  - **GUTTs Enabled**: 7.1, 8.1, 9.1-9.7

- **C11.2 Executive Summarization**: Distill complex info into key points
  - Content compression (many docs → 3 talking points)
  - Priority ranking (what matters most)
  - Audience-aware framing (executive vs technical)
  - **GUTTs Enabled**: 8.3, 8.4

- **C11.3 Dossier Generation**: Create person/company profiles
  - Entity resolution (identify people/companies)
  - Profile compilation (background, role, history, interests)
  - Relationship history summarization
  - **GUTTs Enabled**: 9.2, 9.3, 9.4

- **C11.4 Meeting Context Building**: Assemble relevant background for meetings
  - Project status retrieval
  - Stakeholder analysis
  - Historical context (past meetings, decisions)
  - **GUTTs Enabled**: 7.1, 9.6

**Technical Requirements**:
- Entity resolution and knowledge graph
- Multi-document summarization (LLM-based)
- Template-based document generation
- Version control (brief updates over time)
- Rich formatting (markdown, HTML)

**Priority**: MEDIUM - High-value for collaboration features

---

#### 12. **Explanation & Transparency**
*Enables: 15/66 GUTTs (23%)*

**Core Capabilities**:
- **C12.1 Decision Justification**: Explain why actions were taken
  - Rule-based explanations (link to priority rules)
  - Evidence citation (which data led to decision)
  - Transparency in automation
  - **GUTTs Enabled**: 1.6

- **C12.2 Reasoning Trace**: Show how conclusions were reached
  - Step-by-step logic
  - Intermediate calculations
  - Assumption disclosure
  - **GUTTs Enabled**: 3.4, 8.5

- **C12.3 Confidence & Uncertainty**: Communicate certainty levels
  - Confidence scores on classifications
  - Uncertainty flags ("not enough data to determine")
  - Alternative scenarios
  - **GUTTs Enabled**: 2.2, 5.1

**Technical Requirements**:
- Explainable AI techniques (LIME, SHAP for ML models)
- LLM chain-of-thought prompting
- Logging and audit trails
- Structured explanation templates

**Priority**: LOW-MEDIUM - Important for trust and debugging

---

## Capability Dependency Matrix

### Critical Path Analysis

**Tier 1 Dependencies** (Must have for any functionality):
```
Calendar API (C1) ──────────┐
                            ├──> 60/66 GUTTs (91%)
NLP (C2) ──────────────────┤
                            │
Data Access (C3) ──────────┤
                            │
Action Execution (C4) ─────┘
```

**Tier 2 Enablers** (Differentiate basic from advanced):
```
ML Classification (C5) ───> Intelligent prioritization, automation
Semantic Analysis (C6) ───> Priority alignment, personalization  
Pattern Recognition (C7) ─> Analytics, optimization insights
```

**Tier 3 Specializations** (Advanced use cases):
```
Multi-Party Coord (C8) ───> Complex scheduling scenarios
Resource Mgmt (C9) ───────> In-person meeting logistics
Decision Support (C10) ───> Actionable recommendations
Context Synthesis (C11) ──> Briefing and preparation
Explanation (C12) ────────> Trust and debugging
```

---

## Implementation Roadmap

### Phase 1: Foundation (Weeks 1-4)
**Goal**: Enable basic calendar operations and NLP

**Capabilities to Build**:
- ✅ C1.1, C1.3: Single calendar read/write
- ✅ C2.1, C2.4: Constraint extraction, NLG
- ✅ C4.1, C4.4: Sequential execution, reporting

**Deliverables**:
- Calendar API integration working
- LLM integration for NLP tasks
- Basic workflow engine

**Hero Prompts Enabled**: 1 (partial), 2 (partial), 4 (partial)

---

### Phase 2: Intelligence Layer (Weeks 5-8)
**Goal**: Add ML classification and semantic reasoning

**Capabilities to Build**:
- ✅ C5.1, C5.2, C5.3: Meeting classification, importance, prep time
- ✅ C6.1: Priority-meeting alignment
- ✅ C7.1, C7.2: Time usage analysis, low-value detection

**Deliverables**:
- Meeting classifier deployed (31+ types, 80%+ accuracy)
- Importance scoring algorithm
- Time analytics dashboard

**Hero Prompts Enabled**: 1 (complete), 2 (complete), 3 (complete)

---

### Phase 3: Advanced Scheduling (Weeks 9-12)
**Goal**: Multi-party coordination and automation

**Capabilities to Build**:
- ✅ C1.2: Multi-calendar access
- ✅ C8.1, C8.2, C8.3, C8.4: Availability, optimization, conflicts, auto-reschedule
- ✅ C9.1, C9.2: Room discovery and booking
- ✅ C4.3: Event-driven automation

**Deliverables**:
- Complex scheduling solver
- Automatic rescheduling engine
- Resource booking integration

**Hero Prompts Enabled**: 4 (complete), 5 (complete), 6 (complete)

---

### Phase 4: Collaboration Features (Weeks 13-16)
**Goal**: Context synthesis and briefing generation

**Capabilities to Build**:
- ✅ C3.1, C3.2, C3.3, C3.4: Document, CRM, org, communication data access
- ✅ C11.1, C11.2, C11.3, C11.4: Aggregation, summarization, dossiers, context
- ✅ C6.2, C6.3, C6.4: Interest modeling, objection anticipation, responses
- ✅ C10.3, C10.4: Prep guidance, actionable insights

**Deliverables**:
- Document ingestion pipeline
- CRM integration
- Briefing generation system

**Hero Prompts Enabled**: 7 (complete), 8 (complete), 9 (complete)

---

### Phase 5: Polish & Scale (Weeks 17-20)
**Goal**: Transparency, optimization, enterprise readiness

**Capabilities to Build**:
- ✅ C12.1, C12.2, C12.3: Explanations, reasoning, confidence
- ✅ C7.3: Pattern optimization
- ✅ Performance tuning, caching, error handling

**Deliverables**:
- Explanation framework
- Performance at scale (1000+ meetings/user)
- Enterprise deployment guide

**Hero Prompts Enabled**: All 9 at production quality

---

## Capability Investment Priorities

### High ROI (Build First)
1. **C1.1 + C1.3**: Calendar read/write - Enables 40+ GUTTs
2. **C2.1 + C2.4**: NLP extraction + generation - Enables 35+ GUTTs
3. **C5.1 + C5.2**: Meeting classification + importance - Core intelligence
4. **C4.1 + C4.4**: Workflow execution + reporting - Automation foundation

### Medium ROI (Build Second)
5. **C6.1**: Priority alignment - Key differentiation
6. **C7.1 + C7.2**: Time analytics - High user value
7. **C8.1 + C8.2**: Multi-party scheduling - Complex but valuable
8. **C11.1 + C11.2**: Context synthesis - Briefing features

### Lower ROI (Build Later)
9. **C9.1 + C9.2**: Room booking - Nice-to-have
10. **C12.1**: Explanations - Important for trust but not core value
11. **C3.4**: Communication history - Advanced collaboration
12. **C6.3 + C6.4**: Objection handling - Specialized use case

---

## Technology Stack Recommendations

### Calendar & Identity
- **Microsoft Graph API**: Calendar, People, Teams, OneDrive, SharePoint
- **MSAL (Microsoft Authentication Library)**: OAuth 2.0, token management
- **Webhooks/Subscriptions**: Real-time event monitoring

### LLM & AI
- **Primary LLM**: Claude Sonnet 4.5 (GUTT analysis gold standard, 100% accuracy)
- **Backup LLM**: GPT-4o (multi-modal, cost-effective)
- **Classification**: Fine-tuned model or zero-shot with Claude/GPT-4
- **Embeddings**: text-embedding-ada-002 (OpenAI) or custom

### Data & Storage
- **Database**: PostgreSQL (structured data), Azure Cosmos DB (scale)
- **Cache**: Redis (API responses, user context)
- **Vector Store**: FAISS or Pinecone (semantic search)
- **Documents**: Azure Blob Storage, OneDrive API

### Orchestration & Integration
- **Workflow Engine**: Custom Python (simple) or Azure Logic Apps (enterprise)
- **API Gateway**: Azure API Management or custom FastAPI
- **Message Queue**: Azure Service Bus (async operations)
- **Monitoring**: Application Insights, Prometheus

### Development
- **Language**: Python 3.8+ (ML/AI ecosystem, rapid development)
- **Framework**: FastAPI (API server), Pydantic (data validation)
- **Testing**: pytest (unit), selenium (E2E for Graph Explorer automation)
- **CI/CD**: GitHub Actions, Azure DevOps

---

## Risk Assessment

### High-Risk Capabilities (Require careful implementation)

**C4.3: Event-Driven Automation**
- Risk: Race conditions, duplicate actions, cascading failures
- Mitigation: Idempotency keys, transaction logs, circuit breakers

**C8.3: Conflict Resolution**
- Risk: Infinite rescheduling loops, user frustration
- Mitigation: Max retry limits, user confirmation, undo capability

**C6.1: Priority Alignment**
- Risk: Misalignment with user intent, incorrect accept/decline
- Mitigation: Confidence thresholds, user feedback loop, explanation

**C5.1: Meeting Classification**
- Risk: Classification errors impact all downstream features
- Mitigation: High accuracy requirement (80%+), human-in-loop for critical decisions

### Data Privacy & Security

**Sensitive Data Handled**:
- Calendar events (potentially confidential meetings)
- Email and chat content
- CRM data (customer information)
- Personal preferences and priorities

**Mitigations**:
- OAuth consent and scopes (minimum necessary)
- Data encryption at rest and in transit
- Audit logging of all actions
- GDPR/CCPA compliance (data deletion, portability)
- Tenant isolation (multi-tenant SaaS)

---

## Success Metrics

### Capability-Level KPIs

| Capability | Success Metric | Target |
|------------|---------------|--------|
| C1: Calendar API | API success rate | >99.5% |
| C2: NLP | Constraint extraction accuracy | >90% |
| C5.1: Classification | Meeting type accuracy | >80% |
| C5.2: Importance | Importance alignment with user | >75% |
| C6.1: Alignment | Priority match precision | >70% |
| C8.2: Scheduling | Feasible slot found rate | >85% |
| C11.2: Summarization | Exec summary quality (user rating) | >4/5 |
| C12.1: Explanation | User understanding (survey) | >80% |

### Hero Prompt Completion Rates

| Hero Prompt | Target Success Rate | Failure Acceptable? |
|-------------|---------------------|---------------------|
| 1. Calendar Prioritization | 75% | Yes (user oversight) |
| 2. Meeting Prep Tracking | 90% | No (critical for prep) |
| 3. Time Reclamation | 70% | Yes (suggestions only) |
| 4. Recurring 1:1 | 85% | No (automation expected) |
| 5. Block Time & Reschedule | 80% | No (sequential ops) |
| 6. Multi-Person Scheduling | 60% | Yes (complex constraints) |
| 7. Agenda Creation | 75% | Yes (user edits expected) |
| 8. Executive Briefing | 80% | No (high-stakes meeting) |
| 9. Customer Meeting Prep | 85% | No (external-facing) |

---

## Conclusion

**Core Finding**: 12 foundational capability clusters and 47 specific technical capabilities required to deliver all 9 hero prompts.

**Critical Path**: 
1. Calendar API (C1) - 91% GUTT coverage
2. NLP (C2) - 79% GUTT coverage  
3. ML Classification (C5) - 53% GUTT coverage
4. Semantic Reasoning (C6) - 58% GUTT coverage

**Recommended Approach**: 
- **Phase 1-2** (8 weeks): Foundation + Intelligence → Enables prompts 1-3
- **Phase 3** (4 weeks): Advanced scheduling → Enables prompts 4-6
- **Phase 4** (4 weeks): Collaboration features → Enables prompts 7-9
- **Phase 5** (4 weeks): Polish and scale → Production readiness

**Total Effort**: 20 weeks (5 months) for complete implementation

**LLM Recommendation**: Deploy Claude Sonnet 4.5 as primary LLM for GUTT decomposition and critical reasoning tasks (100% accuracy vs 56% Ollama).

---

---

## Appendix A: C-GUTT Reference

**Note**: This document previously listed 66 original unit tasks from individual hero prompts. Those have been consolidated into **39 atomic C-GUTTs** (Consolidated Generalized Unit Task Taxonomy) which are the actual implementation targets.

For complete C-GUTT specifications, examples, and implementation guidance, see:
- **[CONSOLIDATED_GUTT_REFERENCE.md](./CONSOLIDATED_GUTT_REFERENCE.md)** - Complete inventory of all 39 C-GUTTs with detailed examples
- **[GUTT_CROSS_PROMPT_CONSOLIDATION_ANALYSIS.md](./GUTT_CROSS_PROMPT_CONSOLIDATION_ANALYSIS.md)** - Consolidation methodology showing 66→39 reduction

**Quick C-GUTT Categories**:
- **Calendar Data Operations** (7 C-GUTTs): C-01 to C-07
- **Natural Language Processing** (8 C-GUTTs): C-08 to C-15
- **Reasoning & Decision Making** (7 C-GUTTs): C-16 to C-22
- **Analysis & Insights** (5 C-GUTTs): C-23 to C-27
- **Resource Management** (3 C-GUTTs): C-28 to C-30
- **Output & Communication** (3 C-GUTTs): C-31 to C-33
- **Specialized Collaboration** (6 C-GUTTs): C-34 to C-39

**Implementation Focus**: Build the 39 C-GUTTs (not the original 66 tasks). The consolidated capabilities provide better code reuse (1.69 prompts per C-GUTT average) and clearer architectural boundaries.

---

## C-GUTT Summary Statistics

### Consolidation Overview

| Metric | Value |
|--------|-------|
| **Original Unit Tasks** | 66 (from 9 hero prompts) |
| **Consolidated C-GUTTs** | 39 atomic capabilities |
| **Reduction** | 41% fewer implementation units |
| **Average Reusability** | 1.69 prompts per C-GUTT |
| **Hero Prompts Served** | 9 (100% coverage) |

### C-GUTT Distribution by Category

| Category | C-GUTT Count | Examples |
|----------|--------------|----------|
| Calendar Data Operations | 7 | C-01 (Event Retrieval), C-02 (Multi-Calendar) |
| Natural Language Processing | 8 | C-08 (Priority Extraction), C-09 (Constraints) |
| Reasoning & Decision Making | 7 | C-16 (Alignment Scoring), C-19 (Constraint Solving) |
| Analysis & Insights | 5 | C-23 (Time Aggregation), C-24 (Low-Value Detection) |
| Resource Management | 3 | C-28 (Room Booking), C-29 (Focus Time) |
| Output & Communication | 3 | C-31 (Justification), C-32 (Reporting) |
| Specialized Collaboration | 6 | C-34 (Agenda Planning), C-37 (Research) |

### Most Reused C-GUTTs (Implementation Priority)

| C-GUTT | Capability Name | Prompts | Coverage |
|--------|----------------|---------|----------|
| **C-01** | Calendar Event Retrieval | 5 | 76% |
| **C-19** | Constraint Satisfaction & Slot Finding | 4 | 44% |
| **C-02** | Multi-Calendar Availability | 3 | 33% |
| **C-07** | Meeting Update & Rescheduling | 3 | 33% |
| **C-11** | Meeting Context Extraction | 3 | 33% |
| **C-14** | Document Content Analysis | 3 | 33% |
| **C-20** | Conflict Detection & Resolution | 3 | 33% |
| **C-32** | Reporting & Visualization | 3 | 33% |
| **C-33** | Document Assembly & Formatting | 3 | 33% |

**Key Insight**: Prioritize building high-reuse C-GUTTs first. The top 9 C-GUTTs enable 67% of all hero prompt functionality.

---

## Relationship Between Infrastructure Capabilities and C-GUTTs

This document's **47 infrastructure capabilities** provide the technical foundation for implementing the **39 atomic C-GUTTs**:

**Mapping Example**:

| Infrastructure Capability | Implements C-GUTTs | Notes |
|---------------------------|-------------------|-------|
| C1.1 Single Calendar Read | C-GUTT-01 | Calendar Event Retrieval |
| C5.1 Meeting Type Classification | C-GUTT-03 | Meeting Type (format-based) |
| C5.2 Meeting Importance Classification | C-GUTT-04 | Meeting Importance (value-based) - **distinct from type** |
| C2.1 Constraint Extraction | C-GUTT-09 | Constraint & Requirement Parsing |
| C8.2 Constraint Satisfaction Solving | C-GUTT-19 | Constraint Satisfaction & Slot Finding |

**Implementation Strategy**:
1. Build infrastructure capabilities (this document's 47 capabilities)
2. Compose them into atomic C-GUTTs (39 functional units)
3. Combine C-GUTTs to deliver hero prompts (9 user-facing features)

For detailed C-GUTT specifications with examples, see [CONSOLIDATED_GUTT_REFERENCE.md](./CONSOLIDATED_GUTT_REFERENCE.md).

---

## Appendix B: Analysis Prompt Used

**Original User Request**:
> "given this, let's your own LLM reasoning capability to come up with recommendation to an inventory of capability needed to accomplish the 9 prompts."

**Context Provided**:
- Hero Prompts Reference GUTT Decompositions (66 GUTTs across 9 prompts)
- Claude vs Ollama GUTT comparison analysis
- Existing GUTT evaluation framework documentation

**Analysis Methodology**:

The capability inventory was generated through systematic LLM reasoning:

1. **Pattern Recognition**: Analyzed all 66 GUTTs to identify recurring technical requirements
   - Grouped similar capabilities across prompts (e.g., "Calendar Event Retrieval" appears in multiple contexts)
   - Identified common infrastructure needs (API access, NLP, data processing)
   - Recognized specialized vs. foundational capabilities

2. **Bottom-Up Clustering**: Extracted atomic capabilities from GUTT descriptions
   - Each GUTT's "Skills" and "Capability" fields provided technical requirements
   - Merged related skills into coherent capability clusters
   - Example: "Calendar API integration", "event filtering", "data parsing" → C1.1 Single Calendar Read

3. **Coverage Analysis**: Calculated GUTT enablement for each capability
   - Traced which capabilities are required for each of the 66 GUTTs
   - Quantified coverage percentages (e.g., C1 Calendar API enables 60/66 GUTTs = 91%)
   - Identified critical path capabilities with highest coverage

4. **Dependency Mapping**: Established capability prerequisites and relationships
   - Tier 1 (Foundation): Must-have for any functionality
   - Tier 2 (Intelligence): Differentiates basic from advanced features
   - Tier 3 (Advanced): Enables specialized enterprise use cases

5. **Implementation Planning**: Created phased roadmap based on dependencies
   - Phase sequencing based on capability prerequisites
   - Effort estimation from complexity and scope
   - Hero prompt enablement milestones

6. **Technology Recommendations**: Selected optimal tech stack for each capability
   - Based on industry best practices and existing integrations
   - Considered Microsoft 365 ecosystem (Graph API, MSAL)
   - LLM selection informed by Claude vs Ollama analysis (100% vs 56% accuracy)

**Key Reasoning Principles**:
- **Atomic Decomposition**: Each capability represents a single, well-defined technical function
- **GUTT-Driven**: All capabilities traced back to specific GUTT requirements (no speculative features)
- **Practical Implementation**: Focus on buildable, testable, deployable capabilities
- **Dependency-Aware**: Sequencing respects technical prerequisites
- **Measurement-Oriented**: Success metrics defined for each capability

**Validation**:
- Cross-referenced with existing Scenara 2.0 codebase (meeting_classifier.py, collaborator_discovery.py, etc.)
- Aligned with GUTT v4.0 ACRUE framework principles
- Informed by real-world meeting intelligence deployment experience

This analysis demonstrates LLM reasoning capabilities for:
- **System Architecture**: Designing multi-tier capability frameworks
- **Requirement Engineering**: Extracting technical specs from user stories (GUTTs)
- **Strategic Planning**: Creating phased implementation roadmaps
- **Technology Selection**: Recommending appropriate tools and platforms

---

*This capability inventory provides the technical foundation for building enterprise meeting intelligence at scale.*
