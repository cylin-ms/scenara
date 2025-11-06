# Reference GUTT Decomposition - Ground Truth

**User Prompt**: "Track all my important meetings and flag any that require focus time to prepare for them"

**Correct Granular Decomposition**: **7 Unit Tasks (GUTTs)**

---

## Atomic Unit Tasks (GUTTs)

### **GUTT 1: Calendar Data Retrieval**
- **Capability**: Load and parse calendar events from data source
- **Implementation**: `load_calendar_data()` method
- **Skills Required**: 
  - JSON file I/O
  - Data deserialization
  - Error handling
- **Evidence**: 267 events loaded from `my_calendar_events_complete_attendees.json`

### **GUTT 2: Meeting Importance Classification**
- **Capability**: Score meetings based on multiple importance criteria
- **Implementation**: `calculate_importance_score()` method
- **Skills Required**:
  - Multi-criteria scoring algorithm (9 importance factors)
  - Keyword detection
  - Attendee analysis
  - Confidence weighting
- **Evidence**: Importance scoring with weights (executive: 25, external: 20, large meeting: 15, etc.)

### **GUTT 3: Preparation Time Estimation**
- **Capability**: Calculate required prep time based on meeting type and context
- **Implementation**: `estimate_prep_time()` method
- **Skills Required**:
  - Meeting type classification
  - Time estimation mapping
  - Context-aware adjustments
- **Evidence**: 10+ meeting types with specific prep times (Executive Briefing: 120min, Customer Meeting: 90min, etc.)

### **GUTT 4: Meeting Flagging Logic**
- **Capability**: Identify which meetings need preparation focus time
- **Implementation**: `analyze_meetings()` filtering logic
- **Skills Required**:
  - Threshold-based filtering
  - Criteria evaluation
  - List segmentation
- **Evidence**: Meetings filtered by importance score ≥30 AND prep_time >0

### **GUTT 5: Calendar Gap Analysis**
- **Capability**: Identify available time slots for focus time scheduling
- **Implementation**: `find_available_slots()` method in `schedule_focus_time.py`
- **Skills Required**:
  - Temporal gap detection
  - Work hours enforcement (8 AM - 6 PM)
  - Meeting conflict checking
  - Duration-based slot validation
- **Evidence**: Gap finding algorithm that checks before/between/after meetings

### **GUTT 6: Focus Time Block Scheduling**
- **Capability**: Create and schedule preparation time blocks in calendar
- **Implementation**: `schedule_prep_blocks()` and `.ics` export
- **Skills Required**:
  - Slot allocation algorithm
  - iCalendar format generation
  - Optimal timing selection (day before meeting)
  - Multi-meeting prep aggregation
- **Evidence**: Generated 6 focus time blocks with `.ics` file export

### **GUTT 7: Actionable Recommendations & Reporting**
- **Capability**: Generate user-facing insights, summaries, and guidance
- **Implementation**: `daily_meeting_digest.py` and output formatting
- **Skills Required**:
  - User communication formatting
  - Priority-based reporting
  - Actionable guidance generation
  - Summary statistics calculation
- **Evidence**: Daily digest with prep alerts, schedule overview, tomorrow preview

---

## Why 7 GUTTs (Not 5)?

### Original Claude Analysis Had 5 GUTTs
In my initial evaluation, I grouped related tasks:
- GUTT 3 (Focus Time Scheduling) combined both gap analysis + scheduling
- GUTT 4 (Meeting Tracking) was too broad

### Correct Atomic Decomposition Has 7 GUTTs
Each should be independently implementable:

**Separation Rationale**:

1. **Calendar Data Retrieval** (GUTT 1) 
   - Distinct I/O operation, separate from analysis
   - Different error modes and testing requirements
   
2. **Importance Classification** (GUTT 2) vs **Prep Time Estimation** (GUTT 3)
   - Different algorithms (scoring vs. time mapping)
   - Can be executed independently
   - Original Claude analysis: ✅ Already separated

3. **Meeting Flagging** (GUTT 4)
   - Distinct filtering/selection logic
   - Applies criteria from GUTTs 2 and 3
   - Separate from scoring (consumes scores, applies thresholds)

4. **Gap Analysis** (GUTT 5) vs **Block Scheduling** (GUTT 6)
   - Gap finding is read-only analysis of existing calendar
   - Scheduling is write operation creating new calendar entries
   - Different skills: analysis vs. creation
   - Different outputs: available slots vs. scheduled blocks

5. **Reporting** (GUTT 7)
   - Separate from all analysis tasks
   - Focuses on user communication, not computation
   - Different skill set: presentation vs. calculation

---

## Mapping to Implementation

| GUTT | Primary File | Primary Method/Function |
|------|-------------|------------------------|
| 1. Calendar Data Retrieval | `track_important_meetings.py` | `load_calendar_data()` |
| 2. Importance Classification | `track_important_meetings.py` | `calculate_importance_score()` |
| 3. Prep Time Estimation | `track_important_meetings.py` | `estimate_prep_time()` |
| 4. Meeting Flagging | `track_important_meetings.py` | `analyze_meetings()` filtering |
| 5. Calendar Gap Analysis | `schedule_focus_time.py` | `find_available_slots()` |
| 6. Focus Time Scheduling | `schedule_focus_time.py` | `schedule_prep_blocks()` + `.ics` export |
| 7. Reporting | `daily_meeting_digest.py` | `print_daily_digest()` |

---

## User Request Mapping

**Original Request**: "Track all my important meetings and flag any that require focus time to prepare for them"

**Verb → GUTT Mapping**:

- **"Track"** triggers:
  - GUTT 1: Calendar Data Retrieval (get the meetings)
  - GUTT 2: Importance Classification (identify "important" ones)
  - GUTT 4: Meeting Flagging (select which to track)
  - GUTT 7: Reporting (show tracked meetings)

- **"important meetings"** triggers:
  - GUTT 2: Importance Classification (define and score "important")

- **"flag any that require focus time"** triggers:
  - GUTT 3: Prep Time Estimation (identify which "require" prep)
  - GUTT 4: Meeting Flagging (the "flag" operation)

- **"focus time to prepare for them"** triggers:
  - GUTT 5: Calendar Gap Analysis (find when focus time can fit)
  - GUTT 6: Focus Time Scheduling (create the focus blocks)

---

## Evaluation Framework Enhancement

For the UX comparison tool, we should support:

1. **User-Provided Reference Decomposition**
   - Allow users to input ground truth GUTT count and descriptions
   - Compare LLM decompositions against this reference
   
2. **Granularity Metrics**
   - Too Coarse: Fewer GUTTs than reference (e.g., Ollama's 2 vs reference 7)
   - Too Fine: More GUTTs than reference (over-decomposition)
   - Correct: Matches reference ±1 GUTT
   
3. **Coverage Analysis**
   - Which reference GUTTs are present in LLM decomposition?
   - Which are missing?
   - Which are aggregated into broader GUTTs?
   
4. **Precision/Recall Scoring**
   - Precision: % of LLM GUTTs that match reference tasks
   - Recall: % of reference GUTTs identified by LLM
   - F1 Score: Harmonic mean of precision and recall

---

## Comparison Results

### Ground Truth: 7 GUTTs
1. Calendar Data Retrieval
2. Importance Classification  
3. Prep Time Estimation
4. Meeting Flagging
5. Gap Analysis
6. Focus Time Scheduling
7. Reporting

### Claude: 5 GUTTs (71% coverage)
1. ✅ Importance Classification (matches GUTT 2)
2. ✅ Prep Time Estimation (matches GUTT 3)
3. ⚠️ Focus Time Scheduling (aggregates GUTTs 5+6)
4. ⚠️ Meeting Tracking (aggregates GUTTs 1+4+7)
5. ✅ Actionable Recommendations (matches GUTT 7)

**Missing**: Calendar Data Retrieval, Meeting Flagging as separate tasks
**Aggregated**: Gap analysis + scheduling combined, tracking + retrieval + flagging combined

### Ollama: 2 GUTTs (29% coverage)
1. ⚠️ Retrieve and Store Important Meetings (aggregates GUTTs 1+2+4)
2. ⚠️ Identify and Flag Meetings Requiring Focus Time (aggregates GUTTs 3+5+6+7)

**Missing**: All 7 GUTTs as separate tasks
**Aggregated**: Everything collapsed into 2 broad capability groups

---

## Conclusion

**Correct Answer**: **7 GUTTs** for this user request

This represents the proper atomic decomposition where each GUTT:
- Has a single, clear purpose
- Maps to distinct implementation component
- Uses different primary skills
- Can be independently tested and evaluated
- Represents a unit task, not a capability group
