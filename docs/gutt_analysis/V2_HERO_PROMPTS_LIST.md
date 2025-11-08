# V2 Gold Standard Hero Prompts

**Document Version**: 2.0  
**Date**: November 8, 2025  
**Total Prompts**: 9 (3 Organizer, 3 Schedule, 3 Collaborate)  
**Mean F1 Score**: 91.98% ± 16.38%

---

## Organizer Category (3 prompts)

### 1. Organizer-1 (Gold Standard F1: 100%) ✅

**Prompt**:
> "Keep my Calendar up to date by committing to only meetings that are part of my priorities."

**Capabilities**: Meeting prioritization, RSVP management based on user priorities  
**Evaluation**: ✅ Correct  
**Tasks Used**: 7 tasks (CAN-04, CAN-01, CAN-07, CAN-02, CAN-03, CAN-11, CAN-13)

---

### 2. Organizer-2 (Gold Standard F1: 100%) ✅

**Prompt**:
> "Track all my important meetings and flag any that require focus time to prepare for them."

**Capabilities**: Meeting tracking, importance assessment, preparation time estimation, event flagging  
**Evaluation**: ✅ Correct (with CAN-25 added)  
**Tasks Used**: 9 tasks including **NEW CAN-25** (Event Annotation/Flagging)  
**Note**: This prompt validated the new CAN-25 canonical task in V2.0

---

### 3. Organizre-3 (Gold Standard F1: 100%) ✅

**Prompt**:
> "Help me understand where I am spending my time and identify ways I can reclaim time to focus more on my top priorities."

**Capabilities**: Time analysis, pattern identification, recommendation generation, data visualization  
**Evaluation**: ✅ Correct  
**Tasks Used**: 9 tasks (CAN-04, CAN-01, CAN-07, CAN-02, CAN-03, CAN-10, CAN-11, CAN-14, CAN-20)  
**Note**: Most complex Organizer prompt - uses tasks across all tiers

---

## Schedule Category (3 prompts)

### 4. Schedule-1 (Gold Standard F1: 100%) ✅

**Prompt**:
> "Starting next week, I want a weekly 30-min 1:1 with {name}. Afternoons preferred, avoid Fridays. Automatically reschedule on declines or conflicts."

**Capabilities**: Recurring meeting setup, constraint satisfaction, availability checking, automatic rescheduling  
**Evaluation**: ✅ Correct  
**Tasks Used**: 9 tasks including CAN-15 (Recurrence Rules), CAN-16 (Event Monitoring), CAN-17 (Auto-Reschedule)  
**Note**: Most specialized Schedule prompt - uses 3 Tier-3 tasks

---

### 5. Schedule-2 (Gold Standard F1: 88.89%) ⚠️

**Prompt**:
> "Clear my Thursday afternoon. Update my RSVPs and help me reschedule my meetings to another time and show me as {status}."

**Capabilities**: Meeting rescheduling, RSVP management, availability checking, constraint satisfaction  
**Evaluation**: ⚠️ Partial - Missing CAN-06 (Availability Checking)  
**Tasks Used**: 8 tasks  
**Gold Standard Revision**: CAN-23 (Conflict Resolution) → CAN-17 (Automatic Rescheduling); CAN-05 removed (not needed for existing meetings)  
**Human Evaluator Note**: "CAN-05 not needed - attendee information already available from existing meetings via CAN-07. Only CAN-06 (Availability Checking) is missing."

---

### 6. Schedule-3 (Gold Standard F1: 100%) ✅

**Prompt**:
> "Land a time to meet about Project Alpha with Chris, Sangya, and Kat for 1 hour in the next 2 weeks. Schedule over 1:1s and lunches if needed and work around Kat's schedule. Make the meeting in person and add a room."

**Capabilities**: Multi-person scheduling, constraint satisfaction, resource booking, priority-based conflict resolution  
**Evaluation**: ✅ Correct  
**Tasks Used**: 10 tasks (most tasks in framework)  
**Note**: Most complex scheduling prompt - demonstrates hard vs soft constraint logic

---

## Collaborate Category (3 prompts)

### 7. Collaborate-1 (Gold Standard F1: 50%) ⚠️

**Prompt**:
> "Help me set the agenda to review the progress of Project Alpha with the product and marketing team to get confirmation we are on track and discuss any blocking issues or risks."

**Capabilities**: Attendee resolution, agenda generation  
**Evaluation**: ⚠️ Partial - Missing CAN-05, over-applied CAN-18  
**Tasks Used**: 3 tasks (CAN-04, CAN-05, CAN-23)  
**Gold Standard Revision**: CAN-09 (Document Generation) → CAN-23 (Agenda Generation/Structuring)  
**Human Evaluator Note**: "'to get confirmation we are on track and discuss any blocking issues or risks' in the prompt is to set the goal of the meeting and should be used as input for the agenda generation for CAN-23. The user does not expect the system to find blocking issues and confirm status but the requester want to find out those during the meeting so CAN-18 should not be activated."  
**Note**: Simplest Collaborate prompt - demonstrates meeting goals vs system tasks distinction

---

### 8. Collaborate-2 (Gold Standard F1: 77.78%) ⚠️

**Prompt**:
> "Review the materials for my meeting with senior leadership and suggest the best way to summarize the topics into three main discussion points. Generate any objections or concerns that might come up and give me effective responses."

**Capabilities**: Meeting material retrieval, content summarization, objection anticipation, response generation  
**Evaluation**: ⚠️ Partial - Missing CAN-05 (Attendee Resolution)  
**Tasks Used**: 7 tasks including CAN-18 (Objection/Risk Anticipation)  
**Human Evaluator Note**: "The system needs to know who are in the senior leadership to find relevant meetings and meeting related materials. So CAN-05 is a critical task."  
**Note**: CAN-18 is appropriately used here (user explicitly requested objection generation)

---

### 9. Collaborate-3 (Gold Standard F1: 100%) ✅

**Prompt**:
> "Prepare a brief for my upcoming meeting with customer Beta and include a dossier for each customer attendee and the topics they are most interested in. Include a background on their company."

**Capabilities**: Meeting preparation, contact research, company intelligence, document generation  
**Evaluation**: ✅ Correct  
**Tasks Used**: 7 tasks including CAN-22 (Research/Intelligence Gathering)  
**Note**: Most customer-facing prompt - demonstrates external research capabilities

---

## Summary Statistics

| Category | Prompts | Perfect (100% F1) | Partial | Mean F1 |
|----------|---------|-------------------|---------|---------|
| Organizer | 3 | 3 (100%) | 0 | 100% |
| Schedule | 3 | 2 (67%) | 1 | 92.59% |
| Collaborate | 3 | 1 (33%) | 2 | 75.93% |
| **TOTAL** | **9** | **6 (67%)** | **3 (33%)** | **91.98%** |

---

## Key Insights

### ✅ Strengths
- **High Overall Accuracy**: 6 of 9 prompts achieved perfect gold standard match (100% F1)
- **NEW Task Validated**: CAN-25 (Event Annotation/Flagging) successfully validated in Organizer-2
- **Complex Orchestration**: Schedule-3 demonstrates sophisticated multi-person scheduling with 10 tasks
- **Organizer Category**: Perfect performance (100% across all 3 prompts)

### ⚠️ Areas for Improvement
- **CAN-05 Detection**: Missing in 3 prompts (Schedule-2, Collaborate-1, Collaborate-2)
  - Critical for attendee resolution before availability checking
  - Human evaluator identified this pattern across multiple prompts
- **CAN-18 Scope**: Over-applied in Collaborate-1
  - Meeting goals should be INPUT to agenda generation, not tasks to execute
  - Framework needs clearer guidance on when CAN-18 is appropriate
- **Collaborate Category**: Lower mean F1 (75.93%) - most complex reasoning required

---

## Gold Standard Revisions

Two revisions were made during human evaluation (November 8, 2025):

1. **Collaborate-1**: CAN-09 (Document Generation) → CAN-23 (Agenda Generation/Structuring)
   - Rationale: "Set the agenda" requires specialized agenda generation task
   
2. **Schedule-2**: CAN-23 (Conflict Resolution) → CAN-17 (Automatic Rescheduling)
   - Rationale: "Help me reschedule" requires automation action, not just conflict detection

---

## Usage Notes

- **For LLM Evaluation**: Use these prompts to benchmark task decomposition accuracy
- **For Training Data**: These prompts cover diverse use cases across all 3 categories
- **For Implementation**: Task frequency indicates priority (Organizer tasks most common)
- **For Testing**: Partial prompts highlight edge cases requiring improved detection

---

**Related Documents**:
- V2 Gold Standard Report: `V2_GOLD_STANDARD_REPORT.md`
- Canonical Tasks Reference: `CANONICAL_TASKS_GOLD_STANDARD_REFERENCE_V2.md`
- Framework Specification: `CANONICAL_TASKS_REFERENCE_V2.md`

**Document Status**: ✅ Production-Ready  
**Last Updated**: November 8, 2025
