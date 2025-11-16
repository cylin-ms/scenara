# Workback Plan Examples and ACRUE Evaluation - Part 7

**Meeting Type**: M&A Deal Review  
**Author**: Chin-Yew Lin  
**Created**: November 13, 2025

---

## 7. M&A Deal Review Meeting

### Meeting Context

- **Meeting Type**: Board of Directors M&A Approval Meeting
- **Target Date**: March 20, 2026, 9:00 AM - 3:00 PM PT (Board retreat format)
- **Organizer**: Chief Executive Officer
- **Attendees**: Board of Directors (9 members), CEO, CFO, General Counsel, Head of Corp Dev, M&A Advisors (Goldman Sachs, Skadden Arps)
- **Objective**: Board approval to acquire DataFlow Analytics for $385M cash + stock, strategic rationale review, integration planning
- **Deal Context**: DataFlow = AI-powered data governance platform, $42M revenue, 180 customers, strategic fit for enterprise AI expansion
- **Transaction**: $385M ($270M cash + $115M stock), 12x revenue multiple, ~18 months due diligence, definitive agreement signed subject to Board approval

---

### Example A: Good Workback Plan

```yaml
workback_plan:
  meeting_title: "Board Approval: DataFlow Analytics Acquisition"
  meeting_date: "2026-03-20T09:00:00-08:00"
  meeting_duration_minutes: 360
  organizer: "David Kim, Chief Executive Officer"
  deal_type: "Strategic Acquisition"
  target_company: "DataFlow Analytics, Inc."
  deal_value: "$385M ($270M cash + $115M stock)"
  revenue_multiple: "12x trailing revenue"
  target_revenue: "$42M (2025)"
  complexity: "very_high"
  
  milestones:
    - milestone_id: "M1"
      name: "Due Diligence Workstreams Complete"
      due_date: "2026-01-31T17:00:00-08:00"
      days_before_meeting: 49
      description: "All financial, legal, technical, commercial due diligence complete"
      success_criteria:
        - "Financial DD: 3-year audited financials, revenue quality, GAAP compliance, working capital"
        - "Legal DD: Cap table clean, no litigation, IP ownership verified, customer contracts reviewed"
        - "Technical DD: Product architecture assessed, tech debt quantified, security audit complete"
        - "Commercial DD: Customer retention 92%, NPS 48, pipeline validated, competitive positioning"
        - "All red flags resolved or mitigation plans documented"
      dependencies: []
      owner: "Head of Corp Dev + Goldman Sachs"
      
    - milestone_id: "M2"
      name: "Valuation and Deal Structure Finalized"
      due_date: "2026-02-10T17:00:00-08:00"
      days_before_meeting: 38
      description: "$385M valuation justified, cash/stock mix optimized, earn-out structure agreed"
      success_criteria:
        - "Valuation: 12x 2025 revenue ($42M), justified by 40% growth, 92% retention, strategic fit"
        - "Comparable transactions: 10-15x revenue for similar SaaS acquisitions"
        - "Deal structure: $270M cash (70%) + $115M stock (30%) to retain key team"
        - "Earn-out: $25M performance-based earn-out over 2 years (revenue + retention targets)"
        - "Board Committee (M&A) preliminary approval of valuation"
      dependencies: ["M1"]
      owner: "CFO + Goldman Sachs"
      
    - milestone_id: "M3"
      name: "Integration Plan Developed"
      due_date: "2026-02-24T17:00:00-08:00"
      days_before_meeting: 24
      description: "Day 1-100 integration plan with workstreams, owners, milestones"
      success_criteria:
        - "Integration leadership: VP Integration appointed, cross-functional team formed"
        - "Day 1 plan: IT systems, payroll, benefits, communication, customer outreach"
        - "100-day plan: Product roadmap integration, sales team onboarding, support consolidation"
        - "Synergy targets: $8M cost synergies (facilities, G&A), $15M revenue synergies (cross-sell)"
        - "Retention plan: 85% key employee retention target, retention bonuses, equity grants"
        - "Customer retention plan: 90% customer retention target, customer success outreach"
      dependencies: ["M2"]
      owner: "VP Integration + Head of Corp Dev"
      
    - milestone_id: "M4"
      name: "Financing and Cap Table Impact Assessed"
      due_date: "2026-02-28T17:00:00-08:00"
      days_before_meeting: 20
      description: "Financing sources secured, shareholder dilution calculated, credit facility amended"
      success_criteria:
        - "Cash financing: $270M from cash on hand ($180M) + credit facility draw ($90M)"
        - "Stock financing: 1.8M shares issued (4.2% dilution), Board approval required"
        - "Credit facility: $150M revolver amended to allow $90M draw for acquisition"
        - "Pro forma financials: Combined company $529M revenue (2026E), 15% EBITDA margin"
        - "Shareholder dilution analysis: EPS accretion 5% Year 2, 12% Year 3"
      dependencies: ["M2"]
      owner: "CFO + Treasurer"
      
    - milestone_id: "M5"
      name: "Legal and Regulatory Review Complete"
      due_date: "2026-03-05T17:00:00-08:00"
      days_before_meeting: 15
      description: "Definitive agreement negotiated, regulatory approvals assessed, HSR filing prepared"
      success_criteria:
        - "Definitive agreement: Purchase agreement, employment agreements, escrow terms, reps & warranties"
        - "HSR filing: Hart-Scott-Rodino filing prepared (>$111.4M threshold), FTC review 30 days"
        - "Regulatory risk: Low antitrust risk (combined <5% market share), no foreign ownership issues"
        - "Break-up fee: $15M if deal terminated by buyer, $20M if terminated by seller"
        - "Closing conditions: Board approval, shareholder approval (not required), HSR clearance, no MAE"
      dependencies: ["M1", "M2"]
      owner: "General Counsel + Skadden Arps"
      
    - milestone_id: "M6"
      name: "Board Committee Pre-Reviews Complete"
      due_date: "2026-03-10T17:00:00-08:00"
      days_before_meeting: 10
      description: "M&A Committee and Audit Committee pre-review key aspects"
      success_criteria:
        - "M&A Committee: 2-hour session reviewing strategic rationale, valuation, integration plan"
        - "Audit Committee: Financial DD review, accounting policies, internal controls assessment"
        - "Committee feedback incorporated into Board materials"
        - "No major concerns raised that would block Board approval"
      dependencies: ["M3", "M4", "M5"]
      owner: "CEO + CFO + Head of Corp Dev"
      
    - milestone_id: "M7"
      name: "Board Materials Distributed"
      due_date: "2026-03-17T17:00:00-08:00"
      days_before_meeting: 3
      description: "Comprehensive Board packet with all deal materials"
      success_criteria:
        - "Board memo: Strategic rationale, valuation, financing, integration, risks (25 pages)"
        - "Due diligence summary: Financial, legal, technical, commercial findings (40 pages)"
        - "Integration plan: Day 1-100 plan, synergy targets, retention plans (15 pages)"
        - "Definitive agreement: Redlined purchase agreement (120 pages)"
        - "Fairness opinion: Goldman Sachs fairness opinion ($385M is fair from financial POV)"
        - "Resolutions: Board approval resolutions for execution"
      dependencies: ["M6"]
      owner: "General Counsel + Head of Corp Dev"
      
    - milestone_id: "M8"
      name: "Board Approval Meeting Ready"
      due_date: "2026-03-20T08:00:00-08:00"
      days_before_meeting: 0
      description: "All logistics and decision materials prepared"
      success_criteria:
        - "Meeting setup: 6-hour Board retreat format (9 AM - 3 PM)"
        - "Agenda: Strategic rationale (CEO 30 min), Valuation (CFO 30 min), DD findings (Corp Dev 45 min), Integration (VP Integration 30 min), Legal (GC 30 min), Goldman/Skadden presentations (60 min), Board Q&A (120 min), Vote"
        - "Voting: Simple majority required (5/9), expect 8-9 yes votes"
        - "Post-approval actions: Sign definitive agreement, issue press release, file HSR, investor call"
      dependencies: ["M7"]
      owner: "CEO + Board Secretary"

  tasks:
    # M1 Tasks - Due Diligence
    - task_id: "T1.1"
      milestone_id: "M1"
      name: "Execute Financial Due Diligence"
      description: "3-year audited financials, revenue quality, working capital, GAAP compliance"
      owner: "CFO + Goldman Sachs + Accounting Firm"
      estimated_hours: 200
      due_date: "2026-01-20T17:00:00-08:00"
      dependencies: []
      
    - task_id: "T1.2"
      milestone_id: "M1"
      name: "Execute Legal Due Diligence"
      description: "Cap table, litigation, IP, contracts, regulatory compliance"
      owner: "General Counsel + Skadden Arps"
      estimated_hours: 180
      due_date: "2026-01-22T17:00:00-08:00"
      dependencies: []
      
    - task_id: "T1.3"
      milestone_id: "M1"
      name: "Execute Technical Due Diligence"
      description: "Product architecture, tech stack, scalability, security, tech debt"
      owner: "CTO + Technical Advisors"
      estimated_hours: 120
      due_date: "2026-01-25T17:00:00-08:00"
      dependencies: []
      
    - task_id: "T1.4"
      milestone_id: "M1"
      name: "Execute Commercial Due Diligence"
      description: "Customer retention, pipeline, competitive position, pricing, NPS"
      owner: "Head of Corp Dev + Commercial DD Firm"
      estimated_hours: 100
      due_date: "2026-01-28T17:00:00-08:00"
      dependencies: []
      
    - task_id: "T1.5"
      milestone_id: "M1"
      name: "Compile Due Diligence Summary"
      description: "Aggregate DD findings, identify red flags, recommend mitigation"
      owner: "Head of Corp Dev"
      estimated_hours: 40
      due_date: "2026-01-31T17:00:00-08:00"
      dependencies: ["T1.1", "T1.2", "T1.3", "T1.4"]
      
    # M2 Tasks - Valuation
    - task_id: "T2.1"
      milestone_id: "M2"
      name: "Build Valuation Model"
      description: "DCF analysis, comparable transactions, revenue multiples"
      owner: "CFO + Goldman Sachs"
      estimated_hours: 60
      due_date: "2026-02-05T17:00:00-08:00"
      dependencies: ["T1.5"]
      
    - task_id: "T2.2"
      milestone_id: "M2"
      name: "Negotiate Deal Structure"
      description: "Cash/stock mix, earn-out, escrow, break-up fee"
      owner: "CEO + CFO + General Counsel"
      estimated_hours: 80
      due_date: "2026-02-08T17:00:00-08:00"
      dependencies: ["T2.1"]
      
    - task_id: "T2.3"
      milestone_id: "M2"
      name: "Obtain Goldman Sachs Fairness Opinion"
      description: "Goldman issues fairness opinion: $385M is fair from financial POV"
      owner: "Goldman Sachs + CFO"
      estimated_hours: 40
      due_date: "2026-02-10T17:00:00-08:00"
      dependencies: ["T2.2"]
      
    # M3 Tasks - Integration Planning
    - task_id: "T3.1"
      milestone_id: "M3"
      name: "Appoint Integration Leadership"
      description: "Select VP Integration, form cross-functional integration team"
      owner: "CEO + Head of Corp Dev"
      estimated_hours: 20
      due_date: "2026-02-12T17:00:00-08:00"
      dependencies: ["T2.3"]
      
    - task_id: "T3.2"
      milestone_id: "M3"
      name: "Develop Day 1 Integration Plan"
      description: "IT, payroll, benefits, communication, customer outreach"
      owner: "VP Integration + Integration Team"
      estimated_hours: 80
      due_date: "2026-02-18T17:00:00-08:00"
      dependencies: ["T3.1"]
      
    - task_id: "T3.3"
      milestone_id: "M3"
      name: "Develop 100-Day Integration Plan"
      description: "Product, sales, support, operations integration"
      owner: "VP Integration + Integration Team"
      estimated_hours: 100
      due_date: "2026-02-22T17:00:00-08:00"
      dependencies: ["T3.2"]
      
    - task_id: "T3.4"
      milestone_id: "M3"
      name: "Build Synergy Models"
      description: "Quantify cost synergies ($8M) and revenue synergies ($15M)"
      owner: "CFO + VP Integration"
      estimated_hours: 40
      due_date: "2026-02-24T17:00:00-08:00"
      dependencies: ["T3.3"]
      
    # M4 Tasks - Financing
    - task_id: "T4.1"
      milestone_id: "M4"
      name: "Secure Cash Financing"
      description: "Allocate $180M cash on hand, negotiate $90M credit facility draw"
      owner: "CFO + Treasurer"
      estimated_hours: 30
      due_date: "2026-02-20T17:00:00-08:00"
      dependencies: ["T2.3"]
      
    - task_id: "T4.2"
      milestone_id: "M4"
      name: "Calculate Stock Consideration"
      description: "1.8M shares at $64/share = $115M, 4.2% dilution"
      owner: "CFO"
      estimated_hours: 12
      due_date: "2026-02-22T17:00:00-08:00"
      dependencies: ["T2.3"]
      
    - task_id: "T4.3"
      milestone_id: "M4"
      name: "Build Pro Forma Financials"
      description: "Combined company revenue, EBITDA, EPS accretion/dilution"
      owner: "CFO + FP&A"
      estimated_hours: 50
      due_date: "2026-02-28T17:00:00-08:00"
      dependencies: ["T4.1", "T4.2", "T3.4"]
      
    # M5 Tasks - Legal
    - task_id: "T5.1"
      milestone_id: "M5"
      name: "Negotiate Definitive Agreement"
      description: "Purchase agreement, reps & warranties, indemnification, escrow"
      owner: "General Counsel + Skadden Arps + Seller's Counsel"
      estimated_hours: 150
      due_date: "2026-02-28T17:00:00-08:00"
      dependencies: ["T2.2"]
      
    - task_id: "T5.2"
      milestone_id: "M5"
      name: "Prepare HSR Filing"
      description: "Hart-Scott-Rodino filing for FTC/DOJ antitrust review"
      owner: "Skadden Arps + General Counsel"
      estimated_hours: 40
      due_date: "2026-03-03T17:00:00-08:00"
      dependencies: ["T5.1"]
      
    - task_id: "T5.3"
      milestone_id: "M5"
      name: "Assess Regulatory Risks"
      description: "Antitrust analysis, foreign ownership, industry regulations"
      owner: "Skadden Arps + General Counsel"
      estimated_hours: 30
      due_date: "2026-03-05T17:00:00-08:00"
      dependencies: ["T5.2"]
      
    # M6 Tasks - Committee Reviews
    - task_id: "T6.1"
      milestone_id: "M6"
      name: "M&A Committee Review Session"
      description: "2-hour committee review: strategic rationale, valuation, integration"
      owner: "CEO + CFO + Head of Corp Dev + M&A Committee"
      estimated_hours: 8
      due_date: "2026-03-08T17:00:00-08:00"
      dependencies: ["T3.4", "T4.3", "T5.3"]
      
    - task_id: "T6.2"
      milestone_id: "M6"
      name: "Audit Committee Financial Review"
      description: "2-hour committee review: financial DD, accounting policies, controls"
      owner: "CFO + General Counsel + Audit Committee"
      estimated_hours: 6
      due_date: "2026-03-10T17:00:00-08:00"
      dependencies: ["T1.1", "T4.3"]
      
    # M7 Tasks - Board Materials
    - task_id: "T7.1"
      milestone_id: "M7"
      name: "Draft Board Memo"
      description: "25-page memo: strategic rationale, valuation, financing, integration, risks"
      owner: "Head of Corp Dev + General Counsel"
      estimated_hours: 40
      due_date: "2026-03-14T17:00:00-08:00"
      dependencies: ["T6.1", "T6.2"]
      
    - task_id: "T7.2"
      milestone_id: "M7"
      name: "Compile Board Packet"
      description: "200+ page packet: memo, DD summary, integration plan, agreement, fairness opinion, resolutions"
      owner: "Board Secretary + Head of Corp Dev"
      estimated_hours: 20
      due_date: "2026-03-16T17:00:00-08:00"
      dependencies: ["T7.1"]
      
    - task_id: "T7.3"
      milestone_id: "M7"
      name: "Distribute Board Materials"
      description: "Send packet to all 9 Board members, confirm receipt"
      owner: "Board Secretary"
      estimated_hours: 2
      due_date: "2026-03-17T17:00:00-08:00"
      dependencies: ["T7.2"]
      
    # M8 Tasks - Meeting Preparation
    - task_id: "T8.1"
      milestone_id: "M8"
      name: "Finalize Meeting Agenda and Logistics"
      description: "6-hour retreat format, presentations, Q&A, voting procedure"
      owner: "Board Secretary + CEO"
      estimated_hours: 10
      due_date: "2026-03-19T17:00:00-08:00"
      dependencies: ["T7.3"]
      
    - task_id: "T8.2"
      milestone_id: "M8"
      name: "Prepare Goldman/Skadden Presentations"
      description: "Goldman: valuation + fairness opinion (30 min), Skadden: legal review (30 min)"
      owner: "Goldman Sachs + Skadden Arps"
      estimated_hours: 20
      due_date: "2026-03-19T17:00:00-08:00"
      dependencies: ["T7.3"]
      
    - task_id: "T8.3"
      milestone_id: "M8"
      name: "Prepare Post-Approval Action Plan"
      description: "If approved: sign agreement, press release, HSR filing, investor call"
      owner: "General Counsel + Head of Corp Dev + Corporate Comm"
      estimated_hours: 15
      due_date: "2026-03-20T08:00:00-08:00"
      dependencies: ["T8.1"]

  risks:
    - risk_id: "R1"
      description: "Due diligence reveals material red flags (financial irregularities, customer churn spike, IP disputes)"
      probability: "low"
      impact: "critical"
      mitigation: "Comprehensive DD with top-tier advisors; if material red flag found, renegotiate price or walk away; break-up fee $15M acceptable loss vs. bad acquisition; have backup acquisition targets"
      owner: "Head of Corp Dev"
      
    - risk_id: "R2"
      description: "Board does not approve deal (valuation too high, integration risk, strategic misfit)"
      probability: "low"
      impact: "high"
      mitigation: "Early Board Committee engagement (M&A + Audit); incorporate committee feedback; fairness opinion from Goldman; have CEO 1-on-1s with skeptical Board members pre-meeting; if rejected, revisit valuation or strategic rationale"
      owner: "CEO"
      
    - risk_id: "R3"
      description: "HSR antitrust review extends >30 days or FTC/DOJ challenges deal"
      probability: "low"
      impact: "medium"
      mitigation: "Antitrust analysis shows low risk (<5% combined market share); engage antitrust counsel early; have timing contingency (closing 60-90 days post-approval); if challenged, propose divestitures or abandon deal"
      owner: "General Counsel"
      
    - risk_id: "R4"
      description: "Key DataFlow employees or customers defect during deal process"
      probability: "medium"
      impact: "high"
      mitigation: "Confidentiality until Board approval; retention bonuses for 15 key employees ($5M pool); customer success outreach immediately post-announcement; integration team assigned to employee retention; if >20% employee attrition, revisit deal"
      owner: "VP Integration"
      
    - risk_id: "R5"
      description: "Integration fails to deliver synergies ($23M cost + revenue synergies)"
      probability: "medium"
      impact: "high"
      mitigation: "Experienced VP Integration appointed; Day 1-100 plan with milestones; synergy tracking dashboard; integration steering committee with CEO; conservative synergy estimates (50% probability-adjusted); if <50% synergies, escalate to CEO"
      owner: "VP Integration"
      
    - risk_id: "R6"
      description: "Stock price drop post-announcement (market disapproves of valuation or strategic fit)"
      probability: "medium"
      impact: "medium"
      mitigation: "Investor communication plan: press release emphasizing strategic rationale, synergies, accretion; investor call with CEO/CFO; analyst outreach pre-announcement; if stock drops >5%, CEO explains long-term value on call"
      owner: "CFO + Corporate Comm"

  quality_checks:
    - check_id: "Q1"
      name: "Due Diligence Completeness"
      description: "All 4 DD workstreams complete with no unresolved red flags"
      checkpoint: "M1"
      pass_criteria: "Financial, legal, technical, commercial DD complete; red flags resolved or mitigated"
      
    - check_id: "Q2"
      name: "Valuation Justification"
      description: "12x revenue multiple justified by growth, retention, strategic fit"
      checkpoint: "M2"
      pass_criteria: "Comparable transactions 10-15x; fairness opinion from Goldman; M&A Committee approval"
      
    - check_id: "Q3"
      name: "Integration Plan Readiness"
      description: "Day 1-100 integration plan with workstreams, owners, synergy targets"
      checkpoint: "M3"
      pass_criteria: "VP Integration appointed; plan approved by integration steering committee; synergy models validated"
      
    - check_id: "Q4"
      name: "Financing Secured"
      description: "Cash and stock financing arranged with acceptable dilution"
      checkpoint: "M4"
      pass_criteria: "$270M cash available, credit facility amended, 4.2% dilution acceptable, EPS accretion Year 2+"
      
    - check_id: "Q5"
      name: "Legal Agreement Finalized"
      description: "Definitive agreement negotiated, HSR prepared, regulatory risk low"
      checkpoint: "M5"
      pass_criteria: "Agreement signed subject to Board approval, HSR ready to file, antitrust risk <10%"
      
    - check_id: "Q6"
      name: "Board Committee Alignment"
      description: "M&A and Audit Committees comfortable with deal"
      checkpoint: "M6"
      pass_criteria: "Committee reviews complete, no major concerns, feedback incorporated"
      
    - check_id: "Q7"
      name: "Board Materials Distributed On Time"
      description: "Comprehensive Board packet sent ≥3 days before meeting"
      checkpoint: "M7"
      pass_criteria: "200+ page packet distributed, 100% Board receipt confirmed, ≥3 days review time"

  metadata:
    total_estimated_hours: 1343
    critical_path_days: 49
    number_of_dependencies: 28
    deal_value: "$385M"
    target_company: "DataFlow Analytics, Inc."
    target_revenue: "$42M"
    revenue_multiple: "12x"
    external_advisors: ["Goldman Sachs (Financial)", "Skadden Arps (Legal)", "Commercial DD Firm", "Technical Advisors"]
    key_stakeholders: ["Board of Directors", "CEO", "CFO", "General Counsel", "Head of Corp Dev", "VP Integration", "CTO", "Goldman Sachs", "Skadden Arps"]
    success_indicators:
      - "Board approves acquisition (≥5/9 votes)"
      - "Deal closes within 60-90 days (HSR clearance, closing conditions)"
      - "≥85% key employee retention Year 1"
      - "≥90% customer retention Year 1"
      - "≥50% of synergies ($23M) realized within 18 months"
      - "EPS accretion ≥5% Year 2"

```

**Why This is a Good Workback Plan**:
- ✅ **90-day timeline** allows comprehensive due diligence (financial, legal, technical, commercial)
- ✅ **Four DD workstreams** validate all aspects: financials, legal, tech, customers
- ✅ **Valuation rigor**: DCF, comparables, fairness opinion from Goldman Sachs
- ✅ **Integration planning**: Day 1-100 plan with VP Integration, synergy targets ($23M)
- ✅ **Financing secured**: $270M cash + $115M stock, EPS accretion modeled
- ✅ **Legal rigor**: Definitive agreement, HSR filing, regulatory risk assessment
- ✅ **Board Committee pre-reviews** (M&A + Audit) before full Board
- ✅ **Comprehensive Board materials**: 200+ page packet ≥3 days before meeting
- ✅ **Risk mitigation** for DD red flags, Board rejection, antitrust, employee/customer defection, integration failure
- ✅ **Quality checks** enforce DD completeness, valuation justification, legal finalization

---

### Example B: Bad Workback Plan

```yaml
workback_plan:
  meeting_title: "Acquisition Approval"
  meeting_date: "2026-03-20T09:00:00-08:00"
  meeting_duration_minutes: 360
  organizer: "CEO"
  deal_type: "Acquisition"
  target_company: "DataFlow"
  deal_value: "$385M"
  complexity: "medium"
  
  milestones:
    - milestone_id: "M1"
      name: "Check out company"
      due_date: "2026-03-15T17:00:00-08:00"
      days_before_meeting: 5
      description: "Look at their financials"
      success_criteria:
        - "Financials reviewed"
      dependencies: []
      owner: "Corp Dev"
      
    - milestone_id: "M2"
      name: "Prepare for Board"
      due_date: "2026-03-19T17:00:00-08:00"
      days_before_meeting: 1
      description: "Make presentation"
      success_criteria:
        - "Slides done"
      dependencies: ["M1"]
      owner: "CEO"

  tasks:
    - task_id: "T1"
      milestone_id: "M1"
      name: "Review their numbers"
      description: "Check revenue and expenses"
      owner: "Finance"
      estimated_hours: null
      due_date: "2026-03-14T17:00:00-08:00"
      dependencies: []
      
    - task_id: "T2"
      milestone_id: "M1"
      name: "Talk to their CEO"
      description: "Ask about the business"
      owner: "CEO"
      estimated_hours: null
      due_date: "2026-03-15T17:00:00-08:00"
      dependencies: []
      
    - task_id: "T3"
      milestone_id: "M2"
      name: "Create Board deck"
      description: "Make PowerPoint about why we should buy them"
      owner: "Corp Dev"
      estimated_hours: null
      due_date: "2026-03-19T17:00:00-08:00"
      dependencies: ["T1", "T2"]

  risks:
    - risk_id: "R1"
      description: "Board might not approve"
      probability: "unknown"
      impact: "bad"
      mitigation: "Make good presentation"
      owner: "CEO"

  quality_checks:
    - check_id: "Q1"
      name: "Deal looks okay"
      description: "Check if acquisition is good idea"
      checkpoint: "M1"
      pass_criteria: "Seems reasonable"

  metadata:
    total_estimated_hours: null
    critical_path_days: 5
    number_of_dependencies: 1
    deal_value: "$385M"
    key_stakeholders: ["Board", "CEO", "CFO"]
    success_indicators:
      - "Board approves"
      - "Deal closes"
```

**Why This is a Bad Workback Plan**:
- ❌ **Only 5-day timeline** - M&A due diligence requires 60-90 days for financial, legal, technical, commercial workstreams
- ❌ **No systematic due diligence** - "look at financials" vs. 4 DD workstreams with external advisors
- ❌ **No valuation rigor** - no DCF, comparables, fairness opinion from investment bank
- ❌ **No integration planning** - $385M acquisition with no Day 1-100 plan, synergy targets, retention planning
- ❌ **No financing plan** - $385M funding source undefined (cash? stock? debt?)
- ❌ **No legal due diligence** - no definitive agreement, HSR filing, regulatory risk assessment
- ❌ **No Board Committee pre-reviews** - M&A and Audit Committees blindsided
- ❌ **1-day Board materials** - 200+ page packet requires ≥3 days review (governance best practice)
- ❌ **Vague success criteria** ("financials reviewed", "seems reasonable")
- ❌ **No risk mitigation** for DD red flags, integration failure, employee/customer defection
- ❌ **70% of M&A deals fail to create value** (Harvard Business Review); inadequate DD and integration planning are top causes
- ❌ **Board fiduciary duty breach** - insufficient diligence exposes Board to shareholder lawsuits

---

### ACRUE Assertions for M&A Deal Review Workback Plans

#### Critical Assertions (Must Pass)

**Accuracy Dimension**:
- text: "The workback plan includes comprehensive due diligence (financial, legal, technical, commercial) with ≥60 days for execution"
  - level: critical
  - dimension: Accuracy
  - rationale: "M&A due diligence requires deep investigation; <60 days = missed red flags, bad acquisitions, shareholder lawsuits"

- text: "Plan specifies valuation methodology (DCF, comparables) and fairness opinion from investment bank"
  - level: critical
  - dimension: Accuracy
  - rationale: "Board fiduciary duty requires independent valuation; fairness opinion protects against overpayment claims"

- text: "Timeline allows ≥90 days from due diligence start to Board approval for comprehensive analysis"
  - level: critical
  - dimension: Accuracy
  - rationale: "Complex M&A requires DD, valuation, integration planning, legal documentation; <90 days = rushed decisions"

**Completeness Dimension**:
- text: "Plan includes Day 1-100 integration plan with workstreams, owners, synergy targets, retention plans"
  - level: critical
  - dimension: Completeness
  - rationale: "Integration planning prevents post-close failures; 70% of M&A value loss from poor integration"

- text: "Milestones specify definitive agreement negotiation and regulatory filings (HSR, foreign approvals)"
  - level: critical
  - dimension: Completeness
  - rationale: "Legal documentation and regulatory approvals are closing conditions; missing = deal cannot close"

- text: "Tasks include financing plan (cash, stock, debt) with shareholder dilution and EPS accretion analysis"
  - level: critical
  - dimension: Completeness
  - rationale: "Board must understand funding source and shareholder impact; unfunded deals cannot close"

**Relevance Dimension**:
- text: "Success criteria measure deal value creation (synergy realization, customer retention, EPS accretion) not just Board approval"
  - level: critical
  - dimension: Relevance
  - rationale: "M&A success is value creation, not just deal closing; Board approves based on expected outcomes"

#### Expected Assertions (Should Pass)

**Usefulness Dimension**:
- text: "Plan includes Board Committee pre-reviews (M&A Committee, Audit Committee) ≥7 days before full Board"
  - level: expected
  - dimension: Usefulness
  - rationale: "Committee expertise (M&A strategy, financial diligence) improves Board decision quality"

- text: "Tasks specify external advisor engagement (investment bank, law firm, commercial DD firm, technical advisors)"
  - level: expected
  - dimension: Usefulness
  - rationale: "M&A complexity requires specialized expertise; top-tier advisors reduce risk"

- text: "Quality checks validate due diligence completeness (no unresolved red flags) before Board materials distribution"
  - level: expected
  - dimension: Usefulness
  - rationale: "Red flags must be resolved or mitigated before Board decision; surprises derail approvals"

**Completeness Dimension**:
- text: "Plan includes comprehensive Board packet (DD summary, valuation, integration plan, definitive agreement, fairness opinion) distributed ≥3 days before meeting"
  - level: expected
  - dimension: Completeness
  - rationale: "Board fiduciary duty requires informed decision; 200+ page packet needs ≥3 days review time"

- text: "Milestones specify risk assessment for key deal risks (DD red flags, integration failure, employee/customer defection, regulatory challenges)"
  - level: expected
  - dimension: Completeness
  - rationale: "Board must understand risks and mitigations; risk blindness causes failed deals"

**Accuracy Dimension**:
- text: "Risk mitigation addresses Board rejection scenario (renegotiate valuation, revisit strategic rationale, walk away)"
  - level: expected
  - dimension: Accuracy
  - rationale: "Board may not approve; having Plan B prevents desperation decisions"

#### Aspirational Assertions (Nice to Have)

**Exceptional Dimension**:
- text: "Plan tracks comparable M&A transaction multiples to benchmark valuation reasonableness"
  - level: aspirational
  - dimension: Exceptional
  - rationale: "Comparable deals validate valuation; outlier multiples signal overpayment risk"

- text: "Success indicators measure long-term integration outcomes (Year 1 employee retention ≥85%, customer retention ≥90%, synergy capture ≥50%)"
  - level: aspirational
  - dimension: Exceptional
  - rationale: "M&A value realized over 18-24 months; tracking long-term outcomes enables course correction"

**Usefulness Dimension**:
- text: "Metadata documents post-approval action plan (sign agreement, press release, HSR filing, investor communication)"
  - level: aspirational
  - dimension: Usefulness
  - rationale: "Board approval is milestone, not end; post-approval execution plan ensures timely closing"

- text: "Plan includes sensitivity analysis (best/base/worst case scenarios) for synergy realization and EPS accretion"
  - level: aspirational
  - dimension: Usefulness
  - rationale: "Deals rarely achieve 100% of synergies; sensitivity analysis sets realistic expectations"

---

### ACRUE Rubrics for M&A Deal Review Workback Plans

#### Accuracy Rubric

**Measures**: Realistic timelines, comprehensive due diligence, valuation rigor, integration feasibility

- **Gold Standard (9-10 points)**:
  - ≥90-day timeline from due diligence start to Board approval
  - Comprehensive DD: Financial (audited financials, revenue quality, working capital), Legal (cap table, litigation, IP, contracts), Technical (architecture, tech debt, security), Commercial (retention, pipeline, competition, NPS)
  - External advisors: Investment bank (valuation + fairness opinion), law firm (legal DD + agreement), commercial DD firm, technical advisors
  - Valuation: DCF analysis, comparable transactions, revenue multiples, fairness opinion
  - Integration plan: Day 1-100 with VP Integration, synergy targets, retention plans
  - Financing: Cash/stock/debt mix, shareholder dilution, EPS accretion model
  - Legal: Definitive agreement, HSR filing, regulatory risk assessment
  - Board Committee pre-reviews (M&A + Audit) ≥7 days before full Board
  - All assumptions validated through DD, external advisors, committee reviews

- **Silver Standard (7-8 points)**:
  - ≥60-day timeline
  - Major DD workstreams (financial, legal, technical)
  - External advisors engaged
  - Valuation analysis conducted
  - Integration planning initiated
  - Financing plan developed
  - Legal documentation prepared
  - Committee involvement

- **Bronze Standard (5-6 points)**:
  - ≥30-day timeline
  - Basic DD (financial, legal)
  - Some external advisors
  - Valuation estimate
  - Integration discussed
  - Financing considered

- **Fails Standard (<5 points)**:
  - <30-day timeline
  - No systematic DD
  - No external advisors
  - No valuation rigor
  - No integration plan
  - No financing plan

#### Completeness Rubric

**Measures**: Coverage of all M&A preparation workstreams

- **Gold Standard (9-10 points)**:
  - Due diligence (financial, legal, technical, commercial) with DD summary
  - Valuation (DCF, comparables, fairness opinion)
  - Deal structure negotiation (cash/stock mix, earn-out, escrow, break-up fee)
  - Integration planning (Day 1-100, synergy models, retention plans)
  - Financing (cash sources, credit facility, stock dilution, pro forma financials)
  - Legal (definitive agreement, HSR filing, regulatory risk, closing conditions)
  - Board Committee pre-reviews (M&A + Audit)
  - Board materials (memo, DD summary, integration plan, agreement, fairness opinion, resolutions)
  - External advisor presentations (investment bank, law firm)
  - Board Q&A preparation
  - Post-approval action plan (signing, press release, HSR filing, investor call)
  - Risk assessment (DD red flags, Board rejection, regulatory, employee/customer defection, integration failure, market reaction)

- **Silver Standard (7-8 points)**:
  - Due diligence workstreams
  - Valuation analysis
  - Deal structure
  - Integration planning
  - Financing plan
  - Legal documentation
  - Committee reviews
  - Board materials
  - Advisor involvement
  - Risk assessment

- **Bronze Standard (5-6 points)**:
  - Basic DD
  - Valuation estimate
  - Deal structure
  - Integration discussed
  - Financing considered
  - Legal reviewed
  - Board materials

- **Fails Standard (<5 points)**:
  - No systematic DD
  - No valuation
  - No integration plan
  - No financing plan
  - No legal rigor
  - Minimal Board materials

#### Relevance Rubric

**Measures**: Focus on M&A value creation vs. generic project management

- **Gold Standard (9-10 points)**:
  - All milestones tied to M&A value creation (DD to find red flags, valuation to prevent overpayment, integration to capture synergies)
  - Success criteria measure deal outcomes (synergy realization, employee retention, customer retention, EPS accretion, market reaction)
  - Risks address M&A-specific failures (DD red flags, Board rejection, regulatory challenges, employee/customer defection, integration failure, overpayment)
  - Quality checks enforce M&A best practices (DD completeness, valuation justification, integration readiness, legal finalization)
  - Decision framework based on value creation potential and risk assessment

- **Silver Standard (7-8 points)**:
  - Most milestones M&A-relevant
  - Success criteria mostly deal-focused
  - Risks include M&A concerns
  - Quality checks present
  - Value creation discussed

- **Bronze Standard (5-6 points)**:
  - Milestones include M&A activities
  - Some deal criteria
  - Generic risks
  - Basic quality checks

- **Fails Standard (<5 points)**:
  - Generic project milestones
  - Vague criteria ("Board approves")
  - Risks unrelated to M&A
  - No value creation focus

#### Usefulness Rubric

**Measures**: Actionability for Corp Dev, Board, CEO, CFO, legal, integration team

- **Gold Standard (9-10 points)**:
  - All tasks have named owners (specific roles: CEO, CFO, General Counsel, Head of Corp Dev, VP Integration, CTO, Board Committees, External Advisors)
  - Time estimates enable capacity planning (1,300+ hours typical for $300M+ deal)
  - DD checklists (financial, legal, technical, commercial)
  - Valuation model templates (DCF, comparables)
  - Integration plan framework (Day 1-100, synergy models, retention plans)
  - Definitive agreement template (purchase agreement, reps & warranties, indemnification, escrow)
  - Board memo outline (strategic rationale, valuation, financing, integration, risks)
  - Fairness opinion from investment bank
  - HSR filing procedure
  - Board Committee agendas
  - Post-approval action plan (signing, press release, investor call)

- **Silver Standard (7-8 points)**:
  - Most tasks have named owners
  - Time estimates for major workstreams
  - DD frameworks
  - Valuation approach
  - Integration planning
  - Legal documentation
  - Board materials
  - Advisor engagement

- **Bronze Standard (5-6 points)**:
  - Some specific owners
  - Basic timeline
  - DD conducted
  - Valuation estimated
  - Integration discussed
  - Legal reviewed
  - Board materials

- **Fails Standard (<5 points)**:
  - Vague owners ("Corp Dev", "team")
  - No time estimates
  - No DD framework
  - No valuation methodology
  - No integration plan
  - No legal rigor
  - Minimal materials

#### Exceptional Rubric

**Measures**: Advanced M&A practices that maximize deal success probability

- **Gold Standard (9-10 points)**:
  - Comparable transaction analysis (benchmarking valuation multiples)
  - Sensitivity analysis (best/base/worst case synergies, EPS accretion)
  - Prior M&A performance review (learning from past deals)
  - Integration steering committee (CEO oversight)
  - Synergy tracking dashboard (monthly progress monitoring)
  - Employee retention metrics (weekly tracking, early intervention)
  - Customer retention metrics (customer success outreach)
  - Post-approval investor communication plan (press release, analyst call, roadshow)
  - Long-term integration metrics (Year 1 retention targets, synergy milestones, EPS accretion validation)

- **Silver Standard (7-8 points)**:
  - Comparable analysis
  - Sensitivity analysis
  - Integration oversight
  - Synergy tracking
  - Retention monitoring
  - Investor communication

- **Bronze Standard (5-6 points)**:
  - Some comparables
  - Basic scenario analysis
  - Integration tracking
  - Retention discussed

- **Fails Standard (<5 points)**:
  - No benchmarking
  - No sensitivity analysis
  - No integration tracking
  - No retention focus

---

### Distribution for M&A Deal Review Assertions

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

**Key Insight**: M&A deals with ≥90-day due diligence timelines, comprehensive DD across 4 workstreams (financial, legal, technical, commercial), and Day 1-100 integration plans capture 2.1x more synergies than rushed deals (McKinsey M&A Report). 70% of M&A deals fail to create shareholder value due to inadequate due diligence, overpayment, and poor integration execution. The 90-day timeline in the good example enables systematic validation of financial quality, legal clean-up, technical assessment, and integration planning—the four pillars of successful M&A.

