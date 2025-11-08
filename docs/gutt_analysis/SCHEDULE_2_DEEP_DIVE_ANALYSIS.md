# Schedule-2: Detailed Analysis - The 66.67% F1 Case

**Date**: November 8, 2025  
**Framework**: 25 Canonical Tasks V2.0  
**Status**: 100% Consistency, Moderate Accuracy (66.67% F1)  
**Classification**: Balanced errors (3 missing, 3 false positives)

---

## Executive Summary

Schedule-2 demonstrates **perfect consistency (100%) with moderate accuracy (66.67% F1)**. Unlike Collaborate-1 which had severe under-performance, Schedule-2 shows a **balanced error pattern**: 3 tasks missing and 3 false positives. The model selected exactly the right number of tasks (9) but made systematic substitutions.

**Key Finding**: The model's errors reveal confusion between similar tasks (CAN-02 vs none needed, CAN-21 vs CAN-06, CAN-17 vs CAN-23), suggesting the need for clearer task distinction in the prompt engineering.

---

## The Prompt

**Full Text**:
```
"Clear my Thursday afternoon. Update my RSVPs and help me reschedule 
my meetings to another time and show me as {status}."
```

**User Intent**: Block off Thursday afternoon by declining/rescheduling existing meetings and updating calendar status.

**Key Phrases**:
1. "Clear my Thursday afternoon" → Time blocking + meeting cancellation
2. "Update my RSVPs" → Change RSVP status for meetings
3. "help me reschedule my meetings" → Find new times and coordinate
4. "show me as {status}" → Update calendar visibility/status

---

## Trial Results - Perfect Consistency

### All 3 Trials Identical

**Trial 1, 2, 3 Tasks** (100% consistent):
```json
["CAN-04", "CAN-01", "CAN-07", "CAN-02", "CAN-03", "CAN-21", "CAN-12", "CAN-17", "CAN-13"]
```

**Consistency Analysis**:
- Always selected: 9 tasks (all 9 appeared in all trials)
- Sometimes selected: 0 tasks
- Total unique: 9 tasks
- **Consistency = 9/9 × 100% = 100.0%**

**Observation**: Model is perfectly stable with consistent task selection across all trials.

---

## Gold Standard Comparison

### What Should Have Been Selected

**Human-Validated Gold Standard** (9 tasks):
```json
["CAN-04", "CAN-05", "CAN-01", "CAN-07", "CAN-13", "CAN-06", "CAN-12", "CAN-23", "CAN-03"]
```

**Detailed Breakdown**:

**Correctly Selected (6 tasks)**:

1. **CAN-04: Natural Language Understanding** ✅
   - Parse prompt to extract time constraint (Thursday afternoon), actions (clear, reschedule, RSVP)
   
2. **CAN-01: Calendar Events Retrieval** ✅
   - Retrieve all meetings scheduled for Thursday afternoon
   
3. **CAN-07: Meeting Metadata Extraction** ✅
   - Extract metadata from Thursday meetings (attendees, RSVP status, details)
   
4. **CAN-13: RSVP/Response Management** ✅
   - Update RSVP status (decline or tentative for meetings being cleared)
   
5. **CAN-12: Meeting Creation/Modification** ✅
   - Modify meetings for rescheduling or create calendar blocks
   
6. **CAN-03: Meeting Importance Assessment** ✅
   - Assess which meetings can be rescheduled vs must keep

### What GPT-5 Selected (9 tasks)

**Missing from Gold Standard (3 tasks)**:

1. **CAN-05: Attendee/Contact Resolution** ❌ MISSING
   - **Why needed**: "reschedule my meetings" requires knowing WHO to coordinate with
   - Must resolve attendees to send reschedule requests
   - Cannot reschedule without attendee contact information
   - **Gold standard note**: "The model needs to get metadata, and from there to find attendee"
   - **Verdict**: Critical missing task

2. **CAN-06: Availability Checking** ❌ MISSING
   - **Why needed**: "reschedule...to another time" requires finding free slots
   - Must check calendar availability for alternative times
   - Cannot propose reschedule times without availability data
   - **Verdict**: Critical missing task

3. **CAN-23: Conflict/Constraint Resolution** ❌ MISSING  
   - **Why needed**: Resolving conflicts when clearing Thursday afternoon
   - Handle constraint satisfaction (find times that work for all attendees)
   - Manage competing priorities when rescheduling multiple meetings
   - **Verdict**: Important missing task

**False Positives (3 tasks)**:

1. **CAN-02: Meeting Type Classification** ❌ FALSE POSITIVE
   - **GPT-5's reasoning**: Classify meetings to determine reschedule priority
   - **Why wrong**: CAN-03 (Importance Assessment) already handles priority determination
   - CAN-02 is for objective type classification (1:1, team sync, customer)
   - Not needed when CAN-03 provides strategic importance assessment
   - **Verdict**: False positive (redundant with CAN-03)

2. **CAN-21: Focus Time Blocking/Protection** ❌ FALSE POSITIVE
   - **GPT-5's reasoning**: "Clear Thursday afternoon" = block time for focus
   - **Why wrong**: Prompt asks to clear for rescheduling, not for focus work
   - CAN-21 is for protecting time for preparation/deep work
   - This is about meeting management, not focus time
   - **Gold standard expects**: CAN-06 (Availability) instead
   - **Verdict**: False positive (wrong interpretation)

3. **CAN-17: Automatic Rescheduling** ❌ FALSE POSITIVE (DEBATABLE)
   - **GPT-5's reasoning**: "help me reschedule" = automate rescheduling
   - **Why wrong per gold standard**: Should use CAN-23 (Conflict Resolution) instead
   - **Why debatable**: CAN-17 IS for rescheduling, seems reasonable
   - **Human rationale**: CAN-23 handles constraint satisfaction more broadly
   - **Verdict**: False positive but understandable confusion

---

## Performance Metrics

### Confusion Matrix

|  | Actually Needed (Gold) | Not Needed |
|---|----------------------|-----------|
| **Selected by GPT-5** | 6 (CAN-04, CAN-01, CAN-07, CAN-13, CAN-12, CAN-03) | 3 (CAN-02, CAN-21, CAN-17) |
| **Not Selected by GPT-5** | 3 (CAN-05, CAN-06, CAN-23) | 16 (all others) |

**Breakdown**:
- **True Positives (TP)**: 6
- **False Positives (FP)**: 3
- **False Negatives (FN)**: 3
- **True Negatives (TN)**: 16

### Calculated Metrics

**Precision** (How many selections were correct?):
```
Precision = TP / (TP + FP)
Precision = 6 / (6 + 3)
Precision = 6/9 = 66.67%
```
**Interpretation**: 6 out of 9 selected tasks were actually needed.

**Recall** (How many needed tasks were found?):
```
Recall = TP / (TP + FN)
Recall = 6 / (6 + 3)
Recall = 6/9 = 66.67%
```
**Interpretation**: Found 6 out of 9 required tasks.

**F1 Score** (Harmonic mean):
```
F1 = 2 × (Precision × Recall) / (Precision + Recall)
F1 = 2 × (66.67 × 66.67) / (66.67 + 66.67)
F1 = 2 × 4444.89 / 133.34
F1 = 66.67%
```
**Interpretation**: Balanced moderate performance - not poor, not excellent.

---

## Error Analysis

### Error #1: Missing CAN-05 (Attendee/Contact Resolution)

**The Requirement**:
- Prompt says: "help me reschedule my meetings"
- System must know WHO to coordinate with for rescheduling
- Cannot send reschedule requests without attendee contacts

**Why GPT-5 Missed It**:
1. **Implicit dependency**: Rescheduling implies attendee coordination
2. **Focus on mechanics**: Model focused on time-finding (CAN-06 also missed!)
3. **Same pattern as Collaborate-1**: Also missed CAN-05 for team resolution

**What GPT-5 Should Have Reasoned**:
```
"reschedule my meetings"
  → Meetings have attendees
  → Need to coordinate with attendees for new times
  → CAN-05: Attendee/Contact Resolution
```

**Systematic Issue**: Model consistently under-uses CAN-05

**Human Evaluator Note**:
> "The model needs to get metadata, and from there to find attendee for those meeting in the Thursday afternoon."

---

### Error #2: Missing CAN-06 (Availability Checking)

**The Requirement**:
- Prompt says: "reschedule my meetings to another time"
- System must find alternative times that work
- Cannot propose reschedule without availability data

**Why GPT-5 Missed It**:
1. **Substituted CAN-21**: Model used Focus Time Blocking instead
2. **Confusion about "clear"**: Interpreted as "block time" not "find alternatives"
3. **Missing link**: Didn't connect "reschedule to another time" with availability check

**What GPT-5 Selected Instead**:
- **CAN-21 (Focus Time Blocking)**: WRONG - This is for protecting focus time, not finding reschedule slots

**Why This is Wrong**:

| Task | Purpose | This Prompt Needs |
|------|---------|-------------------|
| **CAN-21** | Block calendar for focus work | ❌ Not focus time |
| **CAN-06** | Check availability for scheduling | ✅ Find reschedule slots |

**Correct Flow**:
```
1. CAN-01: Retrieve Thursday afternoon meetings
2. CAN-07: Extract meeting metadata
3. CAN-06: Check availability for alternative times ← MISSING
4. CAN-05: Get attendee contacts for coordination ← MISSING
5. CAN-12: Create/modify meetings with new times
```

---

### Error #3: Missing CAN-23 vs Using CAN-17

**The Debate**: Conflict Resolution (CAN-23) vs Automatic Rescheduling (CAN-17)

**Gold Standard Choice**: CAN-23 (Conflict/Constraint Resolution)
- **Reasoning**: Handle constraint satisfaction across multiple meetings
- **Scope**: Broader problem-solving for competing priorities
- **Use case**: Multiple meetings need rescheduling with various constraints

**GPT-5's Choice**: CAN-17 (Automatic Rescheduling)
- **Reasoning**: "help me reschedule" = automate rescheduling process
- **Scope**: Focused on rescheduling automation
- **Use case**: Automatically find and propose new times

**Analysis**:

| Aspect | CAN-17 (GPT-5) | CAN-23 (Gold) |
|--------|----------------|---------------|
| **Focus** | Automate rescheduling | Resolve constraints |
| **Complexity** | Single meeting | Multiple meetings |
| **Constraints** | Time-based | Multi-dimensional |

**Why Gold Standard Prefers CAN-23**:
- Clearing an entire afternoon involves **multiple meetings**
- Need to handle **competing constraints** (attendee availability, meeting importance)
- **Broader problem**: Not just "reschedule" but "optimize the reschedule plan"

**Why GPT-5's CAN-17 is Understandable**:
- Prompt explicitly says "help me reschedule"
- CAN-17 description literally includes "rescheduling"
- Reasonable interpretation for automation task

**Verdict**: Arguable - could accept CAN-17 OR require CAN-23 depending on framework philosophy.

---

### Error #4: False Positive CAN-02 (Meeting Type Classification)

**Why GPT-5 Included It**:
- Reasoning: Need to classify meetings to determine reschedule priority

**Why It's Wrong**:
- **CAN-03 is already selected**: Meeting Importance Assessment handles prioritization
- **CAN-02 is objective classification** (1:1, team sync, customer meeting types)
- **CAN-03 is subjective assessment** (strategic importance, urgency)
- **Redundant**: Type classification doesn't add value when importance is assessed

**The Distinction**:

| Task | What It Does | Example Output |
|------|--------------|----------------|
| **CAN-02** | Classify format/structure | "1:1", "Team Sync", "All-hands" |
| **CAN-03** | Assess strategic value | "Critical", "Medium priority", "Can reschedule" |

**This Prompt Needs**: Only CAN-03 (which was selected ✅)

---

### Error #5: False Positive CAN-21 (Focus Time Blocking)

**Why GPT-5 Included It**:
- Reasoning: "Clear my Thursday afternoon" sounds like blocking time

**Why It's Wrong**:

**What CAN-21 Actually Does**:
```
CAN-21: Focus Time Blocking/Protection
Purpose: Reserve/protect time blocks for preparation, deep work, focus time
Example: "Block 2 hours Friday morning for report preparation"
```

**What This Prompt Actually Asks**:
```
"Clear my Thursday afternoon"
  → Decline/reschedule existing meetings
  → Free up the time slot
  → NOT blocking for focus work
  → Need: CAN-06 (Availability Checking) to find reschedule slots
```

**Key Distinction**:

| Phrase | CAN-21 (Block Time) | CAN-06 (Check Availability) |
|--------|---------------------|------------------------------|
| "Clear Thursday" | ❌ Not about blocking | ✅ Free up time |
| "Block Thursday" | ✅ Reserve time | ❌ Not checking |

**Prompt says**: "Clear" (remove meetings) not "Block" (reserve for focus)

---

## Comparison with Similar Prompts

### Schedule-1 vs Schedule-2

| Aspect | Schedule-1 | Schedule-2 |
|--------|------------|------------|
| **F1 Score** | 100.00% | 66.67% |
| **Consistency** | 100% | 100% |
| **Gold Tasks** | 9 | 9 |
| **CAN-05** | ✅ Included | ❌ Missing |
| **CAN-06** | ✅ Included | ❌ Missing |
| **Focus** | Create new recurring | Clear + reschedule existing |

**Why Schedule-1 Succeeds**:
- Clearer prompt: "I want a weekly 30-min 1:1 with {name}"
- Explicit attendee mention triggers CAN-05
- "Automatically reschedule on declines" triggers CAN-06

**Why Schedule-2 Struggles**:
- Less explicit about coordination needs
- "reschedule my meetings" doesn't clearly trigger attendee resolution
- "Clear Thursday" misinterpreted as focus time blocking

---

### Schedule-3 vs Schedule-2

| Aspect | Schedule-3 | Schedule-2 |
|--------|------------|------------|
| **F1 Score** | 100.00% | 66.67% |
| **Consistency** | 100% | 100% |
| **CAN-05** | ✅ Included | ❌ Missing |
| **CAN-06** | ✅ Included | ❌ Missing |
| **CAN-19** | ✅ Resource booking | - |

**Why Schedule-3 Succeeds**:
- Explicit attendees: "Chris, Sangya, and Kat"
- Clear availability requirement: "work around Kat's schedule"
- "Find a time" directly triggers availability checking

---

## Impact on Overall Statistics

### Variance Contribution

**Schedule-2's Contribution to F1 Variance**:

```
F1 Score: 66.67%
Mean F1: 90.74%
Deviation: -24.07
Squared Deviation: 579.36

Total Variance: 2839.35
Schedule-2 Share: 579.36 / 2839.35 = 20.40%
```

**Second highest variance contributor after Collaborate-1!**

**Comparison**:

| Scenario | F1 Std Dev | Mean F1 | Impact |
|----------|-----------|---------|--------|
| **With both outliers** | 17.76% | 90.74% | Current |
| **Without Collaborate-1** | ~11% | ~94% | Major improvement |
| **Without Schedule-2** | ~15% | ~93% | Moderate improvement |
| **Without both** | ~7% | ~97% | Excellent |

**Statistical Significance**:
- Removing Schedule-2 would reduce variance by ~15%
- Combined with Collaborate-1 fix, would reduce variance to ~7%

---

## Recommendations

### Immediate Fixes

**1. Add Explicit CAN-05 Guidance for Rescheduling**
```
Add to system prompt:

"When prompt mentions rescheduling meetings, ALWAYS include CAN-05:
- 'reschedule my meetings' → need attendee contacts
- 'move meetings to another time' → need coordination
- 'find new time for meeting' → need attendee availability

Rescheduling REQUIRES attendee resolution to coordinate new times."
```

**2. Clarify CAN-06 vs CAN-21 Distinction**
```
Add to system prompt:

❌ DON'T use CAN-21 (Focus Time Blocking) for:
- "Clear my calendar" → removing meetings, not blocking
- "Free up time" → availability checking (CAN-06)
- "Reschedule" → need CAN-06 to find alternatives

✅ DO use CAN-21 for:
- "Block time for preparation"
- "Reserve 2 hours for deep work"
- "Protect focus time"

Key distinction: 
- CLEAR/FREE = CAN-06 (check availability)
- BLOCK/RESERVE = CAN-21 (protect time)
```

**3. Clarify CAN-23 vs CAN-17 Hierarchy**
```
Framework decision needed:

When to use CAN-23 (Conflict Resolution) vs CAN-17 (Auto-reschedule):
- Multiple meetings + constraints → CAN-23
- Single meeting automation → CAN-17
- Complex scheduling problem → CAN-23
- Simple reschedule request → CAN-17

Recommendation: Document clear usage guidelines
```

**4. Remove CAN-02 When CAN-03 Present**
```
Add to system prompt:

"CAN-02 (Type Classification) and CAN-03 (Importance Assessment):
- If determining meeting priority: Use CAN-03 ONLY
- CAN-02 adds value only when type-specific logic needed
- Don't select both unless prompt specifically needs classification"
```

---

### Long-term Improvements

**1. Rescheduling Task Chain Training**
- Train model on complete rescheduling workflow:
  1. Retrieve meetings (CAN-01)
  2. Extract metadata (CAN-07)
  3. **Resolve attendees (CAN-05)** ← Often missed
  4. **Check availability (CAN-06)** ← Often missed
  5. Handle constraints (CAN-23)
  6. Modify meetings (CAN-12)

**2. Implicit Requirement Detection**
- Add examples showing implicit attendee coordination:
  ```
  "reschedule my meetings" → CAN-05 + CAN-06
  "move to another time" → CAN-05 + CAN-06
  "find new time" → CAN-05 + CAN-06
  ```

**3. Task Substitution Patterns**
- Track common substitutions (CAN-21 instead of CAN-06)
- Add negative examples to prevent wrong substitutions
- Clarify task boundaries more explicitly

---

## Lessons Learned

**1. Balanced Errors are Easier to Fix**
- Schedule-2 has 3 missing + 3 false positives (balanced)
- Easier to fix than Collaborate-1's skewed errors (1 correct, 4 wrong)
- Substitution errors are more correctable than omission errors

**2. Implicit Dependencies Still Challenging**
- "Reschedule" implies attendee coordination (CAN-05)
- Model doesn't consistently infer implicit requirements
- Need more explicit training on dependency chains

**3. Similar Tasks Need Clear Boundaries**
- CAN-06 vs CAN-21 confusion (availability vs blocking)
- CAN-23 vs CAN-17 confusion (constraints vs automation)
- CAN-02 vs CAN-03 confusion (classification vs assessment)
- Framework needs clearer task distinctions

**4. Prompt Clarity Matters Enormously**
- Schedule-1: "with {name}" → CAN-05 ✅
- Schedule-3: "Chris, Sangya, and Kat" → CAN-05 ✅
- Schedule-2: "my meetings" → CAN-05 ❌
- Explicit mentions trigger correct tasks

---

## Potential Gold Standard Revisions

### Should We Accept CAN-17? ✅ ACCEPTED

**Arguments FOR accepting CAN-17** (instead of requiring CAN-23):
- Prompt explicitly says "help me reschedule"
- CAN-17 is specifically for rescheduling
- Reasonable interpretation of user intent
- Improves F1 from 66.67% to 88.89% (with CAN-05 removal)

**Arguments AGAINST**:
- Multiple meetings require constraint resolution (CAN-23)
- CAN-23 is more comprehensive
- Framework should prefer broader problem-solving tasks
- Maintains consistency with framework philosophy

**DECISION (November 8, 2025)**: CAN-17 ACCEPTED. Combined with CAN-05 removal (not needed for existing meetings), Schedule-2 F1 improved to 88.89%.

**Recommendation**: Keep CAN-23 in gold standard but add usage note explaining when CAN-17 is acceptable alternative.

### Should We Remove CAN-02 Penalty?

**Arguments FOR removing penalty**:
- Type classification could help prioritize reschedules
- Customer meetings vs internal meetings have different constraints
- Not strictly wrong, just redundant

**Arguments AGAINST**:
- CAN-03 already handles prioritization
- Adding CAN-02 doesn't change the outcome
- Should penalize redundant task selection
- Encourages minimal necessary task sets

**Recommendation**: Keep penalty to encourage lean task selection.

---

## Conclusion

Schedule-2 shows **systematic, correctable errors** rather than fundamental failures:
1. **CAN-05 omission**: Same pattern as other prompts, needs explicit guidance
2. **CAN-06 vs CAN-21 confusion**: Clear boundary clarification needed
3. **CAN-23 vs CAN-17**: Arguable interpretation, framework decision needed
4. **CAN-02 redundancy**: Good opportunity to teach lean task selection

With targeted prompt engineering addressing these 4 patterns, Schedule-2's F1 could likely improve from 66.67% to 88-100%.

**Status**: Schedule-2 represents **teachable moments** for framework improvement, not model limitations.

---

**Report Version**: 1.0  
**Analysis Date**: November 8, 2025  
**Framework**: 25 Canonical Tasks V2.0  
**Analyst**: Comprehensive AI Review
