# Gold Standard Reference Report - Writing Guide

**Document Type**: Instructional Template  
**Version**: 1.0  
**Date**: November 7, 2025  
**Purpose**: Guide for creating comprehensive Gold Standard Reference documentation for canonical task analysis

---

## Overview

This guide provides step-by-step instructions for creating a **Gold Standard Reference Report** that documents the authoritative canonical task decomposition for a set of prompts or use cases. This format is used for:

- **LLM Evaluation**: Benchmarking model performance in task decomposition
- **Framework Validation**: Validating canonical task frameworks
- **Training Data**: Ground truth for fine-tuning and prompt optimization
- **Quality Assurance**: Reference standard for production system validation

---

## Report Structure

### Part 1: Document Header & Metadata

#### 1.1 Title and Metadata Block

```markdown
# [Project Name] Canonical Task Analysis - Gold Standard Reference

**Document Version**: [X.X]  
**Date**: [Month Day, Year]  
**Author**: Chin-Yew Lin  
**Framework**: [Framework Name and Version] (e.g., "Calendar.AI Canonical Unit Tasks Framework v2.0 (25 tasks)")

**Related Documents**:
- [Document 1 Title](path/to/document1.md) - Brief description
- [Document 2 Title](path/to/document2.md) - Brief description
- [Document 3 Title](path/to/document3.md) - Brief description
```

**Guidelines**:
- Use clear, descriptive title with "Gold Standard Reference" designation
- Include all version control metadata
- Link to related documents (testing results, framework specs, original decompositions)

---

#### 1.2 Document Summary Section

Create a comprehensive summary with three subsections:

##### A. Purpose Statement

```markdown
### Purpose

This document provides the **gold standard canonical task analysis** for the [N] [project/system] prompts, serving as the authoritative reference for:

1. **LLM Evaluation**: Benchmark model performance in task decomposition
2. **Framework Validation**: Validate the [N] canonical unit tasks framework
3. **Training Data**: Ground truth for fine-tuning and prompt optimization
4. **Quality Assurance**: Reference standard for production system validation
```

**Guidelines**:
- Clearly state what this document IS (gold standard, authoritative reference)
- List 4 primary use cases
- Be specific about the number of prompts and framework version

---

##### B. Methodology Section

Document the **creation process** using a multi-phase structure:

```markdown
### Methodology

This gold standard was created through a rigorous [N]-phase process:

#### Phase 1: Initial Framework Development ([Date Range])
- **Original Analysis**: [Describe initial decomposition approach]
- **Consolidation**: [Describe how common patterns were identified]
- **Framework Evolution**: [Describe refinement process]

#### Phase 2: Automated Baseline Analysis ([Date])
- **Automated Analysis**: [Describe which model/tool was used]
- **Performance**: [State baseline metrics]
- **Key Findings**: 
  - [Finding 1 with metrics]
  - [Finding 2 with metrics]
  - [Finding 3 with metrics]

#### Phase 3: Prompt Optimization & Validation ([Date])
- **Optimization**: Enhanced prompts with [N] critical concepts:
  1. [Concept 1 with description]
  2. [Concept 2 with description]
  3. [Concept 3 with description]
  ...
  
- **[N]-Trial Stability Test**: [N] API calls ([N] trials × [N] prompts)
  - **Average Performance**: F1 [X]% ± [X]% ([Assessment])
  - **Task 1 Detection**: [X]% ([improvement])
  - **Task 2 Detection**: [X]% ([improvement])
  - **Consistency**: [X]% task selection agreement across trials

#### Phase 4: Human Correction & Gold Standard Creation ([Date])
- **Manual Review**: Human expert ([Name]) reviewed [model] outputs
- **Corrections Applied**:
  - [Correction type 1]
  - [Correction type 2]
  - [Correction type 3]
- **Validation**: Cross-referenced with [original source]
- **Final Output**: This gold standard reference document
```

**Guidelines**:
- Use 4-phase structure: Development → Baseline → Optimization → Human Correction
- Include specific dates and date ranges
- Provide concrete metrics for each phase
- Show the evolution/improvement trajectory
- Always end with human validation step

---

##### C. Gold Standard Statistics

Create two summary tables:

**Table 1: Overall Statistics**

```markdown
### Gold Standard Statistics

| Metric | Value |
|--------|-------|
| **Total Prompts** | [N] |
| **Total Canonical Tasks** | [N] (framework size) |
| **Tasks Used** | [N] (unique tasks appearing at least once) |
| **Average Tasks/Prompt** | [X.X] |
| **Tier 1 (Universal) Coverage** | [X]% |
| **Tier 2 (Common) Coverage** | [X]% |
| **Tier 3 (Specialized) Coverage** | [X]% |
```

**Table 2: Task Frequency Distribution**

```markdown
### Task Frequency Distribution

| Task ID | Task Name | Frequency | Prompts |
|---------|-----------|-----------|---------|
| **CAN-01** | [Task Name] | [X]% | [N]/[Total] |
| **CAN-02** | [Task Name] | [X]% | [N]/[Total] |
| **CAN-03** | [Task Name] | [X]% | [N]/[Total] |
...
```

**Guidelines**:
- Calculate frequency as: (Prompts using task / Total prompts) × 100%
- Sort by frequency (descending) or by task ID (ascending) - be consistent
- Include ALL tasks in framework, even if 0% frequency
- Show tier coverage if your framework uses tiering

---

### Part 2: Per-Prompt Analysis

For **each prompt** in your gold standard, create a complete analysis section following this template:

#### 2.1 Prompt Header

```markdown
---

## Hero Prompt [N]: [Descriptive Name] ([identifier])

**Prompt**: "[Full verbatim prompt text in quotes]"

**Capabilities Required**: [High-level summary of what this prompt needs - 5-10 words describing key capabilities]
```

**Guidelines**:
- Use horizontal rule (`---`) to separate prompts
- Number prompts sequentially
- Include both descriptive name AND identifier/slug
- Quote the full prompt exactly as users would write it
- Capabilities summary should be business-level, not technical

---

#### 2.2 Canonical Task Decomposition

Start with task count, then detail each task:

```markdown
### Canonical Task Decomposition: **[N] Tasks**

#### Task 1: [Task Name] (CAN-##)
- **Purpose**: [What this task does in the context of THIS prompt - be specific]
- **Input**: [What data/information this task receives]
- **Output**: [What this task produces - be concrete with examples]
- **Tier**: [Universal/Common/Specialized] (Tier [1/2/3])
- **Dependencies**: [Optional - list prerequisite tasks]
- **Note**: [Optional - special considerations, distinctions, caveats]

#### Task 2: [Task Name] (CAN-##)
- **Purpose**: ...
- **Input**: ...
- **Output**: ...
- **Tier**: ...
```

**Guidelines for Each Task**:

1. **Purpose**: 
   - Be specific to THIS prompt's context
   - Explain WHY this task is needed here
   - 1-2 sentences max

2. **Input**:
   - List concrete data types
   - Reference outputs from dependency tasks if applicable
   - Be specific (not "meeting data" but "calendar events with RSVP status")

3. **Output**:
   - Describe the structure and content
   - Include examples in parentheses where helpful
   - Be concrete (not "analysis results" but "importance scores/ratings aligned with user priorities")

4. **Tier**:
   - Always include tier classification if your framework has tiers
   - Format: `Universal (Tier 1)` or `Specialized (Tier 3)`

5. **Dependencies** (optional):
   - Only include if task MUST wait for another task
   - Format: `Requires CAN-07 (Metadata Extraction)`
   - Explain the dependency briefly

6. **Note** (optional):
   - Use for important distinctions (e.g., "PARENT task - enables CAN-05, CAN-13")
   - Clarify confusions (e.g., "WRITE operation vs CAN-07 READ operation")
   - Highlight special considerations (e.g., "OBJECTIVE classification based on format")

**Task Ordering**:
- Order tasks in **execution order** when possible (shows workflow)
- OR order by tier (Universal → Common → Specialized)
- Be consistent across all prompts

---

#### 2.3 Evaluation Criteria

```markdown
**Evaluation Criteria**:
- [Criterion 1 - how to measure success]
- [Criterion 2 - quality metric]
- [Criterion 3 - accuracy measure]
```

**Guidelines**:
- List 3-5 measurable criteria
- Focus on output quality, accuracy, completeness
- Be specific enough that someone could use these to evaluate
- Examples: "Prioritization accuracy vs user-defined priorities", "Meeting type classification precision", "Context completeness"

---

#### 2.4 Execution Composition

This is the **most important section** - shows HOW tasks work together:

```markdown
### Execution Composition

**How Tasks Work Together to Answer the Prompt:**

\```
STEP 1: [Phase Name - e.g., "Understand User Intent"]
CAN-## (Task Name) → [What happens - extract/analyze/generate/etc.]
CAN-## (Task Name) → [What happens]

STEP 2: [Phase Name - e.g., "Retrieve Data"]
CAN-## (Task Name) → [What happens]

STEP 3: [Phase Name - e.g., "Classify & Analyze"]
CAN-## (Task Name) → [What happens]
CAN-## (Task Name) → [What happens]

STEP 4: [Phase Name - e.g., "Generate Recommendations"]
CAN-## (Task Name) → [Detailed description with examples]
  - [Sub-point 1]
  - [Sub-point 2]

STEP 5: [Phase Name - e.g., "Execute Actions"]
CAN-## (Task Name) → [What happens]

OUTPUT: [Comprehensive description of final result with structure]
  - [Component 1]
  - [Component 2]
  - [Component 3]
\```
```

**Guidelines for Execution Composition**:

1. **Use Code Blocks**: Wrap entire workflow in triple backticks
2. **Number Steps**: STEP 1, STEP 2, etc.
3. **Name Phases**: Give each step a descriptive name
4. **Use Arrow Notation**: `CAN-## (Name) → What it does`
5. **Show Data Flow**: Make it clear what each task produces
6. **Include Details**: Add sub-bullets for complex operations
7. **End with OUTPUT**: Describe the final deliverable structure

---

#### 2.5 Key Orchestration Patterns

```markdown
**Key Orchestration Patterns**:
- **Pattern Type 1**: [Description - e.g., "Parallel Execution: CAN-02A, CAN-02B can run concurrently"]
- **Pattern Type 2**: [Description - e.g., "Parent-Child: CAN-07 must complete before CAN-05, CAN-13"]
- **Pattern Type 3**: [Description - e.g., "Sequential: CAN-04 → CAN-01 → CAN-07 (linear dependency)"]
- **Pattern Type 4**: [Description - e.g., "Decision Point: CAN-14 output determines if CAN-13 runs"]
```

**Common Pattern Types**:
- **Parallel Execution**: Tasks that can run simultaneously
- **Sequential**: Tasks that must run in order
- **Parent-Child**: One task enables others
- **Conditional/Decision Point**: Optional task execution based on results
- **Aggregation**: Multiple tasks feed into one
- **Fan-out/Fan-in**: One task feeds multiple, or multiple feed one
- **Iterative/Loop**: Task repeats for each item

**Guidelines**:
- List 3-6 key patterns
- Use bold for pattern type name
- Explain which specific tasks exhibit this pattern
- Focus on patterns that are important for understanding the workflow

---

#### 2.6 Example Flow

Provide at least **one concrete example** showing the workflow with real data:

```markdown
**Example Flow for [Scenario Description]**:

\```
Input: "[Concrete example input]"

CAN-04: Extract → [Specific extracted values] ✓
CAN-01: Retrieved → [Specific data retrieved] ✓
CAN-07: Metadata → [Specific metadata: Attendees: [list], Agenda: "text"]
CAN-02A: Type = "[Classification Result]" ✓
CAN-02B: Importance = "[Score/Rating]" ([justification]) ✓
CAN-05: Attendees = [analysis result] → [Categorization] ✓
CAN-14: Recommendation = "[Specific recommendation with reasoning]"
CAN-13: Action = [Action taken] (if auto-enabled)

Output: "[Specific output with the actual recommendation/result]"
\```
```

**Guidelines for Example Flows**:

1. **Use Realistic Data**: Make it believable and concrete
2. **Show Every Task**: Demonstrate each task's contribution
3. **Include Actual Values**: Not placeholders - real examples
4. **Use Check Marks**: ✓ to show task completion
5. **Format Consistently**: Task ID: Action = "Result" ✓
6. **Show Data Flow**: Make it clear how each task uses previous outputs
7. **End with Output**: Show the final answer to the user

**Optional**: Include multiple examples if:
- There are important variations in the workflow
- Different scenarios exercise different paths
- Edge cases need illustration

---

### Part 3: Cross-Prompt Analysis (End of Document)

After all per-prompt sections, add summary analysis:

#### 3.1 Task Usage Summary

```markdown
---

## Cross-Prompt Analysis

### Task Usage Summary

| Task ID | Task Name | Used In | Total Usage | Percentage |
|---------|-----------|---------|-------------|------------|
| CAN-01 | [Name] | [Prompt IDs] | [N]/[Total] | [X]% |
| CAN-02 | [Name] | [Prompt IDs] | [N]/[Total] | [X]% |
...

**Observations**:
- **Universal Tasks** (100% coverage): [List task IDs]
- **Common Tasks** (50-99% coverage): [List task IDs]
- **Specialized Tasks** (<50% coverage): [List task IDs]
- **Unused Tasks**: [List task IDs if any]
```

---

#### 3.2 Performance Metrics (if applicable)

If you ran validation tests:

```markdown
### Validation Test Results

#### Overall Performance

| Metric | Value | Assessment |
|--------|-------|------------|
| **Average F1** | [X.X]% ± [X.X]% | [EXCELLENT/GOOD/ACCEPTABLE] |
| **Precision** | [X.X]% ± [X.X]% | [Assessment] |
| **Recall** | [X.X]% ± [X.X]% | [Assessment] |
| **Consistency** | [X.X]% | [Assessment] |

#### Per-Trial Results (if multi-trial testing)

| Trial | F1 | Precision | Recall | Status |
|-------|-----|-----------|--------|--------|
| **Trial 1** | [X]% | [X]% | [X]% | ✅ Success |
| **Trial 2** | [X]% | [X]% | [X]% | ✅ Success |
| **Trial 3** | [X]% | [X]% | [X]% | ✅ Success |

**Variance Analysis**: [Interpret the variance - is it acceptable? Why?]

#### Major Task Detection Improvements

| Task | Original | Optimized | Delta | Prompts |
|------|----------|-----------|-------|---------|
| **CAN-XX** | [X]% | [X]% | **+[X]%** ⭐ | [N]/[Total] |
| **CAN-YY** | [X]% | [X]% | **+[X]%** ⭐ | [N]/[Total] |
...
```

---

#### 3.3 Statistical Validation (if applicable)

```markdown
### Statistical Validation

#### Stability Threshold Analysis
- **EXCELLENT**: F1 variance < 2% → [ACHIEVED/NOT ACHIEVED] ([X]%)
- **GOOD**: F1 variance < 5% → [ACHIEVED/NOT ACHIEVED]
- **ACCEPTABLE**: F1 variance < 10% → [ACHIEVED/NOT ACHIEVED]

#### Consistency Score
- **Definition**: % of task selections that match across all trials
- **Result**: [X.X]% consistency
- **Interpretation**: [What this means]

#### Performance Comparison with Baseline
- **Baseline F1**: [X]% (description)
- **Gold Standard F1**: [X]% ± [X]% (description)
- **Delta**: [+/-X]% ([interpretation])
```

---

#### 3.4 Key Findings

Organize findings thematically:

```markdown
### Key Findings

#### 1. [Finding Theme 1 - e.g., "Prompt Optimization Was Highly Successful"]
- [Supporting point 1 with metrics]
- [Supporting point 2 with metrics]
- [Supporting point 3 with metrics]

#### 2. [Finding Theme 2 - e.g., "Specialized Tasks Benefited Most"]
Tasks that benefited from [optimization approach]:
- **Task ID**: [Description] → [Result]
- **Task ID**: [Description] → [Result]

#### 3. [Finding Theme 3 - e.g., "Universal Tasks Already Stable"]
- **Task ID**: [Description and performance]
- **Task ID**: [Description and performance]

#### 4. [Finding Theme 4 - e.g., "Framework Validation Success"]
- [Validation point 1]
- [Validation point 2]
```

**Guidelines**:
- Use 3-5 major themes
- Number findings sequentially
- Include metrics to support each finding
- Focus on insights, not just data repetition

---

### Part 4: Conclusions

#### 4.1 Optimization Success (if applicable)

```markdown
### Conclusions

#### Optimization Success
The [model/approach] optimization achieved all objectives:
1. ✅ **[Objective 1]**: [Metric] ([assessment])
2. ✅ **[Objective 2]**: [Metric] ([assessment])
3. ✅ **[Objective 3]**: [Metric] ([assessment])
4. ✅ **[Objective 4]**: [Metric] ([assessment])
```

---

#### 4.2 Framework Validation

```markdown
#### Framework Validation
The [N] canonical tasks framework is validated by:
- [Validation evidence 1 with metric]
- [Validation evidence 2 with metric]
- [Validation evidence 3 with metric]
- [Validation evidence 4 with metric]
```

---

#### 4.3 Production Readiness

```markdown
#### Production Readiness
The [system/prompts] are production-ready:
- [Readiness criterion 1 with metric]
- [Readiness criterion 2 with metric]
- [Readiness criterion 3 with metric]
- [Readiness criterion 4 with metric]
```

---

#### 4.4 Future Work

```markdown
#### Future Work
1. **[Area 1]**: [Description of next steps]
2. **[Area 2]**: [Description of next steps]
3. **[Area 3]**: [Description of next steps]
4. **[Area 4]**: [Description of next steps]
```

---

### Part 5: Document Metadata (Footer)

End with comprehensive metadata:

```markdown
---

## Document Metadata

**Version**: [X.X]  
**Created**: [Month Day, Year]  
**Author**: Chin-Yew Lin  
**Total Prompts**: [N]  
**Total Tasks**: [N] ([describe any special counting])  
**Framework**: [Framework Name and Version]  
**Status**: ✅ Gold Standard Reference  

**Validation**:
- ✅ Human expert review ([Name])
- ✅ Cross-referenced with [source]
- ✅ Validated against [test/model] ([N] trials)
- ✅ All [N] canonical tasks represented
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
- Add new prompts as they are created
- Incorporate learnings from production system performance
- Align with [framework] updates

---

*End of Document*
```

---

## Formatting Standards

### Typography and Markdown

1. **Headers**:
   - `#` for document title
   - `##` for major sections (per-prompt, analysis, conclusions)
   - `###` for subsections (execution composition, statistics)
   - `####` for task-level items

2. **Emphasis**:
   - **Bold** for metrics, task IDs, key terms
   - *Italic* for notes, clarifications
   - `Code` for task IDs in text (e.g., `CAN-07`)

3. **Lists**:
   - Use `-` for unordered lists
   - Use `1.` for ordered lists (auto-numbering)
   - Indent sub-items with 2 spaces

4. **Tables**:
   - Use markdown table format with pipes `|`
   - Align headers with `|--------|`
   - **Bold** header row
   - Right-align numbers when possible

5. **Code Blocks**:
   - Use triple backticks for execution flows
   - Use single backticks for inline task IDs
   - NO syntax highlighting needed (plain text)

6. **Status Indicators**:
   - ✅ Success/Achieved/Completed
   - ❌ Failure/Not Achieved/Blocked
   - ⚠️ Warning/Needs Attention
   - ⭐ Highlight/Exceptional Performance
   - 🎯 Target/Goal

### Consistency Rules

1. **Task References**:
   - Always use format: `CAN-##` (with zero-padding if needed)
   - Always include task name on first reference: `CAN-07 (Metadata Extraction)`
   - Can use just `CAN-07` on subsequent references in same section

2. **Percentages**:
   - Always use `%` symbol
   - Include ± for variance: `78.40% ± 0.72%`
   - One decimal place for most metrics
   - Two decimals for small variances (<1%)

3. **Task Decomposition Format**:
   - Always: `#### Task [N]: [Name] (CAN-##)`
   - Always include: Purpose, Input, Output, Tier
   - Optional: Dependencies, Note
   - Use bullet points with `**Label**:` format

4. **Execution Flows**:
   - Always wrap in code blocks
   - Always use `STEP N:` numbering
   - Always use `→` for data flow
   - Always use `✓` for completed tasks
   - Always end with `OUTPUT:` section

5. **Cross-References**:
   - Link related documents in header
   - Reference tasks by ID when showing dependencies
   - Cite specific sections when referring to other parts

---

## Quality Checklist

Before finalizing your Gold Standard Reference report, verify:

### Content Completeness
- [ ] All prompts have complete analysis sections
- [ ] Every task has: Purpose, Input, Output, Tier
- [ ] Execution Composition shows complete workflow for each prompt
- [ ] At least one concrete example flow per prompt
- [ ] Cross-prompt analysis includes task frequency
- [ ] Conclusions section addresses all objectives

### Accuracy
- [ ] All task counts are correct (manual verification)
- [ ] Frequency percentages calculated correctly
- [ ] Task IDs match framework specification
- [ ] Dependencies are accurate and complete
- [ ] Metrics match source data

### Consistency
- [ ] All tasks formatted identically
- [ ] Same section structure for all prompts
- [ ] Consistent terminology throughout
- [ ] Consistent use of status indicators
- [ ] Consistent table formatting

### Clarity
- [ ] Purpose statements are specific to context
- [ ] Input/Output descriptions are concrete
- [ ] Execution flows are understandable
- [ ] Examples use realistic data
- [ ] Notes clarify confusions/distinctions

### Professional Quality
- [ ] No typos or grammatical errors
- [ ] All links work correctly
- [ ] Tables render properly
- [ ] Code blocks format correctly
- [ ] Document metadata is complete

---

## Common Pitfalls to Avoid

### 1. Vague Task Descriptions
❌ **Bad**: "This task analyzes the meeting data"  
✅ **Good**: "Extract detailed metadata from pending invitations (attendees, agenda, organizer, RSVP status)"

### 2. Missing Context in Purpose
❌ **Bad**: "Purpose: Classify meetings by type"  
✅ **Good**: "Purpose: Classify each pending invitation by meeting type to identify high-stakes formats for prep time estimation"

### 3. Abstract Execution Flows
❌ **Bad**: "CAN-01 → Retrieve meetings"  
✅ **Good**: "CAN-01 (Calendar Retrieval) → Load all upcoming meetings within 2-week planning horizon (returns 45 events)"

### 4. Missing Dependencies
❌ **Bad**: List tasks in random order without dependencies  
✅ **Good**: "**Dependencies**: Requires CAN-07 (Metadata Extraction) - needs attendee list before analysis"

### 5. No Concrete Examples
❌ **Bad**: Only abstract workflow descriptions  
✅ **Good**: Include example flow with actual meeting data, attendee names, specific outputs

### 6. Inconsistent Formatting
❌ **Bad**: Some tasks use bullets, others use paragraphs  
✅ **Good**: All tasks use identical bullet format: **Purpose**:, **Input**:, etc.

### 7. Incomplete Statistics
❌ **Bad**: "Most prompts use this task"  
✅ **Good**: "89% frequency (8/9 prompts): organizer-1, organizer-2, ..."

### 8. Missing Cross-References
❌ **Bad**: Mention "parent task" without explanation  
✅ **Good**: "**Note**: PARENT task - enables CAN-05 (Attendees Analysis), CAN-13 (RSVP Update)"

---

## Templates for Copy-Paste

### Task Template
```markdown
#### Task [N]: [Task Name] (CAN-##)
- **Purpose**: [What this task does in THIS prompt's context]
- **Input**: [Specific data types and sources]
- **Output**: [Concrete outputs with examples]
- **Tier**: [Universal/Common/Specialized] (Tier [1/2/3])
- **Dependencies**: [Optional - "Requires CAN-## (Task Name)"]
- **Note**: [Optional - Special considerations]
```

### Execution Flow Template
```markdown
### Execution Composition

**How Tasks Work Together to Answer the Prompt:**

\```
STEP 1: [Phase Name]
CAN-## (Task Name) → [What happens with specifics]

STEP 2: [Phase Name]
CAN-## (Task Name) → [What happens]
CAN-## (Task Name) → [What happens]

STEP 3: [Phase Name]
CAN-## (Task Name) → [What happens with details]
  - [Sub-detail 1]
  - [Sub-detail 2]

OUTPUT: [Final result structure]
  - [Component 1]
  - [Component 2]
\```
```

### Example Flow Template
```markdown
**Example Flow for [Scenario]**:

\```
Input: "[Concrete example input]"

CAN-04: Extract → [Specific values] ✓
CAN-01: Retrieved → [Specific data] ✓
CAN-##: [Action] → [Specific result] ✓

Output: "[Specific output to user]"
\```
```

### Statistics Table Template
```markdown
| Metric | Value |
|--------|-------|
| **Total Prompts** | [N] |
| **Total Tasks** | [N] |
| **Tasks Used** | [N] |
| **Average Tasks/Prompt** | [X.X] |
```

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | November 7, 2025 | Chin-Yew Lin | Initial creation based on CANONICAL_TASKS_GOLD_STANDARD_REFERENCE.md format |

---

*This guide is a living document. Update as the format evolves and best practices are refined.*
