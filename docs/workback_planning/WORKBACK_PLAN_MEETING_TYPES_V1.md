# Workback Plan Meeting Types V1.0

**Date**: November 17, 2025  
**Author**: Chin-Yew Lin  
**Purpose**: Define 10 canonical meeting types requiring workback plans with various T-x time ranges  
**Framework**: Covers T-7 (1 week) through T-90 (90 days) planning horizons

**Related Documents**:
- [Workback Plan Canonical Tasks V1.0](./WORKBACK_PLAN_CANONICAL_TASKS_V1.md)
- [Workback Plan Evaluation Framework V1.0](./WORKBACK_PLAN_EVALUATION_FRAMEWORK_V1.md)

---

## Executive Summary

Workback plans are essential for meetings that require **advance preparation** and **coordinated execution** across multiple stakeholders. This document defines **10 canonical meeting types** organized by planning horizon:

**Planning Horizon Categories**:
- **Short-term** (T-7 to T-14): 1-2 weeks preparation
- **Standard** (T-30 to T-60): 30-60 days preparation (most common)
- **Long-term** (T-90+): 90+ days preparation (strategic initiatives)

**Selection Criteria**:
1. **Cross-functional coordination** - Multiple departments/teams involved
2. **Deliverables required** - Concrete outputs needed before meeting
3. **Stakeholder dependencies** - Sequential approvals or dependencies
4. **Business impact** - High-stakes decisions or launches
5. **Recurring pattern** - Predictable cadence enabling advance planning

---

## 10 Canonical Meeting Types for Workback Planning

### Category 1: Short-Term Planning (T-7 to T-14)

#### 1. Weekly Team Newsletter
**Planning Horizon**: T-7 (1 week)  
**Meeting Classification**: Content Distribution  
**Typical Duration**: Newsletter sent Friday, planning starts previous Friday

**Characteristics**:
- **Participants**: 2-4 (Content creator, Reviewer, Approver, Marketing Ops)
- **Deliverables**: Newsletter content, graphics, distribution list
- **Phases**: Simple sequence (Draft → Review → Approve → Produce → Send)
- **Complexity**: Low - minimal dependencies
- **Approval gates**: 1-2 (content review, final approval)

**Example Prompt**:
> "Create a workback plan for our weekly team newsletter sent every Friday at 9 AM"

**Expected Plan Structure**:
- 8-12 tasks
- 2-4 participants
- 2-3 deliverables
- No formal phases (simple task sequence)
- 1-2 milestones

**Key Dependencies**:
- Content draft → Review
- Review approval → Production
- Production → Distribution

---

#### 2. Sprint Planning Meeting (2-week sprint)
**Planning Horizon**: T-14 (2 weeks)  
**Meeting Classification**: Agile Ceremony  
**Typical Duration**: 2-hour meeting at start of sprint

**Characteristics**:
- **Participants**: 4-6 (PM, Engineering Lead, Design Lead, QA Lead, Scrum Master, Stakeholders)
- **Deliverables**: Sprint backlog, capacity plan, sprint goals document
- **Phases**: Preparation → Execution → Follow-up
- **Complexity**: Medium - moderate dependencies
- **Approval gates**: 1-2 (backlog refinement, sprint commitment)

**Example Prompt**:
> "Create a workback plan for our sprint planning meeting on Nov 29, starting prep today"

**Expected Plan Structure**:
- 15-20 tasks
- 4-6 participants
- 3-4 deliverables
- 3 phases (prep/execute/follow-up)
- 3-4 milestones

**Key Dependencies**:
- Backlog grooming → Story estimation
- Capacity planning → Sprint commitment
- Sprint goals → Task assignment

---

### Category 2: Standard 30-Day Planning (T-30)

#### 3. Monthly Business Review (MBR)
**Planning Horizon**: T-30 (30 days)  
**Meeting Classification**: Executive Review  
**Typical Duration**: 2-3 hour meeting, monthly cadence

**Characteristics**:
- **Participants**: 6-8 (Data owners, Analysts, Presenters, Department heads, Executives)
- **Deliverables**: Metrics dashboard, analysis deck, recommendations document, action items
- **Phases**: Data Collection → Analysis → Presentation Prep → Review → Delivery
- **Complexity**: High - multiple data sources and approvals
- **Approval gates**: 3-4 (data validation, analysis review, deck review, exec preview)

**Example Prompt**:
> "Create a workback plan for our Monthly Business Review with exec team on December 15"

**Expected Plan Structure**:
- 25-35 tasks
- 6-8 participants
- 4-5 deliverables
- 4-5 phases
- 5-6 milestones

**Key Dependencies**:
- Data collection → Data validation
- Analysis → Insights generation
- Draft deck → Multiple review rounds
- Exec preview → Final presentation

---

#### 4. Product Feature Launch
**Planning Horizon**: T-30 (30 days)  
**Meeting Classification**: Launch Event  
**Typical Duration**: Launch day + launch meeting/announcement

**Characteristics**:
- **Participants**: 6-10 (PM, Engineering, QA, Design, Marketing, Sales, Support, Leadership)
- **Deliverables**: Launch plan, feature documentation, marketing materials, training docs, rollout schedule
- **Phases**: Planning → Development Complete → Testing → Pre-launch → Launch → Post-launch
- **Complexity**: High - critical path dependencies
- **Approval gates**: 4-5 (feature complete, QA signoff, launch readiness, go/no-go, post-launch review)

**Example Prompt**:
> "Create a workback plan for launching our new AI assistant feature on January 15, 2026"

**Expected Plan Structure**:
- 35-45 tasks
- 8-10 participants
- 6-8 deliverables
- 6 phases
- 6-8 milestones

**Key Dependencies**:
- Feature complete → QA testing
- QA signoff → Marketing materials
- Documentation → Training
- All pre-launch → Go/no-go decision
- Launch → Monitoring

---

#### 5. Squad Mission Planning (6-8 Week Cycle)
**Planning Horizon**: T-42 to T-56 (6-8 weeks)  
**Meeting Classification**: Agile Squad Planning  
**Typical Duration**: Mission planning session + 2-week milestone reviews

**Characteristics**:
- **Participants**: 8-12 (DRI, PM, Engineers, UX Design/Research, Data Science, Applied Science)
- **Deliverables**: Mission statement, milestone breakdown (2-week increments), metrics dashboard, backlog prioritization
- **Phases**: Mission Definition → Milestone Planning → Execution → 2-Week Check-ins → Cycle Review
- **Complexity**: Medium-High - cross-functional with clear MMM (Mission, Milestones, Metrics)
- **Approval gates**: 2-3 (mission approval, milestone checkpoints, cycle scorecard)

**Squad Model Context** (from GXP/Microsoft):
- Small, cross-functional, autonomous teams (8-12 people)
- Responsible for specific mission with end-to-end value delivery
- Mission = falsifiable, time-boxed objective (1 cycle = 7-8 weeks)
- Milestones = key deliverables in 2-week increments
- Metrics = quantitative measures for testable goals

**Example Prompt**:
> "Create a workback plan for our Squad Mission: 'Improve email search relevance by 20% in 8 weeks' starting December 1"

**Expected Plan Structure**:
- 30-40 tasks
- 8-12 participants (full squad)
- 5-7 deliverables (aligned to 2-week milestones)
- 5 phases (Mission kickoff → Sprint 1 → Sprint 2 → Sprint 3 → Sprint 4 + Review)
- 4-5 milestones (aligned to 2-week increments)

**Key Dependencies**:
- Mission definition → Milestone breakdown
- Each 2-week milestone → Next milestone
- Research/design → Engineering implementation
- Implementation → Data validation
- Cycle end → Metrics review and next mission planning

**Squad Roles**:
- **DRI (Directly Responsible Individual)**: Accountable for mission success, primary decision maker
- **PM**: Define mission, prioritize backlog, ensure alignment with outcomes
- **Engineering**: Build, test, maintain, ensure quality and automation
- **UX Design/Research**: Shape user experience, validate usability/accessibility
- **Data Science**: Data-driven experimentation, modeling, measurable impact

---

### Category 3: Standard 60-Day Planning (T-60)

#### 6. Quarterly Business Review (QBR)
**Planning Horizon**: T-60 (60 days)  
**Meeting Classification**: Strategic Review  
**Typical Duration**: Half-day or full-day meeting, quarterly cadence

**Characteristics**:
- **Participants**: 8-12 (Data owners, Analysts, Department leads, Executives, Board members)
- **Deliverables**: Quarterly metrics report, strategic analysis, recommendations, next quarter OKRs, budget proposals
- **Phases**: Data Collection → Analysis → Strategy Development → Presentation Prep → Review Cycles → Delivery → Follow-up
- **Complexity**: Very High - extensive coordination and approvals
- **Approval gates**: 5-6 (data validation, analysis review, strategy alignment, deck review, exec preview, final signoff)

**Example Prompt**:
> "Create a workback plan for Q4 2025 QBR with board on December 20, starting today"

**Expected Plan Structure**:
- 40-55 tasks
- 8-12 participants
- 6-8 deliverables
- 7 phases
- 8-10 milestones

**Key Dependencies**:
- Data collection (multiple sources) → Consolidation
- Analysis → Strategic insights
- Multiple review cycles (parallel and sequential)
- Exec alignment → Board presentation
- QBR → OKR setting for next quarter

---

#### 6. Annual Kickoff Meeting Planning
**Planning Horizon**: T-60 (60 days)  
**Meeting Classification**: Team Event  
**Typical Duration**: Multi-day event (2-3 days), annual cadence

**Characteristics**:
- **Participants**: 8-15 (Leadership team, Event planning, Content creators, Presenters, Logistics, IT/AV, HR)
- **Deliverables**: Event agenda, presentation decks, venue/logistics plan, team activities, post-event survey
- **Phases**: Planning → Content Development → Logistics → Rehearsal → Event Execution → Follow-up
- **Complexity**: High - many parallel workstreams
- **Approval gates**: 4-5 (agenda approval, budget approval, content review, logistics confirmation, dry run)

**Example Prompt**:
> "Create a workback plan for our annual sales kickoff event January 20-22, 2026"

**Expected Plan Structure**:
- 45-60 tasks
- 10-15 participants
- 8-10 deliverables
- 6 phases
- 8-10 milestones

**Key Dependencies**:
- Venue booking → Logistics planning
- Agenda → Content creation
- Content → Rehearsals
- All logistics → Event execution
- Event → Follow-up survey

---

### Category 4: Long-Term 90-Day Planning (T-90)

#### 7. Product Launch (Major Release)
**Planning Horizon**: T-90 (90 days)  
**Meeting Classification**: Major Launch Event  
**Typical Duration**: Launch day + launch event, annual or semi-annual

**Characteristics**:
- **Participants**: 10-20 (Product, Engineering, Design, QA, Marketing, Sales, Support, Partners, Legal, Finance, Leadership)
- **Deliverables**: Product, launch plan, GTM strategy, marketing campaign, sales enablement, partner materials, pricing, legal docs
- **Phases**: Planning → Development → Alpha → Beta → Release Candidate → Launch Prep → Launch → Post-launch
- **Complexity**: Very High - critical path across multiple teams
- **Approval gates**: 6-8 (feature freeze, alpha, beta, RC, pricing approval, legal review, launch readiness, go/no-go)

**Example Prompt**:
> "Create a workback plan for launching Scenara 2.0 on March 1, 2026, starting today"

**Expected Plan Structure**:
- 60-80 tasks
- 12-20 participants
- 10-15 deliverables
- 8 phases
- 10-12 milestones

**Key Dependencies**:
- Feature freeze → Development complete
- Alpha → Beta → RC (sequential gates)
- Development → Marketing materials
- Beta feedback → Product refinement
- All workstreams converge at launch
- Launch → 30-day post-launch review

---

#### 8. Strategic Planning Offsite
**Planning Horizon**: T-90 (90 days)  
**Meeting Classification**: Strategic Session  
**Typical Duration**: 2-3 day offsite, annual or bi-annual

**Characteristics**:
- **Participants**: 8-15 (Executive team, Department heads, Strategy team, Board advisors, External facilitator)
- **Deliverables**: Strategic plan, OKRs, budget allocation, org changes, communication plan, board deck
- **Phases**: Pre-work → Data Analysis → Strategy Development → Alignment Sessions → Offsite Prep → Offsite Execution → Follow-up
- **Complexity**: Very High - requires extensive pre-work and alignment
- **Approval gates**: 5-6 (data review, strategy drafts, pre-reads, exec alignment, board preview, final approval)

**Example Prompt**:
> "Create a workback plan for our 2026 strategic planning offsite February 10-12, starting today"

**Expected Plan Structure**:
- 50-70 tasks
- 10-15 participants
- 8-12 deliverables
- 7 phases
- 10-12 milestones

**Key Dependencies**:
- Market research → Competitive analysis
- Analysis → Strategy options
- Pre-reads → Offsite discussions
- Offsite outcomes → Communication plan
- Strategic plan → OKR cascade

---

#### 9. Board Meeting (Annual Planning)
**Planning Horizon**: T-90 (90 days)  
**Meeting Classification**: Governance  
**Typical Duration**: 4-6 hour meeting, quarterly with annual planning focus

**Characteristics**:
- **Participants**: 6-12 (CEO, CFO, COO, Board members, Executive team, Legal, Finance, Strategy)
- **Deliverables**: Board deck, financial reports, strategic plan, governance updates, committee reports, resolutions
- **Phases**: Planning → Data Collection → Report Preparation → Exec Review → Board Material Prep → Pre-reads → Board Meeting → Follow-up
- **Complexity**: Very High - high stakes, extensive documentation
- **Approval gates**: 5-7 (financial close, audit review, exec alignment, legal review, board material review, final signoff)

**Example Prompt**:
> "Create a workback plan for Q4 2025 Board Meeting with annual planning on December 15"

**Expected Plan Structure**:
- 55-75 tasks
- 8-12 participants
- 10-15 deliverables
- 8 phases
- 10-12 milestones

**Key Dependencies**:
- Financial close → Audit
- Audit → Board financials
- Strategic analysis → Board recommendations
- All materials → Board package
- Pre-reads distribution → Board meeting
- Board meeting → Action items

---

#### 10. Merger/Acquisition Integration Planning
**Planning Horizon**: T-90+ (90+ days)  
**Meeting Classification**: Integration Kickoff  
**Typical Duration**: Multi-day workshop, one-time event

**Characteristics**:
- **Participants**: 15-30 (Leadership from both companies, Integration team, HR, Legal, Finance, IT, Operations, Comms)
- **Deliverables**: Integration plan, org structure, synergy plan, communication strategy, Day 1 plan, 100-day plan
- **Phases**: Pre-planning → Due Diligence → Integration Planning → Workstream Setup → Kickoff Prep → Integration Kickoff → Execution
- **Complexity**: Extreme - highest complexity, many unknowns
- **Approval gates**: 7-10 (legal approval, board approval, regulatory, org design, communication plan, Day 1 readiness, multiple exec reviews)

**Example Prompt**:
> "Create a workback plan for M&A integration kickoff meeting on February 1, 2026, starting today"

**Expected Plan Structure**:
- 70-100 tasks
- 15-30 participants
- 15-20 deliverables
- 8-10 phases
- 12-15 milestones

**Key Dependencies**:
- Legal close → Integration planning
- Due diligence → Risk assessment
- Org design → Communication plan
- All workstreams → Integration kickoff
- Day 1 plan → 100-day plan
- Multiple parallel and sequential dependencies

---

## Meeting Type Comparison Matrix

| Meeting Type | Planning Horizon | Participants | Tasks | Deliverables | Phases | Complexity | Approval Gates |
|--------------|------------------|--------------|-------|--------------|--------|------------|----------------|
| **1. Weekly Newsletter** | T-7 (1 week) | 2-4 | 8-12 | 2-3 | 1 (sequence) | Low | 1-2 |
| **2. Sprint Planning** | T-14 (2 weeks) | 4-6 | 15-20 | 3-4 | 3 | Medium | 1-2 |
| **3. Monthly Business Review** | T-30 | 6-8 | 25-35 | 4-5 | 5 | High | 3-4 |
| **4. Feature Launch** | T-30 | 8-10 | 35-45 | 6-8 | 6 | High | 4-5 |
| **5. Squad Mission** | T-42 to T-56 (6-8 weeks) | 8-12 | 30-40 | 5-7 | 5 | Medium-High | 2-3 |
| **6. Quarterly Business Review** | T-60 | 8-12 | 40-55 | 6-8 | 7 | Very High | 5-6 |
| **7. Annual Kickoff** | T-60 | 10-15 | 45-60 | 8-10 | 6 | High | 4-5 |
| **8. Major Product Launch** | T-90 | 12-20 | 60-80 | 10-15 | 8 | Very High | 6-8 |
| **9. Strategic Offsite** | T-90 | 10-15 | 50-70 | 8-12 | 7 | Very High | 5-6 |
| **10. Board Meeting** | T-90 | 8-12 | 55-75 | 10-15 | 8 | Very High | 5-7 |
| **11. M&A Integration** | T-90+ | 15-30 | 70-100 | 15-20 | 8-10 | Extreme | 7-10 |

**Trends Observed**:
- **Planning horizon correlates with complexity**: Longer horizons require more coordination
- **Participants scale with complexity**: More complex meetings need more cross-functional involvement
- **Approval gates increase with stakes**: Higher business impact = more governance
- **Task count grows non-linearly**: T-90 meetings have 8-10x more tasks than T-7
- **Deliverables plateau**: Even complex meetings rarely exceed 15-20 concrete deliverables

---

## Planning Horizon Guidelines

### T-7 (1 Week Planning)
**Use Cases**: Weekly recurring meetings, routine updates, simple content delivery

**Characteristics**:
- Minimal coordination needed
- Few dependencies (mostly sequential)
- Single owner or small team
- Low stakes (can reschedule if needed)
- No formal phases

**LLM Prompt Strategy**: Emphasize simplicity and efficiency

---

### T-14 (2 Week Planning)
**Use Cases**: Sprint ceremonies, team meetings, routine presentations

**Characteristics**:
- Some coordination needed
- Moderate dependencies
- Small cross-functional team
- Medium stakes
- Simple phases (prep/execute/follow-up)

**LLM Prompt Strategy**: Balance structure with agility

---

### T-30 (30-Day Planning)
**Use Cases**: Monthly reviews, feature launches, departmental planning

**Characteristics**:
- Significant coordination required
- Multiple dependencies (parallel and sequential)
- Cross-functional teams
- High stakes (business impact)
- Clear phases (4-6)

**LLM Prompt Strategy**: Emphasize dependencies and milestones

**Most Common Horizon**: ~50% of workback plans fall in T-30 range

---

### T-60 (60-Day Planning)
**Use Cases**: Quarterly reviews, annual events, major planning sessions

**Characteristics**:
- Extensive coordination required
- Complex dependency chains
- Multiple teams and stakeholders
- Very high stakes
- Multiple phases (6-7)

**LLM Prompt Strategy**: Focus on critical path and approval gates

---

### T-90+ (90+ Day Planning)
**Use Cases**: Strategic initiatives, major launches, governance events, M&A

**Characteristics**:
- Maximum coordination required
- Highly complex dependencies
- Large cross-functional teams (10-30 people)
- Extreme stakes (company/board level)
- Many phases (8-10)

**LLM Prompt Strategy**: Emphasize risk management, buffer time, contingency planning

**Challenge**: Uncertainty increases with horizon - need flexibility

---

## Meeting Type Selection for Evaluation

### Recommended Test Set (4 Scenarios)

**For LLM evaluation and model comparison**, we recommend testing with these 4 meeting types:

1. **Weekly Newsletter** (T-7) - Simple baseline
   - Tests: Basic task generation, simple dependencies
   - Expected score: 85-90% (straightforward)

2. **Monthly Business Review** (T-30) - Standard complexity
   - Tests: Phase structure, approval gates, data workflows
   - Expected score: 75-85% (moderate difficulty)

3. **Quarterly Business Review** (T-60) - High complexity
   - Tests: Complex dependencies, multiple stakeholders, strategic alignment
   - Expected score: 70-80% (challenging)

4. **Major Product Launch** (T-90) - Very high complexity
   - Tests: Critical path, parallel workstreams, risk management
   - Expected score: 65-75% (most challenging)

**Rationale**: These 4 cover the spectrum from simple to extreme complexity, testing all canonical tasks.

---

## Canonical Task Coverage by Meeting Type

### Task Coverage Matrix

| Canonical Task | Newsletter | Sprint | MBR | Feature | Squad | QBR | Kickoff | Launch | Offsite | Board | M&A |
|----------------|-----------|--------|-----|---------|-----|---------|--------|---------|-------|-----|
| **WBP-01: NLU** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **WBP-02: Milestones** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **WBP-03: Tasks** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **WBP-04: Dependencies** | ⚠️ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **WBP-05: Duration** | ❌ | ⚠️ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **WBP-06: Participants** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **WBP-07: Critical Path** | ❌ | ❌ | ⚠️ | ✅ | ⚠️ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **WBP-08: Backward Sched** | ❌ | ❌ | ⚠️ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **WBP-09: Deliverables** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **WBP-10: Validation** | ⚠️ | ⚠️ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **WBP-11: Doc Gen** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **WBP-12: Buffer** | ❌ | ⚠️ | ⚠️ | ✅ | ⚠️ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **WBP-13: Historical** | ❌ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **WBP-14: Multi-Project** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ✅ |
| **WBP-15: Quality Eval** | ⚠️ | ⚠️ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

**Legend**:
- ✅ Fully applicable
- ⚠️ Partially applicable
- ❌ Not applicable

**Key Insights**:
- **WBP-01, 02, 03, 06, 09, 11**: Universal (all meeting types need these)
- **WBP-07, 08**: Only applicable for T-30+ with complex dependencies
- **WBP-14**: Only truly needed for M&A or large portfolio initiatives
- **Simple meetings** (Newsletter, Sprint): Use 6-8 canonical tasks
- **Complex meetings** (Launch, Board, M&A): Use 12-15 canonical tasks

---

## Implementation Recommendations

### Phase 1: T-30 Focus (Current)
- Implement evaluation framework for T-30 meetings (MBR, Feature Launch)
- Baseline gpt-oss:120b performance on standard 30-day scenarios
- Achieve 80%+ ACRUE scores on T-30 complexity

### Phase 2: Expand to T-7 and T-60
- Add T-7 simple scenarios (Newsletter, Sprint Planning)
- Add T-60 strategic scenarios (QBR, Annual Kickoff)
- Test canonical task coverage across all three horizons

### Phase 3: T-90 Advanced
- Implement WBP-07 (Critical Path) and WBP-08 (Backward Scheduling)
- Add T-90 scenarios (Major Launch, Strategic Offsite, Board Meeting)
- Focus on risk management and contingency planning

### Phase 4: Extreme Complexity (Future)
- Add M&A integration scenario
- Implement WBP-14 (Multi-Project Coordination)
- Test 100+ task workback plans

---

## Example Prompts for Each Meeting Type

### 1. Weekly Newsletter (T-7)
```
Create a workback plan for our weekly team newsletter. 
- Newsletter sent every Friday at 9 AM PST
- Content includes project updates, team wins, upcoming events
- Need approval from team lead before sending
- Target: 500 word newsletter with 2-3 sections
```

### 2. Sprint Planning (T-14)
```
Create a workback plan for Sprint 24 planning meeting on November 29.
- 2-week sprint starting November 29
- Team of 8 engineers, 1 PM, 1 designer
- Need refined backlog, story estimates, and sprint goals
- Meeting scheduled for 2 hours
```

### 3. Monthly Business Review (T-30)
```
Create a workback plan for December MBR on December 15 with exec team.
- Need metrics for all departments (Sales, Marketing, Product, Engineering, Finance)
- Present key insights, trends, and recommendations
- Exec team expects 30-minute presentation + Q&A
- Requires data validation and multiple review rounds
```

### 4. Feature Launch (T-30)
```
Create a workback plan for launching AI assistant feature on January 15, 2026.
- Feature currently in development, code freeze December 20
- Need QA testing, documentation, marketing materials, sales training
- Launch includes blog post, email campaign, in-app announcement
- Post-launch monitoring for 2 weeks
```

### 5. Squad Mission Planning (T-42 to T-56)
```
Create a workback plan for our Squad Mission: 'Improve email search relevance by 20% in 8 weeks'.
- Mission cycle: December 1 - January 26 (8 weeks)
- Squad: 10 people (DRI, PM, 5 engineers, UX designer, UX researcher, data scientist)
- Milestones every 2 weeks (Dec 15, Dec 29, Jan 12, Jan 26)
- Key metrics: Search relevance score, user satisfaction, query success rate
- Deliverables: Research insights, design updates, ML model improvements, A/B test results
```

### 6. Quarterly Business Review (T-60)
```
Create a workback plan for Q4 2025 QBR with board on December 20.
- Full day meeting (9 AM - 5 PM)
- Cover Q4 results, 2025 recap, 2026 strategy, budget requests
- Need comprehensive data analysis from all departments
- Board deck due 1 week before meeting for pre-reads
- Expect 3-4 review cycles with exec team
```

### 6. Annual Kickoff (T-60)
```
Create a workback plan for 2026 Sales Kickoff January 20-22, 2026.
- 3-day event for 200+ sales team members
- Need venue, agenda, presentations, team activities, swag
- Day 1: Company vision, Day 2: Product training, Day 3: Sales training
- Multiple executive presentations requiring content and rehearsal
```

### 7. Major Product Launch (T-90)
```
Create a workback plan for Scenara 2.0 launch on March 1, 2026.
- Major product release with new AI features, redesigned UX, enterprise tier
- Need beta program, launch event, press coverage, partner enablement
- Coordinate Engineering, Product, Marketing, Sales, Support, Legal
- Feature freeze January 15, beta launch February 1, GA March 1
```

### 8. Strategic Offsite (T-90)
```
Create a workback plan for 2026 strategic planning offsite February 10-12.
- Executive team + department heads (15 people)
- Define 2026 strategy, OKRs, budget allocation, org changes
- Need market research, competitive analysis, financial projections
- Pre-reads distributed 2 weeks before offsite
- Offsite facilitated by external consultant
```

### 9. Board Meeting (T-90)
```
Create a workback plan for Q4 2025 Board Meeting December 15 with annual planning focus.
- 6-hour meeting with 8 board members + executive team
- Agenda: Q4 financials, 2025 review, 2026 plan, budget, governance updates
- Need audited financials, board deck (50+ slides), committee reports
- Board materials due 10 days before meeting
- Expect CFO, CEO, COO presentations
```

### 10. M&A Integration (T-90+)
```
Create a workback plan for M&A integration kickoff February 1, 2026.
- Acquiring TechCo (500 employees, $50M revenue)
- Legal close expected November 30
- Need integration plan, org structure, Day 1 plan, 100-day plan
- Workstreams: HR, IT, Finance, Product, Sales, Operations
- Integration team of 30 people across both companies
```

---

## Summary

**11 Canonical Meeting Types** covering planning horizons from **T-7 to T-90+**:

**Short-term (T-7 to T-14)**:
1. Weekly Newsletter
2. Sprint Planning

**Standard 30-Day (T-30)**:
3. Monthly Business Review
4. Product Feature Launch

**Mid-Range (T-42 to T-56)**:
5. Squad Mission Planning (6-8 week cycles)

**Standard 60-Day (T-60)**:
6. Quarterly Business Review
7. Annual Kickoff Meeting

**Long-term 90-Day (T-90+)**:
8. Major Product Launch
9. Strategic Planning Offsite
10. Board Meeting (Annual Planning)
11. M&A Integration Planning

**Key Parameters**:
- Participants: 2-30 (scales with complexity)
- Tasks: 8-100 (scales non-linearly)
- Deliverables: 2-20 (plateaus at high complexity)
- Phases: 1-10 (more phases for longer horizons)
- Approval gates: 1-10 (more gates for higher stakes)

**Next Steps**:
1. Use these 10 types for LLM evaluation testing
2. Baseline gpt-oss:120b on each type
3. Compare models (GPT-5, 120b, Claude) across the spectrum
4. Identify which meeting types are hardest for LLMs to plan

---

**Document Version**: 1.0  
**Created**: November 17, 2025  
**Next Review**: After first round of model evaluation across all 10 types
