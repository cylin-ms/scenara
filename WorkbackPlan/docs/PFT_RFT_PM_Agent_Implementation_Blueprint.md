# AI Project Management Agent: Step-by-Step Implementation Blueprint

**Author**: Chin-Yew Lin  
**Created**: November 17, 2025  
**Document Type**: Implementation Guide

---

## Overview

This document provides a practical, phased implementation plan for building an AI PM Agent with PFT (Preference Fine-Tuning) and RFT (Reinforcement Fine-Tuning) capabilities.

---

## Phase 0 – Scoping & Target Use Cases

### Objectives
- Define initial scope and success criteria
- Select pilot workflows

### Tasks

1. **Pick 2–3 core workflows:**
   - Sprint planning
   - Release planning
   - Weekly status reporting

2. **Decide MVP:**
   - Start **read-only**: the agent only reads tools, outputs text suggestions
   - Move later to "drafts & assisted execution"

### Deliverables
- Selected use cases with clear success metrics
- Stakeholder alignment on MVP scope

---

## Phase 1 – Data & Evaluation Setup

### Objectives
- Establish data collection pipeline
- Create evaluation framework

### Tasks

#### 1.1 Collect Data

Gather examples of:
- Good project plans, timelines, risk registers
- Status emails, Slack summaries
- Real Jira/Asana planning examples
- Notion / Confluence specs

#### 1.2 Construct Preference Pairs

Manually label **"better vs worse"** for:
- Plan structure
- Realism of timelines
- Clarity of risk
- Quality of communication

**Target:** 5k–50k preference pairs

#### 1.3 Define Eval Metrics & Test Prompts

Create a **fixed benchmark set:**
- "Plan a Q3 release…"
- "Generate risk register…"
- "Summarize sprint progress…"

### Deliverables
- Curated dataset of PM artifacts
- Preference pair dataset (5k–50k pairs)
- Evaluation benchmark (20–50 test scenarios)

---

## Phase 2 – Base Model & SFT

### Objectives
- Establish baseline LLM capabilities
- Initial domain adaptation

### Tasks

#### 2.1 Choose Base Model
- Select hosted (OpenAI, Anthropic) or self-hosted (Llama, Mistral)
- Consider: coding capabilities, reasoning strength, context length

#### 2.2 Fine-tune (SFT)

**SFT on:**
- Curated PM corpora
- Your own internal docs (if allowed)

**Training recipe:**
```python
sft_config = {
    "base_model": "selected_base_model",
    "training_data": "pm_corpus",
    "epochs": 3-5,
    "learning_rate": 5e-5,
    "batch_size": 4-8
}
```

#### 2.3 Evaluate

Test questions:
- Is it already giving semi-usable plans?
- If yes, proceed; if not, refine your SFT set

### Deliverables
- SFT-trained model checkpoint
- Baseline evaluation results
- Gap analysis report

---

## Phase 3 – PFT (DPO-style) for Planning Quality

### Objectives
- Improve planning quality through preference learning
- Align model to PM best practices

### Tasks

#### 3.1 Prepare Preference Dataset

**Target:** ~5k–50k preference pairs
- Include diverse domains (infra, product, data, etc.)
- Cover multiple planning aspects:
  - Project breakdowns
  - Timeline estimates
  - Risk assessments
  - Stakeholder communications

#### 3.2 Apply DPO / SimPO

**Training configuration:**
```python
dpo_config = {
    "base_model": "sft_checkpoint",
    "preference_data": "pm_preferences",
    "beta": 0.1,  # KL penalty coefficient
    "learning_rate": 1e-6,
    "epochs": 1-3
}
```

**Train until:**
- Offline eval on test set improves significantly
- Human PMs prefer new outputs > baseline

#### 3.3 Freeze Model

Save as **"PM Planner v1"**

### Deliverables
- PFT-trained model checkpoint
- Evaluation showing improvement over SFT baseline
- Human preference validation results

---

## Phase 4 – Tool Integration (Read-Only)

### Objectives
- Connect to real PM tools
- Enable context-aware suggestions

### Tasks

#### 4.1 Implement Tool Clients

**JiraClient:**
- Authentication (OAuth/API token)
- Search issues (JQL)
- Read issue details, comments, history

**GitHubClient:**
- Read PRs, files, diffs
- Read comments and review threads

**NotionClient:**
- Read pages and blocks
- Query databases

**SlackClient:**
- Read channel history
- Read DMs (with permissions)

**Requirements for all clients:**
- Authentication & permissions
- Correct data mapping
- Good logging
- Error handling & retries

#### 4.2 Build Orchestrator v1

**Flow:**
1. User query: "Help me plan Q3 release for Feature X"
2. Orchestrator:
   - Fetches relevant data from tools
   - Provides as context to the PFT model
3. Model outputs plan/summary
4. User reviews (no execution yet)

#### 4.3 Run Pilot with PMs

- Select 5-10 PM early adopters
- Use as "super PM assistant" for suggestions
- Collect feedback on quality and usefulness

### Deliverables
- Read-only tool integrations (Jira, GitHub, Notion, Slack)
- Orchestrator v1 with context retrieval
- Pilot feedback report

---

## Phase 5 – RFT for Tool Usage (Sandboxed)

### Objectives
- Train model to execute tool workflows correctly
- Ensure safe, accurate tool manipulation

### Tasks

#### 5.1 Create Sandbox Environment

Set up **test instances:**
- Test Jira workspace
- GitHub test repos
- Notion test workspace
- Slack test channels

Populate with **synthetic but realistic projects**

#### 5.2 Design Tool-Usage Tasks

**Examples:**
- "Create sprint issues from plan"
- "Update issue statuses based on text spec"
- "Write PR summary as comment"
- "Generate Slack update from Jira board"

**Target:** 50-100 diverse tasks

#### 5.3 Implement Reward Function

**Reward components:**
```python
def reward_function(task, actions, final_state):
    reward = 0
    
    # API call correctness
    reward += 1.0 if all_calls_valid(actions) else -1.0
    
    # Correct field mapping
    reward += 1.0 if correct_fields(actions) else 0
    
    # Consistency with intent
    reward += 1.0 if matches_intent(task, final_state) else -0.5
    
    # Minimal unnecessary calls
    reward -= 0.1 * count_redundant_calls(actions)
    
    return reward
```

#### 5.4 Run RFT

**Training configuration:**
```python
rft_config = {
    "base_model": "pft_checkpoint",
    "environment": "tool_sandbox",
    "algorithm": "PPO",  # or REINFORCE
    "episodes": 1000-5000,
    "learning_rate": 1e-6
}
```

**Train on simulated tool-usage episodes**

#### 5.5 Evaluate

Test on held-out tasks:
- % of tasks completed successfully
- API call correctness
- State consistency

### Deliverables
- RFT-trained model checkpoint
- Sandbox environment setup
- Tool correctness evaluation report

---

## Phase 6 – Human-in-the-Loop Execution in Production

### Objectives
- Enable safe tool execution with oversight
- Build user trust through transparency

### Tasks

#### 6.1 Introduce "Draft + Approval" Pattern

**For any external effect:**
- Jira update
- Slack post
- Notion page creation

**Agent produces:**
- Draft content
- Proposed actions (structured)

#### 6.2 Build Approval UI

**Features:**
- Display proposed actions clearly
- Allow editing before execution
- Options:
  - "Apply all"
  - "Apply selected"
  - "Edit then apply"
  - "Reject"

**Example UI:**
```
Agent proposes:
✓ Create Jira issue "Implement feature X" in PROJECT-123
✓ Assign to: john@company.com
✓ Set sprint: Sprint 24
✓ Post Slack message to #team-alpha: "Started work on feature X..."

[Edit] [Apply All] [Apply Selected] [Reject]
```

#### 6.3 Gradually Expand

**Start with low-risk actions:**
- Comments on existing issues
- Draft messages (not posted)

**Later include:**
- Field updates
- Status changes
- New issue creation

### Deliverables
- Human-in-the-loop approval interface
- Production-ready orchestrator
- Phased rollout plan

---

## Phase 7 – Hardening, Monitoring, and Scale

### Objectives
- Ensure production reliability
- Enable continuous improvement
- Scale to organization

### Tasks

#### 7.1 Add Observability

**Logging:**
- All tool calls with parameters
- User approvals/rejections
- Model outputs and reasoning traces

**Dashboards:**
- Adoption metrics (users, sessions, tasks)
- Error rates by tool and action type
- Action rejection rates
- Latency (p50, p95, p99)

**Example metrics:**
```python
metrics = {
    "daily_active_users": 50,
    "tasks_completed": 200,
    "approval_rate": 0.85,
    "error_rate": 0.05,
    "avg_latency_ms": 3500
}
```

#### 7.2 Add Policy Controls

**Access control:**
- Who can trigger which actions
- Which projects/repos are in scope
- Time-of-day or environment constraints

**Example policy:**
```yaml
policies:
  - user_role: pm
    allowed_tools: [jira, slack, notion]
    allowed_actions: [create, update, comment]
    requires_approval: [create, update]
  
  - user_role: engineer
    allowed_tools: [jira, github]
    allowed_actions: [comment, read]
    requires_approval: [comment]
```

#### 7.3 Expand PFT/RFT Datasets

**Continuously harvest:**
- Human corrections to agent outputs
- Accepted vs rejected suggestions
- User edits before approval

**Use as new preference data:**
- Accepted = positive example
- Rejected/edited = negative example

**Retrain periodically:**
- Monthly or quarterly
- Measure improvement on holdout set

#### 7.4 Scale Deployment

**Expand to:**
- More teams and projects
- Additional tools (Linear, Asana, Confluence, etc.)
- More complex workflows

### Deliverables
- Production monitoring dashboard
- Policy management system
- Continuous learning pipeline
- Organization-wide rollout plan

---

## Success Metrics

### Planning Quality
- **Human rating:** 4.0+/5.0 for plan clarity, realism, coverage
- **Preference tests:** 70%+ prefer agent plans over baseline

### Tool Correctness
- **API success rate:** 95%+ for all tool operations
- **State consistency:** 90%+ match between intent and execution

### User Adoption
- **Active users:** 50+ PMs/EMs using weekly
- **Task completion:** 100+ tasks/week
- **Approval rate:** 80%+ agent suggestions accepted

### Efficiency Gains
- **Time savings:** 30%+ reduction in manual PM work
- **Latency:** <5s for typical requests
- **Error rate:** <5% requiring human intervention

---

## Risk Mitigation

### Data Quality Risks
- **Mitigation:** Multi-reviewer validation of preference pairs
- **Mitigation:** Regular audits of training data

### Model Safety Risks
- **Mitigation:** Sandbox testing before production
- **Mitigation:** Human-in-the-loop for all tool executions initially
- **Mitigation:** Rate limiting and circuit breakers

### Tool Integration Risks
- **Mitigation:** Comprehensive error handling
- **Mitigation:** Graceful degradation (read-only fallback)
- **Mitigation:** Regular integration tests

### User Trust Risks
- **Mitigation:** Transparent action proposals
- **Mitigation:** Easy undo/rollback mechanisms
- **Mitigation:** Clear audit trail

---

## Timeline Estimate

| Phase | Duration | Cumulative |
|-------|----------|------------|
| Phase 0: Scoping | 2 weeks | 2 weeks |
| Phase 1: Data & Eval Setup | 4 weeks | 6 weeks |
| Phase 2: Base + SFT | 3 weeks | 9 weeks |
| Phase 3: PFT Training | 3 weeks | 12 weeks |
| Phase 4: Tool Integration (Read-only) | 4 weeks | 16 weeks |
| Phase 5: RFT Training | 4 weeks | 20 weeks |
| Phase 6: HITL Production | 4 weeks | 24 weeks |
| Phase 7: Hardening & Scale | 4 weeks | 28 weeks |

**Total: ~6-7 months** for full production deployment

---

## Team Requirements

### Core Team
- **1 ML Engineer:** Model training (SFT, PFT, RFT)
- **1 Backend Engineer:** Tool integrations, orchestrator
- **1 Frontend Engineer:** Approval UI, dashboards
- **1 PM/Product Designer:** Requirements, UX, user testing
- **0.5 DevOps/SRE:** Infrastructure, monitoring

### Extended Team
- **Domain Experts (PMs):** Preference labeling, validation
- **Security/Compliance:** Policy review, audit requirements

---

**End of Implementation Blueprint**
