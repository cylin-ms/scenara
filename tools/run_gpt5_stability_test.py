#!/usr/bin/env python3
"""
GPT-5 Execution Composition Stability Test

Run GPT-5 analysis 3 times with optimized prompts to:
1. Verify prompt optimization improvements
2. Measure stability/variance across runs
3. Compute average performance metrics
4. Identify non-deterministic behavior patterns

This ensures our GPT-5 evaluation is robust and reproducible.
"""

import os
import sys
import json
import time
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any
from collections import defaultdict

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from tools.gpt5_execution_composer import GPT5ExecutionComposer
except ImportError:
    try:
        from gpt5_execution_composer import GPT5ExecutionComposer
    except ImportError:
        print("ERROR: Could not import GPT5ExecutionComposer")
        print("Make sure tools/gpt5_execution_composer.py is available")
        sys.exit(1)


# EXACT same 9 hero prompts for fair comparison
HERO_PROMPTS = [
    {
        "id": "organizer-1",
        "category": "organizer",
        "prompt": "Show me my pending invitations and which ones I should prioritize based on my priorities for this week: customer meetings and product strategy."
    },
    {
        "id": "organizer-2",
        "category": "organizer",
        "prompt": "I have some important meetings this week—flag the ones I need to prep for, and put time on my calendar to prepare."
    },
    {
        "id": "organizer-3",
        "category": "organizer",
        "prompt": "Show me how my meeting time is broken down this month and where I could reclaim time to focus on product development."
    },
    {
        "id": "schedule-1",
        "category": "schedule",
        "prompt": "Schedule my weekly 1:1 with Alex every Monday at 10am. If there's a conflict, auto-bump movable meetings."
    },
    {
        "id": "schedule-2",
        "category": "schedule",
        "prompt": "I need to focus this afternoon. Bump all movable meetings to tomorrow or later this week."
    },
    {
        "id": "schedule-3",
        "category": "schedule",
        "prompt": "Set up a team sync for next Tuesday at 2pm with Sarah, Mike, and the design team. Book the large conference room and prioritize this over non-customer meetings if there's a conflict."
    },
    {
        "id": "collaborate-1",
        "category": "collaborate",
        "prompt": "Pull together a prep agenda for my customer pitch on Friday, including recent work updates from the team."
    },
    {
        "id": "collaborate-2",
        "category": "collaborate",
        "prompt": "Pull a briefing doc for my 1:1 with Jamie tomorrow, including what we've been working on."
    },
    {
        "id": "collaborate-3",
        "category": "collaborate",
        "prompt": "Create a summary of all team meetings this quarter and what we accomplished."
    }
]


def run_single_trial(
    trial_num: int, 
    composer: GPT5ExecutionComposer,
    output_dir: Path,
    verbose: bool = True
) -> Dict[str, Any]:
    """
    Run a single trial of GPT-5 analysis on all 9 prompts.
    
    Args:
        trial_num: Trial number (1, 2, or 3)
        composer: GPT-5 composer instance
        output_dir: Directory to save results
        verbose: Show progress
        
    Returns:
        Trial results dictionary
    """
    print("\n" + "=" * 80)
    print(f"TRIAL {trial_num}/3 - GPT-5 EXECUTION COMPOSITION")
    print("=" * 80)
    print(f"Analyzing {len(HERO_PROMPTS)} hero prompts with OPTIMIZED prompts\n")
    
    all_compositions = []
    successful = 0
    failed = 0
    
    for i, hero in enumerate(HERO_PROMPTS, 1):
        if verbose:
            print(f"\n[Trial {trial_num}] Prompt {i}/{len(HERO_PROMPTS)}: {hero['id']}")
            print(f"  {hero['prompt'][:80]}...")
        
        try:
            composition = composer.compose_execution_plan(
                prompt=hero['prompt'],
                prompt_id=hero['id']
            )
            
            composition['category'] = hero['category']
            composition['trial'] = trial_num
            
            if composition.get('error'):
                print(f"  ❌ Error: {composition['error']}")
                failed += 1
            else:
                task_count = len(composition.get('tasks_covered', []))
                print(f"  ✅ Success! Used {task_count}/24 tasks")
                print(f"     Tasks: {', '.join(composition.get('tasks_covered', []))}")
                successful += 1
            
            all_compositions.append(composition)
            
        except Exception as e:
            print(f"  ❌ Exception: {e}")
            failed += 1
            all_compositions.append({
                "source": "gpt-5",
                "prompt_id": hero['id'],
                "prompt_text": hero['prompt'],
                "category": hero['category'],
                "trial": trial_num,
                "error": str(e),
                "execution_plan": [],
                "tasks_covered": []
            })
        
        # Brief pause between API calls
        if i < len(HERO_PROMPTS):
            time.sleep(1)
    
    # Save trial results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    trial_file = output_dir / f"gpt5_trial{trial_num}_{timestamp}.json"
    
    trial_results = {
        "metadata": {
            "trial": trial_num,
            "source": "gpt-5",
            "model": "dev-gpt-5-chat-jj",
            "model_name": "GPT-5",
            "timestamp": timestamp,
            "total_prompts": len(HERO_PROMPTS),
            "successful": successful,
            "failed": failed,
            "canonical_tasks_version": "2.0",
            "total_canonical_tasks": 24,
            "prompt_optimization": "Optimized November 7, 2025 - Enhanced CAN-07 guidance, specialized task keywords"
        },
        "compositions": all_compositions
    }
    
    with open(trial_file, 'w', encoding='utf-8') as f:
        json.dump(trial_results, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Trial {trial_num} complete: {successful}/{len(HERO_PROMPTS)} successful")
    print(f"💾 Saved to: {trial_file}")
    
    return trial_results


def analyze_stability(trials: List[Dict[str, Any]], output_dir: Path) -> Dict[str, Any]:
    """
    Analyze stability across 3 trials.
    
    Args:
        trials: List of 3 trial result dictionaries
        output_dir: Directory to save analysis
        
    Returns:
        Stability analysis dictionary
    """
    print("\n" + "=" * 80)
    print("STABILITY ANALYSIS - 3 TRIALS")
    print("=" * 80)
    
    # Collect per-prompt task selections
    prompt_tasks = defaultdict(list)  # prompt_id -> [trial1_tasks, trial2_tasks, trial3_tasks]
    
    for trial in trials:
        for comp in trial['compositions']:
            if not comp.get('error'):
                prompt_id = comp['prompt_id']
                tasks = set(comp.get('tasks_covered', []))
                prompt_tasks[prompt_id].append(tasks)
    
    # Compute stability metrics
    stability_analysis = {
        "per_prompt": {},
        "aggregate": {
            "total_prompts": len(HERO_PROMPTS),
            "trials": len(trials),
            "average_task_count": [],
            "task_variance": []
        }
    }
    
    print("\nPER-PROMPT STABILITY:")
    print("-" * 80)
    
    for prompt_id in sorted(prompt_tasks.keys()):
        task_sets = prompt_tasks[prompt_id]
        
        if len(task_sets) != 3:
            print(f"⚠️  {prompt_id}: Only {len(task_sets)}/3 trials successful")
            continue
        
        # Compute intersection (always present) and union (ever present)
        intersection = task_sets[0].intersection(task_sets[1]).intersection(task_sets[2])
        union = task_sets[0].union(task_sets[1]).union(task_sets[2])
        
        # Compute per-trial task counts
        task_counts = [len(ts) for ts in task_sets]
        avg_count = sum(task_counts) / len(task_counts)
        variance = sum((c - avg_count) ** 2 for c in task_counts) / len(task_counts)
        std_dev = variance ** 0.5
        
        # Tasks that vary (in union but not in intersection)
        varying_tasks = union - intersection
        
        # Consistency percentage
        consistency_pct = (len(intersection) / len(union) * 100) if union else 100
        
        stability_analysis["per_prompt"][prompt_id] = {
            "always_selected": sorted(list(intersection)),
            "sometimes_selected": sorted(list(varying_tasks)),
            "task_counts": task_counts,
            "average_task_count": avg_count,
            "std_dev": std_dev,
            "consistency_percentage": consistency_pct
        }
        
        print(f"\n{prompt_id}:")
        print(f"  Task counts: {task_counts[0]}, {task_counts[1]}, {task_counts[2]} (avg: {avg_count:.1f}, std: {std_dev:.2f})")
        print(f"  Consistency: {consistency_pct:.1f}%")
        print(f"  Always selected ({len(intersection)}): {', '.join(sorted(intersection))}")
        if varying_tasks:
            print(f"  ⚠️  Varying ({len(varying_tasks)}): {', '.join(sorted(varying_tasks))}")
    
    # Aggregate stability
    all_task_counts = []
    all_variances = []
    all_consistencies = []
    
    for data in stability_analysis["per_prompt"].values():
        all_task_counts.extend(data["task_counts"])
        all_variances.append(data["std_dev"])
        all_consistencies.append(data["consistency_percentage"])
    
    avg_task_count = sum(all_task_counts) / len(all_task_counts) if all_task_counts else 0
    avg_consistency = sum(all_consistencies) / len(all_consistencies) if all_consistencies else 0
    avg_variance = sum(all_variances) / len(all_variances) if all_variances else 0
    
    stability_analysis["aggregate"] = {
        "average_task_count": avg_task_count,
        "average_consistency": avg_consistency,
        "average_std_dev": avg_variance,
        "interpretation": "High" if avg_consistency >= 90 else "Medium" if avg_consistency >= 75 else "Low"
    }
    
    print("\n" + "=" * 80)
    print("AGGREGATE STABILITY METRICS:")
    print("=" * 80)
    print(f"Average task count: {avg_task_count:.2f} tasks/prompt")
    print(f"Average consistency: {avg_consistency:.1f}%")
    print(f"Average std dev: {avg_variance:.2f} tasks")
    print(f"Stability rating: {stability_analysis['aggregate']['interpretation']}")
    
    # Save analysis
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    analysis_file = output_dir / f"gpt5_stability_analysis_{timestamp}.json"
    
    with open(analysis_file, 'w', encoding='utf-8') as f:
        json.dump(stability_analysis, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Stability analysis saved to: {analysis_file}")
    
    return stability_analysis


def main():
    """Main entry point for stability test"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Run GPT-5 stability test (3 trials) with optimized prompts"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="docs/gutt_analysis/model_comparison/gpt5_stability",
        help="Directory to save results"
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress verbose output"
    )
    
    args = parser.parse_args()
    
    # Create output directory
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("=" * 80)
    print("GPT-5 STABILITY TEST - 3 TRIALS WITH OPTIMIZED PROMPTS")
    print("=" * 80)
    print(f"\nOutput directory: {output_dir}")
    print(f"Prompts: {len(HERO_PROMPTS)}")
    print(f"Trials: 3")
    print(f"Total API calls: {len(HERO_PROMPTS) * 3} (27 calls)")
    print("\nPrompt optimizations:")
    print("  ✅ Enhanced CAN-07 guidance (parent task, metadata extraction)")
    print("  ✅ Specialized task keywords (CAN-18, CAN-20, CAN-23)")
    print("  ✅ Explicit DO/DON'T guidelines")
    print("  ✅ CAN-02A vs CAN-02B differentiation")
    print("  ✅ Dependency chains clarified")
    
    # Initialize composer
    try:
        composer = GPT5ExecutionComposer()
    except Exception as e:
        print(f"\n❌ Failed to initialize GPT-5 composer: {e}")
        return 1
    
    # Run 3 trials
    trials = []
    for trial_num in range(1, 4):
        trial_results = run_single_trial(
            trial_num=trial_num,
            composer=composer,
            output_dir=output_dir,
            verbose=not args.quiet
        )
        trials.append(trial_results)
        
        # Brief pause between trials
        if trial_num < 3:
            print("\nPausing 5 seconds before next trial...")
            time.sleep(5)
    
    # Analyze stability
    stability = analyze_stability(trials, output_dir)
    
    # Print final summary
    print("\n" + "=" * 80)
    print("STABILITY TEST COMPLETE")
    print("=" * 80)
    print(f"\nTrials completed: 3/3")
    print(f"Results saved to: {output_dir}")
    print(f"\nStability rating: {stability['aggregate']['interpretation']}")
    print(f"Average consistency: {stability['aggregate']['average_consistency']:.1f}%")
    print(f"Average task count: {stability['aggregate']['average_task_count']:.2f} tasks/prompt")
    
    print("\n" + "=" * 80)
    print("NEXT STEPS")
    print("=" * 80)
    print("\n1. Compare each trial with gold standard:")
    for i in range(1, 4):
        print(f"   python tools/compare_to_gold.py {output_dir}/gpt5_trial{i}_*.json")
    
    print("\n2. Compute average performance across 3 trials")
    print("\n3. Compare optimized vs original GPT-5 results")
    print("   Original: docs/gutt_analysis/model_comparison/gpt5_compositions_20251107_014703.json")
    print(f"   Optimized: {output_dir}/gpt5_trial*_*.json")
    
    print("\n" + "=" * 80)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
