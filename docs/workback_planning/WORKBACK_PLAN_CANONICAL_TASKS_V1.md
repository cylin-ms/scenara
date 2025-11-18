# Workback Plan Canonical Tasks Framework V1.0

**Date**: November 17, 2025  
**Author**: Chin-Yew Lin  
**Framework**: Workback Planning Canonical Unit Tasks V1.0  
**Purpose**: Define atomic capabilities required for enterprise-grade workback plan generation

**Related Documents**:
- [Reference: Building an Automatic Work-Back Plan Generator Agent](../../workback_ado/Prompt%20what%20is%20a%20workback%20plan/Prompt%20what%20is%20a%20workback%20plan.md) - Industry best practices (10 steps)
- [Scenara Workback Planning Phase 1](../../src/workback_planning/) - Current implementation
- [Ollama Model Comparison Report](../../OLLAMA_MODEL_COMPARISON_REPORT.md) - 120b validation results

---

## Executive Summary

This document decomposes the **top-level workback planning task** into **atomic canonical unit tasks** using the same methodology applied to the 9 Calendar.AI hero prompts analysis.

**Top-Level Task**: 
> "Create a workback plan for [GOAL] by [DEADLINE]"

**Example Hero Prompts**:
1. "Create a workback plan for product launch on Dec 1, 2026"
2. "Generate a workback plan for my QBR presentation on Dec 15, 2025"
3. "Build a workback plan for newsletter launch in 4 weeks"
4. "Create a project plan working backward from my strategic initiatives review"

**Framework Characteristics**:
- **Total Canonical Tasks**: 15 (WBP-01 through WBP-15)
- **Reference Alignment**: Maps to reference document's 10 conceptual steps
- **Scenara Phase 1 Status**: 8/15 tasks implemented (53%)
- **Industry Standard**: Incorporates CPM, PERT, and PM best practices

**Key Insight**: 
Just as the 9 hero prompts required **25 canonical tasks** to decompose "organize my calendar" into atomic capabilities, workback planning requires **15 canonical tasks** to decompose "create a workback plan" into atomic project management capabilities.

---

## Canonical Task Framework Overview

### Tier Classification

**Tier 1: Foundation (Universal)** - Required for all workback plans
- **6 tasks** (WBP-01 through WBP-06)
- **Frequency**: 100% (every workback plan needs these)
- **Examples**: Goal extraction, milestone generation, task decomposition

**Tier 2: Enhancement (Common)** - Required for production quality
- **5 tasks** (WBP-07 through WBP-11)
- **Frequency**: 75%+ (most workback plans benefit)
- **Examples**: Critical path, backward scheduling, resource allocation

**Tier 3: Advanced (Specialized)** - Optional optimization features
- **4 tasks** (WBP-12 through WBP-15)
- **Frequency**: 25-50% (specialized use cases)
- **Examples**: Risk analysis, buffer allocation, multi-project coordination

### Scenara Implementation Status

| Tier | Tasks | Implemented | Status |
|------|-------|-------------|--------|
| **Tier 1** | 6 | 4 (67%) | ⚠️ Missing WBP-05, WBP-06 |
| **Tier 2** | 5 | 2 (40%) | ❌ Missing WBP-07, WBP-08, WBP-10 |
| **Tier 3** | 4 | 2 (50%) | ⚠️ Missing WBP-13, WBP-14 |
| **TOTAL** | **15** | **8 (53%)** | **Phase 1 Complete, Phase 2-3 Needed** |

---

## Tier 1: Foundation Tasks (Universal - Required for All Plans)

### WBP-01: Natural Language Understanding for Project Goals
**Status**: ✅ Implemented (Phase 1)  
**Reference Step**: Step 1 (Define Goal & Deadline)  
**Frequency**: 100%

**Purpose**: Extract project goal, deadline, constraints, and context from user input

**Capabilities**:
- Goal statement parsing ("launch product", "deliver QBR", "complete project")
- Deadline extraction (absolute dates, relative time expressions)
- Constraint identification (team size, resources, dependencies)
- Context extraction (meeting type, stakeholders, business priorities)
- Ambiguity resolution (clarifying questions for missing info)

**Input**: User prompt text or meeting context
**Output**: Structured project parameters
```json
{
  "goal": "Launch e-commerce website",
  "deadline": "2025-10-30",
  "constraints": {
    "team": {"developers": 2, "designer": 1, "qa": 1, "marketing": 1},
    "working_hours": "Mon-Fri, 8h/day",
    "holidays": ["US Federal holidays 2025"]
  },
  "meeting_context": {
    "type": "Project Launch",
    "duration": "6 weeks",
    "stakeholders": ["PM", "Engineering", "Marketing"]
  }
}
```

**Scenara Implementation**:
- ✅ LLMAPIClient with gpt-oss:120b
- ✅ analyze.md prompt (3.1KB) with context extraction
- ✅ Validated on 4 scenarios (Newsletter, Project Launch, QBR, Strategic Initiatives)

**Technical Requirements**:
- LLM integration (GPT-4, Claude, Ollama 120b)
- Temporal expression parsing (dates, durations)
- Entity recognition (people, teams, constraints)
- Meeting intelligence integration (context from calendar events)

---

### WBP-02: Milestone Identification & Hierarchical Breakdown
**Status**: ✅ Implemented (Phase 1)  
**Reference Step**: Step 2 (Break into Milestones)  
**Frequency**: 100%

**Purpose**: Decompose project goal into major milestones and phases

**Capabilities**:
- Hierarchical decomposition (project → phases → milestones)
- Critical milestone identification (launch gates, approvals, deadlines)
- Phase sequencing (logical ordering of major work chunks)
- Milestone dependency mapping (which milestones block others)
- Domain-specific patterns (QBR: data collection → analysis → drafting → review)

**Input**: Project goal and context from WBP-01
**Output**: Milestone hierarchy
```json
{
  "milestones": [
    {
      "id": "M1",
      "name": "Design Complete",
      "phase": "Phase 1: Design",
      "dependencies": [],
      "critical": true
    },
    {
      "id": "M2", 
      "name": "Development Done",
      "phase": "Phase 2: Build",
      "dependencies": ["M1"],
      "critical": true
    },
    {
      "id": "M3",
      "name": "QA Sign-off",
      "phase": "Phase 3: Test",
      "dependencies": ["M2"],
      "critical": true
    }
  ]
}
```

**Scenara Implementation**:
- ✅ O1 analysis stage generates hierarchical breakdown
- ✅ analyze.md prompt guides milestone identification
- ✅ Tested: Newsletter (4 phases), QBR (6 milestones), Project Launch (8 milestones)

**Technical Requirements**:
- LLM with reasoning capability (O1, Claude Opus, GPT-4)
- Domain knowledge (meeting types → typical milestone patterns)
- Hierarchical data structures (tree/graph representation)

---

### WBP-03: Task Decomposition & Granular Breakdown
**Status**: ✅ Implemented (Phase 1)  
**Reference Step**: Step 3 (Decompose into Tasks)  
**Frequency**: 100%

**Purpose**: Break down each milestone into concrete, actionable tasks

**Capabilities**:
- Task granularity optimization (not too high-level, not too detailed)
- Actionable task definition (clear verbs: create, review, approve, deploy)
- Task assignment (map to roles/participants)
- Deliverable identification (what artifact each task produces)
- Work estimation (task complexity and effort)

**Input**: Milestones from WBP-02
**Output**: Detailed task list
```json
{
  "tasks": [
    {
      "id": "T1",
      "name": "Create wireframes",
      "milestone": "M1",
      "description": "Design low-fidelity wireframes for all pages",
      "assigned_to": "Designer",
      "estimated_days": 3,
      "deliverable": "Wireframe document",
      "dependencies": []
    },
    {
      "id": "T2",
      "name": "Stakeholder review wireframes",
      "milestone": "M1",
      "description": "Present wireframes to PM and Engineering for feedback",
      "assigned_to": "Designer",
      "estimated_days": 2,
      "deliverable": "Approved wireframes",
      "dependencies": ["T1"]
    }
  ]
}
```

**Scenara Implementation**:
- ✅ O1 analysis generates 26-50 tasks per scenario
- ✅ structure.md prompt converts to Task model (7 Pydantic models)
- ✅ Quality: Newsletter (26 tasks), Strategic Initiatives (50 tasks)

**Validated Metrics** (November 16, 2025):
- Average: 37.8 tasks per workback plan
- Range: 26-50 tasks
- 120b vs 20b: 8× quality improvement

**Technical Requirements**:
- LLM with domain expertise (PM, project planning)
- Task taxonomy (historical task patterns by meeting type)
- Pydantic models for structured output validation

---

### WBP-04: Dependency Mapping & DAG Construction
**Status**: ✅ Implemented (Phase 1)  
**Reference Step**: Step 4 (Assign Dependencies)  
**Frequency**: 100%

**Purpose**: Map task relationships and build dependency graph

**Capabilities**:
- Dependency identification (what blocks what)
- Dependency type classification (hard blocker vs soft preference)
- Parallel task detection (which tasks can run simultaneously)
- DAG validation (ensure no circular dependencies)
- Predecessor/successor mapping

**Input**: Task list from WBP-03
**Output**: Dependency graph
```json
{
  "tasks": [
    {
      "id": "T3",
      "name": "Develop frontend",
      "dependencies": ["T2"],
      "dependency_type": "hard_blocker",
      "parallel_with": ["T4"]
    },
    {
      "id": "T4",
      "name": "Develop backend API",
      "dependencies": ["T2"],
      "dependency_type": "hard_blocker",
      "parallel_with": ["T3"]
    }
  ]
}
```

**Scenara Implementation**:
- ✅ Task.dependencies field (List[str])
- ✅ GPT-4 structuring stage maps dependencies
- ⚠️ Missing: networkx DAG validation (cycle detection)

**Gap Analysis**:
```python
# MISSING: DAG validation (from reference Section 5.3)
import networkx as nx

def validate_dependencies(plan: WorkbackPlan) -> bool:
    G = nx.DiGraph()
    for task in plan.tasks:
        G.add_node(task.id)
        for dep in task.dependencies:
            G.add_edge(dep, task.id)
    
    if not nx.is_directed_acyclic_graph(G):
        cycles = list(nx.simple_cycles(G))
        raise ValueError(f"Circular dependencies detected: {cycles}")
    
    return True
```

**Technical Requirements**:
- Graph algorithms library (networkx)
- Topological sorting for task ordering
- Cycle detection for validation
- Visualization for debugging (optional)

---

### WBP-05: Duration Estimation
**Status**: ❌ Missing (Phase 3 - CPM Enhancement)  
**Reference Step**: Step 5 (Estimate Durations)  
**Frequency**: 100%

**Purpose**: Estimate time required for each task based on complexity and team capacity

**Capabilities**:
- Base duration lookup (task taxonomy with historical data)
- Team efficiency scaling (adjust for team size, skill level)
- Complexity adjustment (simple vs complex tasks)
- Learning curve consideration (first-time vs repeated tasks)
- Domain-specific estimation (QBR prep: 2 days, product launch: 6 weeks)

**Input**: Tasks from WBP-03 + team profile
**Output**: Duration estimates
```json
{
  "tasks": [
    {
      "id": "T1",
      "name": "Create wireframes",
      "base_duration_days": 3.0,
      "team_efficiency_factor": 1.2,
      "adjusted_duration_days": 2.5,
      "confidence": 0.8
    }
  ]
}
```

**Reference Implementation** (from reference doc Section 5.1):
```python
def estimate_duration(task_name: str, team_profile: dict) -> float:
    """Estimate task duration with team efficiency scaling."""
    # Lookup base duration from historical data
    base = DURATION_TABLE.get(task_name.lower(), 3.0)  # default 3 days
    
    # Apply team efficiency factor
    factor = team_profile.get('efficiency_factor', 1.0)
    
    return round(base / factor, 2)
```

**Scenara Gap**:
- ❌ No historical duration lookup table
- ❌ No team efficiency modeling
- ⚠️ Currently: LLM generates estimated_days (no historical grounding)

**Why This Matters**:
- Without historical data, durations rely purely on LLM "intuition"
- Production systems need realistic, data-driven estimates
- Team capacity affects timeline feasibility

**Phase 3 Priority**: HIGH - Needed for accurate production timelines

**Technical Requirements**:
- Duration database (task name → average duration)
- Team profile storage (skill levels, efficiency factors)
- ML estimation model (trained on historical project data)
- Confidence scoring (how reliable is this estimate)

---

### WBP-06: Participant & Resource Identification
**Status**: ✅ Implemented (Phase 1)  
**Reference Step**: Step 8 (Allocate Resources)  
**Frequency**: 100%

**Purpose**: Identify stakeholders and assign ownership for tasks

**Capabilities**:
- Stakeholder identification (who needs to be involved)
- Role-based assignment (PM, Engineer, Designer, QA, Marketing)
- Responsibility mapping (RACI: Responsible, Accountable, Consulted, Informed)
- Expert identification (who has required skills)
- External stakeholder handling (customers, vendors, partners)

**Input**: Tasks from WBP-03 + meeting context
**Output**: Participant list with assignments
```json
{
  "participants": [
    {
      "id": "P1",
      "name": "Jane Doe",
      "role": "Product Manager",
      "email": "jane@company.com",
      "responsibility": "Accountable",
      "tasks_assigned": ["T1", "T5", "T10"]
    },
    {
      "id": "P2",
      "name": "Engineering Team",
      "role": "Development",
      "responsibility": "Responsible",
      "tasks_assigned": ["T3", "T4", "T6", "T7"]
    }
  ]
}
```

**Scenara Implementation**:
- ✅ Participant model (7 Pydantic models)
- ✅ 120b model extracts 5 participants on average (vs 20b: 0)
- ✅ Validated: Newsletter (4), QBR (5), Strategic Initiatives (5)

**Validated Metrics** (November 16, 2025):
- Average: 5.0 participants per workback plan
- Range: 4-6 participants
- 120b critical advantage: Participant extraction (20b complete failure)

**Gap**: No capacity modeling (can person handle 3 simultaneous tasks?)

**Technical Requirements**:
- Contact resolution (email → full profile)
- Organizational data (reporting structure, team membership)
- Skill matching (task requirements → expert identification)
- Capacity tracking (workload limits)

---

## Tier 2: Enhancement Tasks (Common - Required for Production Quality)

### WBP-07: Critical Path Analysis
**Status**: ❌ Missing (Phase 3 - CPM Enhancement)  
**Reference Step**: Step 6 (Calculate Critical Path)  
**Frequency**: 75%

**Purpose**: Identify longest dependency chain (project bottleneck)

**Capabilities**:
- Longest path calculation through dependency graph
- Critical task identification (tasks on critical path can't slip)
- Slack time calculation (non-critical tasks can slip)
- Bottleneck detection (where project is most at risk)
- "What-if" analysis (impact of task delays)

**Input**: Tasks with dependencies (WBP-04) and durations (WBP-05)
**Output**: Critical path analysis
```json
{
  "critical_path": {
    "total_duration_days": 42,
    "tasks": ["T1", "T2", "T3", "T6", "T8", "T10"],
    "bottleneck": "T6",
    "slack_time": {
      "T4": 5.0,
      "T5": 3.0,
      "T7": 0.0
    }
  }
}
```

**Reference Implementation** (from reference doc Section 5.3):
```python
import networkx as nx

def critical_path(plan):
    """Calculate longest path through dependency graph."""
    G = nx.DiGraph()
    
    # Build weighted graph (weight = duration + buffer)
    for task in plan.tasks:
        G.add_node(task.id, weight=task.duration_days + task.buffer_days)
        for dep in task.depends_on:
            G.add_edge(dep, task.id)
    
    # Find longest path (critical path)
    length = nx.dag_longest_path_length(G, weight='weight')
    path = nx.dag_longest_path(G, weight='weight')
    
    return length, path
```

**Why This Matters**:
- **Project Management 101**: Critical path determines project duration
- **Risk Management**: Tasks on critical path are high-priority (no slack)
- **Resource Optimization**: Non-critical tasks can be deprioritized if needed
- **Stakeholder Communication**: "Project takes 6 weeks minimum due to critical path"

**Scenara Gap**:
- ❌ No critical path calculation
- ❌ Can't identify which tasks are bottlenecks
- ❌ Can't answer "what's the minimum project duration?"

**Phase 3 Priority**: CRITICAL - Industry standard PM requirement

**Technical Requirements**:
- networkx library (DAG algorithms)
- Topological sorting for dependency order
- Weighted graph algorithms (longest path with task durations)
- Visualization (highlight critical path in Gantt chart)

---

### WBP-08: Backward Scheduling & Date Assignment
**Status**: ❌ Missing (Phase 2A - BLOCKER for calendar integration)  
**Reference Step**: Step 7 (Backward Schedule from Deadline)  
**Frequency**: 90%

**Purpose**: Assign concrete start/finish dates working backward from deadline

**Capabilities**:
- Backward pass from deadline (start at end, work to beginning)
- Business day calculation (skip weekends, holidays)
- Time zone handling (cross-timezone project teams)
- Buffer inclusion (add slack time to estimates)
- Dependency-aware scheduling (predecessor must finish before successor starts)

**Input**: Deadline + tasks with durations + holidays
**Output**: Task schedule with dates
```json
{
  "schedule": {
    "project_start": "2025-09-15",
    "project_end": "2025-10-30",
    "tasks": [
      {
        "id": "T10",
        "name": "Launch website",
        "start_date": "2025-10-30",
        "finish_date": "2025-10-30",
        "duration_days": 1,
        "working_days": 1
      },
      {
        "id": "T9",
        "name": "Final QA",
        "start_date": "2025-10-23",
        "finish_date": "2025-10-29",
        "duration_days": 5,
        "working_days": 5
      }
    ]
  }
}
```

**Reference Implementation** (from reference doc Section 5.4):
```python
import pandas as pd

def assign_dates(plan, deadline, holidays):
    """Backward schedule tasks from deadline."""
    # Business day calculator (skip weekends + holidays)
    bday = pd.tseries.offsets.CustomBusinessDay(
        weekmask='Mon Tue Wed Thu Fri',
        holidays=holidays
    )
    
    # Start from deadline
    current_date = deadline
    
    # Reverse topological sort (dependency order backward)
    for task in reversed(topological_sort(plan)):
        task.finish_date = current_date
        task.start_date = current_date - bday * task.duration_days
        
        # Propagate backward for next task
        current_date = task.start_date
    
    return plan
```

**Why This Is CRITICAL for Phase 2**:
Your Phase 2 wants to "Connect to calendar data (my_calendar_events_complete_attendees.json)" but:

**Without WBP-08**:
- Tasks have no dates, just relative order
- Can't integrate with calendar (no concrete dates to display)
- Can't answer "when do I need to start prep for Dec 15 QBR?"

**With WBP-08**:
- "QBR on Dec 15 → Draft slides due Dec 8 → Data collection due Dec 1"
- Can place workback tasks on calendar timeline
- Can trigger reminders ("Start financial report tomorrow")

**Scenara Gap**:
- ❌ No date assignment algorithm
- ❌ Can't convert "4-week timeline" to concrete dates
- ❌ **BLOCKS Phase 2 calendar integration**

**Phase 2A Priority**: CRITICAL BLOCKER - Must implement before calendar integration

**Technical Requirements**:
- pandas business day calendar (skip weekends/holidays)
- Topological sort (dependency-aware ordering)
- Time zone library (pytz, zoneinfo)
- Holiday calendar data (US Federal, regional, company-specific)

---

### WBP-09: Deliverable Identification & Tracking
**Status**: ✅ Implemented (Phase 1)  
**Reference Step**: Step 8 (part of resource allocation)  
**Frequency**: 80%

**Purpose**: Identify concrete outputs and artifacts from tasks

**Capabilities**:
- Deliverable extraction (what artifact does this task produce)
- Artifact type classification (document, code, review, approval)
- Deliverable dependency mapping (which deliverables enable other tasks)
- Quality gate definition (acceptance criteria for deliverables)
- Artifact reference linking (connect to document storage)

**Input**: Tasks from WBP-03
**Output**: Deliverable list
```json
{
  "deliverables": [
    {
      "id": "D1",
      "name": "Wireframe Document",
      "type": "Design Artifact",
      "producing_task": "T1",
      "consuming_tasks": ["T2", "T3"],
      "acceptance_criteria": ["All pages designed", "Stakeholder reviewed"],
      "artifact_reference": {
        "type": "sharepoint",
        "url": "https://company.sharepoint.com/designs/wireframes.pdf"
      }
    }
  ]
}
```

**Scenara Implementation**:
- ✅ Deliverable model (Pydantic)
- ✅ ArtifactReference model (links to SharePoint, OneDrive, etc.)
- ✅ 120b model extracts 4 deliverables on average (vs 20b: 0)

**Validated Metrics** (November 16, 2025):
- Average: 4.0 deliverables per workback plan
- Range: 0-6 deliverables (Strategic Initiatives stochastic: 0 first run, 6 second run)
- 120b critical advantage: Deliverable extraction (20b complete failure)

**Technical Requirements**:
- Document storage integration (SharePoint, OneDrive, Google Drive)
- Artifact type taxonomy (document, slide deck, report, code, review)
- Quality gate definition (acceptance criteria modeling)

---

### WBP-10: Constraint Satisfaction & Validation
**Status**: ❌ Missing (Phase 3)  
**Reference Step**: Step 9 (Validate for Conflicts)  
**Frequency**: 70%

**Purpose**: Validate workback plan meets all constraints and requirements

**Capabilities**:
- Deadline feasibility check (can we meet the deadline?)
- Resource conflict detection (person overallocated to multiple tasks)
- Dependency consistency validation (no orphaned tasks)
- Business rule enforcement (e.g., "no work on weekends")
- Holiday/availability checking (avoid scheduling during vacations)

**Input**: Complete workback plan with dates and assignments
**Output**: Validation report
```json
{
  "validation": {
    "deadline_feasible": true,
    "critical_path_duration": 38,
    "deadline_duration": 42,
    "slack_days": 4,
    "conflicts": [
      {
        "type": "resource_overallocation",
        "participant": "Jane Doe",
        "tasks": ["T3", "T5"],
        "date_range": "2025-10-15 to 2025-10-20",
        "severity": "warning"
      }
    ],
    "risks": [
      {
        "type": "tight_deadline",
        "description": "Only 4 days buffer before deadline",
        "mitigation": "Consider adding resources to critical path tasks"
      }
    ]
  }
}
```

**Reference Implementation** (from reference doc Section 8-9):
```python
def validate_plan(plan, deadline, holidays):
    """Validate workback plan constraints."""
    issues = []
    
    # Check 1: Deadline feasibility
    critical_path_length = calculate_critical_path(plan)
    if critical_path_length > deadline_days:
        issues.append({
            "type": "deadline_infeasible",
            "critical_path": critical_path_length,
            "deadline": deadline_days,
            "shortfall": critical_path_length - deadline_days
        })
    
    # Check 2: Resource conflicts
    for date in date_range:
        tasks_on_date = get_tasks_for_date(plan, date)
        by_person = group_by_participant(tasks_on_date)
        for person, tasks in by_person.items():
            if len(tasks) > 1:
                issues.append({
                    "type": "resource_conflict",
                    "person": person,
                    "date": date,
                    "tasks": tasks
                })
    
    # Check 3: DAG validation (no cycles)
    if not is_dag(plan):
        issues.append({"type": "circular_dependency"})
    
    return issues
```

**Scenara Gap**:
- ⚠️ Partial: Pydantic validates schema
- ❌ No deadline feasibility check
- ❌ No resource conflict detection
- ❌ No DAG cycle detection (missing from WBP-04)

**Phase 3 Priority**: HIGH - Production quality requirement

**Technical Requirements**:
- Constraint solver (feasibility checking)
- Resource allocation algorithms
- Calendar integration (holiday checking)
- Validation rule engine (business rules)

---

### WBP-11: Document Generation & Formatting
**Status**: ⚠️ Partial (JSON only, no visual timeline)  
**Reference Step**: Step 8 (Generate Timeline Artifact)  
**Frequency**: 80%

**Purpose**: Generate human-readable workback plan artifacts

**Capabilities**:
- JSON structured output (API consumption)
- Excel workbook generation (business user format)
- Google Sheets integration (collaborative editing)
- Gantt chart visualization (timeline view)
- PDF report generation (stakeholder distribution)

**Input**: Complete workback plan
**Output**: Multiple format artifacts

**Reference Implementation** (from reference doc Section 6):
```python
from openpyxl import Workbook
from openpyxl.styles import PatternFill

def generate_excel(plan, filename):
    """Generate Excel workbook with Gantt chart."""
    wb = Workbook()
    
    # Sheet 1: Summary
    ws_summary = wb.create_sheet("Summary")
    ws_summary['A1'] = "Goal"
    ws_summary['B1'] = plan.goal
    ws_summary['A2'] = "Deadline"
    ws_summary['B2'] = plan.deadline
    ws_summary['A3'] = "Critical Path Duration"
    ws_summary['B3'] = plan.critical_path_duration
    
    # Sheet 2: Tasks
    ws_tasks = wb.create_sheet("Tasks")
    headers = ["ID", "Name", "Owner", "Duration", "Start", "Finish", "Dependencies", "Critical"]
    for col, header in enumerate(headers, 1):
        ws_tasks.cell(1, col, header)
    
    for row, task in enumerate(plan.tasks, 2):
        ws_tasks.cell(row, 1, task.id)
        ws_tasks.cell(row, 2, task.name)
        ws_tasks.cell(row, 3, task.assigned_to)
        ws_tasks.cell(row, 4, task.duration_days)
        ws_tasks.cell(row, 5, task.start_date)
        ws_tasks.cell(row, 6, task.finish_date)
        ws_tasks.cell(row, 7, ", ".join(task.dependencies))
        ws_tasks.cell(row, 8, "Y" if task.on_critical_path else "N")
    
    # Sheet 3: Gantt (conditional formatting)
    ws_gantt = wb.create_sheet("Gantt")
    # Add Gantt chart using conditional formatting on date columns
    
    wb.save(filename)
```

**Scenara Implementation**:
- ✅ JSON output (WorkbackPlan Pydantic model)
- ✅ 7 Pydantic models for structured data
- ❌ No Excel export
- ❌ No Gantt chart visualization
- ❌ No Google Sheets integration

**Why This Matters**:
- JSON perfect for APIs, poor for business users
- Stakeholders expect Excel/Gantt charts (industry standard)
- Visual timeline critical for understanding dependencies

**Phase 3 Priority**: MEDIUM - Better UX, not functional blocker

**Technical Requirements**:
- openpyxl library (Excel generation)
- Google Sheets API (collaborative editing)
- Gantt chart library (plotly, matplotlib)
- PDF generation (reportlab, weasyprint)

---

## Tier 3: Advanced Tasks (Specialized - Optional Optimizations)

### WBP-12: Buffer Allocation & Risk Contingency
**Status**: ❌ Missing (Phase 3)  
**Reference Step**: Step 8 (part of resource allocation)  
**Frequency**: 50%

**Purpose**: Add time buffers for uncertainty and risk mitigation

**Capabilities**:
- Base buffer calculation (% of task duration)
- Risk-based buffer allocation (high-risk tasks get more buffer)
- Monte Carlo simulation (probabilistic duration modeling)
- Confidence intervals (50%, 90%, 99% completion dates)
- Buffer consumption tracking (how much buffer used during execution)

**Input**: Tasks with durations + risk assessment
**Output**: Tasks with buffer time
```json
{
  "tasks": [
    {
      "id": "T6",
      "name": "System integration testing",
      "base_duration_days": 5.0,
      "risk_level": "high",
      "buffer_days": 1.5,
      "total_duration_days": 6.5,
      "confidence_90_percent": 8.0
    }
  ]
}
```

**Reference Implementation** (from reference doc Section 5.2):
```python
def allocate_buffer(task):
    """Calculate buffer time for uncertainty."""
    # Base buffer: 10% of duration
    base_buffer = task.duration_days * 0.10
    
    # Risk adjustment: +0.5 day for high-risk tasks
    risk_keywords = ["integration", "migration", "deployment", "review"]
    if any(keyword in task.name.lower() for keyword in risk_keywords):
        risk_buffer = 0.5
    else:
        risk_buffer = 0.0
    
    return round(base_buffer + risk_buffer, 1)
```

**Scenara Gap**:
- ❌ No buffer allocation
- ❌ No risk-based adjustment
- ❌ Schedules assume perfect execution (unrealistic)

**Phase 3 Priority**: MEDIUM - Production quality improvement

**Technical Requirements**:
- Risk assessment model (identify high-risk tasks)
- Statistical modeling (probability distributions)
- Monte Carlo simulation (optional, for complex projects)

---

### WBP-13: Historical Pattern Learning
**Status**: ❌ Missing (Phase 4+)  
**Reference Step**: Enhancement to Step 5 (Duration Estimation)  
**Frequency**: 30%

**Purpose**: Learn from historical project data to improve estimates

**Capabilities**:
- Historical duration lookup (actual vs estimated analysis)
- Pattern recognition (similar projects → similar timelines)
- Team velocity tracking (how fast does this team work)
- Accuracy improvement (refine estimates based on actuals)
- Anomaly detection (unusual deviations from historical patterns)

**Input**: Historical project data + current workback plan
**Output**: Refined duration estimates
```json
{
  "task": {
    "id": "T3",
    "name": "Develop frontend",
    "llm_estimate_days": 10.0,
    "historical_average_days": 12.5,
    "team_velocity_factor": 0.9,
    "refined_estimate_days": 11.3,
    "confidence": 0.85,
    "historical_samples": 15
  }
}
```

**Why This Matters**:
- LLM estimates are generic (no company-specific knowledge)
- Historical data grounds estimates in reality
- Team velocity varies (experienced team faster than new team)

**Scenara Gap**:
- ❌ No historical data collection
- ❌ No pattern matching against past projects
- ❌ Pure LLM estimates (no historical grounding)

**Phase 4 Priority**: LOW - Nice-to-have, requires data collection infrastructure

**Technical Requirements**:
- Time tracking integration (Jira, Azure DevOps)
- Historical database (completed projects)
- ML pattern matching (similar project detection)
- Team velocity calculation (story points, task completion rates)

---

### WBP-14: Multi-Project Coordination
**Status**: ❌ Missing (Phase 4+)  
**Reference Step**: Enhancement (not in reference 10 steps)  
**Frequency**: 20%

**Purpose**: Coordinate workback plans across multiple related projects

**Capabilities**:
- Cross-project dependency detection (Project A blocks Project B)
- Resource contention resolution (same person on multiple projects)
- Portfolio-level optimization (prioritize critical projects)
- Master timeline generation (combined Gantt for all projects)
- Dependency propagation (delay in Project A affects Project B)

**Input**: Multiple workback plans
**Output**: Coordinated portfolio plan
```json
{
  "portfolio": {
    "projects": ["Project A", "Project B", "Project C"],
    "cross_project_dependencies": [
      {
        "blocking_project": "Project A",
        "blocking_task": "T5",
        "blocked_project": "Project B",
        "blocked_task": "T1",
        "reason": "Requires API from Project A"
      }
    ],
    "resource_conflicts": [
      {
        "person": "Jane Doe",
        "projects": ["Project A", "Project C"],
        "date_range": "2025-10-01 to 2025-10-15",
        "resolution": "Delay Project C by 2 weeks"
      }
    ]
  }
}
```

**Scenara Gap**:
- ❌ Single-project focus only
- ❌ No cross-project coordination
- ❌ No portfolio-level view

**Phase 4 Priority**: LOW - Advanced enterprise feature

**Technical Requirements**:
- Multi-project data model
- Cross-project dependency graph
- Resource allocation solver (optimization)
- Portfolio management UI

---

### WBP-15: Workback Plan Evaluation & Quality Scoring
**Status**: ✅ Implemented (Phase 1)  
**Reference Step**: Step 10 (Validate & Iterate)  
**Frequency**: 100% (internal quality assurance)

**Purpose**: Evaluate workback plan quality and completeness

**Capabilities**:
- Completeness scoring (all required elements present)
- Quality assessment (reasonable durations, clear dependencies)
- GUTT v4.0 integration (meeting intelligence quality framework)
- Benchmark comparison (vs gold standard plans)
- Improvement recommendations

**Input**: Generated workback plan
**Output**: Quality score and feedback
```json
{
  "evaluation": {
    "overall_score": 8.2,
    "dimensions": {
      "completeness": 9.0,
      "task_granularity": 8.5,
      "dependency_clarity": 7.5,
      "resource_allocation": 8.0,
      "timeline_realism": 8.5
    },
    "strengths": [
      "Clear milestone structure",
      "Detailed task breakdown (37 tasks)",
      "All participants identified"
    ],
    "weaknesses": [
      "Missing critical path analysis",
      "No concrete dates assigned",
      "Some tasks lack clear deliverables"
    ],
    "recommendations": [
      "Add WBP-07 (Critical Path Analysis)",
      "Implement WBP-08 (Backward Scheduling)",
      "Refine deliverable identification for T12, T15, T18"
    ]
  }
}
```

**Scenara Implementation**:
- ✅ 4-scenario validation (Newsletter, Project Launch, QBR, Strategic Initiatives)
- ✅ Quality metrics tracked (tasks, deliverables, participants, dependencies)
- ✅ November 16 testing: F1 scores, consistency analysis
- ⚠️ Manual evaluation (no automated GUTT v4.0 integration yet)

**Validated Metrics** (November 16, 2025):
- Average task quality: 37.8 tasks (26-50 range)
- Deliverable extraction: 4.0 avg (0-6 range)
- Participant identification: 5.0 avg (4-6 range)
- First-attempt success: 75% (3/4 scenarios)

**Phase 4 Priority**: HIGH - Already started, needs GUTT integration

**Technical Requirements**:
- GUTT v4.0 framework integration
- Quality scoring model (trained on gold standard plans)
- Automated evaluation pipeline
- Feedback generation (actionable recommendations)

---

## Hero Prompt Analysis: "Create a Workback Plan for Product Launch on Dec 1, 2026"

### Canonical Task Decomposition

**How Tasks Work Together to Answer the Hero Prompt:**

```
HERO PROMPT: "Create a workback plan for product launch on Dec 1, 2026"

EXECUTION FLOW:

STEP 1: Understand Project Goal (WBP-01)
  Input: "Create a workback plan for product launch on Dec 1, 2026"
  Output: {
    "goal": "Product launch",
    "deadline": "2026-12-01",
    "meeting_type": "Project Launch",
    "constraints": []
  }

STEP 2: Identify Milestones (WBP-02)
  Input: Project goal from WBP-01
  LLM Analysis: Break down product launch into phases
  Output: [
    "M1: Product Requirements Complete",
    "M2: Design & Prototyping Done",
    "M3: Development Complete",
    "M4: Testing & QA Sign-off",
    "M5: Marketing Materials Ready",
    "M6: Launch Day"
  ]

STEP 3: Decompose into Tasks (WBP-03)
  Input: Milestones from WBP-02
  LLM Analysis: For each milestone, generate actionable tasks
  Output: 40 tasks across 6 milestones
    - M1: T1-T5 (requirements gathering, stakeholder interviews, PRD)
    - M2: T6-T12 (wireframes, prototypes, design review)
    - M3: T13-T25 (frontend, backend, API, integration)
    - M4: T26-T32 (unit tests, integration tests, UAT)
    - M5: T33-T38 (website, collateral, launch email)
    - M6: T39-T40 (go-live, monitoring)

STEP 4: Map Dependencies (WBP-04)
  Input: Tasks from WBP-03
  Analysis: Identify what blocks what
  Output: Dependency graph
    - T1 → T2 → T3 (sequential requirements)
    - T6 requires T5 (design needs PRD)
    - T13-T25 require T12 (dev needs approved design)
    - T26-T32 require T25 (QA needs dev complete)
    - etc.

STEP 5: Estimate Durations (WBP-05) ❌ MISSING
  Input: Tasks + team profile
  Should Do: Lookup historical durations, adjust for team
  Current: LLM generates estimated_days (no historical grounding)
  
STEP 6: Identify Participants (WBP-06) ✅ DONE
  Input: Tasks from WBP-03
  LLM Analysis: Map roles to tasks
  Output: [
    "Product Manager" (T1-T5, T33-T38),
    "Designer" (T6-T12),
    "Engineering Team" (T13-T25),
    "QA Team" (T26-T32),
    "Marketing Team" (T33-T38)
  ]

STEP 7: Calculate Critical Path (WBP-07) ❌ MISSING
  Input: Tasks with dependencies + durations
  Should Do: Find longest path through graph
  Current: No critical path identification
  Missing Output: "Critical path = T1→T3→T5→T12→T25→T32 = 120 days"

STEP 8: Backward Schedule (WBP-08) ❌ MISSING - CRITICAL GAP
  Input: Deadline (Dec 1, 2026) + critical path (120 days)
  Should Do: Work backward assigning dates
  Current: No date assignment
  Missing Output: "Start date = Aug 3, 2026"
    - T40 (Launch): Dec 1, 2026
    - T32 (QA Complete): Nov 24, 2026
    - T25 (Dev Complete): Oct 15, 2026
    - T12 (Design Approved): Sep 1, 2026
    - T5 (PRD Done): Aug 15, 2026
    - T1 (Kickoff): Aug 3, 2026

STEP 9: Identify Deliverables (WBP-09) ✅ DONE
  Input: Tasks from WBP-03
  LLM Analysis: Extract concrete outputs
  Output: [
    "PRD Document",
    "Design Mockups",
    "Working Prototype",
    "Tested Codebase",
    "Launch Materials"
  ]

STEP 10: Validate Constraints (WBP-10) ❌ MISSING
  Input: Complete plan
  Should Do: Check deadline feasibility, resource conflicts
  Current: Pydantic validates schema only
  Missing: "✓ Deadline feasible (120 days < 150 available), ⚠️ Resource conflict on T15-T18"

STEP 11: Generate Document (WBP-11) ⚠️ PARTIAL
  Input: Complete plan
  Current: JSON output only
  Missing: Excel workbook with Gantt chart

OUTPUT TO USER:
  ✅ JSON WorkbackPlan with 40 tasks, 6 milestones, 5 participants
  ❌ No start date ("when do I start?")
  ❌ No critical path ("what are the bottlenecks?")
  ❌ No visual timeline (Excel/Gantt)
```

### Scenara Status vs Hero Prompt Requirements

| Requirement | Canonical Tasks | Scenara Status |
|-------------|----------------|----------------|
| Understand goal & deadline | WBP-01 | ✅ Implemented |
| Break into milestones | WBP-02 | ✅ Implemented |
| Decompose into tasks | WBP-03 | ✅ Implemented (40 tasks) |
| Map dependencies | WBP-04 | ✅ Implemented |
| Estimate durations | WBP-05 | ❌ Missing (LLM only) |
| Identify participants | WBP-06 | ✅ Implemented (5 participants) |
| **Calculate critical path** | **WBP-07** | **❌ MISSING - High Priority** |
| **Assign start/finish dates** | **WBP-08** | **❌ MISSING - CRITICAL BLOCKER** |
| Identify deliverables | WBP-09 | ✅ Implemented (5 deliverables) |
| Validate plan | WBP-10 | ❌ Missing |
| Generate timeline doc | WBP-11 | ⚠️ Partial (JSON only) |

**Can Scenara answer this hero prompt today?**
- ⚠️ **PARTIAL**: Can generate task breakdown, dependencies, participants, deliverables
- ❌ **CANNOT**: Assign concrete dates, identify critical path, validate deadline feasibility
- ❌ **BLOCKS Phase 2**: Calendar integration requires WBP-08 (date assignment)

---

## Summary: Implementation Roadmap

### Phase 1: COMPLETE ✅ (November 2025)
**Implemented Tasks**: 8/15 (53%)
- ✅ WBP-01: Natural Language Understanding
- ✅ WBP-02: Milestone Identification
- ✅ WBP-03: Task Decomposition (37.8 avg tasks)
- ✅ WBP-04: Dependency Mapping
- ✅ WBP-06: Participant Identification (5.0 avg participants)
- ✅ WBP-09: Deliverable Identification (4.0 avg deliverables)
- ✅ WBP-11: Document Generation (JSON only)
- ✅ WBP-15: Quality Evaluation (manual)

**Validation**: 4 scenarios tested, 120b model validated (3m24s avg, 75% first-attempt success)

### Phase 2A: CRITICAL PREREQUISITES (Recommended Next - 1 week)
**Priority Tasks**: 2/15
- 🎯 **WBP-08: Backward Scheduling** (BLOCKER for calendar integration)
  - Assign concrete start/finish dates
  - Business day calculation
  - ~100 lines with pandas
- 🎯 **WBP-04: DAG Validation** (Complete existing task)
  - Add networkx cycle detection
  - ~20 lines

**Deliverable**: Workback plans with concrete dates ("Start Dec 1, finish Dec 15")

### Phase 2B: MEETING INTELLIGENCE INTEGRATION (After 2A - 2 weeks)
**Goal**: Connect workback planning to calendar data
- Integrate with `my_calendar_events_complete_attendees.json`
- Map meeting deadlines → workback task dates
- Add to meeting preparation workflow

**Dependencies**: Requires Phase 2A (WBP-08) to have dates to integrate

### Phase 3: CPM ENHANCEMENT LAYER (3-4 weeks)
**Priority Tasks**: 3/15
- 🎯 **WBP-07: Critical Path Analysis** (Industry standard PM requirement)
- 🎯 **WBP-05: Duration Estimation** (Historical data grounding)
- 🎯 **WBP-10: Constraint Satisfaction** (Production quality validation)
- 🔧 **WBP-12: Buffer Allocation** (Risk mitigation)

**Deliverable**: Production-grade workback planning with critical path, realistic estimates, validation

### Phase 4: ADVANCED FEATURES (Future - 2-4 weeks)
**Optional Tasks**: 2/15
- WBP-11: Excel/Sheets Export (Stakeholder UX)
- WBP-13: Historical Pattern Learning (Accuracy improvement)
- WBP-14: Multi-Project Coordination (Enterprise portfolio)
- WBP-15: GUTT v4.0 Integration (Automated evaluation)

---

## Alignment with Reference Document

### Reference 10-Step Methodology Mapping

| Reference Step | Canonical Task(s) | Scenara Status |
|---------------|-------------------|----------------|
| 1. Define Goal & Deadline | WBP-01 | ✅ Complete |
| 2. Break into Milestones | WBP-02 | ✅ Complete |
| 3. Decompose into Tasks | WBP-03 | ✅ Complete |
| 4. Assign Dependencies | WBP-04 | ✅ Complete |
| 5. Estimate Durations | WBP-05 | ❌ Missing |
| 6. Calculate Critical Path | WBP-07 | ❌ Missing |
| 7. Backward Schedule | WBP-08 | ❌ Missing |
| 8. Allocate Resources & Buffers | WBP-06, WBP-12 | ⚠️ Partial |
| 9. Generate Timeline Artifact | WBP-11 | ⚠️ Partial |
| 10. Validate & Iterate | WBP-10, WBP-15 | ⚠️ Partial |

**Scenara Completion vs Reference**: 4/10 steps fully implemented (40%)

### Key Insight
Just as 9 Calendar.AI hero prompts required 25 canonical tasks, workback planning requires 15 canonical tasks that map directly to the reference document's 10-step industry-standard methodology.

**Scenara's advantage**: LLM-native implementation (Steps 1-4) is more sophisticated than traditional algorithmic approaches. The reference assumes manual milestone definition; Scenara's 120b LLM generates them automatically with high quality (37.8 tasks, 5 participants, 4 deliverables on average).

**Scenara's gap**: Missing algorithmic enhancements (Steps 5-7) that convert LLM's implicit reasoning into concrete, actionable timelines with dates.

---

**Document Version**: 1.0  
**Created**: November 17, 2025  
**Next Review**: After Phase 2A implementation (WBP-08 backward scheduling)
