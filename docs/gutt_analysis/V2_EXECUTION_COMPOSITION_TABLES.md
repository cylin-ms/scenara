# V2 Hero Prompts: Execution Composition Tables

**Document Version**: 1.0  
**Date**: November 8, 2025  
**Source**: V2_GOLD_STANDARD_REPORT.md - Execution Composition Sections  
**Purpose**: Quick reference showing how canonical tasks orchestrate to fulfill each hero prompt

---

## Organizer-1: "Keep my Calendar up to date by committing to only meetings that are part of my priorities."

| Step | Atomic Agent Capability |
|------|------------------------|
| **STEP 1: Understand User Intent** | **CAN-04 (Natural Language Understanding)** Extract intent and constraint |
| **STEP 2: Retrieve Pending Invitations** | **CAN-01 (Calendar Events Retrieval)** Load all pending calendar invitations |
| **STEP 3: Extract Meeting Details** | **CAN-07 (Meeting Metadata Extraction)** Extract comprehensive meeting information |
| **STEP 4-5: Classify Meetings (Parallel)** | **CAN-02 (Meeting Type Classification)** Classify by format |
|  | **CAN-03 (Meeting Importance Assessment)** Score strategic value |
| **STEP 6: Match Against User's Priorities** | **CAN-11 (Priority/Preference Matching)** Align meetings with user's known priorities |
| **STEP 7: Execute RSVP Actions** | **CAN-13 (RSVP Status Update)** Update calendar responses based on priority alignment |

**Tasks Used**: 7 (CAN-04, CAN-01, CAN-07, CAN-02, CAN-03, CAN-11, CAN-13)  
**F1 Score**: 100%

---

## Organizer-2: "Track all my important meetings and flag any that require focus time to prepare for them."

| Step | Atomic Agent Capability |
|------|------------------------|
| **STEP 1: Understand Tracking and Flagging Requirements** | **CAN-04 (NLU)** Extract dual intent |
| **STEP 2: Retrieve Upcoming Meetings** | **CAN-01 (Calendar Retrieval)** Load calendar for analysis period |
| **STEP 3: Extract Meeting Context** | **CAN-07 (Metadata Extraction)** Extract complexity indicators |
| **STEP 4-5: Classify and Score Meetings (Parallel)** | **CAN-02 (Meeting Type)** Classify by format |
|  | **CAN-03 (Importance Assessment)** Score strategic value |
| **STEP 6: Estimate Preparation Time** | **CAN-21 (Preparation Time Analysis)** Calculate prep time needed |
| **STEP 7: Filter to Important Meetings** | **CAN-11 (Priority Matching)** Select meetings to track |
| **STEP 8-9: Setup Tracking and Flagging (Parallel)** | **CAN-16 (Event Monitoring)** Configure change tracking |
|  | **CAN-25 (Event Annotation/Flagging)** Flag meetings needing prep (NEW TASK) |

**Tasks Used**: 9 (CAN-04, CAN-01, CAN-07, CAN-02, CAN-03, CAN-21, CAN-11, CAN-16, CAN-25)  
**F1 Score**: 100%  
**Note**: CAN-25 is a NEW canonical task validated in V2.0 for conditional event flagging

---

## Organizer-3: "Help me understand where I am spending my time and identify ways I can reclaim time to focus more on my top priorities."

| Step | Atomic Agent Capability |
|------|------------------------|
| **STEP 1: Understand Analysis Requirements** | **CAN-04 (NLU)** Extract dual intent |
| **STEP 2: Retrieve Meeting History** | **CAN-01 (Calendar Retrieval)** Load comprehensive meeting dataset |
| **STEP 3: Extract Meeting Details** | **CAN-07 (Metadata Extraction)** Extract classification signals |
| **STEP 4-5: Classify and Score Meetings (Parallel)** | **CAN-02 (Meeting Type)** Categorize by format |
|  | **CAN-03 (Importance Assessment)** Score strategic value |
| **STEP 6: Aggregate Time Patterns** | **CAN-10 (Time Aggregation)** Calculate time distribution statistics |
| **STEP 7: Match Against Priorities** | **CAN-11 (Priority Matching)** Analyze priority alignment |
| **STEP 8-9: Generate Insights and Visualizations (Parallel)** | **CAN-14 (Recommendation Engine)** Generate reclamation opportunities |
|  | **CAN-20 (Data Visualization)** Create visual dashboard |

**Tasks Used**: 9 (CAN-04, CAN-01, CAN-07, CAN-02, CAN-03, CAN-10, CAN-11, CAN-14, CAN-20)  
**F1 Score**: 100%  
**Note**: Most complex Organizer prompt - demonstrates full framework capabilities across all tiers

---

## Schedule-1: "Starting next week, I want a weekly 30-min 1:1 with {name}. Afternoons preferred, avoid Fridays. Automatically reschedule on declines or conflicts."

| Step | Atomic Agent Capability |
|------|------------------------|
| **STEP 1: Understand Scheduling Requirements** | **CAN-04 (NLU)** Extract scheduling constraints and automation preferences |
| **STEP 2: Resolve Attendee Identity** | **CAN-05 (Attendee Resolution)** Look up "{name}" in directory |
| **STEP 3: Retrieve Existing Calendar State** | **CAN-01 (Calendar Retrieval)** Load current calendar events |
| **STEP 4: Check Attendee Availability** | **CAN-06 (Availability Checking)** Find afternoon slots avoiding Friday |
| **STEP 5: Select Optimal Time Slot** | **CAN-12 (Constraint Satisfaction)** Apply preferences to select best time |
| **STEP 6: Generate Recurrence Rule** | **CAN-15 (Recurrence Rule Generation)** Create weekly RRULE pattern |
| **STEP 7: Create Recurring Meeting** | **CAN-03 (Event Creation)** Schedule meeting on both calendars |
| **STEP 8: Setup Change Monitoring** | **CAN-16 (Event Monitoring)** Configure webhooks for meeting changes |
| **STEP 9: Enable Automatic Rescheduling** | **CAN-17 (Auto-Reschedule)** Configure rescheduling workflow |

**Tasks Used**: 9 (CAN-04, CAN-05, CAN-01, CAN-06, CAN-12, CAN-15, CAN-03, CAN-16, CAN-17)  
**F1 Score**: 100%  
**Note**: Most specialized Schedule prompt - uses 3 Tier-3 tasks (CAN-15, CAN-16, CAN-17)

---

## Schedule-2: "Clear my Thursday afternoon. Update my RSVPs and help me reschedule my meetings to another time and show me as Out of Office."

| Step | Atomic Agent Capability |
|------|------------------------|
| **STEP 1: Understand Rescheduling Requirements** | **CAN-04 (NLU)** Parse multi-action request |
| **STEP 2: Retrieve Thursday Afternoon Meetings** | **CAN-01 (Calendar Retrieval)** Load meetings in target time block |
| **STEP 3: Extract Meeting Metadata** | **CAN-07 (Metadata Extraction)** Get detailed meeting information including attendee details |
| **STEP 4-5: Update RSVPs and Find Alternative Slots (Parallel)** | **CAN-13 (RSVP Status Update)** Decline or mark tentative |
|  | **CAN-06 (Availability Checking)** Find alternative times for rescheduling |
| **STEP 6: Select Best Alternative Times** | **CAN-12 (Constraint Satisfaction)** Apply preferences |
| **STEP 7: Generate Rescheduling Proposal** | **CAN-17 (Automatic Rescheduling)** Create rescheduling plan |
| **STEP 8: Update Calendar with New Times** | **CAN-03 (Event Creation/Update)** Execute rescheduling |

**Tasks Used**: 8 (CAN-04, CAN-01, CAN-07, CAN-13, CAN-06, CAN-12, CAN-17, CAN-03)  
**F1 Score**: 88.89% (Partial - originally missed CAN-06)  
**Critical Note**: CAN-05 (Attendee Resolution) NOT needed - attendee information already available from existing meetings via CAN-07

---

## Schedule-3: "Land a time to meet about Project Alpha with Chris, Sangya, and Kat for 1 hour in the next 2 weeks. Schedule over 1:1s and lunches if needed and work around Kat's schedule. Make the meeting in person and add a room."

| Step | Atomic Agent Capability |
|------|------------------------|
| **STEP 1: Understand Complex Scheduling Constraints** | **CAN-04 (NLU)** Parse multi-layered requirements |
| **STEP 2: Resolve All Attendees** | **CAN-05 (Attendee/Contact Resolution)** Look up Chris, Sangya, and Kat |
| **STEP 3: Retrieve All 3 Calendars** | **CAN-01 (Calendar Retrieval)** Load calendar events for next 2 weeks |
| **STEP 4: Extract Meeting Metadata** | **CAN-07 (Metadata Extraction)** Get detailed meeting information |
| **STEP 5-6: Classify and Assess Meetings (Parallel)** | **CAN-02 (Meeting Type Classification)** Categorize existing meetings |
|  | **CAN-03 (Importance Assessment)** Score meeting priority |
| **STEP 7: Check Availability with Priority Logic** | **CAN-06 (Availability Checking)** Find common available slots |
| **STEP 8: Select Optimal Time Slot** | **CAN-12 (Constraint Satisfaction)** Apply complex constraint logic |
| **STEP 9-10: Book Resources and Create Meeting (Parallel)** | **CAN-19 (Resource Booking)** Reserve meeting room |
|  | **CAN-03 (Event Creation/Update)** Schedule Project Alpha meeting |

**Tasks Used**: 10 (CAN-04, CAN-05, CAN-01, CAN-07, CAN-02, CAN-03, CAN-06, CAN-12, CAN-19, CAN-03)  
**F1 Score**: 100%  
**Note**: Most complex scheduling prompt - demonstrates hard vs soft constraint resolution

---

## Collaborate-1: "Help me set the agenda to review the progress of Project Alpha with the product and marketing team to get confirmation we are on track and discuss any blocking issues or risks."

| Step | Atomic Agent Capability |
|------|------------------------|
| **STEP 1: Parse Agenda Requirements** | **CAN-04 (NLU)** Extract meeting goals and attendee groups |
| **STEP 2: Resolve Team Membership** | **CAN-05 (Attendee Resolution)** Identify individual team members |
| **STEP 3: Generate Meeting Agenda** | **CAN-23 (Agenda Generation/Structuring)** Create specialized agenda structure |

**Tasks Used**: 3 (CAN-04, CAN-05, CAN-23)  
**F1 Score**: 100%  
**Note**: Simplest Collaborate prompt - demonstrates focused agenda generation capability  
**Gold Standard Revision**: CAN-09 → CAN-23 (specialized agenda generation more appropriate)

---

## Collaborate-2: "Review the materials for my meeting with senior leadership and suggest the best way to summarize the topics into three main discussion points. Generate any objections or concerns that might come up and give me effective responses."

| Step | Atomic Agent Capability |
|------|------------------------|
| **STEP 1: Understand Preparation Requirements** | **CAN-04 (NLU)** Parse multi-part request |
| **STEP 2: Resolve Senior Leadership Attendees (CRITICAL)** | **CAN-05 (Attendee/Contact Resolution)** Identify who is "senior leadership" |
| **STEP 3: Find the Senior Leadership Meeting** | **CAN-01 (Calendar Retrieval)** Locate upcoming meeting |
| **STEP 4: Extract Meeting Details** | **CAN-07 (Metadata Extraction)** Get meeting metadata |
| **STEP 5: Retrieve Meeting Materials** | **CAN-08 (Document Retrieval)** Load all attached materials |
| **STEP 6: Summarize into 3 Main Discussion Points** | **CAN-09 (Document Generation)** Synthesize materials into key themes |
| **STEP 7: Generate Objections and Responses** | **CAN-18 (Objection/Risk Anticipation)** Anticipate senior leadership concerns |

**Tasks Used**: 7 (CAN-04, CAN-05, CAN-01, CAN-07, CAN-08, CAN-09, CAN-18)  
**F1 Score**: 77.78% (Partial - originally missed CAN-05)  
**Critical Fix**: CAN-05 is ESSENTIAL - cannot find "meeting with senior leadership" without knowing who they are

---

## Collaborate-3: "Prepare a brief for my upcoming meeting with customer Beta and include a dossier for each customer attendee and the topics they are most interested in. Include a background on their company."

| Step | Atomic Agent Capability |
|------|------------------------|
| **STEP 1: Understand Brief Requirements** | **CAN-04 (NLU)** Parse multi-component preparation request |
| **STEP 2: Find Customer Beta Meeting** | **CAN-01 (Calendar Retrieval)** Locate upcoming meeting |
| **STEP 3: Extract Customer Attendees** | **CAN-07 (Metadata Extraction)** Get meeting participant details |
| **STEP 4: Resolve Attendees to Full Profiles** | **CAN-05 (Attendee/Contact Resolution)** Build comprehensive profiles |
| **STEP 5: Retrieve Historical Interaction Materials** | **CAN-08 (Document Retrieval)** Load past meeting data |
| **STEP 6-7: Generate Dossiers and Research Company (Parallel)** | **CAN-09 (Document Generation)** Create attendee dossiers and brief structure |
|  | **CAN-22 (Research/Intelligence)** Gather company background |

**Tasks Used**: 7 (CAN-04, CAN-01, CAN-07, CAN-05, CAN-08, CAN-09, CAN-22)  
**F1 Score**: 50.00% (Partial - originally missed CAN-05)  
**Critical Fix**: CAN-05 resolves attendees to enable profile building and historical analysis  
**Note**: Most customer-facing prompt - demonstrates external research capabilities

---

## Summary Statistics

| Metric | Value |
|--------|-------|
| **Total Hero Prompts** | 9 |
| **Total Execution Steps** | 61 (across all prompts) |
| **Simplest Prompt** | Collaborate-1 (3 steps) |
| **Most Complex Prompts** | Organizer-3, Schedule-1 (9 steps each) |
| **Perfect Scores (100% F1)** | 6 of 9 prompts |
| **Partial Scores** | 3 of 9 prompts (Schedule-2, Collaborate-2, Collaborate-3) |
| **Most Common Task** | CAN-04 (NLU) - appears in all 9 prompts |
| **NEW Task Validated** | CAN-25 (Event Annotation/Flagging) in Organizer-2 |

---

## Key Orchestration Patterns

### Pattern 1: Sequential Foundation
**CAN-04 → CAN-01 → CAN-07** appears in 8 of 9 prompts  
Understanding intent → Retrieving data → Extracting metadata forms the foundation

### Pattern 2: Parallel Classification
**CAN-02 + CAN-03** run concurrently in 4 prompts  
Meeting type classification and importance assessment are independent operations

### Pattern 3: Critical Missing Dependency
**CAN-05 (Attendee Resolution)** was missing in 2 prompts (Collaborate-2, Collaborate-3)  
When resolving vague references ("senior leadership", "customer Beta") to specific people, CAN-05 is required  
**Schedule-2 does NOT need CAN-05** - attendees already available from existing meetings via CAN-07

### Pattern 4: Dual-Phase Processing
**Schedule-3** demonstrates complex constraint satisfaction with pure + overridable availability checking

### Pattern 5: Automation Layer
**CAN-16 (Monitoring) → CAN-17 (Auto-Reschedule)** creates event-driven reactive workflows

---

## Usage Notes

**For LLM Developers**:
- Use these tables to understand task orchestration requirements
- Parallel processing opportunities clearly marked
- Critical dependencies highlighted (especially CAN-05)

**For Framework Designers**:
- Identifies common patterns for optimization
- Shows specialized task usage (CAN-21, CAN-25, CAN-22)
- Demonstrates tier distribution across prompt types

**For Training Data Generation**:
- Each step can generate synthetic training examples
- Parallel operations can be varied independently
- Critical dependencies must be maintained in training data

---

**Document Metadata**:
- **Source Report**: V2_GOLD_STANDARD_REPORT.md (2,917 lines)
- **Gold Standard JSON**: v2_gold_standard_v2_20251107.json
- **Framework Version**: Calendar.AI V2.0 (25 canonical tasks)
- **Validation Status**: Human-validated by Chin-Yew Lin
- **Mean F1 Score**: 91.98% ± 16.38%
- **Related Documents**: 
  - V2_HERO_PROMPTS_LIST.md (quick prompt reference)
  - CANONICAL_TASKS_REFERENCE_V2.md (complete task specifications)
  - GOLD_STANDARD_REPORT_WRITING_GUIDE.md (documentation template)
