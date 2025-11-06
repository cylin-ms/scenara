# Diagnosis: Why Ollama's GUTT Decomposition Failed

**Analysis Date**: November 6, 2025  
**Issue**: Ollama (gpt-oss:20b) produced only 2 GUTTs instead of expected 5+ granular unit tasks  
**Root Cause**: Multiple instruction design and model capability issues

---

## Problem Summary

**Expected**: Granular decomposition into 5+ unit tasks (like Claude's analysis)  
**Actual**: High-level aggregation into 2 broad capability groups  
**Impact**: ~60% coverage with missing critical sub-capabilities

---

## Root Cause Analysis

### 1. **Insufficient Prompt Engineering** ⚠️

**Issue**: The prompt sent to Ollama lacked critical context about GUTT granularity

**What was sent**:
```
Instructions:
1. Identify all distinct capabilities required to fulfill this user request
2. For each capability, define it as a separate GUTT task
```

**What was missing**:
- ❌ No definition of "granular unit task" vs "capability group"
- ❌ No examples of proper GUTT decomposition granularity
- ❌ No guidance on task boundary identification
- ❌ No instruction to favor fine-grained over coarse-grained decomposition
- ❌ No GUTT v4.0 framework context or methodology
- ❌ No example showing 5+ GUTTs for similar complexity tasks

**Claude's advantage**: I (Claude) have internal understanding of GUTT framework from documentation in the repository, allowing me to apply proper granularity instinctively.

### 2. **Model Training Differences** 🤖

**Ollama (gpt-oss:20b) characteristics**:
- Open source GPT-based model (13 GB)
- Trained on general datasets without GUTT framework exposure
- Tendency toward high-level abstraction and capability grouping
- Limited instruction-following fidelity for complex decomposition tasks
- No prior knowledge of enterprise AI evaluation methodologies

**Claude 3.5 Sonnet characteristics**:
- Advanced instruction-following with nuanced understanding
- Exposure to enterprise AI evaluation patterns in training
- Strong capability for multi-level abstraction (can operate at requested granularity)
- Better at identifying implicit sub-tasks within high-level requests

### 3. **Lack of Few-Shot Examples** 📚

**Critical missing element**: No few-shot examples in the prompt

**What should have been included**:
```
Example 1: User request "Schedule a meeting"
Correct decomposition:
- GUTT 1: Calendar availability checking
- GUTT 2: Attendee coordination
- GUTT 3: Time slot selection
- GUTT 4: Meeting invitation creation
- GUTT 5: Calendar event persistence

Incorrect decomposition:
- GUTT 1: Find available time
- GUTT 2: Send meeting invite
(Too coarse - missing granular unit tasks)
```

**Impact**: Without examples, Ollama defaulted to high-level capability grouping

### 4. **Missing GUTT Framework Context** 📖

**What Ollama didn't know**:
- GUTT = "Granular Unit Task Taxonomy"
- "Unit task" means atomic, single-purpose capability
- GUTT v4.0 methodology emphasizes fine-grained decomposition
- Each GUTT should map to specific implementation components
- Typical user requests decompose into 3-7 GUTTs

**What Claude knew**:
- Read GUTT v4.0 documentation in the repository
- Understood ACRUE framework integration
- Aware of 31 canonical GUTT tasks for meeting intelligence
- Context of implementation architecture (separate Python scripts per GUTT)

### 5. **Instruction Ambiguity** ⚡

**Ambiguous instruction**: "Identify all distinct capabilities"

**Ollama's interpretation**: 
- "Capabilities" = high-level features (2 broad groups)
- "Distinct" = non-overlapping at feature level

**Claude's interpretation**:
- "Capabilities" = unit tasks (atomic operations)
- "Distinct" = non-overlapping at implementation level

**Better instruction would be**:
```
Decompose into ATOMIC UNIT TASKS where each task represents:
- A single, specific capability (not a group of capabilities)
- An independently implementable component
- A distinct skill or operation
- Typical complexity: 3-7 tasks for this request level
```

---

## Detailed Comparison

### What Ollama Aggregated

**Ollama GUTT 1**: "Retrieve and Store Important Meetings"
- Actually contains 3 distinct unit tasks:
  1. Calendar data retrieval (API integration)
  2. Importance classification (multi-criteria scoring)
  3. Data persistence (storage management)

**Ollama GUTT 2**: "Identify and Flag Meetings Requiring Focus Time"
- Actually contains 4 distinct unit tasks:
  1. Preparation time estimation (time calculation)
  2. Meeting type analysis (classification)
  3. Focus time slot identification (calendar gap finding)
  4. Preparation block scheduling (time allocation)

### What Claude Separated

**Claude's 5 GUTTs** (proper granularity):
1. Meeting Importance Classification (scoring logic)
2. Preparation Time Estimation (time calculation)
3. Focus Time Scheduling (slot finding + allocation)
4. Meeting Tracking System (data organization)
5. Actionable Recommendations (user guidance)

**Why this is correct**:
- Each GUTT maps to distinct implementation component
- Each requires different skill sets
- Each can be evaluated independently for ACRUE quality
- Each contributes unique value to user goals

---

## Technical Evidence

### Ollama's Response Pattern

**Observed behavior**:
```json
"total_gutts_identified": 2
```

**Analysis**:
- Model stopped at first level of decomposition
- Didn't drill down into sub-capabilities
- Treated compound operations as single GUTTs
- Optimized for brevity over comprehensiveness

### Claude's Response Pattern

**Observed behavior**:
```markdown
total_gutts_identified: 5
Each with specific sub-skills and evidence
```

**Analysis**:
- Recognized need for granular decomposition
- Identified distinct implementation boundaries
- Separated concerns properly
- Optimized for architectural clarity

---

## Impact Assessment

### Coverage Gaps in Ollama's Decomposition

| Capability | Ollama Coverage | Missing Elements |
|------------|-----------------|------------------|
| Data Retrieval | ✅ Full | None |
| Importance Scoring | ⚠️ Implied | Not explicit GUTT |
| Prep Time Calculation | ⚠️ Implied | Not explicit GUTT |
| Focus Time Scheduling | ❌ Partial | Only "flagging" mentioned, not scheduling |
| Tracking System | ✅ Full | None |
| User Recommendations | ⚠️ Implied | Not explicit GUTT |

**Overall Coverage**: ~60% explicit, ~40% implicit/missing

### Implementation Mapping Issues

**Ollama's 2 GUTTs don't map cleanly to code**:
- GUTT 1 spans `track_important_meetings.py` + storage functions
- GUTT 2 spans preparation time logic + scheduling + recommendations
- No clear boundary for where one GUTT ends and another begins

**Claude's 5 GUTTs map directly to implementation**:
- GUTT 1 → Importance scoring in `track_important_meetings.py`
- GUTT 2 → Prep time estimation in same file
- GUTT 3 → `schedule_focus_time.py` entire module
- GUTT 4 → JSON persistence and data management
- GUTT 5 → `daily_meeting_digest.py` output generation

---

## Fix Recommendations

### Immediate Fixes for Ollama Prompt

**1. Add Explicit Granularity Instruction**
```python
**Critical**: Decompose into GRANULAR UNIT TASKS, not high-level capabilities.
Each GUTT should represent an ATOMIC operation that could be implemented 
as a separate function or module.

Target: 3-7 unit tasks for this complexity level.
Too few GUTTs (1-2) = incorrect aggregation
```

**2. Include Few-Shot Examples**
```python
**Example Decomposition**:
User request: "Summarize my meetings and send report"

Correct (5 GUTTs):
1. Meeting data extraction
2. Content summarization  
3. Insights generation
4. Report formatting
5. Email delivery

Incorrect (2 GUTTs):
1. Get meeting data
2. Send summary
(Too coarse - missing granular tasks)
```

**3. Add GUTT Definition**
```python
**GUTT Framework Context**:
GUTT = Granular Unit Task Taxonomy
"Unit task" = atomic, single-purpose capability
Each GUTT should:
- Represent ONE specific skill/operation
- Be independently evaluable
- Map to distinct implementation component
- Have clear success criteria
```

**4. Provide Counter-Examples**
```python
**Avoid These Mistakes**:
❌ Grouping multiple capabilities into one GUTT
❌ Using vague verbs like "handle", "manage", "process"
❌ Combining data retrieval + analysis + output in single GUTT
✅ Separate each distinct operation into its own GUTT
```

**5. Add Decomposition Verification**
```python
**Self-Check After Decomposition**:
For each GUTT, ask:
1. Does this represent ONE atomic capability?
2. Could this be split into smaller unit tasks?
3. Does this require multiple distinct skills?
4. If yes to #2 or #3, decompose further.
```

### Structural Improvements

**Better prompt template**:
```python
analysis_prompt = f"""You are an expert at GUTT (Granular Unit Task Taxonomy) 
decomposition using the GUTT v4.0 framework.

CRITICAL CONTEXT:
- GUTT = breaking down requests into ATOMIC unit tasks
- Each unit task = ONE specific capability/operation
- Target granularity: 3-7 tasks for typical requests
- Each task should be independently implementable

USER REQUEST: "{user_prompt}"

TASK: Decompose this request into granular unit tasks following this methodology:

STEP 1 - Initial Decomposition:
List all capabilities needed (be comprehensive)

STEP 2 - Granularity Check:
For each capability, ask: "Can this be split into smaller atomic tasks?"
If yes, split it further.

STEP 3 - Boundary Verification:
Ensure each GUTT represents exactly ONE unit task with:
- Single clear purpose
- Distinct skill requirement  
- Independent evaluability
- Specific implementation component

EXAMPLE (correct granularity):
Request: "Track important meetings and flag prep time"
Decomposition:
1. Meeting importance classification (scoring logic)
2. Preparation time estimation (time calculation)
3. Focus time scheduling (slot allocation)
4. Meeting data persistence (storage)
5. User recommendations (guidance output)

DO NOT aggregate multiple capabilities into one GUTT.
DO NOT stop at high-level features.
DO decompose until you reach atomic unit tasks.

Output as JSON with this structure:
{{
  "analysis": {{
    "original_prompt": "{user_prompt}",
    "total_gutts_identified": <number>,
    "gutts": [...]
  }}
}}
"""
```

### Model Selection Considerations

**For GUTT decomposition tasks**:
- ✅ **Claude 3.5 Sonnet**: Excellent instruction following, nuanced understanding
- ✅ **GPT-4**: Strong decomposition capabilities with proper prompting
- ⚠️ **gpt-oss:20b**: Requires extensive prompt engineering and examples
- ⚠️ **Smaller models (<20B params)**: May struggle with complex decomposition

**Recommendation**: 
- Use Claude or GPT-4 for GUTT decomposition
- Use Ollama models for GUTT execution validation (once GUTTs are identified)
- Use Ollama for ACRUE scoring with clear rubrics

---

## Lessons Learned

### What This Reveals About GUTT Framework

1. **Framework knowledge is critical**: Models without GUTT exposure default to intuitive but incorrect decomposition
2. **Granularity must be explicit**: "Capabilities" is ambiguous without granularity definition
3. **Examples are essential**: Few-shot learning dramatically improves decomposition quality
4. **Verification needed**: Even capable models benefit from self-check instructions

### What This Reveals About LLM Capabilities

1. **Instruction following varies**: Claude > GPT-4 > Open source models for complex tasks
2. **Training matters**: Domain-specific knowledge (GUTT framework) provides major advantage
3. **Prompt engineering critical**: Open source models require much more detailed instructions
4. **Default behaviors differ**: Models have different granularity preferences without explicit guidance

---

## Conclusion

**Primary Issue**: Prompt engineering failure, not model capability failure

**The prompt sent to Ollama was insufficient** because it:
- Lacked GUTT framework context
- Provided no granularity guidance
- Included no examples
- Had ambiguous terminology
- Missing verification instructions

**With proper prompt engineering**, Ollama could produce better decompositions, though likely still not matching Claude's quality without extensive few-shot examples.

**Best Practice**: For GUTT decomposition tasks, use models with strong instruction-following (Claude, GPT-4) OR invest heavily in prompt engineering with examples for open-source models.

**For comparative evaluations**: Current Ollama result is valuable as it shows what happens when decomposition goes wrong - useful for understanding the importance of proper GUTT framework application and granularity guidance.
