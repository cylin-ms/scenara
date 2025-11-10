#!/usr/bin/env python3
"""
Compare GPT-5 Compositions Against Gold Standard

Evaluates GPT-5's execution compositions with metrics:
- Task coverage accuracy (Precision, Recall, F1)
- Missing critical tasks
- Extra/unnecessary tasks
- Per-prompt and aggregate scores
"""

import json
import sys
import argparse
from pathlib import Path
from typing import Dict, Set, List


def load_files(gpt5_file: str, gold_file: str):
    """Load GPT-5 compositions and gold standard"""
    with open(gpt5_file, 'r', encoding='utf-8') as f:
        gpt5_data = json.load(f)
    
    with open(gold_file, 'r', encoding='utf-8') as f:
        gold_data = json.load(f)
    
    return gpt5_data, gold_data


def calculate_metrics(predicted: Set[str], gold: Set[str]) -> Dict:
    """Calculate precision, recall, F1"""
    tp = predicted & gold
    fp = predicted - gold
    fn = gold - predicted
    
    precision = len(tp) / len(predicted) if predicted else 0
    recall = len(tp) / len(gold) if gold else 0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    
    return {
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "correct_tasks": list(tp),
        "missing_tasks": list(fn),
        "extra_tasks": list(fp)
    }


def main():
    parser = argparse.ArgumentParser(description="Compare GPT-5 against gold standard")
    parser.add_argument("gpt5_file", help="Path to GPT-5 compositions JSON")
    parser.add_argument(
        "--gold",
        default="docs/gutt_analysis/gold_standard_analysis.json",
        help="Path to gold standard"
    )
    
    args = parser.parse_args()
    
    print("=" * 100)
    print("GPT-5 VS GOLD STANDARD EVALUATION")
    print("=" * 100)
    
    # Load data
    gpt5_data, gold_data = load_files(args.gpt5_file, args.gold)
    
    print(f"\n📁 GPT-5 file: {args.gpt5_file}")
    print(f"📁 Gold file: {args.gold}")
    
    # Evaluate each prompt
    results = {}
    scores = []
    
    print("\n" + "=" * 100)
    print("PER-PROMPT EVALUATION")
    print("=" * 100)
    
    for prompt_id, gpt5_comp in gpt5_data['compositions'].items():
        if 'error' in gpt5_comp:
            print(f"\n❌ {prompt_id}: Error in GPT-5 composition")
            continue
        
        if prompt_id not in gold_data['prompt_analyses']:
            print(f"\n⚠️  {prompt_id}: Not in gold standard")
            continue
        
        gold_comp = gold_data['prompt_analyses'][prompt_id]
        
        # Get task sets
        gpt5_tasks = set(gpt5_comp.get('tasks_covered', []))
        gold_tasks = set(gold_comp.get('tasks_covered', []))
        
        # Calculate metrics
        metrics = calculate_metrics(gpt5_tasks, gold_tasks)
        results[prompt_id] = metrics
        scores.append(metrics['f1'])
        
        # Print results
        status = "✓" if metrics['f1'] >= 0.8 else "⚠️" if metrics['f1'] >= 0.6 else "❌"
        print(f"\n{status} {prompt_id}:")
        print(f"   Precision: {metrics['precision']:.2%} | Recall: {metrics['recall']:.2%} | F1: {metrics['f1']:.2%}")
        print(f"   GPT-5:  {', '.join(sorted(gpt5_tasks))}")
        print(f"   Gold:   {', '.join(sorted(gold_tasks))}")
        
        if metrics['missing_tasks']:
            print(f"   ❌ Missing: {', '.join(metrics['missing_tasks'])}")
        if metrics['extra_tasks']:
            print(f"   ➕ Extra: {', '.join(metrics['extra_tasks'])}")
    
    # Aggregate scores
    print("\n" + "=" * 100)
    print("AGGREGATE SCORES")
    print("=" * 100)
    
    avg_precision = sum(r['precision'] for r in results.values()) / len(results)
    avg_recall = sum(r['recall'] for r in results.values()) / len(results)
    avg_f1 = sum(scores) / len(scores)
    
    print(f"\n📊 GPT-5 Performance:")
    print(f"   Average Precision: {avg_precision:.2%}")
    print(f"   Average Recall:    {avg_recall:.2%}")
    print(f"   Average F1:        {avg_f1:.2%}")
    print(f"   Prompts Evaluated: {len(results)}/9")
    
    # Performance breakdown
    excellent = sum(1 for f1 in scores if f1 >= 0.9)
    good = sum(1 for f1 in scores if 0.8 <= f1 < 0.9)
    fair = sum(1 for f1 in scores if 0.6 <= f1 < 0.8)
    poor = sum(1 for f1 in scores if f1 < 0.6)
    
    print(f"\n📈 Performance Breakdown:")
    print(f"   Excellent (F1 ≥ 0.9): {excellent} prompts")
    print(f"   Good (F1 ≥ 0.8):      {good} prompts")
    print(f"   Fair (F1 ≥ 0.6):      {fair} prompts")
    print(f"   Poor (F1 < 0.6):      {poor} prompts")
    
    # Systematic analysis
    print("\n" + "=" * 100)
    print("SYSTEMATIC GAP ANALYSIS")
    print("=" * 100)
    
    all_missing = set()
    all_extra = set()
    
    for metrics in results.values():
        all_missing.update(metrics['missing_tasks'])
        all_extra.update(metrics['extra_tasks'])
    
    if all_missing:
        print(f"\n⚠️  Tasks frequently missed by GPT-5:")
        missing_freq = {}
        for task in all_missing:
            missing_freq[task] = sum(1 for m in results.values() if task in m['missing_tasks'])
        for task, freq in sorted(missing_freq.items(), key=lambda x: x[1], reverse=True):
            print(f"   {task}: missed in {freq} prompts")
    
    if all_extra:
        print(f"\n➕ Tasks frequently added unnecessarily:")
        extra_freq = {}
        for task in all_extra:
            extra_freq[task] = sum(1 for m in results.values() if task in m['extra_tasks'])
        for task, freq in sorted(extra_freq.items(), key=lambda x: x[1], reverse=True):
            print(f"   {task}: added in {freq} prompts")
    
    # Overall assessment
    print("\n" + "=" * 100)
    print("ASSESSMENT")
    print("=" * 100)
    
    if avg_f1 >= 0.9:
        grade = "EXCELLENT"
        assessment = "GPT-5 nearly matches gold standard"
    elif avg_f1 >= 0.8:
        grade = "GOOD"
        assessment = "GPT-5 performs well with minor gaps"
    elif avg_f1 >= 0.6:
        grade = "FAIR"
        assessment = "GPT-5 has some gaps but reasonable coverage"
    else:
        grade = "NEEDS IMPROVEMENT"
        assessment = "GPT-5 has significant gaps in task selection"
    
    print(f"\n🎯 Overall Grade: {grade}")
    print(f"   {assessment}")
    print(f"   Average F1 Score: {avg_f1:.2%}")
    
    print("\n" + "=" * 100)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
