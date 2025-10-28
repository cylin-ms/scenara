# Human Validation Protocol for Meeting Classification

## Purpose
Establish ground truth accuracy by comparing LLM classifications against human expert labels.

## Validation Set Selection
- **Size**: 20-50 meetings (statistically significant)
- **Source**: Real calendar data from multiple users
- **Coverage**: All 5 categories represented
- **Difficulty**: Mix of clear cases (90%) and ambiguous cases (10%)

## Human Labeling Process

### Step 1: Independent Expert Classification
**Experts Needed**: 2-3 domain experts (product managers, meeting organizers, executive assistants)

**Labeling Form** (for each meeting):
```json
{
  "meeting_id": "...",
  "subject": "...",
  "description": "...",
  "attendees_count": 10,
  "duration_minutes": 60,
  
  "expert_classification": {
    "specific_type": "Progress Review Meeting",
    "primary_category": "Internal Recurring Meetings (Cadence)",
    "confidence": 0.95,
    "reasoning": "Weekly cadence + 'Flight Review' terminology indicates formal progress tracking",
    "alternative_types": ["Team Status Update Meeting"],
    "difficulty": "easy|medium|hard"
  },
  
  "expert_name": "Chin-Yew Lin",
  "labeling_date": "2025-10-28"
}
```

### Step 2: Inter-Rater Agreement
Calculate Cohen's Kappa or Fleiss' Kappa:
- **κ > 0.8**: Excellent agreement → proceed
- **κ 0.6-0.8**: Good agreement → discuss discrepancies
- **κ < 0.6**: Poor agreement → refine taxonomy or training

### Step 3: Resolve Discrepancies
For meetings where experts disagree:
1. Review together
2. Discuss reasoning
3. Reach consensus or mark as "genuinely ambiguous"
4. Document decision rationale

### Step 4: Create Gold Standard Dataset
```json
{
  "validation_set": {
    "version": "1.0",
    "creation_date": "2025-10-28",
    "total_meetings": 50,
    "experts": ["Expert 1", "Expert 2", "Expert 3"],
    "inter_rater_agreement": 0.87,
    
    "meetings": [
      {
        "meeting_id": "...",
        "ground_truth": {
          "specific_type": "Progress Review Meeting",
          "primary_category": "Internal Recurring Meetings (Cadence)",
          "confidence": 1.0,
          "expert_consensus": 3,
          "difficulty": "easy"
        },
        "expert_labels": [...]
      }
    ]
  }
}
```

## LLM Validation Metrics

### Accuracy Metrics
```python
def calculate_accuracy(llm_results, ground_truth):
    """
    Compare LLM classifications against human expert ground truth
    """
    metrics = {
        # Exact match (specific type)
        "type_accuracy": 0.0,
        
        # Category match (primary category)
        "category_accuracy": 0.0,
        
        # Top-2 accuracy (specific type in top 2 alternatives)
        "type_top2_accuracy": 0.0,
        
        # Weighted by difficulty
        "easy_accuracy": 0.0,
        "medium_accuracy": 0.0,
        "hard_accuracy": 0.0,
        
        # Confusion matrix
        "confusion_matrix": {},
        
        # Error analysis
        "errors": []
    }
    
    correct_type = 0
    correct_category = 0
    
    for llm_result, truth in zip(llm_results, ground_truth):
        # Type accuracy
        if llm_result['specific_type'] == truth['specific_type']:
            correct_type += 1
        else:
            metrics['errors'].append({
                'meeting': llm_result['subject'],
                'predicted': llm_result['specific_type'],
                'actual': truth['specific_type'],
                'llm_confidence': llm_result['confidence']
            })
        
        # Category accuracy
        if llm_result['primary_category'] == truth['primary_category']:
            correct_category += 1
    
    metrics['type_accuracy'] = correct_type / len(ground_truth)
    metrics['category_accuracy'] = correct_category / len(ground_truth)
    
    return metrics
```

### Success Criteria
- **Type Accuracy**: Target ≥ 80% (specific type match)
- **Category Accuracy**: Target ≥ 90% (primary category match)
- **Easy Cases**: Target ≥ 95% (unambiguous meetings)
- **Medium Cases**: Target ≥ 80% (some ambiguity)
- **Hard Cases**: Target ≥ 60% (genuinely ambiguous)

## Error Analysis

### Common Error Patterns to Track
1. **Keyword Confusion**: "Prep" → Status vs Planning
2. **Ambiguous Labels**: "[Async Task]" → Informational vs Status
3. **Multi-Purpose Meetings**: Blend of types
4. **Recurrence Misclassification**: One-time vs recurring
5. **Audience Size Errors**: Small group vs broadcast

### Root Cause Classification
For each error:
- **Taxonomy Gap**: Meeting type not in taxonomy (suggest new type)
- **Prompt Clarity**: Insufficient guidance in prompt (improve prompt)
- **LLM Limitation**: Model doesn't understand context (consider alternative model)
- **Data Quality**: Missing attendee/duration info (improve extraction)
- **Genuine Ambiguity**: Multiple valid interpretations (document in taxonomy)

## Validation Workflow

```
1. Extract 50 meetings from calendar
   ↓
2. Remove PII, prepare labeling form
   ↓
3. 2-3 experts independently label
   ↓
4. Calculate inter-rater agreement
   ↓
5. Resolve discrepancies → Gold standard
   ↓
6. Run LLM classification (GPT-5, Copilot, Ollama)
   ↓
7. Calculate accuracy metrics
   ↓
8. Error analysis → Prompt improvements
   ↓
9. Re-run validation → Measure improvement
   ↓
10. Publish validated dataset
```

## Example Validation Report

```markdown
# Meeting Classification Validation Report

**Date**: October 28, 2025
**Validation Set**: 50 meetings
**Experts**: 3 domain experts
**Inter-Rater Agreement**: κ = 0.87 (excellent)

## Results

### GPT-5 (Centralized Prompt v1.0)
- Type Accuracy: 82% (41/50)
- Category Accuracy: 92% (46/50)
- Easy Cases: 96% (24/25)
- Medium Cases: 75% (12/16)
- Hard Cases: 56% (5/9)

### GitHub Copilot (Centralized Prompt v1.0)
- Type Accuracy: 84% (42/50)
- Category Accuracy: 94% (47/50)
- Easy Cases: 96% (24/25)
- Medium Cases: 81% (13/16)
- Hard Cases: 56% (5/9)

### Error Analysis
Top 3 Error Patterns:
1. "Meeting Prep" → Status (5 cases) - should be Planning
2. "[Async Task]" → ambiguous (3 cases) - needs taxonomy clarification
3. Office Hours → Training vs Informational (2 cases)

### Improvements Implemented
1. Added "Prep" keyword guidance to prompt → +8% accuracy
2. Defined "[Async Task]" classification rule → +4% accuracy
3. Clarified Office Hours in taxonomy → +2% accuracy

### Re-Validation Results
- GPT-5 Type Accuracy: 82% → 90% (+8%)
- Copilot Type Accuracy: 84% → 92% (+8%)
```

## Tools for Validation

### Create Validation Set Tool
```python
def create_validation_set(calendar_data, size=50):
    """
    Sample diverse meetings for human labeling
    """
    import random
    
    # Stratified sampling by tentative category
    meetings_by_category = {}
    for meeting in calendar_data:
        # Use simple heuristics for initial grouping
        category = guess_category(meeting)
        if category not in meetings_by_category:
            meetings_by_category[category] = []
        meetings_by_category[category].append(meeting)
    
    # Sample proportionally
    validation_set = []
    for category, meetings in meetings_by_category.items():
        sample_size = max(5, int(size * len(meetings) / len(calendar_data)))
        validation_set.extend(random.sample(meetings, min(sample_size, len(meetings))))
    
    return validation_set[:size]
```

### Human Labeling Interface
```python
def create_labeling_interface(validation_set):
    """
    Generate Excel/Google Sheets for human labeling
    """
    import pandas as pd
    
    df = pd.DataFrame([
        {
            'Meeting ID': m['id'],
            'Subject': m['subject'],
            'Description': m['bodyPreview'][:200],
            'Attendees': len(m.get('attendees', [])),
            'Duration': 60,  # Calculate from start/end
            
            # Human to fill in:
            'Specific Type': '',
            'Primary Category': '',
            'Confidence (0-100)': '',
            'Reasoning': '',
            'Alternative Types': '',
            'Difficulty (easy/medium/hard)': '',
            'Expert Name': ''
        }
        for m in validation_set
    ])
    
    df.to_excel('validation_labeling_form.xlsx', index=False)
    print(f"Created labeling form with {len(validation_set)} meetings")
```

### Accuracy Calculator
```python
def calculate_validation_metrics(llm_results_file, ground_truth_file):
    """
    Compare LLM results against ground truth
    """
    import json
    from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
    
    llm_data = json.load(open(llm_results_file))
    truth_data = json.load(open(ground_truth_file))
    
    y_true_type = [m['ground_truth']['specific_type'] for m in truth_data['meetings']]
    y_pred_type = [m['classification']['specific_type'] for m in llm_data['meetings']]
    
    y_true_cat = [m['ground_truth']['primary_category'] for m in truth_data['meetings']]
    y_pred_cat = [m['classification']['primary_category'] for m in llm_data['meetings']]
    
    print("=== VALIDATION RESULTS ===")
    print(f"Type Accuracy: {accuracy_score(y_true_type, y_pred_type):.1%}")
    print(f"Category Accuracy: {accuracy_score(y_true_cat, y_pred_cat):.1%}")
    print("\nClassification Report (Types):")
    print(classification_report(y_true_type, y_pred_type))
    
    # Error analysis
    errors = []
    for i, (true_type, pred_type) in enumerate(zip(y_true_type, y_pred_type)):
        if true_type != pred_type:
            errors.append({
                'meeting': llm_data['meetings'][i]['subject'],
                'predicted': pred_type,
                'actual': true_type,
                'confidence': llm_data['meetings'][i]['classification']['confidence']
            })
    
    print(f"\nErrors: {len(errors)}")
    for error in errors[:5]:  # Show first 5
        print(f"  - {error['meeting']}")
        print(f"    Predicted: {error['predicted']} ({error['confidence']:.0%})")
        print(f"    Actual: {error['actual']}")
```

## Recommended Next Steps

1. **Create validation set** (20-50 meetings)
2. **Recruit 2-3 domain experts** (you + colleagues)
3. **Independent labeling** (1-2 hours per expert)
4. **Calculate inter-rater agreement**
5. **Resolve discrepancies** → gold standard
6. **Run LLM validation** → accuracy metrics
7. **Error analysis** → prompt improvements
8. **Iterate** until target accuracy achieved

## Benefits

✅ **Objective Accuracy Measurement**: Know true performance, not just consistency
✅ **Error Pattern Discovery**: Find systematic issues in taxonomy/prompt
✅ **Prompt Optimization**: Data-driven improvements
✅ **Model Selection**: Choose best-performing LLM
✅ **Confidence Calibration**: Validate that high confidence = high accuracy
✅ **Taxonomy Refinement**: Identify missing types or ambiguous definitions
✅ **User Trust**: Demonstrate validated accuracy to stakeholders

---

**Without this validation, we only know models agree 87.5% of the time, not whether they're correct 87.5% of the time!**
