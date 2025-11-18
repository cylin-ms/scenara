# Workback Plan Quality Evaluation Framework V1.0

**Date**: November 17, 2025  
**Author**: Chin-Yew Lin  
**Purpose**: Assertion-based quality evaluation for LLM-generated workback plans using LLM-as-Judge  
**Framework**: ACRUE-based checklist methodology (extends GUTT v4.0)

**Related Documents**:
- [Workback Plan Canonical Tasks V1.0](./WORKBACK_PLAN_CANONICAL_TASKS_V1.md) - 15 canonical tasks framework
- [GUTT v4.0 Analysis](../gutt_analysis/) - Meeting intelligence quality framework
- [Ollama Model Comparison Report](../../OLLAMA_MODEL_COMPARISON_REPORT.md) - 120b validation results
- [Reference: Building Workback Plan Generator](../../workback_ado/Prompt%20what%20is%20a%20workback%20plan/Prompt%20what%20is%20a%20workback%20plan.md)

---

## Executive Summary

This framework uses **assertion-based evaluation** with **LLM-as-Judge** to assess workback plan quality without requiring "perfect" gold standards.

**Evaluation Philosophy**:
> "There is no perfect plan, only a reasonable plan. Use objective assertions that humans or LLMs can verify, not subjective comparisons against gold standards."

**Key Principles**:
1. **Assertion-based**: Each quality check is a yes/no/partial question
2. **LLM-as-Judge**: GPT-4 or Claude evaluates assertions objectively
3. **ACRUE framing**: Structure assertions around Accuracy, Completeness, Relevance, Usefulness, Effectiveness
4. **Binary scoring**: Pass/Fail/Partial (not subjective 0-100 scales)
5. **Human-verifiable**: Each assertion can be checked by human reviewers

**ACRUE Framework Applied to Workback Planning**:
- **Accuracy**: Are facts, dates, dependencies correct?
- **Completeness**: Are all necessary elements present?
- **Relevance**: Do tasks align with the goal?
- **Usefulness**: Can stakeholders execute this plan?
- **Exceptional**: Does the plan go beyond common expectations?

**Methodology**:
1. **Phase 1**: Define assertion checklist (50-60 assertions across ACRUE)
2. **Phase 2**: LLM-as-Judge evaluates each assertion (GPT-4 or Claude as evaluator)
3. **Phase 3**: Calculate pass rate (% assertions passed)
4. **Phase 4**: Human spot-check (validate 10-20% of LLM judgments)

**Current Status**: Phase 1 (this document) - defining assertion checklist

---

## ACRUE Assertion Framework

### Overview: 5 ACRUE Categories with 50+ Assertions

Each assertion is a **binary or ternary check** (Pass ✅ / Fail ❌ / Partial ⚠️) that can be evaluated objectively by LLM-as-Judge or human reviewer.

| ACRUE Category | Assertions | Weight | Focus |
|----------------|------------|--------|-------|
| **A - Accuracy** | 10 assertions | 20% | Facts, dates, dependencies are correct |
| **C - Completeness** | 15 assertions | 25% | All necessary elements present |
| **R - Relevance** | 10 assertions | 20% | Tasks align with goal and context |
| **U - Usefulness** | 10 assertions | 20% | Plan is actionable and executable |
| **E - Exceptional** | 5 assertions | 15% | Plan exceeds common expectations |

**Total**: 50 assertions (can expand to 60+ with sub-assertions)

**Scoring**:
- **Pass (✅)**: 1.0 point
- **Partial (⚠️)**: 0.5 point  
- **Fail (❌)**: 0.0 point
- **Overall Score**: (Total Points / Total Assertions) × 100

**Quality Tiers** (based on pass rate):
- **Excellent**: ≥90% pass rate (45+/50 assertions)
- **Good**: 80-89% pass rate (40-44/50 assertions)
- **Acceptable**: 70-79% pass rate (35-39/50 assertions)
- **Poor**: 60-69% pass rate (30-34/50 assertions)
- **Fail**: <60% pass rate (<30/50 assertions)

---

## A - Accuracy Assertions (10 assertions, 20% weight)

**Focus**: Are facts, dates, dependencies, and relationships correct?

### A1: Goal Extraction Accuracy
**Assertion**: The workback plan correctly identifies the primary goal from the input prompt.

**Evaluation Prompt** (for LLM-as-Judge):
```
Given:
- Input prompt: "{original_prompt}"
- Workback plan goal: "{plan.goal}"

Question: Does the workback plan goal accurately capture the primary objective from the input prompt?

Answer with one of:
- PASS: Goal is accurately extracted
- PARTIAL: Goal is partially correct but missing key details
- FAIL: Goal is incorrect or missing
```

**Example**:
- Input: "Create a workback plan for product launch on Dec 1, 2026"
- Plan Goal: "Product launch" → **PASS** ✅
- Plan Goal: "Project planning" → **FAIL** ❌ (too generic)
- Plan Goal: "Product development" → **PARTIAL** ⚠️ (close but not exact)

---

### A2: Deadline Identification
**Assertion**: The workback plan correctly identifies the deadline (date or time constraint).

**Evaluation Prompt**:
```
Given:
- Input prompt: "{original_prompt}"
- Workback plan deadline: "{plan.deadline}"

Question: Does the workback plan correctly identify the deadline?

Answer with one of:
- PASS: Deadline is correctly identified
- FAIL: Deadline is missing or incorrect
```

**Example**:
- Input: "newsletter launch on December 15"
- Plan Deadline: "2025-12-15" → **PASS** ✅
- Plan Deadline: null → **FAIL** ❌
- Plan Deadline: "2025-12-01" → **FAIL** ❌ (wrong date)

---

### A3: Dependency Logic Validity
**Assertion**: Task dependencies follow logical order (no task depends on a future task that depends on it).

**Evaluation Prompt**:
```
Given the task list with dependencies:
{task_list_with_dependencies}

Question: Are all task dependencies logically valid (no circular dependencies)?

Answer with one of:
- PASS: All dependencies are logical, DAG is valid
- FAIL: Circular dependencies detected OR illogical dependencies

To verify: Construct dependency graph and check for cycles.
```

**Automated Check**:
```python
import networkx as nx

def check_dependency_validity(plan: WorkbackPlan) -> str:
    """A3: Check for circular dependencies."""
    G = nx.DiGraph()
    for task in plan.tasks:
        G.add_node(task.id)
        for dep in task.dependencies:
            G.add_edge(dep, task.id)
    
    if nx.is_directed_acyclic_graph(G):
        return "PASS"
    else:
        cycles = list(nx.simple_cycles(G))
        return f"FAIL: Circular dependencies detected: {cycles}"
```

---

### A4: Task Sequencing Logic
**Assertion**: Tasks that must happen sequentially are properly ordered (e.g., design before development, testing after development).

**Evaluation Prompt**:
```
Given the task list:
{task_list}

Question: Are tasks that have natural sequential order (design → develop → test) properly ordered via dependencies?

Answer with one of:
- PASS: Sequential tasks have correct dependencies
- PARTIAL: Most sequential relationships correct, minor issues
- FAIL: Major sequencing errors (e.g., testing before development)

Check for common patterns:
- Requirements → Design → Development → Testing → Launch
- Draft → Review → Revise → Approve
```

---

### A5: Milestone Placement Accuracy
**Assertion**: Milestones are placed at logical completion points (not arbitrary task boundaries).

**Evaluation Prompt**:
```
Given the milestones and their associated tasks:
{milestone_list}

Question: Are milestones placed at logical phase completion points?

Answer with one of:
- PASS: Milestones mark clear phase boundaries (e.g., "Design Complete", "QA Sign-off")
- PARTIAL: Most milestones logical, some arbitrary
- FAIL: Milestones are arbitrary or poorly placed
```

---

### A6: Participant Role Accuracy
**Assertion**: Participants have roles that match their assigned tasks.

**Evaluation Prompt**:
```
Given participants and their assigned tasks:
{participant_task_mapping}

Question: Do participant roles align with their assigned tasks?

Answer with one of:
- PASS: All participants have appropriate roles for their tasks
- PARTIAL: Most roles appropriate, some mismatches
- FAIL: Significant role-task mismatches (e.g., "Designer" assigned to "Deploy backend")
```

---

### A7: Deliverable-Task Alignment
**Assertion**: Each deliverable is actually produced by its associated task.

**Evaluation Prompt**:
```
Given deliverables and producing tasks:
{deliverable_task_mapping}

Question: Do the producing tasks logically create the listed deliverables?

Answer with one of:
- PASS: All deliverable-task pairs are logical
- PARTIAL: Most pairs logical, some unclear
- FAIL: Deliverables don't match their producing tasks
```

**Example**:
- Task: "Design wireframes" → Deliverable: "Wireframe document" → **PASS** ✅
- Task: "Design wireframes" → Deliverable: "Production code" → **FAIL** ❌

---

### A8: Duration Realism
**Assertion**: Estimated task durations are realistic (not too short or too long).

**Evaluation Prompt**:
```
Given tasks with estimated durations:
{task_duration_list}

Question: Are task durations realistic for the work described?

Answer with one of:
- PASS: All durations seem realistic
- PARTIAL: Most durations reasonable, some questionable
- FAIL: Many unrealistic durations (e.g., "Build entire system: 1 day")

Consider:
- Simple tasks: 1-3 days
- Complex tasks: 5-10 days
- Extremely complex: 10-20 days
```

---

### A9: Stakeholder Coverage Accuracy
**Assertion**: All stakeholders mentioned in the input are represented in the participant list.

**Evaluation Prompt**:
```
Given:
- Input prompt mentions stakeholders: {input_stakeholders}
- Workback plan participants: {plan_participants}

Question: Are all input stakeholders represented in the plan?

Answer with one of:
- PASS: All mentioned stakeholders included
- PARTIAL: Most stakeholders included, some missing
- FAIL: Key stakeholders missing
```

---

### A10: Constraint Capture Accuracy
**Assertion**: Constraints mentioned in the input (approvals, dependencies, resources) are reflected in the plan.

**Evaluation Prompt**:
```
Given:
- Input prompt constraints: "{input_constraints}"
- Workback plan structure: {plan_structure}

Question: Are input constraints properly reflected in the plan?

Answer with one of:
- PASS: All constraints captured (e.g., approval chains, resource limits)
- PARTIAL: Most constraints captured, some missing
- FAIL: Key constraints ignored

Examples of constraints:
- "Need LT approval before exec review" → Should have dependency T_lt_review → T_exec_review
- "Marketing Ops handles final production" → Should have Marketing Ops participant assigned to production task
```

---

## C - Completeness Assertions (15 assertions, 25% weight)

**Focus**: Are all necessary elements present (milestones, tasks, participants, deliverables)?

### C1: Milestone Presence
**Assertion**: The plan includes 3-6 major milestones that mark phase completion points.

**Evaluation Prompt**:
```
Given the workback plan with milestones:
{milestone_list}

Question: Does the plan have 3-6 major milestones?

Answer with one of:
- PASS: 3-6 milestones present
- PARTIAL: 2 or 7-8 milestones (acceptable but not optimal)
- FAIL: <2 or >8 milestones
```

---

### C2: Task Count Adequacy
**Assertion**: The plan has adequate task coverage (20-50 tasks for typical project).

**Evaluation Prompt**:
```
Given the workback plan with {task_count} tasks for a {project_type} project

Question: Is the task count adequate for this project scope?

Answer with one of:
- PASS: Task count appropriate for scope (20-50 for most projects)
- PARTIAL: Slightly over or under but reasonable
- FAIL: Far too few (<10) or too many (>80) tasks
```

---

### C3: Participant Coverage
**Assertion**: The plan identifies 4-8 key stakeholders/participants.

**Evaluation Prompt**:
```
Given the workback plan with {participant_count} participants:
{participant_list}

Question: Are sufficient participants identified for project execution?

Answer with one of:
- PASS: 4-8 participants with diverse roles
- PARTIAL: 2-3 or 9-12 participants (acceptable)
- FAIL: <2 or >12 participants
```

**November 16 Benchmark**: 120b averaged 5.0 participants (4-6 range)

---

### C4: Deliverable Identification
**Assertion**: The plan identifies 3-6 concrete deliverables/artifacts.

**Evaluation Prompt**:
```
Given the workback plan with {deliverable_count} deliverables:
{deliverable_list}

Question: Are key deliverables identified?

Answer with one of:
- PASS: 3-6 deliverables with specific names
- PARTIAL: 1-2 or 7-10 deliverables
- FAIL: 0 deliverables or >10 deliverables
```

**November 16 Benchmark**: 120b averaged 4.0 deliverables (0-6 range with stochastic variance)

---

### C5: Appropriate Workflow Structure
**Assertion**: The plan has appropriate workflow structure for the meeting type.

**Evaluation Prompt**:
```
Given:
- Meeting type: {meeting_type}
- Task list: {task_list}

Question: Does the plan have appropriate structure for this meeting type?

**For complex projects** (product launch, project kickoff, strategic initiative):
- Expect phases: Planning → Execution → Validation → Launch
- PASS: All 4 phases present | PARTIAL: 3 phases | FAIL: <3 phases

**For recurring meetings** (QBR, newsletter, report preparation):
- Expect logical sequence: Preparation → Execution → Follow-up
- PASS: Clear sequence present | PARTIAL: Partial sequence | FAIL: No clear flow

**For simple meetings** (weekly update, 1:1, team sync, brainstorm):
- Expect simple task sequence (NO phases needed)
- PASS: Tasks present and logically ordered | FAIL: No structure

Answer: PASS / PARTIAL / FAIL
```

---

### C6: Appropriate Approval/Review Steps
**Assertion**: The plan includes appropriate review/approval tasks based on meeting type.

**Evaluation Prompt**:
```
Given:
- Meeting type: {meeting_type}
- Task list: {task_list}

Question: Does the plan include appropriate approval/review steps?

**Requires multiple approvals** (product launch, strategic decision, major project):
- PASS: 3+ approval/review tasks | PARTIAL: 1-2 approvals | FAIL: None

**Requires some review** (QBR, newsletter, presentation, report):
- PASS: 1-2 review tasks | PARTIAL: Implicit review | FAIL: Expected but missing

**No approvals needed** (weekly update, 1:1, brainstorm, status sync):
- PASS: Appropriately no formal approvals | N/A

Answer: PASS / PARTIAL / FAIL
```

---

### C7: Dependencies Defined
**Assertion**: At least 30% of tasks have explicit dependencies defined.

**Evaluation Prompt**:
```
Given:
- Total tasks: {task_count}
- Tasks with dependencies: {tasks_with_dependencies}
- Dependency ratio: {dependency_ratio}%

Question: Are dependencies adequately defined?

Answer with one of:
- PASS: ≥30% of tasks have dependencies
- PARTIAL: 15-29% of tasks have dependencies
- FAIL: <15% of tasks have dependencies
```

---

### C8: Task Ownership Assignment
**Assertion**: At least 80% of tasks have assigned owners/participants.

**Evaluation Prompt**:
```
Given:
- Total tasks: {task_count}
- Tasks with assigned owners: {tasks_with_owners}
- Assignment ratio: {assignment_ratio}%

Question: Are tasks adequately assigned to owners?

Answer with one of:
- PASS: ≥80% of tasks assigned
- PARTIAL: 60-79% of tasks assigned
- FAIL: <60% of tasks assigned
```

---

### C9: Milestone Definitions
**Assertion**: Each milestone has at least 3 tasks and a clear completion criterion.

**Evaluation Prompt**:
```
Given the milestones and their tasks:
{milestone_task_mapping}

Question: Are milestones properly defined?

Answer with one of:
- PASS: All milestones have 3+ tasks
- PARTIAL: Most milestones have 3+ tasks, some have fewer
- FAIL: Many milestones have <3 tasks
```

---

### C10: Critical Path Elements
**Assertion**: The dependency structure allows identification of a critical path.

**Evaluation Prompt**:
```
Given the task dependency graph:
{dependency_graph}

Question: Does the dependency structure form a chain that represents a critical path?

Answer with one of:
- PASS: Clear dependency chain from start to end exists
- PARTIAL: Partial dependency chain, some gaps
- FAIL: No discernible critical path (all tasks independent)
```

---

### C11-C15: Context-Aware Completeness Checks

**C11: Completion Task (Context-Aware)**
- Assertion: Plan includes appropriate completion task for meeting type
- **Product/feature launch** → "Launch" or "Go-live" task REQUIRED
- **Project delivery** → "Complete" or "Deliver" task REQUIRED
- **QBR/presentation** → "Present" or "Deliver presentation" REQUIRED
- **Newsletter** → "Send newsletter" or "Publish" REQUIRED
- **Weekly update** → "Conduct meeting" or "Share update" REQUIRED
- **Brainstorm/planning** → No completion task needed (PASS by default)
- PASS: Appropriate completion task present or not needed | FAIL: Expected but missing

**C12: Pre-Delivery Validation (Context-Aware)**
- Assertion: Plan includes appropriate validation before key deliverables
- **Product launch** → Testing/QA REQUIRED (FAIL if missing)
- **Newsletter/content** → Review/editing REQUIRED (FAIL if missing)
- **Presentation** → Draft review REQUIRED (FAIL if missing)
- **Weekly update** → Optional, not required (PASS by default)
- **Brainstorm** → Not applicable (PASS by default)
- PASS: Appropriate validation present or not needed | FAIL: Expected but missing

**C13: Communication/Coordination (Context-Aware)**
- Assertion: Plan includes communication tasks appropriate for team size
- **5+ participants** → Communication tasks REQUIRED (FAIL if missing)
- **2-4 participants** → Some coordination expected (PARTIAL if minimal)
- **1 participant** (solo work) → Not required (PASS by default)
- PASS: Appropriate communication for team size | PARTIAL: Minimal | FAIL: Expected but missing

**C14: Contingency/Buffer Consideration**
- Assertion: Plan shows awareness of risk/buffer (buffer days OR risk mentions)
- PASS: Risk awareness present | PARTIAL: Implicit | FAIL: No risk consideration
- Note: Even simple meetings benefit from time buffers

**C15: Post-Completion Follow-up (Context-Aware)**
- Assertion: Plan includes post-completion follow-up when appropriate
- **Major launch/release** → Monitoring/metrics REQUIRED (FAIL if missing)
- **Ongoing initiative** → Follow-up meeting expected (PARTIAL if missing)
- **One-time deliverable** → Optional (PASS even if missing)
- **Weekly/routine meeting** → Not applicable (PASS by default)
- PASS: Appropriate follow-up or not needed | PARTIAL: Useful but missing | FAIL: Required but missing

---

## R - Relevance Assertions (10 assertions, 20% weight)

**Focus**: Do tasks align with the goal and are they appropriate for the context?

### R1: Goal Alignment
**Assertion**: All tasks contribute to achieving the stated goal.

**Evaluation Prompt**:
```
Given:
- Goal: {plan_goal}
- Task list: {task_list}

Question: Do all tasks contribute to achieving the goal?

Answer with one of:
- PASS: All tasks clearly support the goal
- PARTIAL: Most tasks support goal, some tangential
- FAIL: Many tasks unrelated to goal
```

---

### R2: Meeting Type Appropriateness
**Assertion**: Tasks match typical patterns for this meeting/project type.

**Evaluation Prompt**:
```
Given:
- Meeting type: {meeting_type}
- Task breakdown: {task_summary}

Question: Do tasks match expected patterns for this meeting type?

For example:
- Newsletter Launch: Draft → Review → Approve → Produce → Launch
- QBR: Data Collection → Analysis → Presentation Prep → Review
- Project Launch: Requirements → Design → Develop → Test → Launch

Answer with one of:
- PASS: Tasks follow typical patterns for this type
- PARTIAL: Most tasks appropriate, some deviations
- FAIL: Tasks don't match expected patterns
```

---

### R3: No Out-of-Scope Tasks
**Assertion**: No tasks are clearly outside the project scope.

**Evaluation Prompt**:
```
Given:
- Goal: {plan_goal}
- Task list: {task_list}

Question: Are all tasks within the stated project scope?

Answer with one of:
- PASS: All tasks within scope
- PARTIAL: 1-2 questionable tasks
- FAIL: Multiple out-of-scope tasks
```

---

### R4: Appropriate Granularity
**Assertion**: Task granularity matches project timeline (not too detailed for long projects, not too high-level for short projects).

**Evaluation Prompt**:
```
Given:
- Project timeline: {project_duration}
- Task list: {task_list}

Question: Is task granularity appropriate for timeline?

Guidelines:
- 1-week project: Daily or sub-daily tasks appropriate
- 1-month project: 1-3 day tasks appropriate
- 6-month project: Weekly tasks appropriate

Answer with one of:
- PASS: Granularity matches timeline
- PARTIAL: Mostly appropriate, some inconsistencies
- FAIL: Granularity mismatch (e.g., hourly tasks for 6-month project)
```

---

### R5: Stakeholder Appropriateness
**Assertion**: Identified participants are appropriate for the project type.

**Evaluation Prompt**:
```
Given:
- Project type: {project_type}
- Participants: {participant_list}

Question: Are participants appropriate for this project type?

Expected stakeholders by type:
- Product Launch: PM, Engineering, Design, QA, Marketing
- Newsletter: Content, Reviewers, Approvers, Marketing Ops
- QBR: Data owners, Analysts, Presenters, Executives

Answer with one of:
- PASS: All participants appropriate for project type
- PARTIAL: Most appropriate, some unexpected
- FAIL: Key stakeholders missing or inappropriate participants
```

---

### R6-R10: Additional Relevance Checks

**R6: Timeline Realism**
- Assertion: Total duration matches typical timeline for this project type
- PASS: Timeline realistic | PARTIAL: Tight but feasible | FAIL: Unrealistic timeline

**R7: Resource Appropriateness**
- Assertion: Identified resources (team size, skills) match project needs
- PASS: Resources appropriate | PARTIAL: Close | FAIL: Resource mismatch

**R8: No Redundant Tasks**
- Assertion: No duplicate or redundant tasks
- PASS: All tasks unique | PARTIAL: Minor overlap | FAIL: Significant redundancy

**R9: Priority Focus**
- Assertion: Tasks focus on high-priority/critical-path items
- PASS: Critical tasks prioritized | PARTIAL: Some prioritization | FAIL: No prioritization

**R10: Context-Aware Dependencies**
- Assertion: Dependencies reflect domain knowledge (e.g., "can't launch without approval")
- PASS: Dependencies show domain expertise | PARTIAL: Basic dependencies | FAIL: Naive dependencies

---

## U - Usefulness Assertions (10 assertions, 20% weight)

**Focus**: Is the plan actionable and can stakeholders execute it?

### U1: Task Clarity
**Assertion**: All tasks have clear action verbs and specific objects.

**Evaluation Prompt**:
```
Given the task list:
{task_list}

Question: Are task names clear and actionable?

Check for:
- Action verbs: create, develop, review, approve, test, deploy
- Avoid vague verbs: handle, work on, deal with, manage
- Specific objects: not "work on stuff" but "develop user authentication module"

Answer with one of:
- PASS: All tasks have clear action verbs and specific objects
- PARTIAL: Most tasks clear, some vague
- FAIL: Many vague or unclear tasks
```

---

### U2: Executable Tasks
**Assertion**: Tasks are concrete enough that an owner can start working immediately.

**Evaluation Prompt**:
```
Given a sample of tasks:
{task_sample}

Question: Can an assigned owner start working on these tasks without clarification?

Answer with one of:
- PASS: All tasks are immediately executable
- PARTIAL: Most tasks executable, some need clarification
- FAIL: Many tasks too vague to execute
```

---

### U3: Success Criteria Clarity
**Assertion**: For key tasks, it's clear what "done" means (either explicit or obvious from task name).

**Evaluation Prompt**:
```
Given key tasks (milestones, approvals, launches):
{key_task_list}

Question: Is it clear what "done" means for these tasks?

Answer with one of:
- PASS: Success criteria clear for all key tasks
- PARTIAL: Success criteria mostly clear
- FAIL: Success criteria ambiguous for key tasks
```

---

### U4: Task Name Quality
**Assertion**: Task names are 3-10 words (not too short, not too long).

**Evaluation Prompt**:
```
Given task list with average name length of {avg_words} words:
{task_list}

Question: Are task names appropriately detailed?

Answer with one of:
- PASS: Average 3-10 words, good balance of brevity and clarity
- PARTIAL: Average 2-3 or 10-15 words (acceptable)
- FAIL: Average <2 or >15 words
```

---

### U5: Participant Contact Info
**Assertion**: Participants have sufficient identifying information (name, role, email if available).

**Evaluation Prompt**:
```
Given participant list:
{participant_list}

Question: Do participants have sufficient identifying information?

Answer with one of:
- PASS: All participants have name + role (+ email)
- PARTIAL: All have name, some missing role or email
- FAIL: Participants lack basic identifying information
```

---

### U6-U10: Additional Usefulness Checks

**U6: Deliverable Specificity**
- Assertion: Deliverables have specific names (not generic "document")
- PASS: All deliverables specific | PARTIAL: Most specific | FAIL: Many generic

**U7: Dependency Clarity**
- Assertion: Dependencies are explicit (task IDs or clear references)
- PASS: All dependencies explicit | PARTIAL: Most explicit | FAIL: Dependencies ambiguous

**U8: Milestone Achievability**
- Assertion: Milestones are achievable checkpoints (not aspirational goals)
- PASS: All milestones achievable | PARTIAL: Most achievable | FAIL: Unrealistic milestones

**U9: Communication Plan**
- Assertion: Plan shows how team coordination will happen (if multi-person project)
- PASS: Communication explicit | PARTIAL: Implicit | FAIL: No coordination consideration

**U10: Tooling/Infrastructure References**
- Assertion: Plan references relevant tools/systems (SharePoint, GitHub, etc.) where applicable
- PASS: Relevant tools mentioned | PARTIAL: Some tools | FAIL: No tool references (if applicable)

---

## E - Exceptional Assertions (5 assertions, 15% weight)

**Focus**: Does the plan go beyond common expectations with innovation, optimization, or superior quality?

### E1: Innovation & Best Practices
**Assertion**: The plan incorporates innovative approaches or industry best practices beyond basic execution.

**Evaluation Prompt**:
```
Given the workback plan:
{plan_summary}

Question: Does the plan show innovation or best practices beyond common approaches?

Look for:
- Novel task sequencing or parallel execution strategies
- Use of automation or modern tools
- Risk mitigation strategies
- Efficiency optimizations
- Quality gates beyond standard approvals

Answer with one of:
- PASS: Clear evidence of innovation or best practices (2+ examples)
- PARTIAL: Some innovative elements (1 example)
- FAIL: Standard/conventional approach only
```

---

### E2: Proactive Risk Management
**Assertion**: The plan includes proactive risk management beyond basic buffer time.

**Evaluation Prompt**:
```
Given the workback plan:
{plan_summary}

Question: Does the plan show exceptional risk management?

Look for:
- Contingency tasks for high-risk items
- Multiple approval checkpoints
- Early validation/testing phases
- Fallback strategies
- Risk-specific buffer allocation

Answer with one of:
- PASS: Sophisticated risk management (3+ strategies)
- PARTIAL: Some risk awareness (1-2 strategies)
- FAIL: Minimal or no risk management
```

---

### E3: Optimization & Efficiency
**Assertion**: The plan demonstrates optimization for time, cost, or quality beyond standard execution.

**Evaluation Prompt**:
```
Given the workback plan:
{plan_summary}

Question: Does the plan show optimization thinking?

Look for:
- Parallel task execution where possible
- Just-in-time resource allocation
- Efficient dependency chains (minimal blocking)
- Reuse of existing assets/work
- Lean approach (no unnecessary tasks)

Answer with one of:
- PASS: Clear optimization strategies (3+ examples)
- PARTIAL: Some optimization (1-2 examples)
- FAIL: No optimization, sequential/wasteful approach
```

---

### E4: Stakeholder Experience
**Assertion**: The plan shows exceptional consideration for stakeholder experience and collaboration.

**Evaluation Prompt**:
```
Given the workback plan:
{plan_summary}

Question: Does the plan demonstrate superior stakeholder management?

Look for:
- Clear communication touchpoints
- Stakeholder-specific checkpoints
- Visibility/transparency mechanisms
- Collaborative decision points
- Change management considerations

Answer with one of:
- PASS: Exceptional stakeholder experience (3+ elements)
- PARTIAL: Some stakeholder considerations (1-2 elements)
- FAIL: Minimal stakeholder focus
```

---

### E5: Quality Excellence
**Assertion**: The plan demonstrates commitment to exceptional quality beyond minimum standards.

**Evaluation Prompt**:
```
Given the workback plan:
{plan_summary}

Question: Does the plan show exceptional quality focus?

Look for:
- Multiple quality review stages
- Peer review or cross-functional validation
- User testing or feedback loops
- Quality metrics or success criteria
- Post-launch monitoring/refinement

Answer with one of:
- PASS: Strong quality focus (3+ quality elements)
- PARTIAL: Some quality considerations (1-2 elements)
- FAIL: Minimal quality focus
```

---

## LLM-as-Judge Implementation

### Evaluation Pipeline

```python
from typing import List, Dict
from dataclasses import dataclass
import json

@dataclass
class AssertionResult:
    """Result of a single assertion evaluation."""
    assertion_id: str
    assertion_name: str
    category: str  # A, C, R, U, E
    result: str  # PASS, PARTIAL, FAIL
    score: float  # 1.0, 0.5, 0.0
    reasoning: str
    confidence: float  # 0.0-1.0

class WorkbackPlanAssertionEvaluator:
    """LLM-as-Judge evaluator using ACRUE assertions."""
    
    def __init__(self, judge_llm: str = "gpt-4"):
        self.judge_llm = judge_llm
        self.assertions = self._load_assertions()
    
    def _load_assertions(self) -> Dict[str, Dict]:
        """Load all 50 ACRUE assertions."""
        return {
            # Accuracy (10 assertions)
            "A1": {
                "name": "Goal Extraction Accuracy",
                "category": "Accuracy",
                "weight": 0.02,  # 10 assertions × 0.02 = 20%
                "prompt_template": """..."""  # As defined above
            },
            # ... (all 50 assertions)
        }
    
    def evaluate_assertion(
        self,
        assertion_id: str,
        plan: WorkbackPlan,
        input_prompt: str
    ) -> AssertionResult:
        """Evaluate a single assertion using LLM-as-Judge."""
        assertion = self.assertions[assertion_id]
        
        # Build evaluation prompt
        eval_prompt = self._build_eval_prompt(
            assertion, plan, input_prompt
        )
        
        # Call judge LLM
        judge_response = self._query_judge_llm(eval_prompt)
        
        # Parse result
        result = self._parse_judge_response(judge_response)
        
        return AssertionResult(
            assertion_id=assertion_id,
            assertion_name=assertion["name"],
            category=assertion["category"],
            result=result["verdict"],  # PASS/PARTIAL/FAIL
            score=self._verdict_to_score(result["verdict"]),
            reasoning=result["reasoning"],
            confidence=result.get("confidence", 1.0)
        )
    
    def _verdict_to_score(self, verdict: str) -> float:
        """Convert verdict to numerical score."""
        return {
            "PASS": 1.0,
            "PARTIAL": 0.5,
            "FAIL": 0.0
        }[verdict]
    
    def evaluate_all(
        self,
        plan: WorkbackPlan,
        input_prompt: str
    ) -> Dict:
        """Evaluate all 50 assertions."""
        results = []
        
        for assertion_id in self.assertions.keys():
            result = self.evaluate_assertion(
                assertion_id, plan, input_prompt
            )
            results.append(result)
        
        return self._aggregate_results(results)
    
    def _aggregate_results(self, results: List[AssertionResult]) -> Dict:
        """Aggregate assertion results into overall score."""
        # Group by ACRUE category
        by_category = {
            "Accuracy": [],
            "Completeness": [],
            "Relevance": [],
            "Usefulness": [],
            "Exceptional": []
        }
        
        for result in results:
            by_category[result.category].append(result)
        
        # Calculate category scores
        category_scores = {}
        for category, cat_results in by_category.items():
            total_score = sum(r.score for r in cat_results)
            total_possible = len(cat_results)
            category_scores[category] = (total_score / total_possible) * 100
        
        # Calculate weighted overall score
        weights = {
            "Accuracy": 0.20,
            "Completeness": 0.25,
            "Relevance": 0.20,
            "Usefulness": 0.20,
            "Exceptional": 0.15
        }
        
        overall_score = sum(
            category_scores[cat] * weights[cat]
            for cat in weights.keys()
        )
        
        # Determine tier
        if overall_score >= 90:
            tier = "Excellent"
            status = "Production-ready"
        elif overall_score >= 80:
            tier = "Good"
            status = "Usable with minor edits"
        elif overall_score >= 70:
            tier = "Acceptable"
            status = "Requires review"
        elif overall_score >= 60:
            tier = "Poor"
            status = "Needs rework"
        else:
            tier = "Fail"
            status = "Not usable"
        
        # Generate report
        return {
            "overall_score": round(overall_score, 1),
            "tier": tier,
            "status": status,
            "category_scores": category_scores,
            "assertion_results": results,
            "passed": sum(1 for r in results if r.result == "PASS"),
            "partial": sum(1 for r in results if r.result == "PARTIAL"),
            "failed": sum(1 for r in results if r.result == "FAIL"),
            "total_assertions": len(results)
        }
    
    def generate_report(self, evaluation: Dict) -> str:
        """Generate human-readable evaluation report."""
        report = f"""
# Workback Plan Evaluation Report

**Overall Score**: {evaluation['overall_score']}/100
**Tier**: {evaluation['tier']} ({evaluation['status']})

## Assertion Summary
- ✅ **Passed**: {evaluation['passed']}/50 ({evaluation['passed']/50*100:.1f}%)
- ⚠️ **Partial**: {evaluation['partial']}/50 ({evaluation['partial']/50*100:.1f}%)
- ❌ **Failed**: {evaluation['failed']}/50 ({evaluation['failed']/50*100:.1f}%)

## ACRUE Category Scores
- **Accuracy** (20%): {evaluation['category_scores']['Accuracy']:.1f}/100
- **Completeness** (25%): {evaluation['category_scores']['Completeness']:.1f}/100
- **Relevance** (20%): {evaluation['category_scores']['Relevance']:.1f}/100
- **Usefulness** (20%): {evaluation['category_scores']['Usefulness']:.1f}/100
- **Exceptional** (15%): {evaluation['category_scores']['Exceptional']:.1f}/100

## Failed Assertions (Action Items)
"""
        failed = [r for r in evaluation['assertion_results'] if r.result == "FAIL"]
        for result in failed:
            report += f"- **{result.assertion_id}**: {result.assertion_name}\n"
            report += f"  - Reasoning: {result.reasoning}\n"
        
        return report
```

### Example Usage

```python
# Initialize evaluator
evaluator = WorkbackPlanAssertionEvaluator(judge_llm="gpt-4")

# Evaluate a workback plan
input_prompt = "Create a workback plan for product launch on Dec 1, 2026"
plan_120b = generate_workback_plan(input_prompt, model="gpt-oss:120b")

# Run evaluation
evaluation = evaluator.evaluate_all(plan_120b, input_prompt)

# Generate report
report = evaluator.generate_report(evaluation)
print(report)

# Compare models
models = ["gpt-oss:20b", "gpt-oss:120b", "gpt-4o", "claude-opus-3"]
comparison = compare_models_acrue(input_prompt, models, evaluator)
```

### Expected Output

```
# Workback Plan Evaluation Report

**Overall Score**: 84.5/100
**Tier**: Good (Usable with minor edits)

## Assertion Summary
- ✅ **Passed**: 39/50 (78.0%)
- ⚠️ **Partial**: 8/50 (16.0%)
- ❌ **Failed**: 3/50 (6.0%)

## ACRUE Category Scores
- **Accuracy** (20%): 90.0/100 (9/10 assertions passed)
- **Completeness** (25%): 80.0/100 (12/15 assertions passed)
- **Relevance** (20%): 85.0/100 (8.5/10 assertions passed)
- **Usefulness** (20%): 82.5/100 (8.25/10 assertions passed)
- **Exceptional** (15%): 90.0/100 (4.5/5 assertions passed)

## Failed Assertions (Action Items)
- **C14**: Contingency/Buffer Consideration
  - Reasoning: No explicit buffer days or risk mentions in task estimates
- **U9**: Communication Plan
  - Reasoning: No explicit communication/coordination tasks for multi-person project
- **R8**: No Redundant Tasks
  - Reasoning: Tasks T12 and T15 appear to overlap (both involve "final review")
```

---

## Next Steps

### Immediate Priorities (Week 1-2)

**Priority 1: Implement Assertion Evaluator**
- [ ] Build `WorkbackPlanAssertionEvaluator` class
- [ ] Implement all 50 assertion prompts
- [ ] Integrate with LLM API (GPT-4 as judge)
- [ ] Create automated evaluation pipeline

**Priority 2: Validate with Existing Data**
- [ ] Run evaluator on 4 November 16 scenarios:
  - Newsletter Launch (26 tasks, 4 participants, 5 deliverables)
  - QBR Preparation (35 tasks, 5 participants, 6 deliverables)
  - Project Launch (40 tasks, 6 participants, 5 deliverables)
  - Strategic Initiatives (50 tasks, 5 participants, 0-6 deliverables)
- [ ] Baseline 120b performance across ACRUE dimensions
- [ ] Identify weakest assertions (lowest pass rates)

**Priority 3: Model Comparison**
- [ ] Run GPT-5, gpt-oss:120b, gpt-4o, Claude Opus on same scenarios
- [ ] Compare ACRUE scores across models
- [ ] Generate model comparison report
- [ ] Determine best model for production

**Deliverable**: Model comparison report with ACRUE scores

### Decision Framework

**Based on evaluation results:**

1. **If 120b scores ≥85%**:
   - Deploy Phase 1 as-is ✅
   - Focus on Phase 2A (WBP-08 backward scheduling)
   - Use assertion evaluation for ongoing quality monitoring

2. **If 120b scores 75-84%**:
   - Improve prompts based on failed assertions
   - Add few-shot examples for weak categories
   - Iterate and re-evaluate
   - Consider hybrid approach (120b + GPT-4 for critical sections)

3. **If 120b scores <75%**:
   - Switch to GPT-4o or Claude for production
   - Use 120b for prototyping only
   - Investigate prompt engineering improvements

4. **For any model**:
   - Prioritize canonical tasks (WBP-05 through WBP-15) based on failed assertions
   - Build features that improve lowest-scoring ACRUE categories

### Benefits of Assertion-Based Approach

**vs. Gold Standard Comparison**:
- ✅ No need for "perfect" reference plans
- ✅ Objective yes/no evaluation
- ✅ Clear action items (failed assertions)
- ✅ Human-verifiable (can spot-check LLM judgments)
- ✅ Extensible (add new assertions as needed)

**ACRUE Framing Benefits**:
- ✅ Comprehensive coverage (accuracy, completeness, relevance, usefulness, effectiveness)
- ✅ Stakeholder-friendly categories
- ✅ Maps to business value (effectiveness = deadline achievement)
- ✅ Balanced weighting (completeness 25%, others 15-20%)

**LLM-as-Judge Benefits**:
- ✅ Scalable (evaluate hundreds of plans automatically)
- ✅ Consistent (same LLM applies same standards)
- ✅ Explainable (reasoning for each verdict)
- ✅ Cost-effective (cheaper than human evaluation at scale)

---

## Summary

**Evaluation Approach**: Assertion-based with LLM-as-Judge using ACRUE framework

**50 Assertions**:
- **A (Accuracy)**: 10 assertions, 20% weight - Facts, dates, dependencies correct
- **C (Completeness)**: 15 assertions, 25% weight - All elements present
- **R (Relevance)**: 10 assertions, 20% weight - Tasks align with goal
- **U (Usefulness)**: 10 assertions, 20% weight - Plan is actionable
- **E (Exceptional)**: 5 assertions, 15% weight - Exceeds common expectations

**Scoring**: Pass (1.0) / Partial (0.5) / Fail (0.0) → Overall score 0-100

**Quality Tiers**:
- Excellent (≥90%): Production-ready
- Good (80-89%): Usable
- Acceptable (70-79%): Needs review
- Poor/Fail (<70%): Rework needed

**Next Document**: Implementation of `WorkbackPlanAssertionEvaluator` class with all 50 assertion prompts

---

**Document Version**: 1.0 (Assertion-Based)  
**Created**: November 17, 2025  
**Next Review**: After evaluator implementation and first model comparison

**What We Measure**: Is the plan organized into logical phases/milestones/tasks with clear hierarchy?

### Scoring Rubric

| Score | Criteria |
|-------|----------|
| **15** | Perfect hierarchy: 3-6 milestones, logical phases, clear parent-child relationships |
| **12** | Good structure, minor issues (e.g., unbalanced milestone sizes) |
| **9** | Acceptable hierarchy, some tasks misplaced or milestones unclear |
| **6** | Weak structure, flat task list with minimal grouping |
| **3** | Poor organization, confusing hierarchy |
| **0** | No structure, tasks randomly listed |

### Evaluation Checklist

**Milestone Quality**:
- [ ] 3-6 major milestones identified (not too few, not too many)
- [ ] Milestones represent completion of significant phases
- [ ] Milestones have clear acceptance criteria
- [ ] Milestone sequence is logical (design → build → test → launch)

**Task Organization**:
- [ ] Tasks grouped under appropriate milestones
- [ ] Task granularity consistent (not mixing high-level and micro tasks)
- [ ] Each milestone has 3-10 tasks (not too few, not too many)
- [ ] Task naming follows clear conventions (verb + object)

**Hierarchy Depth**:
- [ ] 2-3 levels maximum (project → milestone → task)
- [ ] No orphaned tasks (every task belongs to a milestone)
- [ ] No circular references in hierarchy

### Example: Project Launch (Good vs Poor)

**Good Structure (15/15)**:
```
Project: Product Launch (Dec 1, 2026)
├── Phase 1: Requirements & Design (6 weeks)
│   ├── M1: Requirements Complete
│   │   ├── T1: Stakeholder interviews (3 days)
│   │   ├── T2: Draft PRD (5 days)
│   │   └── T3: PRD approval (2 days)
│   └── M2: Design Approved
│       ├── T4: Create wireframes (3 days)
│       ├── T5: Design mockups (5 days)
│       └── T6: Design review (2 days)
├── Phase 2: Development (8 weeks)
│   └── M3: Development Complete
│       ├── T7: Frontend development (15 days)
│       ├── T8: Backend API (20 days)
│       └── T9: Integration (5 days)
└── Phase 3: Testing & Launch (4 weeks)
    ├── M4: QA Sign-off
    │   ├── T10: Unit tests (5 days)
    │   └── T11: Integration tests (5 days)
    └── M5: Launch Ready
        └── T12: Go-live (1 day)
```

**Poor Structure (6/15)**:
```
Project: Product Launch
├── T1: Talk to people
├── T2: Write document
├── T3: Build stuff
├── T4: Test things
├── T5: Launch
└── T6: Marketing
```
Problems: No milestones, vague tasks, no hierarchy, inconsistent granularity

### Automated Evaluation

```python
def evaluate_hierarchical_structure(plan: WorkbackPlan) -> float:
    """Evaluate D2: Hierarchical Structure (0-15 points)."""
    score = 0.0
    
    # Check 1: Milestone count (5 points)
    milestone_count = len(plan.milestones) if hasattr(plan, 'milestones') else 0
    if 3 <= milestone_count <= 6:
        score += 5.0
    elif 2 <= milestone_count <= 8:
        score += 3.0
    
    # Check 2: Task distribution across milestones (5 points)
    if milestone_count > 0:
        tasks_per_milestone = [
            len([t for t in plan.tasks if t.milestone_id == m.id])
            for m in plan.milestones
        ]
        avg_tasks = sum(tasks_per_milestone) / len(tasks_per_milestone)
        if 3 <= avg_tasks <= 10:
            score += 5.0
        elif 2 <= avg_tasks <= 15:
            score += 3.0
    
    # Check 3: Task naming quality (5 points)
    action_verbs = ['create', 'develop', 'design', 'test', 'review', 'approve', 
                    'build', 'implement', 'deploy', 'write', 'conduct']
    tasks_with_verbs = sum(
        1 for task in plan.tasks
        if any(verb in task.name.lower() for verb in action_verbs)
    )
    verb_ratio = tasks_with_verbs / max(len(plan.tasks), 1)
    score += 5.0 * verb_ratio
    
    return min(score, 15.0)
```

---

## D3: Dependency Correctness (20 points)

**What We Measure**: Are task dependencies accurate, complete, and cycle-free?

### Scoring Rubric

| Score | Criteria |
|-------|----------|
| **20** | Perfect dependencies: all blocking relationships identified, DAG valid, critical path clear |
| **16** | Good dependencies, minor misses (e.g., optional dependency not marked) |
| **12** | Acceptable dependencies, some missing or incorrect |
| **8** | Weak dependency mapping, significant gaps |
| **4** | Poor dependencies, many errors or circular dependencies |
| **0** | No dependencies or completely incorrect |

### Evaluation Checklist

**Dependency Completeness**:
- [ ] All blocking dependencies identified (task B requires task A)
- [ ] No missing dependencies (orphan tasks that should depend on others)
- [ ] Parallel tasks correctly identified (can run simultaneously)
- [ ] Cross-milestone dependencies captured

**Dependency Correctness**:
- [ ] No circular dependencies (DAG validation passes)
- [ ] Logical ordering (design before development, development before testing)
- [ ] No over-specification (unnecessary dependencies)
- [ ] Dependency types clear (hard blocker vs soft preference)

**Critical Path Implications**:
- [ ] Critical path is identifiable from dependencies
- [ ] Bottleneck tasks clearly dependent on multiple predecessors
- [ ] Launch-critical dependencies marked appropriately

### Example: Newsletter Launch Dependencies

**Good Dependencies (20/20)**:
```json
{
  "tasks": [
    {"id": "T1", "name": "Draft content", "dependencies": []},
    {"id": "T2", "name": "LT review", "dependencies": ["T1"]},
    {"id": "T3", "name": "Incorporate LT feedback", "dependencies": ["T2"]},
    {"id": "T4", "name": "Exec review", "dependencies": ["T3"]},
    {"id": "T5", "name": "Design graphics", "dependencies": ["T1"]},  // Parallel with T2-T4
    {"id": "T6", "name": "Final production", "dependencies": ["T4", "T5"]},
    {"id": "T7", "name": "Launch", "dependencies": ["T6"]}
  ]
}
```
✅ Valid DAG, T5 can run in parallel with T2-T4, all dependencies logical

**Poor Dependencies (8/20)**:
```json
{
  "tasks": [
    {"id": "T1", "name": "Draft content", "dependencies": ["T7"]},  // ❌ Circular!
    {"id": "T2", "name": "LT review", "dependencies": []},  // ❌ Should depend on T1
    {"id": "T3", "name": "Exec review", "dependencies": []},  // ❌ Should depend on T2
    {"id": "T7", "name": "Launch", "dependencies": ["T1"]}  // ❌ Missing T3, T4, T5
  ]
}
```
❌ Circular dependency (T1 → T7 → T1), missing critical dependencies

### Automated Evaluation

```python
import networkx as nx

def evaluate_dependency_correctness(plan: WorkbackPlan, gold_standard: dict) -> float:
    """Evaluate D3: Dependency Correctness (0-20 points)."""
    score = 0.0
    
    # Check 1: DAG validation (10 points) - CRITICAL
    G = nx.DiGraph()
    for task in plan.tasks:
        G.add_node(task.id)
        for dep in task.dependencies:
            G.add_edge(dep, task.id)
    
    if nx.is_directed_acyclic_graph(G):
        score += 10.0
    else:
        # Circular dependencies detected - critical failure
        return 0.0
    
    # Check 2: Dependency coverage vs gold standard (10 points)
    gold_deps = {(e['from'], e['to']) for e in gold_standard.get('dependencies', [])}
    plan_deps = {(dep, task.id) for task in plan.tasks for dep in task.dependencies}
    
    if len(gold_deps) > 0:
        precision = len(gold_deps & plan_deps) / max(len(plan_deps), 1)
        recall = len(gold_deps & plan_deps) / len(gold_deps)
        f1 = 2 * (precision * recall) / max(precision + recall, 0.01)
        score += 10.0 * f1
    else:
        # No gold standard, check for reasonable dependency density
        task_count = len(plan.tasks)
        dep_count = len(plan_deps)
        # Reasonable: 30-80% of tasks have dependencies
        if 0.3 <= (dep_count / task_count) <= 0.8:
            score += 7.0  # Partial credit without gold standard
    
    return min(score, 20.0)
```

---

## D4: Participant Identification (15 points)

**What We Measure**: Are all necessary stakeholders identified and appropriately assigned?

### Scoring Rubric

| Score | Criteria |
|-------|----------|
| **15** | All stakeholders identified, roles clear, ownership assigned |
| **12** | Most stakeholders identified, minor role ambiguities |
| **9** | Key stakeholders present, some missing or unclear assignments |
| **6** | Incomplete stakeholder list, many missing roles |
| **3** | Minimal participant information |
| **0** | No participants identified |

### Evaluation Checklist

**Stakeholder Coverage**:
- [ ] All functional roles represented (PM, Engineering, Design, QA, Marketing)
- [ ] External stakeholders included (customers, vendors, partners)
- [ ] Decision-makers identified (approvers, reviewers)
- [ ] No duplicate roles (same person listed multiple times)

**Assignment Quality**:
- [ ] Each task has an owner (responsible party)
- [ ] Ownership is realistic (person has relevant skills)
- [ ] RACI clarity (Responsible, Accountable, Consulted, Informed)
- [ ] Approval chains clear (who reviews what)

**November 16 Benchmark** (from 120b validation):
- Average: 5.0 participants per plan
- Range: 4-6 participants
- Critical capability: 120b extracts participants, 20b fails (0)

### Example: QBR Preparation

**Good Participant List (15/15)**:
```json
{
  "participants": [
    {
      "id": "P1",
      "name": "Finance Lead",
      "role": "Data Owner",
      "responsibility": "Accountable",
      "tasks": ["T1: Gather financial metrics", "T2: Analyze YoY trends"]
    },
    {
      "id": "P2",
      "name": "Product Manager",
      "role": "Content Creator",
      "responsibility": "Responsible",
      "tasks": ["T5: Draft presentation", "T8: Create executive summary"]
    },
    {
      "id": "P3",
      "name": "VP",
      "role": "Reviewer",
      "responsibility": "Approver",
      "tasks": ["T10: Review draft", "T12: Final approval"]
    },
    {
      "id": "P4",
      "name": "Exec Sponsor",
      "role": "Stakeholder",
      "responsibility": "Informed",
      "tasks": ["T15: QBR presentation"]
    },
    {
      "id": "P5",
      "name": "Design Team",
      "role": "Support",
      "responsibility": "Consulted",
      "tasks": ["T6: Format slides", "T7: Create visuals"]
    }
  ]
}
```
✅ 5 participants, clear roles, RACI defined, all functions covered

**Poor Participant List (4/15)**:
```json
{
  "participants": [
    {"id": "P1", "name": "Person", "role": null, "tasks": []},
    {"id": "P2", "name": "Someone", "role": null, "tasks": []}
  ]
}
```
❌ Vague names, no roles, no task assignments

### Automated Evaluation

```python
def evaluate_participant_identification(plan: WorkbackPlan, gold_standard: dict) -> float:
    """Evaluate D4: Participant Identification (0-15 points)."""
    score = 0.0
    
    # Check 1: Participant count (5 points)
    participant_count = len(plan.participants)
    gold_count = len(gold_standard.get('participants', []))
    
    if gold_count > 0:
        # Compare against gold standard
        count_ratio = participant_count / gold_count
        if 0.8 <= count_ratio <= 1.2:
            score += 5.0
        elif 0.5 <= count_ratio <= 1.5:
            score += 3.0
    else:
        # No gold standard, check against benchmark (4-6 participants)
        if 4 <= participant_count <= 6:
            score += 5.0
        elif 2 <= participant_count <= 8:
            score += 3.0
    
    # Check 2: Role diversity (5 points)
    role_keywords = ['manager', 'engineer', 'designer', 'qa', 'marketing', 
                     'lead', 'director', 'vp', 'exec']
    participants_with_roles = sum(
        1 for p in plan.participants
        if p.role and any(keyword in p.role.lower() for keyword in role_keywords)
    )
    role_ratio = participants_with_roles / max(participant_count, 1)
    score += 5.0 * role_ratio
    
    # Check 3: Task assignment coverage (5 points)
    tasks_assigned = sum(len(p.tasks_assigned) for p in plan.participants)
    total_tasks = len(plan.tasks)
    assignment_ratio = tasks_assigned / max(total_tasks, 1)
    if assignment_ratio >= 0.9:
        score += 5.0
    elif assignment_ratio >= 0.7:
        score += 3.0
    
    return min(score, 15.0)
```

---

## D5: Deliverable Coverage (15 points)

**What We Measure**: Are concrete outputs and artifacts identified for key tasks?

### Scoring Rubric

| Score | Criteria |
|-------|----------|
| **15** | All major deliverables identified, artifact types clear, quality criteria defined |
| **12** | Most deliverables identified, minor gaps |
| **9** | Key deliverables present, some missing or vague |
| **6** | Incomplete deliverable list, many gaps |
| **3** | Minimal deliverable information |
| **0** | No deliverables identified |

### Evaluation Checklist

**Deliverable Completeness**:
- [ ] Milestone deliverables defined (what marks milestone complete)
- [ ] Task outputs identified (what artifact does this task produce)
- [ ] Document types specified (PRD, design doc, code, report)
- [ ] Approval artifacts listed (signed-off documents)

**Deliverable Quality**:
- [ ] Artifact names are specific (not generic "document")
- [ ] Acceptance criteria defined (what makes deliverable "done")
- [ ] Artifact references included (links to SharePoint, OneDrive)
- [ ] Deliverable dependencies mapped (deliverable A enables task B)

**November 16 Benchmark** (from 120b validation):
- Average: 4.0 deliverables per plan
- Range: 0-6 deliverables
- Stochastic variance: Strategic Initiatives (0 first run, 6 second run)

### Example: Project Launch Deliverables

**Good Deliverable List (15/15)**:
```json
{
  "deliverables": [
    {
      "id": "D1",
      "name": "Product Requirements Document (PRD)",
      "type": "Document",
      "producing_task": "T3",
      "acceptance_criteria": ["All features defined", "Stakeholder sign-off"],
      "artifact_reference": {
        "type": "sharepoint",
        "url": "https://company.sharepoint.com/PRD_2026.docx"
      }
    },
    {
      "id": "D2",
      "name": "Approved Design Mockups",
      "type": "Design Artifact",
      "producing_task": "T6",
      "acceptance_criteria": ["All screens designed", "PM approved", "Engineering feasibility confirmed"],
      "artifact_reference": {
        "type": "figma",
        "url": "https://figma.com/project/designs"
      }
    },
    {
      "id": "D3",
      "name": "Tested Codebase",
      "type": "Code",
      "producing_task": "T11",
      "acceptance_criteria": ["All tests passing", "Code review complete", "QA sign-off"],
      "artifact_reference": {
        "type": "github",
        "url": "https://github.com/company/project"
      }
    },
    {
      "id": "D4",
      "name": "Launch Announcement Materials",
      "type": "Marketing Collateral",
      "producing_task": "T13",
      "acceptance_criteria": ["Email template", "Blog post", "Social media posts"],
      "artifact_reference": null
    }
  ]
}
```
✅ 4 deliverables, clear types, acceptance criteria, artifact references

**Poor Deliverable List (4/15)**:
```json
{
  "deliverables": [
    {"id": "D1", "name": "Document", "type": null, "acceptance_criteria": []}
  ]
}
```
❌ Generic name, no type, no acceptance criteria

### Automated Evaluation

```python
def evaluate_deliverable_coverage(plan: WorkbackPlan, gold_standard: dict) -> float:
    """Evaluate D5: Deliverable Coverage (0-15 points)."""
    score = 0.0
    
    # Check 1: Deliverable count (5 points)
    deliverable_count = len(plan.deliverables)
    gold_count = len(gold_standard.get('deliverables', []))
    
    if gold_count > 0:
        count_ratio = deliverable_count / gold_count
        if 0.8 <= count_ratio <= 1.2:
            score += 5.0
        elif 0.5 <= count_ratio <= 1.5:
            score += 3.0
    else:
        # Benchmark: 3-6 deliverables typical
        if 3 <= deliverable_count <= 6:
            score += 5.0
        elif 1 <= deliverable_count <= 8:
            score += 3.0
    
    # Check 2: Deliverable specificity (5 points)
    generic_names = ['document', 'file', 'artifact', 'output', 'thing']
    specific_deliverables = sum(
        1 for d in plan.deliverables
        if not any(generic in d.name.lower() for generic in generic_names)
    )
    specificity_ratio = specific_deliverables / max(deliverable_count, 1)
    score += 5.0 * specificity_ratio
    
    # Check 3: Acceptance criteria defined (5 points)
    deliverables_with_criteria = sum(
        1 for d in plan.deliverables
        if hasattr(d, 'acceptance_criteria') and len(d.acceptance_criteria) > 0
    )
    criteria_ratio = deliverables_with_criteria / max(deliverable_count, 1)
    score += 5.0 * criteria_ratio
    
    return min(score, 15.0)
```

---

## D6: Completeness (15 points)

**What We Measure**: Are all necessary steps included without major gaps?

### Scoring Rubric

| Score | Criteria |
|-------|----------|
| **15** | Complete plan, all phases covered, no missing critical steps |
| **12** | Mostly complete, minor gaps (e.g., missing approval step) |
| **9** | Acceptable coverage, some notable gaps |
| **6** | Incomplete, missing important phases or steps |
| **3** | Major gaps, significant work not accounted for |
| **0** | Severely incomplete, unusable |

### Evaluation Checklist

**Phase Coverage**:
- [ ] Planning phase included (requirements, design)
- [ ] Execution phase included (development, implementation)
- [ ] Quality assurance phase included (testing, review)
- [ ] Launch phase included (deployment, go-live)
- [ ] Post-launch phase included (monitoring, follow-up) if applicable

**Critical Steps**:
- [ ] Stakeholder approvals included
- [ ] Review cycles accounted for
- [ ] Testing and validation steps present
- [ ] Contingency tasks for risks
- [ ] Communication and coordination tasks

**Domain-Specific Requirements**:
- [ ] Meeting type patterns followed (QBR: data → analysis → presentation)
- [ ] Industry best practices included (CPM, approval gates)
- [ ] Regulatory requirements addressed (if applicable)

### Example: Newsletter Launch Completeness

**Complete Plan (15/15)**:
```
Phase 1: Content Creation
  ✓ T1: Draft content
  ✓ T2: Internal review
  ✓ T3: Revisions

Phase 2: Leadership Review
  ✓ T4: LT review
  ✓ T5: Incorporate LT feedback
  ✓ T6: Second LT review (if needed)

Phase 3: Executive Approval
  ✓ T7: Exec review
  ✓ T8: Address exec comments
  ✓ T9: Final exec approval

Phase 4: Production
  ✓ T10: Design graphics
  ✓ T11: Format newsletter
  ✓ T12: Marketing Ops production

Phase 5: Launch
  ✓ T13: Schedule distribution
  ✓ T14: Launch
  ✓ T15: Monitor engagement (post-launch)
```
✅ All phases present, approval cycles included, post-launch monitoring

**Incomplete Plan (7/15)**:
```
Phase 1: Content
  T1: Write newsletter
  
Phase 2: Launch
  T2: Send newsletter
```
❌ Missing: reviews, approvals, design, production, monitoring

### Automated Evaluation

```python
def evaluate_completeness(plan: WorkbackPlan, gold_standard: dict) -> float:
    """Evaluate D6: Completeness (0-15 points)."""
    score = 0.0
    
    # Check 1: Task count adequacy (5 points)
    task_count = len(plan.tasks)
    gold_count = len(gold_standard.get('tasks', []))
    
    if gold_count > 0:
        count_ratio = task_count / gold_count
        if 0.8 <= count_ratio <= 1.2:
            score += 5.0
        elif 0.6 <= count_ratio <= 1.4:
            score += 3.0
    else:
        # Benchmark: 20-50 tasks typical for workback plans
        if 20 <= task_count <= 50:
            score += 5.0
        elif 10 <= task_count <= 60:
            score += 3.0
    
    # Check 2: Phase diversity (5 points)
    phase_keywords = {
        'planning': ['requirement', 'design', 'plan', 'scope'],
        'execution': ['develop', 'build', 'implement', 'create'],
        'validation': ['test', 'review', 'qa', 'validate'],
        'approval': ['approve', 'sign-off', 'review', 'accept'],
        'launch': ['launch', 'deploy', 'release', 'go-live']
    }
    
    phases_covered = 0
    for phase, keywords in phase_keywords.items():
        if any(
            any(keyword in task.name.lower() for keyword in keywords)
            for task in plan.tasks
        ):
            phases_covered += 1
    
    score += (phases_covered / len(phase_keywords)) * 5.0
    
    # Check 3: Critical step presence (5 points)
    critical_keywords = ['review', 'approve', 'test', 'launch']
    tasks_with_critical = sum(
        1 for task in plan.tasks
        if any(keyword in task.name.lower() for keyword in critical_keywords)
    )
    critical_ratio = tasks_with_critical / max(task_count, 1)
    score += 5.0 * critical_ratio
    
    return min(score, 15.0)
```

---

## D7: Actionability (10 points)

**What We Measure**: Are tasks concrete, clear, and executable?

### Scoring Rubric

| Score | Criteria |
|-------|----------|
| **10** | All tasks are concrete, clear verbs, specific outcomes |
| **8** | Most tasks actionable, minor ambiguity |
| **6** | Acceptable clarity, some vague tasks |
| **4** | Many vague tasks, unclear actions |
| **0** | Tasks are abstract, not actionable |

### Evaluation Checklist

**Task Clarity**:
- [ ] Clear action verbs (create, review, approve, test, deploy)
- [ ] Specific objects (not "work on project", but "develop frontend module")
- [ ] No ambiguous terms ("handle", "deal with", "work on")
- [ ] Time-bound where appropriate

**Executability**:
- [ ] Owner can understand what to do
- [ ] Task has clear start and end points
- [ ] Success criteria obvious or derivable
- [ ] No overly broad tasks ("finish project")

### Example: Good vs Poor Task Names

**Good Tasks (10/10)**:
- ✅ "Conduct stakeholder interviews for PRD" (clear verb, specific object)
- ✅ "Design wireframes for checkout flow" (specific, bounded)
- ✅ "Review and approve marketing copy" (clear action, deliverable)
- ✅ "Deploy website to production environment" (concrete, specific)

**Poor Tasks (3/10)**:
- ❌ "Work on requirements" (vague verb, unclear scope)
- ❌ "Handle design stuff" (no clear action, vague object)
- ❌ "Deal with testing" (unclear what "deal with" means)
- ❌ "Finish project" (overly broad, not a single task)

### Automated Evaluation

```python
def evaluate_actionability(plan: WorkbackPlan) -> float:
    """Evaluate D7: Actionability (0-10 points)."""
    score = 0.0
    
    # Check 1: Action verb usage (5 points)
    action_verbs = [
        'create', 'develop', 'design', 'build', 'implement', 'write',
        'review', 'approve', 'test', 'validate', 'deploy', 'launch',
        'conduct', 'gather', 'analyze', 'prepare', 'draft', 'finalize'
    ]
    
    vague_verbs = ['work', 'handle', 'deal', 'manage', 'do', 'finish']
    
    tasks_with_action_verbs = sum(
        1 for task in plan.tasks
        if any(verb in task.name.lower() for verb in action_verbs)
    )
    tasks_with_vague_verbs = sum(
        1 for task in plan.tasks
        if any(verb in task.name.lower() for verb in vague_verbs)
    )
    
    action_ratio = tasks_with_action_verbs / max(len(plan.tasks), 1)
    vague_penalty = tasks_with_vague_verbs / max(len(plan.tasks), 1)
    
    score += 5.0 * (action_ratio - vague_penalty)
    
    # Check 2: Task name length (5 points) - neither too short nor too long
    avg_task_name_length = sum(len(t.name.split()) for t in plan.tasks) / max(len(plan.tasks), 1)
    
    if 3 <= avg_task_name_length <= 7:
        score += 5.0  # Optimal length (e.g., "Review and approve marketing copy")
    elif 2 <= avg_task_name_length <= 10:
        score += 3.0  # Acceptable
    else:
        score += 1.0  # Too short or too long
    
    return max(0.0, min(score, 10.0))
```

---

## Overall Scoring & Classification

### Score Calculation

```python
def calculate_overall_score(dimension_scores: dict) -> dict:
    """Calculate weighted overall score."""
    weights = {
        'D1_goal_understanding': 0.10,
        'D2_hierarchical_structure': 0.15,
        'D3_dependency_correctness': 0.20,
        'D4_participant_identification': 0.15,
        'D5_deliverable_coverage': 0.15,
        'D6_completeness': 0.15,
        'D7_actionability': 0.10
    }
    
    overall_score = sum(
        dimension_scores[dim] * weight
        for dim, weight in weights.items()
    )
    
    # Determine quality tier
    if overall_score >= 90:
        tier = "Excellent"
        status = "Production-ready"
    elif overall_score >= 80:
        tier = "Good"
        status = "Usable with minor edits"
    elif overall_score >= 70:
        tier = "Acceptable"
        status = "Requires review and refinement"
    elif overall_score >= 60:
        tier = "Poor"
        status = "Significant issues, needs rework"
    else:
        tier = "Fail"
        status = "Not usable, fundamental problems"
    
    return {
        'overall_score': round(overall_score, 1),
        'tier': tier,
        'status': status,
        'dimension_scores': dimension_scores
    }
```

### Example Evaluation Report

```json
{
  "plan_id": "newsletter_launch_120b_trial1",
  "model": "gpt-oss:120b",
  "timestamp": "2025-11-16T15:30:00Z",
  "evaluation": {
    "overall_score": 84.5,
    "tier": "Good",
    "status": "Usable with minor edits",
    "dimension_scores": {
      "D1_goal_understanding": 10.0,
      "D2_hierarchical_structure": 13.0,
      "D3_dependency_correctness": 18.0,
      "D4_participant_identification": 12.0,
      "D5_deliverable_coverage": 10.0,
      "D6_completeness": 13.0,
      "D7_actionability": 8.5
    },
    "strengths": [
      "Perfect goal extraction (D1: 10/10)",
      "Strong dependency mapping (D3: 18/20)",
      "Good hierarchical structure (D2: 13/15)"
    ],
    "weaknesses": [
      "Participant roles could be more specific (D4: 12/15)",
      "Some task names vague (D7: 8.5/10)"
    ],
    "recommendations": [
      "Add clearer role definitions for participants",
      "Refine task names to use stronger action verbs",
      "Consider adding 1-2 more deliverables for key milestones"
    ]
  }
}
```

---

## Gold Standard Creation Methodology

### Phase 2: Creating Reference Plans (3-5 Examples)

Following the hero prompts methodology, we need **gold standard workback plans** for evaluation baseline.

**Recommended Gold Standard Examples**:

1. **Newsletter Launch** (Simple, 4-week timeline)
   - Already validated: 26 tasks, 4 participants, 5 deliverables
   - Linear approval chain: Content → LT → Exec → Ops
   - Good for: Testing basic decomposition

2. **QBR Preparation** (Medium, 6-week timeline)
   - Already validated: 35 tasks, 5 participants, 6 deliverables
   - Parallel workstreams: Data collection + Analysis + Presentation
   - Good for: Testing parallel task handling

3. **Project Launch** (Complex, 6-month timeline)
   - Already validated: 40 tasks, 6 participants, 5 deliverables
   - Multi-phase: Requirements → Design → Development → Testing → Launch
   - Good for: Testing long-duration, multi-milestone plans

4. **Strategic Initiatives Review** (Variable, 2-week timeline)
   - Already validated: 50 tasks, 5 participants, 0-6 deliverables (stochastic)
   - Portfolio management: Multiple initiatives, resource allocation
   - Good for: Testing edge cases and variance

5. **Customer Onboarding** (NEW - to be created)
   - Timeline: 8 weeks
   - Cross-functional: Sales, Product, Engineering, Customer Success
   - Good for: Testing external stakeholder coordination

### Gold Standard Creation Process

```python
def create_gold_standard(scenario: str) -> dict:
    """Create gold standard workback plan for evaluation."""
    
    # Step 1: Generate with best model (gpt-oss:120b)
    plan_120b = generate_workback_plan(scenario, model="gpt-oss:120b")
    
    # Step 2: Human expert review and corrections
    plan_corrected = human_review_and_correct(plan_120b)
    
    # Step 3: Validate against reference document's 10 steps
    validate_against_reference(plan_corrected)
    
    # Step 4: Add evaluation metadata
    gold_standard = {
        'scenario': scenario,
        'plan': plan_corrected,
        'creation_method': 'human-validated-120b',
        'validation_date': datetime.now().isoformat(),
        'expert_reviewer': 'Chin-Yew Lin',
        'quality_score': 95.0,  # Expected gold standard score
        'canonical_tasks_used': [
            'WBP-01', 'WBP-02', 'WBP-03', 'WBP-04', 
            'WBP-06', 'WBP-09', 'WBP-15'
        ]
    }
    
    return gold_standard
```

---

## Evaluation Pipeline

### Automated Evaluation Workflow

```python
class WorkbackPlanEvaluator:
    """Automated evaluation pipeline for workback plans."""
    
    def __init__(self, gold_standards: dict):
        self.gold_standards = gold_standards
    
    def evaluate(self, plan: WorkbackPlan, scenario: str) -> dict:
        """Run full evaluation against gold standard."""
        gold = self.gold_standards.get(scenario)
        
        scores = {
            'D1_goal_understanding': evaluate_goal_understanding(plan, gold),
            'D2_hierarchical_structure': evaluate_hierarchical_structure(plan),
            'D3_dependency_correctness': evaluate_dependency_correctness(plan, gold),
            'D4_participant_identification': evaluate_participant_identification(plan, gold),
            'D5_deliverable_coverage': evaluate_deliverable_coverage(plan, gold),
            'D6_completeness': evaluate_completeness(plan, gold),
            'D7_actionability': evaluate_actionability(plan)
        }
        
        result = calculate_overall_score(scores)
        result['scenario'] = scenario
        result['timestamp'] = datetime.now().isoformat()
        
        return result
    
    def compare_models(self, scenario: str, models: list) -> pd.DataFrame:
        """Compare multiple models on same scenario."""
        results = []
        
        for model in models:
            # Generate plan with model
            plan = generate_workback_plan(scenario, model=model)
            
            # Evaluate
            eval_result = self.evaluate(plan, scenario)
            eval_result['model'] = model
            
            results.append(eval_result)
        
        return pd.DataFrame(results)
```

### Example: Model Comparison

```python
# Initialize evaluator with gold standards
evaluator = WorkbackPlanEvaluator(gold_standards={
    'newsletter_launch': load_gold_standard('newsletter_launch.json'),
    'qbr_preparation': load_gold_standard('qbr_preparation.json'),
    'project_launch': load_gold_standard('project_launch.json')
})

# Compare models
models = ['gpt-oss:20b', 'gpt-oss:120b', 'gpt-4o', 'claude-opus-3']
comparison = evaluator.compare_models('newsletter_launch', models)

print(comparison)
```

**Expected Output**:
```
| model          | overall_score | D1  | D2  | D3  | D4  | D5  | D6  | D7  | tier      |
|----------------|---------------|-----|-----|-----|-----|-----|-----|-----|-----------|
| gpt-oss:20b    | 52.3          | 8   | 7   | 10  | 0   | 0   | 12  | 7   | Fail      |
| gpt-oss:120b   | 84.5          | 10  | 13  | 18  | 12  | 10  | 13  | 8.5 | Good      |
| gpt-4o         | 88.2          | 10  | 14  | 19  | 14  | 12  | 14  | 9   | Good      |
| claude-opus-3  | 91.5          | 10  | 15  | 20  | 15  | 14  | 15  | 9.5 | Excellent |
```

---

## Next Steps: Evaluation First Approach

### Immediate Priorities (Phase 1-2: 1-2 weeks)

**Priority 1: Create 3-5 Gold Standard Plans**
- [ ] Newsletter Launch (already have 120b output, need human validation)
- [ ] QBR Preparation (already have 120b output, need human validation)
- [ ] Project Launch (already have 120b output, need human validation)
- [ ] Strategic Initiatives (already have 120b output, need human validation)
- [ ] Customer Onboarding (NEW - create from scratch)

**Priority 2: Implement Evaluation Framework**
- [ ] Build `WorkbackPlanEvaluator` class
- [ ] Implement 7 dimension evaluation functions
- [ ] Create automated scoring pipeline
- [ ] Generate evaluation reports

**Priority 3: Baseline Model Comparison**
- [ ] Run GPT-5 on all 5 gold standard scenarios (3 trials each)
- [ ] Run gpt-oss:120b comparison (validation)
- [ ] Run Claude Opus comparison
- [ ] Generate comparison report

**Deliverable**: Model comparison report showing which LLM produces highest quality workback plans

### Phase 3-4: Build Based on Evaluation Insights (2-4 weeks)

After evaluation baseline established:
- **If 120b scores ≥85**: Deploy Phase 1 as-is, focus on Phase 2A (WBP-08)
- **If 120b scores 70-84**: Improve prompts, add few-shot examples
- **If 120b scores <70**: Consider alternative models (GPT-4o, Claude)

**Then prioritize canonical tasks** based on evaluation gaps:
- Low D3 scores → Prioritize WBP-07 (Critical Path)
- Low D4 scores → Improve participant extraction prompts
- Low D5 scores → Improve deliverable identification prompts
- Low D6 scores → Add completeness checks

**Evaluation-driven development**: Build features that improve lowest-scoring dimensions first.

---

## Summary

**Key Principles**:
1. **Measure first, build second**: Evaluation framework before full implementation
2. **Gold standard baseline**: 3-5 reference plans for comparison
3. **7 quality dimensions**: Weighted scoring (D3 dependencies = 20%, most critical)
4. **Model comparison**: GPT-5 vs 120b vs Claude benchmarking
5. **Evaluation-driven priorities**: Build features that improve scores

**Success Criteria**:
- **Excellent (≥90)**: Production-ready, deploy immediately
- **Good (80-89)**: Usable, iterate on prompts
- **Acceptable (70-79)**: Research needed before production

**November 16 Baseline** (120b, 4 scenarios):
- Estimated overall score: **~82-85** (Good tier)
- Strong: D1 (goal), D2 (structure), D3 (dependencies)
- Weak: D4 (participants - 5 avg, need role clarity), D5 (deliverables - stochastic variance)

**Next Document**: `WORKBACK_PLAN_GOLD_STANDARD_REFERENCE_V1.md` with 3-5 validated reference plans

---

**Document Version**: 1.0  
**Created**: November 17, 2025  
**Next Review**: After gold standard creation and first model comparison
