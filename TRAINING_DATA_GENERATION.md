# Training Data Generation for 7 Top Meeting Type Scenarios

## Overview

This document describes how we generate **evaluation and training data** from 7 high-complexity meeting scenarios for post-training the meeting intelligence system. These scenarios represent critical enterprise meetings that require sophisticated workback planning and preparation.

## 7 Top Meeting Type Scenarios

### 1. Quarterly Business Review (QBR)
- **Complexity**: Critical
- **Typical Duration**: 2 hours
- **Typical Attendees**: 20 (CEO, CFO, Division Heads, Key Stakeholders)
- **Prep Time**: 300 minutes (5 hours)
- **Key Activities**: Data collection from all divisions, financial performance analysis, executive deck creation, rehearsal and Q&A prep
- **Why It Matters**: Board-level strategic meetings requiring extensive cross-functional data collection and executive-level synthesis over 21+ days of milestone-driven workback planning

### 2. Board of Directors Meeting
- **Complexity**: Critical
- **Typical Duration**: 3 hours
- **Typical Attendees**: 11 (Board Members, CEO, CFO, General Counsel)
- **Prep Time**: 360 minutes (6 hours)
- **Key Activities**: Board package preparation, fiduciary materials compilation, legal review and compliance checks, financial statements finalization
- **Why It Matters**: Requires highest level of preparation with fiduciary responsibilities, legal compliance, and governance requirements

### 3. Executive Sales Presentation
- **Complexity**: High → Critical
- **Typical Duration**: 90 minutes
- **Typical Attendees**: 6 (Customer CIO, Customer CFO, VP Sales, Solutions Architect)
- **Prep Time**: 180 minutes (3 hours)
- **Key Activities**: Customer research and intelligence, ROI model customization, technical solution design, competitive analysis, demo preparation
- **Why It Matters**: High-stakes presentations to C-level executives requiring deep customer research and customized business value demonstration

### 4. Product Launch Go/No-Go Decision
- **Complexity**: Critical
- **Typical Duration**: 2 hours
- **Typical Attendees**: 12 (CEO, CTO, CMO, VP Product, VP Sales)
- **Prep Time**: 240 minutes (4 hours)
- **Key Activities**: Launch readiness checklist, technical quality metrics, marketing campaign readiness, sales enablement verification, risk assessment
- **Why It Matters**: High-risk, high-impact decision requiring comprehensive readiness assessment across all go-to-market functions

### 5. Annual SOX 404 Compliance Review
- **Complexity**: High → Critical
- **Typical Duration**: 3 hours
- **Typical Attendees**: 8 (External Auditors, CFO, CTO, Chief Compliance Officer)
- **Prep Time**: 300 minutes (5 hours)
- **Key Activities**: Internal controls testing documentation, control deficiency analysis, remediation plans preparation, IT general controls evidence
- **Why It Matters**: Legally mandated with serious consequences for deficiencies; requires meticulous documentation and evidence collection

### 6. Quarterly Earnings Call
- **Complexity**: Critical
- **Typical Duration**: 90 minutes
- **Typical Attendees**: 500+ (CEO, CFO, IR Director, Analysts, Investors)
- **Prep Time**: 360 minutes (6 hours)
- **Key Activities**: Financial results finalization, earnings script preparation, guidance modeling, Q&A preparation, legal review (Reg FD compliance)
- **Why It Matters**: Public events with regulatory requirements (Reg FD) and significant market impact; poor preparation can result in stock volatility

### 7. M&A Deal Approval (Board)
- **Complexity**: Critical
- **Typical Duration**: 6 hours
- **Typical Attendees**: 14+ (Board Members, CEO, CFO, M&A Advisors, Legal Counsel)
- **Prep Time**: 480 minutes (8 hours)
- **Key Activities**: Due diligence summary, financial valuation analysis, strategic rationale documentation, integration planning, risk assessment, fairness opinion
- **Why It Matters**: Among the most complex corporate decisions, often involving hundreds of millions in capital; requires comprehensive due diligence and strategic analysis

## Training Data Schema

### Base Fields (Microsoft Graph API)
All training data follows the Microsoft Graph API calendar event schema:

```json
{
  "id": "string",
  "subject": "string",
  "bodyPreview": "string",
  "showAs": "busy|free|tentative|away|workingElsewhere",
  "type": "singleInstance|occurrence|exception|seriesMaster",
  "start": {
    "dateTime": "ISO 8601",
    "timeZone": "IANA timezone"
  },
  "end": {
    "dateTime": "ISO 8601",
    "timeZone": "IANA timezone"
  },
  "organizer": {
    "emailAddress": {
      "name": "string",
      "address": "string"
    }
  },
  "attendees": [
    {
      "type": "required|optional",
      "status": {
        "response": "none|organizer|accepted|declined|tentative",
        "time": "ISO 8601"
      },
      "emailAddress": {
        "name": "string",
        "address": "string"
      }
    }
  ],
  "responseStatus": {
    "response": "organizer|accepted|declined|tentative",
    "time": "ISO 8601"
  }
}
```

### Training-Specific Fields
Additional fields for post-training:

```json
{
  "importance_label": "critical|high|medium|low",
  "prep_needed": true|false,
  "prep_time_minutes": number,
  "reasoning": "string explaining why prep is needed and how much time",
  "persona_id": "executive|senior-manager|individual-contributor",
  "generation_timestamp": "ISO 8601"
}
```

### Training Metadata
Additional context for training and evaluation:

```json
{
  "_training_metadata": {
    "source": "workback_scenario",
    "scenario_file": "WORKBACK_PLAN_XX_*.md",
    "complexity": "critical|high|medium|low",
    "meeting_type": "string",
    "preparation_tasks": ["task1", "task2", ...],
    "key_roles": ["role1", "role2", ...],
    "typical_duration_minutes": number,
    "typical_attendee_count": number
  },
  "scenario_key": "scenario_identifier",
  "variation_id": number
}
```

## Generation Process

### Step 1: Base Meeting Objects
Each of the 7 scenarios has a base meeting object in Microsoft Graph API format:
- `workback_ado/WORKBACK_PLAN_01_QBR_meeting.json`
- `workback_ado/WORKBACK_PLAN_02_BOARD_DIRECTORS_meeting.json`
- `workback_ado/WORKBACK_PLAN_03_SALES_PRESENTATION_meeting.json`
- `workback_ado/WORKBACK_PLAN_04_PRODUCT_LAUNCH_meeting.json`
- `workback_ado/WORKBACK_PLAN_05_COMPLIANCE_REVIEW_meeting.json`
- `workback_ado/WORKBACK_PLAN_06_INVESTOR_RELATIONS_meeting.json`
- `workback_ado/WORKBACK_PLAN_07_M&A_DEAL_meeting.json`

These were generated from the workback plan markdown files using `tools/align_workback_meeting_schema.py`.

### Step 2: Training Data Generation
The `tools/generate_workback_training_data.py` tool adds training-specific fields:

```bash
# Generate basic training data (1 example per scenario)
python tools/generate_workback_training_data.py

# Generate with variations (3 personas per scenario)
python tools/generate_workback_training_data.py --variations 3

# Generate with evaluation split (20% for eval)
python tools/generate_workback_training_data.py --variations 3 --eval-split 0.2
```

### Step 3: Persona Variations
The tool generates variations for different personas:

1. **Executive** (120% base prep time)
   - Senior leadership requiring strategic context
   - Focus on high-level implications and decisions
   - Example: CEO, CFO, Board Member

2. **Senior Manager** (100% base prep time)
   - Middle management with execution responsibility
   - Balance of strategic and tactical preparation
   - Example: VP, Director, GM

3. **Individual Contributor** (80% base prep time)
   - Contributors with specific deliverables
   - Focus on tactical execution and details
   - Example: Analyst, Engineer, Specialist

### Step 4: Schema Validation
All generated training data is validated against the schema requirements:

```bash
python post_training/tools/validate_schema_alignment.py \
  --synthetic post_training/data/training/workback_scenarios.jsonl
```

**Validation Results**:
- ✅ All 14 examples pass validation (100%)
- ✅ 76.9% alignment with real meeting data schema
- ✅ All required Graph API fields present
- ✅ All 6 training-specific fields present
- ✅ 100% of examples marked as "critical" importance
- ✅ 100% of examples require preparation (prep_needed=true)
- ✅ Average prep time: 285 minutes (4.75 hours)

## Output Files

### Training Data
- **Location**: `post_training/data/training/workback_scenarios.jsonl`
- **Format**: JSONL (JSON Lines, one object per line)
- **Examples**: 14 (with 3 variations and 20% eval split)
- **Schema**: Graph API + Training fields + Training metadata

### Evaluation Data
- **Location**: `post_training/data/training/workback_scenarios_eval.jsonl`
- **Format**: JSONL
- **Examples**: 7 (with 3 variations and 20% eval split)
- **Purpose**: Hold-out set for evaluation metrics

### Statistics
- **Location**: `post_training/data/training/workback_scenarios_stats.json`
- **Content**: Generation statistics and metadata
  ```json
  {
    "total_training": 14,
    "total_eval": 7,
    "scenarios_processed": 7,
    "variations_per_scenario": 3,
    "output_file": "post_training/data/training/workback_scenarios.jsonl",
    "eval_file": "post_training/data/training/workback_scenarios_eval.jsonl"
  }
  ```

## Evaluation Framework

### Scenario 1: Meeting Prioritization
**Goal**: Test if the model can correctly rank meetings by importance

**Evaluation Metrics**:
- Precision@10: Are the top 10 meetings correctly identified?
- NDCG@10: Normalized Discounted Cumulative Gain
- Importance label accuracy

**Expected Results**:
- All 7 scenarios should rank in top 10% of user's calendar
- Critical meetings (QBR, Board, M&A) should consistently rank highest

### Scenario 2: Prep Time Allocation
**Goal**: Test if the model can accurately estimate preparation time

**Evaluation Metrics**:
- Mean Absolute Error (MAE) vs. ground truth prep times
- Accuracy within ±30 minutes
- Correlation with meeting complexity

**Expected Results**:
- MAE < 45 minutes (15% of average prep time)
- 85%+ accuracy within ±30 minutes
- Strong correlation (r > 0.8) with complexity label

### Scenario 3: Workback Plan Generation Quality
**Goal**: Test if the model can generate high-quality workback plans

**Evaluation Metrics**:
- GUTT v4.0 quality score
- Task completeness (% of expected tasks present)
- Timeline realism (milestones within reasonable timeframes)
- Deliverable specificity

**Expected Results**:
- GUTT score > 0.85 for all 7 scenarios
- 90%+ task completeness vs. reference plans
- 95%+ timeline realism (within ±20% of reference)

## Integration with GUTT v4.0

The 7 workback scenarios are designed to test advanced capabilities of the GUTT v4.0 evaluation framework:

### Grounding
- Meeting details accurately reflected in workback plans
- No hallucinated attendees, dates, or requirements

### Usefulness
- Preparation tasks directly address meeting objectives
- Deliverables match meeting complexity and audience
- Timelines are realistic and achievable

### Thoughtfulness
- Recognition of meeting importance and complexity
- Appropriate resource allocation (time, people, budget)
- Risk identification and mitigation strategies

### Thoroughness
- Comprehensive coverage of all preparation dimensions
- No critical steps missing from workback plan
- Appropriate level of detail for meeting complexity

## Usage Examples

### Example 1: Generate Basic Training Data
```bash
# Generate 1 example per scenario (7 total)
python tools/generate_workback_training_data.py \
  --output post_training/data/training/workback_scenarios_basic.jsonl
```

### Example 2: Generate with Persona Variations
```bash
# Generate 3 variations per scenario (21 total)
# Each scenario gets executive, senior-manager, and IC perspectives
python tools/generate_workback_training_data.py \
  --variations 3 \
  --output post_training/data/training/workback_scenarios_varied.jsonl
```

### Example 3: Generate Train/Eval Split
```bash
# Generate with 80/20 train/eval split
# Training: 16 examples (2-3 variations per scenario)
# Evaluation: 5 examples (1 variation per scenario, 2 scenarios with 0)
python tools/generate_workback_training_data.py \
  --variations 3 \
  --eval-split 0.2 \
  --output post_training/data/training/workback_scenarios_split.jsonl
```

### Example 4: Validate Generated Data
```bash
# Validate schema alignment
python post_training/tools/validate_schema_alignment.py \
  --synthetic post_training/data/training/workback_scenarios.jsonl

# Expected output:
# ✅ All examples pass validation
# 📊 Alignment Score: 76.9%
# ✅ 100% of examples have importance_label=critical
# ✅ 100% of examples have prep_needed=true
```

## Key Insights

### Importance Distribution
**Current**: 100% critical (all 7 scenarios)
- This is expected since these are the TOP 7 meeting types
- These represent the highest-complexity, highest-stakes meetings
- In real usage, the distribution would be more varied

**Recommendation**: Generate additional lower-complexity scenarios to balance the distribution:
- Critical: 20% (top-tier strategic meetings)
- High: 30% (important tactical meetings)
- Medium: 35% (routine team meetings)
- Low: 15% (FYI meetings, optional attendee)

### Prep Time Estimates
**Current**: Average 285 minutes (4.75 hours)
- Range: 180-480 minutes (3-8 hours)
- Varies by meeting complexity and attendee seniority
- Adjusted by persona (+20% for executives, -20% for ICs)

**Validation**: Prep times are realistic based on:
- Industry benchmarks for executive preparation
- Typical workback planning timelines (7-21 days)
- Expected deliverables and review cycles

### Persona Variations
**Rationale**: Different roles require different preparation approaches
- **Executives**: More strategic context, broader implications
- **Senior Managers**: Balance of strategy and execution
- **Individual Contributors**: Focus on specific deliverables

**Application**: Personalized prep recommendations based on:
- User's role in organization
- User's relationship to meeting (organizer, required, optional)
- User's historical prep patterns

## Future Enhancements

### 1. Additional Scenarios
Expand beyond top 7 to include:
- Medium complexity: Team planning sessions, project reviews
- Low complexity: 1:1s, standup meetings, status updates
- Domain-specific: Sales calls, customer support, engineering design reviews

### 2. Calendar Context
Generate evaluation datasets with calendar context:
- Multiple meetings in the same time period
- Conflicting priorities and time constraints
- Preparation time allocation across meetings
- Meeting dependencies (pre-work required)

### 3. Organizational Context
Add organizational patterns:
- Company culture (e.g., "always over-prepare for board meetings")
- Team norms (e.g., "deck distribution 48h before")
- Historical patterns (e.g., "QBRs always run 30min over")

### 4. Dynamic Prep Estimation
Train models to adjust prep time based on:
- User's familiarity with topic
- Availability of pre-existing materials
- Number of stakeholders involved
- Meeting recurrence (first-time vs. recurring)

### 5. Quality Metrics
Develop comprehensive quality metrics:
- Prep time estimation accuracy (MAE, RMSE)
- Importance ranking precision (P@10, NDCG@10)
- Workback plan quality (GUTT v4.0)
- User satisfaction (post-meeting surveys)

## Related Documentation

- **Workback Planning Integration**: `src/workback_planning/README.md`
- **Schema Alignment**: `workback_ado/MEETING_SCHEMA_ALIGNMENT.md`
- **Component Clarification**: `COMPONENT_CLARIFICATION.md`
- **Post-Training Framework**: `post_training/README.md`
- **GUTT v4.0 Evaluation**: `post_training/docs/GUTT_v4.0.md`

## References

### Source Files
- Workback plan markdown files: `workback_ado/WORKBACK_PLAN_*.md`
- Meeting JSON objects: `workback_ado/WORKBACK_PLAN_*_meeting.json`
- Training data generator: `tools/generate_workback_training_data.py`
- Schema alignment tool: `tools/align_workback_meeting_schema.py`
- Schema validator: `post_training/tools/validate_schema_alignment.py`

### Output Files
- Training data: `post_training/data/training/workback_scenarios.jsonl`
- Evaluation data: `post_training/data/training/workback_scenarios_eval.jsonl`
- Statistics: `post_training/data/training/workback_scenarios_stats.json`
