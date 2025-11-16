# Workback Plan Examples and ACRUE Evaluation - Part 5

**Meeting Type**: Regulatory/Compliance Review  
**Author**: Chin-Yew Lin  
**Created**: November 13, 2025

---

## 5. Regulatory/Compliance Review Meeting

### Meeting Context

- **Meeting Type**: Annual SOX 404 Compliance Review with External Auditors
- **Target Date**: March 15, 2026, 2:00 PM - 5:00 PM ET
- **Organizer**: Chief Compliance Officer
- **Attendees**: External Auditors (4), CFO, CTO, Chief Compliance Officer, General Counsel, Internal Audit (8 total)
- **Objective**: Review internal controls testing, certify SOX 404 compliance, identify deficiencies, approve remediation plans
- **Regulatory Context**: SOX Section 404 mandates management assessment and external audit of internal controls over financial reporting
- **Compliance Impact**: Material weakness = restatement risk, stock price impact, regulatory investigation; clean opinion required for NYSE listing

---

### Example A: Good Workback Plan

```yaml
workback_plan:
  meeting_title: "SOX 404 Compliance Review - FY2025 Internal Controls Assessment"
  meeting_date: "2026-03-15T14:00:00-05:00"
  meeting_duration_minutes: 180
  organizer: "Michael Chen, Chief Compliance Officer"
  compliance_framework: "SOX Section 404 - Internal Controls Over Financial Reporting"
  fiscal_year: "FY2025 (ended December 31, 2025)"
  external_auditor: "KPMG LLP"
  complexity: "very_high"
  
  milestones:
    - milestone_id: "M1"
      name: "Control Universe and Testing Plan Finalized"
      due_date: "2025-12-15T17:00:00-05:00"
      days_before_meeting: 90
      description: "Complete control identification, risk assessment, testing methodology"
      success_criteria:
        - "All 127 key financial controls documented in control matrix"
        - "Risk-based testing plan: 35 key controls 100% tested, 92 non-key controls sampled"
        - "External auditor agreement on control scope and testing approach"
        - "Testing timeline: January 2-February 28 (8 weeks)"
        - "Test ownership assigned: Finance (45 controls), IT (38 controls), Operations (44 controls)"
      dependencies: []
      owner: "Chief Compliance Officer + Internal Audit"
      
    - milestone_id: "M2"
      name: "Control Testing Phase Complete"
      due_date: "2026-02-28T17:00:00-05:00"
      days_before_meeting: 15
      description: "All 127 controls tested, evidence collected, deficiencies identified"
      success_criteria:
        - "100% of key controls tested (35/35)"
        - "≥90% of non-key controls tested (83+/92)"
        - "All evidence documented in audit management system"
        - "Deficiencies classified: 0 material weaknesses (target), ≤3 significant deficiencies, ≤15 control deficiencies"
        - "Test results reviewed by control owners and Internal Audit"
      dependencies: ["M1"]
      owner: "Internal Audit Team + Control Owners"
      
    - milestone_id: "M3"
      name: "Deficiency Remediation Plans Approved"
      due_date: "2026-03-05T17:00:00-05:00"
      days_before_meeting: 10
      description: "Remediation plans for all deficiencies developed and management-approved"
      success_criteria:
        - "Remediation plan for each deficiency: root cause, corrective action, owner, timeline, validation"
        - "High-priority deficiencies: remediation target ≤30 days"
        - "Medium-priority: ≤90 days"
        - "Low-priority: ≤180 days"
        - "CFO and CEO approval of remediation commitments"
      dependencies: ["M2"]
      owner: "Control Owners + Chief Compliance Officer"
      
    - milestone_id: "M4"
      name: "Management Assessment Report Drafted"
      due_date: "2026-03-08T17:00:00-05:00"
      days_before_meeting: 7
      description: "Management's assessment of internal controls effectiveness drafted"
      success_criteria:
        - "Assessment conclusion: Effective (if 0 material weaknesses) or Not Effective"
        - "All 127 controls assessed with test results"
        - "All deficiencies disclosed with severity classification"
        - "Remediation plans documented"
        - "CEO and CFO certifications prepared (SOX 302)"
        - "Draft shared with external auditor for review"
      dependencies: ["M3"]
      owner: "Chief Compliance Officer + CFO"
      
    - milestone_id: "M5"
      name: "External Auditor Fieldwork Complete"
      due_date: "2026-03-10T17:00:00-05:00"
      days_before_meeting: 5
      description: "External auditor completes testing of management's assessment"
      success_criteria:
        - "Auditor tested ≥25 key controls independently"
        - "All auditor information requests fulfilled (target: 100%)"
        - "Auditor walkthroughs completed for all key processes"
        - "Auditor preliminary findings reviewed with management"
        - "No new material weaknesses identified by auditor"
      dependencies: ["M4"]
      owner: "External Auditor (KPMG) + Internal Audit Liaison"
      
    - milestone_id: "M6"
      name: "Audit Committee Pre-Briefing Complete"
      due_date: "2026-03-12T17:00:00-05:00"
      days_before_meeting: 3
      description: "Audit Committee Chair pre-briefed on compliance status"
      success_criteria:
        - "1-hour private session with Audit Committee Chair"
        - "Management assessment results shared: conclusion, deficiencies, remediation"
        - "External auditor preliminary opinion previewed"
        - "No surprises for Audit Committee on meeting day"
        - "Chair approval to proceed with full committee review"
      dependencies: ["M5"]
      owner: "Chief Compliance Officer + CFO"
      
    - milestone_id: "M7"
      name: "Final Compliance Review Materials Distributed"
      due_date: "2026-03-14T17:00:00-05:00"
      days_before_meeting: 1
      description: "All meeting materials provided to attendees"
      success_criteria:
        - "Management assessment report (final draft)"
        - "Control testing summary: 127 controls, results, deficiencies"
        - "Remediation plans (detailed) for all deficiencies"
        - "External auditor report on management's assessment"
        - "CEO/CFO certifications (SOX 302)"
        - "Prior year comparison (deficiencies closed, new issues)"
      dependencies: ["M6"]
      owner: "Chief Compliance Officer"
      
    - milestone_id: "M8"
      name: "Compliance Review Meeting Ready"
      due_date: "2026-03-15T13:00:00-05:00"
      days_before_meeting: 0
      description: "Meeting logistics and decision framework prepared"
      success_criteria:
        - "Conference room setup (hybrid: 5 in-person, 3 remote)"
        - "Audit management system access for evidence review"
        - "Decision framework: Approve assessment + remediation plans OR require additional work"
        - "External auditor prepared to issue opinion (Unqualified if 0 material weaknesses)"
        - "CEO/CFO ready to sign certifications post-meeting"
      dependencies: ["M7"]
      owner: "Chief Compliance Officer + Admin"

  tasks:
    # M1 Tasks - Control Universe
    - task_id: "T1.1"
      milestone_id: "M1"
      name: "Update Control Matrix for FY2025"
      description: "Review and update all 127 financial controls for process/system changes"
      owner: "Internal Audit"
      estimated_hours: 40
      due_date: "2025-12-01T17:00:00-05:00"
      dependencies: []
      
    - task_id: "T1.2"
      milestone_id: "M1"
      name: "Conduct Risk Assessment"
      description: "Assess inherent risk and control risk for all financial processes"
      owner: "Internal Audit + Process Owners"
      estimated_hours: 30
      due_date: "2025-12-05T17:00:00-05:00"
      dependencies: ["T1.1"]
      
    - task_id: "T1.3"
      milestone_id: "M1"
      name: "Design Testing Plan"
      description: "Define sample sizes, testing procedures, evidence requirements"
      owner: "Internal Audit"
      estimated_hours: 20
      due_date: "2025-12-10T17:00:00-05:00"
      dependencies: ["T1.2"]
      
    - task_id: "T1.4"
      milestone_id: "M1"
      name: "External Auditor Testing Plan Review"
      description: "KPMG reviews and agrees on testing scope and methodology"
      owner: "KPMG + Internal Audit"
      estimated_hours: 8
      due_date: "2025-12-15T17:00:00-05:00"
      dependencies: ["T1.3"]
      
    # M2 Tasks - Control Testing
    - task_id: "T2.1"
      milestone_id: "M2"
      name: "Execute Finance Controls Testing"
      description: "Test 45 finance-owned controls (revenue, expenses, close, reporting)"
      owner: "Internal Audit + Finance Analysts"
      estimated_hours: 180
      due_date: "2026-02-14T17:00:00-05:00"
      dependencies: ["T1.4"]
      
    - task_id: "T2.2"
      milestone_id: "M2"
      name: "Execute IT Controls Testing"
      description: "Test 38 IT general controls (access, change mgmt, backups, security)"
      owner: "Internal Audit + IT Audit Specialist"
      estimated_hours: 150
      due_date: "2026-02-14T17:00:00-05:00"
      dependencies: ["T1.4"]
      
    - task_id: "T2.3"
      milestone_id: "M2"
      name: "Execute Operations Controls Testing"
      description: "Test 44 ops controls (procurement, inventory, payroll, HR)"
      owner: "Internal Audit + Operations"
      estimated_hours: 170
      due_date: "2026-02-14T17:00:00-05:00"
      dependencies: ["T1.4"]
      
    - task_id: "T2.4"
      milestone_id: "M2"
      name: "Document Control Testing Results"
      description: "Load all test evidence into audit management system, classify deficiencies"
      owner: "Internal Audit"
      estimated_hours: 60
      due_date: "2026-02-21T17:00:00-05:00"
      dependencies: ["T2.1", "T2.2", "T2.3"]
      
    - task_id: "T2.5"
      milestone_id: "M2"
      name: "Control Owner Review of Test Results"
      description: "Process owners review findings, validate deficiency classification"
      owner: "Control Owners (Finance, IT, Ops)"
      estimated_hours: 40
      due_date: "2026-02-28T17:00:00-05:00"
      dependencies: ["T2.4"]
      
    # M3 Tasks - Remediation Planning
    - task_id: "T3.1"
      milestone_id: "M3"
      name: "Develop Deficiency Remediation Plans"
      description: "For each deficiency: root cause analysis, corrective action, timeline"
      owner: "Control Owners + Compliance"
      estimated_hours: 50
      due_date: "2026-03-01T17:00:00-05:00"
      dependencies: ["T2.5"]
      
    - task_id: "T3.2"
      milestone_id: "M3"
      name: "Prioritize Remediation Actions"
      description: "Risk-rank deficiencies, allocate resources, set deadlines"
      owner: "Chief Compliance Officer + Process Owners"
      estimated_hours: 12
      due_date: "2026-03-03T17:00:00-05:00"
      dependencies: ["T3.1"]
      
    - task_id: "T3.3"
      milestone_id: "M3"
      name: "Management Approval of Remediation Plans"
      description: "CFO and CEO approve remediation commitments and timelines"
      owner: "CFO + CEO"
      estimated_hours: 4
      due_date: "2026-03-05T17:00:00-05:00"
      dependencies: ["T3.2"]
      
    # M4 Tasks - Management Assessment
    - task_id: "T4.1"
      milestone_id: "M4"
      name: "Draft Management Assessment Report"
      description: "Prepare SOX 404 management assessment: conclusion, controls, deficiencies"
      owner: "Chief Compliance Officer"
      estimated_hours: 30
      due_date: "2026-03-06T17:00:00-05:00"
      dependencies: ["T3.3"]
      
    - task_id: "T4.2"
      milestone_id: "M4"
      name: "Prepare CEO/CFO Certifications"
      description: "Draft SOX 302 certifications for CEO and CFO signatures"
      owner: "General Counsel"
      estimated_hours: 8
      due_date: "2026-03-07T17:00:00-05:00"
      dependencies: ["T4.1"]
      
    - task_id: "T4.3"
      milestone_id: "M4"
      name: "External Auditor Review of Draft Assessment"
      description: "Share draft with KPMG for preliminary review"
      owner: "KPMG + Chief Compliance Officer"
      estimated_hours: 6
      due_date: "2026-03-08T17:00:00-05:00"
      dependencies: ["T4.2"]
      
    # M5 Tasks - External Auditor Fieldwork
    - task_id: "T5.1"
      milestone_id: "M5"
      name: "Support Auditor Control Testing"
      description: "Provide evidence, walkthroughs, and access for auditor testing"
      owner: "Internal Audit Liaison + Process Owners"
      estimated_hours: 80
      due_date: "2026-03-08T17:00:00-05:00"
      dependencies: ["T4.3"]
      
    - task_id: "T5.2"
      milestone_id: "M5"
      name: "Resolve Auditor Inquiries"
      description: "Answer auditor questions, provide supplemental evidence"
      owner: "Internal Audit + Compliance"
      estimated_hours: 30
      due_date: "2026-03-10T17:00:00-05:00"
      dependencies: ["T5.1"]
      
    # M6 Tasks - Audit Committee Pre-Brief
    - task_id: "T6.1"
      milestone_id: "M6"
      name: "Prepare Audit Committee Briefing Materials"
      description: "Executive summary: assessment conclusion, key deficiencies, auditor status"
      owner: "Chief Compliance Officer"
      estimated_hours: 8
      due_date: "2026-03-11T17:00:00-05:00"
      dependencies: ["T5.2"]
      
    - task_id: "T6.2"
      milestone_id: "M6"
      name: "Conduct Audit Committee Chair Pre-Brief"
      description: "1-hour private session with Chair to preview compliance status"
      owner: "CFO + Chief Compliance Officer"
      estimated_hours: 2
      due_date: "2026-03-12T17:00:00-05:00"
      dependencies: ["T6.1"]
      
    # M7 Tasks - Materials Distribution
    - task_id: "T7.1"
      milestone_id: "M7"
      name: "Finalize Compliance Review Packet"
      description: "Compile: management assessment, control summary, remediation plans, auditor report, certifications"
      owner: "Chief Compliance Officer"
      estimated_hours: 10
      due_date: "2026-03-13T17:00:00-05:00"
      dependencies: ["T6.2"]
      
    - task_id: "T7.2"
      milestone_id: "M7"
      name: "Distribute Materials to Attendees"
      description: "Send packet to all 8 attendees, confirm receipt"
      owner: "Chief Compliance Officer"
      estimated_hours: 2
      due_date: "2026-03-14T17:00:00-05:00"
      dependencies: ["T7.1"]
      
    # M8 Tasks - Meeting Preparation
    - task_id: "T8.1"
      milestone_id: "M8"
      name: "Setup Meeting Logistics"
      description: "Configure room for hybrid meeting, set up audit system access"
      owner: "Admin + IT"
      estimated_hours: 3
      due_date: "2026-03-15T13:00:00-05:00"
      dependencies: []
      
    - task_id: "T8.2"
      milestone_id: "M8"
      name: "Prepare CEO/CFO Certification Signing Ceremony"
      description: "Have certifications ready for signature post-meeting if approved"
      owner: "General Counsel"
      estimated_hours: 2
      due_date: "2026-03-15T13:00:00-05:00"
      dependencies: ["T7.2"]

  risks:
    - risk_id: "R1"
      description: "Material weakness identified during testing, requiring 'Not Effective' conclusion"
      probability: "low"
      impact: "critical"
      mitigation: "Quarterly testing to catch issues early; if material weakness found, accelerate remediation and request auditor re-test; disclosure protocol: Form 8-K within 4 days, investor call"
      owner: "Chief Compliance Officer"
      
    - risk_id: "R2"
      description: "External auditor disagrees with management's assessment or control conclusions"
      probability: "low"
      impact: "high"
      mitigation: "Early and frequent auditor engagement; resolve differences before meeting; escalate to CFO/Audit Committee if unresolved; auditor has final say on opinion"
      owner: "CFO"
      
    - risk_id: "R3"
      description: "Control testing evidence insufficient or missing"
      probability: "medium"
      impact: "high"
      mitigation: "Evidence collection checklist for each control; weekly testing status review; compensating controls documented if primary evidence unavailable; auditor consultation on evidence sufficiency"
      owner: "Internal Audit"
      
    - risk_id: "R4"
      description: "Remediation plans deemed inadequate by Audit Committee or auditor"
      probability: "low"
      impact: "medium"
      mitigation: "Root cause analysis for each deficiency; auditor review of remediation plans pre-meeting; Audit Committee Chair pre-brief to surface concerns early; escalation paths defined"
      owner: "Control Owners"
      
    - risk_id: "R5"
      description: "Testing timeline slips, insufficient time for remediation planning"
      probability: "medium"
      impact: "medium"
      mitigation: "Weekly testing status tracking; red/yellow/green status by control; reallocate resources to at-risk areas; compress remediation planning if needed (can finalize post-meeting with 30-day follow-up)"
      owner: "Chief Compliance Officer"

  quality_checks:
    - check_id: "Q1"
      name: "Control Universe Completeness"
      description: "All key financial processes covered by ≥1 control"
      checkpoint: "M1"
      pass_criteria: "127 controls documented; external auditor agrees scope is complete"
      
    - check_id: "Q2"
      name: "Testing Evidence Quality"
      description: "All control tests have supporting evidence meeting auditor standards"
      checkpoint: "M2"
      pass_criteria: "100% of key controls have evidence; ≥90% of non-key controls"
      
    - check_id: "Q3"
      name: "Deficiency Classification Accuracy"
      description: "Deficiencies correctly classified (material, significant, control)"
      checkpoint: "M2"
      pass_criteria: "Internal Audit and external auditor agree on classification for all deficiencies"
      
    - check_id: "Q4"
      name: "Remediation Plan Adequacy"
      description: "Each deficiency has actionable remediation plan"
      checkpoint: "M3"
      pass_criteria: "All plans include: root cause, corrective action, owner, timeline, validation method"
      
    - check_id: "Q5"
      name: "Management Assessment Conclusion Supportability"
      description: "Assessment conclusion (Effective/Not Effective) supported by test results"
      checkpoint: "M4"
      pass_criteria: "0 material weaknesses = Effective; ≥1 material weakness = Not Effective; conclusion documented with supporting evidence"
      
    - check_id: "Q6"
      name: "External Auditor Alignment"
      description: "External auditor opinion aligns with management assessment"
      checkpoint: "M5"
      pass_criteria: "No material disagreements between management and auditor on control effectiveness"
      
    - check_id: "Q7"
      name: "Audit Committee Chair Approval"
      description: "Audit Committee Chair pre-briefed and comfortable with assessment"
      checkpoint: "M6"
      pass_criteria: "Chair approves proceeding with full committee review; no surprises on meeting day"

  metadata:
    total_estimated_hours: 945
    critical_path_days: 90
    number_of_dependencies: 22
    regulatory_framework: "SOX Section 404"
    number_of_controls: 127
    external_auditor: "KPMG LLP"
    key_stakeholders: ["CEO", "CFO", "CTO", "Chief Compliance Officer", "General Counsel", "Audit Committee", "External Auditor", "Internal Audit"]
    success_indicators:
      - "0 material weaknesses identified"
      - "Unqualified auditor opinion on management's assessment"
      - "CEO/CFO certifications signed (SOX 302)"
      - "All deficiencies have approved remediation plans"
      - "Audit Committee approval of compliance status"

```

**Why This is a Good Workback Plan**:
- ✅ **90-day timeline** allows comprehensive control testing (127 controls) and remediation planning
- ✅ **Systematic control universe**: All 127 financial controls documented, risk-assessed, scoped
- ✅ **Rigorous testing methodology**: 100% key controls, ≥90% non-key controls, evidence standards
- ✅ **Deficiency classification framework**: Material weakness, significant deficiency, control deficiency
- ✅ **Remediation plans** with root cause analysis, corrective actions, timelines, validation
- ✅ **External auditor engagement** throughout (testing plan review, draft assessment review, independent fieldwork)
- ✅ **Audit Committee pre-briefing** ≥3 days before meeting prevents surprises
- ✅ **CEO/CFO certifications** prepared (SOX 302 requirement)
- ✅ **Quality checks** enforce evidence standards and classification accuracy
- ✅ **Risk mitigation** for material weakness discovery, auditor disagreement, evidence gaps

---

### Example B: Bad Workback Plan

```yaml
workback_plan:
  meeting_title: "Compliance Meeting"
  meeting_date: "2026-03-15T14:00:00-05:00"
  meeting_duration_minutes: 180
  organizer: "Compliance"
  compliance_framework: "SOX"
  fiscal_year: "2025"
  complexity: "medium"
  
  milestones:
    - milestone_id: "M1"
      name: "Do compliance stuff"
      due_date: "2026-03-10T17:00:00-05:00"
      days_before_meeting: 5
      description: "Check controls"
      success_criteria:
        - "Controls look okay"
      dependencies: []
      owner: "Compliance team"
      
    - milestone_id: "M2"
      name: "Prepare for meeting"
      due_date: "2026-03-14T17:00:00-05:00"
      days_before_meeting: 1
      description: "Make slides"
      success_criteria:
        - "Slides done"
      dependencies: ["M1"]
      owner: "Compliance"

  tasks:
    - task_id: "T1"
      milestone_id: "M1"
      name: "Test some controls"
      description: "Check if things are working"
      owner: "Audit"
      estimated_hours: null
      due_date: "2026-03-08T17:00:00-05:00"
      dependencies: []
      
    - task_id: "T2"
      milestone_id: "M1"
      name: "Talk to auditor"
      description: "Call the audit firm"
      owner: "Someone"
      estimated_hours: null
      due_date: "2026-03-10T17:00:00-05:00"
      dependencies: []
      
    - task_id: "T3"
      milestone_id: "M2"
      name: "Create presentation"
      description: "Make PowerPoint saying we're compliant"
      owner: "Compliance"
      estimated_hours: null
      due_date: "2026-03-14T17:00:00-05:00"
      dependencies: ["T1", "T2"]

  risks:
    - risk_id: "R1"
      description: "Might find problems"
      probability: "unknown"
      impact: "bad"
      mitigation: "Fix them"
      owner: "Team"

  quality_checks:
    - check_id: "Q1"
      name: "Compliance seems fine"
      description: "Check if compliant"
      checkpoint: "M1"
      pass_criteria: "Looks good"

  metadata:
    total_estimated_hours: null
    critical_path_days: 5
    number_of_dependencies: 1
    regulatory_framework: "SOX"
    key_stakeholders: ["CFO", "Auditor"]
    success_indicators:
      - "Meeting happens"
      - "Pass audit"
```

**Why This is a Bad Workback Plan**:
- ❌ **Only 5-day timeline** - SOX 404 testing requires 8+ weeks for 100+ controls
- ❌ **No control universe defined** - "test some controls" vs. systematic 127-control framework
- ❌ **No testing methodology** - no sample sizes, evidence requirements, deficiency classification
- ❌ **Vague success criteria** ("controls look okay", "looks good") vs. 0 material weaknesses standard
- ❌ **No remediation planning** - deficiencies not addressed
- ❌ **Minimal auditor engagement** - "call the audit firm" vs. testing plan review, fieldwork, opinion
- ❌ **No Audit Committee pre-brief** - leadership blindsided on meeting day
- ❌ **No CEO/CFO certifications** - missing SOX 302 requirement
- ❌ **No evidence standards** - audit failure risk if evidence insufficient
- ❌ **62% of compliance violations** traced to inadequate preparation (Deloitte Compliance Survey)
- ❌ **Material weakness = stock price drop** (avg 3-7% on disclosure day, Audit Analytics)

---

### ACRUE Assertions for Regulatory/Compliance Review Workback Plans

#### Critical Assertions (Must Pass)

**Accuracy Dimension**:
- text: "The workback plan includes complete control universe documentation (all key financial controls identified and risk-assessed)"
  - level: critical
  - dimension: Accuracy
  - rationale: "SOX 404 requires management assessment of ALL internal controls; incomplete control universe = audit failure"

- text: "Plan specifies systematic testing of 100% of key controls with documented evidence"
  - level: critical
  - dimension: Accuracy
  - rationale: "Key controls must be tested at 100% frequency; sampling only for non-key controls"

- text: "Timeline allows ≥60 days for control testing phase (evidence collection, deficiency identification)"
  - level: critical
  - dimension: Accuracy
  - rationale: "Testing 100+ controls requires 8-12 weeks; <60 days = insufficient evidence, rushed assessment"

**Completeness Dimension**:
- text: "Plan includes deficiency classification framework (material weakness, significant deficiency, control deficiency)"
  - level: critical
  - dimension: Completeness
  - rationale: "SOX requires severity classification; material weakness triggers 'Not Effective' conclusion and 8-K disclosure"

- text: "Milestones specify remediation plan development for all identified deficiencies"
  - level: critical
  - dimension: Completeness
  - rationale: "Remediation plans demonstrate management commitment; Audit Committee requires corrective action plans"

- text: "Tasks include external auditor testing plan review and fieldwork coordination"
  - level: critical
  - dimension: Completeness
  - rationale: "External auditor must test management's assessment; auditor fieldwork coordination prevents delays"

**Relevance Dimension**:
- text: "Success criteria measure compliance outcomes (0 material weaknesses, unqualified auditor opinion, CEO/CFO certifications signed) not just task completion"
  - level: critical
  - dimension: Relevance
  - rationale: "Compliance success is regulatory outcome, not just completing activities"

#### Expected Assertions (Should Pass)

**Usefulness Dimension**:
- text: "Plan includes Audit Committee Chair pre-briefing ≥3 days before full committee review"
  - level: expected
  - dimension: Usefulness
  - rationale: "Audit Committee oversight is critical; pre-briefs prevent surprises and enable productive discussions"

- text: "Tasks specify evidence quality standards (e.g., system reports, approval signatures, reconciliations) meeting auditor requirements"
  - level: expected
  - dimension: Usefulness
  - rationale: "Insufficient evidence is leading cause of adverse auditor opinions; evidence standards prevent rework"

- text: "Quality checks validate deficiency classification accuracy with external auditor agreement"
  - level: expected
  - dimension: Usefulness
  - rationale: "Management-auditor disagreement on severity stalls assessments; classification alignment is critical"

**Completeness Dimension**:
- text: "Plan includes CEO/CFO certification preparation (SOX 302 requirements)"
  - level: expected
  - dimension: Completeness
  - rationale: "SOX 302 certifications are regulatory requirement; must be prepared and ready for signature"

- text: "Milestones specify management assessment report drafting with conclusion (Effective/Not Effective)"
  - level: expected
  - dimension: Completeness
  - rationale: "Management assessment is deliverable; conclusion must be supportable by test results"

**Accuracy Dimension**:
- text: "Risk mitigation addresses material weakness discovery scenario (disclosure protocol, investor communication)"
  - level: expected
  - dimension: Accuracy
  - rationale: "Material weakness = Form 8-K within 4 days; disclosure plan prevents compliance violation"

#### Aspirational Assertions (Nice to Have)

**Exceptional Dimension**:
- text: "Plan tracks control testing completion % weekly as leading indicator of timeline risk"
  - level: aspirational
  - dimension: Exceptional
  - rationale: "Weekly tracking enables early intervention; prevents last-minute scrambles"

- text: "Metadata documents prior year deficiencies and remediation status for trend analysis"
  - level: aspirational
  - dimension: Exceptional
  - rationale: "Trend analysis shows improvement or deterioration; informs Audit Committee on control environment health"

**Usefulness Dimension**:
- text: "Success indicators measure remediation effectiveness (% deficiencies closed, time to remediate) not just plan approval"
  - level: aspirational
  - dimension: Usefulness
  - rationale: "Compliance is ongoing; remediation execution matters, not just planning"

- text: "Plan includes audit management system access for evidence review during meeting"
  - level: aspirational
  - dimension: Usefulness
  - rationale: "Real-time evidence review resolves questions faster than digging through files"

---

### ACRUE Rubrics for Regulatory/Compliance Review Workback Plans

#### Accuracy Rubric

**Measures**: Realistic timelines, complete control coverage, validated evidence standards

- **Gold Standard (9-10 points)**:
  - ≥90-day timeline from planning to review meeting
  - Complete control universe (all key financial processes, 100+ controls typical)
  - 100% of key controls tested with documented evidence
  - ≥90% of non-key controls tested
  - External auditor agreement on control scope and testing methodology
  - Deficiency classification framework (material/significant/control)
  - Evidence standards documented and auditor-validated
  - Audit Committee Chair pre-briefed ≥3 days before meeting
  - All assumptions validated through testing or auditor consultation

- **Silver Standard (7-8 points)**:
  - ≥60-day timeline
  - Major controls identified
  - ≥80% of key controls tested
  - External auditor engaged
  - Deficiency classification present
  - Evidence collected
  - Audit Committee involvement

- **Bronze Standard (5-6 points)**:
  - ≥30-day timeline
  - Some control testing
  - Basic evidence collection
  - Auditor contacted
  - Deficiencies tracked

- **Fails Standard (<5 points)**:
  - <30-day timeline
  - No systematic control testing
  - No evidence standards
  - No auditor coordination
  - No deficiency classification

#### Completeness Rubric

**Measures**: Coverage of all SOX 404 compliance workstreams

- **Gold Standard (9-10 points)**:
  - Control universe documentation (all key controls, risk assessment)
  - Testing plan (sample sizes, procedures, evidence requirements)
  - Control testing execution (finance, IT, operations controls)
  - Evidence documentation (audit management system)
  - Deficiency identification and classification
  - Remediation plan development (root cause, corrective action, timeline)
  - Management assessment report (conclusion, controls, deficiencies)
  - External auditor fieldwork coordination
  - CEO/CFO certification preparation (SOX 302)
  - Audit Committee pre-briefing
  - Meeting materials (assessment, control summary, remediation plans, auditor report)
  - Post-meeting actions (certification signing, 8-K filing if needed)

- **Silver Standard (7-8 points)**:
  - Control identification
  - Testing plan
  - Control testing
  - Evidence collection
  - Deficiency tracking
  - Remediation planning
  - Management assessment
  - Auditor engagement
  - Audit Committee briefing

- **Bronze Standard (5-6 points)**:
  - Some control testing
  - Evidence collected
  - Deficiencies noted
  - Auditor contacted
  - Basic reporting

- **Fails Standard (<5 points)**:
  - No systematic testing
  - No evidence framework
  - No deficiency management
  - No auditor coordination
  - No reporting structure

#### Relevance Rubric

**Measures**: Focus on regulatory compliance requirements vs. generic project management

- **Gold Standard (9-10 points)**:
  - All milestones tied to SOX 404 requirements (control assessment, testing, management conclusion, auditor opinion)
  - Success criteria measure compliance outcomes (0 material weaknesses, unqualified opinion, certifications signed)
  - Risks address compliance-specific failures (material weakness, auditor disagreement, evidence gaps, 8-K disclosure)
  - Quality checks enforce regulatory standards (control coverage, evidence quality, deficiency classification)
  - Decision framework based on assessment conclusion (Effective/Not Effective), not arbitrary criteria

- **Silver Standard (7-8 points)**:
  - Most milestones compliance-relevant
  - Success criteria mostly regulatory
  - Risks include compliance concerns
  - Quality checks present
  - Decision criteria defined

- **Bronze Standard (5-6 points)**:
  - Milestones include compliance activities
  - Some regulatory criteria
  - Generic risks
  - Basic quality checks

- **Fails Standard (<5 points)**:
  - Generic project milestones
  - Vague criteria ("looks compliant")
  - Risks unrelated to compliance
  - No regulatory enforcement

#### Usefulness Rubric

**Measures**: Actionability for compliance team and stakeholders

- **Gold Standard (9-10 points)**:
  - All tasks have named owners (specific roles: Internal Audit, CFO, CTO, Control Owners)
  - Time estimates enable capacity planning (900+ hours typical for 100+ controls)
  - Control testing procedures documented with evidence requirements
  - Deficiency classification criteria specified (material/significant/control)
  - Remediation plan template (root cause, action, owner, timeline, validation)
  - Audit Committee briefing agenda and materials
  - External auditor coordination schedule
  - Management assessment report template
  - CEO/CFO certification forms (SOX 302)
  - Evidence quality standards (system reports, signatures, reconciliations)

- **Silver Standard (7-8 points)**:
  - Most tasks have named owners
  - Time estimates for major workstreams
  - Testing procedures defined
  - Deficiency classification framework
  - Remediation planning
  - Audit Committee briefing scheduled
  - Auditor engaged
  - Assessment template

- **Bronze Standard (5-6 points)**:
  - Some specific owners
  - Basic timeline
  - Testing approach described
  - Deficiencies tracked
  - Auditor contacted
  - Reporting planned

- **Fails Standard (<5 points)**:
  - Vague owners ("team", "compliance")
  - No time estimates
  - No testing framework
  - No deficiency management
  - No auditor coordination
  - No reporting structure

#### Exceptional Rubric

**Measures**: Advanced compliance practices that minimize regulatory risk

- **Gold Standard (9-10 points)**:
  - Control testing completion % tracked weekly (leading indicator)
  - Prior year deficiencies tracked with remediation status (trend analysis)
  - Evidence sufficiency validated with auditor before final testing
  - Root cause analysis for all deficiencies (prevents recurrence)
  - Remediation effectiveness metrics (% closed, time to remediate)
  - Audit management system for centralized evidence and collaboration
  - Quarterly control testing (vs. annual) to catch issues early
  - Material weakness disclosure protocol (Form 8-K, investor call, press release)
  - Benchmarking with industry peers (deficiency rates, control maturity)

- **Silver Standard (7-8 points)**:
  - Testing progress tracked
  - Prior year deficiencies reviewed
  - Evidence validation
  - Root cause analysis
  - Remediation tracking
  - Audit system used
  - Disclosure planning

- **Bronze Standard (5-6 points)**:
  - Some progress tracking
  - Deficiency history reviewed
  - Evidence collected
  - Remediation planned

- **Fails Standard (<5 points)**:
  - No progress tracking
  - No trend analysis
  - No evidence validation
  - No root cause analysis

---

### Distribution for Compliance Review Assertions

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

**Key Insight**: Organizations with structured SOX 404 workback plans (≥90 days, 100% key control testing, systematic evidence collection) reduce compliance violations by 62% (Deloitte Compliance Survey). Material weaknesses cost companies an average $9.4M in remediation, stock price impact, and regulatory costs. The 90-day timeline in the good example enables systematic control testing, deficiency remediation, and external auditor coordination—preventing the rushed, incomplete assessments that lead to adverse opinions and restatements.

