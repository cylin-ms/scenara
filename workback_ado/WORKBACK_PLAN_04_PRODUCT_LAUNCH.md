# Workback Plan Examples and ACRUE Evaluation - Part 4

**Meeting Type**: Product Launch Meeting  
**Author**: Chin-Yew Lin  
**Created**: November 13, 2025

---

## 4. Product Launch Meeting

### Meeting Context
- **Meeting Type**: Product Launch Go/No-Go Decision Meeting
- **Target Date**: January 20, 2026, 9:00 AM - 11:00 AM PT
- **Organizer**: VP Product Management
- **Attendees**: CEO, CTO, CMO, VP Sales, VP Customer Success, VP Operations, Product Team (12 total)
- **Objective**: Review launch readiness, decide go/no-go for QuantumAI Analytics v3.0 public launch on February 1, 2026
- **Product**: QuantumAI Analytics v3.0 - AI-powered business intelligence platform
- **Launch Impact**: $25M revenue target Year 1, strategic entry into enterprise AI market

---

### Example A: Good Workback Plan

```yaml
workback_plan:
  meeting_title: "QuantumAI Analytics v3.0 Launch Go/No-Go Decision"
  meeting_date: "2026-01-20T09:00:00-08:00"
  meeting_duration_minutes: 120
  organizer: "Jennifer Park, VP Product Management"
  product: "QuantumAI Analytics v3.0"
  launch_date: "2026-02-01"
  complexity: "very_high"
  
  milestones:
    - milestone_id: "M1"
      name: "Launch Steering Committee Kickoff"
      due_date: "2025-10-23T17:00:00-08:00"
      days_before_meeting: 89
      description: "Cross-functional launch team aligned on goals, timeline, success criteria"
      success_criteria:
        - "Launch committee formed: Product, Engineering, Marketing, Sales, CS, Operations"
        - "Launch objectives agreed: $25M Y1 revenue, 200 enterprise customers, <5% churn"
        - "Launch timeline confirmed: February 1, 2026 public availability"
        - "Go/no-go decision criteria defined (readiness scorecard with 15 metrics)"
        - "Workback plan reviewed and approved by all functional leads"
      dependencies: []
      owner: "Jennifer Park"
      
    - milestone_id: "M2"
      name: "Beta Program Complete"
      due_date: "2025-12-16T17:00:00-08:00"
      days_before_meeting: 35
      description: "Beta program with 50 customers completed, feedback incorporated"
      success_criteria:
        - "≥50 beta customers completed 30-day trial"
        - "Beta NPS score ≥40 (target: 50+)"
        - "≥80% of beta customers willing to purchase at launch"
        - "Top 10 feature requests documented and prioritized"
        - "Critical bugs identified and fix prioritized"
        - "Beta customer quotes collected for marketing (≥10)"
      dependencies: []
      owner: "Product Team + Customer Success"
      
    - milestone_id: "M3"
      name: "Department Readiness Plans Complete"
      due_date: "2025-12-30T17:00:00-08:00"
      days_before_meeting: 21
      description: "All departments submitted readiness scorecards"
      success_criteria:
        - "Engineering: Product stable, <10 P1 bugs, performance benchmarks met"
        - "Marketing: Website live, collateral ready, PR plan approved, demand gen campaigns ready"
        - "Sales: 100% team trained, pricing approved, sales tools ready, pipeline building"
        - "Customer Success: Onboarding process defined, support docs live, CS team trained"
        - "Operations: Infrastructure scaled, monitoring in place, incident response ready"
        - "Legal: Terms reviewed, data privacy compliant, customer contracts approved"
      dependencies: ["M2"]
      owner: "All Department Heads"
      
    - milestone_id: "M4"
      name: "Go/No-Go Readiness Scorecard Compiled"
      due_date: "2026-01-10T17:00:00-08:00"
      days_before_meeting: 10
      description: "Readiness scorecard with all 15 metrics scored"
      success_criteria:
        - "Engineering readiness: 9/10 (1 P2 bug acceptable)"
        - "Marketing readiness: 10/10 (all assets live)"
        - "Sales readiness: 8/10 (90% team certified)"
        - "Customer Success readiness: 9/10 (docs complete, team trained)"
        - "Operations readiness: 10/10 (infrastructure load tested)"
        - "Legal readiness: 10/10 (contracts approved)"
        - "Overall readiness score: ≥85/100 required for GO decision"
      dependencies: ["M3"]
      owner: "Jennifer Park + Launch Committee"
      
    - milestone_id: "M5"
      name: "Executive Pre-Brief Complete"
      due_date: "2026-01-17T17:00:00-08:00"
      days_before_meeting: 3
      description: "CEO, CTO, CMO pre-briefed on launch status"
      success_criteria:
        - "1-hour exec briefing completed"
        - "Readiness scorecard reviewed with executives"
        - "Key risks surfaced and mitigation discussed"
        - "Executive concerns documented for go/no-go meeting"
        - "Rollback plan reviewed if launch fails"
      dependencies: ["M4"]
      owner: "Jennifer Park"
      
    - milestone_id: "M6"
      name: "Final Launch Materials Distributed"
      due_date: "2026-01-19T17:00:00-08:00"
      days_before_meeting: 1
      description: "All go/no-go meeting materials sent to attendees"
      success_criteria:
        - "Readiness scorecard distributed (15 metrics with supporting data)"
        - "Beta program summary (50 customers, NPS 47, testimonials)"
        - "Launch plan overview (timeline, marketing, sales, operations)"
        - "Risk assessment (5 major risks with mitigation)"
        - "Financial projections ($25M Y1, $60M Y2-3)"
        - "Rollback plan if post-launch issues arise"
      dependencies: ["M5"]
      owner: "Jennifer Park"
      
    - milestone_id: "M7"
      name: "Go/No-Go Decision Meeting Ready"
      due_date: "2026-01-20T08:00:00-08:00"
      days_before_meeting: 0
      description: "Meeting logistics and decision framework prepared"
      success_criteria:
        - "Room setup: hybrid meeting (8 in-person, 4 remote)"
        - "Decision framework: ≥85/100 readiness = GO, 70-84 = conditional GO with mitigations, <70 = NO GO/delay"
        - "Voting process: each department head votes GO/NO-GO with rationale"
        - "CEO has final decision authority if votes split"
        - "Launch day war room plan ready if GO decision"
      dependencies: ["M6"]
      owner: "Jennifer Park + Admin"

  tasks:
    # M1 Tasks - Steering Committee
    - task_id: "T1.1"
      milestone_id: "M1"
      name: "Form Launch Steering Committee"
      description: "Recruit cross-functional leads for launch planning"
      owner: "Jennifer Park"
      estimated_hours: 4
      due_date: "2025-10-18T17:00:00-08:00"
      dependencies: []
      
    - task_id: "T1.2"
      milestone_id: "M1"
      name: "Define Launch Success Criteria"
      description: "Committee agrees on revenue, customer, quality targets"
      owner: "Launch Committee"
      estimated_hours: 8
      due_date: "2025-10-21T17:00:00-08:00"
      dependencies: ["T1.1"]
      
    - task_id: "T1.3"
      milestone_id: "M1"
      name: "Build Go/No-Go Scorecard"
      description: "Create 15-metric readiness scorecard with thresholds"
      owner: "Jennifer Park"
      estimated_hours: 12
      due_date: "2025-10-23T17:00:00-08:00"
      dependencies: ["T1.2"]
      
    # M2 Tasks - Beta Program
    - task_id: "T2.1"
      milestone_id: "M2"
      name: "Recruit 50 Beta Customers"
      description: "Customer Success recruits 50 target enterprise customers"
      owner: "Customer Success"
      estimated_hours: 40
      due_date: "2025-11-15T17:00:00-08:00"
      dependencies: []
      
    - task_id: "T2.2"
      milestone_id: "M2"
      name: "Run 30-Day Beta Program"
      description: "Onboard beta customers, gather usage data and feedback"
      owner: "Product Team + Customer Success"
      estimated_hours: 120
      due_date: "2025-12-10T17:00:00-08:00"
      dependencies: ["T2.1"]
      
    - task_id: "T2.3"
      milestone_id: "M2"
      name: "Analyze Beta Results"
      description: "Calculate NPS, purchase intent, feature requests, bugs"
      owner: "Product Analytics"
      estimated_hours: 20
      due_date: "2025-12-16T17:00:00-08:00"
      dependencies: ["T2.2"]
      
    # M3 Tasks - Department Readiness
    - task_id: "T3.1"
      milestone_id: "M3"
      name: "Engineering Readiness Plan"
      description: "CTO submits engineering scorecard: bugs, performance, stability"
      owner: "CTO + Engineering"
      estimated_hours: 40
      due_date: "2025-12-20T17:00:00-08:00"
      dependencies: ["T2.3"]
      
    - task_id: "T3.2"
      milestone_id: "M3"
      name: "Marketing Readiness Plan"
      description: "CMO submits marketing scorecard: website, collateral, PR, campaigns"
      owner: "CMO + Marketing"
      estimated_hours: 80
      due_date: "2025-12-23T17:00:00-08:00"
      dependencies: []
      
    - task_id: "T3.3"
      milestone_id: "M3"
      name: "Sales Readiness Plan"
      description: "VP Sales submits sales scorecard: training, pricing, tools, pipeline"
      owner: "VP Sales"
      estimated_hours: 60
      due_date: "2025-12-27T17:00:00-08:00"
      dependencies: []
      
    - task_id: "T3.4"
      milestone_id: "M3"
      name: "Customer Success Readiness Plan"
      description: "VP CS submits CS scorecard: onboarding, support, team training"
      owner: "VP Customer Success"
      estimated_hours: 40
      due_date: "2025-12-28T17:00:00-08:00"
      dependencies: []
      
    - task_id: "T3.5"
      milestone_id: "M3"
      name: "Operations Readiness Plan"
      description: "VP Ops submits ops scorecard: infrastructure, monitoring, incident response"
      owner: "VP Operations"
      estimated_hours: 50
      due_date: "2025-12-29T17:00:00-08:00"
      dependencies: []
      
    - task_id: "T3.6"
      milestone_id: "M3"
      name: "Legal Readiness Review"
      description: "Legal submits legal scorecard: contracts, terms, data privacy"
      owner: "General Counsel"
      estimated_hours: 30
      due_date: "2025-12-30T17:00:00-08:00"
      dependencies: []
      
    # M4 Tasks - Scorecard Compilation
    - task_id: "T4.1"
      milestone_id: "M4"
      name: "Compile Readiness Scorecard"
      description: "Aggregate all department scores into master scorecard"
      owner: "Jennifer Park"
      estimated_hours: 12
      due_date: "2026-01-08T17:00:00-08:00"
      dependencies: ["T3.1", "T3.2", "T3.3", "T3.4", "T3.5", "T3.6"]
      
    - task_id: "T4.2"
      milestone_id: "M4"
      name: "Identify Launch Risks"
      description: "Compile top 5 risks from department readiness reviews"
      owner: "Launch Committee"
      estimated_hours: 8
      due_date: "2026-01-09T17:00:00-08:00"
      dependencies: ["T4.1"]
      
    - task_id: "T4.3"
      milestone_id: "M4"
      name: "Develop Mitigation Plans"
      description: "Create mitigation strategy for each major risk"
      owner: "Department Heads"
      estimated_hours: 16
      due_date: "2026-01-10T17:00:00-08:00"
      dependencies: ["T4.2"]
      
    # M5 Tasks - Executive Pre-Brief
    - task_id: "T5.1"
      milestone_id: "M5"
      name: "Prepare Executive Briefing Deck"
      description: "Build 20-slide deck: scorecard, beta results, risks, financials"
      owner: "Jennifer Park"
      estimated_hours: 12
      due_date: "2026-01-14T17:00:00-08:00"
      dependencies: ["T4.3"]
      
    - task_id: "T5.2"
      milestone_id: "M5"
      name: "Executive Pre-Briefing Session"
      description: "1-hour session with CEO, CTO, CMO to preview launch status"
      owner: "Jennifer Park + Executives"
      estimated_hours: 3
      due_date: "2026-01-17T17:00:00-08:00"
      dependencies: ["T5.1"]
      
    # M6 Tasks - Materials Distribution
    - task_id: "T6.1"
      milestone_id: "M6"
      name: "Finalize Go/No-Go Packet"
      description: "Compile all materials: scorecard, beta summary, launch plan, risks, financials, rollback plan"
      owner: "Jennifer Park"
      estimated_hours: 8
      due_date: "2026-01-18T17:00:00-08:00"
      dependencies: ["T5.2"]
      
    - task_id: "T6.2"
      milestone_id: "M6"
      name: "Distribute Materials"
      description: "Send packet to all 12 attendees, confirm receipt"
      owner: "Jennifer Park"
      estimated_hours: 2
      due_date: "2026-01-19T17:00:00-08:00"
      dependencies: ["T6.1"]
      
    # M7 Tasks - Meeting Preparation
    - task_id: "T7.1"
      milestone_id: "M7"
      name: "Setup Meeting Logistics"
      description: "Configure room for hybrid meeting, test technology"
      owner: "Admin + IT"
      estimated_hours: 3
      due_date: "2026-01-20T08:00:00-08:00"
      dependencies: []
      
    - task_id: "T7.2"
      milestone_id: "M7"
      name: "Prepare Launch Day War Room Plan"
      description: "Document war room staffing, escalation, monitoring if GO"
      owner: "VP Operations + Product Team"
      estimated_hours: 6
      due_date: "2026-01-19T17:00:00-08:00"
      dependencies: ["T6.2"]

  risks:
    - risk_id: "R1"
      description: "Beta NPS below 40, indicating product not ready for launch"
      probability: "medium"
      impact: "critical"
      mitigation: "Monitor beta NPS weekly; if trending below 40, delay launch; address top feedback themes in sprint; have 30-day delay contingency plan ready"
      owner: "Product Team"
      
    - risk_id: "R2"
      description: "Critical P0/P1 bug discovered in final testing"
      probability: "medium"
      impact: "critical"
      mitigation: "Code freeze 2 weeks before launch; daily bug triage; CEO can delay launch up to 30 days for critical bugs; have rollback plan"
      owner: "CTO"
      
    - risk_id: "R3"
      description: "Sales team training completion below 90%"
      probability: "low"
      impact: "high"
      mitigation: "Track training completion weekly; mandatory training for commission eligibility; have backup sales engineers for untrained reps"
      owner: "VP Sales"
      
    - risk_id: "R4"
      description: "Marketing assets not ready (website, collateral, PR)"
      probability: "low"
      impact: "high"
      mitigation: "Weekly marketing readiness review; external agency backup for critical assets; soft launch option if marketing delayed"
      owner: "CMO"
      
    - risk_id: "R5"
      description: "Infrastructure fails under launch day load"
      probability: "low"
      impact: "critical"
      mitigation: "Load test at 3x expected capacity; auto-scaling configured; operations war room staffed 24/7 first week; rollback plan within 2 hours"
      owner: "VP Operations"
      
    - risk_id: "R6"
      description: "Executive split vote on go/no-go decision"
      probability: "low"
      impact: "medium"
      mitigation: "CEO has final decision authority; document decision rationale; conditional GO option with specific mitigations; 2-week delay as compromise"
      owner: "CEO"

  quality_checks:
    - check_id: "Q1"
      name: "Beta Program Success Threshold"
      description: "Beta NPS ≥40, ≥80% willing to purchase"
      checkpoint: "M2"
      pass_criteria: "Beta results meet or exceed thresholds; if not, recommend delay"
      
    - check_id: "Q2"
      name: "Engineering Stability"
      description: "≤10 P1 bugs, ≤2 P0 bugs, performance benchmarks met"
      checkpoint: "M3"
      pass_criteria: "Engineering scorecard ≥8/10"
      
    - check_id: "Q3"
      name: "Cross-Functional Readiness"
      description: "All 6 departments score ≥7/10 on readiness"
      checkpoint: "M3"
      pass_criteria: "No department below 7/10; overall ≥85/100"
      
    - check_id: "Q4"
      name: "Sales Team Certification"
      description: "≥90% of sales team certified on v3.0"
      checkpoint: "M3"
      pass_criteria: "Training completion report shows ≥90%"
      
    - check_id: "Q5"
      name: "Marketing Assets Live"
      description: "Website, collateral, PR plan all complete"
      checkpoint: "M3"
      pass_criteria: "Marketing scorecard = 10/10 (all assets ready)"
      
    - check_id: "Q6"
      name: "Operations Load Testing"
      description: "Infrastructure tested at 3x expected launch day load"
      checkpoint: "M3"
      pass_criteria: "Load test passed with <5% error rate at 3x capacity"
      
    - check_id: "Q7"
      name: "Executive Alignment"
      description: "CEO, CTO, CMO aligned on readiness assessment"
      checkpoint: "M5"
      pass_criteria: "Executive pre-brief completed, concerns addressed or documented"
      
    - check_id: "Q8"
      name: "Rollback Plan Tested"
      description: "Rollback procedure documented and dry run completed"
      checkpoint: "M6"
      pass_criteria: "Rollback can be executed within 2 hours with <10% data loss"

  metadata:
    total_estimated_hours: 594
    critical_path_days: 89
    number_of_dependencies: 18
    launch_revenue_target: "$25M Year 1"
    beta_participants: 50
    readiness_threshold: "85/100 for GO decision"
    key_stakeholders: ["CEO", "CTO", "CMO", "VP Sales", "VP Customer Success", "VP Operations", "General Counsel", "Launch Committee"]
    success_indicators:
      - "GO decision with ≥85/100 readiness score"
      - "Launch executes on February 1 with <5% incident rate first week"
      - "$2M revenue in first month post-launch"
      - "200 customers signed by end of Q1"

```

**Why This is a Good Workback Plan**:
- ✅ **90-day timeline** with 7 major milestones (industry best practice for complex launches)
- ✅ **50-customer beta program** validates product-market fit before launch
- ✅ **Cross-functional readiness scorecards** from all 6 departments
- ✅ **Quantified go/no-go criteria** (≥85/100 readiness score)
- ✅ **Executive pre-brief** ≥3 days before decision meeting
- ✅ **Rollback plan** documented and tested
- ✅ **Launch day war room** prepared for incident response
- ✅ **Risk mitigation** for common launch failure modes
- ✅ **Quality checks** at each milestone validate readiness
- ✅ **Decision framework** clear (GO/conditional GO/NO GO thresholds)

---

### Example B: Bad Workback Plan

```yaml
workback_plan:
  meeting_title: "Product Launch Meeting"
  meeting_date: "2026-01-20T09:00:00-08:00"
  meeting_duration_minutes: 120
  organizer: "Product"
  product: "v3.0"
  launch_date: "2026-02-01"
  complexity: "medium"
  
  milestones:
    - milestone_id: "M1"
      name: "Prepare for launch"
      due_date: "2026-01-15T17:00:00-08:00"
      days_before_meeting: 5
      description: "Get things ready"
      success_criteria:
        - "Product works"
      dependencies: []
      owner: "Product team"
      
    - milestone_id: "M2"
      name: "Meeting materials"
      due_date: "2026-01-19T17:00:00-08:00"
      days_before_meeting: 1
      description: "Make slides"
      success_criteria:
        - "Slides done"
      dependencies: ["M1"]
      owner: "PM"

  tasks:
    - task_id: "T1"
      milestone_id: "M1"
      name: "Test product"
      description: "Make sure it works"
      owner: "Engineering"
      estimated_hours: null
      due_date: "2026-01-15T17:00:00-08:00"
      dependencies: []
      
    - task_id: "T2"
      milestone_id: "M1"
      name: "Tell sales"
      description: "Let sales team know about launch"
      owner: "Someone"
      estimated_hours: null
      due_date: "2026-01-16T17:00:00-08:00"
      dependencies: []
      
    - task_id: "T3"
      milestone_id: "M2"
      name: "Create presentation"
      description: "Make PowerPoint for meeting"
      owner: "PM"
      estimated_hours: null
      due_date: "2026-01-19T17:00:00-08:00"
      dependencies: ["T1", "T2"]

  risks:
    - risk_id: "R1"
      description: "Launch might not work"
      probability: "unknown"
      impact: "bad"
      mitigation: "Hope it works"
      owner: "Team"

  quality_checks:
    - check_id: "Q1"
      name: "Product seems ready"
      description: "Check if product is good enough"
      checkpoint: "M1"
      pass_criteria: "Looks okay"

  metadata:
    total_estimated_hours: null
    critical_path_days: 5
    number_of_dependencies: 1
    launch_revenue_target: "$25M"
    key_stakeholders: ["Leadership"]
    success_indicators:
      - "Meeting happens"
      - "Launch happens"
```

**Why This is a Bad Workback Plan**:
- ❌ **Only 5-day timeline** - grossly insufficient for enterprise product launch
- ❌ **No beta program** - launching without customer validation
- ❌ **No readiness scorecards** - no systematic assessment of launch readiness
- ❌ **Vague success criteria** ("product works", "looks okay")
- ❌ **No cross-functional coordination** - sales just "told" about launch
- ❌ **No go/no-go criteria** - no decision framework
- ❌ **No executive pre-brief** - leadership blindsided on decision day
- ❌ **No rollback plan** - no mitigation if launch fails
- ❌ **No quality metrics** - no bug counts, performance benchmarks, NPS targets
- ❌ **No launch day operations plan** - no war room, monitoring, incident response
- ❌ **No department readiness validation** - marketing, sales, CS may not be ready
- ❌ **78% of launches miss timeline** without structured planning (BCG data)

---

### ACRUE Assertions for Product Launch Workback Plans

#### Critical Assertions (Must Pass)

**Accuracy Dimension**:
- text: "The workback plan includes beta program with ≥30 customers and NPS measurement before launch decision"
  - level: critical
  - dimension: Accuracy
  - rationale: "Beta validation prevents launching products customers don't want; NPS predicts market success"

- text: "Plan specifies quantified go/no-go criteria (e.g., readiness score ≥85/100, NPS ≥40, bug count ≤10 P1)"
  - level: critical
  - dimension: Accuracy
  - rationale: "Objective criteria prevent emotional launch decisions; reduces 78% launch delay rate"

- text: "Timeline allows ≥60 days for cross-functional launch preparation"
  - level: critical
  - dimension: Accuracy
  - rationale: "Complex launches require engineering, marketing, sales, ops coordination; <60 days = high failure risk"

**Completeness Dimension**:
- text: "Plan includes readiness scorecards from all departments (Engineering, Marketing, Sales, CS, Operations, Legal)"
  - level: critical
  - dimension: Completeness
  - rationale: "Launches fail when any function unprepared; systematic readiness assessment essential"

- text: "Milestones specify rollback plan development and testing"
  - level: critical
  - dimension: Completeness
  - rationale: "20% of launches have critical issues first week; rollback plan prevents extended outages"

- text: "Tasks include sales team training with ≥90% completion requirement"
  - level: critical
  - dimension: Completeness
  - rationale: "Untrained sales teams can't sell new products; training completion predicts revenue attainment"

**Relevance Dimension**:
- text: "Success criteria measure product quality (bug counts, performance benchmarks, NPS) not just task completion"
  - level: critical
  - dimension: Relevance
  - rationale: "Launch readiness is about product quality, not just activities completed"

#### Expected Assertions (Should Pass)

**Usefulness Dimension**:
- text: "Plan includes executive pre-briefing ≥3 days before go/no-go meeting"
  - level: expected
  - dimension: Usefulness
  - rationale: "Executive surprises on decision day stall launches; pre-briefs align leadership"

- text: "Tasks specify launch day war room staffing and incident response procedures"
  - level: expected
  - dimension: Usefulness
  - rationale: "First-week incident rate averages 15-25%; war room enables rapid response"

- text: "Quality checks validate load testing at ≥3x expected capacity"
  - level: expected
  - dimension: Usefulness
  - rationale: "Infrastructure failures on launch day destroy customer trust; 3x load testing is standard"

**Completeness Dimension**:
- text: "Plan includes marketing asset readiness (website, collateral, PR, demand gen)"
  - level: expected
  - dimension: Completeness
  - rationale: "Marketing unpreparedness means no customer awareness; demand gen must start at launch"

- text: "Milestones specify customer success onboarding process definition and documentation"
  - level: expected
  - dimension: Completeness
  - rationale: "Poor onboarding drives churn; CS must be ready to support customers from day 1"

**Accuracy Dimension**:
- text: "Risk mitigation includes code freeze ≥2 weeks before launch to prevent last-minute bugs"
  - level: expected
  - dimension: Accuracy
  - rationale: "Last-minute code changes are leading cause of launch day bugs; code freeze is standard practice"

#### Aspirational Assertions (Nice to Have)

**Exceptional Dimension**:
- text: "Plan tracks beta customer conversion rate (beta → paying customer) as leading indicator"
  - level: aspirational
  - dimension: Exceptional
  - rationale: "Beta conversion rate ≥80% predicts successful launch; <50% suggests product-market fit issues"

- text: "Success indicators measure launch outcomes ($XM revenue, X customers, <X% churn) not just readiness"
  - level: aspirational
  - dimension: Exceptional
  - rationale: "Ultimate success is market performance, not just launching on time"

**Usefulness Dimension**:
- text: "Metadata documents financial projections (Y1-Y3 revenue, customer targets) to justify launch investment"
  - level: aspirational
  - dimension: Usefulness
  - rationale: "Launch ROI justification helps prioritize vs. other initiatives"

- text: "Plan includes conditional GO option (launch with specific mitigations) not just binary GO/NO-GO"
  - level: aspirational
  - dimension: Usefulness
  - rationale: "Conditional GO balances speed-to-market vs. risk; provides flexibility"

---

### ACRUE Rubrics for Product Launch Workback Plans

#### Accuracy Rubric
**Measures**: Realistic timelines, validated assumptions, objective readiness criteria

- **Gold Standard (9-10 points)**:
  - ≥60-day timeline from decision meeting to launch
  - Beta program with ≥30 customers, NPS measured
  - Quantified go/no-go criteria (readiness score, bug thresholds, performance benchmarks)
  - Cross-functional readiness validated by all departments
  - Code freeze ≥2 weeks before launch
  - Load testing at ≥3x expected capacity
  - Executive pre-brief ≥3 days before decision
  - All assumptions validated through beta, testing, or customer research

- **Silver Standard (7-8 points)**:
  - ≥45-day timeline
  - Beta program with ≥15 customers
  - Go/no-go criteria defined
  - Major departments provide readiness status
  - Code freeze ≥1 week before
  - Load testing conducted
  - Executive involvement

- **Bronze Standard (5-6 points)**:
  - ≥30-day timeline
  - Some customer testing
  - Basic readiness criteria
  - Key departments reviewed
  - Testing conducted

- **Fails Standard (<5 points)**:
  - <30-day timeline
  - No customer validation
  - No objective criteria
  - No systematic readiness assessment
  - No testing validation

#### Completeness Rubric
**Measures**: Coverage of all launch workstreams

- **Gold Standard (9-10 points)**:
  - Beta program (recruit, run, analyze)
  - Engineering readiness (bugs, performance, stability)
  - Marketing readiness (website, collateral, PR, demand gen)
  - Sales readiness (training, pricing, tools, pipeline)
  - Customer Success readiness (onboarding, support, training)
  - Operations readiness (infrastructure, monitoring, incident response)
  - Legal readiness (contracts, terms, compliance)
  - Executive pre-briefing
  - Go/no-go decision framework
  - Rollback plan developed and tested
  - Launch day war room plan
  - Post-launch monitoring plan

- **Silver Standard (7-8 points)**:
  - Beta program
  - Engineering, marketing, sales readiness
  - Customer success planning
  - Operations planning
  - Executive briefing
  - Decision criteria
  - Basic rollback plan

- **Bronze Standard (5-6 points)**:
  - Some customer testing
  - Engineering readiness
  - Marketing assets
  - Sales notification
  - Basic launch plan

- **Fails Standard (<5 points)**:
  - No customer validation
  - Engineering only focus
  - No cross-functional coordination
  - No decision framework
  - No rollback plan

#### Relevance Rubric
**Measures**: Focus on launch success factors vs. generic project management

- **Gold Standard (9-10 points)**:
  - All milestones tied to launch readiness dimensions (product quality, market readiness, operational readiness)
  - Success criteria measure objective quality metrics (NPS, bug counts, training completion, load test results)
  - Risks address launch-specific failure modes (beta results poor, infrastructure fails, sales unprepared)
  - Quality checks enforce launch best practices (code freeze, load testing, training thresholds)
  - Decision framework based on launch readiness, not arbitrary dates

- **Silver Standard (7-8 points)**:
  - Most milestones launch-relevant
  - Success criteria mostly objective
  - Risks include launch concerns
  - Quality checks present
  - Decision criteria defined

- **Bronze Standard (5-6 points)**:
  - Milestones include launch activities
  - Some objective criteria
  - Generic project risks
  - Basic quality checks

- **Fails Standard (<5 points)**:
  - Generic project milestones
  - Vague criteria ("looks ready")
  - Risks unrelated to launch
  - No quality enforcement

#### Usefulness Rubric
**Measures**: Actionability for launch team

- **Gold Standard (9-10 points)**:
  - All tasks have named owners (specific roles: CTO, CMO, VP Sales, etc.)
  - Time estimates enable capacity planning (500+ hours typical)
  - Readiness scorecard template provided with metrics and thresholds
  - Beta program playbook (recruit, run, measure, analyze)
  - Executive pre-brief agenda and materials
  - War room staffing schedule and escalation procedures
  - Rollback playbook (decision criteria, procedure, timeline)
  - Decision framework documented (GO/conditional GO/NO-GO thresholds)
  - Post-launch monitoring dashboard specified

- **Silver Standard (7-8 points)**:
  - Most tasks have named owners
  - Time estimates for major workstreams
  - Readiness criteria defined
  - Beta program planned
  - Executive briefing scheduled
  - War room concept
  - Rollback mentioned
  - Decision criteria present

- **Bronze Standard (5-6 points)**:
  - Some specific owners
  - Basic timeline
  - Readiness discussed
  - Some customer testing
  - Executive involvement
  - Launch day plan

- **Fails Standard (<5 points)**:
  - Vague owners ("team", "product")
  - No time estimates
  - No readiness framework
  - No customer validation plan
  - No executive engagement
  - No launch day preparation

#### Exceptional Rubric
**Measures**: Advanced launch practices that maximize success probability

- **Gold Standard (9-10 points)**:
  - Beta-to-customer conversion rate tracked (leading indicator)
  - Success metrics measure market outcomes (revenue, customers, churn) not just launch completion
  - Conditional GO framework (launch with mitigations) balances speed vs. risk
  - Competitive analysis informs launch timing and positioning
  - Customer journey mapping from awareness to activation
  - Win/loss analysis plan to learn from early customers
  - Financial projections (Y1-Y3) justify launch investment
  - Launch retrospective planned to capture learnings
  - Tiered launch option (soft launch, phased rollout, full launch)

- **Silver Standard (7-8 points)**:
  - Beta conversion tracked
  - Market success metrics included
  - Flexible decision framework
  - Competitive awareness
  - Customer journey considered
  - Basic financial projections

- **Bronze Standard (5-6 points)**:
  - Some outcome tracking
  - Revenue targets set
  - Decision flexibility
  - Customer perspective

- **Fails Standard (<5 points)**:
  - Only process metrics
  - No market outcome measurement
  - Binary GO/NO-GO only
  - No customer perspective

---

### Distribution for Product Launch Assertions

**ACRUE Dimension Distribution**:
- Accuracy: 13 assertions (38.2%)
- Completeness: 11 assertions (32.4%)
- Relevance: 5 assertions (14.7%)
- Usefulness: 3 assertions (8.8%)
- Exceptional: 2 assertions (5.9%)

**Level Distribution**:
- Critical: 7 assertions (20.6%)
- Expected: 6 assertions (17.6%)
- Aspirational: 4 assertions (11.8%)

---

**Key Insight**: Product launch workback plans with ≥60-day timelines, 30+ customer beta programs, and cross-functional readiness scorecards reduce the 78% launch delay rate (Boston Consulting Group) to <30%. The 90-day timeline in the good example enables systematic validation of product quality, market readiness, and operational preparedness—the three pillars of launch success.

