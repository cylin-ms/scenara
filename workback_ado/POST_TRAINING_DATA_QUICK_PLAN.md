# Workback Plan Post-Training: Quick Action Plan

**Created**: November 12, 2025  
**Status**: Planning Phase  
**Goal**: Create 500 high-quality training examples for workback plan model

---

## 🎯 Executive Summary

**Problem**: Need training data to teach models to generate high-quality workback plans (structured tasks, dependencies, timelines, participants).

**Solution**: 3-source hybrid approach
1. **ADO Work Items** (40% - 200 examples) - Real execution data ✅ Gold standard
2. **Expert-Validated** (20% - 100 examples) - Synthetic + corrections ✅ Gold standard  
3. **High-Quality Synthetic** (40% - 200 examples) - Template variations ✅ Silver standard

**Timeline**: 12 weeks | **Effort**: 260 hours engineering + 40 hours expert review

---

## 📊 Target Dataset (500 Examples)

### Composition
- **200 ADO-derived** (real projects from Azure DevOps)
- **100 Expert-validated** (reviewed and corrected by PMs)
- **150 High-quality synthetic** (template-based variations)
- **50 Edge cases** (targeted generation for coverage)

### Distribution Targets
- **Complexity**: 30% Q2 (Low), 50% Q3 (Medium), 20% Q1 (High)
- **Industry**: 30% Tech/SaaS, 20% Enterprise, 15% E-commerce, 35% Other
- **Outcomes**: 70% on-time, 20% delayed, 10% failed/cancelled

---

## 🚀 12-Week Roadmap

| Week | Phase | Key Deliverable |
|------|-------|-----------------|
| **1-2** | ADO Transformation | 200 ADO-derived workback plans |
| **3-4** | Synthetic Generation | 150 synthetic workback plans |
| **5-8** | Expert Validation | 100 expert-validated examples + 50 DPO pairs |
| **9-10** | Quality Validation | Quality metrics + filtered dataset |
| **11-12** | Training Formatting | Final SFT/DPO/RLHF datasets |

---

## 🛠️ 5 New Scripts to Build

### 1. `ado_to_workback_transformer.py` (Week 1-2)
**Purpose**: Transform ADO work items into WorkbackPlan training examples

**Key Functions**:
- `cluster_work_items()` - Group related work items into projects
- `extract_project_context()` - Infer goals, team, timeline, risks
- `generate_workback_plan_from_ado()` - Use LLM to create structured plan
- `add_execution_outcomes()` - Compute outcome metrics from actual data

**Input**: `ado_workback_training_data.json` (50 items)  
**Output**: `workback_plans_from_ado_200.json` (200 plans)

### 2. `synthetic_workback_generator.py` (Week 3-4)
**Purpose**: Generate diverse synthetic workback plans from templates

**Key Functions**:
- `load_yaml_templates()` - Parse workback_planning_scenarios.yaml
- `parameterize_template()` - Create variations (duration, team size, industry)
- `enhance_synthetic_plan()` - Use LLM to add realistic details
- `export_to_workback_format()` - Convert to WorkbackPlan schema

**Input**: `workback_planning_scenarios.yaml` (10 templates)  
**Output**: `synthetic_workback_examples_150.json` (150 plans)

### 3. `expert_correction_processor.py` (Week 5-8)
**Purpose**: Process expert reviews and create gold-standard examples

**Key Functions**:
- `parse_expert_reviews()` - Read CSV/HTML expert feedback
- `apply_corrections()` - Implement expert fixes
- `create_dpo_pairs()` - Generate before/after pairs for DPO
- `extract_gold_standard()` - Filter high-scoring examples

**Input**: `expert_review.csv` (100 reviewed examples)  
**Output**: `gold_standard_examples_50.json` + `dpo_pairs_50.json`

### 4. `workback_quality_validator.py` (Week 9-10)
**Purpose**: Validate and filter examples by quality metrics

**Key Functions**:
- `validate_structure()` - Check IDs, dependencies, dates, circular deps
- `assess_content_quality()` - Evaluate descriptions, roles, timeline realism
- `compute_diversity_metrics()` - Measure industry/complexity/outcome distribution
- `filter_high_quality()` - Select top examples passing all checks

**Input**: All generated examples (500+)  
**Output**: `filtered_high_quality_300.json` + `quality_report.json`

### 5. `training_data_formatter.py` (Week 11-12)
**Purpose**: Format validated examples for different training approaches

**Key Functions**:
- `format_for_sft()` - Create messages format (system/user/assistant)
- `format_for_dpo()` - Create chosen/rejected pairs
- `format_for_reward_model()` - Create context/plan/score triples
- `generate_statistics()` - Compute dataset statistics

**Input**: Validated examples  
**Output**: `sft_training_data_500.jsonl`, `dpo_pairs_100.jsonl`, `reward_model_300.jsonl`

---

## 📋 Week 1 Action Items (Nov 12-18)

### Priority 1: Start ADO Transformation (40 hours)

**Day 1-2: Design & Scaffold**
```bash
# Create script
touch workback_ado/ado_to_workback_transformer.py

# Design clustering approach
# - Group by Area Path (e.g., Outlook\Mobile\Authentication)
# - Group by Epic/Feature hierarchy
# - Group by time window (same sprint/quarter)
# - Min cluster size: 3-5 work items
```

**Day 3-4: Implement Clustering**
```python
def cluster_work_items(work_items, method='area_path'):
    """
    Input: List of ADO work items
    Output: List of project clusters
    
    Each cluster = coherent project with:
    - 3-5 related work items
    - Common area/epic/team
    - Similar timeframe
    """
    pass
```

**Day 5: Test Clustering**
```bash
# Test with existing data
python workback_ado/ado_to_workback_transformer.py \
  --input workback_ado/ado_workback_training_data.json \
  --output workback_ado/clusters_test.json \
  --cluster-by area_path \
  --min-size 3

# Expected: 10-15 clusters from 50 items
```

### Priority 2: Analyze Synthetic Templates (8 hours)

**Day 1: Parse YAML Structure**
```bash
# Check what we have
python -c "
import yaml
with open('temp_stratos/experiments/time_benchmark/manufactured/scenarios/workback_planning_scenarios.yaml') as f:
    scenarios = yaml.safe_load(f)
    print(f'Scenarios: {len(scenarios)}')
    for s in scenarios:
        print(f\"  - {s.get('title', 'Unknown')}\")
"
```

**Day 2: Design Transformation**
```markdown
YAML Scenario → WorkbackPlan Mapping:

scenario['title'] → workback_plan.summary
scenario['phases'] → workback_plan.deliverables
scenario['weekly_tasks'] → workback_plan.tasks
week_ordering → task.dependencies
task_descriptions → infer participant.role
scenario['risks'] → workback_plan.notes
```

### Priority 3: Create Quality Validator Stub (12 hours)

**Create validator**:
```bash
touch workback_ado/workback_quality_validator.py
```

**Implement checks**:
```python
def validate_structure(plan):
    """Return (is_valid, checks_dict)"""
    checks = {
        'has_summary': bool(plan.summary),
        'has_tasks': len(plan.tasks) > 0,
        'unique_task_ids': check_unique_ids(plan.tasks),
        'valid_dependencies': check_dependencies(plan.tasks),
        'no_circular_deps': not has_circular_deps(plan.tasks),
        'date_ordering': check_date_ordering(plan.tasks)
    }
    return all(checks.values()), checks
```

**Test on existing data**:
```bash
# Validate ADO examples
python workback_ado/workback_quality_validator.py \
  --input workback_ado/ado_batch_test_10.json \
  --output validation_results.json
```

---

## ✅ Current Assets (What We Already Have)

### Existing Tools ✅
- **`ado_workback_extraction.py`** - Extract and classify ADO work items
- **`compare_llm_vs_heuristic.py`** - Validate classification accuracy
- **`expert_review_workflow.py`** - Generate CSV/HTML expert review interfaces
- **`WORKBACK_PLANNING_GUIDE.md`** - Best practices reference for experts

### Existing Data ✅
- **`ado_workback_training_data.json`** - 50 work items with heuristic classification
- **`ado_batch_test_10.json`** - 10 work items with LLM classification
- **`expert_review.csv/html`** - Review interface templates
- **`workback_planning_scenarios.yaml`** - 10 detailed project templates

### What We Need to Build 🔨
1. ✅ **ADO Clustering** - Group work items into projects
2. ✅ **ADO→WorkbackPlan Transformer** - Generate structured plans from clusters
3. ✅ **Synthetic Variation Generator** - Create template variations
4. ✅ **Quality Validator** - Automated quality checks
5. ✅ **Training Formatter** - Convert to SFT/DPO/RLHF formats

---

## 🎯 Success Metrics

### Data Quality Targets
- ✅ **500 total examples** (mixed quality tiers)
- ✅ **95%+ structural validity** across all examples
- ✅ **4.0+/5.0 expert rating** on validated subset
- ✅ **Diversity entropy > 0.8** for industry/complexity

### Model Performance Targets (After Training)
- **Structural Validity**: 98%+ of generated plans valid
- **Expert Rating**: 4.0+/5.0 average from PM experts
- **vs Baseline (GPT-4)**: +20% expert rating, +30% completeness

### Business Value
- **Time Savings**: 24-48x (2-4 hours → 5 minutes)
- **Adoption**: 70%+ plans used with minimal edits

---

## 📝 Next Steps (This Week)

### Today (Nov 12)
- [x] Create comprehensive data creation plan ✅
- [x] Create quick action plan ✅
- [ ] Review plan with team
- [ ] Get approval to proceed

### Tomorrow (Nov 13)
- [ ] Create `ado_to_workback_transformer.py` scaffold
- [ ] Implement clustering logic
- [ ] Test on 50 existing ADO items

### This Week (Nov 12-18)
- [ ] Complete ADO clustering (3 days)
- [ ] Analyze YAML templates (1 day)
- [ ] Create quality validator stub (2 days)
- [ ] Generate first 10 workback plan examples (1 day)

---

## 📚 Key Resources

### Documentation
- **Full Plan**: `POST_TRAINING_DATA_CREATION_PLAN.md` (comprehensive 1200+ lines)
- **Quick Plan**: `POST_TRAINING_DATA_QUICK_PLAN.md` (this document)
- **ADO Proposal**: `ADO_POST_TRAINING_PROPOSAL.md` (rationale for ADO approach)
- **Workback Guide**: `WORKBACK_PLANNING_GUIDE.md` (best practices)

### Code
- **Existing**: `ado_workback_extraction.py`, `expert_review_workflow.py`
- **To Build**: 5 new scripts (transformer, generator, processor, validator, formatter)

### Data
- **ADO Items**: 50 extracted, 181 available
- **Templates**: 10 YAML scenarios
- **Target**: 500 training examples

---

## 💡 Key Insights

**Why ADO Data is Gold**:
- ✅ Real execution outcomes (not synthetic)
- ✅ Actual dependencies (from work item links)
- ✅ Real timeline data (planned vs actual)
- ✅ Outcome labels (on-time, delayed, blocked)

**Why Hybrid Approach**:
- ADO provides realism but limited diversity
- Synthetic provides diversity but needs validation
- Expert validation ensures quality and teaches model edge cases
- Combined = 500 high-quality, diverse examples

**Critical Success Factor**:
- Quality > Quantity
- Expert validation is essential
- Diversity ensures generalization
- Real execution data teaches what actually works

---

**Status**: Ready to start Week 1  
**Next Review**: End of Week 1 (Nov 18, 2025)  
**Owner**: Chin-Yew Lin
