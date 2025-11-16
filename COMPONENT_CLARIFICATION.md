# Scenara Components Clarification

**Date**: November 13, 2025  
**Purpose**: Clarify separation between different Scenara features

---

## Component Separation

### 1. Workback Planning (src/workback_planning/)

**Purpose**: AI-powered project workback planning using Stratos-Exp architecture

**What it does**:
- Takes a meeting context as input (Graph API format)
- Uses two-stage LLM pipeline (O1 analysis + GPT-4 structuring)
- Generates complete workback plans with:
  - Milestones with due dates
  - Tasks with dependencies
  - Deliverables and artifacts
  - Participant assignments

**Status**: ✅ Phase 1 Complete
- Module structure created
- Data models adapted
- LLM client integrated
- Prompt templates copied
- Ready for testing

**Integration Point**: Meeting Intelligence Pipeline
- Input: Meeting from calendar or example scenarios
- Process: Generate workback plan
- Output: Structured project plan with tasks/milestones

**Example Use Case**:
```python
from src.workback_planning import generate_plan

meeting_context = """
Meeting: Q4 Business Review
Date: December 15, 2025
Participants: CEO, CFO, Division Heads
Goal: Review performance, align on Q1 priorities
"""

result = generate_plan(meeting_context)
# Returns: {'analysis': '...', 'structured': {...}}
```

---

### 2. ADO Workback Classification (workback_ado/)

**Purpose**: LLM-based classification and analysis of Azure DevOps work items

**What it does**:
- Classifies ADO work items (181 items from Scenara project)
- Determines if items need workback planning
- Compares LLM vs heuristic classification
- Expert review workflow for corrections

**Status**: ✅ Complete (November 12-13, 2025)
- LLM batch classification complete
- Expert review tools created
- Comparison analysis done
- Not related to the Stratos-Exp integration

**Tools**:
- `ado_workback_extraction.py`: Extract ADO items
- `compare_llm_vs_heuristic.py`: Compare classification methods
- `expert_review_workflow.py`: Human review UI

**Example Workback Plans**: The 7 workback plan examples (QBR, Board Meeting, etc.) in `workback_ado/` are **reference scenarios** showing what good workback plans look like, not training data.

---

### 3. Meeting Schema Alignment (tools/align_workback_meeting_schema.py)

**Purpose**: Ensure consistency between real calendar data and workback planning inputs

**What it does**:
- Parses meeting context from markdown files
- Converts to Microsoft Graph API schema (SilverFlow format)
- Validates required fields
- Prepares meeting objects as input for workback generator

**Status**: ✅ Complete
- All 7 workback plan examples aligned
- 100% validation success rate
- Ready to use with workback generator

**Why it matters**:
- Real calendar meetings from SilverFlow follow Graph API schema
- Workback plan examples need to follow same schema
- Generator can accept both real meetings and example scenarios
- Consistent input format = reliable output

**Not Used For**: Training data generation (that's a separate concern)

---

### 4. Meeting Intelligence Pipeline (meeting_intelligence.py)

**Purpose**: Core meeting analysis and preparation system

**What it does**:
- Classifies meeting types (31+ types)
- Analyzes meeting importance
- Generates preparation recommendations
- Integrates with calendar data

**Status**: ✅ Operational
- Using GUTT v4.0 evaluation framework
- Connected to SilverFlow calendar extraction
- Ready for workback planning integration (Phase 2)

**Future Integration**: Will incorporate workback planning generator to automatically create project plans for high-complexity meetings

---

## Relationship Between Components

```
Real Calendar Data (SilverFlow)
        ↓
Meeting Intelligence Pipeline
        ↓
Meeting Classification & Analysis
        ↓
High-Complexity Meeting Detected
        ↓
Meeting Schema Alignment ← Workback Plan Examples
        ↓
Workback Planning Generator (src/workback_planning/)
        ↓
Generated Workback Plan (tasks, milestones, dependencies)
        ↓
Present to User
```

**Separate Flow**: ADO classification is a parallel feature for analyzing Azure DevOps work items, not part of the meeting intelligence flow.

---

## What's NOT Connected

### ADO Post-Training ❌
- **Misconception**: Workback plan examples are training data
- **Reality**: They are reference scenarios and validation examples
- **Separation**: ADO classification is about work items, not meetings

### Synthetic Training Data ❌
- **Misconception**: Schema alignment is for generating training data
- **Reality**: It's for ensuring consistent input to the workback generator
- **Separation**: Training data generation (if needed) would be a separate pipeline

---

## Current State (November 13, 2025)

### ✅ Complete
1. **Workback Planning Module** (Phase 1)
   - src/workback_planning/ fully implemented
   - Two-stage LLM pipeline ready
   - Data models and prompts adapted

2. **Meeting Schema Alignment**
   - 7 workback plan examples converted to Graph API format
   - Validation tool created
   - Ready to use as generator input

3. **ADO Workback Classification**
   - 181 ADO items classified
   - Expert review tools operational
   - Comparison analysis complete

### 🔄 In Progress
1. **Workback Generator Testing** (Phase 1, Task #6)
   - Need to run test with Ollama or OpenAI
   - Validate two-stage pipeline
   - Confirm output structure

### 📋 Next Steps
1. **Phase 2: Meeting Intelligence Integration**
   - Integrate workback generator into meeting_intelligence.py
   - Use real calendar meetings as input
   - Test with high-complexity scenarios

2. **Phase 3: CPM Enhancement** (Optional)
   - Add critical path analysis from WorkbackPlan/src/
   - Resource allocation optimization
   - Timeline compression

3. **Phase 4: Evaluation & Quality**
   - Adapt O1-based evaluation from Stratos-Exp
   - Integrate with GUTT v4.0
   - Quality metrics dashboard

---

## Key Takeaway

**Workback Planning** = Take a meeting context → Generate project plan with tasks/milestones

**ADO Classification** = Analyze Azure DevOps items → Determine which need workback planning

**Meeting Schema Alignment** = Ensure consistent meeting format → Input to workback generator

These are **three separate features** with different purposes, not a single training data pipeline.

---

**Documentation Updated**: November 13, 2025  
**Clarification**: Removed incorrect ADO post-training references  
**Focus**: Workback planning for meeting intelligence, not training data generation
