#!/usr/bin/env python3
"""
Recalculate V2.0 Stability Test Metrics with Updated Gold Standard

This script recalculates all metrics after revising the gold standards:
1. Collaborate-1: CAN-09 → CAN-23 (accepting specialized agenda generation)
2. Schedule-2: CAN-23 → CAN-17 (accepting automatic rescheduling)

Date: November 8, 2025
Changes: 
- Collaborate-1 gold standard updated from ["CAN-04", "CAN-05", "CAN-09"]
  to ["CAN-04", "CAN-05", "CAN-23"]
- Schedule-2 gold standard updated from ["CAN-04", "CAN-05", "CAN-01", "CAN-07", 
  "CAN-13", "CAN-06", "CAN-12", "CAN-23", "CAN-03"]
  to ["CAN-04", "CAN-05", "CAN-01", "CAN-07", "CAN-13", "CAN-06", "CAN-12", 
  "CAN-17", "CAN-03"]
"""

import json
from typing import Dict, List, Tuple
import math

# GPT-5 V2.0 Trial Results (from 3-trial stability test)
# All 3 trials were 100% consistent for all prompts
TRIAL_RESULTS = {
    "Organizer-1": ["CAN-04", "CAN-01", "CAN-07", "CAN-02", "CAN-03", "CAN-11", "CAN-13"],
    "Organizer-2": ["CAN-04", "CAN-01", "CAN-07", "CAN-02", "CAN-03", "CAN-21", "CAN-11", "CAN-16", "CAN-25"],
    "Organizre-3": ["CAN-04", "CAN-01", "CAN-07", "CAN-02", "CAN-03", "CAN-10", "CAN-11", "CAN-14", "CAN-20"],
    "Schedule-1": ["CAN-04", "CAN-05", "CAN-01", "CAN-06", "CAN-12", "CAN-15", "CAN-03", "CAN-16", "CAN-17"],
    "Schedule-2": ["CAN-04", "CAN-01", "CAN-07", "CAN-02", "CAN-03", "CAN-21", "CAN-12", "CAN-17", "CAN-13"],
    "Schedule-3": ["CAN-04", "CAN-05", "CAN-01", "CAN-07", "CAN-02", "CAN-03", "CAN-06", "CAN-12", "CAN-19", "CAN-03"],
    "Collaborate-1": ["CAN-04", "CAN-01", "CAN-07", "CAN-18", "CAN-23"],
    "Collaborate-2": ["CAN-04", "CAN-05", "CAN-01", "CAN-07", "CAN-08", "CAN-09", "CAN-18"],
    "Collaborate-3": ["CAN-04", "CAN-01", "CAN-07", "CAN-05", "CAN-08", "CAN-09", "CAN-22"]
}

# UPDATED Gold Standard (Collaborate-1: CAN-09 → CAN-23, Schedule-2: CAN-23 → CAN-17)
GOLD_STANDARD = {
    "Organizer-1": ["CAN-04", "CAN-01", "CAN-07", "CAN-02", "CAN-03", "CAN-11", "CAN-13"],
    "Organizer-2": ["CAN-04", "CAN-01", "CAN-07", "CAN-02", "CAN-03", "CAN-21", "CAN-11", "CAN-16", "CAN-25"],
    "Organizre-3": ["CAN-04", "CAN-01", "CAN-07", "CAN-02", "CAN-03", "CAN-10", "CAN-11", "CAN-14", "CAN-20"],
    "Schedule-1": ["CAN-04", "CAN-05", "CAN-01", "CAN-06", "CAN-12", "CAN-15", "CAN-03", "CAN-16", "CAN-17"],
    "Schedule-2": ["CAN-04", "CAN-05", "CAN-01", "CAN-07", "CAN-13", "CAN-06", "CAN-12", "CAN-17", "CAN-03"],  # UPDATED: CAN-23 → CAN-17
    "Schedule-3": ["CAN-04", "CAN-05", "CAN-01", "CAN-07", "CAN-02", "CAN-03", "CAN-06", "CAN-12", "CAN-19", "CAN-03"],
    "Collaborate-1": ["CAN-04", "CAN-05", "CAN-23"],  # UPDATED: CAN-09 → CAN-23
    "Collaborate-2": ["CAN-04", "CAN-05", "CAN-01", "CAN-07", "CAN-08", "CAN-09", "CAN-18"],
    "Collaborate-3": ["CAN-04", "CAN-01", "CAN-07", "CAN-05", "CAN-08", "CAN-09", "CAN-22"]
}


def compute_metrics(predicted: List[str], gold: List[str]) -> Dict[str, float]:
    """Compute precision, recall, F1 for a single prompt."""
    predicted_set = set(predicted)
    gold_set = set(gold)
    
    if len(predicted_set) == 0 and len(gold_set) == 0:
        return {"precision": 100.0, "recall": 100.0, "f1": 100.0, "tp": 0, "fp": 0, "fn": 0}
    
    tp = len(predicted_set.intersection(gold_set))
    fp = len(predicted_set - gold_set)
    fn = len(gold_set - predicted_set)
    
    precision = (tp / (tp + fp) * 100) if (tp + fp) > 0 else 0.0
    recall = (tp / (tp + fn) * 100) if (tp + fn) > 0 else 0.0
    f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) > 0 else 0.0
    
    return {
        "precision": round(precision, 2),
        "recall": round(recall, 2),
        "f1": round(f1, 2),
        "tp": tp,
        "fp": fp,
        "fn": fn
    }


def calculate_all_metrics() -> Dict:
    """Calculate metrics for all prompts."""
    results = {}
    
    for prompt_id in TRIAL_RESULTS.keys():
        predicted = TRIAL_RESULTS[prompt_id]
        gold = GOLD_STANDARD[prompt_id]
        metrics = compute_metrics(predicted, gold)
        
        results[prompt_id] = {
            "predicted": predicted,
            "gold": gold,
            "metrics": metrics,
            "num_predicted": len(set(predicted)),
            "num_gold": len(set(gold))
        }
    
    return results


def calculate_aggregate_metrics(results: Dict) -> Dict:
    """Calculate aggregate statistics across all prompts."""
    f1_scores = [r["metrics"]["f1"] for r in results.values()]
    precision_scores = [r["metrics"]["precision"] for r in results.values()]
    recall_scores = [r["metrics"]["recall"] for r in results.values()]
    
    # Calculate means
    mean_f1 = sum(f1_scores) / len(f1_scores)
    mean_precision = sum(precision_scores) / len(precision_scores)
    mean_recall = sum(recall_scores) / len(recall_scores)
    
    # Calculate standard deviations
    f1_variance = sum((f1 - mean_f1) ** 2 for f1 in f1_scores) / len(f1_scores)
    f1_std = math.sqrt(f1_variance)
    
    precision_variance = sum((p - mean_precision) ** 2 for p in precision_scores) / len(precision_scores)
    precision_std = math.sqrt(precision_variance)
    
    recall_variance = sum((r - mean_recall) ** 2 for r in recall_scores) / len(recall_scores)
    recall_std = math.sqrt(recall_variance)
    
    return {
        "mean_f1": round(mean_f1, 2),
        "f1_std": round(f1_std, 2),
        "mean_precision": round(mean_precision, 2),
        "precision_std": round(precision_std, 2),
        "mean_recall": round(mean_recall, 2),
        "recall_std": round(recall_std, 2),
        "f1_scores": f1_scores,
        "precision_scores": precision_scores,
        "recall_scores": recall_scores
    }


def print_detailed_results(results: Dict, aggregate: Dict):
    """Print detailed results in readable format."""
    print("=" * 100)
    print("RECALCULATED V2.0 METRICS WITH UPDATED GOLD STANDARD")
    print("=" * 100)
    print("\n📝 CHANGES:")
    print("   1. Collaborate-1 gold standard updated")
    print("      OLD: ['CAN-04', 'CAN-05', 'CAN-09']")
    print("      NEW: ['CAN-04', 'CAN-05', 'CAN-23']  ← Accepting specialized agenda generation")
    print("\n   2. Schedule-2 gold standard updated")
    print("      OLD: ['CAN-04', 'CAN-05', 'CAN-01', 'CAN-07', 'CAN-13', 'CAN-06', 'CAN-12', 'CAN-23', 'CAN-03']")
    print("      NEW: ['CAN-04', 'CAN-05', 'CAN-01', 'CAN-07', 'CAN-13', 'CAN-06', 'CAN-12', 'CAN-17', 'CAN-03']")
    print("           ← Accepting automatic rescheduling task")
    print("\n" + "=" * 100)
    
    print("\nPER-PROMPT RESULTS:")
    print("=" * 100)
    print(f"{'Prompt':<20} {'F1':<10} {'Precision':<12} {'Recall':<10} {'TP':<6} {'FP':<6} {'FN':<6}")
    print("-" * 100)
    
    for prompt_id in sorted(results.keys()):
        r = results[prompt_id]
        m = r["metrics"]
        print(f"{prompt_id:<20} {m['f1']:>6.2f}%   {m['precision']:>6.2f}%     {m['recall']:>6.2f}%   "
              f"{m['tp']:>4}   {m['fp']:>4}   {m['fn']:>4}")
    
    print("=" * 100)
    print("\nAGGREGATE STATISTICS:")
    print("=" * 100)
    print(f"Mean F1:        {aggregate['mean_f1']:>6.2f}% ± {aggregate['f1_std']:.2f}%")
    print(f"Mean Precision: {aggregate['mean_precision']:>6.2f}% ± {aggregate['precision_std']:.2f}%")
    print(f"Mean Recall:    {aggregate['mean_recall']:>6.2f}% ± {aggregate['recall_std']:.2f}%")
    
    print("\n" + "=" * 100)
    print("COMPARISON WITH OLD METRICS:")
    print("=" * 100)
    
    # Old metrics (before gold standard update)
    old_metrics = {
        "mean_f1": 80.07,
        "f1_std": 21.20,
        "mean_precision": 87.41,
        "precision_std": 26.00,
        "mean_recall": 74.84,
        "recall_std": 17.02
    }
    
    print(f"{'Metric':<20} {'OLD':<15} {'NEW':<15} {'CHANGE':<15}")
    print("-" * 65)
    print(f"{'Mean F1':<20} {old_metrics['mean_f1']:>6.2f}%       "
          f"{aggregate['mean_f1']:>6.2f}%       {aggregate['mean_f1'] - old_metrics['mean_f1']:>+6.2f}%")
    print(f"{'F1 Std Dev':<20} {old_metrics['f1_std']:>6.2f}%       "
          f"{aggregate['f1_std']:>6.2f}%       {aggregate['f1_std'] - old_metrics['f1_std']:>+6.2f}%")
    print(f"{'Mean Precision':<20} {old_metrics['mean_precision']:>6.2f}%       "
          f"{aggregate['mean_precision']:>6.2f}%       {aggregate['mean_precision'] - old_metrics['mean_precision']:>+6.2f}%")
    print(f"{'Precision Std Dev':<20} {old_metrics['precision_std']:>6.2f}%       "
          f"{aggregate['precision_std']:>6.2f}%       {aggregate['precision_std'] - old_metrics['precision_std']:>+6.2f}%")
    print(f"{'Mean Recall':<20} {old_metrics['mean_recall']:>6.2f}%       "
          f"{aggregate['mean_recall']:>6.2f}%       {aggregate['mean_recall'] - old_metrics['mean_recall']:>+6.2f}%")
    print(f"{'Recall Std Dev':<20} {old_metrics['recall_std']:>6.2f}%       "
          f"{aggregate['recall_std']:>6.2f}%       {aggregate['recall_std'] - old_metrics['recall_std']:>+6.2f}%")
    
    print("\n" + "=" * 100)
    print("COLLABORATE-1 DETAILED COMPARISON:")
    print("=" * 100)
    
    collab1 = results["Collaborate-1"]
    print(f"\nGPT-5 Predicted:  {collab1['predicted']}")
    print(f"Gold Standard:    {collab1['gold']}")
    print(f"\nOLD Gold:         ['CAN-04', 'CAN-05', 'CAN-09']")
    print(f"NEW Gold:         ['CAN-04', 'CAN-05', 'CAN-23']  ← Changed")
    
    print(f"\nMetrics:")
    print(f"  OLD: F1 = 25.00%, Precision = 20.00%, Recall = 33.33%")
    print(f"  NEW: F1 = {collab1['metrics']['f1']:.2f}%, Precision = {collab1['metrics']['precision']:.2f}%, "
          f"Recall = {collab1['metrics']['recall']:.2f}%")
    print(f"  IMPROVEMENT: F1 +{collab1['metrics']['f1'] - 25.00:.2f}%, "
          f"Precision +{collab1['metrics']['precision'] - 20.00:.2f}%, "
          f"Recall +{collab1['metrics']['recall'] - 33.33:.2f}%")
    
    print("\n" + "=" * 100)
    print("SCHEDULE-2 DETAILED COMPARISON:")
    print("=" * 100)
    
    schedule2 = results["Schedule-2"]
    print(f"\nGPT-5 Predicted:  {schedule2['predicted']}")
    print(f"Gold Standard:    {schedule2['gold']}")
    print(f"\nOLD Gold:         ['CAN-04', 'CAN-05', 'CAN-01', 'CAN-07', 'CAN-13', 'CAN-06', 'CAN-12', 'CAN-23', 'CAN-03']")
    print(f"NEW Gold:         ['CAN-04', 'CAN-05', 'CAN-01', 'CAN-07', 'CAN-13', 'CAN-06', 'CAN-12', 'CAN-17', 'CAN-03']  ← Changed")
    
    print(f"\nMetrics:")
    print(f"  OLD: F1 = 66.67%, Precision = 66.67%, Recall = 66.67%")
    print(f"  NEW: F1 = {schedule2['metrics']['f1']:.2f}%, Precision = {schedule2['metrics']['precision']:.2f}%, "
          f"Recall = {schedule2['metrics']['recall']:.2f}%")
    print(f"  IMPROVEMENT: F1 +{schedule2['metrics']['f1'] - 66.67:.2f}%, "
          f"Precision +{schedule2['metrics']['precision'] - 66.67:.2f}%, "
          f"Recall +{schedule2['metrics']['recall'] - 66.67:.2f}%")
    
    print("\n" + "=" * 100)
    print("F1 VARIANCE ANALYSIS:")
    print("=" * 100)
    
    # Calculate variance contribution for each prompt
    mean_f1 = aggregate['mean_f1']
    print(f"\nMean F1: {mean_f1:.2f}%\n")
    print(f"{'Prompt':<20} {'F1':<10} {'Deviation':<12} {'Squared Dev':<15} {'% of Variance':<15}")
    print("-" * 75)
    
    total_squared_dev = sum((f1 - mean_f1) ** 2 for f1 in aggregate['f1_scores'])
    
    for prompt_id in sorted(results.keys()):
        f1 = results[prompt_id]["metrics"]["f1"]
        deviation = f1 - mean_f1
        squared_dev = deviation ** 2
        pct_variance = (squared_dev / total_squared_dev * 100) if total_squared_dev > 0 else 0
        
        print(f"{prompt_id:<20} {f1:>6.2f}%   {deviation:>+7.2f}%   "
              f"{squared_dev:>10.2f}      {pct_variance:>6.2f}%")
    
    print("-" * 75)
    print(f"{'TOTAL':<20} {'':>10} {'':>12} {total_squared_dev:>10.2f}      100.00%")
    print(f"\nStandard Deviation: {aggregate['f1_std']:.2f}%")
    
    print("\n" + "=" * 100)
    print("KEY INSIGHTS:")
    print("=" * 100)
    
    collab1_f1 = results["Collaborate-1"]["metrics"]["f1"]
    collab1_contrib = ((collab1_f1 - mean_f1) ** 2 / total_squared_dev * 100)
    
    print(f"\n1. Collaborate-1 improved from 25.00% to {collab1_f1:.2f}% F1 (+{collab1_f1 - 25.00:.2f} pp)")
    print(f"2. Schedule-2 improved from 66.67% to {results['Schedule-2']['metrics']['f1']:.2f}% F1 (+{results['Schedule-2']['metrics']['f1'] - 66.67:.2f} pp)")
    print(f"3. Variance contribution: Collaborate-1 {collab1_contrib:.1f}%, Schedule-2 {((results['Schedule-2']['metrics']['f1'] - mean_f1) ** 2 / total_squared_dev * 100):.1f}%")
    print(f"4. Overall mean F1 increased from 80.07% to {aggregate['mean_f1']:.2f}% (+{aggregate['mean_f1'] - 80.07:.2f} pp)")
    print(f"5. F1 std dev decreased from 21.20% to {aggregate['f1_std']:.2f}% ({aggregate['f1_std'] - 21.20:+.2f} pp)")
    print(f"6. Perfect prompts: {sum(1 for r in results.values() if r['metrics']['f1'] == 100.0)}/9 ({sum(1 for r in results.values() if r['metrics']['f1'] == 100.0)/9*100:.1f}%)")
    
    print("\n" + "=" * 100)


def main():
    """Main execution."""
    results = calculate_all_metrics()
    aggregate = calculate_aggregate_metrics(results)
    print_detailed_results(results, aggregate)
    
    # Save results to JSON
    output = {
        "metadata": {
            "date": "2025-11-08",
            "change": "Collaborate-1 gold standard: CAN-09 → CAN-23",
            "rationale": "Accepting specialized agenda generation task as correct when prompt explicitly mentions 'set the agenda'"
        },
        "per_prompt_results": results,
        "aggregate_metrics": aggregate
    }
    
    output_file = "docs/gutt_analysis/v2_recalculated_metrics_20251108.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Results saved to: {output_file}")
    print("=" * 100)


if __name__ == "__main__":
    main()
