# Workback Plan Post-Training Data Creation Plan

**Created**: November 12, 2025  
**Author**: Chin-Yew Lin  
**Purpose**: Comprehensive plan to create high-quality training data for workback plan model post-training

---

## Executive Summary

**Goal**: Create training data for workback plan generation that teaches models to produce high-quality, executable workback plans based on meeting context.

**Key Challenge**: Unlike classification tasks, workback planning requires:
- Complex structured output (tasks, dependencies, timelines, participants)
- Causal reasoning (what leads to success/failure)
- Domain expertise (realistic task decomposition and scheduling)
- Ground truth validation (did the plan work in reality?)

**Solution Approach**: Leverage **historical meeting data** combined with **expert-crafted templates** and **quality validation framework**.

---

## Part 1: Understanding the Data Requirements

### 1.1 What is the Target Model?

The workback plan model needs to generate structured `WorkbackPlan` objects with:

```python
class WorkbackPlan(BaseModel):
    summary: str                           # Brief plan description
    history: List[HistoryEvent]           # Past events/context
    deliverables: List[Deliverable]       # Key outcomes with due dates
    participants: List[Participant]        # People and roles
    artifact_references: List[ArtifactReference]  # Related documents
    tasks: List[Task]                     # Detailed task breakdown
    notes: list[str]                      # Additional notes
```

Each `Task` includes:
- `id`, `name`, `description`
- `participants` (who does it)
- `artifacts` (what they need)
- `dependencies` (what must be done first)
- `start_date`, `due_date` (when it happens)

### 1.2 Training Data Format

For post-training (SFT/DPO/RLHF), we need:

**Input Context** (Meeting Information):
```json
{
  "meeting": {
    "subject": "Q1 Product Launch Planning",
    "start_time": "2025-06-15T09:00:00",
    "duration_minutes": 60,
    "organizer": "Alice Johnson",
    "attendees": ["Bob Smith", "Carol Lee", "David Chen"]
  },
  "meeting_priority": {
    "importance": "High",
    "summary": "Critical milestone for Q1 revenue goals",
    "priorities": [
      "Define launch timeline",
      "Assign ownership of key deliverables",
      "Identify risks and dependencies"
    ]
  },
  "context": {
    "company_type": "Enterprise SaaS",
    "team_size": 50,
    "deadline": "2025-09-30",
    "constraints": ["Limited marketing budget", "Dependency on partner API"]
  }
}
```

**Target Output** (Workback Plan):
```json
{
  "summary": "6-month workback plan for Q1 product launch...",
  "deliverables": [
    {
      "id": "D1",
      "name": "Product Launch",
      "description": "Full product release to production",
      "due_date": "2025-09-30"
    },
    {
      "id": "D2",
      "name": "Beta Release",
      "description": "Limited release to beta customers",
      "due_date": "2025-08-15"
    }
  ],
  "tasks": [
    {
      "id": "T1",
      "name": "Requirements Gathering",
      "description": "Collect and document product requirements",
      "participants": [{"name": "Alice Johnson", "role": "Product Manager"}],
      "dependencies": [],
      "start_date": "2025-04-01",
      "due_date": "2025-04-15"
    },
    {
      "id": "T2",
      "name": "Technical Design",
      "description": "Create system architecture and API specifications",
      "participants": [{"name": "Bob Smith", "role": "Tech Lead"}],
      "dependencies": ["T1"],
      "start_date": "2025-04-16",
      "due_date": "2025-05-01"
    }
  ],
  "notes": [
    "Add 2-week buffer for partner API integration delays",
    "Marketing team has budget constraints - plan low-cost launch activities"
  ]
}
```

**Quality Metrics** (Ground Truth):
```json
{
  "execution_outcome": {
    "delivered_on_time": true,
    "days_early_or_late": 3,
    "budget_variance_percent": -5,
    "quality_score": 4.5
  },
  "task_accuracy": {
    "tasks_completed_as_planned": 18,
    "tasks_added_during_execution": 3,
    "tasks_removed": 1,
    "dependency_violations": 0
  },
  "expert_rating": {
    "completeness": 5,
    "realism": 4,
    "clarity": 5,
    "actionability": 5,
    "overall": 4.8
  }
}
```

---

## Part 2: Data Sources

### 2.1 Primary Source: Historical Meeting Data & Email Archives

**What We Can Extract**:
- ✅ Past executive review preparations (email threads, calendar entries, file versions)
- ✅ Real execution timelines (what was planned vs what actually happened)
- ✅ Actual preparation patterns (when materials were created, reviewed, finalized)
- ✅ Team collaboration data (who worked on what, when)
- ✅ Outcome data (meeting success, delays, issues encountered)

**Example Historical Reconstruction**:
```python
# From Historical Meeting Data to Workback Plan Training Example
historical_data = {
  "meeting": {
    "subject": "Q3 Board Review",
    "date": "2025-10-15",
    "organizer": "CFO",
    "attendees": ["Board members", "C-suite executives"]
  },
  "preparation_timeline": {
    "kickoff_email": "2025-09-17" (4 weeks before),
    "data_requests_sent": "2025-09-20",
    "first_draft_complete": "2025-10-01",
    "executive_review": "2025-10-08",
    "final_materials_sent": "2025-10-13" (48 hours before)
  },
  "artifacts_created": [
    {"file": "Board_Packet_v1.pdf", "created": "2025-10-01", "pages": 120},
    {"file": "Board_Packet_v2.pdf", "created": "2025-10-05", "pages": 135},
    {"file": "Board_Packet_Final.pdf", "created": "2025-10-13", "pages": 150}
  ],
  "team_involved": [
    "CFO", "Controller", "IR Director", "12 Business Unit Leaders"
  ],
  "challenges_noted": [
    "Finance data delayed by 3 days",
    "European unit needed extra review cycle",
    "CEO requested additional risk analysis"
  ]
}

# Transforms into training example
training_example = {
  "input": {
    "meeting_type": "Board Review",
    "deadline": "2025-10-15",
    "complexity": "High",
    "team_size": 15,
    "material_volume": "150 pages"
  },
  "output": {
    "workback_plan": {
      "total_weeks": 4,
      "phases": [
        {
          "name": "Planning & Data Collection",
          "duration_days": 7,
          "tasks": ["Kickoff meeting", "Data requests", "Template preparation"]
        },
        {
          "name": "Content Creation",
          "duration_days": 14,
          "tasks": ["Financial analysis", "BU updates", "First draft assembly"]
        },
        {
          "name": "Review & Refinement",
          "duration_days": 7,
          "tasks": ["Executive review", "Revisions", "Final approval"]
        },
        {
          "name": "Distribution",
          "duration_days": 2,
          "tasks": ["Final production", "Board distribution"]
        }
      ]
    }
  },
  "outcome_metrics": {
    "delivered_on_time": true,
    "rework_cycles": 2,
    "common_blockers": ["Data delays from international units"]
  }
}
```

**Data Collection Sources**:
- ✅ Email archives (preparation threads, data requests, reviews)
- ✅ Calendar history (prep meetings, review sessions)
- ✅ File system metadata (document versions, creation times)
- ✅ Meeting notes and retrospectives

### 2.2 Secondary Source: Synthetic Templates

**Advantage**: Control over diversity and completeness

**Template Categories**:
1. **Product Launch** (8-12 weeks, cross-functional)
2. **Feature Development** (2-6 weeks, engineering-focused)
3. **Marketing Campaign** (4-8 weeks, marketing-focused)
4. **Infrastructure Migration** (12-24 weeks, high complexity)
5. **Customer Onboarding** (1-4 weeks, support-focused)
6. **Regulatory Compliance** (8-16 weeks, legal/compliance)

**Existing Resources**:
- ✅ `workback_planning_scenarios.yaml` (1000+ lines)
- ✅ 10 detailed scenarios with phases, weeks, tasks
- 🔄 Need: Convert to WorkbackPlan format

### 2.3 Expert-Validated Examples

**Process**:
1. Generate plans using existing LLM
2. Expert review and correction (CSV/HTML interfaces ready)
3. Capture expert edits as gold standard
4. Use corrections as training signal

**Status**:
- ✅ Expert review workflow complete: `expert_review_workflow.py`
- ✅ CSV interface: `expert_review.csv`
- ✅ HTML interface: `expert_review.html`
- 🔄 Need: Distribute to PM experts, collect corrections

---

## Part 3: Data Creation Pipeline

### Phase 1: Historical Data Extraction (Weeks 1-2)

**Goal**: Extract 100-200 historical workback plans from past meeting preparations

**Steps**:

#### Step 1.1: Identify High-Value Historical Meetings
```python
# Identify meetings that had significant preparation efforts
def identify_historical_meetings(calendar_data, email_data):
    """
    Find meetings that likely had workback planning:
    - Executive reviews (board, QBRs)
    - Product launches
    - Major customer presentations
    - Regulatory reviews
    """
    high_value_meetings = []
    for meeting in calendar_data:
        if is_high_value_meeting(meeting):
            preparation_data = extract_preparation_data(meeting, email_data)
            if has_sufficient_data(preparation_data):
                high_value_meetings.append((meeting, preparation_data))
    return high_value_meetings

# Example output
historical_meeting = {
    "meeting": {
        "subject": "Q3 Board Review",
        "date": "2025-10-15",
        "attendees": ["Board", "C-suite"]
    },
    "preparation_artifacts": [
        {"file": "Board_Packet_v1.pdf", "created": "2025-10-01"},
        {"file": "Board_Packet_Final.pdf", "created": "2025-10-13"}
    ],
    "preparation_timeline_days": 28,
    "team_members": ["CFO", "Controller", "12 BU Leaders"]
}
```

#### Step 1.2: Reconstruct Preparation Timeline
```python
def reconstruct_timeline(meeting, email_data, file_data, calendar_data):
    """
    From meeting artifacts, reconstruct:
    - When preparation started (kickoff email, first meeting)
    - Key milestones (data collection, draft creation, reviews)
    - Who was involved at each stage
    - Challenges encountered (delays, rework)
    """
    timeline = {
        "kickoff": find_earliest_prep_activity(email_data, meeting),
        "phases": identify_preparation_phases(email_data, file_data),
        "team": extract_team_members(email_data),
        "challenges": extract_challenges_from_emails(email_data)
    }
    return timeline
```

#### Step 1.3: Generate Workback Plan from Historical Data
```python
def generate_workback_plan_from_history(meeting, timeline):
    """
    Use LLM to generate structured WorkbackPlan from historical data
    Input: Meeting info + reconstructed timeline
    Output: WorkbackPlan object
    """
    prompt = f"""
    Given this historical meeting and its actual preparation timeline,
    generate a workback plan that captures the preparation approach used.
    
    Meeting:
    {json.dumps(meeting, indent=2)}
    
    Actual Preparation Timeline:
    {json.dumps(timeline, indent=2)}
    
    Generate a WorkbackPlan with:
    1. Summary: Brief description of the preparation effort
    2. Deliverables: Key outcomes (board packet, presentations, etc.)
    3. Tasks: Detailed task breakdown based on actual activities
    4. Dependencies: Task relationships from timeline
    5. Participants: Team members involved
    6. Notes: Lessons learned from challenges encountered
    
    Output format: JSON matching WorkbackPlan schema
    """
    
    plan = llm_client.query(prompt, temperature=0.1)
    return WorkbackPlan.model_validate(plan)
```

#### Step 1.4: Add Execution Outcome Labels
```python
def add_execution_outcomes(workback_plan, meeting, timeline):
    """
    Compute outcome metrics from actual execution
    """
    return {
        "workback_plan": workback_plan,
        "outcomes": {
            "delivered_on_time": was_on_time(meeting, timeline),
            "preparation_duration_days": timeline['total_days'],
            "rework_cycles": count_rework_cycles(timeline),
            "common_blockers": extract_blockers(timeline),
            "lessons_learned": extract_lessons(timeline)
        }
    }
```

**Deliverables**:
- [ ] `historical_data_extractor.py` - Email/calendar/file analysis script
- [ ] `historical_workback_examples_100.json` - 100 historically-derived workback plans
- [ ] `historical_workback_outcomes_100.json` - Execution outcomes for each plan

**Timeline**: 2 weeks (80 hours)

---

### Phase 2: Synthetic Template Expansion (Weeks 3-4)

**Goal**: Create 100-200 diverse, high-quality synthetic workback plans

**Steps**:

#### Step 2.1: Template Parameterization
```python
# Convert existing scenarios to parameterized templates
template = {
    "scenario_type": "Product Launch",
    "parameters": {
        "duration_weeks": [8, 12, 16],  # Variable duration
        "team_size": [5, 10, 20, 50],   # Variable team size
        "complexity": ["Low", "Medium", "High"],
        "industry": ["SaaS", "E-commerce", "Healthcare", "Finance"]
    },
    "task_templates": [
        {
            "phase": "Planning",
            "tasks": [
                {"name": "Requirements Gathering", "duration_percent": 0.1},
                {"name": "Project Kickoff", "duration_percent": 0.02}
            ]
        },
        {
            "phase": "Development",
            "tasks": [
                {"name": "Feature Implementation", "duration_percent": 0.4},
                {"name": "Integration Testing", "duration_percent": 0.15}
            ]
        }
    ]
}
```

#### Step 2.2: Generate Variations
```python
def generate_template_variations(template, num_variations=20):
    """
    Generate multiple variations of a template by:
    - Varying parameters
    - Adjusting task durations
    - Changing team composition
    - Adding realistic constraints
    """
    variations = []
    for i in range(num_variations):
        params = sample_parameters(template['parameters'])
        plan = instantiate_template(template, params)
        plan = add_realistic_details(plan)  # LLM adds specifics
        variations.append(plan)
    return variations
```

#### Step 2.3: LLM Enhancement
```python
def enhance_synthetic_plan(plan, industry_context):
    """
    Use LLM to add:
    - Realistic task descriptions
    - Industry-specific details
    - Common risks and mitigation strategies
    - Participant roles and responsibilities
    """
    prompt = f"""
    Enhance this workback plan template with realistic details for a {industry_context} project:
    
    Template:
    {json.dumps(plan, indent=2)}
    
    Add:
    1. Detailed task descriptions with industry-specific language
    2. Realistic participant names and roles
    3. Common risks and dependencies for this industry
    4. Artifact references (docs, designs, reports)
    5. Notes with practical insights
    
    Maintain the timeline structure but add depth and realism.
    """
    
    enhanced = llm_client.query(prompt, temperature=0.7)
    return WorkbackPlan.model_validate(enhanced)
```

**Deliverables**:
- [ ] `synthetic_workback_generator.py` - Template expansion script
- [ ] `synthetic_workback_examples_150.json` - 150 synthetic plans
- [ ] `synthetic_templates_library.yaml` - Reusable template library

**Timeline**: 2 weeks (60 hours)

---

### Phase 3: Expert Validation & Correction (Weeks 5-8)

**Goal**: Validate and refine 50-100 high-value examples with expert feedback

**Steps**:

#### Step 3.1: Select High-Value Examples
```python
def select_for_expert_review(all_examples, num_select=100):
    """
    Prioritize examples for expert review:
    - High complexity (Q1) examples
    - Diverse scenarios (different industries, team sizes)
    - Examples with interesting execution outcomes
    - Edge cases and failure scenarios
    """
    return stratified_sample(all_examples, criteria={
        'complexity': {'Q1': 30, 'Q3': 50, 'Q2': 20},
        'outcome': {'success': 70, 'delayed': 20, 'failed': 10},
        'industry': 'uniform'
    })
```

#### Step 3.2: Expert Review Process
```bash
# 1. Export to review interfaces
python expert_review_workflow.py \
  --input synthetic_workback_examples_150.json \
  --output expert_review_batch_1.csv \
  --output-html expert_review_batch_1.html

# 2. Distribute to experts
# - Send CSV to PM team leads (5 experts)
# - Share HTML interface for web-based review
# - Provide WORKBACK_PLANNING_GUIDE.md as reference

# 3. Collect feedback
# Experts mark corrections in columns:
# - Correctness (1-5): Is the plan realistic?
# - Completeness (1-5): Are all tasks covered?
# - Clarity (1-5): Are descriptions clear?
# - Actionability (1-5): Could this be executed?
# - Corrections: Specific fixes needed
```

#### Step 3.3: Process Expert Corrections
```python
def process_expert_corrections(reviewed_csv):
    """
    Parse expert corrections and create gold-standard examples
    """
    reviews = pd.read_csv(reviewed_csv)
    
    gold_examples = []
    for idx, row in reviews.iterrows():
        if row['Correctness'] >= 4 and row['Completeness'] >= 4:
            # High-quality example, use as-is
            gold_examples.append({
                'example': row['workback_plan'],
                'quality': 'gold',
                'expert_score': (row['Correctness'] + row['Completeness'] + 
                                row['Clarity'] + row['Actionability']) / 4
            })
        elif row['Corrections']:
            # Has corrections, create before/after pair for DPO
            gold_examples.append({
                'before': row['workback_plan'],
                'after': apply_corrections(row['workback_plan'], row['Corrections']),
                'quality': 'corrected',
                'corrections': row['Corrections']
            })
    
    return gold_examples
```

**Deliverables**:
- [ ] `expert_review_batch_1.csv` - 100 examples for review
- [ ] `expert_corrections_processed.json` - Processed corrections
- [ ] `gold_standard_examples_50.json` - Expert-validated examples
- [ ] `dpo_pairs_50.json` - Before/after pairs for DPO training

**Timeline**: 4 weeks (40 hours + expert time)

---

### Phase 4: Quality Validation Framework (Weeks 9-10)

**Goal**: Establish automated quality metrics for all training examples

**Quality Dimensions**:

#### 4.1 Structural Validity
```python
def validate_structure(workback_plan):
    """
    Check structural requirements:
    - All required fields present
    - Task IDs unique
    - Dependencies reference valid task IDs
    - Date ordering logical (start < due)
    - No circular dependencies
    """
    checks = {
        'has_summary': bool(workback_plan.summary),
        'has_tasks': len(workback_plan.tasks) > 0,
        'has_deliverables': len(workback_plan.deliverables) > 0,
        'unique_task_ids': len(set(t.id for t in workback_plan.tasks)) == len(workback_plan.tasks),
        'valid_dependencies': all(
            dep in [t.id for t in workback_plan.tasks]
            for task in workback_plan.tasks
            for dep in task.dependencies
        ),
        'no_circular_deps': not has_circular_dependencies(workback_plan.tasks),
        'date_ordering': all(
            task.start_date < parse_date(task.due_date)
            for task in workback_plan.tasks
            if task.start_date and task.due_date
        )
    }
    return all(checks.values()), checks
```

#### 4.2 Content Quality
```python
def assess_content_quality(workback_plan):
    """
    Assess content quality:
    - Task descriptions sufficiently detailed (>50 chars)
    - Participants have roles
    - Deliverables have due dates
    - Timeline realistic (tasks fit within project duration)
    - Complexity appropriate (Q2: 5-15 tasks, Q1: 15-50 tasks)
    """
    return {
        'task_description_length': np.mean([len(t.description) for t in workback_plan.tasks]),
        'participants_have_roles': all(p.role for t in workback_plan.tasks for p in t.participants),
        'deliverables_have_dates': sum(1 for d in workback_plan.deliverables if d.due_date) / len(workback_plan.deliverables),
        'task_count_appropriate': 5 <= len(workback_plan.tasks) <= 50,
        'timeline_realistic': check_timeline_realism(workback_plan)
    }
```

#### 4.3 Diversity Metrics
```python
def compute_diversity_metrics(all_examples):
    """
    Ensure dataset diversity:
    - Industry distribution
    - Complexity distribution
    - Team size distribution
    - Duration distribution
    - Outcome distribution
    """
    return {
        'industry_entropy': compute_entropy([ex['industry'] for ex in all_examples]),
        'complexity_distribution': Counter([ex['complexity'] for ex in all_examples]),
        'team_size_range': (min_team_size, max_team_size),
        'duration_range': (min_duration, max_duration),
        'outcome_balance': Counter([ex['outcome'] for ex in all_examples])
    }
```

**Deliverables**:
- [ ] `workback_quality_validator.py` - Quality validation script
- [ ] `quality_report.json` - Quality metrics for all examples
- [ ] `filtered_high_quality_300.json` - Top 300 examples passing all checks

**Timeline**: 2 weeks (40 hours)

---

### Phase 5: Training Data Formatting (Weeks 11-12)

**Goal**: Format validated examples for different training approaches

#### 5.1 Supervised Fine-Tuning (SFT) Format
```python
def format_for_sft(example):
    """
    Format: <meeting_context> → <workback_plan>
    """
    return {
        "messages": [
            {
                "role": "system",
                "content": "You are an expert project manager. Generate detailed workback plans for meetings."
            },
            {
                "role": "user",
                "content": f"""Create a workback plan for this meeting:

Meeting: {example['meeting']['subject']}
Date: {example['meeting']['start_time']}
Attendees: {', '.join(example['meeting']['attendees'])}

Meeting Priority:
{example['meeting_priority']['summary']}

Key Priorities:
{chr(10).join(f"- {p}" for p in example['meeting_priority']['priorities'])}

Generate a comprehensive workback plan with tasks, deliverables, participants, and timeline."""
            },
            {
                "role": "assistant",
                "content": json.dumps(example['workback_plan'].model_dump(), indent=2)
            }
        ]
    }
```

#### 5.2 Direct Preference Optimization (DPO) Format
```python
def format_for_dpo(example_pair):
    """
    Format: <context> → <chosen_plan> vs <rejected_plan>
    """
    return {
        "prompt": format_meeting_context(example_pair['context']),
        "chosen": example_pair['corrected_plan'],  # Expert-corrected version
        "rejected": example_pair['original_plan']  # Original generated version
    }
```

#### 5.3 RLHF Reward Model Format
```python
def format_for_reward_model(example):
    """
    Format: <context, plan> → <quality_score>
    """
    return {
        "context": format_meeting_context(example['context']),
        "plan": example['workback_plan'],
        "reward": compute_composite_score({
            'expert_rating': example.get('expert_score', 0),
            'execution_success': example.get('outcomes', {}).get('delivered_on_time', False),
            'estimation_accuracy': example.get('outcomes', {}).get('estimation_accuracy', 0),
            'structural_quality': validate_structure(example['workback_plan'])[0]
        })
    }
```

**Deliverables**:
- [ ] `sft_training_data_500.jsonl` - SFT format (500 examples)
- [ ] `dpo_training_pairs_100.jsonl` - DPO format (100 pairs)
- [ ] `reward_model_data_300.jsonl` - Reward model format (300 examples)
- [ ] `data_statistics_report.md` - Dataset statistics and quality metrics

**Timeline**: 2 weeks (40 hours)

---

## Part 4: Data Quality Targets

### Target Dataset Composition

| **Category** | **Count** | **Percentage** | **Source** | **Quality** |
|-------------|----------|---------------|-----------|-------------|
| **Historical-Derived** | 100 | 20% | Email/calendar/file history | Gold (real execution data) |
| **Expert-Validated** | 100 | 20% | Synthetic + expert corrections | Gold (expert-approved) |
| **High-Quality Synthetic** | 250 | 50% | Template-based + LLM generation | Silver (validated) |
| **Diverse Edge Cases** | 50 | 10% | Targeted generation for coverage | Bronze (valid but unusual) |
| **TOTAL** | 500 | 100% | Mixed | Mixed |

### Complexity Distribution Target

| **Complexity** | **Count** | **Percentage** | **Characteristics** |
|---------------|----------|---------------|-------------------|
| **Q2 (Low)** | 150 | 30% | 5-15 tasks, 2-6 weeks, 1-3 people |
| **Q3 (Medium)** | 250 | 50% | 15-30 tasks, 6-12 weeks, 3-10 people |
| **Q1 (High)** | 100 | 20% | 30-50 tasks, 12-24 weeks, 10+ people |

### Industry Distribution Target

| **Industry** | **Count** | **Percentage** |
|-------------|----------|---------------|
| Technology/SaaS | 150 | 30% |
| Enterprise Software | 100 | 20% |
| E-commerce | 75 | 15% |
| Healthcare | 50 | 10% |
| Finance | 50 | 10% |
| Manufacturing | 40 | 8% |
| Other | 35 | 7% |

### Outcome Distribution (for historical-derived examples)

| **Outcome** | **Count** | **Percentage** |
|------------|----------|---------------|
| Delivered on-time | 70 | 70% |
| Delayed (< 1 week) | 20 | 20% |
| Significantly delayed | 8 | 8% |
| Failed/Cancelled | 2 | 2% |

---

## Part 5: Implementation Roadmap

### Timeline Summary (12 weeks)

| **Week** | **Phase** | **Activities** | **Deliverables** |
|---------|----------|----------------|------------------|
| 1-2 | Historical Data Extraction | Identify meetings, reconstruct timeline, generate plans | 100 historical-derived examples |
| 3-4 | Synthetic Expansion | Template parameterization, variation generation | 250 synthetic examples |
| 5-8 | Expert Validation | Expert review, process corrections, create gold standard | 100 expert-validated examples |
| 9-10 | Quality Validation | Build validation framework, filter examples | Quality metrics + filtered dataset |
| 11-12 | Training Formatting | Format for SFT/DPO/RLHF | Final training datasets |

### Resource Requirements

**Engineering Time**:
- Week 1-2: 80 hours (Historical data extraction pipeline)
- Week 3-4: 60 hours (Synthetic generation system)
- Week 5-8: 40 hours (Expert review infrastructure)
- Week 9-10: 40 hours (Quality validation framework)
- Week 11-12: 40 hours (Training data formatting)
- **Total**: 260 hours (~6.5 weeks full-time)

**Expert Time**:
- Week 5-8: 40 hours across 5 experts = 8 hours/expert
- Reviews, corrections, validation

**Compute Resources**:
- LLM API calls: ~2000 calls (plan generation + enhancement)
- Estimated cost: $200-500 (depends on model: GPT-4 vs Ollama)

### Success Criteria

**Phase 1 Success** (Historical Data Extraction):
- [ ] 100 historical meetings transformed to workback plans
- [ ] 90%+ structural validity rate
- [ ] Execution outcomes captured for 70%+ examples

**Phase 2 Success** (Synthetic Expansion):
- [ ] 250 synthetic examples generated
- [ ] Covers 6+ industries, 3 complexity levels
- [ ] Average task description length > 100 chars

**Phase 3 Success** (Expert Validation):
- [ ] 100 examples reviewed by experts
- [ ] Average expert score > 4.0/5.0
- [ ] 50+ gold-standard examples created

**Phase 4 Success** (Quality Validation):
- [ ] 95%+ structural validity across all examples
- [ ] Diversity entropy > 0.8 for industry/complexity
- [ ] 300+ examples pass all quality gates

**Phase 5 Success** (Training Formatting):
- [ ] 500 examples in SFT format
- [ ] 100 preference pairs in DPO format
- [ ] 300 examples in reward model format
- [ ] Complete data statistics report published

---

## Part 6: Data Pipeline Architecture

### High-Level Pipeline

```
┌─────────────────────────────────────────────────────────────┐
│                   RAW DATA SOURCES                          │
├─────────────────────────────────────────────────────────────┤
│  Historical Data  │  YAML Templates  │  Expert Feedback    │
│   (email/cal/files) │  (10 scenarios)  │   (CSV/HTML)        │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                 TRANSFORMATION LAYER                        │
├─────────────────────────────────────────────────────────────┤
│  • Historical Meeting Reconstruction & Timeline Extraction  │
│  • Template Parameterization & Variation                    │
│  • LLM-based Plan Generation                                │
│  • Expert Correction Processing                             │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                  QUALITY VALIDATION                         │
├─────────────────────────────────────────────────────────────┤
│  • Structural Validity Check                                │
│  • Content Quality Assessment                               │
│  • Diversity Metrics Computation                            │
│  • Expert Score Validation                                  │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                   TRAINING DATASETS                         │
├─────────────────────────────────────────────────────────────┤
│  SFT (500)  │  DPO (100 pairs)  │  Reward Model (300)      │
└─────────────────────────────────────────────────────────────┘
```

### Tool/Script Inventory

**New Scripts to Create**:

1. **`historical_data_extractor.py`** (200 lines)
   - Identifies high-value historical meetings
   - Reconstructs preparation timeline from artifacts
   - Generates WorkbackPlan objects
   - Captures execution outcomes

2. **`synthetic_workback_generator.py`** (150 lines)
   - Loads YAML templates
   - Parameterizes and generates variations
   - Uses LLM for enhancement
   - Exports to WorkbackPlan format

3. **`expert_correction_processor.py`** (100 lines)
   - Parses expert review CSV/HTML
   - Applies corrections to plans
   - Creates before/after pairs for DPO
   - Generates gold-standard dataset

4. **`workback_quality_validator.py`** (200 lines)
   - Validates structure (IDs, dependencies, dates)
   - Assesses content quality (descriptions, roles)
   - Computes diversity metrics
   - Filters and ranks examples

5. **`training_data_formatter.py`** (150 lines)
   - Formats for SFT (messages format)
   - Formats for DPO (chosen/rejected pairs)
   - Formats for reward model (context/plan/score)
   - Exports to JSONL files

**Existing Scripts to Leverage**:
- ✅ `expert_review_workflow.py` - Expert review interfaces
- ✅ `compare_llm_vs_heuristic.py` - Classification validation

---

## Part 7: Next Steps (Action Plan)

### Immediate Actions (This Week)

#### 1. Create Historical Data Extraction Script

```bash
# Create the extraction script
touch workback_ado/historical_data_extractor.py

# Test with existing data
python workback_ado/historical_data_extractor.py \
  --email-archive /path/to/email/archive \
  --calendar-export calendar_october.json \
  --output workback_ado/workback_plans_from_history_50.json \
  --min-meeting-attendees 5
```

#### 2. Analyze Existing YAML Scenarios
```bash
# Check scenario structure
python -c "
import yaml
with open('temp_stratos/experiments/time_benchmark/manufactured/scenarios/workback_planning_scenarios.yaml') as f:
    scenarios = yaml.safe_load(f)
    print(f'Found {len(scenarios)} scenarios')
    for scenario in scenarios[:3]:
        print(f'- {scenario.get(\"title\", \"Unknown\")}: {scenario.get(\"estimated_duration\", \"?\")}'
"
```

#### 3. Create Synthetic Generator Stub
```bash
# Create generator script
touch workback_ado/synthetic_workback_generator.py

# Plan generation approach
cat > workback_ado/synthetic_generation_plan.md << 'EOF'
# Synthetic Workback Plan Generation Strategy

## Input: YAML Scenario Templates
- 10 scenarios from workback_planning_scenarios.yaml
- Each has phases, weeks, detailed task lists

## Transformation Process
1. Parse YAML scenario structure
2. Extract phases → Deliverables
3. Extract weekly tasks → Task objects
4. Infer dependencies from week ordering
5. Generate participant roles from task descriptions
6. Use LLM to enhance with realistic details

## Output: WorkbackPlan Objects
- Summary from scenario title/description
- Deliverables from major phases
- Tasks from weekly breakdown
- Dependencies from sequential ordering
- Participants generated (names + roles)
- Notes from risk/constraint sections
EOF
```

#### 4. Review Current Data Quality

```bash
# Check existing historical data sources
python -c "
import json
with open('calendar_october.json') as f:
    data = json.load(f)
    print(f'Total calendar events: {len(data)}')
    print(f'Events with 5+ attendees: {sum(1 for item in data if len(item.get(\"attendees\", [])) >= 5)}')
"
```
```

### Week 1 Goals (Nov 12-18)

**Priority 1**: Historical Data Extraction Pipeline
- [ ] Complete `historical_data_extractor.py`
- [ ] Test meeting identification on calendar exports
- [ ] Generate 10 example workback plans from historical data
- [ ] Validate output structure

**Priority 2**: Synthetic Generator Design
- [ ] Analyze YAML scenario structure
- [ ] Design template parameterization approach
- [ ] Create first synthetic workback plan manually
- [ ] Validate against WorkbackPlan schema

**Priority 3**: Quality Validation Framework
- [ ] Design quality metrics (structural + content)
- [ ] Create validation function stubs
- [ ] Test on 10 examples

### Week 2-3 Goals (Nov 19 - Dec 2)

**Priority 1**: Complete Historical Data Pipeline
- [ ] Generate 100 historical-derived workback plans
- [ ] Capture execution outcomes
- [ ] Compute quality metrics
- [ ] Create outcome_metrics.json

**Priority 2**: Synthetic Generation
- [ ] Complete synthetic_workback_generator.py
- [ ] Generate 250 synthetic examples
- [ ] Ensure diversity (6+ industries, 3 complexities)
- [ ] LLM enhancement pass

**Priority 3**: Expert Review Prep
- [ ] Select 100 high-value examples
- [ ] Export to CSV + HTML
- [ ] Create review guidelines document
- [ ] Distribute to expert team

### Month 2-3 Goals (Dec - Jan)

**Priority 1**: Expert Validation
- [ ] Collect expert reviews (100 examples)
- [ ] Process corrections
- [ ] Create gold-standard dataset (50+)
- [ ] Generate DPO pairs (50+)

**Priority 2**: Quality Validation
- [ ] Complete quality validator
- [ ] Run on all examples (500+)
- [ ] Filter to top 300-400
- [ ] Generate quality report

**Priority 3**: Training Data Formatting
- [ ] Format for SFT (500 examples)
- [ ] Format for DPO (100 pairs)
- [ ] Format for reward model (300)
- [ ] Create data statistics report

---

## Part 8: Success Metrics & KPIs

### Data Quality KPIs

**Target**: 500 total training examples with:
- ✅ 95%+ structural validity
- ✅ Average content quality score > 4.0/5.0
- ✅ Industry entropy > 0.8
- ✅ Complexity distribution: 30% Q2, 50% Q3, 20% Q1

### Model Performance KPIs (Post-Training)

**Evaluation on Hold-Out Set** (100 examples):
- **Structural Validity**: >98% of generated plans pass validation
- **Expert Rating**: Average 4.0+/5.0 from PM experts
- **Task Completeness**: >90% of necessary tasks identified
- **Dependency Accuracy**: >85% of dependencies correctly specified
- **Timeline Realism**: >80% of timelines deemed realistic

**Comparison to Baseline** (GPT-4 zero-shot):
- +20% improvement in expert ratings
- +30% improvement in task completeness
- +50% improvement in dependency accuracy

### Business Value Metrics

**Time Savings**:
- Baseline: 2-4 hours to create detailed workback plan manually
- Target: <5 minutes with AI assistance
- **Value**: 24-48x time savings

**Adoption Metrics**:
- Target: 70%+ of generated plans used with minimal edits
- Target: 50%+ of users prefer AI-generated plans over templates

---

## Conclusion

This plan provides a comprehensive roadmap to create **500 high-quality training examples** for workback plan post-training, combining:
1. **Real execution data** from 100 historical meetings (gold standard)
2. **Expert-validated examples** from 100 reviewed plans (gold standard)
3. **High-quality synthetic data** from 250 template variations (silver standard)
4. **Diverse edge cases** from 50 targeted generations (bronze standard)

**Key Success Factors**:
- ✅ **Leveraging existing assets** (email/calendar archives, expert review workflow, YAML templates)
- ✅ **Hybrid approach** (real data + synthetic + expert validation)
- ✅ **Quality-first mindset** (multiple validation layers)
- ✅ **Practical timeline** (12 weeks, 260 engineering hours)
- ✅ **Clear metrics** (structural validity, expert ratings, diversity)

**Next Step**: Begin with historical data extraction pipeline (Week 1 Priority 1) to validate the approach with real meeting data before scaling to full 500-example dataset.

---

**Document Status**: Draft v1.0  
**Last Updated**: November 12, 2025  
**Next Review**: Start of Week 1 (Nov 12, 2025)
