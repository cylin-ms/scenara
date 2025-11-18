# AI Project Management Agent: Technical Architecture

**Author**: Chin-Yew Lin  
**Created**: November 17, 2025  
**Document Type**: Technical Design Document / RFC

---

## 1. Overview

**Goal:**  
Design an AI PM Agent that:
- Generates high-quality project plans (using PFT), and
- Reliably manipulates PM tooling (using RFT),

for Jira, GitHub, Notion, Slack in an enterprise environment.

---

## 2. Requirements

### Functional Requirements

- **Understand project context from:**
  - Specs, tickets, PRs, chats

- **Generate:**
  - Project plans, timelines, risks, communications

- **Draft or execute actions in:**
  - Jira (issues, epics, sprints)
  - GitHub (PR summaries/comments)
  - Notion (docs/pages)
  - Slack (status updates, reminders)

- **Support human-in-the-loop approval flow**

### Non-Functional Requirements

- Low-latency (< 5–10s) for typical tasks
- Observability & logging
- Scalable across teams/projects
- Authentication & RBAC integration (e.g., SSO/OAuth)

---

## 3. System Architecture

### Core Components

#### 3.1 LLM Service
- PM-specialized model (SFT + PFT)
- Extended with RFT for tool usage

#### 3.2 Agent Orchestrator
- Receives user queries
- Maintains conversation / task state
- Calls tools or LLM as needed
- Applies business rules (approvals, policies)

#### 3.3 Tool Integrations
- **JiraClient**: REST API, JQL, webhooks
- **GitHubClient**: REST/GraphQL, PR metadata
- **NotionClient**: Page DB API
- **SlackClient**: Bot token, channel & DM APIs

#### 3.4 Knowledge & Memory

**Vector Store** (e.g., pgvector, Milvus, Pinecone)
- Embeddings of PRDs, tickets, runbooks, etc.

**Short-term Memory**
- Dialogue + active task state

**Long-term Project Memory**
- Canonical "project summary" doc maintained by the agent

#### 3.5 Policy & Safety Layer
- Action filters
- Rate limits
- Sensitive-action approvals
- Red-team & safety checks (optional)

#### 3.6 Frontend / UX
- Web UI
- Jira plugin
- Notion sidebar
- Slack bot

---

## 4. Model Training Strategy

### 4.1 Base + SFT

- **Start with a capable base model** (coding + reasoning)

- **SFT on:**
  - PRDs, specs, sprint docs, incident reports
  - Real project plans & retros
  - Risk registers, QBR decks

### 4.2 PFT (DPO-style)

- **Collect preference pairs:**
  - [BetterPlan, WorsePlan]
  - [BetterTimeline, WorseTimeline]
  - [BetterRiskList, WorseRiskList]
  - [BetterSlackUpdate, WorseSlackUpdate]

- **Train with DPO-like objective:**
  - Increase log-prob of "better" vs "worse"

**Result:** Model reliably produces high-quality planning artifacts.

### 4.3 RFT (Reinforcement Fine-Tuning)

- **Build a sandbox environment that simulates:**
  - Jira boards, issues, statuses
  - GitHub repos, PRs
  - Notion pages
  - Slack channels/messages

- **Define tasks:**
  - "Create sprint board with these issues"
  - "Move done tickets to 'Done' and write summary"
  - "Create Notion page summarizing PRs"

- **Design rewards:**
  - API call success
  - Correct field mapping
  - Consistency between summary and underlying data
  - Minimizing unnecessary calls

**RFT can be done:**
- Offline on logged human workflows, or
- In a simulated environment

---

## 5. Tool Integration Details

### JiraClient

- **Auth:** OAuth/API token

- **Features:**
  - Search issues with JQL
  - Create/update issues
  - Manage sprints & epics
  - Add comments

### GitHubClient

- **Read:** PRs, files, diffs, comments
- **Write:** PR comments, labels, maybe review summaries

### NotionClient

- **Read:** Pages, blocks
- **Write:** New pages, edit sections, add tables (risk registers, timelines)

### SlackClient

- Post messages to channels/DMs
- Create/update threaded messages
- Optional: ephemeral "drafts" to be edited by user

### Common Requirements

All clients must support:
- Test/sandbox mode
- Robust error handling & retries
- Structured logging

---

## 6. Reasoning & Planning Modules

These are logical modules, usually implemented as:
- System prompts + few-shot examples
- Possible higher-level agent logic

### Examples

#### 6.1 Project Planner
- **Inputs:** Goal, constraints, historical data
- **Output:** Phases, milestones, tasks, owners

#### 6.2 Timeline Estimator
- Uses historical ticket throughput & velocity
- Produces date ranges, buffer times

#### 6.3 Risk Engine
- Scans docs + tickets
- Generates structured risk entries

#### 6.4 Dependency Resolver
- Identifies sequencing constraints
- Proposes critical path

---

## 7. Memory, Retrieval & Context Management

### Multi-source Retrieval
- Vector search over docs
- Jira/GitHub/Notion via API queries

### Context Window Management
- Summarization of older info
- Structured "project summary" document regularly refreshed

**"Project Memory"** can be a Notion page or DB that the agent itself maintains as the canonical state-of-project narrative.

---

## 8. Evaluation & Monitoring

### Offline Evaluation
- Plan quality benchmarks
- Tool correctness tests
- Synthetic scenarios + checklists

### Online Evaluation
- User rating per session
- Action acceptance vs rejection rate
- Incident reports (bad actions, misalignments)

### Telemetry
- Latency, cost, throughput
- API call stats per tool
- Breakdown by team

---

## 9. Security & Governance

### Authentication & Authorization
- **SSO integration** (Azure AD, Okta, etc.)

- **Per-user / per-team scopes:**
  - Which Jira projects
  - Which Slack channels
  - Which GitHub orgs

### Execution Modes
- **"Draft-only" vs "execute" mode** per user / team

### Audit Trail
- **Full audit log for:**
  - Prompts
  - Tool calls
  - Responses
  - Approvals

---

## 10. Roadmap

- **v0.1:** Read-only PM advisor (no tool writes)
- **v0.2:** Draft generator (Jira tickets, Slack messages, Notion pages)
- **v0.3:** Limited auto-execution w/ approvals
- **v1.0:** Org-level deployment, KPIs, governance policies

---

**End of Technical Architecture Document**
