# Workback Plan Examples and ACRUE Evaluation - Part 6

**Meeting Type**: Investor Relations Presentation  
**Author**: Chin-Yew Lin  
**Created**: November 13, 2025

---

## 6. Investor Relations Presentation

### Meeting Context

- **Meeting Type**: Q4 2025 Earnings Call and Investor Presentation
- **Target Date**: January 28, 2026, 5:00 PM - 6:30 PM ET
- **Organizer**: Chief Financial Officer
- **Attendees**: Public call (500+ investors/analysts expected), Presenters: CEO, CFO (Internal prep team: IR Director, Legal, Corporate Comm, Investor Relations)
- **Objective**: Report Q4 and FY2025 financial results, provide FY2026 guidance, answer analyst questions
- **Market Context**: $6.2B market cap, NASDAQ-listed, 18 sell-side analysts covering, quarterly earnings tradition
- **Regulatory**: SEC Regulation FD (Fair Disclosure), Form 8-K filing same day, press release 4:00 PM ET

---

### Example A: Good Workback Plan

```yaml
workback_plan:
  meeting_title: "Q4 2025 Earnings Call and Investor Presentation"
  meeting_date: "2026-01-28T17:00:00-05:00"
  meeting_duration_minutes: 90
  organizer: "Sarah Rodriguez, Chief Financial Officer"
  fiscal_period: "Q4 2025 (Oct-Dec) and Full Year 2025"
  earnings_release_time: "2026-01-28T16:00:00-05:00"
  market_cap: "$6.2B"
  analyst_coverage: 18
  complexity: "very_high"
  
  milestones:
    - milestone_id: "M1"
      name: "Preliminary Financial Close Complete"
      due_date: "2026-01-10T17:00:00-05:00"
      days_before_meeting: 18
      description: "Q4 financials closed, auditor preliminary review complete"
      success_criteria:
        - "Q4 revenue, expenses, earnings per share (EPS) preliminary numbers"
        - "Full year 2025 revenue $487M, GAAP EPS $1.23, non-GAAP EPS $1.89"
        - "External auditor (Deloitte) preliminary review complete, no material adjustments"
        - "Revenue recognition analysis complete (ASC 606 compliance)"
        - "Q4 vs. guidance comparison: Revenue within 2%, EPS within $0.03"
      dependencies: []
      owner: "CFO + Finance Team"
      
    - milestone_id: "M2"
      name: "Earnings Script First Draft Complete"
      due_date: "2026-01-15T17:00:00-05:00"
      days_before_meeting: 13
      description: "CEO and CFO prepared remarks drafted"
      success_criteria:
        - "CEO script: 8-minute strategic highlights (Q4 wins, FY2026 priorities, market outlook)"
        - "CFO script: 12-minute financial results (Q4 revenue breakdown, expenses, EPS, cash flow, FY2026 guidance)"
        - "FY2026 guidance ranges: Revenue $535-555M (10-14% growth), non-GAAP EPS $2.05-2.15 (9-14% growth)"
        - "Key narratives: AI product momentum, enterprise expansion, operating leverage"
        - "Draft reviewed by IR Director for investor messaging"
      dependencies: ["M1"]
      owner: "CFO + IR Director + CEO"
      
    - milestone_id: "M3"
      name: "Legal Compliance Review Complete"
      due_date: "2026-01-18T17:00:00-05:00"
      days_before_meeting: 10
      description: "Legal review of script and materials for Reg FD, forward-looking statements"
      success_criteria:
        - "Script reviewed by General Counsel for Regulation FD compliance"
        - "Forward-looking statement disclaimer approved (guidance, projections, strategy)"
        - "Material non-public information (MNPI) cleared for disclosure"
        - "Selective disclosure risks identified and mitigated"
        - "No SEC reporting violations (10-K/10-Q consistency)"
      dependencies: ["M2"]
      owner: "General Counsel + CFO"
      
    - milestone_id: "M4"
      name: "First Full Rehearsal Complete"
      due_date: "2026-01-21T17:00:00-05:00"
      days_before_meeting: 7
      description: "CEO and CFO rehearse script with IR, legal, corporate communications"
      success_criteria:
        - "Full run-through: CEO remarks 8 min, CFO remarks 12 min, Q&A prep"
        - "Timing validated: 20-minute prepared remarks + 40-minute Q&A + 10-minute buffer"
        - "Narrative flow reviewed: Q4 results → FY2025 highlights → FY2026 guidance → Q&A"
        - "Voice/tone validated: confident but not promotional, balanced optimism"
        - "Feedback from IR, legal, corporate comm incorporated"
      dependencies: ["M3"]
      owner: "CEO + CFO + IR Director"
      
    - milestone_id: "M5"
      name: "Q&A Preparation Book Finalized"
      due_date: "2026-01-23T17:00:00-05:00"
      days_before_meeting: 5
      description: "Top 30 analyst questions with approved responses"
      success_criteria:
        - "≥30 anticipated questions from analyst consensus models and prior calls"
        - "Categories: Q4 results, FY2026 guidance, product pipeline, competition, margins, cash flow, M&A"
        - "Approved responses for each question (CEO or CFO designated)"
        - "Bridge answers for sensitive topics: churn, sales pipeline, hiring plans, pricing"
        - "Regulation FD compliance reviewed for all Q&A responses"
      dependencies: ["M4"]
      owner: "IR Director + CFO + CEO"
      
    - milestone_id: "M6"
      name: "Second Rehearsal with Mock Q&A"
      due_date: "2026-01-25T17:00:00-05:00"
      days_before_meeting: 3
      description: "Full rehearsal including mock analyst Q&A"
      success_criteria:
        - "Full script + 15-question mock Q&A session"
        - "IR Director plays analysts with tough questions (guidance assumptions, margin pressure, competition)"
        - "CEO and CFO practice bridge answers and staying on message"
        - "Timing validated: total call <90 minutes"
        - "Confidence check: CEO and CFO comfortable with script and Q&A"
      dependencies: ["M5"]
      owner: "CEO + CFO + IR Director"
      
    - milestone_id: "M7"
      name: "Final Materials Ready for Distribution"
      due_date: "2026-01-27T17:00:00-05:00"
      days_before_meeting: 1
      description: "Press release, investor deck, 8-K ready for filing"
      success_criteria:
        - "Earnings press release: Q4 results, FY2025 summary, FY2026 guidance, CEO quote"
        - "Investor presentation deck: 25 slides (financial results, segment performance, guidance, Q&A)"
        - "Form 8-K with earnings release as Exhibit 99.1"
        - "Supplemental financials: non-GAAP reconciliation, segment breakdown, KPIs"
        - "All materials approved by CFO, CEO, Legal, Board Chair"
      dependencies: ["M6"]
      owner: "CFO + IR Director + Legal"
      
    - milestone_id: "M8"
      name: "Earnings Call Ready"
      due_date: "2026-01-28T15:00:00-05:00"
      days_before_meeting: 0
      description: "All logistics, filings, and final prep complete"
      success_criteria:
        - "Press release distributed via PR Newswire at 4:00 PM ET (market close)"
        - "Form 8-K filed with SEC by 4:15 PM ET"
        - "Investor deck posted to IR website"
        - "Earnings call dial-in and webcast tested"
        - "CEO and CFO in conference room, Q&A prep book ready"
        - "IR team monitoring for technical issues"
      dependencies: ["M7"]
      owner: "CFO + IR Director"

  tasks:
    # M1 Tasks - Financial Close
    - task_id: "T1.1"
      milestone_id: "M1"
      name: "Execute Q4 Financial Close"
      description: "Close books for Q4 2025, consolidate financials"
      owner: "CFO + Controller"
      estimated_hours: 80
      due_date: "2026-01-08T17:00:00-05:00"
      dependencies: []
      
    - task_id: "T1.2"
      milestone_id: "M1"
      name: "External Auditor Preliminary Review"
      description: "Deloitte reviews Q4 close, identifies adjustments"
      owner: "Deloitte + CFO"
      estimated_hours: 40
      due_date: "2026-01-10T17:00:00-05:00"
      dependencies: ["T1.1"]
      
    # M2 Tasks - Script Drafting
    - task_id: "T2.1"
      milestone_id: "M2"
      name: "Draft CEO Remarks"
      description: "CEO script: Q4 highlights, FY2026 strategy, market positioning"
      owner: "CEO + Corporate Communications"
      estimated_hours: 12
      due_date: "2026-01-13T17:00:00-05:00"
      dependencies: ["T1.2"]
      
    - task_id: "T2.2"
      milestone_id: "M2"
      name: "Draft CFO Financial Review"
      description: "CFO script: Q4 results, FY2025 summary, FY2026 guidance, model assumptions"
      owner: "CFO + IR Director"
      estimated_hours: 16
      due_date: "2026-01-14T17:00:00-05:00"
      dependencies: ["T1.2"]
      
    - task_id: "T2.3"
      milestone_id: "M2"
      name: "Develop FY2026 Guidance Ranges"
      description: "Build guidance model: revenue, expenses, EPS with sensitivity analysis"
      owner: "CFO + FP&A"
      estimated_hours: 24
      due_date: "2026-01-15T17:00:00-05:00"
      dependencies: ["T1.2"]
      
    # M3 Tasks - Legal Review
    - task_id: "T3.1"
      milestone_id: "M3"
      name: "Legal Review of Script"
      description: "General Counsel reviews script for Reg FD, MNPI, forward-looking statements"
      owner: "General Counsel"
      estimated_hours: 8
      due_date: "2026-01-17T17:00:00-05:00"
      dependencies: ["T2.1", "T2.2", "T2.3"]
      
    - task_id: "T3.2"
      milestone_id: "M3"
      name: "Revise Script for Legal Compliance"
      description: "Incorporate legal feedback, add disclaimers, clarify forward-looking statements"
      owner: "CFO + IR Director"
      estimated_hours: 6
      due_date: "2026-01-18T17:00:00-05:00"
      dependencies: ["T3.1"]
      
    # M4 Tasks - First Rehearsal
    - task_id: "T4.1"
      milestone_id: "M4"
      name: "Schedule and Conduct First Rehearsal"
      description: "2-hour session: CEO and CFO deliver script, IR/legal/comm provide feedback"
      owner: "IR Director + CEO + CFO"
      estimated_hours: 6
      due_date: "2026-01-21T17:00:00-05:00"
      dependencies: ["T3.2"]
      
    - task_id: "T4.2"
      milestone_id: "M4"
      name: "Revise Script Based on Rehearsal Feedback"
      description: "Adjust timing, clarify messaging, simplify complex financials"
      owner: "CFO + IR Director"
      estimated_hours: 4
      due_date: "2026-01-21T20:00:00-05:00"
      dependencies: ["T4.1"]
      
    # M5 Tasks - Q&A Prep
    - task_id: "T5.1"
      milestone_id: "M5"
      name: "Compile Analyst Consensus Questions"
      description: "Review prior calls, analyst reports, consensus models for likely questions"
      owner: "IR Director"
      estimated_hours: 12
      due_date: "2026-01-22T17:00:00-05:00"
      dependencies: ["T4.2"]
      
    - task_id: "T5.2"
      milestone_id: "M5"
      name: "Draft Q&A Responses"
      description: "Write approved responses for ≥30 anticipated questions"
      owner: "IR Director + CFO + CEO"
      estimated_hours: 20
      due_date: "2026-01-23T17:00:00-05:00"
      dependencies: ["T5.1"]
      
    # M6 Tasks - Second Rehearsal
    - task_id: "T6.1"
      milestone_id: "M6"
      name: "Conduct Mock Q&A Rehearsal"
      description: "2-hour session: full script + 15-question mock Q&A"
      owner: "CEO + CFO + IR Director"
      estimated_hours: 6
      due_date: "2026-01-25T17:00:00-05:00"
      dependencies: ["T5.2"]
      
    # M7 Tasks - Materials Finalization
    - task_id: "T7.1"
      milestone_id: "M7"
      name: "Draft Earnings Press Release"
      description: "Press release: headline, results, guidance, CEO quote, tables"
      owner: "IR Director + Corporate Communications"
      estimated_hours: 10
      due_date: "2026-01-26T12:00:00-05:00"
      dependencies: ["T6.1"]
      
    - task_id: "T7.2"
      milestone_id: "M7"
      name: "Build Investor Presentation Deck"
      description: "25-slide deck: financial results, segment performance, guidance, appendix"
      owner: "IR Director + CFO"
      estimated_hours: 16
      due_date: "2026-01-26T17:00:00-05:00"
      dependencies: ["T6.1"]
      
    - task_id: "T7.3"
      milestone_id: "M7"
      name: "Prepare Form 8-K Filing"
      description: "Draft 8-K with earnings release as Exhibit 99.1"
      owner: "General Counsel + IR Director"
      estimated_hours: 6
      due_date: "2026-01-27T12:00:00-05:00"
      dependencies: ["T7.1"]
      
    - task_id: "T7.4"
      milestone_id: "M7"
      name: "Final Approval of All Materials"
      description: "CFO, CEO, Legal, Board Chair approve press release, deck, 8-K"
      owner: "CFO + CEO + General Counsel"
      estimated_hours: 4
      due_date: "2026-01-27T17:00:00-05:00"
      dependencies: ["T7.2", "T7.3"]
      
    # M8 Tasks - Earnings Day Execution
    - task_id: "T8.1"
      milestone_id: "M8"
      name: "Distribute Press Release"
      description: "Release via PR Newswire at 4:00 PM ET (market close)"
      owner: "Corporate Communications"
      estimated_hours: 2
      due_date: "2026-01-28T16:00:00-05:00"
      dependencies: ["T7.4"]
      
    - task_id: "T8.2"
      milestone_id: "M8"
      name: "File Form 8-K with SEC"
      description: "Submit 8-K via EDGAR by 4:15 PM ET"
      owner: "General Counsel"
      estimated_hours: 1
      due_date: "2026-01-28T16:15:00-05:00"
      dependencies: ["T8.1"]
      
    - task_id: "T8.3"
      milestone_id: "M8"
      name: "Post Investor Materials to IR Website"
      description: "Upload press release, investor deck, webcast link"
      owner: "IR Director"
      estimated_hours: 1
      due_date: "2026-01-28T16:15:00-05:00"
      dependencies: ["T8.1"]
      
    - task_id: "T8.4"
      milestone_id: "M8"
      name: "Execute Earnings Call"
      description: "CEO and CFO deliver prepared remarks and answer analyst questions"
      owner: "CEO + CFO"
      estimated_hours: 2
      due_date: "2026-01-28T18:30:00-05:00"
      dependencies: ["T8.2", "T8.3"]

  risks:
    - risk_id: "R1"
      description: "Q4 results miss consensus estimates, negative market reaction"
      probability: "low"
      impact: "critical"
      mitigation: "Early guidance range setting with CFO; pre-announce if miss >5%; investor outreach pre-call to manage expectations; focus on FY2026 guidance and long-term strategy; have turnaround narrative ready"
      owner: "CFO"
      
    - risk_id: "R2"
      description: "Regulation FD violation (selective disclosure, MNPI leak)"
      probability: "low"
      impact: "critical"
      mitigation: "Legal review all materials; train CEO/CFO on Reg FD; Q&A prep book approved by counsel; if inadvertent disclosure, file 8-K within 24 hours; have PR crisis plan; monitoring by legal during call"
      owner: "General Counsel"
      
    - risk_id: "R3"
      description: "Tough analyst questions catch CEO/CFO off guard, fumbled response"
      probability: "medium"
      impact: "high"
      mitigation: "≥30 anticipated questions prepared with approved responses; ≥2 rehearsals with mock Q&A; bridge answers for sensitive topics; CEO/CFO can defer to follow-up if needed; IR monitors call and provides real-time notes"
      owner: "IR Director"
      
    - risk_id: "R4"
      description: "Technical issues with earnings call (audio, webcast, dial-in)"
      probability: "low"
      impact: "medium"
      mitigation: "Test webcast and dial-in 1 hour before; backup phone line; IT support on standby; can delay call up to 15 minutes; transcript available post-call"
      owner: "IR Director + IT"
      
    - risk_id: "R5"
      description: "Auditor identifies material adjustment post-release, requires restatement"
      probability: "very_low"
      impact: "critical"
      mitigation: "Auditor preliminary review complete 18 days before call; final auditor sign-off before press release; CFO reviews all material transactions; restatement protocol: 8-K, amended 10-K, investor call"
      owner: "CFO"

  quality_checks:
    - check_id: "Q1"
      name: "Financial Results Auditor-Validated"
      description: "External auditor completes preliminary review with no material adjustments"
      checkpoint: "M1"
      pass_criteria: "Deloitte sign-off on Q4 close; adjustments <$500K materiality threshold"
      
    - check_id: "Q2"
      name: "Legal Compliance Review"
      description: "Script and materials comply with Regulation FD, forward-looking statement rules"
      checkpoint: "M3"
      pass_criteria: "General Counsel approval; no MNPI in script; disclaimers present; Reg FD compliant"
      
    - check_id: "Q3"
      name: "Rehearsal Timing Validation"
      description: "Full script fits within 20-minute prepared remarks window"
      checkpoint: "M4"
      pass_criteria: "CEO remarks ≤8 minutes, CFO remarks ≤12 minutes, total ≤20 minutes"
      
    - check_id: "Q4"
      name: "Q&A Preparation Depth"
      description: "≥30 anticipated analyst questions with approved responses"
      checkpoint: "M5"
      pass_criteria: "Q&A prep book covers top analyst consensus questions, bridge answers for sensitive topics"
      
    - check_id: "Q5"
      name: "Mock Q&A Confidence Check"
      description: "CEO and CFO comfortable answering tough questions in rehearsal"
      checkpoint: "M6"
      pass_criteria: "IR Director rates CEO/CFO Q&A performance ≥8/10; fumbled answers <2/15"
      
    - check_id: "Q6"
      name: "Materials Approval"
      description: "CFO, CEO, Legal, Board Chair approve all earnings materials"
      checkpoint: "M7"
      pass_criteria: "All materials signed off; no last-minute changes"
      
    - check_id: "Q7"
      name: "Timely SEC Filing"
      description: "Press release distributed and 8-K filed within regulatory windows"
      checkpoint: "M8"
      pass_criteria: "Press release at market close (4:00 PM ET); 8-K filed ≤1 hour later"

  metadata:
    total_estimated_hours: 276
    critical_path_days: 18
    number_of_dependencies: 19
    regulatory_framework: "SEC Regulation FD, Form 8-K"
    market_cap: "$6.2B"
    analyst_coverage: 18
    fiscal_period: "Q4 2025 / FY2025"
    external_auditor: "Deloitte"
    key_stakeholders: ["CEO", "CFO", "General Counsel", "IR Director", "Corporate Communications", "Board Chair", "External Auditor", "Sell-Side Analysts", "Institutional Investors"]
    success_indicators:
      - "Earnings call executed without Regulation FD violations"
      - "CEO/CFO deliver confident, on-message presentation"
      - "Analyst questions answered effectively (≥90% satisfaction)"
      - "Stock price reaction within +/-3% (neutral to positive reception)"
      - "SEC filings timely and accurate (no amendments)"

```

**Why This is a Good Workback Plan**:
- ✅ **18-day timeline** from financial close to earnings call enables auditor review, rehearsals, legal compliance
- ✅ **External auditor preliminary review** ≥18 days before call prevents post-release adjustments
- ✅ **Legal compliance review** for Regulation FD, forward-looking statements, MNPI
- ✅ **≥2 full rehearsals** including mock analyst Q&A
- ✅ **Q&A prep book** with ≥30 anticipated questions and approved responses
- ✅ **FY2026 guidance development** with sensitivity analysis and model assumptions
- ✅ **Timely SEC filings** (press release at market close, 8-K within 1 hour)
- ✅ **Risk mitigation** for consensus misses, Reg FD violations, technical issues
- ✅ **Quality checks** enforce auditor validation, legal approval, rehearsal depth
- ✅ **Materials approval** by CFO, CEO, Legal, Board Chair before distribution

---

### Example B: Bad Workback Plan

```yaml
workback_plan:
  meeting_title: "Earnings Call"
  meeting_date: "2026-01-28T17:00:00-05:00"
  meeting_duration_minutes: 90
  organizer: "Finance"
  fiscal_period: "Q4 2025"
  complexity: "medium"
  
  milestones:
    - milestone_id: "M1"
      name: "Get numbers ready"
      due_date: "2026-01-27T17:00:00-05:00"
      days_before_meeting: 1
      description: "Close the quarter"
      success_criteria:
        - "Numbers done"
      dependencies: []
      owner: "CFO"
      
    - milestone_id: "M2"
      name: "Write script"
      due_date: "2026-01-28T12:00:00-05:00"
      days_before_meeting: 0
      description: "Make talking points"
      success_criteria:
        - "Script ready"
      dependencies: ["M1"]
      owner: "IR"

  tasks:
    - task_id: "T1"
      milestone_id: "M1"
      name: "Close books"
      description: "Finish financial close"
      owner: "Finance"
      estimated_hours: null
      due_date: "2026-01-27T17:00:00-05:00"
      dependencies: []
      
    - task_id: "T2"
      milestone_id: "M2"
      name: "Create presentation"
      description: "Make slides about earnings"
      owner: "Someone in IR"
      estimated_hours: null
      due_date: "2026-01-28T11:00:00-05:00"
      dependencies: ["T1"]
      
    - task_id: "T3"
      milestone_id: "M2"
      name: "Practice"
      description: "Run through script once"
      owner: "CEO and CFO"
      estimated_hours: null
      due_date: "2026-01-28T14:00:00-05:00"
      dependencies: ["T2"]

  risks:
    - risk_id: "R1"
      description: "Call might not go well"
      probability: "unknown"
      impact: "bad"
      mitigation: "Hope for best"
      owner: "Team"

  quality_checks:
    - check_id: "Q1"
      name: "Numbers seem right"
      description: "Check if financials look okay"
      checkpoint: "M1"
      pass_criteria: "Looks good"

  metadata:
    total_estimated_hours: null
    critical_path_days: 1
    number_of_dependencies: 1
    key_stakeholders: ["CFO", "CEO"]
    success_indicators:
      - "Call happens"
      - "Investors don't complain too much"
```

**Why This is a Bad Workback Plan**:
- ❌ **Only 1-day timeline** - earnings calls require 14-21 days for auditor review, legal compliance, rehearsals
- ❌ **No external auditor review** - risk of post-release adjustment or restatement
- ❌ **No legal compliance review** - Regulation FD violation risk
- ❌ **Script written day-of** - no time for rehearsal, legal review, messaging refinement
- ❌ **Only 1 practice run** - insufficient Q&A preparation
- ❌ **No Q&A prep book** - CEO/CFO vulnerable to tough analyst questions
- ❌ **No FY2026 guidance process** - analysts expect forward guidance
- ❌ **No SEC filing timeline** - press release and 8-K timing undefined
- ❌ **Vague success criteria** ("numbers done", "looks good")
- ❌ **No risk mitigation** for consensus misses, Reg FD violations, technical issues
- ❌ **Average stock price drop 2.1%** when earnings calls lack preparation (IR Magazine study)
- ❌ **Regulation FD violations** cost companies avg $150K in SEC fines + legal costs + reputational damage

---

### ACRUE Assertions for Investor Relations Workback Plans

#### Critical Assertions (Must Pass)

**Accuracy Dimension**:
- text: "The workback plan includes external auditor preliminary review of financial results ≥7 days before earnings call"
  - level: critical
  - dimension: Accuracy
  - rationale: "Post-release financial adjustments destroy investor confidence; auditor review prevents restatements"

- text: "Plan specifies legal compliance review for SEC Regulation FD (Fair Disclosure) and forward-looking statements"
  - level: critical
  - dimension: Accuracy
  - rationale: "Reg FD violations = SEC enforcement, fines, shareholder lawsuits; legal review is mandatory"

- text: "Timeline allows ≥14 days from financial close to earnings call for script development, rehearsals, legal review"
  - level: critical
  - dimension: Accuracy
  - rationale: "Rushed earnings calls lead to fumbled messaging, Reg FD violations, investor confusion"

**Completeness Dimension**:
- text: "Plan includes ≥2 full rehearsals with CEO and CFO delivering prepared remarks"
  - level: critical
  - dimension: Completeness
  - rationale: "Unrehearsed executives fumble questions, miss key messages; rehearsals ensure confident delivery"

- text: "Milestones specify Q&A preparation with ≥20 anticipated analyst questions and approved responses"
  - level: critical
  - dimension: Completeness
  - rationale: "Unprepared Q&A damages credibility; analyst questions are predictable and must be prepared"

- text: "Tasks include timely SEC filings (press release at market close, Form 8-K within 1 hour)"
  - level: critical
  - dimension: Completeness
  - rationale: "Late SEC filings = Regulation FD violations, trading halts; timely filing is regulatory requirement"

**Relevance Dimension**:
- text: "Success criteria measure investor reception (stock price reaction, analyst feedback, call participation) not just execution"
  - level: critical
  - dimension: Relevance
  - rationale: "Earnings call success is market reception, not just completing the call"

#### Expected Assertions (Should Pass)

**Usefulness Dimension**:
- text: "Plan includes mock Q&A session with tough analyst questions in final rehearsal"
  - level: expected
  - dimension: Usefulness
  - rationale: "Practicing tough questions prevents fumbled responses on live call; IR can simulate analyst pressure"

- text: "Tasks specify FY2026 guidance development with revenue/EPS ranges and model assumptions"
  - level: expected
  - dimension: Usefulness
  - rationale: "Analysts expect forward guidance; guidance ranges must be supportable with model assumptions"

- text: "Quality checks validate script timing (CEO + CFO remarks ≤20 minutes) to allow ≥40 minutes for Q&A"
  - level: expected
  - dimension: Usefulness
  - rationale: "Overly long scripts limit Q&A time; analysts prefer more Q&A interaction"

**Completeness Dimension**:
- text: "Plan includes investor presentation deck preparation (financial results, segment performance, guidance)"
  - level: expected
  - dimension: Completeness
  - rationale: "Investors expect visual materials; deck supports script and enables post-call reference"

- text: "Milestones specify press release drafting with headline, results, guidance, CEO quote"
  - level: expected
  - dimension: Completeness
  - rationale: "Press release is primary earnings communication; must be compelling and accurate"

**Accuracy Dimension**:
- text: "Risk mitigation addresses consensus miss scenario (pre-announcement, investor outreach, turnaround narrative)"
  - level: expected
  - dimension: Accuracy
  - rationale: "Missing consensus = stock price drop; pre-announcement (if miss >5%) and expectation management reduce negative reaction"

#### Aspirational Assertions (Nice to Have)

**Exceptional Dimension**:
- text: "Plan tracks analyst consensus estimates and updates to manage expectation risk"
  - level: aspirational
  - dimension: Exceptional
  - rationale: "Tracking consensus enables proactive expectation management; large beats/misses surprise market"

- text: "Success indicators measure long-term investor confidence (institutional ownership changes, analyst rating changes, conference attendance)"
  - level: aspirational
  - dimension: Exceptional
  - rationale: "Earnings call is one touchpoint; long-term investor confidence is ultimate success measure"

**Usefulness Dimension**:
- text: "Metadata documents prior earnings call performance (stock reaction, analyst feedback, Q&A themes) for continuous improvement"
  - level: aspirational
  - dimension: Usefulness
  - rationale: "Learning from prior calls improves messaging and Q&A preparation"

- text: "Plan includes Board Chair approval of earnings materials (press release, deck, guidance)"
  - level: aspirational
  - dimension: Usefulness
  - rationale: "Board oversight ensures alignment on guidance and messaging; prevents CEO/CFO overreach"

---

### ACRUE Rubrics for Investor Relations Workback Plans

#### Accuracy Rubric

**Measures**: Realistic timelines, auditor validation, legal compliance, guidance rigor

- **Gold Standard (9-10 points)**:
  - ≥18-day timeline from financial close to earnings call
  - External auditor preliminary review ≥7 days before call
  - Legal compliance review (Regulation FD, MNPI, forward-looking statements)
  - FY2026 guidance with revenue/EPS ranges and model assumptions
  - ≥2 full rehearsals (initial + mock Q&A)
  - Q&A prep book with ≥30 anticipated questions
  - SEC filing timeline (press release at market close, 8-K ≤1 hour)
  - Script timing validated (CEO+CFO ≤20 minutes)
  - All assumptions validated through auditor, legal, Board review

- **Silver Standard (7-8 points)**:
  - ≥14-day timeline
  - Auditor review conducted
  - Legal review performed
  - Guidance developed
  - ≥1 rehearsal
  - ≥15 Q&A questions prepared
  - SEC filings planned
  - Timing validated

- **Bronze Standard (5-6 points)**:
  - ≥7-day timeline
  - Financials reviewed
  - Legal consulted
  - Some guidance
  - Script practice
  - Q&A considered

- **Fails Standard (<5 points)**:
  - <7-day timeline
  - No auditor review
  - No legal review
  - No guidance
  - No rehearsal
  - No Q&A prep

#### Completeness Rubric

**Measures**: Coverage of all earnings call preparation workstreams

- **Gold Standard (9-10 points)**:
  - Financial close and auditor preliminary review
  - Script drafting (CEO strategic remarks, CFO financial review)
  - FY2026 guidance development with model
  - Legal compliance review (Reg FD, forward-looking statements)
  - First rehearsal (script delivery, timing, messaging)
  - Q&A preparation book (≥30 questions, approved responses)
  - Second rehearsal with mock Q&A
  - Press release drafting
  - Investor presentation deck (25+ slides)
  - Form 8-K preparation
  - Materials approval (CFO, CEO, Legal, Board)
  - Earnings day execution (press release, 8-K filing, webcast, call)
  - Post-call follow-up (transcript, analyst inquiries, investor outreach)

- **Silver Standard (7-8 points)**:
  - Financial close
  - Script drafting
  - Guidance development
  - Legal review
  - Rehearsal
  - Q&A preparation
  - Press release
  - Investor deck
  - 8-K filing
  - Materials approval
  - Call execution

- **Bronze Standard (5-6 points)**:
  - Financial close
  - Script drafting
  - Some guidance
  - Legal consulted
  - Practice run
  - Press release
  - Call execution

- **Fails Standard (<5 points)**:
  - Financial close only
  - Minimal script prep
  - No guidance
  - No legal review
  - No rehearsal
  - Last-minute materials

#### Relevance Rubric

**Measures**: Focus on investor communication effectiveness vs. generic project management

- **Gold Standard (9-10 points)**:
  - All milestones tied to investor communication requirements (auditor validation, legal compliance, messaging refinement, Q&A readiness)
  - Success criteria measure investor reception (stock price reaction, analyst feedback, call participation, Q&A quality)
  - Risks address IR-specific failures (consensus miss, Reg FD violation, fumbled Q&A, technical issues)
  - Quality checks enforce investor communication standards (auditor sign-off, legal approval, rehearsal depth, SEC filing timeliness)
  - Decision framework based on investor readiness (confident messaging, compliance, Q&A preparedness)

- **Silver Standard (7-8 points)**:
  - Most milestones IR-relevant
  - Success criteria mostly investor-focused
  - Risks include IR concerns
  - Quality checks present
  - Readiness criteria defined

- **Bronze Standard (5-6 points)**:
  - Milestones include IR activities
  - Some investor criteria
  - Generic risks
  - Basic quality checks

- **Fails Standard (<5 points)**:
  - Generic project milestones
  - Vague criteria ("call happens")
  - Risks unrelated to IR
  - No investor communication focus

#### Usefulness Rubric

**Measures**: Actionability for IR team, CEO, CFO, legal

- **Gold Standard (9-10 points)**:
  - All tasks have named owners (specific roles: CFO, CEO, IR Director, General Counsel, Controller, Corporate Comm)
  - Time estimates enable capacity planning (270+ hours typical)
  - Script templates (CEO strategic remarks 8 min, CFO financial review 12 min)
  - FY2026 guidance model with sensitivity analysis
  - Q&A prep book template (question, approved response, bridge answer, Reg FD check)
  - Rehearsal agenda (timing, feedback, messaging validation)
  - Legal review checklist (Reg FD, MNPI, forward-looking statements, disclaimers)
  - Press release template (headline, results, guidance, CEO quote, tables)
  - Investor deck outline (25 slides: results, segments, guidance, appendix)
  - Form 8-K filing procedure
  - Earnings day timeline (press release 4:00 PM, 8-K 4:15 PM, call 5:00 PM)

- **Silver Standard (7-8 points)**:
  - Most tasks have named owners
  - Time estimates for major workstreams
  - Script guidance provided
  - Guidance model developed
  - Q&A prep book
  - Rehearsal scheduled
  - Legal review
  - Press release template
  - Investor deck
  - 8-K procedure

- **Bronze Standard (5-6 points)**:
  - Some specific owners
  - Basic timeline
  - Script drafted
  - Guidance developed
  - Q&A considered
  - Legal consulted
  - Materials created

- **Fails Standard (<5 points)**:
  - Vague owners ("finance", "IR")
  - No time estimates
  - No script guidance
  - No guidance model
  - No Q&A prep
  - No legal review process
  - Minimal materials

#### Exceptional Rubric

**Measures**: Advanced IR practices that maximize investor confidence

- **Gold Standard (9-10 points)**:
  - Analyst consensus tracking with weekly updates (expectation management)
  - Prior earnings call performance analysis (stock reaction, analyst feedback, Q&A themes)
  - Board Chair approval of guidance and materials (governance oversight)
  - Investor perception survey post-call (confidence, clarity, credibility ratings)
  - Sell-side analyst rating changes tracked post-call
  - Institutional ownership monitoring (13F filings)
  - IR website analytics (investor deck downloads, webcast views)
  - Post-call analyst one-on-ones to gather feedback
  - Long-term investor confidence metrics (conference attendance, roadshow interest)

- **Silver Standard (7-8 points)**:
  - Consensus tracking
  - Prior call review
  - Board approval
  - Post-call feedback
  - Analyst ratings tracked
  - IR metrics monitored

- **Bronze Standard (5-6 points)**:
  - Some consensus awareness
  - Basic post-call review
  - Board informed
  - Analyst feedback collected

- **Fails Standard (<5 points)**:
  - No consensus tracking
  - No performance analysis
  - No board oversight
  - No feedback loop

---

### Distribution for Investor Relations Assertions

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

**Key Insight**: Well-prepared earnings calls with ≥2 rehearsals, ≥30 Q&A responses, and legal compliance review result in 2.3% more positive stock price reactions compared to poorly prepared calls (IR Magazine study). Regulation FD violations cost companies an average $150K in SEC fines plus legal costs and reputational damage. The 18-day timeline in the good example enables auditor validation, legal compliance, confident messaging—the three pillars of effective investor communication.

