# Training Data Contract: Data Team → Training Team

**Version**: 1.0  
**Date**: November 18, 2025  
**Author**: Chin-Yew Lin  
**Purpose**: Define interface between data generation team and model training team

---

## Overview

This document specifies the **exact format** of training data that the Data Team delivers to the Training Team, ensuring complete decoupling between data generation and model training.

## Team Responsibilities

### Data Team (Data Generation)
- Generate training scenarios and examples
- Run LLM-as-Judge for PFT preference pairs
- Implement programmatic reward checks for RFT
- **Deliver**: Standardized JSON files + reward function code

### Training Team (Model Training)
- Load training datasets from JSON files
- Execute training pipelines (SFT → PFT → RFT)
- Monitor training metrics and convergence
- **Consume**: Pre-generated data + reward function

**Key Principle**: Training Team should NEVER need to understand how data was generated.

---

## 1. SFT Dataset Format

### File: `data/sft/{vertical}_training.jsonl`

**One JSON object per line:**

```json
{
  "scenario": "Meeting: Quarterly Business Review\nDate: 2025-12-15\nAttendees: CEO, CFO, VP Product...",
  "plan": {
    "milestones": [
      {"id": "M1", "name": "Data collection", "days_before": 21, "depends_on": []},
      {"id": "M2", "name": "Draft deck", "days_before": 14, "depends_on": ["M1"]}
    ],
    "tasks": [
      {"id": "T1", "name": "Collect financials", "owner": "CFO", "milestone": "M1"}
    ],
    "metadata": {
      "meeting_type": "QBR",
      "complexity": "medium"
    }
  },
  "quality_score": 0.92,
  "acrue_passed": 46,
  "acrue_total": 50,
  "source": "expert_validated",
  "generation_timestamp": "2025-11-18T10:30:00Z"
}
```

### Required Fields

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `scenario` | string | Meeting context (raw text) | "Meeting: QBR..." |
| `plan` | object | Structured workback plan | `{milestones: [...], tasks: [...]}` |
| `quality_score` | float | ACRUE pass rate (0.0-1.0) | 0.92 |
| `acrue_passed` | int | Number of assertions passed | 46 |
| `acrue_total` | int | Total assertions evaluated | 50 |
| `source` | string | Data provenance | "expert_validated" or "llm_generated" |
| `generation_timestamp` | string | ISO 8601 timestamp | "2025-11-18T10:30:00Z" |

### Quality Requirements

- **Minimum 25 examples** per vertical
- **Quality threshold**: `quality_score >= 0.85` (85% ACRUE pass rate)
- **Diversity**: Mix of simple (5), medium (15), complex (5) scenarios
- **Format validation**: All plans must parse successfully

### Training Team Usage

```python
import jsonlines

# Load SFT training data
examples = []
with jsonlines.open('data/sft/qbr_training.jsonl') as f:
    for item in f:
        examples.append({
            'input': item['scenario'],
            'output': item['plan']
        })

# Train SFT model
model = train_sft(examples, epochs=3)
```

---

## 2. PFT Dataset Format

### File: `data/pft/{vertical}_preferences.jsonl`

**One preference pair per line:**

```json
{
  "scenario": "Meeting: Quarterly Business Review\nDate: 2025-12-15...",
  "chosen": {
    "plan": {
      "milestones": [...],
      "tasks": [...]
    },
    "acrue_score": 0.88,
    "passed": ["A1", "A2", "C1", "C2", "C3", "C4", "C5", "R1", "R2", "U1"],
    "failed": ["E1", "E2"],
    "temperature": 0.8
  },
  "rejected": {
    "plan": {
      "milestones": [...],
      "tasks": [...]
    },
    "acrue_score": 0.62,
    "passed": ["A1", "R1", "U1"],
    "failed": ["A2", "A4", "C2", "C3", "C4", "R2", "U2"],
    "temperature": 1.5
  },
  "score_gap": 0.26,
  "key_differences": [
    "Chosen plan has complete milestone chain (C2)",
    "Chosen plan identifies backup presenters (U2)",
    "Rejected plan has unrealistic 3-day finalization (A2)"
  ],
  "generation_timestamp": "2025-11-18T10:45:00Z"
}
```

### Required Fields

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `scenario` | string | Meeting context | "Meeting: QBR..." |
| `chosen.plan` | object | Better quality plan | `{milestones: [...]}` |
| `chosen.acrue_score` | float | Quality score (0.0-1.0) | 0.88 |
| `rejected.plan` | object | Lower quality plan | `{milestones: [...]}` |
| `rejected.acrue_score` | float | Quality score (0.0-1.0) | 0.62 |
| `score_gap` | float | Quality difference | 0.26 (26% gap) |
| `key_differences` | array[string] | Human-readable explanation | ["Better milestone chain"] |

### Quality Requirements

- **Minimum 50 preference pairs** per vertical
- **Score gap threshold**: `score_gap >= 0.15` (15% minimum)
- **Balance across ACRUE categories**: 
  - 10 pairs for Accuracy (A1-A10)
  - 15 pairs for Completeness (C1-C15)
  - 10 pairs for Relevance (R1-R10)
  - 10 pairs for Usefulness (U1-U10)
  - 5 pairs for Exceptional (E1-E5)
- **Diversity**: Mix of temperatures (0.8, 1.0, 1.2, 1.5, 1.8)

### Training Team Usage

```python
import jsonlines

# Load PFT preference pairs
preferences = []
with jsonlines.open('data/pft/qbr_preferences.jsonl') as f:
    for item in f:
        preferences.append({
            'prompt': item['scenario'],
            'chosen': item['chosen']['plan'],
            'rejected': item['rejected']['plan']
        })

# Train DPO model
model = train_dpo(model, preferences, beta=0.1, epochs=2)
```

---

## 3. RFT Reward Function

### File: `training/rft_reward_checker.py`

**Data Team delivers executable Python code:**

```python
"""
RFT Reward Function for Workback Planning

Provides deterministic reward signals for reinforcement learning.
Generated by Data Team, consumed by Training Team.

Version: 1.0
Last Updated: 2025-11-18
"""

from typing import Dict, List, Any
from collections import defaultdict


def calculate_reward(plan: Dict[str, Any], scenario: Dict[str, Any]) -> float:
    """
    Calculate reward for RFT training.
    
    Args:
        plan: Generated workback plan with milestones and tasks
        scenario: Meeting context with attendees, constraints, etc.
    
    Returns:
        Reward in range [0.0, 6.0]
    """
    reward = 0.0
    
    # Reward 1: Dependency chain correctness (A5 assertion)
    if check_no_circular_dependencies(plan.get('milestones', [])):
        reward += 1.0
    if check_dependencies_exist(plan.get('milestones', [])):
        reward += 1.0
    
    # Reward 2: Timeline validation (A2, A3 assertions)
    if check_working_days_correct(plan.get('milestones', [])):
        reward += 1.0
    if check_no_impossible_timelines(plan.get('milestones', [])):
        reward += 1.0
    
    # Reward 3: Stakeholder mapping (A4 assertion)
    if check_task_owners_in_attendees(
        plan.get('tasks', []), 
        scenario.get('attendees', [])
    ):
        reward += 1.0
    
    # Reward 4: Constraint satisfaction (A3 assertion)
    if check_respects_holiday_blackouts(
        plan.get('milestones', []), 
        scenario.get('holidays', [])
    ):
        reward += 1.0
    
    return reward


def check_no_circular_dependencies(milestones: List[Dict]) -> bool:
    """Check for cycles in milestone dependency graph"""
    graph = defaultdict(list)
    for m in milestones:
        for dep_id in m.get('depends_on', []):
            graph[m['id']].append(dep_id)
    
    visited = set()
    rec_stack = set()
    
    def has_cycle(node):
        visited.add(node)
        rec_stack.add(node)
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                if has_cycle(neighbor):
                    return True
            elif neighbor in rec_stack:
                return True
        rec_stack.remove(node)
        return False
    
    for node in graph:
        if node not in visited:
            if has_cycle(node):
                return False
    return True


def check_dependencies_exist(milestones: List[Dict]) -> bool:
    """Check that all dependency IDs reference valid milestones"""
    milestone_ids = {m['id'] for m in milestones}
    for m in milestones:
        for dep_id in m.get('depends_on', []):
            if dep_id not in milestone_ids:
                return False
    return True


def check_working_days_correct(milestones: List[Dict]) -> bool:
    """Check timeline calculations respect working days"""
    for m in milestones:
        days_before = m.get('days_before_meeting', 0)
        effort_days = m.get('effort_days', 0)
        
        # Working days = ~70% of calendar days (5/7)
        expected_working = days_before * 5 / 7
        
        # Allow 30% tolerance
        if abs(effort_days - expected_working) > expected_working * 0.3:
            return False
    return True


def check_no_impossible_timelines(milestones: List[Dict]) -> bool:
    """Check that dependent milestones have valid sequencing"""
    milestone_times = {m['id']: m.get('days_before_meeting', 0) 
                       for m in milestones}
    
    for m in milestones:
        m_time = milestone_times.get(m['id'], 0)
        for dep_id in m.get('depends_on', []):
            dep_time = milestone_times.get(dep_id, 0)
            # Dependency must come BEFORE (higher days_before value)
            if dep_time <= m_time:
                return False
    return True


def check_task_owners_in_attendees(tasks: List[Dict], attendees: List[str]) -> bool:
    """Check all task owners are meeting attendees"""
    task_owners = {t.get('owner', '') for t in tasks}
    attendee_set = set(attendees)
    return task_owners.issubset(attendee_set)


def check_respects_holiday_blackouts(
    milestones: List[Dict], 
    holidays: List[str]
) -> bool:
    """Check milestones don't fall on holidays/blackout dates"""
    # Simplified check - production would use proper date arithmetic
    for m in milestones:
        # Check if milestone date conflicts with holidays
        # (Implementation depends on date representation)
        pass
    return True  # Placeholder
```

### Quality Requirements

- **Type hints** for all functions
- **Docstrings** for all functions
- **Unit tests** included (see `test_rft_reward_checker.py`)
- **Deterministic**: Same input → same output (no randomness)
- **Fast**: <10ms per plan evaluation
- **Well-documented**: Comments explaining each check

### Training Team Usage

```python
from training.rft_reward_checker import calculate_reward

# During RFT training loop
for scenario, plan in training_data:
    # Model generates plan
    generated_plan = model.generate(scenario)
    
    # Reward function evaluates plan
    reward = calculate_reward(generated_plan, scenario)
    
    # RL algorithm updates model
    model.update_policy(reward)
```

---

## 4. RFT Scenarios Dataset

### File: `data/rft/{vertical}_scenarios.jsonl`

**Training scenarios without pre-generated plans:**

```json
{
  "scenario": "Meeting: Board Review\nDate: 2026-01-15\nAttendees: CEO, Board Members...",
  "constraints": {
    "attendees": ["CEO", "Board Chair", "Board Member 1", "Board Member 2"],
    "holidays": ["2025-12-25", "2026-01-01"],
    "blackout_dates": ["2025-12-20:2026-01-05"],
    "lead_time_days": 60,
    "meeting_date": "2026-01-15"
  },
  "metadata": {
    "meeting_type": "Board",
    "complexity": "high",
    "num_attendees": 4,
    "has_external_stakeholders": true
  },
  "generation_timestamp": "2025-11-18T11:00:00Z"
}
```

### Quality Requirements

- **100-200 scenarios** per vertical
- **Diverse complexity**: Simple (30%), Medium (50%), Complex (20%)
- **Complete constraints**: All fields required for reward calculation
- **Realistic**: Based on actual meeting patterns

### Training Team Usage

```python
import jsonlines
from training.rft_reward_checker import calculate_reward

# Load RFT scenarios
scenarios = []
with jsonlines.open('data/rft/qbr_scenarios.jsonl') as f:
    scenarios = list(f)

# RFT training loop
for epoch in range(500):
    for scenario_data in scenarios:
        # Model generates plan
        plan = model.generate(scenario_data['scenario'])
        
        # Calculate reward using delivered function
        reward = calculate_reward(plan, scenario_data['constraints'])
        
        # Update model
        optimizer.step(reward)
```

---

## 5. Data Delivery Checklist

### What Data Team Delivers

```
training_data/
├── sft/
│   ├── qbr_training.jsonl          (25+ examples, quality >= 0.85)
│   ├── board_training.jsonl        (25+ examples)
│   ├── ma_training.jsonl           (25+ examples)
│   └── product_launch_training.jsonl (25+ examples)
├── pft/
│   ├── qbr_preferences.jsonl       (50+ pairs, gap >= 0.15)
│   ├── board_preferences.jsonl     (50+ pairs)
│   ├── ma_preferences.jsonl        (50+ pairs)
│   └── product_launch_preferences.jsonl (50+ pairs)
├── rft/
│   ├── qbr_scenarios.jsonl         (100-200 scenarios)
│   ├── board_scenarios.jsonl       (100-200 scenarios)
│   ├── ma_scenarios.jsonl          (100-200 scenarios)
│   └── product_launch_scenarios.jsonl (100-200 scenarios)
└── training/
    ├── rft_reward_checker.py       (Reward function code)
    └── test_rft_reward_checker.py  (Unit tests)
```

### Validation Script

Data Team includes validation:

```python
# validate_training_data.py
import jsonlines
import json

def validate_sft_dataset(filepath):
    """Validate SFT dataset format and quality"""
    with jsonlines.open(filepath) as f:
        examples = list(f)
    
    assert len(examples) >= 25, f"Need 25+ examples, got {len(examples)}"
    
    for ex in examples:
        assert 'scenario' in ex, "Missing scenario field"
        assert 'plan' in ex, "Missing plan field"
        assert 'quality_score' in ex, "Missing quality_score"
        assert ex['quality_score'] >= 0.85, f"Quality too low: {ex['quality_score']}"
    
    print(f"✓ {filepath} validated: {len(examples)} examples")

def validate_pft_dataset(filepath):
    """Validate PFT preference pairs"""
    with jsonlines.open(filepath) as f:
        pairs = list(f)
    
    assert len(pairs) >= 50, f"Need 50+ pairs, got {len(pairs)}"
    
    for pair in pairs:
        assert 'chosen' in pair and 'rejected' in pair
        assert 'score_gap' in pair
        assert pair['score_gap'] >= 0.15, f"Gap too small: {pair['score_gap']}"
    
    print(f"✓ {filepath} validated: {len(pairs)} preference pairs")

# Run validation before delivery
validate_sft_dataset('data/sft/qbr_training.jsonl')
validate_pft_dataset('data/pft/qbr_preferences.jsonl')
```

---

## 6. Training Team Integration

### Complete Training Pipeline

```python
"""
Training pipeline using delivered data.
Training Team does NOT need to know how data was generated.
"""

import jsonlines
from training.rft_reward_checker import calculate_reward

# Step 1: Load SFT data
sft_examples = []
with jsonlines.open('data/sft/qbr_training.jsonl') as f:
    for item in f:
        sft_examples.append({
            'input': item['scenario'],
            'output': item['plan']
        })

# Step 2: Train SFT
print("Training SFT...")
model = load_base_model("gpt-oss:120b")
model = train_sft(model, sft_examples, epochs=3)
model.save("checkpoints/sft_qbr.pt")

# Step 3: Load PFT data
pft_preferences = []
with jsonlines.open('data/pft/qbr_preferences.jsonl') as f:
    for item in f:
        pft_preferences.append({
            'prompt': item['scenario'],
            'chosen': item['chosen']['plan'],
            'rejected': item['rejected']['plan']
        })

# Step 4: Train PFT (DPO)
print("Training PFT (DPO)...")
model = train_dpo(model, pft_preferences, beta=0.1, epochs=2)
model.save("checkpoints/pft_qbr.pt")

# Step 5: Load RFT scenarios
rft_scenarios = []
with jsonlines.open('data/rft/qbr_scenarios.jsonl') as f:
    rft_scenarios = list(f)

# Step 6: Train RFT (Light RL)
print("Training RFT...")
for iteration in range(500):
    for scenario_data in rft_scenarios:
        # Generate plan
        plan = model.generate(scenario_data['scenario'])
        
        # Calculate reward using delivered function
        reward = calculate_reward(plan, scenario_data['constraints'])
        
        # Update policy
        model.update_policy(reward)

model.save("checkpoints/rft_qbr.pt")
print("Training complete!")
```

---

## Summary: Clear Separation of Concerns

| Aspect | Data Team | Training Team |
|--------|-----------|---------------|
| **Generates** | Training data (JSON files) | Model checkpoints |
| **Implements** | Reward function code | Training loops |
| **Knows About** | ACRUE assertions, LLM-as-Judge | PyTorch, LoRA, DPO algorithms |
| **Delivers** | `data/`, `training/rft_reward_checker.py` | Trained models |
| **Tools** | `generate_pft_preference_pairs.py` | Standard ML frameworks |
| **Tests** | Data quality validation | Training convergence |

**Key Benefit**: Training Team can train models **without understanding** how preference pairs were generated or how reward functions were derived from assertions.
