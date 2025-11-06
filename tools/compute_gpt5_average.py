#!/usr/bin/env python3
"""
Compute Average Performance Across GPT-5 Trials

Given 3 GPT-5 trial results, compare each with gold standard
and compute average P/R/F1 scores with variance analysis.
"""

import json
import sys
from pathlib import Path
from typing import List, Dict, Any
from collections import defaultdict

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))


def load_json(file_path: str) -> Dict[str, Any]:
    """Load JSON file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def extract_compositions(trial_data: Dict[str, Any]) -> Dict[str, List[str]]:
    """Extract prompt_id -> tasks_covered mapping"""
    compositions = {}
    
    if "compositions" in trial_data:
        # Batch format (GPT-5 trials)
        for comp in trial_data["compositions"]:
            if not comp.get("error"):
                compositions[comp["prompt_id"]] = comp.get("tasks_covered", [])
    elif "prompt_analyses" in trial_data:
        # Gold standard format (dict mapping prompt_id -> analysis)
        for prompt_id, prompt_data in trial_data["prompt_analyses"].items():
            compositions[prompt_id] = prompt_data.get("tasks_covered", [])
    else:
        # Single composition format
        if not trial_data.get("error") and "prompt_id" in trial_data:
            compositions[trial_data["prompt_id"]] = trial_data.get("tasks_covered", [])
    
    return compositions


def compare_with_gold(
    trial_compositions: Dict[str, List[str]],
    gold_compositions: Dict[str, List[str]]
) -> Dict[str, Any]:
    """
    Compare trial with gold standard, return P/R/F1 metrics.
    """
    results = {
        "per_prompt": {},
        "aggregate": {
            "total_prompts": 0,
            "average_precision": 0.0,
            "average_recall": 0.0,
            "average_f1": 0.0
        }
    }
    
    precisions = []
    recalls = []
    f1s = []
    
    for prompt_id, gold_tasks in gold_compositions.items():
        if prompt_id not in trial_compositions:
            continue
        
        trial_tasks = set(trial_compositions[prompt_id])
        gold_set = set(gold_tasks)
        
        # Calculate metrics
        if len(trial_tasks) == 0:
            precision = 0.0
        else:
            precision = len(trial_tasks & gold_set) / len(trial_tasks)
        
        if len(gold_set) == 0:
            recall = 0.0
        else:
            recall = len(trial_tasks & gold_set) / len(gold_set)
        
        if precision + recall == 0:
            f1 = 0.0
        else:
            f1 = 2 * (precision * recall) / (precision + recall)
        
        results["per_prompt"][prompt_id] = {
            "precision": precision,
            "recall": recall,
            "f1": f1,
            "trial_tasks": sorted(list(trial_tasks)),
            "gold_tasks": sorted(list(gold_set)),
            "missing": sorted(list(gold_set - trial_tasks)),
            "extra": sorted(list(trial_tasks - gold_set))
        }
        
        precisions.append(precision)
        recalls.append(recall)
        f1s.append(f1)
    
    # Aggregate
    if precisions:
        results["aggregate"]["total_prompts"] = len(precisions)
        results["aggregate"]["average_precision"] = sum(precisions) / len(precisions)
        results["aggregate"]["average_recall"] = sum(recalls) / len(recalls)
        results["aggregate"]["average_f1"] = sum(f1s) / len(f1s)
    
    return results


def compute_statistics(values: List[float]) -> Dict[str, float]:
    """Compute mean and standard deviation"""
    if not values:
        return {"mean": 0.0, "std_dev": 0.0, "min": 0.0, "max": 0.0}
    
    mean = sum(values) / len(values)
    variance = sum((v - mean) ** 2 for v in values) / len(values)
    std_dev = variance ** 0.5
    
    return {
        "mean": mean,
        "std_dev": std_dev,
        "min": min(values),
        "max": max(values)
    }


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Compute average GPT-5 performance across 3 trials"
    )
    parser.add_argument(
        "trial1",
        type=str,
        help="Path to trial 1 results JSON"
    )
    parser.add_argument(
        "trial2",
        type=str,
        help="Path to trial 2 results JSON"
    )
    parser.add_argument(
        "trial3",
        type=str,
        help="Path to trial 3 results JSON"
    )
    parser.add_argument(
        "--gold",
        type=str,
        default="docs/gutt_analysis/model_comparison/gold_standard_analysis.json",
        help="Path to gold standard JSON"
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Output JSON file for average results"
    )
    
    args = parser.parse_args()
    
    # Load gold standard
    print("Loading gold standard...")
    gold_data = load_json(args.gold)
    gold_compositions = extract_compositions(gold_data)
    print(f"  ✅ Loaded {len(gold_compositions)} gold compositions")
    
    # Load all 3 trials
    print("\nLoading trial results...")
    trials = []
    for i, trial_file in enumerate([args.trial1, args.trial2, args.trial3], 1):
        trial_data = load_json(trial_file)
        trial_comps = extract_compositions(trial_data)
        print(f"  ✅ Trial {i}: {len(trial_comps)} compositions")
        trials.append(trial_comps)
    
    # Compare each trial with gold
    print("\n" + "=" * 80)
    print("COMPARING TRIALS WITH GOLD STANDARD")
    print("=" * 80)
    
    trial_results = []
    for i, trial_comps in enumerate(trials, 1):
        print(f"\nTrial {i}:")
        result = compare_with_gold(trial_comps, gold_compositions)
        trial_results.append(result)
        
        print(f"  Precision: {result['aggregate']['average_precision']:.4f}")
        print(f"  Recall:    {result['aggregate']['average_recall']:.4f}")
        print(f"  F1:        {result['aggregate']['average_f1']:.4f}")
    
    # Compute average and variance
    print("\n" + "=" * 80)
    print("AVERAGE PERFORMANCE ACROSS 3 TRIALS")
    print("=" * 80)
    
    precisions = [r["aggregate"]["average_precision"] for r in trial_results]
    recalls = [r["aggregate"]["average_recall"] for r in trial_results]
    f1s = [r["aggregate"]["average_f1"] for r in trial_results]
    
    precision_stats = compute_statistics(precisions)
    recall_stats = compute_statistics(recalls)
    f1_stats = compute_statistics(f1s)
    
    print(f"\n📊 Precision: {precision_stats['mean']:.4f} ± {precision_stats['std_dev']:.4f}")
    print(f"   Range: {precision_stats['min']:.4f} - {precision_stats['max']:.4f}")
    
    print(f"\n📊 Recall: {recall_stats['mean']:.4f} ± {recall_stats['std_dev']:.4f}")
    print(f"   Range: {recall_stats['min']:.4f} - {recall_stats['max']:.4f}")
    
    print(f"\n📊 F1 Score: {f1_stats['mean']:.4f} ± {f1_stats['std_dev']:.4f}")
    print(f"   Range: {f1_stats['min']:.4f} - {f1_stats['max']:.4f}")
    
    # Per-prompt variance analysis
    print("\n" + "=" * 80)
    print("PER-PROMPT F1 VARIANCE")
    print("=" * 80)
    
    prompt_f1s = defaultdict(list)
    for result in trial_results:
        for prompt_id, metrics in result["per_prompt"].items():
            prompt_f1s[prompt_id].append(metrics["f1"])
    
    for prompt_id in sorted(prompt_f1s.keys()):
        f1_values = prompt_f1s[prompt_id]
        stats = compute_statistics(f1_values)
        print(f"\n{prompt_id}:")
        print(f"  F1: {stats['mean']:.4f} ± {stats['std_dev']:.4f}")
        print(f"  Values: {', '.join(f'{v:.4f}' for v in f1_values)}")
        
        if stats['std_dev'] > 0.05:
            print(f"  ⚠️  High variance (>{5}%)")
    
    # Overall assessment
    print("\n" + "=" * 80)
    print("STABILITY ASSESSMENT")
    print("=" * 80)
    
    if f1_stats['std_dev'] < 0.02:
        stability = "EXCELLENT (< 2% variance)"
    elif f1_stats['std_dev'] < 0.05:
        stability = "GOOD (< 5% variance)"
    elif f1_stats['std_dev'] < 0.10:
        stability = "MODERATE (< 10% variance)"
    else:
        stability = "POOR (≥ 10% variance)"
    
    print(f"\nStability: {stability}")
    print(f"Average F1: {f1_stats['mean']:.2%} ± {f1_stats['std_dev']:.2%}")
    
    # Save results
    if args.output:
        average_results = {
            "metadata": {
                "trials": 3,
                "gold_standard": args.gold,
                "trial_files": [args.trial1, args.trial2, args.trial3]
            },
            "aggregate": {
                "precision": precision_stats,
                "recall": recall_stats,
                "f1": f1_stats,
                "stability": stability
            },
            "per_prompt_variance": {
                prompt_id: compute_statistics(f1_values)
                for prompt_id, f1_values in prompt_f1s.items()
            },
            "trial_results": trial_results
        }
        
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(average_results, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Saved average results to: {args.output}")
    
    print("\n" + "=" * 80)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
