# Hero Prompts Canonical Task Analysis - Gold Standard Reference

**Document Version**: 1.0  
**Date**: November 7, 2025  
**Author**: Chin-Yew Lin  
**Framework**: Calendar.AI Canonical Unit Tasks Framework v2.0 (24 tasks)

**Related Documents**:
- [GPT5_OPTIMIZATION_SUMMARY.md](model_comparison/GPT5_OPTIMIZATION_SUMMARY.md) - GPT-5 3-trial stability test
- [CONSOLIDATED_GUTT_REFERENCE.md](CONSOLIDATED_GUTT_REFERENCE.md) - Complete canonical tasks specifications
- [Hero_Prompts_Reference_GUTT_Decompositions.md](Hero_Prompts_Reference_GUTT_Decompositions.md) - Original GUTT decompositions

---

## Document Summary

### Purpose

This document provides the **gold standard canonical task analysis** for the 9 Calendar.AI hero prompts, serving as the authoritative reference for:

1. **LLM Evaluation**: Benchmark model performance in task decomposition
2. **Framework Validation**: Validate the 24 canonical unit tasks framework
3. **Training Data**: Ground truth for fine-tuning and prompt optimization
4. **Quality Assurance**: Reference standard for production system validation

### Methodology

This gold standard was created through a rigorous 4-phase process:

#### Phase 1: Initial Framework Development (Oct-Nov 2025)
- **Original GUTT Analysis**: Manual decomposition of 9 hero prompts into 66 capabilities
- **Cross-Prompt Consolidation**: Identified common patterns, reduced to 39 atomic capabilities (C-GUTT)
- **Framework Evolution**: Refined into 24 canonical unit tasks with clear boundaries

#### Phase 2: GPT-5 Baseline Analysis (Nov 6, 2025)
- **Automated Analysis**: GPT-5 analyzed all 9 hero prompts using initial prompts
- **Performance**: F1 79.74% baseline, but gaps in specialized task detection
- **Key Findings**: 
  - CAN-07 (Metadata Extraction): Only 55.6% detection rate (5/9 prompts)
  - CAN-23 (Conflict Resolution): 0% detection rate (0/9 prompts)
  - CAN-22 (Work Attribution): Only 11% detection rate (1/9 prompts)

#### Phase 3: Prompt Optimization & Validation (Nov 7, 2025)
- **Optimization**: Enhanced GPT-5 prompts with 6 critical task concepts
  1. CAN-07 parent task guidance with explicit keywords
  2. CAN-02A vs CAN-02B differentiation (type vs importance)
  3. CAN-13 vs CAN-07 read/write distinction
  4. Specialized task keywords (CAN-18, CAN-20, CAN-23)
  5. DO/DON'T guidelines (9 total)
  6. Dependency chain clarification
  
- **3-Trial Stability Test**: 27 API calls (3 trials × 9 prompts)
  - **Average Performance**: F1 78.40% ± 0.72% (EXCELLENT < 1% variance)
  - **CAN-07 Detection**: 100% (9/9 prompts, +44.4% improvement)
  - **CAN-23 Detection**: 66.7% (6/9 prompts, +66.7% improvement)
  - **CAN-22 Detection**: 100% in collaborate prompts (+89% improvement)
  - **Consistency**: 93.6% task selection agreement across trials

#### Phase 4: Human Correction & Gold Standard Creation (Nov 7, 2025)
- **Manual Review**: Human expert (Chin-Yew Lin) reviewed GPT-5 optimized outputs
- **Corrections Applied**:
  - Ensured all 24 canonical tasks represented across prompts
  - Added missing CAN-04 (NLU) to prompts where omitted
  - Split CAN-02 into CAN-02A (Type) and CAN-02B (Importance) consistently
  - Added CAN-07 (Metadata Extraction) where "pending invitations" appeared
  - Added orchestrated workflows: CAN-17 (Auto-Rescheduling), CAN-23 (Conflict Resolution)
  - Added optional enhancements: CAN-18 (Risk Anticipation), CAN-20 (Visualization)
- **Validation**: Cross-referenced with original GUTT decompositions
- **Final Output**: This gold standard reference document

### Gold Standard Statistics

| Metric | Value |
|--------|-------|
| **Total Prompts** | 9 |
| **Total Canonical Tasks** | 24 (23 unique + CAN-02A/CAN-02B split) |
| **Tasks Used** | 23 (all tasks represented except 1) |
| **Average Tasks/Prompt** | 7.8 |
| **Tier 1 (Universal) Coverage** | 100% |
| **Tier 2 (Common) Coverage** | 95% |
| **Tier 3 (Specialized) Coverage** | 71% |

### Task Frequency Distribution

| Task ID | Task Name | Frequency | Prompts |
|---------|-----------|-----------|---------|
| **CAN-04** | Natural Language Understanding | 100% | 9/9 |
| **CAN-01** | Calendar Events Retrieval | 100% | 9/9 |
| **CAN-02A** | Meeting Type Classification | 89% | 8/9 |
| **CAN-02B** | Meeting Importance Assessment | 78% | 7/9 |
| **CAN-07** | Meeting Metadata Extraction | 100% | 9/9 |
| **CAN-03** | Scheduling Constraint Analysis | 44% | 4/9 |
| **CAN-05** | Meeting Attendees Analysis | 56% | 5/9 |
| **CAN-06** | Availability Checking | 44% | 4/9 |
| **CAN-08** | Meeting Documentation Retrieval | 44% | 4/9 |
| **CAN-09** | Content Generation | 56% | 5/9 |
| **CAN-10** | Meeting Summarization | 33% | 3/9 |
| **CAN-11** | Time Block Scheduling | 22% | 2/9 |
| **CAN-12** | Constraint Satisfaction | 33% | 3/9 |
| **CAN-13** | RSVP Status Update | 44% | 4/9 |
| **CAN-14** | Meeting Insights & Recommendations | 67% | 6/9 |
| **CAN-15** | Time Zone Management | 11% | 1/9 |
| **CAN-16** | Recurring Patterns Detection | 11% | 1/9 |
| **CAN-17** | Automatic Rescheduling | 11% | 1/9 |
| **CAN-18** | Objection/Risk Anticipation | 11% | 1/9 |
| **CAN-19** | Meeting Resources Management | 11% | 1/9 |
| **CAN-20** | Data Visualization | 22% | 2/9 |
| **CAN-21** | Task Duration Estimation | 22% | 2/9 |
| **CAN-22** | Work Attribution Discovery | 33% | 3/9 |
| **CAN-23** | Conflict Resolution | 22% | 2/9 |

---

## Hero Prompt 1: Priority-Based Invitation Management (organizer-1)

**Prompt**: "Show me my pending invitations and which ones I should prioritize based on my priorities for this week: customer meetings and product strategy."

**Capabilities Required**: Priority reasoning, invitation filtering, meeting type classification, importance assessment, decision support

### Canonical Task Decomposition: **8 Tasks**

#### Task 1: Natural Language Understanding (CAN-04)
- **Purpose**: Extract user priorities and time constraints from the prompt
- **Input**: User query with priorities and time window
- **Output**: Structured priorities ["customer meetings", "product strategy"], time_window "this week"
- **Tier**: Universal (Tier 1)

#### Task 2: Calendar Events Retrieval (CAN-01)
- **Purpose**: Retrieve all pending calendar invitations for the current week
- **Input**: Time range (this week), status filter ["pending", "tentative"]
- **Output**: Array of calendar events with pending RSVP status
- **Tier**: Universal (Tier 1)

#### Task 3: Meeting Type Classification (CAN-02A)
- **Purpose**: Classify each pending invitation by meeting type
- **Input**: Calendar events with meeting metadata
- **Output**: Meeting type labels (1:1, customer meeting, internal team, product strategy, etc.)
- **Tier**: Universal (Tier 1)
- **Note**: OBJECTIVE classification based on format/structure

#### Task 4: Meeting Importance Assessment (CAN-02B)
- **Purpose**: Assess strategic importance of each meeting relative to user priorities
- **Input**: Meeting metadata + user priorities
- **Output**: Importance scores/ratings aligned with "customer meetings" and "product strategy"
- **Tier**: Universal (Tier 1)
- **Note**: SUBJECTIVE assessment based on strategic value

#### Task 5: Meeting Metadata Extraction (CAN-07)
- **Purpose**: Extract detailed metadata from pending invitations (attendees, agenda, organizer)
- **Input**: Raw calendar event data
- **Output**: Structured metadata (attendees list, meeting agenda, RSVP status, attachments)
- **Tier**: Common (Tier 2)
- **Note**: PARENT task - enables CAN-05, CAN-13

#### Task 6: Meeting Attendees Analysis (CAN-05)
- **Purpose**: Analyze attendee composition to identify customer vs internal participants
- **Input**: Attendees list from CAN-07
- **Output**: Attendee categorization (customer, internal, executive, etc.)
- **Tier**: Universal (Tier 1)
- **Dependencies**: Requires CAN-07 (Metadata Extraction)

#### Task 7: Meeting Insights & Recommendations (CAN-14)
- **Purpose**: Generate prioritization recommendations based on alignment scores
- **Input**: Meeting type (CAN-02A), importance (CAN-02B), attendee analysis (CAN-05)
- **Output**: Priority rankings with justifications ("High priority: Customer meeting with key stakeholder")
- **Tier**: Common (Tier 2)

#### Task 8: RSVP Status Update (CAN-13)
- **Purpose**: Update RSVP status based on prioritization decisions (optional automation)
- **Input**: Priority recommendations from CAN-14
- **Output**: Calendar API write operations to accept/decline/tentative
- **Tier**: Common (Tier 2)
- **Dependencies**: Requires CAN-07 (Metadata Extraction)
- **Note**: WRITE operation (vs CAN-07 READ operation)

**Evaluation Criteria**:
- Prioritization accuracy vs user-defined priorities
- Meeting type classification precision
- Justification quality linking recommendations to priorities

### Execution Composition

**How Tasks Work Together to Answer the Prompt:**

```
STEP 1: Understand User Intent
CAN-04 (NLU) → Extract: "pending invitations", "prioritize", priorities ["customer meetings", "product strategy"], timeframe ["this week"]

STEP 2: Retrieve Data
CAN-01 (Calendar Retrieval) → Load pending invitations for current week
CAN-07 (Metadata Extraction) → Extract RSVP status, attendees, agenda from each invitation

STEP 3: Classify & Analyze Meetings
CAN-02A (Meeting Type) → Classify each as: 1:1, customer meeting, internal team, product strategy, etc.
CAN-02B (Meeting Importance) → Score importance relative to user priorities
CAN-05 (Attendees Analysis) → Identify customer vs internal participants, executive presence

STEP 4: Generate Recommendations
CAN-14 (Insights & Recommendations) → 
  - Match meetings to priorities ("customer meetings", "product strategy")
  - Rank by alignment score
  - Generate justifications ("High priority: Customer meeting with VP from Key Account - aligns with 'customer meetings' priority")

STEP 5: Execute Actions (Optional)
CAN-13 (RSVP Update) → Auto-accept high-priority matches, decline/tentative others

OUTPUT: Prioritized list of pending invitations with:
  - Which ones to prioritize (sorted by alignment)
  - Why each is recommended (justification linked to priorities)
  - Suggested RSVP actions (accept/decline/tentative)
```

**Key Orchestration Patterns**:
- **Parallel Execution**: CAN-02A, CAN-02B, CAN-05 can analyze same meeting concurrently
- **Parent-Child**: CAN-07 must complete before CAN-05, CAN-13
- **Sequential**: CAN-04 → CAN-01 → CAN-07 → CAN-14 (linear dependency)
- **Decision Point**: CAN-14 recommendations feed optional CAN-13 automation

**Example Flow for One Invitation**:
```
Input: "Meeting with Contoso VP - Q4 Strategy Discussion"

CAN-04: Extract intent ✓
CAN-01: Retrieved as pending invitation ✓
CAN-07: Metadata → Attendees: [VP from Contoso, User], Agenda: "Q4 roadmap alignment"
CAN-02A: Type = "Customer Meeting" ✓
CAN-02B: Importance = "High" (exec + customer + strategy topic) ✓
CAN-05: Attendees = [1 customer exec, 1 internal] → Customer-facing ✓
CAN-14: Recommendation = "HIGH PRIORITY - Aligns with 'customer meetings' AND 'product strategy' priorities. VP-level strategic discussion."
CAN-13: Action = Accept (if auto-enabled)

Output: "PRIORITIZE - Customer meeting with executive, matches both your priorities"
```

---

## Hero Prompt 2: Meeting Prep Tracking (organizer-2)

**Prompt**: "Track all my important meetings and flag any that require focus time to prepare for them."

**Capabilities Required**: Meeting importance detection, preparation time estimation, calendar gap analysis, focus time scheduling

### Canonical Task Decomposition: **9 Tasks**

#### Task 1: Natural Language Understanding (CAN-04)
- **Purpose**: Extract user intent to identify "important meetings" and "prep time" requirements
- **Input**: User query requesting importance tracking and prep time flagging
- **Output**: Intent classification (track + flag), prep time requirement detected
- **Tier**: Universal (Tier 1)

#### Task 2: Calendar Events Retrieval (CAN-01)
- **Purpose**: Retrieve all upcoming meetings within planning horizon
- **Input**: Time range (next 2-4 weeks typical for prep planning)
- **Output**: Array of scheduled calendar events
- **Tier**: Universal (Tier 1)

#### Task 3: Meeting Type Classification (CAN-02A)
- **Purpose**: Classify meetings by type to identify high-stakes formats
- **Input**: Calendar events with metadata
- **Output**: Meeting type labels (board meeting, customer presentation, all-hands, etc.)
- **Tier**: Universal (Tier 1)

#### Task 4: Meeting Importance Assessment (CAN-02B)
- **Purpose**: Identify which meetings qualify as "important" based on criteria
- **Input**: Meeting metadata, attendees, type
- **Output**: Importance scores/flags ("critical", "important", "routine")
- **Tier**: Universal (Tier 1)
- **Criteria**: Executive attendance, customer-facing, strategic impact, high attendee count

#### Task 5: Meeting Metadata Extraction (CAN-07)
- **Purpose**: Extract meeting details to assess prep requirements
- **Input**: Raw calendar event data
- **Output**: Agenda, attachments, meeting notes, organizer, attendees
- **Tier**: Common (Tier 2)
- **Note**: PARENT task - enables CAN-08, CAN-21

#### Task 6: Meeting Documentation Retrieval (CAN-08)
- **Purpose**: Retrieve related documents, agendas, previous meeting notes
- **Input**: Meeting ID, references from CAN-07
- **Output**: Linked documents, agendas, prep materials
- **Tier**: Common (Tier 2)
- **Dependencies**: Requires CAN-07 (Metadata Extraction)

#### Task 7: Task Duration Estimation (CAN-21)
- **Purpose**: Estimate how much prep time is needed for each important meeting
- **Input**: Meeting type (CAN-02A), importance (CAN-02B), documentation (CAN-08)
- **Output**: Estimated prep time (30 min, 1 hour, 2 hours, etc.)
- **Tier**: Common (Tier 2)
- **Dependencies**: Requires CAN-07 (Metadata Extraction)

#### Task 8: Availability Checking (CAN-06)
- **Purpose**: Analyze calendar gaps to find available slots before important meetings
- **Input**: Calendar events from CAN-01, prep time estimates from CAN-21
- **Output**: Available time slots suitable for focus time
- **Tier**: Common (Tier 2)
- **Dependencies**: Requires CAN-01 (Calendar Retrieval)

#### Task 9: Time Block Scheduling (CAN-11)
- **Purpose**: Schedule focus time blocks before flagged meetings
- **Input**: Available slots from CAN-06, prep time requirements from CAN-21
- **Output**: Calendar blocks scheduled for preparation ("Focus: Prep for Board Meeting")
- **Tier**: Common (Tier 2)
- **Note**: Automatic or suggested scheduling based on user preference

**Evaluation Criteria**:
- "Important meeting" identification accuracy (precision/recall)
- Prep time estimation quality (vs actual time needed)
- Lead time coverage (% of important meetings with adequate prep time scheduled)

### Execution Composition

**How Tasks Work Together to Answer the Prompt:**

```
STEP 1: Understand User Intent
CAN-04 (NLU) → Extract: "important meetings", "prep time", "flag if lacking time"

STEP 2: Retrieve Calendar
CAN-01 (Calendar Retrieval) → Load upcoming meetings (next 2-4 weeks)

STEP 3: Identify Important Meetings
CAN-02A (Meeting Type) → Classify: board meetings, customer presentations, exec reviews, all-hands
CAN-02B (Meeting Importance) → Score importance based on:
  - Executive attendance (VP+)
  - Customer-facing
  - Strategic impact
  - High attendee count (>20 people)
  - Meeting type (board > customer > internal)

CAN-07 (Metadata Extraction) → Extract agendas, attachments, organizer notes

STEP 4: Assess Preparation Needs
CAN-08 (Related Documents) → Find prep materials:
  - Presentation decks attached to invite
  - Pre-read documents in email
  - Previous meeting notes on same topic
  - Background materials from organizer

CAN-21 (Prep Time Estimation) → Calculate required prep time:
  - Board meeting with no agenda → 2 hours
  - Customer presentation with deck → 1 hour (review + rehearse)
  - All-hands with pre-read → 30 minutes
  - Recurring exec review → 45 minutes (update metrics)

STEP 5: Find Available Time
CAN-06 (Availability Checking) → Scan calendar for gaps before each important meeting:
  - Must be before the meeting
  - Must match prep time duration
  - Prefer 1-2 days lead time (not day-of)

STEP 6: Schedule or Flag
CAN-11 (Time Block Scheduling) → For each important meeting:
  - If available slot found → Schedule "Focus: Prep for [Meeting]"
  - If NO slot available → FLAG "⚠️ Missing prep time for [Meeting]"

OUTPUT: List showing:
  - Which meetings are important (with criteria)
  - Prep time required for each
  - Which have prep time scheduled ✓
  - Which are FLAGGED for lack of prep time ⚠️
```

**Key Orchestration Patterns**:
- **Importance Filter**: CAN-02A + CAN-02B act as filter - only process meetings that qualify
- **Parallel Enrichment**: CAN-08 and CAN-21 enrich each important meeting
- **Sequential Dependency**: CAN-07 → CAN-08, CAN-21 (need metadata to find docs and estimate time)
- **Gap Analysis**: CAN-06 scans for available slots between CAN-01 events
- **Decision Logic**: CAN-11 compares available slots (CAN-06) vs requirements (CAN-21) → schedule or flag

**Example Flow for One Meeting**:
```
Input: "Board Meeting - Q4 Business Review" (Friday 9am, 2 hours)

CAN-04: Extract intent ✓
CAN-01: Retrieved as scheduled meeting ✓
CAN-02A: Type = "Board Meeting" (highest prep category)
CAN-02B: Importance = "CRITICAL" (board-level, strategic)
CAN-07: Metadata → Agenda: "Financial review, product roadmap, hiring plan", Attachments: None
CAN-08: Related Docs → Found:
  - Q4 financial dashboard (needs update)
  - Previous board deck from Q3
  - Action items from last board meeting
  - NO pre-read deck attached (missing!)
CAN-21: Prep Time Estimate = 2 hours (create deck + rehearse + no materials provided)
CAN-06: Available Slots Before Friday 9am → 
  - Wed 2-4pm ✓ (2 hours available)
  - Thu 10-11am (only 1 hour)
CAN-11: Decision = Schedule "Focus: Prep for Board Meeting" (Wed 2-4pm)

Output: "✓ IMPORTANT: Board Meeting - 2 hours prep time scheduled (Wed 2-4pm)"

---

CONTRAST: If Wed 2-4pm was booked:
CAN-06: Available Slots = NONE (no 2-hour blocks found)
CAN-11: Decision = FLAG "⚠️ IMPORTANT: Board Meeting - Missing 2 hours prep time (no available slots)"

Output: "⚠️ FLAGGED: Board Meeting - Needs 2 hours prep but no calendar space available"
```

---

## Hero Prompt 3: Time Reclamation Analysis (organizer-3)

**Prompt**: "Help me understand where I am spending my time and identify ways I can reclaim time to focus more on my top priorities."

**Capabilities Required**: Time analysis, pattern recognition, priority alignment, optimization recommendations, visualization

### Canonical Task Decomposition: **10 Tasks**

#### Task 1: Natural Language Understanding (CAN-04)
- **Purpose**: Extract user intent for time analysis and reclamation focus
- **Input**: User query requesting time understanding and optimization
- **Output**: Intent classification (analyze time + optimize + prioritize), top priorities reference
- **Tier**: Universal (Tier 1)

#### Task 2: Calendar Events Retrieval (CAN-01)
- **Purpose**: Load historical calendar events for time analysis period
- **Input**: Time range (typically 1-3 months historical data)
- **Output**: Array of past calendar events with durations
- **Tier**: Universal (Tier 1)

#### Task 3: Meeting Type Classification (CAN-02A)
- **Purpose**: Classify past meetings by type for categorization
- **Input**: Historical calendar events
- **Output**: Meeting type labels (1:1, team sync, customer, planning, etc.)
- **Tier**: Universal (Tier 1)

#### Task 4: Meeting Importance Assessment (CAN-02B)
- **Purpose**: Assess which past meetings aligned with top priorities
- **Input**: Meeting metadata + user priorities
- **Output**: Priority alignment scores ("high-value", "medium-value", "low-value")
- **Tier**: Universal (Tier 1)

#### Task 5: Meeting Metadata Extraction (CAN-07)
- **Purpose**: Extract meeting details for analysis
- **Input**: Historical calendar events
- **Output**: Attendees, topics, outcomes, recurrence patterns
- **Tier**: Common (Tier 2)

#### Task 6: Recurring Patterns Detection (CAN-16)
- **Purpose**: Identify recurring meeting patterns and time commitments
- **Input**: Historical calendar data from CAN-01
- **Output**: Detected patterns (weekly 1:1s, daily standups, monthly reviews)
- **Tier**: Specialized (Tier 3)

#### Task 7: Meeting Summarization (CAN-10)
- **Purpose**: Aggregate time spent per category, participant, project
- **Input**: Classified meetings (CAN-02A), metadata (CAN-07), patterns (CAN-16)
- **Output**: Time aggregations ("30% in 1:1s", "20% in customer meetings", "15% with Manager X")
- **Tier**: Common (Tier 2)

#### Task 8: Data Visualization (CAN-20)
- **Purpose**: Create visual representations of time distribution
- **Input**: Aggregated time data from CAN-10
- **Output**: Charts, graphs, dashboards showing time allocation patterns
- **Tier**: Specialized (Tier 3)
- **Note**: "Show patterns", "visualize" keywords trigger this task

#### Task 9: Meeting Insights & Recommendations (CAN-14)
- **Purpose**: Identify low-value meetings and reclamation opportunities
- **Input**: Time aggregations (CAN-10), priority alignment (CAN-02B)
- **Output**: Recommendations ("Decline recurring X meetings", "Delegate Y meetings", "Shorten Z from 60→30 min")
- **Tier**: Common (Tier 2)

#### Task 10: Scheduling Constraint Analysis (CAN-03)
- **Purpose**: Validate reclamation recommendations against constraints
- **Input**: Recommendations from CAN-14, calendar commitments
- **Output**: Feasibility assessment, constraint conflicts
- **Tier**: Universal (Tier 1)
- **Note**: Ensures recommendations respect actual constraints

**Evaluation Criteria**:
- Time categorization accuracy
- Reclamation opportunity identification quality
- Actionability of recommendations
- Visualization clarity

### Execution Composition

**How Tasks Work Together to Answer the Prompt:**

```
STEP 1: Understand User Intent
CAN-04 (NLU) → Extract: "understand where I am spending my time", "identify ways to reclaim time", "focus on top priorities"
→ Intent: Time analysis + optimization + priority alignment

STEP 2: Retrieve Historical Data
CAN-01 (Calendar Retrieval) → Load past 1-3 months of calendar events (historical analysis)

STEP 3: Classify & Enrich Historical Meetings
CAN-02A (Meeting Type) → Classify each past meeting:
  - 1:1s, team syncs, customer meetings, planning sessions, admin time
CAN-02B (Meeting Importance) → Score priority alignment:
  - High-value: Aligns with top priorities (customer focus, strategy)
  - Medium-value: Important but not strategic (team coordination)
  - Low-value: Administrative, could delegate/decline
CAN-07 (Metadata Extraction) → Extract attendees, topics, recurrence patterns

STEP 4: Pattern Detection
CAN-16 (Recurring Patterns) → Identify recurring commitments:
  - Weekly 1:1s (5 hours/week)
  - Daily standups (2.5 hours/week)
  - Monthly all-hands (1 hour/month)
  - Bi-weekly planning (4 hours/month)

STEP 5: Aggregate & Analyze
CAN-10 (Meeting Summarization) → Calculate time distribution:
  - By type: "30% in 1:1s, 25% in customer meetings, 20% in team syncs, 15% in planning, 10% admin"
  - By participant: "8 hours/month with Manager, 6 hours with Product Team"
  - By priority: "40% high-value, 35% medium-value, 25% low-value"

STEP 6: Visualize Patterns
CAN-20 (Data Visualization) → Create visuals:
  - Pie chart: Time by meeting type
  - Bar chart: Hours per week over time (trending up/down?)
  - Heatmap: Meeting density by day/hour
  - Priority breakdown: High vs medium vs low value meetings

STEP 7: Generate Reclamation Recommendations
CAN-14 (Insights & Recommendations) → Identify opportunities based on analysis:
  - LOW-VALUE RECURRING: "You spend 4 hours/month in 'Weekly Admin Review' (low priority). Can you delegate or reduce frequency to monthly?"
  - OVER-INDEXING: "25% of your time is in 1:1s. Can you batch some or shorten from 60→30 min?"
  - PRIORITY MISALIGNMENT: "Only 40% of time aligns with top priorities. Consider declining meetings in category X to free up 5 hours/week."

STEP 8: Validate Feasibility
CAN-03 (Constraint Analysis) → Check recommendations against reality:
  - Can't decline all team syncs (manager expectation)
  - Customer meetings can't be shortened (external constraint)
  - 1:1s with directs are critical (management responsibility)
  → Filter recommendations to ACTIONABLE only

OUTPUT: Comprehensive time analysis with:
  1. WHERE TIME GOES: Breakdown by type, participant, priority (with visualizations)
  2. PATTERNS DETECTED: Recurring commitments, trending changes
  3. RECLAMATION OPPORTUNITIES: Specific recommendations to free up 5-10 hours/week
  4. PRIORITY ALIGNMENT: Gap between current time spend vs top priorities
```

**Key Orchestration Patterns**:
- **Historical Analysis**: All tasks operate on PAST data (1-3 months lookback)
- **Parallel Classification**: CAN-02A, CAN-02B, CAN-07 can process same events concurrently
- **Aggregation Pipeline**: CAN-16 (patterns) + CAN-10 (summarization) → CAN-20 (visualization)
- **Recommendation Filtering**: CAN-14 generates ideas → CAN-03 validates feasibility → Actionable output

**Example Flow for Time Reclamation**:
```
Input: "Help me understand where I am spending my time and reclaim time for customer focus"

CAN-04: Extract → analyze time + optimize + prioritize "customer focus" ✓
CAN-01: Load → 90 days of calendar (180 meetings total) ✓
CAN-02A: Classify → 
  - 50 meetings = "1:1"
  - 30 meetings = "Team Sync"
  - 40 meetings = "Customer Meeting"
  - 30 meetings = "Admin/Planning"
  - 30 meetings = "Other"
CAN-02B: Score →
  - 40 customer meetings = HIGH VALUE (aligns with priority)
  - 30 admin = LOW VALUE (doesn't align)
  - 50 1:1s = MEDIUM VALUE (management responsibility)
CAN-07: Extract metadata ✓
CAN-16: Patterns →
  - Weekly 1:1s with 5 directs (5 hours/week)
  - Daily team standup (30 min/day = 2.5 hours/week)
  - Monthly "Admin Review" (2 hours/month, low-value recurring)
CAN-10: Summarize →
  - 1:1s: 30% (54 hours/quarter)
  - Customer: 25% (45 hours/quarter)
  - Team Sync: 20% (36 hours/quarter)
  - Admin: 15% (27 hours/quarter - LOW VALUE!)
  - Other: 10% (18 hours/quarter)
CAN-20: Visualize → Pie chart showing 15% in low-value admin ✓
CAN-14: Recommend →
  1. "Decline 'Monthly Admin Review' → Reclaim 2 hours/month (24 hours/year)"
  2. "Shorten team standup from 30→15 min → Reclaim 1.25 hours/week (65 hours/year)"
  3. "Delegate 2 recurring 1:1s to senior lead → Reclaim 2 hours/week (104 hours/year)"
CAN-03: Validate →
  1. Admin Review: Can decline (organizer is peer) ✓ ACTIONABLE
  2. Standup shortening: Need team agreement ⚠️ REQUIRES DISCUSSION
  3. Delegate 1:1s: 2 directs are junior (can't delegate) ❌ NOT FEASIBLE

Output: "You spend 15% of time in low-value admin meetings. ACTIONABLE: Decline 'Monthly Admin Review' to reclaim 24 hours/year. DISCUSS: Shorten daily standup to reclaim 65 hours/year."
```

---

## Hero Prompt 4: Multi-Meeting Scheduling (schedule-1)

**Prompt**: "I need to schedule 3 meetings this week: 1:1 with Sarah (30 min), customer demo (1 hour), and team planning (2 hours). Find times that work for everyone."

**Capabilities Required**: Multi-meeting orchestration, availability checking, constraint satisfaction, conflict resolution, calendar writing

### Canonical Task Decomposition: **10 Tasks**

#### Task 1: Natural Language Understanding (CAN-04)
- **Purpose**: Extract scheduling requirements (3 meetings, participants, durations, timeframe)
- **Input**: User query with multiple meeting specifications
- **Output**: Structured meeting specs [
  - {type: "1:1", participant: "Sarah", duration: 30min},
  - {type: "customer demo", duration: 60min},
  - {type: "team planning", duration: 120min}
], timeframe: "this week"
- **Tier**: Universal (Tier 1)

#### Task 2: Calendar Events Retrieval (CAN-01)
- **Purpose**: Retrieve user's calendar for the current week
- **Input**: Time range (this week), user calendar
- **Output**: User's scheduled events with busy/free status
- **Tier**: Universal (Tier 1)

#### Task 3: Meeting Type Classification (CAN-02A)
- **Purpose**: Classify meeting types to understand requirements
- **Input**: Meeting specifications from CAN-04
- **Output**: Meeting type classifications (1:1, customer-facing, internal planning)
- **Tier**: Universal (Tier 1)

#### Task 4: Meeting Attendees Analysis (CAN-05)
- **Purpose**: Identify required participants for each meeting
- **Input**: Meeting specs ("Sarah", "customer", "team")
- **Output**: Attendee lists [sarah@company.com], [customer-contacts], [team-members]
- **Tier**: Universal (Tier 1)

#### Task 5: Availability Checking (CAN-06)
- **Purpose**: Check availability for all participants across all 3 meetings
- **Input**: Attendee lists from CAN-05, user calendar from CAN-01
- **Output**: Free/busy grids for each participant, available time slots
- **Tier**: Common (Tier 2)
- **Dependencies**: Requires CAN-01 (Calendar Retrieval)

#### Task 6: Scheduling Constraint Analysis (CAN-03)
- **Purpose**: Analyze constraints (durations, this week, participant availability)
- **Input**: Meeting requirements from CAN-04, availability from CAN-06
- **Output**: Constraint satisfaction feasibility, potential conflicts
- **Tier**: Universal (Tier 1)

#### Task 7: Constraint Satisfaction (CAN-12)
- **Purpose**: Find time slots that satisfy all constraints for all 3 meetings
- **Input**: Available slots from CAN-06, constraints from CAN-03
- **Output**: Proposed time slots for each meeting OR constraint conflicts
- **Tier**: Common (Tier 2)

#### Task 8: Conflict Resolution (CAN-23)
- **Purpose**: Handle scheduling conflicts if no perfect solution exists
- **Input**: Constraint conflicts from CAN-12
- **Output**: Conflict resolution strategies (bump low-priority meetings, extend to next week, shorten durations)
- **Tier**: Specialized (Tier 3)
- **Note**: "Find times that work" implies handling conflicts if needed

#### Task 9: Meeting Metadata Extraction (CAN-07)
- **Purpose**: Prepare meeting metadata for calendar creation
- **Input**: Meeting specifications from CAN-04
- **Output**: Complete meeting details (titles, agendas, participants, durations)
- **Tier**: Common (Tier 2)

#### Task 10: Time Block Scheduling (CAN-11)
- **Purpose**: Create calendar events for the 3 meetings
- **Input**: Proposed time slots from CAN-12, metadata from CAN-07
- **Output**: Calendar write operations, meeting invitations sent
- **Tier**: Common (Tier 2)
- **Note**: Final execution step to commit meetings to calendar

**Evaluation Criteria**:
- Scheduling success rate (all 3 meetings scheduled within timeframe)
- Constraint satisfaction quality
- Participant availability respect
- Conflict handling effectiveness

### Execution Composition

**How Tasks Work Together to Answer the Prompt:**

```
STEP 1: Parse Multi-Meeting Request
CAN-04 (NLU) → Extract 3 meeting specifications:
  - Meeting 1: {participant: "Sarah", duration: 30min, type: "1:1"}
  - Meeting 2: {participants: "customer", duration: 60min, type: "demo"}
  - Meeting 3: {participants: "team", duration: 120min, type: "planning"}
  - Timeframe: "this week"

STEP 2: Gather Calendar Data
CAN-01 (Calendar Retrieval) → Load user's calendar for this week (Mon-Fri)
CAN-02A (Meeting Type) → Classify each of the 3 meetings to understand requirements:
  - 1:1 = low complexity, flexible
  - Customer demo = high importance, needs prep time before
  - Team planning = high coordination, needs multiple people

STEP 3: Identify Participants
CAN-05 (Attendees Analysis) → Resolve participant names to calendar entries:
  - "Sarah" → sarah.jones@company.com
  - "customer" → Active customer contacts from recent meetings
  - "team" → Engineering team members (lookup from org structure)

STEP 4: Check Availability for ALL Meetings
CAN-06 (Availability Checking) → For EACH meeting, find common free time:
  - 1:1 with Sarah: Check user + Sarah's calendars → Find 30min overlaps
  - Customer demo: Check user + customer calendars → Find 60min overlaps
  - Team planning: Check user + all team members → Find 120min overlaps (hardest!)

STEP 5: Analyze Constraints
CAN-03 (Scheduling Constraint Analysis) → Model requirements:
  - All 3 meetings must fit within "this week" (5 days)
  - Durations fixed (30min, 60min, 120min = 3.5 hours total)
  - Customer demo should not be first/last thing in day (needs prep + debrief)
  - Team planning needs 2-hour block (rare on some calendars)

STEP 6: Find Feasible Solutions
CAN-12 (Constraint Satisfaction) → Attempt to place all 3 meetings:
  - Algorithm: Try to place longest/hardest meeting first (team planning 2hrs)
  - Then place medium meeting (customer demo 1hr)
  - Then place easiest (Sarah 1:1 30min)
  - Result: EITHER all 3 scheduled OR conflicts detected

STEP 7: Handle Conflicts (If Needed)
CAN-23 (Conflict Resolution) → If CAN-12 finds no perfect solution:
  - Strategy 1: Extend timeframe to "this week or early next week"
  - Strategy 2: Offer to bump lower-priority user meetings
  - Strategy 3: Shorten team planning from 2hrs → 90min
  - Strategy 4: Accept partial solution (schedule 2 of 3, flag the 3rd)

STEP 8: Prepare Meeting Details
CAN-07 (Metadata Extraction) → Prepare complete meeting information:
  - Meeting 1: "1:1 with Sarah" (subject, attendees, duration)
  - Meeting 2: "Customer Demo" (subject, attendees, agenda template, duration)
  - Meeting 3: "Team Planning" (subject, all team attendees, duration)

STEP 9: Create Calendar Events
CAN-11 (Time Block Scheduling) → Write to calendar:
  - Create event for Sarah 1:1 (send invite)
  - Create event for customer demo (send invite with agenda)
  - Create event for team planning (send invite to all team members)

OUTPUT: Confirmation showing:
  - Meeting 1 scheduled: Sarah 1:1 (Tue 2:00-2:30pm) ✓
  - Meeting 2 scheduled: Customer Demo (Wed 10:00-11:00am) ✓
  - Meeting 3 scheduled: Team Planning (Thu 1:00-3:00pm) ✓
  OR
  - Conflict report: "Team planning could not fit this week (no 2-hour blocks available). Extend to next week?"
```

**Key Orchestration Patterns**:
- **Multi-Object Scheduling**: System must coordinate 3 separate scheduling workflows in parallel
- **Constraint Propagation**: CAN-03 analyzes global constraints → feeds into CAN-12 optimization
- **Availability Fan-out**: CAN-06 checks N people per meeting (1 for Sarah, M for customer, K for team)
- **Conflict Handling Fallback**: CAN-12 attempts perfect solution → fails → CAN-23 proposes alternatives
- **Metadata Preparation**: CAN-07 runs independently to prepare meeting details while CAN-12 finds slots

**Example Flow - Successful Scheduling**:
```
CAN-04: Parse → 3 meetings, this week ✓
CAN-01: Load calendar → Mon-Fri availability ✓
CAN-02A: Classify → 1:1, demo, planning ✓
CAN-05: Resolve attendees → sarah@co.com, customer@client.com, 5 team members ✓
CAN-06: Find availability →
  - Sarah: Tue 2pm, Wed 9am, Thu 11am (3 slots)
  - Customer: Wed 10am, Thu 2pm (2 slots)
  - Team (all 5): Thu 1-3pm, Fri 2-4pm (2 slots - hard constraint!)
CAN-03: Constraints → All within Mon-Fri ✓
CAN-12: Optimize →
  - Place team planning: Thu 1-3pm (only shared 2-hour slot) ✓
  - Place customer demo: Wed 10am (avoids Thu conflict) ✓
  - Place Sarah 1:1: Tue 2pm (fills remaining need) ✓
CAN-07: Prepare metadata ✓
CAN-11: Write to calendar → 3 invites sent ✓

Output: "Scheduled all 3 meetings: Sarah (Tue 2pm), Customer Demo (Wed 10am), Team Planning (Thu 1-3pm)"
```

**Example Flow - Conflict Requiring Resolution**:
```
CAN-06: Find availability →
  - Team (all 5): NO 2-hour blocks available this week ❌
CAN-12: Constraint satisfaction → FAILED (cannot place team planning)
CAN-23: Conflict resolution →
  - Option 1: Extend to next week (Tue 9-11am available)
  - Option 2: Reduce team planning to 90min (Thu 3-4:30pm available)
  - Option 3: Schedule 2 of 3 now, manual schedule team planning

Output: "Scheduled Sarah (Tue 2pm) and Customer Demo (Wed 10am). Team planning has no 2-hour availability this week. Extend to next Tue 9-11am?"
```

---

## Hero Prompt 5: Buffer Time Insertion (schedule-2)

**Prompt**: "Schedule 30 minutes of buffer time after each of my back-to-back meetings tomorrow."

**Capabilities Required**: Meeting pattern detection, buffer time insertion, calendar optimization, conflict avoidance

### Canonical Task Decomposition: **8 Tasks**

#### Task 1: Natural Language Understanding (CAN-04)
- **Purpose**: Extract buffer time requirements and target meetings
- **Input**: User query requesting buffer insertion
- **Output**: Buffer duration (30 min), criteria ("back-to-back meetings"), timeframe ("tomorrow")
- **Tier**: Universal (Tier 1)

#### Task 2: Calendar Events Retrieval (CAN-01)
- **Purpose**: Retrieve tomorrow's calendar events
- **Input**: Time range (tomorrow, full day)
- **Output**: Array of scheduled meetings for tomorrow
- **Tier**: Universal (Tier 1)

#### Task 3: Meeting Metadata Extraction (CAN-07)
- **Purpose**: Extract meeting start/end times to identify back-to-back patterns
- **Input**: Calendar events from CAN-01
- **Output**: Meeting time blocks with start/end timestamps
- **Tier**: Common (Tier 2)

#### Task 4: Recurring Patterns Detection (CAN-16)
- **Purpose**: Identify back-to-back meeting sequences (meetings with <5 min gap)
- **Input**: Meeting time blocks from CAN-07
- **Output**: Back-to-back meeting pairs/sequences flagged
- **Tier**: Specialized (Tier 3)

#### Task 5: Availability Checking (CAN-06)
- **Purpose**: Check if 30-min buffer slots are available after each back-to-back meeting
- **Input**: Back-to-back meetings from CAN-16, existing calendar from CAN-01
- **Output**: Available buffer slots OR conflicts
- **Tier**: Common (Tier 2)
- **Dependencies**: Requires CAN-01 (Calendar Retrieval)

#### Task 6: Conflict Resolution (CAN-23)
- **Purpose**: Handle conflicts if buffer time overlaps with existing meetings
- **Input**: Buffer slot conflicts from CAN-06
- **Output**: Resolution strategies (reschedule conflicting meeting, shorten meeting, skip buffer)
- **Tier**: Specialized (Tier 3)

#### Task 7: Time Block Scheduling (CAN-11)
- **Purpose**: Insert buffer time blocks into calendar
- **Input**: Available buffer slots from CAN-06, resolved conflicts from CAN-23
- **Output**: Calendar blocks created ("Buffer Time - 30 min")
- **Tier**: Common (Tier 2)

#### Task 8: Meeting Insights & Recommendations (CAN-14)
- **Purpose**: Report buffer insertion results and any unresolved conflicts
- **Input**: Scheduled buffers from CAN-11, conflicts from CAN-23
- **Output**: Summary ("Added 4 buffers, 1 conflict requires manual resolution")
- **Tier**: Common (Tier 2)

**Evaluation Criteria**:
- Back-to-back meeting detection accuracy
- Buffer insertion success rate
- Conflict handling quality
- User calendar integrity maintained

### Execution Composition

**How Tasks Work Together to Answer the Prompt:**

```
STEP 1: Understand Buffer Requirements
CAN-04 (NLU) → Extract: "30 minutes of buffer time", criteria "after each back-to-back meeting", timeframe "tomorrow"

STEP 2: Retrieve Tomorrow's Calendar
CAN-01 (Calendar Retrieval) → Load all events for tomorrow (full day)

STEP 3: Extract Meeting Time Blocks
CAN-07 (Metadata Extraction) → For each meeting, extract:
  - Start time
  - End time
  - Duration
  - Subject (to label buffer blocks)

STEP 4: Detect Back-to-Back Patterns
CAN-16 (Recurring Patterns Detection) → Identify back-to-back meetings:
  - Algorithm: If Meeting_B.start - Meeting_A.end < 5 minutes → BACK-TO-BACK
  - Example: 9:00-10:00am meeting + 10:00-11:00am meeting = BACK-TO-BACK
  - Example: 9:00-10:00am meeting + 10:15-11:00am meeting = NOT back-to-back (15min gap)
  - Result: List of back-to-back sequences

STEP 5: Check Buffer Slot Availability
CAN-06 (Availability Checking) → For each back-to-back meeting endpoint:
  - Check if 30min buffer slot is FREE immediately after
  - Example: Meeting ends 10:00am → Is 10:00-10:30am free?
  - Result: Available slots OR conflicts

STEP 6: Resolve Conflicts (If Any)
CAN-23 (Conflict Resolution) → If buffer slot overlaps with existing meeting:
  - Option 1: Shorten next meeting by 30min (if not important)
  - Option 2: Skip buffer for this occurrence (manual override)
  - Option 3: Reschedule conflicting meeting to later
  - Prioritize user's explicit request (buffer time) over existing low-priority meetings

STEP 7: Insert Buffer Blocks
CAN-11 (Time Block Scheduling) → Create calendar blocks:
  - Subject: "Buffer Time" or "Break - 30 min"
  - Duration: 30 minutes
  - Type: Focus time block (blocks calendar for others)
  - Location: After each back-to-back meeting

STEP 8: Report Results
CAN-14 (Insights & Recommendations) → Summarize:
  - How many back-to-back meetings detected
  - How many buffers successfully added
  - Any conflicts that required resolution
  - Any unresolved conflicts requiring user decision

OUTPUT: Summary with calendar modifications:
  - "Detected 4 back-to-back meeting sequences tomorrow"
  - "Added 30-min buffers after: 10am meeting, 2pm meeting, 4pm meeting (3 of 4)"
  - "Conflict: Cannot add buffer after 11:30am meeting (next meeting starts at 12pm). Reschedule 12pm meeting?"
```

**Key Orchestration Patterns**:
- **Pattern Detection First**: CAN-16 identifies WHICH meetings need buffers before checking availability
- **Sequential Processing**: For each back-to-back sequence, check → resolve → insert
- **Conflict Handling Inline**: CAN-23 runs per-buffer (not batched at end)
- **Availability Gate**: CAN-06 validates each 30min buffer slot before CAN-11 creates it
- **Reporting Layer**: CAN-14 aggregates results from multiple CAN-11 operations

**Example Flow - Successful Buffer Insertion**:
```
Input: "Schedule 30 minutes of buffer time after each back-to-back meeting tomorrow"

CAN-04: Extract → 30min buffer, back-to-back criteria, tomorrow ✓
CAN-01: Load → Tomorrow's calendar:
  - 9:00-10:00am "Team Standup"
  - 10:00-11:00am "Project Review" ← BACK-TO-BACK with 9am
  - 11:00am-12:00pm "Customer Call" ← BACK-TO-BACK with 10am
  - 2:00-3:00pm "1:1 with Manager"
  - 3:00-4:00pm "Design Review" ← BACK-TO-BACK with 2pm
  - 5:00-6:00pm "Wrap-up Meeting"
CAN-07: Extract time blocks ✓
CAN-16: Detect patterns →
  - Sequence 1: 9am → 10am → 11am (2 endpoints need buffers: after 10am, after 11am)
  - Sequence 2: 2pm → 3pm (1 endpoint needs buffer: after 3pm)
  - Total: 3 back-to-back endpoints identified
CAN-06: Check availability →
  - After 10am (10:00-10:30am): CONFLICT (Customer Call starts at 11am, not 10am - wait, 11am is start)
  - After 11am (11:00-11:30am): FREE ✓
  - After 12pm (12:00-12:30pm): FREE ✓
  - After 3pm (3:00-3:30pm): FREE ✓
CAN-23: Not needed (all slots free)
CAN-11: Insert buffers →
  - 11:00-11:30am "Buffer Time" ✓
  - 12:00-12:30pm "Buffer Time" ✓
  - 4:00-4:30pm "Buffer Time" ✓
CAN-14: Report → "Added 3 buffers after back-to-back meetings tomorrow"

Output: "✓ Added 30-min buffers after: 11am meeting, 12pm meeting, 4pm meeting"
```

**Example Flow - With Conflicts**:
```
CAN-01: Load → Tomorrow's calendar:
  - 9:00-10:00am "Meeting A"
  - 10:00-11:00am "Meeting B" ← BACK-TO-BACK
  - 11:00-11:45am "Meeting C" ← BACK-TO-BACK (no space for buffer!)
CAN-16: Detect → 2 back-to-back endpoints (after 10am, after 11am)
CAN-06: Check availability →
  - After 10am (10:00-10:30am): CONFLICT (Meeting C starts at 11am)
  - After 11:45am (11:45am-12:15pm): FREE ✓
CAN-23: Resolve conflict after 10am →
  - Option 1: Shorten Meeting B from 60min → 30min (9:30-10:30am) → Creates buffer 10:30-11:00am
  - Option 2: Reschedule Meeting C to 11:30am (adds 30min delay)
  - Option 3: Skip buffer for this occurrence
  - User Decision Required
CAN-11: Insert available buffer →
  - 11:45am-12:15pm "Buffer Time" ✓
CAN-14: Report →
  - "Added 1 buffer after 11:45am meeting"
  - "Conflict: Cannot add buffer after 10am meeting (Meeting C starts immediately). Options: (1) Shorten Meeting B, (2) Delay Meeting C, (3) Skip this buffer"

Output: "✓ Added 1 of 2 buffers. Conflict at 10am requires your decision: [Options]"
```

---

## Hero Prompt 6: Travel Time-Aware Scheduling (schedule-3)

**Prompt**: "Schedule my quarterly review meetings across all time zones, accounting for travel time between locations."

**Capabilities Required**: Time zone management, travel time calculation, multi-timezone scheduling, location-aware planning

### Canonical Task Decomposition: **9 Tasks**

#### Task 1: Natural Language Understanding (CAN-04)
- **Purpose**: Extract scheduling requirements with time zone and travel considerations
- **Input**: User query requesting multi-timezone scheduling with travel time
- **Output**: Meeting type ("quarterly review"), scope ("all time zones"), constraint ("travel time")
- **Tier**: Universal (Tier 1)

#### Task 2: Calendar Events Retrieval (CAN-01)
- **Purpose**: Retrieve user's calendar to identify scheduling windows
- **Input**: Time range (quarterly planning horizon, typically 1-3 months)
- **Output**: User's scheduled events and availability
- **Tier**: Universal (Tier 1)

#### Task 3: Meeting Attendees Analysis (CAN-05)
- **Purpose**: Identify quarterly review participants and their locations
- **Input**: Meeting type ("quarterly review"), organizational structure
- **Output**: Attendee lists with location/timezone metadata
- **Tier**: Universal (Tier 1)

#### Task 4: Time Zone Management (CAN-15)
- **Purpose**: Convert meeting times across participant time zones
- **Input**: Attendee locations from CAN-05, proposed meeting times
- **Output**: Time zone conversions, optimal meeting windows considering all zones
- **Tier**: Specialized (Tier 3)
- **Note**: Critical for "across all time zones" requirement

#### Task 5: Meeting Resources Management (CAN-19)
- **Purpose**: Identify travel logistics and location requirements
- **Input**: Meeting locations, participant locations
- **Output**: Travel requirements, venue needs, equipment
- **Tier**: Specialized (Tier 3)

#### Task 6: Scheduling Constraint Analysis (CAN-03)
- **Purpose**: Model travel time constraints between locations
- **Input**: Meeting sequence, locations, travel time estimates
- **Output**: Constraint rules (minimum gap = meeting duration + travel time + buffer)
- **Tier**: Universal (Tier 1)

#### Task 7: Availability Checking (CAN-06)
- **Purpose**: Find available slots respecting travel time constraints
- **Input**: User calendar from CAN-01, attendee availability, travel constraints from CAN-03
- **Output**: Feasible time slots with travel time accounted
- **Tier**: Common (Tier 2)
- **Dependencies**: Requires CAN-01 (Calendar Retrieval)

#### Task 8: Constraint Satisfaction (CAN-12)
- **Purpose**: Optimize meeting schedule across all constraints
- **Input**: Available slots from CAN-06, time zone constraints from CAN-15, travel constraints from CAN-03
- **Output**: Optimized meeting schedule OR infeasibility report
- **Tier**: Common (Tier 2)

#### Task 9: Time Block Scheduling (CAN-11)
- **Purpose**: Create calendar events for quarterly reviews with travel blocks
- **Input**: Optimized schedule from CAN-12, time zone info from CAN-15
- **Output**: Calendar events created with correct time zones + travel time blocks
- **Tier**: Common (Tier 2)

**Evaluation Criteria**:
- Time zone conversion accuracy
- Travel time calculation correctness
- Meeting schedule feasibility
- Optimization quality (minimize travel, maximize availability)

### Execution Composition

**How Tasks Work Together to Answer the Prompt:**

```
STEP 1: Parse Multi-Timezone Scheduling Request
CAN-04 (NLU) → Extract: "quarterly review meetings", scope "across all time zones", constraint "travel time between locations"

STEP 2: Retrieve User Calendar
CAN-01 (Calendar Retrieval) → Load quarterly planning horizon (next 1-3 months)

STEP 3: Identify Review Participants & Locations
CAN-05 (Attendees Analysis) → Resolve "quarterly review" participants:
  - Regional teams: APAC team (Singapore), EMEA team (London), Americas team (San Francisco)
  - Executives: CEO (travels), VP Product (SF), VP Sales (NYC)
  - Result: 3 meetings required, different timezones per meeting

STEP 4: Model Time Zone Constraints
CAN-15 (Time Zone Management) → For each meeting, calculate:
  - APAC Review: Singapore timezone (UTC+8), participants in Asia/Pacific
  - EMEA Review: London timezone (UTC+0), participants in Europe/Middle East/Africa
  - Americas Review: San Francisco (UTC-8), participants in North/South America
  - Overlapping work hours: APAC + EMEA = 8am London / 4pm Singapore (limited overlap)
  - No reasonable overlap for all 3 regions → Sequential scheduling required

STEP 5: Model Travel Time Constraints
CAN-19 (Meeting Resources) → Calculate travel logistics:
  - SF → London: 11 hours flight + 3 hours airport/transit = 14 hours minimum
  - London → Singapore: 13 hours flight + 3 hours = 16 hours minimum
  - Singapore → SF: 17 hours flight + 3 hours = 20 hours minimum
  - Result: Minimum 1 day between meetings + jet lag recovery (suggest +1 day = 2 days between)

CAN-03 (Constraint Analysis) → Model scheduling rules:
  - Rule 1: Meeting N+1 must start ≥ (Meeting N end time + travel time + 1 day recovery)
  - Rule 2: Each meeting in participant's local business hours (9am-5pm local time)
  - Rule 3: Respect weekend (don't schedule meetings during traveler's local weekend)

STEP 6: Find Feasible Time Windows
CAN-06 (Availability Checking) → Check availability for all participants across meetings:
  - APAC team availability (Singapore business hours)
  - EMEA team availability (London business hours)
  - Americas team availability (SF business hours)
  - CEO availability (traveling for all 3) ← Critical constraint

STEP 7: Optimize Meeting Sequence
CAN-12 (Constraint Satisfaction) → Solve multi-constraint optimization:
  - Minimize total travel time (optimal route: SF → London → Singapore → SF)
  - Maximize participant availability
  - Respect time zone business hours
  - Insert travel days between meetings
  - Result: Proposed schedule OR infeasibility report

STEP 8: Create Calendar Events with Travel
CAN-11 (Time Block Scheduling) → Write to calendar:
  - Americas Review: Mon 9am PT (San Francisco)
  - Travel block: Tue-Wed (SF → London, 14 hours + recovery)
  - EMEA Review: Thu 2pm GMT (London) [converts to 6am PT - user in London]
  - Travel block: Fri-Sat (London → Singapore, 16 hours + recovery)
  - APAC Review: Mon 10am SGT (Singapore) [converts to 2am GMT, 6pm PT - user in Singapore]
  - Travel block: Tue-Wed (Singapore → SF return)

OUTPUT: Comprehensive travel-aware schedule:
  - 3 quarterly reviews scheduled across time zones
  - Each meeting in participants' local business hours
  - Travel time blocks inserted between meetings
  - Time zone conversions shown for all participants
  - Total trip duration: 9 days (3 meetings + 6 travel/recovery days)
```

**Key Orchestration Patterns**:
- **Multi-Timezone Coordination**: CAN-15 runs for EACH meeting to convert times for all participants
- **Travel Time as Constraint**: CAN-19 + CAN-03 model travel as temporal constraint (not just calendar block)
- **Sequential Optimization**: CAN-12 must solve for optimal route AND meeting times simultaneously
- **Calendar Write Complexity**: CAN-11 creates BOTH meeting invites AND travel blocks (6 calendar entries total)

**Example Flow - Successful Multi-Timezone Scheduling**:
```
Input: "Schedule my quarterly review meetings across all time zones, accounting for travel time"

CAN-04: Extract → quarterly review, all time zones, travel time ✓
CAN-01: Load → Next 3 months calendar ✓
CAN-05: Identify participants →
  - Americas Review: SF team (10 people), VP Product (SF), CEO (traveling)
  - EMEA Review: London team (8 people), VP Sales (NYC), CEO (traveling)
  - APAC Review: Singapore team (6 people), CEO (traveling)
CAN-15: Time zone analysis →
  - Americas: PT (UTC-8)
  - EMEA: GMT (UTC+0)
  - APAC: SGT (UTC+8)
  - 16-hour total spread (no overlapping work hours for all 3 regions)
CAN-19: Travel logistics →
  - SF → London: 14 hours (suggest 2-day buffer)
  - London → Singapore: 16 hours (suggest 2-day buffer)
  - Singapore → SF: 20 hours (suggest 2-day buffer)
CAN-03: Constraints →
  - Each meeting ≥ 2 days after previous (travel + recovery)
  - All meetings in local business hours (9am-5pm local)
CAN-06: Availability →
  - CEO has 2-week window in Month 2 (critical constraint)
  - All regional teams flexible within that window
CAN-12: Optimize →
  - Week 1 Mon: Americas Review (9am PT)
  - Week 1 Thu: EMEA Review (2pm GMT) - 2 days after Americas ✓
  - Week 2 Mon: APAC Review (10am SGT) - 2+ days after EMEA ✓
  - Route: SF → London → Singapore → SF
CAN-11: Create events →
  - Mon Week 1: "Americas Quarterly Review" (9-11am PT)
  - Tue-Wed Week 1: "Travel: SF → London" (blocked time)
  - Thu Week 1: "EMEA Quarterly Review" (2-4pm GMT = 6-8am PT)
  - Fri-Sun Week 1: "Travel: London → Singapore" (blocked time)
  - Mon Week 2: "APAC Quarterly Review" (10am-12pm SGT = 2-4am GMT)
  - Tue-Wed Week 2: "Travel: Singapore → SF Return" (blocked time)

Output: 
"Scheduled 3 quarterly reviews:
 - Americas: Mon 9am PT (San Francisco)
 - EMEA: Thu 2pm GMT (London) - includes 2 days travel from SF
 - APAC: Mon 10am SGT (Singapore) - includes 3 days travel from London
 Total trip: 9 days (3 meetings + 6 travel days)"
```

**Example Flow - With Time Zone Conflicts**:
```
CAN-15: Time zone analysis → APAC participants want 9am SGT, but that's 1am GMT (middle of night for EMEA participants)
CAN-12: Conflict → Cannot find time that's business hours for ALL participants in a single meeting
CAN-23 (if invoked): Resolution options →
  - Option 1: Split APAC into 2 sub-regional meetings (East Asia vs Australia/Pacific)
  - Option 2: Record Americas meeting, share async with APAC (not live)
  - Option 3: Have APAC team attend at 8pm SGT (late evening, not ideal)

Output: "Cannot schedule single APAC meeting in all participants' business hours. Options: [Split meeting] [Async recording] [Late evening for APAC team]"
```

---

## Hero Prompt 7: Collaboration Discovery (collaborate-1)

**Prompt**: "Who are the people I collaborate with the most? Show me how much time I spend with each person."

**Capabilities Required**: Collaboration pattern analysis, time aggregation, attendee analysis, data visualization

### Canonical Task Decomposition: **8 Tasks**

#### Task 1: Natural Language Understanding (CAN-04)
- **Purpose**: Extract collaboration analysis intent
- **Input**: User query requesting collaboration patterns and time metrics
- **Output**: Intent classification (analyze collaborators + quantify time), metrics ("most", "time per person")
- **Tier**: Universal (Tier 1)

#### Task 2: Calendar Events Retrieval (CAN-01)
- **Purpose**: Load historical calendar events for collaboration analysis
- **Input**: Time range (typically 3-6 months for meaningful patterns)
- **Output**: Historical meeting events with attendees
- **Tier**: Universal (Tier 1)

#### Task 3: Meeting Metadata Extraction (CAN-07)
- **Purpose**: Extract attendee information from all meetings
- **Input**: Historical calendar events from CAN-01
- **Output**: Attendee lists for each meeting with participant details
- **Tier**: Common (Tier 2)

#### Task 4: Meeting Attendees Analysis (CAN-05)
- **Purpose**: Analyze attendee participation across all meetings
- **Input**: Attendee lists from CAN-07
- **Output**: Per-person meeting frequency, co-attendance patterns
- **Tier**: Universal (Tier 1)
- **Dependencies**: Requires CAN-07 (Metadata Extraction)

#### Task 5: Work Attribution Discovery (CAN-22)
- **Purpose**: Identify collaboration relationships and work patterns
- **Input**: Attendee co-occurrence data from CAN-05
- **Output**: Collaboration graph, frequent collaborator identification
- **Tier**: Common (Tier 2)
- **Note**: "Who I collaborate with most" requires relationship discovery

#### Task 6: Meeting Summarization (CAN-10)
- **Purpose**: Aggregate time spent per collaborator
- **Input**: Meeting durations, attendee data from CAN-05
- **Output**: Time metrics per person ("Sarah: 15 hours", "Team X: 20 hours")
- **Tier**: Common (Tier 2)

#### Task 7: Data Visualization (CAN-20)
- **Purpose**: Create visual representation of collaboration patterns
- **Input**: Collaborator rankings from CAN-22, time metrics from CAN-10
- **Output**: Charts/graphs showing top collaborators and time distribution
- **Tier**: Specialized (Tier 3)
- **Note**: "Show me" keyword triggers visualization

#### Task 8: Meeting Insights & Recommendations (CAN-14)
- **Purpose**: Generate insights about collaboration patterns
- **Input**: Collaboration analysis from CAN-22, time data from CAN-10
- **Output**: Insights ("Top 5 collaborators account for 60% of meeting time")
- **Tier**: Common (Tier 2)

**Evaluation Criteria**:
- Collaborator identification accuracy
- Time aggregation correctness
- Visualization clarity
- Insight quality

### Execution Composition

**How Tasks Work Together to Answer the Prompt:**

```
STEP 1: Understand Collaboration Analysis Intent
CAN-04 (NLU) → Extract: "who are the people I collaborate with most", "show how much time I spend with each person"
→ Intent: Collaboration discovery + time quantification + visualization

STEP 2: Retrieve Historical Meeting Data
CAN-01 (Calendar Retrieval) → Load 3-6 months of past meetings (sufficient for pattern detection)

STEP 3: Extract Attendee Information
CAN-07 (Metadata Extraction) → For each meeting, extract:
  - Attendee list (email addresses, names)
  - Meeting duration
  - Meeting date/time
  - Meeting subject (context for collaboration type)

STEP 4: Analyze Attendee Participation
CAN-05 (Attendees Analysis) → Calculate per-person metrics:
  - Meeting frequency with each person (count)
  - Co-attendance patterns (1:1 vs group meetings)
  - Categorize participants: directs, peers, executives, external
  - Result: Ranked list of people by meeting frequency

STEP 5: Discover Collaboration Relationships
CAN-22 (Work Attribution) → Build collaboration graph:
  - Identify frequent collaborators (e.g., ≥ 5 meetings in period)
  - Detect collaboration clusters (people who often meet together)
  - Distinguish direct collaboration (1:1s) vs team collaboration (group meetings)
  - Result: Top N collaborators with relationship context

STEP 6: Aggregate Time per Person
CAN-10 (Meeting Summarization) → Calculate time metrics:
  - Total hours with each person
  - Average meeting duration with each person
  - Breakdown: 1:1 time vs group meeting time
  - Example: "Sarah: 15 hours total (10 hours in 1:1s, 5 hours in group meetings)"

STEP 7: Visualize Collaboration Patterns
CAN-20 (Data Visualization) → Create visuals:
  - Bar chart: Top 10 collaborators by total hours
  - Pie chart: Time distribution across top collaborators
  - Heatmap: Meeting frequency over time (trending)
  - Network graph: Collaboration clusters

STEP 8: Generate Insights
CAN-14 (Insights & Recommendations) → Synthesize findings:
  - "Top 5 collaborators: Sarah (15 hrs), Mike (12 hrs), Product Team (20 hrs), CEO (8 hrs), Customer X (10 hrs)"
  - "65% of meeting time with top 5 collaborators"
  - "Heaviest collaboration: Product Team (20 group meetings)"
  - "Most 1:1 time: Sarah (10 hours across 20 meetings)"

OUTPUT: Comprehensive collaboration report with:
  1. WHO: Ranked list of top collaborators
  2. HOW MUCH: Time spent with each (total + 1:1 vs group breakdown)
  3. VISUALIZATION: Charts showing patterns
  4. INSIGHTS: Key patterns and trends
```

**Key Orchestration Patterns**:
- **Historical Analysis**: All tasks operate on PAST data (3-6 months lookback)
- **Metadata Dependency**: CAN-07 must complete before CAN-05 (need attendee lists to analyze participation)
- **Parallel Analysis**: CAN-22 (collaboration discovery) and CAN-10 (time aggregation) can run in parallel after CAN-05
- **Synthesis Layer**: CAN-20 (visualization) and CAN-14 (insights) consume outputs from both CAN-22 and CAN-10

**Example Flow - Collaboration Discovery**:
```
Input: "Who are the people I collaborate with the most? Show me how much time I spend with each person."

CAN-04: Extract → analyze collaborators + quantify time + visualize ✓
CAN-01: Load → Last 6 months (120 meetings total) ✓
CAN-07: Extract attendees →
  - Meeting 1: [User, Sarah] (30min)
  - Meeting 2: [User, Sarah, Mike, Product Team (5 people)] (60min)
  - Meeting 3: [User, CEO] (30min)
  - ... (117 more meetings)
  - Total: 120 meetings with 45 unique people
CAN-05: Analyze participation →
  - Sarah: 25 meetings (20 1:1s, 5 group)
  - Product Team: 20 meetings (all group, 8-10 people each)
  - Mike: 18 meetings (10 1:1s, 8 group)
  - CEO: 12 meetings (6 1:1s, 6 group)
  - Customer X: 10 meetings (all external)
  - ... (40 other people with <10 meetings each)
CAN-22: Discover relationships →
  - Top collaborators: Sarah, Mike, Product Team, CEO, Customer X
  - Collaboration cluster: Product Team meetings often include Sarah + Mike
  - 1:1 relationships: Sarah (primary), Mike (secondary), CEO (executive check-ins)
CAN-10: Aggregate time →
  - Sarah: 15 hours (20*30min 1:1s + 5*60min group)
  - Product Team: 20 hours (20*60min group meetings)
  - Mike: 12 hours (10*30min 1:1s + 8*60min group)
  - CEO: 8 hours (6*60min 1:1s + 6*30min group)
  - Customer X: 10 hours (10*60min external meetings)
  - Others: 35 hours (45 people combined)
  - Total meeting time: 100 hours
CAN-20: Visualize →
  - Bar chart showing: Product Team (20h) > Sarah (15h) > Mike (12h) > Customer X (10h) > CEO (8h)
  - Pie chart: Top 5 = 65 hours (65%), Others = 35 hours (35%)
CAN-14: Generate insights →
  - "Top 5 collaborators consume 65% of your meeting time"
  - "Product Team: Highest total time (20 hours in group settings)"
  - "Sarah: Most frequent 1:1 partner (20 meetings, 15 hours)"
  - "Long-tail: 40 people account for only 35% of time (infrequent collaborators)"

Output:
"TOP COLLABORATORS (Last 6 Months):
 1. Product Team: 20 hours (20 group meetings)
 2. Sarah: 15 hours (20 1:1s, 5 group meetings)
 3. Mike: 12 hours (10 1:1s, 8 group meetings)
 4. Customer X: 10 hours (10 external meetings)
 5. CEO: 8 hours (6 1:1s, 6 group meetings)
 
 Insight: Top 5 collaborators account for 65% of your meeting time (65 of 100 hours)"

[Bar chart visualization showing time distribution]
```

---

## Hero Prompt 8: Meeting Context Retrieval (collaborate-2)

**Prompt**: "Pull up all the meetings with Alex from last month and show me what we discussed."

**Capabilities Required**: Meeting search, participant filtering, content summarization, context retrieval

### Canonical Task Decomposition: **7 Tasks**

#### Task 1: Natural Language Understanding (CAN-04)
- **Purpose**: Extract search criteria (participant, timeframe, content request)
- **Input**: User query requesting meeting retrieval and discussion summary
- **Output**: Search params {participant: "Alex", timeframe: "last month", content_type: "discussions"}
- **Tier**: Universal (Tier 1)

#### Task 2: Calendar Events Retrieval (CAN-01)
- **Purpose**: Retrieve meetings matching search criteria
- **Input**: Time range (last month), participant filter ("Alex")
- **Output**: Array of meetings with Alex from last month
- **Tier**: Universal (Tier 1)

#### Task 3: Meeting Metadata Extraction (CAN-07)
- **Purpose**: Extract meeting details for context
- **Input**: Filtered meetings from CAN-01
- **Output**: Meeting titles, agendas, participants, timestamps, notes
- **Tier**: Common (Tier 2)

#### Task 4: Meeting Documentation Retrieval (CAN-08)
- **Purpose**: Retrieve meeting notes, agendas, attached documents
- **Input**: Meeting IDs from CAN-01, references from CAN-07
- **Output**: Meeting notes, shared documents, action items
- **Tier**: Common (Tier 2)
- **Dependencies**: Requires CAN-07 (Metadata Extraction)
- **Note**: "What we discussed" requires content retrieval

#### Task 5: Meeting Summarization (CAN-10)
- **Purpose**: Summarize discussion topics across all meetings with Alex
- **Input**: Meeting notes and agendas from CAN-08
- **Output**: Discussion summaries per meeting and aggregate themes
- **Tier**: Common (Tier 2)

#### Task 6: Data Visualization (CAN-20)
- **Purpose**: Present meetings and discussions in organized view
- **Input**: Meetings from CAN-01, summaries from CAN-10
- **Output**: Timeline view or grouped display of meetings with summaries
- **Tier**: Specialized (Tier 3)
- **Note**: "Show me" keyword triggers visual presentation

#### Task 7: Meeting Insights & Recommendations (CAN-14)
- **Purpose**: Identify recurring themes or follow-up needs
- **Input**: Discussion summaries from CAN-10, meeting metadata from CAN-07
- **Output**: Insights ("3 meetings focused on Q4 planning, 1 action item pending")
- **Tier**: Common (Tier 2)

**Evaluation Criteria**:
- Meeting retrieval accuracy (precision/recall for "meetings with Alex")
- Discussion summary quality
- Context completeness
- Presentation clarity

### Execution Composition

**How Tasks Work Together to Answer the Prompt:**

```
STEP 1: Parse Retrieval Request
CAN-04 (NLU) → Extract: "meetings with Alex", timeframe "last month", action "show what we discussed"
→ Intent: Meeting search + participant filter + content summarization

STEP 2: Retrieve Historical Meetings
CAN-01 (Calendar Retrieval) → Load all meetings from last month (30-day lookback)

STEP 3: Extract Attendee Information
CAN-07 (Metadata Extraction) → For each meeting, extract:
  - Attendee list
  - Meeting subject
  - Date/time
  - Meeting notes (if available)
  - Attachments/links

STEP 4: Filter Meetings by Participant
CAN-05 (Attendees Analysis) → Filter meetings where "Alex" was attendee:
  - Match "Alex" to actual participants (alex@company.com, Alex Johnson, etc.)
  - Identify all meetings with Alex present
  - Result: Subset of meetings (e.g., 8 out of 60 total meetings)

STEP 5: Retrieve Meeting Documentation
CAN-08 (Meeting Documentation) → For each Alex meeting, gather:
  - Meeting notes (OneNote, Outlook notes)
  - Email threads related to meeting
  - Shared documents attached to invite
  - Follow-up emails with action items

STEP 6: Summarize Each Meeting's Discussion
CAN-10 (Meeting Summarization) → For each Alex meeting, create summary:
  - Meeting date, subject, duration
  - Key topics discussed
  - Decisions made
  - Action items assigned
  - Example: "Mar 15 - Project X Kickoff (60min): Discussed scope, assigned Sarah as PM, decision to launch in Q2"

STEP 7: Visualize Meeting Timeline
CAN-20 (Data Visualization) → Present meetings in organized view:
  - Timeline view: Chronological list of all Alex meetings
  - Group by topic: If multiple meetings on same project
  - Visual summary: 8 meetings, 10 hours total time, 3 topics

STEP 8: Generate Insights
CAN-14 (Insights & Recommendations) → Identify patterns:
  - Recurring themes: "3 of 8 meetings focused on Project X (Q2 launch)"
  - Pending action items: "1 decision still pending: Budget approval"
  - Collaboration intensity: "Weekly cadence (2 meetings/week)"

OUTPUT: Comprehensive meeting context report:
  - LIST: All meetings with Alex from last month (8 meetings)
  - SUMMARIES: What was discussed in each meeting
  - TIMELINE: Chronological view of collaboration
  - INSIGHTS: Patterns, themes, pending items
```

**Key Orchestration Patterns**:
- **Search & Filter**: CAN-01 (retrieve all) → CAN-07 (extract metadata) → CAN-05 (filter by participant)
- **Content Enrichment**: CAN-08 retrieves documentation for EACH filtered meeting
- **Parallel Summarization**: CAN-10 can summarize each meeting independently
- **Presentation Layer**: CAN-20 (visualization) and CAN-14 (insights) consume all summaries

**Example Flow - Meeting Context Retrieval**:
```
Input: "Pull up all the meetings with Alex from last month and show me what we discussed."

CAN-04: Extract → participant: "Alex", timeframe: "last month", action: "show discussions" ✓
CAN-01: Load → Last 30 days (60 meetings total) ✓
CAN-07: Extract metadata for all 60 meetings →
  - Meeting 1: [User, Sarah, Mike] (no Alex)
  - Meeting 2: [User, Alex Johnson] (Alex found!) ✓
  - Meeting 3: [User, Product Team (8 people including alex@company.com)] (Alex found!) ✓
  - ... (58 more meetings, 6 more with Alex)
CAN-05: Filter by participant "Alex" →
  - Matched: alex@company.com, Alex Johnson
  - Filtered: 8 meetings (out of 60 total)
  - Meetings: Mar 1, Mar 4, Mar 8, Mar 11, Mar 15, Mar 18, Mar 22, Mar 29
CAN-08: Retrieve documentation for 8 Alex meetings →
  - Mar 1: Email thread (3 emails), Meeting notes in OneNote
  - Mar 4: Shared deck (ProjectX_Proposal.pptx)
  - Mar 8: No additional docs
  - Mar 11: Action item tracker (Excel)
  - Mar 15: Meeting notes + decision log
  - Mar 18: Email follow-up with questions
  - Mar 22: Shared design mockups (Figma link)
  - Mar 29: Meeting notes + next steps
CAN-10: Summarize each meeting →
  1. Mar 1 - "Project X Kickoff" (60min): Discussed scope, timeline, team assignments. Decision: Go/No-Go in 2 weeks.
  2. Mar 4 - "Proposal Review" (30min): Reviewed deck, Alex provided budget feedback, requested more market data.
  3. Mar 8 - "Quick Sync" (15min): Status check, no major updates.
  4. Mar 11 - "Action Item Review" (30min): Closed 5 of 7 tasks, 2 pending (budget approval, legal review).
  5. Mar 15 - "Go Decision Meeting" (60min): APPROVED Project X for Q2 launch. Sarah assigned as PM.
  6. Mar 18 - "Q&A Session" (30min): Alex had questions on resourcing, clarified dev team allocation.
  7. Mar 22 - "Design Review" (45min): Reviewed mockups, Alex approved direction, requested accessibility audit.
  8. Mar 29 - "Sprint Planning" (60min): Planned first 2 sprints, set Q2 milestones.
CAN-20: Visualize →
  - Timeline view: 8 meetings from Mar 1-29 (roughly weekly cadence)
  - Topic grouping: All 8 meetings related to "Project X"
  - Total time: 5 hours invested with Alex
CAN-14: Generate insights →
  - "8 meetings with Alex in March, all focused on Project X"
  - "Key milestone: Project approved for Q2 launch (Mar 15)"
  - "Pending: 2 action items from Mar 11 (budget approval, legal review)"
  - "Next likely topic: Sprint execution and Q2 milestone tracking"

Output:
"MEETINGS WITH ALEX (Last Month - March 2025): 8 meetings, 5 hours total

1. Mar 1 - Project X Kickoff (60min)
   Discussed: Scope, timeline, team assignments
   Decision: Go/No-Go in 2 weeks

2. Mar 4 - Proposal Review (30min)
   Discussed: Budget, market data needs
   
3. Mar 8 - Quick Sync (15min)
   Status check

4. Mar 11 - Action Item Review (30min)
   Closed: 5 of 7 tasks
   Pending: Budget approval, legal review

5. Mar 15 - Go Decision (60min) ★ KEY MEETING
   DECISION: Approved Project X for Q2 launch
   Assigned: Sarah as PM

6. Mar 18 - Q&A Session (30min)
   Discussed: Resourcing, dev team allocation

7. Mar 22 - Design Review (45min)
   Discussed: UI mockups, accessibility requirements
   Decision: Approved design direction

8. Mar 29 - Sprint Planning (60min)
   Discussed: Sprint 1-2 plans, Q2 milestones

INSIGHT: All 8 meetings focused on Project X progression from kickoff → approval → execution planning.
PENDING: 2 action items from Mar 11 still open (budget approval, legal review)"

[Timeline visualization showing weekly meetings Mar 1-29]
```

---

## Hero Prompt 9: Executive Meeting Preparation (collaborate-3)

**Prompt**: "I have a 1:1 with my VP next week - help me prepare by pulling together recent updates, pending decisions, and anticipated objections."

**Capabilities Required**: Meeting preparation, context aggregation, decision tracking, risk anticipation, content generation

### Canonical Task Decomposition: **11 Tasks**

#### Task 1: Natural Language Understanding (CAN-04)
- **Purpose**: Extract preparation requirements (meeting context, prep materials needed)
- **Input**: User query requesting comprehensive meeting prep
- **Output**: Meeting type ("1:1 with VP"), timeframe ("next week"), prep needs ["recent updates", "pending decisions", "anticipated objections"]
- **Tier**: Universal (Tier 1)

#### Task 2: Calendar Events Retrieval (CAN-01)
- **Purpose**: Retrieve the VP 1:1 meeting and related context
- **Input**: Time range (next week), participant filter ("VP")
- **Output**: Target meeting details
- **Tier**: Universal (Tier 1)

#### Task 3: Meeting Metadata Extraction (CAN-07)
- **Purpose**: Extract meeting details for context
- **Input**: VP 1:1 meeting from CAN-01
- **Output**: Meeting time, attendees, agenda (if exists), previous notes
- **Tier**: Common (Tier 2)

#### Task 4: Meeting Documentation Retrieval (CAN-08)
- **Purpose**: Retrieve relevant documents, previous meeting notes, action items
- **Input**: VP relationship history, meeting references from CAN-07
- **Output**: Past 1:1 notes, action items, related documents
- **Tier**: Common (Tier 2)
- **Dependencies**: Requires CAN-07 (Metadata Extraction)

#### Task 5: Work Attribution Discovery (CAN-22)
- **Purpose**: Identify recent work and projects relevant to VP
- **Input**: User's calendar/work history, VP's areas of responsibility
- **Output**: Recent projects, initiatives, team activities to report
- **Tier**: Common (Tier 2)
- **Note**: "Recent updates" requires discovering what work to report

#### Task 6: Meeting Attendees Analysis (CAN-05)
- **Purpose**: Understand VP's priorities and focus areas
- **Input**: VP's calendar, organizational context
- **Output**: VP's current priorities, concerns, strategic focus
- **Tier**: Universal (Tier 1)
- **Dependencies**: Requires CAN-07 (Metadata Extraction)

#### Task 7: Meeting Type Classification (CAN-02A)
- **Purpose**: Classify meeting as executive 1:1 to apply appropriate prep templates
- **Input**: Meeting metadata from CAN-07
- **Output**: Meeting type classification ("Executive 1:1")
- **Tier**: Universal (Tier 1)

#### Task 8: Content Generation (CAN-09)
- **Purpose**: Generate structured meeting prep document
- **Input**: Recent updates (CAN-22), decisions (CAN-08), VP context (CAN-05)
- **Output**: Prep document with sections (Updates, Decisions Needed, Discussion Topics)
- **Tier**: Common (Tier 2)
- **Dependencies**: Requires CAN-07 (Metadata Extraction)

#### Task 9: Objection/Risk Anticipation (CAN-18)
- **Purpose**: Anticipate VP's potential objections or concerns
- **Input**: Recent updates (CAN-22), VP priorities (CAN-05), organizational context
- **Output**: Anticipated objections with mitigation strategies
- **Tier**: Specialized (Tier 3)
- **Note**: "Anticipated objections" explicitly requires risk analysis

#### Task 10: Meeting Insights & Recommendations (CAN-14)
- **Purpose**: Provide strategic recommendations for the 1:1
- **Input**: All prep materials (CAN-08, CAN-09, CAN-18), VP context (CAN-05)
- **Output**: Recommendations ("Lead with project X win", "Defer topic Y to later meeting")
- **Tier**: Common (Tier 2)

#### Task 11: Meeting Summarization (CAN-10)
- **Purpose**: Create executive summary of prep materials
- **Input**: Full prep document from CAN-09, recommendations from CAN-14
- **Output**: Concise prep brief (1-page summary)
- **Tier**: Common (Tier 2)

**Evaluation Criteria**:
- Prep material completeness (all requested sections present)
- Update relevance and accuracy
- Objection anticipation quality
- Actionability of recommendations
- Document organization and clarity

### Execution Composition

**How Tasks Work Together to Answer the Prompt:**

```
STEP 1: Understand Preparation Needs
CAN-04 (NLU) → Extract: "1:1 with VP", timeframe "next week", prep needs ["recent updates", "pending decisions", "anticipated objections"]
→ Intent: Comprehensive executive meeting prep (3 distinct content requirements)

STEP 2: Locate Target Meeting
CAN-01 (Calendar Retrieval) → Load next week's calendar
Filter: Find 1:1 meeting with VP (identify VP from org structure)

STEP 3: Extract Meeting Context
CAN-07 (Metadata Extraction) → From VP 1:1 meeting:
  - Meeting time, duration
  - Existing agenda (if any)
  - Previous meeting notes (last 1:1 with VP)

STEP 4: Classify Meeting Type
CAN-02A (Meeting Type) → Classify as "Executive 1:1"
→ Triggers executive prep template (not standard meeting prep)

STEP 5: Gather Historical Context
CAN-08 (Meeting Documentation) → Retrieve VP relationship history:
  - Previous 1:1 notes (last 2-3 meetings)
  - Action items from past 1:1s (status?)
  - Decisions pending from previous meetings
  - Email threads with VP

STEP 6A: Discover Recent Work Updates (Prep Need #1)
CAN-22 (Work Attribution) → Identify recent accomplishments to report:
  - Projects completed since last 1:1
  - Key milestones achieved
  - Team wins or customer successes
  - Problems resolved
  - Result: "Recent Updates" section (5-7 bullet points)

STEP 6B: Understand VP's Context (For Anticipation)
CAN-05 (Attendees Analysis) → Analyze VP's current priorities:
  - VP's calendar (what they're focused on)
  - Organizational priorities (strategic context)
  - VP's recent communications (all-hands, emails)
  - Result: VP priority landscape

STEP 7: Generate Prep Document (Prep Need #2)
CAN-09 (Content Generation) → Create structured prep brief:
  - Section 1: Recent Updates (from CAN-22)
  - Section 2: Pending Decisions (from CAN-08 action items)
  - Section 3: Discussion Topics (inferred from context)
  - Section 4: Questions for VP
  - Format: Executive-friendly (bullets, concise)

STEP 8: Anticipate Objections (Prep Need #3)
CAN-18 (Objection/Risk Anticipation) → For each update/decision:
  - Identify potential VP concerns based on their priorities (CAN-05)
  - Anticipate questions VP might ask
  - Prepare mitigation strategies
  - Example: "Update: Delayed feature X → Anticipated objection: Impact on Q2 revenue → Mitigation: Alternative feature Y delivers same value"

STEP 9: Generate Strategic Recommendations
CAN-14 (Insights & Recommendations) → Provide tactical advice:
  - What to lead with (highest impact update)
  - What to defer (low-priority topics)
  - How to frame decisions (aligned with VP priorities)
  - Sensitive topics to handle carefully

STEP 10: Create Executive Summary
CAN-10 (Meeting Summarization) → Condense prep into 1-page brief:
  - Top 3 updates to highlight
  - 2 decisions needing VP input
  - Key anticipated objection with mitigation
  - Recommended meeting flow

OUTPUT: Comprehensive executive prep package:
  1. EXECUTIVE SUMMARY (1-page brief)
  2. RECENT UPDATES (detailed list with context)
  3. PENDING DECISIONS (what needs VP approval)
  4. ANTICIPATED OBJECTIONS (with mitigations)
  5. STRATEGIC RECOMMENDATIONS (meeting tactics)
  6. SUPPORTING MATERIALS (links to docs, previous notes)
```

**Key Orchestration Patterns**:
- **Parallel Content Discovery**: CAN-22 (work updates), CAN-08 (historical decisions), CAN-05 (VP context) run independently
- **Content Generation Synthesis**: CAN-09 consumes outputs from CAN-22, CAN-08, CAN-05
- **Risk Layer**: CAN-18 operates on CAN-09 output to add objection anticipation
- **Recommendation Layer**: CAN-14 synthesizes ALL prior outputs to provide strategic guidance
- **Executive Summary**: CAN-10 distills everything into concise brief

**Example Flow - Executive Meeting Prep**:
```
Input: "I have a 1:1 with my VP next week - help me prepare by pulling together recent updates, pending decisions, and anticipated objections."

CAN-04: Extract → Meeting: "1:1 with VP", timeframe: "next week", prep needs: [updates, decisions, objections] ✓
CAN-01: Load → Next week calendar → Found: "1:1 with VP Sarah" (Tue 2pm, 60min) ✓
CAN-07: Extract meeting context →
  - Last 1:1: 2 weeks ago
  - Previous notes: Discussed Q2 roadmap, VP asked for update on Feature X delay
  - No current agenda set
CAN-02A: Classify → "Executive 1:1" (triggers exec prep template) ✓
CAN-08: Retrieve documentation →
  - Previous 1:1 notes (last 3 meetings)
  - Action items from last meeting: 
    1. "Assess Feature X delay impact" (status: completed)
    2. "Hire senior engineer" (status: in progress)
    3. "Proposal for budget increase" (status: pending VP approval)
  - Email threads: 2 emails from VP asking about hiring timeline

CAN-22: Discover recent updates →
  - Completed: Feature Y launched (2 days ago, positive customer feedback)
  - Completed: Closed 3 critical bugs from last sprint
  - Milestone: Hired 2 engineers (senior role still open)
  - Win: Customer X renewed contract (attributed to Feature Y)
  - Problem resolved: Performance issue fixed (99.9% uptime restored)

CAN-05: Analyze VP context →
  - VP's priorities (from all-hands): Q2 revenue target, product quality, team growth
  - VP's calendar: Heavy focus on customer escalations this week
  - Organizational context: Board meeting next month (VP will report on roadmap)
  - Result: VP is pressure-focused on Q2 execution and customer satisfaction

CAN-09: Generate prep document →
  SECTION 1: RECENT UPDATES
  - Feature Y launched successfully (tied to Customer X renewal - $500K ARR)
  - Resolved performance issue (99.9% uptime restored)
  - Hired 2 engineers (team now at 85% capacity)
  - Closed 3 critical bugs (quality improvement)
  
  SECTION 2: PENDING DECISIONS
  - Budget increase proposal for senior engineer hire (needs VP approval)
  - Feature X delay mitigation plan (defer to Q3 vs cut scope?)
  
  SECTION 3: DISCUSSION TOPICS
  - Q2 roadmap adjustments (given Feature X delay)
  - Hiring pipeline update (senior role)

CAN-18: Anticipate objections →
  Update: "Feature Y launched" → Anticipated objection: "What about Feature X delay from last meeting?" 
    → Mitigation: "Feature X delayed to Q3, but Feature Y delivered equivalent customer value (Customer X renewal proof)"
  
  Update: "Hired 2 engineers" → Anticipated objection: "Why is senior role still open after 3 weeks?"
    → Mitigation: "5 candidates in pipeline, final round interviews this week, expect offer next week"
  
  Decision: "Budget increase" → Anticipated objection: "Why need more budget when hiring is behind?"
    → Mitigation: "Market rate for senior role higher than budgeted, need $20K increase to close top candidate"

CAN-14: Strategic recommendations →
  - LEAD WITH: Customer X renewal (ties to VP's revenue priority) + Feature Y success
  - FRAME POSITIVELY: Feature X delay offset by Feature Y impact (not apologetic)
  - DEFER: Bug fixes (too tactical for exec 1:1, mention briefly)
  - BE READY FOR: Hiring pressure (VP will ask, have concrete timeline)
  - ASK VP: Guidance on Q2 roadmap trade-offs (make VP feel involved in decision)

CAN-10: Create executive summary →
  "1:1 PREP BRIEF - VP Sarah (Tue 2pm)
  
  TOP 3 HIGHLIGHTS:
  1. Feature Y → Customer X renewal ($500K ARR) - Q2 revenue win
  2. 2 engineers hired (team growing, senior role in final interviews)
  3. Performance issue resolved (99.9% uptime)
  
  DECISIONS NEEDED:
  1. Budget increase for senior hire (+$20K)
  2. Feature X: Defer to Q3 or cut scope?
  
  ANTICIPATED PRESSURE POINT:
  - Feature X delay status → Mitigation: Feature Y delivered equivalent value
  
  MEETING FLOW:
  1. Lead with Customer X win (revenue focus)
  2. Transition to hiring update (concrete timeline)
  3. Request budget decision (specific ask)
  4. Discuss Q2 roadmap trade-offs (collaborative tone)"

OUTPUT (Delivered to User):
"EXECUTIVE PREP PACKAGE - 1:1 with VP Sarah (Next Tue 2pm)

═══════════════════════════════════════════════════════
EXECUTIVE SUMMARY (Read this first)
═══════════════════════════════════════════════════════
TOP HIGHLIGHTS:
✓ Feature Y launched → Customer X renewed ($500K ARR)
✓ 2 engineers hired, senior role in final round
✓ Performance restored to 99.9% uptime

DECISIONS NEEDED:
→ Budget increase for senior hire (+$20K above original budget)
→ Feature X timeline: Defer to Q3 vs cut scope?

ANTICIPATED OBJECTION:
VP will ask about Feature X delay (mentioned in last 1:1)
MITIGATION: Feature Y delivered equivalent customer value (Customer X renewal proof)

RECOMMENDED FLOW:
1. Lead with Customer X renewal (ties to VP's Q2 revenue focus)
2. Hiring update (concrete timeline calms VP concern)
3. Request budget approval (specific ask)
4. Collaborative roadmap discussion

═══════════════════════════════════════════════════════
RECENT UPDATES (Detailed)
═══════════════════════════════════════════════════════
1. CUSTOMER WIN: Feature Y → Customer X Renewal
   - Launched 2 days ago
   - Customer X cited Feature Y in renewal decision
   - $500K ARR retained (Q2 revenue target contribution)
   - Positive feedback from 3 other customers

2. TEAM GROWTH: 2 Engineers Hired
   - Filled 2 of 3 open roles
   - Team now at 85% capacity (up from 70%)
   - Senior role: 5 candidates, final interviews this week, expect offer next week

3. QUALITY IMPROVEMENT: Performance Issue Resolved
   - 99.9% uptime restored (was 97% last week)
   - Root cause: Database index optimization
   - Closed 3 critical bugs from last sprint

4. FEATURE X STATUS:
   - Delayed to Q3 (technical complexity underestimated)
   - Impact mitigated by Feature Y success

═══════════════════════════════════════════════════════
PENDING DECISIONS (Need VP Input)
═══════════════════════════════════════════════════════
1. BUDGET INCREASE REQUEST:
   - What: $20K increase for senior engineer role
   - Why: Market rate higher than original budget
   - Impact: Needed to close top candidate (offer expected next week)
   - Decision: Approve $20K increase?

2. FEATURE X ROADMAP:
   - Options: (A) Defer to Q3, (B) Cut scope to fit Q2
   - Trade-off: Quality vs timeline
   - Decision: VP preference on approach?

═══════════════════════════════════════════════════════
ANTICIPATED OBJECTIONS (With Mitigations)
═══════════════════════════════════════════════════════
OBJECTION #1: "What about Feature X delay you mentioned last meeting?"
MITIGATION: "Feature Y delivered equivalent customer value - Customer X renewed specifically citing Feature Y. We de-prioritized Feature X when we saw Feature Y resonating more."

OBJECTION #2: "Why is senior hire still open after 3 weeks?"
MITIGATION: "5 strong candidates in pipeline, final round this week. The delay is because we're holding out for senior/principal level (not settling for mid-level). Expect offer next week."

OBJECTION #3: "Why need more budget when you're behind on hiring?"
MITIGATION: "Original budget was $140K, but market rate for senior/principal is $160K. We can close top candidate (10 years experience, led teams at Big Tech) with the $20K increase. Without it, we risk losing to competing offers."

═══════════════════════════════════════════════════════
STRATEGIC RECOMMENDATIONS
═══════════════════════════════════════════════════════
✓ LEAD WITH Customer X renewal (ties to VP's Q2 revenue priority)
✓ FRAME Feature X positively (not apologetic - we pivoted to higher value)
✓ BE CONCRETE on hiring timeline (VP will pressure, have specific dates)
✓ MAKE VP FEEL INVOLVED (ask for guidance on roadmap trade-offs)
✓ DEFER tactical details (bug fixes - mention briefly, don't dwell)

TONE: Confident, data-driven, collaborative

═══════════════════════════════════════════════════════
SUPPORTING MATERIALS
═══════════════════════════════════════════════════════
- Previous 1:1 notes (link)
- Feature Y launch metrics (link)
- Customer X renewal email (link)
- Budget proposal doc (link)
- Hiring pipeline tracker (link)"
```

---

## Appendix: GPT-5 Optimization & Validation Experiment

### Experiment Overview

**Date**: November 7, 2025  
**Objective**: Optimize GPT-5 prompts and validate performance with 3-trial stability test  
**Scope**: All 9 Calendar.AI hero prompts analyzed for canonical task decomposition  
**Full Report**: [GPT5_OPTIMIZATION_SUMMARY.md](model_comparison/GPT5_OPTIMIZATION_SUMMARY.md)

### Experimental Design

#### Phase 1: Baseline Analysis (Nov 6, 2025)
- **Method**: GPT-5 analyzed 9 hero prompts using initial prompts
- **Performance**: F1 79.74% (single run, no variance data)
- **Gaps Identified**:
  - CAN-07 (Metadata Extraction): Only 55.6% detection (5/9 prompts)
  - CAN-23 (Conflict Resolution): 0% detection (0/9 prompts)
  - CAN-22 (Work Attribution): 11% detection (1/9 prompts)

#### Phase 2: Prompt Optimization (Nov 7, 2025)
Enhanced GPT-5 system and user prompts with **6 critical improvements**:

1. **CAN-07 Parent Task Guidance**:
   - Added explicit keywords: "pending invitations", "RSVP", "attendees", "documents", "prep materials"
   - Listed child tasks: CAN-13, CAN-05, CAN-08, CAN-09, CAN-19, CAN-21
   - **Impact**: CAN-07 detection 55.6% → 100% (+44.4%)

2. **CAN-02A vs CAN-02B Differentiation**:
   - CAN-02A: OBJECTIVE type classification (1:1, team sync, customer)
   - CAN-02B: SUBJECTIVE importance assessment (strategic value, urgency)
   - Guidance: "Use BOTH when prompt asks about 'prioritize' + 'which meetings'"

3. **CAN-13 vs CAN-07 Read/Write Distinction**:
   - CAN-13: WRITE operations (SEND response, UPDATE status)
   - CAN-07: READ operations (EXTRACT/READ RSVP status)
   - Clear mapping: "Pending invitations" = CAN-07, "Respond to invitations" = CAN-13

4. **Specialized Task Keywords**:
   - CAN-18: "anticipate", "risks", "objections", "blockers", "prepare for pushback"
   - CAN-20: "show", "visualize", "dashboard", "patterns", "trends", "display"
   - CAN-23: "auto-reschedule", "bump", "prioritize conflicts", "resolve"
   - **Impact**: CAN-23 detection 0% → 66.7% (+66.7%)

5. **DO/DON'T Guidelines** (9 total):
   - ✅ DO: Include CAN-04 (NLU) as step 1 for all prompts
   - ✅ DO: Use CAN-07 when prompt mentions invitations, RSVP, attendees
   - ✅ DO: Use BOTH CAN-02A and CAN-02B when prioritizing meetings
   - ❌ DON'T: Skip CAN-04, confuse CAN-07 with CAN-13, miss specialized tasks

6. **Dependency Chain Clarification**:
   - CAN-01 (Calendar Retrieval) → CAN-06 (Availability Checking)
   - CAN-07 (Metadata Extraction) → child tasks
   - CAN-12 (Constraint Satisfaction) → CAN-23 (Conflict Resolution)

#### Phase 3: 3-Trial Stability Test (Nov 7, 2025)
- **Method**: Ran GPT-5 on same 9 prompts × 3 independent trials
- **Total API Calls**: 27 (all successful, 100% success rate)
- **Analysis**: Compared each trial against gold standard, computed statistics

### Results Summary

#### Aggregate Performance (3-Trial Average)

| Metric | Mean | Std Dev | Assessment |
|--------|------|---------|------------|
| **F1 Score** | 78.40% | ±0.72% | EXCELLENT (< 1% variance) |
| **Precision** | 74.76% | ±0.25% | Very stable |
| **Recall** | 84.25% | ±1.79% | Good, moderate variance |
| **Consistency** | 93.6% | - | High task agreement |

#### Per-Trial Performance

| Trial | F1 | Precision | Recall | Status |
|-------|-----|-----------|--------|--------|
| **Trial 1** | 78.47% | 74.51% | 82.78% | ✅ Success |
| **Trial 2** | 77.48% | 74.51% | 80.65% | ✅ Success |
| **Trial 3** | 79.24% | 75.25% | 89.33% | ✅ Success |

**Variance Analysis**: F1 variance of 0.72% is well below the 2% EXCELLENT threshold, indicating highly stable performance.

#### Major Task Detection Improvements

| Task | Original | Optimized | Delta | Prompts |
|------|----------|-----------|-------|---------|
| **CAN-07** | 55.6% | 100% | **+44.4%** ⭐ | 9/9 |
| **CAN-23** | 0% | 66.7% | **+66.7%** ⭐ | 6/9 |
| **CAN-22** | 11% | 100%* | **+89%** ⭐ | 3/3 collaborate |
| **CAN-18** | 0% | 33.3% | **+33.3%** | 1/3 (collaborate-3) |
| **CAN-20** | 11% | 66.7% | **+55.7%** | 2/3 (organizer-3, collaborate-1) |

*CAN-22 appears in 3/9 prompts (all collaborate); achieved 100% detection in those prompts

#### Per-Prompt Stability

| Prompt | Avg F1 | Std Dev | Variance | Assessment |
|--------|--------|---------|----------|------------|
| organizer-1 | 74.2% | ±6.0% | HIGH | Needs review |
| organizer-2 | 85.7% | ±1.4% | LOW | Excellent |
| organizer-3 | 75.0% | ±0% | NONE | Perfect |
| schedule-1 | 76.2% | ±1.4% | LOW | Excellent |
| schedule-2 | 84.2% | ±1.4% | LOW | Excellent |
| schedule-3 | 69.2% | ±1.4% | LOW | Excellent |
| collaborate-1 | 75.0% | ±1.7% | LOW | Excellent |
| collaborate-2 | 71.4% | ±0% | NONE | Perfect |
| collaborate-3 | 94.4% | ±0.9% | LOW | Excellent |

**Note**: organizer-1 shows 6% variance - highest across all prompts. Potential area for further investigation.

### Statistical Validation

#### Stability Threshold Analysis
- **EXCELLENT**: F1 variance < 2% → **ACHIEVED** (0.72%)
- **GOOD**: F1 variance < 5% → ACHIEVED
- **ACCEPTABLE**: F1 variance < 10% → ACHIEVED

#### Consistency Score
- **Definition**: % of task selections that match across all 3 trials
- **Result**: 93.6% consistency
- **Interpretation**: Very high agreement in task selection across trials

#### Performance Comparison with Original
- **Original F1**: 79.74% (single run, no variance data)
- **Optimized F1**: 78.40% ± 0.72% (3-trial average with statistical rigor)
- **Delta**: -1.34% (within expected variance, statistically comparable)
- **Trade-off**: Slightly lower aggregate score for MAJOR gains in specialized task detection

### Key Findings

#### 1. Prompt Optimization Was Highly Successful
- Maintained overall F1 performance (within 1.34% of original)
- Dramatically improved specialized task detection (CAN-07, CAN-22, CAN-23)
- Achieved EXCELLENT stability (< 1% F1 variance)

#### 2. Specialized Tasks Benefited Most
Tasks that benefited from explicit keyword guidance:
- **CAN-07**: Parent task concept + keyword list → 100% detection
- **CAN-23**: Conflict resolution keywords → 66.7% detection (vs 0%)
- **CAN-22**: Work attribution in collaboration context → 100% in relevant prompts
- **CAN-20**: Visualization keywords ("show", "visualize") → 66.7% detection

#### 3. Universal Tasks Already Stable
- **CAN-04** (NLU): Maintained 100% detection (already in baseline)
- **CAN-01** (Calendar Retrieval): Maintained 100% detection
- **CAN-02A/B**: Maintained high detection with clearer differentiation

#### 4. Stability Validates Framework
- 93.6% consistency across trials validates framework robustness
- Low variance (< 1%) indicates prompts are deterministic
- Only organizer-1 shows elevated variance (6%) - worth investigating

### Conclusions

#### Optimization Success
The GPT-5 prompt optimization achieved all objectives:
1. ✅ **Maintained Performance**: F1 78.40% comparable to 79.74% baseline
2. ✅ **Improved Specialized Detection**: +44-89% gains on CAN-07, CAN-22, CAN-23
3. ✅ **Achieved Stability**: < 1% F1 variance across 3 trials (EXCELLENT)
4. ✅ **Validated Framework**: 93.6% consistency proves framework robustness

#### Framework Validation
The 24 canonical unit tasks framework is validated by:
- High consistency (93.6%) across independent trials
- Successful differentiation of similar tasks (CAN-02A vs CAN-02B, CAN-07 vs CAN-13)
- Complete coverage of all 9 hero prompts with 23/24 tasks
- Clear parent-child task relationships (CAN-07 → children)

#### Production Readiness
The optimized GPT-5 prompts are production-ready:
- EXCELLENT stability (< 1% variance)
- High accuracy (78.40% F1)
- Comprehensive task coverage
- Well-documented and reproducible

#### Future Work
1. **Investigate organizer-1 Variance**: 6% variance is elevated - review prompt sensitivity
2. **Claude Comparison**: Resume automated Claude testing (paused for API key)
3. **Fine-tuning**: Use gold standard as training data for model fine-tuning
4. **Framework Extension**: Consider additional specialized tasks based on new use cases

---

## Document Metadata

**Version**: 1.0  
**Created**: November 7, 2025  
**Author**: Chin-Yew Lin  
**Total Prompts**: 9  
**Total Tasks**: 24 (23 unique + CAN-02A/CAN-02B split)  
**Framework**: Calendar.AI Canonical Unit Tasks v2.0  
**Status**: ✅ Gold Standard Reference  

**Validation**:
- ✅ Human expert review (Chin-Yew Lin)
- ✅ Cross-referenced with original GUTT decompositions
- ✅ Validated against GPT-5 optimized outputs (3 trials)
- ✅ All 24 canonical tasks represented
- ✅ Consistent task application across all prompts

**Usage**:
This document serves as the authoritative reference for:
- LLM evaluation benchmarking
- Training data for model fine-tuning
- Framework validation and refinement
- Production system quality assurance
- Research and development

**Maintenance**:
- Update when canonical tasks framework evolves
- Add new hero prompts as they are created
- Incorporate learnings from production system performance
- Align with GUTT framework updates

---

*End of Document*
