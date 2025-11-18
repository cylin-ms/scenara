# AI Project Management Agent: Slide Deck

**Author**: Chin-Yew Lin  
**Created**: November 17, 2025  
**Format**: 10-15 Slide Presentation

---

## Slide 1 – Title & Vision

**Title:**  
AI Project Management Agent: From Planning to Execution

**Subtitle:**  
Using Preference Fine-Tuning (PFT) + Reinforcement Fine-Tuning (RFT) with Jira, GitHub, Notion, Slack

**Key Message:**  
Turn LLMs into senior PM copilots that can plan, track, and communicate across your real tools.

---

## Slide 2 – Problem & Opportunity

**PM work is:**
- Fragmented across Jira, GitHub, Notion, Slack
- Full of repetitive status updates and manual planning
- Often inconsistent in quality between teams

**LLMs today:**
- Can "talk about" projects,
- But aren't reliably grounded in your tickets, repos, docs, and chats.

**Opportunity:**  
An agent that can understand the project, propose realistic plans, and operate tools safely.

---

## Slide 3 – Design Goals

1. **Enterprise-grade planning**
   - Hierarchical plans, realistic timelines, clear risks

2. **Tool-native execution**
   - Create/update Jira issues, GitHub PR summaries, Notion specs, Slack updates

3. **Reliable & auditable**
   - Human-in-the-loop approvals
   - Policy guardrails and logs

4. **Composable architecture**
   - Swap model, tools, or data sources without redoing everything

---

## Slide 4 – High-Level Architecture

**Four main layers:**

1. **Foundation & Alignment Layer**
   - Base LLM + SFT + PFT (DPO) + safety policies

2. **Reasoning & Planning Layer**
   - Project planner, timeline estimator, risk engine, dependency resolver

3. **Tool & Data Layer**
   - Jira, GitHub, Notion, Slack connectors
   - Vector search over project docs, tickets, specs

4. **Orchestration & UX Layer**
   - Agent controller, workflows, approvals
   - UI: chat, side-panel in Jira/Notion, Slack app

*(Visual: a 4-layer stack diagram.)*

---

## Slide 5 – Foundation & Alignment (PFT)

- **Start with a strong base LLM** (general + coding).

- **SFT on:**
  - PRDs, sprint docs, design docs, runbooks

- **PFT / DPO on preference datasets:**
  - Good vs bad project breakdowns
  - Strong vs weak timelines
  - Good vs bad risk registers
  - High vs low quality stakeholder comms

**Outcome:**  
The model "thinks like a senior PM."

---

## Slide 6 – Reinforcement Fine-Tuning (RFT) for Tool Workflows

- **Offline environment that simulates:**
  - Jira: create/update tickets, change status, assign
  - GitHub: read PR metadata, post summary comments
  - Notion: read/write pages
  - Slack: draft & send updates (with approval)

- **Reward examples:**
  - +1 if the right Jira field is set
  - +1 if the right repo/branch is referenced
  - +1 if Slack summary matches actual issue state
  - -1 if invalid API calls or inconsistent states

**Outcome:**  
The model executes workflows correctly, not just "talk about them".

---

## Slide 7 – Core Components

- **LLM Core** (PFT + RFT trained)

- **Agent Orchestrator**
  - Decides when to call tools vs. reason internally

- **Memory & Retrieval**
  - Vector DB over specs, tickets, docs

- **Tool Adapters**
  - JiraClient, GitHubClient, NotionClient, SlackClient

- **Policy & Safety Layer**
  - Access scope, rate limiting, approval policy

---

## Slide 8 – Data & Knowledge Flow

1. **User asks:** "Help me plan Q3 release for Feature X."

2. **Agent:**
   - Retrieves relevant docs (Notion/Confluence)
   - Fetches Jira epics + open bugs
   - Checks GitHub branches/PRs
   - Fetches last Slack status updates

3. **LLM:**
   - Synthesizes a project plan, timelines, risks
   - Proposes Jira changes & Slack message drafts

4. **Human:**
   - Reviews & approves changes / messages

---

## Slide 9 – Example Use Case: Sprint Planning

**Input:**  
"Create a 3-sprint plan to ship Feature X."

**Agent:**
- Gets existing Jira epics/issues
- Groups into sprints by priority, dependencies, team capacity
- Proposes new tickets for gaps
- Writes a Slack summary for the team

**Human approves:**
- Agent creates/updates Jira issues
- Posts Slack summary draft to a channel

---

## Slide 10 – Example Use Case: Risk Review

**Input:**  
"List top 10 risks for Feature X and mitigation plans."

**Agent:**
- Reads spec, Jira issues, known blockers
- Uses risk-register patterns to propose:
  - Risk name, impact, probability, owner, mitigation
- Drafts a Notion "Risk Register" section

**Human approves and edits as needed.**

---

## Slide 11 – Evaluation & Metrics

- **Planning quality**
  - Human rating of plans (clarity, realism, coverage)

- **Tool correctness**
  - % of successful Jira/GitHub/Notion actions

- **Latency & UX**
  - Time from request to draft plan

- **Adoption & satisfaction**
  - PM/EM satisfaction scores
  - Reduction in manual PM work

---

## Slide 12 – Security, Governance, & Audit

- **Scoped permissions per tool**

- **All actions logged with:**
  - Who requested
  - What the agent proposed
  - What was executed

- **Sensitive operations require:**
  - Approval
  - Or "draft-only" mode

---

## Slide 13 – Roadmap

- **Phase 1:** Read-only advisor (no writes, only suggestions)
- **Phase 2:** Draft creator (Jira/Slack drafts, Notion pages)
- **Phase 3:** Limited auto-execution with guardrails
- **Phase 4:** Org-wide deployment + custom policies & KPIs

---

**End of Slide Deck**
