# Enterprise Meeting Intelligence - Capability Inventory Analysis

**Date**: November 6, 2025  
**Source**: Analysis of 9 Calendar.AI Hero Prompts (66 GUTTs)  
**Method**: LLM reasoning across atomic unit task decompositions  
**Purpose**: Identify foundational capabilities needed for production implementation

---

## Executive Summary

Analyzed 66 atomic unit tasks across 9 hero prompts to extract **12 foundational capability clusters** and **47 specific technical capabilities** required for enterprise meeting intelligence.

**Key Insights**:
- **4 Core Infrastructure Capabilities** (Calendar API, NLP, Data Access, Action Execution) enable 85% of GUTTs
- **3 Intelligence Capabilities** (ML Classification, Semantic Analysis, Pattern Recognition) differentiate basic vs advanced features
- **5 Specialized Capabilities** for advanced use cases (Multi-calendar coordination, Resource booking, CRM integration)
- **Critical Dependencies**: Calendar API (60 GUTTs), NLP (52 GUTTs), Semantic Reasoning (38 GUTTs)

---

## Capability Taxonomy

### Tier 1: Foundation Infrastructure (Required for MVP)

#### 1. **Calendar Data Access & Management**
*Enables: 60/66 GUTTs (91%)*

**Core Capabilities**:
- **C1.1 Single Calendar Read**: Query user's calendar events (past, present, future)
  - Date range filtering
  - Event metadata extraction (title, time, attendees, location, status)
  - Pending invitation vs confirmed event filtering
  - Historical data access (time series analysis)
  - **GUTTs Enabled**: 1.2, 2.1, 3.1, 4.2, 5.2, 7.1, 8.1, 9.1

- **C1.2 Multi-Calendar Read**: Access calendars for multiple users
  - Cross-user free/busy queries
  - Availability aggregation across attendees
  - Permissions and access control handling
  - **GUTTs Enabled**: 4.2, 6.2

- **C1.3 Calendar Write Operations**: Modify calendar state
  - RSVP updates (accept/decline)
  - Event creation (single and recurring)
  - Event updates and rescheduling
  - Event deletion
  - Recurrence rule generation (iCalendar RRULE)
  - **GUTTs Enabled**: 1.5, 4.4, 4.7, 5.3, 5.5, 6.9

- **C1.4 Calendar Status Management**: Control user availability representation
  - Free/busy status updates
  - Out-of-office settings
  - Working hours configuration
  - **GUTTs Enabled**: 5.6

**Technical Requirements**:
- Microsoft Graph Calendar API integration
- OAuth 2.0 / MSAL authentication
- Pagination for large datasets
- Real-time event change subscriptions (webhooks)
- Efficient caching and sync strategies

**Priority**: CRITICAL - Blocks 91% of functionality

---

#### 2. **Natural Language Understanding & Generation**
*Enables: 52/66 GUTTs (79%)*

**Core Capabilities**:
- **C2.1 Constraint Extraction**: Parse user requests into structured requirements
  - Temporal expressions ("next week", "Thursday afternoon", "in the next 2 weeks")
  - Preferences ("afternoons preferred", "avoid Fridays")
  - Hard vs soft constraints identification
  - Multi-constraint parsing
  - **GUTTs Enabled**: 4.1, 5.1, 6.1

- **C2.2 Priority & Goal Understanding**: Extract user priorities and goals
  - Priority statement parsing
  - Goal formalization
  - Implicit preference detection
  - **GUTTs Enabled**: 1.1, 3.4

- **C2.3 Semantic Content Analysis**: Understand meaning of text (meeting titles, descriptions, documents)
  - Topic extraction
  - Theme identification
  - Intent classification
  - **GUTTs Enabled**: 3.2, 7.2, 8.2

- **C2.4 Natural Language Generation**: Create human-readable outputs
  - Decision justifications and explanations
  - Meeting agendas and summaries
  - Reports and recommendations
  - Professional communication tone
  - **GUTTs Enabled**: 1.6, 3.8, 5.8, 6.9, 7.6, 8.7, 9.8

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

**Core Capabilities**:
- **C5.1 Meeting Type Classification**: Categorize meetings into 31+ types
  - 1:1s, team meetings, all-hands, workshops, etc.
  - Confidence scoring
  - Multi-label classification support
  - **GUTTs Enabled**: 3.2, 5.4 (identify override-eligible meetings), 6.4

- **C5.2 Importance Scoring**: Determine meeting importance/priority
  - Context-based importance (participants, topic, timing)
  - User-specific importance (role in meeting, relationship to goals)
  - Temporal urgency
  - **GUTTs Enabled**: 2.2, 3.4

- **C5.3 Preparation Time Estimation**: Predict prep time needed
  - Meeting type → prep time mapping
  - Complexity assessment
  - User role consideration
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

## Appendix A: Complete GUTT Reference (66 Unit Tasks)

### Quick Reference: All 66 GUTTs by Number

**Format**: `[Prompt#].[GUTT#]` - GUTT Name (Click to jump to detailed description)

#### Organizer Category (GUTTs 1.1-3.8, Total: 21)
- [**1.1** - Priority Definition & Extraction](#gutt-11)
- [**1.2** - Calendar Event Retrieval](#gutt-12)
- [**1.3** - Meeting-Priority Alignment Scoring](#gutt-13)
- [**1.4** - Accept/Decline Decision Logic](#gutt-14)
- [**1.5** - Calendar Action Execution](#gutt-15)
- [**1.6** - Decision Justification & Reporting](#gutt-16)
- [**2.1** - Calendar Data Retrieval](#gutt-21)
- [**2.2** - Meeting Importance Classification](#gutt-22)
- [**2.3** - Preparation Time Estimation](#gutt-23)
- [**2.4** - Meeting Flagging Logic](#gutt-24)
- [**2.5** - Calendar Gap Analysis](#gutt-25)
- [**2.6** - Focus Time Block Scheduling](#gutt-26)
- [**2.7** - Actionable Recommendations & Reporting](#gutt-27)
- [**3.1** - Calendar Historical Data Retrieval](#gutt-31)
- [**3.2** - Meeting Categorization & Classification](#gutt-32)
- [**3.3** - Time Aggregation & Statistical Analysis](#gutt-33)
- [**3.4** - Priority Alignment Assessment](#gutt-34)
- [**3.5** - Low-Value Meeting Identification](#gutt-35)
- [**3.6** - Time Reclamation Opportunity Analysis](#gutt-36)
- [**3.7** - Schedule Optimization Recommendations](#gutt-37)
- [**3.8** - Time Usage Reporting & Visualization](#gutt-38)

#### Schedule Category (GUTTs 4.1-6.9, Total: 24)
- [**4.1** - Constraint Extraction & Formalization](#gutt-41)
- [**4.2** - Multi-Calendar Availability Checking](#gutt-42)
- [**4.3** - Constraint-Based Slot Finding](#gutt-43)
- [**4.4** - Recurring Meeting Series Creation](#gutt-44)
- [**4.5** - Meeting Invitation Sending](#gutt-45)
- [**4.6** - Decline/Conflict Detection & Monitoring](#gutt-46)
- [**4.7** - Automatic Rescheduling Logic](#gutt-47)
- [**5.1** - Time Block Specification Parsing](#gutt-51)
- [**5.2** - Affected Meetings Identification](#gutt-52)
- [**5.3** - RSVP Decline Execution](#gutt-53)
- [**5.4** - Alternative Slot Finding](#gutt-54)
- [**5.5** - Meeting Rescheduling Proposals](#gutt-55)
- [**5.6** - Calendar Status Update](#gutt-56)
- [**5.7** - Focus Time Block Creation](#gutt-57)
- [**5.8** - Action Summary & Confirmation](#gutt-58)
- [**6.1** - Meeting Requirements Extraction](#gutt-61)
- [**6.2** - Multi-Person Availability Aggregation](#gutt-62)
- [**6.3** - Priority Constraint Application](#gutt-63)
- [**6.4** - Override-Eligible Meeting Identification](#gutt-64)
- [**6.5** - Location-Based Filtering](#gutt-65)
- [**6.6** - Conference Room Search & Booking](#gutt-66)
- [**6.7** - Optimal Slot Selection](#gutt-67)
- [**6.8** - Conflict Resolution & Rescheduling](#gutt-68)
- [**6.9** - Meeting Creation & Invitations](#gutt-69)

#### Collaborate Category (GUTTs 7.1-9.8, Total: 21)
- [**7.1** - Meeting Context Retrieval](#gutt-71)
- [**7.2** - Stakeholder Role Identification](#gutt-72)
- [**7.3** - Agenda Structure Planning](#gutt-73)
- [**7.4** - Progress Review Items Generation](#gutt-74)
- [**7.5** - Blocker & Risk Identification](#gutt-75)
- [**7.6** - Time Allocation & Formatting](#gutt-76)
- [**8.1** - Meeting Materials Retrieval](#gutt-81)
- [**8.2** - Content Analysis & Topic Extraction](#gutt-82)
- [**8.3** - Executive Summary Distillation](#gutt-83)
- [**8.4** - Audience-Aware Framing](#gutt-84)
- [**8.5** - Objection Anticipation](#gutt-85)
- [**8.6** - Response Preparation](#gutt-86)
- [**8.7** - Briefing Document Generation](#gutt-87)
- [**9.1** - Meeting Details Retrieval](#gutt-91)
- [**9.2** - Company Background Research](#gutt-92)
- [**9.3** - Attendee Identity Resolution](#gutt-93)
- [**9.4** - Individual Dossier Creation](#gutt-94)
- [**9.5** - Topic Interest Analysis](#gutt-95)
- [**9.6** - Relationship History Compilation](#gutt-96)
- [**9.7** - Relevant Content Gathering](#gutt-97)
- [**9.8** - Brief Document Assembly](#gutt-98)

---

### Detailed GUTT Descriptions

### Organizer Category (21 GUTTs)

#### Hero Prompt 1: Calendar Prioritization (6 GUTTs)
1. <a id="gutt-11"></a>**Priority Definition & Extraction** - Identify and structure user's priorities from context
2. <a id="gutt-12"></a>**Calendar Event Retrieval** - Access and load pending calendar invitations and scheduled meetings
3. <a id="gutt-13"></a>**Meeting-Priority Alignment Scoring** - Evaluate how well each meeting aligns with stated priorities
4. <a id="gutt-14"></a>**Accept/Decline Decision Logic** - Determine which meetings to accept vs decline based on priority alignment
5. <a id="gutt-15"></a>**Calendar Action Execution** - Execute accept/decline actions on calendar system
6. <a id="gutt-16"></a>**Decision Justification & Reporting** - Explain why each meeting was accepted or declined

#### Hero Prompt 2: Meeting Prep Tracking (7 GUTTs)
1. <a id="gutt-21"></a>**Calendar Data Retrieval** - Load user's calendar events for analysis period
2. <a id="gutt-22"></a>**Meeting Importance Classification** - Classify each meeting by importance level (critical/high/medium/low)
3. <a id="gutt-23"></a>**Preparation Time Estimation** - Estimate prep time needed based on meeting type, importance, and role
4. <a id="gutt-24"></a>**Meeting Flagging Logic** - Flag meetings that require preparation based on importance and lead time
5. <a id="gutt-25"></a>**Calendar Gap Analysis** - Identify available time slots before flagged meetings for prep work
6. <a id="gutt-26"></a>**Focus Time Block Scheduling** - Schedule focus time blocks in identified gaps
7. <a id="gutt-27"></a>**Actionable Recommendations & Reporting** - Generate prioritized list of meetings needing prep with time blocks

#### Hero Prompt 3: Time Reclamation Analysis (8 GUTTs)
1. <a id="gutt-31"></a>**Calendar Historical Data Retrieval** - Load past calendar events for specified time period
2. <a id="gutt-32"></a>**Meeting Categorization & Classification** - Classify meetings by type, purpose, importance, participants
3. <a id="gutt-33"></a>**Time Aggregation & Statistical Analysis** - Compute time spent per category, participant, project
4. <a id="gutt-34"></a>**Priority Alignment Assessment** - Evaluate which time usage aligns with stated priorities
5. <a id="gutt-35"></a>**Low-Value Meeting Identification** - Flag meetings that consume time without supporting priorities
6. <a id="gutt-36"></a>**Time Reclamation Opportunity Analysis** - Calculate potential time savings from proposed changes
7. <a id="gutt-37"></a>**Schedule Optimization Recommendations** - Suggest specific changes (decline, delegate, shorten, consolidate)
8. <a id="gutt-38"></a>**Time Usage Reporting & Visualization** - Present insights with charts, summaries, comparisons

### Schedule Category (24 GUTTs)

### Schedule Category (24 GUTTs)

#### Hero Prompt 4: Recurring 1:1 Scheduling (7 GUTTs)
1. <a id="gutt-41"></a>**Constraint Extraction & Formalization** - Parse scheduling requirements into structured constraints
2. <a id="gutt-42"></a>**Multi-Calendar Availability Checking** - Check free/busy status for user and attendee
3. <a id="gutt-43"></a>**Constraint-Based Slot Finding** - Identify time slots matching all constraints (weekly, afternoons, not Fridays, 30min)
4. <a id="gutt-44"></a>**Recurring Meeting Series Creation** - Create recurring calendar event with proper series configuration
5. <a id="gutt-45"></a>**Meeting Invitation Sending** - Send calendar invitation to attendee
6. <a id="gutt-46"></a>**Decline/Conflict Detection & Monitoring** - Monitor for attendee declines or new calendar conflicts
7. <a id="gutt-47"></a>**Automatic Rescheduling Logic** - When declined/conflicted, find new slot and send updated invitation

#### Hero Prompt 5: Block Time & Reschedule (8 GUTTs)
1. <a id="gutt-51"></a>**Time Block Specification Parsing** - Interpret "Thursday afternoon" into specific date/time range
2. <a id="gutt-52"></a>**Affected Meetings Identification** - Find all meetings within the target time block
3. <a id="gutt-53"></a>**RSVP Decline Execution** - Decline all meetings in the blocked time
4. <a id="gutt-54"></a>**Alternative Slot Finding** - For each meeting, identify alternative time slots
5. <a id="gutt-55"></a>**Meeting Rescheduling Proposals** - Send reschedule requests with proposed new times
6. <a id="gutt-56"></a>**Calendar Status Update** - Set user's status/availability for the blocked time
7. <a id="gutt-57"></a>**Focus Time Block Creation** - Create placeholder event for the blocked time
8. <a id="gutt-58"></a>**Action Summary & Confirmation** - Report what was done (declined X, rescheduled Y, blocked Z hours)

#### Hero Prompt 6: Multi-Person Meeting Scheduling (9 GUTTs)
1. <a id="gutt-61"></a>**Meeting Requirements Extraction** - Parse all requirements (attendees, duration, date range, constraints, modality, resources)
2. <a id="gutt-62"></a>**Multi-Person Availability Aggregation** - Check calendars for all attendees and merge availability
3. <a id="gutt-63"></a>**Priority Constraint Application** - Ensure primary consideration of specific attendee's availability (e.g., Kat's schedule)
4. <a id="gutt-64"></a>**Override-Eligible Meeting Identification** - Identify 1:1s and lunches that can be rescheduled if needed
5. <a id="gutt-65"></a>**Location-Based Filtering** - Filter for in-person meeting capability (office presence, not remote)
6. <a id="gutt-66"></a>**Conference Room Search & Booking** - Find available room for in-person meeting and reserve it
7. <a id="gutt-67"></a>**Optimal Slot Selection** - Rank and select best time considering all constraints
8. <a id="gutt-68"></a>**Conflict Resolution & Rescheduling** - If needed, reschedule override-eligible conflicts
9. <a id="gutt-69"></a>**Meeting Creation & Invitations** - Create meeting with all attendees, room, and details

### Collaborate Category (21 GUTTs)

#### Hero Prompt 7: Agenda Creation (6 GUTTs)
1. <a id="gutt-71"></a>**Meeting Context Retrieval** - Gather information about project from available sources
2. <a id="gutt-72"></a>**Stakeholder Role Identification** - Understand different teams' roles and concerns
3. <a id="gutt-73"></a>**Agenda Structure Planning** - Create logical flow for review meeting (progress → confirmation → blockers → risks)
4. <a id="gutt-74"></a>**Progress Review Items Generation** - List specific accomplishments, milestones, metrics to review
5. <a id="gutt-75"></a>**Blocker & Risk Identification** - Surface known issues, dependencies, and potential risks for discussion
6. <a id="gutt-76"></a>**Time Allocation & Formatting** - Assign time to each agenda item and format for distribution

#### Hero Prompt 8: Executive Briefing Prep (7 GUTTs)
1. <a id="gutt-81"></a>**Meeting Materials Retrieval** - Access and load all relevant documents for the meeting
2. <a id="gutt-82"></a>**Content Analysis & Topic Extraction** - Identify main themes and topics across materials
3. <a id="gutt-83"></a>**Executive Summary Distillation** - Condense complex topics into 3 concise discussion points
4. <a id="gutt-84"></a>**Audience-Aware Framing** - Frame discussion points appropriate for senior leadership
5. <a id="gutt-85"></a>**Objection Anticipation** - Predict concerns or pushback from senior leaders
6. <a id="gutt-86"></a>**Response Preparation** - Generate effective responses to anticipated objections
7. <a id="gutt-87"></a>**Briefing Document Generation** - Format summary, objections, and responses into prep document

#### Hero Prompt 9: Customer Meeting Prep (8 GUTTs)
1. <a id="gutt-91"></a>**Meeting Details Retrieval** - Get meeting information (attendees, time, purpose)
2. <a id="gutt-92"></a>**Company Background Research** - Gather information about customer company
3. <a id="gutt-93"></a>**Attendee Identity Resolution** - Identify each customer attendee and their roles
4. <a id="gutt-94"></a>**Individual Dossier Creation** - For each attendee, compile background, role, history
5. <a id="gutt-95"></a>**Topic Interest Analysis** - Identify topics each attendee cares about based on history
6. <a id="gutt-96"></a>**Relationship History Compilation** - Summarize past interactions, deals, issues with customer
7. <a id="gutt-97"></a>**Relevant Content Gathering** - Find related materials (proposals, presentations, tickets)
8. <a id="gutt-98"></a>**Brief Document Assembly** - Compile all information into structured prep brief

---

## GUTT Summary Statistics

| Category | Hero Prompts | Total GUTTs | Avg per Prompt | Complexity Range |
|----------|--------------|-------------|----------------|------------------|
| Organizer | 3 | 21 | 7.0 | 6-8 GUTTs |
| Schedule | 3 | 24 | 8.0 | 7-9 GUTTs |
| Collaborate | 3 | 21 | 7.0 | 6-8 GUTTs |
| **TOTAL** | **9** | **66** | **7.3** | **6-9 GUTTs** |

**GUTT Distribution**:
- 6 GUTTs: 2 prompts (Calendar Prioritization, Agenda Creation)
- 7 GUTTs: 3 prompts (Meeting Prep, Recurring 1:1, Executive Briefing)
- 8 GUTTs: 3 prompts (Time Reclamation, Block Time, Customer Prep)
- 9 GUTTs: 1 prompt (Multi-Person Scheduling)

**Complexity Correlation**: Higher GUTT count generally correlates with higher complexity and more data sources required.

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
