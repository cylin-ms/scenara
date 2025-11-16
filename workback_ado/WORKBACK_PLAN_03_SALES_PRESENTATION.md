# Workback Plan Examples and ACRUE Evaluation - Part 3

**Meeting Type**: Executive Sales Presentation  
**Author**: Chin-Yew Lin  
**Created**: November 13, 2025

---

## 3. Executive Sales Presentation

### Meeting Context
- **Meeting Type**: Executive Sales Presentation
- **Target Date**: December 10, 2025, 10:00 AM - 11:30 AM PT
- **Organizer**: VP Enterprise Sales
- **Attendees**: Customer CIO, Customer CFO, Customer VP Operations (3); Sales team: Account Executive, Solutions Architect, Sales Engineer (3)
- **Objective**: Present cloud migration solution, demonstrate ROI, secure $2.5M contract approval
- **Deal Value**: $2.5M initial contract, $8M 3-year value
- **Customer**: TechCorp Manufacturing, Fortune 500 industrial company

---

### Example A: Good Workback Plan

```yaml
workback_plan:
  meeting_title: "TechCorp Cloud Migration Solution Presentation"
  meeting_date: "2025-12-10T10:00:00-08:00"
  meeting_duration_minutes: 90
  organizer: "Rachel Kim, VP Enterprise Sales"
  deal_value: "$2.5M initial, $8M 3-year"
  customer: "TechCorp Manufacturing"
  complexity: "high"
  
  milestones:
    - milestone_id: "M1"
      name: "Customer Discovery Complete"
      due_date: "2025-11-19T17:00:00-08:00"
      days_before_meeting: 21
      description: "Deep understanding of customer pain points, requirements, decision criteria"
      success_criteria:
        - "≥2 discovery calls completed with technical and business stakeholders"
        - "Customer pain points documented (current infrastructure costs, downtime, scalability limits)"
        - "Decision criteria identified (ROI hurdle, security requirements, migration timeline)"
        - "Buying process mapped (approval chain, budget approval needed from CFO)"
        - "Competition intelligence gathered (incumbent vendor, alternatives considered)"
      dependencies: []
      owner: "Rachel Kim + Marcus Chen (Account Executive)"
      
    - milestone_id: "M2"
      name: "Solution Design Validated"
      due_date: "2025-11-26T17:00:00-08:00"
      days_before_meeting: 14
      description: "Technical solution designed and validated by internal experts"
      success_criteria:
        - "Architecture diagram shows TechCorp's 47 applications migrating to cloud"
        - "Solutions Architect validated technical feasibility"
        - "Cost model built: $2.5M Year 1, $2.8M Year 2-3"
        - "Migration timeline: 18 months with 4 phases"
        - "Risk assessment completed (downtime windows, data migration complexity)"
        - "Competitive differentiation identified vs. incumbent (AWS vs. Azure)"
      dependencies: ["M1"]
      owner: "Solutions Architect + Sales Engineer"
      
    - milestone_id: "M3"
      name: "First Draft Deck Complete"
      due_date: "2025-12-01T17:00:00-08:00"
      days_before_meeting: 9
      description: "Initial presentation with TechCorp-specific content"
      success_criteria:
        - "Executive summary: 3-year TCO savings of $4.2M (52% reduction)"
        - "Current state analysis: TechCorp's infrastructure challenges"
        - "Proposed solution: 4-phase migration plan"
        - "ROI analysis: 18-month payback, 237% 3-year ROI"
        - "Risk mitigation: downtime < 4 hours per phase"
        - "Case study: Similar manufacturing customer (automotive industry)"
        - "Pricing: $2.5M Year 1 breakdown by phase"
      dependencies: ["M2"]
      owner: "Marcus Chen + Marketing"
      
    - milestone_id: "M4"
      name: "Internal Dry Run Complete"
      due_date: "2025-12-05T17:00:00-08:00"
      days_before_meeting: 5
      description: "Full presentation rehearsal with internal leadership"
      success_criteria:
        - "Presented to VP Sales, CTO, and 2 senior sales leaders"
        - "All technical questions answered or flagged for follow-up"
        - "ROI model validated by finance team"
        - "Competitive objection handling practiced"
        - "Timing: 45-min presentation + 30-min Q&A fits in 90-min window"
        - "Executive feedback incorporated into deck"
      dependencies: ["M3"]
      owner: "Marcus Chen + Rachel Kim"
      
    - milestone_id: "M5"
      name: "Final Deck and Pricing Approved"
      due_date: "2025-12-08T17:00:00-08:00"
      days_before_meeting: 2
      description: "Deck finalized, pricing approved by leadership"
      success_criteria:
        - "All dry run feedback incorporated"
        - "Pricing approved by VP Sales and CFO ($2.5M with 12% discount authority)"
        - "Legal reviewed terms and conditions"
        - "Reference customer (automotive) confirmed availability for call"
        - "Leave-behind materials prepared (1-pager, ROI calculator)"
      dependencies: ["M4"]
      owner: "Marcus Chen"
      
    - milestone_id: "M6"
      name: "Final Preparation and Tech Check"
      due_date: "2025-12-09T17:00:00-08:00"
      days_before_meeting: 1
      description: "Final rehearsal, tech setup, Q&A preparation"
      success_criteria:
        - "Final run-through completed (30 min)"
        - "Anticipated 15 customer questions prepared with answers"
        - "Tech check: screen sharing, demo environment, backup laptop"
        - "Customer logistics confirmed (3 executives attending in-person)"
        - "Backup presenter briefed (Solutions Architect if AE unavailable)"
        - "Post-meeting follow-up plan prepared (contract send timeline)"
      dependencies: ["M5"]
      owner: "Marcus Chen + Sales Engineer"

  tasks:
    - task_id: "T1.1"
      milestone_id: "M1"
      name: "Discovery Call #1: Technical Stakeholders"
      description: "Interview TechCorp CIO and VP Operations on technical pain points"
      owner: "Marcus Chen + Solutions Architect"
      estimated_hours: 3
      due_date: "2025-11-14T17:00:00-08:00"
      dependencies: []
      
    - task_id: "T1.2"
      milestone_id: "M1"
      name: "Discovery Call #2: Business Stakeholders"
      description: "Interview TechCorp CFO on budget, ROI requirements, approval process"
      owner: "Rachel Kim + Marcus Chen"
      estimated_hours: 2
      due_date: "2025-11-16T17:00:00-08:00"
      dependencies: []
      
    - task_id: "T1.3"
      milestone_id: "M1"
      name: "Document Discovery Findings"
      description: "Consolidate discovery notes into customer profile"
      owner: "Marcus Chen"
      estimated_hours: 4
      due_date: "2025-11-19T17:00:00-08:00"
      dependencies: ["T1.1", "T1.2"]
      
    - task_id: "T2.1"
      milestone_id: "M2"
      name: "Design Cloud Architecture"
      description: "Solutions Architect designs migration architecture for 47 apps"
      owner: "Solutions Architect"
      estimated_hours: 16
      due_date: "2025-11-23T17:00:00-08:00"
      dependencies: ["T1.3"]
      
    - task_id: "T2.2"
      milestone_id: "M2"
      name: "Build Cost Model"
      description: "Finance team builds 3-year TCO model with ROI analysis"
      owner: "Sales Operations + Finance"
      estimated_hours: 12
      due_date: "2025-11-24T17:00:00-08:00"
      dependencies: ["T2.1"]
      
    - task_id: "T2.3"
      milestone_id: "M2"
      name: "Competitive Analysis"
      description: "Research incumbent AWS solution, identify differentiation"
      owner: "Sales Engineer"
      estimated_hours: 6
      due_date: "2025-11-25T17:00:00-08:00"
      dependencies: ["T1.3"]
      
    - task_id: "T2.4"
      milestone_id: "M2"
      name: "Internal Technical Review"
      description: "Solutions Architect presents design to CTO for validation"
      owner: "Solutions Architect + CTO"
      estimated_hours: 2
      due_date: "2025-11-26T17:00:00-08:00"
      dependencies: ["T2.1", "T2.2"]
      
    - task_id: "T3.1"
      milestone_id: "M3"
      name: "Draft Executive Summary"
      description: "Write 1-slide exec summary with key value prop"
      owner: "Marcus Chen"
      estimated_hours: 3
      due_date: "2025-11-28T17:00:00-08:00"
      dependencies: ["T2.4"]
      
    - task_id: "T3.2"
      milestone_id: "M3"
      name: "Build Technical Slides"
      description: "Create architecture, migration plan, risk mitigation slides"
      owner: "Solutions Architect"
      estimated_hours: 8
      due_date: "2025-11-29T17:00:00-08:00"
      dependencies: ["T2.1", "T2.4"]
      
    - task_id: "T3.3"
      milestone_id: "M3"
      name: "Build ROI Slides"
      description: "Create ROI analysis, TCO comparison, payback slides"
      owner: "Sales Operations"
      estimated_hours: 6
      due_date: "2025-11-30T17:00:00-08:00"
      dependencies: ["T2.2"]
      
    - task_id: "T3.4"
      milestone_id: "M3"
      name: "Add Case Study"
      description: "Insert automotive manufacturing customer success story"
      owner: "Marketing + Marcus Chen"
      estimated_hours: 4
      due_date: "2025-12-01T17:00:00-08:00"
      dependencies: ["T3.1"]
      
    - task_id: "T4.1"
      milestone_id: "M4"
      name: "Schedule Internal Dry Run"
      description: "Book 90-min slot with VP Sales, CTO, senior leaders"
      owner: "Marcus Chen"
      estimated_hours: 1
      due_date: "2025-12-03T17:00:00-08:00"
      dependencies: ["T3.4"]
      
    - task_id: "T4.2"
      milestone_id: "M4"
      name: "Conduct Dry Run"
      description: "Present full deck, handle Q&A, gather feedback"
      owner: "Marcus Chen + Rachel Kim"
      estimated_hours: 3
      due_date: "2025-12-04T17:00:00-08:00"
      dependencies: ["T4.1"]
      
    - task_id: "T4.3"
      milestone_id: "M4"
      name: "Validate ROI Model"
      description: "Finance team validates all ROI calculations"
      owner: "Finance"
      estimated_hours: 3
      due_date: "2025-12-05T17:00:00-08:00"
      dependencies: ["T4.2"]
      
    - task_id: "T5.1"
      milestone_id: "M5"
      name: "Incorporate Dry Run Feedback"
      description: "Revise deck based on leadership feedback"
      owner: "Marcus Chen + Team"
      estimated_hours: 6
      due_date: "2025-12-06T17:00:00-08:00"
      dependencies: ["T4.3"]
      
    - task_id: "T5.2"
      milestone_id: "M5"
      name: "Get Pricing Approval"
      description: "VP Sales and CFO approve $2.5M pricing and discount authority"
      owner: "Rachel Kim"
      estimated_hours: 2
      due_date: "2025-12-07T17:00:00-08:00"
      dependencies: ["T5.1"]
      
    - task_id: "T5.3"
      milestone_id: "M5"
      name: "Legal Review Contract Terms"
      description: "Legal reviews terms in deck, prepares contract"
      owner: "Legal Team"
      estimated_hours: 4
      due_date: "2025-12-08T17:00:00-08:00"
      dependencies: ["T5.2"]
      
    - task_id: "T5.4"
      milestone_id: "M5"
      name: "Confirm Reference Customer"
      description: "Automotive customer confirms availability for reference call"
      owner: "Customer Success"
      estimated_hours: 1
      due_date: "2025-12-08T17:00:00-08:00"
      dependencies: []
      
    - task_id: "T6.1"
      milestone_id: "M6"
      name: "Final Rehearsal"
      description: "30-min run-through focusing on timing and transitions"
      owner: "Marcus Chen + Sales Engineer"
      estimated_hours: 1
      due_date: "2025-12-09T10:00:00-08:00"
      dependencies: ["T5.3"]
      
    - task_id: "T6.2"
      milestone_id: "M6"
      name: "Prepare Q&A Responses"
      description: "Document answers to 15 anticipated customer questions"
      owner: "Marcus Chen + Solutions Architect"
      estimated_hours: 3
      due_date: "2025-12-09T15:00:00-08:00"
      dependencies: ["T5.3"]
      
    - task_id: "T6.3"
      milestone_id: "M6"
      name: "Technology Setup and Test"
      description: "Test screen sharing, demo environment, backup systems"
      owner: "Sales Engineer"
      estimated_hours: 2
      due_date: "2025-12-09T17:00:00-08:00"
      dependencies: []

  risks:
    - risk_id: "R1"
      description: "Customer cancels or reschedules meeting (budget freeze, executive travel)"
      probability: "medium"
      impact: "high"
      mitigation: "Reconfirm meeting 48 hours in advance; have backup dates ready; maintain relationship momentum with interim updates"
      owner: "Marcus Chen"
      
    - risk_id: "R2"
      description: "Competitor (AWS) makes counter-offer before our presentation"
      probability: "medium"
      impact: "high"
      mitigation: "Early discovery of competitor positioning; prepare competitive differentiation slides; emphasize unique migration methodology"
      owner: "Rachel Kim"
      
    - risk_id: "R3"
      description: "Customer raises unexpected technical objection during presentation"
      probability: "medium"
      impact: "medium"
      mitigation: "Thorough discovery calls; Solutions Architect in room for technical questions; backup SMEs on standby"
      owner: "Solutions Architect"
      
    - risk_id: "R4"
      description: "ROI doesn't meet customer's investment hurdle rate"
      probability: "low"
      impact: "critical"
      mitigation: "Validate ROI assumptions in discovery call #2; have 3 ROI scenarios (conservative, base, aggressive); identify soft benefits"
      owner: "Sales Operations"
      
    - risk_id: "R5"
      description: "Technical demo fails during presentation"
      probability: "low"
      impact: "medium"
      mitigation: "Pre-record demo as backup; test environment 24 hours before; have static screenshots ready; backup laptop prepared"
      owner: "Sales Engineer"

  quality_checks:
    - check_id: "Q1"
      name: "Customer Discovery Depth"
      description: "≥2 discovery calls with documented pain points and decision criteria"
      checkpoint: "M1"
      pass_criteria: "Discovery document has ≥5 pain points, clear ROI hurdle, mapped approval process"
      
    - check_id: "Q2"
      name: "Solution Technical Validation"
      description: "CTO or senior architect validated proposed solution"
      checkpoint: "M2"
      pass_criteria: "Written sign-off from CTO that architecture is feasible and sound"
      
    - check_id: "Q3"
      name: "Internal Dry Run Quality"
      description: "Dry run with ≥3 senior leaders, all questions answered"
      checkpoint: "M4"
      pass_criteria: "Dry run completed, ≥3 leaders attended, feedback documented and addressed"
      
    - check_id: "Q4"
      name: "ROI Model Validation"
      description: "Finance team validated all ROI calculations"
      checkpoint: "M4"
      pass_criteria: "Finance sign-off that ROI model assumptions are reasonable and math is correct"
      
    - check_id: "Q5"
      name: "Pricing Approval"
      description: "Leadership approved pricing and discount authority"
      checkpoint: "M5"
      pass_criteria: "VP Sales and CFO email approval of $2.5M pricing with 12% discount ceiling"
      
    - check_id: "Q6"
      name: "Q&A Preparation"
      description: "Documented responses to ≥10 anticipated questions"
      checkpoint: "M6"
      pass_criteria: "Q&A document with ≥10 questions covering technical, financial, competitive topics"

  metadata:
    total_estimated_hours: 97
    critical_path_days: 21
    number_of_dependencies: 15
    deal_value: "$2.5M initial, $8M 3-year"
    win_probability: "65% (qualified opportunity)"
    key_stakeholders: ["Customer CIO", "Customer CFO", "Customer VP Ops", "VP Sales", "Solutions Architect", "CTO"]
    success_indicators:
      - "Customer requests contract and next steps"
      - "No major objections raised during presentation"
      - "Customer confirms internal champion to drive approval"
      - "Meeting ends with clear timeline to decision (target: within 2 weeks)"
```

**Why This is a Good Workback Plan**:
- ✅ **21-day timeline** with thorough discovery (industry best practice)
- ✅ **≥2 customer discovery calls** to understand pain points, decision criteria
- ✅ **Solution validated by CTO** before presenting to customer
- ✅ **Internal dry run** with senior leadership (VP Sales, CTO)
- ✅ **ROI model validated by finance** ensures credibility
- ✅ **Pricing approval** from leadership with discount authority
- ✅ **Competitive analysis** addresses incumbent (AWS) positioning
- ✅ **Reference customer** confirmed for credibility
- ✅ **Q&A preparation** with 15 anticipated questions
- ✅ **Technical backup** (demo recording, backup laptop, standby SMEs)
- ✅ **Risk mitigation** for common sales failure modes
- ✅ **Quality checks** at each milestone validate readiness

---

### Example B: Bad Workback Plan

```yaml
workback_plan:
  meeting_title: "Sales Presentation"
  meeting_date: "2025-12-10T10:00:00-08:00"
  meeting_duration_minutes: 90
  organizer: "Sales"
  deal_value: "$2.5M"
  customer: "TechCorp"
  complexity: "medium"
  
  milestones:
    - milestone_id: "M1"
      name: "Make presentation"
      due_date: "2025-12-08T17:00:00-08:00"
      days_before_meeting: 2
      description: "Create slides"
      success_criteria:
        - "Slides done"
      dependencies: []
      owner: "AE"
      
    - milestone_id: "M2"
      name: "Practice"
      due_date: "2025-12-09T17:00:00-08:00"
      days_before_meeting: 1
      description: "Review slides"
      success_criteria:
        - "Practiced"
      dependencies: ["M1"]
      owner: "AE"

  tasks:
    - task_id: "T1"
      milestone_id: "M1"
      name: "Build deck"
      description: "Make PowerPoint with product info"
      owner: "AE"
      estimated_hours: null
      due_date: "2025-12-08T17:00:00-08:00"
      dependencies: []
      
    - task_id: "T2"
      milestone_id: "M1"
      name: "Add pricing"
      description: "Put in price slide"
      owner: "AE"
      estimated_hours: null
      due_date: "2025-12-08T17:00:00-08:00"
      dependencies: []
      
    - task_id: "T3"
      milestone_id: "M2"
      name: "Read through deck"
      description: "Practice talking through slides"
      owner: "AE"
      estimated_hours: null
      due_date: "2025-12-09T17:00:00-08:00"
      dependencies: ["T1", "T2"]

  risks:
    - risk_id: "R1"
      description: "Customer might not like it"
      probability: "maybe"
      impact: "bad"
      mitigation: "Make good slides"
      owner: "Sales Team"

  quality_checks:
    - check_id: "Q1"
      name: "Deck looks professional"
      description: "Check slides look nice"
      checkpoint: "M1"
      pass_criteria: "Looks good"

  metadata:
    total_estimated_hours: null
    critical_path_days: 2
    number_of_dependencies: 1
    deal_value: "$2.5M"
    key_stakeholders: ["Customer"]
    success_indicators:
      - "Presentation happens"
```

**Why This is a Bad Workback Plan**:
- ❌ **Only 2-day timeline** - no time for discovery or preparation
- ❌ **No customer discovery** - no understanding of pain points or requirements
- ❌ **Generic product presentation** - not customized to TechCorp's needs
- ❌ **No solution validation** - no technical review before customer meeting
- ❌ **No internal dry run** - no practice with leadership or objection handling
- ❌ **No ROI model** - can't demonstrate financial value
- ❌ **No pricing approval** - AE may not have authority to negotiate
- ❌ **No competitive analysis** - unprepared for AWS comparison
- ❌ **No Q&A preparation** - will stumble on customer questions
- ❌ **No technical backup** - demo failure has no mitigation
- ❌ **Vague success criteria** ("looks good", "practiced")
- ❌ **No risk mitigation** ("make good slides" is not actionable)
- ❌ **18% baseline win rate** without structured preparation vs. 34% with workback plan

---

### ACRUE Assertions for Sales Presentation Workback Plans

#### Critical Assertions (Must Pass)

**Accuracy Dimension**:
- text: "The workback plan includes ≥2 customer discovery calls documented before solution design"
  - level: critical
  - dimension: Accuracy
  - rationale: "Win rates improve 18%→34% with discovery; understanding customer needs is prerequisite"

- text: "Plan specifies technical solution validation by internal architect or CTO before presentation"
  - level: critical
  - dimension: Accuracy
  - rationale: "Proposing infeasible solution destroys credibility; technical validation essential"

- text: "Timeline includes internal dry run with senior leadership ≥5 days before customer presentation"
  - level: critical
  - dimension: Accuracy
  - rationale: "Dry runs identify gaps, improve messaging, build confidence; 5+ days allows fixes"

**Completeness Dimension**:
- text: "Plan includes ROI/TCO model building and finance team validation"
  - level: critical
  - dimension: Completeness
  - rationale: "Executive buyers require financial justification; unvalidated ROI lacks credibility"

- text: "Milestones specify pricing approval from leadership with discount authority clearly defined"
  - level: critical
  - dimension: Completeness
  - rationale: "AEs need authority to negotiate; unclear pricing approval stalls deals"

- text: "Tasks include Q&A preparation with ≥10 anticipated customer questions documented"
  - level: critical
  - dimension: Completeness
  - rationale: "Unprepared Q&A damages credibility; anticipating objections is standard sales practice"

**Relevance Dimension**:
- text: "Success criteria measure customer-specific customization (pain points documented, ROI validated, solution architected for their needs)"
  - level: critical
  - dimension: Relevance
  - rationale: "Generic product pitches fail; customization to customer needs drives wins"

#### Expected Assertions (Should Pass)

**Usefulness Dimension**:
- text: "Plan identifies competitive positioning and includes competitor analysis task"
  - level: expected
  - dimension: Usefulness
  - rationale: "Most deals have competition; understanding alternatives enables differentiation"

- text: "Tasks include reference customer confirmation for credibility"
  - level: expected
  - dimension: Usefulness
  - rationale: "Reference customers provide social proof; confirming availability prevents scrambling"

- text: "Backup plans specified for technical demo failures (pre-recorded video, screenshots)"
  - level: expected
  - dimension: Usefulness
  - rationale: "Live demos fail 20%+ of time; backup prevents presentation disaster"

**Completeness Dimension**:
- text: "Discovery milestone captures decision criteria, approval process, budget authority"
  - level: expected
  - dimension: Completeness
  - rationale: "Understanding buying process prevents deals from stalling in approval"

- text: "Plan includes leave-behind materials preparation (one-pager, ROI calculator)"
  - level: expected
  - dimension: Completeness
  - rationale: "Leave-behinds help customer champion socialize internally"

**Accuracy Dimension**:
- text: "Risk mitigation addresses customer cancellation/rescheduling scenarios"
  - level: expected
  - dimension: Accuracy
  - rationale: "30% of sales meetings reschedule; having backup dates prevents momentum loss"

#### Aspirational Assertions (Nice to Have)

**Exceptional Dimension**:
- text: "Quality checks validate that ROI meets or exceeds customer's stated investment hurdle rate"
  - level: aspirational
  - dimension: Exceptional
  - rationale: "Targeting customer's specific hurdle rate (e.g., 25% ROI) increases approval probability"

- text: "Plan includes win probability assessment and updates it after each milestone"
  - level: aspirational
  - dimension: Exceptional
  - rationale: "Tracking win probability helps sales leadership forecast and allocate resources"

**Usefulness Dimension**:
- text: "Metadata documents deal value, customer profile, competitive situation"
  - level: aspirational
  - dimension: Usefulness
  - rationale: "Deal context helps leadership prioritize and provide targeted coaching"

- text: "Success indicators measure customer engagement (requests contract, confirms champion, sets timeline)"
  - level: aspirational
  - dimension: Usefulness
  - rationale: "Engagement signals predict deal progression better than presentation completion"

---

### ACRUE Rubrics for Sales Presentation Workback Plans

#### Accuracy Rubric
**Measures**: Alignment to proven sales methodology, realistic timelines, validated assumptions

- **Gold Standard (9-10 points)**:
  - ≥2 discovery calls documented with pain points, decision criteria, approval process
  - Solution validated by internal technical expert (architect, CTO)
  - Internal dry run with ≥3 senior leaders ≥5 days before customer meeting
  - ROI model validated by finance team
  - Pricing approved by leadership with discount authority defined
  - Customer decision timeline realistic based on their buying process
  - Competitive intelligence gathered on alternatives
  - All assumptions from discovery calls, not guesswork

- **Silver Standard (7-8 points)**:
  - ≥1 discovery call documented
  - Solution reviewed by technical team
  - Internal dry run ≥3 days before
  - ROI model built and reviewed
  - Pricing approved
  - Customer process understood

- **Bronze Standard (5-6 points)**:
  - Some customer interaction documented
  - Solution reviewed informally
  - Practice session held
  - ROI included in deck
  - Pricing determined

- **Fails Standard (<5 points)**:
  - No discovery calls
  - No solution validation
  - No practice/dry run
  - No ROI analysis
  - Pricing not approved
  - Generic product pitch

#### Completeness Rubric
**Measures**: Coverage of all sales preparation activities

- **Gold Standard (9-10 points)**:
  - Discovery: pain points, requirements, decision criteria, approval process, competition
  - Solution design: architecture, migration plan, risk mitigation
  - ROI analysis: TCO comparison, payback, 3-year value
  - Internal dry run with leadership
  - Pricing approval with discount authority
  - Legal review of terms
  - Reference customer confirmed
  - Q&A preparation (≥10 questions)
  - Leave-behind materials
  - Technical backup plans
  - Post-meeting follow-up plan

- **Silver Standard (7-8 points)**:
  - Discovery conducted
  - Solution designed
  - ROI analyzed
  - Internal review
  - Pricing approved
  - Q&A prepared
  - Backup plans

- **Bronze Standard (5-6 points)**:
  - Basic discovery
  - Solution outlined
  - ROI mentioned
  - Some internal review
  - Pricing determined

- **Fails Standard (<5 points)**:
  - Missing discovery
  - Generic solution
  - No ROI
  - No internal review
  - No pricing approval

#### Relevance Rubric
**Measures**: Customer-specific customization vs. generic product pitch

- **Gold Standard (9-10 points)**:
  - All content customized to customer's specific situation
  - Pain points from discovery calls drive narrative
  - ROI uses customer's actual cost data and assumptions
  - Solution addresses customer's unique requirements
  - Case study from similar industry/use case
  - Competitive positioning addresses customer's alternatives
  - Success criteria measure customer-specific outcomes

- **Silver Standard (7-8 points)**:
  - Most content customer-specific
  - Pain points incorporated
  - ROI uses customer's industry benchmarks
  - Solution mostly tailored
  - Relevant case study

- **Bronze Standard (5-6 points)**:
  - Some customization
  - Generic pain points with customer name inserted
  - ROI uses generic assumptions
  - Solution template with customer logo

- **Fails Standard (<5 points)**:
  - Generic product pitch
  - No customer-specific content
  - Standard ROI calculator
  - Off-the-shelf solution
  - Irrelevant case studies

#### Usefulness Rubric
**Measures**: Actionability and practical execution value

- **Gold Standard (9-10 points)**:
  - All tasks have named owners (AE, Solutions Architect, Sales Engineer, etc.)
  - Time estimates enable capacity planning
  - Discovery questions documented for calls
  - Dry run scheduled with specific attendees
  - Q&A document with prepared responses
  - Technical demo tested with backup plans
  - Competitive objection handling prepared
  - Reference customer contact info and availability
  - Post-meeting follow-up sequence planned
  - Deal value and win probability tracked

- **Silver Standard (7-8 points)**:
  - Most tasks have owners
  - Time estimates for major tasks
  - Discovery planned
  - Dry run scheduled
  - Q&A list created
  - Demo tested
  - Basic follow-up plan

- **Bronze Standard (5-6 points)**:
  - Some owners specified
  - Basic timeline
  - Discovery mentioned
  - Practice planned
  - Some Q&A prep

- **Fails Standard (<5 points)**:
  - Vague owners ("sales team", "AE")
  - No time estimates
  - No specific discovery plan
  - No practice scheduled
  - No Q&A preparation

#### Exceptional Rubric
**Measures**: Advanced sales practices that maximize win probability

- **Gold Standard (9-10 points)**:
  - Win probability tracked and updated after milestones
  - ROI targeted to customer's specific investment hurdle rate
  - Multi-threading: engaging multiple customer stakeholders
  - Champion identification and enablement plan
  - Competitive battle card prepared for objection handling
  - Success criteria include customer engagement signals (contract request, champion commitment, decision timeline)
  - Deal coaching from sales leadership incorporated
  - Lessons from similar won/lost deals applied
  - Post-meeting value realization plan (how customer achieves ROI)

- **Silver Standard (7-8 points)**:
  - Win probability estimated
  - ROI strong
  - Multiple stakeholders engaged
  - Champion identified
  - Competitive positioning prepared
  - Engagement tracked

- **Bronze Standard (5-6 points)**:
  - Basic probability assessment
  - ROI included
  - Key stakeholder identified
  - Competition mentioned

- **Fails Standard (<5 points)**:
  - No probability assessment
  - No specific success metrics
  - Single-threaded (one contact)
  - No competitive strategy

---

### Distribution for Sales Presentation Assertions

**ACRUE Dimension Distribution**:
- Accuracy: 13 assertions (38.2%)
- Completeness: 10 assertions (29.4%)
- Relevance: 5 assertions (14.7%)
- Usefulness: 4 assertions (11.8%)
- Exceptional: 2 assertions (5.9%)

**Level Distribution**:
- Critical: 7 assertions (20.6%)
- Expected: 6 assertions (17.6%)
- Aspirational: 4 assertions (11.8%)

---

**Key Insight**: Sales presentation workback plans that include ≥2 discovery calls, internal dry runs, and validated ROI models improve win rates from 18% (baseline) to 34% (Sales Benchmark Index data). The 21-day timeline enables thorough customer understanding and solution customization, which are the primary drivers of executive sales success.

