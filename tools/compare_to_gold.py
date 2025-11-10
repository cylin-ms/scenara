"""
Universal comparison script for evaluating LLM execution compositions against gold standard.
Handles both dict-based (GPT-5) and list-based (Claude) composition formats.
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple

def load_files(model_file: str, gold_file: str = "docs/gutt_analysis/gold_standard_analysis.json") -> Tuple[Dict, Dict]:
    """Load model compositions and gold standard files."""
    with open(model_file, 'r', encoding='utf-8') as f:
        model_data = json.load(f)
    
    with open(gold_file, 'r', encoding='utf-8') as f:
        gold_data = json.load(f)
    
    return model_data, gold_data

def normalize_compositions(model_data: Dict) -> Dict[str, Set[str]]:
    """
    Normalize compositions to dict of {prompt_id: set(task_ids)}.
    Handles multiple formats: compositions (dict/list) and prompt_analyses (dict).
    """
    compositions = {}
    
    # Try 'compositions' key first
    comp_data = model_data.get('compositions')
    
    # Fall back to 'prompt_analyses' (gold standard format)
    if comp_data is None:
        comp_data = model_data.get('prompt_analyses', {})
    
    if isinstance(comp_data, dict):
        # GPT-5 or Gold Standard format: dict with prompt_id as keys
        for prompt_id, comp in comp_data.items():
            # Try 'tasks_covered' first, then extract from execution_plan
            tasks = comp.get('tasks_covered')
            if tasks is None:
                # Gold standard format: extract task_ids from execution_plan
                tasks = [step['task_id'] for step in comp.get('execution_plan', [])]
            compositions[prompt_id] = set(tasks)
    elif isinstance(comp_data, list):
        # Claude format: list of composition objects
        for comp in comp_data:
            prompt_id = comp.get('prompt_id')
            tasks = set(comp.get('tasks_covered', []))
            compositions[prompt_id] = tasks
    
    return compositions

def calculate_metrics(predicted: Set[str], gold: Set[str]) -> Tuple[float, float, float, Set[str], Set[str]]:
    """Calculate Precision, Recall, F1, and identify missing/extra tasks."""
    tp = predicted & gold  # True positives
    fp = predicted - gold  # False positives (extra tasks)
    fn = gold - predicted  # False negatives (missing tasks)
    
    precision = len(tp) / len(predicted) if len(predicted) > 0 else 0
    recall = len(tp) / len(gold) if len(gold) > 0 else 0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    
    return precision, recall, f1, fn, fp

def get_model_name(model_data: Dict) -> str:
    """Extract model name from data."""
    if 'metadata' in model_data:
        return model_data['metadata'].get('model', 'Unknown Model')
    return model_data.get('model', 'Unknown Model')

def main():
    if len(sys.argv) < 2:
        print("Usage: python compare_to_gold.py <model_compositions.json>")
        return 1
    
    model_file = sys.argv[1]
    model_data, gold_data = load_files(model_file)
    
    model_name = get_model_name(model_data)
    model_comps = normalize_compositions(model_data)
    gold_comps = normalize_compositions(gold_data)
    
    print("=" * 100)
    print(f"{model_name.upper()} VS GOLD STANDARD EVALUATION")
    print("=" * 100)
    print()
    print(f"📁 Model file: {model_file}")
    print(f"📁 Gold file: docs/gutt_analysis/gold_standard_analysis.json")
    print()
    
    # Per-prompt evaluation
    print("=" * 100)
    print("PER-PROMPT EVALUATION")
    print("=" * 100)
    print()
    
    results = []
    for prompt_id in sorted(gold_comps.keys()):
        if prompt_id not in model_comps:
            print(f"⚠️  {prompt_id}: Not found in model output")
            continue
        
        model_tasks = model_comps[prompt_id]
        gold_tasks = gold_comps[prompt_id]
        
        precision, recall, f1, missing, extra = calculate_metrics(model_tasks, gold_tasks)
        results.append({
            'prompt_id': prompt_id,
            'precision': precision,
            'recall': recall,
            'f1': f1,
            'missing': missing,
            'extra': extra
        })
        
        # Status indicator
        if f1 >= 0.9:
            status = "✓"
        elif f1 >= 0.6:
            status = "✓" if f1 >= 0.8 else "⚠️"
        else:
            status = "❌"
        
        print(f"{status} {prompt_id}:")
        print(f"   Precision: {precision*100:.2f}% | Recall: {recall*100:.2f}% | F1: {f1*100:.2f}%")
        print(f"   Model:  {', '.join(sorted(model_tasks))}")
        print(f"   Gold:   {', '.join(sorted(gold_tasks))}")
        
        if missing:
            print(f"   ❌ Missing: {', '.join(sorted(missing))}")
        if extra:
            print(f"   ➕ Extra: {', '.join(sorted(extra))}")
        print()
    
    # Aggregate scores
    print("=" * 100)
    print("AGGREGATE SCORES")
    print("=" * 100)
    print()
    
    avg_precision = sum(r['precision'] for r in results) / len(results)
    avg_recall = sum(r['recall'] for r in results) / len(results)
    avg_f1 = sum(r['f1'] for r in results) / len(results)
    
    print(f"📊 {model_name} Performance:")
    print(f"   Average Precision: {avg_precision*100:.2f}%")
    print(f"   Average Recall:    {avg_recall*100:.2f}%")
    print(f"   Average F1:        {avg_f1*100:.2f}%")
    print(f"   Prompts Evaluated: {len(results)}/{len(gold_comps)}")
    print()
    
    # Performance breakdown
    excellent = sum(1 for r in results if r['f1'] >= 0.9)
    good = sum(1 for r in results if 0.8 <= r['f1'] < 0.9)
    fair = sum(1 for r in results if 0.6 <= r['f1'] < 0.8)
    poor = sum(1 for r in results if r['f1'] < 0.6)
    
    print("📈 Performance Breakdown:")
    print(f"   Excellent (F1 ≥ 0.9): {excellent} prompts")
    print(f"   Good (F1 ≥ 0.8):      {good} prompts")
    print(f"   Fair (F1 ≥ 0.6):      {fair} prompts")
    print(f"   Poor (F1 < 0.6):      {poor} prompts")
    print()
    
    # Systematic gap analysis
    print("=" * 100)
    print("SYSTEMATIC GAP ANALYSIS")
    print("=" * 100)
    print()
    
    # Count missing tasks across all prompts
    missing_counts = {}
    extra_counts = {}
    
    for r in results:
        for task in r['missing']:
            missing_counts[task] = missing_counts.get(task, 0) + 1
        for task in r['extra']:
            extra_counts[task] = extra_counts.get(task, 0) + 1
    
    if missing_counts:
        print("⚠️  Tasks frequently missed by model:")
        for task, count in sorted(missing_counts.items(), key=lambda x: -x[1]):
            print(f"   {task}: missed in {count} prompts")
        print()
    
    if extra_counts:
        print("➕ Tasks frequently added unnecessarily:")
        for task, count in sorted(extra_counts.items(), key=lambda x: -x[1]):
            print(f"   {task}: added in {count} prompts")
        print()
    
    # Overall assessment
    print("=" * 100)
    print("ASSESSMENT")
    print("=" * 100)
    print()
    
    if avg_f1 >= 0.9:
        grade = "EXCELLENT"
        assessment = f"{model_name} shows exceptional task composition"
    elif avg_f1 >= 0.8:
        grade = "GOOD"
        assessment = f"{model_name} demonstrates strong task understanding"
    elif avg_f1 >= 0.6:
        grade = "FAIR"
        assessment = f"{model_name} has some gaps but reasonable coverage"
    else:
        grade = "POOR"
        assessment = f"{model_name} needs significant improvement"
    
    print(f"🎯 Overall Grade: {grade}")
    print(f"   {assessment}")
    print(f"   Average F1 Score: {avg_f1*100:.2f}%")
    print()
    print("=" * 100)
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
